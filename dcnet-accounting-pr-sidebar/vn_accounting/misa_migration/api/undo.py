"""Misa Migration undo API — Phase B base + Phase E constraint checks + force.

Phase E commit 6 adds:
  * constraint_check(batch_name) — query dependent docs (Payment Entry
    references, child Stock Entries, etc.) NOT created by this batch
    that block clean Undo.
  * start_undo(batch_name, force=False, sync=False) — refuses if
    constraint_check returns blocking dependents UNLESS force=True.
    force=True logs a warning + proceeds; downstream docs may end up
    referencing cancelled vouchers.
"""

from __future__ import annotations

import frappe
from frappe import _

from vn_accounting.misa_migration import state as st
from vn_accounting.misa_migration.jobs import undo_job


# Dependent-edge mapping: for each batch-created DocType, list the
# (DocType, foreign-key field) pairs to scan for external references.
_DEPENDENT_EDGES: dict[str, list[tuple[str, str]]] = {
    "Sales Invoice": [
        ("Payment Entry Reference", "reference_name"),
        ("Delivery Note Item", "against_sales_invoice"),
    ],
    "Purchase Invoice": [
        ("Payment Entry Reference", "reference_name"),
        ("Purchase Receipt Item", "purchase_invoice"),
    ],
    "Payment Entry": [
        # PEs rarely have downstream dependents; included for symmetry
    ],
    "Journal Entry": [
        # JE rows can be referenced by next JE via against_jvno but that's
        # informational; no FK enforced. Skip.
    ],
    "Stock Entry": [
        ("Stock Entry Detail", "against_stock_entry"),
    ],
}


def _list_batch_posted_targets(batch_name: str) -> list[dict]:
    """Return [{target_doctype, target_name}] for all Posted rows in batch."""
    return frappe.db.sql(
        """
        SELECT DISTINCT target_doctype, target_name
        FROM `tabMisa Migration Row`
        WHERE batch=%s AND status='Posted'
          AND target_doctype IS NOT NULL AND target_name IS NOT NULL
        """,
        (batch_name,),
        as_dict=True,
    )


def _find_external_dependents(
    posted: list[dict],
    batch_target_names: set[str],
) -> list[dict]:
    """For each posted doc, list dependent docs NOT in batch_target_names.

    Args:
      posted: list of {target_doctype, target_name} dicts.
      batch_target_names: set of all docs created by THIS batch, used to
                          exclude same-batch internal references (e.g. PE
                          allocating to a batch-created SI is OK if the PE
                          itself is also batch-created and will be undone).

    Returns:
      List of {posted_doctype, posted_name, dependent_doctype,
               dependent_name, dependent_field} dicts.
    """
    out: list[dict] = []
    by_target_dt: dict[str, list[str]] = {}
    for p in posted:
        by_target_dt.setdefault(p["target_doctype"], []).append(p["target_name"])

    for target_dt, names in by_target_dt.items():
        edges = _DEPENDENT_EDGES.get(target_dt) or []
        if not edges or not names:
            continue
        for dep_dt, dep_field in edges:
            # Check whether the dependent DocType has the named field
            try:
                meta = frappe.get_meta(dep_dt)
                if not meta.has_field(dep_field):
                    continue
            except Exception:
                continue

            placeholders = ",".join(["%s"] * len(names))
            # parent-vs-child handling: child tables have parent column
            try:
                child_table = meta.istable
            except AttributeError:
                child_table = False

            if child_table:
                rows = frappe.db.sql(
                    f"""
                    SELECT DISTINCT parent, parenttype, {dep_field} AS dep_name
                    FROM `tab{dep_dt}`
                    WHERE {dep_field} IN ({placeholders})
                    """,
                    tuple(names),
                    as_dict=True,
                )
                for r in rows:
                    if r["parent"] in batch_target_names:
                        continue
                    out.append({
                        "posted_doctype": target_dt,
                        "posted_name": r["dep_name"],
                        "dependent_doctype": r.get("parenttype") or dep_dt,
                        "dependent_name": r["parent"],
                        "dependent_field": dep_field,
                    })
            else:
                rows = frappe.db.sql(
                    f"""
                    SELECT name, {dep_field} AS dep_name
                    FROM `tab{dep_dt}`
                    WHERE {dep_field} IN ({placeholders})
                    """,
                    tuple(names),
                    as_dict=True,
                )
                for r in rows:
                    if r["name"] in batch_target_names:
                        continue
                    out.append({
                        "posted_doctype": target_dt,
                        "posted_name": r["dep_name"],
                        "dependent_doctype": dep_dt,
                        "dependent_name": r["name"],
                        "dependent_field": dep_field,
                    })
    return out


