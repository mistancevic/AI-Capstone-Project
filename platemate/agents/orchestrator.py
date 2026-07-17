"""First-step orchestrator — the Design §2 target workflow.

Fixed-order triage on every request (DESIGN.md §3 Decide):

  1. SAFETY SCREEN first, on the raw text + seeded counters — before any
     parsing, routing, or model call. A stop here means no nutrition math
     happens at all (Case 7 is the proof).
  2. Scope / targets check — a plan without targets asks, never guesses.
  3. Missing-data check — an unparseable message gets one clarifying
     question, then the structured preset picker (deterministic
     low-confidence rule: required slots, never model self-confidence).
  4. Classify into one of the five named triggers and route to the
     nutrition agent.

Per Moe's directive there are no stubbed agents in the demo path; the
sleep consult remains a conditional one-line note.
"""

from __future__ import annotations

import re

from .. import llm, policy, safety, screens
from ..escalation import Clock, CoachAgreement, CoachQueue, Tier
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

_TRIGGER_KEYWORDS = {
    Trigger.MUST_SKIP: ["have to skip", "must skip", "can't have", "cant have", "no time to eat", "will miss"],
    Trigger.SURPRISE_MEAL: ["dinner tonight", "dinner with", "team dinner", "eating out", "restaurant tonight", "big meal", "banquet"],
    Trigger.OFF_PLAN_EXTRA: ["i ate", "i had", "off-plan", "off plan", "snacked", "grabbed a", "couldn't resist", "happened", "got away from me", "turned into"],
    Trigger.MORNING_CHECK: ["today looks", "chaotic day ahead", "rebuild my day", "plan my day"],
    Trigger.ON_THE_SPOT_SWAP: ["isn't available", "not available", "swap", "replacement", "ran out"],
}

# The guaranteed-parseable fallback (Case 4): tap → prefilled structured stub.
SCENARIO_PRESETS = [
    "Something off-plan happened (I ate something extra)",
    "A big meal is coming up that isn't in the plan",
    "I have to skip a planned meal",
    "Rebuild my day from this morning",
    "My planned meal isn't available — swap it",
]


def classify_trigger(text: str) -> Trigger:
    lowered = text.lower()
    for trigger, keys in _TRIGGER_KEYWORDS.items():
        if any(k in lowered for k in keys):
            return trigger
    return Trigger.UNKNOWN


