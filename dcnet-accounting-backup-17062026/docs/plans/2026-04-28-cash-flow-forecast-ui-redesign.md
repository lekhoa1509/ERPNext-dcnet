# Cash Flow Forecast UI Redesign — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Refresh the Cash Flow Forecast page UI to match the team's shared Frappe-native design language: 4 KPI cards, line chart with 4 datasets, horizontal pivot summary, and paginated grouped detail table — without introducing new CSS framework.

**Architecture:** Single-file Frappe Page rewrite (`cash_flow_forecast.js`) plus one new whitelisted Python endpoint (`get_forecast_entries`). Filter row uses `page.add_field()` exclusively (no custom dropdowns). Detail table is server-side paginated, sharing the existing Redis cache key `forecast:{company}:{from}:{to}` with TTL 300s.

**Tech Stack:** Frappe v16 page system, frappe.Chart (line type), Bootstrap classes shipped with Frappe, jQuery, Python 3 backend. No new dependencies.

**Spec:** `docs/specs/2026-04-28-cash-flow-forecast-ui-redesign-design.md`

---

## File Structure

| Path | Action |
|---|---|
| `vn_accounting/api/forecast.py` | Modify: add `CONFIDENCE_ORDER`, `get_forecast_entries`, helpers `_load_entries_with_cache`, `_filter_entries`, `_compute_group_totals`. Remove `get_drilldown_entries` (Task 8). |
| `vn_accounting/api/test_forecast_entries.py` | Create: TDD unit tests for the pure helpers. |
| `vn_accounting/vn_accounting/page/cash_flow_forecast/cash_flow_forecast.js` | Rewrite section by section across Tasks 3–7. |
| `vn_accounting/vn_accounting/page/cash_flow_forecast/cash_flow_forecast.css` | Strip ~80 lines of `.fcf-*` rules; add ~30 lines for sticky-left, col-selected, KPI card layout, group header. |
| `vn_accounting/translations/vi.csv` | Append ~25 new label rows (Task 9). |

---

## Branch + Worktree Context

- Branch: `feat/cash-flow-forecast-ui-redesign` (already created).
- Worktree: `frappe-bench-dcnet/.worktrees/vn_accounting-cash-flow-ui/`.
- For visual QA: switch `apps/vn_accounting` to this branch temporarily, run `bench build --app vn_accounting && bench clear-cache`, refresh browser. Switch back to `main` after testing if other parallel sessions need main.

---

## Task 1: Backend — TDD pure helpers (`_filter_entries`, `_compute_group_totals`)

**Why first**: Pure functions are TDD-friendly. Test in isolation before wiring to Frappe.

**Files:**
- Create: `vn_accounting/api/test_forecast_entries.py`
- Modify: `vn_accounting/api/forecast.py` (add helpers + `CONFIDENCE_ORDER` near top)

- [ ] **Step 1.1: Write failing test for `_filter_entries`**

Create `vn_accounting/api/test_forecast_entries.py`:

```python
import unittest
from vn_accounting.api.forecast import (
    _filter_entries, _compute_group_totals, CONFIDENCE_ORDER,
)


class TestFilterEntries(unittest.TestCase):
    def _entry(self, **overrides):
        base = {
            "expected_date": "2026-05-15",
            "amount": 1000.0,
            "direction": "inflow",
            "category": "Sales Order",
            "confidence": "committed",
            "source_doctype": "Sales Order",
            "source_name": "SO-001",
            "description": "SO-001 customer ABC",
            "party": "Customer ABC",
        }
        base.update(overrides)
        return base

    def test_no_filter_returns_all(self):
        entries = [self._entry(), self._entry(amount=2000)]
        out = _filter_entries(entries, period_key=None, granularity="monthly",
                              confidences=None, sources=None, search="")
        self.assertEqual(len(out), 2)

    def test_period_key_monthly_match(self):
        entries = [
            self._entry(expected_date="2026-05-15"),
            self._entry(expected_date="2026-06-01"),
        ]
        out = _filter_entries(entries, period_key="2026-05", granularity="monthly",
                              confidences=None, sources=None, search="")
        self.assertEqual(len(out), 1)
        self.assertEqual(out[0]["expected_date"], "2026-05-15")

    def test_period_key_weekly_match(self):
        # 2026-05-04 is a Monday (ISO week 19 of 2026)
        entries = [
            self._entry(expected_date="2026-05-04"),  # ISO 2026-W19
            self._entry(expected_date="2026-05-11"),  # ISO 2026-W20
        ]
        out = _filter_entries(entries, period_key="2026-W19", granularity="weekly",
                              confidences=None, sources=None, search="")
        self.assertEqual(len(out), 1)
        self.assertEqual(out[0]["expected_date"], "2026-05-04")

    def test_confidence_filter(self):
        entries = [
            self._entry(confidence="committed"),
            self._entry(confidence="probable"),
            self._entry(confidence="possible"),
        ]
        out = _filter_entries(entries, period_key=None, granularity="monthly",
                              confidences=["committed", "probable"],
                              sources=None, search="")
        self.assertEqual(len(out), 2)
        self.assertEqual({e["confidence"] for e in out}, {"committed", "probable"})

    def test_source_filter(self):
        entries = [
            self._entry(source_doctype="Sales Order"),
            self._entry(source_doctype="Purchase Order"),
        ]
        out = _filter_entries(entries, period_key=None, granularity="monthly",
                              confidences=None, sources=["Sales Order"], search="")
        self.assertEqual(len(out), 1)
        self.assertEqual(out[0]["source_doctype"], "Sales Order")

    def test_search_matches_description(self):
        entries = [
            self._entry(description="ABC Co. invoice"),
            self._entry(description="XYZ Ltd. payment"),
        ]
        out = _filter_entries(entries, period_key=None, granularity="monthly",
                              confidences=None, sources=None, search="abc")
        self.assertEqual(len(out), 1)

    def test_search_matches_party(self):
        entries = [
            self._entry(party="Customer ABC", description="x"),
            self._entry(party="Supplier XYZ", description="y"),
        ]
        out = _filter_entries(entries, period_key=None, granularity="monthly",
                              confidences=None, sources=None, search="xyz")
        self.assertEqual(len(out), 1)
        self.assertEqual(out[0]["party"], "Supplier XYZ")

    def test_search_matches_source_name(self):
        entries = [
            self._entry(source_name="SO-001"),
            self._entry(source_name="PI-2026-099"),
        ]
        out = _filter_entries(entries, period_key=None, granularity="monthly",
                              confidences=None, sources=None, search="2026-099")
        self.assertEqual(len(out), 1)
        self.assertEqual(out[0]["source_name"], "PI-2026-099")

    def test_combined_filters(self):
        entries = [
            self._entry(confidence="committed", source_doctype="Sales Order"),
            self._entry(confidence="committed", source_doctype="Purchase Order"),
            self._entry(confidence="probable",  source_doctype="Sales Order"),
        ]
        out = _filter_entries(entries, period_key=None, granularity="monthly",
                              confidences=["committed"],
                              sources=["Sales Order"], search="")
        self.assertEqual(len(out), 1)


class TestComputeGroupTotals(unittest.TestCase):
    def _entry(self, **overrides):
        base = {
            "expected_date": "2026-05-15", "amount": 1000.0, "direction": "inflow",
            "confidence": "committed", "source_doctype": "Sales Order",
            "source_name": "x", "category": "x",
        }
        base.update(overrides)
        return base

    def test_empty_entries_returns_zeroed_buckets(self):
        out = _compute_group_totals([])
        self.assertEqual(set(out.keys()),
                         {"overdue", "committed", "probable", "possible"})
        for v in out.values():
            self.assertEqual(v, {"inflow": 0.0, "outflow": 0.0, "count": 0})

    def test_inflow_summed_per_confidence(self):
        entries = [
            self._entry(confidence="committed", direction="inflow", amount=100),
            self._entry(confidence="committed", direction="inflow", amount=200),
            self._entry(confidence="probable",  direction="inflow", amount=50),
        ]
        out = _compute_group_totals(entries)
        self.assertEqual(out["committed"]["inflow"], 300)
        self.assertEqual(out["committed"]["count"], 2)
        self.assertEqual(out["probable"]["inflow"], 50)

    def test_outflow_separated_from_inflow(self):
        entries = [
            self._entry(confidence="committed", direction="inflow",  amount=100),
            self._entry(confidence="committed", direction="outflow", amount=80),
        ]
        out = _compute_group_totals(entries)
        self.assertEqual(out["committed"]["inflow"], 100)
        self.assertEqual(out["committed"]["outflow"], 80)
        self.assertEqual(out["committed"]["count"], 2)


class TestConfidenceOrder(unittest.TestCase):
    def test_order_priorities(self):
        self.assertEqual(CONFIDENCE_ORDER["overdue"], 0)
        self.assertEqual(CONFIDENCE_ORDER["committed"], 1)
        self.assertEqual(CONFIDENCE_ORDER["probable"], 2)
        self.assertEqual(CONFIDENCE_ORDER["possible"], 3)
```

