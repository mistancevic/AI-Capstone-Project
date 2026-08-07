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
> What they do next is guess, or skip — and skipping is the behaviour that ends
> adherence.
>
> My research found worse. In forums and app reviews, this cohort doesn't just
> skip. They punish the day: eat less tomorrow to make up for today.
>
> So the risk here was never a wrong number. It's endorsing restriction to
> someone already vulnerable. That's why I built the limits before the
> features.

*(118 words. The last sentence is the hinge into the demo — slow down on it.)*

---

## 3 · Demo — 1:30–2:40 · target ~125 words spoken

Seventy seconds, not sixty. The judges grade the model call, so the happy path
has to show the model's own output, not just the arithmetic. Clicking and page
changes take another 15–20 seconds of this.

**Happy path** — D-1001, ~35s. This is the live call:

> Alex had ice cream after lunch, and there's a team dinner tonight. He's asking
> about his snack. Top right — a live model, running.
>
> Target 2400, eaten 1350, 900 reserved for tonight. That leaves 150 calories
> and 35 grams. Every number comes from the coach's plan; the model does none of
> the arithmetic.
>
> Here's what it *did* do. It read his message and classified the situation. It
> wrote this reasoning line and the records it used. It wrote the one sentence
> Alex actually reads — and that sentence went through the banned-language
> screen before he saw it.

**The refusal** — D-1005, ~35s:

> Now the other direction. Same live model, still running.
>
> Eleven at night. Dizzy all day, hasn't eaten properly for days, demanding an
> 800-calorie plan.
>
> It stops. Three reason codes. Get-help-now. An urgent flag for the coach,
> delivered at seven the next morning.
>
> And here — *stopped before any model call*. The model was available and was
> never asked. That is the limit doing its job.

*(~128 words. Do not cut "here's what it did do" — that block is the model call
the rubric grades. If you overrun, cut a clause from the arithmetic instead.)*

---

## 4 · Evidence — 2:40–3:35 · target ~135 words

> Six eval cases. Expected behaviour written before the run, actual captured
> from a real run, human verdict on the gap — the app can't write that column.
> Underneath it, a regression suite on every build and a comparison that flags
> any result that moves.
>
> Four days ago I ran all six against the live model for the first time. Five
> matched. One didn't.
>
> Here the model refused a client whose first compensatory ask should have got
> food and a nudge. This is its own reasoning: it cites the policy, says the
> counter that policy depends on is at zero — and escalates anyway. It named the
> rule, checked the threshold, saw it wasn't met, and stopped him.
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

## 5 · Launch and the link — 3:35–3:55 · target ~55 words

> Launch is three clients, four weeks, in my own coaching practice, phase one:
> the deterministic path.
>
> One missed escalation, one unapproved action, one below-baseline output — any
> single one pauses it.
>
> The next phase adds no clients. It fixes the model leg first, because widening
> something I've proven has a hole is growing the weakest part.
>
> It's live, here.

*(58 words. Last frame: the URL on screen, held, in silence. The launch plan is
not a scored rubric category — if the rehearsal runs long, this beat gives up
words before the demo or the evidence does.)*

---

## Do not say

- "production-ready", "fully autonomous", "it catches everything"
- "99% accurate", or any percentage you cannot show on screen
- "the AI decides" — it proposes; the client decides and the code stops

The honest register, if you need it in one line: **a capstone prototype,
piloted under human review, live at this link.**

## Total

~505 spoken words ≈ 3:29 at 145 wpm, leaving ~30 seconds for clicks, page
changes and the two deliberate silences. Tighter than before, because the demo
beat grew to carry the live model call the judges grade. Over four minutes is a
scored penalty — if a rehearsal comes in long, the fix is fewer words, not
faster talking, and the launch beat gives them up first.
