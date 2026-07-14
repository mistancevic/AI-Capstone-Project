# Discovery Working Notes

Status: **working notes, not the PRD.** The approved Discovery record is
[`DISCOVERY.md`](../DISCOVERY.md); nothing here overrides it. These notes
capture the deeper Discovery thinking done against the Product Faculty
4D-method lesson (Module 4, Lesson 1: journey mapping, pain sizing,
diverge/converge), for use in the project presentation and future product
work. Sentiment scores and idea rankings below are **hypotheses from
coaching experience**, to be validated — they are not measured data.

---

## 1. Journey map — the coached client

Modeled on the Shopify merchant journey slide (3 stages, activities per
stage, sentiment curve with valleys). Scores are NPS-style estimates
(-100..+100) from direct coaching experience, not survey data yet.

### Stage 1: GET MY PLAN

| Activity | Est. sentiment | Notes |
|---|---|---|
| Find a coach or an app | +30 | Hopeful, motivated, shopping around |
| Onboard and share needs, habits, goals | +40 | Honeymoon peak — someone finally listens |
| Understand the plan and targets | +5 | First dip: jargon, macros, "why this number?" |

### Stage 2: LIVE MY PLAN (daily loop — highest frequency stage)

| Activity | Est. sentiment | Notes |
|---|---|---|
| Shop and meal-prep | +15 | Routine effort, manageable |
| Eat and log daily | +10 | Fine while life cooperates; logging fatigue builds |
| **Handle disruptions (day goes off-plan)** | **-25** | **Deepest valley.** Decision paralysis → skip the meal → target missed, energy gone, guilt loop |
| Eat out, social events, travel | -10 | Uncertainty and guilt; "I'll just start again Monday" |

### Stage 3: REACH MY GOAL

| Activity | Est. sentiment | Notes |
|---|---|---|
| Review progress with the coach | +20 | Human connection, accountability — the part coaching does well |
| Push through plateaus and boredom | -15 | Second valley: rigid, repetitive plans; motivation dips |
| Adjust the goal, next phase | +10 | Renewed purpose when handled well |

### Reading the map

- **PlateMate v1 attacks the -25 valley**: handle-disruptions is both the
  lowest point and sits in the highest-frequency stage (hit daily, several
  disruptions per week). Frequency × severity — the two dimensions the
  lesson weights most — both peak here. This is the after-the-fact proof
  that the capstone workflow choice was right.
- **The other valleys are the roadmap, not leftovers**: plan boredom and
  variety (-15), social eating and travel (-10), understand-my-plan (+5,
  the ingestion/"explain my plan" opportunity). Future work is the rest of
  a mapped landscape.
- Presentation idea: render this as a sentiment curve over the three
  stages, Shopify-slide style, with the -25 valley highlighted and
  "PlateMate v1" pinned to it.

---

## 2. Five-question pain scorecard (handle-disruptions valley)

| Question | Assessment |
|---|---|
| **Magnitude** — how many have this pain? | Everyone following a prescribed plan (coach- or app-set) whose life is unpredictable — i.e., most working adults on a plan. Direct reachable sample: ~100-person peer cohort in the same fitness challenge. |
| **Frequency** — how often? | Several times a week; the disruption is the norm, not the exception. |
| **Severity** — how bad? | The default response (skip the meal) directly defeats the plan's purpose: missed protein, energy crash, guilt loop, and over time churn from coaching. |
| **Competition** — who else solves it? | Trackers (MyFitnessPal, MacroFactor, MacroMate) log the past but don't decide the remaining day. Coaches are async and don't scale to in-the-moment. Coach-side triage tools (e.g., TrainerFu pattern) flag drift but leave the client alone in the moment. The in-the-moment adaptation slot is unowned white space. |
| **Contrast** — complaints against existing solutions? | The standing complaint against trackers is exactly the wedge: they make you feel bad about what happened instead of telling you what to do next. Rigid plans + guilt loop = abandonment. |

