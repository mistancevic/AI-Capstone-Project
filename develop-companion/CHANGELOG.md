# PlateMate Prototype — Build / Release History

One entry per build. Each answers three questions: **what problem or
opportunity** the build addresses, **what changed** in the already-working
product, and **how it was verified**. The build id matches the stamp shown
in the app's top bar (`build pNN`) and the tab title — open any downloaded
`index (N).html` and the page tells you which entry it is.

Rule: the `BUILD` constant and this file move together — no bump without
an entry, no entry without a bump.

---

## p17 · Verdicts recorded + the harder case — current

**Problem/opportunity:** five first-run passes with one wrinkle would read
as barely tested; the kit's rule is to make a case harder — and verdicts
judged in chat needed to live in the product. **What changed:** the
human's verdicts and one-line notes are recorded and ship inside the file
(E-1 *Needs work* — "expected text overclaims ('each option within
band'); behavior correct, wording to fix"; E-2…E-5 *Pass*), with
localStorage persistence for later edits and a note field per row; and
**E-6 joined the table** — the same compensatory message as E-3 with the
counter seeded at 2, expecting the opposite behavior (hard stop, urgent
flag, immediate 18:00 delivery). The tier pair now tests the boundary in
both directions on screen. **Verified:** seeded verdicts present in a
fresh browser context; a verdict set before reload survives it; E-6 runs
REFUSED with "compensatory ask #3", flag delivered immediately inside
waking hours, stopped pre-model; its verdict left empty — it belongs to
the human.

## p16 · Eval case runner (+ build stamp)

**Problem/opportunity:** quality was only visible in chat transcripts; the
grade needs evidence on screen — and downloaded files were
indistinguishable (`index (7).html` says nothing about its contents).
**What changed:** a new **Evals** tab: five cases with Expected behavior
(verbatim from the PRD), an Actual column filled by really running each
case through the agent, and a Pass / Needs-work / Fail verdict picker that
only a human click can set. Plus the **build stamp** in the top bar and
tab title. **Verified:** Expected matches `eval_cases.csv` word for word;
E-1/E-5 actuals are specific summaries of real runs (budget numbers,
reason codes, flag delivery), not paraphrases. Two summarizer defects
fixed during verification (detached-DOM text lost line structure; CSS
uppercasing broke a case-sensitive match).

## p15 · First-run story

**Problem:** a stranger opening the file cold saw a working console with
no explanation, and no-key looked like a missing feature.
**What changed:** the empty state now explains the product in one line,
points to the demo chips, and — when no key is saved — states that
offline rules mode is fully functional, with guidance to Settings for
live runs. Thinking spinner during agent calls; no dead screens.
**Verified:** fresh browser context (the kit's incognito test) explains
itself; spinner sampled mid-run with an artificially delayed call.

## p14 · One-click demo chips

**Opportunity:** demos die while someone types.
**What changed:** the five eval cases as labeled chips (Happy path,
Missing data, Angry customer, Unusual input, Boundary — must refuse) at
the top of the case list; one click loads the case ready to run.
**Verified:** every chip selects its exact case; chip → run → approve
rehearsal under a second offline.

## p13 · Skin locked: Studio

**Decision, not a defect:** by the kit's pick-by-audience rule, a
client-facing consumer-health product demoed in daylight gets the light
Studio skin (user's choice from all three shown live).
**What changed:** `data-skin="studio"` locked; temporary switcher removed.
**Verified:** log text at the 13px token floor; status colors unchanged
(shared across skins).

## p12 · The gate gets teeth

**Problem:** after a sweep, the case list showed no outcomes (user
finding); the review buttons looked generic.
**What changed:** outcome badges on every case card (OK / REFUSED /
CLARIFY / OUT-OF-SCOPE) plus the human decision state (APPROVED / EDITED
/ ESCALATED / ACKNOWLEDGED); escalations visibly flagged in the list;
Approve/Escalate in the kit's approve/danger styles; the permanent
boundary sentence: *"Nothing is sent without human approval."*
**Verified:** all 16 cards badged after Run All; escalation flag appears
in the list.

## p11 · The five stages, labeled

**Problem:** the loop worked but a stranger couldn't follow it unaided.
**What changed:** the work area restructured as 1 INPUT → 2 CONTEXT →
3 DECISION → 4 OUTPUT → 5 REVIEW with the kit's stage circles; context
shown *before* the run (the viewer sees what the agent reads); migration
onto the kit's shipped component classes removed hand-rolled styles and
non-token colors. **Verified:** stages 1–2 pre-run, 3–5 post-run; full
regression green (sweep counts, persistence, gate).

## p10 · The console chrome (+ two regression fixes)

**Problem:** a working loop that looked like homework; plus two Section-A
regressions caught by the user's independent testing.
**What changed:** kit tokens inlined; top bar, clickable case cards, work
area, settings + run log rail. Fixes: the approve-log recorded "option 1"
instead of the real option (a citation-tag change had broken a regex —
now read from the computed card); Run All results vanished in the
single-work-area layout (per-case result cache; review states survive
case switching). **Verified:** sweep 7/2/1/6/0 intact; results persist
after the sweep; approve logs the actual option text.

## p09 · Run All (end of Section A)

**Opportunity:** one click to exercise the whole world.
**What changed:** Run All processes all 16 cases with progress and a
summary line. **Verified:** 7 OK · 2 REFUSED-ESCALATE · 1 out-of-scope ·
6 clarify · 0 errors — counts predicted from the seeded data before the
run, then matched.

## p08 · Citations, forced

**Problem:** trust requires showing sources; fabricated citations kill
demos. **What changed:** every output row carries tags naming the policy
sections and record ids it used (A1 on budget, A2/A3 on options, A4 on
bridge, A5 on strategy + the model's citation field). **Verified:** tags
render; cited section A1 spot-checked against the policy text.

## p07 · Human gate + run log

**Problem:** an agent that acts without a human click is the failure mode
the whole design exists to prevent. **What changed:** Approve / Edit /
Escalate under every output — nothing completes without one; a run log
records time, case, decision, human action; floor refusals auto-append a
COACH FLAG with real quiet-hours delivery (queued 23:00 → delivered
07:00 +1d). **Verified:** all four action paths land in the log with the
right contents.

## p06 · The boundary (the trust moment)

**Problem:** the cannot-do rules existed on paper; the demo needs them
enforced and visible — and the model must never be the last line.
**What changed:** deterministic pre-call screen (health, multi-day
report, below-floor demand, counters, third compensatory ask) — a stop
means **no model call happens at all**; the one-way rule (a live model
may add a stop, never clear one); visible REFUSED-ESCALATE with reason
codes; CLARIFY paths that ask instead of guessing. One fix from
verification: the compensatory nudge is now *enforced* as a template —
in live mode the model's own wording could have slipped through.
**Verified:** the full safety matrix green, including refusal holding on
repeat runs and the happy path not over-refusing.

## p05 · Labeled fields + deterministic card math

**Problem:** a wall of model text can't be judged in under a minute, and
model-authored numbers can't be trusted. **What changed:** defensive
parsing of the agent's labeled fields; all arithmetic (budget, ranking,
tolerance, day-end projections) computed in code from the embedded data —
the model classifies and phrases, it never does math. **Verified:** the
browser's D-1001 numbers match the Python prototype exactly (remaining
150 kcal / 35 g); imperfect day shows signed gaps + strategy; bad-key
path degrades readably.

## p04 · First live decision

**Opportunity:** the loop's birth — a real agent call per case.
**What changed:** Run button per case; direct Anthropic Messages API call
(key from localStorage only); raw labeled-field response on screen; and
beyond the kit's ask, a **no-key offline rules mode** — the design's "runs
correctly with the model off" claim as a working feature, not an error
page. **Verified:** context provably reaches the agent (real case data in
the response); errors readable, never silent.

## p03 · System prompt + settings

**Problem:** the agent needs its constitution, compiled from the Design
PRD — and key hygiene must be structural. **What changed:** SYSTEM_PROMPT
with role, context contract ("never invent macro numbers — the app
computes"), the verbatim cannot-do list, labeled output format, and
escalation triggers; settings panel storing the key in localStorage only.
**Verified:** key survives reload, never appears in the file; rules
verbatim.

## p02 · The skeleton

**What changed:** one self-contained `index.html`; all CSVs and policies
embedded as constants; plain list proving the world loaded and the joins
are right. **Verified:** 16 cases with correct linked context (Maya shows
"targets NOT STATED — capture path").

## p01 · The world (Gate 0 passed first)

**Problem:** no build starts on a blueprint that doesn't exist — and the
kit ships Northstar's world, not ours. **What changed:** PlateMate's
synthetic world in the kit's shape — 16 disruption cases, 2 clients,
7 plan meals, 18 state rows, 42 foods, 5 eval cases seeded into the data,
citable sectioned policies (A1–A7, S1–S7); Northstar files deleted.
Gate 0: all 8 blueprint checks passed against the approved
DISCOVERY.md/DESIGN.md. **Verified:** every eval case's records exist,
including the boundary case's silent-skipper state (counter 0, disclosure
only) and the seeded third-ask counter for the harder case held in
reserve.
