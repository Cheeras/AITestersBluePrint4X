import json
import tempfile
import unittest
from pathlib import Path

from core.errors import AppError
from core.orchestrator import TestPlanOrchestrator
from core.renderer import render_test_plan
from core.schemas import MODEL_TEST_PLAN_SCHEMA, TEST_PLAN_SCHEMA, complete_test_plan, extract_issue_key, validate_test_plan
from core.settings import Settings, SettingsStore
from tools.http_transport import HttpResponse
from tools.jira_client import JiraClient, adf_to_text
from tools.openrouter_client import OPENROUTER_MODEL, OpenRouterClient


class FakeTransport:
    def __init__(self, responses):
        self.responses = list(responses)
        self.calls = []

    def request(self, method, url, headers=None, json_body=None, timeout=20):
        self.calls.append({"method": method, "url": url, "headers": headers or {}, "json_body": json_body})
        if not self.responses:
            raise AssertionError("Unexpected HTTP request")
        response = self.responses.pop(0)
        return response if isinstance(response, HttpResponse) else json_response(200, response)


def json_response(status, payload):
    return HttpResponse(status, json.dumps(payload).encode("utf-8"), {})


def model_plan(issue_key="PROJ-123"):
    return {
        "objective": "Define the validation approach for the requested behavior.",
        "scope": ["Validate the Jira story at a plan and governance level."],
        "inclusion": ["Functional behavior described by the Jira issue."],
        "test_environment": ["QA environment with a release-candidate build."],
        "defect_reporting_procedure": ["Log defects in Jira with severity, evidence, and reproduction context."],
        "test_strategy": ["Use risk-based functional, integration, security, and accessibility planning where relevant."],
        "test_schedule": ["Begin after entry criteria are met and complete before release approval."],
        "test_deliverables": ["Approved test plan", "Execution summary", "Defect report", "Closure report"],
        "entry_and_exit_criteria": {
            "entry": ["Requirements and build are ready."],
            "exit": ["Exit criteria are met and residual risks are approved."],
        },
        "test_execution": ["Track execution progress and evidence against the approved plan."],
        "test_closure": ["Summarize results, open risks, lessons, and approval decisions."],
        "tools": ["Jira for source requirements and defect reporting."],
        "risks_and_mitigations": [{
            "risk": "Requirements may be incomplete.",
            "impact": "Coverage decisions may be delayed.",
            "mitigation": "Resolve clarification questions before execution.",
            "source_refs": [f"issue:{issue_key}"],
        }],
        "approvals": ["QA lead, product owner, and engineering owner approval required."],
        "assumptions": ["Environment and ownership details require confirmation when absent from Jira."],
        "clarification_questions": ["Confirm dates, owners, environments, and approval workflow."],
    }


def sample_plan(issue_key="PROJ-123"):
    return complete_test_plan(
        model_plan(issue_key),
        {"issue": {"key": issue_key, "summary": "Example story"}, "retrieval": {"warnings": []}},
    )


class SchemaTests(unittest.TestCase):
    def test_extracts_one_issue_key_case_insensitively(self):
        self.assertEqual(extract_issue_key("fetch jira proj-123 and create a plan"), "PROJ-123")

    def test_rejects_missing_or_multiple_issue_keys(self):
        with self.assertRaises(AppError):
            extract_issue_key("create a plan")
        with self.assertRaises(AppError):
            extract_issue_key("compare ABC-1 and XYZ-2")

    def test_schemas_are_strict_and_exclude_test_case_content(self):
        self.assertFalse(TEST_PLAN_SCHEMA["additionalProperties"])
        self.assertFalse(MODEL_TEST_PLAN_SCHEMA["additionalProperties"])
        for forbidden in ("scenarios", "test_cases", "steps", "automation_candidates"):
            self.assertNotIn(forbidden, TEST_PLAN_SCHEMA["properties"])
            self.assertNotIn(forbidden, MODEL_TEST_PLAN_SCHEMA["properties"])
        validate_test_plan(sample_plan(), "PROJ-123")

    def test_deterministic_completion_builds_metadata_and_risk_ids(self):
        context = {
            "issue": {"key": "PROJ-123", "summary": "Example story"},
            "retrieval": {"warnings": ["Acceptance criteria were missing."]},
        }
        completed = complete_test_plan(model_plan(), context)
        self.assertEqual(completed["title"], "Test Plan for PROJ-123")
        self.assertEqual(completed["risks_and_mitigations"][0]["id"], "RISK-001")
        self.assertEqual(completed["generation_warnings"], ["Acceptance criteria were missing."])
        self.assertEqual(completed["source_references"], ["issue:PROJ-123"])
        validate_test_plan(completed, "PROJ-123")

    def test_completion_recovers_missing_plan_sections_with_disclosed_placeholders(self):
        context = {"issue": {"key": "PROJ-123", "summary": "Example story"}, "retrieval": {"warnings": []}}
        completed = complete_test_plan({"objective": "Validate the story."}, context)
        self.assertTrue(completed["test_schedule"])
        self.assertTrue(completed["approvals"])
        self.assertTrue(completed["entry_and_exit_criteria"]["entry"])
        self.assertTrue(any("test_schedule" in warning for warning in completed["generation_warnings"]))
        validate_test_plan(completed, "PROJ-123")

    def test_validation_rejects_empty_required_plan_section(self):
        plan = sample_plan()
        plan["test_execution"] = []
        with self.assertRaises(AppError):
            validate_test_plan(plan, "PROJ-123")

    def test_validation_rejects_legacy_test_cases(self):
        plan = sample_plan()
        plan["test_cases"] = [{"id": "TC-001"}]
        with self.assertRaises(AppError) as caught:
            validate_test_plan(plan, "PROJ-123")
        self.assertIn("unsupported sections", caught.exception.message)

    def test_validation_rejects_non_english_output(self):
        plan = sample_plan()
        plan["clarification_questions"] = ["请确认测试环境。"]
        with self.assertRaises(AppError) as caught:
            validate_test_plan(plan, "PROJ-123")
        self.assertEqual(caught.exception.code, "NON_ENGLISH_MODEL_OUTPUT")


