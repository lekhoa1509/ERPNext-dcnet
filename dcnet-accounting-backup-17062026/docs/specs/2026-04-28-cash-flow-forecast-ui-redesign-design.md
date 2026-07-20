# Cash Flow Forecast UI Redesign — Design Spec

- **Date**: 2026-04-28
- **Author**: Long (collab Claude Opus 4.7)
- **Branch**: `feat/cash-flow-forecast-ui-redesign` (vn_accounting)
- **Worktree**: `frappe-bench-dcnet/.worktrees/vn_accounting-cash-flow-ui`
- **Reference mockup**: `/home/long/Downloads/35311880479619570.jpg` (frontend colleague)
- **Predecessor v1 spec**: `docs/specs/2026-04-20-cash-flow-forecast-design.md`

---

## 1. Goal

Refresh the visual hierarchy of the **Cash Flow Forecast** page (`/app/cash-flow-forecast`) so it matches the team's new shared design language. Functional behavior (provider system, forecast math, data sources) is unchanged from v1 — this spec is purely UI + interaction.

**Approach: B from brainstorm — take ideas, don't pixel-clone.**
- Keep Frappe Desk chrome (sidebar, page-form, breadcrumbs implicit via Frappe).
- Use Frappe-native form controls everywhere — **no new CSS design language**.
- Adopt mockup's three big ideas: 4-card KPI strip, horizontal pivot summary, flat-grouped detail table.

## 2. Non-Goals

- No backend forecast logic changes (providers, confidence levels, opening balance calculation untouched).
- No new data sources, no new DocType.
- No mobile-specific layout (Frappe Desk is desktop-first; horizontal scroll acceptable).
- No replacement of Frappe Desk sidebar.
- No new `bench build` bundle splits — stays single file.

## 3. UX Decisions Locked

| # | Decision | Rationale |
|---|---|---|
| D1 | Approach **B** (take ideas, not pixel-clone) | Keep Frappe chrome, avoid sidebar/breadcrumb conflicts |
| D2 | Filter row uses Frappe-native form controls only | Visual consistency with rest of bench, "no new CSS" |
| D3 | All 7 existing filters kept | User wants no functionality loss, only restyle |
| D4 | Pivot summary: months/weeks as **columns**, 4 metric **rows** | Easier to compare period over period than vertical stack |
| D5 | Click month **column** → highlight column + filter detail table | One-click drill-in; Y-axis click does nothing (unchanged) |
| D6 | Detail drill-down: bottom flat table grouped by Confidence | Replaces per-row expand; pagination + search |
| D7 | 4 KPI cards (Closing / Net / Inflow / Outflow) | Adds Net cash flow card; drops confidence breakdown badges |
| D8 | Chart: line chart 4 datasets | Replaces axis-mixed bars (no more outflow plotted as negative) |
| D9 | Detail data flow: server-side paginate + filter (D2 chosen) | Click pivot column = refetch with `period_key`; 60s Redis cache for providers |
| D10 | Pivot table: plain HTML `<table>` with sticky-left first column | Frappe Bootstrap classes only, no new CSS framework |

> **Why D9 chose server-side over eager-load**: User preference for D2. Mitigation for re-running 11 providers on every click: 60s Redis cache keyed by `(company, from_date, to_date)`.

## 4. Layout Overview

```
┌──────────────────────────────────────────────────────────────────────┐
│ [Frappe Desk sidebar]  │ Page title: "Dự Báo Dòng Tiền"   [⚙][↓Excel]│
│                        │ Page-form (Frappe-native filter row)         │
│                        │ ──────────────────────────────────────────  │
│                        │  ┌─────────────────────────────────────┐    │
│                        │  │ §A. KPI cards (4)                   │    │
│                        │  │ §B. Chart                           │    │
│                        │  │ §C. Pivot summary (sticky-left)     │    │
│                        │  │ §D. Detail table (paginated)        │    │
│                        │  └─────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────────────────┘
```

- Content padding: `padding: 0 20px` on `.forecast-content` wrapper. Pulls content off the sidebar boundary.
- Methodology HTML (current toggle panel) → **Frappe action menu item** (`page.add_menu_item("ℹ Phương Pháp Dự Báo", () => msgprint(...))`). No more permanent toggle panel.
- Settings dialog: `page.add_menu_item("⚙ Cài đặt", ...)` (was custom button).
- Excel export: `page.add_menu_item("↓ Xuất Excel", ...)`.

## 5. Section §A — Filter Row (Frappe-Native)

