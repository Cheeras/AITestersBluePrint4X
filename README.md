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

## Contributing

Keep learning notes in their relevant chapter, include runnable examples where appropriate, and never commit credentials, generated reports, IDE settings, or build artifacts.
