# EInvoice App Rewrite — Design Spec

**Date:** 2026-03-31
**Repo:** goldrag1/einvoice
**Branch:** develop (from main)
**Goal:** Rewrite core modules to fix bugs, security gaps, and improve architecture

---

## 1. Scope

Stabilize the existing einvoice app by rewriting core modules. No new providers, no new features — only fix what's broken and restructure for maintainability.

### Out of Scope

- Implementing Viettel/MISA providers (stubs only, with friendly error)
- New DocTypes or UI pages
- Frontend redesign

---

## 2. Issues Addressed

| # | Severity | Issue |
|---|----------|-------|
| 1 | Critical | API endpoints (`api.py`) lack `frappe.only_for()` role guards — any authenticated user can call them |
| 2 | Critical | Auth tokens fetched on every API call, no caching |
| 3 | Bug | `dcnet_inward_invoice_list.js` calls `einvoice.einvoice.api.sync_inward_invoices()` which does not exist |
| 4 | Bug | `create_purchase_invoice()` creates PI without tax table — wrong totals |
| 5 | Bug | Scheduler crashes if EInvoice Settings doesn't exist yet |
| 6 | Bug | `run_if_frequency_match()` doesn't actually check time elapsed since last sync |
| 7 | Design | Stub providers (Viettel/MISA) raise raw `NotImplementedError` — bad UX |
| 8 | Design | No centralized error handling — mix of `frappe.throw`, bare `except`, inconsistent messages |
| 9 | Design | Business logic mixed into `api.py` (202 lines) — hard to test and audit |

---

## 3. Architecture — New File Structure

```
einvoice/einvoice/
├── __init__.py
├── hooks.py                          # Unchanged (keep 4 scheduler hooks)
├── install.py                        # Unchanged
├── api.py                            # REWRITE — thin layer, role guards, ~60 lines
├── exceptions.py                     # NEW — custom exception hierarchy
│
├── services/
│   ├── __init__.py
│   ├── issuance.py                   # NEW — invoice issuance logic (from api.py)
│   └── sync.py                       # NEW — sync logic (from tasks/__init__.py)
│
├── providers/
│   ├── __init__.py                   # Keep registry pattern
│   ├── base.py                       # REWRITE — token cache, _api_call(), shared logic
│   ├── matbao.py                     # REWRITE — inherit base, use _api_call()
│   ├── viettel.py                    # FIX — raise EInvoiceProviderNotReady
│   └── misa.py                       # FIX — raise EInvoiceProviderNotReady
│
├── tasks/
│   ├── __init__.py                   # SIMPLIFY — thin wrapper to services/sync.py
│   └── sync_inward_invoices.py       # SIMPLIFY — re-export
│
├── doctype/
│   ├── einvoice_inward/
│   │   ├── einvoice_inward.json      # UPDATE — add tax_rate field
│   │   └── einvoice_inward.py        # REWRITE — tax template matching
│   ├── einvoice_settings/
│   │   └── einvoice_settings.py      # FIX — delegate to services
│   ├── einvoice_provider/
│   │   └── einvoice_provider.py      # REFACTOR — use new exceptions
│   ├── einvoice_issuance_log/        # Unchanged
│   └── einvoice_sync_log/            # Unchanged
│
├── public/js/
│   ├── sales_invoice.js              # FIX — error handling for provider errors
│   ├── sales_invoice_list.js         # Unchanged
│   ├── einvoice_provider.js          # FIX — warning for stub providers
│   └── dcnet_inward_invoice_list.js  # FIX — call correct API endpoint
│
└── workspace/einvoice/
    └── einvoice.json                 # Already fixed (title/label → EInvoice)
```

**Summary: 3 new files, 4 rewrites, 5 fixes, 3 refactors, 1 schema update, 6 unchanged.**

---

## 4. Provider Base Class & Token Cache

### 4.1 BaseProvider (rewrite `providers/base.py`)

New concrete methods in BaseProvider:

