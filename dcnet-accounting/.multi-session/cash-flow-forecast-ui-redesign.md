# Task: Cash Flow Forecast UI Redesign — Tasks 3-10 (JS rewrites + cleanup + i18n + live QA)

## Context

The `vn_accounting` Cash Flow Forecast page (`/app/cash-flow-forecast`) is being redesigned per a brainstormed mockup. The new layout: Frappe-native filter row → 4 KPI cards (Closing/Net/Inflow/Outflow) → 4-line balance projection chart → horizontal pivot table (period × source) with click-to-filter → server-paginated detail table grouped by Confidence with search.

Backend Tasks 1+2 are committed (`da6bd00`, `03b0a65`): pure helpers `_filter_entries`, `_compute_group_totals`, `CONFIDENCE_ORDER` plus the new `get_forecast_entries(...)` paginated API that reuses the Redis cache key `forecast:{c}:{from}:{to}` from `get_forecast_data`. 20 unit tests green.

Remaining work (Tasks 3-10 in the plan): replace the entire JS rendering layer (~903 lines), strip ~150 lines of `.fcf-*` CSS, delete the now-unused `get_drilldown_entries` API and dead JS factories, append 37 Vietnamese translations, and live-QA the page in a browser.

**Source-of-truth documents** (must read at session start):
- Plan: `apps/vn_accounting/docs/plans/2026-04-28-cash-flow-forecast-ui-redesign.md` — Tasks 3-10 with exact code blocks and step-by-step instructions
- Spec: `apps/vn_accounting/docs/specs/2026-04-28-cash-flow-forecast-ui-redesign-design.md` — visual layout, behavior, edge cases
- Session 1 wrap-up: `.multi-session/session-last-cash-flow-forecast-ui-redesign.md`

## Scope

- **Project**: `/home/long/long/frappe-bench-dcnet` (bench root)
- **Working directory**: `/home/long/long/frappe-bench-dcnet/.worktrees/vn_accounting-cash-flow-ui` (worktree)
- **Branch**: `feat/cash-flow-forecast-ui-redesign` (already checked out — do NOT create a new branch)
- **Live testing**: requires temporarily switching `apps/vn_accounting` to this branch — see Constraints
- **Related files** (all paths relative to worktree root):

| File | Status | Description |
|------|--------|-------------|
| `vn_accounting/vn_accounting/page/cash_flow_forecast/cash_flow_forecast.js` | REWRITE (~903 → ~600 lines) | Tasks 3-7: filter row, KPI cards, chart, pivot, detail table |
| `vn_accounting/vn_accounting/page/cash_flow_forecast/cash_flow_forecast.css` | EDIT (~311 → ~160 lines) | Strip `.fcf-*` legacy classes, keep new `.cff-*` and add KPI/pivot styles |
| `vn_accounting/api/forecast.py` | EDIT (Task 8) | Remove `get_drilldown_entries` whitelisted endpoint (lines 102-149) |
| `vn_accounting/translations/vi.csv` | APPEND (Task 9) | Add 37 new Vietnamese translations for the redesigned UI |
| `vn_accounting/api/test_forecast_entries.py` | KEEP | 20 existing tests must continue to pass |

Read the plan file for the exact code blocks for each task. Do not invent code that diverges from the plan — the plan was already self-reviewed and survived 9-issue Phase 2 walk-through.

## Requirements

Execute plan tasks **3 → 4 → 5 → 6 → 7 → 8 → 9 → 10** in order. Each plan task has its own checkboxes and a commit step. Work in plan order; commit at the end of each plan task with the message format the plan specifies.

### Task 3 — JS filter row via `page.add_field()`
Replace the existing custom HTML `.fcf-filters` row with 7 native Frappe filter controls (Granularity Select, From Date, To Date, Confidence MultiCheck, Inflow MultiCheck, Outflow MultiCheck, Search Data) created via `page.add_field()`. Strip all `.fcf-*` filter CSS. If `MultiCheck` overflows the row, fall back per plan §3 to `MultiSelect` or a "Confidence" dialog button (plan documents the fallback explicitly).

### Task 4 — 4 KPI cards
Replace `render_summary()` with 4 cards: Closing Balance, Net Cash Flow, Total Inflow, Total Outflow. Each card has icon, label, value, and color cue. Use `frappe.format(value, {fieldtype: "Currency"})`.

### Task 5 — 4-line chart
Replace `render_chart()` with `frappe.Chart` line chart, 4 datasets stacked by confidence (overdue/committed/probable/possible). Use the existing summary cells data (no extra API call). Per plan §5.3, if 4-line null gaps render as interpolation, fall back to single Balance dataset + clip-path split.

### Task 6 — Horizontal pivot table
Replace `render_table()` with horizontal pivot: rows = sources (Sales Order/Purchase Order/Salary/etc.), columns = periods. Click a column header → highlight column + filter the detail table by `period_key`. Click again to deselect.

