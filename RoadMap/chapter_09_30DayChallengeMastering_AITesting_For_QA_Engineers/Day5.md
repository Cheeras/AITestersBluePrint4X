
# 🚨 Day 05/30 — A Prompt Can Tell AI What to Do. But Can It Actually Do the Work for You?



For the last few days, I have been learning how to write better prompts.

Role.

Context.

Instructions.

Constraints.

Output format.

Anti-hallucination rules.

RICE POT.

All of these can dramatically improve an LLM response.

But today I came across a question that completely changed how I look at AI for QA:

What is the difference between a Prompt, a Skill, and an AI Agent?
At first, they can sound like different names for the same thing.

They are not.

And understanding the difference is important if we want to move from simply asking AI questions to actually building AI-powered QA workflows.

Welcome to:

🚀 Day 05/30 — 30 Days to Master AI Testing for QA Engineers
Today’s Learning: Prompt vs Skill vs AI Agent
The blueprint puts these concepts together very simply:

Prompt → Instructions

Skill → Structured Instructions

AI Agent → Brain + Memory + Tools

Let me explain this from a QA Engineer's perspective.

🧠 First — What Is a Prompt?
The document defines a Prompt as:

A set of instructions given to the model.
A prompt tells the LLM what we want.

For example:

Act as a Senior QA Engineer.

Generate 10 functional test cases
for the Login functionality.

Use only the provided requirements.

Do not assume undocumented behaviour.

Output:
Test ID
Scenario
Steps
Expected Result
Priority
The LLM receives the instruction.

It processes it.

It returns the answer.

Conceptually:

QA Engineer
      ↓
    Prompt
      ↓
     LLM
      ↓
   Response
That's extremely useful.

But the prompt itself is still primarily an instruction for the current task.

🧪 Real-Time QA Example — Prompt
Suppose I have a Jira story:

QA-102

Users should be able to log in
using email and password.
I could prompt the LLM:

Act as a Senior QA Engineer.

Generate test cases for QA-102.

Cover:
Functional
Negative
Boundary

Do not invent functionality
not mentioned in the requirement.
And I get test cases.

Great.

Tomorrow I receive QA-103.

I give another prompt.

Then QA-104.

Another prompt.

This works.

But now imagine I want every tester in my organization to follow the same testing rules every time.

That's where the next concept becomes interesting.

🧠 What Is a Skill?
The blueprint explains Skill very simply:

A Skill is a set of instructions properly structured to get a desired output.
It also specifically mentions:

Skill File → .md file that can be shared

and notes that a Skill can also exist as a folder capable of handling multiple things.

That means we start moving from:

“Write this instruction again”
toward:

“Package the instruction so it can be reused.”
🔥 Prompt vs Skill — QA Example
Imagine I regularly generate test cases.

Prompt
Generate test cases for Login.
Use only the requirement.
Include negative scenarios.
Useful.

But now imagine creating a reusable QA Skill containing structured instructions such as:

QA TEST CASE GENERATION SKILL

ROLE
Senior QA Engineer

INPUT
Requirement / Jira Story

PROCESS
Understand requirement
Identify functional scenarios
Identify negative scenarios
Identify boundary conditions
Identify missing information

ANTI-HALLUCINATION RULE
Use only supplied requirements.

If information is missing:
"Needs clarification"

OUTPUT
Test ID
Category
Description
Preconditions
Steps
Expected Result
Priority
Now the QA rules are not being reinvented every time.

The instructions themselves become reusable knowledge.

That is a very different mindset.

💡 Think About It Like Automation Engineering
As automation engineers, we already understand this principle.

We don't normally write:

Launch browser
Login
Logout
Close browser
from scratch in every test.

We create reusable components.

The same thinking starts becoming useful with AI.

One-time instruction
        ↓
      Prompt

Reusable structured instruction
        ↓
       Skill
The blueprint even marks the transition:

Prompt → Skill
as an important next step.

🧪 Real-Time Example — Bug Analysis Skill
Imagine every tester asks AI differently.

Tester A:

Analyze this bug.
Tester B:

What is wrong here?
Tester C:

Find the root cause.
The results can vary significantly.

Instead, imagine creating a standardized Bug Analysis Skill:

ROLE
Senior QA Engineer

INPUT
Bug description
Logs
Screenshots
Requirement

RULES
Use only supplied evidence.

