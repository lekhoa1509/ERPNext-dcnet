"""Misa Account Conflicts — list TKs where Misa name differs from Frappe.

Default auto-resolve (via backfill_audit_fixes step 9) keeps Frappe canonical.
This report surfaces the conflicts so users can review per row and apply
Misa's name via the inline "Rename to Misa" button (rendered by the JS).
"""
from __future__ import annotations

import json
from typing import Any


def execute(filters: dict[str, Any] | None = None) -> tuple[list[dict], list[dict]]:
    filters = filters or {}
    columns = [
        {"label": "Hàng", "fieldname": "row", "fieldtype": "Data", "width": 100},
        {"label": "Đợt nhập", "fieldname": "batch", "fieldtype": "Data", "width": 130},
        {"label": "TK", "fieldname": "misa_tk", "fieldtype": "Data", "width": 80},
        {"label": "Tên Misa", "fieldname": "misa_name", "fieldtype": "Data", "width": 240},
        {"label": "Tên Frappe (hiện tại)", "fieldname": "frappe_name", "fieldtype": "Link",
         "options": "Account", "width": 280},
        {"label": "Trạng thái", "fieldname": "status", "fieldtype": "Data", "width": 90},
        {"label": "Ghi chú", "fieldname": "note", "fieldtype": "Data", "width": 240},
    ]

    from vn_accounting.misa_migration.bulk_pump.account_conflicts import list_account_conflicts
    raw = list_account_conflicts(batch=filters.get("batch"))
    data = []
    for r in raw:
        data.append({
            "row": r["row"],
            "batch": r["batch"],
            "misa_tk": r["misa_tk"],
            "misa_name": r["misa_name"],
            "frappe_name": r["frappe_name"],
            "status": r["status"],
            "note": (r["error_message"] or "")[:200],
        })
    return columns, data
