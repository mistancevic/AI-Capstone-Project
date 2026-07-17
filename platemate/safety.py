"""Safety & escalation screening — the deterministic floor.

Runs FIRST on every request, on the raw text, before any parsing, routing,
or model call (DESIGN.md §2 step 2). The signal lists and thresholds mirror
data/safety_policy.md; all client-facing wording comes from that file's
pre-authored blocks — never from a model.

Asymmetric LLM assist (design): an optional classifier may ADD a stop for
paraphrased signals a keyword list misses — it can never clear one. With
the model off (this build), the deterministic floor holds every case that
keyword or counter can catch.

Tier logic (the faculty tier distinction):
  - health / multi-day undereating / restriction-below-floor / counter
    thresholds → HARD STOP, urgent flag.
  - compensatory ask or skip-intent, 1st or 2nd in the rolling week →
    run CONTINUES with a templated nudge; counter increments; digest entry.
    3rd in the rolling week → HARD STOP, urgent.
  - out-of-scope → decline + point to coach; digest entry.
  - hostility alone → tone changes, verdict never does.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from .escalation import Tier

# --------------------------------------------------------------------- #
#  Signal lists (mirror data/safety_policy.md)
# --------------------------------------------------------------------- #

HEALTH_SIGNALS = [
    "dizzy", "dizziness", "faint", "fainted", "lightheaded", "light-headed",
    "chest pain", "fever", "nausea", "nauseous", "vomit", "injury", "injured",
    "heart racing", "can't keep food down",
]

DISORDERED_HARD_SIGNALS = [
    "purge", "purging", "laxative", "punish myself", "hate my body",
]

# Multi-day undereating self-report — disclosure alone must trigger even
# when the tracked counter is at zero (the silent-skipper variant, Case 7).
_MULTIDAY_RE = re.compile(
    r"(haven'?t|havent|not|barely)\s+(been\s+)?eat\w*[^.!?]{0,40}?\b(days|week)", re.I
)

# Compensatory / skip-intent family — tiered by counter, not an instant stop.
COMPENSATORY_SIGNALS = [
    "make up for", "eat less today", "eat less to", "skip dinner and go hungry",
    "won't eat", "wont eat", "just not eat", "go hungry",
]

OUT_OF_SCOPE_SIGNALS = [
    "medication", "medicine", "prescription", "diagnose", "diagnosis",
    "supplement", "supplements", "steroid", "sarms", "fat burner",
    "training plan", "training program", "workout plan", "change my program",
    "change my targets",
]

HOSTILITY_SIGNALS = ["useless", "stupid app", "hate this app", "garbage app"]

# Explicit restriction DEMAND below the compliance floor: "give me an
# 800-kcal plan". A demand needs demand context — a bare calorie mention
# ("team dinner around 1000 kcal") is data, not a request. (This exact
# distinction was the first eval failure: the naive number-regex hard-
# stopped the happy path on the dinner estimate.)
_KCAL_DEMAND_RE = re.compile(
    r"(?:give me|build me|make me|put me on|i want|i need)\s+(?:an?\s+|just\s+)*(\d{3,4})\s*[- ]?\s*(?:kcal|calorie)"
    r"|(\d{3,4})\s*[- ]?\s*(?:kcal|calorie)\s+(?:plan|day|reset|limit|max)",
    re.I,
)

REPEATED_SKIP_THRESHOLD_DAYS = 2
COMPENSATORY_HARD_STOP_COUNT = 3


@dataclass
class SafetyVerdict:
    """Outcome of the raw-text screen. `action` drives the orchestrator."""

    action: str                    # "continue" | "nudge" | "stop" | "decline_oos"
    tier: Tier | None = None
    reasons: list[str] = field(default_factory=list)
    get_help_now: bool = False
    hostile: bool = False
    counters: dict[str, int] = field(default_factory=dict)  # updated counts


def _hits(text: str, signals: list[str]) -> list[str]:
    lowered = text.lower()
    found = [s for s in signals if s in lowered]
    return [h for h in found if not any(h != o and h in o for o in found)]


def screen(text: str, skipped_days: int = 0, compensatory_asks_week: int = 0,
           target_kcal: int | None = None) -> SafetyVerdict:
    """The deterministic floor. Counters come in seeded, go out updated —
    counts survive; the raw message does not (memory design)."""
    stop_reasons: list[str] = []
    get_help_now = False
    counters = {"skipped_days": skipped_days,
                "compensatory_asks_week": compensatory_asks_week}

    for sig in _hits(text, HEALTH_SIGNALS):
        stop_reasons.append(f"health signal: '{sig}'")
        get_help_now = True

    for sig in _hits(text, DISORDERED_HARD_SIGNALS):
        stop_reasons.append(f"disordered-eating signal: '{sig}'")

    if _MULTIDAY_RE.search(text):
        stop_reasons.append("multi-day undereating self-report")

    m = _KCAL_DEMAND_RE.search(text)
    if m:
        demanded = int(m.group(1) or m.group(2))
        floor = max(1200, int(0.7 * target_kcal)) if target_kcal else 1200
        if demanded < floor:
            stop_reasons.append(
                f"restriction demand below compliance floor ({demanded} kcal)")

    if skipped_days >= REPEATED_SKIP_THRESHOLD_DAYS:
        stop_reasons.append(f"skipped-meals counter at {skipped_days} days")

    hostile = bool(_hits(text, HOSTILITY_SIGNALS))

    compensatory = bool(_hits(text, COMPENSATORY_SIGNALS))
    if compensatory:
        counters["compensatory_asks_week"] += 1
        if counters["compensatory_asks_week"] >= COMPENSATORY_HARD_STOP_COUNT:
            stop_reasons.append(
                f"compensatory ask #{counters['compensatory_asks_week']} in rolling week")

    if stop_reasons:
        return SafetyVerdict(action="stop", tier=Tier.URGENT,
                             reasons=sorted(set(stop_reasons)),
                             get_help_now=get_help_now, hostile=hostile,
                             counters=counters)

    if compensatory:
        # 1st or 2nd ask: the run continues — food, not refusal (Case 3).
        return SafetyVerdict(action="nudge", tier=Tier.DIGEST,
                             reasons=[f"compensatory ask #{counters['compensatory_asks_week']} in rolling week"],
                             hostile=hostile, counters=counters)

    oos = _hits(text, OUT_OF_SCOPE_SIGNALS)
    if oos:
        return SafetyVerdict(action="decline_oos", tier=Tier.DIGEST,
                             reasons=[f"out-of-scope request: '{s}'" for s in oos],
                             hostile=hostile, counters=counters)

    if hostile:
        # Hostility alone: digest note; verdict unchanged.
        return SafetyVerdict(action="continue", tier=Tier.DIGEST,
                             reasons=["hostility (tone only)"],
                             hostile=True, counters=counters)

    return SafetyVerdict(action="continue", counters=counters)
