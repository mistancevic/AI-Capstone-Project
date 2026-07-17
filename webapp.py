"""PlateMate web UI — Python stdlib only, nothing to install.

    python webapp.py            # then open http://localhost:8000

In GitHub Codespaces the port is auto-forwarded: run it, then click the
"Open in Browser" notification (or the PORTS tab -> port 8000 -> globe icon).

The page is a thin skin over the same agents the CLI and demo use:
GET  /api/state?persona=alex|maja   -> plan summary for the persona
POST /api/adapt                     -> run one disrupted-day request
"""

from __future__ import annotations

import json
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from platemate import llm                                    # noqa: E402
from platemate.escalation import Clock, load_agreement       # noqa: E402
from platemate.agents import Orchestrator                    # noqa: E402
from platemate.agents.orchestrator import classify_trigger   # noqa: E402
from platemate.food_db import load_foods                     # noqa: E402
from platemate.models import (                               # noqa: E402
    ClientProfile,
    Route,
    Trigger,
    situation_from_dict,
)
from platemate.plan_parser import capture_targets, parse_plan_file  # noqa: E402

PORT = 8000
PERSONAS = json.loads((ROOT / "data" / "personas.json").read_text(encoding="utf-8"))
FOODS = load_foods()


def build_persona(key: str, targets: dict | None = None):
    p = PERSONAS[key]
    profile = ClientProfile(
        name=p["name"], goal=p["goal"], restrictions=p["restrictions"],
        dislikes=p["dislikes"], likes=p["likes"],
        training_tomorrow=p["training_tomorrow"], usual_bedtime=p["usual_bedtime"],
    )
    plan = parse_plan_file(ROOT / p["plan_file"])
    if plan.needs_target_capture and targets:
        capture_targets(plan, int(targets["calories_kcal"]), int(targets["protein_g"]))
    return plan, profile


def state_payload(key: str) -> dict:
    plan, profile = build_persona(key)
    return {
        "persona": key,
        "name": profile.name,
        "goal": profile.goal,
        "likes": profile.likes,
        "dislikes": profile.dislikes,
        "restrictions": profile.restrictions,
        "training_tomorrow": profile.training_tomorrow,
        "usual_bedtime": profile.usual_bedtime,
        "needs_targets": plan.needs_target_capture,
        "targets": None if plan.targets is None else {
            "calories_kcal": plan.targets.calories_kcal,
            "protein_g": plan.targets.protein_g,
        },
        "meals": [
            {"slot": m.time_hint, "name": m.name, "kcal": m.calories_kcal, "protein_g": m.protein_g}
            for m in plan.meals
        ],
        "llm": llm.available(),
    }


def result_payload(result) -> dict:
    out = {
        "route": result.route.value,
        "trigger": result.trigger.value,
        "consulted": result.consulted_agents,
        "escalation": None,
        "recommendation": None,
        "question": getattr(result, "question", ""),
        "presets": getattr(result, "presets", []),
        "flag": None,
    }
    if result.flag:
        f = result.flag
        out["flag"] = {"tier": f.tier.value, "reasons": f.reason_codes,
                       "counters": f.counter_history, "queued_at": f.queued_at,
                       "delivered_at": f.delivered_at,
                       "trigger_shared": f.trigger_message_shared}
    if result.escalation:
        out["escalation"] = {"reasons": result.escalation.reasons, "message": result.escalation.message}
    rec = result.recommendation
    if rec:
        def opt(o):
            return {
                "name": o.food.name, "kcal": o.food.calories_kcal, "protein_g": o.food.protein_g,
                "rationale": o.rationale, "day_end_kcal_gap": o.day_end_kcal_gap,
                "day_end_protein_gap": o.day_end_protein_gap,
            }
        m = rec.math
        out["recommendation"] = {
            "math": {
                "target_kcal": m.target.calories_kcal, "target_protein_g": m.target.protein_g,
                "consumed_kcal": m.consumed_kcal, "consumed_protein_g": m.consumed_protein_g,
                "reserved_kcal": m.reserved_kcal, "reserved_protein_g": m.reserved_protein_g,
                "remaining_kcal": m.remaining_kcal, "remaining_protein_g": m.remaining_protein_g,
            },
            "options": [opt(o) for o in rec.options],
            "bridge": opt(rec.bridge) if rec.bridge else None,
            "within_tolerance": rec.within_tolerance,
            "strategy_note": rec.strategy_note,
            "sleep_note": rec.sleep_note,
            "coaching_line": rec.coaching_line,
        }
    return out


