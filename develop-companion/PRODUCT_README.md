# PlateMate — macros made simple

A nutrition plan-adaptation agent for coached clients. When real life
disrupts the day — an off-plan snack, a surprise dinner, a meal that has
to be skipped — PlateMate recomputes the rest of the day into 2–3 ranked,
plan-compliant options with the math shown, and hands the decision back to
a human.

**Live demo:** open `index.html`, or visit the hosted link.
It is one self-contained file. No install, no build step, no server.

Built as the capstone for Product Faculty's Agentic AI course.

## What it does

One loop, end to end, as five labelled stages:

1. **Input** — the client's message, in their own words.
2. **Context** — the coach's plan, targets, safety counters, and the
   policy rules the agent reads. Shown *before* the run, so you can see
   what it knows.
3. **Decision** — status, reasons, and citations to the policy sections it
   used.
4. **Output** — the budget arithmetic, ranked options with honest signed
   gaps, a never-skip fallback, and one coaching line.
5. **Review** — approve, edit, or escalate. **Nothing is written without a
   human click.**

## How to run it

Download `index.html` and open it. That's the whole install.

**With no API key it runs on deterministic offline rules and is fully
functional** — every case runs, all arithmetic is exact. That is a designed
mode, not a degraded one.

**To run the live agent, bring your own Anthropic API key** and paste it
into the Settings panel. It is stored only in your browser's local storage
and is sent only to Anthropic's API. It never reaches this repository, any
server of ours, or anyone else — there is no backend here to send it to.

## Changing the model

The model is one line near the top of `index.html`:

```js
const MODEL = "claude-sonnet-4-5";
```

Change that string and reload. Nothing else in the app names a model, so
that is the whole edit.

If Anthropic retires the model, the app does not break: the call fails,
the run falls back to the offline rules, and the error names the model and
points at this line. The header chip tells you which model is in play —
before a run it says which one *will* be requested; after a successful run
it shows the exact version the API reported back.

## Two things worth knowing about the design

**The safety screen runs first, on the raw text, before any model call.**
A stop means no nutrition math ever happens. The model can *add* a stop the
keyword screen missed; it can never clear one. That asymmetry is the whole
safety architecture.

**The app does the arithmetic; the model only writes language.** Budgets,
ranking, and tolerance checks are computed in code from the embedded data.
An independently built Python implementation of the same design produces
identical numbers to the kilocalorie.

## What it deliberately does not do

It handles exactly one loop. It never creates plans, never edits a coach's
targets, never orders food. It runs the seeded cases only — there is no box
to type a new disruption into. Delivery to a coach is simulated. The
skipped-meals counter cannot yet tell intermittent fasting from punitive
skipping. Full list in the app's Evals tab, under Known limitations.

## Data

**Everything here is synthetic.** Two invented client personas, invented
plans, invented messages. No real people, no real health data, anywhere.

## Tabs

- **Console** — the loop, case by case.
- **Evals** — six test cases with expected vs actual behaviour, human
  verdicts, the one improvement made after testing, the known limits, and
  an unseen-phrasing safety probe.
- **Memory** — everything the app remembers, everything it refuses to
  remember, and a button that genuinely forgets.

Build history: [`CHANGELOG.md`](CHANGELOG.md) — one entry per build, what
problem it solved and how it was verified.
