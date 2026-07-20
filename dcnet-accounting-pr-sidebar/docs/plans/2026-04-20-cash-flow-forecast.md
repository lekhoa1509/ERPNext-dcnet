---
project: apps/vn_accounting
base_branch: main
---

# Cash Flow Forecast — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a hook-based cash flow forecast system with 11 providers, a custom Frappe Page, and Dashboard v2 integration.

**Architecture:** Hook-based pull model — each app registers provider functions via `cash_flow_forecast_providers` hook. vn_accounting aggregator discovers all providers at runtime, validates entries, and serves data to a custom Frappe Page with Chart.js visualization + drill-down table. No coupling between apps.

**Tech Stack:** Frappe v16, ERPNext v16, Python 3.14, vanilla JS + Chart.js (frappe.Chart), parameterized SQL queries.

**Spec:** `docs/specs/2026-04-20-cash-flow-forecast-design.md`

**Working directory:** `/home/long/long/frappe-bench-dcnet/` (bench root)

---

## File Map

### vn_accounting (core — new files)

| File | Responsibility |
|------|---------------|
| `vn_accounting/forecast/__init__.py` | Package marker |
| `vn_accounting/forecast/aggregator.py` | `get_all_forecast_entries()`, `validate_entry()` — core engine |
| `vn_accounting/forecast/payment_delay.py` | `get_payment_delay(customer, company)` — per-customer delay from PE history |
| `vn_accounting/forecast/treasury.py` | Provider: Term Deposit interest/maturity + Bank Loan repayment/interest |
| `vn_accounting/forecast/erpnext_providers.py` | 5 providers: Quotation, SO, PO, unpaid SI, unpaid PI |
| `vn_accounting/forecast/payroll_provider.py` | Provider: Payroll (HRMS or GL fallback) |
| `vn_accounting/forecast/tax_provider.py` | Provider: VAT/CIT/PIT projections |
| `vn_accounting/forecast/historical_projection.py` | Provider: recurring OpEx from 12-month GL history |
| `vn_accounting/forecast/test_aggregator.py` | Unit tests for aggregator + validation |
| `vn_accounting/forecast/test_providers.py` | Integration tests for all internal providers |
| `vn_accounting/api/forecast.py` | `@whitelist` API endpoints for page + dashboard chart |
| `vn_accounting/vn_accounting/page/cash_flow_forecast/__init__.py` | Page package marker |
| `vn_accounting/vn_accounting/page/cash_flow_forecast/cash_flow_forecast.json` | Page DocType metadata |
| `vn_accounting/vn_accounting/page/cash_flow_forecast/cash_flow_forecast.js` | Page JS — filters, chart, table, drill-down |
| `vn_accounting/vn_accounting/page/cash_flow_forecast/cash_flow_forecast.css` | Page styles — warnings, badges, layout |

### vn_accounting (modified files)

| File | Change |
|------|--------|
| `vn_accounting/hooks.py` | Add `cash_flow_forecast_providers` list (8 internal providers) |
| `vn_accounting/api/dashboard.py` | Extract `_balance_gl` into importable function; add TK 113 |
| `vn_accounting/api/dashboard_charts.py` | Add `get_cash_flow_forecast_chart()` |
| `vn_accounting/vn_accounting/page/vn_accounting_dashboard/vn_accounting_dashboard.js` | Add forecast chart section |
| `vn_accounting/workspace_sidebar/vn_accounting.json` | Replace 2 placeholder items |
| `vn_accounting/translations/vi.csv` | Add ~25 forecast translation entries |

### dcnet_contract (new files)

| File | Responsibility |
|------|---------------|
| `dcnet_contract/forecast.py` | Provider: contract billing schedule (Projected → inflow) |

### dcnet_contract (modified)

| File | Change |
|------|--------|
| `dcnet_contract/hooks.py` | Add `cash_flow_forecast_providers` |
| `dcnet_contract/translations/vi.csv` | Add 2 category translations |

### dcnet_pakd (new files)

| File | Responsibility |
|------|---------------|
| `dcnet_pakd/forecast.py` | Provider: commission lines (Pending → outflow) |

### dcnet_pakd (modified)

| File | Change |
|------|--------|
| `dcnet_pakd/hooks.py` | Add `cash_flow_forecast_providers` |
| `dcnet_pakd/translations/vi.csv` | Add 4 category translations |

---

## Phase 1: Core Framework (Aggregator + Validation)

### Task 1: Aggregator + Validation Engine

**Files:**
- Create: `apps/vn_accounting/vn_accounting/forecast/__init__.py`
- Create: `apps/vn_accounting/vn_accounting/forecast/aggregator.py`
- Create: `apps/vn_accounting/vn_accounting/forecast/test_aggregator.py`

**TDD required** — pure functions, no Frappe dependencies in validation logic.

- [ ] **Step 1: Create forecast package**

Create `apps/vn_accounting/vn_accounting/forecast/__init__.py` (empty).

- [ ] **Step 2: Write failing tests for validate_entry()**

Create `apps/vn_accounting/vn_accounting/forecast/test_aggregator.py`:

```python
import unittest
from vn_accounting.forecast.aggregator import validate_entry

class TestValidateEntry(unittest.TestCase):
    def _valid_entry(self):
        return {
            "expected_date": "2026-06-15",
            "amount": 15000000.0,
            "direction": "inflow",
            "category": "Contract Service",
            "confidence": "committed",
            "source_doctype": "DCNET Contract",
            "source_name": "CTR-001",
        }

    def test_valid_entry_accepted(self):
        result = validate_entry(self._valid_entry(), "test.provider")
        self.assertIsNotNone(result)

    def test_valid_entry_with_optionals(self):
        entry = self._valid_entry()
        entry.update({"party_type": "Customer", "party": "VNPT", "description": "Service fee"})
        result = validate_entry(entry, "test.provider")
        self.assertIsNotNone(result)

    def test_missing_required_field(self):
        entry = self._valid_entry()
        del entry["expected_date"]
        result = validate_entry(entry, "test.provider")
        self.assertIsNone(result)

    def test_negative_amount(self):
        entry = self._valid_entry()
        entry["amount"] = -100
        self.assertIsNone(validate_entry(entry, "test.provider"))

    def test_zero_amount(self):
        entry = self._valid_entry()
        entry["amount"] = 0
        self.assertIsNone(validate_entry(entry, "test.provider"))

    def test_invalid_direction(self):
        entry = self._valid_entry()
        entry["direction"] = "credit"
        self.assertIsNone(validate_entry(entry, "test.provider"))

    def test_invalid_confidence(self):
        entry = self._valid_entry()
        entry["confidence"] = "maybe"
        self.assertIsNone(validate_entry(entry, "test.provider"))

    def test_overdue_confidence_accepted(self):
        entry = self._valid_entry()
        entry["confidence"] = "overdue"
        self.assertIsNotNone(validate_entry(entry, "test.provider"))

    def test_bad_date_format(self):
        entry = self._valid_entry()
        entry["expected_date"] = "15/06/2026"
        self.assertIsNone(validate_entry(entry, "test.provider"))

    def test_amount_not_number(self):
        entry = self._valid_entry()
        entry["amount"] = "fifteen million"
        self.assertIsNone(validate_entry(entry, "test.provider"))
```

- [ ] **Step 3: Run tests to verify they fail**

Run: `cd /home/long/long/frappe-bench-dcnet && python -m pytest apps/vn_accounting/vn_accounting/forecast/test_aggregator.py -v`
Expected: ImportError — `aggregator` module doesn't exist yet.

- [ ] **Step 4: Implement validate_entry()**

Create `apps/vn_accounting/vn_accounting/forecast/aggregator.py`:

```python
"""Cash Flow Forecast Aggregator.

Discovers all providers via frappe.get_hooks("cash_flow_forecast_providers"),
calls each, validates entries, and returns consolidated forecast data.
"""
import frappe
from datetime import datetime

VALID_DIRECTIONS = ("inflow", "outflow")
VALID_CONFIDENCE = ("overdue", "committed", "probable", "possible")
REQUIRED_FIELDS = ("expected_date", "amount", "direction", "category",
                   "confidence", "source_doctype", "source_name")


def validate_entry(entry, provider_path):
    """Validate a single ForecastEntry dict. Returns entry if valid, None if invalid."""
    if not isinstance(entry, dict):
        return None

    # Check required fields exist and are non-empty strings (except amount)
    for field in REQUIRED_FIELDS:
        if field not in entry or entry[field] is None:
            _log_invalid(provider_path, entry, f"Missing required field: {field}")
            return None

    # Validate amount
    if not isinstance(entry["amount"], (int, float)):
        _log_invalid(provider_path, entry, f"amount must be numeric, got {type(entry['amount'])}")
        return None
    if entry["amount"] <= 0:
        _log_invalid(provider_path, entry, f"amount must be > 0, got {entry['amount']}")
        return None

    # Validate enums
    if entry["direction"] not in VALID_DIRECTIONS:
        _log_invalid(provider_path, entry, f"direction must be one of {VALID_DIRECTIONS}")
        return None
    if entry["confidence"] not in VALID_CONFIDENCE:
        _log_invalid(provider_path, entry, f"confidence must be one of {VALID_CONFIDENCE}")
        return None

    # Validate date format
    try:
        datetime.strptime(str(entry["expected_date"]), "%Y-%m-%d")
    except ValueError:
        _log_invalid(provider_path, entry, f"expected_date must be YYYY-MM-DD, got {entry['expected_date']}")
        return None

    return entry


def _log_invalid(provider_path, entry, reason):
    """Log validation failure. Uses frappe.log_error if available, else pass."""
    try:
        frappe.log_error(
            title="Cash Flow Forecast: invalid entry",
            message=f"Provider: {provider_path}\nReason: {reason}\nEntry: {entry}",
        )
    except Exception:
        pass  # Unit tests run without frappe context


def get_all_forecast_entries(filters):
    """Collect and validate forecast entries from all registered providers.

    Args:
        filters: dict with keys: company (str), from_date (str), to_date (str),
                 confidence (list[str], optional)

    Returns:
        tuple: (entries: list[dict], errors: list[dict])
    """
    entries = []
    errors = []

    for method_path in frappe.get_hooks("cash_flow_forecast_providers"):
        try:
            fn = frappe.get_attr(method_path)
            raw = fn(filters)
            if not isinstance(raw, (list, tuple)):
                errors.append({"provider": method_path, "error": "Provider did not return a list"})
                continue
            for entry in raw:
                validated = validate_entry(entry, method_path)
                if validated:
                    validated["_provider"] = method_path  # Tag for debugging
                    entries.append(validated)
        except Exception as e:
            errors.append({"provider": method_path, "error": str(e)})
            frappe.log_error(
                title=f"Cash flow provider failed: {method_path}",
                message=str(e),
            )

    return entries, errors
```

- [ ] **Step 5: Run tests to verify they pass**

Run: `cd /home/long/long/frappe-bench-dcnet && python -m pytest apps/vn_accounting/vn_accounting/forecast/test_aggregator.py -v`
Expected: All 10 tests PASS.

- [ ] **Step 6: Commit**

```bash
git -C apps/vn_accounting add vn_accounting/forecast/
git -C apps/vn_accounting commit -m "feat(forecast): add aggregator + validate_entry with TDD"
```

