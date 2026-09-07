
# Day 03/30 — 30 Days to Master AI Testing for QA Engineers




Day 03/30 — 30 Days to Master AI Testing for QA Engineers
shankar cheerala
shankar cheerala
Senior Quality Assurance Engineer at NTT DATA

September 2, 2026
🚨 Stop Asking AI: “Generate Test Cases” — Use RICE POT + Guardrails to Make AI Think Like a QA Engineer!
On Day 2, we explored why Prompt Engineering is becoming an essential skill for QA Engineers.

Today, I went one level deeper.

One of the biggest mistakes we can make while using AI for testing is giving a vague instruction like:

“Generate test cases for login.”
Then, when AI produces generic or inaccurate test cases, we blame the model.

But often the real problem is:

❌ Poor context
❌ Weak instructions
❌ Missing constraints
❌ No output controls
❌ No anti-hallucination rules
❌ No guardrails
A Large Language Model does not automatically know:

Our exact business requirements
Application architecture
Security policies
Testing scope
Severity definitions
Priority definitions
Allowed assumptions
Expected output format
Automation framework
Production constraints

We need to provide those instructions.

That is where the RICE POT Prompt Framework + Anti-Hallucination Controls + Guardrails becomes extremely powerful for QA Engineers.

🧠 What Is the RICE POT Framework?
RICE POT is a structured way to build better AI prompts.

R — Role
Who should AI act as?

I — Instructions
What exactly should AI do?

C — Context
What application, feature or business scenario are we dealing with?

E — Examples
Show AI examples of expected behavior.

P — Parameters
Define boundaries, rules, constraints and coverage.

O — Output
Specify exactly how the answer should be structured.

T — Tone
Define how AI should communicate.

But for AI Testing, I believe we should add two more important layers:

🛡️ Anti-Hallucination Controls
and

🚧 Guardrails
Because:

Getting an answer from AI is easy. Getting an answer that is grounded, controlled, verifiable and safe enough to use in QA is the real challenge.
❌ Weak Prompt vs ✅ Controlled Prompt
Consider:

Generate test cases for Login.
AI might produce:

Valid Login
Invalid Login
Forgot Password
Account Lock
CAPTCHA
MFA
Password Expiration

But wait.

What if the requirement never mentioned:

❌ CAPTCHA?

❌ MFA?

❌ Password expiration?

AI may have created perfectly reasonable testing ideas — but they are still unsupported assumptions.

That is one form of hallucination.

🤖 What Is Hallucination in AI?
Hallucination occurs when an AI system generates information that sounds believable but is unsupported, incorrect or fabricated.

For QA Engineers, hallucinations can become dangerous.

Imagine AI generates:

Account should lock after 3 failed attempts.
But the actual requirement says:

Account should lock after 5 failed attempts.
If we blindly convert AI-generated output into automation, our test will fail for the wrong reason.

Even worse:

A developer might modify the application to satisfy an incorrect AI-generated test.

This is why AI-generated test artifacts must always be validated against the source of truth.

🔥 Real-Time Hallucination Example 1 — File Upload
Requirement:

Users should be able to upload profile pictures.
Ask AI:

Generate test cases.
AI might generate:

Verify files above 5 MB cannot be uploaded.
Where did 5 MB come from?

It was never mentioned.

AI filled the missing information with something plausible.

Instead, our prompt should contain:

Do not invent maximum file size.

If the maximum file size is not specified,
mark it as:

Requirement Clarification Required.
Now AI should identify:

Missing Requirement:

Maximum supported upload size is not defined.
That is much more useful to QA.

🔥 Hallucination Example 2 — API Status Codes
Requirement:

POST /users creates a new user.
AI might say:

Expected Status Code = 201
That is common REST practice.

But what if the application specification says:

Successful response = HTTP 200
Therefore the prompt should say:

Do not assume HTTP status codes.

Only use status codes explicitly provided
in the API specification.

If unavailable, return:

Expected Status:
Specification Required
That single guardrail prevents incorrect test design.

🔥 Hallucination Example 3 — Bug Severity
Bug:

User cannot download report.
AI might immediately say:

Severity = Critical
Priority = P0
But we don't yet know:

How many customers are affected?
Is there a workaround?
Is the report business critical?
Is this production only?
Is financial reporting impacted?
Is it intermittent?
Did it work previously?

A better prompt says:

Do not assign Critical severity unless
sufficient evidence supports the recommendation.

If required evidence is missing,
list the missing information first.

Reduce confidence score accordingly.
Now AI becomes much more controlled.

🛡️ Anti-Hallucination Rules for QA Prompts
Whenever I use AI for testing, I can add instructions like:

ANTI-HALLUCINATION RULES:

