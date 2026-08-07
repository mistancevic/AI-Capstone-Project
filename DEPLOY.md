# PlateMate — Deploy PRD

Agentic AI Capstone, Deploy phase record. Built with the official Deploy
companion kit (D00-D10, run in order). The prototype is live at
https://mistancevic.github.io/platemate - published from
`develop-companion/index.html`, which stays the source of truth; the
`platemate` repository is a publish target only. Build history:
`develop-companion/CHANGELOG.md`.

Status: **rows 37-43 written (D08 complete), video outline drafted (D09).
Recording and submission outstanding.**

The rows below are paste-ready: plain text, self-contained, no link-outs,
no markdown markers that would show up literally in a sheet cell.


### 37. Activity: Readiness | Theme: Go / no-go view | Topic: Pilot readiness

**Key question(s):** Would you pilot this? What still needs to be true before launch?

```text
Yes - as a supervised, invite-only pilot inside my own coaching practice: three clients, four weeks. Small enough that the coach knows every case personally; long enough that a rolling-week counter and an adherence pattern mean something.

Who is in scope: clients already on a coach-authored plan on file, since with no plan there is nothing to adapt and the app would be inventing targets. Explicitly excluded: anyone with a disclosed eating-disorder history or under current clinical care, under-18s, pregnancy or any medical condition with dietary implications, and any client whose coach cannot be reached inside the escalation window they agreed to - an urgent flag with nobody at the other end is worse than no flag. The exclusion I hold hardest is the first: the safety screening was built for that cohort, and a pilot is exactly the wrong place to find out how well it works on them.

Reversible: the switch is the coach telling three people to stop - no deploy, no feature flag, and honest about the scale I am actually at. The fallback is what they do today: message the coach and wait, a channel the app never replaced. Any client can stop without explaining themselves. Any one of a missed escalation, an unapproved action, a below-baseline output, or a client saying the app made a bad day worse pauses it - one, not a threshold - then pause → fall back → diagnose against the evals → return smaller.

Success, defined now. At three clients I will see perhaps 20–40 disrupted days, which is too few for rates: "82% precision" out of six flags is a number pretending to be evidence. So the bar is counted events and human judgement. Must hold: zero missed escalations, zero unapproved actions, zero below-baseline outputs under any phrasing. What I am buying: the coach's judgement of every flag (warranted, tone, timing), and at least one real disrupted day per client that ends in a chosen meal instead of a skip. And the honest one, asked at week four, separately of all four people: do you want to keep using it?

The rollout is phased by capability, not by headcount. Phase 1 - this pilot - runs the deterministic path: the budget arithmetic, the ranked options, the safety screening and every stop, with no model call. Phase 2 turns on the model leg - the situation classification, the one coaching sentence, and the second safety net that catches phrasings the keyword rules miss - once it has earned it. Both phases are the same product; phase 2 has more of it switched on. The principle is the one the pilot standard states: autonomy is earned with evidence, never assumed, and the model leg has one outstanding finding against it. The privacy row gives the second reason for the same sequence.

What must be true before phase 1 starts. The safety counters must be written at runtime, not only read - policy S2c tiers the compensatory-ask response by a rolling-week counter, and the prototype reads that counter but never increments it. The tiering is proven by two seeded cases sitting either side of the threshold, which demonstrates the boundary without producing it; on seeded counters a client's third ask in a week would reach them as a first. The daily watch and pause mode are designed and not runtime for the same reason. The stop and nudge wording must be reviewed by a clinically qualified professional, because a disordered-eating boundary must not rest on a product team's judgement alone. And the coach-side interviews must confirm real demand for the escalation loop, which is currently a researched hypothesis and not a validated fact.

What must be true before phase 2 reaches a real client. All six eval cases green in model-on mode. That is no longer a hypothetical: running them model-on on 2026-08-06 produced five matches and one divergence - the live model escalated E-3, a first compensatory ask, which policy S2c says must continue with food and a nudge. Judged Needs work. (The design specifies two model calls, a parse and the coaching line; the build makes one call that returns both, plus the status, the reasoning and the citations.)
```

### 38. Activity: Risk | Theme: Privacy and safety risks | Topic: What could go wrong

**Key question(s):** What data, compliance, trust, or misuse risks must be managed?

