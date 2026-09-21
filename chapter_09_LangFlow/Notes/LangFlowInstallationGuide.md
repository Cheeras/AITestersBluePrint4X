# LangFlow Installation Guide — Local Setup (Windows)

> **Last Updated:** 21-Sep-2026  
> **LangFlow Version:** 1.12.2  
> **Python Version:** 3.13.3  
> **OS:** Windows

---

## Prerequisites

### 1. Install Python (if not already installed)

- Download Python from [python.org/downloads](https://www.python.org/downloads/)
- **Important:** During installation, check **"Add Python to PATH"**
- Verify installation:

```powershell
python --version
```

### 2. Create a Project Directory

```powershell
mkdir langflow-qa
cd langflow-qa
```

---

## Step 1: Install LangFlow

### Option A — Install directly (recommended for learning)

```powershell
pip install langflow
```

### Option B — Install inside a virtual environment (cleaner)

```powershell
pip install virtualenv
python -m venv venv
venv\Scripts\activate      # Activate virtual environment
pip install langflow
```

### Verify Installation

```powershell
pip show langflow
```

Expected output:
```
Name: langflow
Version: 1.12.2
Summary: A Python package with a built-in web application
```

---

## Step 2: Start LangFlow

### Basic Start Command

```powershell
python -m langflow run --host 127.0.0.1 --port 7860
```

> **Note:** If `langflow` command is not found in PATH, use `python -m langflow` instead.

### Available Options

| Option | Description | Default |
|--------|-------------|---------|
| `--host` | Host to bind the server to | `127.0.0.1` |
| `--port` | Port to listen on | `7860` |
| `--log-level` | Logging level (debug/info/warning/error) | `info` |
| `--no-store` | Disable store features (faster boot) | — |
| `--backend-only` | Run only backend without frontend | — |
| `--open-browser` | Auto-open browser after starting | — |
| `--env-file` | Path to `.env` file | — |

### Full Command with Options

```powershell
python -m langflow run --host 127.0.0.1 --port 7860 --log-level info
```

---

## Step 3: Access LangFlow UI

Once LangFlow starts successfully, you will see output like:

```
[OK] Open Langflow -> http://localhost:7860
```

Open **http://localhost:7860** in your browser.

> **Troubleshooting:** If the port shows differently (e.g., 7861, 7862), use that port instead. This happens when port 7860 is already in use.

---

## Step 4: Install Provider Packages (LLM Models)

LangFlow uses **lfx-bundles** for provider-specific components. Different LLM providers require different packages.

### Install All Provider Bundles

```powershell
pip install lfx-bundles
```

This installs support for: Groq, OpenAI, Anthropic, Google, Ollama, DeepSeek, Cohere, Azure, Amazon Bedrock, and many more.

### Install Individual Provider Packages (if needed)

| Provider | Package | Command |
|----------|---------|---------|
| Groq | `langchain-groq` | `pip install langchain-groq` |
| OpenAI | `langchain-openai` | `pip install langchain-openai` |
| Anthropic | `langchain-anthropic` | `pip install langchain-anthropic` |
| Ollama | (included in lfx-bundles) | — |
| Google | `langchain-google-genai` | `pip install langchain-google-genai` |

### Verify Provider Components

```powershell
python -c "from langflow.components import groq; print([x for x in dir(groq) if not x.startswith('_')])"
```

Expected output:
```
Groq components loaded: ['GroqModel']
```

---

## Step 5: Restart LangFlow After Installing Packages

After installing any new packages, **restart LangFlow** to pick them up:

1. **Stop LangFlow:** Press `Ctrl+C` in the terminal where LangFlow is running
2. **Or kill the process:**

```powershell
# Find and kill LangFlow process
netstat -ano | findstr :7860
# Note the PID, then:
taskkill /PID <PID> /F
```

3. **Start again:**

```powershell
python -m langflow run --host 127.0.0.1 --port 7860
```

---

## Step 6: Set Up Groq API Key

### Option A — Environment Variable (Recommended)

```powershell
# Set in current session
$env:GROQ_API_KEY="your-groq-api-key-here"

# Or set permanently via System Environment Variables
```

### Option B — Set in LangFlow UI

1. Open the flow editor
2. Click on the **Groq** node
3. In the **Groq API Key** field, paste your API key
4. Or create a **Variable** in LangFlow:
   - Go to **Settings → Variables**
   - Click **Add New**
   - Name: `GROQ_API_KEY`
   - Value: your API key

> **Get a Groq API Key:** Sign up at [console.groq.com](https://console.groq.com)

---

## Step 7: Create and Run Your First Flow

### Simple Chat Flow (Chat Input → Groq → Chat Output)

1. Open **http://localhost:7860**
2. Click **"Create a flow"** or **"New Project"**
3. From the **Bundles** tab (not Components), find **Groq**
4. Drag **Groq** onto the canvas
5. From **Components → Input & Output**, drag **Chat Input** and **Chat Output**
6. **Connect the nodes:**
   - Chat Input (output) → Groq (input)
   - Groq (output) → Chat Output (input)
7. **Configure the Groq node:**
   - **Groq API Key:** Enter your key (or select from variables)
   - **Model:** Select a model (e.g., `llama-3.1-8b-instant`)
8. Click **Playground** (bottom-right)
9. Type a message in the chat window and press Enter

---

## Troubleshooting

### 1. "langflow is not recognized as a command"

```powershell
# Use python module instead
python -m langflow run --host 127.0.0.1 --port 7860

# Or find the executable
Get-ChildItem $env:APPDATA\Python\Python313\Scripts\langflow.exe
```

### 2. "langchain-groq is not installed" error

```powershell
pip install langchain-groq
# Then restart LangFlow
```

### 3. Port already in use

```powershell
# Find what's using the port
netstat -ano | findstr :7860

# Kill the process
taskkill /PID <PID> /F

# Or use a different port
python -m langflow run --host 127.0.0.1 --port 7861
```

### 4. LangFlow hangs at "Starting Core Services..."

This is normal on first boot — it's loading components and running database migrations. Wait 1-2 minutes.

### 5. "Failed to start telemetry writer" warning

This is harmless. It means the telemetry writer couldn't start due to a Windows parameter issue. The app works fine without it.

### 6. 422 Error when creating a new flow

This happens when the `flow_id` parameter is invalid. Navigate to the Flows page first, then create from there.

### 7. Groq not showing in component search

Groq is under the **Bundles** tab, not **Components**. Click **Bundles** in the left sidebar to find it.

---

## Quick Reference — Common Commands

> **What is pip?** `pip` stands for **"Pip Installs Packages"** — it's the official package installer for Python. It downloads and installs packages from the [Python Package Index (PyPI)](https://pypi.org), which hosts over 500,000 Python packages.

```powershell
# Install LangFlow
pip install langflow

# Install provider bundles
pip install lfx-bundles

# Install Groq runtime dependency
pip install langchain-groq

# Start LangFlow
python -m langflow run --host 127.0.0.1 --port 7860

# Check installed version
pip show langflow

# Verify Groq component
python -c "from langflow.components import groq; print(dir(groq))"
```

---

## LangFlow CLI Commands

```powershell
# Show help
python -m langflow --help

# Run the server
python -m langflow run --host 127.0.0.1 --port 7860

# Run database migrations
python -m langflow migration --fix

# Create a superuser
python -m langflow superuser

# Create an API key
python -m langflow api-key
```

---

## Folder Structure (Recommended)

```
langflow-qa/
├── venv/                    # Virtual environment (optional)
├── data/                    # Database files (auto-created)
│   └── langflow.db
├── flows/                   # Exported flow JSON files
└── .env                     # Environment variables (API keys)
```

---

## Next Steps

1. Explore starter projects on the LangFlow dashboard
2. Try different LLM providers (OpenAI, Ollama for local models)
3. Export your flows as JSON for backup/sharing
4. Check the [LangFlow Documentation](https://docs.langflow.org)