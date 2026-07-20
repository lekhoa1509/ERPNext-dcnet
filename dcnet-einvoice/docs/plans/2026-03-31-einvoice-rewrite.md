# EInvoice Rewrite Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rewrite einvoice core modules to fix bugs, security gaps, and improve architecture while maintaining backward compatibility with existing hooks.py import paths.

**Architecture:** Extract business logic from api.py into services/ layer, add token caching and shared HTTP helpers to provider base class, add role guards to all API endpoints, fix tax template matching for PI creation, fix scheduler frequency check, and fix broken JS references.

**Tech Stack:** Frappe v16, ERPNext v16, Python 3.14, MariaDB, Redis (for token cache)

**Repo:** `apps/einvoice/` (git remote: `goldrag1/einvoice`, branch: `develop` from `main`)

**Spec:** `docs/superpowers/specs/2026-03-31-einvoice-rewrite-design.md`

---

## File Map

| Action | File | Responsibility |
|--------|------|---------------|
| CREATE | `einvoice/einvoice/exceptions.py` | Custom exception hierarchy |
| CREATE | `einvoice/einvoice/services/__init__.py` | Package init |
| CREATE | `einvoice/einvoice/services/issuance.py` | Invoice issuance logic (extracted from api.py) |
| CREATE | `einvoice/einvoice/services/sync.py` | Sync logic (extracted from tasks/__init__.py) + frequency check |
| REWRITE | `einvoice/einvoice/api.py` | Thin API layer with role guards |
| REWRITE | `einvoice/einvoice/providers/base.py` | Token cache, `_api_call()`, shared logic |
| REWRITE | `einvoice/einvoice/providers/matbao.py` | Use base class helpers |
| FIX | `einvoice/einvoice/providers/viettel.py` | Use `EInvoiceProviderNotReady` |
| FIX | `einvoice/einvoice/providers/misa.py` | Use `EInvoiceProviderNotReady` |
| REWRITE | `einvoice/einvoice/doctype/einvoice_inward/einvoice_inward.py` | Tax template matching in `create_purchase_invoice()` |
| REFACTOR | `einvoice/einvoice/doctype/einvoice_settings/einvoice_settings.py` | Delegate to services |
| REFACTOR | `einvoice/einvoice/doctype/einvoice_provider/einvoice_provider.py` | Use new exceptions |
| SIMPLIFY | `einvoice/einvoice/tasks/__init__.py` | Thin wrapper to services/sync.py |
| SIMPLIFY | `einvoice/einvoice/tasks/sync_inward_invoices.py` | Re-export only |
| FIX | `einvoice/public/js/sales_invoice.js` | Error handling for provider errors |
| FIX | `einvoice/public/js/einvoice_provider.js` | Warning for stub providers |
| FIX | `einvoice/public/js/dcnet_inward_invoice_list.js` | Fix doctype name + API call |
| FIX | `einvoice/einvoice/hooks.py` | Add EInvoice Inward list JS hook |

---

### Task 1: Create branch and exceptions module

**Files:**
- Create: `einvoice/einvoice/exceptions.py`

- [ ] **Step 1: Create develop branch**

```bash
cd /home/long/long/frappe-bench-das/apps/einvoice
git checkout -b develop main
```

- [ ] **Step 2: Create exceptions.py**

Create file `einvoice/einvoice/exceptions.py`:

```python
"""
Custom exceptions for EInvoice app.

Hierarchy:
    EInvoiceError
    ├── EInvoiceProviderError      — API/network errors from providers
    ├── EInvoiceProviderNotReady   — Stub provider not yet implemented
    ├── EInvoiceValidationError    — Data validation failures
    └── EInvoiceTaxTemplateError   — Tax template not found/mismatch
"""


class EInvoiceError(Exception):
    """Base exception for all EInvoice errors."""

    def __init__(self, message, detail=None):
        self.message = message
        self.detail = detail
        super().__init__(message)


class EInvoiceProviderError(EInvoiceError):
    """Error from provider API (auth, network, bad response)."""

    def __init__(self, message, provider=None, detail=None):
        self.provider = provider
        super().__init__(message, detail)


class EInvoiceProviderNotReady(EInvoiceError):
    """Provider type not yet implemented."""

    def __init__(self, provider_type):
        msg = f"Provider {provider_type} chưa được hỗ trợ. Vui lòng liên hệ DCNET (info@dcnet.vn)."
        super().__init__(msg)


class EInvoiceValidationError(EInvoiceError):
    """Data validation error."""
    pass


class EInvoiceTaxTemplateError(EInvoiceError):
    """Tax template not found or mismatch."""
    pass
```

- [ ] **Step 3: Commit**

```bash
git add einvoice/einvoice/exceptions.py
git commit -m "feat: add custom exception hierarchy for einvoice"
```

---

### Task 2: Rewrite provider base class with token cache and _api_call

**Files:**
- Rewrite: `einvoice/einvoice/providers/base.py`

- [ ] **Step 1: Rewrite base.py**

Replace entire content of `einvoice/einvoice/providers/base.py`:

```python
"""
Abstract base class for all E-Invoice providers.

Provides:
- Token cache via Frappe Redis cache
- Shared HTTP helper with error handling
- Abstract methods for subclasses to implement
"""

from abc import ABC, abstractmethod

import requests
import frappe

from einvoice.einvoice.exceptions import EInvoiceProviderError


class BaseProvider(ABC):
    """Strategy interface for E-Invoice providers."""

    def __init__(self, provider_doc):
        """
        Args:
            provider_doc: frappe Document of type 'EInvoice Provider'
        """
        self.provider_doc = provider_doc
        self.provider_name = provider_doc.name
        self.api_url = provider_doc.api_url
        self.api_url_purchase = provider_doc.api_url_purchase or provider_doc.api_url
        self.tax_code = provider_doc.tax_code

    # ------------------------------------------------------------------
    # Token Cache
    # ------------------------------------------------------------------
    def _cache_key(self, token_type):
        return f"einvoice_token:{self.provider_name}:{token_type}"

    def _get_cached_token(self, token_type):
        """Get token from Redis cache. Returns None if not cached or expired."""
        return frappe.cache.get_value(self._cache_key(token_type))

    def _set_cached_token(self, token_type, token, ttl_seconds=3500):
        """Store token in Redis cache with TTL (default 3500s for 1h tokens)."""
        frappe.cache.set_value(self._cache_key(token_type), token, expires_in_sec=ttl_seconds)

    def _clear_cached_tokens(self):
        """Clear all cached tokens for this provider."""
        for token_type in ("purchase", "sales", "default"):
            frappe.cache.delete_key(self._cache_key(token_type))

    def authenticate(self):
        """
        Authenticate with the provider API using cached tokens when available.

        Checks cache first. On cache miss, calls _do_authenticate() and caches
        the returned tokens.

        Returns:
            dict of {token_type: token_string}
        """
        # Try cache first
        result = self._do_authenticate_cached()
        if result:
            return result

        # Cache miss — authenticate fresh
        auth_result = self._do_authenticate()
        tokens = auth_result.get("tokens", [])

        token_dict = {}
        for t in tokens:
            self._set_cached_token(t["type"], t["token"], t.get("ttl", 3500))
            token_dict[t["type"]] = t["token"]

        return token_dict

    def _do_authenticate_cached(self):
        """Try to load all required tokens from cache. Returns dict or None."""
        token_types = self._required_token_types()
        result = {}
        for tt in token_types:
            cached = self._get_cached_token(tt)
            if not cached:
                return None
            result[tt] = cached
        return result

    def _required_token_types(self):
        """Return list of token type strings this provider needs.
        Override in subclass if provider uses multiple tokens."""
        return ["default"]

    # ------------------------------------------------------------------
    # HTTP Helper
    # ------------------------------------------------------------------
    def _api_call(self, method, url, headers=None, **kwargs):
        """
        Make an HTTP request with standardized error handling.

        Args:
            method: HTTP method string ("GET", "POST", etc.)
            url: Full URL
            headers: Optional headers dict
            **kwargs: Passed to requests.request (json, params, data, etc.)

        Returns:
            Parsed JSON response

        Raises:
            EInvoiceProviderError on timeout, HTTP error, or connection error
        """
        kwargs.setdefault("timeout", 30)
        kwargs.setdefault("verify", True)

        try:
            resp = requests.request(method, url, headers=headers, **kwargs)
            resp.raise_for_status()
            return resp.json()
        except requests.Timeout:
            raise EInvoiceProviderError(
                "API timeout",
                provider=self.provider_name,
                detail=f"URL: {url}, timeout: {kwargs.get('timeout')}s",
            )
        except requests.HTTPError as e:
            body = e.response.text[:500] if e.response is not None else ""
            raise EInvoiceProviderError(
                f"HTTP {e.response.status_code}" if e.response is not None else "HTTP error",
                provider=self.provider_name,
                detail=body,
            )
        except requests.ConnectionError:
            raise EInvoiceProviderError(
                "Không kết nối được tới API",
                provider=self.provider_name,
                detail=f"URL: {url}",
            )

    # ------------------------------------------------------------------
    # Abstract Methods — subclasses must implement
    # ------------------------------------------------------------------
    @abstractmethod
    def _do_authenticate(self) -> dict:
        """
        Perform actual authentication with the provider API.

        Returns:
            dict with key "tokens": list of {type: str, token: str, ttl: int}
            Example: {"tokens": [{"type": "sales", "token": "jwt...", "ttl": 3500}]}
        """
        ...

    @abstractmethod
    def fetch_inward_invoices(self, from_date: str, to_date: str) -> list[dict]:
        """Fetch inward invoices from the provider. Returns list of raw dicts."""
        ...

    @abstractmethod
    def parse_inward_invoice(self, raw_data: dict) -> dict:
        """Parse a raw invoice dict into standardized EInvoice Inward fields."""
        ...

    @abstractmethod
    def get_invoice_templates(self) -> list[dict]:
        """Fetch available invoice templates from the provider."""
        ...

    @abstractmethod
    def issue_outward_invoice(self, invoice_data: dict) -> dict:
        """Issue an outward invoice. Returns dict with success, invoice_number, etc."""
        ...

    @abstractmethod
    def cancel_invoice(self, invoice_ref: str, reason: str) -> bool:
        """Cancel a previously issued invoice."""
        ...

    @abstractmethod
    def map_sales_invoice_to_payload(self, si_doc, settings_doc) -> dict:
        """Convert ERPNext Sales Invoice to provider-specific payload."""
        ...
```

