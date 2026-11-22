# CrewAI Installation Guide

Short notes on prerequisites, installation, and verification.

---

## 0. Why Use a Virtual Environment?

Think of a virtual environment as a **separate toolbox** for each project, instead of throwing every tool into one giant pile.

### 🎯 What It Achieves

| Problem | Without Virtual Environment | With Virtual Environment |
|---------|:--------------------------:|:------------------------:|
| **Version conflicts** | Project A needs `Flask 2.x`, Project B needs `Flask 1.x` → ❌ Conflict | ✅ Each project gets its own isolated packages |
| **Global clutter** | `pip list` shows 200+ packages from every project ever tried | ✅ Only the packages needed for *this* project |
| **System Python breakage** | Accidentally upgrading a package breaks system tools | ✅ System Python stays clean — nothing affects it |
| **Reproducibility** | "It works on my machine" — but no one knows which versions | ✅ `requirements.txt` or `pyproject.toml` captures exact versions |
| **Clean uninstall** | Need to remove a project? Which packages were its dependencies? | ✅ Just delete the `.venv` folder — completely clean |

### 📦 Visual Comparison

```
❌ WITHOUT venv (one big toolbox)
C:\Python313\Lib\site-packages\
├── flask==1.0  ← Project A needs 2.0!
├── flask==2.0  ← ❌ Can't have both versions
├── django==3.2
├── pytest==7.0
├── crewai==1.0
├── numpy==1.24
└── ... (200+ packages, no idea what belongs to what)

✅ WITH venv (separate toolboxes per project)
Project_A\.venv\Lib\site-packages\
├── flask==2.0
└── pytest==7.0

Project_B\.venv\Lib\site-packages\
├── flask==1.0
└── requests==2.0

Chapter_16_CrewAI\.venv\Lib\site-packages\
├── crewai==1.15
├── crewai-tools==0.24
└── ... (only what this project needs)
```

### 🔑 Bottom Line

> **A virtual environment isolates each project's dependencies so different projects can use different package versions without conflicts, and your system Python stays untouched.**

---

## 1. Prerequisites (Before Installing)

### ✅ Python Version

CrewAI requires **Python >= 3.10 and < 3.14**.

```powershell
# Check your Python version
python --version
```

| Version | Supported? |
|:-------:|:----------:|
| 3.10 | ✅ Yes |
| 3.11 | ✅ Yes |
| 3.12 | ✅ Yes |
| 3.13 | ✅ Yes |
| 3.9 or lower | ❌ No |
| 3.14+ | ❌ No |

### ✅ Recommended: Use a Virtual Environment

Always install CrewAI inside a virtual environment to avoid conflicts with other projects.

#### Option A — Using `venv` (built-in)

```powershell
# Create virtual environment
python -m venv crewai_env

# Activate it
.\crewai_env\Scripts\Activate    # Windows PowerShell
```

#### Option B — Using `uv` (faster, recommended)

```powershell
# Check if uv is installed
uv --version

# Create virtual environment
uv venv

# Activate it
.venv\Scripts\Activate           # Windows PowerShell
```

If `uv` is not installed:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

---

## 2. Install CrewAI

### Basic Install

```powershell
# With pip
pip install crewai

# With uv (faster)
uv pip install crewai
```

### Install with Tools (Recommended for most use cases)

```powershell
# Includes crewai-tools for browser, file, and code tools
pip install 'crewai[tools]'

# With uv
uv pip install 'crewai[tools]'
```

---

## 3. Verify Installation

### Method 1 — pip show

```powershell
pip show crewai
```

**✅ If installed — output looks like:**
```
Name: crewai
Version: 1.15.44
Summary: Cutting-edge framework for orchestrating role-playing, autonomous AI agents.
Home-page: https://crewai.com
Author: Joao Moura
Location: C:\...\site-packages
```

**❌ If not installed:**
```
WARNING: Package(s) not found: crewai
```

### Method 2 — Try importing in Python

```powershell
python -c "import crewai; print(crewai.__version__)"
```

**✅ If installed — prints the version number:**
```
1.15.44
```

**❌ If not installed:**
```
ModuleNotFoundError: No module named 'crewai'
```

### Method 3 — pip list (search)

```powershell
pip list | findstr crewai
```

**✅ If installed:**
```
crewai             1.15.44
crewai-tools       0.24.0
```

**❌ If not installed — no output.**

### Method 4 — With uv

```powershell
uv pip show crewai
```

---

## 4. Quick Install & Verify (All-in-One)

```powershell
# 1. Create & activate venv
python -m venv crewai_env
.\crewai_env\Scripts\Activate

# 2. Install
pip install 'crewai[tools]'

# 3. Verify
python -c "import crewai; print(f'CrewAI {crewai.__version__} installed successfully')"
```

**Expected output:**
```
CrewAI 1.15.44 installed successfully
```

---

## 5. Troubleshooting

| Issue | Solution |
|-------|----------|
| `Python 3.13 not supported` | CrewAI supports `<3.14` — 3.13 is fine. Check your pip/uv version. |
| `pip: command not found` | Ensure Python is added to PATH. Use `python -m pip install crewai` |
| `uv: command not found` | Install uv: `powershell -c "irm https://astral.sh/uv/install.ps1 | iex"` |
| `ERROR: Failed building wheel` | Install Visual C++ build tools or use a pre-built wheel: `pip install crewai --only-binary :all:` |
| `ModuleNotFoundError` after install | Activate your virtual environment first, or you installed in a different venv |

---

## 6. File Locations

| Item | Typical Path |
|------|-------------|
| **Global site-packages** | `C:\Python313\Lib\site-packages\` |
| **uv cache** | `%LOCALAPPDATA%\uv\cache\` |
| **Venv site-packages** | `.venv\Lib\site-packages\` (inside your project) |