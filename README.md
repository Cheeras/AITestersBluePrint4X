# AI Testers Blueprint 4X

AI Testers Blueprint 4X is a hands-on learning repository for software testers who want to use generative AI in testing workflows. It combines foundational notes, reusable prompt-engineering templates, and practical test-automation examples.

## Learning Roadmap

The complete learning path is available in the [AI Tester Blueprint roadmap](RoadMap/AITesterBluePrintRoadMap.png).

## Repository Contents

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

## Chapter 7: AI Agent Basics - Jira Test Plan Creator

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

## Chapter 0: 30-Day Challenge — Mastering AI Testing for QA Engineers

A structured 30-day learning challenge designed for QA engineers to master AI-assisted testing — from prompt engineering fundamentals to building AI-powered QA workflows and agents.

| Day | Topic |
| --- | --- |
| [Day 1](chapter_00_30DayChallengeMastering_AITesting_For_QA_Engineers/Day1.md) | The Journey Begins — Why AI Testing Matters for QA Engineers |
| [Day 2](chapter_00_30DayChallengeMastering_AITesting_For_QA_Engineers/Day2.md) | Prompt Engineering for QA Engineers — Why Better Prompts Produce Better Testing Results |
| [Day 3](chapter_00_30DayChallengeMastering_AITesting_For_QA_Engineers/Day3.md) | RICE POT + Guardrails — Making AI Think Like a QA Engineer |
| [Day 4](chapter_00_30DayChallengeMastering_AITesting_For_QA_Engineers/Day4.md) | Local LLM Test Case Generator — From Jira to Test Cases Using Open-Source Models |
| [Day 5](chapter_00_30DayChallengeMastering_AITesting_For_QA_Engineers/Day5.md) | Prompt vs Skill vs AI Agent — Understanding the Difference |
| [Day 6](chapter_00_30DayChallengeMastering_AITesting_For_QA_Engineers/Day6.md) | The BLAST Framework — Building AI Agents You Can Explain and Trust |
| [Day 7](chapter_00_30DayChallengeMastering_AITesting_For_QA_Engineers/Day7.md) | AI Agents in Action — Building Your First QA AI Agent |

## Chapter 4: JobKit AI — Todo

*Placeholder — content coming soon.*

## Chapter 5: JobTracker AI — Todo

*Placeholder — content coming soon.*

## Chapter 6: Branding & LinkedIn Skills — Todo

*Placeholder — content coming soon.*

## Chapter 8: n8n AI Agents — Jira Automation Workflows

Chapter 8 contains n8n-based AI agent workflows for Jira automation, along with refined bug-triage prompts. These workflows are designed to be imported directly into [n8n](https://n8n.io) and connected to your Jira Cloud instance.

### Bug Triage Prompt Evolution

The chapter tracks the iterative refinement of a bug-triage system prompt across three versions:

- [Raw Bug Triage Prompt](chapter_08_n8n/01_RAW_BugTriageprompt.md) — The original 15+ year veteran QA engineer prompt with severity/priority scales and triage checklist
- [Modified Bug Triage Prompt v1](chapter_08_n8n/02_Modified_BugTraigePromp.prompt.md) — Enhanced with mandatory execution order, Jira + Google Sheets tool integration, and per-issue processing rules
- [Modified Bug Triage Prompt v2](chapter_08_n8n/03_Modified_BugTriagePrompt.prompt.md) — Further refined with structured role/objective sections, evidence-based triage, and JSON output contract

### n8n Agent Workflows

| File | Description |
| --- | --- |
| [`01_FetchJIRATicket_AIAgent.json`](chapter_08_n8n/Agents/01_FetchJIRATicket_AIAgent.json) | Fetch a single Jira ticket by key |
| [`02_CreateJIRATicket_AIAgent.json`](chapter_08_n8n/Agents/02_CreateJIRATicket_AIAgent.json) | Create a new Jira ticket via AI agent |
| [`03_UpdateExistingJIRATicket_AIAgent.json`](chapter_08_n8n/Agents/03_UpdateExistingJIRATicket_AIAgent.json) | Update an existing Jira ticket |
| [`04_FetchJIRA_Ticket_TC_Agent_Local_LLM_Ollama.json`](chapter_08_n8n/Agents/04_FetchJIRA_Ticket_TC_Agent_Local_LLM_Ollama.json) | Fetch Jira ticket and generate test plan using local Ollama LLM |
| [`05_BugTriageAIAgent.json`](chapter_08_n8n/Agents/05_BugTriageAIAgent.json) | Full bug-triage agent — retrieves Jira issues, triages each independently, and writes results to Google Sheets |

## Chapter 9: LangFlow AI Agents

Chapter 9 contains LangFlow-based AI agent workflows for Jira automation and QA workflows. These workflows can be imported directly into [LangFlow](https://github.com/logspace-ai/langflow) and connected to your LLM and Jira instances.

### Available Agents

| Directory | Description |
| --- | --- |
| [`AIAgents/`](chapter_09_LangFlow/AIAgents/) | LangFlow AI agent definitions (coming soon) |

## Overall Notes

- [Bug Triage (AI Agent)](OverAll_Notes/BugTriage.md) — Comprehensive notes on the bug-triage objective, workflow, and AI agent design
- [Advanced AI Tester Notes](OverAll_Notes/4X_Advanced_AI_TesterNotes.docx) — In-depth reference document on advanced AI testing concepts

## Contributing

Keep learning notes in their relevant chapter, include runnable examples where appropriate, and never commit credentials, generated reports, IDE settings, or build artifacts.
