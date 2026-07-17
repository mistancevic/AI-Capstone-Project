"""Nutrition agent: remaining-budget math, option ranking, bridge fallback.

Design intent (from the PRD): skipping is never the default. The agent always
returns at least a bridge option, shows its arithmetic, and — when the day
cannot be balanced within tolerance — explains the multi-day averaging
principle (calories average over 3-7 days, protein stays the daily anchor).
"""

from __future__ import annotations

from .. import policy
from ..food_db import filter_foods
from ..models import (
    AVERAGING_WINDOW_DAYS,
    BudgetMath,
    ClientProfile,
    FoodItem,
    Plan,
    RankedOption,
    Recommendation,
    Situation,
)


def _matches(meal_hint: str, labels: list[str]) -> bool:
    hint = meal_hint.lower()
    return any(hint in label.lower() or label.lower() in hint for label in labels if label)


def compute_budget(plan: Plan, situation: Situation) -> BudgetMath:
    """Remaining budget for the meal being solved =
    daily target
      − (planned meals already eaten + off-plan extras)          [consumed]
      − (upcoming fixed commitments + remaining planned meals)   [reserved]

    Remaining planned meals stay reserved unless they are the slot being
    solved, or the client marked them skipped/displaced.
    """
    assert plan.targets is not None, "targets must be set before adapting"

    consumed_kcal = consumed_prot = 0
    reserved_kcal = sum(k for _, k, _ in situation.upcoming_fixed)
    reserved_prot = sum(p for _, _, p in situation.upcoming_fixed)

    for meal in plan.meals:
        if _matches(meal.time_hint, situation.completed_meals) or meal.name in situation.completed_meals:
            consumed_kcal += meal.calories_kcal
            consumed_prot += meal.protein_g
        elif _matches(meal.time_hint, [situation.meal_to_solve]):
            continue  # this is the slot we are recommending for
        elif _matches(meal.time_hint, situation.skipped_meals):
            continue  # won't happen as planned (skipped or displaced)
        else:
            reserved_kcal += meal.calories_kcal
            reserved_prot += meal.protein_g

    for _, kcal, prot in situation.eaten_off_plan:
        consumed_kcal += kcal
        consumed_prot += prot

    return BudgetMath(
        target=plan.targets,
        consumed_kcal=consumed_kcal,
        consumed_protein_g=consumed_prot,
        reserved_kcal=reserved_kcal,
        reserved_protein_g=reserved_prot,
        remaining_kcal=plan.targets.calories_kcal - consumed_kcal - reserved_kcal,
        remaining_protein_g=plan.targets.protein_g - consumed_prot - reserved_prot,
    )


def _score(food: FoodItem, math: BudgetMath, profile: ClientProfile) -> tuple[float, str]:
    """Lower is better. Protein fit is the anchor; calorie overshoot is
    penalized harder than undershoot (undershoot can average out over days)."""
    protein_gap = math.remaining_protein_g - food.protein_g
    kcal_gap = math.remaining_kcal - food.calories_kcal

    score = abs(protein_gap) * 3.0
    score += (abs(kcal_gap) / 50.0) if kcal_gap >= 0 else (abs(kcal_gap) / 25.0)

    band = policy.tolerance()
    why = []
    if food.protein_g >= math.remaining_protein_g - band["protein_g"]:
        why.append("covers the remaining protein")
    else:
        why.append(f"covers {food.protein_g} g of the {max(math.remaining_protein_g, 0)} g still needed")
    if kcal_gap < -band["calories_kcal"]:
        why.append(f"runs ~{-kcal_gap} kcal over the remaining budget")
    elif kcal_gap >= 0:
        why.append("fits the calorie budget")

    if any(like.lower() in food.name.lower() for like in profile.likes):
        score -= 5.0
        why.append("matches your stated preferences")
    if food.is_bridge:
        score += 8.0  # real meals outrank bridges; bridge is the safety net

    return score, "; ".join(why)