### Task 7 — Paginated detail table grouped by Confidence
Replace the legacy drill-down with a detail table that calls `frappe.xcall("vn_accounting.api.forecast.get_forecast_entries", {...})`. Group entries visually by confidence (overdue → committed → probable → possible) with group totals from the API response. Pagination 20/page. Search box filters server-side. Click on pivot column updates `period_key` filter.

### Task 8 — Cleanup
Remove the `@frappe.whitelist()` `get_drilldown_entries` endpoint (`vn_accounting/api/forecast.py` lines ~102-149) and any JS callers/factories that depended on it. Verify no other JS file references `get_drilldown_entries`.

### Task 9 — i18n
Append 37 new source→translation rows to `vn_accounting/translations/vi.csv`. Plan §9 lists the exact strings. Format: 2-column CSV `source,translated`. Run `bench --site dcnet.localhost clear-cache` for translations to refresh.

### Task 10 — Final verification
Run unit tests, build, clear-cache, navigate via Playwright MCP, take before/after screenshots, verify console errors = 0, then close branch state.

## Acceptance Criteria

Each item must be verifiable. Mark `[x]` only when evidence is captured.

**Functionality (per plan task):**
- [ ] Task 3 done: filter row uses `page.add_field()` (no `.fcf-*` filter HTML/CSS remaining); MultiCheck or documented fallback in place
- [ ] Task 4 done: 4 KPI cards render with icon, label, currency-formatted value, and color
- [ ] Task 5 done: 4-line confidence chart renders without console error; if fallback used, documented in commit message
- [ ] Task 6 done: pivot table is horizontal (rows = sources, columns = periods); clicking a column header highlights it and filters detail table
- [ ] Task 7 done: detail table shows server-paginated entries grouped by confidence with group totals; search filters server-side
- [ ] Task 8 done: `get_drilldown_entries` removed from `vn_accounting/api/forecast.py`; `grep -r "get_drilldown_entries" vn_accounting/` returns no live JS references
- [ ] Task 9 done: `vn_accounting/translations/vi.csv` line count increased by ≥ 37 vs Task 1 baseline; new strings parseable via Python's `csv.reader`

**Build + tests:**
- [ ] Unit tests pass: `PYTHONPATH=.:/home/long/long/frappe-bench-dcnet/apps/frappe /home/long/long/frappe-bench-dcnet/env/bin/python -m unittest vn_accounting.api.test_forecast_entries -v` reports 20/20 OK
- [ ] No syntax errors in JS: `node --check vn_accounting/vn_accounting/page/cash_flow_forecast/cash_flow_forecast.js` returns 0
- [ ] No syntax errors in Python: `/home/long/long/frappe-bench-dcnet/env/bin/python -m py_compile vn_accounting/api/forecast.py` returns 0
- [ ] `bench build --app vn_accounting` succeeds (run from bench root after switching `apps/vn_accounting` to feature branch)

**Live QA via Playwright MCP** (after `bench build` + `bench clear-cache`):
- [ ] Navigate to `http://dcnet.localhost:8001/app/cash-flow-forecast` — page loads, no white screen
- [ ] Browser console shows 0 errors and 0 warnings (excluding known Frappe boot warnings — list any deferred items in session-last)
- [ ] Filter row interactions: change Granularity → reloads chart/pivot; change Confidence MultiCheck → KPI/chart/pivot/detail update
- [ ] KPI cards: Closing balance, Net Cash, Inflow, Outflow display non-empty currency values
- [ ] Chart: 4-line chart (or fallback) renders without overlapping or null-interpolation artifacts
- [ ] Pivot click-to-filter: clicking a period column header highlights the column and updates the detail table to that period only
- [ ] Detail table: rows grouped by confidence with visible group totals; pagination buttons advance pages; search input filters server-side (verify by typing a known string)
- [ ] Take 2 screenshots: full page on first load AND after applying a confidence + period filter — save to `qa-screenshots/cash-flow-forecast-redesign-{1,2}.png` (in worktree root)

**Design QA** (`/design-qa` style — Playwright MCP exploratory pass):
- [ ] Exploratory review of the 4 sections (filter, KPI, chart, pivot, detail) as a first-time user — log structural UX proposals to `docs/design-qa-proposals/cash-flow-forecast-ui-redesign.md` with `## Session YYYY-MM-DD HH:MM` header (append, do not overwrite)
- [ ] Cosmetic fixes (spacing, alignment, label wording, empty-state copy, color consistency) implemented and committed atomically — flow/field/workflow changes are NOT implemented, only logged

**Session hygiene:**
- [ ] All edits committed on `feat/cash-flow-forecast-ui-redesign` (no uncommitted changes at end of last session)
- [ ] If `apps/vn_accounting` was switched to feature branch for live testing, switch back to `main` at the end (it had local uncommitted changes — `vn_accounting/workspace_sidebar/vn_accounting.json` — preserve them)
- [ ] Session-last file `.multi-session/session-last-cash-flow-forecast-ui-redesign.md` updated each session with: what was done, learnings, focused "Next Session Task", remaining acceptance criteria
- [ ] If ALL criteria above are checked AND the page passes live QA, write `ALL_TASKS_COMPLETE` to session-last; otherwise leave it for next session

## Constraints