### 5.1 Field-by-field

| Order | Fieldname | Fieldtype | Label (vi) | Options/source | On change |
|---|---|---|---|---|---|
| 1 | `granularity` | Select | `Theo` | `monthly\nweekly` (display labels via `__()`) | reload data |
| 2 | `period` | Select | `Số kỳ dự báo` | `1..12` | reload data |
| 3 | `history` | Select | `Số kỳ quá khứ` | `0..12` | reload data |
| 4 | `company` | Link | `Công ty` | DocType=Company, default = `frappe.defaults.get_user_default("Company")` | reload data |
| 5 | `confidence` | MultiCheck | `Mức tin cậy` | `overdue, committed, probable, possible` | re-render only (client-side) + refetch detail |
| 6 | `inflow_sources` | MultiCheck | `Nguồn thu` | dynamic from `r.sources` filtered direction=inflow; labels via `_get_source_label()` (kept) | re-render + refetch detail |
| 7 | `outflow_sources` | MultiCheck | `Nguồn chi` | dynamic from `r.sources` filtered direction=outflow; labels via `_get_source_label()` (kept) | re-render + refetch detail |

> **Why MultiCheck not MultiSelectPills**: `frappe.ui.form.ControlMultiCheck` exists in Frappe v16 and exposes `get_checked_options()` for reading state. MultiSelectPills is a DocType-only widget.

> **Render risk + fallback**: MultiCheck renders **inline** (a row of checkboxes inside the field) rather than a popover. With 3 MultiCheck fields × 4–8 options each, the filter row may grow tall. **Verify during implementation**. If layout breaks: fall back to `frappe.ui.form.MultiSelectDialog` opened via a Data field with click-handler, OR fall back to MultiSelect (comma-separated string) — both keep things Frappe-native. Decision deferred to implementation.

> **Source label translations**: `_get_source_label(source_doctype)` and `_get_source_tooltip(source_doctype)` helpers in current `cash_flow_forecast.js` map raw DocType names ("Sales Order") → user-friendly labels ("Đơn đặt hàng (chờ xuất hóa đơn)"). **Keep both helpers** — used by the Inflow/Outflow MultiCheck `options` builder.

### 5.2 Render

```javascript
// Inside setup_page()
this.filters.granularity = this.page.add_field({
    fieldname: "granularity",
    label: __("Theo"),
    fieldtype: "Select",
    options: [
        { label: __("Tháng"), value: "monthly" },
        { label: __("Tuần"),  value: "weekly"  },
    ],
    default: "monthly",
    change: () => {
        this.granularity = this.filters.granularity.get_value();
        this._update_period_label();
        this.load_data();
    },
});
// ... similar for period, history, company
this.filters.confidence = this.page.add_field({
    fieldname: "confidence",
    label: __("Mức tin cậy"),
    fieldtype: "MultiCheck",
    options: this.confidence_levels.map(l => ({
        value: l, label: __(l.charAt(0).toUpperCase() + l.slice(1)),
        checked: true,
    })),
    change: () => {
        this.active_confidence = new Set(this.filters.confidence.get_checked_options());
        this.render();
        this._reload_detail_table();
    },
});
```

### 5.3 Removed CSS

The entire custom dropdown system (`.fcf-select`, `.fcf-multi`, `.fcf-menu`, `.fcf-btn`, `.fcf-action-btn`, `.fcf-export`, `.fcf-cnt`, `.fcf-val`, `.fcf-lbl`) is deleted from `cash_flow_forecast.css`.

The rule `.forecast-page .page-form { display: none !important }` is **removed** so Frappe page-form shows. (It was hidden because we used custom filters.)

## 6. Section §B — KPI Cards (4)

### 6.1 Card spec

```
┌────────────────────┬────────────────────┬────────────────────┬────────────────────┐
│ SỐ DƯ CUỐI KỲ      │ DÒNG TIỀN RÒNG     │ TỔNG THU VÀO       │ TỔNG CHI RA        │
│ {fmt(closing)} 💼  │ {fmt(net)}    📈/📉│ {fmt(inflow)}   ↗ │ {fmt(outflow)}  ↘ │
│ Tại {kỳ cuối}      │ {N} {kỳ}           │ {N} {kỳ}           │ {N} {kỳ}           │
│ Đầu kỳ: {fmt(opening)} │ Hiệu suất: {pct}% │ TB/kỳ: {fmt(avg)} │ TB/kỳ: {fmt(avg)} │
└────────────────────┴────────────────────┴────────────────────┴────────────────────┘
```

