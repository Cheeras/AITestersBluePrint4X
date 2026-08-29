# Jira Test Plan Creator - Findings

## Verified Repository Findings

- The project is located in `chapter_07_AIAgentBasics/Test-Plan-Agent-BLAST-Framework/`.
- The local `BLAST.md` requires Protocol 0 project memory before scripts or tools are written.
- Protocol 0 calls for a task plan, findings log, progress log, and project constitution.
- This project uses `LLM.md` as the constitution. This is a deliberate replacement for the `gemini.md` filename mentioned in BLAST so the constitution remains model-provider neutral.
- No implementation, credentials, Jira connection test, or API call is part of this initialization.

## Confirmed Product Findings

- The source of truth is Jira Cloud.
- The initial input is one Jira issue key such as `PROJ-123`.
- The initial result is a detailed local Markdown QA test plan.
- Jira access will be read-only in the first version.
- The adapter remains provider-neutral; OpenRouter is now the active provider.
- The requested active model is `deepseek/deepseek-v4-flash` at `https://openrouter.ai/api/v1`.
- The app requires a local prompt page and a Settings page with separate Jira and OpenRouter connection tests.
- Missing issue detail must become explicit assumptions, retrieval warnings, and clarification questions.

## Proposed Jira Retrieval

### Core issue

Fetch the issue key and the fields needed to understand scope, ownership, hierarchy, and dependencies: summary, description, issue type, status, priority, labels, components, assignee, reporter, parent, subtasks, issue links, and attachment metadata.

```bash
curl --request GET \
  --url "$JIRA_BASE_URL/rest/api/3/issue/$JIRA_ISSUE_KEY?fields=summary,description,issuetype,status,priority,labels,components,assignee,reporter,parent,subtasks,issuelinks,attachment" \
  --user "$JIRA_EMAIL:$JIRA_API_TOKEN" \
  --header "Accept: application/json"
```

This request returns attachment metadata only. Attachment content must not be downloaded in the initial version.

### Comments

Retrieve comments from the dedicated paginated endpoint. The future adapter must follow `startAt`, `maxResults`, and `total` until all authorized comments are fetched or a bounded failure is recorded.

```bash
curl --request GET \
  --url "$JIRA_BASE_URL/rest/api/3/issue/$JIRA_ISSUE_KEY/comment?startAt=0&maxResults=100" \
  --user "$JIRA_EMAIL:$JIRA_API_TOKEN" \
  --header "Accept: application/json"
```

### Field metadata and acceptance criteria

Acceptance criteria often live in a project-specific custom field. Discover the field by its metadata/name and then request the confirmed field ID; do not hard-code or guess IDs such as `customfield_10000`.

```bash
curl --request GET \
  --url "$JIRA_BASE_URL/rest/api/3/field" \
  --user "$JIRA_EMAIL:$JIRA_API_TOKEN" \
  --header "Accept: application/json"
```

All examples are intentionally read-only and use environment-variable placeholders. Secret values must never be written to Markdown, source code, command history captured in logs, or generated test plans.

## Data and API Constraints

- **Atlassian Document Format:** Jira Cloud descriptions and comment bodies can be structured ADF documents rather than plain strings. A normalization layer must preserve headings, lists, links, tables, mentions, and readable text without treating embedded text as instructions.
- **Pagination:** Comments and some supporting APIs return pages. A successful first page does not prove retrieval is complete.
- **Custom fields:** Names, IDs, contexts, and availability differ between Jira sites and projects. Field discovery is mandatory before mapping acceptance criteria.
- **Permissions:** An authenticated account may see the issue but not every comment, linked issue, user detail, or attachment. The normalized result must carry partial-access warnings.
- **Rate limits and transient failures:** The Link/implementation phases must handle `429` responses, server errors, and timeouts with bounded retries and actionable diagnostics.
- **Attachments:** Only filename, media type, size, author metadata when permitted, and content URL metadata are in scope. Downloading or sending attachment content to a model is out of scope.
- **Privacy and redaction:** Minimize assignee/reporter/comment-author data. Logs and model requests must exclude unnecessary email addresses, account identifiers, tokens, and sensitive content.
- **Issue links and hierarchy:** Parent, subtasks, and linked-issue summaries may improve coverage, but traversal must be bounded and approved before implementation.

