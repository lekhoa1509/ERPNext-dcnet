---
project: apps/vn_accounting
base_branch: main
---

# Cash Flow Forecast — Design Spec

> **Feature:** Dự báo dòng tiền (Cash Flow Forecast)
> **App:** vn_accounting (core + ERPNext providers) + dcnet_contract, dcnet_pakd (external providers)
> **Date:** 2026-04-20
> **Status:** Draft

## 1. Problem Statement

DCNET has future cash inflows from contracts (dcnet_contract), outflows from business plan commissions (dcnet_pakd), treasury instruments (term deposits, bank loans), and standard ERPNext sales/purchase pipeline. Currently no way to see a consolidated forward-looking cash position.

**Users:**
- **Accountant** — needs detailed drill-down to plan payments, ensure sufficient cash
- **Management (BGĐ)** — needs dashboard overview of projected cash position 3-12 months ahead

**Key requirements:**
1. App-agnostic — any installed app can contribute forecast data via hooks
2. Lifecycle-aware — no double-counting across Quotation → SO → SI → PE pipeline
3. Interactive UI — toggle sources, confidence levels, granularity in one page
4. Historical projection — forecast recurring operating expenses based on past patterns

## 2. Architecture: Hook-Based Provider System

### 2.1 Hook Key

Each app registers forecast providers via Frappe's hook mechanism:

```python
# any_app/hooks.py
cash_flow_forecast_providers = [
    "any_app.forecast.get_my_forecast"
]
```

vn_accounting discovers all providers at runtime:

```python
providers = frappe.get_hooks("cash_flow_forecast_providers")
# Returns merged list from ALL installed apps
```

> **Why hook-based (pull) instead of shared DocType (push):** Data is always realtime — no sync needed when source documents are cancelled/revised. Each app manages its own query logic. Zero coupling between apps.

### 2.2 Provider Function Contract

Every provider function MUST conform to this interface:

```python
def get_forecast(filters: dict) -> list[dict]:
    """
    Args:
        filters: {
            "company": str,          # REQUIRED — only return items for this company
            "from_date": str,        # REQUIRED — ISO YYYY-MM-DD, only expected_date >= this
            "to_date": str,          # REQUIRED — ISO YYYY-MM-DD, only expected_date <= this
            "confidence": list[str], # OPTIONAL — if present, filter by these levels.
                                     # If absent, return ALL confidence levels.
                                     # The page UI fetches without confidence filter
                                     # and filters client-side for instant toggling.
        }

    Returns:
        list of ForecastEntry dicts. Each entry represents ONE expected cash movement.
    """
```

### 2.3 ForecastEntry Schema

| Field | Type | Required | Constraints |
|-------|------|----------|------------|
| `expected_date` | str | ✅ | ISO YYYY-MM-DD. The date cash is expected to move. |
| `amount` | float | ✅ | Always positive, > 0. VND only (provider converts if needed). |
| `direction` | str | ✅ | `"inflow"` or `"outflow"` |
| `category` | str | ✅ | Non-empty. App-defined label (e.g. "Contract Service", "Sales Invoice Receivable"). |
| `confidence` | str | ✅ | `"overdue"` / `"committed"` / `"probable"` / `"possible"` |
| `source_doctype` | str | ✅ | DocType name for drill-down link |
| `source_name` | str | ✅ | Document name for drill-down link |
| `party_type` | str | — | `"Customer"` / `"Supplier"` / `"Employee"` / None |
| `party` | str | — | Party name or None |
| `description` | str | — | Short description or None |

### 2.4 Confidence Levels

| Level | Definition | Examples |
|-------|-----------|---------|
| `overdue` | Past due_date, payment not yet received | SI overdue (due_date < today, outstanding > 0), PI overdue |
| `committed` | Legally binding, not yet due | Signed contract (future due_date), approved PAKD, unpaid SI (due_date >= today), deposit interest |
| `probable` | High likelihood, not yet finalized | Sales Order, Purchase Order, PAKD pending approval, Payroll Entry draft |
| `possible` | Estimate or forecast | Quotation (open), projected OpEx, projected tax, projected payroll |

> **Why separate `overdue`:** CFO needs to see how much cash is "stuck" (overdue receivables) vs expected on schedule (committed). Overdue amount is a financial health indicator — high overdue ratio signals collection problems. In the UI, overdue entries render with a distinct red badge.

### 2.5 Provider Rules (Developer Guidelines)

1. **Lifecycle-aware: only return items at their CURRENT stage.** Each document type represents one stage in a lifecycle (Quotation → SO → SI → PE). A provider must exclude documents that have already progressed to the next stage. See §2.8 for details.
2. **Amount always positive.** `direction` determines inflow/outflow. Negative amounts are rejected.
3. **One entry per cash movement.** Do not aggregate — 5 billing rows = 5 entries. Aggregation happens in the aggregator.
4. **`expected_date` = when cash moves, not when document was created.** Use due_date, delivery_date, maturity_date — not posting_date or creation.
5. **Idempotent.** Calling the function twice with same filters returns identical results.
6. **Currency: VND only.** Provider must convert foreign currency amounts before returning.
7. **Respect ALL filters.** Provider MUST filter by company, from_date, to_date. The `confidence` filter is OPTIONAL — if absent, return ALL confidence levels (page UI needs all levels for client-side toggling). If present, filter server-side.
8. **Performance.** Target < 1 second for typical data volumes (< 5,000 entries). Index date fields used in queries.

### 2.6 Aggregator (vn_accounting core)

**File:** `vn_accounting/forecast/aggregator.py`

```python
def get_all_forecast_entries(filters):
    """Collect forecast entries from all registered providers.

    Returns:
        (entries: list[dict], errors: list[dict])
        errors = [{"provider": str, "error": str}, ...]
    """
    entries = []
    errors = []
    for method_path in frappe.get_hooks("cash_flow_forecast_providers"):
        try:
            fn = frappe.get_attr(method_path)
            raw = fn(filters)
            for entry in raw:
                validated = validate_entry(entry, method_path)
                if validated:
                    entries.append(validated)
        except Exception as e:
            errors.append({"provider": method_path, "error": str(e)})
            frappe.log_error(f"Cash flow provider failed: {method_path}", str(e))
    return entries, errors
```

