"""
Abstract base class for all E-Invoice providers.

Every provider must implement all abstract methods.
"""

from abc import ABC, abstractmethod


class BaseProvider(ABC):
    """Strategy interface for E-Invoice providers."""

    def __init__(self, provider_doc):
        """
        Args:
            provider_doc: frappe Document of type 'EInvoice Provider'
        """
        self.provider_doc = provider_doc
        self.api_url = provider_doc.api_url
        self.api_url_purchase = provider_doc.api_url_purchase or provider_doc.api_url
        self.tax_code = provider_doc.tax_code
        self._access_token = None

    # ------------------------------------------------------------------
    # Authentication
    # ------------------------------------------------------------------
    @abstractmethod
    def authenticate(self) -> str:
        """
        Authenticate with the provider API.
        Returns an access token or session identifier.
        Should set self._access_token.
        """
        ...

    # ------------------------------------------------------------------
    # Inward Invoices (Purchase)
    # ------------------------------------------------------------------
    @abstractmethod
    def fetch_inward_invoices(self, from_date: str, to_date: str) -> list[dict]:
        """
        Fetch a list of inward invoices from the provider.

        Args:
            from_date: YYYY-MM-DD
            to_date:   YYYY-MM-DD

        Returns:
            List of raw invoice data dicts from the provider.
        """
        ...

    @abstractmethod
    def parse_inward_invoice(self, raw_data: dict) -> dict:
        """
        Parse a single raw invoice dict into a standardized dict
        matching EInvoice Inward fields.

        Returns dict with keys:
            lookup_code, invoice_number, invoice_pattern, invoice_serial,
            invoice_date, invoice_type, supplier_name, supplier_tax_code,
            supplier_address, total_before_tax, tax_rate, tax_amount,
            total_amount, currency, pdf_url, raw_data (json string)
        """
        ...

    # ------------------------------------------------------------------
    # Outward Invoices (Sales)
    # ------------------------------------------------------------------
    @abstractmethod
    def get_invoice_templates(self) -> list[dict]:
        """
        Fetch available invoice templates/patterns from the provider.

        Returns:
            List of dicts with keys: thDon, khmshDon, khhDon, sLuong, cLai
        """
        ...

    @abstractmethod
    def issue_outward_invoice(self, invoice_data: dict) -> dict:
        """
        Issue (create) an outward invoice on the provider.

        Args:
            invoice_data: Standardized dict built from Sales Invoice.

        Returns dict with keys:
            success (bool), invoice_number, lookup_code, pdf_url,
            xml_url, raw_response (dict)
        """
        ...

    @abstractmethod
    def cancel_invoice(self, invoice_ref: str, reason: str) -> bool:
        """Cancel a previously issued invoice."""
        ...

    # ------------------------------------------------------------------
    # Utilities
    # ------------------------------------------------------------------
    def map_sales_invoice_to_payload(self, si_doc, settings_doc) -> dict:
        """
        Convert an ERPNext Sales Invoice document to the provider-specific
        payload format. Subclasses must override.
        """
        raise NotImplementedError