1. Do not invent requirements.
2. Do not assume missing business rules.
3. Do not invent API endpoints.
4. Do not invent database tables or column names.
5. Do not assume HTTP response codes.
6. Do not invent UI elements that are not mentioned.
7. Do not invent severity or priority definitions.
8. Clearly separate:

   - Facts
   - Assumptions
   - Recommendations
9. If information is missing, return:
   "Requirement Clarification Required."
10. When uncertain, explicitly state uncertainty.
11. Do not present assumptions as facts.
12. Base expected results only on supplied requirements.
13. Provide a confidence score for recommendations.
14. Identify the evidence used to reach critical conclusions.
    This becomes extremely powerful.

🚧 What Are Guardrails?
Guardrails define what an AI system is allowed and not allowed to do.

Think of guardrails like:

Safety boundaries around the LLM.
In traditional automation we write validation logic like:

If condition is true → continue.

If condition is false → stop.
AI systems also need boundaries.

🧠 Prompt Instructions vs Guardrails
These are related, but not exactly the same.

Prompt
Tells AI:

What should you do?
Guardrail
Tells AI:

What are you NOT allowed to do?
For example:

Prompt
Generate Jira bug triage recommendations.
Guardrail
Never modify Jira Severity automatically
when confidence is below 80%.
This is a much stronger AI workflow.

🔥 Real-Time Guardrail Example 1 — Jira Bug Triage
Imagine this AI Agent flow:

Jira
 ↓
AI Agent
 ↓
Bug Triage
 ↓
Severity Recommendation
 ↓
Update Jira
Without guardrails:

AI might automatically change:

Severity = Critical
That could trigger escalation.

Instead:

GUARDRAIL:

If confidence >= 90%
    Recommend severity.

If confidence < 90%
    Do not update Jira.

Mark:
Human Review Required.
Now the flow becomes:

Jira
 ↓
AI Analysis
 ↓
Confidence Check
 ↓
High Confidence?
 ↓
YES → Continue

NO → Human Review
This is much safer.

🔥 Real-Time Guardrail Example 2 — Test Case Generation
Suppose Jira requirement:

User can reset password.
AI starts generating:

OTP expires after 5 minutes.
Guardrail:

Never generate exact numeric business rules
unless they are explicitly present in the source requirement.

If OTP expiration time is missing, output:

Requirement Clarification Required:
OTP expiry duration is not specified.
Now AI helps uncover missing requirements instead of creating them.

🔥 Real-Time Guardrail Example 3 — Automation Code Generation
Suppose we ask:

Generate Selenium automation for payment validation.
AI could potentially generate code containing:

Thread.sleep(10000);
We can add:

AUTOMATION GUARDRAILS:

Do not use Thread.sleep().

Do not use hard-coded credentials.

Do not hard-code environment URLs.

Do not use fragile XPath unless necessary.

Do not disable SSL validation.

Do not log authentication tokens.

Do not store passwords inside source code.
Now AI-generated automation has coding guardrails.

🔥 Real-Time Guardrail Example 4 — Production Database Testing
Imagine AI has access to a database tool.

We absolutely do NOT want:

DELETE FROM CUSTOMER;
or:

DROP TABLE CUSTOMER;
A guardrail could say:

DATABASE GUARDRAILS:

Allow:
SELECT

Disallow:
INSERT
UPDATE
DELETE
DROP
ALTER
TRUNCATE

Production access must remain read-only.
Now AI can investigate without damaging production data.

🔥 Real-Time Guardrail Example 5 — API Testing Agent
AI Agent receives access to API tools.

Guardrails:

Allowed HTTP Methods:

GET
POST to approved test endpoints

Restricted:

DELETE
PATCH
PUT against production
Additional guardrail:

Never send destructive requests against Production.

Environment must be explicitly identified before execution.
This becomes especially important when we move from:

AI generating suggestions
to

AI actually executing tools.
🔥 Real-Time Guardrail Example 6 — Sensitive Data
Suppose production logs contain:

Customer Name
Email
Phone
Card Details
Authentication Token
Guardrail:

Never expose:

Passwords
API Keys
Access Tokens
Credit Card Numbers
Personal customer information

Mask sensitive values before returning output.
Output:

Email:
s*****@example.com

Token:

---

Card:
**** **** **** 1234
QA Engineers working with AI need to think about data protection as well as testing accuracy.

🔥 Real-Time Guardrail Example 7 — Security Testing
Suppose AI is generating security tests.

We want:

✅ Security test ideas

✅ Validation steps

✅ Test-environment-only scenarios

But we should control what AI is allowed to execute automatically.

For example:

Generate security test scenarios.

Do not execute attacks.

Do not target production systems.

Do not attempt destructive exploitation.

Limit recommendations to approved test environments.
This becomes part of responsible AI-assisted testing.

🧩 Now Let's Combine Everything
Our QA prompt structure becomes:

RICE POT + Anti-Hallucination + Guardrails
🔥 Complete Real-Time Example — Banking Login
R — ROLE
Act as a Senior Banking QA Engineer experienced in
Functional, API, Security and Automation Testing.
I — INSTRUCTIONS
Generate comprehensive test scenarios for Login.
C — CONTEXT
Application:
Internet Banking

Fields:

Email
Password
Remember Me
Forgot Password
Login

Business Rules:

Account locks after 5 consecutive failures.

Session expires after 15 minutes of inactivity.

MFA is required for login from a new device.
E — EXAMPLES
Scenario:

Login using valid credentials.

Expected Result:

User successfully authenticates
and reaches Dashboard.
P — PARAMETERS
Generate 30 scenarios.

Include:

Positive
Negative
Boundary
Security
Session
MFA
Accessibility
O — OUTPUT
Test ID
Scenario
Precondition
Steps
Test Data
Expected Result
Priority
Test Type
Automation Candidate
Source Requirement
Confidence
T — TONE
Professional and suitable for Jira.
🛡️ ANTI-HALLUCINATION
Do not invent requirements.

Do not invent fields.

Do not invent business rules.

Do not assume password complexity.

Do not assume OTP expiration.

Do not assume supported browsers.

If information is missing:

Return:
Requirement Clarification Required.

Separate:

FACT
ASSUMPTION
RECOMMENDATION
🚧 GUARDRAILS
Do not generate production credentials.

Do not expose sensitive information.

Do not execute security attacks.

Do not recommend destructive production actions.

Do not automatically change requirements.

Do not mark a test as Final until human review.

If confidence < 80%:

Status = Human Review Required.
Now we have transformed a simple prompt into something that could eventually be used inside an enterprise AI Testing Agent.

🔥 Real-Time Example — AI Bug Triage Agent
Imagine:

Jira
 ↓
Fetch Bug
 ↓
AI Triage
 ↓
Severity
 ↓
Priority
 ↓
Google Sheets
Our AI evaluates:

Payment successful.

₹25,000 deducted.

Order creation failed.
AI may recommend:

Severity:
Critical

Priority:
P1

Confidence:
93%
But before automatically updating Jira:

Guardrail Validation
Is confidence > 90%?

YES

Is financial impact present?

YES

Is supporting evidence available?

YES

Are mandatory triage fields available?

YES
Only then:

Recommendation Approved
Otherwise:

Human Review Required
This is where AI Agents start becoming much more trustworthy.

🏗️ A Better AI Testing Architecture
Instead of:

Requirement
 ↓
LLM
 ↓
Answer
A safer AI Testing architecture is:

Requirement
      ↓
Context
      ↓
RICE POT Prompt
      ↓
LLM
      ↓
Anti-Hallucination Check
      ↓
Guardrail Validation
      ↓
Confidence Check
      ↓
QA Human Review
      ↓
Approved Test Artifact
For AI Agents:

Jira
 ↓
AI Agent
 ↓
LLM Reasoning
 ↓
Guardrails
 ↓
Tool Permission Check
 ↓
Human Approval if Required
 ↓
Google Sheets / Jira / Automation Tool
This is a massive difference.

🧠 Three Layers Every QA Engineer Should Understand
When building AI-powered testing workflows, I now think about three layers:

1️⃣ Prompt Quality
Use:

RICE POT

to make the instruction clear.

2️⃣ Output Reliability
Use:

Anti-Hallucination Controls

to reduce unsupported answers.

3️⃣ Execution Safety
Use:

Guardrails

to prevent unsafe actions.

So:

RICE POT → Reliability → Guardrails
Or even more simply:

Tell AI what to do → Control what it can claim → Control what it can execute.
🔥 Real-Time Examples Across QA
Test Case Generation
Guardrail:

Never invent missing business requirements.
Requirement Analysis
Guardrail:

Highlight ambiguity instead of filling missing requirements.
API Testing
Guardrail:

Do not execute destructive calls against Production.
Database Testing
Guardrail:

Production DB access must be SELECT-only.
Bug Triage
Guardrail:

Do not automatically update Critical/P0 bugs without human validation.
Automation Generation
Guardrail:

No credentials, hard-coded waits or insecure code.
Security Testing
Guardrail:

Generate approved test scenarios, not uncontrolled attacks.
Production Log Analysis
Guardrail:

Mask credentials, tokens and personal information.
AI Test Data Generation
Guardrail:

Generate synthetic data only; never reproduce actual customer information.
📊 RICE POT + Guardrails Cheat Sheet
LayerPurposeRoleDefine AI personaInstructionsDefine taskContextProvide system knowledgeExamplesDemonstrate expected behaviorParametersDefine boundariesOutputStandardize responseToneControl communicationAnti-HallucinationPrevent unsupported claimsGuardrailsRestrict unsafe behaviorConfidenceExpress uncertaintyHuman ReviewFinal validation

