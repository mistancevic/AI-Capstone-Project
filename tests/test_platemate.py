"""Unit tests for PlateMate's deterministic core."""

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from platemate import safety
from platemate.agents import Orchestrator
from platemate.agents import nutrition, sleep_recovery
from platemate.agents.orchestrator import classify_trigger
from platemate.food_db import filter_foods, load_foods
from platemate.models import (
    CALORIE_TOLERANCE_KCAL,
    PROTEIN_TOLERANCE_G,
    ClientProfile,
    Route,
    Situation,
    Trigger,
)
from platemate.plan_parser import capture_targets, parse_plan, parse_plan_file


ALEX_PLAN = ROOT / "data" / "plans" / "plan_alex.md"
MAJA_PLAN = ROOT / "data" / "plans" / "plan_maja.md"


@pytest.fixture()
def foods():
    return load_foods()


@pytest.fixture()
def alex():
    return ClientProfile(name="Alex", likes=["chicken"], dislikes=["lentil"],
                         training_tomorrow=True)


@pytest.fixture()
def alex_plan():
    return parse_plan_file(ALEX_PLAN)


# ---------------------------------------------------------------- parser --

def test_parse_plan_with_targets(alex_plan):
    assert alex_plan.targets is not None
    assert alex_plan.targets.calories_kcal == 2400
    assert alex_plan.targets.protein_g == 160
    assert len(alex_plan.meals) == 4
    assert alex_plan.meals[0].time_hint == "breakfast"


def test_parse_plan_without_targets_needs_capture():
    plan = parse_plan_file(MAJA_PLAN)
    assert plan.needs_target_capture
    capture_targets(plan, 1800, 120)
    assert not plan.needs_target_capture
    assert plan.targets.protein_g == 120


def test_capture_rejects_nonsense():
    plan = parse_plan("Client: X")
    with pytest.raises(ValueError):
        capture_targets(plan, 0, -5)


def test_parse_table_style_meals():
    plan = parse_plan(
        "Client: T\nDaily calories: 2000 kcal\nDaily protein: 150 g\n"
        "| Meal | Food | kcal | protein |\n"
        "| --- | --- | --- | --- |\n"
        "| Lunch | chicken and rice | 600 | 45 |\n"
    )
    assert len(plan.meals) == 1
    assert plan.meals[0].calories_kcal == 600


# ------------------------------------------------------------ budget math --

def test_budget_math_reserves_remaining_planned_meals(alex_plan):
    situation = Situation(completed_meals=["breakfast"], meal_to_solve="lunch")
    math = nutrition.compute_budget(alex_plan, situation)
    # consumed: breakfast 450/35; reserved: snack 350/30 + dinner 750/45
    assert math.consumed_kcal == 450
    assert math.reserved_kcal == 1100
    assert math.remaining_kcal == 2400 - 450 - 1100
    assert math.remaining_protein_g == 160 - 35 - 75


def test_budget_math_skipped_meal_not_reserved(alex_plan):
    situation = Situation(completed_meals=["breakfast"], meal_to_solve="lunch",
                          skipped_meals=["dinner"],
                          upcoming_fixed=[("team dinner", 1000, 60)])
    math = nutrition.compute_budget(alex_plan, situation)
    assert math.reserved_kcal == 350 + 1000  # snack + team dinner, planned dinner displaced
    assert math.remaining_kcal == 2400 - 450 - 1350


# --------------------------------------------------------------- filtering --

def test_filter_respects_restrictions_and_time(foods):
    maja = ClientProfile(name="Maja", restrictions=["lactose"], dislikes=["jerky"])
    picked = filter_foods(foods, maja, available=["home", "shop"], minutes_available=5,
                          meal_type="lunch")
    assert picked, "there must always be something quick to eat"
    for food in picked:
        assert "lactose" not in food.tags
        assert "jerky" not in food.name.lower()
        assert food.prep_minutes <= 5


# ------------------------------------------------------------ recommending --

def test_recommend_never_returns_empty(alex_plan, alex, foods):
    situation = Situation(completed_meals=["breakfast"], meal_to_solve="lunch",
                          minutes_available=5)
    rec = nutrition.recommend(alex_plan, alex, situation, foods)
    assert rec.options or rec.bridge, "skipping must never be the default"
    assert rec.bridge is not None and rec.bridge.food.is_bridge


