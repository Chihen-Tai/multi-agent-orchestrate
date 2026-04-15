---
name: multi-agent-orchestrate
description: Orchestrate tasks across Codex CLI, Copilot CLI, and Gemini CLI. Routes by task type, collects outputs, and synthesizes a final answer.
origin: local
---

# Multi-Agent Orchestrator

Claude acts as **lead orchestrator** — not the sole implementer. Tasks are decomposed and delegated to the right CLI specialist, then synthesized into a final answer.

## When to Use

Invoke this skill when the user asks to:
- Build, fix, debug, or refactor code → delegate to Codex first
- Review or get a second opinion → add Copilot
- Design architecture or brainstorm → start with Gemini
- Do anything high-stakes (auth, payments, large refactors) → use all three

## Agent Roles

| Agent | Strength | Invoke when |
|-------|----------|-------------|
| **Codex CLI** | Repo-aware coding, file edits, debugging, tests | Implementing, fixing, inspecting files |
| **Copilot CLI** | Developer workflow, alternatives, PR reasoning | Reviewing, suggesting alternatives |
| **Gemini CLI** | Broad design, summarization, edge-case analysis | Architecture, docs, second opinion |

## Routing Table

| Task type | Agent sequence |
|-----------|---------------|
| `general` | Codex (implement) → Copilot (review) |
| `architecture` | Gemini (design) → Codex (feasibility) |
| `high_stakes` | Codex → Copilot → Gemini |
| `documentation` | Gemini (draft) → Codex (verify) |

## Python Orchestrator (already built)

Located at `/Applications/codes/AI_agent/orchestrator/`.

```bash
cd /Applications/codes/AI_agent/orchestrator

# General coding task
python main.py "add error handling to login" --type general

# Architecture decision
python main.py "design a caching layer" --type architecture

# High-risk change
python main.py "refactor the auth module" --type high_stakes

# Documentation
python main.py "document the REST API" --type documentation
```

## CLI Invocation Patterns

```bash
# Gemini — non-interactive
gemini -p "your prompt"

# Codex — non-interactive
codex exec "your prompt"

# Copilot — non-interactive
gh copilot -- -p "your prompt" --allow-all-tools
```

## Orchestration Protocol (for Claude)

When orchestrating manually (without the Python script):

1. **Restate** the user's goal in one paragraph
2. **Decompose** into atomic sub-tasks
3. **Delegate** — give each CLI a sharply scoped prompt with: goal, context, constraints, expected output format
4. **Cross-check** — if agents disagree, identify the disagreement and resolve with evidence
5. **Synthesize** — report structure:
   - Objective
   - Delegation plan
   - Findings from each agent
   - Cross-check / disagreements
   - Final synthesis
   - Recommended next action

## Prompt Templates

**Codex:**
> "You are handling a repository-aware engineering subtask. Inspect relevant files, reason carefully, return concise actionable output. Prefer diffs, exact fixes, root-cause analysis. Do not over-explain. Task: {task}"

**Copilot:**
> "You are handling a developer-workflow subtask. Review for correctness, gaps, and alternatives. Be concrete and concise. Task: {task}"

**Gemini:**
> "You are handling an independent analysis subtask. Produce a clean answer with tradeoffs, assumptions, and missing risks. Task: {task}"

## Known Issues

- Gemini CLI may hit 429 (`MODEL_CAPACITY_EXHAUSTED`) during peak hours — the orchestrator handles this gracefully and reports the error without crashing
- Gemini uses model `gemini-3.1-pro-preview` by default; fallback: `gemini -m gemini-2.0-flash -p "..."`
- All three CLIs must be authenticated before use

## Safety Rules

- Never let any CLI make destructive changes without explicit user approval
- Prefer read-only investigation first, then propose edits
- If a task affects many files, ask for a plan before changes
- Never present unverified agent output as fact — always synthesize with judgment