- [ ] **Step 1.2: Run failing tests**

```bash
cd /home/long/long/frappe-bench-dcnet
./env/bin/python -m unittest \
    apps/vn_accounting/vn_accounting/api/test_forecast_entries.py -v
```

Expected: ImportError for `_filter_entries` etc. (functions not yet defined).

- [ ] **Step 1.3: Implement `CONFIDENCE_ORDER` and helpers**

Edit `vn_accounting/api/forecast.py`. Add near the top, after existing imports:

```python
CONFIDENCE_ORDER = {"overdue": 0, "committed": 1, "probable": 2, "possible": 3}
```

Add at the bottom of the file (after `_group_by_month`):

```python
def _filter_entries(entries, *, period_key, granularity, confidences, sources, search):
    """Pure filter: period_key (monthly YYYY-MM or weekly YYYY-Www), confidences, sources, search."""
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
    """Sum inflow/outflow + count by confidence across the FULL filtered set."""
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

- [ ] **Step 1.4: Run tests, verify all pass**

```bash
cd /home/long/long/frappe-bench-dcnet
./env/bin/python -m unittest \
    apps/vn_accounting/vn_accounting/api/test_forecast_entries.py -v
```

Expected: 12 tests, all PASS.

- [ ] **Step 1.5: Commit**

```bash
cd /home/long/long/frappe-bench-dcnet/.worktrees/vn_accounting-cash-flow-ui
git add vn_accounting/api/forecast.py vn_accounting/api/test_forecast_entries.py
git commit -m "feat(forecast): add pure helpers + CONFIDENCE_ORDER for entry filtering

_filter_entries handles period_key (monthly/weekly), confidence, source,
and full-text search across description/source_name/party.
_compute_group_totals returns per-confidence totals across the whole
filtered set (not per-page).

12 unit tests cover empty-set, single-criterion, combined-filter, and
weekly ISO key match cases."
```

---

## Task 2: Backend — `get_forecast_entries` whitelisted endpoint

**Files:**
- Modify: `vn_accounting/api/forecast.py` (add `_load_entries_with_cache` + `get_forecast_entries`)

- [ ] **Step 2.1: Implement cache loader**

Append to `vn_accounting/api/forecast.py` (after the helpers added in Task 1):

```python
def _load_entries_with_cache(company: str, from_date: str, to_date: str) -> list[dict]:
    """Reuse the same cache key as get_forecast_data (TTL 300s)."""
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
```

- [ ] **Step 2.2: Implement `get_forecast_entries`**

Append to `vn_accounting/api/forecast.py`:

```python
@frappe.whitelist()
def get_forecast_entries(
    company: str,
    from_date: str,
    to_date: str,
    granularity: str = "monthly",
    period_key: str = None,
    confidences: list = None,
    sources: list = None,
    search: str = "",
    page: int = 1,
    page_size: int = 20,
) -> dict:
    """Return paginated forecast entries with confidence-group totals.

    Reuses the existing Redis cache populated by `get_forecast_data`.
    """
    page = int(page)
    page_size = int(page_size)
    # frappe.xcall sends list params as JSON-stringified
    if isinstance(confidences, str):
        confidences = frappe.parse_json(confidences) or None
    if isinstance(sources, str):
        sources = frappe.parse_json(sources) or None

    all_entries = _load_entries_with_cache(company, from_date, to_date)
    filtered = _filter_entries(
        all_entries,
        period_key=period_key,
        granularity=granularity,
        confidences=confidences,
        sources=sources,
        search=search or "",
    )
    filtered.sort(key=lambda e: (
        CONFIDENCE_ORDER.get(e["confidence"], 99),
        e["expected_date"],
    ))

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
```

- [ ] **Step 2.3: Smoke test the endpoint via bench console**

```bash
cd /home/long/long/frappe-bench-dcnet
bench --site dcnet.localhost console <<'PY'
import frappe, json
from vn_accounting.api.forecast import get_forecast_entries
company = frappe.db.get_value("Company", {}, "name")
from datetime import date, timedelta
today = date.today().strftime("%Y-%m-%d")
to = (date.today() + timedelta(days=365)).strftime("%Y-%m-%d")
r = get_forecast_entries(
    company=company, from_date=today, to_date=to,
    granularity="monthly", page=1, page_size=5,
)
print("total:", r["total"])
print("page:", r["page"], "size:", r["page_size"])
print("group_totals:", json.dumps(r["group_totals"], default=str))
print("first entry keys:", list(r["entries"][0].keys()) if r["entries"] else [])
PY
```

Expected output:
- `total: <integer ≥ 0>` (in sample data, ~195)
- `group_totals: {"overdue": {...}, "committed": {...}, ...}` with 4 keys
- `first entry keys: [expected_date, amount, direction, category, confidence, source_doctype, source_name, description, party, party_type]`

- [ ] **Step 2.4: Commit**

```bash
cd /home/long/long/frappe-bench-dcnet/.worktrees/vn_accounting-cash-flow-ui
git add vn_accounting/api/forecast.py
git commit -m "feat(forecast): add get_forecast_entries paginated API

Server-side pagination + filtering for the redesigned detail table.
Shares the existing Redis cache key forecast:{c}:{from}:{to} TTL 300s
with get_forecast_data so providers run once per company/date-range
tuple every 5 minutes.

