D:\Workspace\AITestersBluePrint4X\chapter_08_n8n\Agents

Here is the Problem statement which i want to build. I want you to build an n8n workflow that performs this: a screenshot to bug reporter, where i will be uploading ad image. What you will do is connect to a Git Repo and create a bug report automatically in that project

🔴 Problem

Bug reporting is tedious and inconsistent

📥 Input:UI Screenshot, Error Logs
↓
📤 Output:Jira Bug with Steps to Reproduce

What it does

Analyzes a screenshot of a bug and drafts a complete bug report, including visual details.

👤 Helpful For

Testers who need to file bugs quickly without typing out every visual detail.

🔧 Implementation Guide
n8n

Webhook Trigger (image upload) → OpenAI Vision Node → Structured Output Parser → Jira Node (create issue)

put this file in the @file:Agents folder - 08_Screenshot_To_Bug_Reporter_AIAgent.json

Please lets first research which is cheaper model we can use, I have access to the groq.com and openrouter.io let me know what is the plan in the Plan.md file in the @file:Agents directory of the @file:chapter_08_n8n

ask me for the questions that you want to me answer
