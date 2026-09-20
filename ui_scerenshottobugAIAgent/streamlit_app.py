import streamlit as st
import requests
from pathlib import Path

# ── Config ──────────────────────────────────────────────────────────────
N8N_FORM_URL = (
    "https://aitestersqa.app.n8n.cloud/form/da47e150-8172-41d8-ba30-da2078f9e0b5"
)

st.set_page_config(
    page_title="AwasomeQA — Bug Reporter",
    page_icon="📸",
    layout="centered",
)

# ── Inline Light-Mode Styles ────────────────────────────────────────────
st.markdown(
    """
<style>
    #MainMenu, header, footer { visibility: hidden; }
    .stApp { background: #f5f7fb; }
    .block-container { max-width: 640px !important; padding-top: 2rem !important; }

    .header {
        display: flex; align-items: center; gap: 14px; margin-bottom: 28px;
    }
    .logo {
        width: 44px; height: 44px; border-radius: 11px;
        background: linear-gradient(135deg, #2563eb, #7c3aed);
        color: #fff; font-size: 20px; font-weight: 800;
        display: flex; align-items: center; justify-content: center; flex-shrink: 0;
    }
    .header-text h1 { font-size: 22px; font-weight: 800; margin: 0; color: #0f172a; }
    .header-text p { font-size: 13px; color: #64748b; margin: 0; }

    .card {
        background: #fff; border: 1px solid #e2e8f0; border-radius: 14px;
        padding: 24px; box-shadow: 0 1px 3px rgba(15,23,42,0.06);
    }
    .card h2 { font-size: 18px; font-weight: 700; margin: 0 0 4px; color: #0f172a; }
    .card .subtitle { font-size: 13px; color: #64748b; margin: 0 0 20px; }

    .footer { text-align: center; font-size: 12px; color: #64748b; margin-top: 24px; }
    .footer a { color: #2563eb; text-decoration: none; }

    .stFileUploader > div { border: 2px dashed #e2e8f0 !important;
        border-radius: 12px !important; padding: 28px !important; }
    .stAlert { border-radius: 10px; }
</style>
""",
    unsafe_allow_html=True,
)

# ── Header ──────────────────────────────────────────────────────────────
st.markdown(
    """
<div class="header">
    <div class="logo">A</div>
    <div>
        <h1 style="margin:0;font-size:22px;font-weight:800">AwasomeQA</h1>
        <p style="margin:0;font-size:13px;color:#64748b">Quality first — Screenshot to Bug Reporter</p>
    </div>
</div>
""",
    unsafe_allow_html=True,
)

# ── Card ────────────────────────────────────────────────────────────────
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown("<h2>Report a UI Bug</h2>", unsafe_allow_html=True)
st.markdown(
    '<p class="subtitle">Upload a screenshot. AI drafts a Jira bug report.</p>',
    unsafe_allow_html=True,
)

screenshot = st.file_uploader(
    "Screenshot *", type=["png", "jpg", "jpeg", "webp"], label_visibility="collapsed"
)

error_logs = st.text_area(
    "Error logs",
    placeholder="Paste console errors or stack traces (optional)",
    label_visibility="visible",
)

project_key = st.text_input(
    "Jira project key *",
    placeholder="e.g. VWO",
    label_visibility="visible",
)

if st.button("🚀 Submit Bug Report", type="primary", use_container_width=True):
    if not screenshot:
        st.error("Please upload a screenshot.")
    elif not project_key.strip():
        st.error("Please enter the Jira project key.")
    else:
        with st.spinner("Analyzing screenshot with AI…"):
            try:
                files = {"Screenshot": (screenshot.name, screenshot.getvalue(), screenshot.type)}
                data = {
                    "Error logs": error_logs,
                    "Jira project key": project_key.strip(),
                }
                r = requests.post(N8N_FORM_URL, files=files, data=data, timeout=60)
                if r.ok:
                    st.success("✅ Bug report submitted! Check Jira for the new issue.")
                    st.balloons()
                else:
                    st.error(f"Submission failed (HTTP {r.status_code}). Please try again.")
            except Exception as e:
                st.error(f"Error: {e}")

st.markdown("</div>", unsafe_allow_html=True)

st.markdown(
    '<div class="footer">Powered by <a href="https://n8n.io" target="_blank">n8n</a> · AwasomeQA</div>',
    unsafe_allow_html=True,
)