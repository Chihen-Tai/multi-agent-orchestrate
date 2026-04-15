"""
Formats and synthesizes agent outputs into a final report.
"""

from agents import AgentResult


def synthesize(task: str, task_type: str, results: list[tuple[str, AgentResult]]) -> str:
    lines = []
    lines.append("=" * 60)
    lines.append(f"OBJECTIVE: {task}")
    lines.append(f"TASK TYPE: {task_type}")
    lines.append("=" * 60)

    for role, result in results:
        lines.append(f"\n── {role} ──")
        if result.success and result.output:
            lines.append(result.output)
        elif result.error:
            lines.append(f"[ERROR] {result.error}")
        else:
            lines.append("[No output returned]")

    lines.append("\n" + "=" * 60)
    lines.append("SYNTHESIS")
    lines.append("=" * 60)

    successful = [(role, r) for role, r in results if r.success and r.output]
    failed = [(role, r) for role, r in results if not r.success]

    if not successful:
        lines.append("All agents failed. Check CLI availability and authentication.")
    else:
        lines.append(f"{len(successful)}/{len(results)} agent(s) responded successfully.")
        if failed:
            failed_names = ", ".join(role for role, _ in failed)
            lines.append(f"Failed: {failed_names}")
        lines.append("\nReview each agent's output above and apply judgment.")
        lines.append("Resolve disagreements by preferring the more specific or evidence-backed answer.")

    return "\n".join(lines)