def test_recommend_within_tolerance_flag(alex_plan, alex, foods):
    situation = Situation(
        trigger=Trigger.SURPRISE_MEAL,
        eaten_off_plan=[("ice cream", 300, 5)],
        completed_meals=["breakfast"],
        upcoming_fixed=[("colleague dinner", 1000, 60)],
        skipped_meals=["dinner"],
        meal_to_solve="lunch",
    )
    rec = nutrition.recommend(alex_plan, alex, situation, foods)
    assert rec.within_tolerance
    best = rec.options[0]
    assert abs(best.day_end_kcal_gap) <= CALORIE_TOLERANCE_KCAL
    assert abs(best.day_end_protein_gap) <= PROTEIN_TOLERANCE_G
    assert rec.strategy_note == ""


def test_recommend_out_of_tolerance_triggers_strategy(alex_plan, alex, foods):
    situation = Situation(
        trigger=Trigger.OFF_PLAN_EXTRA,
        eaten_off_plan=[("whole pizza", 850, 30)],
        completed_meals=["breakfast", "lunch", "snack"],
        meal_to_solve="dinner",
        minutes_available=20,
    )
    rec = nutrition.recommend(alex_plan, alex, situation, foods)
    assert not rec.within_tolerance
    assert "average" in rec.strategy_note
    assert "don't skip" in rec.strategy_note


def test_math_shown_adds_up(alex_plan, alex, foods):
    situation = Situation(completed_meals=["breakfast"], meal_to_solve="lunch")
    rec = nutrition.recommend(alex_plan, alex, situation, foods)
    m = rec.math
    assert m.remaining_kcal == m.target.calories_kcal - m.consumed_kcal - m.reserved_kcal
    assert m.remaining_protein_g == m.target.protein_g - m.consumed_protein_g - m.reserved_protein_g


# ----------------------------------------------------------------- safety --

@pytest.mark.parametrize("message", [
    "I feel dizzy and weak",
    "I've been sick with a fever since yesterday",
    "what supplements should I take?",
    "can you write me a training plan?",
    "should I change my medication timing around meals?",
])
def test_safety_screen_escalates(message):
    assert safety.screen(message).action in ("stop", "decline_oos")


def test_safety_screen_repeated_skips():
    assert safety.screen("nothing special", skipped_days=2).action == "stop"
    assert safety.screen("nothing special", skipped_days=1).action == "continue"


def test_safety_screen_passes_normal_requests():
    assert safety.screen("I ate a burger, what should dinner be?").action == "continue"


# ----------------------------------------------------------- sleep agent --

def test_sleep_consult_on_late_meal():
    assert sleep_recovery.should_consult(Situation(meal_time="21:30"))
    assert sleep_recovery.should_consult(Situation(upcoming_fixed=[("team dinner", 900, 50)]))
    assert not sleep_recovery.should_consult(Situation(meal_time="12:30"))


def test_sleep_advice_mentions_training_when_relevant(alex):
    note = sleep_recovery.advise(Situation(meal_time="21:00"), alex)
    assert "train tomorrow" in note


# ------------------------------------------------------------ orchestrator --

def test_trigger_classification():
    assert classify_trigger("I have to skip lunch today") == Trigger.MUST_SKIP
    assert classify_trigger("team dinner tonight!") == Trigger.SURPRISE_MEAL
    assert classify_trigger("I ate a donut") == Trigger.OFF_PLAN_EXTRA
    assert classify_trigger("my planned meal isn't available") == Trigger.ON_THE_SPOT_SWAP


def test_orchestrator_safety_first(alex_plan, alex, foods):
    orch = Orchestrator(alex_plan, alex, foods, use_llm=False)
    result = orch.handle_text("I feel dizzy, what should I eat for lunch?")
    assert result.route == Route.ESCALATE
    assert result.recommendation is None


def test_orchestrator_requires_targets(foods, alex):
    plan = parse_plan_file(MAJA_PLAN)  # no targets
    orch = Orchestrator(plan, alex, foods, use_llm=False)
    result = orch.handle(Situation(trigger=Trigger.MUST_SKIP))
    assert result.route == Route.CLARIFY
    assert "targets" in result.question.lower()


def test_orchestrator_routes_to_sleep_on_late_dinner(alex_plan, alex, foods):
    orch = Orchestrator(alex_plan, alex, foods, use_llm=False)
    result = orch.handle(Situation(
        trigger=Trigger.ON_THE_SPOT_SWAP,
        completed_meals=["breakfast", "lunch", "snack"],
        meal_to_solve="dinner", meal_time="21:00", available=["restaurant"],
    ))
    assert result.route == Route.NUTRITION_WITH_SLEEP
    assert result.recommendation.sleep_note


def test_orchestrator_out_of_scope_smalltalk(alex_plan, alex, foods):
    orch = Orchestrator(alex_plan, alex, foods, use_llm=False)
    result = orch.handle_text("what's the weather like?")
    assert result.route == Route.CLARIFY  # unparseable -> ask + presets, never guess
