# Sheet ↔ repo divergence — Discovery and Design rows

Found 2026-07-29 while adding copy-paste formatting to `DISCOVERY.md` and
`DESIGN.md`; updated the same day once the sheet's cell notes were
supplied. **All diverging rows are now settled** — see each section for how. This note records what differed and how each case was decided, so the
repo and the sheet can stay deliberately different where that is correct.

Method: every Student Response cell (sheet rows 9–28) compared against the
matching answer in the repo, whitespace-normalised and with markdown `**`
emphasis ignored. Develop rows 29–36 were checked at the same time and are
**in sync** — this note concerns Discovery and Design only.

Of 20 rows, 10 match exactly and 10 differ. Of the 10 that differ, **three
are explained** (deliberate: the cell holds the as-reviewed answer, a cell
note records the revision), **three are trivial** (≤60 characters), and
**four needed a decision — one now resolved (row 25), three open: 20, 23, 26**.

## Explained — revision recorded as a sheet cell note

After the Product Faculty review, the decision was to leave the reviewed
answer in the cell and record the revision as a note, so the reviewed text
stays intact. The repo `.md` carries the revised wording. That is why
these three differ, and it is intentional.

**The notes below exist only inside the spreadsheet.** The Drive API does
not return cell notes at all — not as content, not as comments — so this
file is their only durable copy. Verbatim:

> **F15** — Revised after Product Faculty review (Moe): added a seeded
> compensatory-restriction safety case ("should I eat less to make up for
> it?") alongside the dizziness case, with refuse-and-coach as the known
> good answer.

> **F16** — Revised after Product Faculty review (Moe): added the explicit
> rule that the app never recommends eating less or skipping to compensate
> for an off-plan meal — off-plan days are handled by multi-day averaging,
> never restriction. Refusal language and hard-stop vs soft-nudge tiers are
> specified in the Design section (row 26).

> **F18** — Revised after Product Faculty review (Moe): demo trimmed to the
> core orchestrator-to-nutrition-agent recompute; sleep consult is
> conditional on the core loop being solid; stubbed agents removed from the
> demo scope; both safety cases (dizziness, compensatory restriction)
> shown.

> **F19** — Design approved by Moe Ali (Product Faculty), Jul 2026 — safety
> architecture praised, no design changes requested. Build-scope caution
> carried to Develop: Milestone 1 = Case 1 (happy path) + Case 7 (hard
> stop) end to end, before the tier pair. "Prove the loop first, then earn
> the complexity." Full feedback in DESIGN.md.

(F19's row matches the repo exactly; its note is provenance, not a
revision record.)

## Settled — how each diverging row was resolved

Re-examined 2026-07-29 after a challenge about whether the repo text had
been paraphrased rather than copied. Two checks settle it.

**Check 1 — was the repo rewritten?** Every Design answer in `DESIGN.md`
today is byte-identical to the first Design commit (`203a95c`), with
exactly two exceptions: row 25 (the block pulled in from the sheet today)
and row 22 (the Maja → Maya rename, requested). Nothing was reworded,
expanded, or invented afterwards.

**Check 2 — are the remaining differences real?** Comparing word bags with
all formatting stripped (pipes, arrows, list markers, punctuation):

| Row | Result |
|---|---|
| **20** | **REAL gap — 129 words exist only in the repo** |
| 23 | same content; the repo renders a markdown table, the sheet flattens it to prose |
| 26 | same content; same table-vs-prose difference |
| 28 | identical content, formatting only |
| 25 | resolved — pulled into `DESIGN.md`, now matching |

So rows 23, 26 and 28 were never a divergence. A markdown table cannot be
pasted into a spreadsheet cell, so it was flattened into arrow notation
when filling the sheet — `| tool | type | check |` became
`tool — type — check`. Same facts, different rendering. No action.

### Row 20 — resolved as a cell note, not cell text

The sheet's Target workflow cell stops at step 8; the repo carries a
closing out-of-scope paragraph after it. Direction confirmed: 129 words
exist only in the repo, none only in the sheet, so F20 is a clean prefix
rather than an altered version.

**Decision (2026-07-29): it stays out of the cell.** F20 asks *"How does
the workflow change when the agent is introduced? List the future process
as text steps."* An out-of-scope list does not answer that question, and
padding the cell with it would answer something nobody asked. The content
is design record, not process steps — so it lives in `DESIGN.md` (full
text, four labelled paragraphs) and in a cell note for provenance.

Note prepared for F20:

> **F20** — Scope boundary (context, not part of the answer): the daily
> watch (clock-triggered counter advancement, one gentle check-in after
> three silent days, coach flagged at the same thresholds) and
> client-declared pause mode are designed but deliberately out of demo
> scope. The hard stop fires on either channel independently, so if a
> tracked counter and a self-report both fire the coach is flagged twice —
> deduplication is future work and over-flagging on this signal errs safe.
> In demo scope: only the seeded skipped-meals counter, feeding the step-2
> safety screen. Full text in DESIGN.md.

This is the origin of Develop limits 3 and 6, which is why it is worth
recording somewhere rather than dropping.

**With this, every diverging row is settled.** The repo is the fuller
design record by design; the sheet answers the questions as asked.

## Trivial

Rows 22 (Inputs and context) and 24 (Memory decision) differ by two
characters; row 28 (Initial eval plan) by sixty. Follow whatever is
decided for the rest.

## In sync

Rows 9, 10, 11, 12, 13, 14, 17, 19, 21, 27 — and all Develop rows, 29–36.

## The open question about notes

The cell notes above are invisible to any reader who does not hover the
cell, and invisible to tooling entirely. That is the same problem that put
the build-order directive out of sight in F29, where the resolution was to
move it into the cell text. Rows 15, 16 and 18 are a different case — the
argument for leaving the reviewed answer untouched is real — but the
consequence is that a reviewer reading F16 today sees the pre-feedback
answer without the compensatory-restriction rule, which is the single
strongest thing the Discovery review asked for.

Worth deciding explicitly: leave as-is, or put the revised answer in the
cell with a one-line "revised after PF review" prefix so the improvement is
visible without hovering.
