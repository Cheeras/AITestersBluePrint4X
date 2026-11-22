# Running First CrewAI Agent — Issues & Fixes

A detailed record of all issues encountered while running `test_01_analyst_AIAgent.py` for the first time, along with root causes and fixes applied.

---

## Issue 1 — `ModuleNotFoundError: No module named 'crewai'`

### ❌ Error

```
from crewai import Agent, Task, Crew
ModuleNotFoundError: No module named 'crewai'
```

### 🔍 Root Cause

CrewAI was **not installed** in the Python environment. The `.venv` folder existed but was created **without pip** (`python -m venv .venv` with no `--without-pip` flag, but the system had a broken pip setup). Running `pip install` outside the venv installed packages to the **global user site-packages** instead, so the activated venv couldn't find them.

### ✅ Fix

```powershell
# 1. Remove the broken .venv
Remove-Item -Recurse -Force .venv

# 2. Recreate the virtual environment (this time with pip)
python -m venv .venv

# 3. Install crewai inside the venv
.venv\Scripts\python.exe -m pip install 'crewai[tools]'
```

---

## Issue 2 — Wrong Parameter Names in `Crew()`

### ❌ Error

No explicit error, but the agent wouldn't execute properly.

### 🔍 Root Cause

The `Crew()` constructor expects **plural** parameter names:

```python
# ❌ Wrong
crew = Crew(
    agent=[qa_agent],    # Should be agents (plural)
    task=[test_case_create],  # Should be tasks (plural)
)

# ✅ Correct
crew = Crew(
    agents=[qa_agent],
    tasks=[test_case_create],
)
```

### ✅ Fix

Changed `agent` → `agents` and `task` → `tasks`.

---

## Issue 3 — Model Name Passed as Literal String Instead of Variable

### ❌ Error

```
Model `{os.getenv('groq_model')}` does not exist
```

The error shows `{os.getenv('GROQ_MODEL')}` as a literal string, not the resolved value.

### 🔍 Root Cause

The model parameter was using **double quotes** instead of an **f-string**:

```python
# ❌ Wrong — plain string, os.getenv() is NOT executed
model = "openai/{os.getenv('GROQ_MODEL')}",

# ✅ Correct — f-string, os.getenv() IS executed
model = f"openai/{os.getenv('GROQ_MODEL')}",
```

### ✅ Fix

Added the `f` prefix before the string to make it an f-string, so Python evaluates `{os.getenv('GROQ_MODEL')}` and substitutes the actual value.

---

## Issue 4 — Model Name `llama3-70b-8192` Was Decommissioned

### ❌ Error

```
The model `llama3-70b-8192` has been decommissioned and is no longer supported.
```

### 🔍 Root Cause

The `.env` file originally had `openai/gpt-oss-120b` (a valid Groq model). When troubleshooting Issue 3, the model was changed to `llama3-70b-8192`, but this model has been **decommissioned** by Groq.

### ✅ Fix

Reverted the `.env` back to the original model:

```
GROQ_MODEL = openai/gpt-oss-120b
```

This model is listed in Groq's **Production Models** page at https://console.groq.com/docs/models.

---

## Issue 5 — CrewAI Doesn't Have a Native `groq` Provider

### ❌ Error

```
Unable to initialize LLM with model 'groq/openai/gpt-oss-120b'.
The model did not match any supported native provider.
```

### 🔍 Root Cause

CrewAI's `LLM()` uses a **provider prefix** in the model name (`openai/`, `anthropic/`, `gemini/`, etc.). When `groq/` was used as the prefix, CrewAI didn't recognize it as a supported provider.

Groq's API is **OpenAI-compatible**, so the correct provider is `openai/` with the `base_url` pointing to Groq's endpoint.

### ✅ Fix

```python
# ❌ Wrong — groq is not a recognized provider
model = f"groq/{os.getenv('GROQ_MODEL')}",

# ✅ Correct — use openai provider with Groq's base URL
model = f"openai/{os.getenv('GROQ_MODEL')}",
base_url = "https://api.groq.com/openai/v1"
```

---

## Issue 6 — `IndentationError` Due to Duplicate Lines

