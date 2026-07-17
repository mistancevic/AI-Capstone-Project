# Research Program — Validating the Journey Map with Real-World Evidence

Purpose: convert the journey map's estimated sentiment scores
([`assets/journey-map.png`](assets/journey-map.png)) from coaching-experience
hypotheses into evidence-backed findings, via six separate, labeled
investigations. Each investigation runs standalone (fresh chat, prompt below),
returns results in the standard output schema, and gets merged here and into
an evidence-annotated v2 of the map.

## The six investigations

| # | Investigation | Method (official label) | Channel | Expected output |
|---|---|---|---|---|
| 1 | Published evidence | Secondary / desk research (literature review) | Studies, industry reports | **DONE — see [`evidence-desk-research.md`](evidence-desk-research.md).** Logging valley supported (likely understated); disruption valley: pain supported, mechanism corrected (binge, not just skip); rigidity-as-feature; plateau≠boredom split. |
| 2 | Tracker complaints | Review mining (Voice of Customer) | App-store reviews | **DONE — see [`evidence-review-mining.md`](evidence-review-mining.md).** Logging valley supported again (understated); disruption need is LATENT (zero complaints — coach side feels it); guilt-free = table stakes (MacroFactor owns it); skip-mechanism contradicted 2nd time. |
| 3 | Users in their own words | Netnography / social listening | Reddit, forums | **DONE — via Gemini Deep Research (Reddit-capable); see [`evidence-netnography.md`](evidence-netnography.md).** The (g) split answered: binge modal (~45–50%), adapt (~30–35%), skip minority (~15–20%); disruption confirmed deepest via AVE cascade; understand-the-plan gets first verdict (~0); strategic-vs-maladaptive skip split is a new design requirement. Literature fallback retained as [`evidence-lapse-literature.md`](evidence-lapse-literature.md). |
| 4 | How incumbents serve the journey | Competitive UX audit / teardown → gap analysis | Competitor apps + public materials | **DONE — see [`evidence-competitive-teardown.md`](evidence-competitive-teardown.md).** Wedge is NOT empty whitespace: MFP shipped a pull-based "what should I eat now?" chatbot (Jun 2026); Mealner claims the identical wedge (waitlist). Surviving ground = initiation + acting on the answer + coach-visible record (nobody owns all three). Social-events is the cleanest empty field. MacroFactor's "do nothing" counter-thesis logged. |
| 5 | The coach's side | Expert / key-informant research + trade research | Coach forums, interviews | **DONE (desk, Part A) — see [`evidence-coach-side.md`](evidence-coach-side.md); weakest/most disconfirming pass.** No coach-attributed churn, no coach time-cost, no WTP signal, zero support for skip-mechanism; a segment of coaches ideologically *reject* mid-week monitoring. Best number is client-side (37% exit on competing priorities, Zizzi 2016). Coach-channel thesis demoted to primary-research hypothesis. Part B interview guide drafted. |
| 6 | Our own numbers | Primary research (survey) | ~100-peer cohort | The only first-party data; validates scores |

Sequencing: 1 first (cheapest, frames everything) → 2 + 3 in parallel
(valley validation) → 4 (needs valleys confirmed to know where to look) →
5 alongside → 6 last (questions get sharper after seeing how people talk
about the pain in the wild). Triangulation rule: a valley counts as
validated when at least three independent channels support it.

## The synthesis artifacts (a separate list)

Data collection gathers evidence; synthesis turns evidence into decisions.
The investigations above feed the artifacts below — the journey map is not
an investigation, it is the canvas the investigations' findings land on.

| # | Artifact | Method (official label) | Consumes | Status |
|---|---|---|---|---|
| 1 | Client persona | User persona (synthetic) | Coaching experience, segment definition | Done (Discovery) |
| 2 | **Journey map with sentiment curve** | **User/customer journey mapping — the emotion-curve variant is an experience map; score overlays make it quantified journey mapping** | All six investigations | v1 done (hypothesis, EST-labeled); v2 evidence-annotated planned after investigations return |
| 3 | Pain-point scorecard | Pain-point prioritization (magnitude / frequency / severity / competition / contrast) | Journey map + evidence | Done (Discovery notes §2) |
| 4 | Idea ranking | Impact × feasibility prioritization matrix (diverge/converge) | Ideation | Done (Discovery notes §3) |
| 5 | Competitive gap matrix | Gap analysis | Investigation 4 | Done (evidence-competitive-teardown.md §gap matrix) |
| 6 | Positioning set | Positioning statements, category definition, strategy test | Everything above | Done (strategy-notes.md) |