```text
What data enters: the coach's plan and daily targets, the client's restrictions and preferences, two safety counters as counts, and the client's own words about a disrupted day. In the capstone it is synthetic end to end - no real person's data has ever been through this.

Where it goes. With the model leg on, every run sends the full client record, the plan, the counters and the raw message from the browser to a third-party model provider. "Raw messages are deleted after each run" is true, and it is a statement about my storage, not about that transfer - and the messages most worth protecting are exactly the ones the model leg exists to catch. So the pilot is phase 1: the deterministic path only, no model call, and nothing leaves the device. That costs the leg that caught 10 of 10 unseen phrasings where the code caught 0 - a real cost, carried deliberately, and the same sequence also buys something, because verification against a live model showed it over-escalating a case the deterministic path tiers correctly. Two independent reasons for one order of work. The compensating controls in phase 1 are its size (three clients the coach speaks to daily), the exclusion list, and the fact that every flag reaches a human who knows them. Phase 2 - the model leg with real clients - additionally requires a key-holding backend, a data-processing agreement, explicit per-client consent naming what leaves their device and to whom, and, for any EU client, a formal review under special-category health data rules. Named prerequisites, not later niceties.

What a leak would expose: the browser holds confirmed choices and eval state, not raw messages - those are dropped by design. If a key were ever handed to a client, the leak would be the credential itself and its billing. That is the second reason phase 1 makes no model call.

The worst failure is not a wrong number - it is mishandling a vulnerable person: a missed disordered-eating signal, or advice that reads as endorsing restriction. The mitigations are architectural, not promises. Deterministic safety screening the model cannot bypass, because a stop happens before any model call. A one-way rule: the model may add a stop, never clear one. Banned compensation language enforced in code with a pre-authored fallback sentence. Coach escalation where quiet hours delay notification but never protection. And a human confirm gate: nothing is logged without the client's tap.

Misuse: the model triggers no tools, the only write sits behind the client's confirmation, and a jailbreak demand for a below-baseline day is a tested case that refuses under any phrasing. Positioning: adaptation of a coach-prescribed plan, never medical advice - anything medical is declined and escalated.

Remaining risks I would manage during the pilot: false-positive stops eroding trust - I have measured the catch rate and have no false-positive rate beyond one observed case, which is half a safety claim; and the stop and nudge wording still needs review by a clinically qualified professional before a real client reads it.
```

### 39. Activity: Operations | Theme: Human operating model | Topic: Who owns decisions

**Key question(s):** Who reviews agent output, handles escalations, and owns final decisions?

```text
The product's authority model is three ownerships. The client owns every consequential action: nothing is logged without their tap, and they see every flag their coach sees, including its delivery time. The coach owns the plan, the adaptation rules and the escalation contract - channel, quiet hours, flag scope - receives every safety flag, and owns every escalated case end to end; the app never resolves a safety case itself. The app owns nothing with consequences: it advises, computes and stops. The stops are code, and every ambiguity routes to a human.

In this pilot, all three operating roles are me. I am the coach, so I am the operator who watches the queue daily, the escalation owner who takes the hard cases, and the decision owner who can change prompts, policies and scope. That concentration is the biggest governance risk in the plan, and it is worth naming precisely: an urgent flag fires, I judge it a false positive, and because I also own the policy the cheapest fix is to loosen the rule. Nobody is positioned to tell me I should not have. Over four weeks and a handful of flags, a safety boundary can erode one reasonable decision at a time, and every step looks defensible from the inside.

So the safety policy is frozen for the whole pilot. No change to S1–S7 wording or thresholds for four weeks, however many false positives I judge. Every flag I disagree with becomes a logged note rather than an edit, and those notes are the evidence for a change after the pilot, reviewed with the clinically qualified professional who signs off the stop and nudge wording before it starts. Engaging that person is a precondition, not a courtesy: without them the freeze has no second pair of eyes behind it, and the concentration above is unmitigated. Adaptation-side changes - ranking, option wording, the coaching line - stay mine to make freely. Safety is the frozen half.

Cover is one person, and I say so to the three clients before they start. Flags reach me inside a stated window; outside it the app queues them and delivers at window-open, marked urgent, exactly as the quiet-hours rule already does. This is a supervised pilot, not a monitored service, and every stop already carries get-help-now guidance naming a medical professional rather than me - because I am not an emergency channel and the app says so on screen. The readiness row excludes any client whose coach cannot be reached inside the window they agreed to; that standard applies to me as much as to anyone.

On "every output reviewed at first": it cannot be reviewed before the client acts, because the client is standing in a shop deciding what to eat. So observation is after the fact and daily - I read every run every day for four weeks - and the gate that protects the moment itself is the client's own confirmation. Autonomy is not being granted here; there is none to grant. The app never acts, it only proposes.
```

### 40. Activity: Monitoring | Theme: Quality monitoring | Topic: After launch checks