### ❌ Error

```
IndentationError: unexpected indent
```

### 🔍 Root Cause

During multiple edits to the file, duplicate lines were accidentally introduced:

```python
groq_llm = LLM(
    model=f"openai/{os.getenv('GROQ_MODEL')}",
    api_key=os.getenv("GROQ_API_KEY"),   # ← Original
    base_url=os.getenv("GROQ_BASE_URL")  # ← Original
)
    api_key=os.getenv("GROQ_API_KEY"),   # ← Duplicate!
    base_url=os.getenv("GROQ_BASE_URL")  # ← Duplicate!
)
```

### ✅ Fix

Removed the duplicate lines.

---

## Issue 7 — `UnicodeEncodeError` on Windows Console

### ❌ Error

```
UnicodeEncodeError: 'charmap' codec can't encode character '\u2011' in position 539
```

### 🔍 Root Cause

The AI-generated test case output contained **Unicode characters** (like non-breaking hyphens `\u2011` and emoji). Windows terminal uses **cp1252 encoding** by default, which cannot encode all Unicode characters.

### ✅ Fix

```python
# Before
print(result)

# After — encode with UTF-8, replacing unsupported characters
print(result.raw if hasattr(result, 'raw') else str(result).encode('utf-8', errors='replace').decode('utf-8'))
```

---

## Final Working Configuration

### `.env` File

```env
GROQ_API_KEY = gsk_your_key_here
GROQ_MODEL = openai/gpt-oss-120b
GROQ_BASE_URL = https://api.groq.com/openai/v1
```

### Python Code (Key Part)

```python
load_dotenv()
groq_llm = LLM(
    model=f"openai/{os.getenv('GROQ_MODEL')}",
    api_key=os.getenv("GROQ_API_KEY"),
    base_url=os.getenv("GROQ_BASE_URL")
)

qa_agent = Agent(
    role="QA Engineer",
    goal="Analyse the feature and create 5-10 test cases.",
    backstory="Senior QA engineer with 15 years of experience",
    llm=groq_llm,
    verbose=True,
)

test_case_create = Task(
    description="Create 5-10 Testcase",
    expected_output="A numbered list of 5-10 test cases...",
    agent=qa_agent
)

crew = Crew(
    agents=[qa_agent],
    tasks=[test_case_create],
    verbose=True
)

result = crew.kickoff()
```

### Execution Command

```powershell
.venv\Scripts\python.exe test_01_analyst_AIAgent.py
```

---

## Summary of All Fixes

| # | Issue | Root Cause | Fix |
|:-:|-------|------------|-----|
| 1 | `ModuleNotFoundError: crewai` | .venv created without pip, crewai installed globally | Recreated .venv and installed crewai inside it |
| 2 | Wrong Crew params | Used `agent`/`task` instead of `agents`/`tasks` | Changed to plural parameter names |
| 3 | Model name as literal string | Missing `f` prefix on f-string | Added `f` prefix to evaluate `{os.getenv()}` |
| 4 | Model decommissioned | `llama3-70b-8192` no longer supported | Reverted to `openai/gpt-oss-120b` |
| 5 | Groq provider not recognized | Used `groq/` prefix instead of `openai/` | Changed to `openai/` prefix with Groq base URL |
| 6 | IndentationError | Duplicate lines from multiple edits | Removed duplicate lines |
| 7 | UnicodeEncodeError | Windows cp1252 can't encode Unicode | Used UTF-8 encoding with replacement in print |

---

## Lessons Learned

1. **Always use a virtual environment** — isolates dependencies per project.
2. **Check the `.venv` has pip** — recreate if `pip` is missing.
3. **CrewAI uses provider prefixes** — `openai/`, `anthropic/`, `gemini/`, etc. Groq is OpenAI-compatible, so use `openai/` prefix.
4. **f-strings vs plain strings** — `f"openai/{var}"` evaluates `{var}`, but `"openai/{var}"` keeps it literal.
5. **Windows console + Unicode** — Use `.encode('utf-8', errors='replace')` to handle Unicode safely.
6. **Check model availability** — Verify the model exists on the provider's docs before using it.