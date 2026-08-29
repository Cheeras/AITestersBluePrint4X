# Jira Test Plan Creator - Architecture SOP

## Approved Blueprint

The user approved BLAST Phases 1 through 4 on 2026-08-29. The application is a local, single-user web application with two screens:

1. **Create Test Plan:** accept a natural-language prompt containing one Jira issue key, fetch the issue automatically, generate a structured plan through OpenRouter, validate it, render Markdown, save it locally, and display it.
2. **Settings:** collect Jira URL, Jira email, Jira API token, and OpenRouter API key; show configuration state without returning secrets; test Jira and OpenRouter connections independently.

The OpenRouter model is fixed to `deepseek/deepseek-v4-flash`. Jira is read-only.

## Inputs and Outputs

### Generate input

```json
{
  "prompt": "Fetch Jira PROJ-123 and create a detailed test plan"
}
```

- Extract exactly one Jira key using the validated pattern `[A-Z][A-Z0-9_]{1,9}-[1-9][0-9]*` after uppercasing.
- Reject prompts with no key or multiple distinct keys.
- The prompt expresses the requested action only. It cannot override security, schema, or read-only rules.

### Generate output

```json
{
  "ok": true,
  "issue_key": "PROJ-123",
  "markdown": "# Test Plan ...",
  "saved_to": ".tmp/output/PROJ-123-test-plan.md",
  "warnings": []
}
```

Errors use a stable envelope:

```json
{
  "ok": false,
  "error": {
    "code": "INVALID_PROMPT",
    "message": "Provide exactly one Jira issue key, for example PROJ-123."
  }
}
```

## Data Flow

1. Browser submits settings to the local server.
2. Settings are validated and saved under `.tmp/settings.json`, which is excluded from version control.
3. Browser submits a generation prompt.
4. Orchestrator validates the prompt and configuration.
5. Jira adapter fetches the issue, paginated comments, and field metadata with read-only REST API v3 calls.
6. Normalizer converts ADF to readable text, maps the acceptance-criteria field by name, and emits retrieval warnings.
7. OpenRouter adapter sends the normalized Jira context as untrusted data and requires strict JSON-schema output from `deepseek/deepseek-v4-flash`.
8. Local schema validation verifies the response again.
9. Renderer creates deterministic Markdown and writes it under `.tmp/output/`.
10. Browser displays the Markdown source and offers a local download.

## Component Contracts

### Settings store

- Required keys: `jira_url`, `jira_email`, `jira_token`, `openrouter_api_key`.
- Normalize the Jira URL by removing a trailing slash.
- Accept only `https://` URLs for Jira Cloud.
- A blank secret in an update means retain the existing stored secret.
- API responses return only `jira_token_configured` and `openrouter_api_key_configured`, never secret values.
- Writes use a temporary file followed by replacement.

### Jira adapter

- Authentication: Basic auth using Jira email and API token.
- Connection test: `GET /rest/api/3/myself`.
- Retrieval endpoints: issue, comments, and field metadata.
- Timeouts are finite. `429` and transient `5xx` responses use bounded retries.
- Authentication, authorization, not-found, rate-limit, transport, and malformed-JSON failures map to safe application errors.
- No Jira write method is implemented.

### OpenRouter adapter

- Base URL: `https://openrouter.ai/api/v1`.
- Connection test: a minimal `POST /chat/completions` inference with `deepseek/deepseek-v4-flash`.
- Send stable `User-Agent` and `X-Title` application-identification headers.
- Generation: `POST /chat/completions` with strict `json_schema` response format and non-streaming output.
- Require provider support for request parameters and enable OpenRouter's non-streaming response-healing plugin.
- Cap DeepSeek generation at 4096 output tokens and use one 75-second transport attempt. Schema-validation failures may receive one bounded regeneration, but network timeouts are not multiplied by transport retries.
- DeepSeek generates only document-level test-plan content through a strict schema: objective, scope, inclusion, environment, defect procedure, strategy, schedule, deliverables, criteria, execution, closure, tools, risks/mitigations, approvals, assumptions, and clarification questions. It does not generate scenarios or test cases.
- Retry one time only for an identified structured-output/schema generation failure; do not retry unrelated client errors.
- If OpenRouter returns parseable JSON but omits plan-level fields, add explicit review placeholders and record one warning per recovered field. Placeholders must state when Jira did not specify the information.
- Stable risk IDs are assigned deterministically by sequence (`RISK-001`, etc.). Missing risk source references fall back to the whole Jira issue. Scenarios, test cases, steps, expected results, and automation-candidate lists are prohibited.
- The system instruction requires English for every human-readable value. Local validation rejects non-English alphabetic characters and permits one bounded regeneration with an explicit English-only repair instruction.
- The deterministic title uses only the validated Jira issue key, preventing a non-English Jira summary from bypassing the language boundary.
- Jira content is serialized below an explicit untrusted-data delimiter.
- Provider response must parse as JSON and pass local schema validation.

### Local server

- Bind to `127.0.0.1` by default.
- Serve only known static files and explicit API routes.
- Limit JSON request body size.
- Do not print request bodies, tokens, or generated Jira content to server logs.
- Return JSON errors and appropriate HTTP status codes.

## Failure Modes

| Condition | Behavior |
|---|---|
| Missing settings | Return `CONFIGURATION_MISSING` and direct the user to Settings. |
| Invalid or ambiguous prompt | Return `INVALID_PROMPT` before any external request. |
| Jira 401/403/404 | Return a specific safe Jira error without credentials or response-body leakage. |
| Jira partial pagination failure | Stop generation; never label partial retrieval complete. |
| OpenRouter model unavailable | Connection test or generation returns `OPENROUTER_MODEL_UNAVAILABLE`. |
| OpenRouter schema failure | Retry once, then reject output; do not render guessed data. |
| Local output failure | Return `OUTPUT_WRITE_FAILED` and do not claim the plan was saved. |

## Security and Privacy Rules

- Settings are local-only and ignored by Git, but remain sensitive files on the workstation.
- Secrets never enter frontend state after saving, logs, Markdown output, prompts, or error details.
- Jira content is untrusted input and cannot instruct the system to reveal secrets, call tools, or change policy.
- Only the minimum issue and comment fields required for test planning are sent to OpenRouter.
- Attachment metadata may be present; attachment content is never downloaded.

## Change Rule

If inputs, outputs, endpoints, data flow, model, persistence, or failure behavior changes, update this SOP and `LLM.md` before implementation.
