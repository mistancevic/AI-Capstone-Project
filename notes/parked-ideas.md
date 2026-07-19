# Parked Ideas & Initiatives — the product beyond the capstone

Principle: **nothing valuable gets deleted; it gets parked with provenance
and a revival condition.** The capstone trims scope to prove the core loop;
this file is the shelf where every trimmed ambition waits. Each entry says
where it came from and what would bring it back.

Rule of thumb inherited from faculty review: *prove the loop first, then
earn the complexity.* This file is the complexity queue.

## Near-term (v1.x — first additions after the capstone demo)

| Idea | Provenance | Revival condition |
|---|---|---|
| **Daily watch** — clock-triggered counters advancing on silent days, one gentle check-in after 3 silent days, coach flag at the same thresholds | Designed in DESIGN.md, out of demo scope | Demo loop proven; needs real scheduling runtime |
| **Pause mode (runtime)** — client-declared "away until Sunday": suspends logging expectations, auto-resumes, appears in coach digest, never mutes the safety screen | Designed in DESIGN.md; demo carries only seeded state | Same as daily watch — they ship together |
| **Weekly digest to the coach** — adherence summary per client, flags rolled up | DESIGN.md (watch); discovery diverge/converge table | First real coach using it |
| **Flag deduplication** — counter + self-report both firing currently delivers the flag twice (errs safe) | DESIGN.md, explicitly future work | First coach complaint about double flags — not before |
| **Client-facing weekly review digest** | Discovery diverge/converge (scored 6/7) | After coach digest exists |

## v2 product initiatives (each is a strategy bet, not just a feature)

| Initiative | Provenance | Why it waits / revival condition |
|---|---|---|
| **Social events & travel mode** — pre-event calorie banking, travel day handling, "you have a wedding Saturday" planning | Investigation 4: the **cleanest competitive whitespace** — zero features across all six incumbents; investigation 3: hermit strategy + banking behaviors documented | The strongest candidate for the first post-v1 wedge widening; needs v1 retention data first |
| **Coach-side experience** — digest, triage inbox, roster view | Strategy notes: the moat deepener (switching costs once a roster runs through the app) | First 2–3 real coaches onboarded; their interviews (investigation 5 Part B) shape it |
| **Full sleep & recovery agent** — late meal ↔ sleep ↔ tomorrow's training reasoning; assessment structured by QQRT (quantity, quality, regularity, timing — the sleep-science four-determinant model, used literally in its home domain here). The current one-line note is already a timing intervention. | Discovery step-0 orchestrator vision; trimmed by Moe to a conditional one-line note | Core loop solid in production, and evidence that clients act on the note |
| **Multi-agent registry (fitness / movement / recovery agents)** — the original step-0 orchestrator vision; `platemate/agents/stubs.py` is this idea's placeholder code | Discovery; Moe's no-stubs directive removed it from the demo path — **parked, not deleted** | Each agent added only when its domain has a real data source and a consuming decision; never as stubs |
| **Boredom/variety engine** — rotate equivalent options to fight culinary fatigue, without touching targets | Investigations 1–4: plateau≠boredom split; *no incumbent solves both halves* | Careful: investigation 3 shows a cohort *weaponizes* monotony — variety must be opt-in, never pushed |
| **Calendar integration** — see the disruption coming (meeting over lunch) before it happens | Strategy notes ("steady energy" section) | Only with honest, consented value; stays out until the pull-based loop earns trust |

## Long-horizon / conditional

| Idea | Provenance | Condition |
|---|---|---|
| **Initial plan crafting** — the app drafts the plan a coach then edits and owns | Discovery scalability note | Changes the category (plan authority shifts); only with coach demand and regulatory care |
| **Food ordering / nearest-shop integration** — turn the chosen option into an order or a route | Discovery ("next version" from day one) | Real user base; partnership economics |
| **Lapse-prediction nudging** — ML predicting a risky day before it breaks | Investigation 3 fallback: 0.72 group-level accuracy, poor individual generalization, ~4 weeks personal data needed | Realistic expectations documented; needs months of real data per user; v3+ at earliest |
| **"Steady energy" measurement features** — glycemic claims, focus scores, calendar-triggered fueling | Strategy notes | Only when honestly measurable; positioning language may use "steady energy" now, features may not |
| **Coach directory / find-a-coach** — matching clients to coaches | Investigation 4: activity-1 whitespace (nobody in the set does matching) | A different business; revisit only if coach-side distribution stalls |
| **Premium hard-stop-override package** — a package tier where urgent flags wake the coach through quiet hours | DESIGN.md agreement schema (config present, unused) | A coach asks for it and prices it |

## Naming & brand

- **Prep & Rep** — vetted successor name (prepare and repeat; fitness-culture
  resonance). Revival: post-capstone rebrand decision, after checking the
  collision landscape again.
- **Mealan** — parked as potential house brand.
- Competitive watch: **Mealner** (closest concept, waitlist as of Jul 2026 —
  investigation 4) — check quarterly whether it shipped.

## Explicitly NOT parked (active Develop backlog — do not shelve these)

- **Strategic-vs-punitive skip distinction** in the skipped-meals counter
  (declared fasting windows count as knowledge, not risk) — investigation 3's
  design requirement; prevents false-positive escalations on IF users.
- The Design-mandated data files missing from the spike (`state_seed.json`,
  `tolerance.json`, `banned_language.md`, coach agreements, `examples.md`)
  — see the readiness audit in [`develop-prep.md`](develop-prep.md).
- The seven eval cases and Moe's two-milestone build order.
