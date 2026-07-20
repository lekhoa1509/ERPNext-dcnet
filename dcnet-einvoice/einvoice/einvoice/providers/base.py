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

    # Outward issue capability — quyết định IssuanceService dispatch sang đâu:
    # - "direct": provider tự ký (HSM hoặc pre-signed) → issue_outward_invoice
    # - "push-draft": ERP đẩy nháp, user ký USB ngoài (web admin) → push_draft_invoice
    # Provider mới phải khai báo rõ. Default "direct" giữ legacy behavior.
    OUTWARD_CAPABILITY = "direct"

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

    def download_attachment(self, attach_url: str, kind: str) -> bytes:
        """Download a PDF or XML by authenticated URL. Returns bytes on success.

        kind ∈ {"pdf", "xml"}. Raises EInvoiceProviderError on hard fail
        (404, exhausted retries). Subclasses implement provider-specific auth
        + URL handling. Default impl raises NotImplementedError so providers
        without inward attachments don't break the interface.
        """
        raise NotImplementedError(
            f"{self.provider_name} does not implement download_attachment"
        )

    def _invalidate_cached_token(self, token_type: str) -> None:
        """Clear one cached token (counterpart to _clear_cached_tokens for all)."""
        frappe.cache.delete_key(self._cache_key(token_type))

    @abstractmethod
    def map_sales_invoice_to_payload(self, si_doc, settings_doc) -> dict:
        """Convert ERPNext Sales Invoice to provider-specific payload."""
        ...