## Standard output schema (all prompts request this)

1. **Evidence table:** journey activity → finding → source (URL + date) →
   strength (strong / moderate / weak).
2. **Quotes:** short verbatims (≤ 25 words) with links.
3. **Numbers:** any hard statistic with its citation.
4. **Disconfirming evidence:** anything that contradicts the hypothesis —
   mandatory section, honesty over comfort.
5. **Verdict per valley:** supports / contradicts / no signal, against the
   estimated scores.

## Shared context block (paste at the top of every prompt)

```text
Context: I am validating a user-journey hypothesis for a nutrition app
concept. Persona: busy desk professionals (developers, PMs, designers)
following a nutrition plan prescribed by a human coach or an app. Journey,
3 stages / 10 activities: GET MY PLAN (find coach/app; onboard; understand
the plan) → LIVE MY PLAN (shop & meal-prep; eat & log daily; handle
disruptions when the day breaks; social events & travel) → REACH MY GOAL
(progress reviews with coach; plateaus & boredom; adjust goal). Hypothesized
pain valleys (estimated sentiment, -100..+100): understand-the-plan +5,
eat-&-log-daily -12 (logging fatigue), handle-disruptions -25 (deepest:
decision paralysis when the plan breaks mid-day, default becomes skipping
the meal), social-events-&-travel -10, plateaus-&-boredom -15. I need
EVIDENCE, not opinions: real sources with URLs and dates, short verbatim
quotes, hard numbers where they exist, and a mandatory section for
disconfirming evidence. Do not invent sources; if a claim can't be sourced,
say so.
```

---

## Prompt 1 — Desk research (secondary / literature review)

```text
[paste shared context block]

Task: literature and industry-report sweep. Find published, citable
evidence on: (a) dietary-adherence drop-off over time in coached or
self-directed nutrition plans; (b) food-tracking app abandonment — rates,
timelines, and stated reasons (logging burden especially); (c) meal
skipping under time pressure and decision fatigue in working adults;
(d) plan rigidity vs. flexibility and its effect on adherence (rigid vs.
flexible dietary restraint literature); (e) what happens to adherence
between coaching check-ins. Prefer peer-reviewed studies and large-sample
industry surveys; note sample sizes and years. Return results in this
schema: evidence table (journey activity → finding → source URL + date →
strength), hard numbers with citations, mandatory disconfirming-evidence
section, and a verdict per hypothesized valley (supports / contradicts /
no signal).
```

## Prompt 2 — Review mining (Voice of Customer)

```text
[paste shared context block]

Task: review mining of nutrition/tracking apps. Apps: MyFitnessPal,
Lose It!, MacroFactor, Lifesum, Yazio, Mealime (add others you find
relevant). Mine publicly visible app-store reviews and review roundups for
1–2 star complaint themes AND 5-star praise themes. Classify every theme
against the 10 journey activities. I care most about: logging burden and
abandonment (eat-&-log-daily), anything describing the moment a day goes
off-plan and the app not helping (handle-disruptions), guilt/shame
mechanics, plan boredom, and social-eating or travel struggles. Return:
ranked complaint themes with approximate frequency and which apps they
attach to, 8–12 short verbatim quotes (≤25 words) with links, praise
themes (what incumbents do well — honesty required), the mandatory
disconfirming-evidence section, and a verdict per hypothesized valley.
```

## Prompt 3 — Netnography (social listening)