Returns entries (current page) + group_totals (across full filtered set)
+ total + page + page_size."
```

---

## Task 3: JS — Replace filter row with `page.add_field()`

**Files:**
- Modify: `vn_accounting/vn_accounting/page/cash_flow_forecast/cash_flow_forecast.js` (replace `setup_page` and remove `_create_select` / `_create_multi`)

- [ ] **Step 3.1: Read current setup_page to map fields**

```bash
sed -n '33,141p' /home/long/long/frappe-bench-dcnet/.worktrees/vn_accounting-cash-flow-ui/vn_accounting/vn_accounting/page/cash_flow_forecast/cash_flow_forecast.js
```

Confirm the current 7 controls + buttons are: granularity, period, history, company, confidence, inflow, outflow, methodology, settings, export.

- [ ] **Step 3.2: Replace `setup_page()` and remove dropdown factories**

Edit the file. Replace lines 33–260 (everything from `setup_page()` through `_create_multi()` end-brace) with:

```javascript
setup_page() {
    this.page.wrapper.addClass("forecast-page");
    this.filters = {};

    // ── Filter row: Frappe-native page-form fields ────────────
    this.filters.granularity = this.page.add_field({
        fieldname: "granularity",
        label: __("Granularity"),
        fieldtype: "Select",
        options: `${__("By Month")}\n${__("By Week")}`,
        default: __("By Month"),
        change: () => {
            const v = this.filters.granularity.get_value();
            this._granularity = (v === __("By Week")) ? "weekly" : "monthly";
            this._update_period_label();
            this.load_data();
        },
    });

    this.filters.period = this.page.add_field({
        fieldname: "period",
        label: __("Forecast Periods"),
        fieldtype: "Select",
        options: Array.from({ length: 12 }, (_, i) => String(i + 1)).join("\n"),
        default: "12",
        change: () => {
            this._period = this.filters.period.get_value();
            this.load_data();
        },
    });

    this.filters.history = this.page.add_field({
        fieldname: "history",
        label: __("History Periods"),
        fieldtype: "Select",
        options: ["0", ...Array.from({ length: 12 }, (_, i) => String(i + 1))].join("\n"),
        default: "0",
        change: () => {
            this._history = this.filters.history.get_value();
            this.load_data();
        },
    });

    this.filters.company = this.page.add_field({
        fieldname: "company",
        label: __("Company"),
        fieldtype: "Link",
        options: "Company",
        default: this._company,
        change: () => {
            this._company = this.filters.company.get_value();
            this.load_data();
        },
    });

    this.filters.confidence = this.page.add_field({
        fieldname: "confidence",
        label: __("Confidence"),
        fieldtype: "MultiCheck",
        options: this.confidence_levels.map((l) => ({
            value: l,
            label: __(l.charAt(0).toUpperCase() + l.slice(1)),
            checked: true,
        })),
        change: () => {
            this.active_confidence = new Set(this.filters.confidence.get_checked_options());
            this.render();
            this.detail_page = 1;
            this._reload_detail_table();
        },
    });

    // Inflow / Outflow MultiCheck — populated dynamically after first load_data().
    this.filters.inflow_sources = this.page.add_field({
        fieldname: "inflow_sources", label: __("Inflow Sources"),
        fieldtype: "MultiCheck", options: [],
        change: () => this._on_source_change(),
    });
    this.filters.outflow_sources = this.page.add_field({
        fieldname: "outflow_sources", label: __("Outflow Sources"),
        fieldtype: "MultiCheck", options: [],
        change: () => this._on_source_change(),
    });

    // ── Action menu items (Methodology / Settings / Refresh / Export) ──
    this.page.add_menu_item(`ℹ ${__("Methodology")}`, () => this._show_methodology());
    this.page.add_menu_item(`⚙ ${__("Settings")}`, () => this._show_settings_dialog());
    this.page.add_menu_item(`↻ ${__("Refresh (clear cache)")}`, () => this._refresh_force());
    this.page.set_secondary_action(`↓ ${__("Excel")}`, () => this.export_excel());

    // ── Content area ──
    this.content = $(`<div class="forecast-content">
        <div class="error-banner" style="display:none"></div>
        <div class="forecast-timestamp"></div>
        <div class="kpi-row"></div>
        <div class="chart-container"></div>
        <div class="pivot-container"></div>
        <div class="detail-container"></div>
    </div>`).appendTo(this.page.main);
}

_update_period_label() {
    const lbl = this._granularity === "weekly" ? __("Forecast (weeks)") : __("Forecast (months)");
    this.filters.period.df.label = lbl;
    this.filters.period.refresh_input?.();
}

_on_source_change() {
    const inflow = this.filters.inflow_sources.get_checked_options();
    const outflow = this.filters.outflow_sources.get_checked_options();
    this.active_sources = new Set([...inflow, ...outflow]);
    this.render();
    this.detail_page = 1;
    this._reload_detail_table();
}

_show_methodology() {
    frappe.msgprint({
        title: __("Methodology"),
        message: this._get_methodology_html(),
        indicator: "blue",
        wide: true,
    });
}

_refresh_force() {
    frappe.xcall("frappe.cache.delete_value", {
        key: `forecast:${this._company}:${this._from_date}:${this._to_date}`,
    }).finally(() => this.load_data());
}
```

Also update the constructor — replace lines 11–31 (current constructor body) to initialize new state:

```javascript
constructor(page) {
    this.page = page;
    this.entries = [];
    this.errors = [];
    this.opening_balance = 0;
    this.threshold = 500000000;
    this.historical = [];
    this.confidence_levels = ["overdue", "committed", "probable", "possible"];
    this.active_confidence = new Set(this.confidence_levels);
    this.active_sources = new Set();
    this.all_sources = [];

    this._granularity = "monthly";
    this._period = "12";
    this._history = "0";
    this._company = frappe.defaults.get_user_default("Company") || "";

    // Detail table state (D2 server-side paginated)
    this.detail_search = "";
    this.detail_page = 1;
    this.detail_page_size = 20;
    this.selected_period = null;

    this.setup_page();
    this.load_data();
}
```

Remove `_load_companies()` (Frappe Link field auto-loads).

- [ ] **Step 3.3: Update `_update_source_dropdowns` to use new MultiCheck fields**

Replace the existing `_update_source_dropdowns` (around lines 287–315) with:

```javascript
_update_source_dropdowns() {
    const inflow_src = new Set();
    const outflow_src = new Set();
    for (const src_confs of Object.values(this._cells || {})) {
        for (const [src, confs] of Object.entries(src_confs)) {
            for (const amounts of Object.values(confs)) {
                if (amounts.inflow > 0) inflow_src.add(src);
                if (amounts.outflow > 0) outflow_src.add(src);
            }
        }
    }

    const make_options = (src_set) => [...src_set].sort().map((s) => ({
        value: s, label: this._get_source_label(s), checked: this.active_sources.has(s),
    }));

    // Replace MultiCheck options dynamically
    this.filters.inflow_sources.df.options = make_options(inflow_src);
    this.filters.inflow_sources.refresh_input?.();
    this.filters.outflow_sources.df.options = make_options(outflow_src);
    this.filters.outflow_sources.refresh_input?.();
}
```

(Keep `_get_source_label` and `_get_source_tooltip` unchanged — they're used by this builder.)

- [ ] **Step 3.4: Strip dropdown CSS from `cash_flow_forecast.css`**

Delete lines covering `.fcf-filters`, `.fcf-btn`, `.fcf-action-btn`, `.fcf-lbl`, `.fcf-val`, `.fcf-cnt`, `.fcf-export`, `.fcf-select`, `.fcf-multi`, `.fcf-menu`, `.fcf-option`, and the rule `.forecast-page .page-form { display: none !important; }`.

Keep: badge styles for confidence (`.badge-overdue`, `.badge-committed`, `.badge-probable`, `.badge-possible`, `.badge-historical`), warning row classes (`.warning-red`, `.warning-yellow`, `.historical-row`), direction colors (`.direction-in`, `.direction-out`, `.color-balance`), `.forecast-content`, `.error-banner`, `.methodology-panel`.

Add to the top:

```css
/* Padding from sidebar */
.forecast-page .forecast-content {
    padding: 0 20px;
}
```

- [ ] **Step 3.5: Verify page loads without errors**

```bash
cd /home/long/long/frappe-bench-dcnet
bench build --app vn_accounting && bench clear-cache
```

Open `http://dcnet.localhost:8001/app/cash-flow-forecast` in browser. Expected:
- Filter row shows 7 Frappe-native controls (Granularity, Forecast, History, Company, Confidence checkboxes, Inflow Sources checkboxes, Outflow Sources checkboxes).
- Console: 0 errors.
- "Methodology", "Settings", "Refresh" appear in page menu (...) — Excel as secondary action.
- KPI/Chart/Pivot/Detail areas empty (next tasks fill them).
- Page sits with 20px gap from left sidebar.

