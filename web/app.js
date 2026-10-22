const app = document.querySelector('#app');
const YEARS = ['2023-24', '2024-25', '2025-26'];
const escape = value => String(value).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const money = (n, digits = 0) => '$' + n.toLocaleString('en-US', { minimumFractionDigits: digits, maximumFractionDigits: digits });
let selectedYear = '2025-26';
let budget, templates, layouts;
const allocations = year => budget.filter(r => r.metric_type === 'allocation' && r.amount !== null && (!year || r.fiscal_year === year));
const total = year => allocations(year).reduce((sum, r) => sum + r.amount, 0);
const fill = (key, values = {}) => templates[key].replace(/\{(\w+)\}/g, (_, name) => escape(values[name] ?? ''));
const metric = (label, value, note) => `<div class="metric-card"><div class="metric-label">${escape(label)}</div><div class="metric-value">${escape(value)}</div><div class="metric-note">${escape(note)}</div></div>`;
const heading = (title, description) => `<div class="section-title">${title}</div><div class="section-description">${description}</div>`;
function navigation(section) {
  return `<nav class="st-key-top_nav" aria-label="Main navigation"><div class="nav-columns" data-testid="stHorizontalBlock">${['home', 'compare', 'requests', 'programs', 'about'].map((name, i) => `<div data-testid="stColumn"><div data-testid="stButton"><button type="button" data-section="${name}" kind="${i === 0 ? 'tertiary' : name === section ? 'primary' : 'secondary'}" ${name === section ? 'aria-current="page"' : ''}><p>${i === 0 ? 'S&A BUDGET EXPLORER' : name.toUpperCase()}</p></button></div></div>`).join('')}</div></nav>`;
}
function home() {
  const latest = total('2025-26'), start = total('2023-24');
  const programs = allocations('2025-26').filter(r => r.amount > 0).sort((a, b) => b.amount - a.amount);
  const biggest = programs[0];
  const hero = templates['hero-shell'].replace('data:image/png;base64,{mascot_base64}', 'assets/tiger_mascot.png');
  return `${hero}<div id="overview"></div><main class="overview-layout"><div class="overview-main">${templates['overview-intro']}
    <div class="metric-grid">${metric('FY2025–26 Allocation', `$${(latest / 1e6).toFixed(2)}M`, 'Total S&A allocation')}${metric('Change Since FY2023–24', `+${((latest-start)/start*100).toFixed(1)}%`, `+${money(latest-start)} across the three-year view`)}${metric('Funded Programs', new Set(programs.map(r => r.program_name_standardized)).size, 'Programs with a positive FY2025–26 allocation')}${metric('Largest Allocation', `$${(biggest.amount/1000).toFixed(1)}K`, `${biggest.program_name_standardized} · ${(biggest.amount/latest*100).toFixed(1)}% of budget`)}</div>
    ${heading('Total allocation over time', 'Overall S&A allocation from FY2023–24 through FY2025–26.')}
    <div class="chart-frame" data-testid="stPlotlyChart"><div id="trend-chart" class="chart" role="img" aria-label="Total allocation over time"></div></div>
    ${heading('Where the money goes', 'The ten largest program allocations for the selected fiscal year.')}
    <div class="year-selector"><label for="fiscal-year">Fiscal year</label><select id="fiscal-year">${YEARS.map(year => `<option ${year === selectedYear ? 'selected' : ''}>${year}</option>`).join('')}</select></div>
    <div class="chart-frame" data-testid="stPlotlyChart"><div id="ranking-chart" class="chart" role="img" aria-label="Ten largest program allocations"></div></div>
    </div></main><div class="page-footer-space"></div>`;
}
function compare() {
  const start = total(YEARS[0]), latest = total(YEARS[2]);
  const grouped = new Map();
  for (const r of allocations()) {
    if (!grouped.has(r.program_name_standardized)) grouped.set(r.program_name_standardized, {});
    const values = grouped.get(r.program_name_standardized);
    values[r.fiscal_year] = (values[r.fiscal_year] ?? 0) + r.amount;
  }
  const increases = [...grouped].filter(([,v]) => v[YEARS[0]] !== undefined && v[YEARS[2]] !== undefined).map(([name,v]) => ({ name, start: v[YEARS[0]], end: v[YEARS[2]], change: v[YEARS[2]]-v[YEARS[0]] })).filter(r => r.change > 0).sort((a,b) => b.change-a.change).slice(0,5);
  return `<main>${templates['compare-page']}${templates['compare-section-intro']}
    <div class="st-key-compare_snapshot_cards"><div class="snapshot-grid">${YEARS.map((year, i) => `<div class="compare-year-card"><div class="compare-year">FY${year}</div><div class="compare-year-value">$${(total(year)/1e6).toFixed(2)}M</div><div class="compare-year-note">Total allocation</div><div class="compare-year-change">${i === 0 ? 'Starting year' : `+${((total(year)-total(YEARS[i-1]))/total(YEARS[i-1])*100).toFixed(1)}% from prior year`}</div></div>`).join('')}</div></div>
    <section class="compare-summary"><div class="compare-summary-label">Across the three-year view</div><div class="compare-summary-text">Total S&A allocation increased by <strong>${money(latest-start)}</strong> from FY2023–24 to FY2025–26, a <strong>${((latest-start)/start*100).toFixed(1)}%</strong> increase.</div></section>
    ${templates['compare-movers-intro']}<div class="st-key-compare_increases">${increases.map((r, i) => `<div class="increase-row"><div class="increase-rank">${i+1}</div><div class="increase-main"><div class="increase-program">${escape(r.name)}</div><div class="increase-years">FY2023–24 <strong>${money(r.start)}</strong><span class="increase-arrow">→</span>FY2025–26 <strong>${money(r.end)}</strong></div></div><div class="increase-change">+${money(r.change)}</div></div>`).join('')}</div></main>`;
}
const placeholders = {
  requests: { label: 'Requests', title: 'What was requested — and what was allocated?', description: 'Explore program funding requests, final allocations, funding gaps, and decision-year outcomes.' },
  programs: { label: 'Programs', title: 'Explore one program at a time', description: 'Follow individual programs across years and understand their allocations, requests, budget share, and organizational changes.' },
  about: { label: 'About', title: 'Why this project exists', description: "Learn about the project's inspiration, data sources, methodology, limitations, and the questions behind this student-created research dashboard." }
};
function ranking() {
  const data = allocations(selectedYear).filter(r => r.amount > 0).sort((a,b) => b.amount-a.amount).slice(0,10).reverse();
  return Plotly.react('ranking-chart', [{ type: 'bar', orientation: 'h', x: data.map(r => r.amount), y: data.map(r => r.program_name_standardized), marker: { color: '#168C8C', line: { width: 0 } }, hovertemplate: '<b>%{y}</b><br>Allocation: $%{x:,.2f}<extra></extra>' }], structuredClone(layouts.ranking), { displayModeBar: false, responsive: true });
}
async function render() {
  let section = new URLSearchParams(location.search).get('section') || 'home';
  if (!['home','compare','requests','programs','about'].includes(section)) section = 'home';
  for (const el of document.querySelectorAll('.js-plotly-plot')) Plotly.purge(el);
  app.innerHTML = navigation(section) + (section === 'home' ? home() : section === 'compare' ? compare() : fill('subpage-shell', placeholders[section]));
  if (section === 'home') {
    await Promise.all([
      Plotly.newPlot('trend-chart', [{ type: 'scatter', x: YEARS, y: YEARS.map(total), mode: 'lines+markers+text', line: { color: '#168C8C', width: 4 }, marker: { size: 11, color: '#168C8C', line: { color: '#FFFFFF', width: 2 } }, text: YEARS.map(y => `$${(total(y)/1e6).toFixed(2)}M`), textposition: 'top center', textfont: { color: '#172033', size: 12 }, hovertemplate: '<b>%{x}</b><br>Allocation: $%{y:,.2f}<extra></extra>' }], structuredClone(layouts.trend), { displayModeBar: false, responsive: true }),
      ranking()
    ]);
    if (location.hash === '#overview') document.querySelector('#overview').scrollIntoView();
  }
}
app.addEventListener('click', event => {
  const button = event.target.closest('[data-section]');
  if (!button) return;
  const url = new URL(location.href); url.searchParams.set('section', button.dataset.section); url.hash = '';
  history.pushState(null, '', url); render(); window.scrollTo(0,0);
});
app.addEventListener('change', event => {
  if (event.target.id === 'fiscal-year') { selectedYear = event.target.value; ranking(); }
});
window.addEventListener('popstate', render);
try {
  [budget, templates, layouts] = await Promise.all(['budget.json', 'templates.json', 'chart-layouts.json'].map(async file => { const response = await fetch(file); if (!response.ok) throw Error(`Unable to load ${file}`); return response.json(); }));
  await render();
} catch (error) {
  console.error(error);
  app.innerHTML = '<main class="subpage-shell"><div class="subpage-title">Unable to load the dashboard</div><p>Please refresh the page to try again.</p></main>';
}
