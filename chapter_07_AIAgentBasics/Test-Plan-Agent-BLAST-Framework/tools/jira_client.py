from __future__ import annotations

import base64
import time
from urllib.parse import quote, urlencode

from core.errors import AppError
from core.settings import Settings
from tools.http_transport import TransportError, UrlLibTransport


CORE_FIELDS = [
    "summary", "description", "issuetype", "status", "priority", "labels", "components",
    "assignee", "reporter", "parent", "subtasks", "issuelinks", "attachment",
]


class JiraClient:
    def __init__(self, settings: Settings, transport=None, retries: int = 2):
        self.settings = settings
        self.transport = transport or UrlLibTransport()
        self.retries = retries

    @property
    def headers(self) -> dict[str, str]:
        token = base64.b64encode(f"{self.settings.jira_email}:{self.settings.jira_token}".encode()).decode()
        return {"Accept": "application/json", "Authorization": f"Basic {token}"}

    def test_connection(self) -> dict:
        self._require_settings()
        data = self._get("/rest/api/3/myself")
        return {
            "ok": True,
            "service": "jira",
            "message": "Jira connection succeeded.",
            "account": data.get("displayName") or data.get("accountId") or "Authenticated account",
        }

    def fetch_issue_context(self, issue_key: str) -> dict:
        self._require_settings()
        field_metadata = self._get("/rest/api/3/field")
        acceptance_fields = [
            item for item in field_metadata
            if isinstance(item, dict) and _is_acceptance_field(item.get("name", "")) and item.get("id")
        ]
        fields = CORE_FIELDS + [item["id"] for item in acceptance_fields]
        query = urlencode({"fields": ",".join(fields)})
        issue = self._get(f"/rest/api/3/issue/{quote(issue_key)}?{query}")
        comments = self._fetch_comments(issue_key)
        return normalize_issue(issue, comments, acceptance_fields)

    def _fetch_comments(self, issue_key: str) -> list[dict]:
        comments: list[dict] = []
        start_at = 0
        page_size = 100
        for _ in range(10):
            page = self._get(
                f"/rest/api/3/issue/{quote(issue_key)}/comment?{urlencode({'startAt': start_at, 'maxResults': page_size})}"
            )
            values = page.get("comments", [])
            if not isinstance(values, list):
                raise AppError("JIRA_INVALID_RESPONSE", "Jira returned an invalid comments response.", 502)
            comments.extend(values)
            total = int(page.get("total", len(comments)))
            if len(comments) >= total or not values:
                return comments
            start_at += len(values)
        raise AppError("JIRA_PAGINATION_LIMIT", "Jira comments exceeded the configured retrieval limit.", 502)

    def _get(self, path: str):
        url = f"{self.settings.jira_url}{path}"
        response = None
        for attempt in range(self.retries + 1):
            try:
                response = self.transport.request("GET", url, headers=self.headers, timeout=20)
            except TransportError as exc:
                if attempt < self.retries:
                    time.sleep(0.15 * (attempt + 1))
                    continue
                raise AppError("JIRA_UNREACHABLE", "Jira could not be reached. Check the URL and network.", 502) from exc
            if response.status == 429 or 500 <= response.status <= 599:
                if attempt < self.retries:
                    time.sleep(0.15 * (attempt + 1))
                    continue
            break
        if response is None:
            raise AppError("JIRA_UNREACHABLE", "Jira could not be reached.", 502)
        _raise_jira_status(response.status)
        try:
            return response.json()
        except (UnicodeDecodeError, ValueError) as exc:
            raise AppError("JIRA_INVALID_RESPONSE", "Jira returned malformed JSON.", 502) from exc

    def _require_settings(self):
        missing = self.settings.missing_for_jira()
        if missing:
            raise AppError("CONFIGURATION_MISSING", f"Configure {', '.join(missing)} in Settings.")


def _raise_jira_status(status: int):
    if 200 <= status <= 299:
        return
    messages = {
        400: ("JIRA_BAD_REQUEST", "Jira rejected the request. Verify the issue key and site configuration.", 400),
        401: ("JIRA_AUTHENTICATION_FAILED", "Jira authentication failed. Check the email and API token.", 401),
        403: ("JIRA_AUTHORIZATION_FAILED", "The Jira account is not allowed to access this resource.", 403),
        404: ("JIRA_NOT_FOUND", "The Jira issue or endpoint was not found or is not accessible.", 404),
        429: ("JIRA_RATE_LIMITED", "Jira rate-limited the request. Try again later.", 429),
    }
    code, message, app_status = messages.get(status, ("JIRA_ERROR", "Jira returned an unexpected error.", 502))
    raise AppError(code, message, app_status)