- **Never switch `apps/vn_accounting` to a feature branch while it has uncommitted local changes you didn't make.** At session 1 start, `apps/vn_accounting` was on `main` with `M vn_accounting/workspace_sidebar/vn_accounting.json` from a parallel session. Verify the same state before switching for live test, and switch back to `main` after.
- **Do not modify backend helpers from Tasks 1-2** (`_filter_entries`, `_compute_group_totals`, `_load_entries_with_cache`, `get_forecast_entries`) unless a live-QA finding forces a change — if so, document the change in session-last with reasoning.
- **Do not introduce new pip or npm dependencies.** All work uses Frappe-native APIs (`page.add_field`, `frappe.Chart`, `frappe.xcall`, `frappe.ui.form.MultiCheck`).
- **Do not change the cache key format** (`forecast:{company}:{from_date}:{to_date}`) — both `get_forecast_data` and `get_forecast_entries` rely on it; changing breaks the 5-minute cache reuse.
- **Do not delete `get_drilldown_entries` until Task 8** — Tasks 3-7 still need the existing endpoint as a safety net during incremental migration; Task 8 removes it once the new pipeline works.
- **JS file size hard limit 800 lines.** Plan estimates ~600 final lines. If approaching 700, extract render helpers into a separate `cash_flow_forecast.helpers.js` and import via `app_include_js`.
- **Vietnamese diacritics required** in any user-visible string (KPI labels, empty states, tooltips). Use `__()` and put English-source + Vietnamese-target rows in `translations/vi.csv` (Task 9).
- **Do NOT push the branch to `dcnet-cloud` remote.** This branch ships via `goldrag1/vn_accounting`. Pushing to `dcnet-cloud` requires a feature-branch + PR per the project memory (`feedback_dcnet_always_pr`).

## Verification Commands

```bash
# Working directory throughout: worktree root
cd /home/long/long/frappe-bench-dcnet/.worktrees/vn_accounting-cash-flow-ui

# Unit tests (no bench needed — uses bench's Python venv via absolute path)
PYTHONPATH=.:/home/long/long/frappe-bench-dcnet/apps/frappe \
  /home/long/long/frappe-bench-dcnet/env/bin/python -m unittest vn_accounting.api.test_forecast_entries -v

# Static checks
node --check vn_accounting/vn_accounting/page/cash_flow_forecast/cash_flow_forecast.js
/home/long/long/frappe-bench-dcnet/env/bin/python -m py_compile vn_accounting/api/forecast.py

# CSV format check (Task 9)
/home/long/long/frappe-bench-dcnet/env/bin/python -c "
import csv
with open('vn_accounting/translations/vi.csv') as f:
    rows = list(csv.reader(f))
print(f'rows={len(rows)}')
assert all(len(r) >= 2 for r in rows if r), 'Some rows have <2 columns'
print('OK')
"

# Live build + page load (requires switching apps/vn_accounting branch — coordinate first)
# 1. Verify apps/vn_accounting state:
cd /home/long/long/frappe-bench-dcnet/apps/vn_accounting && git status -s && git branch --show-current
# 2. If clean enough to switch (only known local edits), checkout feature branch:
git stash push -m "session-X stash before live QA" && git checkout feat/cash-flow-forecast-ui-redesign
cd /home/long/long/frappe-bench-dcnet && bench build --app vn_accounting && bench --site dcnet.localhost clear-cache
# 3. After QA, switch back:
cd /home/long/long/frappe-bench-dcnet/apps/vn_accounting && git checkout main && git stash pop
```

## Agent Persona

You are a senior Frappe v16 developer continuing a multi-session task. Your prior session committed the backend (Tasks 1-2). The plan file at `apps/vn_accounting/docs/plans/2026-04-28-cash-flow-forecast-ui-redesign.md` has exact code blocks for every step — copy them verbatim unless the plan documents a fallback. Use `frappe.xcall` for whitelisted API calls (returns Promise resolving to the dict directly). Use `page.add_field({fieldtype, label, fieldname, change: () => {}})` for filter controls. Use `frappe.Chart` (already loaded on desk) for the line chart. Use `frappe.format(value, {fieldtype: "Currency"})` for money. Read `~/.claude/rules/frappe-v16-ui.md` and `~/.claude/rules/frappe.md` if you forget any framework gotcha (especially the `app_include_js` cache-busting rule for `.bundle.js`).

For live QA, use the Playwright MCP tools (`mcp__plugin_playwright_playwright__browser_*`). The site `dcnet.localhost:8001` requires a logged-in session — Playwright MCP gets a fresh session each launch, so navigate to `/login`, type Administrator credentials, then navigate to `/app/cash-flow-forecast`. If the page does not exist (404), confirm `apps/vn_accounting` is on the feature branch and that `bench build --app vn_accounting` was re-run.

## Model

auto

## Time Budget

- Max hours: 3
- Max sessions: 8
- Session minutes: 15 (per-session cap)

The agent decides how to split work across sessions. Plan tasks 3-7 (JS rewrites) are the biggest; tasks 8+9 are small; task 10 is QA + verification.
