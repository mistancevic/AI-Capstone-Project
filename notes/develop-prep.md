# Develop Phase — Preparation (mapping the two Develop lessons onto PlateMate)

Purpose: orient for the Develop phase before it starts, the way we prepared
for Design. This maps every concept from the two Develop lessons — Lesson 1
(model selection + prompt engineering / output optimization) and Lesson 2
(RAG, fine-tuning, evaluation) — onto where PlateMate's **Design already
answers it** and what is **genuinely open**.

**Gate: no Develop build work until the Develop guide is issued.** This is
planning, not building.

## The one big finding

PlateMate is unusually well-positioned for Develop because the Design
deliberately pushed the model to the edges: **exactly two LLM calls
(`parse_situation`, `coaching_line`), everything else deterministic code
over named files, and the app runs correctly with the model off.** For most
products Develop is a large LLM-optimization lift; for PlateMate the LLM
surface is tiny and sits behind a deterministic floor, so most of the
lessons' machinery (RAG pipelines, fine-tuning, heavy prompt frameworks) is
**not needed** — and the parts that matter (prompt engineering + evaluation)
are already scaffolded in DESIGN.md.

---

## Pillar 1 — Model selection (Lesson 1)

Only two calls to select a model for, both low-stakes language jobs behind
the deterministic floor.

| Factor | PlateMate position | Decision |
|---|---|---|
| **Quality** | `parse_situation` only extracts structured fields; `coaching_line` is one sentence, screened by the banned-language filter and replaceable by a deterministic fallback. Model errors cannot produce unsafe output — the floor catches them. | Modest bar; a strong current Claude model clears it comfortably. |
| **Latency** | Single-turn, one card per request; not a streaming/chat product. | A fast model is fine; no special latency engineering. |
| **Scale** | Capstone demo scale; trivial RPM/TPM. | Non-issue. |
| **Data security** | **Synthetic data only; no real PII is ever stored** (memory design). No HIPAA / residency / on-prem pressure. | Commercial API is fine; a genuine advantage of the no-shadow-profile design. |
| **Modalities** | Text only. | No multimodal need. |
| **Cost** | Two calls per request, tiny prompts. | Negligible; a smaller/faster model is even viable given the low-stakes jobs. |

**Open decision:** pick the model for the two calls (default: a strong
current Claude model). Optionally A/B a smaller model for `parse_situation`
since it's pure extraction — decide with the eval, not by guessing.

---

## Pillar 2 — Output optimization (Lesson 1)

The 2×2 matrix (context × behavioral): **PlateMate needs prompt engineering
only.** No RAG, no fine-tuning (see below).

**The five quality dimensions, already designed:**

- **Relevant** — both prompts are grounded in the structured situation + the
  named files; `parse_situation` reads the raw message, `coaching_line`
  reads the validated card + `examples.md`.
- **Consistent** — the deterministic floor, the banned-language screen, and
  the fallback line guarantee consistency exactly where it matters; the
  seven eval cases test it.
- **Appropriate** — the safety screen + banned-language screen **are** the
  "appropriate" filter, implemented in code (red-teaming territory — see
  evaluation).
- **Affordable** — two small calls; trivial.
- **Fast enough** — single-turn; fine.

**The two prompts (the real prompt-engineering work):**

1. `parse_situation` — **few-shot**: examples of message → structured fields
   (trigger form, eaten, constraint ahead, time). Output must be valid
   structured data (JSON-validity is a hard eval — it feeds code). Keyword
   rules are the model-off fallback.
2. `coaching_line` — **few-shot off `examples.md`**: tone taught by
   demonstration, not instruction. Screened by `banned_language.md`;
   deterministic fallback on failure.

**Strategies from the lesson already in the architecture:**
- *Split complex tasks into subtasks* → the orchestrator's fixed-order
  triage (safety → scope → missing-data → classify into 5 triggers → route)
  is exactly "intent classification then route to a focused prompt."
- *Provide reference text* → `examples.md` as few-shot reference.
- *Clear instructions / delimit / specify format* → the card's labeled-field
  schema.
- Chain-of-thought and "give the model time to think" are largely
  unnecessary — the reasoning lives in deterministic code, not the model.

---

## RAG and fine-tuning (Lesson 2) — deliberately not used

