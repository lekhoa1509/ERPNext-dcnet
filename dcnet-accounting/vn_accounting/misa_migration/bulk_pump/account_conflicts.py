"""Account Conflict review API — list Misa Account Conflicts and let user
choose Frappe vs Misa canonical name per row.

Default auto-resolve (in backfill_audit_fixes step 9) keeps Frappe name.
This API surfaces the conflicts so a user can override per row.

Whitelisted entries (UI consumers):
  list_account_conflicts(batch=None) -> [{...}]
      Return all Conflict rows for the batch (or globally) with Misa name vs
      Frappe canonical name side-by-side.
  rename_account_to_misa(row_name, new_misa_name) -> {ok, ...}
      Apply the Misa name to the Frappe Account (rename_doc + GL cascades).
"""
from __future__ import annotations

import json
from typing import Any

import frappe


@frappe.whitelist()
def list_account_conflicts(batch: str | None = None) -> list[dict[str, Any]]:
    """Return conflicts as a list of {row, misa_tk, misa_name, frappe_name,
    error_message} dicts."""
    where = "WHERE file_type='Account' AND status IN ('Conflict','Posted')"
    args: tuple = ()
    if batch:
        where += " AND batch=%s"
        args = (batch,)
    rows = frappe.db.sql(
        f"""SELECT name, batch, status, raw_payload, error_message, target_name
            FROM `tabMisa Migration Row` {where} AND error_message LIKE %s
            ORDER BY name""",
        args + ("%đã có tên%",) if args else ("%đã có tên%",),
        as_dict=True,
    )
    out: list[dict[str, Any]] = []
    for r in rows:
        try:
            p = json.loads(r.raw_payload or "{}")
        except (TypeError, ValueError):
            p = {}
        misa_tk = p.get("Số tài khoản", "")
        misa_name = p.get("Tên tài khoản", "")
        frappe_name = r.target_name or ""
        if not frappe_name and misa_tk:
            # Find Frappe canonical via account_resolver
            from vn_accounting.misa_migration.bulk_pump import account_resolver
            frappe_name = account_resolver.resolve(str(misa_tk),
                frappe.db.get_value("Misa Migration Batch", r.batch, "company")) or ""
        out.append({
            "row": r.name,
            "batch": r.batch,
            "status": r.status,
            "misa_tk": misa_tk,
            "misa_name": misa_name,
            "frappe_name": frappe_name,
            "error_message": r.error_message,
        })
    return out


@frappe.whitelist()
def rename_account_to_misa(row_name: str, new_misa_name: str | None = None) -> dict[str, Any]:
    """Apply Misa's name to the matching Frappe Account.

    Args:
      row_name: Misa Migration Row.name
      new_misa_name: override the name to apply (defaults to row's Misa Tên tài khoản)

    Renames Account.account_name (and updates the docname which is composed
    from <number> - <name> - <abbr>) via frappe.rename_doc — this cascades
    to every GL Entry/JE Account/Payment/etc.
    """
    row = frappe.db.get_value(
        "Misa Migration Row",
        row_name,
        ["raw_payload", "target_name", "batch"],
        as_dict=True,
    )
    if not row:
        return {"ok": False, "error": "Row not found"}
    try:
        p = json.loads(row.raw_payload or "{}")
    except (TypeError, ValueError):
        return {"ok": False, "error": "Cannot parse raw_payload"}

    misa_name = new_misa_name or p.get("Tên tài khoản")
    if not misa_name:
        return {"ok": False, "error": "No Misa name to apply"}

    company = frappe.db.get_value("Misa Migration Batch", row.batch, "company")
    abbr = frappe.db.get_value("Company", company, "abbr") or ""
    account_number = (p.get("Số tài khoản") or "").strip()

    # Resolve current Frappe Account
    from vn_accounting.misa_migration.bulk_pump import account_resolver
    current_name = row.target_name or account_resolver.resolve(account_number, company)
    if not current_name or not frappe.db.exists("Account", current_name):
        return {"ok": False, "error": f"No matching Frappe account for TK {account_number}"}

    new_full_name = f"{account_number} - {misa_name} - {abbr}"
    if current_name == new_full_name:
        return {"ok": True, "no_change": True, "name": current_name}

    # Update account_name + rename
    frappe.db.set_value("Account", current_name, "account_name", misa_name,
                        update_modified=False)
    frappe.rename_doc("Account", current_name, new_full_name,
                      force=True, ignore_permissions=True)
    # Update Migration Row marker
    frappe.db.set_value("Misa Migration Row", row_name, {
        "target_name": new_full_name,
        "status": "Posted",
        "error_message": f"RENAMED to Misa name: {misa_name}",
    }, update_modified=False)
    # Invalidate resolver cache
    account_resolver.reset()
    frappe.db.commit()
    return {"ok": True, "old_name": current_name, "new_name": new_full_name}
