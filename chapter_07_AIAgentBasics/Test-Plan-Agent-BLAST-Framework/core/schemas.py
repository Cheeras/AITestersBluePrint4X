from __future__ import annotations

import re

from core.errors import AppError


ISSUE_KEY_PATTERN = re.compile(r"(?<![A-Z0-9_])([A-Z][A-Z0-9_]{1,9}-[1-9][0-9]*)(?![A-Z0-9_])")


def _string() -> dict:
    return {"type": "string", "minLength": 1}


def _strings() -> dict:
    return {"type": "array", "minItems": 1, "items": _string()}


def _object(required: list[str], properties: dict) -> dict:
    return {"type": "object", "additionalProperties": False, "required": required, "properties": properties}


def extract_issue_key(prompt: str) -> str:
    if not isinstance(prompt, str) or not prompt.strip():
        raise AppError("INVALID_PROMPT", "Enter a prompt containing one Jira issue key, for example PROJ-123.")
    keys = list(dict.fromkeys(ISSUE_KEY_PATTERN.findall(prompt.upper())))
    if len(keys) != 1:
        raise AppError("INVALID_PROMPT", "Provide exactly one Jira issue key, for example PROJ-123.")
    return keys[0]


PLAN_LIST_FIELDS = [
    "scope",
    "inclusion",
    "test_environment",
    "defect_reporting_procedure",
    "test_strategy",
    "test_schedule",
    "test_deliverables",
    "test_execution",
    "test_closure",
    "tools",
    "approvals",
    "assumptions",
    "clarification_questions",
]


MODEL_TEST_PLAN_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["objective", *PLAN_LIST_FIELDS, "entry_and_exit_criteria", "risks_and_mitigations"],
    "properties": {
        "objective": _string(),
        **{field: _strings() for field in PLAN_LIST_FIELDS},
        "entry_and_exit_criteria": _object(["entry", "exit"], {"entry": _strings(), "exit": _strings()}),
        "risks_and_mitigations": {
            "type": "array",
            "minItems": 1,
            "items": _object(
                ["risk", "impact", "mitigation", "source_refs"],
                {"risk": _string(), "impact": _string(), "mitigation": _string(), "source_refs": _strings()},
            ),
        },
    },
}


TEST_PLAN_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": [
        "schema_version", "source_issue_key", "title", "objective", *PLAN_LIST_FIELDS,
        "entry_and_exit_criteria", "risks_and_mitigations", "source_references", "generation_warnings",
    ],
    "properties": {
        "schema_version": _string(),
        "source_issue_key": _string(),
        "title": _string(),
        "objective": _string(),
        **{field: _strings() for field in PLAN_LIST_FIELDS},
        "entry_and_exit_criteria": _object(["entry", "exit"], {"entry": _strings(), "exit": _strings()}),
        "risks_and_mitigations": {
            "type": "array",
            "minItems": 1,
            "items": _object(
                ["id", "risk", "impact", "mitigation", "source_refs"],
                {
                    "id": _string(), "risk": _string(), "impact": _string(),
                    "mitigation": _string(), "source_refs": _strings(),
                },
            ),
        },
        "source_references": _strings(),
        "generation_warnings": {"type": "array", "items": {"type": "string"}},
    },
}