class Orchestrator:
    def __init__(self, plan: Plan, profile: ClientProfile, foods: list[FoodItem],
                 agreement: CoachAgreement | None = None,
                 clock: Clock | None = None,
                 use_llm: bool | None = None):
        self.plan = plan
        self.profile = profile
        self.foods = foods
        self.agreement = agreement or CoachAgreement()
        self.clock = clock or Clock("12:00")
        self.queue = CoachQueue(agreement=self.agreement)
        self.use_llm = llm.available() if use_llm is None else use_llm
        self.registry = {"nutrition": nutrition, "sleep_recovery": sleep_recovery}

    # ------------------------------------------------------------------ #

    def handle_text(self, text: str, skipped_days: int = 0,
                    compensatory_asks_week: int = 0,
                    situation: Situation | None = None,
                    **situation_overrides) -> AgentResult:
        """Entry point for a client message. Safety screen runs on the RAW
        text before anything else — including before the parse call."""
        target_kcal = self.plan.targets.calories_kcal if self.plan.targets else None
        verdict = safety.screen(text, skipped_days=skipped_days,
                                compensatory_asks_week=compensatory_asks_week,
                                target_kcal=target_kcal)

        if verdict.action == "stop":
            return self._hard_stop(verdict, text)

        if verdict.action == "decline_oos":
            flag = self.queue.submit(Tier.DIGEST, verdict.reasons, verdict.counters, self.clock)
            return AgentResult(
                route=Route.OUT_OF_SCOPE,
                escalation=Escalation(reasons=verdict.reasons,
                                      message=policy.block("decline_out_of_scope"),
                                      tier=Tier.DIGEST.value),
                flag=flag, counters=verdict.counters)

        # 2. Targets check — ask, never guess (Case 2).
        if self.plan.needs_target_capture:
            return AgentResult(route=Route.CLARIFY,
                               question=policy.block("capture_targets"),
                               counters=verdict.counters)

        # 3. Situation: structured input wins; else parse (LLM when on,
        #    keyword rules when off); required-slot check gates the card.
        if situation is None:
            parsed = llm.parse_situation(text) if self.use_llm else None
            situation = parsed or Situation(raw_text=text, trigger=classify_trigger(text))
            minutes = re.search(r"(\d+)\s*min", text.lower())
            if minutes:
                situation.minutes_available = int(minutes.group(1))
        for key, value in situation_overrides.items():
            setattr(situation, key, value)

        if situation.trigger == Trigger.UNKNOWN and not (
            situation.eaten_off_plan or situation.upcoming_fixed or situation.skipped_meals
        ):
            # Deterministic low-confidence rule: required slots missing →
            # one clarifying question + the preset picker. No guessed card.
            return AgentResult(route=Route.CLARIFY,
                               question=policy.block("clarify_question"),
                               presets=list(SCENARIO_PRESETS),
                               counters=verdict.counters)

        # 4. Route to the nutrition agent.
        rec = nutrition.recommend(self.plan, self.profile, situation, self.foods)
        consulted = ["nutrition"]
        route = Route.NUTRITION
        if sleep_recovery.should_consult(situation):
            rec.sleep_note = sleep_recovery.advise(situation, self.profile)
            consulted.append("sleep_recovery")
            route = Route.NUTRITION_WITH_SLEEP

        # Coaching line: nudge template on a compensatory 1st/2nd ask;
        # otherwise LLM line (screened) or the deterministic fallback.
        replaced = False
        if verdict.action == "nudge":
            rec.coaching_line = policy.block("nudge_compensatory")
        else:
            raw_line = (llm.coaching_line(rec, self.profile.name)
                        if self.use_llm else policy.banned_language()[1])
            rec.coaching_line, replaced = screens.screen_coaching_line(raw_line)

        flag = None
        if verdict.tier is Tier.DIGEST and verdict.reasons:
            flag = self.queue.submit(Tier.DIGEST, verdict.reasons, verdict.counters, self.clock)

        return AgentResult(route=route, trigger=situation.trigger,
                           recommendation=rec, consulted_agents=consulted,
                           flag=flag, counters=verdict.counters,
                           coaching_line_replaced=replaced)

    def handle(self, situation: Situation, skipped_days: int = 0,
               compensatory_asks_week: int = 0) -> AgentResult:
        """Entry point for an already-structured situation (demo & tests)."""
        return self.handle_text(situation.raw_text or "", skipped_days=skipped_days,
                                compensatory_asks_week=compensatory_asks_week,
                                situation=situation)

    # ------------------------------------------------------------------ #

    def _hard_stop(self, verdict: safety.SafetyVerdict, text: str) -> AgentResult:
        """The stop path: templated message, safe default, flag with
        quiet-hours delivery. No nutrition math has run."""
        flag = self.queue.submit(Tier.URGENT, verdict.reasons, verdict.counters,
                                 self.clock, share_trigger=True)
        delivery = (f"delivery {flag.delivered_at}" if flag.delivered_at != self.clock.now
                    else "delivered immediately")
        parts = [policy.block("stop_why"), "", policy.block("stop_safe_default"),
                 "", policy.block("stop_averaging")]
        if any("restriction demand" in r for r in verdict.reasons):
            parts += ["", policy.block("refusal_floor")]
        if verdict.get_help_now:
            parts += ["", policy.block("get_help_now")]
        parts += ["", policy.block("stop_flag_notice", delivery=delivery)]

        return AgentResult(
            route=Route.ESCALATE,
            escalation=Escalation(reasons=verdict.reasons, message="\n".join(parts),
                                  tier=Tier.URGENT.value,
                                  get_help_now=verdict.get_help_now),
            flag=flag, counters=verdict.counters)
