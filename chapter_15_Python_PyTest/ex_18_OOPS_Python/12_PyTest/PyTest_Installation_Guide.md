# PyTest Installation Guide

## Quick Install

```powershell
pip install pytest
```

Verify installation:

```powershell
pytest --version
```

---

## Global vs Virtual Environment vs VS Code Interpreter

Understanding these three concepts is key to avoiding import errors.

### Global Python Installation

- Installed when you first install Python from [python.org](https://python.org) or the Microsoft Store
- Located at a system path like `C:\Users\<user>\AppData\Local\Programs\Python\Python313\python.exe`
- Packages installed globally (e.g., `pip install pytest`) are available to **all projects** on your machine
- **Downside:** Different projects may need different versions of the same package — global install causes conflicts

### Virtual Environment (`.venv`)

- An **isolated copy** of Python created inside your project folder
- Located at `D:\Workspace\AITestersBluePrint4X\.venv\`
- Packages installed here are **only available to this project**
- **Benefit:** Each project gets its own dependencies — no version conflicts
- Created with: `python -m venv .venv`
- Activated with: `.venv\Scripts\activate` (you'll see `(.venv)` in the prompt)

### VS Code Python Interpreter

- VS Code doesn't automatically know which Python to use — you must **tell it**
- The selected interpreter determines:
  - Which packages VS Code can resolve for `import` statements
  - Which Python runs when you click the ▶️ Run button
  - Which diagnostics and IntelliSense suggestions you get
- You select it via: <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>P</kbd> → **Python: Select Interpreter**

### The Key Difference — Visualized

```
┌─────────────────────────────────────────────────┐
│                   YOUR MACHINE                   │
│                                                   │
│  ┌─────────────────────┐   ┌──────────────────┐  │
│  │  Global Python       │   │  Project A .venv │  │
│  │  C:\Python313\       │   │  Project\.venv\  │  │
│  │                      │   │                  │  │
│  │  Packages:           │   │  Packages:       │  │
│  │  ├── pytest 8.0      │   │  ├── pytest 9.1  │  │
│  │  ├── requests        │   │  └── requests    │  │
│  │  └── flask           │   │                  │  │
│  └─────────────────────┘   └──────────────────┘  │
│                                                   │
│  ┌──────────────────────────────────────────┐     │
│  │  VS Code — Select ONE Interpreter        │     │
│  │                                           │     │
│  │  If you pick → Global:                    │     │
│  │    import pytest  → ✅ resolves (8.0)     │     │
│  │                                           │     │
│  │  If you pick → .venv:                     │     │
│  │    import pytest  → ✅ resolves (9.1)     │     │
│  │                                           │     │
│  │  If .venv has NO pytest installed:        │     │
│  │    import pytest  → ❌ cannot resolve      │     │
│  └──────────────────────────────────────────┘     │
└─────────────────────────────────────────────────┘
```

### Why You Got the Error

| Layer | Python Used | Has pytest? | Result |
|---|---|---|---|
| **Terminal** (your `.venv`) | `.venv\Scripts\python.exe` | ❌ Not installed | `pip show pytest` → not found |
| **System PATH** (global) | `C:\Python313\python.exe` | ✅ Yes | `pytest --version` → works |
| **VS Code** (your `.venv`) | `.venv\Scripts\python.exe` | ❌ Not installed | `import pytest` → cannot resolve |

Your terminal's `pytest --version` found the **global** pytest on PATH, but VS Code was using the **`.venv`** interpreter which didn't have it. That's why the import failed.

### The Fix

**Option A — Install pytest in your `.venv` (recommended):**
```powershell
# Make sure (.venv) is active in your terminal
pip install pytest
```
Now both terminal and VS Code use the same `.venv` — import resolves.

**Option B — Switch VS Code to the global interpreter (not recommended):**
1. <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>P</kbd> → **Python: Select Interpreter**
2. Choose the global Python (e.g., `Python 3.13`)
3. ⚠️ This defeats the purpose of having a venv

---

## Common Pitfall: "Cannot resolve import pytest"

### The Scenario

You installed pytest, but VS Code still shows `import pytest` as unresolved.

### The Cause

Your terminal and VS Code are using **different Python interpreters**.

| Command | Result | Meaning |
|---|---|---|
| `pip show pytest` | `WARNING: Package(s) not found: pytest` | ❌ Not installed in the current venv |
| `pip list \| findstr pytest` | (empty) | ❌ Confirms — not in the venv |
| `pytest --version` | `pytest 9.1.1` | ✅ But this is a **global/system** pytest, not from your venv |

Your `.venv` doesn't have pytest, but a separate global installation exists on your PATH. VS Code uses the **`.venv` interpreter**, which can't find it — hence the import error.

### The Fix

Install pytest **inside your active venv**:

```powershell
# Make sure your venv is activated (you should see (.venv) in the prompt)
pip install pytest
```

After that, all commands will agree:

```powershell
pip show pytest          # ✅ Shows version & location inside .venv
pip list | findstr pytest  # ✅ Shows pytest in the list
pytest --version         # ✅ Still works (now from .venv)
```

### VS Code Interpreter Check

If the error persists, verify VS Code is using the correct interpreter:

1. Press <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>P</kbd>
2. Type **Python: Select Interpreter**
3. Choose the interpreter from your `.venv` folder

### How to Check the Location of `.venv`

The `.venv` is a **folder** (not a single file), typically created at your project root.

**Check if it exists in your project:**
```powershell
ls .venv
```

**Find where Python is currently running from (venv must be active):**
```powershell
python -c "import sys; print(sys.executable)"
```
If your venv is active, this shows a path like:
```
D:\Workspace\AITestersBluePrint4X\.venv\Scripts\python.exe
```

**Check pip's location (venv must be active):**
```powershell
pip -V
```
Output shows something like:
```
pip 24.x from D:\Workspace\AITestersBluePrint4X\.venv\Lib\site-packages\pip ...
```

**On Windows, `.venv` may be hidden — force list it:**
```powershell
ls -Force .venv
```

---

## Install Companion Packages (Optional)

```powershell
pip install pytest-html      # HTML test reports
pip install pytest-xdist     # Parallel test execution
pip install pytest-cov       # Code coverage
```

## Verify Everything Works

Create a simple test file `test_sample.py`:

```python
def test_pass():
    assert 1 + 1 == 2

def test_fail():
    assert 2 + 2 == 5
```

Run it:

```powershell
pytest test_sample.py -v
```

Expected output — one passed, one failed:

```
test_sample.py::test_pass PASSED
test_sample.py::test_fail FAILED
```