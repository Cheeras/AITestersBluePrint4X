from __future__ import annotations


def render_test_plan(plan: dict) -> str:
    lines = [
        f"# {plan['title']}",
        "",
        f"**Source Jira:** `{plan['source_issue_key']}`  ",
        f"**Schema:** `{plan['schema_version']}`  ",
        f"**Source references:** {_refs(plan['source_references'])}",
        "",
        "## Objective",
        "",
        plan["objective"],
    ]
    _list_section(lines, "Scope", plan["scope"])
    _subsection(lines, "Assumptions", plan["assumptions"])
    _subsection(lines, "Clarification Questions", plan["clarification_questions"])
    _list_section(lines, "Inclusion", plan["inclusion"])
    _list_section(lines, "Test Environment", plan["test_environment"])
    _list_section(lines, "Defect Reporting Procedure", plan["defect_reporting_procedure"])
    _list_section(lines, "Test Strategy", plan["test_strategy"])
    _list_section(lines, "Test Schedule", plan["test_schedule"])
    _list_section(lines, "Test Deliverables", plan["test_deliverables"])

    lines.extend(["", "## Entry and Exit Criteria", ""])
    _subsection(lines, "Entry Criteria", plan["entry_and_exit_criteria"]["entry"])
    _subsection(lines, "Exit Criteria", plan["entry_and_exit_criteria"]["exit"])

    _list_section(lines, "Test Execution", plan["test_execution"])
    _list_section(lines, "Test Closure", plan["test_closure"])
    _list_section(lines, "Tools", plan["tools"])

    lines.extend(["", "## Risks and Mitigations", ""])
    lines.extend(["| ID | Risk | Impact | Mitigation | Sources |", "|---|---|---|---|---|"])
    for item in plan["risks_and_mitigations"]:
        lines.append(
            f"| {_cell(item['id'])} | {_cell(item['risk'])} | {_cell(item['impact'])} | "
            f"{_cell(item['mitigation'])} | {_cell(_refs(item['source_refs']))} |"
        )

    _list_section(lines, "Approvals", plan["approvals"])
    if plan["generation_warnings"]:
        _subsection(lines, "Generation Warnings", plan["generation_warnings"])
    return "\n".join(lines).strip() + "\n"


def _list_section(lines: list[str], heading: str, items: list[str]):
    lines.extend(["", f"## {heading}", ""])
    lines.extend(_bullets(items))


def _subsection(lines: list[str], heading: str, items: list[str]):
    lines.extend(["", f"### {heading}", ""])
    lines.extend(_bullets(items))


def _bullets(items: list[str]) -> list[str]:
    return [f"- {item}" for item in items]


def _refs(items: list[str]) -> str:
    return ", ".join(f"`{item}`" for item in items)


def _cell(value) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")
