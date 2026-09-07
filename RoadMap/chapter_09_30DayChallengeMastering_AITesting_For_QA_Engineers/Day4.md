
# 🚨 Day 04/30 — What If Your QA Test Case Generator Could Read Jira and Generate Test Cases Using a Local LLM?



Most QA Engineers are already experimenting with AI.

We open an AI tool, paste a requirement, type:

> “Generate test cases for this requirement.”

And within seconds, we get an answer.

Useful? Yes.

But today I learned something much more interesting:

🔥**What if we stop using AI only as a chat window and start building our own AI-powered QA solution?**

Imagine this workflow:

```
JIRA Ticket
     ↓
Fetch Requirement
     ↓
Load QA Test Case Template
     ↓
Local/Open-Source LLM
     ↓
Generate Test Cases
     ↓
QA Engineer Reviews the Output
```

That is what I explored today as part of my:

## 🚀 30 Days to Master AI Testing for QA Engineers

Based entirely on my AI Tester Blueprint learning, Day 04 is about moving from**Prompt Engineering**toward **Open-Source Models, Local LLMs, the Local Test Case Generator, and the BLAST Framework** .

---

### 🔄 Quick Recap — What We Learned Earlier

Before building AI-powered QA applications, the blueprint first establishes an important foundation:

### Prompt Engineering.

Instead of vague instructions like:

> “Write test cases for login”

the material recommends being specific about:

* what needs to be generated,
* the context,
* the expected format,
* and the constraints.

For example, the document shows a stronger request that asks for functional login test cases covering valid login, invalid email, invalid password, empty fields, and SQL injection, with a defined Jira-style output structure.

The bigger lesson?

> **The quality of AI output depends heavily on the quality of the instructions and context we provide.**

And that leads to today's next step.

---

## 🧠 From Prompting an LLM → Building With an LLM

There is a big difference between these two approaches.

### Approach 1

```
QA Engineer
     ↓
AI Chat
     ↓
Generate Test Cases
```

### Approach 2

```
QA Engineer
     ↓
QA Application
     ↓
Jira
     ↓
Prompt Template
     ↓
LLM
     ↓
Generated Test Cases
```

The second approach starts looking like an actual**AI-enabled QA workflow**rather than a one-time conversation.

And this is where**Open-Source Models and Local LLMs**become interesting.

---

## 🤖 What Is an Open-Source Model?

The blueprint introduces several popular open-source model families, including:

**Qwen****Llama****Gemma****Mistral****DeepSeek****Kimi K3**

The material highlights benefits such as transparency, community contribution, and reduced dependency on a single vendor.

For a QA Engineer, the interesting part is not simply knowing these names.

The real question is:

> **Can I run one of these models myself and use it inside my QA workflow?**

Yes—that is exactly what the blueprint explores next.

---

## 💻 Local LLM — Running AI on Your Own Machine

The document introduces tools such as:

* **Ollama**
* **LM Studio**
* **llama.cpp**

and smaller models such as:

* gemma3:1b
* llama3.2
* deepseek-r1:1.5b

for experimenting with locally running models.

The concept is simple.

Instead of:

```
Requirement
    ↓
External AI Service
    ↓
Response
```

we can experiment with:

```
Requirement
    ↓
LLM Running Locally
    ↓
Response
```

That creates a different level of control.

---

## 🔐 Why Can This Matter for QA Engineers?

Think about the kind of information QA teams handle every day:

Requirements.

Test cases.

Jira stories.

Defects.

Logs.

API documentation.

Automation code.

Some organizations may prefer that such information remain inside their own environment.

The blueprint describes local LLMs as private, capable of working without internet after setup, and providing greater control over the model. It also clearly mentions the disadvantages: local models can be slower, need significant infrastructure/RAM, and may have more limited knowledge.

So this isn't:

> Local LLM good, Cloud LLM bad.

It is about understanding the trade-off.

---

## 🚀 Real-Time QA Example — Local Test Case Generator

This was the most interesting part of today's learning.

The blueprint gives an objective:

### Generate Test Cases from requirements using an open-source model.

Then it extends that idea:

### Fetch the requirement from Jira and create Test Cases around it.

Imagine a QA Engineer types:

```
create test cases for QA-102
```

Instead of manually opening Jira, copying the requirement, opening an LLM, pasting the requirement and asking for test cases, the application can automate the workflow.

---

## 🔥 End-to-End Flow

The blueprint describes a flow like this:

```
User Request
"create test cases for QA-102"

             ↓

Extract Jira Key
QA-102

             ↓

Connect to Jira

             ↓

Fetch
Summary
Description
Acceptance Criteria

             ↓

Load Test Case Template

             ↓

Merge Requirement + Template

             ↓

Send to LLM

             ↓

Generate Test Cases

             ↓

Display Result
```

