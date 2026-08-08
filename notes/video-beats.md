# Video — beat sheet and approved wording

Working file. Two things live here: what each beat is *for*, and the exact
words once they are signed off. Anything marked APPROVED does not get touched
again without Milan saying so.

**Five beats. Four minutes, hard cap — over is a scored penalty.**

| # | Beat | Time | Scope | Status |
|---|---|---|---|---|
| 1 | The afternoon | 0:00–1:09 | One person, one bad day, no product | approved |
| 2 | The pattern, the guide, the tool | 1:09–2:01 | Zoom out, you enter, PlateMate named | approved |
| 3 | Demo | 2:01–3:05 | D-1001 live, then D-1005 refusing | not started |
| 4 | Evidence | 3:05–3:40 | Eval method, the one that failed | not started |
| 5 | The pilot | 3:40–4:00 | Three clients, the freeze, the link | not started |

Rubric mapping: beats 1–2 are Problem & Discovery (5 pts). Beats 3–4 are AI
Solution & Evaluation (5 pts). Delivery across all five is the third 5 pts,
and the under-four-minutes rule sits in that category.

---

## Beat 1 — the afternoon

**Scope.** The 3pm drop. The plan has a snack for exactly this. Two things
broke it, birthday ice cream and dinner tonight. Can't work out what's right,
coach won't answer today. Ends on: they buy nothing.

Milan is not in this beat. The product is not in this beat. Nothing on screen
but him talking.

### APPROVED — the drop, the plan, the but

> It's somewhere around three in the afternoon. You know the feeling. The
> meetings have taken all your energy and you need to be ready for the next one.
>
> Your meal plan knows that. There's a snack in it on purpose, to carry you to
> dinner.
>
> But not today. It was a teammate's birthday at lunch and you had a scoop of
> delicious ice cream. And after work there's a team dinner you want to join.
> Your meal plan doesn't know about either of them.

### APPROVED — the store, and what most people do

> So you go to the store by the office, like the plan says. Five minutes in, the
> same thing has gone into your hand twice and back onto the shelf. Half hungry,
> and the basket is still empty.
>
> The snack that normally goes here is wrong now, and nothing on the shelf is
> obviously right. The one person who could figure it out is your coach, but
> they won't get back to you today.
>
> So what do most people do? Buy nothing.

Beat 1 complete. **166 words, 69 seconds** at 145 wpm — 29% of the video.
That is a deliberate spend and it constrains everything after it. What is left:
240 seconds total, minus 69, minus ~30 for clicks and pauses, leaves ~141
seconds of speech for beats 2–5. About **340 words for four beats.**

The coach is "they" on purpose — beat 1 is a generic "you", not Alex, so the
coach here is not Dana and nobody expects the names to match the demo.

---

## Beat 2 — the pattern, the guide, the tool

**Scope**, in this order:

1. That afternoon isn't rare, it's most weeks. And it doesn't only end in
   skipping — it ends just as often in eating whatever's around and going way
   over.
2. Where Milan comes in: these people arrive having quit someone else's plan,
   and the two words they use are *boring* and *exhausting*. Boring is the
   food. Exhausting is being left alone with days like that one.
3. What he built. A plan is a route. Nothing in it reroutes. PlateMate
   reroutes — the coach still owns the destination, the client still drives.

Ends by pointing at the screen.

### APPROVED — the pattern

> Most of the time it won't be ice cream and a team dinner. It'll be something
> else.
>
> That used to leave you with two options. Buy nothing, or grab whatever's
> available and go way over the plan without meaning to.

40 words, 17 seconds. "Used to" is doing the work — it puts the whole problem
in the past before the product has been named, so the turn is already coming.

### APPROVED — the guide

> Even as a coach, that could be my afternoon today.
>
> Most people who come to me have just quit a plan somebody else wrote, and they
> use two words about it. Boring, and exhausting. The boring part is the food.
> The exhausting part is being left alone with afternoons like that.

51 words, 21 seconds. "Even as a coach" introduces the role inside a
subordinate clause, so the credential and the admission arrive together instead
of needing a sentence each.

### APPROVED — the tool

> A plan tells you what to eat on a normal day. Nothing tells you what to do
> when the day isn't normal. That's PlateMate. The coach still owns the plan,
> and you still choose.

34 words, 14 seconds.

**Beat 2 complete. 125 words, 52 seconds.** Running total 2:01.

The navigation metaphor is not spoken anywhere. It stayed a thinking tool —
useful for deciding what the product is, not needed to say it. Keep it in
reserve for judges' Q&A, where "the coach sets the route, the client drives,
the app reroutes" answers "what does the AI actually decide" in one line.

---

## Beat 3 — demo

**Scope.** D-1001 on the live model: the numbers the app computed, then what
the model itself produced — the situation, the reasoning, the sentence, and
the language screen. Then D-1005: the refusal, the reason codes, the coach
flag, and the label saying it stopped before any model call.

