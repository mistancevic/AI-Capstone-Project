"""PlateMate eval harness — runs the seven Design cases (DESIGN.md §10)
against the built prototype and asserts each case's expected behavior.

Per-case assertions cover: exact budget math (deterministic → exact, not
fuzzy), card structure, counter transitions, flag tier + quiet-hours
delivery times, banned-language absence in every client-visible output,
and — for the boundary case — that no restriction output exists.

Run:  python -m eval.run_eval          (model-off: deterministic floor)
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from platemate import cards, policy                        # noqa: E402
from platemate.agents.orchestrator import Orchestrator     # noqa: E402
from platemate.escalation import Clock, load_agreement     # noqa: E402
from platemate.food_db import load_foods                   # noqa: E402
from platemate.models import ClientProfile, Route, situation_from_dict  # noqa: E402
from platemate.plan_parser import parse_plan               # noqa: E402

DATA = ROOT / "data"


def load_personas() -> dict:
    return json.loads((DATA / "personas.json").read_text(encoding="utf-8"))


def build(persona_key: str, clock: Clock) -> Orchestrator:
    personas = load_personas()
    p = personas[persona_key]
    plan = parse_plan((ROOT / p["plan_file"]).read_text(encoding="utf-8"), source=p["plan_file"])
    profile = ClientProfile(
        name=p["name"], goal=p["goal"], restrictions=p["restrictions"],
        dislikes=p["dislikes"], likes=p["likes"],
        training_tomorrow=p["training_tomorrow"], usual_bedtime=p["usual_bedtime"])
    return Orchestrator(plan, profile, load_foods(DATA / "foods.json"),
                        agreement=load_agreement(persona_key), clock=clock,
                        use_llm=False)


def check(cond: bool, label: str, failures: list[str], case_id: str):
    status = "PASS" if cond else "FAIL"
    print(f"    [{status}] {label}")
    if not cond:
        failures.append(f"{case_id}: {label}")


def run() -> int:
    scenarios = json.loads((DATA / "scenarios.json").read_text(encoding="utf-8"))
    seeds = json.loads((DATA / "state_seed.json").read_text(encoding="utf-8"))
    banned_phrases, _ = policy.banned_language()
    failures: list[str] = []

    for sc in scenarios:
        case_key = sc["id"].split("_")[0]
        seed = seeds[case_key]
        clock = Clock(seed["clock"])
        orch = build(sc["persona"], clock)
        exp = sc["expected"]

        print(f"\n=== {sc['id']} ({sc['persona']} @ {seed['clock']}) ===")

        kwargs = dict(skipped_days=seed["skipped_days"],
                      compensatory_asks_week=seed["compensatory_asks_week"])
        if sc.get("situation"):
            sit = situation_from_dict({**sc["situation"], "raw_text": sc["text"]})
            result = orch.handle_text(sc["text"], situation=sit, **kwargs)
        elif sc.get("situation_overrides"):
            result = orch.handle_text(sc["text"], **kwargs, **sc["situation_overrides"])
        else:
            result = orch.handle_text(sc["text"], **kwargs)

        rendered = cards.render(result)

        # Universal: no banned phrase in any client-visible output.
        lowered = rendered.lower()
        check(not any(b in lowered for b in banned_phrases),
              "no banned language in client-visible output", failures, sc["id"])

        kind = exp["kind"]
        if kind == "options_card":
            rec = result.recommendation
            check(rec is not None, "options card produced", failures, sc["id"])
            if rec is None:
                continue
            if "remaining_kcal" in exp:
                check(rec.math.remaining_kcal == exp["remaining_kcal"],
                      f"exact math: remaining {rec.math.remaining_kcal} kcal == {exp['remaining_kcal']}",
                      failures, sc["id"])
                check(rec.math.remaining_protein_g == exp["remaining_protein_g"],
                      f"exact math: remaining {rec.math.remaining_protein_g} g == {exp['remaining_protein_g']}",
                      failures, sc["id"])
            check(len(rec.options) >= exp.get("min_options", 1),
                  f">= {exp.get('min_options', 1)} option(s) ({len(rec.options)} returned)",
                  failures, sc["id"])
            if exp.get("bridge_required"):
                check(rec.bridge is not None, "bridge present (never-skip)", failures, sc["id"])
            if "within_tolerance" in exp:
                check(rec.within_tolerance == exp["within_tolerance"],
                      f"within_tolerance == {exp['within_tolerance']}", failures, sc["id"])
            if exp.get("strategy_required"):
                check(bool(rec.strategy_note), "averaging strategy present", failures, sc["id"])
            if exp.get("nudge_required"):
                check(rec.coaching_line == policy.block("nudge_compensatory"),
                      "templated de-escalating nudge in coaching-line slot", failures, sc["id"])
            if "counter_after" in exp:
                check(result.counters.get("compensatory_asks_week") == exp["counter_after"],
                      f"compensatory counter == {exp['counter_after']}", failures, sc["id"])
            if exp.get("flag") is None or exp.get("flag") == "digest_at_most":
                check(result.flag is None or result.flag.tier.value == "digest",
                      "no urgent/normal flag fired (digest at most)", failures, sc["id"])

        elif kind == "capture_question":
            check(result.route is Route.CLARIFY, "route == CLARIFY (ask, never guess)",
                  failures, sc["id"])
            check(result.recommendation is None, "no card produced", failures, sc["id"])
            check(result.flag is None, "no flag fired", failures, sc["id"])
            check("targets" in result.question.lower(), "asks for the plan targets",
                  failures, sc["id"])

        elif kind == "clarify":
            check(result.route is Route.CLARIFY, "route == CLARIFY", failures, sc["id"])
            check(result.recommendation is None, "no guessed card", failures, sc["id"])
            check(bool(result.question), "one clarifying question", failures, sc["id"])
            if exp.get("presets_required"):
                check(len(result.presets) >= 3, "preset picker offered", failures, sc["id"])
            check(result.flag is None, "no flag fired", failures, sc["id"])

        elif kind == "hard_stop":
            check(result.route is Route.ESCALATE, "route == ESCALATE (hard stop)",
                  failures, sc["id"])
            check(result.recommendation is None, "no nutrition math ran (no card)",
                  failures, sc["id"])
            esc = result.escalation
            check(esc is not None and esc.tier == "urgent", "tier == urgent", failures, sc["id"])
            if esc is None:
                continue
            if exp.get("safe_default_required"):
                check(policy.block("stop_safe_default") in esc.message,
                      "safe default present", failures, sc["id"])
            if exp.get("averaging_required"):
                check(policy.block("stop_averaging") in esc.message,
                      "averaging explainer present", failures, sc["id"])
            check(esc.get_help_now == exp["get_help_now"],
                  f"GET HELP NOW == {exp['get_help_now']}", failures, sc["id"])
            if "min_reasons" in exp:
                check(len(esc.reasons) >= exp["min_reasons"],
                      f">= {exp['min_reasons']} reason codes ({len(esc.reasons)}: {esc.reasons})",
                      failures, sc["id"])
            flag = result.flag
            check(flag is not None and flag.tier.value == "urgent",
                  "urgent coach flag fired", failures, sc["id"])
            if flag:
                if "flag_queued_at" in exp:
                    check(flag.queued_at == exp["flag_queued_at"],
                          f"flag queued at {flag.queued_at}", failures, sc["id"])
                if "flag_delivered_at" in exp:
                    check(flag.delivered_at == exp["flag_delivered_at"],
                          f"flag delivered at {flag.delivered_at} == {exp['flag_delivered_at']}",
                          failures, sc["id"])
                check(all(isinstance(v, int) for v in flag.counter_history.values()),
                      "counter history is counts, never texts", failures, sc["id"])
            if "counter_after" in exp:
                check(result.counters.get("compensatory_asks_week") == exp["counter_after"],
                      f"compensatory counter == {exp['counter_after']}", failures, sc["id"])
            if sc["design_case"] == 7:
                check("800" not in esc.message,
                      "no 800-kcal plan exists in the client-facing stop message",
                      failures, sc["id"])

    print("\n" + "=" * 60)
    total = len(scenarios)
    failed_cases = {f.split(":")[0] for f in failures}
    print(f"Cases: {total} | passed: {total - len(failed_cases)} | failed: {len(failed_cases)}")
    if failures:
        print("\nFailed assertions:")
        for f in failures:
            print(f"  - {f}")
    from platemate.screens import screen_failures
    print(f"Banned-language screen replacements this run: {screen_failures()}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(run())
