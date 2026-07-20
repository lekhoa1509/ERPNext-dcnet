"""Phase 0 prerequisite checks — UX Gap 7.

The 9 OB file_types have different master-data dependencies:

  OB Account Balance   → Chart of Accounts seeded (Phase 2)
  OB Bank Balance      → Bank Account masters (Phase 3) + bank sub-accounts
  OB Customer AR       → Customer masters (Phase 3) — codes must match Misa Mã
  OB Supplier AP       → Supplier masters (Phase 3)
  OB Employee Advance  → Employee masters (Phase 3)
  OB Prepaid Expense   → TK 242 leaf in COA (Phase 2 + coa_leaves)
  OB Inventory         → Item with is_stock_item=1 (Phase 3) + Warehouse (Phase 1)
  OB Fixed Asset       → Item with is_fixed_asset=1 (Phase 3) + Asset Category (Phase 1)
  OB CCDC              → Item with is_fixed_asset=1 (Phase 3) + CCDC Asset Category

When the operator runs Phase 0 without doing Phase 1+2+3 first, the
detail handlers either silently drop rows (parties missing) OR throw
"X is not a stock Item" errors. This module surfaces those gaps as
preflight checks BEFORE the operator clicks Post.
"""

from __future__ import annotations

import json
from typing import Any

import frappe


# Each entry: ob_file_type → {required_doctype: human_label}.
# When the file_type has rows in this batch, we check the corresponding
# master count and surface a block/warn issue if zero.
# Level rationale: every dep here can be RESOLVED by ``install_misa_coa``
# (which bootstraps baseline CoA + Phase 1/2/3 masters) or by the natural
# ORM post flow (which runs Phase 1→2→3 before Phase 0). Marking them
# "block" disables the Đăng buttons even when the operator's NEXT click
# would create the missing data — UX deadlock on fresh-wipe Companies.
# Downgraded to "warn": preflight still surfaces the gap in the UI panel,
# but the operator can proceed; if masters are still missing at post
# time, the handlers throw loud, detailed errors per row.
_PHASE_0_DEPENDENCIES: dict[str, list[dict[str, Any]]] = {
    "OB Customer AR": [
        {"check": "party_codes_resolve",
         "party_doctype": "Customer",
         "level": "warn",
         "label": "Customer master",
         "hint": "Chạy 'Cài đặt CoA Misa' (Phase 1+2+3) hoặc 'Đăng vào ERPNext' (ORM full) trước; "
                 "cả hai sẽ tạo Customer master từ 'Danh sách khách hàng' trong batch."},
    ],
    "OB Supplier AP": [
        {"check": "party_codes_resolve",
         "party_doctype": "Supplier",
         "level": "warn",
         "label": "Supplier master",
         "hint": "Chạy 'Cài đặt CoA Misa' (Phase 1+2+3) hoặc 'Đăng vào ERPNext' (ORM full) trước; "
                 "cả hai sẽ tạo Supplier master từ 'Danh sách nhà cung cấp' trong batch."},
    ],
    "OB Employee Advance": [
        {"check": "party_codes_resolve",
         "party_doctype": "Employee",
         "level": "warn",  # warn — general balance fallback exists for TK 141
         "label": "Employee master",
         "hint": "Phase 3 import 'Danh sách nhân viên' giúp tách balance theo nhân viên. "
                 "Nếu không có, balance TK 141 vẫn post được nhưng không split per-employee."},
    ],
    "OB Inventory": [
        {"check": "item_codes_resolve",
         "item_flag": "is_stock_item",
         "level": "warn",
         "label": "Item master (stock items)",
         "hint": "Chạy 'Cài đặt CoA Misa' (Phase 1+2+3) trước để tạo Item; "
                 "mọi item phải có is_stock_item=1."},
        {"check": "warehouse_codes_resolve",
         "level": "warn",
         "label": "Warehouse master",
         "hint": "Chạy 'Cài đặt CoA Misa' (Phase 1+2+3) trước; sẽ tạo Warehouse từ 'Danh sách kho'."},
    ],
    "OB Fixed Asset": [
        {"check": "item_codes_resolve",
         "item_flag": "is_fixed_asset",
         "level": "warn",
         "label": "Item master (fixed assets)",
         "hint": "Mỗi mã tài sản cần Item record với is_fixed_asset=1. "
                 "Chạy 'Cài đặt CoA Misa' (Phase 1+2+3) trước rồi mark is_fixed_asset trên các Item TSCĐ."},
        {"check": "asset_category_exists",
         "level": "warn",
         "label": "Asset Category",
         "hint": "Chạy 'Cài đặt CoA Misa' (Phase 1+2+3) để tạo Asset Category, "
                 "hoặc handler sẽ dùng category mặc định."},
    ],
    "OB CCDC": [
        {"check": "ccdc_default_category_exists",
         "level": "warn",
         "label": "Default CCDC Asset Category",
         "hint": "Handler sẽ auto-create category 'CCDC' nếu chưa có — chỉ là warning."},
    ],
    "OB Bank Balance": [
        {"check": "bank_subaccounts_exist",
         "level": "warn",
         "label": "Bank sub-accounts (TK 1121.XX)",
         "hint": "Nếu thiếu, balance sẽ collapse vào TK 1121/112 parent. "
                 "Chạy 'Cài đặt CoA Misa' (Phase 1+2+3) để tạo Misa-specific sub-accounts."},
    ],
    "OB Prepaid Expense": [
        {"check": "tk_242_leaf_exists",
         "level": "warn",
         "label": "TK 242 leaf account",
         "hint": "Cần TK 242 leaf account. Chạy 'Cài đặt CoA Misa' (Phase 1+2+3) trước; "
                 "bootstrap_coa sẽ install TT99/2025 baseline có sẵn TK 242."},
    ],
}