---

### Task 2: Payment Delay Helper

**Files:**
- Create: `apps/vn_accounting/vn_accounting/forecast/payment_delay.py`

**Verify at end** — uses frappe.db.sql, needs site context for integration test.

- [ ] **Step 1: Implement get_payment_delay()**

Create `apps/vn_accounting/vn_accounting/forecast/payment_delay.py`:

```python
"""Per-customer payment delay calculation from historical Payment Entry data.

Calculates median days late (PE.posting_date - SI.due_date) for a customer
over the last 12 months. Used by inflow providers to adjust expected_date
to be more realistic for Vietnamese B2B payments.
"""
import frappe
from datetime import timedelta


def get_payment_delay(customer, company):
    """Return median payment delay in days for a customer.

    Args:
        customer: Customer name
        company: Company name

    Returns:
        int: median delay days (0 if on-time or no history)
    """
    delays = frappe.db.sql("""
        SELECT DATEDIFF(pe.posting_date, si.due_date) as delay
        FROM `tabPayment Entry Reference` per
        JOIN `tabPayment Entry` pe ON pe.name = per.parent
        JOIN `tabSales Invoice` si ON si.name = per.reference_name
        WHERE per.reference_doctype = 'Sales Invoice'
          AND pe.party_type = 'Customer'
          AND pe.party = %(customer)s
          AND pe.company = %(company)s
          AND pe.docstatus = 1
          AND si.due_date IS NOT NULL
          AND pe.posting_date >= DATE_SUB(CURDATE(), INTERVAL 12 MONTH)
    """, {"customer": customer, "company": company}, as_dict=True)

    if not delays:
        return 0

    values = sorted([max(0, d.delay) for d in delays])  # Only count late payments
    return values[len(values) // 2]  # median


# In-memory cache per API call (cleared between requests)
_delay_cache = {}


def get_payment_delay_cached(customer, company):
    """Cached version — one DB query per customer per request."""
    key = f"{customer}:{company}"
    if key not in _delay_cache:
        _delay_cache[key] = get_payment_delay(customer, company)
    return _delay_cache[key]


def clear_delay_cache():
    """Call at the start of each forecast API request."""
    global _delay_cache
    _delay_cache = {}


def adjust_expected_date(expected_date_str, customer, company):
    """Adjust expected_date by customer's historical delay.

    Only for inflow — outflow providers should NOT call this.
    Returns: adjusted date as string YYYY-MM-DD.
    """
    delay = get_payment_delay_cached(customer, company)
    if delay <= 0:
        return expected_date_str

    from datetime import datetime
    dt = datetime.strptime(expected_date_str, "%Y-%m-%d")
    adjusted = dt + timedelta(days=delay)
    return adjusted.strftime("%Y-%m-%d")
```

- [ ] **Step 2: Commit**

```bash
git -C apps/vn_accounting add vn_accounting/forecast/payment_delay.py
git -C apps/vn_accounting commit -m "feat(forecast): add per-customer payment delay helper"
```

---

## Phase 2: Internal Providers (vn_accounting)

### Task 3: Treasury Provider

**Files:**
- Create: `apps/vn_accounting/vn_accounting/forecast/treasury.py`

**Verify at end** — queries Term Deposit + Bank Loan child tables.

- [ ] **Step 1: Implement get_treasury_forecast()**

```python
"""Treasury forecast provider.

Data sources:
- Term Deposit Interest schedule rows (status != 'Booked') → inflow
- Term Deposit maturity (status != 'Matured') → inflow
- Bank Loan Repayment schedule rows (status != 'Booked') → outflow
"""
import frappe
from datetime import date


def get_treasury_forecast(filters):
    company = filters.get("company")
    from_date = filters.get("from_date")
    to_date = filters.get("to_date")
    if not company or not from_date or not to_date:
        return []

    entries = []
    entries.extend(_get_deposit_interest(company, from_date, to_date))
    entries.extend(_get_deposit_maturity(company, from_date, to_date))
    entries.extend(_get_loan_repayments(company, from_date, to_date))
    return entries


def _get_deposit_interest(company, from_date, to_date):
    rows = frappe.db.sql("""
        SELECT ti.due_date, ti.interest_amount, ti.name,
               td.name as deposit_name, td.bank
        FROM `tabTerm Deposit Interest` ti
        JOIN `tabTerm Deposit` td ON td.name = ti.parent
        WHERE td.company = %(company)s
          AND td.docstatus = 0
          AND ti.status IN ('Pending', 'Draft Created')
          AND ti.due_date BETWEEN %(from_date)s AND %(to_date)s
    """, {"company": company, "from_date": from_date, "to_date": to_date}, as_dict=True)

    return [{
        "expected_date": str(r.due_date),
        "amount": float(r.interest_amount),
        "direction": "inflow",
        "category": "Deposit Interest",
        "confidence": "committed",
        "party_type": "Supplier",
        "party": r.bank,
        "source_doctype": "Term Deposit",
        "source_name": r.deposit_name,
        "description": f"Interest - {r.deposit_name}",
    } for r in rows]


def _get_deposit_maturity(company, from_date, to_date):
    deposits = frappe.get_all("Term Deposit", filters={
        "company": company, "docstatus": 0,
        "status": ["not in", ["Matured", "Broken"]],
        "maturity_date": ["between", [from_date, to_date]],
    }, fields=["name", "deposit_amount", "maturity_date", "bank"])

    return [{
        "expected_date": str(d.maturity_date),
        "amount": float(d.deposit_amount),
        "direction": "inflow",
        "category": "Deposit Maturity",
        "confidence": "committed",
        "party_type": "Supplier",
        "party": d.bank,
        "source_doctype": "Term Deposit",
        "source_name": d.name,
        "description": f"Maturity - {d.name}",
    } for d in deposits]


def _get_loan_repayments(company, from_date, to_date):
    rows = frappe.db.sql("""
        SELECT lr.due_date, lr.total_payment, lr.principal_amount,
               lr.interest_amount, lr.name,
               bl.name as loan_name, bl.bank
        FROM `tabBank Loan Repayment` lr
        JOIN `tabBank Loan` bl ON bl.name = lr.parent
        WHERE bl.company = %(company)s
          AND bl.docstatus = 0
          AND lr.status IN ('Pending', 'Draft Created')
          AND lr.due_date BETWEEN %(from_date)s AND %(to_date)s
    """, {"company": company, "from_date": from_date, "to_date": to_date}, as_dict=True)

    entries = []
    for r in rows:
        if r.principal_amount and float(r.principal_amount) > 0:
            entries.append({
                "expected_date": str(r.due_date),
                "amount": float(r.principal_amount),
                "direction": "outflow",
                "category": "Loan Repayment",
                "confidence": "committed",
                "party_type": "Supplier",
                "party": r.bank,
                "source_doctype": "Bank Loan",
                "source_name": r.loan_name,
                "description": f"Principal - {r.loan_name}",
            })
        if r.interest_amount and float(r.interest_amount) > 0:
            entries.append({
                "expected_date": str(r.due_date),
                "amount": float(r.interest_amount),
                "direction": "outflow",
                "category": "Loan Interest",
                "confidence": "committed",
                "party_type": "Supplier",
                "party": r.bank,
                "source_doctype": "Bank Loan",
                "source_name": r.loan_name,
                "description": f"Interest - {r.loan_name}",
            })
    return entries
```

