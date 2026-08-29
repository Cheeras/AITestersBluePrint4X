# Jira Test Plan Creator

A local BLAST/A.N.T. application that reads one Jira Cloud issue and generates an English, document-level Markdown QA test plan through OpenRouter using `deepseek/deepseek-v4-flash`.

The application produces test-planning and governance content. It deliberately does **not** generate test scenarios, test cases, test steps, expected-result tables, or automation-candidate lists.

## Features

- Accepts a natural-language request containing exactly one Jira issue key.
- Retrieves Jira issue fields, acceptance criteria, comments, relationships, and attachment metadata through read-only Jira Cloud REST API v3 requests.
- Provides separate Jira and OpenRouter connection checks on the Settings page.
- Uses a provider-neutral generation boundary with OpenRouter as the active adapter.
- Validates structured model output before rendering or saving it.
- Requires English-only output, even when Jira contains another language.
- Retries once with an English-only repair instruction when non-English model output is detected.
- Displays the generated Markdown in the browser and saves it atomically under `.tmp/output/`.
- Keeps Jira and OpenRouter credentials out of source control and API responses.

## Output Contract

Every generated plan contains these sections:

1. Objective
2. Scope
3. Inclusion
4. Test Environment
5. Defect Reporting Procedure
6. Test Strategy
7. Test Schedule
8. Test Deliverables
9. Entry and Exit Criteria
10. Test Execution
11. Test Closure
12. Tools
13. Risks and Mitigations
14. Approvals

Assumptions and clarification questions appear as subsections under Scope. Jira-derived risks retain source references, and missing Jira planning details are presented as explicit review placeholders rather than invented facts.

## Architecture

```text
Prompt UI
   -> Input validation and orchestration
   -> Read-only Jira adapter
   -> Jira/ADF normalization
   -> OpenRouter DeepSeek adapter
   -> Deterministic schema and English validation
   -> Markdown renderer
   -> Browser preview and .tmp/output/<ISSUE-KEY>-test-plan.md
```

Key directories and files:

- `app.py`: local HTTP server and API routes.
- `core/`: orchestration, schemas, validation, rendering, settings, and safe errors.
- `tools/`: read-only Jira, OpenRouter, and HTTP transport adapters.
- `static/`: Create Plan and Settings user interfaces.
- `tests/`: standard-library unit and integration tests with mock transports.
- `architecture/SOP.md`: implemented A.N.T. architecture and operating rules.
- `task_plan.md`, `findings.md`, `progress.md`, and `LLM.md`: BLAST project memory and constitution.

## Requirements

- Python 3.11 or newer.
- A Jira Cloud account with access to the requested issues.
- A Jira API token.
- An OpenRouter API key with access to `deepseek/deepseek-v4-flash`.

No third-party Python packages are required.

## Run Locally

From the repository root:

```powershell
cd chapter_07_AIAgentBasics\Test-Plan-Agent-BLAST-Framework
python app.py
```

Open <http://127.0.0.1:8765>.

If port `8765` is already occupied by an older copy of the application, stop that process before starting the updated server.

## Configure Connections

Open **Settings** and enter:

- Jira URL, such as `https://your-company.atlassian.net`
- Jira account email
- Jira API token
- OpenRouter API key

Save the settings, then run **Test Jira connection** and **Test OpenRouter connection** independently.

Local secrets are written only to the ignored `.tmp/settings.json` file and are never returned by the Settings API. The following environment variables can override saved values:

```text
JIRA_BASE_URL
JIRA_EMAIL
JIRA_API_TOKEN
OPENROUTER_API_KEY
```

## Generate a Test Plan

On **Create plan**, enter a request containing one Jira issue key:

```text
Fetch Jira PROJ-123 and create a test plan
```

Select **Generate test plan**. The application validates the issue key, retrieves Jira context, generates and validates the English plan, displays it in the browser, and saves it as:

```text
.tmp/output/PROJ-123-test-plan.md
```

Posting comments or modifying Jira is outside the application's scope.

## Local API

| Method | Route | Purpose |
|---|---|---|
| `GET` | `/api/health` | Check local server readiness. |
| `GET` | `/api/settings` | Return non-secret settings and configured-state flags. |
| `POST` | `/api/settings` | Save local Jira and OpenRouter settings. |
| `POST` | `/api/connections/jira/test` | Test the read-only Jira identity request. |
| `POST` | `/api/connections/openrouter/test` | Test minimal DeepSeek inference through OpenRouter. |
| `POST` | `/api/generate` | Fetch one Jira issue and generate its Markdown test plan. |

## Test

```powershell
python -m unittest discover -s tests -v
node --check static/app.js
```

The automated suite uses mock transports and does not call external services. Live Jira and OpenRouter checks require valid local settings.

## Security Boundaries

- Jira access is read-only.
- Jira and prompt content are treated as untrusted data.
- Credentials are excluded from tracked files, browser responses, and safe error messages.
- Attachment metadata may be retrieved, but attachment bodies are not downloaded.
- API requests use finite timeouts and bounded retries.
- Invalid, non-English, or structurally incomplete model output is not rendered as a successful plan.