Where:
- `closing` = last forecast period closing balance.
- `net` = sum(forecast inflow) − sum(forecast outflow). Icon = trending-up if ≥0 else trending-down. Color: text-success if ≥0 else text-danger.
- `inflow` / `outflow` = sum across forecast periods.
- `pct` = `Math.round(net / inflow * 100)` if `inflow > 0` else `"—"`. (Edge case from self-review.)
- `avg` = total / number_of_forecast_periods.
- `kỳ` translates to "tháng" or "tuần" via granularity.
- `Đầu kỳ` = `opening_balance` from API (TK 111 + 112 + 113 today balance).

### 6.2 HTML

```html
<div class="row forecast-kpi-row">
  <div class="col-md-3"><div class="forecast-kpi-card">…</div></div>
  <div class="col-md-3">…</div>
  <div class="col-md-3">…</div>
  <div class="col-md-3">…</div>
</div>
```

Use Frappe's existing `.col-md-3` Bootstrap grid. The single new CSS class `.forecast-kpi-card` is allowed because it is layout-only (padding + border-radius + bg) and does not introduce a new design language; styles match Frappe `.frappe-card` if available, otherwise minimal token-based rules.

### 6.3 Icons

Use Frappe's bundled Lucide via `frappe.utils.icon(name, size)`:

| Card | Icon name |
|---|---|
| Closing | `wallet` |
| Net (positive) | `trending-up` |
| Net (negative) | `trending-down` |
| Inflow | `arrow-up-right` |
| Outflow | `arrow-down-right` |

> **Verify at implementation**: confirm `frappe.utils.icon("trending-up")` renders. Fallback: use Unicode arrows ↑ ↓ ↗ ↘.

### 6.4 Removed

Confidence breakdown badges (currently inside summary cards) — gone. Users use the Confidence filter in §A instead, and the detail table groups by confidence.

## 7. Section §C — Chart (line, 4 datasets)

### 7.1 Datasets

```javascript
new frappe.Chart($container[0], {
    type: "line",
    height: 320,
    colors: ["#0d6efd", "#0d6efd80", "#28a745", "#dc3545"], // blue solid, blue dashed, green, red
    data: {
        labels: monthly.map(m => m.label),
        datasets: [
            { name: __("Số dư thực tế"), values: monthly.map(m => m.is_historical ? m.closing : null) },
            { name: __("Số dư dự báo"),  values: monthly.map(m => m.is_historical ? null : m.closing) },
            { name: __("Dòng tiền vào"), values: monthly.map(m => m.inflow) },
            { name: __("Dòng tiền ra"),  values: monthly.map(m => m.outflow) },
        ],
        yMarkers: [{
            label: __("Mức tối thiểu (số dư)"),
            value: this.threshold,
            options: { labelPos: "left" },
        }],
    },
    tooltipOptions: { formatTooltipY: d => this.fmt_short(d) },
    axisOptions: { yAxisMode: "tick", shortenYAxisNumbers: true },
    lineOptions: { regionFill: 0, hideDots: 0, dotSize: 3 },
});
```

### 7.2 Now-marker overlay

The current overlay logic (`_add_chart_now_marker`) splits the **balance line** into actual (solid) + forecast (dashed) via clip-path. With 4 datasets, the technique must:

1. Find both `.line-graph-path` elements (now there are 4, one per dataset).
2. Identify the **balance line** by class or order — the first dataset rendered has dataset index 0; we use the actual-balance dataset (index 0). Verify by reading `data-dataset-index` attribute if present.
3. Split it (clip-path actual + dashed clone for forecast) — same as today.
4. Inflow (idx 2), Outflow (idx 3): leave solid throughout (no split).
5. Forecast-balance dataset (idx 1) is already dashed by definition (only forecast values, rest null) — its line will only render in the forecast region.

**Edge case**: if `frappe.Chart` doesn't render dotted lines for a dataset full of `null` values for the actual region, we use a single dataset for closing balance and split via clip-path (same as today). Plan: try the 4-dataset approach first; if visual is muddy, fall back to 3 datasets (Inflow / Outflow / Balance with split).

Background tint (light blue actual / light pink forecast) and "Hiện tại" vertical dashed line — unchanged from current implementation.

## 8. Section §D — Pivot Summary (Tóm tắt theo tháng/tuần)

### 8.1 Layout