**Error isolation:** One provider crashing does NOT break the entire forecast. The UI shows a warning banner listing failed providers.

**Validation** (`validate_entry()`): Each entry validated against §2.3 schema:
- All required fields present and correct type
- `amount` > 0
- `direction` in ("inflow", "outflow")
- `confidence` in ("overdue", "committed", "probable", "possible")
- `expected_date` parseable as YYYY-MM-DD

Invalid entries are logged to Error Log (with provider path and field-level errors) and skipped. Valid entries from the same provider are still included.

### 2.7 Provider Template (for new app developers)

```python
# my_app/forecast.py
import frappe

def get_my_app_forecast(filters):
    """Cash flow forecast provider for My App.

    Provider contract: see vn_accounting docs/specs/2026-04-20-cash-flow-forecast-design.md §2

    Rules:
    - Only return items at their current lifecycle stage (§2.8)
    - Amount in VND, always positive
    - Respect all filters: company, from_date, to_date, confidence
    """
    company = filters.get("company")
    from_date = filters.get("from_date")
    to_date = filters.get("to_date")
    confidence_filter = filters.get("confidence", ["committed", "probable", "possible"])

    if not company or not from_date or not to_date:
        return []

    entries = []
    rows = frappe.get_all("My Future Payment", filters={
        "company": company,
        "expected_date": ["between", [from_date, to_date]],
        "status": "Pending",
    }, fields=["name", "expected_date", "amount", "party", "description"])

    for row in rows:
        confidence = "committed"
        if confidence not in confidence_filter:
            continue
        entries.append({
            "expected_date": str(row.expected_date),
            "amount": float(row.amount),
            "direction": "outflow",
            "category": "My App Payment",
            "confidence": confidence,
            "party_type": "Supplier",
            "party": row.party,
            "source_doctype": "My Future Payment",
            "source_name": row.name,
            "description": row.description,
        })
    return entries
```

```python
# my_app/hooks.py
cash_flow_forecast_providers = [
    "my_app.forecast.get_my_app_forecast"
]
```

### 2.8 Lifecycle-Aware Double-Counting Prevention

ERPNext documents follow a lifecycle: Quotation → Sales Order → Sales Invoice → Payment Entry (sales side) and Purchase Order → Purchase Invoice → Payment Entry (purchase side). Each stage is a different provider with a different confidence level.

**Rule: each provider only returns documents that have NOT progressed to the next stage.**

```
SALES LIFECYCLE (inflow):
  Quotation (possible)
    └→ SO created → Quotation.status != "Open" → excluded by Quotation provider
  Sales Order (probable)
    └→ SI created → SO.per_billed = 100 → excluded by SO provider
  Sales Invoice unpaid (committed)
    └→ PE created → SI.outstanding_amount = 0 → excluded by SI provider
  Payment Entry = already in GL → no provider needed

PURCHASE LIFECYCLE (outflow):
  Purchase Order (probable)
    └→ PI created → PO.per_billed = 100 → excluded by PO provider
  Purchase Invoice unpaid (committed)
    └→ PE created → PI.outstanding_amount = 0 → excluded by PI provider
  Payment Entry = already in GL → no provider needed
```

Each provider naturally excludes progressed documents via its own status/amount filters. No cross-provider coordination needed. Users can safely enable all providers without double-counting.

**DCNET-specific lifecycle (parallel, non-overlapping with ERPNext):**
- Contract billing schedule (Projected) → becomes Invoiced when SI created → contract provider excludes
- PAKD commission lines (Pending) → becomes Posted when JE/AS created → PAKD provider excludes
- Treasury schedule rows → linked JE created → treasury provider excludes

These are independent lifecycles from ERPNext's Quotation→SO→SI chain.

## 3. UI: Custom Frappe Page

### 3.1 Page Metadata

- **Page name:** `cash-flow-forecast`
- **Route:** `/desk/cash-flow-forecast`
- **Title:** "Cash Flow Forecast" (vi: "Dự Báo Dòng Tiền")
- **Type:** Custom Frappe Page (vanilla JS + Chart.js), same pattern as Dashboard v2

> **Why Custom Page instead of Script Report:** Need combined chart + data table + interactive source toggles + confidence checkboxes in one view. Script Report is too limited for this UX.

### 3.2 Page Layout

```
┌──────────────────────────────────────────────────────────────┐
│  Dự Báo Dòng Tiền                                    [Export]│
├──────────────────────────────────────────────────────────────┤
│  Company: [DCNET ▾]  Period: [12 Months ▾]  Gran: [Monthly ▾]│
├──────────────────────────────────────────────────────────────┤
│  Confidence:  ☑ Committed  ☐ Probable  ☐ Possible            │
├──────────────────────────────────────────────────────────────┤
│  Sources:                                                     │
│  ☑ Sales Invoice    ☑ Contract Revenue   ☑ Deposit Interest  │
│  ☑ Purchase Invoice ☑ PAKD Commission    ☑ Loan Repayment   │
│  ☐ Sales Order      ☐ Quotation          ☐ Projected OpEx   │
│  ☐ Purchase Order                                            │
│  ⚠ [Provider X failed: connection error]  (warning if any)  │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  ██ ██ ██ ██ ██ ██ ██ ██ ██ ██ ██ ██   ← Bar chart          │
│  ── ── ── ── ── ── ── ── ── ── ── ──   ← Balance line       │
│  T5  T6  T7  T8  T9 T10 T11 T12  T1  T2  T3  T4            │
│                                                               │
├──────────────────────────────────────────────────────────────┤
│  Period  │ Opening │ Inflow  │ Outflow │  Net   │ Closing   │
│──────────┼─────────┼─────────┼─────────┼────────┼───────────│
│  T5/2026 │  500M   │  280M   │   95M   │ +185M  │   685M    │
│    ▸ details (click to expand)                               │
│  T6/2026 │  685M   │  340M   │  110M   │ +230M  │   915M    │
│    ▸ details                                                 │
│  ...                                                         │
│  T3/2027 │  2.1B   │  175M   │   75M   │ +100M  │   2.2B    │
│  T4/2027 │  2.2B   │  175M   │   75M   │ +100M  │   2.3B    │
└──────────────────────────────────────────────────────────────┘
```

