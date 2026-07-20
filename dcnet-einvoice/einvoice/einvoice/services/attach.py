"""
Attach Service — background download + attach PDF/XML cho EInvoice Inward.

Public API:
- enqueue_attach_files(invoice_names): whitelisted RPC entry, validates perm
  per invoice, enqueues attach_files_batch on `long` queue.
- attach_files_batch(invoice_names, user, source): worker entry; sequential
  per-invoice with 1 commit per invoice; creates 1 EInvoice Sync Log + 1
  Notification Log for the user when done.
- attach_files_for_invoice(invoice_name, provider): per-invoice algorithm,
  idempotent skip nếu cả 2 file đã có; download missing only.

Helpers (private):
- _compute_final_status: truth table → (status, error_text)
- _persist_file: save bytes via file_manager + idempotent delete-old
- _sanitize_filename: strip filesystem-unsafe chars, preserve VN diacritics
- _publish_realtime: SocketIO push to user
"""

import re
import unicodedata
from typing import Optional

import frappe
from frappe.utils import now_datetime
from frappe.utils.file_manager import save_file

from einvoice.einvoice.exceptions import EInvoiceProviderError


VALID_SOURCES = ("sync", "manual", "scheduled")


# ---------------------------------------------------------------------------
# Whitelisted entry
# ---------------------------------------------------------------------------
@frappe.whitelist()
def enqueue_attach_files(invoice_names) -> dict:
    """Enqueue attach job. Validates `read` permission per invoice.

    Accepts list[str] or JSON-serialized string (Frappe RPC param).
    """
    if isinstance(invoice_names, str):
        import json

        try:
            invoice_names = json.loads(invoice_names)
        except Exception:
            invoice_names = [invoice_names]
    if not isinstance(invoice_names, (list, tuple)) or not invoice_names:
        frappe.throw("invoice_names phải là list không rỗng")

    user = frappe.session.user
    for name in invoice_names:
        if not frappe.has_permission("EInvoice Inward", "read", name):
            raise frappe.PermissionError(
                f"Không có quyền đọc EInvoice Inward {name}"
            )

    # Reset retry_count khi user manual trigger (cho user 5 lần fresh)
    for name in invoice_names:
        frappe.db.set_value(
            "EInvoice Inward",
            name,
            "attach_retry_count",
            0,
            update_modified=False,
        )
    frappe.db.commit()

    job_id = f"einvoice_attach:manual:{frappe.utils.now()}"
    frappe.enqueue(
        attach_files_batch,
        queue="long",
        job_id=job_id,
        timeout=max(600, len(invoice_names) * 60),
        invoice_names=list(invoice_names),
        user=user,
        source="manual",
    )
    return {"enqueued": len(invoice_names), "job_id": job_id}


# ---------------------------------------------------------------------------
# Batch worker
# ---------------------------------------------------------------------------
def attach_files_batch(invoice_names, user: str, source: str = "sync") -> dict:
    """Sequential worker. 1 commit/invoice, 1 Sync Log entry for batch,
    1 Notification Log for the triggering user when done.
    """
    if source not in VALID_SOURCES:
        source = "manual"
    invoice_names = list(invoice_names or [])
    if not invoice_names:
        return {"ok": 0, "fail": 0, "partial": 0, "skip": 0}

    batch_id = frappe.generate_hash(length=10)
    sync_log = _create_sync_log(batch_id, source, user, len(invoice_names))

    # Lookup providers cache by EInvoice Inward → provider doc name
    provider_cache = {}

    counts = {"ok": 0, "fail": 0, "partial": 0, "skip": 0}
    errors = []

    for invoice_name in invoice_names:
        try:
            inv = frappe.get_doc("EInvoice Inward", invoice_name)
        except frappe.DoesNotExistError:
            counts["fail"] += 1
            errors.append(f"{invoice_name}: record không tồn tại")
            continue

        provider = provider_cache.get(inv.provider)
        if provider is None:
            try:
                provider = _resolve_provider(inv.provider)
                provider_cache[inv.provider] = provider
            except Exception as e:
                counts["fail"] += 1
                errors.append(f"{invoice_name}: provider load fail — {e}")
                _set_status(invoice_name, "Lỗi", str(e))
                frappe.db.commit()
                continue

        try:
            res = attach_files_for_invoice(invoice_name, provider)
        except Exception as e:
            counts["fail"] += 1
            errors.append(f"{invoice_name}: {type(e).__name__}: {e}")
            _set_status(invoice_name, "Lỗi", f"{type(e).__name__}: {e}")
            frappe.db.commit()
            continue

        # Tally
        status_field = frappe.db.get_value(
            "EInvoice Inward", invoice_name, "attach_status"
        )
        if status_field == "Đã đính kèm":
            counts["ok"] += 1
        elif status_field == "Một phần":
            counts["partial"] += 1
        elif status_field == "Lỗi":
            counts["fail"] += 1
            if res.get("error"):
                errors.append(f"{invoice_name}: {res['error']}")
        else:
            counts["skip"] += 1
        frappe.db.commit()

    _finalize_sync_log(sync_log, counts, errors)
    _create_notification(user, batch_id, counts, sync_log)
    return counts


