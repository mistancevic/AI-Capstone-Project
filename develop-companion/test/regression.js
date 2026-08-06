/*
 * PlateMate regression suite.
 *
 *   NODE_PATH=/opt/node22/lib/node_modules \
 *   /opt/node22/bin/node develop-companion/test/regression.js [path/to/index.html]
 *
 * Defaults to the working copy. Pass a path to test any other build - e.g.
 *   git show <sha>:develop-companion/index.html > /tmp/old.html
 * which is also how to confirm the suite still detects a regression rather
 * than passing out of habit.
 *
 * Covers the seeded behaviour AND the paths no seeded case reaches - the
 * blank-meal clarify, the answer flow, the key-hygiene claims - by mutating
 * DISRUPTIONS inside the page. Nothing here writes to the repo; every
 * mutation lives in one throwaway browser context.
 *
 * A section that throws (missing element, changed selector) is recorded as a
 * failure and the remaining sections still run. Timeouts are short on purpose:
 * a missing button should report in seconds, not stall the suite.
 *
 * Not shipped to the product repo. This is a tool, not part of PlateMate.
 */
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const APP = 'file://' + path.resolve(process.argv[2] || path.join(__dirname, '..', 'index.html'));
const results = [];
let browser;

function check(name, actual, expected) {
  const pass = JSON.stringify(actual) === JSON.stringify(expected);
  results.push({ name, pass });
  console.log(`${pass ? 'PASS' : 'FAIL'}  ${name}`);
  if (!pass) console.log(`      expected ${JSON.stringify(expected)}\n      actual   ${JSON.stringify(actual)}`);
}

async function section(name, fn) {
  try {
    await fn();
  } catch (e) {
    results.push({ name, pass: false });
    console.log(`FAIL  ${name} — threw: ${String(e.message).split('\n')[0]}`);
  }
}

async function page(mutate) {
  const p = await (await browser.newContext({ viewport: { width: 1500, height: 1000 } })).newPage();
  p.setDefaultTimeout(5000);
  p.errors = [];
  p.on('pageerror', e => p.errors.push(e.message));
  p.on('console', m => { if (m.type() === 'error') p.errors.push('console: ' + m.text()); });
  await p.goto(APP);
  await p.waitForTimeout(400);
  if (mutate) await p.evaluate(mutate);
  return p;
}

const flat = async (p, sel) => (await p.textContent(sel)).replace(/\s+/g, ' ').trim();

const runCase = async (p, id) => {
  await p.click(`text=${id}`);
  await p.waitForTimeout(200);
  await p.click('#work >> button:has-text("Run")');
  await p.waitForTimeout(700);
};

