# Task: VN Accounting Dashboard v2 — Hybrid Frappe Page

## Context

The VN Accounting app currently uses a Frappe Workspace for its "Tổng quan" (Overview) dashboard. Workspace widgets have a low ceiling — no interactive date filters, no delta % comparison, no control over chart layout or KPI card styling. The goal is to replace the dashboard area with a custom Frappe Page that renders CRM-quality KPI cards and charts using `frappe.Chart` (already loaded on desk), while keeping the existing 60+ sidebar items unchanged.

Design spec: `docs/superpowers/specs/2026-04-14-vn-accounting-dashboard-v2-design.md`

## Scope

- Project: `/home/long/long/frappe-bench-dcnet` (bench root, app at `apps/vn_accounting`)
- Branch: create new `feat/dashboard-v2` on the vn_accounting repo (`apps/vn_accounting`)
- Related files:

| File | Status | Description |
|------|--------|-------------|
| `apps/vn_accounting/vn_accounting/vn_accounting/page/vn_accounting_dashboard/vn_accounting_dashboard.json` | NEW | Page DocType fixture |
| `apps/vn_accounting/vn_accounting/vn_accounting/page/vn_accounting_dashboard/vn_accounting_dashboard.js` | NEW | Main JS — filters, KPI cards, chart rendering (~200 lines) |
| `apps/vn_accounting/vn_accounting/vn_accounting/page/vn_accounting_dashboard/vn_accounting_dashboard.css` | NEW | CSS Grid layout, KPI card styling, responsive (~100 lines) |
| `apps/vn_accounting/vn_accounting/vn_accounting/page/vn_accounting_dashboard/vn_accounting_dashboard.html` | NEW | Empty or minimal template |
| `apps/vn_accounting/vn_accounting/api/dashboard.py` | NEW | Python API — main endpoint + KPI functions (~150 lines) |
| `apps/vn_accounting/vn_accounting/api/dashboard_charts.py` | NEW | Chart data functions — 8 charts (~150 lines) |
| `apps/vn_accounting/vn_accounting/api/__init__.py` | NEW | Empty init for api module |
| `apps/vn_accounting/vn_accounting/workspace_sidebar/vn_accounting.json` | MODIFY | Change "Tổng quan" item: link_type Workspace → Page |
| `apps/vn_accounting/vn_accounting/install.py` | MODIFY | Add `_sync_workspace_sidebar()` update for new link_type |
| `apps/vn_accounting/vn_accounting/hooks.py` | NO CHANGE | Frappe auto-discovers Pages from JSON fixtures |
| `apps/vn_accounting/vn_accounting/vn_accounting/number_card_methods.py` | NO CHANGE | Keep for backward compat |
| `apps/vn_accounting/vn_accounting/vn_accounting/report_utils.py` | NO CHANGE | Import constants from here |

## Requirements

### R1: Python API — `api/dashboard.py`

Create `apps/vn_accounting/vn_accounting/api/dashboard.py` with a single `@frappe.whitelist()` endpoint:

```python
@frappe.whitelist()
def get_dashboard(from_date=None, to_date=None, company=None):
```

Returns a dict with two keys: `kpis` (list of 5 items) and `charts` (dict of 8 items).

**KPI items** — each returns:
```python
{"title": str, "value": float, "delta": float|None, "color": str}
```

| KPI | GL Query | Delta Logic | Color |
|-----|----------|-------------|-------|
| Tổng Doanh Thu | `SUM(credit-debit)` WHERE account LIKE `511%`, posting_date in range | (current - previous) / abs(previous) × 100 | `#2e7d32` |
| Tổng Chi Phí | `SUM(debit-credit)` WHERE account LIKE `621%..642%`, posting_date in range | same pattern | `#e65100` |
| Công Nợ Phải Thu | `SUM(debit-credit)` WHERE account LIKE `131%`, all time (balance) | (balance_now - balance_at_from_date) / abs(balance_at_from_date) × 100 | `#1565c0` |
| Công Nợ Phải Trả | `SUM(credit-debit)` WHERE account LIKE `331%`, all time (balance) | same pattern | `#c62828` |
| Tồn Quỹ | `SUM(debit-credit)` WHERE account LIKE `111%` OR `112%`, all time (balance) | same pattern | `#00695c` |