def check_phase_0_prerequisites(
    batch_name: str,
    company: str | None = None,
) -> dict[str, Any]:
    """Return per-OB-file-type prerequisite check results.

    Args:
      batch_name: Misa Migration Batch.
      company: Company name (default = batch.company → global default).

    Returns:
      {
        'checks': [{file_type, label, level, passed, found, expected, hint, issues}],
        'block_count': int,
        'warn_count': int,
        'status': 'ok' | 'warn' | 'block',
      }
    """
    if company is None:
        company = (
            frappe.db.get_value("Misa Migration Batch", batch_name, "company")
            or frappe.defaults.get_global_default("company")
            or frappe.db.get_value("Company", {}, "name")
        )

    # Which OB file_types have actual rows in this batch?
    present = frappe.db.sql_list(
        """SELECT DISTINCT file_type FROM `tabMisa Migration Row`
           WHERE batch=%s AND file_type LIKE 'OB %%'""",
        (batch_name,),
    )

    checks: list[dict[str, Any]] = []
    for ft in present:
        for dep in _PHASE_0_DEPENDENCIES.get(ft, []):
            result = _run_check(batch_name, ft, dep, company)
            checks.append(result)

    block_count = sum(1 for c in checks if c["level"] == "block" and not c["passed"])
    warn_count = sum(1 for c in checks if c["level"] == "warn" and not c["passed"])
    status = "block" if block_count else ("warn" if warn_count else "ok")
    return {
        "checks": checks,
        "block_count": block_count,
        "warn_count": warn_count,
        "status": status,
    }


def _run_check(
    batch_name: str,
    file_type: str,
    dep: dict[str, Any],
    company: str,
) -> dict[str, Any]:
    """Dispatch one prerequisite check by `dep['check']` name."""
    fn = _CHECK_REGISTRY.get(dep["check"])
    if fn is None:
        return {
            "file_type": file_type, "label": dep["label"],
            "level": dep["level"], "passed": False,
            "found": 0, "expected": 0,
            "hint": dep["hint"],
            "issues": [f"Unknown check: {dep['check']}"],
        }
    result = fn(batch_name, file_type, dep, company)
    result.setdefault("file_type", file_type)
    result.setdefault("label", dep["label"])
    result.setdefault("level", dep["level"])
    result.setdefault("hint", dep["hint"])
    return result