If MultiCheck visually overflows the filter row (3 checkbox groups too tall), switch the 3 MultiCheck fields to `MultiSelect` fieldtype as a fallback (string of comma-separated values; `change` callback parses with `.split(",")`). Document the choice in commit message.

- [ ] **Step 3.6: Commit**

```bash
cd /home/long/long/frappe-bench-dcnet/.worktrees/vn_accounting-cash-flow-ui
git add vn_accounting/vn_accounting/page/cash_flow_forecast/cash_flow_forecast.js \
        vn_accounting/vn_accounting/page/cash_flow_forecast/cash_flow_forecast.css
git commit -m "refactor(cash-flow): switch filter row to Frappe page-form fields

Replace ~150 lines of custom .fcf-* dropdown JS + ~80 lines of CSS with
page.add_field() for all 7 filters. Uses Select / Link / MultiCheck
fieldtypes natively. Methodology / Settings / Refresh moved to page
menu, Excel to secondary action. Adds 20px content padding from sidebar.

KPI/Chart/Pivot/Detail areas left empty for next tasks."
```

---

## Task 4: JS — Replace `render_summary` with 4 KPI cards

**Files:**
- Modify: `cash_flow_forecast.js` — replace `render_summary` body
- Modify: `cash_flow_forecast.css` — add KPI card layout

- [ ] **Step 4.1: Replace `render_summary` body**

Find `render_summary(monthly)` (around line 376) and replace its full body with:

```javascript
render_summary(monthly) {
    const $row = this.content.find(".kpi-row").empty();
    const forecast = monthly.filter((m) => !m.is_historical);
    if (!forecast.length) return;

    const total_in = forecast.reduce((s, m) => s + m.inflow, 0);
    const total_out = forecast.reduce((s, m) => s + m.outflow, 0);
    const net = total_in - total_out;
    const last = forecast[forecast.length - 1];
    const last_closing = last.closing;
    const period_count = forecast.length;
    const period_word = this._granularity === "weekly" ? __("weeks") : __("months");
    const last_label = last.label;

    const performance = total_in > 0
        ? `${Math.round((net / total_in) * 100)}%`
        : "—";

    const avg_in = total_in / period_count;
    const avg_out = total_out / period_count;

    const card = (label, value, value_class, footer, icon_html) => `
        <div class="col-md-3">
            <div class="forecast-kpi-card">
                <div class="kpi-label">${label}</div>
                <div class="kpi-value ${value_class}">${value} ${icon_html}</div>
                <div class="kpi-footer text-muted">${footer}</div>
            </div>
        </div>`;

    const arrow_up = `<span class="kpi-icon direction-in">▲</span>`;
    const arrow_down = `<span class="kpi-icon direction-out">▼</span>`;
    const wallet = `<span class="kpi-icon">💼</span>`;

    $row.html(`<div class="row">${
        card(
            __("Closing Balance"),
            this.fmt_short(last_closing),
            "color-balance",
            `${__("At")} ${last_label} · ${__("Opening:")} ${this.fmt_short(this.opening_balance)}`,
            wallet,
        ) +
        card(
            __("Net Cash Flow"),
            this.fmt_short(net),
            net >= 0 ? "direction-in" : "direction-out",
            `${period_count} ${period_word} · ${__("Performance:")} ${performance}`,
            net >= 0 ? arrow_up : arrow_down,
        ) +
        card(
            __("Total Inflow"),
            this.fmt_short(total_in),
            "direction-in",
            `${period_count} ${period_word} · ${__("Avg/period:")} ${this.fmt_short(avg_in)}`,
            arrow_up,
        ) +
        card(
            __("Total Outflow"),
            this.fmt_short(total_out),
            "direction-out",
            `${period_count} ${period_word} · ${__("Avg/period:")} ${this.fmt_short(avg_out)}`,
            arrow_down,
        )
    }</div>`);
}
```

- [ ] **Step 4.2: Add KPI CSS**

Append to `cash_flow_forecast.css`:

```css
/* KPI cards */
.forecast-page .kpi-row {
    margin: 12px 0 18px;
}
.forecast-page .forecast-kpi-card {
    background: var(--card-bg, #fff);
    border: 1px solid var(--border-color);
    border-radius: 8px;
    padding: 14px 16px;
    height: 100%;
}
.forecast-page .forecast-kpi-card .kpi-label {
    font-size: 11px;
    text-transform: uppercase;
    color: var(--text-muted);
    letter-spacing: 0.5px;
    margin-bottom: 4px;
}
.forecast-page .forecast-kpi-card .kpi-value {
    font-size: 22px;
    font-weight: 600;
    line-height: 1.2;
    margin-bottom: 4px;
}
.forecast-page .forecast-kpi-card .kpi-footer {
    font-size: 11px;
}
.forecast-page .forecast-kpi-card .kpi-icon {
    font-size: 13px;
    margin-left: 4px;
}
```

- [ ] **Step 4.3: Build and verify**

```bash
cd /home/long/long/frappe-bench-dcnet
bench build --app vn_accounting && bench clear-cache
```

Refresh browser. Expected:
- 4 cards in a row at ≥1200px viewport.
- Card values formatted via `fmt_short` ("9.7 tỷ", "808 tr").
- Net card icon green ↑ if positive, red ↓ if negative.
- "Performance:" shows "—" if Inflow=0.
- Console: 0 errors.

- [ ] **Step 4.4: Commit**

```bash
cd /home/long/long/frappe-bench-dcnet/.worktrees/vn_accounting-cash-flow-ui
git add vn_accounting/vn_accounting/page/cash_flow_forecast/cash_flow_forecast.js \
        vn_accounting/vn_accounting/page/cash_flow_forecast/cash_flow_forecast.css
git commit -m "feat(cash-flow): 4 KPI cards (Closing/Net/Inflow/Outflow)

Replaces 3-card breakdown with 4-card layout matching the team mockup.
Net card adds 'Performance' (Net/Inflow %) with —fallback when Inflow=0.
Inflow/Outflow cards show TB/period (avg). Closing card shows opening
balance reference."
```

---

## Task 5: JS — Replace `render_chart` with 4-line chart

**Files:**
- Modify: `cash_flow_forecast.js` — replace `render_chart` and `_add_chart_now_marker`

- [ ] **Step 5.1: Replace `render_chart`**

Find `render_chart(monthly)` (around line 496) and replace the body with:

```javascript
render_chart(monthly) {
    const $c = this.content.find(".chart-container").empty();
    if (!monthly.length) return;

    const hc = this.historical.length;

    new frappe.Chart($("<div></div>").appendTo($c)[0], {
        type: "line",
        height: 320,
        colors: ["#0d6efd", "#7ba6f5", "#28a745", "#dc3545"], // actual blue, forecast blue (lighter), green, red
        data: {
            labels: monthly.map((m) => m.label),
            datasets: [
                { name: __("Actual Balance"),  values: monthly.map((m) => m.is_historical ? m.closing : null) },
                { name: __("Forecast Balance"), values: monthly.map((m) => m.is_historical ? null : m.closing) },
                { name: __("Cash Inflow"),     values: monthly.map((m) => m.inflow) },
                { name: __("Cash Outflow"),    values: monthly.map((m) => m.outflow) },
            ],
            yMarkers: [{
                label: __("Minimum Threshold (Balance)"),
                value: this.threshold,
                options: { labelPos: "left" },
            }],
        },
        tooltipOptions: { formatTooltipY: (d) => this.fmt_short(d) },
        axisOptions: { yAxisMode: "tick", shortenYAxisNumbers: true },
        lineOptions: { regionFill: 0, hideDots: 0, dotSize: 3 },
    });

    if (hc > 0 && hc < monthly.length) {
        this._add_chart_overlay($c, hc, monthly.length);
    }
}
```

