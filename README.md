# RICE-POT Framework for Prompt Engineering

RICE-POT is a practical framework for writing clear, complete, and reusable AI prompts. It helps remove ambiguity by defining the AI's role, the task, the relevant background, and the expected response.

## The Framework

| Element | Meaning | Guiding question |
| --- | --- | --- |
| **R** | Role | Who should the AI act as? |
| **I** | Instructions | What should the AI do? |
| **C** | Context | What background information does it need? |
| **E** | Examples | What does a good result look like? |
| **P** | Parameters | What rules, limits, or constraints apply? |
| **O** | Output | How should the response be structured? |
| **T** | Tone | How should the response sound? |

## Reusable Prompt Template

```text
Role:
Act as a [role or subject-matter expert].

Instructions:
[Describe the task clearly using action verbs.]

Context:
[Provide the audience, objective, situation, and relevant background.]

Examples:
[Provide one or more examples of the desired result.]

Parameters:
- Include: [...]
- Exclude: [...]
- Length: [...]
- Constraints: [...]

Output:
Return the answer as [a table, checklist, JSON document, report, code, etc.].

Tone:
Use a [professional, friendly, technical, persuasive, etc.] tone.
```

## Example: Creating Software Test Cases

```text
Role:
Act as a senior QA engineer specializing in web applications.

Instructions:
Create test cases for a user-login feature.

Context:
Users sign in with an email address and password. After five failed
attempts, the account is locked for 15 minutes.

Examples:
Include positive, negative, boundary, security, and usability scenarios.

Parameters:
- Do not invent requirements.
- List unclear requirements separately.
- Assign a priority to every test case.
- Write no more than 15 test cases.

Output:
Return a table with these columns:
Test ID | Scenario | Preconditions | Steps | Expected Result | Priority

Tone:
Be concise, precise, and professional.
```

## Quick Memory Aid

Think of RICE-POT as:

> **Persona + Task + Background + Samples + Rules + Format + Voice**

Not every prompt needs all seven sections. Use the elements that improve clarity, and provide enough detail for the AI to produce a useful response without guessing.