**Token cache via Frappe Redis cache:**
- `_get_cached_token(token_type)` — cache key: `einvoice_token:{provider_name}:{token_type}`
- `_set_cached_token(token_type, token, ttl_seconds)` — default TTL 3500s (for 1h tokens)
- `authenticate()` — concrete method: check cache → if miss, call `_do_authenticate()` (abstract) → cache result
- Subclasses only implement `_do_authenticate()` returning `{tokens: [{type, token, ttl}]}`

**Shared HTTP helper:**
```python
def _api_call(self, method, url, **kwargs):
    # Default timeout 30s
    # Handle: Timeout → EInvoiceProviderError
    # Handle: HTTPError → EInvoiceProviderError with status code + response body[:500]
    # Handle: ConnectionError → EInvoiceProviderError
    # Return: parsed JSON
```

**Abstract methods (unchanged interface):**
- `_do_authenticate()` — NEW, replaces `authenticate()`
- `fetch_inward_invoices(from_date, to_date)`
- `parse_inward_invoice(raw_data)`
- `get_invoice_templates()`
- `issue_outward_invoice(payload)`
- `cancel_invoice(invoice_id, reason)`
- `map_sales_invoice_to_payload(si_doc, **kwargs)`

### 4.2 MatbaoProvider (rewrite `providers/matbao.py`)

- Implement `_do_authenticate()` returning 2 tokens: `{tokens: [{type: "purchase", token, ttl: 3500}, {type: "sales", token, ttl: 3500}]}`
- Replace all `requests.post/get` with `self._api_call()`
- Keep existing mapping/parse logic — only restructure for base class inheritance
- `parse_inward_invoice()`: add `tax_rate` extraction from `ThueSuat` field, fallback calculate from `tax_amount / total_before_tax * 100`

### 4.3 Stub Providers (fix `viettel.py`, `misa.py`)

All methods raise `EInvoiceProviderNotReady(provider_type)` instead of `NotImplementedError`.

---

## 5. API Layer Rewrite

### 5.1 `api.py` — Thin Layer (~60 lines)

Every endpoint gets `frappe.only_for(["System Manager", "Accounts Manager"])` as first line.

```python
@frappe.whitelist()
def issue_single_invoice(sales_invoice, provider=None, pattern=None, serial=None, issue_mode=None):
    frappe.only_for(["System Manager", "Accounts Manager"])
    return IssuanceService.issue_single(sales_invoice, provider, pattern, serial, issue_mode)

@frappe.whitelist()
def issue_bulk_invoices(sales_invoices, provider=None, pattern=None, serial=None, issue_mode=None):
    frappe.only_for(["System Manager", "Accounts Manager"])
    return IssuanceService.issue_bulk(sales_invoices, provider, pattern, serial, issue_mode)

@frappe.whitelist()
def get_providers(company=None):
    frappe.only_for(["System Manager", "Accounts Manager"])
    filters = {"enabled": 1}
    if company:
        filters["company"] = company
    return frappe.get_all("EInvoice Provider", filters=filters,
        fields=["name", "provider_name", "provider_type",
                "default_invoice_pattern", "default_invoice_serial"])

@frappe.whitelist()
def sync_inward_invoices():  # Fixes bug #3
    frappe.only_for(["System Manager", "Accounts Manager"])
    return SyncService.run_sync(sync_type="Manual")

@frappe.whitelist()
def has_app_permission():
    # Unchanged — used for app screen permission
```

### 5.2 `services/issuance.py` — IssuanceService

**`issue_single(sales_invoice, provider, pattern, serial, issue_mode)`:**
1. Validate: SI submitted, not already issued
2. Resolve provider by company if not specified
3. Try provider flow: `authenticate()` → `map_sales_invoice_to_payload()` → `issue_outward_invoice()`
4. Catch `EInvoiceProviderNotReady` → return `{success: False, message: friendly_msg}`
5. Catch `EInvoiceProviderError` → log error + return `{success: False, message, detail}`
6. On success: create `EInvoice Issuance Log`, update SI custom fields
7. Return `{success: True, invoice_number, lookup_code, pdf_url}`