def handle_adapt(body: dict) -> dict:
    persona = body.get("persona", "alex")
    message = (body.get("message") or "").strip()
    targets = body.get("targets")
    skipped_days = int(body.get("skipped_days") or 0)
    comp_asks = int(body.get("compensatory_asks_week") or 0)

    plan, profile = build_persona(persona, targets)
    clock = Clock((body.get("clock") or "15:00").strip() or "15:00")
    orch = Orchestrator(plan, profile, FOODS,
                        agreement=load_agreement(persona), clock=clock)

    sit_data = body.get("situation")
    if sit_data:
        situation = situation_from_dict(sit_data)
        situation.raw_text = message or situation.raw_text
        if situation.trigger == Trigger.UNKNOWN:
            situation.trigger = classify_trigger(situation.raw_text)
        result = orch.handle(situation, skipped_days=skipped_days,
                             compensatory_asks_week=comp_asks)
    else:
        result = orch.handle_text(message, skipped_days=skipped_days,
                                  compensatory_asks_week=comp_asks)
    return result_payload(result)


class Handler(BaseHTTPRequestHandler):
    def _send(self, code: int, content: bytes, ctype: str) -> None:
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def _json(self, code: int, data: dict) -> None:
        self._send(code, json.dumps(data).encode("utf-8"), "application/json; charset=utf-8")

    def do_GET(self):  # noqa: N802
        url = urlparse(self.path)
        if url.path in ("/", "/index.html"):
            self._send(200, INDEX_HTML.encode("utf-8"), "text/html; charset=utf-8")
        elif url.path == "/api/state":
            persona = parse_qs(url.query).get("persona", ["alex"])[0]
            if persona not in PERSONAS:
                self._json(404, {"error": "unknown persona"})
            else:
                self._json(200, state_payload(persona))
        else:
            self._json(404, {"error": "not found"})

    def do_POST(self):  # noqa: N802
        if urlparse(self.path).path != "/api/adapt":
            self._json(404, {"error": "not found"})
            return
        try:
            length = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(length) or b"{}")
            self._json(200, handle_adapt(body))
        except Exception as exc:  # surface the error to the UI instead of a blank 500
            self._json(400, {"error": str(exc)})

    def log_message(self, fmt, *args):  # quieter console
        pass