- [ ] **Step 2: Commit**

```bash
git -C apps/vn_accounting add vn_accounting/forecast/treasury.py
git -C apps/vn_accounting commit -m "feat(forecast): add treasury provider (deposit + loan)"
```

---

### Task 4: ERPNext Pipeline Providers (5 providers)

**Files:**
- Create: `apps/vn_accounting/vn_accounting/forecast/erpnext_providers.py`

**Verify at end** — queries standard ERPNext DocTypes.

- [ ] **Step 1: Implement 5 ERPNext providers**

Create `apps/vn_accounting/vn_accounting/forecast/erpnext_providers.py` with these functions:
- `get_quotation_forecast(filters)` — Open quotations not ordered, confidence=possible
- `get_sales_order_forecast(filters)` — Submitted, per_billed<100, confidence=probable
- `get_purchase_order_forecast(filters)` — Submitted, per_billed<100, confidence=probable
- `get_unpaid_si_forecast(filters)` — Submitted, outstanding>0, is_return=0, confidence=committed/overdue
- `get_unpaid_pi_forecast(filters)` — Submitted, outstanding>0, is_return=0, confidence=committed/overdue

Key implementation details per spec §5.2:
- SI/PI: use `due_date` directly. If `due_date < today` and outstanding > 0 → confidence = "overdue"
- SI: apply `adjust_expected_date()` from payment_delay module for committed (not overdue)
- SO: check Payment Schedule child table for due_date, fallback transaction_date + 30
- PO: check Payment Schedule child table, fallback earliest schedule_date + 30
- Quotation: use valid_till, fallback transaction_date + 30
- SO amount = `grand_total * (100 - per_billed) / 100`

Each function follows the same pattern: query, loop, build entry dict, return list.

File target: ~250 LOC (5 functions × ~50 LOC each).

- [ ] **Step 2: Commit**

```bash
git -C apps/vn_accounting add vn_accounting/forecast/erpnext_providers.py
git -C apps/vn_accounting commit -m "feat(forecast): add 5 ERPNext pipeline providers (QT/SO/PO/SI/PI)"
```

---

### Task 5: Payroll Provider

**Files:**
- Create: `apps/vn_accounting/vn_accounting/forecast/payroll_provider.py`

- [ ] **Step 1: Implement get_payroll_forecast()**

Strategy per spec §5.3a:
1. If HRMS installed → query last submitted Payroll Entry total, project monthly
2. Fallback → query GL for TK 334 + 3383 + 3384 + 3386 in past 3 months, median forward

Output: direction=outflow, category="Payroll"/"Social Insurance"
Expected dates: 5th of each month (salary), 20th (insurance contributions)
Confidence: probable (from Payroll Entry) or possible (from GL)

File target: ~100 LOC.

- [ ] **Step 2: Commit**

```bash
git -C apps/vn_accounting add vn_accounting/forecast/payroll_provider.py
git -C apps/vn_accounting commit -m "feat(forecast): add payroll provider (HRMS + GL fallback)"
```

---

### Task 6: Tax Provider

**Files:**
- Create: `apps/vn_accounting/vn_accounting/forecast/tax_provider.py`

- [ ] **Step 1: Implement get_tax_forecast()**

Per spec §5.3b:
- VAT (TK 33311): monthly, due 20th of following month. Query last 3 months credit balance, project median.
- CIT (TK 3334): quarterly, due 30th of first month of next quarter. Project 25% of last year total ÷ 4.
- PIT (TK 3335): monthly, due 20th of following month. Query last 3 months, median.

Output: direction=outflow, confidence=possible, category="VAT Payment"/"Corporate Income Tax"/"Personal Income Tax"

File target: ~120 LOC.

- [ ] **Step 2: Commit**

```bash
git -C apps/vn_accounting add vn_accounting/forecast/tax_provider.py
git -C apps/vn_accounting commit -m "feat(forecast): add tax obligations provider (VAT/CIT/PIT)"
```

---

### Task 7: Historical OpEx Projection

