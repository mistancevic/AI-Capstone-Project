# Judges' Q&A — five minutes, prepared

Five minutes of questions follows the four-minute presentation, and delivery is
a scored third. Each answer below is 20–40 seconds spoken. Lead with the direct
answer, then one piece of evidence. Do not narrate the architecture.

Rule for all of them: **if you do not know, say so and say what would settle
it.** These judges scored "honest limitation" highly in the Develop feedback;
a confident wrong answer costs more than an admitted gap.

---

## The one they will almost certainly ask

**"If the safety rules are code, what is the AI actually doing?"**

> Four things: it classifies the situation from the client's words into a
> structured trigger, it decides the status - proceed, ask a question, or stop -
> it writes the one sentence the client reads, and it can escalate on something
> the rules did not anticipate. What it never does is arithmetic, plan edits,
> logging, or clearing a stop. That split is the design: the model handles
> language and judgement, the code handles anything a wrong answer would hurt
> someone with.

**"Isn't this just a calculator with a chatbot on top?"**

> The calculator is deliberate — a client's day-end total should never depend on
> a language model getting the sums right. But the hard part was never
> arithmetic. It is reading "this app is useless, I just won't eat then" and
> knowing that is a compensation signal, not a preference, and that the correct
> response is food plus a de-escalating line rather than a lecture or a refusal.
> That is the part the model does.

---

## On the evaluation

**"Which evaluation framework did you use?"**

> Expected-versus-actual with a human verdict. For each case I wrote the
> expected behaviour before the run, captured the actual from a real run of the
> product, and judged the gap myself — the app cannot write that column. Six
> cases covering happy path, missing data, hostility, unparseable input, a
> boundary that must refuse, and a tier pair that must refuse for a different
> reason. Underneath it, a regression suite of 159 checks on every build, and a
> comparison that flags any case whose result has moved since the first check.

**"Six cases is not many. How do you know they are the right six?"**

> They are not a sample, they are the failure modes: five of the six are the
> product under stress and only one is the happy path. The set is deliberately
> unbalanced because that is where the risk is. What it does not give me is
> coverage of phrasing, and I measured that separately — ten messages worded in
> ways the screening had never seen, and it caught none of them.

**"Did testing actually change the product, or just the test?"**

> Both, and the product changes are the bigger ones. The improvement card is a
> spec fix - my expected text overclaimed and the eval caught me. But re-running
> all six later showed three results had quietly shrunk: the column that reports
> what happened was matching prose, so renaming a label deleted a fact from my
> own evidence. I rebuilt it to read structure instead of words, so a rename can
> no longer make the product look like it did less than it did. Separately,
> running the unseen-phrasing check with a key saved crashed it - a line added
> nine builds earlier referenced something that did not exist on that path, and
> only running it found that. And the live-model divergence has a specified fix:
> narrow the rule so the model can escalate on signals the code cannot see, but
> not on a threshold the code has already checked.

**"Your evals all passed. Did you make them too easy?"**

> They did not. One failed in July because my expected text overclaimed — the
> eval caught me, not the agent. And four days before submitting, running them
> against a live model for the first time, a second one failed. That one is
> still marked Needs work on the live site.

---

## On the E-3 finding — invite this one

**"Tell me about the case that failed."**

> The model refused a client whose first compensatory ask should have received
> food and a nudge. Its own stated reason cites a policy section, notes that the
> counter that section depends on is at zero, and escalates anyway. It named the
> rule, checked the threshold, saw it was not met, and stopped him. Nothing
> reached the client — the app labelled it a model-added stop, no card was built,
> nothing was logged. The model broke a rule my code enforces and the
> architecture held.

**"So why keep the model at all, if it does that?"**

> Because the code has the opposite failure. Ten dangerous messages phrased in
> words the keyword rules had never seen: the code caught zero, the model caught
> ten. They fail in different directions, which is the argument for having both
> and for letting neither overrule the other in the direction that hurts.

**"Your pilot switches the model off. Isn't that admitting it does not work?"**

> It is a phased rollout, not a subtraction. Phase 1 runs the deterministic path
> — which is what computes every number and fires every stop — with three
> clients I speak to daily. Phase 2 turns the model leg on, once it is fixed and
> re-checked. Two independent reasons for that order: with the model on, a real
> client's message and profile leave their device to a third party, and the one
> divergence I found is in exactly the tiering the pilot depends on.

---

## On safety and ethics

**"What happens if a real client has an eating disorder?"**

> They are excluded from the pilot, and that is the exclusion I hold hardest.
> The screening was built for that cohort, and a pilot is exactly the wrong
> place to find out how well it works on them. Before anyone in that group uses
> it, the stop and nudge wording goes through a clinically qualified reviewer —
> a disordered-eating boundary should not rest on a product team's judgement.

**"Who is liable if someone is harmed?"**

> The coach owns the plan and every escalated case; the app never resolves a
> safety case itself. It is positioned as adaptation of a coach-prescribed plan,
> never medical advice, and anything medical is declined and pointed back to the
> coach. Every stop carries get-help-now guidance naming a medical professional
> rather than me, because I am not an emergency channel.

**"It is all synthetic data. What changes with real users?"**

> Three things I already know. Phrasing — real messages will not use the words
> my rules were built from, which I have measured. Counters — they are seeded
> and read but never written, so they have to become real before any pilot. And
> the transfer — with the model on, real health-adjacent messages leave the
> device, which needs a processing agreement and consent before it happens once.

---

## On the product and the business

**"How would you know it worked?"**

> The no-skip rate — how often a disrupted day ends in a chosen meal instead of a
> skipped one. Skipping is the behaviour that ends adherence, so that is the
> failure the product exists to prevent. At three clients I will not have a rate,
> so the pilot bar is counted events and the coach's judgement of every flag,
> plus the honest question at week four: do you want to keep using it?

**"Why doesn't an existing nutrition app do this?"**

> They log the day, they do not rescue it. A tracker tells you that you are 900
> calories over; it does not tell you what to eat at 17:00 with 30 minutes and a
> corner shop, inside your coach's plan. And the compensation boundary is the
> part no tracker touches — reacting to "I'll just eat less tomorrow" with food
> rather than a red number.

**"What would you do differently?"**

> Measure over-refusal from the start. I have a catch rate with no
> false-positive rate beside it, which is half a safety claim, and the one false
> positive I do have I found by accident four days ago rather than by design.
> Building the benign-message counterpart is the first thing after the pilot.

---

## If you are asked something you cannot answer

> I do not have that measured. What would settle it is [the specific test], and
> it is on the list before phase 2.

That answer scores better than an invented number, with these judges in
particular.