Do not assume root cause.

Separate:
Verified Facts
Missing Information
Hypotheses

If information is unavailable:
"Insufficient information to determine"

OUTPUT
Symptoms
Verified Facts
Missing Information
Possible Hypothesis
Recommended Next Steps
Now the testing philosophy becomes reusable.

This aligns with the blueprint's anti-hallucination approach, which explicitly says to use only supplied PRDs, API documentation, logs, screenshots, test data, and user input, and to separate verified facts from unknown information.

🚨 But Skill Still Doesn't Mean Autonomous Execution
This is where the third concept appears.

🤖 AI Agent
The blueprint gives one of the simplest explanations I have seen:

LLM → Brain
AI Agent → Brain + Memory + Tools (Workflows)
This distinction matters.

An LLM can think about the information we provide.

But an Agent can be designed around more than the model alone.

Conceptually:

 ┌──────────────┐
                 │    Brain     │
                 │     LLM      │
                 └──────┬───────┘
                        │
             ┌──────────┼──────────┐
             ↓          ↓          ↓
          Memory       Tools     Workflow
Now AI begins moving from:

“Tell me what you know.”
toward:

“Use the available systems to complete a workflow.”
🧪 QA Example — From Prompt to Agent
Let's use the Jira Test Case Generator covered in the blueprint.

Stage 1 — Prompt
I manually copy QA-102 and ask:

Generate test cases for QA-102.
Flow:

Jira
 ↓
QA manually copies story
 ↓
Prompt
 ↓
LLM
 ↓
Test Cases
Stage 2 — Skill
Now my Test Case Generation rules are standardized.

Jira Requirement
       ↓
QA Test Generation Skill
       ↓
LLM
       ↓
Structured Test Cases
My QA rules can now remain consistent across requirements.

Stage 3 — Agent-Style Workflow
Now imagine the AI workflow has access to Jira as a tool.

The blueprint's Jira Test Case Generator already describes a workflow that:

Receives Jira ID
      ↓
Fetches Jira details
      ↓
Reads Test Case Template
      ↓
Uses LLM
      ↓
Generates Test Cases
Its detailed implementation retrieves the Jira summary, description, and acceptance criteria, loads the test-case template, combines them, and sends them to the configured LLM.

Now we aren't manually moving every piece of information ourselves.

The system is doing more of the workflow.

🔥 This Is the Evolution
LevelWhat It MeansQA ExamplePromptInstructions“Generate 10 test cases”SkillReusable structured instructionsStandard QA Test Generation SkillLLMBrainUnderstands requirement and generates contentAI AgentBrain + Memory + Tools + WorkflowUses connected systems to perform a QA workflow

The blueprint specifically distinguishes an LLM as the Brain, while an AI Agent adds memory, tools, and workflows.

🧠 Why Does “Memory” Matter?
Imagine an AI workflow handling multiple interactions.

Without context, every interaction effectively starts from the information supplied at that moment.

But the blueprint includes Memory as one of the defining pieces of an AI Agent.

Conceptually:

Brain
+
Memory
+
Tools
+
Workflow
========

AI Agent
This is important because workflows often need information from previous actions.

For QA, that could mean maintaining the context necessary to continue a multi-step workflow instead of treating every step as an isolated prompt.

The document also describes BLAST as tracking findings, tasks, plans, code, progress, context, and memory—reinforcing the importance of maintaining context when building AI systems.

🔧 Why Do “Tools” Matter?
This is perhaps the biggest jump.

An LLM alone doesn't automatically become your Jira system.

It doesn't automatically become your API client.

The blueprint emphasizes connecting AI to real systems as part of AI Engineering.

Once tools are introduced, the workflow can start interacting with systems around it.

For example:

 AI Agent

               ↓

       ┌───────┼────────┐
       ↓       ↓        ↓
     Jira   LLM Tool   Workflow
Now AI isn't limited to generating text.

It can participate in the QA process.

🚀 Real-Time Scenario — Jira Test Case Generation
Imagine this command:

Create test cases for QA-102
With only a Prompt
You manually retrieve QA-102.

You copy the requirement.

You paste it into the LLM.

You receive test cases.

With a Skill
You have standardized QA instructions defining:

Role.

Coverage.

Constraints.

Output format.

Anti-hallucination rules.

Every Jira story can follow the same QA methodology.

