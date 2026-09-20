# Plan: Screenshot to Bug Reporter — n8n AI Agent

## Overview

Build an n8n workflow that accepts a UI screenshot URL, analyzes it using a vision-capable LLM, and automatically creates a structured GitHub issue with the bug report.

---

## 🔬 Model Research — Cost Comparison

### OpenRouter Vision Models (Cheapest First)

| Model | Input Price | Output Price | Notes |
|---|---|---|---|
| **DeepSeek V4 Flash Vision Exp (batch)** | **$0.11/M tokens** | **$0.33/M tokens** | ✅ **Selected — cheapest vision model** |
| DeepSeek V4 Flash Vision Exp | $0.2156/M tokens | $0.6468/M tokens | Standard (non-batch) |
| Other vision models (GPT-4o, Claude, Gemini) | $2.50–$15/M tokens | $10–$75/M tokens | Too expensive for this use case |

### Groq Vision Models

Groq offers **Llama 3.2 11B Vision** (free tier available) but:
- Free tier has rate limits (30 req/min, 15k req/day)
- Vision support is available but less mature for structured output parsing
- No batch pricing available

### ✅ Decision: OpenRouter — DeepSeek V4 Flash Vision Exp (batch)

**Why:**
- Cheapest vision model available ($0.11/M input tokens)
- 1.05M context window — plenty for screenshot analysis
- Good at structured output (JSON mode supported)
- You already have OpenRouter access
- Batch pricing = ~50% cheaper than standard

**Estimated cost per screenshot:**
- ~1 screenshot = ~1,000–2,000 image tokens + ~500 text tokens
- Cost per analysis: **~$0.0002–$0.0005** (fractions of a cent)

---

## 🏗️ Architecture

```
User POSTs image URL
        │
        ▼
┌───────────────────┐
│   Webhook Node    │  Receives { "imageUrl": "https://..." }
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│ HTTP Request Node │  Downloads the image (binary)
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│   Code Node #1    │  Converts binary → base64
│                   │  Constructs OpenRouter API payload
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│ HTTP Request Node │  POST to OpenRouter API
│ (OpenRouter API)  │  Model: deepseek/deepseek-v4-flash-vision-exp:batch
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│   Code Node #2    │  Parses LLM response → structured bug report
│                   │  Extracts: title, description, steps, expected/actual, env
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│   GitHub Node     │  Creates issue in Cheeras/AITestersBluePrint4X
│ (Create Issue)    │  With title, body (markdown), labels
└────────┬──────────┘
         │
         ▼
    Response to User
  (Issue URL + summary)
```

---

## 📋 Workflow Nodes (6 nodes)

| # | Node Type | n8n TypeVersion | Purpose |
|---|---|---|---|
| 1 | **Webhook** | v1 | Receive POST with `imageUrl` |
| 2 | **HTTP Request** | v4.2 | Download image from URL (GET, binary) |
| 3 | **Code (JavaScript)** | v2 | Convert binary to base64, build OpenRouter payload |
| 4 | **HTTP Request** | v4.2 | Call OpenRouter `/chat/completions` with vision model |
| 5 | **Code (JavaScript)** | v2 | Parse LLM JSON response → structured bug fields |
| 6 | **GitHub** | **v2** | Create issue in repo with bug report |

---

## 📝 System Prompt for Vision LLM

```
You are a QA engineer analyzing a UI screenshot for bugs.
Examine the image carefully and return a JSON object with:

{
  "title": "Short, descriptive bug title (max 80 chars)",
  "description": "Clear description of what the bug is",
  "steps_to_reproduce": ["Step 1", "Step 2", "..."],
  "expected_behavior": "What should happen",
  "actual_behavior": "What actually happens (the bug)",
  "environment": "Browser/OS/Device info if visible",
  "severity": "Critical/Major/Minor/Trivial",
  "visual_clues": ["List of visual anomalies seen in screenshot"]
}

Focus on visual defects: layout breaks, alignment issues, missing elements,
color contrast problems, text truncation, overlapping elements, etc.
```

---

## 🔧 Implementation Steps

1. Create the n8n workflow JSON with all 6 nodes and connections
2. Save as `08_Screenshot_To_Bug_Reporter_AIAgent.json` in `Agents/` folder
3. Import into n8n instance
4. Configure credentials:
   - **OpenRouter API** — Create a credential of type `Header Auth` or use the native `$credentials.openRouterApi.apiKey` reference in the Authorization header
   - **GitHub** — Create a GitHub OAuth2 or Personal Access Token credential (repo: `Cheeras/AITestersBluePrint4X`)
5. Activate workflow
6. Test: POST `{ "imageUrl": "<screenshot-url>" }` to webhook

---

## 📦 Final JSON — Key Details

| Property | Value |
|---|---|
| **Workflow name** | `08_Screenshot_To_Bug_Reporter_AIAgent` |
| **GitHub node version** | `typeVersion: 2` (latest n8n) |
| **OpenRouter auth** | `Bearer {{ $credentials.openRouterApi.apiKey }}` |
| **Model** | `deepseek/deepseek-v4-flash-vision-exp:batch` |
| **Webhook path** | `screenshot-to-bug` |
| **Response format** | `json_object` (structured output) |

---

## 📤 Expected Output

A GitHub issue created in `Cheeras/AITestersBluePrint4X` with:

**Title:** `[Bug] Login button overlaps with password field on mobile viewport`

**Body (Markdown):**
```markdown
## Description
The login button overlaps with the password field when viewed at 375px width.

## Steps to Reproduce
1. Open the login page on a mobile device (375px viewport)
2. Enter credentials
3. Observe the login button position

## Expected Behavior
Login button should be below the password field with 16px spacing.

## Actual Behavior
Login button overlaps with password field by ~10px.

## Environment
Chrome 120, Android 14, Pixel 7

## Visual Clues
- Button positioned at absolute bottom: 0
- Password field has no bottom margin
- No media query for mobile viewport
```

---

## 🚫 Out of Scope (for now)

- Binary file upload (using URL only for simplicity)
- Multiple screenshot support
- JIRA integration (using GitHub issues instead)
- Email/Slack notification on new bug
- Auto-assign to team members