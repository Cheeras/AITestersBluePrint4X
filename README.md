# AI Testers Blueprint 4X

AI Testers Blueprint 4X is a hands-on learning repository for software testers who want to use generative AI in testing workflows. It combines foundational notes, reusable prompt-engineering templates, and practical test-automation examples.

## Learning Roadmap

The complete learning path is available in the [AI Tester Blueprint roadmap](RoadMap/AITesterBluePrintRoadMap.png).

## Repository Contents

### Chapter 0: 30-Day Challenge — Mastering AI Testing for QA Engineers

A 9-day foundational series covering the essentials of AI-assisted testing.

| Day | Topic |
|---|---|
| [Day 1](chapter_00_30DayChallengeMastering_AITesting_For_QA_Engineers/Day1.md) | Introduction to AI in Testing |
| [Day 2](chapter_00_30DayChallengeMastering_AITesting_For_QA_Engineers/Day2.md) | Prompt Engineering Basics |
| [Day 3](chapter_00_30DayChallengeMastering_AITesting_For_QA_Engineers/Day3.md) | Test Case Generation with AI |
| [Day 4](chapter_00_30DayChallengeMastering_AITesting_For_QA_Engineers/Day4.md) | Bug Analysis & Reporting |
| [Day 5](chapter_00_30DayChallengeMastering_AITesting_For_QA_Engineers/Day5.md) | AI for Test Automation |
| [Day 6](chapter_00_30DayChallengeMastering_AITesting_For_QA_Engineers/Day6.md) | AI Agents in Testing |
| [Day 7](chapter_00_30DayChallengeMastering_AITesting_For_QA_Engineers/Day7.md) | RAG & Advanced Topics |
| [Day 8](chapter_00_30DayChallengeMastering_AITesting_For_QA_Engineers/Day8.md) | Connecting AI to the Real QA Ecosystem |
| [Day 9](chapter_00_30DayChallengeMastering_AITesting_For_QA_Engineers/Day9.md) | LangFlow & LangChain — Visual AI Agent Builders |

### Chapter 1: LLM Basics

- [Anti-hallucination rules](chapter_01_LLMBasics/ANTI-HALLUCINATION.rules.md) for producing more reliable, evidence-based AI responses.

### Chapter 2: Prompt Engineering

- [Salesforce login automation task](chapter_02_prompt_eng/00_Task1.md)
- [RICE-POT prompt template](chapter_02_prompt_eng/01_RICE_POT_Template.md)
- [RICE-POT example](chapter_02_prompt_eng/02_RICE_POT.example.md)
- [Enterprise Selenium framework plan](chapter_02_prompt_eng/04_Plan_Framework.md)
- [Salesforce Selenium automation framework](chapter_02_prompt_eng/RICE_POT_SeleniumAdvancedFramework/)
- [Enterprise VWO Login Test Plan](chapter_02_prompt_eng/prompt_templates/app_vwo_testplan.md) — Comprehensive enterprise-grade test plan for the VWO login dashboard, aligned with PRD requirements
- [Test Cases — Login & Registration](chapter_02_prompt_eng/Task1_9thAug_TestCasesCreation_UsingLocalLLMOllama/testcase.md) — Markdown-formatted test cases for login and registration flows

#### Prompt Templates

Ready-to-use prompt templates for various QA workflows:

| Template | Description |
|---|---|
| [API Test Case Generator](chapter_02_prompt_eng/prompt_templates/apitestcasegenerator.md) | Generate API test cases from endpoint specs |
| [Bug Analysis](chapter_02_prompt_eng/prompt_templates/bugananlysis.md) | Analyze and triage bug reports |
| [Bug Classification](chapter_02_prompt_eng/prompt_templates/bugclassification.md) | Classify bugs by severity, priority, and component |
| [Bug Report from Issue](chapter_02_prompt_eng/prompt_templates/bugreportfromissue.md) | Convert raw issues into structured bug reports |
| [Convert Notes to Bug Report](chapter_02_prompt_eng/prompt_templates/convertnotestoBugReport.md) | Transform informal notes into formal bug reports |
| [Negative Test Case Generator](chapter_02_prompt_eng/prompt_templates/negativetestcase.md) | Generate negative/edge-case test scenarios |
| [PRD to Test Case](chapter_02_prompt_eng/prompt_templates/prdtotestcase.md) | Convert product requirements into test cases |
| [Regression Test Case](chapter_02_prompt_eng/prompt_templates/regressiontestcase.md) | Generate regression test suites |
| [Test Case Creator](chapter_02_prompt_eng/prompt_templates/testcase_creator.md) | General-purpose test case generation |