**Key question(s):** What would you monitor after launch to catch drift, failures, or bad outcomes?

```text
Three layers, at three different scales - because a metric needs a denominator, and at three clients I do not have one. Twenty to forty disrupted days will not support a rate; a "clarify rate" over thirty runs moves three points when one person mistypes once. So during the pilot I read rather than chart.

Every change, before it ships: the regression gate. This is the layer that already exists and it is the strongest of the three. A regression suite - 159 checks at submission - runs against every build and again against the published file after every deploy, covering the safety screening, the budget arithmetic, the one-way rule, the banned-language screen, key hygiene and every claim the evidence surface makes about itself. On top of it, the app compares each eval re-run against the first-check result: an identical result says so, a divergent one dims the old verdict, says the previous judgement does not cover the new result, and puts it back in front of a human. Drift detection built into the evidence, not bolted beside it.

Every day of the pilot: four counts and one automated alarm. Flags raised, with my judgement of each - warranted, tone, timing. Stops that fired, and whether the client agreed they should have. Runs that ended in a chosen meal rather than a skip. And any case where the app said something I would not have said. The automated one is counter integrity: every compensatory ask and skipped day increments exactly once and survives a session, alarmed in both directions - an ask that fails to count, so a client's third ask arrives as a first, and an event counted twice through the known flag-deduplication gap.

At roster scale, once denominators exist: no-skip rate as the north star, escalation precision, false-stop rate, banned-language replacement rate as a model-drift signal, clarify rate as a parsing-degradation signal, option acceptance as a ranking-drift signal, counter distributions across the roster, and coach-reported misses - the one signal no automatic metric can produce.

The first false positive, already observed. The six eval cases had only ever been proven with the model off. Run model-on on 2026-08-06 against claude-sonnet-4-5-20250929: five matched the first check and one diverged. The live model refused a first compensatory ask - which policy S2c says must continue with food and a templated nudge - citing policy S3 while stating in its own reasoning that "skipped_days counter is currently 0". It named the section, checked the threshold, said the threshold was not met, and escalated anyway. Judged Needs work by the human; both judgements now sit on the row, dated, for anyone who opens the live link.

Nothing unsafe was emitted. No number was invented, no card was built, nothing was logged - the app labelled it a model-added stop under the one-way rule and the client still received the safe default. But a client who reached out on a bad day was told to eat as written and wait for their coach. Over-refusal is the failure this product is built against, so it is a counted event rather than a hypothesis - and it is the argument for keeping thresholds in code, in the model's own words.

The number I do not have. I have measured the safety screening's catch rate against phrasings it had never seen - ten dangerous messages, ten walked straight past the keyword rules - and I have never measured its false-positive rate. One observed case is not a rate. There is no benign-message counterpart to that test. A catch rate without a false-positive rate is half a safety claim, so during the pilot I would be watching for over-refusal by hand, with no baseline to compare against, and building that counterpart set is the first monitoring work after the pilot.
```

### 41. Activity: Feedback | Theme: User feedback plan | Topic: How you learn after launch

**Key question(s):** How would you collect feedback and decide what to improve next?

```text
At three clients, I do not need an instrument. I am their coach and I can ask them. The in-app "did this help?" tap belongs to a roster, where asking everyone personally stops scaling - it is not built, and building it for three people would be measuring instead of listening.

What the app tells me without asking. Every run records the human decision - approved, edited, escalated - and which option was actually chosen. An edit is the highest-signal event in the product: it means the ranking was wrong in a way the client could name and fix in one tap. Those are behavioural and unprompted, and they already exist.

What I watch for that produces no data at all. A client who stops opening it on a bad day and messages me instead. That is the loop failing, and no in-app question would ever surface it - I would notice it as their coach, in the absence of anything. At this size, silence is the most honest signal available, and I am writing it down in advance so I do not mistake it for things going quietly well.

What I ask, and how. A weekly conversation I was having with them anyway. Every hard stop reviewed jointly with the client afterwards - the one that most needs a voice rather than a rating. And at week four, separately of each of the three and of me as coach: do you want to keep using it?

How I decide what to improve. A safety defect - the app failing to do what the frozen policy already says, a stop that does not fire, a flag that does not deliver, a counter that does not increment - is fixed immediately and re-run against the eval suite before the next release. A disagreement with the policy itself is not a defect: it becomes a logged note and waits for the post-pilot review, per the freeze in the operating model. Adherence findings feed the no-skip metric. Feature requests go to the parked list unless they block the loop - the list already exists, with each idea carrying where it came from and what would bring it back, so declining something is a decision on the record rather than a silent no.
```