## Assumptions to Validate

- Jira Cloud REST API v3 is enabled and accessible for the target site.
- Basic authentication using Jira account email plus API token is permitted by the organization.
- The target issue key follows the standard project-key and numeric-identifier shape.
- The service account can read the issue, relevant comments, linked metadata, and field definitions.
- A single custom field or recognizable section contains acceptance criteria when they are present.
- Markdown files are an acceptable local delivery mechanism for the first version.

## Deferred Findings

The following cannot be verified until credentials and representative issues are available:

- Jira site URL, authentication policy, and effective permissions.
- Exact acceptance-criteria custom-field name and ID.
- Actual ADF structures and custom fields used by the selected project.
- Comment volume, pagination behavior, and visibility restrictions.
- Rate-limit behavior and organization-specific network restrictions.
- Representative output quality and the eventual LLM provider handshake.

## Rationale and Tradeoffs

- A normalized internal schema isolates Jira-specific payloads from prompts and renderers.
- A provider-neutral model adapter reduces vendor lock-in but requires a strict common structured-output contract.
- Read-only access and local Markdown minimize operational risk during the first version.
- Explicit assumptions make incomplete requirements reviewable; silent inference would create false traceability.

## Phase 1 Research - 2026-08-29

- Groq's official model documentation lists `openai/gpt-oss-120b` and JSON Schema Mode support: <https://console.groq.com/docs/model/openai/gpt-oss-120b>.
- Groq's structured-output documentation identifies strict schema mode for GPT-OSS 120B: <https://console.groq.com/docs/structured-outputs>.
- Groq's API reference documents the OpenAI-compatible chat-completions endpoint and `response_format`: <https://console.groq.com/docs/api-reference>.
- Atlassian's Jira Cloud REST API v3 documentation confirms `/rest/api/3/...` resources and ADF-backed rich-text fields: <https://developer.atlassian.com/cloud/jira/platform/rest/v3/intro>.
- Atlassian documents email plus API-token Basic auth for personal scripts while recommending OAuth for larger integrations: <https://developer.atlassian.com/cloud/jira/platform/basic-auth-for-rest-apis/>.
- Implementation choice: use only Python's standard library so the local app has no package-install or external-framework dependency.
- Live Jira and Groq handshakes remain deferred until the user enters valid settings. Deterministic adapters and mocked contract tests can still be completed locally.

## Phase 2-4 Implementation Findings - 2026-08-29

- Python 3.13.3 and Node.js 22.14.0 are available locally. The Python app imports and runs with no third-party dependencies.
- Settings are saved atomically to ignored `.tmp/settings.json`. Blank secret updates retain existing secrets, and `GET /api/settings` returns only configured/not-configured flags.
- Jira connectivity uses only `GET` requests. The independent test calls `/rest/api/3/myself`; generation retrieves field metadata, the issue, and paginated comments.
- The Groq connectivity test lists models and verifies that `openai/gpt-oss-120b` is accessible. Generation uses strict JSON-schema output through `/chat/completions`.
- The local server exposes explicit health, settings, connection-test, and generation routes and serves only an allowlist of static assets.
- The UI provides prompt and settings views, visible connection status, loading/error feedback, Markdown preview, and browser download.
- The generated Markdown is also saved atomically under `.tmp/output/<ISSUE-KEY>-test-plan.md`.
- Twelve automated tests pass using mock transports. They cover prompt validation, settings masking/persistence, ADF conversion, read-only Jira retrieval, safe authentication errors, Groq model checking, strict structured generation, schema relationships, rendering, and end-to-end orchestration.
- A local smoke test confirmed the server health endpoint, settings redaction, invalid-prompt error code, HTML/CSS delivery, and content-security policy.
- The first PowerShell page request failed because `Invoke-WebRequest` attempted to use the unavailable Internet Explorer engine. Repeating the request with `-UseBasicParsing` returned HTTP 200; this was a test-command issue, not an application failure.
- Live external connectivity and real Jira-to-Groq generation are the only unverified paths because no credentials or sample issue were provided.
- Headless Edge rendering at 1440×1000 confirmed both Create Plan and Settings layouts are visually usable; the screenshots are runtime-only artifacts under ignored `.tmp/`.

