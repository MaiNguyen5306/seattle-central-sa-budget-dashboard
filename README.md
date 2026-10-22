# Seattle Central S&A Budget Explorer

Interactive dashboard analyzing Seattle Central College S&A allocations, requests, and historical budget trends.

## Vercel web version

The browser version uses HTML, CSS, JavaScript, and locally bundled Plotly. It requires Node.js 22 or newer, with no npm dependencies or Python server. The original Streamlit application and research pipeline remain available.

```sh
npm run dev
```

Open `http://localhost:3000`. Restart the command after source edits to rebuild the preview.

```sh
npm run build
npm run check
```

The build produces `dist/`. The checks verify budget totals, identical copied CSS and tiger image, navigation, year selection, chart data, and comparison rows. They do not perform a browser screenshot comparison.

### Deploy to Vercel

Import this GitHub repository into Vercel, using the repository root as the Root Directory. The included `vercel.json` configures:

- Framework Preset: **Other**
- Build Command: **npm run build**
- Output Directory: **dist**

No environment variables are required. If the Vercel project has existing build overrides, update them to these values. Deployment publishes only the built dashboard and its budget dataset, not the research notebooks, training notes, or source PDFs. These changes must be committed and pushed before a Git-based Vercel deployment can use them.

Vercel hosts the site; make design changes in this repository and redeploy to see them on Vercel.

### Continue designing

- `app/styles.css`: original shared design, hero, navigation, cards, chart frames, and responsive rules.
- `app/compare.css`: original Compare page design.
- `app/assets/`: original images, copied unchanged during builds.
- `web/templates.json`: existing page markup and wording, initially extracted from the Streamlit source.
- `web/app.js`: browser navigation, metrics, comparison cards, year selector, and charts.
- `web/runtime.css`: browser layout equivalents for Streamlit containers and widgets.
- `web/chart-layouts.json`: original Plotly chart layout definitions.
- `data/processed/sa_budget_canonical.csv`: authoritative dashboard data, read on every build.

The browser page markup and chart layouts are independent of the Python rendering code after migration. Update the `web/` files when changing the Vercel version. Both versions share the original CSS, image assets, and canonical CSV.

Home and Compare retain their existing content and controls. Requests, Programs, and About retain the existing placeholders. Navigation keeps the `?section=compare` URL format and supports browser Back/Forward. The fiscal-year selector updates the top-ten chart without reloading the page.

The original stylesheet and image bytes are preserved. Browser layout is implemented separately from Streamlit, so exact pixel parity still requires comparing both versions in a browser at matching viewport sizes.

## Original Streamlit version

With your Python environment activated:

```sh
streamlit run app/app.py
```

The five notebooks in `notebooks/` preserve extraction, cleaning, budget analysis, fee/enrollment context, and international funding research. Supporting sources and limitations are documented in `docs/` and `source_docs/SOURCES.md`.
