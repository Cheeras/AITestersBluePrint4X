# PIP vs UV — Complete Guide

## What is PIP?

**PIP** stands for **P**ip **I**nstalls **P**ackages. It is the **official** package installer for Python, included by default with Python 3.4+.

### Where PIP is Used

| Use Case | Example |
|---|---|
| Installing packages | `pip install requests` |
| Installing from requirements file | `pip install -r requirements.txt` |
| Uninstalling packages | `pip uninstall pytest` |
| Listing installed packages | `pip list` |
| Showing package details | `pip show pytest` |
| Upgrading packages | `pip install --upgrade pytest` |
| Freezing current environment | `pip freeze > requirements.txt` |

### How PIP Works

```
Python Package Index (PyPI)
     ┃  (https://pypi.org)
     ┃
     ▼
  pip install requests
     ┃
     ┃  Downloads the package
     ┃  Resolves dependencies
     ┃  Installs into site-packages
     ┃
     ▼
  Your Python Environment
  (site-packages/)
```

### Common PIP Commands

```powershell
# Install a package
pip install requests

# Install a specific version
pip install pytest==8.0.0

# Install with minimum version
pip install "pytest>=8.0"

# Install from requirements file
pip install -r requirements.txt

# List installed packages
pip list

# Show package details
pip show pytest

# Uninstall a package
pip uninstall pytest

# Upgrade a package
pip install --upgrade pytest

# Freeze current environment to file
pip freeze > requirements.txt

# Check for outdated packages
pip list --outdated
```

---

## What is UV?

**UV** is a **fast** Python package and project manager, built in **Rust**. It is a drop-in replacement for pip, pip-tools, pipenv, poetry, and virtualenv — all in one tool.

Created by the same team behind Ruff (the fast Python linter).

### Where UV is Used

| Use Case | Example |
|---|---|
| Installing packages (faster) | `uv pip install requests` |
| Creating virtual environments | `uv venv` |
| Running commands in venv | `uv run python script.py` |
| Managing projects | `uv init`, `uv add`, `uv sync` |
| Locking dependencies | `uv lock` |
| Replacing pip entirely | `uv pip install -r requirements.txt` |

### How UV Works

```
Python Package Index (PyPI)
     ┃
     ┃  ⚡ UV downloads in parallel
     ┃  ⚡ Uses HTTP caching aggressively
     ┃  ⚡ Resolves dependencies faster
     ┃
     ▼
  uv pip install requests
     ┃
     ┃  Much faster than pip
     ┃  (10x-100x speed improvement)
     ┃
     ▼
  Your Python Environment
  (site-packages/)
```

### Common UV Commands

```powershell
# Install a package (pip-compatible syntax)
uv pip install requests

# Create a virtual environment
uv venv

# Activate the venv (Windows)
.venv\Scripts\activate

# Run a script in the venv
uv run python script.py

# Initialize a new project
uv init my_project

# Add a dependency to the project
uv add pytest

# Sync environment with lock file
uv sync

# Generate a lock file
uv lock

# Install from requirements file
uv pip install -r requirements.txt

# List installed packages
uv pip list

# Show package details
uv pip show pytest
```

---

## Key Differences — PIP vs UV

| Aspect | PIP | UV |
|---|---|---|
| **Language** | Python | Rust |
| **Speed** | Slow (sequential downloads) | ⚡ Fast (parallel downloads, aggressive caching) |
| **Built-in venv** | ❌ No (uses `venv` module) | ✅ Yes (`uv venv`) |
| **Project management** | ❌ No (needs Poetry/Pipenv) | ✅ Yes (`uv init`, `uv add`, `uv sync`) |
| **Lock file** | ❌ No (uses `requirements.txt`) | ✅ Yes (`uv.lock`) |
| **Drop-in replacement** | — | ✅ Yes (`uv pip` mirrors `pip`) |
| **Part of Python stdlib** | ✅ Yes (included with Python) | ❌ No (must install separately) |
| **Caching** | Basic | Aggressive (HTTP + global cache) |
| **Parallel downloads** | ❌ No | ✅ Yes |
| **Resolution algorithm** | SAT solver (slow) | Pubgrub (fast, same as Poetry) |

---

## Speed Comparison

| Operation | PIP | UV | Speedup |
|---|---|---|---|
| Install `requests` (cold cache) | ~3-5s | ~0.3s | **10-15x** |
| Install `numpy` (cold cache) | ~30-60s | ~3-5s | **10-12x** |
| Install from `requirements.txt` (50 packages) | ~60-120s | ~5-10s | **10-15x** |
| Resolve dependencies | ~5-10s | ~0.5-1s | **10x** |

---

## When to Use Which

### Use PIP when...

- ✅ You want the **official** Python package manager (no extra install)
- ✅ You are on a **restricted** system where you cannot install new tools
- ✅ You need **maximum compatibility** with CI/CD systems
- ✅ You are working on a **simple script** with few dependencies
- ✅ You want the **most widely documented** approach

### Use UV when...

- ✅ You want **10x-100x faster** package installation
- ✅ You need a **single tool** for venv + packages + project management
- ✅ You are starting a **new project** and want modern tooling
- ✅ You work with **large requirements files** (50+ packages)
- ✅ You want **deterministic builds** with lock files
- ✅ You are tired of slow `pip install` in CI/CD pipelines

---

## Installation

### Install PIP

PIP comes with Python by default. To verify:

```powershell
pip --version
```

If missing, install it:

```powershell
python -m ensurepip --upgrade
```

### Install UV

```powershell
# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Or via pip
pip install uv

# Verify
uv --version
```

---

## Practical Examples Side by Side

### Creating a Virtual Environment

```powershell
# PIP way
python -m venv .venv
.venv\Scripts\activate

# UV way
uv venv
.venv\Scripts\activate
```

### Installing Packages

```powershell
# PIP way
pip install requests pytest

# UV way
uv pip install requests pytest
```

### Installing from Requirements

```powershell
# PIP way
pip install -r requirements.txt

# UV way
uv pip install -r requirements.txt
```

### Freezing Dependencies

```powershell
# PIP way
pip freeze > requirements.txt

# UV way
uv pip freeze > requirements.txt
```

---

## Summary

```
┌─────────────────────────────────────────────────────┐
│                                                     │
│   PIP                          UV                   │
│   ───                          ──                   │
│   Official Python tool         Rust-based speedster │
│   Slow but reliable            10-100x faster       │
│   Package installer only       Package + project    │
│   No lock file                 Lock file support    │
│   Comes with Python            Must install         │
│                                                     │
│   Use PIP for:                 Use UV for:          │
│   • Simple scripts             • Large projects     │
│   • Restricted systems         • Fast CI/CD         │
│   • Maximum compatibility      • Modern workflows   │
│                                                     │
└─────────────────────────────────────────────────────┘
```

> **Bottom line:** PIP is the standard that works everywhere. UV is the modern, blazing-fast alternative. You can use both side by side — UV's `uv pip` commands are fully compatible with pip's syntax.