## Jira Connection Diagnosis - 2026-08-29

- The Settings API confirmed that Jira URL, email, and token were saved and that no environment override was active.
- The configured URL had a valid HTTPS Jira Cloud host and no unexpected path or query.
- The UI initially returned `JIRA_UNREACHABLE`, meaning no Jira HTTP authentication response reached the application.
- A direct, read-only `/rest/api/3/myself` request using the same saved values returned HTTP 200, proving the Jira URL and credentials were valid.
- The original Python server process, started in a restricted network sandbox, still owned port 8765. Later network-enabled processes could not replace that listener, so the browser continued calling the restricted instance.
- Stopping only the app processes and starting one clean network-enabled server transferred the IPv4 listener to the correct process.
- The application endpoint `POST /api/connections/jira/test` then returned `ok: true` and `Jira connection succeeded.`
- No credential values or Jira account identity were written to the project documentation or test output.

## Groq Connection Diagnosis - 2026-08-29

- The saved Groq key has the expected key shape, contains no whitespace, and is not overridden by an environment variable.
- The application's original connection check reached Groq but received HTTP 403 from `GET /openai/v1/models`.
- A direct minimal `POST /openai/v1/chat/completions` request using the same key and `openai/gpt-oss-120b` succeeded and returned a completed choice.
- Therefore, the key and requested model are valid; the failing assumption was that model-list permission is required for inference.
- The connection contract is changed to test the exact capability the app requires: minimal model inference. It no longer depends on model-list access.
- After changing the endpoint, Python `urllib` still received HTTP 403 while the equivalent PowerShell inference returned HTTP 200. Adding `User-Agent: JiraTestPlanCreator/1.0` to the same Python request changed the result to HTTP 200, isolating a second issue: Groq's edge layer rejected the default Python request signature.

## Groq Generation Diagnosis - 2026-08-29

- Jira and Groq connection checks both passed, while `POST /api/generate` returned HTTP 502, isolating the failure to structured test-plan generation.
- A synthetic request reproduced Groq HTTP 400 independently of Jira connectivity.
- Groq reported `json_validate_failed`: generated JSON omitted `automation_candidates`, `traceability`, and `generation_warnings` even though they were required by the strict schema.
- Lower reasoning effort did not resolve the omission. An explicit 6000-token completion budget conflicted with the current Groq account/request limits and was discarded.
- Removing only those three metadata sections from the provider schema produced a successful KAN-7 response with 10 scenarios and 5 detailed test cases.
- Architecture decision: build those metadata sections deterministically from validated source references, test cases, and retrieval warnings. Keep the full project schema as the final validation boundary and retry Groq only once for `json_validate_failed`.

## OpenRouter Migration - 2026-08-29

