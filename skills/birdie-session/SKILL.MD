---
name: birdie-session
description: Summarise the current session and write a handover document to a markdown file, enabling suspend/resume and agent-to-agent handoff.
triggers:
  - summarize session
  - summarise session
  - save session
  - suspend session
  - session handover
  - handover
  - hand off session
  - checkpoint session
  - resume session
  - session summary
---

# Birdie Session Skill

This skill captures the essential state of the current session and writes it to a plain-markdown file so that a human or another agent can resume exactly where things left off.

---

## When to invoke

- The user asks to **suspend**, **save**, **summarise**, or **hand off** the current session.
- The user wants to **resume** a session from a previously written file.
- An agent needs to pass work to a successor agent.

---

## Output file

Name the file `YYYYMMDD-<slug>.md` where:
- `YYYYMMDD` is today's date (e.g. `20260524`)
- `<slug>` is a short, lowercase, hyphen-separated description of the session topic (e.g. `birdie-system-tests`, `auth-refactor`, `api-rate-limiting`)

Write it in the current working directory unless the user specifies a different path.

If an existing file with the same name is present, **overwrite it** — it is a live checkpoint, not an append log.

---

## Document format

Write exactly the following sections, in this order. Omit a section only if it is genuinely empty. Never invent content — every claim must reflect something that actually happened or was said in the session.

```markdown
# Session: <one-line description of the overall goal>

**Date:** YYYY-MM-DD  
**Time:** HH:MM (local, 24 h)  
**Branch:** `<branch-name>` (or "n/a")  
**Repo:** `<absolute path>` (or "n/a")

---

## Project context

<What a successor needs to know about the project to make sense of the session:
 key directories, relevant frameworks, test runner, constraints, anything non-obvious.
 Two to five bullet points. Skip if the repo is self-explanatory from the goal.>

---

## Topic: <what was worked on>

<Describe the specific task or question this session addressed. One short paragraph.>

**<Decision label or outcome>**  
<Explain the agreed approach, or "No code was written — design only." if applicable.>

---

## Conversation log

A compressed, chronological record of the session. Each entry is one of three kinds:

- **Human:** — what the user asked or said (paraphrase; keep intent intact)
- **Agent:** — what the AI decided or explained (key reasoning only; skip filler)
- **Tool:** `tool_name(args)` → outcome or key result (one line; omit trivial calls)

Group closely related turns into a single entry when they form one logical exchange.

> Human: <first message>  
> Agent: <first key decision>  
> Tool: `tool_name(...)` → result  
> Human: <follow-up>  
> ...

---

## <Topic-specific section, e.g. "Agreed design" or "Implementation">

<Use named subsections (###) for distinct parts of the design or implementation.
 Include code blocks for any agreed-upon code, config, or commands.>

---

## Rejected alternatives

<Each alternative that was considered and explicitly ruled out, with the reason.
 Omit this section if nothing was rejected.>

---

## Next steps (not started)

<Ordered list of concrete actions a successor should take.
 Be specific: name files, commands, and services.>

- Create ...
- Write ...
- Add ...
```

---

## Rules

- **Plain markdown only.** No HTML, no frontmatter, no non-standard extensions.
- **Be concrete.** Name files, functions, flags, and commands by their actual names.
- **Be brief.** Each section should be as short as it can be while remaining complete.
- **Do not editorialize.** Report what happened; do not evaluate quality or add opinions.
- **Dates and times are absolute.** Write `2026-05-24` / `14:37`, never "today" or "just now".
- **Conversation log is compressed, not verbatim.** Capture intent and outcomes; discard pleasantries and repeated attempts.
- After writing the file, print the absolute path so the user knows where it landed.

---

## Resuming from a session file

When the user says "resume" and points to a session file (or one matching `????????-*.md` exists in the working directory):

1. Read the file.
2. Announce in three sentences: the goal, the current state, and the first next step.
3. Ask the user whether to proceed with the first next step or redirect.
4. Do not repeat the full document — summarise only.