def _is_acceptance_field(name: str) -> bool:
    normalized = " ".join(str(name).lower().replace("_", " ").split())
    return "acceptance criteria" in normalized or "acceptance criterion" in normalized


def adf_to_text(value) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, list):
        return "\n".join(filter(None, (adf_to_text(item) for item in value))).strip()
    if not isinstance(value, dict):
        return str(value).strip()
    node_type = value.get("type")
    if node_type == "text":
        return str(value.get("text", ""))
    if node_type == "hardBreak":
        return "\n"
    content = value.get("content", [])
    joined = "".join(adf_to_text(item) for item in content)
    if node_type in {"doc", "paragraph", "heading", "blockquote", "listItem", "bulletList", "orderedList", "table", "tableRow"}:
        return joined.strip() + ("\n" if joined.strip() else "")
    return joined.strip()


def normalize_issue(issue: dict, comments: list[dict], acceptance_fields: list[dict]) -> dict:
    fields = issue.get("fields") if isinstance(issue, dict) else None
    if not isinstance(fields, dict) or not issue.get("key"):
        raise AppError("JIRA_INVALID_RESPONSE", "Jira returned an invalid issue response.", 502)

    acceptance_values = []
    for metadata in acceptance_fields:
        value = adf_to_text(fields.get(metadata["id"]))
        if value:
            acceptance_values.append({"field_id": metadata["id"], "field_name": metadata.get("name", ""), "text": value})

    warnings = []
    if not acceptance_fields:
        warnings.append("No acceptance-criteria field was discovered by name.")
    elif not acceptance_values:
        warnings.append("Acceptance-criteria fields were discovered but contain no readable value.")

    return {
        "schema_version": "1.0",
        "issue": {
            "key": issue["key"],
            "summary": fields.get("summary") or "",
            "description": adf_to_text(fields.get("description")),
            "issue_type": _name(fields.get("issuetype")),
            "status": _name(fields.get("status")),
            "priority": _name(fields.get("priority")),
            "labels": fields.get("labels") or [],
            "components": [_name(item) for item in fields.get("components") or []],
            "assignee_display_name": _display_name(fields.get("assignee")),
            "reporter_display_name": _display_name(fields.get("reporter")),
        },
        "acceptance_criteria": acceptance_values,
        "comments": [
            {
                "id": str(item.get("id", "")),
                "body": adf_to_text(item.get("body")),
                "created_at": item.get("created"),
                "updated_at": item.get("updated"),
            }
            for item in comments if isinstance(item, dict)
        ],
        "issue_links": _normalize_links(fields.get("issuelinks") or []),
        "parent": _issue_ref(fields.get("parent")),
        "subtasks": [_issue_ref(item) for item in fields.get("subtasks") or [] if _issue_ref(item)],
        "attachments": [
            {
                "id": str(item.get("id", "")),
                "filename": item.get("filename", ""),
                "media_type": item.get("mimeType", ""),
                "size_bytes": item.get("size", 0),
            }
            for item in fields.get("attachment") or [] if isinstance(item, dict)
        ],
        "retrieval": {"complete": True, "warnings": warnings},
    }


def _name(value) -> str:
    return value.get("name", "") if isinstance(value, dict) else ""


def _display_name(value):
    return value.get("displayName") if isinstance(value, dict) else None


def _issue_ref(value):
    if not isinstance(value, dict) or not value.get("key"):
        return None
    return {"key": value["key"], "summary": (value.get("fields") or {}).get("summary", "")}


def _normalize_links(links: list) -> list[dict]:
    normalized = []
    for link in links:
        if not isinstance(link, dict):
            continue
        link_type = link.get("type") or {}
        outward = link.get("outwardIssue")
        inward = link.get("inwardIssue")
        if outward:
            ref = _issue_ref(outward)
            if ref:
                normalized.append({"relationship": link_type.get("outward", "relates to"), **ref})
        if inward:
            ref = _issue_ref(inward)
            if ref:
                normalized.append({"relationship": link_type.get("inward", "relates to"), **ref})
    return normalized
