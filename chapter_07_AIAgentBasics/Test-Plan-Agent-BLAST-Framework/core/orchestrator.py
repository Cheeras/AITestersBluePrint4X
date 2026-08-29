from __future__ import annotations

from pathlib import Path

from core.errors import AppError
from core.renderer import render_test_plan
from core.schemas import extract_issue_key
from core.settings import SettingsStore
from tools.jira_client import JiraClient
from tools.openrouter_client import OpenRouterClient


class TestPlanOrchestrator:
    def __init__(
        self, settings_store: SettingsStore, output_dir: Path,
        jira_factory=JiraClient, llm_factory=OpenRouterClient,
    ):
        self.settings_store = settings_store
        self.output_dir = output_dir
        self.jira_factory = jira_factory
        self.llm_factory = llm_factory

    def test_jira(self) -> dict:
        settings = self.settings_store.load()
        return self.jira_factory(settings).test_connection()

    def test_openrouter(self) -> dict:
        settings = self.settings_store.load()
        return self.llm_factory(settings.openrouter_api_key).test_connection()

    def generate(self, prompt: str) -> dict:
        issue_key = extract_issue_key(prompt)
        settings = self.settings_store.load()
        missing = settings.missing_for_generation()
        if missing:
            raise AppError("CONFIGURATION_MISSING", f"Configure {', '.join(missing)} in Settings before generating.")

        context = self.jira_factory(settings).fetch_issue_context(issue_key)
        plan = self.llm_factory(settings.openrouter_api_key).generate_test_plan(context, prompt)
        markdown = render_test_plan(plan)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        output_path = self.output_dir / f"{issue_key}-test-plan.md"
        temporary = output_path.with_suffix(".tmp")
        try:
            temporary.write_text(markdown, encoding="utf-8")
            temporary.replace(output_path)
        except OSError as exc:
            raise AppError("OUTPUT_WRITE_FAILED", "The generated test plan could not be saved locally.", 500) from exc

        warnings = list(context.get("retrieval", {}).get("warnings", [])) + list(plan.get("generation_warnings", []))
        return {
            "ok": True,
            "issue_key": issue_key,
            "markdown": markdown,
            "saved_to": f".tmp/output/{output_path.name}",
            "warnings": warnings,
        }
