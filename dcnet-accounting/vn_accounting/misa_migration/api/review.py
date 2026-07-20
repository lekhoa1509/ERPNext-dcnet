"""Misa Migration review API — Phase B."""

from __future__ import annotations

import json

import frappe
from frappe import _

from vn_accounting.misa_migration import state as st
from vn_accounting.misa_migration.importers.orchestrator import get_counts


@frappe.whitelist()
def list_rows(
    batch_name: str,
    file_type: str | None = None,
    status: str | None = None,
    search: str | None = None,
    page: int = 1,
    limit: int = 50,
) -> dict:
    """Server-paginated row listing for Review screen."""
    try:
        page = max(1, int(page))
        limit = min(200, max(1, int(limit)))
    except (TypeError, ValueError):
        page, limit = 1, 50

    filters = {"batch": batch_name}
    if file_type:
        filters["file_type"] = file_type
    if status:
        filters["status"] = status
    or_filters = []
    if search:
        or_filters = [
            ["raw_payload", "like", f"%{search}%"],
            ["target_name", "like", f"%{search}%"],
            ["error_message", "like", f"%{search}%"],
        ]

    total = frappe.db.count("Misa Migration Row", filters)
    rows = frappe.get_all(
        "Misa Migration Row",
        filters=filters,
        or_filters=or_filters or None,
        fields=["name", "row_index", "file_type", "entity_type", "status",
                "target_doctype", "target_name", "error_message",
                "raw_payload", "parsed_payload"],
        order_by="file_type asc, row_index asc",
        start=(page - 1) * limit,
        page_length=limit,
    )
    return {"rows": rows, "total": total, "page": page, "limit": limit}


@frappe.whitelist()
def aggregate_counts(batch_name: str) -> dict:
    return {"batch": batch_name, "counts": get_counts(batch_name)}


@frappe.whitelist()
def resolve_row(batch_name: str, row_name: str, action: str,
                rename_suffix: str | None = None) -> dict:
    """Resolve a Conflict row.

    Actions:
      skip      → status = Skipped
      use_existing → status = Exists (keep target_name, no create)
      overwrite → status = Ready (will overwrite existing on post; not implemented yet — uses rename for now)
      rename    → status = Ready, target_name modified with suffix (-MIGRATED default)
    """
    row = frappe.get_doc("Misa Migration Row", row_name)
    if row.batch != batch_name:
        frappe.throw(_("Row không thuộc batch này"))
    if row.status not in ("Conflict", "Invalid"):
        frappe.throw(_("Chỉ resolve được row ở trạng thái Conflict/Invalid (hiện: {0}).").format(row.status))

    if action == "skip":
        row.status = "Skipped"
    elif action == "use_existing":
        row.status = "Exists"
    elif action == "rename":
        suffix = rename_suffix or "-MIGRATED"
        try:
            normalized = json.loads(row.parsed_payload or "{}")
        except (ValueError, TypeError):
            normalized = {}
        # Append suffix to dedupe key — Phase B v1 stamp into parsed_payload
        # so the importer's build_doc uses the suffixed code.
        for key in ("_code", "uom_name", "_tk"):
            if normalized.get(key):
                normalized[key] = f"{normalized[key]}{suffix}"
                break
        row.parsed_payload = json.dumps(normalized, ensure_ascii=False)
        row.status = "Ready"
    elif action == "overwrite":
        # Phase B v1: treat as rename — true overwrite (delete+recreate) deferred
        row.status = "Ready"
    else:
        frappe.throw(_("Action không hợp lệ: {0}").format(action))

    row.error_message = None
    row.db_update()
    frappe.db.commit()
    return {"row": row_name, "new_status": row.status}


@frappe.whitelist()
def mark_reviewed(batch_name: str) -> dict:
    """Transition PARSED → REVIEWED after user confirms review.

    Blocks if any rows remain in Invalid (must skip or resolve first).

    UX Gap 4: also auto-promote rows at status='New' (the parser
    default) to 'Ready' so the Phase 0+4 orchestrators pick them up
    when Post runs. Without this, the operator must touch every row
    individually OR rely on a side-effect of conflict resolution —
    neither is acceptable for the bulk OB import flow where most rows
    don't have conflicts. Rows already at Ready/Exists/Skipped/Conflict
    are left alone; Invalid blocks the transition (checked above).
    """
    status = frappe.db.get_value("Misa Migration Batch", batch_name, "status")
    if status != st.PARSED:
        frappe.throw(_("Không thể mark reviewed ở trạng thái {0} — phải là PARSED.").format(status))

    n_invalid = frappe.db.count("Misa Migration Row",
                                {"batch": batch_name, "status": "Invalid"})
    if n_invalid > 0:
        frappe.throw(_("Còn {0} dòng Invalid — sửa hoặc skip trước khi tiếp tục.").format(n_invalid))

    # UX Gap 4: auto-promote unresolved New rows to Ready
    n_promoted = frappe.db.sql(
        """UPDATE `tabMisa Migration Row` SET status='Ready'
           WHERE batch=%s AND status='New'""",
        (batch_name,),
    )
    promoted_count = frappe.db.count(
        "Misa Migration Row", {"batch": batch_name, "status": "Ready"}
    )

    batch = frappe.get_doc("Misa Migration Batch", batch_name)
    with st.lock_for_batch(batch):
        batch = frappe.get_doc("Misa Migration Batch", batch_name)
        st.transition(batch, st.REVIEWED,
                      reason=f"user marked reviewed; {promoted_count} rows Ready")
        batch.save(ignore_permissions=True)
        frappe.db.commit()
    return {"batch": batch_name, "status": st.REVIEWED,
            "ready_rows": promoted_count}


@frappe.whitelist()
def skip_all_invalid(batch_name: str) -> dict:
    """Bulk-mark all Invalid rows in a batch as Skipped.

    Used by ReviewStep's quick-action banner when Misa source data has
    deterministic header/footer artifacts (e.g. 'Tổng' total rows, sub-header
    rows in Item file row #4) that fail validate() but should not block
    posting. Operator can click "Bỏ qua tất cả N dòng" to skip in one shot.
    """
    n = frappe.db.sql(
        """UPDATE `tabMisa Migration Row` SET status='Skipped'
           WHERE batch=%s AND status='Invalid'""",
        (batch_name,),
    )
    skipped = frappe.db.sql("SELECT ROW_COUNT()")[0][0]
    frappe.db.commit()
    return {"batch": batch_name, "skipped": int(skipped)}
