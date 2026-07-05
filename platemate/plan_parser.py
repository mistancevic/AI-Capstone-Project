"""Parse an uploaded coach plan (markdown) into targets + baseline meals.

Plans are synthetic documents. The parser reads two shapes:

  - a header block with lines like "Daily calories: 2400 kcal" and
    "Daily protein: 160 g"
  - a meal table with rows "| Breakfast ... | 450 | 35 |" or bullet lines
    "- Breakfast: oats with whey — 450 kcal, 35 g protein"

If the document does not state daily targets, `Plan.targets` is None and the
app must capture them during onboarding (`capture_targets`).
"""

from __future__ import annotations

import re
from pathlib import Path

from .models import Plan, PlannedMeal, Targets

_CAL_RE = re.compile(r"daily\s+calories?\s*[:\-]?\s*(\d{3,5})\s*kcal", re.I)
_PROT_RE = re.compile(r"daily\s+protein\s*[:\-]?\s*(\d{2,4})\s*g", re.I)
_CLIENT_RE = re.compile(r"client\s*[:\-]?\s*(.+)", re.I)

# "- Breakfast: oats with whey — 450 kcal, 35 g protein"
_BULLET_MEAL_RE = re.compile(
    r"^[-*]\s*(?P<name>[^:]+):\s*(?P<desc>.+?)[—\-–]+\s*(?P<kcal>\d{2,4})\s*kcal[,;]?\s*(?P<prot>\d{1,3})\s*g",
    re.I,
)

# "| Breakfast | oats with whey | 450 | 35 |"
_TABLE_MEAL_RE = re.compile(
    r"^\|\s*(?P<name>[A-Za-z][^|]*?)\s*\|\s*(?P<desc>[^|]*?)\s*\|\s*(?P<kcal>\d{2,4})\s*\|\s*(?P<prot>\d{1,3})\s*\|"
)


def parse_plan(text: str, source: str = "") -> Plan:
    client = "Client"
    m = _CLIENT_RE.search(text)
    if m:
        client = m.group(1).strip()

    targets = None
    cal_m, prot_m = _CAL_RE.search(text), _PROT_RE.search(text)
    if cal_m and prot_m:
        targets = Targets(calories_kcal=int(cal_m.group(1)), protein_g=int(prot_m.group(1)))

    meals: list[PlannedMeal] = []
    for line in text.splitlines():
        line = line.strip()
        m = _BULLET_MEAL_RE.match(line) or _TABLE_MEAL_RE.match(line)
        if not m:
            continue
        name = m.group("name").strip()
        if name.lower() in {"meal", "---", ""} or set(name) <= {"-", " "}:
            continue  # table header/separator rows
        meals.append(
            PlannedMeal(
                name=f"{name}: {m.group('desc').strip()}".rstrip(": "),
                calories_kcal=int(m.group("kcal")),
                protein_g=int(m.group("prot")),
                time_hint=name.lower(),
            )
        )

    return Plan(client_name=client, targets=targets, meals=meals, source=source)


def parse_plan_file(path: str | Path) -> Plan:
    p = Path(path)
    return parse_plan(p.read_text(encoding="utf-8"), source=str(p))


def capture_targets(plan: Plan, calories_kcal: int, protein_g: int) -> Plan:
    """Onboarding-capture path: the plan omitted targets, so the client (or
    coach) states them and we attach them without touching anything else."""
    if calories_kcal <= 0 or protein_g <= 0:
        raise ValueError("targets must be positive")
    plan.targets = Targets(calories_kcal=calories_kcal, protein_g=protein_g)
    return plan


def plan_summary(plan: Plan) -> str:
    """The echo-back-for-confirmation text shown after upload."""
    lines = [f"Plan loaded for {plan.client_name} ({plan.source or 'inline'})."]
    if plan.targets:
        lines.append(f"Daily targets: {plan.targets}")
    else:
        lines.append("Daily targets: NOT stated in the document — I need to capture them before adapting anything.")
    if plan.meals:
        lines.append("Baseline meals:")
        for meal in plan.meals:
            lines.append(f"  - {meal.name} ({meal.calories_kcal} kcal, {meal.protein_g} g protein)")
    return "\n".join(lines)
