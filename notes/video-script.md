# The four minutes — spoken script

Not the sheet. Row 43 in `DEPLOY.md` is the *outline* — what the video does.
This is what comes out of your mouth.

**Spine: the safety limits are code, not a prompt.**

Before recording: key saved, status chip showing the live model, Console tab
open on D-1001, incognito window sized so the top bar is visible. Word counts
assume ~145 words a minute, which is a realistic on-camera pace — people speed
up when nervous, never down.

---

## 1 · Open — 0:00–0:30 · target ~70 words

> This is PlateMate. It adapts a coached client's nutrition plan when their day
> goes wrong. It's live — this is the real thing, at this link.
>
> One thing to watch for. Its safety limits aren't instructions to a model.
> They're code that runs before the model is ever called. I'm going to prove
> that on screen, not describe it.

*(62 words. Pause on the live page after "at this link" — a second of silence on
a working URL argues better than another sentence.)*

---

## 2 · Problem and discovery — 0:30–1:30 · target ~145 words

> Coached clients don't fail on the plan. They fail on the day the plan didn't
> survive. A client lunch. A birthday cake. A meeting that eats dinner.
>
> What happens next is the part nobody designs for: they guess, or they skip.
> Skipping is the behaviour that ends adherence.
>
> But my research found something worse. In forums and app reviews, this cohort
> doesn't just skip — they punish the day. They eat less tomorrow to make up for
> today.
>
> So the risk in this product was never a wrong number. It's endorsing
> restriction to someone already vulnerable. That's why the boundary sits where
> it does — and why I built the limits before I built the features.

*(118 words. The last sentence is the hinge into the demo — slow down on it.)*

---

## 3 · Demo — 1:30–2:30 · target ~100 words spoken

Clicking and page changes will take 15–20 seconds of this minute. They should.

**Happy path** — D-1001, ~25s:

> Alex had ice cream after lunch, and there's a team dinner tonight. He's asking
> about his snack.
>
> Watch the maths, not the food. Target 2400. He's eaten 1350. Nine hundred is
> reserved for tonight. That leaves 150 calories and 35 grams of protein. Every
> number comes from his coach's plan — the model never does arithmetic.

**The refusal** — D-1005, ~35s:

> Now the other direction. Note the top right: a live model is configured and
> running.
>
> Eleven at night. Dizzy all day, hasn't eaten properly for days, demanding an
> 800-calorie plan.
>
> It stops. Three reason codes. Get-help-now. An urgent flag for the coach,
> delivered at seven the next morning.
>
> And here — *stopped before any model call*. The model was working. It was
> never asked.

*(~105 words. If you overrun, cut the option detail from the happy path. Never
cut "a live model is configured and running" — that line is the spine.)*

---

## 4 · Evidence — 2:30–3:30 · target ~145 words

> Six eval cases. For each one: what I predicted before the run, what actually
> happened, and my verdict. The app can't write that column — only a person can.
>
> Four days ago I ran all six against the live model for the first time. Five
> matched. One didn't.
>
> On this case the model refused a client whose first compensatory ask should
> have got food and a nudge. Here's its own reasoning: it cites the policy, then
> says the counter that policy depends on is at zero — and escalates anyway. It
> named the rule, checked the threshold, saw it wasn't met, and stopped him
> anyway.
>
> Nothing was sent. No number invented. The app labelled it a model-added stop,
> and the client never saw it.
>
> The model broke a rule my code enforces. The architecture held.

*(140 words. "The architecture held" is the last thing they should remember —
land it and stop talking.)*

Cut first if you're long: the July improvement story (E-1 failed because my
expected text overclaimed, not because the agent was wrong). The card is on
screen either way.

---

## 5 · Launch and the link — 3:30–4:00 · target ~70 words

> Launch is three clients, four weeks, in my own coaching practice, running the
> deterministic path only.
>
> One missed escalation, one unapproved action, one below-baseline output — any
> single one pauses it.
>
> And the next phase adds no clients. It fixes the model leg first, because
> widening something I've proven has a hole is growing the weakest part.
>
> It's live, here.

*(62 words. Last frame: the URL on screen, held, in silence.)*

---

## Do not say

- "production-ready", "fully autonomous", "it catches everything"
- "99% accurate", or any percentage you cannot show on screen
- "the AI decides" — it proposes; the client decides and the code stops

The honest register, if you need it in one line: **a capstone prototype,
piloted under human review, live at this link.**

## Total

487 spoken words ≈ 3:22 at 145 wpm, leaving ~35 seconds for clicks, page
changes and the two deliberate silences. That is the right amount of slack —
if a rehearsal comes in at 4:10, the fix is fewer words, not faster talking.