- [ ] **Step 2: Commit**

```bash
git add einvoice/einvoice/providers/base.py
git commit -m "refactor: rewrite BaseProvider with token cache and _api_call helper"
```

---

### Task 3: Rewrite MatbaoProvider to use base class helpers

**Files:**
- Rewrite: `einvoice/einvoice/providers/matbao.py`

- [ ] **Step 1: Rewrite matbao.py**

Replace entire content of `einvoice/einvoice/providers/matbao.py`:

```python
"""
Mắt Bão (Mifi) E-Invoice Provider Implementation.

API Documentation:
- Purchase (Inward):  POST /auth/token → GET /hoa-don-dau-vao/load-data-tct
- Sales (Outward):    POST /api/auth/login → POST /api/invoice/create-invoice
"""

import json

import frappe
from frappe.utils import now_datetime, flt

from einvoice.einvoice.providers.base import BaseProvider
from einvoice.einvoice.exceptions import EInvoiceProviderError


class MatbaoProvider(BaseProvider):
    """Full implementation for Mắt Bão (Mifi) E-Invoice service."""

    def _required_token_types(self):
        return ["purchase", "sales"]

    # ------------------------------------------------------------------
    # Authentication
    # ------------------------------------------------------------------
    def _do_authenticate(self) -> dict:
        """Authenticate with both Mắt Bão APIs (purchase + sales)."""
        purchase_token = self._authenticate_purchase()
        sales_token = self._authenticate_sales()
        return {
            "tokens": [
                {"type": "purchase", "token": purchase_token, "ttl": 3500},
                {"type": "sales", "token": sales_token, "ttl": 3500},
            ]
        }

    def _authenticate_purchase(self) -> str:
        """Authenticate with the Purchase (Inward) API."""
        token = self.provider_doc.get_password("api_token")
        if not token:
            raise EInvoiceProviderError(
                "Thiếu token xác thực cho API Hóa đơn mua vào.",
                provider=self.provider_name,
            )

        url = f"{self.api_url_purchase}/auth/token"
        data = self._api_call("POST", url, json={"token": token})

        jwt_token = data.get("data", {}).get("accessToken") or data.get("token", "")
        if not jwt_token and isinstance(data, str):
            jwt_token = data

        if not jwt_token:
            raise EInvoiceProviderError(
                "Không nhận được token từ API purchase.",
                provider=self.provider_name,
                detail=str(data)[:500],
            )

        return jwt_token

    def _authenticate_sales(self) -> str:
        """Authenticate with the Sales (Outward) API."""
        username = self.provider_doc.api_username
        password = self.provider_doc.get_password("api_password")

        if not username or not password:
            raise EInvoiceProviderError(
                "Thiếu username/password cho API Hóa đơn bán ra.",
                provider=self.provider_name,
            )

        url = f"{self.api_url}/api/auth/login"
        data = self._api_call("POST", url, json={
            "MST": self.tax_code,
            "TDNhap": username,
            "MKhau": password,
        })

        if not data.get("success"):
            raise EInvoiceProviderError(
                f"Login thất bại: {data.get('message', 'Lỗi không xác định')}",
                provider=self.provider_name,
            )

        return data["data"]["accessToken"]

    def _get_auth_headers(self, token_type):
        """Get Authorization header for the given token type."""
        token = self._get_cached_token(token_type)
        if not token:
            # Re-authenticate if token expired
            self.authenticate()
            token = self._get_cached_token(token_type)
        return {"Authorization": f"Bearer {token}"}

    # ------------------------------------------------------------------
    # Inward Invoices (Purchase)
    # ------------------------------------------------------------------
    def fetch_inward_invoices(self, from_date: str, to_date: str) -> list[dict]:
        """Fetch inward invoices from Mắt Bão's TCT sync endpoint."""
        headers = self._get_auth_headers("purchase")
        url = f"{self.api_url_purchase}/hoa-don-dau-vao/load-data-tct"

        body = {
            "comName": "",
            "comTaxCode": "",
            "no": "",
            "fromDateYMD": from_date,
            "toDateYMD": f"{to_date} 23:59:59",
            "trangthai": -1,
            "loaihoadon": -1,
            "pattern": "",
            "serial": "",
        }

        data = self._api_call("GET", url, headers=headers, json=body, timeout=60)

        if isinstance(data, list):
            return data
        if isinstance(data, dict) and "data" in data:
            return data["data"] if isinstance(data["data"], list) else []
        return []

    def parse_inward_invoice(self, raw_data: dict) -> dict:
        """Parse a Mắt Bão inward invoice into standardized format."""
        total_before_tax = flt(raw_data.get("tgTCThue", raw_data.get("TgTCThue", 0)))
        tax_amount = flt(raw_data.get("tgTThue", raw_data.get("TgTThue", 0)))

        # Extract tax rate from API field or calculate
        tax_rate = flt(raw_data.get("thueSuat", raw_data.get("ThueSuat", 0)))
        if not tax_rate and total_before_tax:
            tax_rate = round(tax_amount / total_before_tax * 100, 0)

        return {
            "lookup_code": raw_data.get("maTraCuu", raw_data.get("MaTraCuu", "")),
            "provider_invoice_id": str(raw_data.get("id", raw_data.get("Id", ""))),
            "invoice_number": str(raw_data.get("shDon", raw_data.get("SHDon", ""))),
            "invoice_pattern": raw_data.get("khmshDon", raw_data.get("KHMSHDon", "")),
            "invoice_serial": raw_data.get("khhDon", raw_data.get("KHHDon", "")),
            "invoice_date": (raw_data.get("nLap") or raw_data.get("NLap", ""))[:10] or None,
            "invoice_type": self._map_invoice_type(
                raw_data.get("khmshDon", raw_data.get("KHMSHDon", ""))
            ),
            "supplier_name": raw_data.get("tenNBan", raw_data.get("TenNBan", "")),
            "supplier_tax_code": raw_data.get("mstNBan", raw_data.get("MSTNBan", "")),
            "supplier_address": raw_data.get("dchiNBan", raw_data.get("DChiNBan", "")),
            "total_before_tax": total_before_tax,
            "tax_rate": tax_rate,
            "tax_amount": tax_amount,
            "total_amount": flt(raw_data.get("tgTTTBSo", raw_data.get("TgTTTBSo", 0))),
            "currency": "VND",
            "pdf_url": raw_data.get("urlDownloadPDF", ""),
            "raw_data": json.dumps(raw_data, ensure_ascii=False, default=str),
        }

    @staticmethod
    def _map_invoice_type(khmshdon: str) -> str:
        """Map Mắt Bão invoice pattern to standardized type."""
        mapping = {"1": "GTGT", "2": "Bán hàng"}
        return mapping.get(str(khmshdon), "Khác")

    # ------------------------------------------------------------------
    # Outward Invoices (Sales)
    # ------------------------------------------------------------------
    def get_invoice_templates(self) -> list[dict]:
        """Fetch available invoice templates from Mắt Bão."""
        from datetime import datetime

        headers = self._get_auth_headers("sales")
        url = f"{self.api_url}/api/invoice/templates"
        params = {"year": str(datetime.now().year)}

        data = self._api_call("GET", url, headers=headers, params=params)

        if data.get("success"):
            return data.get("data", [])
        return []

    def issue_outward_invoice(self, invoice_data: dict) -> dict:
        """Issue an outward invoice via Mắt Bão API."""
        headers = self._get_auth_headers("sales")
        url = f"{self.api_url}/api/invoice/create-invoice"

        # API expects a list of invoice objects
        data = self._api_call("POST", url, headers=headers, json=[invoice_data], timeout=60)

        if not data.get("success"):
            return {
                "success": False,
                "invoice_number": None,
                "lookup_code": None,
                "pdf_url": None,
                "xml_url": None,
                "raw_response": data,
                "error": data.get("message", "Lỗi không xác định"),
            }

        result = data["data"][0] if data.get("data") else {}
        result_data = result.get("data", {})

        return {
            "success": result.get("success", False),
            "invoice_number": str(result_data.get("shDon", "")),
            "lookup_code": result_data.get("maTraCuu", ""),
            "maso_hdon": result_data.get("maSoHDon", ""),
            "pdf_url": result_data.get("urlDownloadPDF", ""),
            "xml_url": result_data.get("urlDownloadXML", ""),
            "raw_response": data,
        }

    def cancel_invoice(self, invoice_ref: str, reason: str) -> bool:
        """Cancel an invoice on Mắt Bão."""
        headers = self._get_auth_headers("sales")
        url = f"{self.api_url}/api/invoice/cancel-invoice"

        data = self._api_call("POST", url, headers=headers, json={
            "MaSoHDon": invoice_ref,
            "LDo": reason,
        })

        return data.get("success", False)

    # ------------------------------------------------------------------
    # Data Mapping
    # ------------------------------------------------------------------
    def map_sales_invoice_to_payload(self, si_doc, settings_doc) -> dict:
        """Convert an ERPNext Sales Invoice into Mắt Bão create-invoice payload."""
        provider = self.provider_doc
        issue_mode = 0 if settings_doc.default_issue_mode == "Draft" else 1

        items = []
        for idx, item in enumerate(si_doc.items, start=1):
            tax_rate = self._get_item_tax_rate(si_doc, item)
            tax_amount = flt(item.amount * tax_rate / 100, 2)

            items.append({
                "TChat": 1,
                "STT": idx,
                "MHHDVu": item.item_code or "",
                "THHDVu": item.item_name or "",
                "DVTinh": item.uom or "",
                "SLuong": flt(item.qty),
                "DGia": flt(item.rate),
                "ThTienChuaCK": flt(item.amount),
                "TLCKhau": flt(item.discount_percentage) if hasattr(item, "discount_percentage") else 0,
                "STCKhau": flt(item.discount_amount) if hasattr(item, "discount_amount") else 0,
                "ThTien": flt(item.amount),
                "TSuat": tax_rate,
                "TThue": tax_amount,
                "TgTien": flt(item.amount) + tax_amount,
            })

        lookup = f"{si_doc.name}_{now_datetime().strftime('%Y%m%d%H%M%S')}"

        customer_tax_id = si_doc.tax_id or ""
        if not customer_tax_id and si_doc.customer:
            customer_tax_id = frappe.db.get_value("Customer", si_doc.customer, "tax_id") or ""

        return {
            "KHMSHDon": provider.default_invoice_pattern or "1",
            "KHHDon": provider.default_invoice_serial or "",
            "MaTraCuu": lookup,
            "MTChieu": lookup,
            "NLap": f"{si_doc.posting_date}T00:00:00",
            "LoaiHDon": issue_mode,
            "TCHDon": 0,
            "LoaiTraHang": 0,
            "DVTTe": 704,
            "TGia": 1000.00,
            "HTTToan": settings_doc.default_payment_method or "Chuyển khoản",
            "GChu": si_doc.remarks or "",
            "NMua_Ten": si_doc.customer_name or "",
            "NMua_MST": customer_tax_id,
            "NMua_DChi": si_doc.customer_address or frappe.db.get_value(
                "Address", si_doc.customer_address, "address_line1"
            ) or "",
            "NMua_MKHang": si_doc.customer or "",
            "NMua_SDThoai": getattr(si_doc, "contact_mobile", ""),
            "NMua_DCTDTu": getattr(si_doc, "contact_email", ""),
            "NMua_HVTNMHang": "",
            "NMua_STKNHang": "",
            "NMua_TNHang": "",
            "DSHHDVu": items,
            "TTCKTMai": flt(si_doc.discount_amount) if hasattr(si_doc, "discount_amount") else 0,
            "TGTKhac": 0,
            "TgThTien": flt(si_doc.total),
            "TgTThue": flt(si_doc.total_taxes_and_charges),
            "TgTTTBSo": flt(si_doc.grand_total),
            "TgTTTBChu": si_doc.in_words or "",
        }

    @staticmethod
    def _get_item_tax_rate(si_doc, item):
        """Extract the VAT tax rate for an item from the Sales Invoice tax table."""
        for tax in si_doc.taxes:
            if "VAT" in (tax.description or "").upper() or "GTGT" in (tax.description or "").upper():
                return flt(tax.rate)
        if hasattr(item, "item_tax_rate") and item.item_tax_rate:
            try:
                rates = json.loads(item.item_tax_rate)
                for account, rate in rates.items():
                    return flt(rate)
            except Exception:
                pass
        return 0
```

