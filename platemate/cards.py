"""Output cards — DESIGN.md §7: labeled fields a reviewer can judge in
under sixty seconds. Four outputs: options card, imperfect-day card (same
renderer, gap-labeled), stop message (assembled on the stop path from
pre-authored blocks), coach flag."""

from __future__ import annotations

from .escalation import CoachFlag
from .models import AgentResult, Recommendation


def render_options_card(rec: Recommendation) -> str:
    lines = ["BUDGET"]
    lines += [f"  {l}" for l in rec.math.lines()]
    lines.append("")
    header = "OPTIONS" if rec.within_tolerance else \
        "OPTIONS (closest possible — no option lands in the band today)"
    lines.append(header)
    for i, opt in enumerate(rec.options, 1):
        f = opt.food
        kcal_gap = f"{opt.day_end_kcal_gap:+d}"
        prot_gap = f"{opt.day_end_protein_gap:+d}"
        verdict = " ✓" if rec.within_tolerance and i == 1 else ""
        lines.append(
            f"  {i}. {f.name} — {f.calories_kcal} kcal, {f.protein_g} g protein, "
            f"{f.prep_minutes} min — day-end {kcal_gap} kcal / {prot_gap} g{verdict}")
    lines.append("")
    if rec.bridge:
        b = rec.bridge.food
        lines.append("BRIDGE")
        lines.append(f"  {b.name} — {b.calories_kcal} kcal, {b.protein_g} g protein "
                     "— if nothing above works, take this instead of skipping.")
        lines.append("")
    if rec.strategy_note:
        lines.append("STRATEGY")
        lines.append(f"  {rec.strategy_note}")
        lines.append("")
    if rec.sleep_note:
        lines.append("NOTE")
        lines.append(f"  {rec.sleep_note}")
        lines.append("")
    lines.append("COACHING LINE")
    lines.append(f"  {rec.coaching_line}")
    return "\n".join(lines)


def render_flag(flag: CoachFlag) -> str:
    lines = [
        f"COACH FLAG [{flag.tier.value.upper()}]",
        f"  Reason codes: {'; '.join(flag.reason_codes)}",
        f"  Counters: {flag.counter_history}",
        f"  Queued: {flag.queued_at} — delivered: {flag.delivered_at}",
    ]
    if flag.trigger_message_shared:
        lines.append("  Triggering message shared once, per the coaching agreement.")
    return "\n".join(lines)


def render(result: AgentResult) -> str:
    """Render whatever the run produced, as the client sees it."""
    parts: list[str] = []
    if result.question:
        parts.append(result.question)
        if result.presets:
            parts.append("")
            parts += [f"  [{i}] {p}" for i, p in enumerate(result.presets, 1)]
    elif result.escalation:
        parts.append(result.escalation.message)
    elif result.recommendation:
        parts.append(render_options_card(result.recommendation))
    if result.flag:
        parts += ["", render_flag(result.flag)]
    return "\n".join(parts)