```text
[paste shared context block]

Task: netnography across public communities. Sources: Reddit (r/loseit,
r/nutrition, r/fitness, r/MacroFactor, r/1200isplenty, r/gainit,
r/xxfitness, coaching-related subs), plus any active fitness/nutrition
forums. Find real threads where people describe: (a) the plan breaking
mid-day — surprise meals, meetings eating lunch, and what they did next;
(b) skipping a meal because they didn't know what fit the plan;
(c) logging fatigue and quitting trackers; (d) guilt after off-plan
eating and compensation behavior (eating less to "make up for it");
(e) plan boredom and drift; (f) travel/social-event struggles; (g) what
people report actually doing right after breaking the plan mid-day:
skipping, bingeing, or adapting — I want the split. Return:
per-theme thread count impression (common / occasional / rare), 10–15
short verbatim quotes (≤25 words) with links and dates, which journey
activity each maps to, the mandatory disconfirming-evidence section, and
a verdict per hypothesized valley. Ethics: public posts only, no
usernames in the output.
```

## Prompt 4 — Competitive UX audit / teardown → gap analysis

```text
[paste shared context block]

Task: competitive teardown against the journey. Competitors: MyFitnessPal,
MacroFactor, Lifesum, Mealime, Mealner (mealner.com — closest concept),
and one coach-platform (Trainerize or a similar coach-client app). Using
public materials — product sites, help centers, feature docs, review
descriptions, walkthrough videos — map each competitor against the 10
journey activities: what feature (if any) serves that activity, how well
(served / partially served / unserved), and evidence for the rating.
Apply one probe scenario everywhere: "mid-afternoon, the user ate
something off-plan and has a big dinner coming — does the product tell
them what to eat NOW to stay on plan?" Return: a gap matrix (activity ×
competitor, served/partial/unserved), per-competitor notes on the probe
scenario, where the whitespace is (activities no one serves), the
mandatory disconfirming-evidence section (who comes closest to serving
the disruption moment), and a verdict per hypothesized valley. Note:
ratings from public materials only — flag anything that needs hands-on
verification, and I will verify those in the apps myself.
```

## Prompt 5 — Expert / key-informant research (coach side)

```text
[paste shared context block]

Task, part A (desk): find coach-side evidence — trainer and nutrition-coach
forums, industry surveys, blog posts, and reviews of coach platforms
(TrainerFu, Trainerize, etc.) — about: how coaches monitor client adherence
between check-ins, how much time they spend answering routine "what do I
eat instead" questions, when they find out a client fell off the plan, and
client churn attributed to "life happening." Return in the standard schema.

Task, part B: draft a short key-informant interview guide (8 questions,
≤10 minutes) I can run with 3–5 real coaches, covering: how they build
plans, what happens between check-ins, how clients report disruptions,
what they'd want flagged vs. handled automatically, tone concerns around
compensation/restriction language, and willingness to pay for an
adherence tool for their roster. Neutral wording, no leading questions,
no mention of my product concept until a final optional section.
```

## Investigation 6 — Peer survey (primary research; ours to field)

Instrument (5 questions, ~2 minutes, for the ~100-person cohort):

1. When did you last skip a meal because you didn't know what to eat that
   would fit your plan? (this week / this month / can't remember / never)
2. In a normal week, how many times does real life (meetings, events,
   travel, cravings) break your planned eating? (0 / 1–2 / 3–5 / 6+)
3. What do you do when it happens? (open text)
4. How do you feel about logging food daily? (love it / tolerate it /
   avoid it / quit apps because of it)
5. If an app could tell you, in under a minute, exactly what to eat next
   to stay on your plan when the day breaks — would you use it? Would you
   pay? (use: yes/no; pay: yes/no/only if my coach recommends it)

Q1–Q2 validate the -25 valley frequency; Q4 validates -12; Q3 is the
open-text goldmine; Q5 probes willingness to pay and the coach-channel
hypothesis in one stroke.

---

## Merge protocol

Results from each investigation come back to the main session and are:
1. condensed into an evidence section per valley in `discovery-notes.md`,
2. rendered into an evidence-annotated v2 of the journey map (same HTML
   format, valleys carrying citation counts and one quote each),
3. weighed by the triangulation rule (3+ independent channels = validated).