This is much closer to how I believe AI should be used in real QA environments.

🧩 My Reusable Master Prompt for AI Testing
ROLE:

Act as a Senior QA Engineer experienced in
Functional, API, Automation, Database,
Security and Performance Testing.

INSTRUCTIONS:

Analyze the supplied requirement and generate
comprehensive testing recommendations.

CONTEXT:

Application:
[Application]

Feature:
[Feature]

Requirements:
[Requirements]

EXAMPLES:

Provide examples if available.

PARAMETERS:

Cover:

Positive
Negative
Boundary
Security
Integration
Database
Error Handling
Usability

ANTI-HALLUCINATION:

Do not invent requirements.

Do not assume missing business rules.

Do not invent API endpoints.

Do not invent database structures.

Do not assume status codes.

Separate:

Facts
Assumptions
Recommendations

If information is unavailable, return:

Requirement Clarification Required.

GUARDRAILS:

Do not expose credentials.

Do not use real customer data.

Do not recommend destructive Production actions.

Do not automatically approve high-risk decisions.

If confidence is below 80%, return:

Human Review Required.

OUTPUT:

Test Case ID
Scenario
Precondition
Steps
Test Data
Expected Result
Priority
Test Type
Automation Candidate
Source Requirement
Assumption
Confidence
Review Status

TONE:

Professional, concise and suitable for
Jira/Test Management systems.
This is no longer just a prompt.

It starts looking like a policy for an AI QA Agent.

⚠️ The Most Important Lesson From Day 3
AI can generate:

✅ Test Cases

✅ Automation Code

✅ Bug Triage

✅ API Scenarios

✅ Test Data

✅ Requirement Analysis

✅ Security Ideas

✅ Regression Recommendations

But we should never assume:

AI output = Correct output.
Instead:

AI Output
   ↓
Validate Against Source
   ↓
Check Assumptions
   ↓
Check Guardrails
   ↓
Evaluate Confidence
   ↓
Human QA Review
AI should accelerate decision-making.

It should not silently replace QA judgment.

🚀 The Bigger Picture
Today we are manually writing prompts.

Tomorrow we could build:

Jira Requirement
       ↓
AI Agent
       ↓
RICE POT Prompt
       ↓
Requirement Analysis
       ↓
Test Generation
       ↓
Anti-Hallucination Validation
       ↓
Guardrails
       ↓
Confidence Score
       ↓
Human Review
       ↓
Automation
       ↓
Bug Triage
       ↓
Jira / Google Sheets
That is where things become truly interesting.

We are moving from:

Manual Testing
to

Automation Testing
to

AI-Assisted Testing
to

AI-Augmented Quality Engineering 🚀
🎯 Day 03 Key Takeaways
Today I learned:

✅ Why vague prompts create weak QA outputs.

✅ How the RICE POT Framework improves Prompt Engineering.

✅ R — Role

✅ I — Instructions

✅ C — Context

✅ E — Examples

✅ P — Parameters

✅ O — Output

✅ T — Tone

✅ What AI hallucination means for software testing.

✅ Why missing requirements must never be silently invented.

✅ How Anti-Hallucination instructions improve reliability.

✅ What AI Guardrails are.

✅ Why AI Agents need execution boundaries.

✅ Why confidence scoring can be useful.

✅ Why sensitive information must be protected.

✅ Why critical actions should require human review.

My biggest takeaway:

A powerful AI Testing system needs more than a good prompt. It needs context, anti-hallucination controls, guardrails, validation and human judgment.
The future QA Engineer will not simply ask AI:

“Can you generate my test cases?”
They will design systems that ensure AI generates:

🎯 Relevant outputs
📚 Grounded outputs
🛡️ Controlled outputs
🔒 Safe outputs
✅ Verifiable outputs
That is the real journey toward mastering AI Testing.

🔜 Day 04 — Coming Next
Next I will explore:

🔥 Zero-Shot Prompting

🔥 One-Shot Prompting

🔥 Few-Shot Prompting

🔥 How examples influence LLM behavior

🔥 How Few-Shot prompting improves test-case consistency

🔥 Zero-Shot vs One-Shot vs Few-Shot using the same QA requirement

🔥 How to combine these techniques with Guardrails

The journey continues. 🚀

30 Days to Master AI Testing for QA Engineers
Day 03 Complete ✅
#30DaysOfAITesting #AITesting #AIForQA #PromptEngineering #RICEPOT #LLMTesting #GenerativeAI #Guardrails #AIHallucination #ResponsibleAI #QualityEngineering #QAAutomation #SoftwareTesting #TestAutomation #Selenium #Playwright #APITesting #Jira #AITesters #AIEngineering
