"""Optional Claude-powered layer.

Two jobs, both with rule-based fallbacks so the whole app runs offline:

  1. parse a free-text disrupted-day message into a structured Situation
  2. write the closing coaching line for a recommendation

The safety screen (platemate.safety) always runs BEFORE anything here and is
never delegated to the model. If the anthropic SDK is missing or no
credentials resolve, `available()` is False and callers use the fallbacks.
"""

from __future__ import annotations

import os
from typing import Optional

from .models import Recommendation, Situation, Trigger

MODEL = "claude-opus-4-8"

try:
    import anthropic
    from pydantic import BaseModel, Field

    _SDK = True
except ImportError:  # pragma: no cover
    _SDK = False

_client = None


def available() -> bool:
    return _SDK and bool(os.environ.get("ANTHROPIC_API_KEY") or os.environ.get("ANTHROPIC_AUTH_TOKEN"))


def _get_client():
    global _client
    if _client is None:
        _client = anthropic.Anthropic()
    return _client


if _SDK:

    class _FoodEvent(BaseModel):
        label: str
        calories_kcal: int = Field(description="best estimate in kcal")
        protein_g: int = Field(description="best estimate in grams of protein")

    class _ParsedSituation(BaseModel):
        trigger: str = Field(
            description="one of: off_plan_extra, surprise_meal, must_skip, "
            "morning_check, on_the_spot_swap, unknown"
        )
        eaten_off_plan: list[_FoodEvent] = Field(default_factory=list)
        completed_meals: list[str] = Field(
            default_factory=list, description="planned meals already eaten as planned, e.g. ['breakfast']"
        )
        upcoming_fixed: list[_FoodEvent] = Field(
            default_factory=list, description="commitments that will definitely happen, e.g. a team dinner"
        )
        meal_to_solve: str = Field(description="the meal slot to recommend for, e.g. 'lunch'")
        skipped_meals: list[str] = Field(default_factory=list)
        meal_time: str = Field(default="", description="HH:MM if the solved meal has a known (esp. late) time")


_PARSE_SYSTEM = (
    "You turn a coached nutrition client's free-text message about a disrupted day "
    "into a structured situation record. Estimate calories and protein conservatively "
    "and realistically when the client gives only a food name. Do not give advice."
)


def parse_situation(text: str) -> Optional[Situation]:
    """LLM path for turning free text into a Situation. Returns None on any
    failure so the caller can fall back to the rule-based parser."""
    if not available():
        return None
    try:
        response = _get_client().messages.parse(
            model=MODEL,
            max_tokens=2048,
            thinking={"type": "adaptive"},
            system=_PARSE_SYSTEM,
            messages=[{"role": "user", "content": text}],
            output_format=_ParsedSituation,
        )
        parsed = response.parsed_output
        try:
            trigger = Trigger(parsed.trigger)
        except ValueError:
            trigger = Trigger.UNKNOWN
        return Situation(
            raw_text=text,
            trigger=trigger,
            eaten_off_plan=[(e.label, e.calories_kcal, e.protein_g) for e in parsed.eaten_off_plan],
            completed_meals=parsed.completed_meals,
            upcoming_fixed=[(e.label, e.calories_kcal, e.protein_g) for e in parsed.upcoming_fixed],
            meal_to_solve=parsed.meal_to_solve or "lunch",
            skipped_meals=parsed.skipped_meals,
            meal_time=parsed.meal_time,
        )
    except Exception:
        return None


def coaching_line(rec: Recommendation, client_name: str) -> str:
    """One warm, non-judgmental closing line. Falls back to a canned line."""
    fallback = (
        "One imperfect day doesn't break a plan — hit your protein, enjoy the "
        "meal, and we rebalance across the week."
    )
    if not available():
        return fallback
    try:
        summary = "; ".join(rec.math.lines())
        response = _get_client().messages.create(
            model=MODEL,
            max_tokens=200,
            system=(
                "You are a supportive nutrition coach's assistant. Write ONE short, "
                "warm, non-judgmental sentence (no emoji) that reassures the client "
                "and reinforces: protein is the daily anchor, calories average out "
                "over 3-7 days, and skipping meals is never the answer."
            ),
            messages=[{"role": "user", "content": f"Client {client_name}. Day math: {summary}"}],
        )
        text = next((b.text for b in response.content if b.type == "text"), "").strip()
        return text or fallback
    except Exception:
        return fallback
