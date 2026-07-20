## Session 2026-04-28 10:10

Exploratory design QA of the redesigned Cash Flow Forecast page (`/app/cash-flow-forecast`).
Tested with Playwright MCP on `dcnet.localhost:8001`. Console: 0 errors, 5 warnings (Frappe boot SVG preloads — not our code).

### Cosmetic fixes implemented (committed d518616)

- **"At" translation missing** — KPI Closing Balance sub-label showed "At T4/2027" instead of "Tại T4/2027". Added `At,Tại` row to `translations/vi.csv`.

### Structural UX proposals (logged only — do NOT implement without user approval)

1. **Filter row has no labels.** The 5 dropdowns render without visible labels: "Theo tháng | 12 | 0 | DCNET | Tất cả". Users cannot tell what "12" and "0" mean. The `page.add_field()` API sets the placeholder text inside the field, but the fields sit in a bare flex row with no above-row labels. Proposal: add a `<label>` row or use `title` attributes as tooltips, or restructure the filter row as a Frappe form card with field labels visible.

2. **Chart y-axis scaling squashes Inflow/Outflow lines.** Balance lines peak at 1-3 tỷ while Inflow/Outflow are ~600 tr–1 tỷ range. Since all 4 share one y-axis, the balance scale dominates and the Inflow/Outflow lines appear near-flat visually. Options: (a) separate y-axes (frappe-charts doesn't support dual-axis), (b) normalize to same tỷ scale, (c) split chart into two sections (Balance above, Inflow/Outflow below).

3. **Pivot table has no horizontal scroll indicator.** The table extends beyond the viewport (13+ periods). There is a scrollbar at the bottom, but no visual fade or "→" hint to signal more columns exist. First-time users see T4/2026 → T3/2027 cut off, may think the data ends there.

4. **Pivot column highlight persists across filter changes.** After clicking T7/2026, navigating to another Granularity and back does not clear the highlight. The detail table also shows stale "2026-07" filter chip until user clicks the × on the chip. Minor UX friction but can confuse.

5. **Empty-state "no data" copy missing.** If the company has no forecast entries, the KPI cards show VND 0 and the detail table is blank with no message. Should show "Chưa có dữ liệu dự báo — thêm giao dịch trong SO/PO/Phiếu lương để bắt đầu" or similar.

6. **Search placeholder in detail table is generic.** Shows "Tìm kiếm giao dịch..." — acceptable, but could hint at searchable fields: "Tìm theo mô tả, đối tác...".

### Screenshots

- `qa-screenshots/cash-flow-design-qa-1.png` — full page first load
- `qa-screenshots/cash-flow-design-qa-2.png` — after clicking T7/2026 pivot header (filter chip visible, detail shows 11 transactions)

---

## Session 2026-04-28 15:58

Second exploratory pass after deploying the feature branch to `apps/vn_accounting` (detached at `3b23034`) and live-loading on `dcnet.localhost:8001`. 1920×1800 viewport, fresh Playwright session. Console: 0 errors, 5 warnings (all are unrelated Frappe core preload warnings for `pos-icons.svg` / `lucide/icons.svg` etc. — not our code).

### Spec deviations found (LOG only — needs user decision before fix)

These are deviations from the design spec / plan that were committed during the multi-session run. None of them break the page; they preserve the prior behavior instead of implementing the spec.

1. **Pivot table is still vertical (metrics × periods), spec said horizontal (sources × periods).** Plan §6 / spec called for rows = source DocType (Sales Order, Purchase Order, Salary Slip, …) and columns = period (T1/2026 … T12/2026), so users can spot which revenue/expense stream drives a given month. The committed pivot keeps the legacy structure: rows = `Mở đầu / Dòng Tiền Vào / Dòng Tiền Ra / Kết thúc`, columns = period. Cell click-to-filter is wired up against period only — there is no source axis. To meet the spec, `render_pivot_table()` needs to aggregate `cells[period][source]` then transpose so source becomes the row dimension; KPI/chart can keep using the existing `cells` structure.

2. **Chart datasets are 4 metric series, spec said 4 confidence stacks.** Plan §5 / spec called for one line per confidence (`overdue`, `committed`, `probable`, `possible`) so users can see how confidence bands stack toward the closing balance. The committed chart keeps the legacy 4 lines: `Số dư thực tế / Số dư dự báo / Dòng tiền vào / Dòng tiền ra` — same as the pre-redesign chart, just plotted on the new layout. Confidence is collapsed into "anything not overdue" before plotting. To meet the spec, `render_chart()` needs to emit one dataset per confidence band with cumulative balance per period; null gaps fall back to single-balance per plan §5.3.

3. **Confidence filter is a single-Select, not MultiCheck.** Plan §3 documented this as an acceptable fallback when MultiCheck overflows the page-form row, and the implementation took the fallback. Real-world impact: user cannot view "Committed + Probable" simultaneously — must pick one bucket or "Tất cả". Worth checking whether the current 5-filter row width actually requires the fallback (1920×1800 viewport had room) before deciding to switch back to MultiCheck.

4. **Source filter is missing entirely.** Plan §3 documented this fallback ("Source MultiCheck removed (not supported in page.add_field) — all sources active"). User cannot scope the page to "Sales Orders only" or "Payroll only". Pivot only filters by period click, not by source. If pivot becomes horizontal (finding #1), per-row click could substitute for a source filter and this gap closes.

### Additional UX observations (LOG only)

5. **Filter row labels are missing — `page.add_field` renders Select fields without a `.control-label` element.** DOM check confirms: `document.querySelectorAll('.page-form .frappe-control')` finds 5 fields but none have a `.control-label` child (`labelStyle: "no-label-el"`). User sees raw values "Theo tháng | 12 | 0 | DCNET | Tất cả" with no hint of meaning. The Link field for Company is the only one whose combobox accessible name reflects "Công ty"; the 4 Selects show only the option text. This is a Frappe-native limitation of `page.add_field` in toolbar context, not a regression from this work — but the spec assumed visible labels. Options: (a) custom DOM injection to add `<label>` siblings, (b) keep as-is and rely on tooltips via `description` field option, (c) revert to a custom HTML filter row that explicitly labels each field.

6. **KPI Closing card has duplicated "Tại T4/2027" prefix in two places.** The card label reads `Tại T4/2027 · Đầu kỳ: 1.8 tỷ` — the "Tại T4/2027" is redundant if the period is already implied by the page-level "Forecast Periods = 12" filter. Considered cosmetic but borderline.

### Cosmetic fixes implemented this session

(None — all findings this round are structural and require user decision.)

### Screenshots

- `qa-screenshots/cash-flow-forecast-redesign-1-initial.png` — first load at 1920×941, viewport-clipped
- `qa-screenshots/cash-flow-forecast-redesign-2-fullpage.png` — full page at 1920×1800, all 4 sections visible (filter row, KPI cards, chart, pivot, detail table grouped by Confidence)

---

## Session 2026-04-28 22:57 — Corporate Finance Expert Review

Pass through the page as a **CFO / FP&A analyst** would use it for cash management, debt covenant compliance, working-capital decisions, and board reporting. Page renders cleanly post-fixes (commits `e3916c6` … `acdd2a4`) — this review is about **what financial decisions the page does and does not enable**, not about pixels.

### What works well (keep)

- **4 KPI hierarchy is correct.** Closing Balance is the headline number a CFO checks first; Net Cash Flow signals burn; gross Inflow vs Outflow exposes the magnitude of activity. The icon affordances (▲/▼/💼) are restrained.
- **Confidence laddering (Quá hạn / Đã cam kết / Có thể / Dự kiến)** matches the standard 4-bucket forecast taxonomy used by treasury tools (Float, Pulse). Multi-select with default-all means the user can isolate "what's signed" vs "what's still hopeful" in one click.
- **Source filter grouped Thu/Chi** mirrors the inflow/outflow mental model and stops the user mixing AR-driving sources with AP-driving ones in one filter.
- **Pivot warning rows** (yellow highlight) flag months where closing dips below the configured threshold — exactly the trigger event a treasury team needs.
- **Methodology menu item** gives audit transparency about how each forecast line is built (which provider, which assumptions). For board-pack screenshots this is non-negotiable.

### Critical gaps for a finance expert (LOG — needs decision)

1. **No probability-weighted forecast value.** The 4 confidence buckets are filterable but not weighted. A CFO wants to see one "expected" line that applies, e.g., 100/80/50/20 % weights to overdue/committed/probable/possible. The current page only allows toggling buckets — toggling has the same effect as a 0/100 weight, which is a coarse instrument. Industry standard: show a single weighted "Likely" closing balance alongside the 4-band closing.

2. **Cumulative Balance and per-period Inflow/Outflow share one Y-axis.** Closing balance peaks at ~3 tỷ; monthly inflow/outflow tops out around ~1 tỷ. They are in different units (stock vs flow) and putting them on one axis makes the inflow/outflow lines look near-flat. Either: (a) split into two stacked panels (balance above, inflow/outflow bar chart below), (b) plot inflow/outflow as bars and balance as line, or (c) dual axis (frappe-charts limitation — would need a different lib).

3. **Min-cash threshold rendered as a flat baseline only.** The chart shows `Mức tối thiểu (số dư)` as a line. A CFO needs the chart to **highlight months where closing balance breaches the threshold** — red shading, exclamation marker, or a "first breach in T9/2026" badge. The pivot table already highlights yellow/red rows; the chart should mirror that.

4. **No runway / days-of-cash KPI.** Closing Balance is a number; it doesn't tell the user "we have 18 months of cash at current burn". For early-stage / cash-burning companies (and any company headed into seasonality), runway is the headline metric. Computed as: `closing_balance / |avg_monthly_net_outflow|` when net is negative; ∞ when positive.

5. **No scenario / variance comparison.** All numbers are point estimates. A finance expert always wants:
   - Best/Base/Worst case toggle (drives different probability weightings)
   - Variance vs prior forecast (what changed since last week's run?) — currently there's no snapshot history
   - Variance vs budget (line items overspent vs plan) — depends on a budget DocType being present

6. **Missing AR-aging / DSO context inside the page.** Sales Invoice forecasts use `payment_delay` data from history but the page doesn't show **how long** receivables typically take or **which customers are dragging the forecast**. A click on "Hợp đồng" or "Hóa Đơn Bán" should optionally drill into "by counterparty" so the CFO can call the right customer.

7. **Net Cash Flow KPI should also break down by direction.** Currently shows `Inflow − Outflow`. In a net-negative environment, the CFO wants to read it as "we burn 961 tr/year, of which 840 tr is OpEx and 120 tr is debt service". Without a category axis on the KPI, every month's red number looks the same.

8. **Operating vs Investing vs Financing classification is absent.** VAS (and IFRS) cash flow statement separates these three. The page lumps everything under one "Outflow" bucket. For lender/board reporting the page can't be used directly — user must export to Excel and reclassify.

9. **No alerting or saved views.** Every visit re-applies the default filter. A CFO with a covenant of "min 500 tr cash on hand" wants to subscribe to a daily email / push when the forecast breaches that line. Saved views ("My weekly check") would let other roles return to a curated state without re-filtering.

10. **Detail table doesn't sort by impact within group.** Within "Quá hạn" the rows show `+1.1 tỷ / -2.1 tỷ (156 giao dịch)`. The table is then ordered by `expected_date` — which means a 50 tr Sales Invoice is shown above a 500 tr one if it's older. A CFO needs the largest line first inside each group — that's where attention should go.

11. **No counterparty concentration view.** "If our top 3 customers all delay by 30 days, what happens?" The current page can't answer this without exporting. Options: a "Top 10 expected receivables" panel; a heatmap of counterparty × month.

12. **Currency abbreviation `tỷ` / `tr` is ambiguous in formal context.** Internal users understand it. Board/auditor reports need full numbers (1,800,000,000 VND) or thousands of VND. A "Format" toggle (compact / full / thousands) would let the same page serve both audiences.

### Cosmetic / data-quality issues observed

- "Đã cam kết" appears as the visible label for Committed even though `vi.csv` says "Cam Kết" — a Frappe core translation override is winning. Acceptable but inconsistent with project's vi.csv. Lower priority.
- Pivot table column "T3/2..." truncates the year on the right edge — horizontal overflow indicator missing (already logged in session 1 finding #3).
- Detail table groups don't show a percentage of total alongside the absolute amounts (e.g., "Quá hạn — 1.1 tỷ thu / 2.1 tỷ chi (35% tổng dòng tiền)"). Useful for prioritization.

### Recommended priority for next iteration

If the team can ship 3 things in the next sprint, the highest-value financial improvements are:

1. **Probability-weighted single line** in the chart + KPI (item #1) — single biggest credibility win for non-technical finance users.
2. **Threshold breach highlight on chart** (item #3) — the chart already has the threshold line, just visualize when it's crossed.
3. **Sort detail rows by amount inside each confidence bucket** (item #10) — one-line code change, high cognitive payoff.

Items #4 (runway), #5 (variance), #8 (operating/investing/financing) are all "v2 enhancements" — they each require a data model expansion (snapshot history, account categorization).
