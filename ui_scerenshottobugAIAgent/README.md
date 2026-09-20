# AwasomeQA — Screenshot to Bug Reporter UI

Lightweight static HTML/JS UI for the **Screenshot to Bug Reporter** n8n AI Agent. Testers upload a UI screenshot, optionally add error logs and a Jira project key, and the workflow drafts a complete Jira bug.

## Deploy to Vercel

1. Push to GitHub.
2. In [Vercel](https://vercel.com), click **Add New → Project**.
3. Import the repo, set root directory to `ui_scerenshottobugAIAgent`.
4. Deploy — zero config, no build step needed.

## Run locally

Just open `index.html` in any browser. No server required.

## How it works

```
Static UI → POST multipart form → n8n Form Trigger
  → Groq Vision → Jira Create Bug → Attach Screenshot
```