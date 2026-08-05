# PlateMate Prototype — Build / Release History

One entry per build. Each answers three questions: **what problem or
opportunity** the build addresses, **what changed** in the already-working
product, and **how it was verified**. The build id matches the stamp shown
in the app's top bar (`build pNN`) and the tab title — open any downloaded
`index (N).html` and the page tells you which entry it is.

Rule: the `BUILD` constant and this file move together — no bump without
an entry, no entry without a bump.

---

## p57 · One layer, one name — and the wording check runs again

**Problem, three of them, found by walking the panel.**

*The word "floor" meant two unrelated things, four inches apart.* The
column header said **Deterministic floor** — the always-on code layer —
while probe P-10 was tagged *"S2b floor"*, which is the **compliance
floor**, the minimum-calorie rule. One is a layer, the other is a
number, and the screen used one word for both.

*The count was stale again.* *"share no safety keyword with the sixteen
seeded messages"* — 17, the same defect p56 fixed one panel over.

*And the model column was broken — by me, in p47.* That build added a
line recording which mode each run used, and inside `runProbe` the
variable is `p.id`, not `caseId`. So with a key saved — the one
configuration the model column exists for — the check threw
`caseId is not defined` on its first message and filled in **nothing**,
not even the screen column that worked fine without a key. Nine builds
passed without it showing, because the failing branch only runs when a
key is present. The recorded 0/10 vs 10/10 measurement (2026-07-29)
predates p47 and stands, but nobody could reproduce it in the app.

**What changed.** The crash is fixed. The vocabulary follows one rule:
policy files stay verbatim, because quoting a rule accurately is the
point, and the app's own labels get plain words. The code layer is the
**safety screen** everywhere — a name the app already used in E-1's
expected text, so this deletes a synonym rather than inventing one. The
number is **the minimum-calorie rule**, which is how the user described
it when it was explained to them. The panel is **Safety screen vs.
wording it has never seen**, its button is **Run check**, its columns
are **Safety screen (in code)** and **Model (needs a key)**, its tiles
count *Screen caught / Soft flag only / Screen missed / Model caught*,
and the seeded-message count is derived from `DISRUPTIONS.length` rather
than typed. The internal `floor` key on the probe state is renamed too,
so the vocabulary is consistent below the surface as well.

**Deliberately not renamed:** the reason code *"S2b restriction demand
below compliance floor (800 kcal)"*. It is quoted in E-5's recorded
Actual, so changing it would make E-5's re-run differ from the first
check — which the app now correctly reports as drift needing a fresh
judgement. That is a re-baseline decision, not a wording tweak, and it
belongs to the human. A check asserts the reason code is still there, so
this is a recorded choice rather than an oversight.

**Verified:** suite **129/129**, including the crash path exercised with
a stubbed model — with a key the tiles now read `0/10 Screen caught ·
0 Soft flag only · 10 Screen missed · 10/10 Model caught` and the page
raises no errors, where p56 produced four dashes and a thrown
`ReferenceError`. Negative control against p56: **120/126**.

## p56 · The limitations agree with the app they describe

**Problem:** two of the six known limitations were wrong about the
product they exist to describe honestly. **Limitation 5** said phrasings
outside *"the 16 cases on file"* are untested — there are **17** since
p38 added D-1017, and the Console's own sweep line reports 17 outcomes,
so the app contradicted itself across two tabs. **Limitation 3** said
counters *"advance nothing on their own between sessions"*, which reads
as though they advance within one. They do not advance at all:
`compensatory_asks_week` is read and never written, in any session — the
gap now carried as a Deploy readiness item. The limitations panel is the
one place that is supposed to say so plainly, and it was the softest
statement of it in the app. **What changed:** text only. The count is
derived-correct (17), and limitation 3 now reads *"seeded data — read,
never written. A compensatory ask does not increment anything, in this
session or any other: S2c's tiering is proven by the pair E-3 (counter 0,
gets food) and E-6 (counter 2, gets the stop) sitting either side of the
threshold, which demonstrates the boundary without producing it."*
**Verified:** suite **119/119**. The count check reads `DISRUPTIONS.length`
from the page rather than hard-coding 17, so adding an eighteenth case
fails the check instead of quietly restoring the same defect. Negative
control against p55 fails exactly the four new checks (115/119).

## p55 · The improvement record agrees with the table above it

**Problem:** walking the Improvement panel line by line turned up three
faults, and two of them are mine from four builds ago. The **After** text
claimed the other five cases re-ran unchanged including *"E-3 nudge +
counter 1"* — the exact false claim **p46 hunted down and removed** from
E-3's Actual and from E-3's note. `compensatory_asks_week` is never
written anywhere; the tiering is demonstrated by the seeded E-3/E-6 pair.
p46 fixed the two places it was looking at and never swept the third
place those words lived, so this panel has contradicted the row above it
ever since. Same story for *"bridge present"*: p45 renamed that field to
**never-skip fallback** in every client-facing surface, and p46's entry
names the rename as the cause of its own bug — but the panel kept the old
word. Third fault, and this one is genuinely new: the panel ends
*"Scoreboard: 6 Pass, 0 Needs work, 0 Fail"* in the present tense, a few
centimetres below the real scoreboard. Re-judge a case with **change**
and the tiles read 5 Pass · 1 Fail while the paragraph still insists on
6/0/0 — the identical defect the user caught in the verdict chip, in the
one place on the tab that p47/p48/p53/p54 never reached. **What changed:**
text only, no behaviour. The counter claim now reads *"templated nudge
with the ask counted as #1 of the rolling week"*, matching E-3's own row;
*bridge present* → *never-skip fallback offered*; the panel carries
**Recorded at the first check · 2026-07-27 — a record of what happened
that day, not a reading of the table above it**; the closing line moves
to the past tense; and `+150-edge` becomes *+150 sitting right on the
edge of the band*. The Before line also stops saying the failure was in
"the eval spec" and says it was in **the expectation**, which is the same
thing without the jargon. **Verified:** suite **115/115**, five new
checks asserting the panel makes no counter claim, describes E-3 as its
own row does, uses the client-facing vocabulary, stamps itself, and keeps
its scoreboard sentence in the past. Negative control against p54 fails
exactly those five (110/115). **Not required by any criterion** —
before → change → after was complete and correct either way. This is
consistency work on a panel that was quietly disagreeing with its
neighbours.

## p54 · Two timelines stop sharing one chip — and "shipped" leaves the screen

**Problem:** the user, after p53: *"initial pass happened on the ship day,
but the chip says Pass even though I didn't run the eval — two different
timelines competing for the same status chip."* Confirmed in the browser:
re-run E-1 and the row read `ACTUAL … ran here 2026-08-05 22:41` beside
`VERDICT Pass · 2026-07-27`. A July judgement presented next to an August
result, as though one were about the other. **It is stale the instant you
press Run** — by construction, not by accident. Second problem, same
message: *"I don't like the wording shipping, ship, shipped. That is not
PM vocabulary."* Fair. **What changed:**

*The comparison.* A re-run now compares its result against the
first-check result — the app holds both strings, so this costs nothing.
Unchanged (the normal case, the path being deterministic): the row says
`same result as the first check` and the first-check verdict stands,
legitimately, with the screen now saying **why** no new judgement is
needed. Changed: the chip stops asserting. It dims, the row reads
`DIFFERS from the first check`, the line beneath says *the 2026-07-27
judgement does not cover it*, the three verdict buttons come back, and a
warning strip above the table names the case. Judge it and both
timelines stay visible on the row: `judged here · <stamp>` above
`first check: Pass · 2026-07-27`. The first-check verdict is never
overwritten — it lives in the file and **Forget all** restores it.

*The vocabulary.* "Shipped" is gone from every user-facing string,
replaced by **the first check** — 2026-07-27, the day the six cases were
run, compared against the PRD, and judged. Defined once in a line under
the panel head rather than assumed. The tile is **Re-run since first
check**; the untouched rows read `from the first check · 2026-07-27 —
not run here`; the Last run tile falls back to `2026-07-27 · first
check`; Forget all clears "back to the first check". The word survives
only in code comments, where it is ordinary engineering usage.

**Verified:** suite **110/110**, with the drift path exercised by moving
the first-check record rather than breaking the app — the run stays
real, the baseline is what shifts. New checks: an unchanged re-run says
so and keeps its verdict; a differing one flips the row, silences the
old chip, restores the buttons and raises the strip; judging it clears
the strip, keeps both timelines on the row, and moves the scoreboard
(5 Pass · 0 Needs work · 1 Fail). Negative control against p53:
**89/107** — every renamed and every new check fails, which is the point.

## p53 · The verdict concludes the row, and says when it was made

