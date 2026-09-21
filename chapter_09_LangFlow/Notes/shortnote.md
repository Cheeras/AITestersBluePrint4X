**To Create the AI Agents we have several options**

1. Low Code and No Code Tool
   * n8n, LangFlow
2. Vibe Coding
   * Antigravity
   * VS Code direct
   * Claude Code,Codex,Kiro IDE,Cursor, Windsurf
3. Proper Coding (Python Crew.ai)
   * Crew AI
   * LangChain
   * Autogen
   * Google ADK

**LangFlow**

LangFlow is 100% free and open source

LangFlow actually belong to Lang family, it has lot of Open source tools that are created

1. LangFlow - which is replica of n8n which drag and drop version creation of AI Agents
2. LangChain - Perfectly 100% Code to create AI Agents
3. LangSmith - observability and debugging of AI Agents
4. LangGraph - when you share the things from one agent to another agent - State machine - means share some information from agent to another agent- Multiple agents talking to each other
5. LangFuse
6. LangServe
7. Lang*

But as QA we will learning only  LangFlow and LangChain which is more than enough

**LangFlow:**

LangFlow is a  visual drag and drop builder for creating LLM-powered applications and AI Agent workflows, **no Python required**, but fully extensible when you need it

Advantage of LangFlow is if you create traditional AI agent you have to write a code , install packages, need to debug

but in the case LangFlow Drag and drop the required tools and component and configure them according and see the data flow in real time and export as JSON and download to future reusability

What Makes LangFlow Different from others No-Code Tools?

![image.png](https://eraser.imgix.net/workspaces/bhSR1i1RNhgFLX5vDxgp/WWS31TdyovhjTB1TVo9v2jWpPei1/image_aAXMaFC9d0f8SGvYrnnep.png?ixlib=js-3.8.0)

**Most the companies are using LangFlow suprisingly HDFC Bank,Oracle using the LangFlow**

Wingify use n8n

Tekion uses LangFlow

![image.png](https://eraser.imgix.net/workspaces/bhSR1i1RNhgFLX5vDxgp/WWS31TdyovhjTB1TVo9v2jWpPei1/image_u5G4cvSPuuRWzCQUllL3-.png?ixlib=js-3.8.0)

### When NOT to Use LangFlow

- **High-throughput production pipelines** — If you're processing 10,000+ test results per minute, use code
- **Complex state machines** -> **LangGraph** gives you finer control for intricate branching
- **Custom ML model integration** — If you need custom model fine-tuning, code is better
- **When your team already knows Python well** -> <u>Code gives you more control</u>

### When LangFlow Absolutely Shines

- Rapid prototyping of agent ideas ("Will this workflow even work?")
- Teams with mixed skill levels (manual testers + automation engineers)
- Demonstrating AI capabilities to stakeholders (visual is persuasive)
- Building internal tools that non-developers need to modify
- Connecting LLM reasoning to existing tools (Jira, Slack, APIs)

![image.png](https://eraser.imgix.net/workspaces/bhSR1i1RNhgFLX5vDxgp/WWS31TdyovhjTB1TVo9v2jWpPei1/image_VIHKqdF3ynXQLAy1xN2uo.png?ixlib=js-3.8.0)

## Installation & Setup

1. Local (for the Development) - **Learning**
2. Cloud (Final Deployments) - **Production**
3. By Using Docker Container - Yet to explain how