**Previous period** for flow KPIs: mirror the selected range backwards. E.g., if from_date=Apr 1, to_date=Apr 30, previous = Mar 1..Mar 31. Calculate via: `diff = date_diff(to_date, from_date); prev_from = add_days(from_date, -(diff+1)); prev_to = add_days(from_date, -1)`.

**Delta = None** when previous period value is 0 (avoid division by zero). Frontend renders "—" for null delta.

**Chart data** — return standard frappe-charts format. 8 chart panels in 4 rows × 2 columns (50/50 split, matching CRM dashboard layout):

| Chart key | Type | Position | Data structure |
|-----------|------|----------|----------------|
| `revenue_expense` | bar (stacked) | Row 1 Left | `{labels: ["T1"..."T12"], datasets: [{name: "Doanh thu", values: [...]}, {name: "Chi phí", values: [...]}, {name: "Lợi nhuận", values: [...]}]}` |
| `cash_timeline` | line | Row 1 Right | `{labels: [...monthly...], datasets: [{name: "Tồn quỹ", values: [...cumulative...]}]}` |
| `ar_by_customer` | donut | Row 2 Left | `{labels: [customer_names], datasets: [{values: [outstanding_amounts]}]}` — top 4 + "Khác" |
| `ap_by_supplier` | donut | Row 2 Right | `{labels: [supplier_names], datasets: [{values: [outstanding_amounts]}]}` — top 4 + "Khác" |
| `revenue_by_item_group` | donut | Row 3 Left | `{labels: [item_group_names], datasets: [{values: [revenue_amounts]}]}` — top 4 + "Khác". Query: `SELECT item_group, SUM(amount) FROM tabSales Invoice Item sii JOIN tabSales Invoice si ON sii.parent=si.name WHERE si.docstatus=1 AND si.posting_date BETWEEN ... GROUP BY item_group ORDER BY SUM(amount) DESC LIMIT 4` |
| `expense_by_type` | donut | Row 3 Right | `{labels: [expense_labels], datasets: [{values: [amounts]}]}`. Group GL expenses by account prefix: 641%→"Chi phí bán hàng", 642%→"Chi phí quản lý", 632%→"Giá vốn hàng bán", others→"Khác" |
| `top_customers_revenue` | bar | Row 4 Left | `{labels: [customer_names], datasets: [{name: "Doanh thu", values: [...]}]}`. Query: `SELECT customer, SUM(grand_total) FROM tabSales Invoice WHERE docstatus=1 AND posting_date BETWEEN ... GROUP BY customer ORDER BY SUM(grand_total) DESC LIMIT 5` |
| `ar_aging` | bar (stacked) | Row 4 Right | `{labels: ["0-30 ngày", "31-60 ngày", "61-90 ngày", ">90 ngày"], datasets: [{name: "Công nợ", values: [...]}]}`. Calculate from Sales Invoice: days_overdue = today - due_date, bucket by ranges. |

Import constants from `vn_accounting.vn_accounting.report_utils` (REVENUE_PREFIX, EXPENSE_PREFIXES, AR_PREFIX, AP_PREFIX, CASH_PREFIX, BANK_PREFIX).

Reuse the `_sum_gl()` and `_sum_gl_multi()` patterns from `dashboard_chart_source/revenue_expense_monthly/revenue_expense_monthly.py` and `number_card_methods.py`. Do NOT duplicate SQL query patterns — extract shared helpers if needed.

For donut charts (AR/AP): query submitted Sales Invoice / Purchase Invoice grouped by customer/supplier, `WHERE docstatus=1 AND outstanding_amount > 0`, `ORDER BY SUM(outstanding_amount) DESC LIMIT 4`. Group the rest as "Khác".

**API file size note:** With 8 charts + 5 KPIs, `api/dashboard.py` will exceed 200 lines. Split into `api/dashboard.py` (main endpoint + KPI functions, ~150 lines) and `api/dashboard_charts.py` (chart data functions, ~150 lines). Import chart functions into dashboard.py.

### R2: Frappe Page Files

