"""Sleep & recovery agent.

Consulted by the orchestrator when a food decision also touches sleep or
tomorrow's training — the canonical case being a late dinner. It only ever
annotates the nutrition recommendation; it never overrides the plan.
"""

from __future__ import annotations

from ..models import ClientProfile, Situation

LATE_HOUR = 20  # meals at/after 20:00 count as "late"


def _hour(time_str: str) -> int | None:
    try:
        return int(time_str.split(":")[0])
    except (ValueError, AttributeError, IndexError):
        return None


def is_late(situation: Situation) -> bool:
    if "late" in situation.meal_time.lower():
        return True
    hour = _hour(situation.meal_time)
    return hour is not None and hour >= LATE_HOUR


def should_consult(situation: Situation) -> bool:
    """The orchestrator consults us when the meal being solved is late, or a
    known upcoming commitment is a late dinner."""
    if is_late(situation):
        return True
    return any("dinner" in label.lower() for label, _, _ in situation.upcoming_fixed)


def advise(situation: Situation, profile: ClientProfile) -> str:
    notes: list[str] = []

    if is_late(situation) or any("dinner" in l.lower() for l, _, _ in situation.upcoming_fixed):
        notes.append(
            f"Aim to finish the late meal 2-3 h before your usual bedtime "
            f"({profile.usual_bedtime}); keep it lighter on fat and easy on "
            "alcohol so it doesn't cut into deep sleep."
        )
    if profile.training_tomorrow:
        notes.append(
            "You train tomorrow — anchor tonight's protein (it supports "
            "overnight recovery) and don't go to bed heavily under-fuelled, "
            "or the session will feel flat."
        )
    if not notes:
        notes.append("No sleep or training conflict with this meal — timing is fine as planned.")
    return " ".join(notes)
