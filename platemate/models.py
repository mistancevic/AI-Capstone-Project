"""Core data models for PlateMate.

Everything the agents pass between each other is a plain dataclass so the
whole pipeline is inspectable and testable without any AI in the loop.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


# Tolerance rule (encoded as data, per the PRD): a day that lands within
# these margins of target counts as compliant. Anything beyond triggers the
# multi-day averaging strategy.
PROTEIN_TOLERANCE_G = 10
CALORIE_TOLERANCE_KCAL = 150

# Calories can average over a 3-7 day window; protein stays the daily anchor.
AVERAGING_WINDOW_DAYS = (3, 7)


@dataclass(frozen=True)
class Targets:
    """Daily targets prescribed by the coach's plan (or captured at onboarding)."""

    calories_kcal: int
    protein_g: int

    def __str__(self) -> str:
        return f"{self.calories_kcal} kcal / {self.protein_g} g protein"


@dataclass(frozen=True)
class PlannedMeal:
    """One baseline meal from the prescribed plan."""

    name: str
    calories_kcal: int
    protein_g: int
    time_hint: str = ""  # e.g. "08:00", "lunch", "late"


@dataclass
class Plan:
    """A parsed coach plan. `targets` is None when the uploaded document does
    not state them — that is the onboarding-capture path."""

    client_name: str
    targets: Targets | None
    meals: list[PlannedMeal] = field(default_factory=list)
    notes: str = ""
    source: str = ""

    @property
    def needs_target_capture(self) -> bool:
        return self.targets is None


@dataclass
class ClientProfile:
    """Synthetic persona: preferences, restrictions, and context the agents
    filter against. No real personal information."""

    name: str
    goal: str = ""
    restrictions: list[str] = field(default_factory=list)  # e.g. ["lactose"]
    dislikes: list[str] = field(default_factory=list)
    likes: list[str] = field(default_factory=list)
    training_tomorrow: bool = False
    usual_bedtime: str = "23:00"


class Availability(str, Enum):
    HOME = "home"          # have-at-home
    SHOP = "shop"          # nearby-shop
    RESTAURANT = "restaurant"


@dataclass(frozen=True)
class FoodItem:
    """One entry in the food & macro reference table."""

    name: str
    calories_kcal: int
    protein_g: int
    availability: tuple[str, ...]          # subset of Availability values
    prep_minutes: int = 0
    tags: tuple[str, ...] = ()             # e.g. ("bridge", "vegetarian", "dairy")
    meal_types: tuple[str, ...] = ("lunch", "dinner")

    @property
    def is_bridge(self) -> bool:
        return "bridge" in self.tags


class Route(str, Enum):
    """Where the orchestrator can send a request."""

    NUTRITION = "nutrition"
    NUTRITION_WITH_SLEEP = "nutrition+sleep_recovery"
    ESCALATE = "escalate_to_coach"
    OUT_OF_SCOPE = "out_of_scope"


class Trigger(str, Enum):
    """The recurring-workflow triggers from the PRD."""

    OFF_PLAN_EXTRA = "off_plan_extra"      # ate something off-plan
    SURPRISE_MEAL = "surprise_meal"        # unplanned large meal coming
    MUST_SKIP = "must_skip"                # a planned meal cannot happen
    MORNING_CHECK = "morning_check"        # rebuild before the day breaks
    ON_THE_SPOT_SWAP = "on_the_spot_swap"  # planned meal unavailable right now
    UNKNOWN = "unknown"


@dataclass
class Situation:
    """A structured description of the disrupted day, either parsed from the
    client's free-text message (LLM path) or supplied directly (demo/eval)."""

    raw_text: str = ""
    trigger: Trigger = Trigger.UNKNOWN
    eaten_off_plan: list[tuple[str, int, int]] = field(default_factory=list)
    #   ^ (label, kcal, protein_g) for anything already consumed off-plan
    completed_meals: list[str] = field(default_factory=list)
    #   ^ names of planned meals already eaten as planned
    upcoming_fixed: list[tuple[str, int, int]] = field(default_factory=list)
    #   ^ (label, est_kcal, est_protein_g) commitments that WILL happen (e.g. team dinner)
    meal_to_solve: str = "lunch"           # which meal slot we are recommending for
    skipped_meals: list[str] = field(default_factory=list)
    available: list[str] = field(default_factory=lambda: ["home", "shop"])
    minutes_available: int = 30
    meal_time: str = ""                    # e.g. "21:30" when the solved meal is late
    health_flags: list[str] = field(default_factory=list)
    #   ^ raw phrases that tripped the safety screen, if any


def situation_from_dict(data: dict) -> Situation:
    """Build a Situation from a plain JSON dict (used by the eval scenarios)."""
    return Situation(
        raw_text=data.get("raw_text", ""),
        trigger=Trigger(data.get("trigger", "unknown")),
        eaten_off_plan=[tuple(e) for e in data.get("eaten_off_plan", [])],
        completed_meals=list(data.get("completed_meals", [])),
        upcoming_fixed=[tuple(e) for e in data.get("upcoming_fixed", [])],
        meal_to_solve=data.get("meal_to_solve", "lunch"),
        skipped_meals=list(data.get("skipped_meals", [])),
        available=list(data.get("available", ["home", "shop"])),
        minutes_available=data.get("minutes_available", 30),
        meal_time=data.get("meal_time", ""),
    )


@dataclass
class BudgetMath:
    """The remaining-day arithmetic, kept explicit so it can be shown to the
    client ("with the math shown") and asserted in tests."""

    target: Targets
    consumed_kcal: int
    consumed_protein_g: int
    reserved_kcal: int          # upcoming fixed commitments
    reserved_protein_g: int
    remaining_kcal: int         # what the meal we're solving for may use
    remaining_protein_g: int

    def lines(self) -> list[str]:
        return [
            f"Daily target:            {self.target.calories_kcal:>5} kcal | {self.target.protein_g:>4} g protein",
            f"Already consumed:      - {self.consumed_kcal:>5} kcal | {self.consumed_protein_g:>4} g",
            f"Reserved (upcoming):   - {self.reserved_kcal:>5} kcal | {self.reserved_protein_g:>4} g",
            f"Remaining for this meal: {self.remaining_kcal:>5} kcal | {self.remaining_protein_g:>4} g",
        ]


@dataclass
class RankedOption:
    food: FoodItem
    score: float
    rationale: str
    day_end_kcal_gap: int      # projected day total minus target (after this option)
    day_end_protein_gap: int


@dataclass
class Recommendation:
    """The nutrition agent's answer for one disrupted-day request."""

    math: BudgetMath
    options: list[RankedOption]
    bridge: RankedOption | None
    within_tolerance: bool
    strategy_note: str = ""    # multi-day averaging advice when out of tolerance
    coaching_line: str = ""
    sleep_note: str = ""


@dataclass
class Escalation:
    """A refusal + hand-off to the human coach."""

    reasons: list[str]
    message: str


@dataclass
class AgentResult:
    """What the orchestrator returns for any request."""

    route: Route
    trigger: Trigger = Trigger.UNKNOWN
    recommendation: Recommendation | None = None
    escalation: Escalation | None = None
    consulted_agents: list[str] = field(default_factory=list)
