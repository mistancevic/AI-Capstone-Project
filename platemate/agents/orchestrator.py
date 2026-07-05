"""First-step orchestrator.

Order of operations on every request:

  1. Safety screen (rule-based, always first, never delegated to a model).
  2. Read the situation — either a structured Situation is supplied, or the
     free text is parsed (Claude when available, keyword rules otherwise).
  3. Route: nutrition agent computes budget + ranked options; the sleep &
     recovery agent is consulted when the decision touches sleep or
     tomorrow's training; anything else escalates to the coach.
"""

from __future__ import annotations

import re

from .. import llm, safety
from ..models import (
    AgentResult,
    ClientProfile,
    Escalation,
    FoodItem,
    Plan,
    Route,
    Situation,
    Trigger,
)
from . import nutrition, sleep_recovery
from .stubs import STUB_AGENTS

_TRIGGER_KEYWORDS = {
    Trigger.MUST_SKIP: ["have to skip", "must skip", "can't have", "cant have", "no time to eat", "will miss"],
    Trigger.SURPRISE_MEAL: ["dinner with", "team dinner", "eating out", "restaurant tonight", "big meal", "banquet"],
    Trigger.OFF_PLAN_EXTRA: ["i ate", "i had", "off-plan", "off plan", "snacked", "grabbed a", "couldn't resist"],
    Trigger.MORNING_CHECK: ["today looks", "chaotic day ahead", "rebuild my day", "plan my day"],
    Trigger.ON_THE_SPOT_SWAP: ["isn't available", "not available", "swap", "replacement", "out of", "ran out"],
}


def classify_trigger(text: str) -> Trigger:
    lowered = text.lower()
    for trigger, keys in _TRIGGER_KEYWORDS.items():
        if any(k in lowered for k in keys):
            return trigger
    return Trigger.UNKNOWN


class Orchestrator:
    def __init__(self, plan: Plan, profile: ClientProfile, foods: list[FoodItem], use_llm: bool | None = None):
        self.plan = plan
        self.profile = profile
        self.foods = foods
        self.use_llm = llm.available() if use_llm is None else use_llm
        self.registry = {
            "nutrition": nutrition,
            "sleep_recovery": sleep_recovery,
            **{a.name: a for a in STUB_AGENTS},
        }

    # ------------------------------------------------------------------ #

    def handle_text(self, text: str, skipped_days: int = 0, **situation_overrides) -> AgentResult:
        """Entry point for a free-text client message."""
        escalation = safety.screen(text, skipped_days=skipped_days)
        if escalation:
            return AgentResult(route=Route.ESCALATE, escalation=escalation)

        situation = None
        if self.use_llm:
            situation = llm.parse_situation(text)
        if situation is None:
            situation = Situation(raw_text=text, trigger=classify_trigger(text))
            minutes = re.search(r"(\d+)\s*min", text.lower())
            if minutes:
                situation.minutes_available = int(minutes.group(1))
        for key, value in situation_overrides.items():
            setattr(situation, key, value)
        return self.handle(situation, skipped_days=skipped_days)

    def handle(self, situation: Situation, skipped_days: int = 0) -> AgentResult:
        """Entry point for an already-structured situation (demo & eval)."""
        escalation = safety.screen_situation(situation, skipped_days=skipped_days)
        if escalation:
            return AgentResult(route=Route.ESCALATE, trigger=situation.trigger, escalation=escalation)

        if self.plan.needs_target_capture:
            return AgentResult(
                route=Route.ESCALATE,
                trigger=situation.trigger,
                escalation=Escalation(
                    reasons=["plan has no daily targets yet"],
                    message=(
                        "Your uploaded plan doesn't state daily calorie and protein "
                        "targets. Tell me the targets (or ask your coach) and I'll "
                        "take it from there — I won't guess numbers for you."
                    ),
                ),
            )

        if situation.trigger == Trigger.UNKNOWN and not (
            situation.eaten_off_plan or situation.upcoming_fixed or situation.skipped_meals
        ):
            return AgentResult(
                route=Route.OUT_OF_SCOPE,
                trigger=situation.trigger,
                escalation=Escalation(
                    reasons=["request not recognized as a nutrition-adaptation task"],
                    message=(
                        "I can help rework today's meals when the plan gets disrupted. "
                        "For anything else, your coach is the right person."
                    ),
                ),
            )

        consulted = ["nutrition"]
        rec = nutrition.recommend(self.plan, self.profile, situation, self.foods)

        route = Route.NUTRITION
        if sleep_recovery.should_consult(situation):
            rec.sleep_note = sleep_recovery.advise(situation, self.profile)
            consulted.append("sleep_recovery")
            route = Route.NUTRITION_WITH_SLEEP

        rec.coaching_line = (
            llm.coaching_line(rec, self.profile.name)
            if self.use_llm
            else "One imperfect day doesn't break a plan — hit your protein, enjoy "
                 "the meal, and we rebalance across the week."
        )

        return AgentResult(route=route, trigger=situation.trigger,
                           recommendation=rec, consulted_agents=consulted)