**`issue_bulk(sales_invoices, ...)`:**
1. Validate count <= `bulk_issuance_limit` from Settings
2. `> 5` invoices → `frappe.enqueue()` with `queue='long'`, `timeout=1200`
3. `<= 5` → inline loop calling `issue_single()` for each
4. Return `{success, message, results[], background}`

### 5.3 `services/sync.py` — SyncService

Move all logic from `tasks/__init__.py`:
- `run_if_frequency_match()` — with proper guards (see Section 7)
- `run_sync(sync_type)` → `_sync_provider()` → `_try_auto_match()`
- `_create_sync_log()`

---

## 6. Purchase Invoice Tax Template Matching

### 6.1 `einvoice_inward.json` — New Field

```json
{
    "fieldname": "tax_rate",
    "fieldtype": "Percent",
    "label": "Tax Rate (%)",
    "read_only": 1,
    "insert_after": "tax_amount"
}
```

### 6.2 `einvoice_inward.py` — Auto-Calculate Tax Rate

In `validate()`:
```python
if not self.tax_rate and self.total_before_tax:
    self.tax_rate = (self.tax_amount or 0) / self.total_before_tax * 100
```

### 6.3 `create_purchase_invoice()` — Tax Template Resolution

**`_resolve_tax_template()` logic:**

1. Calculate `actual_rate` from inward invoice: `tax_amount / total_before_tax * 100` (round to 0 decimal)
2. Fetch all `Purchase Taxes and Charges Template` for the company
3. For each template, read `taxes` child table → find row with `charge_type = "On Net Total"` → get `rate`
4. **Exact match:** find template where `rate == actual_rate`
5. If 1 match → use it
6. If multiple matches → prefer `is_default=1`, else take first
7. If no match → fallback to `is_default=1` + `frappe.msgprint` warning: "Không tìm thấy mẫu thuế {actual_rate}%. Đang dùng mẫu mặc định."
8. If no template at all → `frappe.throw()` with guidance: "Công ty {company} chưa có Purchase Taxes and Charges Template mặc định. Vui lòng tạo tại: /app/purchase-taxes-and-charges-template/new"

**PI creation flow:**
1. Find/create supplier via `_get_or_create_supplier()`
2. Resolve tax template via `_resolve_tax_template()`
3. Create PI with line item using `total_before_tax`
4. Set `pi.taxes_and_charges = template.name` → call `pi.set_taxes()`
5. Compare `pi.total_taxes_and_charges` vs `self.tax_amount` — if >1% difference → msgprint warning
6. Save PI, update cross-links

---

## 7. Scheduler & Frequency Check

### 7.1 `run_if_frequency_match()` in `services/sync.py`

```python
def run_if_frequency_match():
    # 1. Guard: Settings doesn't exist → silent return
    if not frappe.db.exists("EInvoice Settings", "EInvoice Settings"):
        return

    settings = frappe.get_single("EInvoice Settings")
    if not settings.enable_auto_sync or not settings.sync_frequency:
        return

    # 2. Map frequency to seconds
    freq_map = {
        "Every 15 Min": 900,
        "Hourly": 3600,
        "Every 6 Hours": 21600,
        "Daily": 86400,
        "Weekly": 604800,
    }
    min_interval = freq_map.get(settings.sync_frequency)
    if not min_interval:
        return

    # 3. Check elapsed time since last sync
    if settings.last_sync_datetime:
        elapsed = (now_datetime() - settings.last_sync_datetime).total_seconds()
        if elapsed < min_interval:
            return

    # 4. Distributed lock via Redis (TTL 5 min)
    lock_key = "einvoice_sync_running"
    if frappe.cache.get_value(lock_key):
        return
    frappe.cache.set_value(lock_key, 1, expires_in_sec=300)

    try:
        SyncService.run_sync(sync_type="Scheduled")
    finally:
        frappe.cache.delete_key(lock_key)
```

### 7.2 `tasks/__init__.py` — Thin Wrapper

```python
from einvoice.einvoice.services.sync import run_if_frequency_match, SyncService

def run_sync(sync_type="Manual"):
    return SyncService.run_sync(sync_type=sync_type)
```

Keeps backward compatibility with hooks.py import paths.