- [ ] **Step 5.2: Replace `_add_chart_now_marker` → `_add_chart_overlay` (simplified for 4 datasets)**

The 4-dataset approach already splits Actual/Forecast lines via null gap. Now-marker overlay only needs:
1. Background tint (light blue actual region, light pink forecast region)
2. Vertical "Hiện tại" dashed line + label

It no longer needs clip-path on the balance line (datasets 1+2 already render as separate disconnected segments).

Replace `_add_chart_now_marker` with:

```javascript
_add_chart_overlay($container, hc, total) {
    setTimeout(() => {
        const svg = $container.find("svg")[0];
        if (!svg) return;
        const drawArea = svg.querySelector(".chart-draw-area");
        if (!drawArea) return;

        const bbox = drawArea.getBBox();
        const step = bbox.width / Math.max(total - 1, 1);
        const x = hc * step;
        const ns = "http://www.w3.org/2000/svg";

        // Background: actual period (light blue)
        const bgA = document.createElementNS(ns, "rect");
        Object.entries({ x: 0, y: 0, width: x, height: bbox.height, fill: "rgba(59,130,246,0.06)" })
            .forEach(([k, v]) => bgA.setAttribute(k, v));
        drawArea.insertBefore(bgA, drawArea.firstChild);

        // Background: forecast period (light pink)
        const bgF = document.createElementNS(ns, "rect");
        Object.entries({ x, y: 0, width: bbox.width - x, height: bbox.height, fill: "rgba(239,68,68,0.05)" })
            .forEach(([k, v]) => bgF.setAttribute(k, v));
        drawArea.insertBefore(bgF, bgA.nextSibling);

        // Vertical dashed line
        const line = document.createElementNS(ns, "line");
        Object.entries({
            x1: x, x2: x, y1: 0, y2: bbox.height,
            stroke: "#94a3b8", "stroke-dasharray": "6,4", "stroke-width": "1.5",
        }).forEach(([k, v]) => line.setAttribute(k, v));
        drawArea.appendChild(line);

        // "Current" label
        const txt = document.createElementNS(ns, "text");
        txt.setAttribute("x", x);
        txt.setAttribute("y", bbox.height + 14);
        txt.setAttribute("text-anchor", "middle");
        txt.setAttribute("font-size", "11");
        txt.setAttribute("fill", "#64748b");
        txt.setAttribute("font-weight", "600");
        txt.textContent = __("Current");
        drawArea.appendChild(txt);
    }, 300);
}
```

- [ ] **Step 5.3: Build and verify**

```bash
cd /home/long/long/frappe-bench-dcnet
bench build --app vn_accounting && bench clear-cache
```

Refresh browser. Expected:
- Chart shows 4 lines: Actual (solid darker blue), Forecast (solid lighter blue), Inflow (green), Outflow (red).
- Actual line ends at "Hiện tại" marker; Forecast line starts there.
- Background light blue (left) / light pink (right) of "Hiện tại".
- Threshold y-marker labeled "Mức tối thiểu (số dư)" / "Minimum Threshold (Balance)".
- No more outflow bar plotted as negative; both Inflow and Outflow shown as positive lines.
- Console: 0 errors.

If the Actual + Forecast lines render as one connected line (frappe-charts may interpolate over null), fall back to a single-dataset Balance line and re-introduce the clip-path split from the previous implementation. Document fallback choice in commit message.

- [ ] **Step 5.4: Commit**

```bash
cd /home/long/long/frappe-bench-dcnet/.worktrees/vn_accounting-cash-flow-ui
git add vn_accounting/vn_accounting/page/cash_flow_forecast/cash_flow_forecast.js
git commit -m "feat(cash-flow): line chart with 4 datasets, drop axis-mixed bars

Inflow and Outflow now plot as solid green/red lines (not bars below
zero). Balance line splits actual/forecast via separate null-padded
datasets, removing the clip-path hack. Background tint + vertical
'Hiện tại' marker preserved."
```

---

## Task 6: JS — Replace `render_table` with horizontal pivot + click handler

**Files:**
- Modify: `cash_flow_forecast.js` — replace `render_table`, remove `_load_drilldown` and per-row drill-down rendering
- Modify: `cash_flow_forecast.css` — add sticky-left + col-selected rules

- [ ] **Step 6.1: Replace `render_table` with pivot rendering**

Find `render_table(monthly)` and replace its full body with:

```javascript
render_table(monthly) {
    const $c = this.content.find(".pivot-container").empty();
    if (!monthly.length) return;

    const fmt = (v) => this.fmt(v);

    const periodHeaderCells = monthly.map((m) =>
        `<th class="period-col" data-period="${m.key}" data-historical="${m.is_historical ? 1 : 0}">${m.label}</th>`
    ).join("");

    const rowCells = (key, valueFn, classFn) => monthly.map((m) => {
        const cls = classFn ? classFn(m) : "";
        return `<td class="${cls}" data-period="${m.key}">${valueFn(m)}</td>`;
    }).join("");

    const closingClass = (m) => {
        if (m.closing < 0) return "warning-red";
        if (m.closing < this.threshold) return "warning-yellow";
        return "";
    };

    $c.html(`
        <h6 class="forecast-section-title">${__("Summary by month/week")}</h6>
        <div class="forecast-pivot-wrap">
        <table class="table table-bordered forecast-pivot-table">
            <thead>
                <tr>
                    <th class="sticky-left">${__("Metric")}</th>
                    ${periodHeaderCells}
                </tr>
            </thead>
            <tbody>
                <tr><th class="sticky-left">${__("Opening")}</th>${rowCells("opening", (m) => fmt(m.opening))}</tr>
                <tr><th class="sticky-left">${__("Inflow")}</th>${rowCells("inflow", (m) => fmt(m.inflow), () => "direction-in")}</tr>
                <tr><th class="sticky-left">${__("Outflow")}</th>${rowCells("outflow", (m) => fmt(m.outflow), () => "direction-out")}</tr>
                <tr><th class="sticky-left">${__("Closing")}</th>${rowCells("closing", (m) => fmt(m.closing), closingClass)}</tr>
            </tbody>
        </table>
        </div>
    `);

    // Click cột tháng/tuần → highlight + filter detail
    this.$pivot = $c.find(".forecast-pivot-table");
    const self = this;
    this.$pivot.on("click", "th.period-col, td:not(.sticky-left)", function() {
        const $cell = $(this);
        const period = $cell.attr("data-period");
        if (!period) return;
        const $colHeader = self.$pivot.find(`th.period-col[data-period="${period}"]`);
        if ($colHeader.attr("data-historical") === "1") return;  // historical: no-op

        const newPeriod = self.selected_period === period ? null : period;
        self._select_period(newPeriod);
    });

    // Re-apply highlight if a period is currently selected (after re-render)
    if (this.selected_period) {
        this.$pivot.find(`[data-period="${this.selected_period}"]`).addClass("col-selected");
    }
}

_select_period(period_key) {
    this.selected_period = period_key;
    this.$pivot.find(".col-selected").removeClass("col-selected");
    if (period_key) {
        this.$pivot.find(`[data-period="${period_key}"]`).addClass("col-selected");
    }
    this.detail_page = 1;
    this._reload_detail_table();
}
```

- [ ] **Step 6.2: Add pivot CSS**

Append to `cash_flow_forecast.css`:

```css
/* Pivot table */
.forecast-page .forecast-section-title {
    font-size: 13px;
    margin: 16px 0 8px;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
.forecast-page .forecast-pivot-wrap {
    overflow-x: auto;
    border: 1px solid var(--border-color);
    border-radius: 6px;
}
.forecast-page .forecast-pivot-table {
    margin: 0;
}
.forecast-page .forecast-pivot-table th,
.forecast-page .forecast-pivot-table td {
    text-align: right;
    white-space: nowrap;
    font-size: 12px;
    padding: 6px 10px;
}
.forecast-page .forecast-pivot-table th.sticky-left,
.forecast-page .forecast-pivot-table td.sticky-left {
    position: sticky;
    left: 0;
    background: var(--card-bg, #fff);
    text-align: left;
    z-index: 2;
    border-right: 2px solid var(--border-color);
}
.forecast-page .forecast-pivot-table thead th.period-col[data-historical="0"] {
    cursor: pointer;
}
.forecast-page .forecast-pivot-table thead th.period-col[data-historical="1"] {
    cursor: default;
    opacity: 0.7;
}
.forecast-page .forecast-pivot-table tbody td:not(.sticky-left) {
    cursor: pointer;
}
.forecast-page .forecast-pivot-table .col-selected {
    background: var(--bg-light-blue, #e8f0fe);
}
```

- [ ] **Step 6.3: Build and verify**

```bash
cd /home/long/long/frappe-bench-dcnet
bench build --app vn_accounting && bench clear-cache
```

Refresh browser. Expected:
- Pivot table shows 4 rows × N columns (months/weeks).
- First column "Metric" sticky-left, scroll horizontally with right-side data.
- Click any cell in T05/2026 column → that whole column highlights light blue + (Task 7 will refresh detail table).
- Click again → un-highlights.
- Click historical column → no highlight (cursor: default).
- Console: 0 errors.

- [ ] **Step 6.4: Commit**

```bash
cd /home/long/long/frappe-bench-dcnet/.worktrees/vn_accounting-cash-flow-ui
git add vn_accounting/vn_accounting/page/cash_flow_forecast/cash_flow_forecast.js \
        vn_accounting/vn_accounting/page/cash_flow_forecast/cash_flow_forecast.css
git commit -m "feat(cash-flow): horizontal pivot summary with click-to-filter

Replaces 7-column vertical table (Period/Opening/Inflow/Outflow/Net/MoM/
Closing) with horizontal pivot: 4 metric rows × N period columns. First
column sticky-left so users can scroll across long periods. Clicking any
cell in a period column highlights the column + signals detail table to
filter (next task wires the refresh)."
```

---

## Task 7: JS — Replace drill-down with paginated grouped detail table

**Files:**
- Modify: `cash_flow_forecast.js` — replace `_load_drilldown` and `_render_drilldown_page` with `_reload_detail_table` + `_render_detail`

- [ ] **Step 7.1: Add detail table render function**

Replace the existing `_load_drilldown` and `_render_drilldown_page` (and any per-row click handler in `render_table` — already removed in Task 6) with the new functions.

Append new methods to the class:

```javascript
async _reload_detail_table() {
    if (!this._company) return;
    const $c = this.content.find(".detail-container");
    if (!$c.find(".detail-loading").length) {
        $c.html(`<div class="detail-loading text-center text-muted" style="padding:20px">${__("Loading...")}</div>`);
    }
    try {
        const r = await frappe.xcall("vn_accounting.api.forecast.get_forecast_entries", {
            company: this._company,
            from_date: this._from_date,
            to_date: this._to_date,
            granularity: this._granularity,
            period_key: this.selected_period,
            confidences: [...this.active_confidence],
            sources: [...this.active_sources],
            search: this.detail_search || "",
            page: this.detail_page || 1,
            page_size: this.detail_page_size,
        });
        this._render_detail(r);
    } catch (e) {
        $c.html(`<div class="alert alert-danger">${e.message || String(e)}</div>`);
    }
}

_render_detail(r) {
    const $c = this.content.find(".detail-container").empty();
    const cl = {
        overdue: __("Overdue"), committed: __("Committed"),
        probable: __("Probable"), possible: __("Possible"),
    };
    const conf_order = ["overdue", "committed", "probable", "possible"];

    // Header row: title + chip + search
    const chip = this.selected_period
        ? `<span class="badge badge-period">📅 ${this.selected_period} <a href="#" class="chip-clear" style="margin-left:4px">✕</a></span>`
        : "";
    const search_input = `<input type="text" class="form-control input-sm detail-search-input"
        placeholder="${__("Search transactions...")}" value="${frappe.utils.escape_html(this.detail_search || "")}" style="max-width:280px">`;

    let html = `
        <div class="detail-header">
            <h6 class="forecast-section-title">${__("Forecast Detail Transactions")}</h6>
            <div class="detail-toolbar">${chip}${search_input}</div>
        </div>
    `;

    if (!r.entries.length) {
        const msg = this.selected_period
            ? __("No transactions in {0}").replace("{0}", this.selected_period)
            : __("No transactions");
        html += `<div class="detail-empty text-muted text-center" style="padding:20px">${msg}</div>`;
        $c.html(html);
        this._wire_detail_events($c);
        return;
    }

    // Table with confidence groups (insert <tr.dd-group-header> at confidence boundaries)
    html += `<table class="table table-bordered detail-table">
        <thead><tr>
            <th>${__("Type")}</th>
            <th>${__("Description")}</th>
            <th>${__("Status")}</th>
            <th>${__("Expected Date")}</th>
            <th>${__("Reference")}</th>
            <th>${__("Party")}</th>
            <th class="text-right">${__("Inflow")}</th>
            <th class="text-right">${__("Outflow")}</th>
            <th class="text-right">${__("Net")}</th>
        </tr></thead><tbody>`;

    let last_conf = null;
    for (const e of r.entries) {
        if (e.confidence !== last_conf) {
            const g = r.group_totals[e.confidence] || { inflow: 0, outflow: 0, count: 0 };
            html += `<tr class="dd-group-header"><td colspan="9">
                <span class="badge badge-${e.confidence}">${cl[e.confidence] || e.confidence}</span>
                <span class="text-muted" style="margin-left:8px">
                    ${__("Total")}: <span class="direction-in">+${this.fmt_short(g.inflow)}</span>
                    / <span class="direction-out">-${this.fmt_short(g.outflow)}</span>
                    (${g.count} ${__("entries")})
                </span>
            </td></tr>`;
            last_conf = e.confidence;
        }
        const inflow = e.direction === "inflow" ? this.fmt(e.amount) : "—";
        const outflow = e.direction === "outflow" ? this.fmt(e.amount) : "—";
        const net = e.direction === "inflow" ? e.amount : -e.amount;
        const net_class = net >= 0 ? "direction-in" : "direction-out";
        html += `<tr>
            <td>${frappe.utils.escape_html(this._get_source_label(e.source_doctype) || e.category || "")}</td>
            <td>${frappe.utils.escape_html(e.description || "")}</td>
            <td><span class="badge badge-${e.confidence}">${cl[e.confidence]}</span></td>
            <td>${e.expected_date}</td>
            <td>${e.source_name ? `<a href="/app/${frappe.router.slug(e.source_doctype)}/${e.source_name}" target="_blank">${e.source_name}</a>` : "—"}</td>
            <td>${frappe.utils.escape_html(e.party || "—")}</td>
            <td class="text-right direction-in">${inflow}</td>
            <td class="text-right direction-out">${outflow}</td>
            <td class="text-right ${net_class}">${this.fmt(net)}</td>
        </tr>`;
    }
    html += `</tbody></table>`;

    // Pagination footer
    const start = (r.page - 1) * r.page_size + 1;
    const end = Math.min(r.page * r.page_size, r.total);
    const total_pages = Math.max(1, Math.ceil(r.total / r.page_size));

    let pager = "";
    if (total_pages > 1) {
        pager += `<button class="btn btn-default btn-sm pager-prev" ${r.page <= 1 ? "disabled" : ""}>‹</button>`;
        for (let p = 1; p <= total_pages; p++) {
            pager += `<button class="btn btn-${p === r.page ? "primary" : "default"} btn-sm pager-page" data-page="${p}">${p}</button>`;
        }
        pager += `<button class="btn btn-default btn-sm pager-next" ${r.page >= total_pages ? "disabled" : ""}>›</button>`;
    }

    html += `<div class="detail-footer">
        <span class="text-muted">${__("Showing {0} - {1} of {2} transactions")
            .replace("{0}", start).replace("{1}", end).replace("{2}", r.total)}</span>
        <div class="detail-pager">${pager}</div>
    </div>`;

    $c.html(html);
    this._wire_detail_events($c);
}

_wire_detail_events($c) {
    const self = this;
    // Search debounce
    $c.find(".detail-search-input").on("input", function() {
        const v = $(this).val();
        clearTimeout(self._search_debounce_t);
        self._search_debounce_t = setTimeout(() => {
            self.detail_search = v;
            self.detail_page = 1;
            self._reload_detail_table();
        }, 300);
    });
    // Pager
    $c.find(".pager-prev").on("click", () => {
        if (self.detail_page > 1) { self.detail_page--; self._reload_detail_table(); }
    });
    $c.find(".pager-next").on("click", () => {
        self.detail_page++;
        self._reload_detail_table();
    });
    $c.find(".pager-page").on("click", function() {
        self.detail_page = parseInt($(this).attr("data-page"));
        self._reload_detail_table();
    });
    // Filter chip clear
    $c.find(".chip-clear").on("click", (e) => {
        e.preventDefault();
        self._select_period(null);
    });
}
```