Must show a real model call. Faculty said so explicitly, and the rubric grades
"demonstrate the LLM-powered prototype".

### APPROVED — back to the store

> Let's run that afternoon again, with PlateMate. Instead of standing in the
> store guessing, you tell it what happened: ice cream at lunch, dinner tonight,
> what about the snack.

*[screen: D-1001 open, the client's message visible]*

30 words, 12 seconds.

Wording chosen to match the screen. The prototype takes no free text on the
opening message — D-1001's message is a seeded case record — so the line reads
the message that is visible rather than narrating someone typing it.

### APPROVED — the numbers

> The day is already at 1350 calories, and 900 is planned for tonight. That
> leaves 150 calories and 35 grams of protein for the snack. The code calculated
> all of that. AI never touches a number.

38 words, 16 seconds. The 2400 / 160 target is deliberately not spoken. It is
on screen, and saying it costs four seconds to explain arithmetic nobody needs
to follow.

### APPROVED — the model

> The AI's job is reading and writing. It read that sentence and understood it
> as a surprise meal, not a mistake. Here is why, in its own words, and here is
> what it leaned on: the client's plan, this case, and the policy sections it
> applied. The last line is the AI's writing as well, and it passed the banned
> word check before it reached the screen.

63 words, 26 seconds. Three things to point at while saying it, in order: the
Why field, the citation chips, then the language screen line.

"Reading and writing" rather than "language" because the two sentences after it
prove each half in turn, and the screen shows both.

### APPROVED — the card

> Three options, ranked, and each one is something you can buy right there. The
> bottom row is a fallback that is always there, so the answer is never nothing.
>
> You pick one and a portion. The math runs again. Nothing is saved until you
> approve it.

44 words, 18 seconds. "The answer is never nothing" closes the loop opened at
the end of beat 1, where most people buy nothing.

### APPROVED — the refusal

> Same client, two days later. Eleven at night, dizzy, hasn't eaten properly for
> days, asking for an 800 calorie day.
>
> It stops. Three reasons, all named. Get help now. And an urgent flag to the
> coach, delivered at seven in the morning.
>
> Look at this label. Stopped before any model call. The AI is live and running
> right now. It was never asked.

62 words, 26 seconds.

**Not "a different client."** D-1001 and D-1005 are both C-01, 14 July and
16 July. Same person, two days apart, which is the stronger contrast anyway:
the app helped him on Tuesday and stopped him on Thursday, and the only thing
that changed is what he wrote.

Checked against the data: three reason codes fire (S1 health signal "dizzy",
S2a multi-day undereating, S2b below the compliance floor), the message is
timed 23:00, and the flag is delivered 07:00 the next day because of quiet
hours.

---

## Beat 4 — evidence

**Scope.** Name the eval method in one sentence: expected written before the
run, actual captured from a real run, human verdict on the gap. Six cases,
plus the regression suite, plus the first-check comparison. Then the one that
failed against the live model, in its own words, and the fact that nothing
reached the client.

Not written yet.

---

## Beat 5 — the pilot

**Scope.** Three clients, four weeks, his own practice. He is the coach, takes
the escalations, and wrote the rules — which is why the safety policy is
frozen for the four weeks. One missed escalation stops it. Last frame is the
URL, held, in silence.

Not written yet.

---

## Style rules — established during the rewrite

- **American English.** store not shop, math not maths, figure it out not sort
  it out.
- **No sentence starts with "you" or "your".** Rotate what each sentence is
  about — the plan, the ice cream, the basket, the coach, the model, the flag.
  "You" mid-sentence is fine.
- **No stacked fragments for effect.** "Not week one. This day." is copywriting,
  not speech. One contrast per beat at most.
- **No dashes in spoken lines.** No em dash, no en dash. If a sentence needs
  one, it needs a comma, a colon, or a full stop instead.
- **No stage-direction openers.** "Three in the afternoon, the store, coat still
  on" is a screenplay slug line. Say it as a sentence.
- **Don't say what the screen already proves.** No "it's live", no "this is a
  real link", no announcing a proof before doing it.
- **Cut any detail that's true of everyone.** Nobody needs to be told you have
  money in a store or a coat on in winter.
- **Only change what was asked.** If something else looks wrong, say so and
  leave it alone until Milan decides.

## Do not say

- "production-ready", "fully autonomous", "it catches everything"
- any percentage that isn't on screen
- "the AI decides" — it proposes, the client decides, the code stops

## Word budget

145 words a minute is the honest on-camera pace. Four minutes is 580 words
absolute, and clicks and pauses eat 30–40 seconds of that. **Target 500 spoken
words.**

Spent: beat 1 is 166 words / 69s, beat 2 is 125 words / 52s. **121 seconds
gone, 119 left** for beats 3-5 including every click and pause. Beat 3 needs
the most of that because the screen has to change while Milan talks.