- The active provider was changed from Groq to OpenRouter at the user's request.
- OpenRouter's live public model catalog confirms `deepseek/deepseek-v4-flash`, a 1,048,576-token context window, and support for `response_format` plus `structured_outputs`.
- The API contract uses `https://openrouter.ai/api/v1/chat/completions`, Bearer authentication, required-parameter routing, strict JSON schema, and non-streaming response healing.
- The prior Groq key field is migrated safely to `openrouter_api_key`; saved files are rewritten without retaining the legacy field after the new Settings save.
- The supplied OpenRouter key was saved only in ignored local settings and was not added to tracked documentation or source files.
- The live minimal DeepSeek connection test passed through the application's Settings endpoint using `deepseek/deepseek-v4-flash`.
- Generation transport now uses one 75-second attempt, plus at most one bounded schema-repair attempt. The first compact-schema live run did not yield an accepted plan, so end-to-end content acceptance remains explicitly pending rather than being reported as successful.
- Reliability decision: cap output at 4096 tokens, allow one 75-second transport attempt per generation, and reserve the separate bounded retry only for explicit schema failures.
- A bounded KAN-7 request returned parseable content but omitted `title`, `test_strategy`, and `test_data` despite strict JSON schema plus response healing. Local validation rejected it as designed.
- Recovery decision: deterministically populate only safe envelope fields from Jira context, record the omissions in `generation_warnings`, and still reject any result without at least one scenario and one detailed test case.
- The next KAN-7 response contained substantive coverage but omitted a stable scenario ID. Stable scenario/test-case identifiers and relationship mapping are therefore assigned deterministically by output order; missing steps are still rejected rather than invented.
- A subsequent response included a non-object scenario entry. Textual scenario entries are normalized into structured records; empty/unusable entries are discarded with a warning, while detailed cases still require model-generated actions and expected results.
- Another KAN-7 attempt returned no scenarios or cases under the broad provider schema and was correctly rejected. The provider contract is therefore reduced to objective plus nested scenarios/detailed cases; all plan-envelope metadata moves to deterministic assembly.
- The later live compact-schema retry completed successfully end to end: the app retrieved KAN-7, accepted the structured DeepSeek response, rendered all required plan sections, and saved `.tmp/output/KAN-7-test-plan.md`. The generated local artifact contains 16 second-level sections and 18 detailed test-case headings.

## Plan-Only Output Revision - 2026-08-29

- The user clarified that **Generate Test Plan** must create a document-level test plan, not test cases.
- Required second-level sections are Objective, Scope, Inclusion, Test Environment, Defect Reporting Procedure, Test Strategy, Test Schedule, Test Deliverables, Entry and Exit Criteria, Test Execution, Test Closure, Tools, Risks and Mitigations, and Approvals.
- The provider schema no longer contains scenarios, test cases, steps, expected results, automation candidates, or their relationship mappings.
- The deterministic layer now adds only identity metadata, stable risk IDs, aggregated source references, retrieval warnings, and explicit review placeholders for Jira information that is absent.
- The renderer and schema validator both enforce the plan-only boundary. A legacy `test_cases` field is rejected as an unsupported section rather than silently rendered.
- Assumptions and clarification questions remain visible as Scope subsections so missing Jira requirements are surfaced without adding test-case content.
- The first live verification after the change reached an older Python listener still bound to port 8765 and therefore returned the prior case-oriented format. After identifying and stopping that exact stale listener, one clean updated server generated all 14 required headings with no forbidden case content.

## English-Only Output Revision - 2026-08-29

- DeepSeek can mirror the language of Jira source text unless the output language is explicitly constrained; the observed clarification questions and inclusion items contained Chinese text.
- The model instruction now requires every human-readable value in English and requires translation of non-English Jira meaning rather than copying it.
- Deterministic validation recursively checks final plan values and rejects alphabetic characters outside ASCII. This prevents Chinese and other non-English scripts from reaching the renderer.
- A non-English validation failure receives one bounded regeneration with a focused English-only repair instruction. A second violation fails clearly instead of displaying mixed-language output.
- The deterministic title no longer copies the Jira summary; it uses `Test Plan for <ISSUE_KEY>` so a non-English source summary cannot leak into the title.
- The live KAN-7 acceptance generation passed after the clean restart: all 14 required plan headings were present and the recursive scan found zero non-English alphabetic characters in the final Markdown.