Also update `load_data` so it calls `_reload_detail_table` after main data loads:

Find the `load_data` method (around line 319). After `this.render();`, add:
```javascript
this.detail_page = 1;
this._reload_detail_table();
```

- [ ] **Step 7.2: Add detail table CSS**

Append to `cash_flow_forecast.css`:

```css
/* Detail table */
.forecast-page .detail-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin: 18px 0 8px;
}
.forecast-page .detail-toolbar {
    display: flex;
    gap: 8px;
    align-items: center;
}
.forecast-page .badge-period {
    padding: 4px 8px;
    background: var(--bg-light-blue, #e8f0fe);
    color: var(--primary);
    border-radius: 4px;
    font-size: 11px;
}
.forecast-page .badge-period .chip-clear {
    color: inherit;
    text-decoration: none;
}
.forecast-page .detail-table {
    font-size: 12px;
}
.forecast-page .detail-table .dd-group-header {
    background: var(--bg-light-gray, #f9fafb);
    font-weight: 600;
}
.forecast-page .detail-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 8px;
}
.forecast-page .detail-pager .btn {
    margin-left: 2px;
}
.forecast-page .detail-empty {
    border: 1px dashed var(--border-color);
    border-radius: 6px;
    margin-top: 8px;
}
```

- [ ] **Step 7.3: Build and verify**

```bash
cd /home/long/long/frappe-bench-dcnet
bench build --app vn_accounting && bench clear-cache
```

Refresh browser. Expected:
- Detail table renders below pivot, grouped by Confidence (3-4 sections).
- Each section header has badge + cumulative inflow/outflow + count.
- Pagination at bottom showing "Hiển thị 1 - 20 của 195 giao dịch" + page buttons.
- Search input upper-right; type "abc", wait 300ms, table refetches.
- Click pivot column T05/2026 → chip "📅 2026-05 ✕" appears above table, table filters to entries in T05.
- Click ✕ on chip → period unselected, table shows all.
- Click page 2 button → table refetches page 2.
- Console: 0 errors.

- [ ] **Step 7.4: Commit**

```bash
cd /home/long/long/frappe-bench-dcnet/.worktrees/vn_accounting-cash-flow-ui
git add vn_accounting/vn_accounting/page/cash_flow_forecast/cash_flow_forecast.js \
        vn_accounting/vn_accounting/page/cash_flow_forecast/cash_flow_forecast.css
git commit -m "feat(cash-flow): paginated grouped detail table

Replaces per-row drill-down with bottom flat table grouped by Confidence.
Server-side pagination via get_forecast_entries (page_size=20). Search
input with 300ms debounce. Clicking a pivot column shows a filter chip
above the table; clicking the chip's ✕ clears the period filter.

Group totals shown in section headers come from the FULL filtered set
(not page) so they don't drift across pages."
```

---

## Task 8: Cleanup — remove `get_drilldown_entries` API + dead JS

**Files:**
- Modify: `vn_accounting/api/forecast.py` (remove `get_drilldown_entries`)
- Modify: `vn_accounting/vn_accounting/page/cash_flow_forecast/cash_flow_forecast.js` (remove `_load_drilldown` / `_render_drilldown_page` if any leftover, remove `_create_select` / `_create_multi`, remove `export_excel` placeholder if dead)

- [ ] **Step 8.1: Verify no callers of `get_drilldown_entries`**

```bash
grep -rn "get_drilldown_entries" /home/long/long/frappe-bench-dcnet/apps/vn_accounting/ \
    --include="*.py" --include="*.js"
```

Expected: only the function definition itself in `api/forecast.py`. Any caller would need to be updated; if the only result is the definition, proceed.

- [ ] **Step 8.2: Remove `get_drilldown_entries` from `api/forecast.py`**

Find the `@frappe.whitelist()` block for `get_drilldown_entries` (around line 99–146) and delete the whole function.

- [ ] **Step 8.3: Remove dead JS helper functions**

In `cash_flow_forecast.js`, delete:
- `_create_select(...)` (around line 145–197 in original)
- `_create_multi(...)` (around line 199–260)
- `_load_companies()` (around line 278–285)
- `_load_drilldown(...)` and `_render_drilldown_page(...)` (around line 668+) if any leftover

Run `wc -l cash_flow_forecast.js` to confirm size dropped (target ≤700 lines from original 903).

- [ ] **Step 8.4: Build, verify nothing broken**

```bash
cd /home/long/long/frappe-bench-dcnet
bench build --app vn_accounting && bench clear-cache
```

Refresh browser. Expected: page loads, console 0 errors, all sections (Filter, KPI, Chart, Pivot, Detail) work as in Task 7.

- [ ] **Step 8.5: Commit**

```bash
cd /home/long/long/frappe-bench-dcnet/.worktrees/vn_accounting-cash-flow-ui
git add vn_accounting/api/forecast.py \
        vn_accounting/vn_accounting/page/cash_flow_forecast/cash_flow_forecast.js
git commit -m "refactor(cash-flow): remove deprecated get_drilldown_entries + dead JS

get_drilldown_entries is replaced by get_forecast_entries; no callers
remain. Dead JS factories (_create_select, _create_multi, _load_drilldown,
_load_companies) removed. File size dropped from ~903 to <=700 lines."
```

---

## Task 9: i18n — Add Vietnamese translations

**Files:**
- Modify: `vn_accounting/translations/vi.csv`

- [ ] **Step 9.1: Append new rows to vi.csv**

Open `vn_accounting/translations/vi.csv` and append (do not duplicate existing keys; if a key already exists, skip):

