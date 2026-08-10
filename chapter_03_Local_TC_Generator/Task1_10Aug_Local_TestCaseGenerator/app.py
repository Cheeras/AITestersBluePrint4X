"""
Local TestCase Generator — Streamlit Web App
Fetches requirements from JIRA or manual input, then generates
structured test cases via local Ollama or cloud Groq LLM.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import streamlit as st

from src.jira_client import JIRAClient
from src.prompt_builder import PromptBuilder
from src.llm_service import LLMService
from src.output_handler import save_to_file, format_test_cases


# ── Page config ────────────────────────────────────────────────────
st.set_page_config(
    page_title="Local TestCase Generator",
    page_icon="🧪",
    layout="wide",
)

st.title("🧪 Local TestCase Generator")
st.caption(
    "Fetch requirements from JIRA or paste them manually, "
    "then generate test cases using Ollama (local) or Groq (cloud)."
)

# ── Shared state ───────────────────────────────────────────────────
for key, default in [
    ("requirements", ""),
    ("feature_name", ""),
    ("generated_output", ""),
    ("llm_provider", "groq"),
    ("jira_url", os.getenv("JIRA_URL", "https://shankar-ch.atlassian.net")),
    ("jira_email", os.getenv("JIRA_EMAIL", "")),
    ("jira_token", os.getenv("JIRA_API_TOKEN", "")),
]:
    if key not in st.session_state:
        st.session_state[key] = default

# ── Tabs ───────────────────────────────────────────────────────────
tab_settings, tab_jira, tab_manual, tab_output = st.tabs([
    "⚙️ Settings",
    "📋 Fetch from JIRA",
    "✏️ Manual Requirements",
    "📊 Generated Test Cases",
])

# ══════════════════════════════════════════════════════════════════════
# TAB: Settings
# ══════════════════════════════════════════════════════════════════════
with tab_settings:
    st.header("⚙️ Settings")

    # ── JIRA Connection ────────────────────────────────────────────
    st.subheader("🔗 JIRA Connection")
    col1, col2, col3 = st.columns(3)
    with col1:
        jira_url = st.text_input(
            "JIRA URL",
            value=st.session_state.jira_url,
            placeholder="https://your-domain.atlassian.net",
        )
    with col2:
        jira_email = st.text_input(
            "JIRA Email",
            value=st.session_state.jira_email,
            placeholder="you@example.com",
        )
    with col3:
        jira_token = st.text_input(
            "JIRA API Token",
            value=st.session_state.jira_token,
            type="password",
            placeholder="Your JIRA API token",
        )

    if st.button("🔍 Test JIRA Connection", use_container_width=True):
        with st.spinner("Testing JIRA connection..."):
            try:
                client = JIRAClient(url=jira_url, email=jira_email, api_token=jira_token)
                ok = client.test_connection()
                if ok:
                    st.success("✅ JIRA connection successful!")
                    st.session_state.jira_url = jira_url
                    st.session_state.jira_email = jira_email
                    st.session_state.jira_token = jira_token
                else:
                    st.error("❌ JIRA connection failed — check credentials.")
            except Exception as e:
                st.error(f"❌ JIRA Error: {e}")

    st.divider()

    # ── LLM Provider ───────────────────────────────────────────────
    st.subheader("🤖 LLM Provider")
    llm_choice = st.radio(
        "Select LLM Provider",
        ["groq", "ollama"],
        index=0 if st.session_state.llm_provider == "groq" else 1,
        format_func=lambda x: (
            f"☁️  Groq (Cloud — llama-3.1-8b-instant, FREE)" if x == "groq"
            else f"🖥️  Ollama (Local — gemma3:1b)"
        ),
        horizontal=True,
    )
    st.session_state.llm_provider = llm_choice

    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("🧪 Test Ollama Connection", use_container_width=True):
            with st.spinner("Testing Ollama..."):
                ok, msg = LLMService.test_ollama()
                if ok:
                    st.success(msg)
                else:
                    st.error(msg)
    with col_b:
        if st.button("🧪 Test Groq Connection", use_container_width=True):
            with st.spinner("Testing Groq..."):
                ok, msg = LLMService.test_groq()
                if ok:
                    st.success(msg)
                else:
                    st.error(msg)

    st.divider()
    st.caption("Made with Streamlit • Ollama • Groq • JIRA")

# ══════════════════════════════════════════════════════════════════════
# TAB: Fetch from JIRA
# ══════════════════════════════════════════════════════════════════════
with tab_jira:
    st.subheader("📋 Fetch Requirements from JIRA")
    col1, col2 = st.columns([2, 1])
    with col1:
        issue_key = st.text_input(
            "JIRA Issue Key",
            placeholder="e.g. PROJ-42",
        )
    with col2:
        fetch_btn = st.button("🔍 Fetch Requirements", use_container_width=True)

    if fetch_btn and issue_key.strip():
        with st.spinner(f"Fetching {issue_key.strip()} from JIRA..."):
            try:
                client = JIRAClient(
                    url=st.session_state.jira_url,
                    email=st.session_state.jira_email,
                    api_token=st.session_state.jira_token,
                )
                issue = client.fetch_issue(issue_key.strip())
                summary = issue.get("fields", {}).get("summary", issue_key)
                reqs = client.extract_requirements(issue)
                st.session_state.requirements = reqs
                st.session_state.feature_name = summary
                st.success(f"✅ Fetched: {summary}")
            except Exception as e:
                st.error(f"❌ Failed to fetch: {e}")

    if st.session_state.requirements:
        st.text_area(
            "Fetched Requirements (editable)",
            value=st.session_state.requirements,
            height=250,
            key="jira_reqs",
            on_change=lambda: setattr(st.session_state, "requirements", st.session_state.jira_reqs),
        )
        if st.button("🚀 Generate Test Cases from JIRA", type="primary"):
            st.session_state.feature_name = st.session_state.feature_name or "JIRA Issue"
            with st.spinner(f"Generating test cases via {st.session_state.llm_provider}..."):
                try:
                    builder = PromptBuilder()
                    prompt = builder.build(
                        st.session_state.requirements,
                        feature=st.session_state.feature_name,
                    )
                    raw = LLMService.generate(prompt, provider=st.session_state.llm_provider)
                    st.session_state.generated_output = format_test_cases(
                        raw, feature=st.session_state.feature_name
                    )
                    st.success("✅ Test cases generated! Switch to 'Generated Test Cases' tab.")
                except Exception as e:
                    st.error(f"❌ Generation failed: {e}")
    else:
        st.info("👆 Enter a JIRA issue key and click 'Fetch Requirements' to begin.")

# ══════════════════════════════════════════════════════════════════════
# TAB: Manual Requirements
# ══════════════════════════════════════════════════════════════════════
with tab_manual:
    st.subheader("✏️ Paste Requirements Manually")
    manual_feature = st.text_input(
        "Feature Name",
        placeholder="e.g. Login Module",
        value=st.session_state.feature_name,
    )
    manual_reqs = st.text_area(
        "Requirements",
        placeholder="Paste your PRD, user story, or feature description here...",
        height=300,
        value=st.session_state.requirements,
    )

    if st.button("🚀 Generate Test Cases", type="primary", key="manual_gen"):
        if not manual_reqs.strip():
            st.warning("⚠️ Please enter some requirements first.")
        else:
            st.session_state.requirements = manual_reqs
            st.session_state.feature_name = manual_feature or "Feature"
            with st.spinner(f"Generating test cases via {st.session_state.llm_provider}..."):
                try:
                    builder = PromptBuilder()
                    prompt = builder.build(manual_reqs, feature=st.session_state.feature_name)
                    raw = LLMService.generate(prompt, provider=st.session_state.llm_provider)
                    st.session_state.generated_output = format_test_cases(
                        raw, feature=st.session_state.feature_name
                    )
                    st.success("✅ Test cases generated! Switch to 'Generated Test Cases' tab.")
                except Exception as e:
                    st.error(f"❌ Generation failed: {e}")

# ══════════════════════════════════════════════════════════════════════
# TAB: Generated Test Cases
# ══════════════════════════════════════════════════════════════════════
with tab_output:
    st.subheader("📊 Generated Test Cases")
    if st.session_state.generated_output:
        st.markdown(st.session_state.generated_output)

        col_a, col_b = st.columns(2)
        with col_a:
            path = save_to_file(st.session_state.generated_output)
            st.success(f"💾 Saved to `{path}`")
            with open(path, "r", encoding="utf-8") as f:
                st.download_button(
                    "📥 Download as .md",
                    data=f.read(),
                    file_name=os.path.basename(path),
                    mime="text/markdown",
                    use_container_width=True,
                )
        with col_b:
            st.code(st.session_state.generated_output, language="markdown")
    else:
        st.info("👈 Generate test cases from the JIRA or Manual tab first.")