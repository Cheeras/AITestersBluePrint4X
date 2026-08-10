"""Formats LLM outputs into clean Markdown test-case tables and saves them."""
import os
import re
from datetime import datetime

OUTPUT_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "output"
)


def save_to_file(content: str, filename: str = None) -> str:
    """Save generated test cases to a timestamped .md file."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"testcases_{timestamp}.md"
    filepath = os.path.join(OUTPUT_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    return filepath


def strip_llm_noise(raw: str) -> str:
    """
    Remove common LLM preamble/blabber before the table.
    Returns the portion starting from the first markdown table header.
    """
    # Try to find the pipe-delimited table
    lines = raw.split("\n")
    start = 0
    for i, line in enumerate(lines):
        if line.strip().startswith("| Test") or line.strip().startswith("|Test"):
            start = i
            break
    return "\n".join(lines[start:]) if start else raw


def validate_test_cases(text: str) -> bool:
    """Check that the output contains at least a table with expected columns."""
    required = ["Test ID", "Description", "Steps", "Expected Result"]
    return all(col.lower() in text.lower() for col in required)


def format_test_cases(raw_response: str, feature: str = "") -> str:
    """
    Take raw LLM response, clean it, add a title, validate it.
    Returns a polished Markdown string ready to display or save.
    """
    title = f"# Generated Test Cases — {feature}\n\n" if feature else "# Generated Test Cases\n\n"
    body = strip_llm_noise(raw_response)

    if not validate_test_cases(body):
        title += (
            "> ⚠️ The generated output may not contain all required columns. "
            "Please review manually.\n\n"
        )

    return title + body