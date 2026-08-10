## Comprehensive Architecture Plan — Local TestCase Generator

---

### 1. Overview

**Project**: Local TestCase Generator — A Python web application that fetches requirements from JIRA, combines them with a QA prompt template, and sends them to an LLM (Ollama locally or Groq cloud API) to generate structured test cases.

**Tech Stack**: Python 3.11+, Streamlit (web UI), Ollama (local LLM), Groq API (cloud LLM), Atlassian JIRA REST API

---

### 2. Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Streamlit Web UI                       │
│  ┌──────────┐  ┌──────────────┐  ┌───────────────────┐  │
│  │ JIRA Tab │  │ Requirements │  │ Generated TC      │  │
│  │ (fetch)  │  │ Tab (manual) │  │ Output Tab        │  │
│  └──────────┘  └──────────────┘  └───────────────────┘  │
└──────────┬──────────┬────────────────┬──────────────────┘
           │          │                │
┌──────────▼──┐ ┌─────▼──────┐ ┌──────▼──────────────────┐
│ JIRA Client │ │ Requirement│ │    LLM Service Layer     │
│ (atlassian- │ │ Reader     │ │  ┌────────────────────┐  │
│  python-api)│ │ (text/file)│ │  │ OllamaProvider     │  │
└──────┬──────┘ └────────────┘ │  │ (local llama3)     │  │
       │                       │  ├────────────────────┤  │
       │                       │  │ GroqProvider       │  │
       │                       │  │ (cloud mixtral)    │  │
       │                       │  └────────┬───────────┘  │
       │                       └───────────┼──────────────┘
       │                                   │
┌──────▼───────────────────────────────────▼──────────────┐
│              Prompt Builder                             │
│  Template (testcase_creator.md) + Requirements          │
│  → Final Prompt with Anti-Hallucination Rules           │
└─────────────────────────────────────────────────────────┘
```

---

### 3. File Structure (to be created)

```
chapter_03_Local_TC_Generator/
└── Task1_10Aug_Local_TestCaseGenerator/
    ├── .env                          # Secrets (JIRA token, Groq key) — NEVER commit
    ├── .env.example                  # Template for .env without real secrets
    ├── requirements.txt              # Python dependencies
    ├── app.py                        # Streamlit entry point
    ├── src/
    │   ├── __init__.py
    │   ├── resources/
    │   │   ├── plan.md               # THIS FILE
    │   │   ├── Prompt.md             # Filled with final prompt (will populate)
    │   │   ├── Finetune_Prompt.md    # Filled with finetuning prompt (will populate)
    │   │   └── RoughDiagramofLocalTestcaseGenerator.png
    │   ├── jira_client.py            # JIRA REST API wrapper
    │   ├── llm_service.py            # LLM abstraction (Ollama + Groq)
    │   ├── prompt_builder.py         # Builds final prompt from template + requirements
    │   └── output_handler.py         # Formats & saves generated test cases
    ├── templates/
    │   └── testcase_creator.md       # Already exists — QA prompt template
    └── output/                       # Generated test case outputs
        └── .gitkeep
```

---

### 4. Step-by-Step Implementation

#### Phase 1: Environment & Config

**Step 1** — Create `.env` and `.env.example`

- `.env` stores: `JIRA_URL`, `JIRA_EMAIL`, `JIRA_API_TOKEN`, `GROQ_API_KEY`, `OLLAMA_MODEL`, `GROQ_MODEL`
- `.env.example` is the same but with placeholder values
- Use `python-dotenv` to load at runtime
- **Critical**: Add `.env` to .gitignore

**Step 2** — Create `requirements.txt`

```
streamlit==1.31.0
python-dotenv==1.0.0
requests==2.31.0
groq==0.4.0
ollama==0.1.8
atlassian-python-api==3.41.0
```

**Step 3** — Create .gitignore

```
.env
__pycache__/
*.pyc
output/
.venv/
```

---

#### Phase 2: Core Services (parallel — Steps 4, 5, 6)

**Step 4** — `src/jira_client.py` — JIRA Integration

- Class `JIRAClient` with methods:
  - `__init__(url, email, api_token)` — reads from env vars
  - `fetch_issue(issue_key)` — gets single issue by key (e.g., `PROJ-123`)
  - `fetch_issues_by_query(jql)` — gets issues by JQL query
  - `extract_requirements(issue)` — extracts description/acceptance criteria as text
- Uses `atlassian-python-api` library
- Error handling for auth failures, network timeouts, invalid issues

**Step 5** — `src/llm_service.py` — LLM Abstraction Layer

- Abstract class/interface `LLMProvider` with method `generate(prompt: str) -> str`
- `OllamaProvider`:
  - Calls local Ollama API at `http://localhost:11434/api/generate`
  - Configurable model (default: `llama3`)
  - Streaming response support