With an Agent Workflow
The system can follow the workflow described in the blueprint:

User:
"Create test cases for QA-102"

           ↓

Extract QA-102

           ↓

Fetch Jira Ticket

           ↓

Get:
Summary
Description
Acceptance Criteria

           ↓

Load QA Instructions / Template

           ↓

Send Context to LLM

           ↓

Generate Structured Test Cases
The blueprint's Jira application specifically describes this flow and uses a local Ollama backend with an optional hosted fallback.

This is where QA starts moving toward AI-assisted workflow automation.

🛡️ Where Do Guardrails Fit?
Another important realization:

Moving from Prompt → Skill → Agent does not mean removing QA controls.

It makes them even more important.

The document's anti-hallucination rules say the AI should:

Use only explicitly supplied information.

Not invent APIs, UI elements, features, error codes, or behavior.

Identify missing information.

Generate only from verified facts.

Perform a self-check for hallucinations or contradictions.

So a more mature workflow becomes:

AI Agent
    ↓
Tool retrieves Jira
    ↓
Skill defines QA methodology
    ↓
LLM generates output
    ↓
Anti-Hallucination Rules
    ↓
QA Validation
That combination is much more interesting than simply asking:

“Generate test cases.”
🎯 One Important Misunderstanding I Had
Earlier, I thought:

Prompt = Instructions

Skill = Instructions

Agent = Instructions
So I wondered:

Aren't these basically the same?
Now the distinction is clearer.

PROMPT
"What should AI do?"

        ↓

SKILL
"How should AI repeatedly perform this type of task?"

        ↓

AI AGENT
"How can AI use a brain, memory,
tools and workflow to carry out the task?"
That's the progression.

🧪 Another QA Example — Bug Triage
Suppose we have 100 Jira defects.

Prompt
Analyze this Jira defect
and recommend severity.
One defect at a time.

Skill
Create standardized bug-triage instructions:

Role:
QA Lead

Analyze:
User Impact
Business Impact
Reproducibility
Workaround

Rules:
Do not invent missing information.

Output:
Recommended Severity
Reason
Missing Information
Now every bug can follow the same triage logic.

Agent Workflow
Conceptually:

Jira
 ↓
Retrieve Defect
 ↓
Apply Bug Triage Skill
 ↓
LLM Brain
 ↓
Structured Classification
 ↓
Continue Workflow
That is a much bigger leap than “AI generated a response.”

💡 The Bigger Lesson for QA Engineers
We shouldn't stop learning at:

How do I write a prompt?
The progression in the blueprint points toward:

Prompt Engineering
       ↓
Skills
       ↓
AI Agents
       ↓
RAG
       ↓
MCP
       ↓
LLM Evaluation
       ↓
AI Testing
The overall roadmap explicitly places Prompt Engineering before Generative AI, AI Agents, RAG, MCP, LLM Evaluation, and AI Testing tools.

So Prompt Engineering is the foundation.

It is not the destination.

🔥 My Biggest Day 05 Takeaway
Today I learned this simple distinction:

Prompt
Give AI instructions.

Skill
Package those instructions in a structured, reusable way.

AI Agent
Combine the LLM brain with memory, tools and workflows.

That one distinction makes many AI concepts much easier to understand.

And from a QA perspective:

Prompt
   ↓
Generate something

Skill
   ↓
Generate it consistently

AI Agent
   ↓
Participate in the workflow
🚀 Why This Matters for the Future QA Engineer
A traditional QA Engineer might ask:

“How do I test this feature?”
An Automation Engineer might ask:

“How do I automate this feature?”
An AI-enabled QA Engineer increasingly needs to think:

“What parts of this QA workflow can be expressed as reusable skills, connected to tools, and executed through AI-assisted workflows while keeping validation and guardrails in place?”
That's a very different mindset.

And that's exactly why I'm doing this learning journey.

🚀 Day 05/30 — 30 Days to Master AI Testing for QA Engineers
Prompt vs Skill vs AI Agent
Prompt = Instructions

Skill = Structured Instructions

AI Agent = Brain + Memory + Tools + Workflow

Now the roadmap starts becoming much clearer.

#AITesting #AIAgents #PromptEngineering #SoftwareTesting #QualityAssurance #QAAutomation #SDET #GenerativeAI #LLM #JIRA #TestAutomation #AITester #AIForTesting #AgenticAI #30DaysOfAITesting