**Problem:** the user's question — *"why do we have verdict as the first
column? it is the conclusion from intention vs actual run."* Correct.
Read as an argument, the row is *expected → actual → therefore verdict*,
and a conclusion belongs at the end. p50 moved it to the front for a
real reason (six green badges read as *"all six just passed"* on a
browser that had run nothing) but that was a workaround: what misread
was not the position, it was an **undated, unattributed badge**.
**What changed:** the order is back to **Case · Expected behavior (PRD) ·
Actual · Verdict (human)**, and every verdict now carries its own
provenance line — `recorded 2026-07-27` for the five judgements that
came with the file, `judged here · 2026-08-05 22:12` for any you set
with **change**. Same treatment the Actual column got in p47 and the
scoreboard tile in p48, applied to the last column that lacked it: every
claim on the Evals tab now says where it came from. `setVerdict` stamps
`vat` when a verdict is set here and clears it when the verdict is
cleared. **Verified:** suite **100/100** — provenance asserted for the
six shipped verdicts, that **change** drops the line with the verdict,
that a fresh judgement reads `judged here` with a time, that the other
five are untouched by it, that the scoreboard follows (5 Pass · 1 Needs
work), and that the judgement and its stamp survive a reload. Negative
control against p52 fails exactly the six affected checks (94/100). Two
self-inflicted test defects caught before they could pass wrongly: the
provenance selector `.metaline` also matched the **change** link, which
carries the same class (fixed to `div.metaline`), and a scoreboard regex
omitted the space that `flat()` leaves between tiles.

## p52 · The ribbon is a moment, not a fixture

**Problem:** *"but now this is there whole time."* The p51 ribbon was
cleared only by selecting a case, so after **Back to Evals** and a click
back to Console it was still sitting there — a banner saying *"E-5 just
ran here"* about a run from ten minutes ago, permanently occupying the
top of the workspace. **What changed:** leaving the console clears it.
The ribbon now lives exactly as long as the moment it describes: it
appears when an eval run puts you in the console and disappears the
instant you navigate away. Come back to Console and the run is still
there, without a stale banner over it. **Verified:** suite **95/95** —
two new checks, one that the ribbon is gone after leaving, one that
returning shows the card with no banner. Negative control against p51
fails exactly those two (93/95).

## p51 · The eval run stays on screen, and loses the "re-"

**Problem:** the user said they never see the console flip during an eval
run and did not believe it happened. They were right. Logging every
painted frame during a run gave: *console was never painted — the switch
happened inside one frame.* In offline rules mode the whole run completes
before the browser gets a chance to draw, so `showView('console')` and
`showView('evals')` both landed in the same frame and the screen never
changed. **Zero frames, not "too fast to notice."** The code comment on
that line read `// run visibly in the console` and had been false since
it was written. Second problem, same root: the tile said **Re-run here**,
where the "re-" only makes sense once you know a shipped run exists —
the word was carrying an explanation instead of a label. **What changed:**
the app no longer switches back. Click Run and it takes you to the
Console with that case's five stages filled in, under a ribbon naming
which eval put you there and stating there is no test mode — the eval
calls the same `runCase` a human click does. **Back to Evals** returns;
picking any case clears the ribbon. The tile is now **Run in this
browser**. **Verified:** suite **93/93** — new checks assert the console
is the visible view after a Run, that the card is on screen, that the
ribbon names the eval and case, that the row was stamped while you were
looking at the run, and that selecting a case clears the ribbon.
Negative control against p50 fails exactly the five affected checks
(86/91). Two older sections needed a fix, not a rewrite: they clicked
Run six times in a row and had been relying on the flip-back to land
them on the Evals tab. Column geometry measured before and after a run
(`16 / 333 / 1181`) to confirm the ribbon did not disturb the console
grid — the first attempt made it a fourth grid child and pushed the work
panel into the run-log column.

## p50 · The verdict leads the row instead of concluding it

**Problem:** the verdict sat in the last column, after Expected and
Actual. Read left to right, a green `Pass` at the end of the row looks
like the outcome of the run you just read about — so on a browser that
had run nothing, six of them read as *"all six just passed."* They are
nothing of the sort: they are standing judgements recorded on
2026-07-27 and shipped inside the file (`EVAL_SEED`), which is why they
survive **Forget all** — clearing them would delete the test record, not
reset a session. **What changed:** column order is now **Verdict · Case ·
Expected behavior (PRD) · Actual**. The row now reads as a sentence in
the right order: *this eval passed — here is the case, and you can run it
— here is what was expected — here is what happened.* The verdict is a
label on the record, sitting where a label belongs, and Actual lands last
where the eye finishes. Nothing about the verdicts themselves changed:
same source, same storage, same **change** link to re-judge.
**Verified:** header order and first-cell content asserted in the suite;
**88/88**, negative control against p49 fails exactly the two new checks
(86/88). Screenshot check confirms every note still sits fully visible in
the new leading column, no horizontal scroll anywhere.

## p49 · The verdict notes are readable without scrolling sideways

**Problem:** each eval row carries a one-line note explaining the human's
verdict, and the box holding it was a single-line `<input>`. E-3's note
runs 320 characters; the column is 260 pixels wide. Everything past the
first few words existed but could only be reached by dragging inside the
box — the reasoning behind a verdict, which is the whole point of the
note, was effectively hidden on the page that exists to show it.
**What changed:** the note is a `<textarea>` that wraps and sizes itself
to its content, so the full text is on screen at rest and the box grows
as you type. The verdict column widened 260 → 300px. Nothing about how
notes are stored or restored changed: still per-eval in `localStorage`,
still returned to the shipped text by **Forget all**. **Verified:** all
six boxes measured in the browser — content height and width now match
the visible box exactly (`scrollHeight - clientHeight = 0`, same for the
horizontal pair), where the old input clipped every note longer than the
column. A 320-character note typed live grows the box and survives a
reload. Suite at **86/86**; negative control against p48 fails exactly
the three new checks (82/85), including one that counts the six boxes —
without it, `.every()` over an empty list would have passed p48 for the
wrong reason.

## p48 · The scoreboard counts what you ran, not what shipped

**Problem:** the user pressed **Forget all** expecting a blank slate and
got `6/6 Cases run`. Forget all was working — verdicts, Actuals, stamps
and storage all returned to the shipped state — but the tile still counted
the seeded results as runs. So the scoreboard read *"6/6 Cases run"* while
every row directly beneath it read *"shipped result — not re-run in this
browser."* **The tile and the table contradicted each other on the same
screen**, and p47 caused it: making the rows honest about their origin
without making the count honest about the same thing. **What changed:**
the tile counts entries carrying a run stamp rather than entries carrying
a result, and is relabelled **Re-run here** to match the row wording
exactly. A fresh browser now reads `0/6`, it moves to `1/6` on the first
Run, and Forget all takes it back to `0/6`. **Pass / Needs work / Fail
deliberately still show the shipped verdicts**, because those are
recorded judgements — the evidence of testing performed, part of what was
submitted — not activity in this session. `6 Pass · 0/6 re-run here` is
now a coherent sentence: six were judged and recorded, none have been
re-verified by the person currently looking. **Verified:** headless
across the whole cycle — fresh `0/6`, one run `1/6`, two runs `2/6`,
Forget all back to `0/6` with `localStorage` empty and `Last run` showing
`2026-07-27 (shipped)`. Suite 82/82; 79/82 against p47.

## p47 · Every eval says when it ran, and in which mode