```csv
"Cash Flow Forecast","Dự Báo Dòng Tiền"
"Closing Balance","Số dư cuối kỳ"
"Opening:","Đầu kỳ:"
"Net Cash Flow","Dòng tiền ròng"
"Performance:","Hiệu suất:"
"Total Inflow","Tổng thu vào"
"Total Outflow","Tổng chi ra"
"Avg/period:","TB/kỳ:"
"Actual Balance","Số dư thực tế"
"Forecast Balance","Số dư dự báo"
"Cash Inflow","Dòng tiền vào"
"Cash Outflow","Dòng tiền ra"
"Minimum Threshold (Balance)","Mức tối thiểu (số dư)"
"Summary by month/week","Tóm tắt theo tháng/tuần"
"Forecast Detail Transactions","Chi tiết giao dịch dự báo"
"Search transactions...","Tìm kiếm giao dịch..."
"Showing {0} - {1} of {2} transactions","Hiển thị {0} - {1} của {2} giao dịch"
"By Month","Theo tháng"
"By Week","Theo tuần"
"Forecast Periods","Số kỳ dự báo"
"History Periods","Số kỳ quá khứ"
"Inflow Sources","Nguồn thu"
"Outflow Sources","Nguồn chi"
"Refresh (clear cache)","Làm mới (xóa cache)"
"Excel","Xuất Excel"
"Type","Loại giao dịch"
"Description","Mô tả"
"Status","Trạng thái"
"Expected Date","Ngày dự kiến"
"Reference","Tham chiếu"
"Party","Đối tác"
"Net","Thuần"
"Total","Tổng"
"entries","giao dịch"
"No transactions","Không có giao dịch"
"No transactions in {0}","Không có giao dịch trong {0}"
"Metric","Chỉ tiêu"
"Granularity","Theo"
```

- [ ] **Step 9.2: Apply translations**

```bash
cd /home/long/long/frappe-bench-dcnet
bench --site dcnet.localhost clear-cache
```

- [ ] **Step 9.3: Verify on Vietnamese site**

Refresh `http://dcnet.localhost:8001/app/cash-flow-forecast`. Expected: all visible strings render in Vietnamese (the user's site language is `vi`). Specifically check: KPI labels, pivot row headers (Số dư đầu kỳ etc.), detail column headers (Mô tả, Đối tác, Thuần), search placeholder, "Hiển thị X - Y của Z giao dịch".

- [ ] **Step 9.4: Commit**

```bash
cd /home/long/long/frappe-bench-dcnet/.worktrees/vn_accounting-cash-flow-ui
git add vn_accounting/translations/vi.csv
git commit -m "i18n(cash-flow): add Vietnamese translations for redesigned UI"
```

---

## Task 10: Final verification + branch wrap

- [ ] **Step 10.1: Run all unit tests**

```bash
cd /home/long/long/frappe-bench-dcnet
./env/bin/python -m unittest \
    apps/vn_accounting/vn_accounting/api/test_forecast_entries.py \
    apps/vn_accounting/vn_accounting/forecast/test_aggregator.py \
    -v
```

Expected: all PASS.

- [ ] **Step 10.2: Manual UI smoke test (browser)**

Open `http://dcnet.localhost:8001/app/cash-flow-forecast`. Verify the §15 list from the spec:

- Filter row (7 fields) visible inline at 1440px viewport
- 4 KPI cards side-by-side
- Chart shows 4 lines, Actual solid + Forecast (after Hiện tại marker)
- Pivot 4 rows × 12 columns (or 13 with current period); first column sticky-left
- Click T05 column → highlight + detail filters
- Detail grouped by Confidence with 3-4 section headers
- Search debounces, pagination works
- Page menu (...) has Methodology / Settings / Refresh; secondary action = Excel
- Console: 0 errors

- [ ] **Step 10.3: Performance check**

In browser DevTools Network tab:
- Cold load `/api/method/vn_accounting.api.forecast.get_forecast_data`: ≤1s
- Click pivot column (cache hit): ≤200ms for `get_forecast_entries`
- Pagination click: ≤200ms

- [ ] **Step 10.4: Push branch**

```bash
cd /home/long/long/frappe-bench-dcnet/.worktrees/vn_accounting-cash-flow-ui
git push -u goldrag1 feat/cash-flow-forecast-ui-redesign
```

- [ ] **Step 10.5: Final summary commit (if needed) and report**

If any small fixes were made during smoke tests, commit them. Otherwise:

```bash
git log --oneline main..HEAD
```

Should show ~10 atomic commits, one per task.

Report ready for merge: PR or direct merge to main per project policy.

---

## Self-Review

### Spec coverage check

| Spec section | Covered by |
|---|---|
| §1 Goal / §3 D1–D10 | All tasks 3–7 cover the 10 decisions |
| §4 Layout (padding) | Task 3.4 CSS adds `.forecast-content { padding: 0 20px }` |
| §5 Filter row (Frappe-native) | Task 3 (full rewrite via `page.add_field`) |
| §6 KPI cards | Task 4 |
| §7 Chart 4 lines | Task 5 |
| §8 Pivot table | Task 6 |
| §9 Detail table | Task 7 |
| §10 API (new endpoint, removed endpoint, cache) | Tasks 1, 2 (new); 8 (remove) |
| §11 Files affected | Tasks 1–9 cover them; aggregator.py untouched as planned |
| §12 i18n | Task 9 |
| §13 Edge cases (empty, Inflow=0, period_key+granularity, historical no-op, provider error, search no result, cache shared) | All wired in code shown in tasks 4 (Inflow=0 → "—"), 6 (historical no-op), 7 (empty + chip), 2 (cache reuse) |
| §14 Out of scope | None of the tasks touch out-of-scope items |
| §15 Verification plan | Task 10 mirrors §15 |

No gaps.

### Placeholder scan

No "TBD", "TODO", "implement later", "fill in details", "similar to Task N" patterns. Each step has actual code or actual command with expected output.

### Type / signature consistency

| Symbol | Where defined | Where used |
|---|---|---|
| `CONFIDENCE_ORDER` | Task 1.3 (forecast.py) | Task 1 tests, Task 2 sort, Task 7 detail rendering (via API response) |
| `_filter_entries(entries, *, period_key, granularity, confidences, sources, search)` | Task 1.3 | Task 1 tests, Task 2 endpoint |
| `_compute_group_totals(entries)` | Task 1.3 | Task 1 tests, Task 2 endpoint |
| `_load_entries_with_cache(company, from_date, to_date)` | Task 2.1 | Task 2.2 endpoint |
| `get_forecast_entries(company, from_date, to_date, granularity, period_key, confidences, sources, search, page, page_size)` | Task 2.2 | Task 7 JS call (`_reload_detail_table`) |
| `this.filters.{granularity, period, history, company, confidence, inflow_sources, outflow_sources}` | Task 3.2 setup_page | Task 3.3 update_source_dropdowns, Task 4–7 nothing else needed |
| `this.selected_period` | Task 3.2 constructor | Task 6 select_period, Task 7 _reload_detail_table |
| `this.detail_search`, `this.detail_page`, `this.detail_page_size` | Task 3.2 constructor | Task 7 wire_detail_events |
| `this.$pivot` | Task 6.1 render_table | Task 6.1 _select_period |
| `_select_period(period_key)` | Task 6.1 | Task 6.1 click handler, Task 7 chip clear |
| `_reload_detail_table()` | Task 7.1 | Task 3 (filter changes), Task 6 (_select_period), Task 7 (search/pager) |
| `_render_detail(r)` | Task 7.1 | Task 7.1 _reload_detail_table |
| `_wire_detail_events($c)` | Task 7.1 | Task 7.1 _render_detail |
| `_get_source_label(src)`, `_get_source_tooltip(src)` | unchanged from existing code | Task 3.3 source dropdowns, Task 7 detail render |

All names consistent.

### Risks acknowledged in spec, surfaced in plan

- **MultiCheck inline render width** (Task 3.5): plan explicitly instructs fallback to MultiSelect if too tall, document in commit.
- **4-line chart null-gap behavior** (Task 5.3): plan instructs fallback to single Balance dataset + clip-path if frappe.Chart connects across nulls.

No further changes needed. Plan ready for execution.

---

## Execution Handoff

Plan complete and saved to `docs/plans/2026-04-28-cash-flow-forecast-ui-redesign.md`. Two execution options:

**1. Subagent-Driven (recommended)** — I dispatch a fresh subagent per task, review between tasks, fast iteration.

**2. Inline Execution** — Execute tasks in this session using executing-plans, batch execution with checkpoints.

Which approach?