**Files:**
- Create: `apps/vn_accounting/vn_accounting/forecast/historical_projection.py`

- [ ] **Step 1: Implement get_opex_forecast()**

Per spec §5.3 (updated):
- Query GL for TK 6xx (excluding payroll TK 642x) in past 12 months
- Group by account + month
- Recurring threshold: >= 8 of 12 months (fallback: >= 4 of 6 if < 12 months history)
- Projection: same-month-last-year if available, else median
- Cap at 2× median per month

File target: ~130 LOC.

- [ ] **Step 2: Commit**

```bash
git -C apps/vn_accounting add vn_accounting/forecast/historical_projection.py
git -C apps/vn_accounting commit -m "feat(forecast): add historical OpEx projection (12-month seasonal)"
```

---

### Task 8: Register hooks + Opening Balance fix

**Files:**
- Modify: `apps/vn_accounting/vn_accounting/hooks.py`
- Modify: `apps/vn_accounting/vn_accounting/api/dashboard.py`

- [ ] **Step 1: Add cash_flow_forecast_providers to hooks.py**

Add after existing `scheduler_events`:

```python
# Cash Flow Forecast — provider registration
cash_flow_forecast_providers = [
    "vn_accounting.forecast.treasury.get_treasury_forecast",
    "vn_accounting.forecast.erpnext_providers.get_quotation_forecast",
    "vn_accounting.forecast.erpnext_providers.get_sales_order_forecast",
    "vn_accounting.forecast.erpnext_providers.get_purchase_order_forecast",
    "vn_accounting.forecast.erpnext_providers.get_unpaid_si_forecast",
    "vn_accounting.forecast.erpnext_providers.get_unpaid_pi_forecast",
    "vn_accounting.forecast.payroll_provider.get_payroll_forecast",
    "vn_accounting.forecast.tax_provider.get_tax_forecast",
    "vn_accounting.forecast.historical_projection.get_opex_forecast",
]
```

- [ ] **Step 2: Fix opening balance to include TK 113**

In `dashboard.py`, update `_balance_gl_cash()` or add a new function:

```python
def _balance_gl_liquidity(company, to_date=None):
    """TK 111 (cash) + TK 112 (bank) + TK 113 (cash in transit)."""
    return (
        _balance_gl(company, "111", to_date)
        + _balance_gl(company, "112", to_date)
        + _balance_gl(company, "113", to_date)
    )
```

- [ ] **Step 3: Commit**

```bash
git -C apps/vn_accounting add vn_accounting/hooks.py vn_accounting/api/dashboard.py
git -C apps/vn_accounting commit -m "feat(forecast): register 9 providers in hooks + add TK 113 to liquidity balance"
```

---

## Phase 3: External Providers (dcnet_contract + dcnet_pakd)

### Task 9: dcnet_contract Provider

**Files:**
- Create: `apps/dcnet_contract/dcnet_contract/forecast.py`
- Modify: `apps/dcnet_contract/dcnet_contract/hooks.py`
- Modify: `apps/dcnet_contract/dcnet_contract/translations/vi.csv`

- [ ] **Step 1: Implement get_contract_forecast()**

Per spec §5.4:
- Query billing schedule state='Projected', contract status IN ('Active','Suspended'), docstatus=1
- JOIN contract for company filter + customer
- Apply `adjust_expected_date()` from vn_accounting.forecast.payment_delay
- category = "Contract Setup Fee" or "Contract Service" (from item_type)

```python
import frappe
from vn_accounting.forecast.payment_delay import adjust_expected_date

def get_contract_forecast(filters):
    company = filters.get("company")
    from_date = filters.get("from_date")
    to_date = filters.get("to_date")
    if not company or not from_date or not to_date:
        return []

    rows = frappe.db.sql("""
        SELECT bs.due_date, bs.amount, bs.item_type,
               c.name as contract_name, c.customer
        FROM `tabDCNET Contract Billing Schedule` bs
        JOIN `tabDCNET Contract` c ON c.name = bs.parent
        WHERE c.company = %(company)s
          AND c.docstatus = 1
          AND c.status IN ('Active', 'Suspended')
          AND bs.state = 'Projected'
          AND bs.due_date BETWEEN %(from_date)s AND %(to_date)s
    """, {"company": company, "from_date": from_date, "to_date": to_date}, as_dict=True)

    entries = []
    for r in rows:
        adjusted_date = adjust_expected_date(str(r.due_date), r.customer, company)
        entries.append({
            "expected_date": adjusted_date,
            "amount": float(r.amount),
            "direction": "inflow",
            "category": f"Contract {r.item_type}",
            "confidence": "committed",
            "party_type": "Customer",
            "party": r.customer,
            "source_doctype": "DCNET Contract",
            "source_name": r.contract_name,
            "description": f"{r.item_type} - {r.contract_name}",
        })
    return entries
```

- [ ] **Step 2: Add hook to dcnet_contract/hooks.py**

Add at end of file:
```python
# Cash Flow Forecast provider
cash_flow_forecast_providers = [
    "dcnet_contract.forecast.get_contract_forecast"
]
```

- [ ] **Step 3: Add translations to vi.csv**

Append to `dcnet_contract/translations/vi.csv`:
```csv
Contract Setup Fee,Phí Lắp Đặt Hợp Đồng
Contract Service,Dịch Vụ Hợp Đồng
```

- [ ] **Step 4: Commit**

```bash
git -C apps/dcnet_contract add dcnet_contract/forecast.py dcnet_contract/hooks.py dcnet_contract/translations/vi.csv
git -C apps/dcnet_contract commit -m "feat(forecast): add cash flow forecast provider for contract billing"
```

---

### Task 10: dcnet_pakd Provider