- [ ] **Step 2: Commit**

```bash
git add einvoice/einvoice/providers/matbao.py
git commit -m "refactor: rewrite MatbaoProvider with token cache and _api_call"
```

---

### Task 4: Fix stub providers

**Files:**
- Fix: `einvoice/einvoice/providers/viettel.py`
- Fix: `einvoice/einvoice/providers/misa.py`

- [ ] **Step 1: Rewrite viettel.py**

Replace entire content of `einvoice/einvoice/providers/viettel.py`:

```python
"""Viettel S-Invoice Provider — Stub for future implementation."""

from einvoice.einvoice.providers.base import BaseProvider
from einvoice.einvoice.exceptions import EInvoiceProviderNotReady


class ViettelProvider(BaseProvider):

    def _do_authenticate(self):
        raise EInvoiceProviderNotReady("Viettel")

    def fetch_inward_invoices(self, from_date, to_date):
        raise EInvoiceProviderNotReady("Viettel")

    def parse_inward_invoice(self, raw_data):
        raise EInvoiceProviderNotReady("Viettel")

    def get_invoice_templates(self):
        raise EInvoiceProviderNotReady("Viettel")

    def issue_outward_invoice(self, invoice_data):
        raise EInvoiceProviderNotReady("Viettel")

    def cancel_invoice(self, invoice_ref, reason):
        raise EInvoiceProviderNotReady("Viettel")

    def map_sales_invoice_to_payload(self, si_doc, settings_doc):
        raise EInvoiceProviderNotReady("Viettel")
```

