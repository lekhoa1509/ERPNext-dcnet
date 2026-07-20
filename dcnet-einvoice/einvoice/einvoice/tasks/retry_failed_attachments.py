import frappe
from frappe.utils import add_days, now_datetime


def retry_failed_attachments():
    """Daily — retry records with attach_status='Lỗi' in last 7 days, retry_count < 5."""
    candidates = frappe.get_all(
        "EInvoice Inward",
        filters={
            "attach_status": "Lỗi",
            "creation": [">=", add_days(now_datetime(), -7)],
            "attach_retry_count": ["<", 5],
        },
        pluck="name",
    )
    if not candidates:
        return {"retried": 0}

    from einvoice.einvoice.services.attach import attach_files_batch
    frappe.enqueue(
        attach_files_batch,
        queue="long",
        job_id=f"einvoice_attach:scheduled:{frappe.utils.today()}",
        timeout=max(600, len(candidates) * 60),
        invoice_names=candidates,
        user="Administrator",
        source="scheduled",
    )
    return {"retried": len(candidates)}
