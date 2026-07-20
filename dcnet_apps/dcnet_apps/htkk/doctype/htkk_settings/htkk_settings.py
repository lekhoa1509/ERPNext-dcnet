"""HTKK Settings — cấu hình chung và mapping tài khoản cho module HTKK."""

import frappe
from frappe.model.document import Document


class HTKKSettings(Document):
    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from frappe.types import DF

        from dcnet_apps.htkk.doctype.htkk_account_mapping.htkk_account_mapping import (
            HTKKAccountMapping,
        )

        account_mapping: DF.Table[HTKKAccountMapping]
        default_cit_rate: DF.Percent
        default_finance_book: DF.Link | None
    # end: auto-generated types

    @frappe.whitelist()
    def seed_default_mapping(self):
        """Gọi từ nút 'Tạo mapping mặc định' trên form."""
        from dcnet_apps.htkk.install import seed_default_mapping

        vn_companies = frappe.get_all(
            "Company",
            filters={"country": "Vietnam"},
            pluck="name",
        )
        for company in vn_companies:
            seed_default_mapping(company)

        frappe.msgprint(
            f"Đã tạo mapping mặc định cho {len(vn_companies)} công ty Việt Nam.",
            alert=True,
        )