## RICE-POT Prompting Framework

RICE-POT is a reusable structure for writing clear and complete prompts.

| Element | Meaning | Guiding question |
| --- | --- | --- |
| **R** | Role | Who should the AI act as? |
| **I** | Instructions | What should the AI do? |
| **C** | Context | What background information does it need? |
| **E** | Examples | What does a good result look like? |
| **P** | Parameters | What rules or constraints apply? |
| **O** | Output | How should the response be structured? |
| **T** | Tone | How should the response sound? |

Use only the elements that add useful clarity. A compact prompt can follow this structure:

```text
Role: Act as a [role or subject-matter expert].
Instructions: [Describe the task with clear action verbs.]
Context: [Provide the objective, audience, and relevant background.]
Examples: [Show one or more examples of the desired result.]
Parameters: [List inclusions, exclusions, limits, and constraints.]
Output: Return the answer as [table, checklist, JSON, report, code, etc.].
Tone: Use a [professional, friendly, technical, concise, etc.] tone.
```

## Salesforce Selenium Framework

The Chapter 2 example applies the RICE-POT plan to an enterprise-style Salesforce login test suite built with:

- Java 11 and Maven
- Selenium WebDriver and WebDriverManager
- TestNG with data-driven valid and invalid login scenarios
- Page Object Model with PageFactory
- Chrome, Firefox, and Edge execution
- Extent Reports, Log4j2 logging, and failure screenshots
- Thread-local WebDriver management for parallel execution

### Project Structure

```text
RICE_POT_SeleniumAdvancedFramework/
|-- pom.xml
|-- testng.xml
`-- src/test/
    |-- java/com/salesforce/qa/
    |   |-- base/
    |   |-- listeners/
    |   |-- pages/
    |   |-- testdata/
    |   |-- tests/
    |   `-- utils/
    `-- resources/
        |-- config.properties
        `-- log4j2.xml
```

### Prerequisites

- JDK 11 or later
- Apache Maven 3.8 or later
- Chrome, Firefox, or Edge installed for the selected test suite
- Valid Salesforce test credentials for the positive login scenario

### Configure and Run

1. Open `src/test/resources/config.properties` inside the framework directory.
2. Replace `${username}` and `${password}` with credentials for a dedicated Salesforce test account. Never commit real credentials.
3. From the framework directory, run:

```bash
mvn clean test
```

The default `testng.xml` suite runs valid and invalid login tests in Chrome, Firefox, and Edge. Generated logs, Maven build output, and HTML test reports are excluded from version control.

## Chapter 3: Local TestCase Generator

A Python-based Streamlit web application that generates structured test cases from JIRA issues or manual requirements using local (Ollama) or cloud (Groq) LLMs.

### Features

- **JIRA Integration** — Fetch requirements directly from JIRA issues using the REST API
- **Manual Input** — Paste requirements directly for quick test case generation
- **Dual LLM Support** — Choose between local Ollama (`gemma3:1b`) or cloud Groq (`llama-3.1-8b-instant`)
- **Connection Testing** — Built-in buttons to verify JIRA, Ollama, and Groq connectivity
- **Anti-Hallucination Rules** — Automatically appends verification rules from Chapter 1 to every prompt
- **Markdown Output** — Generates formatted test case tables with download capability

### Project Structure

```text
chapter_03_Local_TC_Generator/
└── Task1_10Aug_Local_TestCaseGenerator/
    ├── app.py                    # Streamlit entry point
    ├── requirements.txt          # Python dependencies
    ├── .env.example              # Environment variable template
    ├── src/
    │   ├── jira_client.py        # JIRA REST API wrapper
    │   ├── llm_service.py        # Ollama + Groq abstraction layer
    │   ├── prompt_builder.py     # Prompt construction from template + rules
    │   ├── output_handler.py     # Format, validate, and save test cases
    │   └── resources/
    │       ├── plan.md           # Architecture plan
    │       └── RoughDiagramofLocalTestcaseGenerator.png
    ├── templates/
    │   └── testcase_creator.md   # QA prompt template
    └── output/                   # Generated test case files
```