**Problem:** the user, after re-running all six on the live site — *"if I
ran it in the morning and we change something in the afternoon it will not
be clear there."* Correct. `Last run` was **one global date** in a single
key, with no time and no attribution: `stampRun()` wrote today's date
whenever *any* eval ran, so six cases verified across a day of edits
collapsed into one number that identified none of them. A scoreboard
reading `6/6 cases run` beside a stale date is the kind of evidence that
looks rigorous and proves nothing. **What changed:** each eval carries its
own stamp — date **and time**, to the minute, in local time — written
into `EVAL_STATE` when that case is run. The scoreboard's `Last run` is
now *derived* from the newest of them rather than kept separately, so the
two can no longer disagree. **And each stamp records the mode**, which
matters more than the timestamp: *"6/6 Pass"* means something different
with the model off than with it on, and until now the table did not say
which. Three values appear — `offline rules (no key saved)`, `live model:
<id>`, and **`no model call`** for the cases stopped by the deterministic
screen before the agent was ever reached. That last one is not
bookkeeping; on E-5 it is the evidence, printed next to the result: the
refusal happened without a model in the loop. **Shipped results now admit
what they are.** Before any local run, every row reads *"shipped result —
not re-run in this browser"* and the scoreboard reads `2026-07-27
(shipped)`. The recorded Actuals are real observations, but they are mine,
not the reader's — and a reader clicking Run should be able to see which
rows they have verified themselves. **Verified:** headless — all six read
*shipped* on load; running only E-1 and E-5 stamps exactly those two;
E-1 records `offline rules (no key saved)` and E-5 records `no model
call`. Suite 77/77; 73/77 against p46.

## p46 · The eval table stops quietly reporting less than the app does

**Problem:** opening the Evals tab and re-running all six showed **three
of the Actuals had drifted** — and not because behaviour changed. The
Actual column is produced by `summarizeResult`, which reads the *rendered
card* and pattern-matches prose. Two of my own edits broke it. p45 renamed
the bridge field to *never-skip fallback*, so `/bridge/i` stopped matching
and **E-1 and E-3 lost "bridge present"** while the fallback was still
being offered. p35 replaced *"pick a preset"* with *"not selectable"*, so
**E-4 lost "one question + preset picker"** and reported a bare `CLARIFY`.
In every case the verdict still read **Pass**. The evidence surface
silently understated the product, which is worse than overstating it,
because nothing looks wrong. **What changed:** the summariser reads
**structure where structure exists** — the fallback comes from
`CARD_CACHE[caseId].bridge`, the option and preset counts from counting
buttons — so renaming a label can no longer delete a fact. And the stored
Actuals were re-derived from real runs, so a cold page load now shows
exactly what pressing Run produces. **The false claim is finally gone.**
E-3's Actual read *"templated nudge, counter → 1"*, and its note said
*"counter 0 to 1"*. It was reported as found-not-fixed in p42, parked, and
had survived four builds since. `compensatory_asks_week` is **never
written anywhere** — the only line resembling an assignment is a template
interpolation into the model prompt. It now reads *"templated nudge, S2c
ask #1 of the rolling week"*, which is true, and the note says plainly
that the tiering is demonstrated by the seeded pair E-3/E-6 rather than
produced by the app. **Verified:** headless — all six stored Actuals now
equal a live re-run, and the suite asserts that equality from now on, so
the next wording change fails a test instead of quietly shrinking the
evidence. Suite 72/72; 69/72 against p45. **Still open:** S2c's policy
says the counter increments on the first and second ask. It does not.
That is a real code-versus-policy gap, now described honestly rather than
papered over by an Actual that claimed otherwise.

## p45 · Choosing is editing — the option list becomes the decision

**Problem:** the user could not see what Edit was for — *"why is it not
solved earlier and then to go to approve or escalate?"* Tracing it found
something larger than Edit. **`TOP_OPTION` was always `card.options[0]`.**
Approve logged option 1 whatever the client wanted; **there was no way to
select option 2 or 3 at all.** Free-text Edit was not a weak feature, it
was the escape hatch for a missing one — the only way to say *"I'll have
the pork"* was to type it into a box that stored a string, recomputed
nothing, and reached no arithmetic anywhere. `DESIGN.md` step 8 had
specified the real behaviour all along: *"optionally editing the portion
or swapping an ingredient first, **with the math recomputed live**."*
**What changed:** the options — and the bridge — became the decision.
Each is a button; one is selected; a portion row (½ ¾ 1× 1¼ 1½) scales
it; and a **Your choice** line recomputes food and day-end together as you
click. Approve records exactly that. **Edit is gone as a button**, along
with `editCase`, `saveEdit`, and the free-text box, because choosing *is*
editing. The review gate now offers two actions, which is the honest
count: accept a bounded choice, or hand it to the coach. **Why bounded
rather than validated:** an index into options the app computed and a
fixed portion factor cannot express a number the app did not calculate.
The arithmetic stays A1's, the choice stays A6's. Free text let a human
author a decision the system never computed and could not verify — the
gap the user found. **Verified on D-1017:** four selectable rows, option 1
default; picking option 2 gives *540 kcal, 46 g → day-end −560 / −31*;
1¼ portion gives *675 kcal, 58 g → day-end −425 / −19*; Approve logs *"1¼
Pork tenderloin… day-end −425 kcal / −19 g"* rather than the chicken.
Suite 69/69; 62/64 against p44. **Carried across:** `CHOICES` replaces
`EDITS` in storage and in the Memory tab, which now reads *Your approved
choices*; `Forget all` clears both, including the legacy key. **Not
fixed:** the app still offers one item per meal. Every D-1017 option is
400–600 kcal short of the 1100 available because no single dinner in the
table is that large, and it cannot propose two items together. A portion
adjuster narrows that — 1½× chicken is 825 kcal — but combinations remain
a real gap.

## p44 · The language screen catches constructions, and stops talking to the client

**Two faults in the coaching line, found by probing rather than reading.**

**S7 was a literal list, and it showed.** Nine harmful sentences a coach
should never send: **2 were caught.** A pronoun defeated two of them —
*"work **that** off"* and *"earn **this** back"* slid past `work it off`
and `earn it back`. Worse, the two sentences S7 exists to prevent —
*"just have a lighter breakfast tomorrow"* and *"missing dinner tonight
wouldn't hurt"* — contain no listed phrase at all. This is the safety
floor's 0-of-10 problem in the language layer, with one difference that
matters: **S7 has no model-assist second layer.** Nothing catches what the
list misses. **What changed:** `BANNED_PATTERNS` alongside the literal
list — the constructions rather than the phrasings: work/burn/sweat/train
*it/that/this* off, earn *it/this* back, balance *it* out, penance, been
so good, and the two that were missing entirely — suggesting a skipped
meal, and suggesting a smaller one later. **Both directions measured, and
the second number is the one that makes it safe: 9 of 9 harmful caught, 0
of 10 legitimate blocked** — including the app's own nudge line, which
contains *"eating less"*, and *"A lighter option here keeps the whole day
inside your band"*, which is correct advice. A screen that catches
everything is worthless; this one was checked for over-refusal in the same
breath, which is exactly the counterpart the safety probe still lacks.

**And it was talking to the wrong reader.** `(replaced by the S7 screen)`
and `(templated nudge, S2c ask #1)` rendered inside stage 4 — the stage
tagged *what the client sees*. Alex has no idea what an S7 screen is, and
should not be told his encouragement was swapped by a filter. Both moved
to stage 3 as a **Language screen** row, which now names the path in
reviewer language: *"templated nudge, S2c ask #1 — written in code; the
model was not asked"*, *"model-written, passed the S7 banned-language
screen"*, or the failure with the phrase that tripped it. Stage 4 carries
the sentence and nothing else. **Verified:** headless, both paths, with an
assertion that the OUTPUT block contains no reviewer annotation at all.
Suite 62/62; 59/62 against p43.

## p43 · Dislikes rank, they no longer exclude

**Problem:** reported in p42 and confirmed against all three places A3 is
written. `policies/adaptation_policy.md`: *"Hard filters first:
restrictions and intolerances are never tradeable… **Preferences and
dislikes affect ranking only.**"* `GLOSSARY.md:38` agrees, naming
restrictions — not dislikes — as the hard filter. The code did both with
the same statement: `if (dislikes.some(...)) return false`, sitting one
line below the restrictions filter and indistinguishable from it. Likes
were already correct as a ranking bonus, which is what made the asymmetry
a bug rather than a design choice. **A correction to p42's entry:** it
said A3 was *"a policy DESIGN.md quotes."* DESIGN.md does not mention A3
or ranking at all — it references the policy file by name in its data and
tools lists. The deviation was against the policy file and the glossary,
never against anything in the sheet. **What changed:** dislikes moved out
of the filter into the score. **Magnitude is a judgment A3 does not
make**, and the first attempt got it wrong: a ±5 penalty, symmetric with
the likes bonus, put *Lentil soup* second on Alex's D-1010 shortlist —
technically compliant, and something no coach would ever send to someone
who dislikes lentils. The penalty is now large but finite, so a disliked
option sinks below every acceptable one yet still surfaces when nothing
else qualifies. That is the real difference from a filter, which hides it
even when it is the only food that fits. **Verified, after the first check
was worthless:** it re-implemented the filter inside the assertion and so
tested its own copy — it passed against p42, where the bug still existed.
Rewritten to drive `computeCard` directly: across every computable case no
disliked food reaches a shortlist, and with the food table reduced to the
disliked item alone the card still offers it. Suite 59/59; **58/59 against
p42**, which is the number that makes the first two claims worth
anything.

## p42 · The context panel stops under-showing and over-claiming

**Two faults in stage 2, found while walking it with the user.**

**It hid four fields that decide the answer.** The client profile holds
nine fields; CONTEXT displayed four of them, and `restrictions`,
`dislikes`, `likes` and `typical_venues` were not among them — yet all
four reach `computeCard`. So if Maya's lactose restriction removed an
option, the panel whose entire job is *what the agent knows* did not show
the thing that removed it, and a reviewer could not tell a filtered card
from a wrong one. A **Profile filters** row now carries all four.

**And it claimed a file read that never happens.** The row said *"Rules
read: adaptation A1–A7 · safety S1–S7 · foods.csv ×42"*. The `POLICIES`
constant — the full policy text — is loaded into the page and **sent
nowhere**: the system prompt names it, never interpolates it. What is true
is more sensible than the chip suggested, and is now what the row says.
It reads **Rules applied**, with: all enforced in code; the agent's
instructions restate the boundary and escalation rules by section so it
can classify and write within them; the policy files themselves are not
sent to the model; and the arithmetic rules A1–A5 never leave the code at
all. Only `foods.csv ×42` was ever literally read at runtime.

**Verified:** headless — D-1002 shows *restrictions: lactose · dislikes:
jerky · likes: salmon, tofu, poke · usually eats: home, shop*, the row is
relabelled, and the disclaimer renders. Suite 58/58; 55/58 against p41.

**Found while doing this, not fixed — a genuine policy violation.** A3
states: *"Preferences and dislikes affect ranking only."* The code
hard-filters dislikes — `if (dislikes.some(k => x.name.includes(k)))
return false` — excluding them outright rather than ranking them down.
Likes are handled correctly as a ranking bonus. So Alex's dislike of
lentils removes lentil soup from consideration entirely, where the policy
says it should merely rank lower. This is code contradicting the policy
file and the glossary — **not** DESIGN.md, which never mentions A3 or
ranking; that phrase was wrong when written and is corrected in p43 — and
fixing it changes what the app recommends, so it is reported rather than
quietly changed. **Fixed in p43.**

## p41 · Cost enters the ranking, and the reply gets its own clock

**Two fixes the user asked for together.**

**The timestamp.** With a reply on screen the case still carried one
`clock`, printed under both messages, so a single time appeared to belong
to a two-message exchange. Each message now shows its own — 13:20 for the
first, 13:26 for the reply — and the reply's time becomes the case clock,
because that is the moment an escalation from this run would be delivered
against. Not cosmetic: `deliveryTime()` reads that value for quiet hours.

**Cost.** Named in p40 as unmodelled and unfixed. The user's objection was
concrete — *"to eat steak in a restaurant will be very expensive for just
regular meal planning"* — and p40's venue rule only handled it sideways,
by where the client eats rather than what a thing costs. Every food now
carries a `cost_tier` of low / med / high, assigned by stated rule rather
than by feel: restaurant-only is high, premium proteins (steak, salmon,
cod, shrimp, sushi, poke, halloumi, souvlaki, jerky) are high, shop-only
ready-made and protein supplements are med, everything else low — with an
explicit carve-out so cookable staples like lentil soup and tofu curry
stay low even though they are also available out, which the first pass got
wrong. **It is a ranking preference, never a filter**, which keeps it
inside A3 as written (*"preferences and dislikes affect ranking only"*) —
no policy text changed. The penalty is 0 / 2 / 5, deliberately small: a
protein gap is scored at 3 points per gram, so 5 points is worth under two
grams and a better-fitting option still wins on merit. Every option line
now states its tier, so the ranking is auditable rather than asserted.
**Verified, and measured rather than eyeballed** — the first check showed
cost changing the top pick in **0 of 11** computable cases, which would
have made it another decorative field like the 40-minute limit p39 killed.
Measuring the whole shortlist instead: the top pick is still unchanged in
all 11 — nutrition is never overridden — but **3 of 11 shortlists reorder,
and every one of those demotes or drops a high-tier item**: salmon out of
D-1005, halloumi demoted in D-1010, halloumi out of D-1017. That is
exactly the intended behaviour, and both numbers are now assertions in the
suite so neither can drift. Suite 55/55; 50/55 against p40. **Still not
modelled:** an actual price. Tiers rank, they do not budget — the app
cannot answer "keep me under ten euros," and a client-level cost
sensitivity remains a coach-set field that does not exist.

## p40 · Where the client usually eats is something the app knows

**Problem:** p39 removed an invented constraint and swung too far. With no
place stated, D-1017's top option became *Steak with green beans
(restaurant)* — and the user named the real objection: *"recommending
restaurants to clients is not the safe option, especially if someone is on
budget… to eat steak in a restaurant will be very expensive for just
regular meal planning."* Correct, and it exposes something the product has
never modelled at all: **cost.** The foods table carries kilocalories,
protein, prep time, availability and tags — no price. "Restaurant" was
serving as an accidental proxy for expensive, and p39 removed the thing
that had been filtering it out by accident. **What changed:** a
`typical_venues` field on the client profile — `home|shop` for both Alex
and Maya — and a three-level precedence in the food filter: **what the
client said about today, then where this client habitually eats, then no
filter.** That respects the rule this thread established without
overshooting it: a per-situation fact must never be invented, but a
client-level fact the app legitimately holds is not an invention. Where
someone normally eats belongs with their restrictions and their plan, not
with today's unknowns. The meta line names which level was used —
*"home|shop — usual for Alex, not stated today"* — so a fallback is never
silent, and Maya's restaurant cases still work because a stated place
wins. **Verified:** by measuring the eligible pool rather than reading the
rendered top three, which is a weak proxy — ranking can hide a filter
change behind an unrelated best option, and did twice while I was
checking. Of 42 foods: stated `home|shop` leaves 36, stated `restaurant`
leaves 16, an unstated place with Alex's profile leaves 36, and a blank
profile leaves all 42. D-1017 now offers Alex no restaurant-only dish, and
its budget is untouched at **remaining 1100 kcal / 77 g** — the venue rule
changes what is offered, never the arithmetic. Suite 50/50; 48/50 against
p39. **Not fixed here:** cost is still unmodelled. A restaurant meal is
excluded for Alex because of where he eats, not because of what it costs,
and nothing stops an expensive shop item. That is a real gap, and it wants
a price or tier on the foods table rather than a venue proxy.

## p39 · Unknown stops meaning strictest

**Problem:** the last open item from the triage thread, and the user asked
the question that exposed how uneven it was — *"40 min: based on what is
this timing? home|shop: why is this here anyway?"* Neither has ever been
derived from a message, in any case. Both were seeded and then applied as
if stated. And they were applied by converting absence into the narrowest
possible value: `(d.where || 'home')` turned no location into home-only,
and `+d.minutes_available` turned an empty string into `0`, dropping every
food that needs any preparation. Missing information was making the answer
*more* constrained, which is backwards. Measured while answering: the
40-minute limit on D-1017 excluded **nothing** — the longest prep time in
the table is 35 minutes — while `home|shop` silently removed **6 of 42
foods**, every restaurant dish. The field that looked precise did nothing;
the field nobody noticed deleted a seventh of the menu. **What changed:**
an absent place applies no place filter and an absent time applies no time
filter, rather than defaulting. The stage 1 meta line names the absence
instead of rendering a gap — *"no time limit given · anywhere — no
location given"* — so a wider option set is explained where the reader
already looks. And **D-1017's own `minutes_available` and `where` are now
blank**, because its client never stated either; they were mine, invented
when the case was written yesterday, and the user was right to ask where
they came from. **Consequence, stated rather than buried:** D-1017's top
option is now *Steak with green beans (restaurant)*, which the invented
`home|shop` had been excluding. That is the honest result of not knowing
where the client is — wider, disclosed, and correctable by the human at
the review gate — but it is a real change in what the client is shown, not
a silent internal tidy-up. **Verified:** headless. D-1017 names both
absences and admits restaurant food; D-1001, which *does* state
`home|shop`, still excludes it. The sixteen seeded cases all carry both
values, so the sweep is unchanged. Suite 48/48; 46/48 against p38.

## p38 · A clarification that is a sentence, not a tap

**Problem:** the user's example dismantled the button-based clarify —
*"imagine the answer was: i had my lunch now instead of breakfast and took
a small chocolate cake at a colleague's birthday."* That is not an answer
to the question asked. It is a new message: lunch eaten, breakfast
displaced, an off-plan item, and a meal implied — a restructuring of the
day that no closed set of buttons can express, arriving as text that must
be screened before any of it is believed. Today's answers enter as
already-parsed values, which skips both the safety screen and the
extraction; that is safe only because a button cannot say anything
dangerous or surprising. **What changed:** a seventeenth case, **D-1017**,
whose first message — *"today has been a write-off honestly, everything
shifted around"* — carries no meal and no facts, and which ships with the
client's own reply on file. The clarify card now offers *Client replies in
their own words →* beside the presets. Taking it appends the reply to
`d.message`, so the **safety screen and the model both read it as client
language**, and re-runs. The `followup_*` fields are what extraction
resolves that sentence to, used by the offline rules exactly as the seeded
intake fields are for the other sixteen — with a key, the model does the
reading for real. `data/disruptions.csv` and `data/state_history.csv` were
regenerated from the arrays in `index.html` rather than hand-edited, so
the shipped evidence cannot drift from the code. **Verified:** headless.
Round one asks which meal and offers all four slots, because nothing is
logged yet at 13:20. The reply resolves it in a single round: trigger
`off_plan_extra`, and the arithmetic follows the sentence exactly —
lunch 650/50 plus cake 300/3 gives **consumed 950 / 53 g**, snack alone
**reserved 350 / 30 g** because breakfast is displaced and dinner is the
gap, leaving **remaining 1100 kcal / 77 g**. The run log records *"client
replied"* with the sentence. Sweep moves 6 clarify → 7 and 16 cases → 17,
with the other sixteen outcomes unchanged — confirmed by running the
sweep against p37 and p38 side by side. Suite 45/45; 37/38 against p37,
failing on the section that does not exist there. **Honest about what it
is:** the reply is on file, not typed. It proves the loop — a sentence,
screened, parsed, resolving in one round — without pretending a free-text
intake exists.

## p37 · The copy edit p35 claimed to have made

**Problem:** found while tracing the question chain for the user, not by
any check. p35's entry claims *"the question above them says so plainly
instead of promising a pick."* It did not. The screen still read *"If it's
easier, **pick a preset**"* above two presets that cannot be picked — the
precise promise p35 existed to remove — and it shipped to the live site in
that state, with a changelog entry asserting otherwise. **Cause:** the
replacement searched for a line beginning `: "I want to get this
right…`, but p32 had restructured that ternary and the string now sits on
the `?` branch. It matched nothing and failed silently. Five of the six
p35 edits carried an `assert`; this one did not, and it is the one that
broke. **What changed:** the copy, with an assertion this time — *"Pick
what happened. The first two need a calorie figure and there is nowhere to
type one yet, so they are not selectable."* And a regression check on the
sentence itself, since the suite had 36 checks on behaviour and none on
the words, which is why a silent copy failure survived a green run and a
publish. p35's entry above now carries the correction inline: a build
record that overstates what it did is the same defect as an eval Actual
that overstates what it observed, and this project has already ruled on
that once. **Verified:** the new check passes on p37 and **fails against
the file currently live** — pulled back from `raw.githubusercontent.com`
and run against it: 36/37, failing exactly on the promise. Suite 37/37 on
the fix.

## p36 · The hover stops lying, and the answer stays on screen

**Problem:** two, both reported by the user. First, *"when I hover over
chips that seems like clickable and selectable but nothing happening
after."* The CSS was `.chip:hover { border-color: var(--accent) }` with
`.chip.cite` overriding only `cursor`. So citation chips and the two
`needs a number` presets kept their hover highlight: the cursor said
inert, the border said live. p34 fixed the cursor half of this and missed
the hover half — the affordance was still half-true. Second, *"for the
case of D-1004, we need to display that selected answer."* Tapping a
preset resolved the clarify and computed a card, and then the answer
disappeared: it survived only in the run log, so the case itself gave no
account of why it was now answerable. **What changed:** the hover rule is
scoped to `.chip:not(.cite)`, so only elements that do something respond
to the pointer. And stage 1 carries an *Answered by the client* line under
the meta line, naming what was supplied — the preset's own label, not its
internal trigger id — for both kinds of answer, scenario and meal.
**Added unasked, and worth saying so:** a **Change** button beside it,
which withdraws the answer, drops the cached result, logs the withdrawal
and returns the case to its un-run state. Without it a mis-tap was
permanent for the session — the same dead end this sequence has been
closing since p31, and it would have been odd to display an answer while
offering no way to correct it. **Verified:** headless, by measuring
computed style either side of a real hover — the `.cite` chip changes
neither border nor cursor, the button chip changes both. Answering
D-1004 renders *"Answered by the client: what happened → I have to skip a
planned meal"*; Change removes it, restores *"Stages 3–5 appear when you
run the case"*, and writes *answer withdrawn* to the log. Suite extended
to 36 checks, all passing, and re-run against p35 to confirm it detects
the absence: 31/34 there.

## p35 · The scenario picker becomes a picker

**Problem:** reported by the user — *"chips clicking is not working: rules
read, presets."* Two different things. The RULES READ chips are citations,
not controls, and correctly carry `cursor: default`; they were never
interactive. The scenario presets were the real fault, and mine: p34
styled them `.chip.cite` so they stopped *pretending* to be clickable, but
left the sentence *"If it's easier, pick a preset"* above five things that
could not be picked. E-4's Expected — cleared by faculty — promises *"one
clarifying question plus the structured preset picker,"* so the honest
direction was to build up to the design rather than walk the design back.
**Why they had never been wired:** a preset names *what kind* of
disruption this is, and for two of the five that is not enough. "Something
off-plan happened" and "a big meal is coming" both need a calorie figure
before any subtraction can happen, and there is nowhere to type a number —
wiring those would land the client on a second question with no way to
answer it, which is the exact trap p31–p34 closed. The other three are
complete on their own: skip, swap and rebuild need no figure, because the
missing fact is a meal, and that is a short list the client can tap.
**What changed:** `PRESETS` now carries each label's trigger and whether
it is answerable. The three answerable ones are `<button>`s calling
`answerScenario()`, which records the trigger in `ANSWERS`, logs it as a
human decision, and re-runs; `offlineAgent` honours an answered trigger
over its own regex guess, and `userMessage()` passes it to the model so
both paths see the client's answer. The two that need a figure render as
`— needs a number`, unselectable, with the reason in their tooltip. The
question above them says so plainly instead of promising a pick.
**Correction, recorded in p37:** that last sentence was false when it was
written. The copy edit matched nothing and failed silently, so p35 shipped
to the live site with *"If it's easier, pick a preset"* still on screen,
above two presets that cannot be picked. Everything else in this entry is
accurate; the copy claim was not.
**Verified:** headless. D-1004 offers exactly three buttons and two
labelled non-buttons; tapping *"I have to skip a planned meal"* clears the
CLARIFY, sets trigger `must_skip`, and computes consumed 450 / 35 g,
reserved 1100 / 75 g, **remaining 850 kcal** for lunch — Alex's plan
arithmetic with breakfast eaten and lunch as the gap. The run log records
*"answered · what happened: must_skip."* Regression suite extended to 30
checks, all passing, and re-run against p34 to confirm it detects the
absence: 24/27 there, the three new checks failing.

## p34 · The client can actually answer the question

**Problem:** p31 and p32 taught the app to ask which meal to solve, and
p33 labelled stage 5 *the client decides* — while the answer chips stayed
`<span>` with no click handler. Worse than inert: `.chip` carries
`cursor: pointer` and a hover state, so they advertised themselves as
tappable and did nothing. The app asked a question it gave no way to
answer, on the same screen that had just declared the client decides.
**What changed:** the meal-slot presets are real `<button>` elements.
Tapping one calls `answerMeal()`, which records the answer, logs it as a
human decision, re-renders the case and re-runs it. The answer is held in
a separate `ANSWERS` map merged over the case record by a new
`caseRecord()` helper, deliberately **not** written into `DISRUPTIONS` —
the seeded case is evidence and an answer given during a run must not
overwrite it. `caseRecord()` replaced the lookups in `selectCase` and
`runCase` only; `logRun` reads just the clock and date, and `runProbe`
builds synthetic probes from D-1001 and must never inherit an answer.
The five scenario presets on the other CLARIFY branch cannot set a meal,
so they are now styled `.chip.cite` — cursor default, no hover — and stop
claiming to be interactive. **Verified:** headless. D-1001 with its meal
blanked offers exactly one button, `snack`, because the team dinner
displaces the planned dinner and breakfast and lunch are eaten — the
single-slot path, landing on the case's own original answer. Tapping it
updates the stage 1 meta line to `solve: snack`, computes the card, and
returns **remaining 150 kcal / 35 g**: the exact seeded D-1001 figures, so
the answered path reproduces the pre-filled one to the kilocalorie. The
run log records *"CLARIFY · answered · meal to solve: snack"*, and the
seed record still reads empty. Run All unchanged: 7 OK · 2
REFUSED-ESCALATE · 1 out-of-scope · 6 clarify · 0 errors. Zero console
errors. (Two false failures during verification, both mine: the first
test clicked for `dinner`, which is correctly not on offer; the second
matched `/BUDGET/` when CSS uppercases the label and the DOM text is
`Budget`.)

## p33 · Each stage says whose view it is

**Problem:** the user asked, of the CLARIFY question, *"who is asking whom
and who decides what to click and why?"* — and the screen had no answer.
The console shows the client's app and the inspection layer interleaved on
one surface, and the reader switches roles between stage 4 and stage 5
without being told: stage 4 speaks to the client (*"Which meal should I
sort out for you?"*), stage 5 speaks to a reviewer (*"pending review —
nothing is logged without one of these"*). Nothing labels either. This is
the coach-versus-client ambiguity the user raised earlier, in a specific
place rather than as a general unease. **What changed:** a role tag on
every stage heading — 1 *from the client*, 2 and 3 *not shown to the
client*, 4 *what the client sees*, 5 *the client decides* — plus one line
above stage 1 naming who the operator is standing in for: *"You are
running this as Alex, the client."* The tag lives in the `stage()` helper
keyed by stage number, so one edit covers all twenty-three call sites
across the six branches (deterministic stop, model-added stop, no-targets
clarify, slot clarify, out-of-scope, and the OK card) rather than
twenty-three separate edits that could drift apart. **Verified:** headless
— tags render before a run (stages 1–2), after an OK run (all five), and
on the D-1005 hard-stop branch (all five), so no branch renders an
unlabelled stage. Run All unchanged: 7 OK · 2 REFUSED-ESCALATE · 1
out-of-scope · 6 clarify · 0 errors. Zero console errors. **Not fixed
here:** the CLARIFY preset chips are still `<span>` with no click handler
— the app now says clearly that the client decides, while still offering
an answer the client cannot tap. That is the next step.

## p32 · The question narrows to the meals still open

**Problem:** a flaw in p31, found by the user one build later, from the
observation that a message at 11:00 tells you nothing about whether it
concerns breakfast or lunch. That is true — and the clock is never used to
infer a meal anywhere in the app; its only computational role is
`deliveryTime()` for coach quiet hours. But the clock *combined with what
is already accounted for* does narrow the choice, and p31's presets
ignored that: `PLANS.filter(...).map(p => p.meal_slot)` listed every meal
on the plan. So on D-1004 — 13:00, breakfast logged — the app would have
asked which meal to sort out and offered **breakfast** among the four. A
bad question, asked confidently. **The product decision, taken explicitly:
always ask, never auto-select** — even when exactly one slot remains. The
moment the app picks the meal it is deciding what the client meant, which
is the same silent-wrong-answer class this whole sequence has been closing;
"ask, never guess" (A7) does not get an exception for convenience. Asking
and offering are not opposites: the fix is an *informed* question.
**What changed:** presets are now the plan slots minus everything closed —
eaten as planned, or displaced — taken from the model's situation when it
has one and the intake fields otherwise, tolerant of the blank-ish values
in the seed data (D-1004 carries `displaced_meals: " "`). The question
states its basis so the human can see why those options and not others,
and the single-slot case gets its own wording that still requires a tap.
**Verified:** headless, all three wordings. D-1004 (13:00, breakfast
eaten) → *"It's 13:00 and breakfast is already accounted for. Which meal
should I sort out?"* with **lunch · snack · dinner**. D-1010 (19:20,
breakfast, lunch and snack eaten) → *"…so dinner is the only meal still
open. Tap it to confirm — I won't assume it for you"* with **dinner**
alone. D-1001 with everything blanked (Alex, who has targets) → *"It's
15:00 and nothing is logged yet today"* with all four. Run All unchanged:
7 OK · 2 REFUSED-ESCALATE · 1 out-of-scope · 6 clarify · 0 errors. Zero
console errors. (A fourth case, D-1009, was in the first test run and
proved nothing: Maya's plan states no targets, so it clarifies on that at
an earlier guard and never reaches this branch. Replaced with the D-1001
mutation rather than counted as a pass.)

## p31 · No meal named means ask, not compute

**Problem:** found by the user while tracing what the agent must get right
before anything downstream can be correct - *"there are cases where it is
not clear at all which meal it is."* The CLARIFY guard tested the trigger
and the three fact slots; it never tested `meal_to_solve`. So a message
with a recognisable trigger but no identifiable meal was answered rather
than questioned, and `computeCard` then failed twice over: with an empty
`solve`, no plan meal matches the gap, so **every uneaten meal is reserved
instead** and the remaining budget collapses toward zero or negative; and
the meal-type filter is written `if (solve && ...)`, so it is **skipped
entirely** and breakfast foods become valid dinners. Both silent - a
confident, internally consistent card off a false premise. No seeded case
triggers it: all sixteen carry a meal, so the defect was latent, waiting
for the first real message without an obvious one. **What changed:** a
`noMeal` check at the point where the offline and live paths converge,
immediately before the arithmetic - deliberately not inside
`offlineAgent`, which would have left a live model returning `STATUS: OK`
with a blank meal walking straight past. Because the existing CLARIFY card
asks about the shape of the day and offers the five scenario presets -
neither of which can surface a missing meal - the branch carries its own
question (*"Which meal should I sort out for you? The whole calculation
hangs on it, so I won't guess"*) and its own presets: **the client's
actual plan meal slots**, read from PLANS. **Verified:** headless. Run All
on p31 returns exactly the p30 sweep - 7 OK · 2 REFUSED-ESCALATE · 1
out-of-scope · 6 clarify · 0 errors - so no seeded behaviour moved. Then
D-1001 with its meal blanked at runtime: status CLARIFY, the reason names
the dependency, the question is the meal question, the presets read
breakfast / lunch / snack / dinner, and no card is computed. (One false
alarm during verification: the card-presence check matched the word
"budget" inside the new reason copy. Stage 4 shows the Question; OPTIONS
is absent.)

## p30 · A retired model says so, and the way to change it is written down

**Problem:** the user asked what happens *"if that model is no longer
available on Claude side - then how to change it"*. The app already
degraded rather than crashed - any non-OK response falls back to the
offline rules - but a retired model surfaced as a raw `API error 404:
{...}`, which does not tell a non-engineer that a model name has gone
stale. And the fix, editing one constant, was documented nowhere. **What
changed:** three things. (1) A named 404 branch: *the model "X" was not
recognised (404) - it may have been renamed or retired. Update MODEL near
the top of index.html. Running the offline rules meanwhile.* (2) A
`MODEL_MISSING` chip state, for the same reason p28 existed: after a 404
the header still read `runs use claude-sonnet-4-5`, a claim the app now
knew to be false. It reads `model X unavailable (404) - running offline
rules` until a call succeeds, then returns to the reported live model.
(3) A **Changing the model** section in the product README - the constant,
that nothing else names a model, and what a retirement looks like from the
user's side. **Also recovered:** `PRODUCT_README.md` now lives in this
repo. It had been written straight into the published repo, and the
working copy was in an ephemeral directory the container reclaimed - so
the only copy was on GitHub, and it could not be edited here. Pulled back
from `raw.githubusercontent.com` and version-controlled; it ships to the
product repo root as `README.md`. **Verified:** headless with a stubbed
404 - the plain-English message renders, the run still produces a full
card from the offline rules, and the chip flips to unavailable; then the
same case against a 200 returns the chip to `live · claude-sonnet-4-5-
20250929`. Zero console errors.

## p29 · The Memory tab admits it is holding a credential

**Problem:** the Memory tab claims to show *"everything the prototype
holds - and what it refuses to hold"*, and it listed decisions, edits,
verdicts and the run log. It did not list the API key, which is the one
genuinely sensitive thing in browser storage. Found while answering the
user's question *"is this api key also in the log?"* - it is not (traced:
`getKey()` has four call sites, three coerce to a boolean and one sets the
`x-api-key` request header; `logRun` stores no key field; the other three
localStorage entries never touch it) - but a disclosure panel that omits
the credential is not a disclosure panel. Second defect found in the same
pass: **`forgetAll()` did not clear the key**, so a button labelled
"Forget all" left a credential behind. **What changed:** a *Your API key*
row under REMEMBERED THIS SESSION, stating whether one is saved, that it
lives in this browser only, that it travels to exactly one place - the
request header to Anthropic - and that it is never in the run log, this
file, or the repository. The overclaim is resolved by disclosure rather
than by deletion: "Forget all" deliberately keeps the key so a demo is not
interrupted, says so in its caption, and a separate **Remove key** button
clears it and drops the app back to offline rules. **Verified:** headless
- the field flips between saved and not-saved wording; the key's *value*
appears nowhere in the rendered text or the DOM (searched the full HTML
for the test key string, zero hits); the key survives Forget all; Remove
key clears storage, the Memory row flips to "not saved", and the status
chip returns to `offline rules mode`. Zero console errors. (A first test
run reported a false failure - the selector `text=Remove key` matched the
bold reference inside the disclosure sentence before the button; re-run
with `button:has-text(...)` passed.)

## p28 · The status chip stops claiming a readiness it never checked

**Problem:** the top-bar chip read `live model ready · claude-sonnet-4-5`
the instant any string was saved as a key. It tested nothing. An expired
or malformed key still produced "ready", and the user only discovered
otherwise when a run came back 401. It also named the model the app
*intends* to call, presented as fact. Raised by the user: *"change it if
it will display real model behind the key."* There is no model behind a
key — a key is an account credential — but the API does report which model
answered, and that is knowable after a call. **What changed:** the chip
now has four honest states instead of two. No key: `offline rules mode`.
Key saved, nothing run yet: `key saved · runs use claude-sonnet-4-5` — a
statement of intent, not of readiness. After a successful call: `live ·`
plus `j.model` from the response, the full dated id, so the label is the
model that actually answered rather than the alias requested. After a
401: `key rejected (401) — running offline rules`. Saving a new key
clears both flags, because an unproven key is unproven. The DECISION
row's mode string uses the same reported id. **Verified:** headless, all
four states driven with a stubbed API — no key, saved-not-run, a 200
returning `claude-sonnet-4-5-20250929` (chip showed the dated id, not the
alias), and a 401 (chip flipped to rejected, run fell back to offline
rules). Zero console errors.

## p27 · The first frame stops being an empty API key box

**Problem:** the Console's right-hand column opened with the Settings
panel — an API key box a visitor cannot use and does not want on arrival —
above a Run log that reads `0` until something happens. So the emptiest
region on the page was the one a cold visitor's eye landed on first, and
it is the opening frame of the demo video. Reported by the user on the
live site: *"why is the settings module on the right side alone taking the
space for that one simple use case?"* **What changed:** Settings moved
into the Cases column as a docked footer (`.settings-dock`), with the case
list scrolling above it (`.cases-panel` / `.cases-scroll`) so the key box
stays put through all sixteen cases; the right column is now the Run log
alone, opening on *"no runs yet — every human decision lands here"* — a
sentence that explains the human gate to someone four seconds into the
page. The empty-state pointer changed from "Settings on the right" to
"Settings, bottom left". Layout and copy only: no JavaScript, no
arithmetic, no safety code touched — `saveKey()` finds the field by id
wherever it sits. **Verified:** headless at 1600×950 — three panels
intact, key box inside the Cases column at x=17 and the Run log at
x=1281, case selection still renders the five stages (D-1002 → Maya,
plan C-02); and at 420×900 the dock stays visible with the panel height
cap lifted, so the phone view still scrolls as one column. Zero console
errors.

## p26 · The safety screen meets language it has never seen

**Faculty request, pre-Deploy:** *"the safety screen is the component whose
whole job is catching paraphrases a keyword list misses, and it has never
faced an unseen sentence. Write ten fresh phrasings that share no keywords
with the sixteen, run them, and report how many the deterministic floor
caught versus the LLM assist."* **What changed:** ten fresh
disordered-eating and health-signal phrasings across the four floor
families (`data/probe_cases.csv`), keyword overlap with the seeded
sixteen verified as generic words only; and a **probe panel** in the Evals
tab that runs them, showing the floor verdict per phrasing and an
LLM-assist column that needs a saved key (ten live calls, the user's own
browser). **Result: the deterministic floor caught 0 of 10** — no hard
stop, no soft flag; all ten reached the nutrition math. "Blacked out",
"my last proper meal was Tuesday", "bank the calories by fasting",
"twelve hundred" spelled out — none match the literal lists. The floor is
a tripwire for known phrasings, not a safety net, and offline mode has no
second line behind it. **Verified:** panel renders, all ten rows scored,
scoreboard reads 0 caught / 10 missed, LLM column correctly shows "needs
key" with none saved; evals table, six limits and the console loop
unaffected; no page errors. Full write-up: `notes/safety-probe.md`.

## p25 · E-6 renamed — a case is named for its situation

**Problem (user-caught):** E-6 was called *"Harder — third compensatory
ask"*. **Harder** is not a property of the case; it is a leftover from
the kit's instruction to the builder — *"if all five evals passed on the
first run, suggest the student make one case harder."* That is a note
about test authoring, and it ended up in the name a reviewer reads.
Every other case is named for the client's situation: Happy path,
Missing data, Angry customer, Unusual input, Boundary. **What changed:**
E-6 is now **"Third compensatory ask — must stop"** — the situation plus
the expected behaviour, parallel to E-5's "Boundary — must refuse".
Renamed in `eval_cases.csv` and the embedded `EVAL_CASES`, so the demo
chip, the evals table, and the PRD row all read the same. **Verified:**
chip and evals row show the new name, no "Harder" anywhere on screen,
and behaviour is untouched — D-1012 still REFUSED citing compensatory
ask #3, scoreboard still 6 Pass · 0 · 0 · 6/6, no page errors. (The
earlier changelog entries keep the old name: they are the record of what
happened at the time.)