**RAG: not needed.** The data (foods, plan, personas) is small, structured,
and queried deterministically — this is lookup/filtering, not
embedding-based semantic retrieval. The context window is never stressed
(plan + today's intake + a foods subset + examples is small; no chunking).
Function calling is relevant conceptually — PlateMate's tools are
functions — but **the control flow is code, not the model deciding which
tool to call.** That is a safety choice, not an omission: the model never
triggers a tool, so it can't be manipulated into an unsafe call. *Revisit
only if* the food reference grows large enough that deterministic filtering
becomes unwieldy (not a v1 concern).

**Fine-tuning: not needed, and actively avoided.** Tone and format are
handled by few-shot + the banned-language screen — the lesson's "start
simple" rule. The lesson's own warning is decisive here: fine-tuning can
**shift alignment and erode safety guardrails** — the one thing PlateMate's
architecture must never compromise. Prompt engineering gives faster
iteration and keeps the safety behavior intact. *Revisit only if* a
measured behavioral gap survives good prompting — unlikely for a
one-sentence coaching line.

Decision-framework verdict (start simple → add only on evidence):
**prompt engineering is the whole optimization stack for v1.**

---

## Pillar 3 — Evaluation (Lesson 2) — PlateMate's strongest fit

The **seven eval cases in DESIGN.md already are the evaluation suite**:
human-authored ground truth as (input → expected behavior), covering the
happy path, three edges, the imperfect-day path, the tier-distinction pair,
and the boundary/jailbreak case.

**Test-every-substep** — PlateMate's Check gate has four verifications
already; the deterministic functions are exactly unit-testable. Test types
from the lesson map cleanly:

| Lesson test type | PlateMate application |
|---|---|
| **String / number match** | `macro_calculator` outputs — Case 1 exact kcal/protein, Case 5 gap labels. Deterministic → exact assertions, not fuzzy grading. |
| **Schema validity** | The card's labeled-field structure (BUDGET · OPTIONS · BRIDGE · NOTE · COACHING LINE, in order). |
| **JSON validity** | `parse_situation` must emit a valid structured object — non-negotiable, it feeds code. |
| **Semantic similarity** | `coaching_line` tone vs `examples.md` — graded by an LLM (the one genuinely fuzzy check). |
| **Faithfulness** | Options must be grounded in `foods.json` + the plan — no invented foods or numbers. The deterministic design makes numeric faithfulness near-guaranteed (code computes them); the screen + examples ground the sentence. |

**Faithfulness, concretely:** every option's macros trace to `foods.json`
and every budget number traces to `macro_calculator` over the plan — a
faithfulness score of 1.0 is a *structural* property here, not a hope,
because the numbers are computed, not generated.

**Pass-rate gate:** the lesson's "80% is fine with fallbacks" maps to the
build-readiness gate; the deterministic parts should target 100% (they're
exact), while the two LLM parts carry the fallback + screen for their tail.
Set a per-case expected outcome and gate the demo on it.

**LLM-as-grader:** use categorical pass/fail (not numeric scores) for the
two fuzzy checks — parse quality and coaching-line tone.

**Adversarial / red-teaming — PlateMate is purpose-built for this.** The
eight probe areas, mapped:

| Red-team area | PlateMate's built-in defense |
|---|---|
| PII leaks | No real PII stored at all (memory design) — minimal surface. |
| Insecure tool use | Only write is `log_confirmed_choice`, behind the client's Confirm; the model never triggers tools. |
| Prompt hacking / jailbreak | **Case 7** ("ignore your rules… 800-kcal plan"): the compliance floor is code — no such output exists under any phrasing; the LLM can only *add* a stop, never clear one. |
| Harmful content | Banned-language screen; disordered-eating boundary; medical signal → GET HELP NOW. |
| Medical / legal advice | Safety screen escalates; out-of-scope declined and pointed to the coach. |
| Competitor / political / etc. | Out-of-scope classifier → decline + digest. |

This is a demo-day asset: PlateMate's safety architecture *is* a red-team
defense by construction, and Case 7 is the runnable proof.

---

## The genuinely open Develop decisions (short list)

Everything above is answered by Design except these, and none is large:

1. **Model choice** for the two calls (default: strong Claude model; maybe a
   smaller one for `parse_situation` — decide with the eval).
2. **The two prompt designs** — few-shot, both drawing on `examples.md`.
3. **The eval harness** — turn the seven cases into runnable tests:
   exact-match for the deterministic parts, LLM-as-grader (categorical) +
   faithfulness for the two LLM parts.
4. **Build order (Moe's directive):** Milestone 1 = Case 1 (happy path) +
   Case 7 (hard stop) end to end — the full spine, zero tier logic — before
   the tier pair and the rest. "Prove the loop first, then earn the
   complexity."

## When the Develop guide arrives

Expect it to ask the questions this doc pre-answers (model, optimization
technique, eval plan). Milestone 1 is the first build move; this prep is the
map to build against.