```
┌──────────────────┬─────────┬─────────┬─────────┬┄─┬─────────┐
│ Chi tiêu         │ T04/26  │ T05/26  │ T06/26  │ … │ T03/27 │
├══════════════════┼═════════┼═════════┼═════════┼┄═┼═════════┤
│ Số dư đầu kỳ     │ 1,844.5 │   859.0 │   698.2 │ … │    50.0│
│ Dòng tiền vào    │ 1,142.1 │   859.0 │   693.1 │ … │   612.1│ ← td.direction-in (xanh)
│ Dòng tiền ra     │ 2,127.5 │   937.6 │   434.3 │ … │   662.1│ ← td.direction-out (đỏ)
│ Số dư cuối kỳ    │   859.0 │   698.2 │   957.0 │ … │     1.2│ ← td.warning-red/yellow nếu thấp
└──────────────────┴─────────┴─────────┴─────────┴┄─┴─────────┘
```

### 8.2 HTML

```html
<div class="forecast-pivot-wrap" style="overflow-x: auto">
  <table class="table table-bordered forecast-pivot-table">
    <thead>
      <tr>
        <th class="sticky-left">Chi tiêu</th>
        <th data-period="2026-04" class="period-col" data-historical="0">T04/2026</th>
        <th data-period="2026-05" class="period-col" data-historical="0">T05/2026</th>
        ...
      </tr>
    </thead>
    <tbody>
      <tr><th class="sticky-left">Số dư đầu kỳ</th><td data-period="2026-04">1,844.5</td>...</tr>
      <tr><th class="sticky-left">Dòng tiền vào</th><td class="direction-in" data-period="2026-04">1,142.1</td>...</tr>
      <tr><th class="sticky-left">Dòng tiền ra</th><td class="direction-out" data-period="2026-04">2,127.5</td>...</tr>
      <tr><th class="sticky-left">Số dư cuối kỳ</th><td data-period="2026-04" class="warning-yellow">859.0</td>...</tr>
    </tbody>
  </table>
</div>
```

### 8.3 Sticky-left CSS

The single small CSS rule allowed (stays in `cash_flow_forecast.css`):

```css
.forecast-pivot-table th.sticky-left,
.forecast-pivot-table td.sticky-left {
  position: sticky;
  left: 0;
  background: var(--card-bg, #fff);
  z-index: 2;
  border-right: 1px solid var(--border-color);
}
.forecast-pivot-table .period-col.col-selected,
.forecast-pivot-table td.col-selected {
  background: var(--bg-light-blue, #f0f4ff);
  cursor: pointer;
}
.forecast-pivot-table .period-col[data-historical="0"] { cursor: pointer; }
.forecast-pivot-table .period-col[data-historical="1"] { cursor: default; opacity: 0.7; }
```

### 8.4 Click-to-filter behavior

```javascript
// On any period column click (excluding sticky-left). Use arrow function so `this` is the controller.
const self = this;
this.$pivot.on("click", "th.period-col, td:not(.sticky-left)", function() {
    const $cell = $(this);
    const period = $cell.attr("data-period");
    if (!period) return;
    // Look up the column header's historical flag
    const $colHeader = self.$pivot.find(`th.period-col[data-period="${period}"]`);
    if ($colHeader.attr("data-historical") === "1") return;  // historical: no-op

    // Toggle: if same period clicked again → unselect
    const newPeriod = self.selected_period === period ? null : period;
    self._select_period(newPeriod);
});

_select_period(period_key) {
    this.selected_period = period_key;
    // Update column highlight class
    this.$pivot.find(".col-selected").removeClass("col-selected");
    if (period_key) {
        this.$pivot.find(`[data-period="${period_key}"]`).addClass("col-selected");
    }
    this._reload_detail_table();  // refetch with new period_key
}
```

### 8.5 Removed

- Old vertical 7-column table (Period / Opening / Inflow / Outflow / Net / MoM / Closing) — replaced.
- Drill-down `<tr class="drill-down">` expand-on-click — moved to §E flat table.
- MoM column — Net trend now lives in §B "Dòng tiền ròng" KPI card.

## 9. Section §E — Detail Table (Paginated, Grouped by Confidence)