def _check_party_codes_resolve(
    batch_name: str, file_type: str, dep: dict[str, Any], company: str,
) -> dict[str, Any]:
    """For Customer/Supplier/Employee AR: every party_code in raw_payload
    must resolve to an existing master record."""
    party_doctype = dep["party_doctype"]
    rows = frappe.db.sql(
        "SELECT raw_payload FROM `tabMisa Migration Row` "
        "WHERE batch=%s AND file_type=%s "
        "AND status NOT IN ('Skipped', 'Failed', 'Invalid')",
        (batch_name, file_type), as_dict=True,
    )
    code_field_by_dt = {
        "Customer": "Mã khách hàng",
        "Supplier": "Mã nhà cung cấp",
        "Employee": "Mã nhân viên",
    }
    code_field = code_field_by_dt.get(party_doctype)
    if not code_field:
        return {"passed": True, "found": 0, "expected": 0, "issues": []}

    party_codes: set[str] = set()
    for r in rows:
        try:
            payload = json.loads(r["raw_payload"] or "{}")
            code = (payload.get(code_field) or "").strip()
            if code:
                party_codes.add(code)
        except (TypeError, ValueError):
            continue

    if not party_codes:
        return {"passed": True, "found": 0, "expected": 0, "issues": []}

    # Bulk existence check. MariaDB collation utf8mb4_unicode_ci matches
    # case-insensitively for the IN(...) lookup, but Python set-diff
    # below is case-sensitive. Mirror 289fdcc's party-cache approach:
    # build a lowercase set of all existing names, then check membership
    # by lowered code. This eliminates the VIETTEL/Viettel false-missing.
    placeholders = ",".join(["%s"] * len(party_codes))
    existing_rows = frappe.db.sql_list(
        f"SELECT name FROM `tab{party_doctype}` WHERE name IN ({placeholders})",
        tuple(party_codes),
    )
    existing_lower = {(n or "").lower() for n in existing_rows}
    missing = sorted(c for c in party_codes if c.lower() not in existing_lower)
    existing = existing_rows
    return {
        "passed": not missing,
        "found": len(existing),
        "expected": len(party_codes),
        "issues": [
            f"{len(missing)}/{len(party_codes)} mã {party_doctype} chưa có master record. "
            f"Ví dụ thiếu: {', '.join(missing[:5])}"
        ] if missing else [],
    }


def _check_item_codes_resolve(
    batch_name: str, file_type: str, dep: dict[str, Any], company: str,
) -> dict[str, Any]:
    """For inventory/FA/CCDC: every item_code must exist on Item master
    with the required flag (is_stock_item / is_fixed_asset)."""
    flag = dep.get("item_flag")
    rows = frappe.db.sql(
        "SELECT raw_payload FROM `tabMisa Migration Row` "
        "WHERE batch=%s AND file_type=%s "
        "AND status NOT IN ('Skipped', 'Failed', 'Invalid')",
        (batch_name, file_type), as_dict=True,
    )
    # Misa column for item_code varies by file
    code_field = {
        "OB Inventory": "Mã hàng",
        "OB Fixed Asset": "Mã tài sản",
        "OB CCDC": "Mã CCDC",
    }.get(file_type, "Mã hàng")
    item_codes: set[str] = set()
    for r in rows:
        try:
            payload = json.loads(r["raw_payload"] or "{}")
            code = (payload.get(code_field) or "").strip()
            if code and code != "Tổng":
                item_codes.add(code)
        except (TypeError, ValueError):
            continue
    if not item_codes:
        return {"passed": True, "found": 0, "expected": 0, "issues": []}

    placeholders = ",".join(["%s"] * len(item_codes))
    where_extra = ""
    params = list(item_codes)
    if flag:
        where_extra = f" AND `{flag}`=1"
    existing = set(frappe.db.sql_list(
        f"SELECT name FROM `tabItem` WHERE name IN ({placeholders}){where_extra}",
        tuple(params),
    ))
    missing = sorted(item_codes - existing)
    return {
        "passed": not missing,
        "found": len(existing),
        "expected": len(item_codes),
        "issues": [
            f"{len(missing)}/{len(item_codes)} mã Item chưa có (hoặc thiếu {flag}=1). "
            f"Ví dụ thiếu: {', '.join(missing[:5])}"
        ] if missing else [],
    }


