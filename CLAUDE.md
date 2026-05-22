# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Educational dashboard (in Portuguese) covering competitive markets and the role of the state in the economy. Topics include Consumer Theory, Firm Theory, General Equilibrium, Pareto Efficiency, Monopoly vs. Competition, Public Goods & Externalities, Musgrave Functions, and an interactive Quiz.

## Running the App

```bash
pip install -r requirements.txt
streamlit run app.py
```

The dev container auto-starts the server on port 8501 with:
```
streamlit run app.py --server.enableCORS false --server.enableXsrfProtection false
```

There is no test suite or linter configured.

## Architecture

**This is a single-file Streamlit app (`app.py`, ~1380 lines).** There are no modules, packages, or separate component files — all logic, UI, and data live in one file.

### Structure within `app.py`

1. **Page config + custom CSS** — inline CSS injected via `st.markdown(..., unsafe_allow_html=True)` at the top of the file. CSS class names to know: `.main-header`, `.concept-card`, `.metric-box`, `.quiz-correct`, `.quiz-incorrect`.

2. **Tab layout** — 9 tabs created via `st.tabs([...])` and rendered in a single `with tabs[n]:` block each. Tabs are numbered 0–8 and correspond in order to: Visão Geral, Teoria do Consumidor, Teoria da Firma, Equilíbrio Geral, Caixa de Edgeworth, Monopólio vs. Concorrência, Bens Públicos & Externalidades, Funções de Musgrave, Quiz.

3. **Interactive charts** — all charts are built with `plotly.graph_objects` (`go.Figure`). The pattern is: sliders → analytic computation → figure construction → `st.plotly_chart(fig, use_container_width=True)`. Each tab that has a chart follows a `col_params | col_graph` two-column split.

4. **Session state** — only the Quiz tab (Tab 9) uses `st.session_state` (keys: `quiz_answers`, `quiz_submitted`). All other tabs are stateless — slider values are computed fresh on each rerender.

5. **Sidebar** — at the bottom of the file, renders quick-reference expanders for each topic.

### Key Conventions

- All Plotly figures use `template='plotly_dark'`, `paper_bgcolor='#0e1117'`, `plot_bgcolor='#1a1a2e'`, and grid color `'#2a2a4e'` — match this in any new chart.
- Primary accent color: `#e94560` (red). Secondary: `#4ecdc4` (teal). Highlight: `#f9d923` (yellow). Text muted: `#a7b5c9`.
- All economic models use **Cobb-Douglas** functions (`U = x1^α * x2^(1-α)`, `F = A * z1^γ * z2^(1-γ)`). The analytic solutions are computed inline rather than via numerical solvers.
- Slider widget keys follow the pattern `"{tab_prefix}_{param}"` (e.g., `"cons_alpha"`, `"firm_w1"`, `"mono_a"`), which matters for Streamlit state isolation between tabs.

## Theming

`.streamlit/config.toml` sets the dark theme globally:
- `primaryColor = "#e94560"`
- `backgroundColor = "#0e1117"`
- `secondaryBackgroundColor = "#1a1a2e"`
- `textColor = "#c4cdd8"`