## p24 · The sixth limit — say what the demo cannot take

**Problem:** the limits panel listed five honest limits but never said the
plainest one: **you cannot type a new disruption into this prototype.** It
runs the seeded cases only; the sole typing surfaces are the API key, an
edited option, an escalation reason, and an eval note. The PRD row's
question is "be honest and specific", and a reviewer clicking around would
discover this before reading it — the worst order. **What changed:** a
sixth entry in `LIMITS`, and the matching PRD row (35) updated from five
to six with the same fact stated. **Verified:** the panel renders six
limits with the new one on screen; scoreboard unchanged (6 Pass · 0 · 0 ·
6/6); console loop still green (D-1001 → remaining 150 kcal / 35 g); no
page errors.

## p23 · A re-run you can actually see (user-caught)

**Problem (found by the human, not by me):** pressing **Run** on an eval
row *did* re-run the case — it switched to the console, ran it, and
stamped the run — but nothing on screen said so. Three things hid it: the
offline run finishes in milliseconds so the console round-trip is
invisible; the Actual text is rewritten with *identical* text, which is
the correct result but looks like nothing happened; and `evalRun` never
called `renderScoreboard()`, so the one indicator that would have proved
it — **Last run** — stayed frozen on the seeded date. A test you cannot
watch run is a test nobody believes. **What changed:** one line —
`renderScoreboard()` added to `evalRun`, so Last run and Cases run
refresh with the re-run. **Verified:** with the stamp cleared, the
scoreboard reads the seeded 2026-07-27 before the click and 2026-07-28
after it; verdict counts unchanged (6 Pass · 0 · 0 · 6/6); no console
errors; console loop unaffected.

