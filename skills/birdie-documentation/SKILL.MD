---
name: birdie-documentation
description: Review and sync Birdie's documentation against its Python implementation. Detects stale, missing, or duplicated content and makes targeted fixes.
triggers:
  - birdie documentation
  - birdie docs
  - sync documentation
  - sync docs
  - update documentation
  - update docs
  - documentation review
  - docs review
  - documentation audit
  - docs out of sync
  - documentation out of date
  - stale documentation
  - missing documentation
---

# Birdie Documentation Skill

This skill governs how to audit and repair Birdie's documentation so it stays
truthful and non-redundant with respect to the Python implementation.

---

## Scope

**Source of truth** – every `.py` file under `birdie/` and its subdirectories
(recursively). This includes `birdie/agent/`, `birdie/core/`, `birdie/skills/`,
`birdie/main.py`, `birdie/cli.py`, etc.

**Documentation files** – exactly:
- `README.md` (project root)
- `doc/cli.md`
- `doc/skills.md`
- `doc/agents.md`
- `doc/mcp.md`
- `doc/architecture.md`

---

## Quality criteria

### 1. Accuracy

Every claim in a documentation file must match the current source code.
Check:
- constants (e.g. `MAX_MESSAGES`, `MIN_MESSAGES`, `COMPRESSION_WINDOW`),
- class names, method signatures, and public API shape,
- file paths mentioned in prose or code blocks,
- flags and config fields (defaults, types, names),
- slash commands and key bindings listed in `doc/cli.md`,
- the project layout diagram in `doc/architecture.md`,
- the provider table in `doc/architecture.md` (vendors, env vars, classes).

When the code and the docs disagree, the code is right. Fix the docs.

### 2. Completeness

Every **public, user-facing** feature must appear somewhere in the documentation:
- a public method on `DynamicAgent` (in `birdie/agent/run.py`),
- a CLI flag or slash command (in `birdie/cli.py`),
- an LLM provider/vendor (in `birdie/core/llm_provider.py`),
- a configurable field accepted by `DynamicAgent.from_config()`,
- a bundled skill or agent (under `birdie/skills/` or `birdie/agents/`).

Internal helpers (prefixed with `_`) and test utilities do not need to be documented.

### 3. De-duplication

Each concept lives in **one** document. Cross-references use links, not repeated prose.

**Ownership map** (if a concept belongs to a file, that file owns the full
explanation; all others may carry one sentence + a link):

| Concept | Owns it |
|---|---|
| CLI flags, slash commands, key bindings | `doc/cli.md` |
| SKILL.MD format, entrypoints, skill loading | `doc/skills.md` |
| AGENT.MD format, sub-agent system | `doc/agents.md` |
| MCP integration, `mcp_server` frontmatter | `doc/mcp.md` |
| Agent loop, system prompt tiers, compaction algorithm, LTM store, providers, sessions, `DynamicAgent` API | `doc/architecture.md` |
| Installation, quick-start, high-level feature summary | `README.md` |

Acceptable duplication: `README.md` may include a one-paragraph summary of any
feature before linking to the owning file. `doc/cli.md` may contain a short
"how automatic compaction works" summary because users arrive there from the
`/compact` command — but the algorithmic detail stays in `doc/architecture.md`.
Any other repetition is a bug.

### 4. Single-topic files

No file should mix unrelated topics. `doc/architecture.md` covers internal
implementation; `doc/cli.md` covers the user-facing interface. If a section
reads like architecture inside a CLI reference, move the algorithmic content
to `doc/architecture.md` and replace it with a prose summary + link.

---

## Workflow

### Step 1 – Collect source facts

Read the relevant Python files. Extract:
- public constants and their values,
- class names and their public methods,
- CLI flags (`argparse` or equivalent in `birdie/cli.py`),
- slash commands (the dispatch table in `birdie/cli.py`),
- key bindings,
- provider classes and vendor names (`birdie/core/llm_provider.py`),
- config fields consumed in `DynamicAgent.from_config()` (`birdie/agent/run.py`),
- entrypoint schemes (`birdie/core/entrypoints.py`),
- SKILL.MD frontmatter fields parsed by `birdie/core/loader.py`,
- AGENT.MD frontmatter fields parsed by `birdie/core/agent_loader.py`.

### Step 2 – Read all documentation files

Read `README.md` and each file in `doc/`. Do not skip any.

### Step 3 – Compare and build a findings list

For each documentation file, identify:

**Stale** – the doc says X but the code says Y (wrong constant, removed flag,
renamed class, etc.).

**Missing** – a public feature exists in code with no matching documentation.

**Duplicated** – the same explanation appears in two or more files beyond the
permitted one-sentence-plus-link context setup.

**Misplaced** – a topic is documented in the wrong file per the ownership map.

Number every finding. State the file, the line range (if stale), and the
specific fix needed.

### Step 4 – Fix

Make targeted edits. Do not rewrite sections that are correct. Do not introduce
new prose beyond what is needed to describe the facts. Match the existing
writing style: present tense, no passive voice, imperative for instructions,
code samples for every non-trivial configuration option.

When a section is removed from one file because it belongs in another:
- In the source file, replace it with one sentence summarising the concept
  and a Markdown link to the owning file and section heading.
- In the owning file, integrate the content at the correct location.

After every edit, re-read the surrounding paragraph to confirm the transition
is coherent.

### Step 5 – Verify

After all edits are complete:
1. Re-read each changed file from top to bottom.
2. Confirm every claim now matches the code.
3. Confirm no finding from Step 3 remains unaddressed.
4. Report a summary: N files changed, list of findings fixed.

---

## Common gotchas

- `doc/architecture.md` currently has a duplicate **System prompt** top-level
  section (appears at line ~443 and again at line ~689). The second occurrence
  is a stub. Deduplicate: keep whichever is more complete, remove the other.

- `doc/cli.md` contains a `/compact` description that partially re-explains the
  compaction algorithm. The CLI file may keep the user-facing behaviour (what
  the command does, example output, configuring thresholds via JSON config), but
  algorithmic internals (split point logic, `RemoveMessage` mechanism, LTM
  write path) belong solely in `doc/architecture.md`. Use a link.

- `README.md` describes memory in a multi-paragraph section; the detail
  duplicates `doc/architecture.md`. The README section is allowed as a summary,
  but should end with a link to `doc/architecture.md` for full detail — verify
  the link exists and points to the correct anchor.

- The project layout diagram in `doc/architecture.md` must match the actual
  directory tree under `birdie/`. Re-run `find birdie -name "*.py" | sort` and
  compare. Pay particular attention to `acp_mcp_server.py` and `errors.py`
  which exist in the source but may be absent from the diagram.

- `birdie/core/errors.py` — check whether it defines public exception types
  that should be mentioned in `doc/architecture.md` or the API surface.

- `birdie/core/models.py` defines the data models (`Skill`, `SkillTool`,
  `AgentDef`, `MCPServerConfig`). Verify that the field descriptions in
  `doc/skills.md` and `doc/agents.md` match the actual dataclass fields.