---

## 8. Custom Exceptions (`exceptions.py`)

```python
class EInvoiceError(Exception):
    """Base exception"""
    def __init__(self, message, detail=None):
        self.message = message
        self.detail = detail
        super().__init__(message)

class EInvoiceProviderError(EInvoiceError):
    """Provider API error (auth, network, bad response)"""
    def __init__(self, message, provider=None, detail=None):
        self.provider = provider
        super().__init__(message, detail)

class EInvoiceProviderNotReady(EInvoiceError):
    """Provider not yet implemented"""
    def __init__(self, provider_type):
        msg = f"Provider {provider_type} chưa được hỗ trợ. Vui lòng liên hệ DCNET (info@dcnet.vn)."
        super().__init__(msg)

class EInvoiceValidationError(EInvoiceError):
    """Data validation error"""
    pass

class EInvoiceTaxTemplateError(EInvoiceError):
    """Tax template not found or mismatch"""
    pass
```

### Error handling rules

| Layer | Behavior |
|---|---|
| `providers/` | Raise `EInvoiceProviderError` or `EInvoiceProviderNotReady` — never catch internally |
| `services/` | Catch provider errors → log via `log_einvoice_error()` → return `{success: False, message}` |
| `api.py` | Catch service errors → return response dict for JS client |
| DocType controllers | Catch specific errors → `frappe.throw()` with Vietnamese message for end user |

### Logging helper

```python
def log_einvoice_error(title, message, provider=None):
    frappe.log_error(
        title=f"[EInvoice] {title}",
        message=message,
        reference_doctype="EInvoice Provider" if provider else None,
        reference_name=provider,
    )
```

---

## 9. JS Fixes

### 9.1 `dcnet_inward_invoice_list.js` — Fix bug #3

Call the now-existing endpoint:
```javascript
frappe.call({
    method: "einvoice.einvoice.api.sync_inward_invoices",
    freeze: true,
    freeze_message: __("Đang đồng bộ hóa đơn đầu vào..."),
    callback: function(r) {
        if (r.message) frappe.msgprint(r.message);
        cur_list.refresh();
    }
});
```

### 9.2 `sales_invoice.js` — Error handling

Add handling for `{success: false}` responses from `issue_single_invoice`:
```javascript
if (r.message && !r.message.success) {
    frappe.msgprint({title: __("Lỗi"), message: r.message.message, indicator: "red"});
    return;
}
```

### 9.3 `einvoice_provider.js` — Stub warning

On `provider_type` change to Viettel/MISA:
```javascript
if (["Viettel", "MISA"].includes(frm.doc.provider_type)) {
    frappe.msgprint(__("Provider {0} chưa được hỗ trợ. Vui lòng liên hệ DCNET.", [frm.doc.provider_type]));
}
```

---

## 10. Change Summary

| Type | Count | Files |
|---|---|---|
| NEW | 3 | `exceptions.py`, `services/issuance.py`, `services/sync.py` |
| REWRITE | 4 | `api.py`, `providers/base.py`, `providers/matbao.py`, `einvoice_inward.py` |
| FIX | 5 | `viettel.py`, `misa.py`, `sales_invoice.js`, `einvoice_provider.js`, `dcnet_inward_invoice_list.js` |
| REFACTOR | 3 | `tasks/__init__.py`, `einvoice_settings.py`, `einvoice_provider.py` |
| SCHEMA | 0 | `einvoice_inward.json` already has `tax_rate` field — no change needed |
| UNCHANGED | 6 | `hooks.py`, `install.py`, `einvoice_settings.json`, `einvoice_provider.json`, issuance_log, sync_log |

**Total: 16 files changed, 3 files new.**

---

## 11. Testing Strategy

1. **Unit test per service:** `test_issuance.py`, `test_sync.py`
2. **Provider test:** mock HTTP responses, verify token cache behavior
3. **Tax template matching:** test with 0%, 5%, 8%, 10% rates + missing template scenario
4. **Scheduler:** test frequency check with mocked `last_sync_datetime`
5. **Integration:** full flow — sync inward → auto-match → create PI with tax