The document specifically describes parsing the Jira key, fetching ticket details, loading a template from a local /templates folder, generating through the configured LLM, and returning the generated test cases in a chat-style interface.

This is where AI Testing becomes much more exciting.

We're moving from:

> **“AI, give me test cases.”**

to:

> **“Build a reusable QA workflow that generates test-case drafts from real requirements.”**

---

## 🧪 Why Do We Need Test Case Templates?

One important part of the blueprint is the use of reusable prompt templates.

Instead of rewriting the same instructions every time, QA teams can maintain templates such as:

```
templates/
    │
    ├── Basic Test Case Generation
    ├── PRD to Test Cases
    ├── API Test Cases
    ├── Negative Test Cases
    └── Regression Suite
```

The document explicitly describes prompt templates as **ready-to-use templates for STLC** .

For example, a Test Case Generation template can define:

```
ROLE:
You are a Senior QA Engineer.

TASK:
Generate test cases for the provided feature.

CONSTRAINTS:
Use ONLY the provided requirements.

Do NOT assume undocumented behavior.

If information is missing:
"Not specified"

FORMAT:
Test ID
Description
Preconditions
Steps
Expected Result
Priority
```

This is powerful because the **requirement changes, but the QA standards can stay consistent** .

---

## 🛡️ And This Also Helps Control Hallucination

The blueprint repeatedly emphasizes constraints such as:

> Use only the provided requirements.

> Do not assume undocumented behavior.

> Mark unclear information appropriately.

> Do not invent error messages or codes.

For PRD-to-Test-Case generation, it explicitly asks the LLM to cover functional, negative, boundary, and edge scenarios while using only the PRD content.

This matters because AI-generated test cases can look extremely professional even when they contain assumptions.

As QA Engineers, our job isn't only:

### Generate.

It is also:

### Verify.

---

## ☁️ Local LLM + Cloud LLM

The blueprint doesn't stop with a local model.

It also introduces cloud-based LLM options and describes an architecture where:

### Ollama

can be used locally,

while a hosted model can act as an alternative or fallback.

Conceptually:

```
┌── Local LLM
                    │
Jira → QA App ──────┤
                    │
                    └── Cloud LLM
```

The Test Case Generator example specifically uses**Ollama as the default backend**and allows a hosted provider when Ollama is unavailable or explicitly selected.

That teaches another valuable lesson:

> **Our QA application does not necessarily have to be tied permanently to one LLM.**

---

## 🏗️ What Would This QA Application Contain?

The blueprint proposes a lightweight application with two main screens.

### 💬 Screen 1 — Chat

QA Engineer enters:

```
create test cases for QA-102
```

### ⚙️ Screen 2 — Settings

The configuration contains information such as:

```
Jira URL
Jira Email
Jira API Token
LLM Provider
Groq API Key
```

The material describes this as a two-screen Streamlit application with separate Chat and Settings interfaces.

This already starts to feel like an internal QA productivity tool rather than a normal prompt.

---

## 🔐 Important Lesson — Never Hardcode Credentials

This is one lesson every automation engineer should pay attention to.

Imagine putting this into your code:

```
jira_token = "actual_token_here"
```

and then pushing the project to GitHub.

🚨 Dangerous.

The blueprint specifically instructs that Jira tokens and LLM keys should**not be hardcoded**and should instead be persisted through a configuration layer excluded from version control.

AI Testing still requires good engineering practices.

AI doesn't remove:

Security.

Architecture.

Configuration management.

Code quality.

QA discipline.

---

## 💥 Then Comes the BLAST Framework

Another major topic introduced in this section is:

## B.L.A.S.T

The framework is intended to help us understand and track what we're building instead of blindly generating a large amount of AI-created code.

According to the blueprint:

### B — Blueprint

### L — Link

### A — Architect

### S — Stylise

### T — Trigger & Deploy

Let's understand it using our Test Case Generator.

---

## 🔵 B — Blueprint

Before coding anything:

### Define what you are building.

For example:

```
Goal:

Build a QA application
that accepts a Jira ID,
fetches the requirement,
loads a Test Case template,
uses an LLM,
and returns Test Case drafts.
```

Simple.

Clear.

Understandable.

Don't start with code.

Start with the **Blueprint** .

---

## 🔗 L — Link

Next understand the connections.

```
Jira
 ↓
REST API
 ↓
QA Application
 ↓
Prompt Template
 ↓
LLM
```

What talks to what?

Where does the data come from?

Where does the requirement go?

Where does the Test Case template come from?

This makes the solution easier to understand.

---

## 🏗️ A — Architect

Now organize the application.

The blueprint example separates responsibilities into components such as:

```
app.py

settings

config_store.py

jira_client.py

llm_client.py

templates/

requirements.txt
```

Each piece has a clear responsibility—for example Jira integration, configuration, LLM interaction and templates.

This is much better than one giant AI-generated file containing everything.

---

## 🎨 S — Stylise

Now make it usable.

Instead of forcing QA Engineers to run Python commands manually, create a simple user interface.

Example:

```
-----------------------------------

     AI TEST CASE GENERATOR

-----------------------------------

Enter Request:

[ create test cases for QA-102 ]

               [ SEND ]

-----------------------------------
```

Then provide a Settings page for configuration.

Now the tool becomes usable by other testers too.

---

## 🚀 T — Trigger & Deploy

Finally:

Trigger the entire workflow.

```
QA enters Jira ID
       ↓
Fetch requirement
       ↓
Load template
       ↓
Call LLM
       ↓
Generate Test Cases
       ↓
Display results
```

The blueprint calls this stage**Trigger and Deploy**and discusses running the application locally or through other deployment approaches.

---

## 🚨 The Biggest Lesson From BLAST

One statement in the material stood out for me.

The BLAST framework is intended to make sure we don't create:

> **AI code or a solution that we don't understand.**

This is extremely important.

Because today AI can generate an entire application in minutes.

But imagine your manager asks:

> Where are the Jira credentials stored?

And you don't know.

> How does the application fetch the Jira requirement?

And you don't know.

> Which component sends information to the LLM?

And you don't know.

> What happens if the local model is unavailable?

And you don't know.

Then we haven't really engineered the solution.

We've only generated it.

---

## 🧠 AI Should Help Us Build Faster — Not Stop Us From Understanding

A better approach is:

```
Understand
    ↓
Plan
    ↓
Architect
    ↓
Generate
    ↓
Review
    ↓
Test
    ↓
Improve
```

That is why the blueprint combines:

### RICE POT

for structured prompting,

with

### BLAST

for structured building.

---

## 🔥 Imagine This in a Real QA Team

Traditional process:

```
Jira Story
    ↓
QA opens Jira
    ↓
Reads Requirement
    ↓
Writes Test Cases
    ↓
Reviews Coverage
```

AI-assisted process:

```
Jira Story
     ↓
QA Application
     ↓
Fetch Requirement
     ↓
Apply Test Case Template
     ↓
LLM
     ↓
Generate Test Case Draft
     ↓
QA Review
```

The word**Draft**matters.

The blueprint itself describes the Jira Test Case Generator as an internal productivity tool designed to turn a Jira ticket into a**test case draft**using either a local model or hosted fallback.

AI generates.

QA validates.

That still remains important.

---

## 🎯 Day 04 — My Biggest Takeaways

Today I learned that AI Testing is much more than knowing how to ask ChatGPT a question.

A QA Engineer can start thinking about:

✅ Open-source models

✅ Local LLMs

✅ Ollama

✅ Cloud LLM alternatives

✅ Jira integration

✅ Requirement extraction

✅ Reusable Test Case templates

✅ Anti-hallucination constraints

✅ LLM-based Test Case generation

✅ Secure credential handling

✅ Application architecture

✅ BLAST Framework

And most importantly:

> **Don't blindly create AI-generated applications that you cannot explain.**

---

## 🚀 The Evolution of a QA Engineer

Traditional QA:

```
Requirement
    ↓
Test Cases
    ↓
Execution
```

Automation QA:

```
Requirement
    ↓
Test Cases
    ↓
Automation
    ↓
Execution
```

AI-assisted QA:

```
Requirement
    ↓
Jira/API
    ↓
Prompt Template
    ↓
LLM
    ↓
Test Case Draft
    ↓
QA Validation
    ↓
Automation
```

That is a very different way of thinking about testing.

---

## 💡 One Final Thought

For years, QA Engineers learned tools such as automation frameworks, APIs and CI/CD.

Now another capability is becoming important:

### Understanding how AI can be integrated into the QA workflow itself.

Not just:

> “Use AI.”

But:

> **Understand the model. Structure the prompt. Control the context. Build the workflow. Validate the output.**

That is what I am trying to learn through:

## 🚀 30 Days to Master AI Testing for QA Engineers

### Day 04 ✅

**Open-Source Models + Local LLMs + Jira Test Case Generator + BLAST Framework**

More learning ahead. 🚀

#AITesting #SoftwareTesting #QualityAssurance #QAAutomation #TestAutomation #SDET #GenerativeAI #LLM #OpenSourceAI #Ollama #JIRA #PromptEngineering #RICEPOT #BLASTFramework #AIForTesting #ArtificialIntelligence #QATesting #30DaysOfAITesting
