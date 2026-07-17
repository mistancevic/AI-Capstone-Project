"""Check-gate screens (DESIGN.md §3 Check step).

Check 4 — output-language screen: the one LLM-authored element (the
coaching line) is scanned against data/banned_language.md; on a hit it is
replaced by the deterministic fallback line. Failures are counted in
aggregate only — the discarded line itself is dropped.
"""

from __future__ import annotations

from . import policy

_failure_count = 0  # aggregate only, for evaluation


def screen_coaching_line(line: str) -> tuple[str, bool]:
    """Return (safe line, was_replaced)."""
    global _failure_count
    banned, fallback = policy.banned_language()
    lowered = line.lower()
    if any(phrase in lowered for phrase in banned):
        _failure_count += 1
        return fallback, True
    return line, False


def screen_failures() -> int:
    return _failure_count