### Prerequisites

- Python 3.11+
- Ollama (optional, for local LLM) — install from [ollama.com](https://ollama.com)
- Groq API key (optional, for cloud LLM) — free at [console.groq.com](https://console.groq.com/keys)

### Configure and Run

1. Copy `.env.example` to `src/.env` and fill in your credentials.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
streamlit run app.py
```

4. Open **http://localhost:8501** in your browser.

### Architecture

The application follows a modular service-layer pattern:

- **Streamlit UI** (`app.py`) — 4 tabs: Settings, JIRA Fetch, Manual Input, Generated Output
- **JIRA Client** (`jira_client.py`) — Connects to Atlassian Cloud via `atlassian-python-api`
- **LLM Service** (`llm_service.py`) — Abstract provider pattern with Ollama (local) and Groq (cloud) implementations
- **Prompt Builder** (`prompt_builder.py`) — Merges the QA template with requirements and anti-hallucination rules
- **Output Handler** (`output_handler.py`) — Cleans LLM responses, validates table format, saves to file

## Chapter 4: JobKit AI (Todo)

> 🚧 *Placeholder — coming soon.*  
> This chapter will explore AI-assisted job application tools and workflows for QA professionals.

## Chapter 5: JobTracker AI (Todo)

> 🚧 *Placeholder — coming soon.*  
> This chapter will cover AI-powered job tracking and application management.

## Chapter 6: Branding & LinkedIn Skills (Todo)

> 🚧 *Placeholder — coming soon.*  
> This chapter will focus on AI-driven personal branding and LinkedIn profile optimization for QA engineers.

## Chapter 7: AI Agent Basics — Jira Test Plan Creator

Chapter 7 includes a local BLAST/A.N.T. agent that accepts one Jira Cloud issue key, retrieves the issue context through read-only APIs, and generates an English, document-level Markdown QA test plan with OpenRouter and `deepseek/deepseek-v4-flash`.

- [Jira Test Plan Creator project](chapter_07_AIAgentBasics/Test-Plan-Agent-BLAST-Framework/)
- [Setup and usage guide](chapter_07_AIAgentBasics/Test-Plan-Agent-BLAST-Framework/README.md)
- [BLAST project constitution](chapter_07_AIAgentBasics/Test-Plan-Agent-BLAST-Framework/LLM.md)
- [Architecture SOP](chapter_07_AIAgentBasics/Test-Plan-Agent-BLAST-Framework/architecture/SOP.md)

### Features

- Read-only Jira Cloud issue, field-metadata, and comment retrieval
- Local Create Plan and Settings interfaces
- Independent Jira and OpenRouter connection tests
- Provider-neutral LLM boundary with DeepSeek through OpenRouter
- Strict structured-output and deterministic validation
- English-only output with one bounded language-repair attempt
- Explicit assumptions and clarification questions for missing Jira information
- Local Markdown preview, download, and ignored `.tmp/output/` persistence
- No generated test scenarios, test cases, test steps, or expected-result tables

### Test Plan Output

The generated plan contains Objective, Scope, Inclusion, Test Environment, Defect Reporting Procedure, Test Strategy, Test Schedule, Test Deliverables, Entry and Exit Criteria, Test Execution, Test Closure, Tools, Risks and Mitigations, and Approvals.

### Run Locally

The application requires Python 3.11 or newer and has no third-party Python dependencies.

```powershell
cd chapter_07_AIAgentBasics\Test-Plan-Agent-BLAST-Framework
python app.py
```

## Chapter 8: n8n — AI Agent Workflows

[n8n](https://n8n.io) is an open-source workflow automation platform. This chapter contains exported n8n AI agent workflows for JIRA operations and bug triage automation.

### Prompt Resources

| File | Description |
|---|---|
| [Raw Bug Triage Prompt](chapter_08_n8n/01_RAW_BugTriageprompt.md) | Original bug triage prompt |
| [Modified Bug Triage Prompt v1](chapter_08_n8n/02_Modified_BugTraigePromp.prompt.md) | First iteration of the triage prompt |
| [Modified Bug Triage Prompt v2](chapter_08_n8n/03_Modified_BugTriagePrompt.prompt.md) | Refined bug triage prompt |

### n8n AI Agent Workflows (JSON)

| Workflow | Description |
|---|---|
| [Fetch JIRA Ticket](chapter_08_n8n/Agents/01_FetchJIRATicket_AIAgent.json) | Agent that retrieves JIRA ticket details |
| [Create JIRA Ticket](chapter_08_n8n/Agents/02_CreateJIRATicket_AIAgent.json) | Agent that creates new JIRA tickets |
| [Update JIRA Ticket](chapter_08_n8n/Agents/03_UpdateExistingJIRATicket_AIAgent.json) | Agent that updates existing JIRA tickets |
| [Fetch JIRA + Local LLM (Ollama)](chapter_08_n8n/Agents/04_FetchJIRA_Ticket_TC_Agent_Local_LLM_Ollama.json) | Agent that fetches JIRA tickets and processes them with a local Ollama LLM |
| [Bug Triage Agent](chapter_08_n8n/Agents/05_BugTriageAIAgent.json) | Agent that triages bugs using AI classification |
| [Screenshot to Bug Reporter (DeepSeek)](chapter_08_n8n/Agents/08_Screenshot_To_Bug_Reporter_AIAgent_Deepseek.json) | Webhook-driven workflow that analyzes a UI screenshot via DeepSeek Vision and creates a GitHub issue |
| [Screenshot to Bug Reporter (Groq + Jira)](chapter_08_n8n/Agents/09_Screenshot_to_Bug_Reporter_AIAgent_UI.json) | Form-driven workflow that analyzes an uploaded UI screenshot, creates a structured Jira Bug, and attaches the original screenshot |
| [Screenshot to Bug Reporter (Webhook)](chapter_08_n8n/Agents/10_Screenshot_to_Bug_Rep_AIAgent_WebHook.json) | Webhook-triggered version that accepts multipart file upload or JSON `imageUrl` payload |

### Reference Notes

| File | Description |
|---|---|
| [Webhook Understanding Guide](chapter_08_n8n/WebhookUnderstanding.md) | Comprehensive beginner-friendly guide on webhooks with layman and real-time examples |
| [Short Notes](chapter_08_n8n/short_notes.md) | Quick reference on n8n workflow creation approaches |

### How to Use

1. Import the JSON files into your n8n instance (n8n.io or self-hosted).
2. Configure the JIRA credentials and LLM nodes as needed.
3. Activate the workflows and trigger them via webhooks or schedules.

The Screenshot to Bug Reporter workflow setup and acceptance checks are documented in [its plan](chapter_08_n8n/Agents/plan_codex.md). Configure the referenced Groq Header Auth and Jira Cloud credentials after import; no secrets are stored in the export.

## Screenshot to Bug Reporter — Web UI

A lightweight, Vercel-deployed web UI for the **Screenshot to Bug Reporter** agent. Testers upload a UI screenshot (plus optional error logs and a Jira project key) and the n8n workflow drafts a complete Jira bug with the screenshot attached.

- **Live URL:** [https://bug-reporter-tawny.vercel.app](https://bug-reporter-tawny.vercel.app)
- [UI source code](ui_scerenshottobugAIAgent/) — single `index.html` with vanilla HTML/CSS/JS (no frameworks, no build step)
- **Flow:** Static UI → POST multipart form → n8n Webhook → Groq Vision → Jira Create Bug → Attach Screenshot
- **Webhook endpoint:** `https://aitestersqa.app.n8n.cloud/webhook/screenshot-to-bug-webhook`

## Chapter 9: LangFlow — AI Agent Workflows

[LangFlow](https://github.com/langflow/langflow) is an open-source visual framework for building AI agent workflows. It is installed locally and runs at `http://127.0.0.1:7860`.

### Installation Guide

A complete step-by-step installation guide is available at:
- [LangFlow Installation Guide](chapter_09_LangFlow/Notes/LangFlowInstallationGuide.md)

### Setup

```powershell
# 1. Install LangFlow
pip install langflow

# 2. Install the Groq and Composio/Jira provider bundles
pip install "lfx-bundles[groq,composio]"

# 3. Start LangFlow
python -m langflow run --host 127.0.0.1 --port 7860
```

Open **http://localhost:7860** in your browser.

### Current Contents

| File | Description |
|---|---|
| [LangFlow AI Agents](chapter_09_LangFlow/AIAgents/) | Directory for LangFlow workflow exports |
| [LangFlow Tasks](chapter_09_LangFlow/Task_Agents/) | Directory for task-specific agent workflows |
| [Installation Guide](chapter_09_LangFlow/Notes/LangFlowInstallationGuide.md) | Complete step-by-step local setup guide |
| [Quick Install Guide](chapter_09_LangFlow/Notes/LangFlowInstall.md) | Quick pip-based installation steps |
| [Short Notes](chapter_09_LangFlow/Notes/shortnote.md) | Quick reference on LangFlow concepts and comparison with other tools |

### LangFlow AI Agent Workflows

| Workflow | Description |
|---|---|
| [Hello World (Groq)](chapter_09_LangFlow/AIAgents/01__GROQ_LangFlow_Simple_HelloWorld.json) | Simple Groq-based chat flow — Chat Input → Groq → Chat Output |
| [Bug Triaging Agent v2](chapter_09_LangFlow/AIAgents/AI4X_002_Bug_Triaging_Agent.json) | Bug triaging agent using API Request → Parser → Prompt → DeepSeek |
| [Bug Triaging Agent v3](chapter_09_LangFlow/AIAgents/AI4X_003_Bug_Triage_AI_Agent.json) | Refined bug triaging agent with Jira API integration and structured output |
| [Jira Composio Connector](chapter_09_LangFlow/AIAgents/JIRAComposia.json) | Jira integration via Composio bundle — fetch issue details using Composio API Key |
| [Bug Triaging Agent (Composio)](chapter_09_LangFlow/AIAgents/005_Bug_Triaging_AIAgent_Composio.json) | Retrieves a Jira issue with Composio, parses its details, and uses DeepSeek to generate a bug-triage response |
| [Agent Notes](chapter_09_LangFlow/AIAgents/notes.md) | Quick notes on system messages and agent behavior |

### Key Features

- **Visual drag-and-drop builder** — No Python required to build AI agent workflows
- **Multiple LLM providers** — Groq, OpenAI, Anthropic, Ollama, Google, DeepSeek, and more via Bundles
- **Pre-built components** — Chat Input/Output, Prompt Templates, RAG, Agents, MCP Tools
- **Playground** — Test your flows directly in the browser
- **Export as JSON** — Save and share flows for reusability

### First Flow: Chat with Groq

1. Open **http://localhost:7860**
2. Create a new flow
3. From **Bundles** tab, add **Groq** to canvas
4. From **Components → Input & Output**, add **Chat Input** and **Chat Output**
5. Connect: Chat Input → Groq → Chat Output
6. Configure Groq with your API key and select a model
7. Click **Playground** and start chatting

## Overall Notes

Comprehensive reference notes covering key concepts across the repository.

| File | Description |
|---|---|
| [Bug Triage Notes](OverAll_Notes/BugTriage.md) | Notes on bug triage processes and best practices |
| [RAG Raw Notes](OverAll_Notes/RAGNotes_raw.md) | Raw notes on Retrieval-Augmented Generation |
| [RAG Understanding Guide](OverAll_Notes/RAGNotes_understanding.md) | Detailed textual explanation of RAG concepts |
| [RAG Complete Guide](OverAll_Notes/RAGCompleteGuide.md) | Comprehensive RAG guide with visual diagrams |
| [4X Advanced AI Tester Notes](OverAll_Notes/4X_Advanced_AI_TesterNotes.docx) | Advanced AI tester reference document |


## Contributing

Keep learning notes in their relevant chapter, include runnable examples where appropriate, and never commit credentials, generated reports, IDE settings, or build artifacts.