def complete_test_plan(plan: object, context: dict | None = None) -> dict:
    if not isinstance(plan, dict):
        raise AppError("INVALID_MODEL_OUTPUT", "The model returned an invalid test-plan object.", 502)

    context = context or {}
    issue = context.get("issue") if isinstance(context.get("issue"), dict) else {}
    issue_key = str(issue.get("key") or plan.get("source_issue_key") or "UNKNOWN")
    result = {key: value for key, value in plan.items() if key in MODEL_TEST_PLAN_SCHEMA["properties"]}
    recovered: list[str] = []

    result["schema_version"] = "2.0"
    result["source_issue_key"] = issue_key
    result["title"] = f"Test Plan for {issue_key}"
    if not isinstance(result.get("objective"), str) or not result["objective"].strip():
        result["objective"] = f"Define and govern validation of the requirements documented in {issue_key}."
        recovered.append("objective")

    defaults = {
        "scope": "Scope details are not specified in Jira; confirm them during test-plan review.",
        "inclusion": "Included product behavior is not fully specified in Jira; confirm it before execution.",
        "test_environment": "The test environment is not specified in Jira; the QA owner must confirm it.",
        "defect_reporting_procedure": "Use the team's approved defect workflow; severity, ownership, and evidence requirements require confirmation.",
        "test_strategy": "Use a risk-based strategy derived from the available Jira requirements and clearly recorded assumptions.",
        "test_schedule": "Dates are not specified in Jira; schedule planning depends on build and environment readiness.",
        "test_deliverables": "Provide this approved test plan, execution evidence, defect reports, and a closure summary.",
        "test_execution": "Execute according to the approved strategy and record results and evidence in the team's agreed system.",
        "test_closure": "Close testing after exit criteria are met, residual risks are accepted, and results are summarized.",
        "tools": "Required tools are not specified in Jira; confirm the approved test-management and defect-tracking tools.",
        "approvals": "QA lead, product owner, and engineering owner approval status is pending confirmation.",
        "assumptions": "No unstated requirement is treated as a Jira fact; review all planning assumptions before execution.",
        "clarification_questions": "Confirm missing scope, environment, schedule, ownership, and approval details before execution.",
    }
    for field, fallback in defaults.items():
        value = result.get(field)
        if not isinstance(value, list) or not any(isinstance(item, str) and item.strip() for item in value):
            result[field] = [fallback]
            recovered.append(field)
        else:
            result[field] = [item.strip() for item in value if isinstance(item, str) and item.strip()]

    criteria = result.get("entry_and_exit_criteria")
    if not isinstance(criteria, dict):
        criteria = {}
    entry = _clean_strings(criteria.get("entry"))
    exit_items = _clean_strings(criteria.get("exit"))
    if not entry:
        entry = ["Requirements, build, environment, data, and responsible owners are ready and approved."]
        recovered.append("entry_and_exit_criteria.entry")
    if not exit_items:
        exit_items = ["Agreed coverage is complete, blocking defects are resolved or accepted, and closure is approved."]
        recovered.append("entry_and_exit_criteria.exit")
    result["entry_and_exit_criteria"] = {"entry": entry, "exit": exit_items}

    raw_risks = result.get("risks_and_mitigations")
    risks: list[dict] = []
    if isinstance(raw_risks, list):
        for item in raw_risks:
            if not isinstance(item, dict):
                continue
            risk = str(item.get("risk") or "").strip()
            impact = str(item.get("impact") or "").strip()
            mitigation = str(item.get("mitigation") or "").strip()
            if not risk or not impact or not mitigation:
                continue
            risks.append({
                "id": f"RISK-{len(risks) + 1:03d}",
                "risk": risk,
                "impact": impact,
                "mitigation": mitigation,
                "source_refs": _clean_strings(item.get("source_refs")) or [f"issue:{issue_key}"],
            })
    if not risks:
        risks = [{
            "id": "RISK-001",
            "risk": "Incomplete Jira planning information may cause coverage, scheduling, or ownership gaps.",
            "impact": "Testing may be delayed or important product risks may remain unassessed.",
            "mitigation": "Resolve the recorded clarification questions and obtain plan approval before execution.",
            "source_refs": [f"issue:{issue_key}"],
        }]
        recovered.append("risks_and_mitigations")
    result["risks_and_mitigations"] = risks

    source_refs = {f"issue:{issue_key}"}
    for risk in risks:
        source_refs.update(risk["source_refs"])
    result["source_references"] = sorted(source_refs)
    warnings = [str(item) for item in context.get("retrieval", {}).get("warnings", []) if item]
    warnings.extend(f"Model omitted or invalidated {field}; added an explicit review placeholder." for field in recovered)
    result["generation_warnings"] = list(dict.fromkeys(warnings))
    return result


