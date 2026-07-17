# PlateMate Safety & Escalation Policy (synthetic)

The deterministic floor. This file is the single source for signal lists,
counter thresholds, flag tiers, delivery rules, and every pre-authored
message on a path where a bad sentence could do damage. The code reads the
marked blocks; the model never authors stop or nudge wording.

PlateMate only advises. It recommends options, never logs or finalizes
anything without the client's confirmation, and never overrides the
coach-set plan. The screen implementing this policy runs before any
routing and before any language model is consulted.

## Signal lists

**Health / medical** (any hit → hard stop, urgent flag, GET HELP NOW):
dizzy, dizziness, faint, fainted, lightheaded, light-headed, chest pain,
fever, nausea, vomiting, can't keep food down, injury, heart racing.

**Disordered-eating / restriction family:**
- Multi-day undereating self-report (e.g. "haven't eaten properly for
  days") → hard stop, urgent.
- Explicit restriction demand below the compliance floor (e.g. "give me an
  800-kcal plan") → hard stop, urgent. The compliance floor is code: no
  day is ever built below the plan's baseline, under any phrasing.
- Compensatory ask ("should I eat less to make up for it?", skip-intent
  "I just won't eat then") → tier by counter, see thresholds.
- purge, laxative, punish myself, hate my body → hard stop, urgent.

**Out-of-scope** (decline + point to coach; digest entry only):
medication, prescription, diagnosis, supplements, steroids, fat burner,
training plan / program changes, plan-target changes.

**Hostility alone** ("this app is useless") → never a safety verdict:
calm acknowledgment, normal card, digest entry. Anger changes the tone of
the reply, never the verdict; the highest-severity signal governs.

## Counter thresholds

- Skipped-meals counter ≥ 2 consecutive days → hard stop, urgent flag.
  (Strategic/declared skips are out of counter scope — future distinction
  per evidence-netnography.md; v1 counts unexplained skips only.)
- Compensatory asks: 1st and 2nd in a rolling 7-day week → run continues,
  templated nudge replaces the coaching line, counter increments, digest
  entry per flag scope. **3rd in the rolling week → hard stop, urgent.**
- Counters count knowledge, not silence, and survive raw-message deletion
  (counts persist; texts do not).

## Flag tiers and delivery

| Tier | Delivery |
|---|---|
| **Urgent** | Immediately if inside waking hours; queued and delivered at quiet-hours window-open otherwise, marked urgent, top of inbox |
| **Normal** | With the daily digest |
| **Digest** | Rolled into the weekly digest, count-only, per the agreement's flag scope |

Quiet hours delay *notification*, never *protection*: the client-side stop
message, safe default, and (for medical signals) GET HELP NOW are always
immediate. The client sees every flag and its delivery time. The flag
carries reason codes and counter history as counts — never message texts;
the triggering message is delivered once per the coaching agreement.

## Pre-authored wording (code reads these blocks verbatim)

<!-- block:stop_why -->
I'm stepping in instead of answering, because what you wrote tells me food math is not what you need right now.
<!-- end -->

<!-- block:stop_safe_default -->
Safe default: eat your planned meal as written. No adjustments today.
<!-- end -->

<!-- block:stop_averaging -->
One rough day changes almost nothing across a week — calories average out over 3-7 days, and your plan already accounts for that.
<!-- end -->

<!-- block:get_help_now -->
GET HELP NOW: if you feel unwell — dizzy, faint, or worse — please contact a medical professional or someone near you right away. Your coach has been flagged, but they are not an emergency channel.
<!-- end -->

<!-- block:stop_flag_notice -->
Your coach has been sent an urgent flag about this ({delivery}). You see exactly what they see: the reason codes and this conversation's trigger, once, per your agreement.
<!-- end -->

<!-- block:nudge_compensatory -->
I hear that today feels heavy — and eating less now to cover what already happened is the one trade I won't help with, because it always costs more than it pays. Here are real options that keep you fed and keep the plan alive.
<!-- end -->

<!-- block:refusal_floor -->
I can't build you a day below your plan's baseline — that's a line this app never crosses, no matter how it's asked.
<!-- end -->

<!-- block:decline_out_of_scope -->
That's one for your coach, not for me — I only adapt the plan you already have. I've noted it in your weekly digest.
<!-- end -->

<!-- block:capture_targets -->
Your uploaded plan doesn't state daily calorie and protein targets. Tell me the targets (or ask your coach) and I'll take it from there — I won't guess numbers for you.
<!-- end -->

<!-- block:clarify_question -->
I want to get this right and I'm missing the shape of the day. What happened — something extra, a meal you'll miss, or a big meal coming up? If it's easier, pick one of the presets below.
<!-- end -->