INDEX_HTML = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>PlateMate — macros made simple</title>
<style>
  :root{
    --bg:#f6f4ee; --card:#ffffff; --ink:#22301f; --muted:#68755f;
    --green:#2e6b3f; --green-soft:#e7efe6; --amber:#8a5a12; --amber-soft:#faf1de;
    --red:#8c2f2f; --red-soft:#f9e8e6; --indigo:#3b4a7a; --indigo-soft:#e9ecf7;
    --line:#e2ddd0; --radius:14px;
  }
  *{box-sizing:border-box}
  body{margin:0;background:var(--bg);color:var(--ink);
       font:15px/1.55 "Georgia","Iowan Old Style",serif;}
  .sans{font-family:"Avenir Next","Segoe UI",system-ui,sans-serif}
  header{padding:26px 20px 10px;text-align:center}
  header h1{margin:0;font-size:30px;font-weight:600;letter-spacing:.2px}
  header h1 em{color:var(--green)}
  header p{margin:6px 0 0;color:var(--muted);font-style:italic}
  main{max-width:960px;margin:0 auto;padding:14px 16px 60px;display:grid;gap:16px}
  .card{background:var(--card);border:1px solid var(--line);border-radius:var(--radius);
        padding:18px 20px;box-shadow:0 1px 2px rgba(40,50,35,.05)}
  .card h2{margin:0 0 10px;font-size:17px;font-weight:600}
  .row{display:flex;flex-wrap:wrap;gap:10px;align-items:center}
  label{font-size:13px;color:var(--muted)}
  select,input[type=text],input[type=number],textarea{
    font:14px/1.4 "Avenir Next","Segoe UI",system-ui,sans-serif;
    border:1px solid var(--line);border-radius:8px;padding:8px 10px;background:#fdfcf9;color:var(--ink)}
  textarea{width:100%;resize:vertical;min-height:64px}
  input[type=number]{width:86px}
  .chip{display:inline-block;padding:3px 10px;border-radius:999px;font-size:12px;
        background:var(--green-soft);color:var(--green);font-family:"Avenir Next","Segoe UI",system-ui,sans-serif}
  .chip.gray{background:#efece3;color:var(--muted)}
  .chip.red{background:var(--red-soft);color:var(--red)}
  .chip.indigo{background:var(--indigo-soft);color:var(--indigo)}
  table{border-collapse:collapse;width:100%;font-family:"Avenir Next","Segoe UI",system-ui,sans-serif;font-size:14px}
  td,th{padding:6px 8px;text-align:right;border-bottom:1px dashed var(--line)}
  td:first-child,th:first-child{text-align:left}
  .presets button, .actions button{
    font:13px "Avenir Next","Segoe UI",system-ui,sans-serif;border:1px solid var(--line);
    background:#fdfcf9;border-radius:999px;padding:7px 14px;cursor:pointer}
  .presets button:hover{border-color:var(--green);color:var(--green)}
  .actions button.primary{background:var(--green);border-color:var(--green);color:#fff;
    font-size:15px;padding:10px 22px;border-radius:10px}
  .actions button.primary:hover{background:#25572f}
  fieldset{border:1px solid var(--line);border-radius:10px;padding:10px 12px;margin:0}
  legend{font-size:12px;color:var(--muted);padding:0 6px;
         font-family:"Avenir Next","Segoe UI",system-ui,sans-serif}
  .grid2{display:grid;grid-template-columns:1fr 1fr;gap:12px}
  @media(max-width:720px){.grid2{grid-template-columns:1fr}}
  .opt{border:1px solid var(--line);border-radius:10px;padding:10px 14px;margin:8px 0;
       display:flex;gap:12px;align-items:baseline}
  .opt .rank{font-size:20px;color:var(--green);font-weight:700;min-width:22px}
  .opt .macros{margin-left:auto;white-space:nowrap;color:var(--muted);
       font-family:"Avenir Next","Segoe UI",system-ui,sans-serif;font-size:13px}
  .note{border-radius:10px;padding:12px 14px;margin-top:10px;font-size:14px}
  .note.amber{background:var(--amber-soft);color:var(--amber)}
  .note.indigo{background:var(--indigo-soft);color:var(--indigo)}
  .note.green{background:var(--green-soft);color:var(--green)}
  .note.red{background:var(--red-soft);color:var(--red)}
  .coach{margin-top:12px;padding-left:14px;border-left:3px solid var(--green);font-style:italic}
  .muted{color:var(--muted)}
  .hidden{display:none}
  #spinner{color:var(--muted);font-style:italic}
</style>
</head>
<body>
<header>
  <h1>Plate<em>Mate</em></h1>
  <p>macros made simple — your plan, adapted to real life</p>
</header>
<main>

  <section class="card" id="planCard">
    <div class="row" style="justify-content:space-between">
      <h2 style="margin:0">The plan</h2>
      <span>
        <label for="persona">client&nbsp;</label>
        <select id="persona">
          <option value="alex">Alex — lean muscle gain</option>
          <option value="maja">Maja — fat loss, steady energy</option>
        </select>
      </span>
    </div>
    <div id="planBody" class="sans" style="margin-top:10px"></div>
    <div id="targetsCapture" class="hidden note amber sans" style="margin-top:10px">
      This plan doesn't state daily targets — PlateMate won't guess. Enter what the coach prescribed:
      <div class="row" style="margin-top:8px">
        <label>kcal/day <input type="number" id="capKcal" value="1800"></label>
        <label>protein g/day <input type="number" id="capProt" value="120"></label>
        <span class="muted">applied to your next request</span>
      </div>
    </div>
  </section>

  <section class="card">
    <h2>What happened to your day?</h2>
    <div class="presets row" style="margin-bottom:10px">
      <button data-preset="icecream">🍦 Ice cream + team dinner</button>
      <button data-preset="fivemin">⏱ 5-minute lunch</button>
      <button data-preset="pizza">🍕 Whole pizza day</button>
      <button data-preset="late">🌙 Late restaurant swap</button>
      <button data-preset="safety">🚨 Safety case</button>
    </div>
    <textarea id="message" placeholder="e.g. I ate an ice cream and have a big team dinner tonight — what should lunch be?"></textarea>

    <div class="grid2" style="margin-top:12px">
      <fieldset>
        <legend>Solve for</legend>
        <div class="row">
          <select id="mealSlot">
            <option>breakfast</option><option selected>lunch</option>
            <option>snack</option><option>dinner</option>
          </select>
          <label>minutes <input type="number" id="minutes" value="30" min="0"></label>
          <label>time (opt.) <input type="text" id="mealTime" size="5" placeholder="21:00"></label>
        </div>
        <div class="row" style="margin-top:8px" id="availBoxes">
          <label><input type="checkbox" value="home" checked> at home</label>
          <label><input type="checkbox" value="shop" checked> nearby shop</label>
          <label><input type="checkbox" value="restaurant"> restaurant</label>
        </div>
      </fieldset>
      <fieldset>
        <legend>Plan status today</legend>
        <div class="sans" style="font-size:13px">
          <div id="completedBoxes"><span class="muted">already eaten as planned:</span></div>
          <div id="skippedBoxes" style="margin-top:6px"><span class="muted">won't happen as planned:</span></div>
        </div>
      </fieldset>
      <fieldset>
        <legend>Eaten off-plan (optional)</legend>
        <div class="row">
          <input type="text" id="offLabel" placeholder="what?" size="14">
          <label>kcal <input type="number" id="offKcal" min="0"></label>
          <label>protein g <input type="number" id="offProt" min="0"></label>
        </div>
      </fieldset>
      <fieldset>
        <legend>Fixed commitment coming (optional)</legend>
        <div class="row">
          <input type="text" id="upLabel" placeholder="e.g. team dinner" size="14">
          <label>~kcal <input type="number" id="upKcal" min="0"></label>
          <label>~protein g <input type="number" id="upProt" min="0"></label>
        </div>
      </fieldset>
    </div>

    <div class="row actions" style="margin-top:14px;justify-content:space-between">
      <label class="sans muted">days of skipped meals lately
        <input type="number" id="skippedDays" value="0" min="0" style="width:60px"></label>
      <label class="sans muted">compensatory asks this week
        <input type="number" id="compAsks" value="0" min="0" style="width:60px"></label>
      <label class="sans muted">clock
        <input type="text" id="clock" value="15:00" size="5" style="width:60px"></label>
      <button class="primary" id="go">Adapt my day</button>
    </div>
  </section>

  <section class="card hidden" id="resultCard">
    <div class="row" id="routeChips"></div>
    <div id="resultBody"></div>
  </section>

</main>
<script>
const $ = id => document.getElementById(id);
let STATE = null;

async function loadState(){
  const res = await fetch('/api/state?persona=' + $('persona').value);
  STATE = await res.json();
  const t = STATE.targets;
  let html = '';
  html += '<div class="row" style="margin-bottom:8px">';
  html += t ? `<span class="chip">${t.calories_kcal} kcal / ${t.protein_g} g protein daily</span>`
            : '<span class="chip red">targets not in plan</span>';
  if (STATE.restrictions.length) html += `<span class="chip gray">avoids: ${STATE.restrictions.join(', ')}</span>`;
  if (STATE.training_tomorrow) html += '<span class="chip indigo">trains tomorrow</span>';
  html += `<span class="chip gray">AI layer: ${STATE.llm ? 'Claude' : 'offline rules'}</span></div>`;
  html += '<table><tr><th>baseline meal</th><th>kcal</th><th>protein</th></tr>';
  for (const m of STATE.meals)
    html += `<tr><td>${m.name}</td><td>${m.kcal}</td><td>${m.protein_g} g</td></tr>`;
  html += '</table>';
  $('planBody').innerHTML = html;
  $('targetsCapture').classList.toggle('hidden', !STATE.needs_targets);
  renderMealBoxes();
}

function renderMealBoxes(){
  const slots = STATE.meals.map(m => m.slot);
  const mk = (box, name) => {
    box.querySelectorAll('label').forEach(e => e.remove());
    for (const s of slots){
      const l = document.createElement('label');
      l.style.marginLeft = '8px';
      l.innerHTML = `<input type="checkbox" name="${name}" value="${s}"> ${s}`;
      box.appendChild(l);
    }
  };
  mk($('completedBoxes'), 'completed');
  mk($('skippedBoxes'), 'skipped');
}

function checks(name){
  return [...document.querySelectorAll(`input[name=${name}]:checked`)].map(e => e.value);
}
function setChecks(name, values){
  document.querySelectorAll(`input[name=${name}]`).forEach(e => e.checked = values.includes(e.value));
}
function setAvail(values){
  document.querySelectorAll('#availBoxes input').forEach(e => e.checked = values.includes(e.value));
}

const PRESETS = {
  icecream: {msg:"I ate an ice cream this morning and I have a colleague dinner tonight, probably around 1000 kcal. What should I do for lunch?",
    slot:'lunch', minutes:30, time:'', avail:['home','shop'], completed:['breakfast'], skipped:['dinner'],
    off:['ice cream',300,5], up:['colleague dinner',1000,60], days:0},
  fivemin: {msg:"Meetings all day, I have 5 minutes for lunch at my desk. Help.",
    slot:'lunch', minutes:5, time:'', avail:['home','shop'], completed:['breakfast'], skipped:[],
    off:['',null,null], up:['',null,null], days:0},
  pizza: {msg:"I ate a whole pizza this afternoon on top of everything. Dinner?",
    slot:'dinner', minutes:20, time:'', avail:['home','shop'], completed:['breakfast','lunch','snack'], skipped:[],
    off:['whole margherita pizza',850,30], up:['',null,null], days:0},
  late: {msg:"My planned dinner isn't available, I'm at a restaurant and it's already 9pm. What do I order?",
    slot:'dinner', minutes:60, time:'21:00', avail:['restaurant'], completed:['breakfast','lunch'], skipped:[],
    off:['',null,null], up:['',null,null], days:0},
  safety: {msg:"I've been feeling dizzy today and honestly I've barely eaten anything for three days. What should I eat?",
    slot:'lunch', minutes:30, time:'', avail:['home','shop'], completed:[], skipped:[],
    off:['',null,null], up:['',null,null], days:3},
};

document.querySelectorAll('.presets button').forEach(b => b.onclick = () => {
  const p = PRESETS[b.dataset.preset];
  $('message').value = p.msg; $('mealSlot').value = p.slot;
  $('minutes').value = p.minutes; $('mealTime').value = p.time;
  setAvail(p.avail); setChecks('completed', p.completed); setChecks('skipped', p.skipped);
  $('offLabel').value = p.off[0]; $('offKcal').value = p.off[1] ?? ''; $('offProt').value = p.off[2] ?? '';
  $('upLabel').value = p.up[0]; $('upKcal').value = p.up[1] ?? ''; $('upProt').value = p.up[2] ?? '';
  $('skippedDays').value = p.days;
});

$('persona').onchange = loadState;

$('go').onclick = async () => {
  const off = $('offLabel').value.trim();
  const up = $('upLabel').value.trim();
  const situation = {
    raw_text: $('message').value,
    completed_meals: checks('completed'),
    skipped_meals: checks('skipped'),
    eaten_off_plan: off ? [[off, +$('offKcal').value || 0, +$('offProt').value || 0]] : [],
    upcoming_fixed: up ? [[up, +$('upKcal').value || 0, +$('upProt').value || 0]] : [],
    meal_to_solve: $('mealSlot').value,
    minutes_available: +$('minutes').value || 30,
    meal_time: $('mealTime').value.trim(),
    available: [...document.querySelectorAll('#availBoxes input:checked')].map(e => e.value),
  };
  const body = {
    persona: $('persona').value,
    message: $('message').value,
    situation,
    skipped_days: +$('skippedDays').value || 0,
    compensatory_asks_week: +$('compAsks').value || 0,
    clock: $('clock').value || '15:00',
  };
  if (STATE.needs_targets)
    body.targets = {calories_kcal: +$('capKcal').value, protein_g: +$('capProt').value};

  $('resultCard').classList.remove('hidden');
  $('routeChips').innerHTML = '';
  $('resultBody').innerHTML = '<p id="spinner">PlateMate is thinking…</p>';
  const res = await fetch('/api/adapt', {method:'POST',
    headers:{'Content-Type':'application/json'}, body: JSON.stringify(body)});
  const data = await res.json();
  render(data);
  $('resultCard').scrollIntoView({behavior:'smooth'});
};

function render(d){
  if (d.error){
    $('resultBody').innerHTML = `<div class="note red">${d.error}</div>`;
    return;
  }
  let chips = `<span class="chip ${d.route === 'escalate_to_coach' ? 'red' : ''}">route: ${d.route}</span>`;
  chips += `<span class="chip gray">trigger: ${d.trigger}</span>`;
  for (const a of d.consulted) chips += `<span class="chip indigo">agent: ${a}</span>`;
  $('routeChips').innerHTML = chips;

  if (d.question && !d.recommendation && !d.escalation){
    let h = `<div class="note"><b>PlateMate asks:</b><br>${d.question}</div>`;
    if (d.presets && d.presets.length){
      h += '<ul class="sans" style="font-size:13px">';
      for (const pr of d.presets) h += `<li>${pr}</li>`;
      h += '</ul>';
    }
    $('resultBody').innerHTML = h;
    return;
  }
  if (d.escalation && !d.recommendation){
    let h = '<div class="note red"><strong>Escalated to your coach.</strong><ul>';
    for (const r of d.escalation.reasons) h += `<li>${r}</li>`;
    h += `</ul>${d.escalation.message.replace(/\n/g,'<br>')}</div>`;
    if (d.flag){
      h += `<div class="note red sans" style="font-size:13px"><b>COACH FLAG [${d.flag.tier.toUpperCase()}]</b><br>` +
           `reasons: ${d.flag.reasons.join('; ')}<br>` +
           `queued ${d.flag.queued_at} — delivered ${d.flag.delivered_at}</div>`;
    }
    $('resultBody').innerHTML = h;
    return;
  }

  const r = d.recommendation, m = r.math;
  let h = `<h2 style="margin-top:12px">Remaining-day math</h2>
  <table>
    <tr><td>Daily target</td><td>${m.target_kcal} kcal</td><td>${m.target_protein_g} g protein</td></tr>
    <tr><td>Already consumed</td><td>− ${m.consumed_kcal}</td><td>− ${m.consumed_protein_g} g</td></tr>
    <tr><td>Reserved for the rest of the day</td><td>− ${m.reserved_kcal}</td><td>− ${m.reserved_protein_g} g</td></tr>
    <tr><td><strong>Remaining for this meal</strong></td><td><strong>${m.remaining_kcal} kcal</strong></td><td><strong>${m.remaining_protein_g} g</strong></td></tr>
  </table>
  <h2 style="margin-top:16px">Ranked options</h2>`;
  r.options.forEach((o, i) => {
    h += `<div class="opt"><span class="rank">${i + 1}</span>
      <span>${o.name}<br><span class="muted sans" style="font-size:13px">${o.rationale}</span></span>
      <span class="macros">${o.kcal} kcal · ${o.protein_g} g</span></div>`;
  });
  if (r.bridge){
    h += `<div class="opt" style="border-style:dashed"><span class="rank">☂</span>
      <span>${r.bridge.name}<br><span class="muted sans" style="font-size:13px">bridge fallback — if nothing above works, take this instead of skipping</span></span>
      <span class="macros">${r.bridge.kcal} kcal · ${r.bridge.protein_g} g</span></div>`;
  }
  h += r.within_tolerance
    ? '<div class="note green">Best option lands the day within tolerance (±150 kcal / ±10 g protein). ✔</div>'
    : `<div class="note amber"><strong>Multi-day strategy.</strong> ${r.strategy_note}</div>`;
  if (r.sleep_note) h += `<div class="note indigo"><strong>Sleep &amp; recovery.</strong> ${r.sleep_note}</div>`;
  if (r.coaching_line) h += `<div class="coach">${r.coaching_line}</div>`;
  $('resultBody').innerHTML = h;
}

loadState();
</script>
</body>
</html>
"""


def main() -> None:
    server = ThreadingHTTPServer(("0.0.0.0", PORT), Handler)
    print(f"PlateMate web UI running: http://localhost:{PORT}")
    print("(in Codespaces: click the 'Open in Browser' popup, or PORTS tab -> 8000)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nBye — protein first, calories second.")


if __name__ == "__main__":
    main()