def validate_test_plan(plan: object, expected_issue_key: str) -> dict:
    if not isinstance(plan, dict):
        raise AppError("INVALID_MODEL_OUTPUT", "The model returned an invalid test-plan object.", 502)
    missing = [key for key in TEST_PLAN_SCHEMA["required"] if key not in plan]
    if missing:
        raise AppError("INVALID_MODEL_OUTPUT", f"Model output is missing required sections: {', '.join(missing)}.", 502)
    extras = set(plan) - set(TEST_PLAN_SCHEMA["properties"])
    if extras:
        raise AppError("INVALID_MODEL_OUTPUT", f"Model output contains unsupported sections: {', '.join(sorted(extras))}.", 502)
    if plan.get("source_issue_key") != expected_issue_key:
        raise AppError("INVALID_MODEL_OUTPUT", "Model output does not reference the requested Jira issue.", 502)
    if not isinstance(plan.get("objective"), str) or not plan["objective"].strip():
        raise AppError("INVALID_MODEL_OUTPUT", "The test plan objective is empty.", 502)

    for field in PLAN_LIST_FIELDS + ["source_references"]:
        value = plan.get(field)
        if not isinstance(value, list) or not value or any(not isinstance(item, str) or not item.strip() for item in value):
            raise AppError("INVALID_MODEL_OUTPUT", f"The test plan section {field} is invalid or empty.", 502)
    if not isinstance(plan.get("generation_warnings"), list):
        raise AppError("INVALID_MODEL_OUTPUT", "Generation warnings must be a list.", 502)

    criteria = plan.get("entry_and_exit_criteria")
    if not isinstance(criteria, dict) or set(criteria) != {"entry", "exit"}:
        raise AppError("INVALID_MODEL_OUTPUT", "Entry and exit criteria are invalid.", 502)
    for field in ("entry", "exit"):
        value = criteria[field]
        if not isinstance(value, list) or not value or any(not isinstance(item, str) or not item.strip() for item in value):
            raise AppError("INVALID_MODEL_OUTPUT", f"The {field} criteria are invalid or empty.", 502)

    risks = plan.get("risks_and_mitigations")
    if not isinstance(risks, list) or not risks:
        raise AppError("INVALID_MODEL_OUTPUT", "Risks and mitigations are required.", 502)
    ids: list[str] = []
    for item in risks:
        if not isinstance(item, dict):
            raise AppError("INVALID_MODEL_OUTPUT", "A risk and mitigation entry is invalid.", 502)
        if any(not isinstance(item.get(field), str) or not item[field].strip() for field in ("id", "risk", "impact", "mitigation")):
            raise AppError("INVALID_MODEL_OUTPUT", "Every risk needs an ID, impact, and mitigation.", 502)
        if not isinstance(item.get("source_refs"), list) or not item["source_refs"]:
            raise AppError("INVALID_MODEL_OUTPUT", "Every risk needs at least one source reference.", 502)
        ids.append(item["id"])
    if len(ids) != len(set(ids)):
        raise AppError("INVALID_MODEL_OUTPUT", "Risk IDs must be unique.", 502)
    if _contains_non_english_letters(plan):
        raise AppError(
            "NON_ENGLISH_MODEL_OUTPUT",
            "OpenRouter generated non-English test-plan content. Regenerate the plan in English.",
            502,
        )
    return plan


def _clean_strings(value: object) -> list[str]:
    if not isinstance(value, list):
        return []
    return [item.strip() for item in value if isinstance(item, str) and item.strip()]


def _contains_non_english_letters(value: object) -> bool:
    if isinstance(value, str):
        return any(character.isalpha() and ord(character) > 127 for character in value)
    if isinstance(value, dict):
        return any(_contains_non_english_letters(item) for item in value.values())
    if isinstance(value, list):
        return any(_contains_non_english_letters(item) for item in value)
    return False