class SettingsTests(unittest.TestCase):
    def test_settings_save_masks_secrets_and_blank_updates_retain_them(self):
        with tempfile.TemporaryDirectory() as directory:
            store = SettingsStore(Path(directory) / "settings.json")
            view = store.save({
                "jira_url": "https://example.atlassian.net/", "jira_email": "qa@example.com",
                "jira_token": "jira-secret", "openrouter_api_key": "router-secret",
            })
            self.assertNotIn("jira_token", view)
            self.assertNotIn("openrouter_api_key", view)
            self.assertTrue(view["jira_token_configured"])
            store.save({"jira_url": "https://example.atlassian.net", "jira_email": "qa@example.com", "jira_token": "", "openrouter_api_key": ""})
            self.assertEqual(store.load().jira_token, "jira-secret")

    def test_settings_require_https_jira_url(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(AppError):
                SettingsStore(Path(directory) / "settings.json").save({"jira_url": "http://example.test"})


class JiraTests(unittest.TestCase):
    def test_adf_normalization(self):
        adf = {"type": "doc", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Hello"}, {"type": "hardBreak"}, {"type": "text", "text": "world"}]}]}
        self.assertEqual(adf_to_text(adf).strip(), "Hello\nworld")

    def test_connection_and_full_read_only_retrieval(self):
        settings = Settings("https://example.atlassian.net", "qa@example.com", "token", "router")
        issue = {
            "key": "PROJ-123",
            "fields": {
                "summary": "Add checkout", "description": {"type": "doc", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Checkout story"}]}]},
                "issuetype": {"name": "Story"}, "status": {"name": "Open"}, "priority": {"name": "High"},
                "labels": ["checkout"], "components": [{"name": "Web"}], "assignee": None, "reporter": None,
                "parent": None, "subtasks": [], "issuelinks": [], "attachment": [],
                "customfield_101": "Given valid payment, complete checkout",
            },
        }
        transport = FakeTransport([
            {"displayName": "QA User"},
            [{"id": "customfield_101", "name": "Acceptance Criteria"}],
            issue,
            {"startAt": 0, "maxResults": 100, "total": 1, "comments": [{"id": "1", "body": "Review edge cases", "created": "now", "updated": "now"}]},
        ])
        client = JiraClient(settings, transport=transport, retries=0)
        self.assertTrue(client.test_connection()["ok"])
        context = client.fetch_issue_context("PROJ-123")
        self.assertEqual(context["acceptance_criteria"][0]["field_id"], "customfield_101")
        self.assertEqual(context["comments"][0]["body"], "Review edge cases")
        self.assertTrue(all(call["method"] == "GET" for call in transport.calls))
        self.assertTrue(all("token" not in call["url"] for call in transport.calls))

    def test_authentication_error_is_safe(self):
        settings = Settings("https://example.atlassian.net", "qa@example.com", "secret-token", "")
        client = JiraClient(settings, transport=FakeTransport([json_response(401, {"error": "raw response"})]), retries=0)
        with self.assertRaises(AppError) as caught:
            client.test_connection()
        self.assertEqual(caught.exception.code, "JIRA_AUTHENTICATION_FAILED")
        self.assertNotIn("secret-token", caught.exception.message)


class OpenRouterTests(unittest.TestCase):
    def test_connection_confirms_requested_model_with_minimal_inference(self):
        transport = FakeTransport([{"model": OPENROUTER_MODEL, "choices": [{"message": {"content": "OK"}, "finish_reason": "stop"}]}])
        result = OpenRouterClient("router-key", transport=transport, retries=0).test_connection()
        self.assertEqual(result["model"], OPENROUTER_MODEL)
        self.assertEqual(transport.calls[0]["method"], "POST")
        self.assertTrue(transport.calls[0]["url"].endswith("/chat/completions"))
        self.assertEqual(transport.calls[0]["json_body"]["model"], OPENROUTER_MODEL)
        self.assertEqual(transport.calls[0]["headers"]["User-Agent"], "JiraTestPlanCreator/1.0")

    def test_generation_uses_plan_only_strict_schema_and_validates_response(self):
        transport = FakeTransport([{"choices": [{"message": {"content": json.dumps(model_plan())}}]}])
        context = {"issue": {"key": "PROJ-123", "summary": "Story"}, "retrieval": {"warnings": []}}
        result = OpenRouterClient("router-key", transport=transport, retries=0).generate_test_plan(context, "Fetch PROJ-123")
        request_body = transport.calls[0]["json_body"]
        provider_schema = request_body["response_format"]["json_schema"]["schema"]
        self.assertEqual(result["source_issue_key"], "PROJ-123")
        self.assertTrue(request_body["response_format"]["json_schema"]["strict"])
        self.assertEqual(request_body["model"], OPENROUTER_MODEL)
        self.assertTrue(request_body["provider"]["require_parameters"])
        self.assertEqual(request_body["plugins"][0]["id"], "response-healing")
        self.assertNotIn("test_cases", provider_schema["properties"])
        self.assertNotIn("scenarios", result)

    def test_generation_retries_one_schema_failure(self):
        failure = json_response(400, {"error": {"code": "json_validate_failed", "message": "Schema mismatch"}})
        success = {"choices": [{"message": {"content": json.dumps(model_plan())}}]}
        transport = FakeTransport([failure, success])
        context = {"issue": {"key": "PROJ-123", "summary": "Story"}, "retrieval": {"warnings": []}}
        result = OpenRouterClient("router-key", transport=transport, retries=0).generate_test_plan(context, "Fetch PROJ-123")
        self.assertEqual(len(transport.calls), 2)
        self.assertEqual(result["source_issue_key"], "PROJ-123")

    def test_generation_retries_non_english_output_once(self):
        non_english = model_plan()
        non_english["clarification_questions"] = ["请确认测试环境。"]
        responses = [
            {"choices": [{"message": {"content": json.dumps(non_english, ensure_ascii=False)}}]},
            {"choices": [{"message": {"content": json.dumps(model_plan())}}]},
        ]
        transport = FakeTransport(responses)
        context = {"issue": {"key": "PROJ-123", "summary": "Story"}, "retrieval": {"warnings": []}}
        result = OpenRouterClient("router-key", transport=transport, retries=0).generate_test_plan(context, "Fetch PROJ-123")
        self.assertEqual(len(transport.calls), 2)
        self.assertEqual(result["source_issue_key"], "PROJ-123")
        self.assertIn("English only", transport.calls[1]["json_body"]["messages"][-1]["content"])


class RendererAndOrchestratorTests(unittest.TestCase):
    def test_renderer_produces_only_plan_level_sections(self):
        markdown = render_test_plan(sample_plan())
        expected = [
            "Objective", "Scope", "Inclusion", "Test Environment", "Defect Reporting Procedure",
            "Test Strategy", "Test Schedule", "Test Deliverables", "Entry and Exit Criteria",
            "Test Execution", "Test Closure", "Tools", "Risks and Mitigations", "Approvals",
        ]
        for heading in expected:
            self.assertIn(f"## {heading}", markdown)
        self.assertNotIn("## Test Cases", markdown)
        self.assertNotIn("## Detailed Test Cases", markdown)
        self.assertNotIn("TC-001", markdown)

    def test_orchestrator_fetches_generates_and_writes_output(self):
        class FakeJira:
            def __init__(self, settings): pass
            def fetch_issue_context(self, issue_key):
                return {"issue": {"key": issue_key}, "retrieval": {"warnings": ["Source warning"]}}

        class FakeLLM:
            def __init__(self, key): pass
            def generate_test_plan(self, context, prompt): return sample_plan(context["issue"]["key"])

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            store = SettingsStore(root / "settings.json")
            store.save({"jira_url": "https://example.atlassian.net", "jira_email": "qa@example.com", "jira_token": "token", "openrouter_api_key": "key"})
            orchestrator = TestPlanOrchestrator(store, root / "output", FakeJira, FakeLLM)
            result = orchestrator.generate("Fetch Jira PROJ-123 and create a test plan")
            self.assertTrue(result["ok"])
            output = (root / "output" / "PROJ-123-test-plan.md")
            self.assertTrue(output.exists())
            self.assertNotIn("Detailed Test Cases", output.read_text(encoding="utf-8"))
            self.assertIn("Source warning", result["warnings"])


if __name__ == "__main__":
    unittest.main()
