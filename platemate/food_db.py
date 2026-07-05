"""Load and filter the synthetic food & macro reference table."""

from __future__ import annotations

import json
from pathlib import Path

from .models import ClientProfile, FoodItem

DEFAULT_FOODS_PATH = Path(__file__).resolve().parent.parent / "data" / "foods.json"


def load_foods(path: str | Path = DEFAULT_FOODS_PATH) -> list[FoodItem]:
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    return [
        FoodItem(
            name=item["name"],
            calories_kcal=item["calories_kcal"],
            protein_g=item["protein_g"],
            availability=tuple(item["availability"]),
            prep_minutes=item.get("prep_minutes", 0),
            tags=tuple(item.get("tags", [])),
            meal_types=tuple(item.get("meal_types", ["lunch", "dinner"])),
        )
        for item in raw
    ]


def filter_foods(
    foods: list[FoodItem],
    profile: ClientProfile,
    available: list[str],
    minutes_available: int,
    meal_type: str = "lunch",
) -> list[FoodItem]:
    """Keep only foods the client can actually get, prepare in time, and eat."""
    out = []
    for food in foods:
        if not any(a in food.availability for a in available):
            continue
        if food.prep_minutes > minutes_available:
            continue
        if meal_type and meal_type not in food.meal_types and not food.is_bridge:
            continue
        if any(r in food.tags for r in profile.restrictions):
            continue
        if any(d.lower() in food.name.lower() for d in profile.dislikes):
            continue
        out.append(food)
    return out
