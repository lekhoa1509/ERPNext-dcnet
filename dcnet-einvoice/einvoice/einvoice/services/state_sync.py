"""Sync trạng thái HĐ đầu ra đã đẩy lên provider (EasyInvoice).

Orchestrator: sync_pending_invoices() được gọi từ scheduler cron mỗi 15min.
"""
import frappe
from frappe.utils import now_datetime

from einvoice.einvoice.exceptions import EInvoiceProviderError


def sync_pending_invoices(provider_name=None) -> dict:
    """Sync state cho mọi SI đã pushed nhưng chưa issued.

    Groups by einvoice_provider, batches 50 SI per API call.
    Returns: {checked: int, updated: int}
    """
    filters = {"docstatus": 1, "einvoice_pushed": 1, "einvoice_issued": 0}
    if provider_name:
        filters["einvoice_provider"] = provider_name

    pending = frappe.get_all(
        "Sales Invoice",
        filters=filters,
        fields=["name", "einvoice_ikey", "einvoice_provider"],
        limit=500,
    )
    if not pending:
        return {"checked": 0, "updated": 0}

    # Group by provider
    by_provider = {}
    for si in pending:
        if not si.einvoice_provider or not si.einvoice_ikey:
            continue
        by_provider.setdefault(si.einvoice_provider, []).append(si)

    total_updated = 0
    for prov_name, sis in by_provider.items():
        prov_doc = frappe.get_doc("EInvoice Provider", prov_name)
        if not prov_doc.enabled or not prov_doc.get("enable_outward"):
            continue
        try:
            provider = prov_doc.get_provider_instance()
            provider.authenticate()
        except Exception as e:
            frappe.log_error(
                title=f"[EInvoice] Outward sync auth failed: {prov_name}",
                message=str(e),
            )
            continue

        # Batch 50 ikeys per call
        for i in range(0, len(sis), 50):
            batch = sis[i:i + 50]
            ikeys = [si.einvoice_ikey for si in batch]
            try:
                states = provider.sync_invoice_state(ikeys)
            except EInvoiceProviderError as e:
                frappe.log_error(
                    title=f"[EInvoice] sync_invoice_state failed: {prov_name}",
                    message=str(e),
                )
                continue

            for si in batch:
                state = states.get(si.einvoice_ikey)
                if not state or state.get("error") == "not_found":
                    continue
                if state.get("invoice_status") is None:
                    continue
                total_updated += _apply_state_update(
                    si.name, state, prov_name, provider
                )

            frappe.db.commit()

    return {"checked": len(pending), "updated": total_updated}


def _apply_state_update(si_name: str, state: dict, provider_name: str, provider) -> int:
    """Apply provider state to SI. Idempotent. Returns 1 if updated."""
    code = state.get("invoice_status")
    text = state.get("status_text") or ""
    updates = {"einvoice_status_text": text}

    if code in (1, 2):
        updates.update({
            "einvoice_issued": 1,
            "einvoice_number": state.get("no") or "",
            "einvoice_lookup_code": state.get("lookup_code") or "",
            "einvoice_link_view": state.get("link_view") or "",
            "einvoice_issued_at": now_datetime(),
        })
        # Enqueue download PDF/XML in background
        ikey = state.get("ikey") or ""
        if ikey:
            frappe.enqueue(
                "einvoice.einvoice.services.state_sync._download_and_attach",
                queue="long",
                si_name=si_name,
                ikey=ikey,
                provider_name=provider_name,
                timeout=120,
            )
    elif code == 5:
        updates["einvoice_status_text"] = "Đã hủy trên EasyInvoice"

    frappe.db.set_value("Sales Invoice", si_name, updates, update_modified=False)
    return 1


def _download_and_attach(si_name: str, ikey: str, provider_name: str):
    """Background job: tải PDF + XML và đính kèm vào SI."""
    if not ikey:
        return
    prov_doc = frappe.get_doc("EInvoice Provider", provider_name)
    provider = prov_doc.get_provider_instance()
    si = frappe.get_doc("Sales Invoice", si_name)

    for kind in ("pdf", "xml"):
        target_field = "einvoice_pdf_url" if kind == "pdf" else "einvoice_xml_file"
        if si.get(target_field):
            continue  # already attached, skip

        try:
            content = provider.download_attachment(ikey, kind)
        except Exception as e:
            frappe.log_error(
                title=f"[EInvoice] Download {kind} failed: {si_name}",
                message=str(e),
            )
            continue

        ext = kind
        filename = f"{si_name}-einvoice.{ext}"
        file_doc = frappe.get_doc({
            "doctype": "File",
            "file_name": filename,
            "attached_to_doctype": "Sales Invoice",
            "attached_to_name": si_name,
            "is_private": 1,
            "content": content,
        })
        file_doc.insert(ignore_permissions=True)

        frappe.db.set_value(
            "Sales Invoice", si_name, target_field,
            file_doc.file_url, update_modified=False
        )

    frappe.db.commit()
