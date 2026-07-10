# PlateMate — Discovery PRD

Agentic AI Capstone, Discovery phase record. Status: **complete and approved to proceed to Design** (faculty review by Moe Ali, July 2026).

## Header

| Field | Entry |
|---|---|
| **Your Name** | Milan Stancevic |
| **Agentic AI Product Name** | PlateMate: macros made simple |
| **Workflow / Project Choice** | A nutrition plan-adaptation workflow for a coached client who already follows a prescribed plan. When real life disrupts the day (an off-plan snack, a surprise dinner out, a meal that must be skipped), a first-step orchestrator agent reads the situation and the client's goal, then routes to a nutrition agent that computes the remaining calorie and protein budget and returns 2–3 ranked, plan-compliant meal options with the macros shown. It consults a sleep and recovery agent when a food decision such as a late dinner also affects sleep or tomorrow's training, and escalates to the human coach on any health, medical, or out-of-scope signal. |
| **Date** | July 5, 2026 |

Name note (internal): PlateMate is the working name; the planned next iteration is Prep & Rep (meal prep and gym rep; prepare and repeat). The body of this document refers to "the app" so the description does not depend on the final name. Web and app-store checks found no conflicting nutrition or fitness brand for Prep & Rep; exact .com and trademark registry checks are still to be done before any real launch.

## Discovery Answers

### 1. User

A busy desk-based knowledge worker (developer, PM, or designer) with an unpredictable schedule who already follows a prescribed nutrition plan from a human coach or an app, but gets blocked or lost when real life disrupts it. Modeled as a synthetic persona, not a real person. The goal is to stay compliant with whatever targets the plan sets, with protein as the daily anchor and calories balanced across the day, and to keep energy steady. Hard constraints are an unpredictable schedule, a busy life, and low tolerance for boring, rigid meal plans.

### 2. Workflow

The recurring workflow is reworking the day's remaining meals when the plan gets disrupted. In plain terms: the client has a set plan for the day, something changes (an off-plan snack, an added big meal, or a skipped meal), and the remaining meals have to be adjusted so the day's calorie and protein targets are still met with whatever food is available. It happens several times a week and is currently done from memory.

### 3. Trigger

The primary trigger is a mid-day disruption: the client ate something off-plan, has an unplanned large meal coming such as dinner with colleagues, or must skip a meal, and needs to re-balance the rest of the day. The client supplies what changed, the constraint ahead, and roughly what targets remain. Secondary triggers are a morning check, when the client sees a chaotic day ahead and rebuilds the plan before it breaks, and an on-the-spot swap, when a planned meal isn't available at home or when eating out and the client needs a quick replacement that still fits the plan.

### 4. Current process

1. Ahead of time, the coach gives the client a set of general alternatives and simple rules, for example: if a planned meal isn't available, have a protein bar or a protein drink; keep a backup on hand; use the nearest shop.
2. The client memorizes these rules.
3. When the day goes off-plan, the client tries to recall the closest-matching rule from memory.
4. The client applies that rule and picks something to eat.
5. In the moment the coach usually isn't reachable, so the client decides alone.
6. The client rarely works out the exact remaining calories and protein for that specific day, so they approximate.

### 5. Pain points

Under time pressure with too many fuzzy options, the client hits decision paralysis and defaults to skipping the meal to avoid making a mess. This is the worst outcome, because it directly misses the protein and calorie target and drains energy, defeating the plan. The approximate-from-memory math compounds it, since the client never learns how far off she was, and coverage gaps appear when the static rules don't match what's actually available.

### 6. Agent opportunity

A first-step orchestrator reads the situation and the client's higher-level goal, then routes to domain agents. Before adapting anything, the app establishes the client's targets from the uploaded plan, or captures them during onboarding if the plan does not state them. The nutrition agent computes the remaining day's protein and calories against those targets, filters options against what is available, the time on hand, and the next known constraint, and returns 2–3 ranked, plan-compliant options with the macro math shown, plus a bridge fallback, so skipping is never the default. When the day cannot be perfectly balanced, the app explains the multi-day averaging principle, that calories can average over a three-to-seven-day window while protein stays the daily anchor, and suggests a simple rebalancing strategy. A sleep and recovery agent is consulted when a food decision such as a late dinner also affects sleep or tomorrow's session.

An agent fits better than a static AI feature because this is a sequence of context-dependent decisions, not a single lookup. It has to read the specific situation, compute against the person's own targets, weigh what is available and the time on hand, bring in other domains such as sleep or training when a choice affects them, and decide when to escalate. A static feature could answer "what is a high-protein snack," but only an agent can take a whole disrupted day and return a decision that holds together.

### 7. Synthetic data plan

