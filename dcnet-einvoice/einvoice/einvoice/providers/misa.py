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
