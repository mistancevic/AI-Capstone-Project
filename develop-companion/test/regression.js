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
    const stamps = () => p.$$eval('#evalsTable td[id^="actual-"] .metaline', e => e.map(x => x.textContent.trim()));
    check('a shipped result says so, and is not passed off as a local run',
      (await stamps()).every(t => /shipped result/.test(t)), true);

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
      after.map(t => /^run /.test(t)), [true, false, false, false, true, false]);
    check('the stamp carries a time, not just a date',
      /^run \d{4}-\d{2}-\d{2} \d{2}:\d{2} · /.test(after[0]), true);
    check('a pre-model stop records that no model was called',
      /· no model call$/.test(after[4]), true);
    check('a run that reached the agent records which mode it used',
      /· offline rules|· live model/.test(after[0]), true);
  });

  await section('the scoreboard counts this session, not the shipped seed', async () => {
    const p = await page();
    await p.click('#tab-evals');
    await p.waitForTimeout(300);
    const board = async () => (await flat(p, '#scoreboard'));
    check('a fresh browser has re-run nothing', /0\/6Run in this browser/.test(await board()), true);
    check('shipped verdicts still count as recorded judgements', /6Pass/.test(await board()), true);

    await p.click('#evalsTable >> tr:has-text("E-1") >> button:has-text("Run")');
    await p.waitForTimeout(1400);
    check('running one moves the count', /1\/6Run in this browser/.test(await board()), true);

    await p.click('#tab-memory');
    await p.waitForTimeout(300);
    await p.click('button:has-text("Forget all")');
    await p.waitForTimeout(500);
    await p.click('#tab-evals');
    await p.waitForTimeout(400);
    check('Forget all returns the table to the shipped state',
      /0\/6Run in this browser/.test(await board()) && /2026-07-27 \(shipped\)/.test(await board()), true);
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
      /run \d{4}-\d{2}-\d{2} \d{2}:\d{2}/.test(await flat(p, '#actual-E-1')), true);

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
    // div.metaline, not .metaline: the "change" link is a span carrying the same class
    const prov = () => p.$$eval('#evalsTable td:last-child > div.metaline',
      els => els.map(x => x.textContent.trim()));
    check('every shipped verdict says it came with the file',
      await prov(), Array(6).fill('recorded 2026-07-27'));

    // re-judge E-1 here: change, then pick a verdict
    await p.click('#evalsTable tr:nth-child(2) >> text=change');
    await p.waitForTimeout(300);
    check('changing a verdict drops its provenance line too',
      (await prov()).length, 5);
    await p.click('#evalsTable tr:nth-child(2) button:has-text("Needs work")');
    await p.waitForTimeout(300);
    check('a verdict judged here says so, with a time',
      /^judged here · \d{4}-\d{2}-\d{2} \d{2}:\d{2}$/.test((await prov())[0]), true);
    check('and the five inherited ones are untouched',
      (await prov()).slice(1), Array(5).fill('recorded 2026-07-27'));
    check('the scoreboard follows the new judgement',
      /5Pass 1Needs work/.test(await flat(p, '#scoreboard')), true);

    await p.reload();
    await p.waitForTimeout(400);
    await p.click('#tab-evals');
    await p.waitForTimeout(300);
    check('the judgement and its stamp survive a reload',
      /^judged here · \d{4}/.test((await prov())[0]), true);
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
