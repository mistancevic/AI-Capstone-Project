"""Interactive PlateMate CLI.

Usage:  python -m platemate.cli [--persona alex|maja]

Type a disrupted-day message and PlateMate routes it: the safety screen runs
first, then the nutrition agent answers with the math and ranked options.
With ANTHROPIC_API_KEY set, free text is parsed by Claude; otherwise a
keyword classifier is used (structured details like exact calories eaten are
then best supplied via the demo/eval paths).
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from . import llm
from .agents import Orchestrator
from .agents.nutrition import format_recommendation
from .food_db import load_foods
from .models import ClientProfile, Route
from .plan_parser import capture_targets, parse_plan_file, plan_summary

ROOT = Path(__file__).resolve().parent.parent


def main() -> None:
    parser = argparse.ArgumentParser(description="PlateMate interactive CLI")
    parser.add_argument("--persona", choices=["alex", "maja"], default="alex")
    args = parser.parse_args()

    personas = json.loads((ROOT / "data" / "personas.json").read_text(encoding="utf-8"))
    p = personas[args.persona]
    profile = ClientProfile(
        name=p["name"], goal=p["goal"], restrictions=p["restrictions"],
        dislikes=p["dislikes"], likes=p["likes"],
        training_tomorrow=p["training_tomorrow"], usual_bedtime=p["usual_bedtime"],
    )
    plan = parse_plan_file(ROOT / p["plan_file"])

    print(f"PlateMate — persona: {profile.name}")
    print(f"AI layer: {'Claude (' + llm.MODEL + ')' if llm.available() else 'rule-based fallback (set ANTHROPIC_API_KEY for LLM parsing)'}")
    print(plan_summary(plan))

    if plan.needs_target_capture:
        print("\nThis plan doesn't state daily targets — I need them before adapting anything.")
        kcal = int(input("Daily calories (kcal): ").strip())
        prot = int(input("Daily protein (g): ").strip())
        capture_targets(plan, kcal, prot)
        print(f"Targets set: {plan.targets}")

    orch = Orchestrator(plan, profile, load_foods())
    print("\nTell me what happened to your day (or 'quit'):")

    while True:
        try:
            text = input(f"\n{profile.name}> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not text or text.lower() in {"quit", "exit", "q"}:
            break

        result = orch.handle_text(text)
        if result.route == Route.ESCALATE:
            print("\n[escalated to coach]")
            for reason in result.escalation.reasons:
                print(f"  - {reason}")
            print(f"\n{result.escalation.message}")
        elif result.route == Route.OUT_OF_SCOPE:
            print(f"\n{result.escalation.message}")
        else:
            print(f"\n[route: {result.route.value}; trigger: {result.trigger.value}]\n")
            print(format_recommendation(result.recommendation))

    print("\nBye — protein first, calories second.")


if __name__ == "__main__":
    main()