Lesson's guidance: if you pick two, pick frequency and severity — both max
out here.

---

## 3. Diverge / converge (reconstructed idea list)

Ideas touched during Discovery, scored impact × feasibility (1-10, draft
judgment). Winner chosen originally by narrative convergence; the scorecard
confirms it.

| Idea | Impact | Feasibility | Verdict |
|---|---|---|---|
| **Disrupted-day recompute (plan adaptation)** | **9** | **9** | **Winner: highest-frequency pain, deterministic math, low autonomy risk** |
| Meal-variety generator (anti-boredom) | 7 | 8 | Strong v2 — attacks the -15 valley |
| Plan ingestion + "explain my plan" | 6 | 7 | Partially in v1 (ingestion); explain-mode later |
| Weekly review digest (client-facing) | 6 | 7 | Complements coach digest already designed |
| Coach triage dashboard | 8 | 5 | Second user + second interface = second product; future |
| Restaurant menu scanner | 7 | 5 | Photo → macros is noisy; later |
| Grocery-list builder | 5 | 8 | Useful, not differentiating |
| Initial diet-plan crafting | 8 | 4 | Contradicts positioning (we adapt an existing plan); high autonomy risk; explicitly out |
| Food ordering integration | 6 | 3 | Real-world actions, payments, liability; explicitly v2+ |

---

## 4. Validation plan (turning intuition into data)

The missing quantitative leg (Shopify had NPS; we have none). Cheapest fix:
a 3-question warm survey to the ~100-peer cohort:

1. When did you last skip a meal because you didn't know what to eat?
2. How many times in a normal week does your day break your meal plan?
3. What do you do when it happens?

Even ~20 responses converts "my friend has this problem" into "N of 20
skipped a meal last week." Optionally add a per-stage mini-score ("how do
you feel about X part of following your plan?") to validate the journey-map
sentiment estimates with real numbers.

---

## 5. Business impact framing

- **Coach capacity**: automating routine adaptation lets one coach serve
  more clients without diluting the human connection — the app absorbs the
  data lifting, the coach keeps the psychology (the TrainerFu division of
  labor).
- **Coach revenue and retention**: clients who stop skipping stay on plan,
  see results, and renew; adherence is the strongest churn lever a coaching
  business has.
- **Monetization surface**: the coaching packages ladder (Essential /
  Standard / Premium) designed in the Design phase is itself the pricing
  model — escalation access is the paid differentiator.
- **Product thesis (verbatim, for the presentation)**: "the app takes over
  the routine work so the coach is left with what only a human can do — the
  genuine connection."

---

## 6. Lesson ↔ project validation map

- **Step-change AI fit** ("not every problem is an AI problem"): adapting a
  known plan to a disrupted day = reasoning + personalization on
  deterministic math; confirmed independently by faculty review.
- **Feasibility inversion** (PM owns intelligence feasibility upfront): done
  literally — the pre-Design prototype spike proved the core loop before
  Design started. Name it this way in the presentation.
- **Qual + quant** ("intuition tells you where to look, data tells you
  whether you're right"): qualitative side unusually strong (builder is a
  practicing coach); quantitative side = survey above, pending.
- **Frequency + severity screening**: both max out on the chosen pain.

---

## 7. Open threads (carried from the Design audit)

1. Add the synthetic coach-client agreement document to the demo data
   inventory (born in Design rows 22/26; missing from Discovery row 15's
   list — one sentence fixes it).
2. Add one conditional sleep-consult eval case (rows 14/18/20 promise it;
   row 28 doesn't test it yet).
3. Align trigger counting language ("primary + two secondary" vs "the five
   trigger forms") in row 21.
4. Add a standalone 2-days-skipped-meals eval case (counter-only path, no
   keywords).
5. Design rows 23 (tools) and 25 (output) are working versions pending the
   4D Design lesson.
6. Awaiting Moe's preference: change-notes as cell notes vs. in-cell update
   markers.
