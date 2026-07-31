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
      'Sweep done: 7 OK · 2 REFUSED-ESCALATE · 1 out-of-scope · 6 clarify · 0 errors');
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
