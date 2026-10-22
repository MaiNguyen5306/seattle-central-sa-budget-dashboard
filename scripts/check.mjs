import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import vm from 'node:vm';
import './build.mjs';
const budget = JSON.parse(await readFile('dist/budget.json'));
const templates = JSON.parse(await readFile('dist/templates.json'));
const layouts = JSON.parse(await readFile('dist/chart-layouts.json'));
for (const [year, expected] of Object.entries({ '2023-24': 1513171.18, '2024-25': 1733008.51, '2025-26': 1801888.48 })) {
  const sum = budget.filter(r => r.fiscal_year === year && r.metric_type === 'allocation').reduce((s,r) => s+(r.amount ?? 0),0);
  assert.ok(Math.abs(sum-expected)<0.005, `Allocation total: ${year}`);
}
for (const name of ['styles.css', 'compare.css']) assert.deepEqual(await readFile(`dist/${name}`), await readFile(`app/${name}`));
assert.deepEqual(await readFile('dist/assets/tiger_mascot.png'), await readFile('app/assets/tiger_mascot.png'));
const events = {}, plots = [];
const app = { innerHTML: '', addEventListener: (name, handler) => { events[name] = handler; } };
const data = { 'budget.json': budget, 'templates.json': templates, 'chart-layouts.json': layouts };
const context = vm.createContext({
  document: { querySelector: selector => selector === '#app' ? app : { scrollIntoView() {} }, querySelectorAll: () => [] },
  location: { href: 'http://localhost/', search: '', hash: '' },
  URL, URLSearchParams, structuredClone, console,
  history: { pushState(_, __, url) { context.location.href = url.href; context.location.search = url.search; context.location.hash = url.hash; } },
  window: { addEventListener() {}, scrollTo() {} },
  fetch: async file => ({ ok: true, json: async () => data[file] }),
  Plotly: { purge() {}, newPlot: async (id, traces, layout) => plots.push({ id, traces, layout }), react: async (id, traces, layout) => plots.push({ id, traces, layout }) }
});
let source = await readFile('web/app.js','utf8');
await vm.runInContext(`(async () => { ${source} })()`,context);
assert.ok(app.innerHTML.includes('hero-shell'));
assert.ok(app.innerHTML.includes('$1.80M'));
assert.ok(app.innerHTML.includes('+19.1%'));
assert.equal(plots.length,2);
for (const year of ['2023-24','2024-25','2025-26']) {
  events.change({ target: { id: 'fiscal-year', value: year } });
  const plot = plots.at(-1);
  assert.equal(plot.id,'ranking-chart'); assert.equal(plot.traces[0].x.length,10);
  assert.deepEqual(plot.traces[0].x, budget.filter(r => r.fiscal_year === year && r.metric_type === 'allocation' && r.amount > 0).sort((a,b) => b.amount-a.amount).slice(0,10).reverse().map(r => r.amount));
}
for (const section of ['compare','requests','programs','about','home']) {
  events.click({ target: { closest: () => ({ dataset: { section } }) } });
  await new Promise(resolve => setImmediate(resolve));
  assert.ok(app.innerHTML.includes(`aria-current="page"`));
  if (section === 'compare') { assert.equal((app.innerHTML.match(/class="increase-row"/g)||[]).length,5); assert.ok(app.innerHTML.includes('$288,717')); }
  else if (section === 'home') assert.ok(app.innerHTML.includes('hero-shell'));
  else assert.ok(app.innerHTML.includes('This section will be designed and built next.'));
}
console.log('Passed: source CSS/image parity, allocation totals, all five routes, all three year selections, chart data, comparison rows. Browser pixel comparison is a separate check.');
