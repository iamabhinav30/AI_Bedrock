---
name: prompt-engineer
description: >
  Use this skill whenever the user wants to write, improve, fix, or review a prompt for any AI model — especially Claude, ChatGPT, Copilot, or any LLM. Triggers include: "help me write a prompt", "improve this prompt", "my prompt isn't working", "write a prompt for X", "how do I ask the AI to...", "make this prompt better", "review my prompt", or any time the user pastes a prompt and seems unsatisfied with results. Also trigger when the user describes a task they want an AI to do but hasn't written the prompt yet — offer to write one using the four-technique framework. This skill turns vague AI requests into precise, structured, high-performing prompts.
---

# Prompt Engineer

A skill for writing, improving, and structuring prompts that get great results from AI models — based on Anthropic's four-technique framework.

---

## The Four Techniques (Always Apply All Four)

### 1. Be Clear and Direct
- **Lead with an explicit action verb**: Write, Summarize, Extract, Compare, Generate, Classify, Translate, Rewrite, List, Explain
- Put the instruction in the very first sentence — never bury it
- Use simple, plain language — no ambiguity
- State WHO the AI should act as (if relevant): "You are a senior software engineer..."

**Before:** `I need something about customer feedback analysis`
**After:** `Analyze the customer feedback below and identify the top 3 recurring complaints.`

---

### 2. Be Specific
- Add concrete requirements: length, format, tone, audience, constraints
- Spell out what to include AND what to exclude
- Break complex tasks into numbered steps
- Specify the output format explicitly (bullet list, JSON, table, paragraph, etc.)

**Add specifics like:**
- `Respond in under 150 words`
- `Use a professional but friendly tone`
- `Do not include any code — plain English only`
- `Format as a numbered list with a one-sentence explanation per item`

---

### 3. Structure with XML Tags
Use tags to clearly separate different types of content in the prompt. This prevents the model from confusing instructions with input data.

**Common tag patterns:**
```
<instructions> ... </instructions>
<context> ... </context>
<document> ... </document>
<input> ... </input>
<format> ... </format>
<example> ... </example>
<constraints> ... </constraints>
```

**Use when the prompt has:**
- A document or text to work on
- User-provided input that's separate from instructions
- Multiple distinct sections (role + task + format)
- Examples alongside instructions

---

### 4. Provide Examples
- Include at least one input → output example for format-sensitive tasks
- Use examples to show edge cases or special handling
- For negative examples, label them clearly: `# Bad output:` / `# Good output:`
- Wrap examples in `<example>` tags when combining with other content

---

## Workflow: How to Help the User

### Step A — Understand the Goal
Ask (or infer from context):
1. What task should the AI perform?
2. What is the input? (text, code, data, image, nothing)
3. What should the output look like? (format, length, tone)
4. Which AI model is this for? (Claude, Copilot, ChatGPT, etc.)
5. Any constraints? (length, language, audience, what to avoid)

If the user pastes an existing prompt, diagnose it first (see Diagnosis section below).

---

### Step B — Write or Rewrite the Prompt

Always produce the improved prompt inside a clearly labelled code block so the user can copy it easily:

```
[IMPROVED PROMPT]

<your prompt here>
```

Then briefly explain (2–3 sentences max) what you changed and why.

---

### Step C — Offer Variants (Optional)
For high-stakes prompts, offer 2 variants:
- **Concise version** — minimal, fast
- **Detailed version** — fully specified, with examples and tags

---

## Diagnosis: When the User Shares a Broken Prompt

Check for these failure patterns in order:

| Problem | Symptom | Fix |
|---|---|---|
| No action verb | Vague, meandering response | Add explicit verb at line 1 |
| No specifics | Too long / wrong format | Add length, tone, format rules |
| Mixed content | Model confuses instructions with data | Add XML tags to separate sections |
| No examples | Wrong style or structure | Add 1–2 input/output examples |
| Too long | Model loses track | Split into smaller focused prompts |
| Contradictory | Inconsistent output | Remove conflicting instructions |

---

## Prompt Templates by Use Case

### Summarization
```
Summarize the following <document> in exactly 3 bullet points.
Each bullet should be one sentence. Focus on key decisions and outcomes only.

<document>
{{PASTE TEXT HERE}}
</document>
```

### Content Generation
```
Write a [FORMAT] about [TOPIC] for [AUDIENCE].

Requirements:
- Length: [X words / X paragraphs]
- Tone: [professional / casual / persuasive]
- Include: [specific elements]
- Avoid: [specific elements]
```

### Data Extraction
```
Extract the following fields from the text below and return as JSON.

Fields to extract:
- name
- date
- amount
- status

<text>
{{PASTE TEXT HERE}}
</text>

Return only valid JSON. No explanation.
```

### Code Tasks
```
You are a senior [LANGUAGE] developer.

<task>
[Describe what the code should do]
</task>

<constraints>
- Do not use external libraries
- Add a comment for each function
- Handle edge cases: [list them]
</constraints>

Return only the code. No explanation unless asked.
```

### Review / Critique
```
Review the following [DOCUMENT TYPE] and provide structured feedback.

<document>
{{PASTE CONTENT HERE}}
</document>

For each issue found, provide:
1. What the problem is
2. Why it matters
3. A specific suggestion to fix it

Focus on [clarity / logic / grammar / tone / structure]. Ignore [minor typos / formatting].
```

---

## Copilot-Specific Tips

Since the user is working with **Microsoft Copilot**, keep these in mind:

- Copilot works well with **role framing**: `"Act as a project manager and..."`
- Use **slash commands** where available (`/summarize`, `/rewrite`, `/explain`)
- For Word/Excel Copilot: be explicit about the target cell range or document section
- Copilot in Teams/Outlook: always specify the audience (`"Write for a non-technical stakeholder"`)
- Keep prompts **under 500 characters** for chat Copilot; longer prompts work better in Copilot Studio
- Use **follow-up prompts** to refine: after the first output, prompt `"Make it more concise"` or `"Add a section on risks"`

---

## Output Format for Delivering Prompts

Always structure your response like this:

```
## Improved prompt

[paste the full ready-to-use prompt here in a code block]

## What changed
[2–3 sentences explaining the key improvements]

## Tips for using it
[1–2 optional tips if the user might want to tweak it further]
```

Keep explanations short. The prompt itself is the deliverable.