Create directory: `apps/vn_accounting/vn_accounting/vn_accounting/page/vn_accounting_dashboard/`

**vn_accounting_dashboard.json:**
```json
{
    "content": null,
    "doctype": "Page",
    "module": "VN Accounting",
    "name": "vn-accounting-dashboard",
    "page_name": "vn-accounting-dashboard",
    "standard": "Yes",
    "system_page": 0,
    "title": "VN Accounting Dashboard",
    "roles": [{"role": "Accounts User"}, {"role": "Accounts Manager"}]
}
```

**vn_accounting_dashboard.js** (~200 lines):

Entry point pattern (follow `apps/vn_banking/vn_banking/vn_banking/page/bank_reconcile/bank_reconcile.js`):
```javascript
frappe.pages["vn-accounting-dashboard"].on_page_load = function (wrapper) {
    const page = frappe.ui.make_app_page({
        parent: wrapper,
        title: __("Tổng Quan Kế Toán"),
        single_column: true,
    });
    // ... setup filters, render dashboard
};
```

**Filter bar** — use `page.add_field()`:
1. **Kỳ kế toán** — `fieldtype: "Select"`, options: `Tháng này\nQuý này\nNăm nay\nTùy chọn`, default: "Tháng này"
2. **Custom date range** — `fieldtype: "DateRange"`, hidden by default, shown only when "Tùy chọn" selected
3. **Công ty** — `fieldtype: "Link"`, options: "Company", default: `frappe.defaults.get_user_default("Company")`. Hide if only 1 company.

Date preset logic using `frappe.datetime.month_start()`, `.month_end()`, `.quarter_start()`, `.quarter_end()`, `.year_start()`, `.year_end()` — all confirmed available in Frappe v16.

On any filter change → call `frappe.xcall("vn_accounting.api.dashboard.get_dashboard", {from_date, to_date, company})` → re-render KPIs and charts.

**KPI cards** — CRM-style thin cards focused on numbers. Render as HTML in `.vna-kpi-row`:
```html
<div class="vna-kpi-card">
    <div class="vna-kpi-title">{title}</div>
    <div class="vna-kpi-value">{formatted_value}</div>
    <div class="vna-kpi-delta {up|down|neutral}">{arrow} {delta}%</div>
</div>
```
**Design notes (match CRM screenshot):**
- NO colored top border — clean flat card like CRM
- Title: small, muted, uppercase
- Value: large bold number — the focal point
- Delta: small text below, green/red colored
- Card has minimal padding, subtle shadow — thin and clean

Format values with `format_currency(value, "VND", 0)` (no decimals). Delta arrow: ↑ for positive (green), ↓ for negative (red), — for null.

**Charts** — 8 panels in 4 rows × 2 equal columns (50/50 split like CRM). Each chart in a card with title + subtitle.

Render using `new frappe.Chart(container, config)`:

| Chart | Row | Side | frappe.Chart config |
|-------|-----|------|---------------------|
| Revenue/Expense | 1 | Left | `type: "bar"`, `barOptions: {stacked: true}`, colors: `["#2e7d32", "#e65100", "#1565c0"]`, height: 280 |
| Cash Timeline | 1 | Right | `type: "line"`, colors: `["#00695c"]`, height: 280 |
| AR by Customer | 2 | Left | `type: "donut"`, colors: `["#1565c0", "#42a5f5", "#90caf9", "#bbdefb", "#e0e0e0"]`, height: 280 |
| AP by Supplier | 2 | Right | `type: "donut"`, colors: `["#c62828", "#ef5350", "#ef9a9a", "#ffcdd2", "#e0e0e0"]`, height: 280 |
| Revenue by Item Group | 3 | Left | `type: "donut"`, colors: `["#7c4dff", "#b388ff", "#d1c4e9", "#ede7f6", "#e0e0e0"]`, height: 280 |
| Expense by Type | 3 | Right | `type: "donut"`, colors: `["#ff6f00", "#ffa726", "#ffcc80", "#fff3e0", "#e0e0e0"]`, height: 280 |
| Top 5 Customers | 4 | Left | `type: "bar"`, colors: `["#1565c0"]`, height: 280 |
| AR Aging | 4 | Right | `type: "bar"`, `barOptions: {stacked: false}`, colors: `["#4caf50", "#ff9800", "#f44336", "#b71c1c"]`, height: 280 |