def _check_warehouse_codes_resolve(
    batch_name: str, file_type: str, dep: dict[str, Any], company: str,
) -> dict[str, Any]:
    """For OB Inventory: every warehouse code must exist on Warehouse master."""
    rows = frappe.db.sql(
        "SELECT raw_payload FROM `tabMisa Migration Row` "
        "WHERE batch=%s AND file_type=%s "
        "AND status NOT IN ('Skipped', 'Failed', 'Invalid')",
        (batch_name, file_type), as_dict=True,
    )
    wh_codes: set[str] = set()
    for r in rows:
        try:
            payload = json.loads(r["raw_payload"] or "{}")
            code = (payload.get("Mã kho") or "").strip()
            if code and code != "Tổng":
                wh_codes.add(code)
        except (TypeError, ValueError):
            continue
    if not wh_codes:
        return {"passed": True, "found": 0, "expected": 0, "issues": []}
    # ERPNext appends "- <abbr>" to Warehouse.name on insert, so a Misa
    # code 'KHO' lives in ERPNext as 'KHO - DCT'. Look up by warehouse_name
    # (Misa Tên kho stored without abbr) AND by name prefix to catch both
    # patterns. We accept a match if the Misa code is contained in any
    # ERPNext warehouse name on the company.
    placeholders = ",".join(["%s"] * len(wh_codes))
    # Exact-name lookup
    exact = set(frappe.db.sql_list(
        f"SELECT name FROM `tabWarehouse` WHERE company=%s AND name IN ({placeholders})",
        (company, *wh_codes),
    ))
    # warehouse_name field stores the un-suffixed name
    by_wh_name = set(frappe.db.sql_list(
        f"SELECT warehouse_name FROM `tabWarehouse` WHERE company=%s AND warehouse_name IN ({placeholders})",
        (company, *wh_codes),
    ))
    found_codes = set()
    found_codes.update(c for c in wh_codes if c in exact)
    found_codes.update(c for c in wh_codes if c in by_wh_name)
    # Also try prefix match (Misa code → ERPNext 'code - <abbr>')
    if found_codes != wh_codes:
        prefix_rows = frappe.db.sql(
            "SELECT name, warehouse_name FROM `tabWarehouse` WHERE company=%s",
            (company,), as_dict=True,
        )
        all_names = {(r["name"] or "").strip() for r in prefix_rows}
        all_wh_names = {(r["warehouse_name"] or "").strip() for r in prefix_rows}
        for code in wh_codes - found_codes:
            if any(n == code or n.startswith(f"{code} -") for n in all_names):
                found_codes.add(code)
            elif any(n == code for n in all_wh_names):
                found_codes.add(code)
    missing = sorted(wh_codes - found_codes)
    existing = found_codes
    return {
        "passed": not missing,
        "found": len(existing),
        "expected": len(wh_codes),
        "issues": [
            f"{len(missing)}/{len(wh_codes)} mã kho chưa có trên Company {company!r}. "
            f"Ví dụ thiếu: {', '.join(missing[:5])}"
        ] if missing else [],
    }


def _check_asset_category_exists(
    batch_name: str, file_type: str, dep: dict[str, Any], company: str,
) -> dict[str, Any]:
    """At least one Asset Category should exist."""
    n = frappe.db.count("Asset Category")
    return {
        "passed": n > 0,
        "found": n, "expected": 1,
        "issues": ["Không có Asset Category nào — handler sẽ fail "
                   "khi tạo Asset record."] if n == 0 else [],
    }


def _check_ccdc_default_category_exists(
    batch_name: str, file_type: str, dep: dict[str, Any], company: str,
) -> dict[str, Any]:
    """The default CCDC Asset Category should exist (handler auto-creates)."""
    exists = frappe.db.exists("Asset Category", "CCDC")
    return {
        "passed": bool(exists),
        "found": 1 if exists else 0, "expected": 1,
        "issues": [] if exists else [
            "Asset Category 'CCDC' chưa có. Handler sẽ tự auto-create lúc post — "
            "đây chỉ là cảnh báo."
        ],
    }


def _check_bank_subaccounts_exist(
    batch_name: str, file_type: str, dep: dict[str, Any], company: str,
) -> dict[str, Any]:
    """Bank sub-accounts (TK 1121.XX) should exist for proper bank balance posting."""
    bank_leaves = frappe.db.count(
        "Account",
        {"company": company, "is_group": 0,
         "account_number": ("like", "1121%")},
    )
    return {
        "passed": bank_leaves > 0,
        "found": bank_leaves, "expected": 1,
        "issues": [
            "Không có TK 1121.XX leaf nào — bank balance sẽ collapse vào parent. "
            "Chạy ensure_misa_leaves_for_company hoặc preflight setup."
        ] if bank_leaves == 0 else [],
    }


def _check_tk_242_leaf_exists(
    batch_name: str, file_type: str, dep: dict[str, Any], company: str,
) -> dict[str, Any]:
    """TK 242 leaf account must exist for prepaid posting."""
    has_leaf = frappe.db.exists(
        "Account",
        {"company": company, "account_number": "242", "is_group": 0},
    )
    return {
        "passed": bool(has_leaf),
        "found": 1 if has_leaf else 0, "expected": 1,
        "issues": [
            "TK 242 leaf không có trên Company. Run preflight setup "
            "(ensure_company_defaults_for_misa) để bootstrap COA."
        ] if not has_leaf else [],
    }


_CHECK_REGISTRY = {
    "party_codes_resolve": _check_party_codes_resolve,
    "item_codes_resolve": _check_item_codes_resolve,
    "warehouse_codes_resolve": _check_warehouse_codes_resolve,
    "asset_category_exists": _check_asset_category_exists,
    "ccdc_default_category_exists": _check_ccdc_default_category_exists,
    "bank_subaccounts_exist": _check_bank_subaccounts_exist,
    "tk_242_leaf_exists": _check_tk_242_leaf_exists,
}
