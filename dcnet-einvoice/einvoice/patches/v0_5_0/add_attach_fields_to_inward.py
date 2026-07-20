"""
Backfill `attach_status="Chưa tải"` on existing EInvoice Inward records that
have a Mắt Bão URL but no local file yet, so users can run the bulk action
to retroactively download.
"""

import frappe


def execute():
    # Force schema sync so new columns exist before we backfill.
    frappe.reload_doc("einvoice", "doctype", "einvoice_inward")

    if not frappe.db.has_column("EInvoice Inward", "attach_status"):
        return

    candidates = frappe.db.sql(
        """
        SELECT name FROM `tabEInvoice Inward`
        WHERE (IFNULL(pdf_url,'')<>'' OR IFNULL(xml_url,'')<>'')
          AND IFNULL(pdf_file,'')=''
          AND IFNULL(xml_file,'')=''
          AND IFNULL(attach_status,'')=''
        """,
        as_dict=False,
    )
    if not candidates:
        return

    for (name,) in candidates:
        frappe.db.set_value(
            "EInvoice Inward",
            name,
            "attach_status",
            "Chưa tải",
            update_modified=False,
        )
    frappe.db.commit()