- [ ] **Step 2: Rewrite misa.py**

Replace entire content of `einvoice/einvoice/providers/misa.py`:

```python
"""MISA meInvoice Provider — Stub for future implementation."""

from einvoice.einvoice.providers.base import BaseProvider
from einvoice.einvoice.exceptions import EInvoiceProviderNotReady


class MisaProvider(BaseProvider):

    def _do_authenticate(self):
        raise EInvoiceProviderNotReady("MISA")

    def fetch_inward_invoices(self, from_date, to_date):
        raise EInvoiceProviderNotReady("MISA")

    def parse_inward_invoice(self, raw_data):
        raise EInvoiceProviderNotReady("MISA")

    def get_invoice_templates(self):
        raise EInvoiceProviderNotReady("MISA")

    def issue_outward_invoice(self, invoice_data):
        raise EInvoiceProviderNotReady("MISA")

    def cancel_invoice(self, invoice_ref, reason):
        raise EInvoiceProviderNotReady("MISA")

    def map_sales_invoice_to_payload(self, si_doc, settings_doc):
        raise EInvoiceProviderNotReady("MISA")
```

- [ ] **Step 3: Commit**

```bash
git add einvoice/einvoice/providers/viettel.py einvoice/einvoice/providers/misa.py
git commit -m "fix: stub providers raise EInvoiceProviderNotReady instead of NotImplementedError"
```

---

### Task 5: Create services layer — issuance.py

**Files:**
- Create: `einvoice/einvoice/services/__init__.py`
- Create: `einvoice/einvoice/services/issuance.py`

- [ ] **Step 1: Create services/__init__.py**

Create file `einvoice/einvoice/services/__init__.py`:

```python
```

(Empty file — package marker only.)

- [ ] **Step 2: Create services/issuance.py**

Create file `einvoice/einvoice/services/issuance.py`:

```python
"""
Invoice Issuance Service.

Handles single and bulk outward invoice issuance via providers.
Extracted from api.py for testability and separation of concerns.
"""

import json

import frappe
from frappe.utils import now_datetime, flt

from einvoice.einvoice.exceptions import (
    EInvoiceProviderError,
    EInvoiceProviderNotReady,
)


def log_einvoice_error(title, message, provider=None):
    """Log error with [EInvoice] prefix for easy filtering."""
    frappe.log_error(
        title=f"[EInvoice] {title}",
        message=message,
        reference_doctype="EInvoice Provider" if provider else None,
        reference_name=provider,
    )


class IssuanceService:
    """Service class for invoice issuance operations."""

    @staticmethod
    def issue_single(sales_invoice, provider=None, pattern=None, serial=None, issue_mode=None):
        """
        Issue a single outward e-invoice from a submitted Sales Invoice.

        Returns:
            dict with keys: success, message, invoice_number, lookup_code, pdf_url
        """
        si_doc = frappe.get_doc("Sales Invoice", sales_invoice)

        # Validations
        if si_doc.docstatus != 1:
            return {"success": False, "message": "Chỉ có thể xuất hóa đơn đỏ cho Sales Invoice đã Submit."}
        if si_doc.einvoice_issued:
            return {"success": False, "message": "Sales Invoice này đã xuất hóa đơn đỏ rồi."}

        settings = frappe.get_single("EInvoice Settings")
        provider_doc = _resolve_provider(si_doc, provider, settings)
        provider_name = provider_doc.name

        # Override pattern/serial if provided
        if pattern:
            provider_doc.default_invoice_pattern = pattern
        if serial:
            provider_doc.default_invoice_serial = serial
        if issue_mode:
            settings.default_issue_mode = issue_mode

        try:
            provider_instance = provider_doc.get_provider_instance()
            provider_instance.authenticate()
            payload = provider_instance.map_sales_invoice_to_payload(si_doc, settings)
            result = provider_instance.issue_outward_invoice(payload)
        except EInvoiceProviderNotReady as e:
            return {"success": False, "message": e.message}
        except EInvoiceProviderError as e:
            log_einvoice_error(
                f"Issue failed - {sales_invoice}",
                f"{e.message}\n{e.detail or ''}",
                provider=provider_name,
            )
            _create_issuance_log(provider_name, sales_invoice, "Failed", error=str(e.message))
            return {"success": False, "message": f"Lỗi provider: {e.message}"}

        # Create Issuance Log
        if result.get("success"):
            _create_issuance_log(
                provider_name, sales_invoice, "Success",
                invoice_number=result.get("invoice_number", ""),
                lookup_code=result.get("lookup_code", ""),
                pdf_url=result.get("pdf_url", ""),
            )

            # Update Sales Invoice custom fields
            frappe.db.set_value("Sales Invoice", sales_invoice, {
                "einvoice_issued": 1,
                "einvoice_provider": provider_name,
                "einvoice_number": result.get("invoice_number", ""),
                "einvoice_lookup_code": result.get("lookup_code", ""),
                "einvoice_pdf_url": result.get("pdf_url", ""),
                "einvoice_issued_at": now_datetime(),
            }, update_modified=False)

            frappe.db.commit()
            return {
                "success": True,
                "message": "Xuất hóa đơn đỏ thành công!",
                "invoice_number": result.get("invoice_number"),
                "lookup_code": result.get("lookup_code"),
                "pdf_url": result.get("pdf_url"),
            }
        else:
            error_msg = result.get("error", "Lỗi không xác định")
            _create_issuance_log(provider_name, sales_invoice, "Failed", error=error_msg)
            return {"success": False, "message": f"Xuất hóa đơn đỏ thất bại: {error_msg}"}

    @staticmethod
    def issue_bulk(sales_invoices, provider=None, pattern=None, serial=None, issue_mode=None):
        """
        Issue outward e-invoices for multiple Sales Invoices.

        Args:
            sales_invoices: JSON string or list of Sales Invoice names

        Returns:
            dict with keys: success, message, results, background
        """
        if isinstance(sales_invoices, str):
            sales_invoices = json.loads(sales_invoices)

        settings = frappe.get_single("EInvoice Settings")
        limit = settings.bulk_issuance_limit or 50

        if len(sales_invoices) > limit:
            return {
                "success": False,
                "message": f"Số lượng tối đa là {limit} hóa đơn/lần. Bạn đã chọn {len(sales_invoices)}.",
            }

        if len(sales_invoices) > 5:
            frappe.enqueue(
                _process_bulk_issuance,
                queue="long",
                timeout=1200,
                sales_invoices=sales_invoices,
                provider=provider,
                pattern=pattern,
                serial=serial,
                issue_mode=issue_mode,
            )
            return {
                "success": True,
                "message": f"Đang xử lý {len(sales_invoices)} hóa đơn ở chế độ nền. "
                           f"Kiểm tra kết quả tại EInvoice Issuance Log.",
                "background": True,
            }

        return _process_bulk_issuance(sales_invoices, provider, pattern, serial, issue_mode)


def _resolve_provider(si_doc, provider_name, settings):
    """Resolve provider, priority by company of the Sales Invoice."""
    company = si_doc.company
    if provider_name:
        provider_doc = frappe.get_doc("EInvoice Provider", provider_name)
        if provider_doc.company != company:
            frappe.throw(
                f"Provider '{provider_name}' thuộc công ty '{provider_doc.company}', "
                f"không khớp với công ty '{company}' của hóa đơn."
            )
        return provider_doc

    candidates = frappe.get_all(
        "EInvoice Provider",
        filters={"enabled": 1, "company": company},
        pluck="name",
    )
    if len(candidates) == 1:
        return frappe.get_doc("EInvoice Provider", candidates[0])
    if len(candidates) > 1:
        if settings.default_provider:
            dp = frappe.get_doc("EInvoice Provider", settings.default_provider)
            if dp.company == company and dp.enabled:
                return dp
        frappe.throw(f"Công ty '{company}' có nhiều provider. Vui lòng chọn provider cụ thể.")
    frappe.throw(f"Không tìm thấy provider nào được bật cho công ty '{company}'.")


def _create_issuance_log(provider_name, sales_invoice, status, invoice_number="",
                         lookup_code="", pdf_url="", error=""):
    """Create an EInvoice Issuance Log record."""
    log = frappe.new_doc("EInvoice Issuance Log")
    log.provider = provider_name
    log.sales_invoice = sales_invoice
    log.issued_at = now_datetime()
    log.status = status
    log.provider_invoice_number = invoice_number
    log.provider_lookup_code = lookup_code
    log.provider_pdf_url = pdf_url
    log.error_detail = error
    log.insert(ignore_permissions=True)


def _process_bulk_issuance(sales_invoices, provider=None, pattern=None, serial=None, issue_mode=None):
    """Process bulk issuance sequentially."""
    results = []
    for si_name in sales_invoices:
        result = IssuanceService.issue_single(
            sales_invoice=si_name,
            provider=provider,
            pattern=pattern,
            serial=serial,
            issue_mode=issue_mode,
        )
        results.append({"sales_invoice": si_name, "status": result.get("success"), "detail": result})

    success_count = sum(1 for r in results if r["status"])
    fail_count = len(results) - success_count

    return {
        "success": True,
        "message": f"Hoàn tất: {success_count} thành công, {fail_count} lỗi.",
        "results": results,
        "background": False,
    }
```

