---
project: apps/vn_accounting
base_branch: main
---

# VN Accounting Dashboard v2 — Hybrid Frappe Page

## Summary

Replace the Frappe Workspace widget-based dashboard with a custom **Frappe Page** (`vn-accounting-dashboard`) that renders KPI cards with delta %, interactive charts via `frappe.Chart`, and filter bar with date range presets + company selector. Keeps existing workspace sidebar (60+ items) unchanged.

> **Why Frappe Page, not Vue SPA:** frappe-ui chart components (NumberChart, AxisChart, DonutChart) are thin wrappers around frappe-charts. `frappe.Chart` (v2.0.0-rc27) is already loaded on desk. Building a Vite SPA pipeline for one page is unjustified overhead. A Frappe Page with vanilla JS + `frappe.Chart` + CSS Grid achieves visual parity with CRM dashboard at zero new build dependencies.

> **Why not improve existing Workspace:** Workspace widgets have a fixed rendering pipeline — no control over delta %, no interactive date filters, no responsive grid layout, no chart interactivity beyond what Dashboard Chart provides. Ceiling is too low.

## Architecture

```
┌──────────────────────────────────────────────────┐
│ Frappe Desk Shell (navbar, sidebar, etc.)         │
│ ┌──────────┬─────────────────────────────────────┐│
│ │ Workspace│  Frappe Page: vn-accounting-dashboard││
│ │ Sidebar  │  ┌─────────────────────────────────┐ ││
│ │ (60+     │  │ Filter Bar: [Kỳ KT] [Công ty]  │ ││
│ │  items)  │  ├─────────────────────────────────┤ ││
│ │          │  │ KPI Row: 5 number cards w/ delta │ ││
│ │ Tổng quan│  ├──────────────────┬──────────────┤ ││
│ │ Quỹ TM   │  │ Revenue/Expense  │ AR by Cust   │ ││
│ │ Ngân hàng│  │ Bar Chart (2/3)  │ Donut (1/3)  │ ││
│ │ Mua hàng │  ├──────────────────┬──────────────┤ ││
│ │ Bán hàng │  │ Cash Timeline    │ AP by Supp   │ ││
│ │ ...      │  │ Line Chart (2/3) │ Donut (1/3)  │ ││
│ │          │  └──────────────────┴──────────────┘ ││
│ └──────────┴─────────────────────────────────────┘│
└──────────────────────────────────────────────────┘
```

## 1. Filter Bar

Two controls in `page.page_form` (Frappe Page built-in filter area):

### 1.1 Kỳ kế toán (Date Range)

**Approach:** Custom Select + DateRange hybrid.

Presets via `page.add_field({ fieldtype: "Select" })`:
- Tháng này (default)
- Quý này
- Năm nay
- Tùy chọn → shows a DateRange picker

When "Tùy chọn" selected, a second `DateRange` field appears. Otherwise hidden.

Preset logic (all in JS):
```javascript
function getPresetDates(preset) {
    const today = frappe.datetime.get_today();
    switch (preset) {
        case "Tháng này":
            return [frappe.datetime.month_start(), frappe.datetime.month_end()];
        case "Quý này":
            return [frappe.datetime.quarter_start(), frappe.datetime.quarter_end()];
        case "Năm nay":
            return [frappe.datetime.year_start(), frappe.datetime.year_end()];
    }
}
```

> **Why Select+DateRange, not DateRangePicker alone:** Accountants think in fiscal periods (tháng/quý/năm), not arbitrary date ranges. Presets match their mental model. Custom range is escape hatch.

### 1.2 Công ty (Company)

`page.add_field({ fieldtype: "Link", options: "Company" })`. Default: `frappe.defaults.get_user_default("Company")`.

Hidden if only 1 company exists (check via `frappe.boot.user.defaults.company` or API).

### 1.3 Filter Change → Reload

On any filter change: call `get_dashboard()` API → re-render all KPIs + charts. Show loading spinner on the page body during fetch.

## 2. KPI Cards (Row 1)

5 cards in a horizontal flex row, each card is a styled `<div>`:

```
┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ Tổng Doanh Thu│ │ Tổng Chi Phí │ │  CN Phải Thu │ │  CN Phải Trả │ │   Tồn Quỹ    │
│ 1,234,567,890│ │  987,654,321 │ │  456,789,012 │ │  321,654,987 │ │  567,890,123 │
│  ▲ +12.5%    │ │  ▼ -3.2%     │ │  ▲ +8.1%     │ │  ▼ -5.4%     │ │  ▲ +2.7%     │
└──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘
```

Card HTML structure:
```html
<div class="vna-kpi-card" style="border-top: 3px solid {color}">
    <div class="vna-kpi-title">{title}</div>
    <div class="vna-kpi-value">{formatted_value}</div>
    <div class="vna-kpi-delta {up|down}">
        {arrow} {delta}%
    </div>
</div>
```

**Value formatting:** `format_currency(value, "VND", 0)` — no decimals for VND.

**Delta calculation (server-side):** Compare current period vs previous period of same length.
- If filter = "Tháng này" → delta = (this month - last month) / last month × 100
- If filter = "Quý này" → delta = (this quarter - last quarter) / last quarter × 100
- If filter = "Năm nay" → delta = (this year - last year) / last year × 100
- If filter = custom range → delta = (this range - previous range of same length) / previous × 100
- If previous period = 0 → delta = null (display "—" instead of infinity)

**Delta for balance KPIs** (AR, AP, Cash): delta = (balance now - balance at start of period) / balance at start × 100.

> **Why delta % matters:** Transforms static numbers into trend signals. An accountant seeing "Công nợ phải thu: 456M" doesn't know if that's concerning. "Công nợ phải thu: 456M ▲+8.1%" immediately signals growth that may need attention.

## 3. Charts (Row 2-3)

CSS Grid: 2 rows × 2 columns, left column 2fr, right column 1fr.

### 3.1 Revenue / Expense / Profit — Stacked Bar

- **Type:** `bar`, stacked
- **Data:** Monthly breakdown within the selected date range
- **Datasets:** Doanh thu (green), Chi phí (orange), Lợi nhuận (blue)
- **Labels:** T1, T2, ... T12 (month numbers)
- **Source:** Reuses `_sum_gl()` / `_sum_gl_multi()` logic from existing `revenue_expense_monthly.py`

frappe.Chart config:
```javascript
new frappe.Chart(container, {
    type: "bar",
    data: { labels, datasets },
    colors: ["#2e7d32", "#e65100", "#1565c0"],
    barOptions: { stacked: true },
    tooltipOptions: { formatTooltipY: d => format_currency(d, "VND", 0) },
    height: 280
});
```

### 3.2 AR by Customer — Donut

- **Type:** `donut`
- **Data:** Top 4 customers by outstanding_amount from submitted Sales Invoices
- **Source:** `frappe.db.sql` grouping `tabSales Invoice` by customer, `WHERE docstatus=1 AND outstanding_amount > 0`

### 3.3 Cash Balance Timeline — Line

- **Type:** `line`
- **Data:** Monthly cumulative balance of TK 111 + TK 112
- **Source:** Reuses logic from existing `cash_balance_timeline.py`

### 3.4 AP by Supplier — Donut

- **Type:** `donut`
- **Data:** Top 4 suppliers by outstanding_amount from submitted Purchase Invoices
- **Source:** `frappe.db.sql` grouping `tabPurchase Invoice` by supplier, `WHERE docstatus=1 AND outstanding_amount > 0`

### Chart Interactivity

`frappe.Chart` v2 supports:
- Hover tooltips (built-in)
- Click on data point → can wire to navigation (e.g., click customer in donut → open Customer list filtered)
- `isNavigable: true` enables this

We wire donut chart clicks to open filtered list views:
```javascript
chart.parent.addEventListener("data-select", (e) => {
    const label = e.detail.label; // customer/supplier name
    frappe.set_route("List", "Sales Invoice", { customer: label, docstatus: 1 });
});
```

> **Why clickable charts:** Transforms dashboard from display-only to navigation hub. Accountant sees a large AR slice → clicks → lands on the filtered invoice list. Zero extra clicks vs current flow (see chart → manually navigate → set filters).