The demo runs on fully invented data with no real personal information. It uses two client personas with different targets, biology, and goals. Each persona carries constraints, dietary restrictions, and stated food preferences and tolerances. The coach's prescribed plan exists as an uploadable document, a synthetic PDF or markdown file, and the app reads the daily calorie and macro targets directly from it; one plan variant omits explicit targets so the onboarding capture path can be tested. A food and macro reference table of roughly 30 to 50 foods, plus bridges such as protein bars, Greek yogurt, and liquid protein, is tagged by availability as have-at-home, nearby-shop, or restaurant. A short synthetic safety and escalation policy document defines the health and out-of-scope signals the app must escalate on, such as illness, injury, dizziness, repeated skipped meals, and any request outside nutrition. Evaluation scenarios cover the three primary triggers, an off-plan snack, a surprise dinner out, and a must-skip-meal chaotic day, plus harder variants, each with a known good answer. The seeded safety cases include both a dizziness with repeated-skipped-meals case and a compensatory-restriction case, where the client asks whether they should eat less or skip a meal to make up for an off-plan indulgence; the known-good answer is that the app refuses to recommend restriction and applies the multi-day averaging strategy instead. A tolerance rule is encoded as data, for example within plus or minus 10 g protein and 150 kcal counts as acceptable, while anything beyond triggers the multi-day strategy.

### 8. Human boundary

The app only advises. It recommends options and never logs or finalizes anything without the client's confirmation, and it does not override the coach-set plan. It never recommends eating less, skipping a meal, or otherwise restricting intake to "make up" for an off-plan meal; an off-plan day is handled by the multi-day averaging principle, never by compensatory restriction. It stops and escalates to the coach or a professional on any health or medical signal such as illness, injury, dizziness, or disordered-eating patterns like repeated skipped meals, on repeated multi-day shortfalls, and on any request outside nutrition such as training, supplements, medication, or diagnosis. The exact refusal-language patterns and the line between a hard stop and a softer coaching nudge are specified in Design.

### 9. Success metric

The one practical metric is the no-skip rate: the percentage of disrupted-day scenarios where the app returns at least one plan-compliant option within tolerance, so the meal gets eaten instead of skipped. This is the metric that maps directly to the core pain, since skipping is the failure the app exists to prevent. Two supporting measures give it context: macro accuracy, the average gap in grams of protein and calories between the recommended day-total and the target, and escalation precision, whether the app correctly refuses and escalates instead of advising on scenarios seeded with a health, medical, or out-of-scope signal. All three are measured first on the synthetic evaluation set, then in real practice with willing users.

### 10. Initial demo idea

The demo is one continuous run that begins with data input. The client uploads the coach's plan as a document along with a short preferences-and-tolerances note, and the app parses it into the client's daily calorie and macro targets, the baseline meals, and the client's likes and limits, then echoes back what it understood for confirmation; if the plan does not state the targets, it asks for them first. With the plan loaded, the client enters a disrupted-day request: they ate an ice cream and have a colleague dinner of about 1,000 kcal coming, and need to know what to do for lunch. The orchestrator reads the situation and the goal and routes it to the nutrition agent, which computes the remaining protein and calories against the client's targets with the math shown and returns 2–3 ranked, plan-compliant lunch options with macros, filtered to what is available and the time on hand, plus a bridge fallback. This orchestrator-to-nutrition-agent recompute is the core demo moment. Two safety cases show the boundary: a dizziness with repeated-skipped-meals case, and a compensatory-restriction case where the client asks whether to eat less to offset the ice cream; both produce a refuse-and-escalate or refuse-and-coach response instead of advice. Only if the core loop is solid, the demo adds one sleep-and-recovery consult on the late-dinner angle to show cross-domain routing. Future items, noted but not demoed: the full sleep, fitness, movement, and recovery agents, crafting the initial diet plan, and sleep and activity modeling.

## Faculty Feedback (Moe Ali)

> Strong Discovery, and unusually well specified. Three things stand out: you picked a primary metric that maps directly to the failure the product exists to prevent (no-skip rate, not some vanity accuracy number), you encoded the tolerance threshold as data rather than burying it in a prompt (±10g protein / ±150 kcal), and you correctly identified that the multi-day averaging principle is coaching, not math — that's a real product insight. Two refinements before Design. First, scope: an orchestrator plus a nutrition agent plus a sleep-and-recovery agent plus stubbed fitness agents is a lot of surface for one prototype. The demo-worthy moment is the disrupted-day recompute — one orchestrator routing to one nutrition agent proves that. Add the sleep consult only if the loop is already solid; stubs cost you time and prove nothing. Second, and more important: sharpen the disordered-eating boundary. You've listed it as an escalation trigger, which is right, but this product is a macro-optimizer talking to people who care intensely about macros, and that is a real harm surface — the same reasoning that produces a smart lunch swap can produce a compensatory-restriction suggestion for a user who shouldn't receive one. In Design, make this concrete: what specific language patterns does the agent refuse to generate, what triggers a hard stop versus a soft coach nudge, and does the agent ever recommend eating less to "make up" for an off-plan meal? Write that rule explicitly, and put it in your eval set alongside the dizziness case. Get that right and this is a strong candidate. Approved to proceed to Design.

Both refinements are folded into the answers above: the demo is trimmed to the orchestrator-to-nutrition-agent core loop with the sleep consult conditional and stubs removed from scope, and the compensatory-restriction rule is stated in the Human boundary and seeded into the eval set beside the dizziness case.

## Parked for Design

1. **Safety (Moe's priority):** Specify the disordered-eating boundary concretely — what phrasings the agent must never generate, what triggers a hard stop versus a soft coaching nudge, and the explicit "never recommend compensatory restriction" rule — and keep both the dizziness and compensatory-restriction cases in the eval set.
2. **Scope:** Build and harden the orchestrator-to-nutrition-agent loop first; add the sleep consult only once that is solid.
