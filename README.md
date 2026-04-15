# Multi-Agent Orchestrate

A Claude Code skill that turns Claude into a **lead orchestrator**, delegating tasks to the right CLI agent — Codex, Copilot, or Gemini — then synthesizing results into a single answer.

## Overview

Instead of Claude handling everything alone, this skill routes sub-tasks to specialized CLI tools based on their strengths, then cross-checks and synthesizes their outputs.

```
User Request
     │
     ▼
 Claude (Orchestrator)
     │
     ├──► Codex CLI      (coding, file edits, debugging)
     ├──► Copilot CLI    (review, alternatives, PR reasoning)
     └──► Gemini CLI     (architecture, docs, analysis)
          │
          ▼
     Synthesized Answer
```

## Routing Logic

| Task Type | Agent Sequence |
|-----------|---------------|
| `general` | Codex → Copilot |
| `architecture` | Gemini → Codex |
| `high_stakes` | Codex → Copilot → Gemini |
| `documentation` | Gemini → Codex |

## Installation

### As a Claude Code Skill

Copy the skill into your Claude skills directory:

```bash
git clone https://github.com/Chihen-Tai/multi-agent-orchestrate.git \
  ~/.claude/skills/multi-agent-orchestrate
```

Then invoke it in Claude Code with:

```
/multi-agent-orchestrate
```

### Python Orchestrator

A ready-to-use Python orchestrator is available at `/Applications/codes/AI_agent/orchestrator/`.

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

## Prerequisites

All three CLIs must be installed and authenticated:

| CLI | Install | Auth |
|-----|---------|------|
| Codex | `npm install -g @openai/codex` | `codex auth` |
| Copilot | `gh extension install github/gh-copilot` | `gh auth login` |
| Gemini | [Install guide](https://ai.google.dev/gemini-api/docs/gemini-cli) | `gemini auth` |

## CLI Quick Reference

```bash
# Gemini — non-interactive
gemini -p "your prompt"

# Codex — non-interactive
codex exec "your prompt"

# Copilot — non-interactive
gh copilot -- -p "your prompt" --allow-all-tools
```

## Safety Rules

- Never let any CLI make destructive changes without explicit user approval
- Prefer read-only investigation first, then propose edits
- If a task affects many files, ask for a plan before changes
- Never present unverified agent output as fact — always synthesize with judgment

## Known Issues

- Gemini CLI may hit `429 MODEL_CAPACITY_EXHAUSTED` during peak hours — fallback: `gemini -m gemini-2.0-flash -p "..."`
- All three CLIs must be authenticated before the orchestrator runs

## File Structure

```
.
├── SKILL.md      # Claude Code skill definition
└── README.md     # This file
```

## License

MIT
