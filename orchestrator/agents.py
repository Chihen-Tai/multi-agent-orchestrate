"""
Subprocess wrappers for each CLI agent.
Each function runs the agent non-interactively and returns its stdout as a string.
"""

import subprocess
import shutil
from dataclasses import dataclass


@dataclass
class AgentResult:
    agent: str
    output: str
    error: str
    success: bool


def _run(cmd: list[str], timeout: int = 120) -> tuple[str, str, bool]:
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return result.stdout.strip(), result.stderr.strip(), result.returncode == 0
    except subprocess.TimeoutExpired:
        return "", f"Timed out after {timeout}s", False
    except FileNotFoundError as e:
        return "", f"CLI not found: {e}", False


def ask_gemini(prompt: str, timeout: int = 120) -> AgentResult:
    if not shutil.which("gemini"):
        return AgentResult("gemini", "", "gemini CLI not found in PATH", False)
    stdout, stderr, ok = _run(["gemini", "-p", prompt], timeout=timeout)
    return AgentResult("gemini", stdout, stderr, ok)


def ask_codex(prompt: str, timeout: int = 120) -> AgentResult:
    if not shutil.which("codex"):
        return AgentResult("codex", "", "codex CLI not found in PATH", False)
    stdout, stderr, ok = _run(["codex", "exec", prompt], timeout=timeout)
    return AgentResult("codex", stdout, stderr, ok)


def ask_copilot(prompt: str, timeout: int = 120) -> AgentResult:
    if not shutil.which("gh"):
        return AgentResult("copilot", "", "gh CLI not found in PATH", False)
    stdout, stderr, ok = _run(
        ["gh", "copilot", "--", "-p", prompt, "--allow-all-tools"],
        timeout=timeout,
    )
    return AgentResult("copilot", stdout, stderr, ok)