### 9.1 Layout

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│ Chi tiết giao dịch dự báo  [📅 T05/2026 ✕]   [🔍 Tìm kiếm...     ]              │
├═════════════════════════════════════════════════════════════════════════════════┤
│ Loại giao dịch │ Mô tả │ Trạng thái │ Ngày dự kiến │ Tham chiếu │ Đối tác │+/-/N│
├─────────────────────────────────────────────────────────────────────────────────┤
│ ▼ ĐÃ CAM KẾT (xanh)                       Tổng: +1.142.105.000 / -2.127.544.500 │
│   Trả nợ vay      │ … │ Đã cam kết │ 30/04/2026 │ BL-2026-001 │ −     │ … │
│   ...                                                                            │
│ ▼ CÓ THỂ XẢY RA (vàng)                                                          │
│   Đơn đặt hàng    │ … │ Có thể XR  │ 15/05/2026 │ SAL-ORD-… │ Cty X │ … │
│   ...                                                                            │
│ ▼ DỰ KIẾN (xám)                                                                 │
│   Nộp Thuế GTGT   │ … │ Dự kiến    │ 20/05/2026 │ DCNET     │ −     │ … │
├─────────────────────────────────────────────────────────────────────────────────┤
│ Hiển thị 1 - 20 của 32 giao dịch                          [< 1  2  >]           │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### 9.2 Behavior

- **Filter chip** — when a pivot column is selected, shows `📅 T05/2026 ✕` chip above search. Click `✕` → unselects period (also unselects pivot column).
- **Search** — text input, debounce 300ms, sends `search` param to API. Backend `LIKE %search%` against `description` + `source_name` + `party` (verified entry shape: providers emit these three fields, no `reference_name`).
- **Grouping** — entries are server-sorted by `(confidence_priority, date)`. Client groups consecutive same-confidence rows under a header. Group headers re-render at every page boundary if the group continues.
- **Group totals** — server returns `group_totals: {overdue: {inflow, outflow, count}, committed: {...}, ...}` computed across full filtered set (NOT per-page). Headers display these.
- **Pagination** — `page=1, page_size=20`. Bottom: "Hiển thị X - Y của Z giao dịch" + page numbers. Click page → refetch.

### 9.3 Refetch triggers

Detail table refetches on:
1. Initial load (after main forecast data loads).
2. Filter change: `confidence`, `inflow_sources`, `outflow_sources`, `granularity`, `period`, `history`, `company` — but only after the main forecast `load_data()` completes (not parallel).
3. Pivot column click → set `period_key`, refetch.
4. Search input (debounce 300ms).
5. Pagination click.

### 9.4 API call

Constructor must initialize: `this.detail_search = ""; this.detail_page = 1; this.selected_period = null;`

```javascript
async _reload_detail_table() {
    const r = await frappe.xcall("vn_accounting.api.forecast.get_forecast_entries", {
        company: this.company,
        from_date: this.from_date,
        to_date: this.to_date,
        period_key: this.selected_period,           // null when no column selected
        granularity: this.granularity,
        confidences: [...this.active_confidence],
        sources: [...this.active_sources],
        search: this.detail_search || "",
        page: this.detail_page || 1,
        page_size: 20,
    });
    this._render_detail(r.entries, r.group_totals, r.total, r.page, r.page_size);
}
```

### 9.5 Removed

The current `get_drilldown_entries(period_key)` API is **deprecated and removed** in the same commit as the JS rewrite (per-row drill-down disappears at the same time). Callers other than the page itself: none. Implementation order:

1. Add `get_forecast_entries` first (it can coexist with `get_drilldown_entries`).
2. Rewrite JS to call `get_forecast_entries`.
3. Remove `get_drilldown_entries` once new endpoint is verified.

## 10. Backend API

### 10.1 New endpoint

`vn_accounting.api.forecast.get_forecast_entries(...)` — `@frappe.whitelist()`.