- [ ] **Step 3: Commit**

```bash
git add einvoice/einvoice/services/__init__.py einvoice/einvoice/services/issuance.py
git commit -m "feat: extract issuance logic into services/issuance.py"
```

---

### Task 6: Create services/sync.py with frequency check and distributed lock

**Files:**
- Create: `einvoice/einvoice/services/sync.py`

- [ ] **Step 1: Create services/sync.py**

Create file `einvoice/einvoice/services/sync.py`:

```python
"""
Sync Service — Inward Invoice Synchronization.

Fetches inward invoices from all active providers, creates staging records,
and attempts auto-matching with existing Purchase Invoices.

Extracted from tasks/__init__.py for testability and separation of concerns.
"""

import uuid

import frappe
from frappe.utils import now_datetime, add_days, getdate, today, flt

from einvoice.einvoice.exceptions import EInvoiceProviderError, EInvoiceProviderNotReady


FREQ_MAP = {
    "Every 15 Min": 900,
    "Hourly": 3600,
    "Every 6 Hours": 21600,
    "Daily": 86400,
    "Weekly": 604800,
}


def log_einvoice_error(title, message, provider=None):
    """Log error with [EInvoice] prefix for easy filtering."""
    frappe.log_error(
        title=f"[EInvoice] {title}",
        message=message,
        reference_doctype="EInvoice Provider" if provider else None,
        reference_name=provider,
    )


def run_if_frequency_match():
    """
    Entry point from scheduler hooks.

    Guards:
    - EInvoice Settings must exist
    - Auto-sync must be enabled
    - Enough time must have elapsed since last sync
    - Distributed lock prevents concurrent runs
    """
    if not frappe.db.exists("EInvoice Settings", "EInvoice Settings"):
        return

    settings = frappe.get_single("EInvoice Settings")

    if not settings.enable_auto_sync:
        return

    freq = settings.sync_frequency
    if not freq:
        return

    min_interval = FREQ_MAP.get(freq)
    if not min_interval:
        return

    # Check elapsed time since last sync
    if settings.last_sync_datetime:
        elapsed = (now_datetime() - settings.last_sync_datetime).total_seconds()
        if elapsed < min_interval:
            return

    # Distributed lock via Redis
    lock_key = "einvoice_sync_running"
    if frappe.cache.get_value(lock_key):
        return
    frappe.cache.set_value(lock_key, 1, expires_in_sec=300)

    try:
        SyncService.run_sync(sync_type="Scheduled")
    finally:
        frappe.cache.delete_key(lock_key)


class SyncService:
    """Service class for inward invoice sync operations."""

    @staticmethod
    def run_sync(sync_type="Manual"):
        """
        Main sync logic. Fetches inward invoices from all active providers
        and creates EInvoice Inward staging records.

        Returns:
            dict with keys: status, fetched, new, dup, errors
        """
        settings = frappe.get_single("EInvoice Settings")
        date_range = settings.default_date_range_days or 30

        to_date = today()
        from_date = str(add_days(getdate(to_date), -date_range))

        providers = frappe.get_all(
            "EInvoice Provider",
            filters={"enabled": 1},
            fields=["name"],
        )

        if not providers:
            frappe.logger().info("EInvoice: No active providers found for sync.")
            return {"status": "No providers", "fetched": 0, "new": 0, "dup": 0, "errors": 0}

        total_fetched = 0
        total_new = 0
        total_dup = 0
        total_errors = 0
        error_details = []
        batch_id = str(uuid.uuid4())[:8]

        for prov in providers:
            try:
                result = _sync_provider(prov.name, from_date, to_date, batch_id, settings)
                _create_sync_log(prov.name, sync_type, result, from_date, to_date)
                total_fetched += result["fetched"]
                total_new += result["new"]
                total_dup += result["dup"]
                total_errors += result["errors"]
                if result.get("error_detail"):
                    error_details.append(result["error_detail"])
            except EInvoiceProviderNotReady as e:
                # Skip stub providers silently during sync
                frappe.logger().info(f"EInvoice: Skipping {prov.name} — {e.message}")
            except Exception as e:
                total_errors += 1
                err_msg = f"Provider {prov.name}: {str(e)}"
                error_details.append(err_msg)
                _create_sync_log(
                    prov.name, sync_type,
                    {"fetched": 0, "new": 0, "dup": 0, "errors": 1, "error_detail": err_msg},
                    from_date, to_date,
                )
                log_einvoice_error(
                    f"Sync Error - {prov.name}",
                    frappe.get_traceback(),
                    provider=prov.name,
                )

        # Determine overall status
        if total_errors == 0:
            status = "Success"
        elif total_new > 0:
            status = "Partial"
        else:
            status = "Failed"

        # Update settings
        settings.last_sync_datetime = now_datetime()
        settings.last_sync_status = status
        settings.last_sync_error = error_details[0] if error_details else ""
        settings.save(ignore_permissions=True)
        frappe.db.commit()

        frappe.logger().info(
            f"EInvoice Sync: fetched={total_fetched}, new={total_new}, "
            f"dup={total_dup}, errors={total_errors}"
        )

        return {
            "status": status,
            "fetched": total_fetched,
            "new": total_new,
            "dup": total_dup,
            "errors": total_errors,
        }


def _sync_provider(provider_name, from_date, to_date, batch_id, settings):
    """Sync invoices from a single provider."""
    provider_doc = frappe.get_doc("EInvoice Provider", provider_name)
    provider = provider_doc.get_provider_instance()

    provider.authenticate()
    raw_invoices = provider.fetch_inward_invoices(from_date, to_date)

    result = {"fetched": len(raw_invoices), "new": 0, "dup": 0, "errors": 0, "error_detail": ""}
    errors = []

    for raw in raw_invoices:
        try:
            parsed = provider.parse_inward_invoice(raw)
            lookup_code = parsed.get("lookup_code")

            if not lookup_code:
                result["errors"] += 1
                errors.append("Hóa đơn thiếu mã tra cứu (lookup_code)")
                continue

            if frappe.db.exists("EInvoice Inward", {"lookup_code": lookup_code}):
                result["dup"] += 1
                continue

            inv = frappe.new_doc("EInvoice Inward")
            inv.provider = provider_name
            inv.lookup_code = lookup_code
            inv.provider_invoice_id = parsed.get("provider_invoice_id", "")
            inv.invoice_number = parsed.get("invoice_number", "")
            inv.invoice_pattern = parsed.get("invoice_pattern", "")
            inv.invoice_serial = parsed.get("invoice_serial", "")
            inv.invoice_date = parsed.get("invoice_date")
            inv.invoice_type = parsed.get("invoice_type", "Khác")
            inv.supplier_name = parsed.get("supplier_name", "")
            inv.supplier_tax_code = parsed.get("supplier_tax_code", "")
            inv.supplier_address = parsed.get("supplier_address", "")
            inv.total_before_tax = parsed.get("total_before_tax", 0)
            inv.tax_rate = parsed.get("tax_rate", 0)
            inv.tax_amount = parsed.get("tax_amount", 0)
            inv.total_amount = parsed.get("total_amount", 0)
            inv.currency = parsed.get("currency", "VND")
            inv.pdf_url = parsed.get("pdf_url", "")
            inv.raw_data = parsed.get("raw_data", "")
            inv.sync_batch_id = batch_id
            inv.status = "New"
            inv.company = provider_doc.company
            inv.insert(ignore_permissions=True)
            result["new"] += 1

            _try_auto_match(inv, settings)

        except Exception as e:
            result["errors"] += 1
            errors.append(str(e))

    if errors:
        result["error_detail"] = "; ".join(errors[:10])

    return result


def _try_auto_match(inv, settings):
    """Attempt to auto-match an inward invoice with an existing Purchase Invoice."""
    if not inv.supplier_tax_code or not inv.total_amount:
        return

    tol_pct = (settings.match_total_tolerance_pct or 1) / 100
    tol_days = settings.match_date_tolerance_days or 3

    total = inv.total_amount
    low = total * (1 - tol_pct)
    high = total * (1 + tol_pct)

    filters = {
        "docstatus": ["in", [0, 1]],
        "grand_total": ["between", [low, high]],
        "einvoice_inward": ["is", "not set"],
        "company": inv.company,
    }

    suppliers = frappe.get_all("Supplier", filters={"tax_id": inv.supplier_tax_code}, pluck="name")
    if not suppliers:
        return

    filters["supplier"] = ["in", suppliers]

    if inv.invoice_date:
        from_d = str(add_days(getdate(inv.invoice_date), -tol_days))
        to_d = str(add_days(getdate(inv.invoice_date), tol_days))
        filters["posting_date"] = ["between", [from_d, to_d]]

    candidates = frappe.get_all("Purchase Invoice", filters=filters, pluck="name")

    if len(candidates) == 1:
        pi_name = candidates[0]
        inv.linked_purchase_invoice = pi_name
        inv.status = "Matched"
        inv.save(ignore_permissions=True)

        frappe.db.set_value("Purchase Invoice", pi_name, {
            "einvoice_inward": inv.name,
            "einvoice_lookup_code": inv.lookup_code,
        })


def _create_sync_log(provider_name, sync_type, result, from_date, to_date):
    """Create a Sync Log record for a single provider."""
    status = "Success" if result["errors"] == 0 else ("Partial" if result["new"] > 0 else "Failed")
    log = frappe.new_doc("EInvoice Sync Log")
    log.provider = provider_name
    log.sync_type = sync_type
    log.start_time = now_datetime()
    log.end_time = now_datetime()
    log.date_from = from_date
    log.date_to = to_date
    log.total_fetched = result["fetched"]
    log.new_created = result["new"]
    log.duplicates_skipped = result["dup"]
    log.errors = result["errors"]
    log.status = status
    log.error_detail = result.get("error_detail", "")
    log.insert(ignore_permissions=True)
    return status
```

