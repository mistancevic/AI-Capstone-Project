# Evidence — Investigation 4: Competitive Teardown → Gap Analysis

Status: **completed.** Public-materials pass across MyFitnessPal, MacroFactor,
Lifesum, Mealime, Mealner, Trainerize. Ratings are from product sites, help
centres, App Store listings, and third-party reviews — **not hands-on**; the
run flagged a verification list (below) that is ours to close in the apps.
Sources not yet spot-checked. This is the competitive gap matrix (synthesis
artifact 5).

Caveat the run states plainly: a teardown tests whether the *market has
responded* to a pain, not whether the pain *exists*. Absence of a feature is
weak evidence of pain. These verdicts speak to **positioning**, not to the
journey-map sentiment scores.

## The headline: the wedge is not empty white space — it is narrow, defensible ground

The premise "no one serves the disruption moment" is **false as stated.**
Two independent parties are already on it:

1. **MyFitnessPal shipped Nutrition Coach (help doc dated Jun 11, 2026)** —
   a chatbot grounded in today's diary plus ~2 weeks of history that fields
   the exact probe: *"What should I eat with my remaining calories?"* /
   *"What should I eat right now?"*, with a suggested-prompt of
   "Am I on track with my goals today?". It answers our question.
2. **Mealner (mealner.com, waitlist)** is our hypothesis verbatim as a
   landing page — "the meal you ate becomes a fixed point… re-planned the
   rest of your day", "no streaks, no shame, no red numbers", upload your
   nutritionist's plan. Not shipped (no App Store listing, no pricing), but
   independent convergence on the identical wedge *including the tone*.

**What is still unowned** (the narrowed, surviving wedge):
- **Nobody *initiates*.** Every product waits to be asked. MFP Coach is
  pull-based — the user must open the app at 3pm and type. The person least
  likely to do that is the one who just ate the thing.
- **MFP Coach cannot act on its answer** — it "cannot log food for you and
  cannot edit your goals"; it answers, then hands the work back.
- **No coach-visible record of the moment.** No product combines
  (a) automatic detection of a broken day + (b) a specific pushed
  instruction + (c) a coach-visible record of it. Trainerize owns (c),
  MFP nearly has (b), **no one has (a).**
- **MFP Coach is barely distributed:** iOS-only, English-only, Premium/
  Premium+, 6 countries, still rolling out.

The strategic read, in one line: **our defensibility was never the re-plan
calculation** (MFP does that math; Mealner claims it) — **it is the trigger
and the coach handoff.** This is exactly what strategy-notes already says
(answer 9: assume the feature is copied; the moat is the combined operating
model — coach-owned plan, escalation, traceability, roster distribution).
The teardown *confirms* that position and kills the weaker version of the
pitch.

## Gap matrix (activity × competitor)

● served · ◐ partial · ○ unserved · ? claimed but unverifiable (pre-launch)

| # | Activity | MyFitnessPal | MacroFactor | Lifesum | Mealime | Mealner | Trainerize |
|---|---|---|---|---|---|---|---|
| 1 | Find coach/app | ○ | ○ | ○ | ○ | ○ | ◐ |
| 2 | Onboard | ● | ● | ● | ● | ? | ● |
| 3 | Understand the plan | ● | ● | ◐ | ○ | ? | ● |
| 4 | Shop & meal-prep | ● | ○ | ● | ● | ○ | ● |
| 5 | Eat & log daily | ● | ● | ● | ◐ | ? | ● |
| 6 | **Handle disruptions** | ◐ | ○ | ○ | ○ | ? | ◐ |
| 7 | **Social events & travel** | ◐ | ○ | ○ | ○ | ○ | ○ |
| 8 | Progress reviews w/ coach | ◐ | ○ | ◐ | ○ | ○ | ● |
| 9 | Plateaus & boredom | ◐ | ◐ | ◐ | ◐ | ? | ◐ |
| 10 | Adjust goal | ◐ | ● | ◐ | ○ | ? | ● |

