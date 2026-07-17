"""Escalation machinery: coaching agreements, the scenario-controllable
clock, flag tiers, and the simulated coach queue with quiet-hours delivery.

Rule (DESIGN.md): quiet hours delay *notification*, never *protection*.
The client-side stop message is always immediate; the flag's delivery time
is computed from the agreement and shown to the client — the client sees
what the coach sees.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


class Tier(str, Enum):
    URGENT = "urgent"
    NORMAL = "normal"
    DIGEST = "digest"


# --------------------------------------------------------------------- #
#  Clock — scenario-controllable so the 23:00 case is reproducible.
# --------------------------------------------------------------------- #

def _to_minutes(hhmm: str) -> int:
    h, m = hhmm.split(":")
    return int(h) * 60 + int(m)


def _to_hhmm(minutes: int) -> str:
    return f"{(minutes % (24 * 60)) // 60:02d}:{minutes % 60:02d}"


@dataclass(frozen=True)
class Clock:
    now: str  # "HH:MM"

    @property
    def minutes(self) -> int:
        return _to_minutes(self.now)


# --------------------------------------------------------------------- #
#  Coaching agreement (parsed from data/coach_agreement_<persona>.md)
# --------------------------------------------------------------------- #

_KV_RE = re.compile(r"^(?P<key>[a-z_]+):\s*(?P<value>.+)$")


@dataclass(frozen=True)
class CoachAgreement:
    channel: str = "in-app coach inbox"
    response_window_hours: int = 24
    quiet_start: str = "21:00"
    quiet_end: str = "07:00"
    flag_scope: str = "all"        # "all" | "urgent_only"
    hard_stop_override: str = "none"

    def in_quiet_hours(self, clock: Clock) -> bool:
        start, end, now = map(_to_minutes, (self.quiet_start, self.quiet_end, clock.now))
        if start <= end:
            return start <= now < end
        return now >= start or now < end  # window crosses midnight

    def delivery_time(self, clock: Clock) -> str:
        """When a flag queued now is delivered, per quiet hours."""
        if not self.in_quiet_hours(clock):
            return clock.now
        end = _to_minutes(self.quiet_end)
        crosses_midnight = _to_minutes(self.quiet_start) > end
        next_day = crosses_midnight and clock.minutes >= _to_minutes(self.quiet_start)
        return f"{_to_hhmm(end)} (+1d)" if next_day else _to_hhmm(end)


def load_agreement(persona_key: str) -> CoachAgreement:
    path = DATA_DIR / f"coach_agreement_{persona_key}.md"
    values: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        m = _KV_RE.match(line.strip())
        if m:
            values[m.group("key")] = m.group("value").strip()
    quiet = values.get("quiet_hours", "21:00-07:00")
    quiet_start, quiet_end = quiet.split("-")
    return CoachAgreement(
        channel=values.get("channel", "in-app coach inbox"),
        response_window_hours=int(values.get("response_window_hours", "24")),
        quiet_start=quiet_start.strip(),
        quiet_end=quiet_end.strip(),
        flag_scope=values.get("flag_scope", "all"),
        hard_stop_override=values.get("hard_stop_override", "none"),
    )


# --------------------------------------------------------------------- #
#  Flags and the simulated coach queue
# --------------------------------------------------------------------- #

@dataclass
class CoachFlag:
    tier: Tier
    reason_codes: list[str]
    counter_history: dict[str, int]     # counts only — never message texts
    queued_at: str
    delivered_at: str
    trigger_message_shared: bool = False  # once, per the agreement
    note: str = ""


@dataclass
class CoachQueue:
    """Demo inbox — nothing real is sent."""

    agreement: CoachAgreement
    flags: list[CoachFlag] = field(default_factory=list)

    def submit(self, tier: Tier, reasons: list[str], counters: dict[str, int],
               clock: Clock, share_trigger: bool = False, note: str = "") -> CoachFlag | None:
        if tier is Tier.DIGEST and self.agreement.flag_scope == "urgent_only":
            return None  # kept in app state, not delivered — the package the client chose
        delivered = clock.now if tier is not Tier.URGENT else self.agreement.delivery_time(clock)
        if tier is Tier.NORMAL:
            delivered = "with daily digest"
        elif tier is Tier.DIGEST:
            delivered = "with weekly digest"
        flag = CoachFlag(tier=tier, reason_codes=list(reasons), counter_history=dict(counters),
                         queued_at=clock.now, delivered_at=delivered,
                         trigger_message_shared=share_trigger, note=note)
        self.flags.append(flag)
        return flag
