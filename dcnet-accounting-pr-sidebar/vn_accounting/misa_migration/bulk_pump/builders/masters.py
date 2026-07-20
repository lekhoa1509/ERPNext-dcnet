"""Phase 1/3 master bulk-pump — Employee, Bank Account.

ORM Phase importers fail on these for various validation reasons (missing
Department FK, Bank parent record, locale-specific name quirks). This SQL
path is the bulk_pump alternative: skip validate/hooks, insert minimal
NOT-NULL fields directly. The created records are bare master rows good
enough for downstream voucher references (party_type=Employee, PE.bank_account).

Each builder returns {target_dt: [row_dict, ...]} compatible with
bulk_executor.bulk_insert(). Builders also mark Misa Migration Row →
Posted via the runner (orchestrator does the UPDATE after inserts succeed).
"""
from __future__ import annotations

import json
import secrets
from typing import Any

import frappe


def _gen_name() -> str:
    return secrets.token_hex(5)


# -----------------------------------------------------------------------
# Employee — Misa shape:
#   STT, Mã nhân viên, Tên nhân viên, Chức danh, Tên đơn vị,
#   Trạng thái người dùng, Số tài khoản, Tên ngân hàng, Trạng thái
# -----------------------------------------------------------------------

def build_employee_dicts(
    batch_name: str,
    company: str,
    posting_user: str = "Administrator",
) -> dict[str, list[dict]]:
    """Build tabEmployee rows from Misa Employee file_type."""
    rows = frappe.db.sql(
        "SELECT name AS row_name, raw_payload FROM `tabMisa Migration Row` "
        "WHERE batch=%s AND file_type='Employee' "
        "AND status NOT IN ('Skipped','Invalid','Posted')",
        (batch_name,), as_dict=True,
    )
    now = frappe.utils.now()
    emp_rows: list[dict] = []
    row_to_name: dict[str, str] = {}   # Misa Migration Row.name → Employee.name
    seen: set[str] = set()

    for r in rows:
        try:
            p = json.loads(r["raw_payload"] or "{}")
        except (TypeError, ValueError):
            continue
        emp_code = (p.get("Mã nhân viên") or "").strip()
        emp_name = (p.get("Tên nhân viên") or "").strip()
        if not emp_code or not emp_name:
            continue
        # Pass-through if Employee already exists
        if frappe.db.exists("Employee", emp_code):
            row_to_name[r["row_name"]] = emp_code
            continue
        if emp_code in seen:
            row_to_name[r["row_name"]] = emp_code
            continue
        seen.add(emp_code)
        # Misa "Trạng thái" → ERPNext status
        misa_status = (p.get("Trạng thái") or "").strip()
        status = "Active" if misa_status == "Đang sử dụng" else "Left"
        emp_rows.append({
            "name": emp_code,
            "creation": now, "modified": now,
            "owner": posting_user, "modified_by": posting_user,
            "docstatus": 0, "idx": 0,
            "employee": emp_code,
            "employee_name": emp_name[:140],
            "first_name": emp_name[:140],
            "designation": (p.get("Chức danh") or "")[:140] or None,
            "department": (p.get("Tên đơn vị") or "")[:140] or None,
            "company": company,
            "status": status,
            "gender": "Other",
            "date_of_joining": "2020-01-01",
            "date_of_birth": "1990-01-01",
            "naming_series": "HR-EMP-",
        })
        row_to_name[r["row_name"]] = emp_code

    return {
        "Employee": emp_rows,
        "_row_to_name": row_to_name,   # consumed by orchestrator to update Misa rows
    }


# -----------------------------------------------------------------------
# Bank Account — Misa shape:
#   STT, Số tài khoản, Tên ngân hàng, Tên chi nhánh ngân hàng,
#   Chủ tài khoản, Chi nhánh, Trạng thái
# -----------------------------------------------------------------------

def build_bank_account_dicts(
    batch_name: str,
    company: str,
    posting_user: str = "Administrator",
) -> dict[str, list[dict]]:
    """Build tabBank + tabBank Account rows from Misa Bank Account file_type."""
    rows = frappe.db.sql(
        "SELECT name AS row_name, raw_payload FROM `tabMisa Migration Row` "
        "WHERE batch=%s AND file_type='Bank Account' "
        "AND status NOT IN ('Skipped','Invalid','Posted')",
        (batch_name,), as_dict=True,
    )
    now = frappe.utils.now()
    bank_rows: list[dict] = []
    bank_acc_rows: list[dict] = []
    row_to_name: dict[str, str] = {}
    seen_banks: set[str] = set()
    seen_ba: set[str] = set()

    for r in rows:
        try:
            p = json.loads(r["raw_payload"] or "{}")
        except (TypeError, ValueError):
            continue
        acc_no = (p.get("Số tài khoản") or "").strip()
        bank_name = (p.get("Tên ngân hàng") or "").strip()
        if not acc_no or not bank_name:
            continue
        # Bank parent record (one per distinct bank name)
        if bank_name not in seen_banks and not frappe.db.exists("Bank", bank_name):
            bank_rows.append({
                "name": bank_name[:140],
                "creation": now, "modified": now,
                "owner": posting_user, "modified_by": posting_user,
                "docstatus": 0, "idx": 0,
                "bank_name": bank_name[:140],
            })
            seen_banks.add(bank_name)
        ba_name = f"{acc_no} - {bank_name}"[:140]
        if ba_name in seen_ba:
            row_to_name[r["row_name"]] = ba_name
            continue
        if frappe.db.exists("Bank Account", ba_name):
            row_to_name[r["row_name"]] = ba_name
            seen_ba.add(ba_name)
            continue
        is_disabled = (p.get("Trạng thái") or "").strip() == "Ngừng sử dụng"
        bank_acc_rows.append({
            "name": ba_name,
            "creation": now, "modified": now,
            "owner": posting_user, "modified_by": posting_user,
            "docstatus": 0, "idx": 0,
            "account_name": ba_name,
            "bank": bank_name[:140],
            "bank_account_no": acc_no[:140],
            "branch_code": (p.get("Tên chi nhánh ngân hàng") or "")[:140] or None,
            "company": company,
            "account_type": "Bank",
            "is_company_account": 1,
            "disabled": 1 if is_disabled else 0,
        })
        seen_ba.add(ba_name)
        row_to_name[r["row_name"]] = ba_name

    return {
        "Bank": bank_rows,
        "Bank Account": bank_acc_rows,
        "_row_to_name": row_to_name,
    }
