# Glossary — IDs, Prefixes, Codes & Abbreviations

One place for every identifier and shorthand used across the project. When
an output, log row, or document cites a code, this is where it resolves.

## Record ID prefixes (synthetic data)

| Prefix | Means | Lives in | Example |
|---|---|---|---|
| **D-** | **D**isruption case — one client message on one day, the unit the agent processes | `develop-companion/data/disruptions.csv` | D-1001 = Alex's ice-cream + team-dinner day |
| **C-** | **C**lient (persona) | `develop-companion/data/clients.csv` | C-01 = Alex, C-02 = Maya |
| **E-** | **E**val case — a test with expected behavior, pointing at a D- case | `develop-companion/data/eval_cases.csv` | E-5 = Boundary, must refuse (runs D-1005) |
| *(Numbering)* | Starts at 1001 (cases) / 01 (clients) for even width — labels only; no logic depends on them | | |

**D- ids run in date order** across the nine-day timeline (14–22 July), so
they are a history, not a menu. E- ids are just test numbers. The two only
look aligned by accident: E-1…E-5 use D-1001…D-1005 because those are the
first days' cases, and then it breaks — **E-6 is D-1012, not D-1006**,
because the third-compensatory-ask test needs a message arriving *after*
two asks already stand in the rolling week (C-01's counter: 0 until Jul 18,
1 on Jul 19, **2 on Jul 20** — D-1012's date — then reset). D-1006 is a
five-minutes-for-lunch case on Jul 17, when the counter is still 0.

The Python prototype's eval set uses plain case numbers (Case 1–7, from
DESIGN.md §10) and scenario ids (`case1_happy_path` …) instead of D-/E- ids.
Mapping: E-1→Case 1, E-2→Case 2, E-3→Case 3, E-4→Case 4, E-5→Case 7;
Design Cases 5 (imperfect day) and 6 (third compensatory ask) are the
"make one case harder" reserves for eval Section C (kit prompt 17).

## Policy section codes (citable rules)

**A- = Adaptation policy** (`develop-companion/policies/adaptation_policy.md`) — the math rules:

| Code | Rule |
|---|---|
| A1 | Budget math — remaining = target − consumed − reserved; every number traces |
| A2 | Tolerance band — ±150 kcal / ±10 g protein, per-macro verdicts independent |
| A3 | Ranking — protein anchor; hard filters (restrictions) never tradeable |
| A4 | Never-skip bridge — always one compatible fallback option |
| A5 | Imperfect day — exact gap labels + 3–7-day averaging; math never escalates |
| A6 | Confirm gate — nothing logs without the client's click (the only write) |
| A7 | Plan authority — the coach's plan is never edited; missing targets → ask |

**S- = Safety policy** (`develop-companion/policies/safety_policy.md`) — the floor:

| Code | Rule |
|---|---|
| S1 | Health signals (dizzy, faint, fever…) → hard stop + GET HELP NOW |
| S2a | Multi-day undereating self-report → hard stop (disclosure alone triggers) |
| S2b | Restriction demand below the compliance floor → refusal naming the floor |
| S2c | Compensatory ask / skip-intent → tiered: 1st–2nd nudge + counter, 3rd = stop |
| S3 | Skipped-days counter ≥ 2 → hard stop |
| S4 | Out-of-scope (supplements, medication, training) → decline to coach, digest |
| S5 | Hostility → changes tone only, never the verdict |
| S6 | Flag tiers & delivery — quiet hours delay notification, never protection |
| S7 | Banned language list + deterministic fallback coaching line |

(The repo-root `data/safety_policy.md` states the same rules for the Python
prototype, with pre-authored wording blocks the code reads verbatim.)

## Statuses, tiers, modes (what the app shows)

| Term | Meaning |
|---|---|
| **OK** | Safety passed; an options card was produced; awaiting human review |
| **REFUSED-ESCALATE** | A hard stop fired; no card; coach flagged; safe default shown |
| **CLARIFY** | Required facts missing (targets or situation slots) — the app asks, never guesses |
| **OUT-OF-SCOPE** | S4 decline; pointed to the coach; digest entry only |
| **URGENT / NORMAL / DIGEST** | Coach-flag tiers (S6): immediate-or-window-open / daily digest / weekly count-only |
| **offline rules mode** | No API key: deterministic keyword parse + fallback line — the design's model-off claim, running |
| **one-way rule** | A live model may ADD a stop the keywords missed; it can never clear a deterministic stop |
| **queued / delivered (+1d)** | Flag timing: when it fired vs. when quiet hours let it reach the coach (next day) |

## Counters & the band

| Term | Meaning |
|---|---|
| **skipped_days_counter** | Consecutive days with skipped meals; ≥2 triggers S3. Resets on a confirmed eaten day |
| **compensatory_asks_week** | Compensatory asks in a rolling 7-day window; the 1-2-vs-3 tier lever (S2c). Counters store counts, never message texts |
| **the band** | The A2 tolerance: ±150 kcal / ±10 g protein on the projected day-end total |
| **bridge** | The always-available never-skip fallback food (A4) |
| **day-end +N / −N** | An option's projected day total minus target — the signed gap label |

## The five stages (kit console, prompt 11)

**1 INPUT** the message · **2 CONTEXT** what the agent reads · **3 DECISION**
status + why + citations · **4 OUTPUT** the labeled fields · **5 REVIEW**
approve / edit / escalate — the human gate.

## Project-wide shorthand (documents & research)

| Term | Meaning |
|---|---|
| **4D** | The Product Faculty method: Discovery → Design → Develop → Deploy |
| **PRD** | Product Requirements Document — the capstone master sheet |
| **EST / n CH** | Journey-map labels: estimated score / number of independent research channels supporting it (≥3 = triangulated) |
| **AVE** | Abstinence violation effect — the "day's ruined, eat anyway" spiral (a.k.a. what-the-hell effect); the corrected disruption mechanism |
| **QQRT** | Quantity, quality (incl. bioavailability), regularity, timing — the four-axis lens in `notes/strategy-notes.md` |
| **IF / OMAD** | Intermittent fasting / one-meal-a-day — strategic skipping patterns the skip counter must not punish |
| **JITAI** | Just-in-time adaptive intervention (research term for in-the-moment support) |
| **B2B2C** | Business-to-business-to-consumer — the coach-led distribution model |
| **WTP** | Willingness to pay |
| **M1 / M2** | Moe's build order: Case 1 + Case 7 spine first, then the tier pair and the rest |