## 4. Python API

### File: `vn_accounting/api/dashboard.py`

Single endpoint, single round-trip:

```python
@frappe.whitelist()
def get_dashboard(from_date=None, to_date=None, company=None):
    """Returns all dashboard data in one call."""
    company = company or frappe.defaults.get_user_default("Company")
    if not from_date or not to_date:
        from_date = frappe.utils.get_first_day(frappe.utils.nowdate())
        to_date = frappe.utils.get_last_day(frappe.utils.nowdate())

    # Calculate previous period for delta
    diff = frappe.utils.date_diff(to_date, from_date)
    prev_from = frappe.utils.add_days(from_date, -(diff + 1))
    prev_to = frappe.utils.add_days(from_date, -1)

    return {
        "kpis": [
            _get_revenue_kpi(from_date, to_date, prev_from, prev_to, company),
            _get_expense_kpi(from_date, to_date, prev_from, prev_to, company),
            _get_ar_kpi(from_date, to_date, company),
            _get_ap_kpi(from_date, to_date, company),
            _get_cash_kpi(from_date, to_date, company),
        ],
        "charts": {
            "revenue_expense": _get_revenue_expense_chart(from_date, to_date, company),
            "cash_timeline": _get_cash_timeline_chart(from_date, to_date, company),
            "ar_by_customer": _get_ar_by_customer(company),
            "ap_by_supplier": _get_ap_by_supplier(company),
        },
    }
```

**KPI return format (per item):**
```python
{
    "title": "Tổng Doanh Thu",
    "value": 1234567890,
    "delta": 12.5,         # percentage, null if prev=0
    "color": "#2e7d32",
}
```

**Chart return format:** Standard frappe-charts `{ labels: [...], datasets: [...] }`.

### Delta Calculation Pattern

For flow KPIs (Revenue, Expenses):
```python
def _calc_delta(current, previous):
    if not previous:
        return None
    return round((current - previous) / abs(previous) * 100, 1)
```

For balance KPIs (AR, AP, Cash): compare balance at `to_date` vs balance at `from_date - 1 day` (opening balance).

### Reuse from Existing Code

`report_utils.py` constants (REVENUE_PREFIX, EXPENSE_PREFIXES, etc.) and GL query patterns from `number_card_methods.py` are reused. The new `api/dashboard.py` imports these directly.

The existing `number_card_methods.py` and `dashboard_chart_source/` files remain for backward compatibility (workspace may still reference them). No breaking changes.

## 5. Frontend Files

### 5.1 Page Definition

**`page/vn_accounting_dashboard/vn_accounting_dashboard.json`:**
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

### 5.2 Main JS

**`page/vn_accounting_dashboard/vn_accounting_dashboard.js`** (~200 lines)

Structure:
```javascript
frappe.pages["vn-accounting-dashboard"].on_page_load = function (wrapper) {
    const page = frappe.ui.make_app_page({
        parent: wrapper,
        title: __("Tổng Quan Kế Toán"),
        single_column: true,
    });

    // Add filters
    const period_field = page.add_field({ /* Select: presets */ });
    const date_range_field = page.add_field({ /* DateRange: hidden by default */ });
    const company_field = page.add_field({ /* Link: Company */ });

    // Dashboard container
    page.main.html(`
        <div class="vna-dashboard">
            <div class="vna-kpi-row"></div>
            <div class="vna-chart-grid">
                <div class="vna-chart-main" id="vna-revenue-expense"></div>
                <div class="vna-chart-side" id="vna-ar-donut"></div>
                <div class="vna-chart-main" id="vna-cash-timeline"></div>
                <div class="vna-chart-side" id="vna-ap-donut"></div>
            </div>
        </div>
    `);

    // Load and render
    loadDashboard(page);
};

function loadDashboard(page) {
    const [from_date, to_date] = getDatesFromFilter(page);
    const company = page.fields_dict.company.get_value();

    frappe.xcall("vn_accounting.api.dashboard.get_dashboard", {
        from_date, to_date, company
    }).then(data => {
        renderKPIs(page, data.kpis);
        renderCharts(page, data.charts);
    });
}
```

