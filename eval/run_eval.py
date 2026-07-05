"""Evaluation harness for PlateMate.

Runs the synthetic scenario set through the orchestrator and reports the
PRD's three metrics:

  - no-skip rate ......... % of disrupted-day scenarios where the app returns
                           at least one plan-compliant option (or bridge), so
                           the meal gets eaten instead of skipped
  - macro accuracy ....... mean absolute gap between the recommended day
                           total and the target (kcal and protein g)
  - escalation precision . of the requests the app escalated, how many were
                           truly escalation-worthy (recall reported too)

Usage:  python -m eval.run_eval  [--scenarios data/scenarios.json]

Runs fully offline (deterministic rule path, no LLM calls).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from platemate.agents import Orchestrator                     # noqa: E402
from platemate.food_db import load_foods                      # noqa: E402
from platemate.models import ClientProfile, Route, situation_from_dict  # noqa: E402
from platemate.plan_parser import capture_targets, parse_plan_file      # noqa: E402

# Onboarding-captured targets for the plan variant that omits them (Maja).
CAPTURED_TARGETS = {"maja": (1800, 120)}


def load_personas() -> dict:
    return json.loads((ROOT / "data" / "personas.json").read_text(encoding="utf-8"))


def build_orchestrator(persona_key: str, personas: dict, foods) -> Orchestrator:
    p = personas[persona_key]
    profile = ClientProfile(
        name=p["name"],
        goal=p["goal"],
        restrictions=p["restrictions"],
        dislikes=p["dislikes"],
        likes=p["likes"],
        training_tomorrow=p["training_tomorrow"],
        usual_bedtime=p["usual_bedtime"],
    )
    plan = parse_plan_file(ROOT / p["plan_file"])
    if plan.needs_target_capture:
        kcal, prot = CAPTURED_TARGETS[persona_key]
        capture_targets(plan, kcal, prot)
    return Orchestrator(plan, profile, foods, use_llm=False)


def run(scenarios_path: Path) -> int:
    scenarios = json.loads(scenarios_path.read_text(encoding="utf-8"))
    personas = load_personas()
    foods = load_foods()

    rows = []
    nutrition_total = nutrition_served = 0
    kcal_gaps: list[int] = []
    prot_gaps: list[int] = []
    tp = fp = fn = tn = 0
    route_correct = 0
    failures: list[str] = []

    for sc in scenarios:
        orch = build_orchestrator(sc["persona"], personas, foods)
        skipped_days = sc.get("skipped_days", 0)

        if sc.get("situation"):
            result = orch.handle(situation_from_dict(sc["situation"]), skipped_days=skipped_days)
        else:
            result = orch.handle_text(sc["message"], skipped_days=skipped_days)

        exp = sc["expected"]
        escalated = result.route == Route.ESCALATE
        expected_escalate = exp.get("escalate", False)

        if escalated and expected_escalate:
            tp += 1
        elif escalated and not expected_escalate:
            fp += 1
        elif not escalated and expected_escalate:
            fn += 1
        else:
            tn += 1

        ok = result.route.value == exp["route"]

        if not expected_escalate:
            nutrition_total += 1
            rec = result.recommendation
            served = bool(rec and (rec.options or rec.bridge))
            if served:
                nutrition_served += 1
                best = rec.options[0] if rec.options else rec.bridge
                kcal_gaps.append(abs(best.day_end_kcal_gap))
                prot_gaps.append(abs(best.day_end_protein_gap))
            ok = ok and served
            if "min_options" in exp:
                ok = ok and rec is not None and len(rec.options) >= exp["min_options"]
            if "within_tolerance" in exp:
                ok = ok and rec is not None and rec.within_tolerance == exp["within_tolerance"]
            if exp.get("expect_strategy_note"):
                ok = ok and rec is not None and bool(rec.strategy_note)

        if ok:
            route_correct += 1
        else:
            failures.append(f"{sc['id']}: got route={result.route.value}, expected={exp['route']}")
        rows.append((sc["id"], result.route.value, "PASS" if ok else "FAIL"))

    # ---- report ------------------------------------------------------- #
    print("=" * 74)
    print("PlateMate evaluation")
    print("=" * 74)
    for sid, route, status in rows:
        print(f"  [{status}] {sid:<42} -> {route}")
    print("-" * 74)

    no_skip = 100.0 * nutrition_served / nutrition_total if nutrition_total else 0.0
    precision = 100.0 * tp / (tp + fp) if (tp + fp) else 100.0
    recall = 100.0 * tp / (tp + fn) if (tp + fn) else 100.0
    avg_kcal = sum(kcal_gaps) / len(kcal_gaps) if kcal_gaps else 0.0
    avg_prot = sum(prot_gaps) / len(prot_gaps) if prot_gaps else 0.0

    print(f"  No-skip rate:          {no_skip:5.1f}%  ({nutrition_served}/{nutrition_total} disrupted days got an eatable option)")
    print(f"  Macro accuracy:        avg |day-end gap| = {avg_kcal:.0f} kcal / {avg_prot:.1f} g protein")
    print(f"  Escalation precision:  {precision:5.1f}%   (recall {recall:.1f}%)")
    print(f"  Scenario checks:       {route_correct}/{len(scenarios)} passed")
    if failures:
        print("  Failures:")
        for f in failures:
            print(f"    - {f}")
    print("=" * 74)
    return 0 if not failures else 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scenarios", default=ROOT / "data" / "scenarios.json", type=Path)
    sys.exit(run(parser.parse_args().scenarios))
