"""Post Journal Entries for submitted Asset Repairs with no posted_je.

Covers all classifications — Chi phí (D 6427/C 111), Sửa chữa lớn vốn hóa
(D 2413/C 331), Nâng cấp cải tạo (D 2412/C 331). Pre-v0.5.0 flow had no
posting for any classification without PI/Stock Consumption; this patch
backfills all of them.

Uses the first available Supplier as a placeholder party for TK 331 (Payable)
credit entries. This is acceptable for demo/backfill: production ARs will have
a real supplier selected by the accountant before submit.

Idempotent: WHERE clause limits to posted_je IS NULL rows only.
"""
from __future__ import annotations

import frappe
from vn_accounting.utils.accounting_posting import build_default_entries, post_je_from_entries


def _get_default_supplier() -> str | None:
    rows = frappe.db.sql_list("SELECT name FROM `tabSupplier` ORDER BY name LIMIT 1")
    return rows[0] if rows else None


def execute() -> None:
    if not frappe.db.exists("DocType", "Asset Repair"):
        return

    rows = frappe.db.sql(
        """SELECT name, repair_classification, repair_cost, company,
                  completion_date, has_vat, vat_rate, asset_name
           FROM `tabAsset Repair`
           WHERE docstatus = 1
             AND repair_classification IN ('Chi phí', 'Sửa chữa lớn vốn hóa', 'Nâng cấp cải tạo')
             AND (posted_je IS NULL OR posted_je = '')""",
        as_dict=True,
    )

    if not rows:
        return

    default_supplier = _get_default_supplier()

    for row in rows:
        try:
            entries = build_default_entries(
                event_type="Asset Repair",
                classification=row.repair_classification,
                amount=row.repair_cost,
                has_vat=bool(row.has_vat),
                vat_rate=float(row.vat_rate or 10),
                company=row.company,
                asset_name=row.asset_name,
            )
            # TK 331 credit requires party. Add default supplier for backfill.
            if default_supplier:
                for entry in entries:
                    credit_acc = entry.get("account_credit", "")
                    if "331" in credit_acc:
                        entry["party_type"] = "Supplier"
                        entry["party"] = default_supplier

            posting_date = str(row.completion_date)[:10] if row.completion_date else frappe.utils.today()
            remark = f"Hạch toán sửa chữa TSCĐ {row.name} ({row.repair_classification})"
            je_name = post_je_from_entries(
                entries=entries,
                company=row.company,
                posting_date=posting_date,
                user_remark=remark,
                ref_doctype="Asset Repair",
                ref_name=row.name,
                submit=True,
            )
            frappe.db.set_value("Asset Repair", row.name, "posted_je", je_name, update_modified=False)
        except Exception as exc:
            frappe.log_error(f"backfill_asset_repair_je: {row.name} — {exc}", "Patch v0_5_0")

    frappe.db.commit()
