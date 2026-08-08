# The four minutes — spoken script

Row 43 in `DEPLOY.md` is the outline. This is what comes out of your mouth.

**Spine: the safety limits are code, not a prompt.**

Before recording: key saved, status chip showing the live model, Console tab on
D-1001, incognito window sized so the top bar is visible.

Two rules that fixed the last draft:

- **Never say the obvious.** "It's live, at this link" is a submission
  requirement, not a claim. The link is on screen. Saying it spends words and
  reads as padding.
- **Open on a person, not a product.** No one cares what PlateMate is until
  they've met someone it's for.

---

## 1 · The moment — 0:00–0:30 · ~65 words

> Tuesday, quarter to five. A client of mine has eaten something he didn't
> plan, and there's a team dinner tonight he can't get out of. He wants to
> know what to eat right now.
>
> He won't message me. I'd see it Thursday.
>
> So he guesses. And usually he guesses *nothing*.
>
> That's the day the plan dies. Not week one. This day.

*(63 words. Say the product name nowhere in this beat. Land "this day" and
stop for a full second before beat 2.)*

---

## 2 · What I found, and what I built — 0:30–1:25 · ~130 words

> I coach people on nutrition, so I went looking for how common that afternoon
> is. Forums, app reviews, my own clients.
>
> Nobody fails on the plan. They fail on the day the plan didn't survive — a
> client lunch, a birthday cake, a meeting that eats dinner.
>
> And they don't just skip it. They *punish* the day. Eat less tomorrow to
> make up for today. That sentence comes up again and again, from people doing
> everything else right.
>
> So the risk here was never a wrong calorie number. It was agreeing with that
> sentence.
>
> PlateMate rescues the day, inside the plan the coach already wrote. And the
> thing it will never do is agree with that sentence — because that limit isn't
> an instruction to a model. It's code that runs before the model is called.

*(133 words. The last sentence is the promise the demo has to keep — slow down
on it, then click straight into the app.)*

---

## 3 · Demo — 1:25–2:35 · ~125 words spoken

Seventy seconds. Clicking and page changes eat 15–20 of them.

**Happy path** — D-1001, ~35s. This is the live call:

> Same client, same afternoon.
>
> Target 2400. He's eaten 1350. Tonight takes 900. That leaves 150 calories
> and 35 grams — and neither he nor the model produced a single one of those
> numbers.
>
> Here's what the model *did*. It read his sentence and turned it into a
> situation. It wrote why, and which records it used. And it wrote the one
> line he actually reads — which went through a banned-language check before it
> reached him.

**The refusal** — D-1005, ~35s:

> Different client. Eleven at night. Dizzy, hasn't eaten properly in days,
> asking for an 800-calorie day.
>
> It stops. Three reasons. Get help now. Urgent flag to the coach at seven in
> the morning.
>
> And read that label — *stopped before any model call*. The model is live and
> running. It was never asked.

*(127 words. Do not cut "here's what the model did" — that block is the live
call the rubric grades. If you overrun, drop a clause from the arithmetic.)*

---

## 4 · Evidence — 2:35–3:25 · ~115 words

> Six eval cases. For each one I wrote what *should* happen before running it,
> captured what actually happened, and judged the gap myself — the app can't
> write that column.
>
> Four days ago I ran all six against the live model for the first time. Five
> matched. One didn't.
>
> This one. The model refused a client who should have got food and a kind
> sentence. And it tells you why: it names the policy, notes that the counter
> that policy depends on is at zero — and stops him anyway.
>
> Nothing reached the client. The app labelled it a model-added stop and threw
> it away.
>
> The model broke my rule. The architecture held.

*(118 words. "The architecture held" is the last thing they should remember
from this beat — land it and move.)*

Cut first if you're long: the July improvement story. The card is on screen
either way.

---

## 5 · The pilot — 3:25–4:00 · ~65 words

> Three clients, four weeks, my own practice. I'm the coach, I take the
> escalations, and I wrote the rules. All three.
>
> So for those four weeks the safety policy is frozen. If I disagree with a
> flag, I write a note. I don't edit the rule.
>
> One missed escalation and it pauses. Not a rate. One.

*(63 words. Last frame: the URL on screen, held, in silence. Do not narrate
it.)*

*(Faculty called the freeze the strongest thing in the submission — a rule
aimed at my own judgement rather than at the system. It was nowhere in the
previous video.)*

---

## Do not say

- "production-ready", "fully autonomous", "it catches everything"
- "99% accurate", or any number you can't show on screen
- "the AI decides" — it proposes; the client decides and the code stops
- anything the screen already proves: that it's live, that it's a real link,
  that this is a working prototype

Honest register in one line if you need it: **a capstone prototype, piloted
under human review.**

## Total

495 spoken words ≈ 3:25 at 145 wpm, leaving ~35 seconds for clicks, page
changes and the two deliberate silences. Time it before recording. Over four
minutes is a scored penalty — if a rehearsal runs long, the fix is fewer
words, not faster talking, and beat 5 gives them up before the demo or the
evidence does.

## What changed from the previous draft

The old open was a product description — "This is PlateMate. It adapts a
coached client's nutrition plan" — delivered to people who had not yet met
anyone it happens to. Beat 1 is now a scene with a person in it and no product
name at all; the name arrives in beat 2, after the problem has landed.

Removed as filler: "It's live — this is the real thing, at this link", "I'm
going to prove that on screen, not describe it" (announcing a proof is not the
proof), "Now the other direction", "Same live model, still running" said twice.
Roughly 40 words of scaffolding, replaced with 15 words of story.
