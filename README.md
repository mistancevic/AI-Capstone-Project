# PlateMate: macros made simple

An agentic nutrition plan-adaptation assistant for coached clients. When real
life disrupts the day — an off-plan snack, a surprise dinner out, a meal that
must be skipped — a first-step **orchestrator agent** reads the situation and
routes it to a **nutrition agent** that computes the remaining calorie and
protein budget and returns 2–3 ranked, plan-compliant meal options with the
macro math shown, plus a bridge fallback so **skipping is never the default**.
A **sleep & recovery agent** is consulted when a food decision (like a late
dinner) also affects sleep or tomorrow's training, and any health, medical,
or out-of-scope signal is **escalated to the human coach**.

Built as the capstone project for the PRD in [`PRD.md`](PRD.md). All data is
synthetic — two invented personas, fake coach plans, and a seeded evaluation
set. No real personal information anywhere.

## Status

The prototype now implements the approved Design (see
[`DESIGN.md`](DESIGN.md)): safety screen first on raw text, counter-tiered
escalation (nudge vs. hard stop), quiet-hours coach-flag delivery, the
banned-language output screen with a deterministic fallback line, the
tolerance band as data (`data/tolerance.json`), and labeled output cards.
The seven Design eval cases run green (`python -m eval.run_eval`, model-off
deterministic mode — the app runs correctly with the model switched off, by
design). Built per the faculty build order: the Case 1 + Case 7 spine
first, then the tier pair and the rest. Discovery and Design are complete
and faculty-approved ([`DISCOVERY.md`](DISCOVERY.md), [`DESIGN.md`](DESIGN.md));
this Develop pass ran as a pre-guide hypothesis
([`notes/develop-prep.md`](notes/develop-prep.md)). Trimmed ambitions are
parked, not deleted ([`notes/parked-ideas.md`](notes/parked-ideas.md)).

## Quick start

```bash
# Optional (the core app is stdlib-only; this adds the Claude layer + tests)
pip install -r requirements.txt

# The web UI (stdlib only, nothing to install) — open http://localhost:8000
# In GitHub Codespaces: run it, then click the "Open in Browser" popup
# (or the PORTS tab -> port 8000 -> globe icon).
python webapp.py

# The continuous demo run from the PRD (plan upload -> disrupted day ->
# onboarding capture -> safety escalation -> stubbed agents)
python demo.py

# The evaluation harness: no-skip rate, macro accuracy, escalation precision
python -m eval.run_eval

# Interactive chat
python -m platemate.cli --persona alex   # or maja

# Tests
python -m pytest tests/ -q
```

Everything runs **fully offline** by default. If `ANTHROPIC_API_KEY` is set
(and the `anthropic` package installed), PlateMate additionally uses Claude
(`claude-opus-4-8`) to parse free-text disrupted-day messages into structured
situations and to write the closing coaching line. The safety screen and all
macro math stay deterministic and rule-based either way — the model is never
in the loop for safety or arithmetic.

## Architecture

```
client message
     │
     ▼
┌───────────────────────────────────────────────────────────┐
│ Orchestrator (platemate/agents/orchestrator.py)           │
│  1. SAFETY SCREEN first — rule-based, never delegated     │
│  2. read the situation (Claude parse, or keyword rules)   │
│  3. route                                                 │
└──────┬──────────────────────┬──────────────────┬──────────┘
       │                      │                  │
       ▼                      ▼                  ▼
  Nutrition agent      Sleep & recovery     Escalate to coach
  budget math,         (consulted on late   (health / medical /
  ranked options,      meals & training     disordered-eating /
  bridge fallback,     conflicts)           out-of-scope)
  multi-day strategy
                                            [stubs: fitness,
                                             movement, recovery]
```

### The core loop (nutrition agent)

1. **Budget math, shown to the client**
   `remaining = daily target − (planned meals eaten + off-plan extras)
   − (upcoming fixed commitments + remaining planned meals)`
2. **Filter** the ~40-item food table by availability (home / shop /
   restaurant), prep time available, meal slot, dietary restrictions, and
   dislikes.
3. **Rank**: protein fit is the anchor (weighted 3×), calorie overshoot is
   penalized harder than undershoot, stated preferences earn a bonus. Real
   meals outrank bridges; the best bridge is always attached as the
   never-skip fallback.
4. **Tolerance rule (encoded as data)**: a projected day within ±10 g protein
   and ±150 kcal of target is compliant. Beyond that, the agent explains the
   multi-day averaging principle — calories can average over a 3–7 day
   window, protein stays the daily anchor — and gives a concrete
   rebalancing amount.

### Safety boundary

`platemate/safety.py` implements `data/safety_policy.md` and runs **before
any routing and before any model call**. It refuses and hands off to the
coach on: health/medical signals (illness, dizziness, injury, …),
disordered-eating patterns (including 2+ days of skipped meals), and
out-of-scope requests (training programming, supplements, medication,
diagnosis). The app only advises; it never logs or finalizes anything without
the client's confirmation and never overrides the coach's plan.

## Repository layout

```
platemate/
  models.py               dataclasses + the tolerance rule as data
  plan_parser.py          coach-plan (markdown) parsing + onboarding capture
  food_db.py              food table loading & filtering
  safety.py               escalation screen (always first)
  llm.py                  optional Claude layer (parse + coaching line)
  cli.py                  interactive REPL
  agents/
    orchestrator.py       routing, trigger classification
    nutrition.py          budget math, ranking, bridge, multi-day strategy
    sleep_recovery.py     late-meal / training-day advice
    stubs.py              fitness, movement, recovery (registered, stubbed)
data/
  plans/alex_plan.md      synthetic plan WITH daily targets
  plans/maja_plan.md      synthetic plan WITHOUT targets (onboarding path)
  personas.json           two synthetic client personas
  foods.json              ~40 foods + bridges, tagged by availability
  safety_policy.md        the escalation policy the code implements
  scenarios.json          10 evaluation scenarios with expected outcomes
eval/run_eval.py          metrics: no-skip rate, macro accuracy, escalation precision
webapp.py                 zero-dependency web UI (plan card, presets, results)
demo.py                   the continuous PRD demo run
tests/test_platemate.py   25 unit tests for the deterministic core
```

## Evaluation results (synthetic set)

`python -m eval.run_eval` on the 10-scenario set:

| Metric | Result |
|---|---|
| No-skip rate | **100%** (7/7 disrupted days got an eatable option) |
| Macro accuracy | avg abs. day-end gap ≈ 184 kcal / 7.4 g protein |
| Escalation precision | **100%** (recall 100%) |
| Scenario checks | 10/10 passed |

## Scope notes / future work

Registered but stubbed (escalate to the coach for now): fitness, movement,
and recovery agents. Not built, per the PRD: crafting the initial diet plan,
sleep and activity modeling.