**Each chart card has title + subtitle** (like CRM):
```html
<div class="vna-chart-card">
    <div class="vna-chart-title">Doanh Thu / Chi Phí</div>
    <div class="vna-chart-subtitle">Theo tháng trong kỳ chọn</div>
    <div id="vna-revenue-expense"></div>
</div>
```

Wire donut chart click → navigate to filtered list:
```javascript
chart.parent.addEventListener("data-select", (e) => {
    frappe.set_route("List", "Sales Invoice", {customer: e.detail.label, docstatus: 1});
});
```

Add tooltip formatting for bar/line charts: `tooltipOptions: {formatTooltipY: d => format_currency(d, "VND", 0)}`.

**Loading state**: Show `frappe.show_progress("Loading dashboard...", 30, 100)` or a spinner during API call. Clear on completion.

**vn_accounting_dashboard.css** (~100 lines):

```css
.vna-dashboard { padding: 20px; }
.vna-kpi-row { display: flex; gap: 16px; margin-bottom: 24px; }
.vna-kpi-card {
    flex: 1;
    background: var(--card-bg);
    border-radius: 8px;
    padding: 14px 16px;
    box-shadow: var(--card-shadow);
}
/* Thin KPI cards — CRM style: title small, number big, delta subtle */
.vna-kpi-title { font-size: 11px; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 4px; }
.vna-kpi-value { font-size: 24px; font-weight: 700; color: var(--text-color); margin-bottom: 2px; }
.vna-kpi-delta { font-size: 12px; font-weight: 500; }
.vna-kpi-delta.up { color: var(--green-600); }
.vna-kpi-delta.down { color: var(--red-600); }
.vna-kpi-delta.neutral { color: var(--text-muted); }
/* 50/50 grid — matches CRM dashboard equal-column layout */
.vna-chart-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
}
.vna-chart-card {
    background: var(--card-bg);
    border-radius: 8px;
    padding: 16px;
    box-shadow: var(--card-shadow);
}
```

CSS variables `--card-bg`, `--card-shadow`, `--green-600`, `--red-600`, `--text-muted`, `--text-color` are all confirmed available in Frappe v16 desk.

**vn_accounting_dashboard.html** — empty file (layout built in JS).

### R3: Workspace Sidebar Integration

In `workspace_sidebar/vn_accounting.json`, change the "Tổng quan" item (first item, idx ~1):

**Before:** `"link_type": "Workspace", "link_to": "VN Accounting"`
**After:** `"link_type": "Page", "link_to": "vn-accounting-dashboard"`

Keep icon as "home". Keep all other 60+ sidebar items unchanged.

### R4: Install Hook Update

In `install.py`, the `_sync_workspace_sidebar()` function already re-syncs sidebar items from the JSON fixture. After changing the JSON, running `bench migrate` will pick up the change. No extra code needed — just verify the JSON change is correct.

## Acceptance Criteria

- [ ] `bench --site dcnet.localhost migrate` completes without errors (Page synced from JSON)
- [ ] `bench build --app vn_accounting` completes without errors
- [ ] API endpoint works: `bench --site dcnet.localhost execute "frappe.call('vn_accounting.api.dashboard.get_dashboard')"` returns dict with `kpis` (5 items) and `charts` (8 keys)
- [ ] Each KPI item has keys: `title`, `value` (number), `delta` (number or None), `color` (hex string)
- [ ] Revenue/expense chart data has `labels` (list of month strings) and `datasets` (3 datasets: Doanh thu, Chi phí, Lợi nhuận)
- [ ] All 4 donut charts return `labels` (list of names, max 5 including "Khác") and `datasets` (1 dataset with values)
- [ ] `top_customers_revenue` returns labels (customer names) + datasets with revenue values
- [ ] `ar_aging` returns 4 age-bucket labels and corresponding outstanding amounts
- [ ] Page loads at `http://dcnet.localhost:8001/desk/vn-accounting-dashboard` without JS errors
- [ ] Filter bar visible: period selector (Select) + company dropdown (Link)
- [ ] Changing period filter (Tháng này / Quý này / Năm nay) reloads all KPIs and charts
- [ ] 5 KPI cards render in a horizontal row — thin CRM-style (no colored border, just number + delta)
- [ ] 8 charts render in 4 rows × 2 equal columns (50/50 grid like CRM dashboard), each with title + subtitle
- [ ] Sidebar item "Tổng quan" navigates to the new Page (not the old Workspace)
- [ ] QA with headed browser (`/connect-chrome` → navigate to `http://dcnet.localhost:8001/desk/vn-accounting-dashboard`): verify KPIs show data, charts render, filters work, sidebar "Tổng quan" link works, no console errors
- [ ] All changes committed with descriptive message on `feat/dashboard-v2` branch

