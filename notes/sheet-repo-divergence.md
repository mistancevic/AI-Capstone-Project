# Sheet ↔ repo divergence — Discovery and Design rows

Found 2026-07-29 while adding copy-paste formatting to `DISCOVERY.md` and
`DESIGN.md`; updated the same day once the sheet's cell notes were
supplied. **Row 25 has been reconciled; nothing else has.** This note records what differs
so the decision is made deliberately, not by an accidental paste.

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

## Open — one real gap (rows 23, 26, 28 cleared; 25 resolved)

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

### Row 20 — the one genuine gap

The sheet's Target workflow cell is missing the closing paragraph the repo
carries, roughly 129 words:

> **Designed but out of demo scope (future work, labeled):** a separate
> clock-triggered daily watch that advances the skipped-days and off-target
> counters, sends one gentle check-in after three silent days, and flags
> the coach at the same thresholds; and a client-declared pause for life
> events ("away until Sunday") that suspends logging expectations for a
> bounded window, auto-resumes, appears in the coach's digest, and never
> mutes the safety screen. The hard stop fires on either channel
> independently — tracked counter or the client's own words; if both fire,
> the coach receives the flag twice (deduplication is future work;
> over-flagging on this signal errs safe). The only watch element in demo
> scope is the seeded skipped-meals counter feeding the step-2 safety
> screen.

This is scope-boundary content: what is designed but deliberately not
built, and why the coach can be flagged twice. It is the Design-phase
statement of two things that later became Develop limits 3 and 6, and it
answers the demo-scope half of the faculty's Discovery directive. A
reviewer reading only the sheet does not see it.

**Decision needed:** paste it into F20, or leave the sheet as reviewed.
Unlike rows 15/16/18 there is no cell note covering this one — the
omission looks accidental rather than chosen.

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
