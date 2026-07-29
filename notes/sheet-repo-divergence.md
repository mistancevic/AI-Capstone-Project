# Sheet ↔ repo divergence — Discovery and Design rows

Found 2026-07-29 while adding copy-paste formatting to `DISCOVERY.md` and
`DESIGN.md`; updated the same day once the sheet's cell notes were
supplied. **Nothing has been reconciled.** This note records what differs
so the decision is made deliberately, not by an accidental paste.

Method: every Student Response cell (sheet rows 9–28) compared against the
matching answer in the repo, whitespace-normalised and with markdown `**`
emphasis ignored. Develop rows 29–36 were checked at the same time and are
**in sync** — this note concerns Discovery and Design only.

Of 20 rows, 10 match exactly and 10 differ. Of the 10 that differ, **three
are explained** (deliberate: the cell holds the as-reviewed answer, a cell
note records the revision), **three are trivial** (≤60 characters), and
**four need a decision**.

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

## Still unexplained — a decision is needed

| Row | Theme | Verdict | Extra text |
|---|---|---|---|
| **20** | Target workflow | repo has more | repo +773 |
| **23** | Tools or simulated tools | both differ | sheet +368, repo +472 |
| **25** | Output format | **SHEET has more** | sheet +346 |
| **26** | Escalation rules | both differ | sheet +670, repo +696 |

**Row 25 is the one to look at first.** The sheet carries roughly 346
characters the repo does not: *Agent tone* (warm, plain language; the math
is shown but never lectured) and *Banned agent moves* (no guilt framing —
"to make up for", "you earned it" — no praising a skipped meal, no fake
cheerfulness, no lecturing). That is real design content missing from
`DESIGN.md`, and pasting the repo version over that cell would destroy it.

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
