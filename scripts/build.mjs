import { mkdir, copyFile, cp, readFile, writeFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
const root = fileURLToPath(new URL('../', import.meta.url));
process.chdir(root);
await mkdir('dist', { recursive: true });
for (const file of ['index.html', 'app.js', 'runtime.css', 'templates.json', 'chart-layouts.json']) await copyFile(`web/${file}`, `dist/${file}`);
await copyFile('app/styles.css', 'dist/styles.css');
await copyFile('app/compare.css', 'dist/compare.css');
await cp('app/assets', 'dist/assets', { recursive: true });
await cp('web/vendor', 'dist/vendor', { recursive: true });
// Parse quoted CSV fields (including embedded newlines) without changing source data.
export function parseCSV(input) {
  const rows = []; let row = [], field = '', quoted = false;
  for (let i = 0; i < input.length; i++) {
    const c = input[i];
    if (c === '"') {
      if (quoted && input[i + 1] === '"') { field += '"'; i++; }
      else quoted = !quoted;
    } else if (c === ',' && !quoted) { row.push(field); field = ''; }
    else if (c === '\n' && !quoted) { row.push(field.replace(/\r$/, '')); rows.push(row); row = []; field = ''; }
    else field += c;
  }
  if (field || row.length) { row.push(field.replace(/\r$/, '')); rows.push(row); }
  const headers = rows.shift();
  return rows.filter(r => r.some(Boolean)).map(r => Object.fromEntries(headers.map((h, i) => [h, r[i] ?? ''])));
}
const rows = parseCSV(await readFile('data/processed/sa_budget_canonical.csv', 'utf8'));
const years = ['2023-24', '2024-25', '2025-26'];
const budget = rows.filter(r => years.includes(r.fiscal_year)).map(r => ({ ...r, amount: r.amount === '' ? null : Number(r.amount) }));
for (const year of years) {
  const allocations = budget.filter(r => r.fiscal_year === year && r.metric_type === 'allocation');
  if (!allocations.length || allocations.some(r => r.amount !== null && !Number.isFinite(r.amount))) throw Error(`Invalid allocations for ${year}`);
}
await writeFile('dist/budget.json', JSON.stringify(budget));
console.log(`Built dist/: ${budget.length} budget records; original CSS and image assets copied unchanged.`);
