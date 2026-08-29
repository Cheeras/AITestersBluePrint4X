# Jira Test Plan Creator - Task Plan

## North Star

Create a reliable, reviewable, and traceable Markdown test plan from one Jira Cloud issue key (for example, `PROJ-123`). The future agent must distinguish Jira facts from generated assumptions and trace its proposed coverage back to source material.

## Protocol 0 Status

> **Blueprint approved:** On 2026-08-29 the user explicitly requested implementation of BLAST Phases 1-4. Implementation may proceed under the approved schemas, SOP, read-only Jira boundary, and secret-handling rules.

### Confirmed Decisions

- Source of truth: Jira Cloud.
- Initial input: one Jira issue key.
- Initial output: a detailed local Markdown QA test plan.
- Output level: planning and governance only; do not generate test scenarios, test cases, test steps, or expected-result tables.
- Output language: English only, even when the Jira source contains another language.
- Model integration: provider-neutral adapter with OpenRouter as the active provider.
- Model: `deepseek/deepseek-v4-flash` through `https://openrouter.ai/api/v1`.
- Jira access: read-only in the first version.
- Credentials: entered through a local Settings page, stored only in ignored `.tmp/settings.json`, and never committed or returned to the browser.
- Missing requirements: expose assumptions, gaps, and clarification questions; never silently invent facts.
- Constitution: `LLM.md` intentionally fulfills the `gemini.md` role named in BLAST.
- Activity tracking: event-based, with real elapsed-time checkpoints rather than fabricated entries.

## Goals and Checklist

### Phase 0 - Initialization

- [x] Review the local BLAST protocol and project notes.
- [x] Record the objective, confirmed decisions, constraints, and risks.
- [x] Initialize `task_plan.md`, `findings.md`, `progress.md`, and `LLM.md`.
- [x] Define conceptual input, normalized Jira, and generated-plan schemas.
- [x] Document sanitized Jira Cloud REST API request examples.
- [x] Review and approve the Blueprint.
- [ ] Confirm the discovered Jira acceptance-criteria field after credentials are supplied.

### Phase 1 - Blueprint and Schema Confirmation

- [x] Confirm Jira Cloud and a read-only, single-issue permission boundary.
- [x] Confirm the minimum source fields and direct relationship context.
- [x] Refine the schemas in `LLM.md` for the UI and provider structured-output contract.
- [x] Confirm detailed test-plan sections and `.tmp/output/<KEY>-test-plan.md` naming.
- [x] Approve the Blueprint before implementation begins.

### Phase 2 - Link and Connectivity

- [x] Configure the Jira URL, email, and API token in ignored local settings.
- [x] Verify authentication with the read-only `/rest/api/3/myself` request.
- [x] Verify access to an allowed sample issue and field metadata.
- [x] Implement separate Jira and OpenRouter connection-test endpoints and Settings UI controls.
- [x] Verify Jira issue, field, and comment contracts through mock transports.
- [x] Verify OpenRouter model metadata and structured-output support.
- [x] Verify the configured OpenRouter key can invoke `deepseek/deepseek-v4-flash` through the live Settings endpoint.
- [x] Record handshake tests, errors, and results in `progress.md`.

> Jira and OpenRouter connection verification passed. A live Jira-to-OpenRouter generation also passed; stakeholder review of the resulting plan remains pending.

### Phase 3 - A.N.T. Architecture and Tools

- [x] Write architecture SOPs before implementing deterministic tools.
- [x] Implement input validation and orchestration.
- [x] Implement a read-only Jira API adapter with pagination and bounded retries.
- [x] Normalize Jira fields and Atlassian Document Format into a stable schema.
- [x] Implement a provider-neutral LLM generation adapter with OpenRouter as the active provider.
- [x] Validate structured model output deterministically.
- [x] Render validated output as a local Markdown test plan.
- [x] Keep intermediate artifacts and local settings in ignored `.tmp/`; support environment overrides.

### Phase 4 - Prompt and Output Refinement

- [x] Define prompts that treat Jira text as untrusted data.
- [x] Require source references, assumptions, risks, and clarification questions.
- [x] Refine Markdown organization for QA review and traceability.
- [x] Build a responsive prompt UI and Settings UI with accessible labels and status feedback.
- [ ] Review a generated plan with stakeholders before declaring the format stable.

### Phase 5 - Verification

- [x] Unit-test issue-key validation, ADF normalization, rendering, settings, and safe error mapping.
- [x] Schema-test every required plan section and rejection of legacy test-case fields.
- [x] Integration-test Jira and OpenRouter adapters using mock transports and sanitized fixtures.
- [x] Verify authentication failure redaction and deterministic invalid-prompt handling.
- [x] Verify stable risk IDs and source references without scenario or test-case output.
- [x] Reject non-English model output and retry once with an English-only repair instruction.
- [x] Verify the settings API never returns saved secrets.
- [x] Smoke-test health, HTML, CSS, CSP, and server-side API behavior locally.
- [x] Run a live Jira-to-OpenRouter end-to-end generation.
- [ ] Review real output coverage and quality with a representative Jira issue.

### Trigger - Local Run

- [x] Document the zero-dependency startup command in `README.md`.
- [x] Start the application on `127.0.0.1:8765`.
- [x] Confirm `/api/health` reports `ready`.
- [x] Keep the current local server session running for user evaluation.

## Success Criteria

- A valid Jira issue key results in a schema-valid, readable Markdown test plan.
- The plan includes Objective, Scope, Inclusion, Test Environment, Defect Reporting Procedure, Test Strategy, Test Schedule, Test Deliverables, Entry and Exit Criteria, Test Execution, Test Closure, Tools, Risks and Mitigations, and Approvals.
- The generated Markdown contains no test scenarios, test cases, step tables, expected results, or automation-candidate section.
- Every human-readable Markdown value is English; non-English responses fail deterministic validation instead of being displayed.
- Jira-derived claims retain source references; generated suggestions are visibly distinguished from source facts.
- Missing or ambiguous requirements are reported rather than silently filled in.
- Invalid input and external failures produce clear, actionable errors without leaking secrets.
- Jira remains read-only and no comment, issue, or attachment is created or modified.

## Dependencies

- A Jira Cloud site URL and authorized test account.
- A Jira API token with least-privilege access to the target issues.
- Representative, non-sensitive Jira issues or sanitized fixtures.
- A later-selected LLM provider and credentials behind the provider-neutral interface.
- OpenRouter API access to `deepseek/deepseek-v4-flash`.

## Risks and Mitigations

| Risk | Planned mitigation |
|---|---|
| Acceptance criteria use project-specific custom fields | Discover fields from `/rest/api/3/field`; never guess a custom-field ID. |
| Jira descriptions/comments use Atlassian Document Format | Normalize ADF deterministically before model input. |
| Comments or related data are paginated | Follow Jira pagination metadata and record partial-retrieval warnings. |
| Jira content attempts prompt injection | Treat all retrieved content as untrusted data and enforce constitutional rules. |
| LLM fabricates requirements or traceability | Require structured output, source references, explicit assumptions, and schema validation. |
| Secrets or personal data leak into logs | Use environment variables, redact diagnostics, and minimize identity fields. |
| Excessive related-issue traversal | Establish bounded traversal limits during Blueprint approval. |

## Out of Scope for the Initial Version

- Posting the test plan to Jira or modifying any Jira object.
- Downloading or interpreting attachment contents.
- Generating executable automated tests.
- Multi-user hosting, accounts, roles, and remote deployment.
