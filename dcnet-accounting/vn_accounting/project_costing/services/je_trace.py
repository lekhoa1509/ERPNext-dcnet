"""JE traceability — fetch Journal Entries linked to a Project Costing master.

Embedded section on Project Costing form renders 4 grouped lists (one per
marker type). Each row contains JE name, date, net amount, source ref, link.

Marker shape: `[PROJECT_COSTING:<costing>][TYPE:<X>]` where X ∈ {
  ALLOCATION_RUN, WIP_OVERRIDE, STAGE_COGS, CLOSE_WRITEOFF }.
"""
from __future__ import annotations

import re

import frappe
from frappe import _
from frappe.utils import flt

from vn_accounting.project_costing.services.close_engine import compute_wip_balance


_TYPE_LABELS = {
    "ALLOCATION_RUN": _("Phân bổ chi phí gián tiếp"),
    "WIP_OVERRIDE": _("Bù tài khoản WIP"),
    "STAGE_COGS": _("Giá vốn theo giai đoạn"),
    "CLOSE_WRITEOFF": _("Write-off khi đóng công trình"),
}

_GROUP_ORDER = ["ALLOCATION_RUN", "WIP_OVERRIDE", "STAGE_COGS", "CLOSE_WRITEOFF"]


@frappe.whitelist()
def get_project_costing_jes(costing_name: str) -> dict:
    """Return grouped JE rows for embedded section.

    Returns:
        {
          "groups": [
            {"type": "<X>", "label": "...", "rows": [...], "total": float},
            ...
          ],
          "wip_balance": float,   # current 154 balance for project
        }
    """
    if not frappe.db.exists("Project Costing", costing_name):
        return {"groups": [], "wip_balance": 0}

    project = frappe.db.get_value("Project Costing", costing_name, "project")

    # Strategy 1: marker substring lookup for [PROJECT_COSTING:<costing>] —
    # matches WIP_OVERRIDE / STAGE_COGS / CLOSE_WRITEOFF where the marker
    # encodes the costing name directly.
    base_marker = f"[PROJECT_COSTING:{costing_name}]"
    direct_rows = frappe.db.sql("""
        SELECT name, posting_date, user_remark, total_debit
        FROM `tabJournal Entry`
        WHERE docstatus = 1
          AND user_remark LIKE %s
        ORDER BY posting_date DESC, name DESC
    """, (f"%{base_marker}%",), as_dict=True)

    # Strategy 2: CAR allocations — JE marker uses CAR.name not project name.
    # Find JEs via JEA reference_type='Cost Allocation Run' + project filter.
    car_rows = []
    if project:
        car_rows = frappe.db.sql("""
            SELECT DISTINCT je.name, je.posting_date, je.user_remark,
                   SUM(jea.debit_in_account_currency) AS amount
            FROM `tabJournal Entry Account` jea
            JOIN `tabJournal Entry` je ON je.name = jea.parent
            WHERE je.docstatus = 1
              AND jea.reference_type = 'Cost Allocation Run'
              AND jea.project = %s
            GROUP BY je.name
            ORDER BY je.posting_date DESC, je.name DESC
        """, (project,), as_dict=True)

    # Bucket by TYPE marker
    type_re = re.compile(r"\[TYPE:(\w+)\]")
    by_type: dict[str, list[dict]] = {t: [] for t in _GROUP_ORDER}
    seen_je_names: set[str] = set()

    def _bucket(r, override_amount=None):
        if r.name in seen_je_names:
            return
        seen_je_names.add(r.name)
        m = type_re.search(r.user_remark or "")
        if not m:
            return
        t = m.group(1)
        if t not in by_type:
            return
        # Extract source ref if present
        src_match = re.search(r"\[SRC:([^:\]]+):([^\]]+)\]", r.user_remark or "")
        si_match = re.search(r"\[SI:([^\]]+)\]", r.user_remark or "")
        car_match = re.search(r"\[PROJECT_COSTING:(CAR-[^\]]+)\]", r.user_remark or "")
        ref_label = ""
        if src_match:
            ref_label = f"{src_match.group(1)} {src_match.group(2)}"
        elif si_match:
            ref_label = f"SI {si_match.group(1)}"
        elif car_match:
            ref_label = car_match.group(1)
        by_type[t].append({
            "je_name": r.name,
            "posting_date": r.posting_date,
            "amount": flt(override_amount if override_amount is not None else r.get("total_debit") or r.get("amount")),
            "ref": ref_label,
            "url": f"/app/journal-entry/{r.name}",
        })

    for r in direct_rows:
        _bucket(r)
    for r in car_rows:
        # For CAR JEs, the JE's total_debit is the multi-project sum; use
        # this-project share instead (already computed in query)
        _bucket(r, override_amount=r.amount)

    # Build groups in deterministic order
    groups = []
    for t in _GROUP_ORDER:
        rows = by_type.get(t, [])
        groups.append({
            "type": t,
            "label": _TYPE_LABELS.get(t, t),
            "rows": rows,
            "total": sum(r["amount"] for r in rows),
        })

    # WIP balance probe
    project = frappe.db.get_value("Project Costing", costing_name, "project")
    company = frappe.db.get_value("Project Costing", costing_name, "company")
    balance = compute_wip_balance(project, company) if (project and company) else 0

    return {
        "groups": groups,
        "wip_balance": balance,
    }