## Constraints

- Do NOT modify `hooks.py` — Frappe auto-discovers Pages from JSON fixtures, no hook entry needed
- Do NOT delete or modify `number_card_methods.py` or `dashboard_chart_source/` — keep for backward compatibility
- Do NOT modify `sidebar_route_options.bundle.js` or `dashboard_charts.bundle.js`
- Do NOT add new npm/pip dependencies — use only `frappe.Chart` (already loaded on desk) and built-in Frappe controls
- Split API into `api/dashboard.py` (~150 lines, main endpoint + KPIs) and `api/dashboard_charts.py` (~150 lines, 8 chart data functions) — neither file over 200 lines
- Keep `vn_accounting_dashboard.js` under 400 lines — split into render helpers if needed. With 8 charts the JS will be larger than the original 4-chart estimate.
- Use parameterized SQL queries (%(param)s pattern) — never f-string interpolation in SQL
- Import account prefixes from `vn_accounting.vn_accounting.report_utils` — do not hardcode account numbers

## Verification Commands

bench --site dcnet.localhost migrate
bench build --app vn_accounting
bench --site dcnet.localhost execute "frappe.call('vn_accounting.api.dashboard.get_dashboard')"
curl -s -o /dev/null -w "HTTP %{http_code}" http://dcnet.localhost:8001/desk/vn-accounting-dashboard

## Agent Persona

You are a senior Frappe v16 developer building a custom dashboard page. Key patterns:

- **Frappe Page**: create files in `page/<name>/` with .json, .js, .css, .html. Entry: `frappe.pages["name"].on_page_load = function(wrapper) { ... }`. Use `frappe.ui.make_app_page()` for page scaffold.
- **Filters**: `page.add_field({fieldtype, options, fieldname, label, default})`. Access via `page.fields_dict.fieldname.get_value()`.
- **Charts**: `new frappe.Chart(container_element, {type, data, colors, height, ...})`. Destroy old chart before creating new: `if (chart) chart.destroy();`.
- **API calls**: `frappe.xcall("dotted.path.to.function", {args})` returns Promise.
- **Date helpers (JS)**: `frappe.datetime.month_start()`, `.month_end()`, `.quarter_start()`, `.quarter_end()`, `.year_start()`, `.year_end()`, `.get_today()`.
- **Currency formatting (JS)**: `format_currency(value, "VND", 0)` — available globally on desk.
- **After creating page files**: `bench --site dcnet.localhost migrate` to sync Page record into DB, then `bench build --app vn_accounting` is NOT needed for Page files (they're not bundled). However, if you modify any `.bundle.js` or `.bundle.css`, then bench build IS needed.
- **Working directory**: stay at bench root `/home/long/long/frappe-bench-dcnet`. Use absolute paths.
- **bench serve**: already running on port 8001. Do NOT restart it unless explicitly needed.
- **CSS variables**: use `var(--card-bg)`, `var(--card-shadow)`, `var(--green-600)`, `var(--red-600)`, `var(--text-muted)`, `var(--text-color)` — all available in Frappe v16 desk.

Reference implementation: Frappe CRM dashboard at `apps/crm/frontend/src/pages/Dashboard.vue` and `apps/crm/crm/api/dashboard.py` — study the data format and rendering pattern.

## Model

auto

## Time Budget

- Max hours: 3
- Max sessions: 7