- `GroqProvider`:
  - Uses Groq Python SDK with API key
  - Model: `mixtral-8x7b-32768` (free tier)
  - Handles rate limiting (1M tokens/day)
- `LLMService` factory that selects provider based on config

**Step 6** — `src/prompt_builder.py` — Prompt Construction

- Reads `templates/testcase_creator.md`
- Replaces `[NUMBER]` with intelligent estimate based on requirement size
- Replaces `[FEATURE]` with feature name extracted from JIRA/reference
- Replaces `[PASTE REQUIREMENTS HERE]` with actual requirements
- Appends anti-hallucination rules from ANTI-HALLUCINATION.rules.md
- Returns final prompt string

---

#### Phase 3: Streamlit UI

**Step 7** — `app.py` — Main Streamlit Application

Three tabs:

**Tab 1: "Fetch from JIRA"**

- Input fields: JIRA Issue Key, or JQL query
- "Fetch Requirements" button → calls `JIRAClient.fetch_issue()`
- Displays fetched requirements in a text area (editable)
- "Generate Test Cases" button → triggers full pipeline

**Tab 2: "Manual Requirements"**

- Large text area for pasting requirements directly
- "Generate Test Cases" button → same pipeline without JIRA

**Tab 3: "Generated Test Cases"**

- Radio button: Ollama / Groq (LLM selection)
- Displays generated test cases in a markdown table
- "Download as .md" button
- "Copy to Clipboard" button

---

#### Phase 4: Pipeline Integration

**Step 8** — `src/output_handler.py` — Output Management

- `save_to_file(content, filename)` — saves to `output/` folder with timestamp
- `format_as_markdown(raw_response)` — parses LLM response into clean markdown table
- `validate_test_cases(markdown)` — checks minimum columns (ID, Description, etc.)

**Step 9** — Wire everything in `app.py`

Flow:

1. User provides requirements (JIRA or manual)
2. `PromptBuilder.build_prompt(requirements)` → final prompt
3. `LLMService.generate(prompt)` → raw LLM response
4. `OutputHandler.format_as_markdown(response)` → formatted test cases
5. Display in Streamlit + offer download

---

#### Phase 5: Polish & Documentation

**Step 10** — Fill `Prompt.md` — Document the final prompt template used by the app with examples

**Step 11** — Fill `Finetune_Prompt.md` — Document the finetuning strategy for improving LLM outputs

**Step 12** — Update README.md in repository root with Chapter 3 link

---

### 5. Environment Variables (`.env`)

| Variable           | Purpose                | Source                                     |
| ------------------ | ---------------------- | ------------------------------------------ |
| `JIRA_URL`       | Atlassian instance URL | JIRA Cloud setup                           |
| `JIRA_EMAIL`     | Account email          | JIRA account                               |
| `JIRA_API_TOKEN` | API token for auth     | JIRA token API                             |
| `GROQ_API_KEY`   | Groq cloud API key     | console.groq.com/keys                      |
| `OLLAMA_MODEL`   | Ollama model name      | Local Ollama install (default:`llama3`)  |
| `GROQ_MODEL`     | Groq model name        | Groq docs (default:`mixtral-8x7b-32768`) |

---

### 6. Verification

1. **Unit Tests (manual)**: Run `app.py` and test each tab independently
2. **JIRA Integration**: Enter a valid JIRA issue key from `shankar-ch.atlassian.net`, verify requirements are fetched
3. **Ollama Integration**: Select Ollama, verify test cases are generated (requires Ollama running locally)
4. **Groq Integration**: Select Groq, verify test cases are generated using cloud API
5. **Output Validation**: Verify generated test cases match the template format (7 columns, anti-hallucination rules applied)
6. **Error Handling**: Test with invalid JIRA keys, network offline, and empty requirements

---

### 7. Known Decisions

- **BLAST Framework** mentioned in Task2.txt is not a recognized Python framework — using **Streamlit** instead (best fit for a simple web UI with minimal boilerplate)
- Ollama model defaults to `llama3` (most capable open-source model for test case generation)
- Groq free tier model: `mixtral-8x7b-32768` (1M tokens/day free)
- JIRA credentials and Groq key go in `.env` — **never committed to git**
