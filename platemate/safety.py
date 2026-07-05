"""Safety & escalation screening.

The policy is deliberately rule-based and runs FIRST on every request,
before any routing (and regardless of whether an LLM is available): on any
health, medical, disordered-eating, or out-of-scope signal the app refuses
to advise and hands off to the human coach.

The signal list mirrors data/safety_policy.md.
"""

from __future__ import annotations

from .models import Escalation, Situation

# Signals that indicate a health / medical situation.
HEALTH_SIGNALS = [
    "dizzy", "dizziness", "faint", "fainted", "lightheaded", "light-headed",
    "sick", "ill", "illness", "fever", "nausea", "nauseous", "vomit",
    "injury", "injured", "pain", "chest pain", "heart",
]

# Signals of possible disordered-eating patterns.
DISORDERED_SIGNALS = [
    "haven't eaten in days", "havent eaten in days", "not eaten for days",
    "purge", "purging", "laxative", "punish myself", "hate my body",
]

# Requests outside nutrition adaptation → out of scope, coach decides.
OUT_OF_SCOPE_SIGNALS = [
    "medication", "medicine", "prescription", "diagnose", "diagnosis",
    "supplement", "supplements", "steroid", "sarms", "fat burner",
    "training plan", "training program", "workout plan", "change my program",
]

# Repeated skipped meals across days is an escalation trigger even without
# any keyword — the caller passes the count via `skipped_days`.
REPEATED_SKIP_THRESHOLD_DAYS = 2

COACH_HANDOFF = (
    "I'm not going to advise on this one. This is outside what I can safely "
    "help with, so I'm flagging it to your coach right now — please reach out "
    "to them (or a medical professional if you feel unwell). Your plan can wait; "
    "you come first."
)


def screen(text: str, skipped_days: int = 0) -> Escalation | None:
    """Return an Escalation when the message trips the policy, else None."""
    lowered = f" {text.lower()} "
    reasons: list[str] = []

    def matched(signals: list[str]) -> list[str]:
        hits = [s for s in signals if s in lowered]
        # keep only the most specific hit when one signal contains another
        # (e.g. report 'supplements', not both 'supplement' and 'supplements')
        return [h for h in hits if not any(h != o and h in o for o in hits)]

    for sig in matched(HEALTH_SIGNALS):
        reasons.append(f"health signal: '{sig}'")
    for sig in matched(DISORDERED_SIGNALS):
        reasons.append(f"possible disordered-eating signal: '{sig}'")
    for sig in matched(OUT_OF_SCOPE_SIGNALS):
        reasons.append(f"out-of-scope request: '{sig}'")
    if skipped_days >= REPEATED_SKIP_THRESHOLD_DAYS:
        reasons.append(f"repeated skipped meals ({skipped_days} days in a row)")

    if not reasons:
        return None
    return Escalation(reasons=sorted(set(reasons)), message=COACH_HANDOFF)


def screen_situation(situation: Situation, skipped_days: int = 0) -> Escalation | None:
    esc = screen(situation.raw_text, skipped_days=skipped_days)
    if esc:
        situation.health_flags = esc.reasons
    return esc