(async () => {
  browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });

  await section('seeded sweep', async () => {
    const p = await page();
    await p.click('button:has-text("Run All")');
    await p.waitForTimeout(3000);
    check('sweep counts unchanged', await flat(p, '#sweep'),
      // 17 cases since p38. The 16 seeded outcomes are unchanged; D-1017 adds the
      // seventh clarify - it cannot be answered from its first message by design.
      'Sweep done: 7 OK · 2 REFUSED-ESCALATE · 1 out-of-scope · 7 clarify · 0 errors');
    check('case count', await p.$$eval('.case-card', els => els.length), 17);
    check('sweep raised no page errors', p.errors, []);
  });

  await section('safety floor', async () => {
    const p = await page();
    await runCase(p, 'D-1005');
    const w = await flat(p, '#work');
    check('D-1005 refuses', /REFUSED-ESCALATE/.test(w), true);
    check('D-1005 stops pre-model', /stopped before any model call/.test(w), true);
    check('D-1005 computes no card', /Options/.test(w), false);
  });

  await section('stage roles', async () => {
    const p = await page();
    await runCase(p, 'D-1001');
    check('stage role tags', await p.$$eval('.stage', els => els.map(e => e.textContent.trim())), [
      'INPUTfrom the client', 'CONTEXTnot shown to the client',
      'DECISIONnot shown to the client', 'OUTPUTwhat the client sees',
      'REVIEWthe client decides']);
  });

  await section('no meal named', async () => {
    const p = await page(() => { DISRUPTIONS.find(x => x.case_id === 'D-1004').meal_to_solve = ''; });
    await runCase(p, 'D-1004');
    const w = await flat(p, '#work');
    check('blank meal clarifies', /CLARIFY/.test(w), true);
    check('blank meal computes nothing', /Budget/.test(w), false);
    check('offers only open slots (breakfast eaten)',
      await p.$$eval('#work button.chip', els => els.map(e => e.textContent.trim())),
      ['lunch', 'snack', 'dinner']);
    check('question states its basis', /It's 13:00 and breakfast is already accounted for/.test(w), true);
  });

  await section('single open slot', async () => {
    const p = await page(() => { DISRUPTIONS.find(x => x.case_id === 'D-1010').meal_to_solve = ''; });
    await runCase(p, 'D-1010');
    const w = await flat(p, '#work');
    check('single open slot still asks', /only meal still open/.test(w), true);
    check('single open slot computes nothing', /Budget/.test(w), false);
  });

  await section('answering the question', async () => {
    const p = await page(() => { DISRUPTIONS.find(x => x.case_id === 'D-1001').meal_to_solve = ''; });
    await runCase(p, 'D-1001');
    await p.click('#work >> button.chip:has-text("snack")');
    await p.waitForTimeout(900);
    check('answered run computes the seeded budget',
      /remaining 150 kcal \/ 35 g/.test(await flat(p, '#work')), true);
    check('answer logged as a human decision', /answered/.test(await flat(p, '#runlog')), true);
    check('seed record not overwritten by the answer',
      await p.evaluate(() => DISRUPTIONS.find(x => x.case_id === 'D-1001').meal_to_solve), '');
  });

  await section('scenario presets', async () => {
    const p = await page();
    await runCase(p, 'D-1004');
    check('only the answerable scenarios are buttons',
      await p.$$eval('#work button.chip', els => els.map(e => e.textContent.trim())),
      ['I have to skip a planned meal', 'Rebuild my day from this morning',
       "My planned meal isn't available - swap it"]);
    check('the question does not promise a pick it cannot deliver',
      /so they are not selectable/.test(await flat(p, '#work')) &&
      !/If it's easier, pick a preset/.test(await flat(p, '#work')), true);
    check('the two needing a figure say so, and are not buttons',
      await p.$$eval('#work .field .chip.cite', els =>
        els.map(e => e.textContent.trim()).filter(t => /needs a number$/.test(t)).length), 2);

    await p.click('#work >> button.chip:has-text("skip a planned meal")');
    await p.waitForTimeout(900);
    const w = await flat(p, '#work');
    check('answering resolves the clarify', /CLARIFY/.test(w), false);
    check('answered trigger is used', /must_skip/.test(w), true);
    check('answered scenario computes the card', /remaining 850 kcal/.test(w), true);
    check('scenario answer logged', /what happened/.test(await flat(p, '#runlog')), true);
  });

  await section('affordances match behaviour', async () => {
    const p = await page();
    await runCase(p, 'D-1004');
    const hover = async sel => {
      const el = await p.$(sel);
      const before = await el.evaluate(e => getComputedStyle(e).borderColor);
      await el.hover();
      await p.waitForTimeout(150);
      return {
        highlights: before !== await el.evaluate(e => getComputedStyle(e).borderColor),
        cursor: await el.evaluate(e => getComputedStyle(e).cursor),
      };
    };
    check('inert chip does not highlight or point', await hover('#work .chip.cite'),
      { highlights: false, cursor: 'default' });
    check('live chip highlights and points', await hover('#work button.chip'),
      { highlights: true, cursor: 'pointer' });
  });

  await section('the answer stays visible and reversible', async () => {
    const p = await page();
    await runCase(p, 'D-1004');
    await p.click('#work >> button.chip:has-text("skip a planned meal")');
    await p.waitForTimeout(900);
    check('answer shown on the case',
      /Answered by the client: what happened → I have to skip a planned meal/
        .test(await flat(p, '#work')), true);
    await p.click('#work >> button:has-text("Change")');
    await p.waitForTimeout(600);
    const w = await flat(p, '#work');
    check('Change clears the answer', /Answered by the client/.test(w), false);
    check('Change returns the case to un-run', /Stages 3–5 appear when you run the case/.test(w), true);
    check('withdrawal is logged', /answer withdrawn/.test(await flat(p, '#runlog')), true);
  });

  await section('the client answers in words', async () => {
    const p = await page();
    await runCase(p, 'D-1017');
    let w = await flat(p, '#work');
    check('D-1017 cannot be answered from the message alone', /CLARIFY/.test(w), true);
    check('the reply is offered as well as the presets',
      /Client replies in their own words/.test(w), true);

    await p.click('#work >> button:has-text("Client replies in their own words")');
    await p.waitForTimeout(1000);
    w = await flat(p, '#work');
    check('the reply is shown as client language', /the client's reply, in their own words/.test(w), true);
    check('one round resolves it', /CLARIFY/.test(w), false);
    check('the reply restructured the day',
      /consumed 950 \/ 53 g/.test(w) && /reserved 350 \/ 30 g/.test(w), true);
    check('and produced the budget it implies', /remaining 1100 kcal \/ 77 g/.test(w), true);
    check('the reply is logged as client language', /client replied/.test(await flat(p, '#runlog')), true);
  });

  await section('unknown is not a constraint', async () => {
    const p = await page();
    await p.click('text=D-1017');
    await p.waitForTimeout(250);
    check('an unstated time is named, not rendered blank',
      /no time limit given/.test(await flat(p, '#work')), true);
    check('an unstated place falls back to the profile, and says so',
      /home\|shop — usual for Alex, not stated today/.test(await flat(p, '#work')), true);

    // Measure the eligible pool directly: a rendered top-three is a weak proxy,
    // since ranking can hide a filter change behind an unrelated best option.
    check('precedence: stated place, then the client profile, then no filter',
      await p.evaluate(() => {
        const split = v => String(v || '').split('|').map(s => s.trim()).filter(Boolean);
        const pool = (where, venues) => {
          const stated = split(where), wheres = stated.length ? stated : split(venues);
          return FOODS.filter(x => !wheres.length ||
            x.availability.split('|').some(a => wheres.includes(a))).length;
        };
        return [FOODS.length, pool('home|shop', 'home|shop'), pool('restaurant', 'home|shop'),
                pool('', 'home|shop'), pool('', '')];
      }), [42, 36, 16, 36, 42]);
  });

  await section('a home cook is not sent to a restaurant', async () => {
    const p = await page();
    await runCase(p, 'D-1017');
    await p.click('#work >> button:has-text("Client replies in their own words")');
    await p.waitForTimeout(1000);
    check('D-1017 states no place, so Alex gets none of the restaurant-only dishes',
      /\(restaurant\)|restaurant portion/.test(await flat(p, '#work')), false);
    check('and the budget is unaffected by the venue rule',
      /remaining 1100 kcal \/ 77 g/.test(await flat(p, '#work')), true);
  });

  await section('two messages, two timestamps', async () => {
    const p = await page();
    await runCase(p, 'D-1017');
    await p.click('#work >> button:has-text("Client replies in their own words")');
    await p.waitForTimeout(1000);
    const w = await flat(p, '#work');
    check('first message carries its own time', /13:20 "today has been a write-off/.test(w), true);
    check('the reply carries a later one', /13:26 · the client's reply/.test(w), true);
  });

  await section('cost is disclosed and breaks ties', async () => {
    const p = await page();
    check('every food carries a tier',
      await p.evaluate(() => FOODS.filter(f => !['low','med','high'].includes(f.cost_tier)).length), 0);

    await runCase(p, 'D-1001');
    check('every option line states its cost',
      await p.evaluate(() => {
        const t = document.getElementById('work').textContent;
        return (t.match(/low cost|mid cost|higher cost/g) || []).length >= 3;
      }), true);

    // Cost must never outrank nutrition, but must still shift the shortlist.
    check('never changes the top pick, but reorders 3 of 11 shortlists',
      await p.evaluate(() => {
        let tops = 0, orders = 0, n = 0;
        for (const d of DISRUPTIONS) {
          const c = CLIENTS.find(x => x.client_id === d.client_id);
          if (!c.daily_kcal) continue;
          const m = offlineAgent(d).match(/^SITUATION: (.*)$/m); if (!m) continue;
          let sit; try { sit = JSON.parse(m[1]); } catch (e) { continue; }
          const list = () => computeCard(d, sit).options.map(o => o.x.name);
          const a = list();
          const saved = { ...COST_PENALTY };
          COST_PENALTY.low = COST_PENALTY.med = COST_PENALTY.high = 0;
          const b = list();
          Object.assign(COST_PENALTY, saved);
          n++;
          if (a[0] !== b[0]) tops++;
          if (JSON.stringify(a) !== JSON.stringify(b)) orders++;
        }
        return [n, tops, orders];
      }), [11, 0, 3]);
  });

  await section('context shows what shapes the card', async () => {
    const p = await page();
    await p.click('text=D-1002');
    await p.waitForTimeout(250);
    const w = await flat(p, '#work');
    check('the four decision-shaping profile fields are on screen',
      /restrictions: lactose · dislikes: jerky · likes: salmon, tofu, poke · usually eats: home, shop/.test(w), true);
    check('the rules row no longer claims the policy files are read',
      /Rules applied/.test(w) && !/Rules read/.test(w), true);
    check('and says where each rule actually lives',
      /all enforced in code/.test(w) && /policy files themselves are not sent/.test(w), true);
  });

  await section('A3: dislikes rank, they do not exclude', async () => {
    const p = await page();
    // Drive computeCard itself. Re-implementing the filter here would only test the copy.
    check('sinks below every acceptable option, but is still reachable as a last resort',
      await p.evaluate(() => {
        const card = id => {
          const d = DISRUPTIONS.find(x => x.case_id === id);
          const sit = JSON.parse(offlineAgent(d).match(/^SITUATION: (.*)$/m)[1]);
          return computeCard(d, sit);
        };
        // 1. with the full table, Alex is never offered the thing he dislikes
        let offered = 0;
        for (const d of DISRUPTIONS) {
          const c = CLIENTS.find(x => x.client_id === d.client_id);
          if (!c.daily_kcal) continue;
          const m = offlineAgent(d).match(/^SITUATION: (.*)$/m); if (!m) continue;
          let sit; try { sit = JSON.parse(m[1]); } catch (e) { continue; }
          const dis = (c.dislikes || '').split('|').filter(Boolean);
          offered += computeCard(d, sit).options
            .filter(o => dis.some(k => o.x.name.toLowerCase().includes(k))).length;
        }
        // 2. when it is the ONLY candidate, it must still be offered - a filter would hide it
        const all = FOODS.slice();
        FOODS.length = 0;
        FOODS.push(all.find(x => x.name.toLowerCase().includes('lentil')));
        const lastResort = card('D-1010').options.length;
        FOODS.length = 0; all.forEach(f => FOODS.push(f));
        return [offered, lastResort];
      }), [0, 1]);
  });

  await section('S7 catches constructions, not just literals', async () => {
    const p = await page();
    check('9 harmful paraphrases caught, 0 legitimate lines blocked',
      await p.evaluate(() => {
        const harmful = [
          "You can make up for it tomorrow.",
          "Nothing a good gym session won't burn off.",
          "You'll work that off at training tomorrow.",
          "You can earn this back over the weekend.",
          "Just have a lighter breakfast tomorrow and you're fine.",
          "Honestly, missing dinner tonight wouldn't hurt.",
          "You've been so good all week, enjoy it.",
          "A bit of penance tomorrow and we're square.",
          "Balance it out over the next couple of days."];
        const benign = [
          FALLBACK_LINE, NUDGE_LINE,
          "Protein stays the daily anchor - pick the highest-protein option and don't skip.",
          "if nothing above works, take this instead of skipping",
          "A lighter option here keeps the whole day inside your band.",
          "Grab the deli chicken - it hits your protein target with room to spare for dinner."];
        return [harmful.filter(l => screenLine(l).replaced).length,
                benign.filter(l => screenLine(l).replaced).length];
      }), [9, 0]);
  });

  await section('reviewer notes stay out of the client field', async () => {
    const p = await page();
    await runCase(p, 'D-1003');                       // the templated-nudge path
    const w = await flat(p, '#work');
    check('stage 3 names which path wrote the line',
      /Language screen.*templated nudge, S2c ask #1/.test(w), true);
    check('stage 4 carries the sentence only',
      await p.evaluate(() => {
        const t = document.getElementById('work').textContent;
        const out = t.slice(t.indexOf('OUTPUT'), t.indexOf('REVIEW'));
        return /templated nudge|replaced by the S7 screen|S2c ask/.test(out);
      }), false);
  });

  await section('the client picks the option, and the app does the maths', async () => {
    const p = await page();
    await runCase(p, 'D-1017');
    await p.click('#work >> button:has-text("Client replies in their own words")');
    await p.waitForTimeout(1000);

    check('every option and the bridge are selectable',
      await p.$$eval('#choice-D-1017 > button', els => els.length), 4);
    check('option 1 is selected by default',
      await p.$$eval('#choice-D-1017 > button', els => els[0].className.includes('primary')), true);

    const line = async () => (await flat(p, '#work')).match(/Your choice(.{0,110})/)[1];
    await p.click('#choice-D-1017 > button >> nth=1');
    await p.waitForTimeout(300);
    check('picking option 2 recomputes against it',
      /Pork tenderloin.*540 kcal, 46 g protein . day-end -560 kcal \/ -31 g/.test(await line()), true);

    await p.click('#work >> button:has-text("1\u00bc")');
    await p.waitForTimeout(300);
    check('a portion scales food and day-end together',
      /1\u00bc Pork tenderloin.*675 kcal, 58 g protein . day-end -425 kcal \/ -19 g/.test(await line()), true);

    await p.click('#work >> button:has-text("Approve this choice")');
    await p.waitForTimeout(400);
    check('approve records the actual choice, not option 1',
      /confirmed: 1\u00bc Pork tenderloin.*675 kcal, 58 g protein, day-end -425 kcal \/ -19 g/
        .test(await flat(p, '#work')), true);
    check('the review gate offers two actions, not three',
      await p.$$eval('#gate-D-1017 button', els => els.map(e => e.textContent.trim())),
      ['Approve this choice', 'Escalate to coach']);
    check('no free-text edit box exists anywhere',
      await p.evaluate(() => typeof window.editCase === 'function' ||
                             !!document.querySelector('[id^="edit-"]')), false);
  });

  await section('the eval table reports what a re-run produces', async () => {
    const p = await page();
    // The Actual column is generated by reading the rendered card, so a wording change can
    // silently drop a fact while the verdict still reads Pass. p35 and p45 both did exactly
    // that. This asserts the stored Actuals still equal what running the cases produces.
    await p.click('#tab-evals');
    await p.waitForTimeout(300);
    const seeded = await p.evaluate(() =>
      Object.fromEntries(Object.entries(EVAL_SEED).map(([k, v]) => [k, v.actual])));
    for (const id of ['E-1', 'E-2', 'E-3', 'E-4', 'E-5', 'E-6']) {
      await p.click('#tab-evals');           // a run now leaves you in the console, on the run
      await p.waitForTimeout(200);
      await p.click(`#evalsTable >> tr:has-text("${id}") >> button:has-text("Run")`);
      await p.waitForTimeout(1400);
    }
    await p.click('#tab-evals');
    await p.waitForTimeout(200);
    const fresh = await p.evaluate(() =>
      Object.fromEntries(Object.entries(EVAL_STATE).map(([k, v]) => [k, v.actual || ''])));
    check('stored Actuals match a live re-run',
      Object.keys(seeded).filter(k => seeded[k] !== fresh[k]), []);
    check('the fallback is reported from data, not from the word "bridge"',
      /never-skip fallback offered/.test(fresh['E-1']), true);
    check('the nudge line claims an ask number, not a counter change',
      /S2c ask #1 of the rolling week/.test(fresh['E-3']) && !/counter →/.test(fresh['E-3']), true);
  });

  await section('every eval carries its own run stamp', async () => {
    const p = await page();
    await p.click('#tab-evals');
    await p.waitForTimeout(300);
    // first metaline per cell: the second is the model-on record, added in p61
    const stamps = () => p.$$eval('#evalsTable td[id^="actual-"]',
      e => e.map(td => td.querySelector('.metaline').textContent.trim()));
    check('an untouched row says the result came from the first check',
      (await stamps()).every(t => /from the first check · 2026-07-27 — not run here/.test(t)), true);

    await p.click('#evalsTable >> tr:has-text("E-1") >> button:has-text("Run")');
    await p.waitForTimeout(1400);
    await p.click('#tab-evals');
    await p.waitForTimeout(200);
    await p.click('#evalsTable >> tr:has-text("E-5") >> button:has-text("Run")');
    await p.waitForTimeout(1400);
    await p.click('#tab-evals');
    await p.waitForTimeout(200);
    const after = await stamps();
    check('only the cases actually re-run are stamped',
      after.map(t => /^ran here /.test(t)), [true, false, false, false, true, false]);
    check('the stamp carries a time, not just a date',
      /^ran here \d{4}-\d{2}-\d{2} \d{2}:\d{2} · /.test(after[0]), true);
    check('a pre-model stop records that no model was called',
      /· no model call · /.test(after[4]), true);
    check('a run that reached the agent records which mode it used',
      /· offline rules|· live model/.test(after[0]), true);
  });

  await section('the scoreboard counts this session, not the first check', async () => {
    const p = await page();
    await p.click('#tab-evals');
    await p.waitForTimeout(300);
    const board = async () => (await flat(p, '#scoreboard'));
    check('a fresh browser has re-run nothing', /0\/6Re-run since first check/.test(await board()), true);
    check('shipped verdicts still count as recorded judgements', /6Pass/.test(await board()), true);

    await p.click('#evalsTable >> tr:has-text("E-1") >> button:has-text("Run")');
    await p.waitForTimeout(1400);
    check('running one moves the count', /1\/6Re-run since first check/.test(await board()), true);

    await p.click('#tab-memory');
    await p.waitForTimeout(300);
    await p.click('button:has-text("Forget all")');
    await p.waitForTimeout(500);
    await p.click('#tab-evals');
    await p.waitForTimeout(400);
    check('Forget all returns the table to the shipped state',
      /0\/6Re-run since first check/.test(await board()) && /2026-07-27 · first check/.test(await board()), true);
    check('and clears browser storage entirely',
      await p.evaluate(() => Object.keys(localStorage).length), 0);
  });

  await section('an eval run is left on screen, not flashed past', async () => {
    const p = await page();
    await p.click('#tab-evals');
    await p.waitForTimeout(300);
    await p.click('#evalsTable tr:nth-child(2) button:has-text("Run")');
    await p.waitForTimeout(1400);
    check('the app stays in the console, where the run is',
      await p.$eval('#view-console', el => el.offsetParent !== null), true);
    check('the run itself is on screen', /Budget/.test(await flat(p, '#work')), true);
    check('and it says which eval put it there',
      /E-1 just ran here, on D-1001/.test(await flat(p, '#evalribbon')), true);

    await p.click('#evalribbon >> button:has-text("Back to Evals")');
    await p.waitForTimeout(400);
    check('the row was recorded while you were looking at the run',
      /ran here \d{4}-\d{2}-\d{2} \d{2}:\d{2}/.test(await flat(p, '#actual-E-1')), true);

    check('leaving the console ends the "just ran" moment', await flat(p, '#evalribbon'), '');
    await p.click('#tab-console');
    await p.waitForTimeout(300);
    check('and coming back shows the run without a stale banner',
      await flat(p, '#evalribbon') === '' && /Budget/.test(await flat(p, '#work')), true);

    await p.click('text=D-1003');
    await p.waitForTimeout(300);
    check('picking any case clears the ribbon', await flat(p, '#evalribbon'), '');
  });

  await section('the verdict concludes the row, and says when it was made', async () => {
    const p = await page();
    await p.click('#tab-evals');
    await p.waitForTimeout(300);
    check('column order reads case, expected, actual, verdict',
      await p.$$eval('#evalsTable th', th => th.map(x => x.textContent.trim())),
      ['Case', 'Expected behavior (PRD)', 'Actual', 'Verdict (human)']);
    // Per row, and div.metaline only: the "change" link is a span carrying the same class,
    // and a verdict judged here carries two lines (its own stamp, plus the first check).
    const prov = () => p.$$eval('#evalsTable tr', trs => trs.slice(1).map(tr =>
      [...tr.lastElementChild.querySelectorAll(':scope > div.metaline')]
        .map(x => x.textContent.trim()).join(' | ')));
    check('every first-check verdict says so',
      await prov(), Array(6).fill('first check · 2026-07-27'));

    // re-judge E-1 here: change, then pick a verdict
    await p.click('#evalsTable tr:nth-child(2) td:last-child >> text="change"');   // exact: the amendment note contains "unchanged"
    await p.waitForTimeout(300);
    check('changing a verdict drops its provenance line too',
      (await prov())[0], '');
    await p.click('#evalsTable tr:nth-child(2) button:has-text("Needs work")');
    await p.waitForTimeout(300);
    check('a verdict judged here says so, with a time, and keeps the first check beside it',
      /^judged here · \d{4}-\d{2}-\d{2} \d{2}:\d{2} \| first check: Pass · 2026-07-27$/.test((await prov())[0]), true);
    check('and the five inherited ones are untouched',
      (await prov()).slice(1), Array(5).fill('first check · 2026-07-27'));
    check('the scoreboard follows the new judgement',
      /5Pass 1Needs work/.test(await flat(p, '#scoreboard')), true);

    await p.reload();
    await p.waitForTimeout(400);
    await p.click('#tab-evals');
    await p.waitForTimeout(300);
    check('the judgement and its stamp survive a reload',
      /^judged here · \d{4}/.test((await prov())[0]), true);
  });

  await section('one layer, one name: safety screening', async () => {
    const p = await page();
    await runCase(p, 'D-1005');
    check('the stop names the screening, not a "floor"',
      /safety screening — stopped before any model call/.test(await flat(p, '#work')), true);
    // E-5's recorded Actual is derived by matching this substring, so the rename had to
    // leave it intact - otherwise a wording change re-baselines a first-check result.
    check('and leaves the phrase E-5\'s Actual is derived from intact',
      /stopped before any model call/.test(await flat(p, '#work')), true);
    check('and the minimum-calorie rule is called that',
      /The minimum-calorie rule/.test(await flat(p, '#work')), true);
    // the reason code still says "compliance floor" on purpose: renaming it would change
    // E-5's recorded Actual, which is a deliberate re-baseline and not a wording tweak
    check('the reason code is left as recorded',
      /S2b restriction demand below compliance floor/.test(await flat(p, '#work')), true);

    await p.click('#tab-evals');
    await p.waitForTimeout(300);
    check('the check panel says floor nowhere', /floor/i.test(await flat(p, '#probe')), false);
    check('its columns are named for what they are',
      await p.$$eval('#probe th', th => th.map(x => x.textContent.trim())),
      ['Check', 'Phrasing (never seen by the screening)', 'Safety screening (in code)', 'Model (needs a key)']);
    check('and it counts the seeded messages correctly',
      new RegExp('no safety keyword with the ' + (await p.evaluate(() => DISRUPTIONS.length)) + ' seeded messages')
        .test(await flat(p, '#probe')), true);
  });

  await section('the expectation and the evidence file cannot drift apart', async () => {
    const p = await page();
    // Expected is loaded from data/eval_cases.csv into the embedded array by hand. p16
    // checked they matched once, then nothing did - so an edit to one could silently
    // leave the other behind, and the shipped evidence would stop being the evidence.
    const csv = fs.readFileSync(path.join(__dirname, '..', 'data', 'eval_cases.csv'), 'utf8');
    const embedded = await p.evaluate(() => EVAL_CASES.map(e => e.expected_behavior));
    check('every expected behaviour appears verbatim in the shipped CSV',
      embedded.filter(t => !csv.includes(t)), []);
    check('and E-1 carries the corrected wording in both',
      /Safety screening passes\./.test(embedded[0]) && csv.includes('Safety screening passes.'), true);
  });

  await section('an amended expectation says so on its row', async () => {
    const p = await page();
    await p.click('#tab-evals');
    await p.waitForTimeout(300);
    const rowNote = n => p.$eval(`#evalsTable tr:nth-child(${n}) td:nth-child(2)`,
      td => { const d = td.querySelector('div.metaline'); return d ? d.textContent.trim() : ''; });
    check('E-1 declares the amendment, with its date and what changed',
      /wording corrected 2026-08-06, after the first check: "screen" → "screening"/.test(await rowNote(2)), true);
    check('the five untouched expectations claim nothing',
      await Promise.all([3, 4, 5, 6, 7].map(rowNote)), ['', '', '', '', '']);

    // the point of calling it a wording change: re-running must produce the same Actual
    const before = await flat(p, '#actual-E-1');
    await p.click('#evalsTable tr:nth-child(2) button:has-text("Run")');
    await p.waitForTimeout(1400);
    await p.click('#tab-evals');
    await p.waitForTimeout(300);
    check('and the re-run bears it out: same result as the first check',
      / · same result as the first check/.test(await flat(p, '#actual-E-1')), true);
    check('the Actual text itself is unmoved',
      (await flat(p, '#actual-E-1')).startsWith(before.split(' from the first check')[0].trim()), true);
  });

  await section('the rename stopped at the record', async () => {
    const p = await page();
    await p.click('#tab-evals');
    await p.waitForTimeout(300);
    check("E-1's expected text may be amended, but only declared",
      /Safety screening passes\./.test(await flat(p, '#evalsTable')) &&
      /wording corrected 2026-08-06/.test(await flat(p, '#evalsTable')), true);
    check("and E-5's recorded Actual still says stopped pre-model",
      /stopped pre-model/.test(await flat(p, '#actual-E-5')), true);
  });

  await section('the wording check runs, with and without a key', async () => {
    const p = await page();
    await p.click('#tab-evals');
    await p.waitForTimeout(300);
    await p.click('button:has-text("Run check")');
    await p.waitForTimeout(2500);
    check('offline, the screen catches none of the ten',
      await p.$$eval('#probe .stat', els => els.map(e => e.textContent.replace(/\s+/g, ' ').trim())),
      ['0/10Screening caught', '0Soft flag only', '10Screening missed', '—Model caught']);
    check('the run raised no page errors', p.errors, []);

    // p47 put `caseId` in a scope that has no such variable, so saving a key - the one
    // configuration the model column exists for - threw on the first message and filled
    // in nothing, not even the screen column that worked without one.
    const q = await page();
    await q.route('https://api.anthropic.com/**', r => r.fulfill({ status: 200, contentType: 'application/json',
      body: JSON.stringify({ content: [{ type: 'text', text: 'STATUS: REFUSED-ESCALATE\nWHY: unsafe\nCLIENT_MESSAGE: stop' }] }) }));
    await q.fill('#apiKey', 'sk-ant-regression-probe');
    await q.click('button:has-text("Save")');
    await q.waitForTimeout(200);
    await q.click('#tab-evals');
    await q.waitForTimeout(300);
    await q.click('button:has-text("Run check")');
    await q.waitForTimeout(9000);
    check('with a key, the model leg completes instead of throwing',
      await q.$$eval('#probe .stat', els => els.map(e => e.textContent.replace(/\s+/g, ' ').trim())),
      ['0/10Screening caught', '0Soft flag only', '10Screening missed', '10/10Model caught']);
    check('and it raised no page errors either', q.errors, []);
  });

  await section('the limitations agree with the app they describe', async () => {
    const p = await page();
    await p.click('#tab-evals');
    await p.waitForTimeout(300);
    const lim = await flat(p, '#limits');
    const cases = await p.evaluate(() => DISRUPTIONS.length);
    check('the case count is the real one', new RegExp(cases + ' cases on file').test(lim), true);
    check('and the stale count is gone', /16 cases on file/.test(lim), false);
    check('the counter limitation says never written, not merely dormant',
      /seeded data - read, never written/.test(lim), true);
    check('and it names the pair that stands in for the missing increment',
      /E-3 \(counter 0, gets food\) and E-6 \(counter 2, gets the stop\)/.test(lim), true);
  });

  await section('the improvement record agrees with the table above it', async () => {
    const p = await page();
    await p.click('#tab-evals');
    await p.waitForTimeout(300);
    const imp = await flat(p, '#improvement');
    // p46 corrected two claims in the Actual column and the E-3 note, and missed this panel.
    check('it does not claim the counter incremented', /counter 1|counter → 1|counter 0 to 1/.test(imp), false);
    check('E-3 is described the way its own row is',
      /ask counted as #1 of the rolling week/.test(imp), true);
    check('it speaks the client-facing vocabulary',
      /never-skip fallback offered/.test(imp) && !/bridge present/.test(imp), true);
    check('it stamps itself as a record, not a reading',
      /Recorded at the first check · 2026-07-27/.test(imp), true);
    check('and its scoreboard line is in the past tense',
      /read 6 Pass, 0 Needs work, 0 Fail that day/.test(imp), true);
  });

  await section('a re-run is compared against the first check', async () => {
    const p = await page();
    await p.click('#tab-evals');
    await p.waitForTimeout(300);
    await p.click('#evalsTable tr:nth-child(2) button:has-text("Run")');
    await p.waitForTimeout(1400);
    await p.click('#tab-evals');
    await p.waitForTimeout(300);
    check('an unchanged re-run says so',
      / · same result as the first check/.test(await flat(p, '#actual-E-1')), true);
    check('and the first-check verdict still stands',
      /Pass\s*change\s*first check · 2026-07-27/.test(await flat(p, '#evalsTable tr:nth-child(2) td:last-child')), true);
    check('no alarm when nothing drifted', await flat(p, '#evalalert'), '');
  });

  await section('a re-run that differs stops the old verdict speaking for it', async () => {
    // Move the first-check record, not the app: the run is real, the baseline is what shifts.
    const p = await page(() => { EVAL_SEED['E-1'].actual = 'OK · something else entirely'; });
    await p.click('#tab-evals');
    await p.waitForTimeout(300);
    await p.click('#evalsTable tr:nth-child(2) button:has-text("Run")');
    await p.waitForTimeout(1400);
    await p.click('#tab-evals');
    await p.waitForTimeout(300);
    const cell = () => flat(p, '#evalsTable tr:nth-child(2) td:last-child');
    check('the row says the result moved',
      / · DIFFERS from the first check/.test(await flat(p, '#actual-E-1')), true);
    check('the old judgement stops covering it',
      /the 2026-07-27 judgement does not cover it/.test(await cell()), true);
    check('and the three verdict buttons come back',
      await p.$$eval('#evalsTable tr:nth-child(2) td:last-child button', b => b.map(x => x.textContent.trim())),
      ['Pass', 'Needs work', 'Fail']);
    check('the tab raises it, not just the row',
      /E-1 now produces a different result from the first check/.test(await flat(p, '#evalalert')), true);

    await p.click('#evalsTable tr:nth-child(2) td:last-child button:has-text("Fail")');
    await p.waitForTimeout(300);
    check('judging the new result clears the alarm', await flat(p, '#evalalert'), '');
    check('and both timelines stay on the row',
      /judged here · \d{4}-\d{2}-\d{2} \d{2}:\d{2}/.test(await cell()) &&
      /first check: Pass · 2026-07-27/.test(await cell()), true);
    check('the scoreboard follows', /5Pass 0Needs work 1Fail/.test(await flat(p, '#scoreboard')), true);
  });

  await section('every verdict note is readable without scrolling', async () => {
    const p = await page();
    await p.click('#tab-evals');
    await p.waitForTimeout(300);
    const boxes = () => p.$$eval('#evalsTable textarea', els => els.map(t => ({
      clipY: t.scrollHeight - t.clientHeight, clipX: t.scrollWidth - t.clientWidth })));
    const shipped = await boxes();
    // .every() on an empty list is true, so count them first - otherwise a build with no
    // wrapping note field at all would pass this check for the wrong reason.
    check('every case has a wrapping note field', shipped.length, 6);
    check('the longest shipped note is not clipped in either direction',
      shipped.length === 6 && shipped.every(b => b.clipY <= 1 && b.clipX <= 1), true);

    await p.fill('#evalsTable tr:nth-child(2) textarea', 'x '.repeat(160));
    await p.waitForTimeout(200);
    check('a note typed now grows its box too',
      (await boxes())[0].clipY <= 1, true);
    await p.click('#evalsTable th');
    await p.reload();
    await p.waitForTimeout(400);
    await p.click('#tab-evals');
    await p.waitForTimeout(300);
    check('and survives a reload', await p.$eval('#evalsTable textarea', t => t.value.length), 320);
  });

  await section('the second check stands beside the first, not over it', async () => {
    const p = await page();
    await p.click('#tab-evals');
    await p.waitForTimeout(300);
    check('the tab says a model-on check happened, and when',
      /Model-on check · 2026-08-06: the same six cases re-run with live model/.test(await flat(p, '#modelcheck')), true);
    check('and names what diverged',
      /5 matched; E-3 diverged and was judged again/.test(await flat(p, '#modelcheck')), true);
    check('the tiles are still the first check, and say so',
      /The tiles above are the first check, and stay that way/.test(await flat(p, '#modelcheck')), true);

    const row = n => flat(p, `#evalsTable tr:nth-child(${n}) td:last-child`);
    check('E-3 carries both judgements, in order',
      /Pass.*first check · 2026-07-27.*Needs work.*model-on check · 2026-08-06/.test(await row(4)), true);
    check('and the second judgement carries its reason',
      /named the section, checked the threshold, said the threshold was not met, and escalated anyway/.test(await row(4)), true);
    check('the first-check verdict is untouched by it',
      await p.evaluate(() => EVAL_SEED['E-3'].verdict), 'Pass');
    check('a case that matched carries no second verdict',
      /model-on check/.test(await row(2)), false);
    check('but its Actual records that it was checked',
      / model-on check · 2026-08-06 · live model.*· same result$/.test(await flat(p, '#actual-E-1')), true);
    check("E-3's Actual says what the model produced instead",
      /DIFFERS — REFUSED - model-added stop \(one-way rule\)/.test(await flat(p, '#actual-E-3')), true);
  });

  await section('a run says it is running', async () => {
    const p = await page();
    await p.route('https://api.anthropic.com/**', async r => {
      await new Promise(res => setTimeout(res, 400));
      r.fulfill({ status: 200, contentType: 'application/json',
        body: JSON.stringify({ content: [{ type: 'text', text: 'STATUS: OK\nWHY: x\nCOACHING_LINE: y' }] }) });
    });
    await p.fill('#apiKey', 'sk-ant-regression-busy');
    await p.click('button:has-text("Save")');
    await p.waitForTimeout(200);
    await p.click('text=D-1001');
    await p.waitForTimeout(250);
    const runBtn = () => p.$eval('#work button.run', b => ({
      dimmed: +getComputedStyle(b).opacity < 1,
      clickable: getComputedStyle(b).pointerEvents !== 'none',
      says: getComputedStyle(b, '::after').content }));
    check('idle: solid, clickable, no running label',
      await runBtn(), { dimmed: false, clickable: true, says: 'none' });

    p.click('#work >> button:has-text("Run")').catch(() => {});
    await p.waitForTimeout(150);
    const during = await runBtn();
    check('while running: dimmed, not clickable, and says so',
      { dimmed: during.dimmed, clickable: during.clickable, running: /running/.test(during.says) },
      { dimmed: true, clickable: false, running: true });
    check('the tabs stay usable throughout',
      await p.$eval('#tab-evals', b => getComputedStyle(b).pointerEvents), 'auto');

    await p.waitForTimeout(1200);
    check('and it goes back to normal when the run ends',
      await runBtn(), { dimmed: false, clickable: true, says: 'none' });
  });

  await section('nothing that accumulates can be started twice', async () => {
    // Offline the whole loop is synchronous, so a double start cannot interleave and a
    // test run without a key passes on the buggy build too. The bug needs the awaits:
    // a key saved, and a model call per row.
    const p = await page();
    await p.route('https://api.anthropic.com/**', async r => {
      await new Promise(res => setTimeout(res, 40));
      r.fulfill({ status: 200, contentType: 'application/json',
        body: JSON.stringify({ content: [{ type: 'text', text: 'STATUS: REFUSED-ESCALATE\nWHY: x\nCLIENT_MESSAGE: y' }] }) });
    });
    await p.fill('#apiKey', 'sk-ant-regression-double');
    await p.click('button:has-text("Save")');
    await p.waitForTimeout(200);
    await p.click('#tab-evals');
    await p.waitForTimeout(300);
    await p.evaluate(() => { runProbe(); runProbe(); });   // two clicks, one tick
    await p.waitForTimeout(9000);
    check('a double-started check still counts exactly ten',
      await p.$$eval('#probe .stat', els => els.map(e => e.textContent.replace(/\s+/g, ' ').trim())),
      ['0/10Screening caught', '0Soft flag only', '10Screening missed', '10/10Model caught']);
    check('and the run raised no page errors', p.errors, []);
  });

  await section('the Memory tab claims only what it holds', async () => {
    const p = await page();
    await p.click('#tab-memory');
    await p.waitForTimeout(300);
    const m = await flat(p, '#view-memory');
    check('a browser that judged nothing says so',
      /6 from the first check \(2026-07-27\) - none judged in this browser yet/.test(m), true);
    check('the heading names the browser, not the session',
      /REMEMBERED IN THIS BROWSER/.test(m), true);
    check('the session-only rows are marked as such',
      (m.match(/this session only/g) || []).length, 2);
    check('there is no claim of a day close that does not happen',
      /at day close it collapses to totals/.test(m), false);
    check('and the budget is listed as not held',
      /not held at all - recomputed from the plan and the seeded day/.test(m), true);

    // judge one here, and only that one becomes something this browser remembers
    await p.click('#tab-evals');
    await p.waitForTimeout(300);
    await p.click('#evalsTable tr:nth-child(2) td:last-child >> text="change"');
    await p.waitForTimeout(250);
    await p.click('#evalsTable tr:nth-child(2) td:last-child button:has-text("Pass")');
    await p.waitForTimeout(250);
    await p.click('#tab-memory');
    await p.waitForTimeout(300);
    check('a verdict judged here is counted apart from the five that came with the file',
      /5 from the first check \(2026-07-27\), 1 judged in this browser/.test(await flat(p, '#view-memory')), true);
  });

  await section('key hygiene', async () => {
    const CANARY = 'sk-ant-regression-canary-value';
    const p = await page();
    await p.fill('#apiKey', CANARY);
    await p.click('button:has-text("Save")');
    await p.waitForTimeout(300);
    check('key value absent from rendered text', (await p.textContent('body')).includes(CANARY), false);
    check('key value absent from the DOM', (await p.content()).includes(CANARY), false);
    await p.click('#tab-memory');
    await p.waitForTimeout(250);
    check('memory tab discloses the key', /Your API key/.test(await flat(p, '#view-memory')), true);
    await p.click('button:has-text("Forget all")');
    await p.waitForTimeout(250);
    check('Forget all keeps the key, as stated',
      await p.evaluate(() => !!localStorage.getItem('platemate_api_key')), true);
    await p.click('button:has-text("Remove key")');
    await p.waitForTimeout(250);
    check('Remove key clears it',
      await p.evaluate(() => !localStorage.getItem('platemate_api_key')), true);
  });

  await section('status chip honesty', async () => {
    const p = await page();
    check('no key', await flat(p, '#statusChip'), 'offline rules mode');
    await p.fill('#apiKey', 'sk-ant-x');
    await p.click('button:has-text("Save")');
    await p.waitForTimeout(250);
    check('key saved, nothing run', await flat(p, '#statusChip'), 'key saved · runs use claude-sonnet-4-5');

    await p.route('https://api.anthropic.com/**', r => r.fulfill({
      status: 404, contentType: 'application/json', body: '{"error":"not_found"}' }));
    await runCase(p, 'D-1001');
    check('retired model reported honestly', await flat(p, '#statusChip'),
      'model claude-sonnet-4-5 unavailable (404) — running offline rules');
    check('retired model still produces a card', /Budget/.test(await flat(p, '#work')), true);
  });

  await browser.close();
  const failed = results.filter(r => !r.pass);
  console.log(`\n${results.length - failed.length}/${results.length} passed`);
  if (failed.length) console.log('failed: ' + failed.map(f => f.name).join(', '));
  process.exit(failed.length ? 1 : 0);
})();