**Files:**
- Create: `apps/dcnet_pakd/dcnet_pakd/forecast.py`
- Modify: `apps/dcnet_pakd/dcnet_pakd/hooks.py`
- Modify: `apps/dcnet_pakd/dcnet_pakd/translations/vi.csv`

- [ ] **Step 1: Implement get_pakd_forecast()**

Per spec §5.5:
- Query commission lines state='Pending'
- JOIN PAKD for workflow_state → confidence mapping (Approved=committed, Pending*=probable)
- JOIN DCNET Contract + Billing Schedule for due_date (via billing_schedule_idx)
- Filter company via Contract table (PAKD has no company field)

```python
import frappe

def get_pakd_forecast(filters):
    company = filters.get("company")
    from_date = filters.get("from_date")
    to_date = filters.get("to_date")
    if not company or not from_date or not to_date:
        return []

    rows = frappe.db.sql("""
        SELECT cl.component, cl.amount, cl.name as line_name,
               p.name as pakd_name, p.workflow_state, p.sales_person,
               bs.due_date
        FROM `tabPAKD Commission Line` cl
        JOIN `tabPhuong An Kinh Doanh` p ON p.name = cl.parent
        JOIN `tabDCNET Contract` c ON c.name = p.contract_ref
        JOIN `tabDCNET Contract Billing Schedule` bs
            ON bs.parent = c.name AND bs.idx = cl.billing_schedule_idx
        WHERE cl.state = 'Pending'
          AND c.company = %(company)s
          AND bs.due_date BETWEEN %(from_date)s AND %(to_date)s
    """, {"company": company, "from_date": from_date, "to_date": to_date}, as_dict=True)

    entries = []
    for r in rows:
        if r.workflow_state == "Approved":
            confidence = "committed"
        elif r.workflow_state in ("Pending GĐ TT KD", "Pending P. Tổng hợp",
                                   "Pending GĐ CN", "Pending BGĐ"):
            confidence = "probable"
        else:
            continue

        entries.append({
            "expected_date": str(r.due_date),
            "amount": float(r.amount),
            "direction": "outflow",
            "category": f"PAKD {r.component}",
            "confidence": confidence,
            "party_type": "Employee",
            "party": r.sales_person,
            "source_doctype": "Phuong An Kinh Doanh",
            "source_name": r.pakd_name,
            "description": f"{r.component} - {r.pakd_name}",
        })
    return entries
```

- [ ] **Step 2: Add hook + translations**

Same pattern as Task 9 — add to hooks.py and vi.csv.

- [ ] **Step 3: Commit**

```bash
git -C apps/dcnet_pakd add dcnet_pakd/forecast.py dcnet_pakd/hooks.py dcnet_pakd/translations/vi.csv
git -C apps/dcnet_pakd commit -m "feat(forecast): add cash flow forecast provider for PAKD commission"
```

---

## Phase 4: API Layer + Custom Frappe Page

### Task 11: Forecast API Endpoints

**Files:**
- Create: `apps/vn_accounting/vn_accounting/api/forecast.py`

- [ ] **Step 1: Implement whitelist API**

```python
"""Forecast API endpoints for the Cash Flow Forecast page and Dashboard v2."""
import frappe
from datetime import date, timedelta
from vn_accounting.forecast.aggregator import get_all_forecast_entries
from vn_accounting.forecast.payment_delay import clear_delay_cache
from vn_accounting.api.dashboard import _balance_gl


@frappe.whitelist()
def get_forecast_data(company=None, months=12):
    """Main API for the forecast page. Returns all entries + opening balance.

    Called once on page load / company+period change. Client filters by
    confidence + source without re-fetching.
    """
    if not company:
        company = frappe.defaults.get_user_default("Company")

    today = date.today()
    from_date = today.strftime("%Y-%m-%d")
    to_date = (today + timedelta(days=months * 30)).strftime("%Y-%m-%d")

    clear_delay_cache()

    entries, errors = get_all_forecast_entries({
        "company": company,
        "from_date": from_date,
        "to_date": to_date,
    })

    # Opening balance: TK 111 + 112 + 113
    opening = (
        _balance_gl(company, "111")
        + _balance_gl(company, "112")
        + _balance_gl(company, "113")
    )

    # Minimum cash threshold from settings
    threshold = frappe.db.get_single_value("VN Accounting Settings", "minimum_cash_threshold") or 500000000

    # Collect available categories and sources for filter UI
    categories = sorted(set(e["category"] for e in entries))
    sources = sorted(set(e["source_doctype"] for e in entries))

    return {
        "entries": entries,
        "errors": errors,
        "opening_balance": opening,
        "minimum_threshold": threshold,
        "categories": categories,
        "sources": sources,
        "from_date": from_date,
        "to_date": to_date,
    }


@frappe.whitelist()
def get_forecast_chart(company=None, months=12):
    """Simplified API for Dashboard v2 chart. Committed only, monthly."""
    if not company:
        company = frappe.defaults.get_user_default("Company")

    today = date.today()
    from_date = today.strftime("%Y-%m-%d")
    to_date = (today + timedelta(days=months * 30)).strftime("%Y-%m-%d")

    clear_delay_cache()

    entries, _ = get_all_forecast_entries({
        "company": company,
        "from_date": from_date,
        "to_date": to_date,
        "confidence": ["committed"],
    })

    opening = (
        _balance_gl(company, "111")
        + _balance_gl(company, "112")
        + _balance_gl(company, "113")
    )

    # Group by month
    monthly = _group_by_month(entries, from_date, to_date, opening)

    return {
        "labels": [m["label"] for m in monthly],
        "datasets": {
            "inflow": [m["inflow"] for m in monthly],
            "outflow": [m["outflow"] for m in monthly],
            "balance": [m["closing"] for m in monthly],
        },
    }


def _group_by_month(entries, from_date, to_date, opening):
    """Group entries by YYYY-MM and compute rolling balance."""
    from collections import defaultdict
    from datetime import datetime

    monthly_data = defaultdict(lambda: {"inflow": 0, "outflow": 0})

    for e in entries:
        month_key = e["expected_date"][:7]  # YYYY-MM
        if e["direction"] == "inflow":
            monthly_data[month_key]["inflow"] += e["amount"]
        else:
            monthly_data[month_key]["outflow"] += e["amount"]

    # Build sorted month list
    start = datetime.strptime(from_date, "%Y-%m-%d")
    end = datetime.strptime(to_date, "%Y-%m-%d")
    months = []
    current = start.replace(day=1)
    while current <= end:
        key = current.strftime("%Y-%m")
        months.append(key)
        if current.month == 12:
            current = current.replace(year=current.year + 1, month=1)
        else:
            current = current.replace(month=current.month + 1)

    # Compute rolling balance
    result = []
    balance = opening
    for key in months:
        data = monthly_data.get(key, {"inflow": 0, "outflow": 0})
        net = data["inflow"] - data["outflow"]
        closing = balance + net
        # Label: T5/2026
        month_num = int(key.split("-")[1])
        year = key.split("-")[0]
        result.append({
            "label": f"T{month_num}/{year}",
            "inflow": data["inflow"],
            "outflow": data["outflow"],
            "net": net,
            "opening": balance,
            "closing": closing,
        })
        balance = closing

    return result
```