@frappe.whitelist()
def constraint_check(batch_name: str) -> dict:
    """Find external docs referencing batch-created docs.

    Returns:
      {
        "batch": str,
        "blocked_docs": [{posted_*, dependent_*, dependent_field}, ...],
        "blocked_count": int,
        "checked_posted_count": int,
        "can_undo_cleanly": bool,
      }
    """
    posted = _list_batch_posted_targets(batch_name)
    batch_names = {p["target_name"] for p in posted if p.get("target_name")}
    blocked = _find_external_dependents(posted, batch_names)
    return {
        "batch": batch_name,
        "blocked_docs": blocked,
        "blocked_count": len(blocked),
        "checked_posted_count": len(posted),
        "can_undo_cleanly": len(blocked) == 0,
    }


@frappe.whitelist()
def start_undo(
    batch_name: str,
    force: bool = False,
    sync: bool = False,
) -> dict:
    """Enqueue undo_batch on a POSTED batch.

    Args:
      batch_name: target batch.
      force: bypass constraint_check blocking dependents (logs warning).
      sync: run synchronously instead of enqueuing.
    """
    status = frappe.db.get_value("Misa Migration Batch", batch_name, "status")
    if status != st.POSTED:
        frappe.throw(_("Không thể Undo ở trạng thái {0} — phải là POSTED.").format(status))

    constraints = constraint_check(batch_name)
    if not force and constraints["blocked_count"] > 0:
        preview = constraints["blocked_docs"][:10]
        lines = [
            f"{b['dependent_doctype']} {b['dependent_name']} "
            f"đang tham chiếu {b['posted_doctype']} {b['posted_name']}"
            for b in preview
        ]
        more = f"\n…và {constraints['blocked_count'] - 10} bản ghi khác" \
            if constraints['blocked_count'] > 10 else ""
        frappe.throw(
            _("Không thể Undo: {0} bản ghi bên ngoài batch đang tham chiếu "
              "đến doc do batch tạo. Gửi force=true để bỏ qua (rủi ro "
              "tham chiếu orphan).\n\n{1}{2}")
            .format(constraints["blocked_count"], "\n".join(lines), more)
        )
    if force and constraints["blocked_count"] > 0:
        frappe.log_error(
            title=f"Misa Undo forced with {constraints['blocked_count']} dependents",
            message=f"Batch {batch_name} undone with force=True; "
                    f"{constraints['blocked_count']} external dependents may "
                    f"now reference cancelled docs.",
        )

    if sync:
        return undo_job.undo_batch(batch_name)

    job = frappe.enqueue(
        "vn_accounting.misa_migration.jobs.undo_job.undo_batch",
        batch_name=batch_name, queue="default", timeout=14400,
    )
    frappe.db.set_value("Misa Migration Batch", batch_name, "job_id", job.id, update_modified=False)
    frappe.db.commit()
    return {
        "batch": batch_name, "queued": True, "job_id": job.id,
        "forced": force, "dependent_count": constraints["blocked_count"],
    }


@frappe.whitelist()
def get_undo_progress(batch_name: str) -> dict:
    from vn_accounting.misa_migration.importers.orchestrator import get_counts
    batch_status = frappe.db.get_value("Misa Migration Batch", batch_name, "status")
    counts = get_counts(batch_name)
    n_reversed = sum(c.get("Reversed", 0) for c in counts.values())
    return {"batch": batch_name, "status": batch_status,
            "counts": counts, "reversed": n_reversed}
