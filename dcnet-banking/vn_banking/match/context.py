from dataclasses import dataclass, field
from datetime import date, timedelta
from decimal import Decimal

import frappe

from vn_banking.match.base import InvoiceRef


@dataclass
class MatchContext:
    bank_account: str
    company: str
    direction: str                                          # "credit" or "debit"
    party_invoice_type: str                                 # "Sales Invoice" | "Purchase Invoice"
    party_type: str                                         # "Customer" | "Supplier"
    posting_date_window: tuple[date, date] = (date.min, date.max)
    outstanding_invoices: dict[str, list[InvoiceRef]] = field(default_factory=dict)
    party_by_bank_account: dict[str, str] = field(default_factory=dict)
    tolerance: Decimal = Decimal("1000")
    settings: object = None                                 # frappe.get_single("Bank Statement Settings")

    def for_direction(self, direction: str) -> "MatchContext":
        """Return a shallow-copied context flipped to the given direction."""
        if direction == self.direction:
            return self
        return build_context(
            bank_account=self.bank_account,
            from_date=self.posting_date_window[0],
            to_date=self.posting_date_window[1],
            direction=direction,
            settings=self.settings,
        )


def build_context(bank_account: str, from_date: date, to_date: date,
                  direction: str = "credit", settings=None) -> MatchContext:
    """Build a MatchContext -- 1 SQL per invoice type to preload outstanding invoices."""
    if settings is None:
        settings = frappe.get_single("Bank Statement Settings")
    tolerance = Decimal(str(settings.tolerance_fixed_amount or 1000))
    tol_days = int(settings.amount_date_tolerance_days or 3)
    company = frappe.db.get_value("Bank Account", bank_account, "company") or frappe.defaults.get_user_default("Company")

    if direction == "credit":
        party_invoice_type = "Sales Invoice"
        party_type = "Customer"
    else:
        party_invoice_type = "Purchase Invoice"
        party_type = "Supplier"

    party_field = "customer" if party_type == "Customer" else "supplier"
    rows = frappe.db.sql(
        f"""
        SELECT name, {party_field} AS party, outstanding_amount, posting_date
        FROM `tab{party_invoice_type}`
        WHERE docstatus = 1
          AND company = %(company)s
          AND outstanding_amount > 0
          AND posting_date BETWEEN %(from_date)s AND %(to_date)s
        """,
        {"company": company,
         "from_date": from_date - timedelta(days=tol_days * 10),
         "to_date": to_date + timedelta(days=tol_days * 10)},
        as_dict=True,
    )
    outstanding: dict[str, list[InvoiceRef]] = {}
    for r in rows:
        outstanding.setdefault(r.party, []).append(
            InvoiceRef(doctype=party_invoice_type, name=r.name, outstanding=Decimal(str(r.outstanding_amount)))
        )

    party_by_bank_account = dict(frappe.db.sql("""
        SELECT bank_account_no, party
        FROM `tabBank Account`
        WHERE bank_account_no IS NOT NULL AND bank_account_no != ''
    """) or [])

    return MatchContext(
        bank_account=bank_account,
        company=company,
        direction=direction,
        party_invoice_type=party_invoice_type,
        party_type=party_type,
        posting_date_window=(from_date, to_date),
        outstanding_invoices=outstanding,
        party_by_bank_account=party_by_bank_account,
        tolerance=tolerance,
        settings=settings,
    )