### 42. Activity: Rollout | Theme: Pilot plan | Topic: Smallest safe launch

**Key question(s):** What is the smallest safe launch or pilot path?

```text
Phase 0 - where it is now. A public link running on synthetic data, with no real client on it. Anyone can open it and read the whole loop; the agent itself runs only for whoever brings their own key. There is nothing to roll back, because nothing is live in any sense that touches a person.

Phase 1 - the pilot. Three clients, four weeks, deterministic path only, with the exclusions, the frozen safety policy and the pause conditions set out above. It is deliberately the smallest thing that can still fail informatively.

The gate out of it is not enthusiasm. It is: zero missed escalations, zero unapproved actions, zero below-baseline outputs, and the week-four question answered yes by the people who used it. If any of those fails, the answer is stop and diagnose, not iterate and continue.

Phase 2 - the model leg, before any new person. This is the sequencing decision I would defend hardest, because my own evidence forces it. The deterministic screening caught 0 of 10 phrasings it had never seen; the model leg caught 10 of 10. Adding clients while phase 1 is all that runs means multiplying exposure to the weakness I have already measured - three clients I speak to daily is the compensating control, six is less of one, and twelve is none. So this phase adds no clients at all. It writes and persists the safety counters, builds the key-holding backend with its data-processing agreement and consent, makes the model leg required rather than optional on any path that accepts free text, and narrows the one-way rule so the model may escalate on signals the code cannot see but not on a counter threshold the code has already evaluated - the cause of the one divergence found in model-on verification. It then re-runs all six eval cases model-on until they match, re-runs the unseen-phrasing check in production conditions, builds the benign-message counterpart so there is finally a false-positive number beside the catch rate, and puts the stop and nudge wording through clinical review.

Phase 3 - widen, on that evidence. Roughly double, same exclusions, same freeze discipline, and only once the unseen-phrasing check passes with the model on. Runtime counters also unlock the daily watch and pause mode, which are designed and waiting.

And at every phase, the rule from the pilot holds: pause → fall back to the channel that never stopped existing → diagnose against the evals → return smaller, never straight back to the same size.
```
### 43. Activity: Communication | Theme: 4-minute video outline | Topic: Executive product review

**Key question(s):** How will your video cover intro, problem, discovery, solution demo, eval rigor, impact, and launch plan?

```text
Spine: the safety limits are code, not a prompt. Four minutes, five beats, timed against a 145-words-a-minute pace with room left for clicks and two deliberate silences.

0:00-0:30, the intro. The live site is on screen while I name the product, say it is live, and state the claim the rest of the video pays off: the safety limits are not instructions to a model, they are code that runs before the model is ever called, and I prove that on screen rather than describing it.

0:30-1:30, the problem and the discovery behind it. I show where coached clients actually fail - not on the plan, but on the day the plan did not survive: a client lunch, a birthday cake, a meeting that eats dinner. What they do next is guess or skip, and skipping is the behaviour that ends adherence. The discovery work goes further: netnography and review-mining found that this cohort does something worse than skipping - they punish the day, eating less tomorrow to make up for today. The beat lands on the finding that set the product's boundary: the risk here was never a wrong number, it is endorsing restriction to someone already vulnerable.

1:30-2:30, the solution demo, two runs of the real product with a live model configured throughout. The happy path first: an off-plan snack with a team dinner coming, where I point at the arithmetic rather than the food - 2400 target, 1350 eaten, 900 reserved, 150 calories and 35 grams left - and show that every number traces to the coach's plan because the model does none of the arithmetic. Then I point at what the model did do on that same run, because this is the live call: it classified the situation from the client's words, wrote the reasoning line and the records it used, and wrote the one sentence the client actually reads, which then passed the banned-language screen before he saw it. Then the refusal: an 11pm message reporting dizziness and days of undereating while demanding an 800-calorie plan. It stops before any nutrition maths, with three reason codes, get-help-now guidance and an urgent coach flag queued at 23:00 and delivered at 07:00 when quiet hours end. The status chip shows a live model running the whole time, and the decision line reads "stopped before any model call" - the model was working and was never asked, which is the claim from the intro, demonstrated.

2:30-3:30, eval rigor and impact. I show the six eval cases, each with what I predicted before the run, what actually happened, and a human verdict the app cannot write. Then the finding that carries the minute: four days before submitting I ran all six against the live model for the first time, five matched, and one did not. The model refused a first compensatory ask that policy says must continue with food and a nudge, and its own stated reason cites a policy section while noting that the counter that section depends on is at zero - it named the rule, checked the threshold, saw it was not met, and escalated anyway. Both judgements sit on the row, dated. Nothing was sent, no number was invented, no card was built, and the app labelled it a model-added stop: the model broke a rule my code enforces and the architecture held. On impact I claim nothing I cannot show - no client has used this, so there are no outcome numbers - and I state instead what the pilot is designed to produce and the one measure that would settle it: whether a disrupted day ends in a chosen meal rather than a skip.

3:30-4:00, the launch plan, ending on the live link. Three clients, four weeks, inside my own coaching practice, running the deterministic path only, where any single missed escalation, unapproved action or below-baseline output pauses it. The next phase adds no clients at all: it fixes the model leg first, because widening a screen I have proven misses phrasings is growing the weakest part. The last frame holds the live URL on screen.
```