- [ ] **Step 2: Commit**

```bash
git add einvoice/einvoice/services/sync.py
git commit -m "feat: extract sync logic into services/sync.py with frequency check and distributed lock"
```

---

### Task 7: Rewrite api.py as thin layer with role guards

**Files:**
- Rewrite: `einvoice/einvoice/api.py`

- [ ] **Step 1: Rewrite api.py**

Replace entire content of `einvoice/einvoice/api.py`:

```python
"""
Whitelisted API endpoints for EInvoice.

Thin layer: validates permissions, parses input, delegates to services.
All endpoints require System Manager or Accounts Manager role.
"""

import frappe

from einvoice.einvoice.services.issuance import IssuanceService
from einvoice.einvoice.services.sync import SyncService


def has_app_permission():
    """Permission check for apps screen."""
    return "System Manager" in frappe.get_roles() or "Accounts Manager" in frappe.get_roles()


@frappe.whitelist()
def issue_single_invoice(sales_invoice, provider=None, pattern=None, serial=None, issue_mode=None):
    """Issue a single outward e-invoice from a submitted Sales Invoice."""
    frappe.only_for(["System Manager", "Accounts Manager"])
    return IssuanceService.issue_single(sales_invoice, provider, pattern, serial, issue_mode)


@frappe.whitelist()
def issue_bulk_invoices(sales_invoices, provider=None, pattern=None, serial=None, issue_mode=None):
    """Issue outward e-invoices for multiple Sales Invoices."""
    frappe.only_for(["System Manager", "Accounts Manager"])
    return IssuanceService.issue_bulk(sales_invoices, provider, pattern, serial, issue_mode)


@frappe.whitelist()
def get_providers(company=None):
    """Get list of enabled providers for the dropdown."""
    frappe.only_for(["System Manager", "Accounts Manager"])
    filters = {"enabled": 1}
    if company:
        filters["company"] = company
    return frappe.get_all(
        "EInvoice Provider",
        filters=filters,
        fields=["name", "provider_name", "provider_type",
                "default_invoice_pattern", "default_invoice_serial"],
    )


@frappe.whitelist()
def sync_inward_invoices():
    """Trigger manual sync of inward invoices from all active providers."""
    frappe.only_for(["System Manager", "Accounts Manager"])
    return SyncService.run_sync(sync_type="Manual")
```

- [ ] **Step 2: Commit**

```bash
git add einvoice/einvoice/api.py
git commit -m "refactor: rewrite api.py as thin layer with role guards, add sync_inward_invoices endpoint"
```

---

### Task 8: Simplify tasks/ to thin wrapper

**Files:**
- Simplify: `einvoice/einvoice/tasks/__init__.py`
- Simplify: `einvoice/einvoice/tasks/sync_inward_invoices.py`

- [ ] **Step 1: Rewrite tasks/__init__.py**

Replace entire content of `einvoice/einvoice/tasks/__init__.py`:

```python
"""
Background Job: Sync Inward Invoices from E-Invoice Providers.

Thin wrapper — delegates to services/sync.py.
Kept for backward compatibility with hooks.py import paths.
"""

from einvoice.einvoice.services.sync import run_if_frequency_match, SyncService  # noqa: F401


def run_sync(sync_type="Manual"):
    return SyncService.run_sync(sync_type=sync_type)
```

- [ ] **Step 2: Rewrite tasks/sync_inward_invoices.py**

Replace entire content of `einvoice/einvoice/tasks/sync_inward_invoices.py`:

```python
"""
Background Job: Sync Inward Invoices.
Re-exports from tasks/__init__.py for clean import path.
"""
from . import run_if_frequency_match, run_sync  # noqa: F401
```

- [ ] **Step 3: Commit**

```bash
git add einvoice/einvoice/tasks/__init__.py einvoice/einvoice/tasks/sync_inward_invoices.py
git commit -m "refactor: simplify tasks/ to thin wrapper over services/sync.py"
```

---

### Task 9: Rewrite einvoice_inward.py with tax template matching

**Files:**
- Rewrite: `einvoice/einvoice/doctype/einvoice_inward/einvoice_inward.py`

- [ ] **Step 1: Rewrite einvoice_inward.py**

Replace entire content of `einvoice/einvoice/doctype/einvoice_inward/einvoice_inward.py`:

```python
import frappe
from frappe.model.document import Document
from frappe.utils import today, flt


class EInvoiceInward(Document):
    """Staging record for an inward invoice fetched from an E-Invoice provider."""

    def validate(self):
        if self.linked_purchase_invoice and self.status == "New":
            self.status = "Matched"

        # Auto-calculate tax rate if not set
        if not self.tax_rate and self.total_before_tax:
            self.tax_rate = round((self.tax_amount or 0) / self.total_before_tax * 100, 0)

    @frappe.whitelist()
    def match_purchase_invoice(self, purchase_invoice):
        """Manually match this staging record to an existing Purchase Invoice."""
        self.linked_purchase_invoice = purchase_invoice
        self.status = "Matched"
        self.save(ignore_permissions=True)

        frappe.db.set_value(
            "Purchase Invoice",
            purchase_invoice,
            {
                "einvoice_inward": self.name,
                "einvoice_lookup_code": self.lookup_code,
            },
        )
        frappe.msgprint(f"Đã ghép nối với {purchase_invoice}", alert=True)

    @frappe.whitelist()
    def create_purchase_invoice(self):
        """Create a new Purchase Invoice from this staging record's data."""
        supplier = self._get_or_create_supplier()
        tax_template = self._resolve_tax_template()

        pi = frappe.new_doc("Purchase Invoice")
        pi.supplier = supplier
        pi.company = self.company
        pi.posting_date = self.invoice_date or today()
        pi.bill_no = self.invoice_number
        pi.bill_date = self.invoice_date
        pi.einvoice_inward = self.name
        pi.einvoice_lookup_code = self.lookup_code

        pi.append("items", {
            "item_name": f"Hóa đơn {self.invoice_number} từ {self.supplier_name}",
            "description": f"Nhập từ HĐĐT - Mã tra cứu: {self.lookup_code}",
            "qty": 1,
            "rate": self.total_before_tax or 0,
            "expense_account": frappe.get_cached_value(
                "Company", pi.company, "default_expense_account"
            ),
        })

        # Apply tax template
        if tax_template:
            pi.taxes_and_charges = tax_template.name
            pi.set_taxes()

            # Compare calculated tax with HĐĐT tax
            calculated_tax = flt(pi.total_taxes_and_charges)
            expected_tax = flt(self.tax_amount)
            if expected_tax and calculated_tax:
                diff_pct = abs(calculated_tax - expected_tax) / expected_tax * 100
                if diff_pct > 1:
                    frappe.msgprint(
                        f"Thuế tính theo mẫu ({frappe.format_value(calculated_tax, 'Currency')}) "
                        f"chênh lệch với thuế trên HĐĐT ({frappe.format_value(expected_tax, 'Currency')}). "
                        f"Vui lòng kiểm tra.",
                        alert=True,
                    )

        pi.insert(ignore_permissions=True)

        self.linked_purchase_invoice = pi.name
        self.status = "PI Created"
        self.save(ignore_permissions=True)

        frappe.msgprint(f"Đã tạo {pi.name} (Draft). Vui lòng kiểm tra và submit.", alert=True)
        return pi.name

    def _resolve_tax_template(self):
        """
        Find the best matching Purchase Taxes and Charges Template by tax rate.

        Logic:
        1. Calculate actual_rate from inward invoice
        2. Find templates for this company
        3. Match by tax rate (On Net Total)
        4. Fallback to is_default if no rate match
        5. Throw if no template exists at all
        """
        actual_rate = round(self.tax_rate or 0, 0)

        templates = frappe.get_all(
            "Purchase Taxes and Charges Template",
            filters={"company": self.company},
            fields=["name", "is_default"],
        )

        if not templates:
            frappe.throw(
                f"Công ty {self.company} chưa có Purchase Taxes and Charges Template. "
                f"Vui lòng tạo tại: /app/purchase-taxes-and-charges-template/new"
            )

        # Try to match by tax rate
        matched = []
        for tmpl in templates:
            taxes = frappe.get_all(
                "Purchase Taxes and Charges",
                filters={
                    "parent": tmpl.name,
                    "charge_type": "On Net Total",
                },
                fields=["rate"],
                limit=1,
            )
            if taxes and round(flt(taxes[0].rate), 0) == actual_rate:
                matched.append(tmpl)

        if len(matched) == 1:
            return frappe.get_doc("Purchase Taxes and Charges Template", matched[0].name)

        if len(matched) > 1:
            # Prefer is_default
            for m in matched:
                if m.is_default:
                    return frappe.get_doc("Purchase Taxes and Charges Template", m.name)
            return frappe.get_doc("Purchase Taxes and Charges Template", matched[0].name)

        # No rate match — fallback to default
        for tmpl in templates:
            if tmpl.is_default:
                frappe.msgprint(
                    f"Không tìm thấy mẫu thuế {actual_rate}%. "
                    f"Đang dùng mẫu mặc định. Vui lòng kiểm tra.",
                    alert=True,
                )
                return frappe.get_doc("Purchase Taxes and Charges Template", tmpl.name)

        # No default either — throw with guidance
        frappe.throw(
            f"Công ty {self.company} chưa có Purchase Taxes and Charges Template mặc định. "
            f"Vui lòng tạo tại: /app/purchase-taxes-and-charges-template/new"
        )

    def _get_or_create_supplier(self):
        """Find an existing supplier by tax code, or create a new one."""
        if self.supplier_tax_code:
            existing = frappe.db.get_value(
                "Supplier", {"tax_id": self.supplier_tax_code}, "name"
            )
            if existing:
                return existing

        supplier = frappe.new_doc("Supplier")
        supplier.supplier_name = self.supplier_name or "Nhà cung cấp không xác định"
        supplier.supplier_group = frappe.db.get_single_value(
            "Buying Settings", "supplier_group"
        ) or "All Supplier Groups"
        supplier.tax_id = self.supplier_tax_code
        supplier.insert(ignore_permissions=True)
        return supplier.name

    @frappe.whitelist()
    def ignore_invoice(self):
        """Mark this invoice as ignored."""
        self.status = "Ignored"
        self.save(ignore_permissions=True)
        frappe.msgprint("Đã bỏ qua hóa đơn này.", alert=True)
```

- [ ] **Step 2: Commit**

```bash
git add einvoice/einvoice/doctype/einvoice_inward/einvoice_inward.py
git commit -m "feat: rewrite einvoice_inward with tax template matching by rate"
```

---

### Task 10: Refactor einvoice_settings.py and einvoice_provider.py

**Files:**
- Refactor: `einvoice/einvoice/doctype/einvoice_settings/einvoice_settings.py`
- Refactor: `einvoice/einvoice/doctype/einvoice_provider/einvoice_provider.py`

- [ ] **Step 1: Rewrite einvoice_settings.py**

Replace entire content of `einvoice/einvoice/doctype/einvoice_settings/einvoice_settings.py`:

```python
import frappe
from frappe.model.document import Document


class EInvoiceSettings(Document):
    """Central settings for E-Invoice Integration."""

    @frappe.whitelist()
    def sync_now(self):
        """Trigger an immediate sync of inward invoices from all active providers."""
        from einvoice.einvoice.services.sync import SyncService

        frappe.enqueue(
            SyncService.run_sync,
            queue="long",
            timeout=600,
            sync_type="Manual",
        )
        frappe.msgprint("Đã khởi chạy đồng bộ hóa đơn mua vào ở chế độ nền.", alert=True)

    @frappe.whitelist()
    def test_connection(self):
        """Test connection to the default provider."""
        if not self.default_provider:
            frappe.throw("Vui lòng chọn Nhà cung cấp HĐĐT mặc định trước.")

        from einvoice.einvoice.doctype.einvoice_provider.einvoice_provider import test_connection
        return test_connection(self.default_provider)
```

- [ ] **Step 2: Rewrite einvoice_provider.py**

Replace entire content of `einvoice/einvoice/doctype/einvoice_provider/einvoice_provider.py`:

```python
import frappe
from frappe.model.document import Document
from frappe.utils import now_datetime

from einvoice.einvoice.exceptions import (
    EInvoiceProviderError,
    EInvoiceProviderNotReady,
)


class EInvoiceProvider(Document):
    """Represents a single E-Invoice provider configuration."""

    def get_provider_instance(self):
        """Return the appropriate provider class instance based on provider_type."""
        from einvoice.einvoice.providers import get_provider_class

        klass = get_provider_class(self.provider_type)
        return klass(self)


@frappe.whitelist()
def test_connection(docname):
    """Test the API connection for a provider and update its status."""
    doc = frappe.get_doc("EInvoice Provider", docname)
    try:
        provider = doc.get_provider_instance()
        provider.authenticate()
        doc.connection_status = "Connected"
        doc.last_tested = now_datetime()
        doc.save(ignore_permissions=True)
        frappe.db.commit()
        return {"success": True, "message": "Kết nối thành công!"}
    except EInvoiceProviderNotReady as e:
        doc.connection_status = "Failed"
        doc.last_tested = now_datetime()
        doc.save(ignore_permissions=True)
        frappe.db.commit()
        return {"success": False, "message": e.message}
    except EInvoiceProviderError as e:
        doc.connection_status = "Failed"
        doc.last_tested = now_datetime()
        doc.save(ignore_permissions=True)
        frappe.db.commit()
        return {"success": False, "message": f"Kết nối thất bại: {e.message}"}
    except Exception as e:
        doc.connection_status = "Failed"
        doc.last_tested = now_datetime()
        doc.save(ignore_permissions=True)
        frappe.db.commit()
        return {"success": False, "message": f"Kết nối thất bại: {str(e)}"}


@frappe.whitelist()
def refresh_templates(docname):
    """Fetch latest invoice templates from the provider."""
    doc = frappe.get_doc("EInvoice Provider", docname)
    try:
        provider = doc.get_provider_instance()
        provider.authenticate()
        return provider.get_invoice_templates()
    except EInvoiceProviderNotReady as e:
        frappe.msgprint(e.message)
        return []
    except EInvoiceProviderError as e:
        frappe.msgprint(f"Lỗi: {e.message}")
        return []
```

- [ ] **Step 3: Commit**

```bash
git add einvoice/einvoice/doctype/einvoice_settings/einvoice_settings.py einvoice/einvoice/doctype/einvoice_provider/einvoice_provider.py
git commit -m "refactor: update settings and provider controllers to use new exceptions and services"
```

---

### Task 11: Fix JavaScript files

**Files:**
- Fix: `einvoice/public/js/sales_invoice.js`
- Fix: `einvoice/public/js/einvoice_provider.js`
- Fix: `einvoice/public/js/dcnet_inward_invoice_list.js`

- [ ] **Step 1: Fix sales_invoice.js — add error handling**

In `einvoice/public/js/sales_invoice.js`, replace the callback inside `primary_action` (lines 105-113) with:

```javascript
                        callback(r) {
                            if (r.exc) return;
                            if (r.message && !r.message.success) {
                                frappe.msgprint({
                                    title: __("Lỗi"),
                                    message: r.message.message,
                                    indicator: "red",
                                });
                                return;
                            }
                            if (r.message) {
                                frappe.show_alert({
                                    message: r.message.message || "Thành công!",
                                    indicator: "green",
                                });
                            }
                            frm.reload_doc();
                        },
```

- [ ] **Step 2: Fix einvoice_provider.js — add stub warning**

In `einvoice/public/js/einvoice_provider.js`, add after the `provider_type(frm)` handler (after line 18):

```javascript
        // Warn about stub providers
        if (["Viettel", "MISA"].includes(frm.doc.provider_type)) {
            frappe.msgprint(
                __("Provider {0} chưa được hỗ trợ. Vui lòng liên hệ DCNET.", [frm.doc.provider_type])
            );
        }
```

Also update `_test_connection` callback to handle the new response format (replace lines 52-59):

```javascript
        callback(r) {
            frappe.dom.unfreeze();
            frm.reload_doc();
            if (!r.exc && r.message) {
                if (r.message.success) {
                    frappe.show_alert({
                        message: __(r.message.message),
                        indicator: "green",
                    });
                } else {
                    frappe.msgprint({
                        title: __("Lỗi"),
                        message: r.message.message,
                        indicator: "red",
                    });
                }
            }
        },
```

- [ ] **Step 3: Fix dcnet_inward_invoice_list.js — fix doctype name and hook**

Replace entire content of `einvoice/public/js/dcnet_inward_invoice_list.js`:

```javascript
frappe.listview_settings["EInvoice Inward"] = {
    refresh: function (listview) {
        listview.page.add_inner_button(
            __("Cập nhật Hóa đơn đầu vào mới"),
            function () {
                frappe.call({
                    method: "einvoice.einvoice.api.sync_inward_invoices",
                    freeze: true,
                    freeze_message: __("Đang đồng bộ hóa đơn từ nhà cung cấp..."),
                    callback: function (r) {
                        if (r.message) {
                            const res = r.message;
                            let msg = `Đồng bộ hoàn tất: Tìm thấy ${res.fetched || 0} hóa đơn.`;
                            if (res.new > 0) msg += ` (Thêm mới: ${res.new})`;
                            if (res.dup > 0) msg += ` (Trùng: ${res.dup})`;
                            if (res.errors > 0) msg += ` (Lỗi: ${res.errors})`;

                            frappe.msgprint({
                                title: __("Kết quả đồng bộ"),
                                message: msg,
                                indicator: res.new > 0 ? "green" : "orange",
                            });
                            listview.refresh();
                        }
                    },
                });
            }
        );
    },
};
```

- [ ] **Step 4: Commit**

```bash
git add einvoice/public/js/sales_invoice.js einvoice/public/js/einvoice_provider.js einvoice/public/js/dcnet_inward_invoice_list.js
git commit -m "fix: JS error handling, stub provider warning, fix inward invoice list sync button"
```

---

### Task 12: Fix hooks.py — add EInvoice Inward list JS

**Files:**
- Fix: `einvoice/einvoice/hooks.py`

- [ ] **Step 1: Add EInvoice Inward to doctype_list_js**

In `einvoice/einvoice/hooks.py`, change `doctype_list_js` (line 24-26) from:

```python
doctype_list_js = {
    "Sales Invoice": "public/js/sales_invoice_list.js",
}
```

to:

```python
doctype_list_js = {
    "Sales Invoice": "public/js/sales_invoice_list.js",
    "EInvoice Inward": "public/js/dcnet_inward_invoice_list.js",
}
```

- [ ] **Step 2: Commit**

```bash
git add einvoice/einvoice/hooks.py
git commit -m "fix: register EInvoice Inward list JS in hooks.py"
```

---

### Task 13: Build assets and verify

- [ ] **Step 1: Build frontend assets**

```bash
cd /home/long/long/frappe-bench-das
bench build --app einvoice
```

Expected: Build completes without errors.

- [ ] **Step 2: Run migration**

```bash
bench --site das.localhost migrate
```

Expected: Migration completes without errors.

- [ ] **Step 3: Clear cache**

```bash
bench --site das.localhost clear-cache
```

- [ ] **Step 4: Verify Python imports**

```bash
cd /home/long/long/frappe-bench-das
bench --site das.localhost execute "einvoice.einvoice.exceptions.EInvoiceError" 2>&1 | head -5
bench --site das.localhost execute "einvoice.einvoice.services.issuance.IssuanceService" 2>&1 | head -5
bench --site das.localhost execute "einvoice.einvoice.services.sync.SyncService" 2>&1 | head -5
```

Expected: No ImportError — modules load cleanly.

- [ ] **Step 5: Verify scheduler import chain**

```bash
bench --site das.localhost execute "einvoice.einvoice.tasks.sync_inward_invoices.run_if_frequency_match" 2>&1 | head -5
```

Expected: No ImportError. Function runs and returns (no-op since auto_sync is off).

- [ ] **Step 6: Push to remote**

```bash
cd /home/long/long/frappe-bench-das/apps/einvoice
git push -u origin develop
```