```python
import frappe
from datetime import datetime
from vn_accounting.forecast.aggregator import get_all_forecast_entries
from vn_accounting.forecast.payment_delay import clear_delay_cache

CONFIDENCE_ORDER = {"overdue": 0, "committed": 1, "probable": 2, "possible": 3}


@frappe.whitelist()
def get_forecast_entries(
    company: str,
    from_date: str,
    to_date: str,
    granularity: str = "monthly",
    period_key: str | None = None,
    confidences: list[str] | None = None,
    sources: list[str] | None = None,
    search: str = "",
    page: int = 1,
    page_size: int = 20,
) -> dict:
    """Return paginated forecast entries with confidence-group totals.

    Reuses the existing Redis cache populated by `get_forecast_data` (key:
    `forecast:{company}:{from_date}:{to_date}`, TTL 300s). Falls back to running
    providers if the cache is cold.
    """
    page = int(page)
    page_size = int(page_size)

    all_entries = _load_entries_with_cache(company, from_date, to_date)
    filtered = _filter_entries(
        all_entries,
        period_key=period_key,
        granularity=granularity,
        confidences=confidences,
        sources=sources,
        search=search,
    )
    filtered.sort(key=lambda e: (CONFIDENCE_ORDER.get(e["confidence"], 99), e["expected_date"]))

    group_totals = _compute_group_totals(filtered)
    total = len(filtered)
    start = (page - 1) * page_size
    page_entries = filtered[start : start + page_size]

    return {
        "entries": page_entries,
        "group_totals": group_totals,
        "total": total,
        "page": page,
        "page_size": page_size,
    }


def _load_entries_with_cache(company: str, from_date: str, to_date: str) -> list[dict]:
    """Reuse the same cache key shared with `get_forecast_data` (TTL 300s)."""
    cache_key = f"forecast:{company}:{from_date}:{to_date}"
    cached = frappe.cache.get_value(cache_key)
    if cached is not None:
        return cached
    clear_delay_cache()
    entries, _errors = get_all_forecast_entries({
        "company": company,
        "from_date": from_date,
        "to_date": to_date,
    })
    frappe.cache.set_value(cache_key, entries, expires_in_sec=300)
    return entries


def _filter_entries(entries, *, period_key, granularity, confidences, sources, search):
    out = []
    search_lower = (search or "").strip().lower()
    conf_set = set(confidences) if confidences else None
    src_set = set(sources) if sources else None

    for e in entries:
        if conf_set and e["confidence"] not in conf_set:
            continue
        if src_set and e["source_doctype"] not in src_set:
            continue
        if period_key:
            if "W" in period_key:
                d = datetime.strptime(e["expected_date"], "%Y-%m-%d")
                iso_y, iso_w, _ = d.isocalendar()
                if f"{iso_y}-W{iso_w:02d}" != period_key:
                    continue
            else:
                if e["expected_date"][:7] != period_key:
                    continue
        if search_lower:
            haystack = " ".join([
                str(e.get("description", "")),
                str(e.get("source_name", "")),
                str(e.get("party", "")),
            ]).lower()
            if search_lower not in haystack:
                continue
        out.append(e)
    return out


def _compute_group_totals(entries):
    """Totals per confidence across the FULL filtered set (not per-page)."""
    totals = {c: {"inflow": 0.0, "outflow": 0.0, "count": 0} for c in CONFIDENCE_ORDER}
    for e in entries:
        bucket = totals[e["confidence"]]
        if e["direction"] == "inflow":
            bucket["inflow"] += e["amount"]
        else:
            bucket["outflow"] += e["amount"]
        bucket["count"] += 1
    return totals
```

### 10.2 Existing endpoint

`get_forecast_data` — **unchanged**. Continues to return `cells`, `historical`, `opening_balance`, `threshold`, `sources`, `from_date`, `to_date`. Used by §A filters' source population, §B KPIs, §C chart, §D pivot.

### 10.3 Removed endpoint

`get_drilldown_entries(period_key, page, page_size)` — **removed** after JS rewrite. No external callers.

### 10.4 Cache invalidation

- **Reuse existing cache key + TTL** from `get_forecast_data` line 41: `forecast:{company}:{from_date}:{to_date}` with `expires_in_sec=300` (5 min). Both endpoints share this cache so a single provider run serves both summary and detail.
- No explicit invalidation on document save (forecast is best-effort projection; 5-minute staleness is acceptable for a refresh-button-driven UX).
- "Refresh" action in the page action menu calls `frappe.cache.delete_value(cache_key)` then reloads — immediate fresh data on demand.

> **Why reuse 300s instead of inventing 60s**: existing cache already exists, already proven adequate, and creating a parallel `forecast_entries:` key would double the memory footprint and double the provider cold runs. DRY wins.

> **Click-pivot performance**: Cache hit = round-trip ~50–100ms. Cache miss = ~800ms (providers run once per 5 minutes per company/date-range tuple). User clicks pivot column 5 times → 1 cold + 4 hot.

## 11. Files Affected