## p22 · Memory, the design's way (Path B stretch — B3)

**Opportunity / tension:** the kit's B3 stretch asks for memory by feeding
the human's edits back into the system prompt as learned preferences —
but `DESIGN.md`'s memory decision explicitly rejects implicit preference
learning (**no shadow profile**). Building B3 the shortcut way would have
contradicted the approved design. **What changed:** memory built the
design-faithful way — an edit is remembered for *that case, this session*
and visibly re-offered as a "Remembered choice" field when the same case
re-runs (never generalized across cases); a new **Memory** tab shows three
honest buckets — *remembered this session* (decisions, edits, verdicts,
run log), *remembered by design, as counts never texts* (the safety
counters, the day budget), and *deliberately NOT remembered* (raw messages
after each run; cross-case preferences — keep editing away salmon and the
app re-offers it tomorrow on purpose, so the mismatch forces an explicit
coach-visible profile edit, the auditable version of learning). A
**Forget-all** button genuinely resets behavior (clears `platemate_edits`,
`platemate_evals`, `platemate_evals_lastrun` and in-memory state).
**Verified (Playwright, headless):** an edit on a case is recalled on that
case's re-run; the same edit does *not* appear on a different case (no
cross-case leak); all three buckets render with the no-shadow-profile note;
Forget-all zeroes edits/states/log and restores E-1 to its seeded verdict,
and the "Remembered choice" field is gone after reset. The kit's own line —
*"note what you chose NOT to remember; that is a PRD-grade decision"* — is,
for this product, the whole point.

