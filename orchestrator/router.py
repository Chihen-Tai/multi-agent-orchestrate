"""
Routes a task to the appropriate agent(s) based on task type.

Task types:
  general       - Codex implements, Copilot reviews
  architecture  - Gemini designs, Codex checks feasibility
  high_stakes   - Codex proposes, Copilot reviews, Gemini surfaces edge cases
  documentation - Gemini drafts, Codex verifies accuracy
"""

from agents import ask_codex, ask_copilot, ask_gemini, AgentResult
from typing import Callable


def _codex_implement(task: str) -> str:
    return (
        f"You are handling a repository-aware engineering subtask. "
        f"Inspect relevant context, reason carefully, and return concise actionable output. "
        f"Prefer diffs, exact fixes, root-cause analysis, and test steps. Do not over-explain.\n\n"
        f"Task: {task}"
    )


def _copilot_review(task: str) -> str:
    return (
        f"You are handling a developer-workflow and implementation-support subtask. "
        f"Review the following task for correctness, gaps, and alternatives. "
        f"Be concrete and concise.\n\n"
        f"Task: {task}"
    )


def _gemini_design(task: str) -> str:
    return (
        f"You are handling an independent analysis and design subtask. "
        f"Produce a clean, well-structured answer with tradeoffs, assumptions, and missing risks.\n\n"
        f"Task: {task}"
    )


def _gemini_edgecase(task: str) -> str:
    return (
        f"You are a second-opinion reviewer. Identify edge cases, blind spots, "
        f"and failure modes that may have been missed.\n\n"
        f"Task: {task}"
    )


def _codex_feasibility(task: str) -> str:
    return (
        f"You are checking the feasibility of a proposed design against real code constraints. "
        f"Flag any implementation blockers or concerns.\n\n"
        f"Task: {task}"
    )


def _gemini_draft(task: str) -> str:
    return (
        f"You are drafting clear, developer-friendly documentation. "
        f"Write prose that is accurate, well-structured, and easy to follow.\n\n"
        f"Task: {task}"
    )


def _codex_verify_docs(task: str) -> str:
    return (
        f"You are verifying that documentation is technically accurate. "
        f"Flag any inaccuracies, missing details, or misleading claims.\n\n"
        f"Task: {task}"
    )


ROUTES: dict[str, list[tuple[Callable, str, Callable]]] = {
    "general": [
        (ask_codex, "Codex (implement)", _codex_implement),
        (ask_copilot, "Copilot (review)", _copilot_review),
    ],
    "architecture": [
        (ask_gemini, "Gemini (design)", _gemini_design),
        (ask_codex, "Codex (feasibility)", _codex_feasibility),
    ],
    "high_stakes": [
        (ask_codex, "Codex (implement)", _codex_implement),
        (ask_copilot, "Copilot (review)", _copilot_review),
        (ask_gemini, "Gemini (edge cases)", _gemini_edgecase),
    ],
    "documentation": [
        (ask_gemini, "Gemini (draft)", _gemini_draft),
        (ask_codex, "Codex (verify)", _codex_verify_docs),
    ],
}

VALID_TYPES = list(ROUTES.keys())


def route(task: str, task_type: str) -> list[tuple[str, AgentResult]]:
    """Run all agents for the given task type and return (role, result) pairs."""
    if task_type not in ROUTES:
        raise ValueError(f"Unknown task type '{task_type}'. Choose from: {VALID_TYPES}")

    results = []
    for agent_fn, role, prompt_fn in ROUTES[task_type]:
        scoped_prompt = prompt_fn(task)
        result = agent_fn(scoped_prompt)
        results.append((role, result))
    return results
