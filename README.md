# multi-agent-orchestrate

A Claude Code skill that turns Claude into a **lead orchestrator**, delegating tasks to the right CLI agent — Codex, Copilot, or Gemini — then synthesizing results into a single answer.

## Overview

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

Paste this prompt into Claude Code:

```
Please install the multi-agent-orchestrate skill:

git clone https://github.com/Chihen-Tai/multi-agent-orchestrate.git ~/.claude/skills/multi-agent-orchestrate

Then confirm ~/.claude/skills/multi-agent-orchestrate/SKILL.md exists.
```

Then invoke it anytime with:

```
/multi-agent-orchestrate
```

## File Structure

```
.
├── SKILL.md              # Claude Code skill definition
├── README.md             # This file
└── orchestrator/         # Python implementation
    ├── __init__.py
    ├── main.py           # Entry point
    ├── router.py         # Task routing logic
    ├── agents.py         # CLI subprocess wrappers
    └── synthesizer.py    # Output formatter
```

## Python Orchestrator

```bash
cd orchestrator

python main.py "add error handling to login" --type general
python main.py "design a caching layer"      --type architecture
python main.py "refactor the auth module"    --type high_stakes
python main.py "document the REST API"       --type documentation
```

## Prerequisites

All three CLIs must be installed and authenticated:

| CLI | Install | Auth |
|-----|---------|------|
| Codex | `npm install -g @openai/codex` | `codex auth` |
| Copilot | `gh extension install github/gh-copilot` | `gh auth login` |
| Gemini | [Install guide](https://ai.google.dev/gemini-api/docs/gemini-cli) | `gemini auth` |

## Known Issues

- Gemini CLI may hit `429 MODEL_CAPACITY_EXHAUSTED` during peak hours — fallback: `gemini -m gemini-2.0-flash -p "..."`
- All three CLIs must be authenticated before the orchestrator runs

## License

MIT