# ---------------------------------------------------------------------------
# Per-invoice algorithm
# ---------------------------------------------------------------------------
def attach_files_for_invoice(invoice_name: str, provider) -> dict:
    """Returns {pdf, xml, error}. pdf/xml ∈ {ok, skip, fail}."""
    inv = frappe.get_doc("EInvoice Inward", invoice_name)

    needs_pdf = bool(getattr(inv, "pdf_url", None)) and not getattr(inv, "pdf_file", None)
    needs_xml = bool(getattr(inv, "xml_url", None)) and not getattr(inv, "xml_file", None)

    if not (needs_pdf or needs_xml):
        # Idempotent skip — if both files already attached & status not yet sync'd
        if getattr(inv, "pdf_file", None) and getattr(inv, "xml_file", None) and getattr(inv, "attach_status", None) != "Đã đính kèm":
            frappe.db.set_value(
                "EInvoice Inward",
                inv.name,
                "attach_status",
                "Đã đính kèm",
                update_modified=False,
            )
        return {"pdf": "skip", "xml": "skip", "error": None}

    _set_status(inv.name, "Đang tải", None)
    _publish_realtime(inv.name, "Đang tải")

    pdf_result, pdf_err = (
        _download_one(inv, "pdf", provider) if needs_pdf else ("skip", None)
    )
    # Refresh inv to pick up pdf_file just set
    inv = frappe.get_doc("EInvoice Inward", invoice_name)
    xml_result, xml_err = (
        _download_one(inv, "xml", provider) if needs_xml else ("skip", None)
    )

    error_text = pdf_err or xml_err
    status, computed_err = _compute_final_status(pdf_result, xml_result, inv)
    final_err = error_text or computed_err

    update = {"attach_status": status}
    if final_err is not None:
        update["attach_error"] = final_err[:500]
    if status == "Lỗi":
        update["attach_retry_count"] = (inv.attach_retry_count or 0) + 1

    frappe.db.set_value(
        "EInvoice Inward", inv.name, update, update_modified=False
    )
    _publish_realtime(inv.name, status)
    return {"pdf": pdf_result, "xml": xml_result, "error": final_err}


def _download_one(inv, kind: str, provider):
    """Download 1 file (pdf hoặc xml), persist to File doc + set field.

    Returns (result, error_text). result ∈ {ok, fail}.
    """
    url = getattr(inv, f"{kind}_url", None)
    if not url:
        return "skip", None
    try:
        content = provider.download_attachment(url, kind)
    except EInvoiceProviderError as e:
        return "fail", str(e)
    except Exception as e:
        return "fail", f"{type(e).__name__}: {e}"

    try:
        _persist_file(inv, kind, content)
    except Exception as e:
        return "fail", f"Persist fail: {type(e).__name__}: {e}"
    return "ok", None


# ---------------------------------------------------------------------------
# Final status truth table
# ---------------------------------------------------------------------------
def _compute_final_status(pdf_result: str, xml_result: str, inv) -> tuple:
    """Truth table — see spec.

    Returns (status, error_text or None).
    """
    pdf_present = bool(getattr(inv, "pdf_file", None)) or pdf_result == "ok"
    xml_present = bool(getattr(inv, "xml_file", None)) or xml_result == "ok"

    pdf_url_set = bool(getattr(inv, "pdf_url", None))
    xml_url_set = bool(getattr(inv, "xml_url", None))

    # Compute "needed" — only count source URLs that exist.
    pdf_needed = pdf_url_set
    xml_needed = xml_url_set

    pdf_ok = pdf_present or not pdf_needed
    xml_ok = xml_present or not xml_needed

    pdf_failed = pdf_result == "fail"
    xml_failed = xml_result == "fail"

    if pdf_ok and xml_ok and (pdf_present or xml_present):
        return "Đã đính kèm", None

    if pdf_failed and xml_failed:
        return "Lỗi", "Tải cả PDF và XML đều thất bại"

    if (pdf_failed and not xml_needed) or (xml_failed and not pdf_needed):
        return "Lỗi", "Tải file thất bại"

    if pdf_failed or xml_failed:
        return "Một phần", "Một file tải thất bại"

    if not (pdf_present or xml_present):
        # No source URLs to begin with — leave as empty (caller likely shouldn't reach here)
        return "Chưa tải", None
    return "Một phần", None