### 3.3 Filter Controls

| Control | Type | Default | Behavior |
|---------|------|---------|----------|
| Company | Frappe Link dropdown | Default company | Reload all data on change |
| Period | Select: 3/6/12 months | 12 Months | Recalculate to_date, refetch |
| Granularity | Select: Monthly/Weekly | Monthly | Re-group existing data (no refetch) |
| Confidence | Checkbox group | [Committed] checked | Re-filter existing data (no refetch) |
| Sources | Checkbox group (dynamic) | All "committed" sources checked | Re-filter existing data (no refetch) |

**Performance note:** Company/Period changes trigger API refetch (aggregator called without confidence filter → returns ALL entries). Confidence/Sources/Granularity changes only re-filter and re-group data already in browser — instant response, no API call.

**UX hint for filter mismatch:** When user enables a source whose entries are all at a confidence level not currently checked, show a subtle tooltip: e.g., enabling "Sales Order" while only "Committed" is checked → tooltip "Sales Order entries require 'Probable' confidence — check it to see them". No auto-toggling — user decides.

### 3.4 Chart

- **Type:** Bar chart (Chart.js) + Line overlay
- **Bar datasets:** Inflow (green, #28a745) + Outflow (red, #dc3545) per period
- **Line dataset:** Projected Closing Balance (dark blue, #0056b3, dashed)
- **Dashed line** distinguishes forecast from historical charts (solid) on Dashboard v2
- **Y-axis:** Abbreviated notation (1M, 500K) matching Dashboard v2 style
- **Hover tooltip:** Period, Inflow total, Outflow total, Net, Closing Balance

### 3.5 Data Table

**Summary rows (grouped by period):**

| Column | Description |
|--------|------------|
| Period | "T5/2026" (monthly) or "W20/2026" (weekly) |
| Opening Balance | Cash position at start of period |
| Inflow | Sum of all inflow entries in period |
| Outflow | Sum of all outflow entries in period |
| Net | Inflow − Outflow |
| Closing Balance | Opening + Net |

**Rule:** First period's Opening Balance = current GL balance of TK 111 (cash) + TK 112 (bank) + TK 113 (cash in transit) — reuse `_balance_gl` from Dashboard v2 API with expanded account pattern

> **Why include TK 113:** Cash in transit (tiền đang chuyển) represents money already sent from one bank to another, or cash being deposited. For an ISP collecting from multiple agents/channels, TK 113 can hold 100-500M at month-end. Excluding it underestimates the actual cash position and may trigger false shortfall warnings.. Each subsequent period's Opening = previous period's Closing (rolling).

**Visual warnings (3 tiers):**
- Closing Balance < 0 → row highlighted **red** (cash shortfall — need to borrow or defer payments)
- Closing Balance < minimum threshold → row highlighted **yellow** (approaching danger zone)
- Closing Balance healthy → normal

**Minimum cash threshold:** Configurable in VN Accounting Settings (default 500,000,000 VND = 500M). This is the minimum operating cash a company needs to maintain. The chart renders this as a horizontal dashed line. CFO's key question answered: "tháng nào cần vay ngắn hạn?"

### 3.6 Drill-Down

Click a period row → expand to show individual entries:

| Sub-column | Description |
|------------|------------|
| Date | expected_date |
| Direction | ↑ Inflow / ↓ Outflow (icon + color) |
| Amount | Formatted VND |
| Category | From provider |
| Confidence | Badge: committed(green) / probable(yellow) / possible(gray) |
| Party | party_type + party name |
| Source | Link to source_doctype/source_name (clickable, opens in new tab) |
| Description | Short text |

### 3.7 Export

Export button generates Excel with:
- Sheet 1: Summary (period rows with Opening/Inflow/Outflow/Net/Closing)
- Sheet 2: Detail (all individual entries, flat table)

## 4. Dashboard v2 Integration

### 4.1 Chart on Dashboard

Add a forecast chart to the existing Dashboard v2 page (`/desk/vn-accounting-dashboard`):

- **Position:** After the existing "Dòng Tiền" (historical cash flow) chart
- **Type:** Same as §3.4 but simplified — committed only, monthly, 12 months
- **Click:** Opens full forecast page (`/desk/cash-flow-forecast`)

### 4.2 API Endpoint

```python
@frappe.whitelist()
def get_cash_flow_forecast_chart(company=None, months=12):
    """Returns chart datasets for Dashboard v2.
    Calls aggregator with confidence=["committed"], groups by month.
    """
```

Reuses the same `get_all_forecast_entries()` aggregator — no duplicate logic.

## 5. Provider Implementations

### 5.1 vn_accounting — Treasury Provider

**File:** `vn_accounting/forecast/treasury.py`

**Hook registration:**
```python
# vn_accounting/hooks.py (add to existing)
cash_flow_forecast_providers = [
    # Treasury
    "vn_accounting.forecast.treasury.get_treasury_forecast",
    # ERPNext pipeline
    "vn_accounting.forecast.erpnext_providers.get_quotation_forecast",
    "vn_accounting.forecast.erpnext_providers.get_sales_order_forecast",
    "vn_accounting.forecast.erpnext_providers.get_purchase_order_forecast",
    "vn_accounting.forecast.erpnext_providers.get_unpaid_si_forecast",
    "vn_accounting.forecast.erpnext_providers.get_unpaid_pi_forecast",
    # Payroll (HRMS)
    "vn_accounting.forecast.payroll_provider.get_payroll_forecast",
    # Tax obligations
    "vn_accounting.forecast.tax_provider.get_tax_forecast",
    # Historical projection
    "vn_accounting.forecast.historical_projection.get_opex_forecast",
]
```

**Treasury data sources:**

| Source | Direction | Category | Condition for inclusion |
|--------|-----------|----------|----------------------|
| Term Deposit interest schedule | inflow | "Deposit Interest" | Schedule row has no linked JE |
| Term Deposit principal maturity | inflow | "Deposit Maturity" | Deposit status != Matured |
| Bank Loan repayment schedule | outflow | "Loan Repayment" | Schedule row has no linked JE |
| Bank Loan interest schedule | outflow | "Loan Interest" | Schedule row has no linked JE |

All confidence = "committed" (contractual obligations with banks).

### 5.2 vn_accounting — ERPNext Pipeline Providers

**File:** `vn_accounting/forecast/erpnext_providers.py`

#### expected_date Strategy per DocType

| DocType | expected_date source | Fallback |
|---------|---------------------|----------|
| Quotation | `valid_till` | `transaction_date + 30 days` |
| Sales Order | `Payment Schedule.due_date` (if exists) | `transaction_date + 30 days` |
| Purchase Order | `Payment Schedule.due_date` (if exists) | earliest item `schedule_date + 30 days` |
| Sales Invoice | `due_date` (header field) | `posting_date + 30 days` |
| Purchase Invoice | `due_date` (header field) | `posting_date + 30 days` |

> **Why +30 days as fallback:** Standard Vietnamese B2B payment terms are 30 days. This is a reasonable default when no explicit due date is set.

### 5.2a Payment Delay Factor (Realistic Date Adjustment)

Vietnamese B2B payments are often late. The +30 day fallback and even explicit `due_date` values are **optimistic**. Real payment behavior varies significantly by customer:

- Telecom giants (VNPT, Viettel, FPT): typically 45-60 days, sometimes 90
- Government agencies: 60-90 days, up to 120
- Mid-size enterprises: 30-45 days

**Solution:** Calculate a per-Customer/Customer Group `payment_delay_days` from historical Payment Entry data:

```python
def get_payment_delay(customer, company):
    """Calculate average days late for a customer.
    delay = PE.posting_date - SI.due_date for all paid SIs in last 12 months.
    Returns: median delay in days (0 if on-time or no history).
    """
    delays = frappe.db.sql("""
        SELECT DATEDIFF(pe.posting_date, si.due_date) as delay
        FROM `tabPayment Entry Reference` per
        JOIN `tabPayment Entry` pe ON pe.name = per.parent
        JOIN `tabSales Invoice` si ON si.name = per.reference_name
        WHERE per.reference_doctype = 'Sales Invoice'
          AND pe.party = %(customer)s AND pe.company = %(company)s
          AND pe.docstatus = 1 AND pe.posting_date >= DATE_SUB(CURDATE(), INTERVAL 12 MONTH)
    """, {"customer": customer, "company": company})
    if not delays:
        return 0
    values = sorted([d.delay for d in delays])
    return values[len(values) // 2]  # median
```

**Providers that apply delay factor:** Unpaid SI, Contract billing (inflow providers where customer is known). The delay shifts `expected_date` forward:

```python
expected_date = due_date + timedelta(days=get_payment_delay(customer, company))
```

**Outflow providers:** Do NOT apply delay factor — company controls its own payment timing. Use due_date as-is.

> **Caching:** Payment delay is computed once per API call (per customer), cached in a dict. Not stored in DB — recalculated fresh each time to reflect latest payment patterns.

#### Quotation Provider (inflow, possible)

```python
def get_quotation_forecast(filters):
    """Open quotations not yet converted to Sales Order."""
    # Filters: status='Open', valid_till >= from_date OR valid_till is NULL
    # Note: Quotation has NO per_ordered field. Use status='Open' to exclude
    #   quotations already converted to SO (status becomes 'Ordered').
    # expected_date = valid_till or transaction_date + 30 days
    # amount = grand_total (tax-inclusive)
```

#### Sales Order Provider (inflow, probable)

```python
def get_sales_order_forecast(filters):
    """Submitted SOs not yet fully billed."""
    # Filters: docstatus=1, per_billed < 100, status not in (Closed, Cancelled)
    # amount = grand_total * (100 - per_billed) / 100  (remaining unbilled portion)
    # expected_date strategy:
    #   1. If Payment Schedule child table exists → use due_date from first unpaid row
    #   2. Fallback: transaction_date + 30 days
    # Note: SO has per_billed (percentage) but NOT billed_amount as a direct field.
    #   Calculate remaining from grand_total and per_billed.
```

#### Purchase Order Provider (outflow, probable)

```python
def get_purchase_order_forecast(filters):
    """Submitted POs not yet fully billed."""
    # Filters: docstatus=1, per_billed < 100, status not in (Closed, Cancelled)
    # amount = grand_total * (100 - per_billed) / 100
    # expected_date strategy:
    #   1. If Payment Schedule child table exists → use due_date from first unpaid row
    #   2. Fallback: earliest item schedule_date + 30 days
    # Note: schedule_date is DELIVERY date, not payment date.
    #   Adding 30 days estimates when payment is due after goods received.
```

#### Unpaid Sales Invoice Provider (inflow, committed)

```python
def get_unpaid_si_forecast(filters):
    """Submitted SIs with outstanding balance."""
    # Filters: docstatus=1, outstanding_amount > 0, is_return=0
    # amount = outstanding_amount (already accounts for partial payments)
    # expected_date = due_date (header field, set by payment terms)
    # Fallback if due_date is NULL: posting_date + 30 days
```

#### Unpaid Purchase Invoice Provider (outflow, committed)

```python
def get_unpaid_pi_forecast(filters):
    """Submitted PIs with outstanding balance."""
    # Filters: docstatus=1, outstanding_amount > 0, is_return=0
    # amount = outstanding_amount
    # expected_date = due_date (header field)
    # Fallback if due_date is NULL: posting_date + 30 days
```

### 5.3 vn_accounting — Historical Operating Expense Projection

**File:** `vn_accounting/forecast/historical_projection.py`

**Concept:** Analyze GL entries from the past 12 months to identify recurring operating expenses (rent, utilities, internet), then project forward using same-month-last-year when available.

```python
def get_opex_forecast(filters):
    """Project recurring operating expenses based on 12-month history.

    Algorithm:
    1. Query GL entries for expense accounts (TK 6xx) in past 12 months
    2. Group by account + month → get monthly series per account
    3. For each account:
       - If appears in >= 8 of 12 months → classified as "recurring"
       - If < 12 months history available: fallback to 6-month window, threshold >= 4 of 6
       - If < 2 months history: skip entirely
    4. Projection method per account:
       - If 12 months available → use SAME-MONTH-LAST-YEAR amount (captures seasonality)
       - Fallback → median of available months
    5. Each projected month = 1 entry per recurring account
    """
```

> **Why 12 months instead of 6:** ISP/DC companies have seasonal patterns — Q4 chi nhiều hơn (bonus, license renewal cuối năm), Q1 thu ít hơn (sau Tết). 6-month window misses these patterns entirely. Same-month-last-year is the gold standard for recurring expense projection.

**Output:**
- direction = "outflow"
- confidence = "possible"
- category = "Projected OpEx: {account_name}" (e.g. "Projected OpEx: 6271 - Chi phí thuê văn phòng")
- source_doctype = "Account", source_name = account name
- party = None (aggregated, not per-vendor)

**Heuristic details:**
- **Recurring threshold:** >= 8 of 12 months (or >= 4 of 6 with short history). Catches monthly expenses while excluding one-offs.
- **Same-month-last-year priority:** If projecting T12/2026, use actual T12/2025 amount. Accounts for year-end spikes (bonus, license renewals). Fallback to median if same-month data unavailable.
- **Amount = median as fallback (not mean):** Robust to outlier months.
- **Excluded accounts:** salary-related (TK 642x with account_type containing "Payroll") — handled by dedicated Payroll provider (§5.3a).
- **Cap:** If projected monthly exceeds 2× median, cap at median. Prevents outlier inflation.

### 5.3a vn_accounting — Payroll Provider

**File:** `vn_accounting/forecast/payroll_provider.py`

**Concept:** Project future payroll obligations (lương + BHXH + BHYT + TNCN). Payroll is typically 25-30% of total operating expenses for ISP/DC companies — too large to omit.

```python
def get_payroll_forecast(filters):
    """Project future payroll from HRMS data or GL history.

    Strategy (in priority order):
    1. If HRMS installed + Payroll Entry exists for recent months:
       → Use last submitted Payroll Entry's total as baseline
       → Project forward monthly (payroll is highly predictable)
    2. Fallback: Query GL entries for payroll accounts (TK 334, 3383, 3384, 3386)
       in past 3 months, take median, project forward
    """
```

**Output:**
- direction = "outflow"
- confidence = "probable" (if from recent Payroll Entry) or "possible" (if from GL history)
- category = "Payroll" (salary) / "Social Insurance" (BHXH/BHYT/BHTN)
- expected_date = 5th of each month (typical VN salary payment date) for salary, 20th for insurance contributions
- source_doctype = "Payroll Entry" (if HRMS) or "Account" (if GL fallback)

**HRMS detection:** `"hrms" in frappe.get_installed_apps()`. If HRMS not installed → GL fallback only.

### 5.3b vn_accounting — Tax Obligations Provider

**File:** `vn_accounting/forecast/tax_provider.py`

**Concept:** Project periodic tax payments based on recent tax liability.

```python
def get_tax_forecast(filters):
    """Project future tax obligations from GL history.

    Tax types and schedules (Vietnamese tax calendar):
    1. VAT (GTGT) — monthly, due 20th of following month
       → Query TK 33311 (VAT payable) credit balance last 3 months
       → Project median forward, expected_date = 20th of each month
    2. CIT (TNDN) — quarterly provisional, due 30th of first month of next quarter
       → Query TK 3334 (CIT payable) balance last quarter
       → Project 25% of last year's CIT annually ÷ 4
       → expected_date = Jan 30, Apr 30, Jul 30, Oct 30
    3. PIT (TNCN) — monthly, due 20th of following month
       → Query TK 3335 balance, project forward
    """
```

**Output:**
- direction = "outflow"
- confidence = "possible" (projected from history, actual amount varies)
- category = "VAT Payment" / "Corporate Income Tax" / "Personal Income Tax"
- expected_date = Vietnamese tax calendar dates (20th monthly for VAT/PIT, 30th quarterly for CIT)
- source_doctype = "Account", source_name = tax account name

### 5.4 dcnet_contract — Contract Revenue Provider

**File:** `apps/dcnet_contract/dcnet_contract/forecast.py`

**Hook registration:**
```python
# dcnet_contract/hooks.py (add to existing)
cash_flow_forecast_providers = [
    "dcnet_contract.forecast.get_contract_forecast"
]
# File location: apps/dcnet_contract/dcnet_contract/forecast.py
```

**Inclusion criteria:**

| Contract status | Billing state | Include? | Confidence |
|----------------|--------------|---------|------------|
| Active | Projected | ✅ | committed |
| Suspended | Projected | ✅ | committed (debt still owed) |
| Draft (docstatus=0) | — | ❌ | — |
| Invoiced | — | ❌ | Already in GL |
| Paid | — | ❌ | Already in GL |
| Cancelled | — | ❌ | No obligation |

**Query:** JOIN `tabDCNET Contract Billing Schedule` (bs.state='Projected', bs.due_date in range) with `tabDCNET Contract` (c.status IN ('Active','Suspended'), c.docstatus=1, c.company=filter).

**Output fields:**
- `expected_date` = bs.due_date
- `amount` = bs.amount
- `direction` = "inflow"
- `category` = "Contract Setup Fee" or "Contract Service" (from bs.item_type)
- `party_type` = "Customer", `party` = c.customer

### 5.5 dcnet_pakd — Commission Outflow Provider

**File:** `apps/dcnet_pakd/dcnet_pakd/forecast.py`

**Hook registration:**
```python
# dcnet_pakd/hooks.py (add to existing)
cash_flow_forecast_providers = [
    "dcnet_pakd.forecast.get_pakd_forecast"
]
# File location: apps/dcnet_pakd/dcnet_pakd/forecast.py
```

**Inclusion criteria:**

| PAKD workflow_state | Commission line state | Include? | Confidence |
|--------------------|----------------------|---------|------------|
| Approved | Pending | ✅ | committed |
| Pending GĐ TT KD / Pending P. Tổng hợp / Pending GĐ CN / Pending BGĐ | Pending | ✅ | probable |
| Draft | — | ❌ | — |
| Rejected | — | ❌ | — |
| Any | Posted | ❌ | Already in GL |
| Any | Cancelled | ❌ | — |

**Note on expected_date:** PAKD Commission Line has no date field — only `billing_schedule_idx`. Provider must JOIN back to `tabDCNET Contract Billing Schedule` via contract_ref to get `due_date`. This is acceptable because dcnet_pakd already depends on dcnet_contract (contract_ref is a Link field).

**Note on company filter:** `Phuong An Kinh Doanh` does NOT have a `company` field directly. The query MUST filter company via the joined DCNET Contract table (`c.company = %(company)s`), not via the PAKD table.

**Output fields:**
- `expected_date` = billing schedule's due_date
- `amount` = cl.amount
- `direction` = "outflow"
- `category` = "PAKD {component}" (e.g. "PAKD Manager Services", "PAKD Sales Commission", "PAKD Add Costs", "PAKD License Fee")
- `party_type` = "Employee", `party` = p.sales_person

## 6. Edge Cases

### 6.1 Business Edge Cases

| Scenario | Expected behavior |
|----------|------------------|
| Contract cancelled mid-term | Contract provider returns 0 rows (billing state → Cancelled) |
| Contract revised (new term) | Old billing schedule replaced. Provider reads current state — always correct |
| PAKD rejected after being probable | Commission lines cancelled. Provider returns 0 |
| Term Deposit rolled over | Old deposit closes (JE exists → excluded), new deposit has new schedule |
| Bank Loan early repayment | Schedule rows still exist, linked JE created after posting → excluded |
| SO partially billed (50%) | SO provider returns remaining 50%. SI provider returns the billed 50% (if unpaid). No overlap. |
| SI paid partially | SI provider returns outstanding_amount (remaining). Already-paid portion excluded. |
| Quotation expired (valid_till < today) | Quotation provider excludes (valid_till < from_date) |
| Credit Note (SI is_return=1) | Excluded by SI provider (is_return=0 filter) |
| Debit Note (PI is_return=1) | Excluded by PI provider (is_return=0 filter) |
| No providers installed (fresh vn_accounting) | `frappe.get_hooks()` returns only vn_accounting's own providers. ERPNext data still shown. |
| OpEx projection on new company (< 6 months history) | Uses available months. If < 2 months → skip (not enough data for pattern). |
| No recurring expenses found | OpEx provider returns []. Valid — company has no predictable expenses. |
| **Advance payment (trả trước 30%)** | Customer pays 30% upfront via PE before SI created. SI later created with full grand_total but outstanding = 70%. SI provider returns outstanding_amount (70%), not grand_total. PE already in GL → no double-count. |
| **Contract billing + SI overlap (draft SI)** | Contract billing state='Projected' → SI created but still Draft (docstatus=0). Contract provider still sees Projected (SI not submitted). SI provider ignores Draft (docstatus filter). **Risk:** neither counts it. **Fix:** Contract provider treats Projected as included regardless — SI only counts when submitted. Gap = Draft SI window (typically minutes). Acceptable. |
| **Tax payment varies significantly** | Tax provider uses median of recent months. If business is growing fast, actual VAT will be higher. Confidence = "possible" signals this uncertainty. |

### 6.2 Technical Edge Cases

| Scenario | Expected behavior |
|----------|------------------|
| Provider throws exception | Caught by try/except. Other providers still run. Warning banner in UI. Error logged. |
| Provider returns invalid entry | Entry skipped. Logged to Error Log. Other entries from same provider still included. |
| Provider returns amount = 0 or negative | Rejected by validation |
| Provider ignores company filter | Aggregator cannot detect this — documented as provider responsibility |
| Very large result set (>10,000 entries) | In-memory grouping. Python handles 10k dicts easily. No pagination. |
| GL balance query fails | Opening balance defaults to 0 with warning. Forecast entries still shown. |
| Source checkbox unchecked → re-checked | Data already in browser, instant re-filter. No API call. |

## 7. Sidebar & Navigation

Replace 2 existing placeholder items in vn_accounting workspace sidebar:

| Current (placeholder) | New |
|----------------------|-----|
| "[Pending] Dự báo dòng tiền" under Quỹ tiền mặt | link_type=Page, link_to="cash-flow-forecast" |
| "[Pending] Dự báo dòng tiền" under Ngân hàng | link_type=Page, link_to="cash-flow-forecast" |

Both point to the same page.

## 8. Translations

Add to `vn_accounting/translations/vi.csv`:

```csv
Cash Flow Forecast,Dự Báo Dòng Tiền
Opening Balance,Số Dư Đầu Kỳ
Closing Balance,Số Dư Cuối Kỳ
Inflow,Thu Vào
Outflow,Chi Ra
Confidence,Mức Độ Chắc Chắn
Committed,Đã Cam Kết
Probable,Khả Năng Cao
Possible,Có Thể
Cash Shortfall Warning,Cảnh Báo Thiếu Hụt Tiền Mặt
Provider Error,Lỗi Nhà Cung Cấp Dữ Liệu
No forecast data available,Không có dữ liệu dự báo
Sales Invoice Receivable,Công Nợ Phải Thu (Hóa Đơn)
Purchase Invoice Payable,Công Nợ Phải Trả (Hóa Đơn)
Sales Order Pipeline,Đơn Hàng Bán Chờ Xuất HĐ
Purchase Order Pipeline,Đơn Hàng Mua Chờ Nhận HĐ
Quotation Pipeline,Báo Giá Chờ Duyệt
Projected OpEx,Chi Phí Hoạt Động Dự Báo
Deposit Interest,Lãi Tiền Gửi
Deposit Maturity,Đáo Hạn Tiền Gửi
Loan Repayment,Trả Nợ Vay
Loan Interest,Lãi Vay
```

Add to `dcnet_contract/translations/vi.csv`:
```csv
Contract Setup Fee,Phí Lắp Đặt Hợp Đồng
Contract Service,Dịch Vụ Hợp Đồng
```

Add to `dcnet_pakd/translations/vi.csv`:
```csv
PAKD Manager Services,Dịch Vụ Quản Lý PAKD
PAKD Add Costs,Chi Phí Ngoài PAKD
PAKD License Fee,Phí GPVT PAKD
PAKD Sales Commission,Hoa Hồng Kinh Doanh PAKD
```

## 9. Sample Data

dcnet_sample MUST generate rich forecast data for QA and demo. The data should produce a realistic 12-month forecast with variety across all provider types.

### 9.1 Contract Forecast Data (inflow via dcnet_contract)

| Contract | Customer | Type | Monthly Amount | Term | Start | Projected rows remaining |
|----------|----------|------|---------------|------|-------|------------------------|
| CTR-SAMPLE-001 | VNPT Đà Nẵng | Recurring/Monthly | 45,000,000 | 24 months | 2025-07-01 | ~15 rows |
| CTR-SAMPLE-002 | FPT Telecom | Recurring/Monthly | 28,000,000 | 12 months | 2026-01-01 | ~8 rows |
| CTR-SAMPLE-003 | Viettel IDC | Recurring/Prepay | 180,000,000 | 6 months | 2026-04-01 | 1 row (lump sum) |
| CTR-SAMPLE-004 | CMC Telecom | One-off | 95,000,000 | — | 2026-05-15 | 1 row |
| CTR-SAMPLE-005 | SCTV | Recurring/Monthly | 12,500,000 | 36 months | 2025-01-01 | ~9 rows |
| CTR-SAMPLE-006 | Mobifone | Recurring/Monthly | 67,000,000 | 12 months | 2026-03-01 | ~11 rows |
| CTR-SAMPLE-007 | VNG Cloud | Recurring/Monthly | 38,000,000 | 18 months | 2026-02-01 | ~14 rows |
| CTR-SAMPLE-008 | Vingroup | One-off + Setup | 250M setup + 55M/month | 24 months | 2026-06-01 | 1 + ~24 rows |

**~85 inflow entries** from contracts.

### 9.2 PAKD Commission Data (outflow via dcnet_pakd)

| PAKD | Sales Person | workflow_state | Components | ~Amount/month |
|------|-------------|---------------|-----------|--------------|
| PAKD-SAMPLE-001 | NV-001 (Nguyễn Văn A) | Approved | MS+AC+GPVT+KD | 6.75M |
| PAKD-SAMPLE-002 | NV-002 (Trần Thị B) | Approved | MS+KD | 3.36M |
| PAKD-SAMPLE-003 | NV-001 | Approved | MS+AC | 2.7M (lump) |
| PAKD-SAMPLE-004 | NV-003 (Lê Văn C) | Pending BGĐ | MS+AC+KD | 4.28M |
| PAKD-SAMPLE-005 | NV-002 | Approved | MS+GPVT+KD | 1.88M |
| PAKD-SAMPLE-006 | NV-004 (Phạm Thị D) | Pending P. Tổng hợp | All 4 | 10.05M |
| PAKD-SAMPLE-007 | NV-001 | Approved | MS+KD | 5.7M |
| PAKD-SAMPLE-008 | NV-003 | Approved | All 4 | 15.75M setup + 8.25M/month |

**~200 outflow entries** (committed: ~150, probable: ~50).

### 9.3 Treasury Data (inflow + outflow via vn_accounting)

| Instrument | Type | Amount | Rate | Term | Remaining entries |
|-----------|------|--------|------|------|------------------|
| TD-SAMPLE-001 | Term Deposit | 2B | 5.5% | 12mo, monthly interest | ~8 interest + 1 maturity |
| TD-SAMPLE-002 | Term Deposit | 500M | 6.0% | 6mo, end-of-term | 1 interest + 1 maturity |
| BL-SAMPLE-001 | Bank Loan | 3B | 8.5% | 36mo, EMI | ~12 repayments |
| BL-SAMPLE-002 | Bank Loan | 800M | 7.0% | 12mo, interest-only | ~8 interest + 1 principal |

**~30 entries** (10 inflow + 20 outflow).

### 9.4 ERPNext Pipeline Data (inflow + outflow)

| DocType | Count | Amount range | Status | Confidence |
|---------|-------|-------------|--------|------------|
| Quotation | 5 | 15M–120M | Open, valid_till future | possible |
| Sales Order | 8 | 20M–85M | To Deliver and Bill / To Bill | probable |
| Purchase Order | 6 | 10M–60M | To Receive and Bill / To Bill | probable |
| Sales Invoice (unpaid) | 12 | 8M–45M | Unpaid/Overdue, outstanding > 0 | committed |
| Purchase Invoice (unpaid) | 10 | 5M–35M | Unpaid/Overdue, outstanding > 0 | committed |

**~41 entries** from ERPNext pipeline.

### 9.5 Historical OpEx Projection Data

Ensure GL entries exist for past 6 months with recurring patterns:

| Expense account | Monthly amount (approx) | Frequency |
|----------------|------------------------|-----------|
| 6271 - Thuê văn phòng | 35,000,000 | Every month |
| 6272 - Điện nước | 12,000,000 | Every month (varies ±2M) |
| 6273 - Internet/viễn thông | 8,500,000 | Every month |
| 6278 - Dịch vụ thuê ngoài | 25,000,000 | 5 of 6 months |
| 6411 - Lương quản lý | SKIP (payroll-related) | — |
| 6417 - Bảo hiểm | 18,000,000 | Every month |

**~60 projected entries** (5 recurring accounts × 12 months).

### 9.6 Expected Totals with All Sources

When viewing 12-month forecast with ALL sources and ALL confidence levels:

| Metric | Approximate |
|--------|------------|
| Total entries | ~416 |
| Inflow entries | ~148 (contracts + treasury + quotation + SO + unpaid SI) |
| Outflow entries | ~268 (PAKD + treasury + PO + unpaid PI + projected OpEx) |
| Monthly inflow range | 155M – 425M |
| Monthly outflow range | 75M – 180M |
| Net positive every month? | Yes (with committed+probable). Toggle "possible" → still positive but lower. |

**Key demo moments:**
- T10/2026 spike (Viettel IDC prepay 180M)
- Gradual decline T1-T4/2027 (contracts expiring)
- Toggle "Quotation" on → adds ~5 possible inflows, total rises
- Toggle "Projected OpEx" on → adds steady ~98.5M/month outflow, net drops visibly
- Toggle "Probable" on → SO/PO entries appear, chart changes shape

### 9.7 Sample Data Generation

- Forecast data is a BYPRODUCT of correct source documents, not a separate generation step
- Ensure contracts have future acceptance_date + long terms → Projected billing rows
- Ensure PAKDs are Approved/Pending with Pending commission lines
- Ensure treasury instruments have future schedule rows without JEs
- Ensure ERPNext pipeline: create Quotations (Open), SOs (unbilled), POs (unbilled), SIs (unpaid), PIs (unpaid)
- Ensure GL entries exist for expense accounts across past 6 months
- Verify: aggregator returns 400+ entries for 12-month range

## 10. Testing

### 10.1 Unit Tests (aggregator + validation)

- `test_validate_entry_valid` — all required fields → accepted
- `test_validate_entry_missing_field` — missing expected_date → rejected
- `test_validate_entry_negative_amount` → rejected
- `test_validate_entry_invalid_direction` — "credit" → rejected
- `test_validate_entry_invalid_confidence` — "maybe" → rejected
- `test_validate_entry_bad_date` — "not-a-date" → rejected
- `test_aggregator_error_isolation` — provider throws → others still collected
- `test_aggregator_empty_hooks` → returns ([], [])
- `test_aggregator_filters_passed` — filters reach provider unchanged

### 10.2 Integration Tests (providers)

- `test_contract_provider_only_projected` — Invoiced/Paid excluded
- `test_contract_provider_respects_company` — different company → 0
- `test_contract_provider_respects_date_range` — outside range excluded
- `test_pakd_provider_confidence_mapping` — Approved=committed, Pending=probable
- `test_pakd_provider_only_pending_lines` — Posted excluded
- `test_treasury_provider_excludes_posted_je`
- `test_treasury_provider_includes_both_types` — deposits + loans
- `test_quotation_provider_excludes_ordered` — per_ordered > 0 excluded
- `test_so_provider_excludes_fully_billed` — per_billed=100 excluded
- `test_so_provider_partial_billing` — returns remaining amount only
- `test_si_provider_excludes_paid` — outstanding=0 excluded
- `test_si_provider_excludes_returns` — is_return=1 excluded
- `test_po_provider_excludes_fully_billed`
- `test_pi_provider_excludes_paid`
- `test_opex_provider_recurring_detection` — 4/6 months → included, 2/6 → excluded
- `test_opex_provider_median_calculation` — uses median not mean
- `test_opex_provider_insufficient_history` — < 2 months → returns []

### 10.3 Lifecycle Tests (no double-counting)

- `test_quotation_to_so_lifecycle` — create Quotation → create SO from it → Quotation no longer in forecast, SO appears
- `test_so_to_si_lifecycle` — fully bill SO → SO disappears, SI appears
- `test_si_to_pe_lifecycle` — pay SI → SI disappears from forecast

### 10.4 Page Tests

- `test_opening_balance_matches_gl` — first period = GL balance TK 111+112
- `test_closing_balance_rolling` — period N closing = period N+1 opening
- `test_negative_closing_flagged` — closing < 0 triggers warning in data

## 11. File Structure

All paths relative to repo root. Python package = inner directory.

### vn_accounting (core — 8 providers + page + chart)

```
apps/vn_accounting/
  vn_accounting/                         ← pip-installed Python package
    forecast/
      __init__.py
      aggregator.py                      — get_all_forecast_entries(), validate_entry()
      treasury.py                        — get_treasury_forecast()
      erpnext_providers.py               — quotation, SO, PO, unpaid SI, unpaid PI (5 providers)
      payroll_provider.py                — get_payroll_forecast() (HRMS or GL fallback)
      tax_provider.py                    — get_tax_forecast() (VAT/CIT/PIT)
      historical_projection.py           — get_opex_forecast() (12-month seasonal)
      payment_delay.py                   — get_payment_delay() per-customer helper
    vn_accounting/                       ← Frappe module dir
      page/
        cash_flow_forecast/
          __init__.py
          cash_flow_forecast.py          — Frappe Page controller
          cash_flow_forecast.js          — Page JS (chart + table + filters)
          cash_flow_forecast.css         — Page styles
          cash_flow_forecast.json        — Page metadata
    api/
      forecast.py                        — @whitelist API endpoints for page
      dashboard_charts.py                — add get_cash_flow_forecast_chart()
    translations/vi.csv                  — add forecast translations
    hooks.py                             — add cash_flow_forecast_providers, register page
```

### dcnet_contract (1 provider)

```
apps/dcnet_contract/
  dcnet_contract/                        ← pip-installed Python package
    forecast.py                          — get_contract_forecast() (~50 LOC)
    hooks.py                             — add cash_flow_forecast_providers line
    translations/vi.csv                  — add category translations
```

### dcnet_pakd (1 provider)

```
apps/dcnet_pakd/
  dcnet_pakd/                            ← pip-installed Python package
    forecast.py                          — get_pakd_forecast() (~60 LOC)
    hooks.py                             — add cash_flow_forecast_providers line
    translations/vi.csv                  — add category translations
```

## 12. Scope Summary

**v1 (this spec):**
- Hook-based provider system with validation + lifecycle prevention + overdue detection
- 8 ERPNext/DCNET providers: Treasury, Contract, PAKD, Quotation, SO, PO, unpaid SI, unpaid PI
- 3 projection providers: Historical OpEx (12-month, seasonal), Payroll, Tax obligations
- Payment delay factor (per-customer historical late payment adjustment)
- Opening balance includes TK 111 + TK 112 + TK 113
- Minimum cash threshold with 3-tier visual warnings
- Custom Frappe Page with chart + table + interactive toggles
- Dashboard v2 chart (simplified, committed only)
- Sample data for demo/QA (~500+ entries)
- Sidebar navigation (replace placeholders)
- Vietnamese translations
- Export to Excel

**Out of scope (future):**
- Budget vs actual comparison (forecast accuracy tracking)
- Scenario modeling (what-if analysis)
- Multi-currency support
- Push notifications for projected shortfall
- einvoice provider
- vn_banking provider
- CAPEX planning (equipment purchase forecasting beyond PO pipeline)
