# Sheet ↔ repo divergence — Discovery and Design rows

Found 2026-07-29, while adding copy-paste formatting to `DISCOVERY.md` and
`DESIGN.md`. **Nothing has been reconciled.** This note records what
differs so the decision is made deliberately, not by an accidental paste.

Method: every Student Response cell (sheet rows 9–28) compared against the
matching answer in the repo, whitespace-normalised and with markdown `**`
emphasis ignored. Develop rows 29–36 were checked at the same time and are
**in sync** — this note concerns Discovery and Design only.

## Summary

11 of 20 rows match. 9 differ, and they differ in **both directions** —
neither artifact is a superset of the other.

| Row | Theme | Verdict | Extra text |
|---|---|---|---|
| 9–14 | User → Agent opportunity | in sync | |
| **15** | Synthetic data plan | **repo has more** | repo +372, sheet +52 |
| **16** | Human boundary | **repo has more** | repo +338 |
| 17 | Success metric | in sync | |
| **18** | Initial demo idea | **both differ** | sheet +529, repo +608 |
| 19 | Agent role | in sync | |
| **20** | Target workflow | **repo has more** | repo +773 |
| 21 | Agent loop | in sync | |
| **22** | Inputs and context | trivial | 2 chars each way |
| **23** | Tools | **both differ** | sheet +368, repo +472 |
| **24** | Memory decision | trivial | repo +2 |
| **25** | Output format | **SHEET has more** | sheet +346 |
| **26** | Escalation rules | **both differ** | sheet +670, repo +696 |
| 27 | Human approval point | in sync | |
| **28** | Initial eval plan | trivial | repo +60 |

## The two that matter most

**Row 16 (Human boundary) — the repo carries Moe's requested refinement,
the sheet does not.** The repo adds: *"It never recommends eating less,
skipping a meal, or otherwise restricting intake to 'make up' for an
off-plan meal; an off-plan day is handled by the multi-day averaging
principle, never by compensatory restriction,"* plus a pointer that the
refusal-language patterns and the hard-stop-vs-nudge line are specified in
Design. That is the direct answer to the single strongest thing Moe asked
for in the Discovery review — *"sharpen the disordered-eating boundary…
write that rule explicitly."* Row 15 carries the matching eval-set half
(the compensatory-restriction case beside the dizziness case).

If the sheet is what gets graded, the graded artifact currently does not
contain the response to the faculty's main Discovery request.

**Row 25 (Output format) — the sheet carries a block the repo lost.**
Roughly 346 characters covering *Agent tone* (warm, plain language; the
math is shown but never lectured) and *Banned agent moves* (no guilt
framing — "to make up for", "you earned it" — no praising a skipped meal,
no fake cheerfulness, no lecturing). This is real design content that
`DESIGN.md` does not have; it must not be lost by pasting the repo version
over it.

## Probable cause

The repo files were edited after the sheet was filled — Discovery's
post-feedback refinements (rows 15, 16) went into the `.md` and never back
into the cells — while some sheet cells were edited directly and never
came back to the repo (row 25). No single sync direction is correct.

## Decision needed

Per row, one of: keep the sheet, take the repo, or merge both. Rows 22, 24
and 28 are trivial (a couple of characters) and can follow whatever is
decided for the rest. The Develop rows need no action.

Until a decision is made, **the sheet is authoritative** for Discovery and
Design: it is what was reviewed and approved.
