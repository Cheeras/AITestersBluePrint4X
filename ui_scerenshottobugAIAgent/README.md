# AwasomeQA — Screenshot to Bug Reporter UI (Streamlit)

Lightweight Streamlit UI for the **Screenshot to Bug Reporter** n8n AI Agent. Testers upload a UI screenshot, optionally add error logs and a Jira project key, and the workflow drafts a complete Jira bug.

## Run locally

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Deploy to Streamlit Community Cloud

1. Push to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io) → New app.
3. Select repo and branch, set main file to `streamlit_app.py`.
4. Deploy — free, no config needed.

## How it works

```
Streamlit UI → POST multipart form → n8n Form Trigger
  → Groq Vision → Jira Create Bug → Attach Screenshot
```