MFP's ◐ on activity 6 = pull-based chatbot that can't act; Trainerize's ◐ =
a swap-time macro-misalignment *notification* (fires on a planned swap, not
a logged deviation; warns rather than re-plans; real fallback is the client
messaging the coach — high-latency, doesn't scale).

## Whitespace, ranked

1. **Social events & travel (activity 7) — the cleanest empty field.**
   Zero features across all six. No pre-event budgeting, no travel mode.
   Competitively *emptier than the disruption moment* — under-priced at −10
   relative to disruptions at −25. Worth promoting in the roadmap story.
2. **Push-based disruption response (activity 6, initiation).** MFP has the
   capability and doesn't use it proactively. Detection of "this log broke
   the day" + initiation exists nowhere.
3. **Coach handoff of the moment (activity 6 × 8).** The (a)+(b)+(c)
   combination is unowned.
4. **Boredom as distinct from plateau (activity 9).** Split between two
   product categories, addressed by neither. MacroFactor solves the
   metabolic plateau algorithmically (its headline); recipe apps churn
   variety; **no one solves both.** Confirms the investigation-1 split.

**Do NOT build here (commoditised):** onboarding, daily logging (photo/
voice/barcode is table stakes across all six), grocery lists, database
scale (MFP's 20.5M foods is not a winnable axis).

## Verdict per hypothesised valley (positioning lens)

| Valley | Estimate | Verdict | Reasoning |
|---|---|---|---|
| Understand the plan | +5 | No signal | Well-served (MacroFactor publishes its algorithm; MFP Coach explains). Teardown says nothing about sentiment. |
| Eat & log daily | −12 | No signal (competitive) | Six products converged on fast logging in ~18 months — circumstantial support for logging fatigue, not proof. Supporting stats are vendor-blog garbage (see below). |
| **Handle disruptions** | −25 (deepest) | **Contradicts as stated / survives as narrowed** | "No one serves this" is false (MFP, Jun 2026). "This is where the plan breaks" is *supported* by three unprompted parties (MFP's 2024 Calorie-Goals-by-Meal copy, Mealner's homepage, an MFP community feature request). **Rewrite the wedge as: served only reactively, on iOS, behind a paywall, in 6 countries, by a chatbot that can't act and never initiates.** |
| Social events & travel | −10 | **Supports (cleanest whitespace)** | Zero features anywhere. Competitively the emptiest field. |
| Plateaus & boredom | −15 | Partially contradicts | Plateau half solved well by MacroFactor; boredom half unserved. Confirms the split (investigation 1). |

## Disconfirming evidence — the part that must change the pitch

1. **MFP shipped a pull-based version of our wedge ~5 weeks before this
   run.** The honest claim is no longer "whitespace" but "no one initiates
   it, acts on it, or ties it to the coach — and the one who answers it is
   iOS/Premium/6-country."
2. **MFP has described our exact pain valley in its own marketing since
   2024** (Calorie Goals by Meal: "it's dinner time and you have way too
   many or way too few calories left") and shipped a *weak* answer (static,
   user-entered per-meal budgets that never redistribute). A big incumbent
   has looked at this for two years. Our bet requires "they under-valued
   it," not "it's unsolvable."
3. **Mealner independently converged on identical positioning and tone** —
   the differentiation is not the re-plan concept itself.
4. **MacroFactor's counter-thesis is credible and evidence-backed.** A team
   with scientific standing *deliberately refuses* intra-day re-planning:
   daily variance is noise, the correct response to one off-plan lunch is
   nothing. They attack the same emotional pain (shame, "day is ruined") by
   **removing the verdict** rather than **issuing a correction.** If they
   are right, the −25 valley is real but a mid-afternoon "eat this now" push
   could read as exactly the surveillance-y nagging our persona is fleeing.
   *This is the sharpest strategic challenge on record — see response below.*
5. **Trainerize is a channel threat, not just a competitor.** It already has
   the client relationship, the plan, the log, the compliance score, and the
   swap-warning primitive. For them a re-plan is a feature; for us it is a
   company.

Closeness-to-the-disruption-moment, ranked: MyFitnessPal (shipped, pull,
narrow) > Trainerize (warning primitive + human fallback) > Mealner (claims,
ships nothing) > MacroFactor (deliberate refusal) > Lifesum (unknown) >
Mealime (n/a).

## Our answer to the MacroFactor counter-thesis (must be in the deck)

MacroFactor is right *for its user* — a self-directed tracker with no coach,
optimising multi-day energy expenditure, where a single lunch is noise. We
are not that product and do not serve that user:

- **Different customer.** Ours is a **coached** client whose **coach has
  prescribed** adherence and who **opted into** in-the-moment help through
  that coach. The intervention is consented and coach-governed, not imposed.
- **Different failure mode.** MacroFactor's "do nothing" answer assumes the
  user *tolerates* the deviation calmly. Our netnography (investigation 3)
  shows the modal reaction is the AVE binge cascade — "day's ruined, start
  tomorrow" — which "do nothing" does not interrupt. We are not correcting
  the *calories*; we are interrupting the *belief that the day is ruined*.
- **We already removed the verdict too.** Banned compensation language, no
  red zones, pivot-as-success, multi-day averaging — we agree shame is the
  enemy. We add *direction* on top of *no-shame*, only when the client
  asks and the plan permits it.
- **Delivery, not surveillance.** Pull-with-consent + quiet hours +
  advise-only autonomy + coach-set escalation. The design already answers
  "is this nagging?" with no. Keep it that way — do not add unprompted
  push as a default; make initiation an opt-in the coach and client set.

Net: the teardown does not break the thesis, but it forbids the lazy
version of it. Retire "no one serves this moment." Say instead: *the moment
is answered today only reactively, generically, and invisibly to the coach —
we detect it, act on it within a coach-prescribed plan, and leave the coach
a record.*

## Numbers worth keeping (and the ones to refuse)

Keep: MFP Coach is iOS-only / English-only / 6 countries / Premium (narrow
distribution of the nearest competitor); MFP Meal Planner floors at 1,200
(women) / 1,500 (men) kcal; Mealime ~5M users; Lifesum 65M (self-reported);
MacroFactor has **no coach portal** ("we don't currently have a built-in
coaching portal" — tells coaches to have clients export spreadsheets).

**Refuse (do NOT put in a deck):** the logging-attrition percentages that
flood vendor blogs — "80% quit in 2 weeks" / "70% in 2 weeks" / "50% in 3
weeks" — mutually contradictory, all competitor-product blogs, none linking
a primary study. The one semi-traceable chain is a scoping review's ~70%
discontinuation within 100 days (secondary). If logging fatigue must be
quantified for the deck, it needs its own PubMed pass — investigation 1's
Kidman 2024 (86% diet-app abandonment, n=525,824) remains the citable one.

## Verification list (ours to close, hands-on)

- **Lifesum** — does the new "AI Nutrition Coach" do intra-day guidance?
  (highest-value unknown in this teardown)
- **MFP Coach** — run the probe at 3pm with a real off-plan log: does it
  account for a *known upcoming* dinner, or only remaining calories? Does it
  ever push unprompted?
- **MacroFactor** — any in-app "remaining macros" surface not in public docs?
- **Trainerize** — does the client app show the coach's plan re-weighted
  after a logged deviation, or only compliance-to-date? Is there a
  client-facing coach directory (activity 1)?
- **Mealime Pro** — is the calorie filter responsive to anything logged, or
  static plan-time filtering?

## Program consequences

- Synthesis artifact 5 (competitive gap matrix) → **done.**
- Strategy notes updated: wedge re-narrowed (initiation + action + coach
  record, not "empty moment"); MacroFactor counter-thesis + response added;
  Trainerize logged as the channel threat; social-events promoted as the
  cleanest whitespace.
- Journey map v2: no sentiment change from this channel (positioning-only),
  but the disruption-valley annotation should carry the narrowed claim, and
  social-events deserves a "cleanest competitive whitespace" note.
- Triangulation unaffected (teardown is a positioning channel, not a
  sentiment channel) — the 3-channel valley verdicts from investigations
  1–3 stand.
