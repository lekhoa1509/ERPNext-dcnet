"""Viettel S-Invoice Provider — Stub for future implementation."""

from dcnet_apps.einvoice.providers.base import BaseProvider


class ViettelProvider(BaseProvider):
    def authenticate(self):
        raise NotImplementedError("Viettel provider chưa được implement.")

    def fetch_inward_invoices(self, from_date, to_date):
        raise NotImplementedError("Viettel provider chưa được implement.")

    def parse_inward_invoice(self, raw_data):
        raise NotImplementedError("Viettel provider chưa được implement.")

    def get_invoice_templates(self):
        raise NotImplementedError("Viettel provider chưa được implement.")

    def issue_outward_invoice(self, invoice_data):
        raise NotImplementedError("Viettel provider chưa được implement.")

    def cancel_invoice(self, invoice_ref, reason):
        raise NotImplementedError("Viettel provider chưa được implement.")
