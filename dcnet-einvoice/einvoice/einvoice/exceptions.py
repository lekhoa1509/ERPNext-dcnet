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
        msg = f"Provider {provider_type} chưa được hỗ trợ. Vui lòng liên hệ DCNet (info@dcnet.vn)."
        super().__init__(msg)


class EInvoiceValidationError(EInvoiceError):
    """Data validation error."""
    pass


class EInvoiceTaxTemplateError(EInvoiceError):
    """Tax template not found or mismatch."""
    pass