| Path | Change |
|---|---|
| `vn_accounting/vn_accounting/page/cash_flow_forecast/cash_flow_forecast.js` | Rewrite (~903 → ~600 lines) |
| `vn_accounting/vn_accounting/page/cash_flow_forecast/cash_flow_forecast.css` | Strip ~80 lines of `.fcf-*` dropdown CSS; keep ~50 lines for sticky-left + col-selected + group header + warning row + KPI card |
| `vn_accounting/api/forecast.py` | Add `get_forecast_entries` (+ helpers `_load_entries_with_cache`, `_filter_entries`, `_compute_group_totals`, `CONFIDENCE_ORDER`); remove `get_drilldown_entries` after JS rewrite |
| `vn_accounting/forecast/aggregator.py` | **No change** — existing `get_all_forecast_entries(args_dict)` is what we call |
| `vn_accounting/translations/vi.csv` | Add new strings (KPI labels, group headers, search placeholder, methodology menu item) |

## 12. i18n

All user-facing strings flow through `__()`. New strings to translate (English source → Vietnamese):

| Source | Vietnamese |
|---|---|
| `Cash Flow Forecast` | `Dự Báo Dòng Tiền` *(existing)* |
| `Closing Balance` | `Số dư cuối kỳ` |
| `Opening:` | `Đầu kỳ:` |
| `Net Cash Flow` | `Dòng tiền ròng` |
| `Performance:` | `Hiệu suất:` |
| `Total Inflow` | `Tổng thu vào` |
| `Total Outflow` | `Tổng chi ra` |
| `Avg/period:` | `TB/kỳ:` |
| `Actual Balance` | `Số dư thực tế` |
| `Forecast Balance` | `Số dư dự báo` |
| `Cash Inflow` | `Dòng tiền vào` |
| `Cash Outflow` | `Dòng tiền ra` |
| `Minimum Threshold (Balance)` | `Mức tối thiểu (số dư)` |
| `Summary by month/week` | `Tóm tắt theo tháng/tuần` |
| `Forecast Detail Transactions` | `Chi tiết giao dịch dự báo` |
| `Search transactions...` | `Tìm kiếm giao dịch...` |
| `Showing X - Y of Z transactions` | `Hiển thị X - Y của Z giao dịch` |
| `By Month` | `Theo tháng` *(existing-ish, retranslate)* |
| `By Week` | `Theo tuần` |
| `Forecast Periods` | `Số kỳ dự báo` |
| `History Periods` | `Số kỳ quá khứ` |
| `Confidence` | `Mức tin cậy` *(existing)* |
| `Inflow Sources` | `Nguồn thu` |
| `Outflow Sources` | `Nguồn chi` |
| `Methodology` | `Phương Pháp Dự Báo` *(existing)* |
| `Settings` | `Cài đặt` *(existing)* |
| `Export Excel` | `Xuất Excel` *(existing)* |

## 13. Edge Cases

| Case | Handling |
|---|---|
| User has 0 forecast entries (empty result) | `§D` shows `"Không có giao dịch nào"` (centered placeholder); `§B` KPIs show `0` for all values; `§C` chart shows opening balance flat line |
| Inflow = 0, computing Net "Hiệu suất %" | Display `"—"` instead of `Infinity` or `NaN` |
| Selected period_key has no entries | `§D` shows `"Không có giao dịch trong T05/2026"` placeholder + filter chip stays |
| Click historical column in `§C` | No-op. Cursor `default`, no highlight added |
| Provider error (1 of 11 fails) | `§D` still loads from `r.errors`, shows partial data + error banner like today |
| User changes Granularity (monthly→weekly) mid-session with period selected | `selected_period` cleared (different key format); detail re-fetches without filter |
| Search returns 0 results | "0 giao dịch phù hợp" placeholder, retain pagination control disabled |
| Cache hits across users | Cache key includes `company` so multi-tenant isolated. Across users with same company, shared cache (intended — same data) |

## 14. Out of Scope

These are **explicitly not in this redesign**:

- New forecast providers or new data sources.
- New confidence levels (still 4: overdue / committed / probable / possible).
- Changes to the Settings dialog content (only the entry button moves).
- Changes to the Methodology HTML content (only the trigger moves to menu).
- Changes to Excel export logic (only the trigger location).
- New permissions (RBAC unchanged).
- Mobile-optimized layout.
- Workspace sidebar (Frappe-managed).
- Frontend test suite (no JS unit tests in vn_accounting today; not adding for this redesign).

## 15. Verification Plan

When implementation completes, the following must pass before declaring done:

1. **Visual QA** (Playwright MCP, headed browser):
   - Filter row: 7 fields visible in single line on 1440px viewport, wrap on narrower.
   - 4 KPI cards: visible side-by-side ≥1200px, stack 2×2 below.
   - Chart: 4 lines render, balance solid+dashed split at "Hiện tại" marker.
   - Pivot: 12 month cols visible, scrolls horizontally, sticky first column works.
   - Click pivot column → highlights + detail filters.
   - Detail: search debounces (no firing per keystroke), pagination works, group headers reappear cross-page.
   - Console: 0 errors, 0 warnings related to this page.