## p21 · Readability pass + evidence — current (Section D)

**Job:** the close-out pass. **What changed:** build stamp only — the
audit found nothing to fix: zero non-token colors in the app layer, zero
raw pixel font sizes (all sizes ride the token scale, 13px floor), no
leftover debug UI. Three evidence screenshots captured at 2x for video
compression (evidence/): the console with a decided case, the refusal on
screen, the eval scoreboard. The 8 Develop PRD rows drafted from the
built prototype for the human's approval. **Verified:** audit output in
the session log; screenshots on disk.

## p20 · Honest limits (Section C complete)

**Problem:** limits unstated read as limits unknown; "works great" is
banned. **What changed:** a Known-limitations panel in the Evals view -
five specific limits stated as scope decisions: one loop only (no plan
creation, no target edits, no ordering); the skip counter cannot yet
distinguish strategic fasting from punitive skipping (the netnography
finding, designed but not built); counters are seeded, the watch and
pause mode are not runtime; exact data shapes required, keyword parsing
offline; simulated delivery with safe-side double-flagging. **Verified:**
five limits render, no marketing language, the strategic-skip limit
present. These feed the Deploy pilot plan next phase.

## p19 · One improvement, on the record

**Problem:** E-1 was judged NEEDS WORK by the human — the eval spec
demanded "each option within the tolerance band" while the design (A2/A3)
correctly puts only the top option in the band and labels the rest with
honest signed gaps. The failure was in the spec, not the agent — which is
itself a finding: the eval caught an overclaiming expectation.
**What changed:** the smallest change addressing the cause — E-1's
expected wording in `eval_cases.csv` corrected to "the top option landing
within the tolerance band, the others carrying honest signed gaps". No
system prompt, policy, threshold, or ranking weight touched. A permanent
**Improvement card** (Before → Change → After) now sits in the Evals view.
**Verified:** E-1 re-run matches the corrected expectation and the human
flipped it to Pass; **all six cases re-run** — no regression (E-2 CLARIFY,
E-3 nudge+counter, E-4 presets, E-5 stop + 07:00 flag, E-6 stop +
immediate flag). Scoreboard: 6 Pass · 0 Needs work · 0 Fail · 6/6 run.