### 5.3 CSS

**`page/vn_accounting_dashboard/vn_accounting_dashboard.css`** (~100 lines)

Key layout rules:
```css
.vna-dashboard { padding: 20px; }

.vna-kpi-row {
    display: flex;
    gap: 16px;
    margin-bottom: 24px;
}

.vna-kpi-card {
    flex: 1;
    background: var(--fg-color);
    border-radius: 8px;
    padding: 16px;
    box-shadow: var(--card-shadow);
}

.vna-chart-grid {
    display: grid;
    grid-template-columns: 2fr 1fr;
    gap: 16px;
}

.vna-kpi-delta.up { color: var(--green-600); }
.vna-kpi-delta.down { color: var(--red-600); }
```

### 5.4 HTML Template (optional)

**`page/vn_accounting_dashboard/vn_accounting_dashboard.html`** — can be empty (layout built in JS) or contain the static skeleton.

## 6. Sidebar Integration

### Change to Workspace Sidebar

In `workspace_sidebar/vn_accounting.json`, the "Tổng quan" item changes:

**Before:**
```json
{ "label": "Tổng quan", "link_type": "Workspace", "link_to": "VN Accounting", "icon": "home" }
```

**After:**
```json
{ "label": "Tổng quan", "link_type": "Page", "link_to": "vn-accounting-dashboard", "icon": "home" }
```

> **Why Page link_type:** Page type opens in the same tab within the desk SPA, keeps sidebar visible, and supports active highlight. Verified in vn_banking's bank-reconcile page which uses the same pattern.

### Permission Note

Page roles include `Accounts User` and `Accounts Manager`. The sidebar item uses `link_type: "Page"` which checks `allowed_pages` — admin users always pass. For non-admin users with Accounts User role, the page role permission grants access.

## 7. Migration / Install Hook

In `install.py`, add to `after_migrate()`:
- Ensure Page record exists in DB (Frappe auto-syncs from JSON on migrate, so no extra code needed for the Page itself)
- Update `_sync_workspace_sidebar()` to pick up the new "Tổng quan" link_type change

No data migration needed — this is additive.

## 8. What Changes vs What Stays

| Component | Status | Notes |
|-----------|--------|-------|
| `page/vn_accounting_dashboard/` | **NEW** | 4 files: .json, .js, .css, .html |
| `api/dashboard.py` | **NEW** | Single endpoint, reuses report_utils |
| `workspace_sidebar/vn_accounting.json` | **MODIFIED** | "Tổng quan" link_type → Page |
| `hooks.py` | **NO CHANGE** | Page auto-discovered by Frappe |
| `number_card_methods.py` | **NO CHANGE** | Kept for backward compat |
| `dashboard_chart_source/` | **NO CHANGE** | Kept for backward compat |
| `dashboard_charts.bundle.js` | **NO CHANGE** | Still handles workspace charts if user visits workspace directly |
| `sidebar_route_options.bundle.js` | **NO CHANGE** | Sidebar behavior unchanged |
| `workspace/vn_accounting.json` | **NO CHANGE** | Workspace still exists for shortcuts |

## 9. Edge Cases

### Khi nào khác?

- **No GL Entries yet (new company):** All KPIs return 0, delta = null (display "—"). Charts render empty with "Chưa có dữ liệu" message.
- **Single company:** Company filter hidden. Default company used automatically.
- **No Fiscal Year defined:** Falls back to calendar year (existing logic in `_get_fiscal_year_dates()`).
- **Custom date range spanning fiscal years:** Works correctly — GL queries use `BETWEEN from_date AND to_date`, no fiscal year constraint.
- **Large GL Entry volume:** Queries are simple aggregates with `LIKE` on indexed `account` column + `company` filter. Performance should be acceptable for <1M GL entries. For larger volumes, consider caching (future optimization, not in v1).
- **Page permission for non-admin:** Page roles (Accounts User, Accounts Manager) control access. Users without these roles won't see the page or the sidebar item (Frappe's `is_item_allowed()` checks page permissions).