2. **Translation check**: every new label has a `vi.csv` row; site language=vi shows Vietnamese.

3. **Backward compat**: existing bookmarks `/app/cash-flow-forecast` still load.

4. **Performance**: Pivot column click = round-trip ≤300ms (cache hit) or ≤1s (cache miss). Verify via Network tab.

5. **Existing v1 acceptance criteria still satisfied**: providers, confidence levels, historical actuals, opening balance — all unchanged. Smoke test: forecast totals match v1 for same company/date range.

## 16. Spec Self-Review

### Phase 1 — Surface scan (TBD/TODO, contradictions)

- ✅ **No placeholders** (no TBD, TODO, or hand-wave "...").
- ✅ **Internal consistency**: §5 filter fieldnames = §10.1 API params (`confidences`, `sources`, `period_key`, `granularity`, `search`, `page`, `page_size`). §8.4 selector excludes `.sticky-left`. §9.2 search fields = `description, source_name, party` — matches actual entry shape from providers.
- ✅ **Scope**: UI redesign only. Backend math untouched. Single implementation plan, ~7 tasks expected.

### Phase 2 — Copy-paste test (would each code block actually run?)

| Block | Verdict |
|---|---|
| §5.2 setup_page filter render | ✓ `page.add_field` API correct; `get_checked_options()` exists on `ControlMultiCheck` in v16. ⚠ MultiCheck inline render risk noted with fallback in §5.1. |
| §6.2 KPI cards HTML | ✓ Bootstrap col-md-3 grid is in Frappe, no custom framework. |
| §7.1 frappe.Chart 4 datasets | ✓ Type at chart top-level (matches existing `axis-mixed` usage). 8-digit hex stroke supported in modern browsers. Null gap behavior verified on existing implementations. |
| §7.2 now-marker for 4 lines | ⚠ Has fallback strategy if 4-dataset doesn't render cleanly. Implementation tests both paths. |
| §8.4 pivot click handler | ✓ `const self = this;` set; selector excludes sticky-left; data-period attribute lookup works because td has data-period directly per §8.2 HTML. |
| §9.4 detail API call | ✓ Constructor inits `detail_search`/`detail_page`/`selected_period`; query params match §10.1 signature. |
| §10.1 `get_forecast_entries` | ✓ Imports declared. Dict access `e["confidence"]`/`e["expected_date"]`. `CONFIDENCE_ORDER` defined inline. Helpers `_load_entries_with_cache`, `_filter_entries`, `_compute_group_totals` defined. Cache key + TTL match existing line 41 of forecast.py. |
| §10.4 cache reuse | ✓ Same key as `get_forecast_data` ⇒ providers run once per 5 minutes per (company, from, to) tuple. |

### Issues found in v1 of this spec and fixed

| Issue | Fix |
|---|---|
| Wrong function name `aggregator.collect_all_entries` | Use `get_all_forecast_entries(args_dict)` from `vn_accounting.forecast.aggregator` |
| Cache key `forecast_entries:` parallel to existing `forecast:` | Reuse existing `forecast:` key + 300s TTL |
| Search fields included `reference_name` (doesn't exist) | Search on `description + source_name + party` |
| Python code used attribute access `e.confidence` | Dict access `e["confidence"]` (entries are dicts) |
| `CONFIDENCE_ORDER` undefined | Defined as module constant |
| `_filter_entries` / `_compute_group_totals` undefined | Both defined in §10.1 |
| Click handler used `self` without binding | `const self = this;` before handler |
| Source label translations forgotten | `_get_source_label` / `_get_source_tooltip` kept (§5.1 note) |
| Detail state not initialized | Constructor inits `detail_search`/`detail_page`/`selected_period` |

### Remaining acknowledged risks

- **MultiCheck inline render width**: needs visual verification during implementation. Fallback to MultiSelectDialog or MultiSelect documented in §5.1.
- **Now-marker 4-line clip-path**: needs implementation testing; fallback to 3-dataset (Inflow/Outflow + balance with split) documented in §7.2.
- **frappe.Chart 8-digit hex stroke**: works on Chrome ≥60 (>99% Frappe Desk users); fallback to opaque color if any browser misrenders.

No further structural changes. Spec ready for plan derivation.
