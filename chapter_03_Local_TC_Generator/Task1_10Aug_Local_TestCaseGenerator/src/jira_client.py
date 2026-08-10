"""JIRA REST API client — fetches requirements from JIRA issues."""
import os
from atlassian import Jira
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))


class JIRAClient:
    """Wraps Atlassian JIRA REST API for fetching issue requirements."""

    def __init__(self, url=None, email=None, api_token=None):
        self.url = url or os.getenv("JIRA_URL")
        self.email = email or os.getenv("JIRA_EMAIL")
        self.api_token = api_token or os.getenv("JIRA_API_TOKEN")
        self._jira = None

    def _connect(self):
        if self._jira is None:
            if not all([self.url, self.email, self.api_token]):
                raise ValueError(
                    "JIRA credentials not configured. "
                    "Set JIRA_URL, JIRA_EMAIL, JIRA_API_TOKEN in .env"
                )
            self._jira = Jira(
                url=self.url,
                username=self.email,
                password=self.api_token,
                cloud=True,
            )
        return self._jira

    def fetch_issue(self, issue_key: str) -> dict:
        """Fetch a single JIRA issue by key (e.g. PROJ-42)."""
        jira = self._connect()
        issue = jira.issue(issue_key)
        return issue

    def extract_requirements(self, issue: dict) -> str:
        """Extract description and acceptance criteria from an issue."""
        fields = issue.get("fields", {})
        parts = []

        summary = fields.get("summary", "")
        if summary:
            parts.append(f"## Summary\n{summary}")

        description = fields.get("description", "")
        if description:
            parts.append(f"## Description\n{description}")

        # Try to extract acceptance criteria
        custom_fields = fields.copy()
        for key, value in custom_fields.items():
            if "acceptance" in str(key).lower() and value:
                parts.append(f"## Acceptance Criteria\n{value}")
                break

        return "\n\n".join(parts) if parts else "No requirements found in issue."

    def test_connection(self) -> bool:
        """Verify JIRA connectivity and credentials."""
        try:
            jira = self._connect()
            jira.myself()
            return True
        except Exception:
            return False