- [ ] **Step 2: Commit**

```bash
git -C apps/vn_accounting add vn_accounting/api/forecast.py
git -C apps/vn_accounting commit -m "feat(forecast): add whitelist API endpoints for page + dashboard chart"
```

---

### Task 12: Custom Frappe Page (JS + Chart + Table)

**Files:**
- Create: `apps/vn_accounting/vn_accounting/vn_accounting/page/cash_flow_forecast/__init__.py`
- Create: `apps/vn_accounting/vn_accounting/vn_accounting/page/cash_flow_forecast/cash_flow_forecast.json`
- Create: `apps/vn_accounting/vn_accounting/vn_accounting/page/cash_flow_forecast/cash_flow_forecast.js`
- Create: `apps/vn_accounting/vn_accounting/vn_accounting/page/cash_flow_forecast/cash_flow_forecast.css`

- [ ] **Step 1: Create page JSON metadata**

```json
{
    "content": null,
    "creation": "2026-04-20 00:00:00",
    "docstatus": 0,
    "doctype": "Page",
    "idx": 0,
    "module": "VN Accounting",
    "name": "cash-flow-forecast",
    "page_name": "cash-flow-forecast",
    "roles": [
        {"role": "Accounts User"},
        {"role": "Accounts Manager"},
        {"role": "System Manager"}
    ],
    "standard": "Yes",
    "title": "Cash Flow Forecast"
}
```

- [ ] **Step 2: Implement page JS**

Full page implementation following the pattern from `vn_accounting_dashboard.js` (292 lines):
- `on_page_load` → create page with `frappe.ui.make_app_page()`
- Filter controls: Company (Link), Period (Select: 3/6/12), Granularity (Select: Monthly/Weekly)
- Checkbox groups: Confidence levels (overdue/committed/probable/possible), Source toggles
- `load_data()` → `frappe.xcall("vn_accounting.api.forecast.get_forecast_data", {company, months})`
- `render_chart()` → frappe.Chart with bar (inflow green + outflow red) + line (balance dashed blue) + threshold line (dashed orange)
- `render_table()` → HTML table with period rows + expandable drill-down
- Client-side filtering: confidence + source checkboxes re-filter `this.entries` without API call
- Warning highlights: closing < 0 → red row, closing < threshold → yellow row
- Export button → generate Excel with 2 sheets
- Source/confidence mismatch tooltip (spec §3.3)

Target: ~400 LOC JS. Reference pattern: `vn_accounting_dashboard.js`.

- [ ] **Step 3: Create page CSS**

Styles for: warning rows (red/yellow), confidence badges, drill-down expand/collapse, chart container, source toggle grid, export button.

Target: ~80 LOC CSS.

- [ ] **Step 4: Commit**

```bash
git -C apps/vn_accounting add vn_accounting/vn_accounting/page/cash_flow_forecast/
git -C apps/vn_accounting commit -m "feat(forecast): add Custom Frappe Page with chart + drill-down table"
```

---

## Phase 5: Integration (Dashboard + Sidebar + Translations)

### Task 13: Dashboard v2 Chart + Sidebar + Translations

**Files:**
- Modify: `apps/vn_accounting/vn_accounting/api/dashboard_charts.py`
- Modify: `apps/vn_accounting/vn_accounting/vn_accounting/page/vn_accounting_dashboard/vn_accounting_dashboard.js`
- Modify: `apps/vn_accounting/vn_accounting/workspace_sidebar/vn_accounting.json`
- Modify: `apps/vn_accounting/vn_accounting/translations/vi.csv`

- [ ] **Step 1: Add forecast chart to Dashboard v2 API**

In `dashboard_charts.py`, add function that calls `get_forecast_chart()` from `api/forecast.py`.

- [ ] **Step 2: Add chart rendering to Dashboard v2 JS**

In `vn_accounting_dashboard.js`, add a new chart section after the existing "Dòng Tiền" chart. Use same frappe.Chart pattern. Click → navigate to `/desk/cash-flow-forecast`.

- [ ] **Step 3: Update workspace sidebar JSON**