# ---------------------------------------------------------------------------
# File persistence
# ---------------------------------------------------------------------------
def _persist_file(invoice, kind: str, content: bytes) -> str:
    """Save bytes as private File doc, attach to invoice, set pdf_file/xml_file.

    Idempotent: deletes existing File with same fname before re-saving.
    Returns file_url.
    """
    ext = "pdf" if kind == "pdf" else "xml"
    base = (
        f"{invoice.get('invoice_pattern') or 'HD'}-"
        f"{invoice.get('invoice_serial') or ''}-"
        f"{invoice.get('invoice_number') or invoice.name}"
    )
    fname = _sanitize_filename(f"{base}.{ext}")

    existing = frappe.db.get_value(
        "File",
        {
            "attached_to_doctype": "EInvoice Inward",
            "attached_to_name": invoice.name,
            "file_name": fname,
        },
        "name",
    )
    if existing:
        frappe.delete_doc(
            "File", existing, ignore_permissions=True, delete_permanently=True
        )

    file_doc = save_file(
        fname=fname,
        content=content,
        dt="EInvoice Inward",
        dn=invoice.name,
        is_private=1,
    )
    frappe.db.set_value(
        "EInvoice Inward",
        invoice.name,
        f"{kind}_file",
        file_doc.file_url,
        update_modified=False,
    )
    return file_doc.file_url


_UNSAFE_RE = re.compile(r'[/\\:*?"<>|\x00-\x1f]')


def _sanitize_filename(s: str) -> str:
    """Strip filesystem-unsafe chars; preserve Vietnamese diacritics."""
    if not s:
        return "file"
    s = unicodedata.normalize("NFC", s)
    s = _UNSAFE_RE.sub("_", s)
    s = s.strip(" .")
    return s or "file"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _set_status(invoice_name: str, status: str, error: Optional[str]) -> None:
    update = {"attach_status": status}
    if error is not None:
        update["attach_error"] = error[:500]
    frappe.db.set_value(
        "EInvoice Inward", invoice_name, update, update_modified=False
    )


def _publish_realtime(invoice_name: str, status: str) -> None:
    try:
        frappe.publish_realtime(
            event="einvoice_attach_progress",
            message={"invoice_name": invoice_name, "status": status},
            after_commit=True,
        )
    except Exception:
        # Don't fail the worker on realtime publish errors
        pass


def _resolve_provider(provider_name: str):
    """Look up EInvoice Provider, instantiate provider class."""
    from einvoice.einvoice.providers import get_provider_class

    provider_doc = frappe.get_doc("EInvoice Provider", provider_name)
    cls = get_provider_class(provider_doc.provider_type)
    return cls(provider_doc)


def _create_sync_log(batch_id: str, source: str, user: str, total: int):
    """Best-effort Sync Log entry. Returns doc or None."""
    try:
        doc = frappe.get_doc(
            {
                "doctype": "EInvoice Sync Log",
                "batch_id": batch_id,
                "started_at": now_datetime(),
                "triggered_by": user,
                "source": source,
                "summary": f"Attach files batch — {total} hóa đơn",
            }
        ).insert(ignore_permissions=True)
        frappe.db.commit()
        return doc
    except Exception:
        return None


def _finalize_sync_log(sync_log, counts: dict, errors: list) -> None:
    if not sync_log:
        return
    try:
        msg = (
            f"OK: {counts['ok']}, Partial: {counts['partial']}, "
            f"Fail: {counts['fail']}, Skip: {counts['skip']}"
        )
        if errors:
            msg += "\n\nLỗi:\n" + "\n".join(errors[:50])
        frappe.db.set_value(
            "EInvoice Sync Log",
            sync_log.name,
            {"finished_at": now_datetime(), "result_message": msg[:5000]},
            update_modified=False,
        )
        frappe.db.commit()
    except Exception:
        pass


def _create_notification(user: str, batch_id: str, counts: dict, sync_log) -> None:
    try:
        n_ok = counts["ok"]
        n_total = sum(counts.values())
        n_fail = counts["fail"]
        subject = (
            f"Tải file Mắt Bão: {n_ok}/{n_total} thành công, {n_fail} lỗi"
        )
        body = (
            f"<p>Sync batch {batch_id}: {n_ok} OK, "
            f"{counts['partial']} một phần, {n_fail} lỗi, "
            f"{counts['skip']} bỏ qua.</p>"
        )
        log = {
            "doctype": "Notification Log",
            "subject": subject,
            "for_user": user,
            "type": "Alert",
            "email_content": body,
        }
        if sync_log:
            log["document_type"] = "EInvoice Sync Log"
            log["document_name"] = sync_log.name
        frappe.get_doc(log).insert(ignore_permissions=True)
        frappe.db.commit()
    except Exception:
        pass