def _project_day_end(food: FoodItem, math: BudgetMath) -> tuple[int, int]:
    """Projected (day_total − target) after eating this option, assuming the
    upcoming fixed commitments land as estimated."""
    kcal_gap = (math.consumed_kcal + math.reserved_kcal + food.calories_kcal) - math.target.calories_kcal
    prot_gap = (math.consumed_protein_g + math.reserved_protein_g + food.protein_g) - math.target.protein_g
    return kcal_gap, prot_gap


def recommend(
    plan: Plan,
    profile: ClientProfile,
    situation: Situation,
    foods: list[FoodItem],
    top_n: int = 3,
) -> Recommendation:
    math = compute_budget(plan, situation)

    candidates = filter_foods(
        foods,
        profile,
        available=situation.available,
        minutes_available=situation.minutes_available,
        meal_type=situation.meal_to_solve,
    )

    ranked: list[RankedOption] = []
    for food in candidates:
        score, why = _score(food, math, profile)
        kcal_gap, prot_gap = _project_day_end(food, math)
        ranked.append(RankedOption(food=food, score=score, rationale=why,
                                   day_end_kcal_gap=kcal_gap, day_end_protein_gap=prot_gap))
    ranked.sort(key=lambda r: r.score)

    meals = [r for r in ranked if not r.food.is_bridge][:top_n]
    bridges = [r for r in ranked if r.food.is_bridge]
    bridge = min(bridges, key=lambda r: r.score) if bridges else None

    # A recommendation is "within tolerance" when its best option lands the
    # projected day inside the tolerance band.
    band = policy.tolerance()  # the band as data (data/tolerance.json), Check 2
    best = meals[0] if meals else bridge
    within = bool(
        best
        and abs(best.day_end_protein_gap) <= band["protein_g"]
        and abs(best.day_end_kcal_gap) <= band["calories_kcal"]
    )

    strategy = ""
    if not within:
        strategy = _strategy_note(best)

    return Recommendation(math=math, options=meals, bridge=bridge,
                          within_tolerance=within, strategy_note=strategy)


def _strategy_note(best: RankedOption | None) -> str:
    low, high = AVERAGING_WINDOW_DAYS
    kcal_gap = best.day_end_kcal_gap if best else 0
    per_day = max(50, round(abs(kcal_gap) / low / 50) * 50)
    if kcal_gap > 0:
        adjust = f"trim roughly {per_day} kcal/day over the next few days"
    elif kcal_gap < 0:
        adjust = (
            f"you'll land about {abs(kcal_gap)} kcal under today — add a snack "
            f"later if you can, or add roughly {per_day} kcal/day over the next few days"
        )
    else:
        adjust = "keep the next few days on plan"
    return (
        "Today won't balance perfectly, and that is fine: calories can "
        f"average out over a {low}-{high} day window, so {adjust}. Protein "
        "stays the daily anchor — pick the highest-protein option above "
        "and don't skip."
    )


def format_recommendation(rec: Recommendation) -> str:
    lines = ["Remaining-day math:"]
    lines += [f"  {line}" for line in rec.math.lines()]
    lines.append("")
    if rec.options:
        lines.append("Ranked options:")
        for i, opt in enumerate(rec.options, 1):
            lines.append(
                f"  {i}. {opt.food.name} — {opt.food.calories_kcal} kcal, "
                f"{opt.food.protein_g} g protein ({opt.rationale})"
            )
    if rec.bridge:
        b = rec.bridge.food
        lines.append(
            f"  Bridge fallback: {b.name} — {b.calories_kcal} kcal, {b.protein_g} g protein "
            "(if nothing above works, take this instead of skipping)"
        )
    if rec.strategy_note:
        lines.append("")
        lines.append(f"Strategy: {rec.strategy_note}")
    if rec.sleep_note:
        lines.append("")
        lines.append(f"Sleep & recovery: {rec.sleep_note}")
    if rec.coaching_line:
        lines.append("")
        lines.append(f"Coach's corner: {rec.coaching_line}")
    return "\n".join(lines)
