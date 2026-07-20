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