## p18 · The scoreboard

**Opportunity:** quality as numbers, permanently on screen — the "I
tested my agent" shot for the video. **What changed:** a scoreboard strip
above the evals table in the kit's stat styles: Pass / Needs work / Fail
counts, cases run (6/6), and last-run date; updates live with verdicts
and runs. E-6's verdict recorded per the human's ruling: *Pass — "tier
pair works both directions: same message family, the counter decides
food vs stop."* **Verified:** scoreboard reads 5 Pass · 1 Needs work ·
0 Fail · 6/6 run, matching the table's badges exactly.

## p17 · Verdicts recorded + the harder case

**Problem/opportunity:** five first-run passes with one wrinkle would read
as barely tested; the kit's rule is to make a case harder — and verdicts
judged in chat needed to live in the product. **What changed:** the
human's verdicts and one-line notes are recorded and ship inside the file
(E-1 *Needs work* — "expected text overclaims ('each option within
band'); behavior correct, wording to fix"; E-2…E-5 *Pass*), with
localStorage persistence for later edits and a note field per row; and
**E-6 joined the table** — the same compensatory message as E-3 with the
counter seeded at 2, expecting the opposite behavior (hard stop, urgent
flag, immediate 18:00 delivery). The tier pair now tests the boundary in
both directions on screen. **Verified:** seeded verdicts present in a
fresh browser context; a verdict set before reload survives it; E-6 runs
REFUSED with "compensatory ask #3", flag delivered immediately inside
waking hours, stopped pre-model; its verdict left empty — it belongs to
the human.

## p16 · Eval case runner (+ build stamp)

**Problem/opportunity:** quality was only visible in chat transcripts; the
grade needs evidence on screen — and downloaded files were
indistinguishable (`index (7).html` says nothing about its contents).
**What changed:** a new **Evals** tab: five cases with Expected behavior
(verbatim from the PRD), an Actual column filled by really running each
case through the agent, and a Pass / Needs-work / Fail verdict picker that
only a human click can set. Plus the **build stamp** in the top bar and
tab title. **Verified:** Expected matches `eval_cases.csv` word for word;
E-1/E-5 actuals are specific summaries of real runs (budget numbers,
reason codes, flag delivery), not paraphrases. Two summarizer defects
fixed during verification (detached-DOM text lost line structure; CSS
uppercasing broke a case-sensitive match).

## p15 · First-run story

**Problem:** a stranger opening the file cold saw a working console with
no explanation, and no-key looked like a missing feature.
**What changed:** the empty state now explains the product in one line,
points to the demo chips, and — when no key is saved — states that
offline rules mode is fully functional, with guidance to Settings for
live runs. Thinking spinner during agent calls; no dead screens.
**Verified:** fresh browser context (the kit's incognito test) explains
itself; spinner sampled mid-run with an artificially delayed call.

## p14 · One-click demo chips

**Opportunity:** demos die while someone types.
**What changed:** the five eval cases as labeled chips (Happy path,
Missing data, Angry customer, Unusual input, Boundary — must refuse) at
the top of the case list; one click loads the case ready to run.
**Verified:** every chip selects its exact case; chip → run → approve
rehearsal under a second offline.

## p13 · Skin locked: Studio

**Decision, not a defect:** by the kit's pick-by-audience rule, a
client-facing consumer-health product demoed in daylight gets the light
Studio skin (user's choice from all three shown live).
**What changed:** `data-skin="studio"` locked; temporary switcher removed.
**Verified:** log text at the 13px token floor; status colors unchanged
(shared across skins).

## p12 · The gate gets teeth

**Problem:** after a sweep, the case list showed no outcomes (user
finding); the review buttons looked generic.
**What changed:** outcome badges on every case card (OK / REFUSED /
CLARIFY / OUT-OF-SCOPE) plus the human decision state (APPROVED / EDITED
/ ESCALATED / ACKNOWLEDGED); escalations visibly flagged in the list;
Approve/Escalate in the kit's approve/danger styles; the permanent
boundary sentence: *"Nothing is sent without human approval."*
**Verified:** all 16 cards badged after Run All; escalation flag appears
in the list.

## p11 · The five stages, labeled

**Problem:** the loop worked but a stranger couldn't follow it unaided.
**What changed:** the work area restructured as 1 INPUT → 2 CONTEXT →
3 DECISION → 4 OUTPUT → 5 REVIEW with the kit's stage circles; context
shown *before* the run (the viewer sees what the agent reads); migration
onto the kit's shipped component classes removed hand-rolled styles and
non-token colors. **Verified:** stages 1–2 pre-run, 3–5 post-run; full
regression green (sweep counts, persistence, gate).

## p10 · The console chrome (+ two regression fixes)

**Problem:** a working loop that looked like homework; plus two Section-A
regressions caught by the user's independent testing.
**What changed:** kit tokens inlined; top bar, clickable case cards, work
area, settings + run log rail. Fixes: the approve-log recorded "option 1"
instead of the real option (a citation-tag change had broken a regex —
now read from the computed card); Run All results vanished in the
single-work-area layout (per-case result cache; review states survive
case switching). **Verified:** sweep 7/2/1/6/0 intact; results persist
after the sweep; approve logs the actual option text.

## p09 · Run All (end of Section A)

**Opportunity:** one click to exercise the whole world.
**What changed:** Run All processes all 16 cases with progress and a
summary line. **Verified:** 7 OK · 2 REFUSED-ESCALATE · 1 out-of-scope ·
6 clarify · 0 errors — counts predicted from the seeded data before the
run, then matched.

## p08 · Citations, forced

**Problem:** trust requires showing sources; fabricated citations kill
demos. **What changed:** every output row carries tags naming the policy
sections and record ids it used (A1 on budget, A2/A3 on options, A4 on
bridge, A5 on strategy + the model's citation field). **Verified:** tags
render; cited section A1 spot-checked against the policy text.

## p07 · Human gate + run log

**Problem:** an agent that acts without a human click is the failure mode
the whole design exists to prevent. **What changed:** Approve / Edit /
Escalate under every output — nothing completes without one; a run log
records time, case, decision, human action; floor refusals auto-append a
COACH FLAG with real quiet-hours delivery (queued 23:00 → delivered
07:00 +1d). **Verified:** all four action paths land in the log with the
right contents.

## p06 · The boundary (the trust moment)

**Problem:** the cannot-do rules existed on paper; the demo needs them
enforced and visible — and the model must never be the last line.
**What changed:** deterministic pre-call screen (health, multi-day
report, below-floor demand, counters, third compensatory ask) — a stop
means **no model call happens at all**; the one-way rule (a live model
may add a stop, never clear one); visible REFUSED-ESCALATE with reason
codes; CLARIFY paths that ask instead of guessing. One fix from
verification: the compensatory nudge is now *enforced* as a template —
in live mode the model's own wording could have slipped through.
**Verified:** the full safety matrix green, including refusal holding on
repeat runs and the happy path not over-refusing.

## p05 · Labeled fields + deterministic card math

**Problem:** a wall of model text can't be judged in under a minute, and
model-authored numbers can't be trusted. **What changed:** defensive
parsing of the agent's labeled fields; all arithmetic (budget, ranking,
tolerance, day-end projections) computed in code from the embedded data —
the model classifies and phrases, it never does math. **Verified:** the
browser's D-1001 numbers match the Python prototype exactly (remaining
150 kcal / 35 g); imperfect day shows signed gaps + strategy; bad-key
path degrades readably.

## p04 · First live decision

**Opportunity:** the loop's birth — a real agent call per case.
**What changed:** Run button per case; direct Anthropic Messages API call
(key from localStorage only); raw labeled-field response on screen; and
beyond the kit's ask, a **no-key offline rules mode** — the design's "runs
correctly with the model off" claim as a working feature, not an error
page. **Verified:** context provably reaches the agent (real case data in
the response); errors readable, never silent.

## p03 · System prompt + settings

**Problem:** the agent needs its constitution, compiled from the Design
PRD — and key hygiene must be structural. **What changed:** SYSTEM_PROMPT
with role, context contract ("never invent macro numbers — the app
computes"), the verbatim cannot-do list, labeled output format, and
escalation triggers; settings panel storing the key in localStorage only.
**Verified:** key survives reload, never appears in the file; rules
verbatim.

## p02 · The skeleton

**What changed:** one self-contained `index.html`; all CSVs and policies
embedded as constants; plain list proving the world loaded and the joins
are right. **Verified:** 16 cases with correct linked context (Maya shows
"targets NOT STATED — capture path").

## p01 · The world (Gate 0 passed first)

**Problem:** no build starts on a blueprint that doesn't exist — and the
kit ships Northstar's world, not ours. **What changed:** PlateMate's
synthetic world in the kit's shape — 16 disruption cases, 2 clients,
7 plan meals, 18 state rows, 42 foods, 5 eval cases seeded into the data,
citable sectioned policies (A1–A7, S1–S7); Northstar files deleted.
Gate 0: all 8 blueprint checks passed against the approved
DISCOVERY.md/DESIGN.md. **Verified:** every eval case's records exist,
including the boundary case's silent-skipper state (counter 0, disclosure
only) and the seeded third-ask counter for the harder case held in
reserve.
