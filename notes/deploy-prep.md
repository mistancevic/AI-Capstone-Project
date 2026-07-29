# Deploy Phase — Preparation (final module: agentic AI, mapped onto PlateMate)

Same drill as `develop-prep.md`: map the module's frameworks onto where
PlateMate already answers them, then draft the capstone-sheet Deploy
answers. Deploy is a paper phase for us (readiness, risk, operations,
monitoring, rollout) — no build gate needed.

## The module's frameworks vs. PlateMate (the short version)

| Module concept | PlateMate position |
|---|---|
| Three agent characteristics (autonomy, goal-oriented, environmental) | Autonomy deliberately capped at advise-only (the spectrum point is a *choice*, not a limitation); goal = the no-skip rate; environment = client messages + tracked state |
| Sense / plan / act | Ours is observe / decide / act / **check** — the fourth step (the gate before the card renders) is the design's addition, and the module's challenge list is why it exists |
| Architecture stack (foundation / reasoning / orchestration) | Foundation layer: exactly two LLM calls. Reasoning layer: deterministic fixed-order triage — deliberately NOT model-driven. Tooling: 12 tools, control flow in code, the model never triggers a tool |
| Build approach (scratch / framework / hybrid) | From scratch, justified by the module's own criterion: safety-critical control. The whole app is small because the intelligence is confined |
| Orchestration pattern | Single orchestrator routing to one specialist (nutrition) with a conditional consult (sleep) — the module's pattern 3 in miniature; true multi-agent is parked |
| Hallucination fixes (grounding, thresholds, cross-validation) | Numbers are computed, not generated (structural faithfulness); required-slot gating instead of model confidence; the one-way LLM safety assist IS asymmetric cross-validation |
| Task-looping fixes (termination, state, planning) | Single-pass runs; clarify-once-then-presets is a termination criterion; counters are state tracking |
| Reliability fixes (fallbacks, structured data, modularity) | Model-off fallbacks on both LLM calls; structured Situation objects between steps (the module's "JSON not freeform" rule); safety screen independent of everything downstream |

**When-to-build framework (5 dimensions), verdict run honestly:** task
complexity — the *disruption* is open-ended (agent justified for parse +
context), the *math* is not (kept deterministic; the module's "don't
build" rule applied inside the product); performance — safety paths need
deterministic behavior, so they got code, not model; resources — two
small calls, trivially justified; environment — health-adjacent = high
risk, hence floor + human gates (the module's caution applied as
architecture); scale — B2B2C roster model scales by coach, not by ad
spend. Net: PlateMate is the module's decision framework *applied inside
one product* — agentic where open-endedness demands it, automated where
predictability demands it.

**OpenClaw lessons vs. PlateMate:** (1) guardrails before capabilities —
ours are day-one architecture (floor, banned language, escalation), not
bolt-ons; (2) permission scoping — one write, behind the client's tap;
the model can never trigger an action; (3) human-in-the-loop first, then
earn autonomy — the package/tier roadmap in the coach agreement is
exactly this progression; (4) **chat as the interface** — OpenClaw's
adoption exploded because it met users inside WhatsApp/Slack. Disruption
reports are already chat-shaped one-liners; delivering PlateMate inside
the chat apps clients already use is a real adoption lever → parked
(see parked-ideas.md; privacy review required first — disordered-eating
disclosures over third-party chat platforms is a serious question).

---

## Capstone-sheet Deploy answers (draft, paste-ready)

**Pilot readiness — would you pilot this? What must be true first?**

> Yes, as a supervised invite-only pilot inside the founder's own coaching
> practice. Before launch, five things must be true: the coach-side
> interviews confirm real demand for the escalation loop (today it is a
> researched hypothesis, not a validated fact); the peer survey calibrates
> the pain magnitudes and willingness to pay; the two language-model calls
> run against a real model with the seven-case evaluation green in
> model-on mode (it is currently proven in model-off mode); the stop and
> nudge wording is reviewed by a clinically qualified professional,
> because the disordered-eating boundary must not rest on a product
> team's judgment alone; and the daily watch and pause mode are built,
> since counters that only exist as seeded data cannot protect anyone
> between sessions.

**Privacy and safety risks — what could go wrong?**

> The data is health-adjacent and the worst failure is not a wrong number,
> it is mishandling a vulnerable person: a missed disordered-eating signal,
> or advice that reads as endorsing restriction. Mitigations are
> architectural — a deterministic safety floor the model cannot bypass, a
> language model that can only add stops and never clear them, banned
> compensation language enforced in code with a pre-authored fallback, and
> a coach escalation with quiet hours delaying notification but never
> protection. Privacy: raw disruption messages are deleted after each run,
> only counters persist, the triggering message is shared with the coach
> exactly once per the signed agreement, and no behavioral profile is ever
> built. Misuse: the model cannot trigger tools, the only write sits
> behind the client's confirmation, and jailbreak attempts are a tested
> evaluation case — a demand for a below-baseline day produces a refusal
> under any phrasing. Trust and compliance: the app is positioned as
> adaptation of a coach-prescribed plan, never as medical advice; anything
> medical is declined and escalated. Remaining risks to manage in pilot:
> false-positive stops eroding trust (monitored), and clinical review of
> all safety wording before any real client sees it.

**Human operating model — who owns decisions?**

> Three humans, three ownerships. The client owns every consequential
> action: nothing is logged without their one-tap confirmation, and they
> see every flag the coach sees, including its delivery time. The coach
> owns the plan, the adaptation rules, and the escalation contract
> (channel, quiet hours, flag scope, package tier), receives every safety
> flag, and owns every escalated case end to end — the app never resolves
> a safety case itself. The operator (founder during pilot) owns the
> system: reviews evaluation runs before every release, audits flag logs
> and screen-failure counts weekly, and owns the decision to widen or halt
> the pilot. The app owns nothing with consequences: it advises, computes,
> and stops — the stops are code, and every ambiguity routes to a human.

**Quality monitoring — what would you watch after launch?**

> The evaluation suite becomes a regression gate: all seven cases re-run
> on every change. In production, eight signals, reviewed weekly during
> pilot: the no-skip rate (the north-star metric); escalation precision
> (what share of flags the coach judges warranted); the false-stop rate
> (safety screen stopping innocent requests — our first evaluation run
> proved over-refusal is the likelier failure, so it gets its own metric);
> the banned-language replacement rate (a rise means model drift); the
> clarify rate (a rise means parsing degradation); option acceptance rate
> (a fall means ranking drift); counter distributions across the roster
> (sudden shifts mean detection drift); and coach-reported misses — cases
> the coach believes should have been flagged and weren't, the one signal
> no automatic metric can produce.

**User feedback plan — how do you learn after launch?**

> Three channels with different jobs. In-app: one tap on every card —
> did this help, yes or no — plus which option was confirmed, rejected,
> or edited; low friction because the segment already resents logging.
> The coach: a weekly pilot debrief against their roster — coaches
> surface what clients never type, and their judgment of each flag
> (warranted, tone, timing) is collected on every escalation. The audit:
> every hard stop reviewed jointly with the coach after the fact.
> Prioritization rule: safety findings are fixed immediately and
> re-evaluated before the next release; adherence findings feed the
> no-skip metric; feature requests go to the parked list unless they
> unblock the pilot's success gates.

**Pilot plan — smallest safe launch?**

> One coach (the founder), three to five consenting clients from the
> existing practice, invite-only, four weeks. Preconditions: daily watch
> and pause mode built, model-on evaluation green, clinical review of
> safety wording complete, coach agreement signed with a real escalation
> channel and quiet hours. Success gates to widen: zero missed
> escalations in the coach's judgment, zero safety incidents, and a
> visible no-skip improvement against each client's own baseline weeks.
> Next ring, only after all three gates: two to three external coaches
> recruited through the key-informant interviews, each with a small
> roster slice — testing the real hypothesis, that a coach who did not
> build the product will trust it with their clients.

**4-minute video outline**

> 0:00–0:30, intro and the person: a coached client whose plan is good
> and whose day is not — the meeting that ate lunch, the ice cream that
> happened. 0:30–1:00, the problem with evidence: when the day breaks,
> the modal reaction is the what-the-hell binge, not a shrug — one
> off-plan lunch becomes an abandoned day; trackers log the past and
> around 86 percent of diet-app users abandon them. 1:00–1:30, the
> solution in one sentence and the safety spine: the first safe action
> after a disruption — two or three plan-compliant options with the math
> shown, advise-only, deterministic floor, a model that can only add
> stops, the coach in the loop. 1:30–2:45, the demo, two contrasting
> minutes: the happy path (disruption typed, card with budget math,
> one-tap confirm) and the 23:00 boundary case (jailbreak plus health
> signal → no math, pre-authored stop, get-help-now, urgent flag
> delivered at 07:00) — same app, opposite behaviors, decided by code.
> 2:45–3:20, evaluation rigor: seven cases including the tier pair and
> the jailbreak; three runs to green; the failures found were
> over-refusal, and fixing them without touching a single safety
> threshold is the story; everything passes with the model switched off.
> 3:20–4:00, impact and launch: the no-skip rate as the north-star
> metric, coach-led distribution, the smallest safe pilot, and what is
> deliberately parked.

---

## QQRT axis review (future-fit check, per user request)

All four axes hold for future versions; each has a current home and a
parked home — no axis is orphaned:

- **Quantity** — v1's core (budget math, gram targets). Stays the coach's
  language forever; never adjusted by the app.
- **Quality** — completed with bioavailability; parked home:
  bioavailability-aware ranking + coach-side plan authoring (DIAAS desk
  pass first).
- **Regularity** — the product's true axis: no-skip rate, counters,
  multi-day averaging today; the daily watch, digests, and the survey's
  frequency matrix instrument it tomorrow.
- **Timing** — minimal in v1 (clock, quiet hours, late-meal note); parked
  home: the QQRT-structured sleep agent and calendar integration
  (chrononutrition desk pass before any claim).

## Submission requirements — from the tracker sheet (recorded 2026-07-29)

The tracker is a **separate sheet from the PRD**, and it changes one thing
we had been assuming. The PRD forbids link-outs; the tracker **asks for
links**. Columns, with the course's suggested timing:

| Col | Asks for | Suggested |
|---|---|---|
| H | Discovery section complete in your PRD? | Week 3 |
| I | Design section complete in your PRD? | Week 4 |
| J | Develop section complete in your PRD? | Week 6 |
| K | Deploy section complete in your PRD? | Week 8 |
| L | **Paste your prototype link** | Week 8 |
| M | **Paste your 4-minute video link** | Week 8 |
| N | Paste slides, data, repo, or supporting materials | Week 8 |
| O | Will you attend Demo Day? | Demo Day |

### What this settles

**A prototype link is required, and it is a Week 8 / Deploy deliverable.**
That is the concrete target the Develop kit's no-publishing rule was
holding the line for: hosting is not forbidden, it is *scheduled*. The
rule lifts when the Deploy companion is extracted, and column L is what it
lifts for.

**The PRD's no-link-out rule is not in tension with this.** The answers
stay self-contained — a reviewer must understand the loop from row 36
alone. The tracker is where the artifacts get attached. Two different
questions: *did you explain it* vs *can we see it*.

**Column N is the repo.** `mistancevic/AI-Capstone-Project` is public, so
it can be pasted as supporting materials — the build history in
`develop-companion/CHANGELOG.md` (p01–p25, one entry per build with what
changed and how it was verified) is the strongest thing in there for a
reviewer who wants evidence of process.

### Consequences to plan for in Deploy

1. **Hosting the one-file prototype.** It is a single self-contained
   `index.html` with no build step, so any static host serves it. The open
   question is the API key: the app runs fully on offline rules with no
   key, which is the right default for a public link — a hosted demo must
   never ship a key, and the settings field stays the only way to add one.
2. **The 4-minute video** (col M) is the vehicle for showing the prototype
   running — the walkthrough already drafted in PRD row 36 is its script:
   happy path, boundary refusal, evals scoreboard, memory panel.
3. **Demo Day attendance** (col O) is a separate decision, not a
   deliverable.

Nothing here is actionable until the Deploy guide and companion arrive.
