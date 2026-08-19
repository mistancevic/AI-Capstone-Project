# From prototype to something a real person can use

Plan for `platemate-app`, the third repo. Written 2026-08-09, after the capstone
was submitted and before the review came back.

## Why a third repo

| Repo | What it is | Lifecycle |
|---|---|---|
| `AI-Capstone-Project` | Coursework record: the four PRDs, the notes, `develop-companion/` as source of truth for the demo | Frozen after review, then archived |
| `platemate` | The capstone artifact. One static file on GitHub Pages, build p62 | **Frozen forever.** The PRD points at it. It is evidence, not a product |
| `platemate-app` | The real product. Server, database, secrets, deploy config | Where work goes from here |

Not a branch of `platemate`. One bad push to `main` breaks the artifact under
review, and deploy secrets do not belong in the same repo as a public Pages site.

The new repo starts by copying `develop-companion/index.html` and splitting it:
the screening, the arithmetic, the filter and the card stay client-side; the
model call moves behind a server.

---

## The one thing that makes it an app

Today the browser calls `api.anthropic.com` directly with a key from
`localStorage`. That cannot ship to a real user. Your key in their browser is
your key stolen; their own key is a nutrition client signing up for an API
account.

**A server holds the key.** The browser posts a case to your server, the server
calls Anthropic, the server returns the parsed fields. Everything else in this
plan is downstream of that.

---

## Architecture

```
browser                      server                    Anthropic
───────                      ──────                    ─────────
screening (S1-S7)  ────┐
  stop? render stop,   │     POST /run
  never call out       │       verify client token
                       └───►   re-run screening       ───► messages API
                               call model                  (key in env)
                               parse fields          ◄───
budget maths      ◄──────────  write run + counters
filter + rank                  return fields
build card
  ▼
human approves    ─────────►  POST /approve
                               write the choice
```

Two things worth stating plainly.

**The screening runs twice, client and server.** The client copy is for speed
and for working offline. The server copy is the one that counts, because a
client-side check is advice, not a control. The server must never call the model
on a case its own screening stops.

**The one-way rule stays where it is.** Screening before the call, model may add
a stop and never clear one. Moving to a server changes nothing about that.

---

## Schema

Six tables. Postgres via Supabase, or SQLite if it stays this small.

**`coaches`** — id, name, email
**`clients`** — id, coach_id, display_name, access_token, daily_kcal,
daily_protein_g, restrictions, typical_where, typical_minutes, excluded (bool),
consent_at, created_at

**`plans`** — id, client_id, meal_slot, kcal, protein_g, ordinal
The coach's baseline. Replaces `plans.csv`.

**`counters`** — client_id, date, skipped_days, compensatory_asks_week, updated_at
**This is the table that does not exist today.** The demo seeds counters and
never writes them, which is why S2c and S3 are demonstrated by a seeded pair
rather than produced at runtime. Writing them is the precondition the Deploy PRD
already names.

**`runs`** — one row per case. See logging below.
**`escalations`** — id, run_id, client_id, reason_codes, queued_at,
deliver_at, delivered_at, acknowledged_at, coach_note

Quiet hours live here: `queued_at` is when it fired, `deliver_at` is when the
coach may see it. That is the 23:00 / 07:00 behaviour, as data instead of a
display string.

---

## The endpoint

`POST /run`

```
in   { client_token, message, meal_to_solve?, minutes?, where? }
out  { status, situation, why, citations, coaching_line,
       budget, options, fallback, reason_codes?, model_called, model_id }
```

- Verify `client_token`, load client + plan + counters
- Run the screening server-side. A stop returns immediately, `model_called:false`
- Otherwise call Anthropic with the key from the environment
- Parse defensively. Unparseable returns a FORMAT status, never a crash
- Apply the one-way rule
- Compute the budget, filter and rank, build the card
- Screen the coaching line against the banned list
- Write the run row and any counter change
- Return

`POST /approve` — records the client's choice and closes the run. Nothing is
final until this fires. That is the human gate, unchanged.

---

## What to log

One row per run, in `runs`:

| Column | Why it matters |
|---|---|
| client_id, created_at | who and when |
| message | the raw text |
| gate_fired | which of the seven gates ended it, or none |
| reason_codes | S-codes, as an array |
| **model_called** (bool) | the claim the whole architecture rests on |
| model_id, latency_ms, error | what actually answered |
| model_raw | the returned fields, verbatim, before parsing |
| model_added_stop (bool) | model escalated where the code did not |
| status | OK / CLARIFY / REFUSED-ESCALATE / OUT-OF-SCOPE / FORMAT |
| target_kcal, consumed, reserved, remaining_kcal, remaining_protein | the arithmetic, as computed |
| options | what was offered |
| chosen_option, portion, approved_at | what the human did |
| line_source | model-written / replaced by S7 / templated nudge |

`model_raw` and `model_added_stop` are the two that earn their keep. Together
they turn E-3 from an accident into a monitor.

---

## The coach dashboard

Four views. Nothing else.

**Runs** — newest first, status, stop reason, whether the model was called.

**Counters** — current value per client, so the tiering is visible rather than
inferred.

**Model-added stops** — every run where the model escalated and the code did
not, with `model_raw` expandable. This is the live over-refusal monitor. E-3 was
found by accident; this view finds the next one on purpose.

**Abandoned after a stop** — the client was refused and did not come back that
day. The best available proxy for a false positive that actually cost something.

---

## Build order

Each step ships and works before the next begins.

1. **Server + key.** One function, one endpoint, key in an env var. The existing
   UI points at it instead of Anthropic. Nothing else changes.
2. **Database + clients.** Client record, access token, plan as rows. Delete the
   CSVs from the client bundle.
3. **Counters written.** `counters` updated on every qualifying run. S2c and S3
   now tier for real.
4. **Run logging.** Every field above.
5. **Coach dashboard.** The four views.

### Then the safety gate, before any real person

Not optional, and not after. These are the parked items, and the reason they are
parked is timing, not doubt:

- **S2b scope fix.** The unscoped floor pattern reads a snack-sized number as a
  below-floor demand. 1 in 10 benign messages hard-stopped today.
- **S2c object test.** "won't eat" with no object check counts a food dislike as
  skip intent. At counter 2 that is a hard stop with an urgent flag.
- **Widened keyword floor.** The offline screening caught **0 of 10** dangerous
  messages in unseen wording. That is the layer that survives the model being
  unavailable.
- **Model leg required, not optional,** on any free-text path. It caught 10 of
  10 on the same test. Offline-only free text has no second layer at all.
- **The benign ten and the dangerous ten as regression suites**, both run on
  every build, both reported.
- **Consent and a processing agreement.** With the model on, a real
  health-adjacent message leaves the device to a third party. That needs
  agreeing once, before it happens once.
- **Exclusion held.** Anyone with a disclosed eating-disorder history stays out
  of the pilot, and the stop and nudge wording goes past a clinically qualified
  reviewer before that changes.

6. **Three clients, four weeks,** per the Deploy PRD. Policy frozen. One missed
   escalation stops it.

---

## Not building

No chat interface. No coach roster or multi-coach anything. No mobile app. No
login. No analytics beyond the four views. No notifications beyond the
escalation queue.

Three clients for four weeks needs none of it, and every hour spent there is an
hour not spent on the safety gate above.

## Stack

Cloudflare Workers or Vercel for the function, Supabase for Postgres. Both free
at this size, both deploy from GitHub. The choice matters less than picking one
today and not revisiting it.
