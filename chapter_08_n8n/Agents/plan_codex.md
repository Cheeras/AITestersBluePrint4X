# Plan: Screenshot to Bug Reporter AI Agent (Codex)

## Goal

Create a Jira Bug from a tester-submitted UI screenshot, include a structured AI draft, and attach the original screenshot to the created issue.

## Workflow

1. **On bug report submission** — n8n form accepts one screenshot, optional error logs, and the Jira project key.
2. **Normalize Intake** — validates the single file and records its binary property, MIME type, file name, logs, and project key.
3. **Screenshot to Base64** — creates a data URL for the vision request while retaining the original binary for attachment.
4. **Groq Vision - Draft Bug Report** — calls Groq's OpenAI-compatible vision endpoint using a referenced Header Auth credential. The initial model is `qwen/qwen3.6-27b`, matching the model shown in the supplied workflow screenshot; update that one model field if Groq changes its available model IDs.
5. **Parse Bug Report** — validates the JSON response and creates Jira wiki-markup description content.
6. **Jira - Create Bug** — creates a Bug in the submitted project.
7. **Prepare Attachment** and **Jira - Attach Screenshot** — retrieve the original binary and attach it to the newly created Jira issue.

## Required n8n configuration

- Create an **HTTP Header Auth** credential named `Groq API Header Auth` with header name `Authorization` and value `Bearer <your-groq-api-key>`.
- Select that credential in **Groq Vision - Draft Bug Report** after import.
- Select a Jira Software Cloud credential in both Jira nodes.
- Ensure the Jira project has an issue type named `Bug` and the account may create issues and attachments.

## Acceptance checks

1. Import `09_Screenshot_to_Bug_Reporter_AIAgent_codex.json` into n8n.
2. Submit a PNG/JPEG/WebP screenshot and a valid Jira project key through the generated form.
3. Confirm a Jira Bug is created with description, visual clues, and any submitted logs.
4. Confirm the original uploaded screenshot appears as an attachment on that issue.

## Scope boundary

This workflow drafts and files a bug; it does not deduplicate issues, assign owners, alter priority fields, or send notifications. Review the AI-produced report during normal Jira triage.
