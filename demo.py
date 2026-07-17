"""PlateMate demo — one continuous run, exactly as described in the PRD.

  1. Upload the coach's plan; the app parses targets + baseline meals and
     echoes back what it understood for confirmation.
  2. Disrupted-day request: "I ate an ice cream and have a ~1000 kcal
     colleague dinner tonight — what should lunch be?" The orchestrator
     routes it, the nutrition agent shows the math and 2-3 ranked options
     plus a bridge fallback, the sleep & recovery agent weighs in on the
     late dinner, and a coaching line closes it out.
  3. The onboarding-capture path: Maja's plan omits targets, so the app
     asks for them before adapting anything.
  4. A seeded safety case (dizzy + three days of skipped meals) shows the
     app refuse and escalate to the coach.
  5. Fitness, movement, and recovery appear as registered but stubbed agents.

Runs fully offline; set ANTHROPIC_API_KEY to see Claude-generated coaching
lines and free-text situation parsing instead of the rule-based fallbacks.

Usage:  python demo.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from platemate import llm
from platemate.agents import Orchestrator
from platemate.agents.nutrition import format_recommendation
from platemate.food_db import load_foods
from platemate.models import ClientProfile, Situation, Trigger
from platemate.plan_parser import capture_targets, parse_plan_file, plan_summary


def banner(title: str) -> None:
    print("\n" + "=" * 74)
    print(title)
    print("=" * 74)


def main() -> None:
    personas = json.loads((ROOT / "data" / "personas.json").read_text(encoding="utf-8"))
    foods = load_foods()

    print("PlateMate: macros made simple — demo run")
    print(f"AI coaching layer: {'Claude (' + llm.MODEL + ')' if llm.available() else 'offline rule-based fallback'}")

    # ------------------------------------------------------------------ #
    banner("STEP 1 — Upload the coach's plan (Alex)")
    alex_raw = personas["alex"]
    alex = ClientProfile(
        name=alex_raw["name"], goal=alex_raw["goal"], restrictions=alex_raw["restrictions"],
        dislikes=alex_raw["dislikes"], likes=alex_raw["likes"],
        training_tomorrow=alex_raw["training_tomorrow"], usual_bedtime=alex_raw["usual_bedtime"],
    )
    alex_plan = parse_plan_file(ROOT / alex_raw["plan_file"])
    print(plan_summary(alex_plan))
    print(f"Preferences noted: likes {', '.join(alex.likes)}; dislikes {', '.join(alex.dislikes) or 'none'}.")
    print("Client confirms: looks right. ✔")

    # ------------------------------------------------------------------ #
    banner("STEP 2 — Disrupted-day request")
    message = ("I ate an ice cream this morning and I have a colleague dinner "
               "tonight, probably around 1000 kcal. What should I do for lunch?")
    print(f'Alex: "{message}"\n')

    orch = Orchestrator(alex_plan, alex, foods)
    situation = Situation(
        raw_text=message,
        trigger=Trigger.SURPRISE_MEAL,
        eaten_off_plan=[("ice cream", 300, 5)],
        completed_meals=["breakfast"],
        upcoming_fixed=[("colleague dinner", 1000, 60)],
        skipped_meals=["dinner"],  # planned dinner is displaced by the colleague dinner
        meal_to_solve="lunch",
        available=["home", "shop"],
        minutes_available=30,
    )
    result = orch.handle(situation)
    print(f"Orchestrator: safety screen clear -> trigger '{result.trigger.value}' "
          f"-> route '{result.route.value}' (consulted: {', '.join(result.consulted_agents)})\n")
    print(format_recommendation(result.recommendation))

    # ------------------------------------------------------------------ #
    banner("STEP 3 — Onboarding capture (Maja's plan omits targets)")
    maja_raw = personas["maja"]
    maja = ClientProfile(
        name=maja_raw["name"], goal=maja_raw["goal"], restrictions=maja_raw["restrictions"],
        dislikes=maja_raw["dislikes"], likes=maja_raw["likes"],
        training_tomorrow=maja_raw["training_tomorrow"], usual_bedtime=maja_raw["usual_bedtime"],
    )
    maja_plan = parse_plan_file(ROOT / maja_raw["plan_file"])
    print(plan_summary(maja_plan))

    maja_orch = Orchestrator(maja_plan, maja, foods)
    probe = maja_orch.handle(Situation(raw_text="what should I eat for lunch?",
                                       trigger=Trigger.ON_THE_SPOT_SWAP))
    print(f"\nPlateMate: {probe.question or probe.escalation.message}")
    print('\nMaja: "Coach says 1800 kcal and 120 g protein."')
    capture_targets(maja_plan, 1800, 120)
    print(f"PlateMate: got it — daily targets set to {maja_plan.targets}. ✔")

    # ------------------------------------------------------------------ #
    banner("STEP 4 — Seeded safety case: refuse and escalate")
    safety_msg = ("I've been feeling dizzy today and honestly I've barely eaten "
                  "anything for three days. What should I eat?")
    print(f'Maja: "{safety_msg}"\n')
    safety_result = maja_orch.handle_text(safety_msg, skipped_days=3)
    print(f"Orchestrator: route '{safety_result.route.value}'")
    print("Signals detected:")
    for reason in safety_result.escalation.reasons:
        print(f"  - {reason}")
    print(f"\nPlateMate: {safety_result.escalation.message}")

    # ------------------------------------------------------------------ #
    banner("STEP 5 — Future agents (parked, per the no-stubs directive)")
    print("  Parked initiatives (see notes/parked-ideas.md): sleep & recovery "
          "as a full agent,\n  fitness/movement/recovery agents, initial plan "
          "crafting — each returns only\n  when its domain has a real data "
          "source and a consuming decision.")
    print("\nDemo complete.")


if __name__ == "__main__":
    main()