Replace the 2 placeholder items (find `"[Pending] Dự báo dòng tiền"`) with:
```json
{
    "type": "Link",
    "link_type": "Page",
    "link_to": "cash-flow-forecast",
    "label": "Dự báo dòng tiền",
    "icon": "trending-up"
}
```

- [ ] **Step 4: Add translations to vi.csv**

Append ~25 entries per spec §8 (Cash Flow Forecast, Opening Balance, Closing Balance, etc.).

- [ ] **Step 5: Add minimum_cash_threshold field to VN Accounting Settings**

If not exists, add a Currency field `minimum_cash_threshold` to the Settings DocType JSON with default 500000000.

- [ ] **Step 6: bench build + bench clear-cache**

```bash
cd /home/long/long/frappe-bench-dcnet
bench build --app vn_accounting
bench --site dcnet.localhost clear-cache
bench --site dcnet.localhost migrate
```

- [ ] **Step 7: Commit**

```bash
git -C apps/vn_accounting add -A
git -C apps/vn_accounting commit -m "feat(forecast): add Dashboard v2 chart, sidebar links, translations, Settings field"
```

---

## Phase 6: Sample Data + QA + Final Verification

### Task 14: Sample Data for Forecast

**Files:**
- Determine exact location in dcnet_sample (read dcnet_sample structure first)

- [ ] **Step 1: Ensure source documents produce forecast data**

Sample data for forecast is a BYPRODUCT of correct source documents. Verify/create:
- Contracts with future Projected billing rows (acceptance_date recent, long terms)
- PAKDs in Approved/Pending states with Pending commission lines
- Term Deposits with future interest schedule rows (status=Pending)
- Bank Loans with future repayment schedule rows (status=Pending)
- Quotations with status=Open, valid_till in future
- Sales Orders with per_billed < 100
- Purchase Orders with per_billed < 100
- Sales Invoices with outstanding_amount > 0
- Purchase Invoices with outstanding_amount > 0
- GL entries for TK 6xx expense accounts across past 6-12 months (for OpEx projection)

Use dcnet_sample's existing generators where possible. Add/adjust data for forecast demo moments per spec §9.

- [ ] **Step 2: Verify aggregator returns 400+ entries**

```bash
bench --site dcnet.localhost execute "exec(open('/tmp/test_forecast.py').read())"
```

Where `/tmp/test_forecast.py`:
```python
from vn_accounting.forecast.aggregator import get_all_forecast_entries
entries, errors = get_all_forecast_entries({
    "company": "DCNET",
    "from_date": "2026-05-01",
    "to_date": "2027-04-30",
})
print(f"Total entries: {len(entries)}")
print(f"Errors: {errors}")
print(f"Inflows: {sum(1 for e in entries if e['direction'] == 'inflow')}")
print(f"Outflows: {sum(1 for e in entries if e['direction'] == 'outflow')}")
print(f"Categories: {sorted(set(e['category'] for e in entries))}")
print(f"Confidence: {sorted(set(e['confidence'] for e in entries))}")
```

- [ ] **Step 3: Commit sample data**

```bash
git -C apps/dcnet_sample add -A
git -C apps/dcnet_sample commit -m "feat: add sample data for cash flow forecast demo"
```

---

### Task 15: Browser QA + Final Verification

**Files:** None — QA only.

- [ ] **Step 1: Navigate to forecast page**

Open `/desk/cash-flow-forecast`. Verify:
- Page loads without console errors
- Chart renders with bar + line
- Table shows period rows with Opening/Inflow/Outflow/Net/Closing
- Default: Committed only checked

- [ ] **Step 2: Test filter interactions**

- Toggle "Probable" → more entries appear, chart updates instantly (no loading spinner)
- Toggle "Possible" → OpEx + Quotation entries appear
- Toggle "Overdue" → overdue SI/PI appear with red badge
- Change Period → refetch data (loading spinner)
- Change Company → refetch data

- [ ] **Step 3: Test drill-down**

Click a period row → expand shows individual entries with:
- Direction icons (↑/↓)
- Confidence badges (green/yellow/gray/red)
- Clickable source links → opens document in new tab

- [ ] **Step 4: Test source toggles**

- Uncheck "Sales Invoice" → SI entries disappear, chart updates
- Check "Quotation" → tooltip appears "requires Possible confidence"
- Check "Possible" → Quotation entries appear

- [ ] **Step 5: Test warning highlights**

- Verify Closing Balance < threshold → yellow row
- (If applicable with sample data) Closing Balance < 0 → red row

- [ ] **Step 6: Test Dashboard v2 integration**

Navigate to `/desk/vn-accounting-dashboard`. Verify:
- New "Dự Báo Dòng Tiền" chart appears after historical cash flow chart
- Shows committed only, 12 months
- Click chart → navigates to forecast page

- [ ] **Step 7: Test sidebar links**

Verify both sidebar items (under Quỹ tiền mặt + Ngân hàng) navigate to forecast page.

- [ ] **Step 8: Final commit if any fixes**

---

## Self-Review Notes

- ✓ **Spec coverage:** All 12 sections of spec mapped to tasks. §2 architecture → T1. §2.8 lifecycle → T4. §3 page → T12. §4 dashboard → T13. §5.1-5.5 providers → T3-T10. §6 edge cases → handled in provider implementations. §7 sidebar → T13. §8 translations → T13. §9 sample → T14. §10 testing → T1 (unit) + T15 (browser).
- ✓ **Placeholder scan:** No TBD/TODO. All tasks have concrete code or clear implementation instructions with spec references.
- ✓ **Type consistency:** `validate_entry()` signature consistent across T1 code + T1 tests. `get_all_forecast_entries(filters)` returns `(entries, errors)` — consistent in T1, T11, T14. Provider function signature `fn(filters) → list[dict]` consistent across T3-T10.