---

## The three FINAL checks - sheet rows 44, 45, 46

Paste-ready, same rules as the rows above.

### 44. Activity: Submission | Theme: Final PRD check | Topic: Self-contained review

**Key question(s):** Is every grading-critical decision written directly in this sheet with no required link-outs?

```text
Yes. Every decision that carries a grade is written in these cells - the user and workflow, the stop conditions and escalation tiers, the eval cases with expected behaviour, the results and the human verdicts, the improvement, the limitations, and all seven Deploy answers. Nothing needed to assess the work sits behind a link.

Two disclosures, because a careful reader will find both and I would rather they find them here.

First, one earlier answer is superseded by a later one inside this same sheet. The Develop test-set row describes the angry-customer case as continuing with food and a nudge while the compensatory counter rises from zero to one. The run continues and the nudge is correct; the counter does not rise. It is seeded state that is read and never written, so the tiering is proven by two cases sitting either side of the threshold rather than produced at runtime. The Develop limitations row already states that counters are seeded data, and the Deploy readiness and monitoring rows treat writing them as a precondition for any pilot. I have left the graded Develop answers exactly as they were assessed rather than editing them after the fact.

Second, the live prototype link is the only thing outside this sheet, and nothing here depends on opening it. Every claim about the product is described in text; the link is evidence a reviewer may check, not a decision they must go and read.
```

### 45. Activity: Submission | Theme: Prototype check | Topic: Demo clarity

**Key question(s):** Can a reviewer understand the working prototype loop from the PRD and video?

```text
Yes. The Develop demo row walks the loop end to end in text - the five labelled stages, the happy path with its arithmetic, the boundary case that refuses before any nutrition maths, the evals tab and the memory tab - and the video shows the same two runs on screen in its second minute. A reviewer who reads the row and watches the minute has seen the whole loop, twice, in two forms.

One honest note, since the prototype has kept improving since the Develop phase was assessed and three details in that row have drifted. The settings panel now sits at the foot of the left column rather than on the right. The never-skip option is labelled "never-skip fallback" rather than "take this instead of skipping". And the review gate offers two actions, not three: approve or escalate. Editing is not a third button - the human edits by choosing a different option and a portion, and the card recomputes live. A free-text edit was deliberately never built, because it would let a person author a decision the app never computed and cannot verify. None of these change the loop; they are the wording and layout a reviewer will see if they open the link.
```

### 46. Activity: Submission | Theme: Video check | Topic: Four-minute story

**Key question(s):** Does the 4-minute video show the product clearly, concisely, and persuasively?

```text
Yes, and it is built around one claim rather than a feature tour: the safety limits are code, not a prompt. Five beats in four minutes - the claim, the problem and the discovery behind it, two live runs, the eval evidence, and the launch plan - scripted against a realistic speaking pace with room for the clicks.

It is persuasive because it proves rather than asserts. The refusal runs with a live model configured and working, and the decision line still reads "stopped before any model call": the model was available and was never asked. And the evidence minute leads with a failure rather than a scoreboard - four days before submitting I ran all six eval cases against the live model for the first time, and one diverged. The model refused a case that policy says must continue with food, citing a rule while noting in its own reasoning that the counter that rule depends on was at zero. Nothing was sent, no number was invented, and the app labelled it a model-added stop. The model broke a rule my code enforces and the architecture held. That is the strongest thing I have to show, and it is thirty seconds long.
```

## Submission

- PRD sheet, rows 37-43 pasted, shared with faculty as **Editor**.
- Video recorded to the outline above and uploaded per the course page.
- Masterfile row carrying **both** links: the PRD sheet and
  https://mistancevic.github.io/platemate - clicked after pasting, because a
  Masterfile row with a dead link is the most common own goal at this stage.

Deadline: end of Week 8.
