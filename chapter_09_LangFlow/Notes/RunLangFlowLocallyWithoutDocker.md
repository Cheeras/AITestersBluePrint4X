# Run LangFlow Locally Without Docker — Step-by-Step Guide

> **Created:** 26-Sep-2026
> **LangFlow Version:** 1.12.2
> **Python Version:** 3.13.3
> **OS:** Windows
> **Scenario:** LangFlow is already installed via pip (no Docker, no container)

---

## Table of Contents

1. [Prerequisites Check](#1-prerequisites-check)
2. [Activate the Python Environment](#2-activate-the-python-environment)
3. [Verify LangFlow Installation](#3-verify-langflow-installation)
4. [Check if Port 7860 Is Free](#4-check-if-port-7860-is-free)
5. [Start LangFlow](#5-start-langflow)
6. [Verify LangFlow Is Running](#6-verify-langflow-is-running)
7. [Access the LangFlow UI](#7-access-the-langflow-ui)
8. [Troubleshooting — Startup Stalls or Delays](#8-troubleshooting--startup-stalls-or-delays)
9. [Troubleshooting — Port Already in Use](#9-troubleshooting--port-already-in-use)
10. [Troubleshooting — Duplicate Processes](#10-troubleshooting--duplicate-processes)
11. [Stopping LangFlow](#11-stopping-langflow)
12. [Quick-Start One-Liner](#12-quick-start-one-liner)

---

## 1. Prerequisites Check

Before starting, ensure the following are available on your system:

| Requirement            | Check Command                             |
| ---------------------- | ----------------------------------------- |
| Python 3.10+ installed | `python --version`                      |
| pip available          | `pip --version`                         |
| LangFlow installed     | `pip show langflow`                     |
| Port 7860 free         | See[Step 4](#4-check-if-port-7860-is-free) |

**Important:** LangFlow runs as a native Python application. Docker is **not required**. It uses Uvicorn (an ASGI server) internally and binds to `http://127.0.0.1:7860`.

---

## 2. Activate the Python Environment

If you are using a virtual environment (recommended), activate it first.

**PowerShell (Windows):**

```powershell
# If your venv is inside the project folder
.\venv\Scripts\Activate.ps1

# Or if a different venv path
& "D:\Workspace\AITestersBluePrint4X\.venv\Scripts\Activate.ps1"
```

**Command Prompt (Windows):**

```cmd
venv\Scripts\activate
```

**Git Bash / WSL (Linux/macOS):**

```bash
source venv/bin/activate
```

> After activation, your terminal prompt will show `(venv)` at the beginning.

---

## 3. Verify LangFlow Installation

Run these checks to confirm LangFlow is installed and find its version:

### 3.1 Check package metadata

```powershell
pip show langflow
```

Expected output (version may differ):

```
Name: langflow
Version: 1.12.2
Summary: A Python package with a built-in web application
```

### 3.2 Check LangFlow CLI

```powershell
python -m langflow --version
```

Expected output:

```
langflow 1.12.2
```

> **Note:** Use `python -m langflow` instead of the bare `langflow` command if the executable is not in your PATH.

### 3.3 (Optional) View all available CLI options

```powershell
python -m langflow run --help
```

This lists every startup flag (host, port, workers, backend-only mode, SSL, log level, etc.).

---

## 4. Check if Port 7860 Is Free

LangFlow's default port is **7860**. Verify no other process is already listening on it.

### 4.1 Using PowerShell

```powershell
Get-NetTCPConnection -LocalPort 7860 -State Listen -ErrorAction SilentlyContinue
```

- **No output** → Port is free. Proceed to start.
- **Output shows a process** → Port is occupied. Either kill that process or use a different port (e.g., `--port 7861`).

### 4.2 Using Command Prompt

```cmd
netstat -ano | findstr :7860
```

### 4.3 Identify the process using the port

```powershell
Get-NetTCPConnection -LocalPort 7860 -ErrorAction SilentlyContinue |
    Select-Object LocalAddress, LocalPort, OwningProcess
```

If a process owns port 7860, you can see its PID. To identify the process:

```powershell
Get-Process -Id <PID> | Select-Object Id, ProcessName, StartTime
```

---

## 5. Start LangFlow

### 5.1 Basic start command

```powershell
python -m langflow run --host 127.0.0.1 --port 7860
```

This starts LangFlow on `http://127.0.0.1:7860`.

### 5.2 Start with common options

```powershell
python -m langflow run --host 127.0.0.1 --port 7860 --log-level info --no-store
```

| Flag                 | Purpose                                                   |
| -------------------- | --------------------------------------------------------- |
| `--host 127.0.0.1` | Bind only to localhost (secure for local dev)             |
| `--port 7860`      | Use port 7860 (you can change if busy)                    |
| `--log-level info` | Show informational log messages                           |
| `--no-store`       | Disable store features (can speed up first boot slightly) |
| `--open-browser`   | Auto-open browser after startup                           |

### 5.3 Start with debug logging (for troubleshooting)

```powershell
python -m langflow run --host 127.0.0.1 --port 7860 --log-level debug
```

Debug mode shows detailed logs including:

- Which services are initializing
- Which components and bundles are being loaded
- Database connection details
- Any missing optional dependencies (these are warnings, not errors)

### 5.4 What to expect during startup

LangFlow goes through several initialization phases:

```
[transformers] PyTorch was not found. Models won't be available...   ← benign warning
+ Initializing Langflow                                              ← core startup
+ Checking Environment                                               ← configuration check
| Starting Core Services...                                          ← service initialization
  (CORS warnings — safe to ignore for local dev)
+ Starting Core Services (≈30s)
+ Connecting Database (≈2s)
+ Loading Components                                                  ← component discovery
+ Adding Starter Projects                                             ← starter templates
- Launching Langflow...                                               ← final setup
┌─────────────────────────────────────────────────────────────────────┐
│  [OK] Open Langflow -> http://localhost:7860                       │
└─────────────────────────────────────────────────────────────────────┘
INFO:     Uvicorn running on http://127.0.0.1:7860
```

> **Total first startup time can take 60–90 seconds** because LangFlow discovers and caches all components and bundles. Subsequent restarts are faster. Subsequent restarts are typically 15–30 seconds.

---

## 6. Verify LangFlow Is Running

Once the terminal shows the `[OK]` message and Uvicorn line, confirm the server is reachable.

### 6.1 HTTP check (PowerShell)

```powershell
Invoke-WebRequest -Uri http://127.0.0.1:7860 -TimeoutSec 10
```

Expected output: `HTTP 200`

### 6.2 HTTP check (Command Prompt)

```cmd
curl http://127.0.0.1:7860
```

### 6.3 Verify the listening port

```powershell
Get-NetTCPConnection -State Listen -LocalPort 7860
```

Expected output:

```
LocalAddress  LocalPort  OwningProcess
------------  ---------  -------------
127.0.0.1     7860       <PID>
```

### 6.4 Verify the Python process

```powershell
Get-CimInstance Win32_Process -Filter "name = 'python.exe'" |
    Select-Object ProcessId, CommandLine
```

Look for a command line containing `-m langflow run`. The process should show non-trivial CPU and memory usage:

```powershell
Get-Process -Id <PID> | Select-Object Id, StartTime, CPU, WorkingSet64, Responding
```

---

## 7. Access the LangFlow UI

Open your browser and navigate to:

```
http://localhost:7860
```

You should see the LangFlow welcome screen with options to:

- **Create a new flow** — Build AI agent workflows visually
- **Open an existing flow** — Import or resume saved flows
- **Explore starter projects** — Pre-built templates to learn from
- **Access the Playground** — Test flows interactively

---

## 8. Troubleshooting — Startup Stalls or Delays

### Symptom: Terminal shows "Starting Core Services..." but nothing happens for minutes

**Cause:** First-time component caching, bundle loading, and database initialization can take 60–90 seconds. This is normal.

**What to do:**

1. **Wait longer.** Do not kill the process for at least 2 minutes.
2. If still stuck, restart with debug logging to see where it's hanging:

```powershell
python -m langflow run --host 127.0.0.1 --port 7860 --log-level debug
```

3. Common slow phases visible in debug mode:
   - `Building components cache` — scanning all installed bundles
   - `Caching types` — serializing type metadata
   - `Connecting Database` — SQLite migrations
   - `Adding Starter Projects` — creating starter templates for the default user

### Symptom: LangFlow starts but browser shows "Connection refused"

**Cause:** The startup sequence printed the `[OK]` message before Uvicorn fully finished binding.

**Solution:** Wait 10–15 seconds after the `[OK]` message and try again.

---

## 9. Troubleshooting — Port Already in Use

### Symptom: `Address already in use` error when starting

### Solution A — Use a different port

```powershell
python -m langflow run --host 127.0.0.1 --port 7861
```

### Solution B — Kill the process on the port

Find and kill the process:

```powershell
# Find the process
$connection = Get-NetTCPConnection -LocalPort 7860 -ErrorAction SilentlyContinue
$connection | Select-Object LocalAddress, LocalPort, OwningProcess
$pid = $connection.OwningProcess

# Kill it
Stop-Process -Id $pid -Force

# Verify it's gone
Get-Process -Id $pid -ErrorAction SilentlyContinue
```

Or with Command Prompt:

```cmd
netstat -ano | findstr :7860
taskkill /PID <PID> /F
```

---

## 10. Troubleshooting — Duplicate Processes

### Symptom: Multiple LangFlow processes are running (e.g., from previous failed starts)

### Identify all LangFlow processes

```powershell
Get-CimInstance Win32_Process -Filter "name = 'python.exe'" |
    Select-Object ProcessId, CommandLine |
    Where-Object { $_.CommandLine -match "langflow" }
```

### List which processes own which ports

```powershell
Get-NetTCPConnection -State Listen -ErrorAction SilentlyContinue |
    Where-Object { $_.LocalPort -in 7860,7861,7862 } |
    Select-Object LocalAddress, LocalPort, OwningProcess
```

### Kill all LangFlow processes

```powershell
Get-CimInstance Win32_Process -Filter "name = 'python.exe'" |
    Where-Object { $_.CommandLine -match "langflow" } |
    ForEach-Object { Stop-Process -Id $_.ProcessId -Force }
```

---

## 11. Stopping LangFlow

### Method A — Graceful shutdown (from the terminal where LangFlow is running)

Press `Ctrl+C` in the terminal. LangFlow will shut down cleanly.

### Method B — Kill by process ID

```powershell
# Find the PID of the LangFlow process
Get-CimInstance Win32_Process -Filter "name = 'python.exe'" |
    Where-Object { $_.CommandLine -match "langflow run" }

# Kill it
Stop-Process -Id <PID> -Force
```

### Method C — Kill by port (if you know the port)

```powershell
$pid = (Get-NetTCPConnection -LocalPort 7860).OwningProcess
Stop-Process -Id $pid -Force
```

---

## 12. Quick-Start One-Liner

If LangFlow is already installed and you are in the correct Python environment, this single command is all you need:

```powershell
python -m langflow run --host 127.0.0.1 --port 7860
```

Then open **http://localhost:7860** in your browser.

---

## Summary of Commands Used in This Session

| Step | Command                                                 | Purpose                          |
| ---- | ------------------------------------------------------- | -------------------------------- |
| 1    | `python --version`                                    | Verify Python availability       |
| 2    | `Get-NetTCPConnection -LocalPort 7860 -State Listen`  | Check port availability          |
| 3    | `python -m langflow run --host 127.0.0.1 --port 7860` | Start LangFlow                   |
| 4    | `Invoke-WebRequest -Uri http://127.0.0.1:7860`        | Verify LangFlow is serving       |
| 5    | `Get-Process python`                                  | Inspect running LangFlow process |
| 6    | `Get-NetTCPConnection -LocalPort 7860`                | Confirm listening socket         |
| 7    | `Stop-Process -Id <PID> -Force`                       | Stop a LangFlow instance         |

---

## Key Takeaways

1. **No Docker needed** — LangFlow is a pure Python package (`pip install langflow`).
2. **First startup is slow** (60–90s) due to component caching; subsequent starts are faster.
3. **Use `--log-level debug`** to diagnose startup issues.
4. **Port 7860 is the default** — use `--port` to change it if busy.
5. **Always activate your virtual environment** before running `python -m langflow`.
6. **LangFlow automatically opens the SQLite database** at `%APPDATA%\Python\Python313\site-packages\langflow\langflow.db` — no separate database server needed.
