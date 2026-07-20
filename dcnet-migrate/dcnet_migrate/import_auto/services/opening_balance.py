"""Opening-balance import helpers for Vietnamese accounting migration.

This module is intentionally separate from the existing AI Smart Import flow.
The regular Import Auto paths are already useful for master data; opening
balances need deterministic accounting rules and pre-flight reconciliation.
"""

from __future__ import annotations

from collections import defaultdict
import hashlib
import html
import json
import re
import unicodedata
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any

import frappe
from frappe import _
from frappe.utils import cstr, flt, getdate, now_datetime, strip_html

from dcnet_migrate.import_auto.services.ai_client import (
    _chat_completion,
    _get_ai_config,
    _parse_json_response,
)
from dcnet_migrate.import_auto.services.excel import extract_records
from dcnet_migrate.import_auto.services.excel import summarize_workbook
from dcnet_migrate.import_auto.services.importer import _update_parent_status
from dcnet_migrate.import_auto.services.utils import normalize_key, scan_excel_files, truncate_text


OPENING_FILES = {
    # === Danh mục kế toán ===
    "chart_of_accounts": "Danh_sach_he_thong_tai_khoan.xlsx",
    # === Số dư đầu kỳ (02_So_Du_Dau_Ky) ===
    "account_balance":    "Danh_sach_so_du_tai_khoan.xlsx",
    "customer_balance":   "Danh_sach_cong_no_khach_hang.xlsx",
    "supplier_balance":   "Danh_sach_cong_no_nha_cung_cap.xlsx",
    "employee_balance":   "Danh_sach_cong_no_nhan_vien.xlsx",
    "bank_balance":       "Danh_sach_nhap_so_du_tai_khoan_ngan_hang.xlsx",
    "stock_balance":      "Danh_sach_ton_kho_vthh.xlsx",
    "fixed_asset":        "Danh_sach_tai_san_co_dinh_dau_ky.xlsx",
    "tools":              "Danh_sach_cong_cu_dung_cu_dau_ky.xlsx",
    "prepaid":            "Danh_sach_chi_phi_tra_truoc_dau_ky.xlsx",
    "deferred_revenue":   "Danh_sach_doanh_thu_nhan_truoc_dau_ky.xlsx",
    # === Phát sinh trong năm (03_Phat_Sinh_Trong_Nam) ===
    "sales_invoice":      "Bang_ke_hoa_don_chung_tu_hang_hoa_dich_vu_ban_ra_mau_quan_tri.xlsx",
    "purchase_invoice":   "Bang_ke_hoa_don_chung_tu_hang_hoa_dich_vu_mua_vao_mau_quan_tri.xlsx",
    "stock_detail":       "So_chi_tiet_vat_tu_hang_hoa.xlsx",
    "general_journal":    "So_nhat_ky_chung.xlsx",
    # legacy (kept for backward compat)
    "gl_detail":          "So_chi_tiet_cac_tai_khoan 01-2026.xlsx",
}

HEADER_ROWS = {
    "chart_of_accounts": 3,
    "account_balance":  3,
    "customer_balance": 3,
    "supplier_balance": 3,
    "employee_balance": 3,
    "bank_balance":     3,
    "stock_balance":    4,
    "fixed_asset":      3,
    "tools":            3,
    "prepaid":          3,
    "deferred_revenue": 3,
    "sales_invoice":    4,
    "purchase_invoice": 4,
    "stock_detail":     4,
    "general_journal":  4,
    "gl_detail":        4,
}

DETAIL_ACCOUNT_KEYS = {"bank_balance", "customer_balance", "supplier_balance", "employee_balance"}

INVOICE_MIGRATION_TYPES = {"sales_invoice", "purchase_invoice"}

# Commit the invoice import in batches of this many rows instead of one giant
# transaction. A single all-or-nothing transaction over thousands of invoices
# holds tabCompany/tabAccount row locks for the whole run and, when the web
# request hits the proxy/worker timeout, rolls back everything — the root cause
# of the observed 504 + "Lock wait timeout" / "SAVEPOINT does not exist" cascade.
# Committing per batch releases locks between chunks and persists progress so a
# timed-out or retried import resumes via the idempotent skip below.
INVOICE_IMPORT_BATCH_SIZE = 50

OPENING_PARTY_BUCKETS = {
    "Customer": "customers",
    "Supplier": "suppliers",
    "Employee": "employees",
}

STOCK_OPENING_DEFAULT_ACCOUNT_PREFIXES = ("1561", "156", "155", "152", "153", "151", "157")
STOCK_OPENING_SOURCE_MARKER = "Import Auto Opening Stock"

# Warehouse name patterns → preferred TK prefixes (longest-match wins inside each tuple).
# Mirrors the heuristic used in vn_accounting misa_migration.
_WAREHOUSE_ACCOUNT_HINTS: list[tuple[re.Pattern, tuple[str, ...]]] = [
    (re.compile(r"nguy[eê]n\s*v[aậ]t\s*li[eệ]u|nguy[eê]n\s*li[eệ]u|\bnvl\b", re.I), ("152",)),
    (re.compile(r"c[oô]ng\s*c[uụ]|d[uụ]ng\s*c[uụ]|\bccdc\b", re.I), ("1531", "153")),
    (re.compile(r"th[aà]nh\s*ph[aẩ]m|\btp\b", re.I), ("1551", "155")),
    (re.compile(r"g[uử]i\s*b[aá]n|h[aà]ng\s*g[uử]i", re.I), ("157",)),
    (re.compile(r"b[aả]o\s*thu[eế]|bonded", re.I), ("158",)),
]


# Hardcoded column plans for preview_only migration types when AI doesn't provide a valid plan.
# amount_col / name_col may be "|"-separated candidate names — first one with a non-zero value wins.
# credit_account "__temporary_opening__" resolves to _ensure_temporary_opening_account() at runtime.
_HARDCODED_PREVIEW_COLUMN_PLANS: dict[str, dict] = {
    "fixed_asset": {
        "is_feasible": True,
        "debit_account": "211",
        "credit_account": "__temporary_opening__",
        "amount_col": "Nguyên giá|Nguyên Giá|NGUYÊN GIÁ|Giá trị còn lại|Giá trị ban đầu",
        "name_col": "Tên TSCĐ|Mã TSCĐ|Số TSCĐ|Tên tài sản cố định",
        "_hardcoded": True,
        "notes": "Tự động: Nợ TK 211 (Nguyên giá), Có Temporary Opening",
    },
    "prepaid": {
        "is_feasible": True,
        "debit_account": "242",
        "credit_account": "__temporary_opening__",
        "amount_col": "Giá trị phân bổ|Số tiền|Giá trị còn lại|Giá trị|Thành tiền|Số tiền phân bổ",
        "name_col": "Nội dung chi phí|Khoản CPTT|Nội dung|Tên chi phí|Diễn giải",
        "_hardcoded": True,
        "notes": "Tự động: Nợ TK 242, Có Temporary Opening",
    },
    "deferred_revenue": {
        "is_feasible": True,
        "debit_account": "__temporary_opening__",
        "credit_account": "3387",
        "amount_col": "Số tiền|Giá trị|Thành tiền|Giá trị còn lại|Doanh thu nhận trước",
        "name_col": "Nội dung|Diễn giải|Tên hợp đồng|Khách hàng|Tên khách hàng",
        "_hardcoded": True,
        "notes": "Tự động: Nợ Temporary Opening, Có TK 3387 (Doanh thu nhận trước)",
    },
}


@dataclass
class OpeningRow:
    source: str
    source_row: int
    account_number: str
    account: str | None
    debit: float
    credit: float
    party_type: str | None = None
    party_code: str | None = None
    party: str | None = None
    bank_account_no: str | None = None
    bank_account: str | None = None
    label: str | None = None

    def as_dict(self) -> dict:
        return {
            "source": self.source,
            "source_row": self.source_row,
            "account_number": self.account_number,
            "account": self.account,
            "debit": self.debit,
            "credit": self.credit,
            "party_type": self.party_type,
            "party_code": self.party_code,
            "party": self.party,
            "bank_account_no": self.bank_account_no,
            "bank_account": self.bank_account,
            "label": self.label,
        }


def _clear_existing_accounts(company: str) -> dict:
    """Delete all accounts for company that have no GL entries. Children deleted before parents."""
    accounts = frappe.db.sql(
        """
        SELECT name, account_number
        FROM `tabAccount`
        WHERE company = %s
        ORDER BY lft DESC
        """,
        company,
        as_dict=True,
    )
    deleted = skipped_gl = skipped_err = 0
    for acc in accounts:
        has_gl = frappe.db.exists("GL Entry", {"account": acc.name, "is_cancelled": 0})
        if has_gl:
            skipped_gl += 1
            continue
        try:
            frappe.delete_doc("Account", acc.name, force=True, ignore_permissions=True)
            deleted += 1
        except Exception:
            skipped_err += 1
    frappe.db.commit()
    return {"deleted": deleted, "skipped_gl": skipped_gl, "skipped_err": skipped_err}


def import_chart_of_accounts(import_doc, force: bool = False, clear: bool = False) -> dict:
    """Import Chart of Accounts from MISA Excel file.

    Creates 5 TT200 root groups then imports all accounts in topological order
    (parents before children, determined by account number prefix).

    If clear=True, deletes all existing accounts without GL entries first.
    """
    company = import_doc.company

    cleared = None
    if clear:
        cleared = _clear_existing_accounts(company)

    file_map = _opening_file_map_from_slots(import_doc)
    file_path = file_map.get("chart_of_accounts")
    if not file_path:
        frappe.throw(_("Chưa upload file hệ thống tài khoản vào slot 'Hệ thống tài khoản'."))

    records = extract_records(file_path, None, HEADER_ROWS["chart_of_accounts"])
    abbr = frappe.db.get_value("Company", company, "abbr") or "DCNET"

    # Parse accounts from file
    accounts = []
    for row in records:
        num = _text(row.get("Số tài khoản") or row.get("Mã TK") or row.get("Số TK"))
        name = _text(row.get("Tên tài khoản") or row.get("Tên TK"))
        tinh_chat = _text(row.get("Tính chất") or "")
        if not num or not name:
            continue
        # Skip inactive accounts
        trang_thai = _text(row.get("Trạng thái") or "")
        if trang_thai and "không" in trang_thai.lower():
            continue
        balance_must_be = "Credit" if "có" in tinh_chat.lower() else "Debit"
        accounts.append({"num": num, "name": name, "balance_must_be": balance_must_be})

    if not accounts:
        frappe.throw(_("Không tìm thấy tài khoản hợp lệ trong file."))

    # Build set of account numbers for parent resolution
    num_set = {a["num"] for a in accounts}

    def find_parent_num(num: str) -> str | None:
        best = ""
        for candidate in num_set:
            if num.startswith(candidate) and len(candidate) < len(num) and len(candidate) > len(best):
                # Handle dot-separated accounts like "1121.20" whose parent could be "1121"
                rest = num[len(candidate):]
                if rest and (rest[0].isdigit() or rest[0] == "."):
                    best = candidate
        return best or None

    # Determine is_group (has children in file) and parent for each account
    for acc in accounts:
        acc["parent_num"] = find_parent_num(acc["num"])
        acc["is_group"] = any(
            a["num"] != acc["num"] and find_parent_num(a["num"]) == acc["num"]
            for a in accounts
        )

    # Ensure TT200 root groups exist
    _tt200_root = _ensure_tt200_roots(company, abbr)

    # Sort: parents before children (by account number length then alpha)
    accounts.sort(key=lambda a: (len(a["num"]), a["num"]))

    created = skipped = 0
    errors = []
    for acc in accounts:
        num = acc["num"]
        try:
            existing = frappe.db.get_value("Account", {"account_number": num, "company": company}, "name")
            if existing and not force:
                skipped += 1
                continue

            if acc["parent_num"]:
                parent_name = frappe.db.get_value(
                    "Account", {"account_number": acc["parent_num"], "company": company}, "name"
                )
            else:
                parent_name = _tt200_root_for_num(num, _tt200_root)

            if not parent_name:
                errors.append({"num": num, "error": "Không tìm thấy tài khoản cha"})
                continue

            if existing:
                doc = frappe.get_doc("Account", existing)
                doc.account_name = acc["name"]
                doc.balance_must_be = acc["balance_must_be"]
                doc.flags.ignore_permissions = True
                doc.save()
            else:
                doc = frappe.new_doc("Account")
                doc.account_name = acc["name"]
                doc.account_number = num
                doc.company = company
                doc.parent_account = parent_name
                doc.is_group = 1 if acc["is_group"] else 0
                doc.balance_must_be = acc["balance_must_be"]
                _set_account_type(doc, num)
                doc.flags.ignore_permissions = True
                doc.insert()

            created += 1
        except Exception as exc:
            errors.append({"num": num, "error": cstr(exc)[:200]})

    return {
        "total": len(accounts),
        "created": created,
        "skipped": skipped,
        "errors": errors,
        "error_count": len(errors),
        "cleared": cleared,
    }


# --- TT200 root groups -------------------------------------------------------

_TT200_ROOTS = [
    {"name_vi": "Tài sản", "root_type": "Asset",     "balance_must_be": "Debit",  "prefixes": ("1", "2")},
    {"name_vi": "Nợ phải trả", "root_type": "Liability", "balance_must_be": "Credit", "prefixes": ("3",)},
    {"name_vi": "Vốn chủ sở hữu", "root_type": "Equity",    "balance_must_be": "Credit", "prefixes": ("4",)},
    {"name_vi": "Doanh thu", "root_type": "Income",   "balance_must_be": "Credit", "prefixes": ("5", "7")},
    {"name_vi": "Chi phí",   "root_type": "Expense",  "balance_must_be": "Debit",  "prefixes": ("6", "8", "9")},
]

# Prefix-based account type mapping — applies to the account AND all its children
_ACCOUNT_TYPE_PREFIXES: list[tuple[tuple[str, ...], str]] = [
    (("1111", "1112"),                           "Cash"),
    (("1121", "1122", "1123"),                   "Bank"),
    (("131",),                                   "Receivable"),
    (("138",),                                   "Receivable"),  # phải thu khác
    (("331",),                                   "Payable"),
    (("336",),                                   "Payable"),     # phải trả nội bộ
    (("333", "3331", "33311", "33312"),          "Tax"),
    (("211", "213"),                             "Fixed Asset"),
    (("214",),                                   "Accumulated Depreciation"),
    (("241",),                                   "Capital Work in Progress"),
    (("411",),                                   "Equity"),
    (("151", "152", "153", "155", "156", "157"), "Stock"),
]


def _ensure_tt200_roots(company: str, abbr: str) -> dict[str, str]:
    """Create TT200 root account groups if they don't exist. Returns {name_vi: actual_doc_name}."""
    result = {}
    for grp in _TT200_ROOTS:
        full_name = f"{grp['name_vi']} - {abbr}"
        existing = frappe.db.get_value("Account", full_name, "name")
        if existing:
            result[grp["name_vi"]] = existing
            continue
        # Also search by root_type in case the name differs
        by_type = frappe.db.get_value(
            "Account",
            {"company": company, "root_type": grp["root_type"], "parent_account": ["in", ["", None]]},
            "name",
        )
        if by_type:
            result[grp["name_vi"]] = by_type
            continue
        doc = frappe.new_doc("Account")
        doc.account_name = grp["name_vi"]
        doc.company = company
        doc.is_group = 1
        doc.root_type = grp["root_type"]
        doc.balance_must_be = grp["balance_must_be"]
        # Bypass mandatory parent_account check for root accounts
        doc.flags.ignore_mandatory = True
        doc.flags.ignore_permissions = True
        doc.insert()
        result[grp["name_vi"]] = doc.name
    return result


def _tt200_root_for_num(num: str, roots: dict[str, str]) -> str | None:
    first = num[0] if num else ""
    for grp in _TT200_ROOTS:
        if first in grp["prefixes"]:
            return roots.get(grp["name_vi"])
    return None


def _set_account_type(doc, num: str) -> None:
    for prefixes, account_type in _ACCOUNT_TYPE_PREFIXES:
        if any(num.startswith(p) for p in prefixes):
            doc.account_type = account_type
            return


def analyze_opening_migration_files(import_doc) -> dict:
    """Classify opening-balance migration files from the per-slot uploads.

    AI is used only to detect header row and generate column_plan for
    preview_only slots. Migration type comes from the slot assignment
    (user already chose which slot to upload to), so classification is
    deterministic and AI cannot change it.
    """
    file_map = _opening_file_map_from_slots(import_doc)
    if not file_map:
        frappe.throw(_("Vui lòng upload ít nhất 1 file trước khi chạy phân tích."))

    summaries = []
    for migration_type, file_path in file_map.items():
        try:
            summary = summarize_workbook(file_path, max_sample_rows=10, sample_strategy="first")
            summary["migration_type_hint"] = migration_type
        except Exception as exc:
            summary = {
                "file_name": Path(file_path).name,
                "file_path": file_path,
                "migration_type_hint": migration_type,
                "error": str(exc)[:300],
            }
        summaries.append(summary)

    # AI only needed for header_row_number + column_plan (not migration_type)
    ai_result = _classify_opening_files_with_ai(import_doc, summaries)
    ai_files = ai_result.get("files") or []
    ai_error = ai_result.get("error")
    ai_by_name = {cstr(item.get("file_name")).strip(): item for item in ai_files if item.get("file_name")}

    files = []
    for migration_type, file_path in file_map.items():
        file_name = Path(file_path).name
        fallback = _classify_opening_file({"file_path": file_path, "file_name": file_name})
        ai_item = ai_by_name.get(file_name) or {}

        base_handler = _handler_for_migration_type(migration_type)
        column_plan = None
        handler = base_handler
        if base_handler == "preview_only":
            raw_plan = ai_item.get("column_plan")
            if (
                isinstance(raw_plan, dict)
                and raw_plan.get("is_feasible")
                and cstr(raw_plan.get("debit_account")).strip()
                and cstr(raw_plan.get("amount_col")).strip()
            ):
                column_plan = raw_plan
                handler = "ai_journal"
            elif migration_type in _HARDCODED_PREVIEW_COLUMN_PLANS:
                # Fallback hardcoded plan when AI doesn't provide one
                column_plan = _HARDCODED_PREVIEW_COLUMN_PLANS[migration_type]
                handler = "ai_journal"

        files.append({
            "file_name": file_name,
            "file_path": file_path,
            "migration_type": migration_type,
            "handler": handler,
            "column_plan": column_plan,
            "header_row_number": ai_item.get("header_row_number") or fallback.get("header_row_number"),
            "row_count": fallback.get("row_count") or 0,
            "confidence": 100,
            "reason": _("File được gán slot bởi người dùng."),
            "ai_classified": bool(ai_item),
        })

    master_plan = _inspect_opening_missing_parties(file_map)

    result = {
        "ok": True,
        "ai_used": bool(ai_files),
        "ai_warning": (
            _("Không kết nối được AI endpoint; header row và column_plan dùng rule local.")
            if ai_error else None
        ),
        "company": _company(import_doc),
        "files": files,
        "master_plan": master_plan,
        "auto_master": master_plan,
        "message": _opening_analysis_message(len(files), bool(ai_error), master_plan),
    }

    import_doc.status = "Analyzed"
    import_doc.analysis_json = frappe.as_json(result, indent=2)
    import_doc.save(ignore_permissions=True)
    frappe.db.commit()
    return result


def preview_opening_migration(import_doc) -> dict:
    """Return a unified preview for opening JE and hardcoded invoice handlers."""
    company = _company(import_doc)
    file_map = _opening_file_map_from_slots(import_doc)
    analysis = _analysis_or_fallback_slots(import_doc)
    errors = []

    opening_journal = {}
    try:
        opening_journal = _build_opening_journal_plan(company, file_map)
    except Exception as exc:
        opening_journal = {
            "rows": [],
            "row_count": 0,
            "total_debit": 0,
            "total_credit": 0,
            "difference": 0,
            "missing_links": [],
            "source_breakdown": [],
        }
        errors.append({"scope": "opening_journal", "message": str(exc)})

    invoices = {
        "sales_invoice": _invoice_summary(file_map, "sales_invoice"),
        "purchase_invoice": _invoice_summary(file_map, "purchase_invoice"),
    }
    stock_opening = _stock_opening_summary(company=company, file_map=file_map)
    posting_date = str(getdate(getattr(import_doc, "posting_date", None) or "2026-01-01"))

    return {
        "ok": not errors,
        "company": company,
        "posting_date": posting_date,
        "files": _normalise_opening_analysis_files(analysis.get("files") or []),
        "file_presence": _file_presence_summary(file_map),
        "unrecognized_files": [],
        "opening_journal": opening_journal,
        "invoices": invoices,
        "stock_opening": stock_opening,
        "related": _related_file_summary(file_map),
        "existing_opening_entries": _existing_opening_entries(company),
        "file_kpis": _file_based_kpis(file_map, invoices),
        "errors": errors,
    }


def preview_opening_balances(import_doc) -> dict:
    """Build a deterministic preview for opening-balance accounting import."""
    company = _company(import_doc)
    file_map = _opening_file_map_from_slots(import_doc)
    plan = _build_opening_journal_plan(company, file_map)
    related = _related_file_summary(file_map)
    existing = _existing_opening_entries(company)
    return {
        "ok": not plan["missing_links"] and abs(plan["difference"]) < 0.5,
        "company": company,
        "posting_date": str(getdate(getattr(import_doc, "posting_date", None) or frappe.utils.today())),
        "files": _file_presence_summary(file_map),
        "unrecognized_files": [],
        "journal_entry": plan,
        "related": related,
        "existing_opening_entries": existing,
        "notes": [
            "AI chỉ dùng để nhận diện loại file; bước ghi dữ liệu chạy bằng Python hardcode theo từng handler.",
            "Nếu vừa thêm hoặc thay file, bấm lại AI phân tích file hoặc Xem kế hoạch để preview lại.",
            "Chỉ tạo Opening Journal Entry cho số dư kế toán, công nợ party và ngân hàng.",
            "Tồn kho, TSCĐ, CCDC/CPTT được phân tích riêng để xử lý ở bước sau, không tự submit trong bước này.",
            "Tài khoản cha trong file số dư không được import để tránh double-count.",
        ],
    }


def execute_opening_balances(
    import_doc,
    posting_date: str | None = None,
    submit: bool | int | str = False,
    force: bool | int | str = False,
    balance_account: str | None = None,
) -> dict:
    """Create the opening Journal Entry as draft by default.

    ``submit`` is opt-in because opening balances affect GL immediately.
    """
    company = _company(import_doc)
    posting_date = str(getdate(posting_date or "2026-01-01"))
    submit = bool(int(submit)) if isinstance(submit, str) and submit.isdigit() else bool(submit)
    force = bool(int(force)) if isinstance(force, str) and force.isdigit() else bool(force)

    _ensure_coa_account_types(company)
    _ensure_coa_balance_type(company)

    existing = _existing_opening_entries(company)
    if existing and not force:
        frappe.throw(
            _(
                "Đã có Opening Journal Entry do Import Auto tạo cho công ty này. "
                "Bật tùy chọn tạo lại nếu bạn chắc chắn muốn tạo thêm bản mới."
            )
        )

    file_map = _opening_file_map_from_slots(import_doc)

    # Auto-create missing Customer/Supplier/Employee before building the plan
    _process_opening_party_candidates(
        file_map, create=True, company=company,
        posting_date=str(getdate(posting_date or "2026-01-01")),
    )
    frappe.db.commit()

    plan = _build_opening_journal_plan(company, file_map)
    if plan["missing_links"]:
        frappe.throw(_("Chưa thể import số dư đầu kỳ vì còn thiếu mapping master data. Xem preview để biết chi tiết."))
    if not plan["rows"]:
        dbg = plan.get("_debug") or {}
        frappe.throw(_(
            "Không tìm thấy dòng số dư đầu kỳ hợp lệ để tạo Journal Entry. "
            "Debug: account_rows={0}, detail_rows={1}, skipped_stock={2}, "
            "rows_before_split={3}, overridden={4}. "
            "Kiểm tra: (1) TK kho (15x) đã tách sang Stock Reco — file số dư TK có TK không phải kho không? "
            "(2) Cột Excel đúng 'Dư Nợ'/'Dư Có'? "
            "(3) Tất cả TK bị ghi đè bởi file công nợ/ngân hàng?"
        ).format(
            dbg.get("account_rows_count", "?"),
            dbg.get("detail_rows_count", "?"),
            dbg.get("skipped_stock_count", "?"),
            dbg.get("rows_before_split", "?"),
            dbg.get("overridden_accounts", []),
        ))
    if abs(plan["difference"]) >= 0.5:
        breakdown = plan.get("source_breakdown") or []
        lines = [
            f"  • {b['source']}: Nợ {b['debit']:,.0f} | Có {b['credit']:,.0f} | Ròng {b['debit']-b['credit']:+,.0f}"
            for b in breakdown
        ]
        detail = "\n".join(lines) if lines else ""
        if balance_account:
            # Auto-balance: add one line to the opposite side using the specified account.
            diff = plan["difference"]  # positive → debit excess → add credit; negative → credit excess → add debit
            balance_row = {
                "account": balance_account,
                "debit": 0.0 if diff > 0 else abs(diff),
                "credit": diff if diff > 0 else 0.0,
                "party_type": None,
                "party": None,
                "bank_account": None,
                "label": f"Bù chênh lệch đầu kỳ ({diff:+,.0f})",
                "source": "auto_balance",
                "source_row": 0,
            }
            plan["rows"].append(balance_row)
            plan["total_debit"] = round(plan["total_debit"] + balance_row["debit"], 2)
            plan["total_credit"] = round(plan["total_credit"] + balance_row["credit"], 2)
            plan["difference"] = round(plan["total_debit"] - plan["total_credit"], 2)
        else:
            frappe.throw(_(
                "Opening Journal Entry chưa cân. Chênh lệch: {0:,.0f}\n"
                "Tổng Nợ: {1:,.0f}  |  Tổng Có: {2:,.0f}\n\n"
                "Phân tích theo nguồn:\n{3}\n\n"
                "Tip: Kiểm tra (1) File số dư TK có đủ TK vốn/lợi nhuận (411, 421...) không? "
                "(2) Số dư TK 131 / 331 / 112 có khớp với tổng file công nợ / ngân hàng không?\n"
                "Hoặc chọn 'TK bù chênh lệch' trong dialog để tự động cân bằng."
            ).format(
                plan["difference"],
                plan["total_debit"],
                plan["total_credit"],
                detail,
            ))

    savepoint = "opening_balance_import"
    frappe.db.savepoint(savepoint)
    try:
        je = frappe.new_doc("Journal Entry")
        je.voucher_type = "Opening Entry"
        je.is_opening = "Yes"
        je.company = company
        je.posting_date = posting_date
        je.user_remark = _opening_remark(import_doc, posting_date)
        # Sort: debit rows first so running balance stays non-negative during sequential GL insert.
        # ERPNext's validate_balance_type checks the cumulative balance after each GL entry row;
        # posting all debits before credits prevents false "must always be Debit" errors on 131/141.
        sorted_rows = sorted(plan["rows"], key=lambda r: (0 if r.get("debit", 0) > 0 else 1))
        for row in sorted_rows:
            account_row = {
                "account": row["account"],
                "debit_in_account_currency": row["debit"],
                "credit_in_account_currency": row["credit"],
                "user_remark": _row_remark(row),
            }
            if row.get("party_type") and row.get("party"):
                account_row["party_type"] = row["party_type"]
                account_row["party"] = row["party"]
            if row.get("bank_account"):
                account_row["bank_account"] = row["bank_account"]
            je.append("accounts", account_row)

        je.insert(ignore_permissions=True)
        if submit:
            je.submit()

        _mark_opening_balance_summary(import_doc, je.name, plan, posting_date, submit)
        frappe.db.commit()

        return {
            "ok": True,
            "journal_entry": je.name,
            "docstatus": je.docstatus,
            "submitted": bool(submit),
            "posting_date": posting_date,
            "rows": len(plan["rows"]),
            "total_debit": plan["total_debit"],
            "total_credit": plan["total_credit"],
            "auto_balanced": bool(balance_account) and abs(plan.get("difference") or 0) < 0.5,
            "balance_account": balance_account or None,
        }
    except Exception:
        frappe.db.rollback(save_point=savepoint)
        raise


def execute_opening_stock_reconciliation(
    import_doc,
    posting_date: str | None = None,
    submit: bool | int | str = False,
    force: bool | int | str = False,
    allow_difference: bool | int | str = False,
    limit: int | None = None,
) -> dict:
    """Create an Opening Stock Reconciliation from the stock detail file.

    Vietnamese accounting still expects inventory value in accounts such as
    1561. ERPNext requires that value to enter through Stock Ledger first, so
    this handler creates a Stock Reconciliation that posts GL to the warehouse
    stock account and uses Temporary Opening only as the contra account.
    """
    company = _company(import_doc)
    posting_date = str(getdate(posting_date or getattr(import_doc, "posting_date", None) or "2026-01-01"))
    submit = bool(int(submit)) if isinstance(submit, str) and submit.isdigit() else bool(submit)
    force = bool(int(force)) if isinstance(force, str) and force.isdigit() else bool(force)
    allow_difference = (
        bool(int(allow_difference))
        if isinstance(allow_difference, str) and allow_difference.isdigit()
        else bool(allow_difference)
    )
    limit = int(limit or 0)

    file_map = _opening_file_map_from_slots(import_doc)
    plan = _build_stock_opening_plan(company, file_map, limit=limit)
    account_balance_stock_value = _stock_like_account_balance_net(company, file_map)
    balance_difference = round(plan["total_value"] - account_balance_stock_value, 2)
    hard_errors = [e for e in (plan.get("errors") or []) if e.get("severity", "error") != "warning"]
    if not plan["rows"]:
        frappe.throw(_("Không tìm thấy dòng tồn kho đầu kỳ hợp lệ trong file chi tiết vật tư hàng hóa."))
    if hard_errors:
        frappe.throw(_("Chưa thể import tồn kho đầu kỳ vì còn {0} lỗi dữ liệu. Xem kế hoạch để biết chi tiết.").format(len(hard_errors)))
    if abs(balance_difference) >= 0.5 and not allow_difference:
        frappe.throw(
            _(
                "Giá trị tồn kho trong file chi tiết ({0}) đang lệch số dư các tài khoản kho trên bảng số dư ({1}). "
                "Chênh lệch {2}. Không import tự động để tránh treo Temporary Opening; nếu kế toán xác nhận dữ liệu này đúng, bật tùy chọn cho phép lệch."
            ).format(
                frappe.format_value(plan["total_value"], {"fieldtype": "Currency"}),
                frappe.format_value(account_balance_stock_value, {"fieldtype": "Currency"}),
                frappe.format_value(balance_difference, {"fieldtype": "Currency"}),
            )
        )

    source_key = _stock_opening_source_key(company, file_map, posting_date)
    existing = _find_existing_opening_stock_reconciliation(company, source_key)
    if existing and not force:
        frappe.throw(
            _(
                "Đã có Stock Reconciliation do Import Auto tạo cho tồn kho đầu kỳ: {0}. "
                "Bật tùy chọn tạo lại nếu bạn chắc chắn muốn tạo thêm bản mới."
            ).format(existing)
        )

    result = {
        "ok": True,
        "mode": "opening_stock",
        "stock_reconciliation": None,
        "docstatus": 0,
        "submitted": bool(submit),
        "posting_date": posting_date,
        "rows": len(plan["rows"]),
        "source_rows": plan["source_rows"],
        "total_qty": plan["total_qty"],
        "total_value": plan["total_value"],
        "account_balance_stock_value": account_balance_stock_value,
        "balance_difference": balance_difference,
        "created_items": 0,
        "created_warehouses": 0,
        "created_uoms": 0,
        "updated_warehouses": 0,
        "errors": [],
    }

    savepoint = "opening_stock_reconciliation_import"
    frappe.db.savepoint(savepoint)
    try:
        reconciliation = frappe.new_doc("Stock Reconciliation")
        reconciliation.company = company
        reconciliation.purpose = "Opening Stock"
        reconciliation.posting_date = posting_date
        reconciliation.posting_time = "00:00:00"
        reconciliation.set_posting_time = 1
        reconciliation.expense_account = _stock_opening_adjustment_account(company)
        reconciliation.cost_center = _default_cost_center(company)

        for row in plan["rows"]:
            item_code, item_created, uom_created = _ensure_opening_stock_item(row)
            warehouse, warehouse_created, warehouse_updated = _ensure_opening_stock_warehouse(
                company,
                row["warehouse_label"],
                row.get("stock_account"),
            )
            result["created_items"] += int(item_created)
            result["created_uoms"] += int(uom_created)
            result["created_warehouses"] += int(warehouse_created)
            result["updated_warehouses"] += int(warehouse_updated)

            reconciliation.append("items", {
                "item_code": item_code,
                "warehouse": warehouse,
                "qty": row["qty"],
                "valuation_rate": row["valuation_rate"],
                "allow_zero_valuation_rate": 1 if not row["valuation_rate"] else 0,
            })

        reconciliation.insert(ignore_permissions=True)
        reconciliation.add_comment("Comment", _stock_opening_comment(source_key, file_map, plan))
        if submit:
            reconciliation.submit()

        result["stock_reconciliation"] = reconciliation.name
        result["docstatus"] = reconciliation.docstatus
        result["message"] = _(
            "Đã tạo Stock Reconciliation {0} với {1} dòng tồn kho đầu kỳ."
        ).format(reconciliation.name, len(plan["rows"]))

        _mark_opening_stock_summary(import_doc, result)
        frappe.db.commit()
        return result
    except Exception:
        frappe.db.rollback(save_point=savepoint)
        raise


def execute_invoice_import(
    import_doc,
    invoice_type: str,
    submit: bool | int | str = False,
    force: bool | int | str = False,
    limit: int | None = None,
) -> dict:
    """Create Sales/Purchase Invoice drafts from hardcoded Vietnamese tax lists."""
    invoice_type = cstr(invoice_type).strip()
    if invoice_type not in INVOICE_MIGRATION_TYPES:
        frappe.throw(_("Loại hóa đơn không hợp lệ: {0}").format(invoice_type))

    company = _company(import_doc)
    submit = bool(int(submit)) if isinstance(submit, str) and submit.isdigit() else bool(submit)
    force = bool(int(force)) if isinstance(force, str) and force.isdigit() else bool(force)
    limit = int(limit or 0)

    file_map = _opening_file_map_from_slots(import_doc)
    groups = _group_invoice_rows(file_map, invoice_type)
    if limit > 0:
        groups = groups[:limit]

    master_plan = _inspect_opening_missing_parties(file_map)
    required_bucket = "customers" if invoice_type == "sales_invoice" else "suppliers"
    missing_parties = int((master_plan.get(required_bucket) or {}).get("missing") or 0)
    if missing_parties:
        party_label = _("Customer") if invoice_type == "sales_invoice" else _("Supplier")
        frappe.throw(
            _(
                "Còn {0} {1} chưa có trong DB. "
                "Vui lòng bấm 'Tạo master thiếu' và xác nhận trước khi import hóa đơn."
            ).format(missing_parties, party_label)
        )

    result = {
        "ok": True,
        "invoice_type": invoice_type,
        "doctype": "Sales Invoice" if invoice_type == "sales_invoice" else "Purchase Invoice",
        "created": 0,
        "skipped": 0,
        "failed": 0,
        "created_names": [],
        "errors": [],
    }

    if not groups:
        result["ok"] = False
        result["message"] = _("Không tìm thấy dòng hóa đơn hợp lệ.")
        return result

    _ensure_coa_account_types(company)
    _ensure_coa_balance_type(company)
    _ensure_company_round_off_settings(company)
    if invoice_type == "purchase_invoice":
        _ensure_company_purchase_invoice_settings(company)

    savepoint = f"{invoice_type}_migration"
    frappe.db.savepoint(savepoint)
    for index, group in enumerate(groups, start=1):
        # Flush the previous batch before starting a new one: releases row locks
        # held so far and persists committed invoices. Kept at the top of the loop
        # so it runs regardless of the `continue` on the skip path below.
        if index > 1 and (index - 1) % INVOICE_IMPORT_BATCH_SIZE == 0:
            frappe.db.commit()
        row_savepoint = f"{invoice_type}_{index}"
        try:
            frappe.db.savepoint(row_savepoint)
            existing_name = _find_existing_migration_invoice(result["doctype"], company, group["source_key"])
            if existing_name and not force:
                result["skipped"] += 1
                continue

            invoice = _build_migration_invoice(company, invoice_type, group)
            invoice.flags.ignore_mandatory = True
            invoice.insert(ignore_permissions=True)
            if submit:
                invoice.submit()
            result["created"] += 1
            result["created_names"].append(invoice.name)
            frappe.db.release_savepoint(row_savepoint)
        except Exception as exc:
            frappe.db.rollback(save_point=row_savepoint)
            result["failed"] += 1
            result["errors"].append({
                "row": index,
                "source_key": group.get("source_key"),
                "error": _clean_error_message(exc, limit=500),
            })
            frappe.clear_messages()

    if result["failed"]:
        result["ok"] = False

    _mark_invoice_import_summary(import_doc, invoice_type, result)
    frappe.db.commit()
    result["message"] = _(
        "Đã tạo {0}, bỏ qua {1}, lỗi {2} hóa đơn."
    ).format(result["created"], result["skipped"], result["failed"])
    return result


def create_opening_missing_masters(import_doc) -> dict:
    """Create Customer/Supplier/Employee and Bank Account masters after explicit user approval."""
    file_map = _opening_file_map_from_slots(import_doc)
    company = _company(import_doc)
    result = _process_opening_party_candidates(
        file_map,
        create=True,
        company=company,
        posting_date=getattr(import_doc, "posting_date", None) or "2026-01-01",
    )
    bank_result = _process_opening_bank_accounts(file_map, create=True, company=company)
    result["banks"] = bank_result
    result["ok"] = not bool(result.get("failed")) and not bool(bank_result.get("failed"))
    result["message"] = _opening_master_create_message(result)

    refreshed_plan = _inspect_opening_missing_parties(file_map)
    _mark_opening_master_summary(import_doc, result, refreshed_plan)
    frappe.db.commit()
    return result


def _classify_opening_files_with_ai(import_doc, summaries: list[dict]) -> dict:
    # Opening Balance Import must use the shared Import Auto Settings, not the
    # hidden per-document AI fields. Passing None keeps config centralized:
    # Import Auto Settings -> site_config/env API key.
    config = _get_ai_config(None)
    if not config.api_key or not config.enabled or not summaries:
        return {"files": [], "error": None}

    payload = {
        "allowed_types": [
            "account_balance",
            "customer_balance",
            "supplier_balance",
            "employee_balance",
            "bank_balance",
            "stock_balance",
            "stock_detail",
            "fixed_asset",
            "tools",
            "prepaid",
            "deferred_revenue",
            "sales_invoice",
            "purchase_invoice",
            "general_journal",
            "gl_detail",
            "unknown",
        ],
        "required_json_schema": {
            "files": [
                {
                    "file_name": "string — tên file gốc",
                    "migration_type": "một trong allowed_types — ưu tiên slot đã gán, xác nhận bằng cột",
                    "header_row_number": "số nguyên (1-based) hoặc null",
                    "handler": "opening_journal | stock_reconciliation | sales_invoice | purchase_invoice | preview_only | ignored",
                    "confidence": "0-100",
                    "reason": "lý do tiếng Việt, ngắn gọn (tối đa 1 câu)",
                    "column_plan": {
                        "__comment": "CHỈ điền cho preview_only khi có thể tạo JE đơn giản. Để null cho tất cả handler khác.",
                        "debit_account": "số TK Nợ theo TT200, vd '242', '211', '3387'",
                        "credit_account": "số TK Có theo TT200, vd '411', '__temporary_opening__'",
                        "amount_col": "tên cột chứa số tiền — dùng | để liệt kê nhiều candidate, vd 'Nguyên giá|Giá trị còn lại'",
                        "name_col": "tên cột mô tả/diễn giải, hoặc null",
                        "is_feasible": "true nếu chắc chắn mapping đúng, false nếu không chắc",
                        "note": "giải thích ngắn tiếng Việt về mapping",
                    },
                }
            ]
        },
        "workbooks": summaries,
    }
    messages = [
        {
            "role": "system",
            "content": (
                "Bạn phân tích file Excel kế toán Việt Nam (xuất từ MISA) để import vào ERPNext v16.\n"
                "Trả về STRICT JSON only — không kèm markdown, không text ngoài JSON.\n\n"
                "NGỮ CẢNH QUAN TRỌNG:\n"
                "• Người dùng đã TỰ GÁN từng file vào slot migration_type theo tên file.\n"
                "• Nhiệm vụ chính: XÁC NHẬN migration_type đúng không, detect header_row, và tạo column_plan.\n"
                "• Nếu migration_type từ slot không khớp nội dung file → confidence thấp (<60) + ghi rõ lý do.\n\n"
                "DẤU HIỆU CỘT ĐẶC TRƯNG (tên cột MISA thực tế):\n"
                "┌─ Số dư kế toán (handler: opening_journal) ─────────────────────────────────────────────────┐\n"
                "│ account_balance  : Số tài khoản / Mã TK · Tên tài khoản · Dư Nợ · Dư Có (1 dòng/TK)      │\n"
                "│ customer_balance : Mã KH / Mã khách hàng · Tên KH · Dư Nợ · Dư Có (TK 131)               │\n"
                "│ supplier_balance : Mã NCC / Mã nhà cung cấp · Tên NCC · Dư Nợ · Dư Có (TK 331)           │\n"
                "│ employee_balance : Mã NV / Mã nhân viên · Tên NV · Dư Nợ (tạm ứng)                        │\n"
                "│ bank_balance     : Ngân hàng / Chi nhánh · STK / Số tài khoản ngân hàng · Số dư cuối kỳ   │\n"
                "├─ Kho (handler: stock_reconciliation) ──────────────────────────────────────────────────────┤\n"
                "│ stock_balance    : Mã hàng · Tên hàng · Tên kho · SL tồn / Số lượng · Đơn giá · Thành tiền│\n"
                "│                   KHÔNG có cột Nhập/Xuất riêng — chỉ có số tồn cuối kỳ                    │\n"
                "│ stock_detail     : Mã hàng · Nhập (số lượng + tiền) · Xuất · Tồn — Sổ chi tiết VTHH       │\n"
                "│ tools            : Mã CCDC / Tên CCDC · Số lượng · Giá trị · Bộ phận sử dụng              │\n"
                "├─ Tài sản / Chi phí (handler: preview_only → cần column_plan) ─────────────────────────────┤\n"
                "│ fixed_asset      : Mã TSCĐ / Tên TSCĐ · Nguyên giá · Hao mòn lũy kế · Giá trị còn lại    │\n"
                "│ prepaid          : Nội dung chi phí / Khoản CPTT · Số tiền / Giá trị phân bổ · Số tháng   │\n"
                "│ deferred_revenue : Nội dung / Diễn giải · Số tiền / Giá trị · Kỳ phân bổ (TK 3387)        │\n"
                "├─ Hóa đơn phát sinh (handler: sales_invoice / purchase_invoice) ──────────────────────────┤\n"
                "│ sales_invoice    : Số HĐ · Mã KH · Ngày HĐ · Mã hàng · Thành tiền · Thuế VAT             │\n"
                "│ purchase_invoice : Số HĐ · Mã NCC · Ngày HĐ · Mã hàng · Thành tiền · Thuế VAT            │\n"
                "├─ Nhật ký (handler: ignored — quá phức tạp) ────────────────────────────────────────────────┤\n"
                "│ general_journal  : Ngày hạch toán · Số chứng từ · Tài khoản · TK đối ứng · PS Nợ · PS Có  │\n"
                "│                   Đây là sổ nhật ký chung — ghi nhiều dòng/chứng từ, KHÔNG import tự động │\n"
                "│ gl_detail        : Sổ chi tiết tài khoản — dùng để đối chiếu, KHÔNG import tự động         │\n"
                "└────────────────────────────────────────────────────────────────────────────────────────────┘\n\n"
                "PHÂN BIỆT QUAN TRỌNG:\n"
                "• stock_balance vs stock_detail: stock_balance CHỈ có số tồn (không có cột Nhập/Xuất riêng).\n"
                "• general_journal vs sales_invoice: general_journal có cột 'Tài khoản' + 'TK đối ứng' cùng 1 dòng.\n\n"
                "COLUMN_PLAN — mặc định theo TT200 (chỉ điền cho preview_only, is_feasible=true):\n"
                "• fixed_asset    : debit='211',  credit='__temporary_opening__', amount_col='Nguyên giá|Giá trị còn lại'\n"
                "• prepaid        : debit='242',  credit='__temporary_opening__', amount_col='Giá trị phân bổ|Số tiền|Giá trị còn lại'\n"
                "• deferred_revenue: debit='__temporary_opening__', credit='3387', amount_col='Số tiền|Giá trị|Thành tiền'\n"
                "• general_journal: is_feasible=false (quá phức tạp, cần xử lý thủ công)\n"
                "• gl_detail      : is_feasible=false (chỉ dùng để đối chiếu)\n\n"
                "Với MISA, header row thường nằm ở hàng 3-5 (có dòng tiêu đề báo cáo phía trên).\n"
                "Phát hiện header row = hàng đầu tiên có >3 ô không rỗng và chứa từ khóa tên cột thực tế."
            ),
        },
        {
            "role": "user",
            "content": truncate_text(
                json.dumps(payload, ensure_ascii=False, default=str),
                max_length=30000,
            ),
        },
    ]
    try:
        raw = _chat_completion(
            config.api_base_url,
            config.model,
            config.api_key,
            messages,
            max(int(config.timeout_seconds or 60), 90),
        )
        parsed = _parse_json_response(raw)
    except Exception as exc:
        # _chat_completion uses frappe.throw(), which appends a msgprint to
        # frappe.local.message_log before raising. This path is intentionally
        # non-fatal because we fall back to deterministic local rules, so clear
        # that queued msgprint to avoid a scary "Could not connect..." popup
        # after a successful fallback analysis.
        frappe.clear_messages()
        frappe.log_error(frappe.get_traceback(), "Opening Balance AI Classification Failed")
        frappe.clear_messages()
        return {"files": [], "error": str(exc)}

    files = parsed.get("files") if isinstance(parsed, dict) else None
    if not isinstance(files, list):
        return {"files": [], "error": _("AI không trả về danh sách file hợp lệ.")}
    return {"files": [file for file in files if isinstance(file, dict)], "error": None}


def _merge_ai_file_classification(fallback_files: list[dict], ai_files: list[dict]) -> list[dict]:
    ai_by_name = {
        cstr(item.get("file_name")).strip(): item
        for item in ai_files
        if cstr(item.get("file_name")).strip()
    }
    merged = []
    for fallback in fallback_files:
        ai_item = ai_by_name.get(fallback["file_name"]) or {}
        migration_type = cstr(ai_item.get("migration_type") or fallback["migration_type"]).strip()
        if migration_type not in set(OPENING_FILES) | {"unknown"}:
            migration_type = fallback["migration_type"]
        if migration_type == "unknown" and fallback.get("migration_type") != "unknown":
            migration_type = fallback["migration_type"]

        base_handler = _handler_for_migration_type(migration_type)
        column_plan = None
        handler = base_handler
        if base_handler == "preview_only":
            raw_plan = ai_item.get("column_plan")
            if (
                isinstance(raw_plan, dict)
                and raw_plan.get("is_feasible")
                and cstr(raw_plan.get("debit_account")).strip()
                and cstr(raw_plan.get("amount_col")).strip()
            ):
                column_plan = raw_plan
                handler = "ai_journal"

        merged.append({
            **fallback,
            "migration_type": migration_type,
            "handler": handler,
            "column_plan": column_plan,
            "confidence": int(flt(ai_item.get("confidence") or fallback.get("confidence") or 0)),
            "reason": ai_item.get("reason") or fallback.get("reason"),
            "ai_classified": bool(ai_item),
            "header_row_number": ai_item.get("header_row_number") or fallback.get("header_row_number"),
        })
    return merged


def _normalise_opening_analysis_files(files: list[dict]) -> list[dict]:
    normalised = []
    for item in files or []:
        if not isinstance(item, dict):
            continue
        migration_type = cstr(item.get("migration_type")).strip()
        normalised.append({
            **item,
            "handler": _handler_for_migration_type(migration_type),
        })
    return normalised


def _analysis_or_fallback_slots(import_doc) -> dict:
    """Return analysis_json if available, else build minimal fallback from file_slots_json."""
    if getattr(import_doc, "analysis_json", None):
        try:
            parsed = frappe.parse_json(import_doc.analysis_json)
            if isinstance(parsed, dict) and isinstance(parsed.get("files"), list):
                return parsed
        except Exception:
            pass
    file_map = _opening_file_map_from_slots(import_doc)
    files = []
    for migration_type, file_path in file_map.items():
        files.append(_classify_opening_file({"file_path": file_path, "file_name": Path(file_path).name}))
    return {"ok": True, "ai_used": False, "files": files}


def _analysis_or_fallback(import_doc, discovered_files: list[str]) -> dict:
    if getattr(import_doc, "analysis_json", None):
        try:
            parsed = frappe.parse_json(import_doc.analysis_json)
            if isinstance(parsed, dict) and isinstance(parsed.get("files"), list):
                return parsed
        except Exception:
            pass

    summaries = []
    for file_path in discovered_files:
        try:
            summaries.append(summarize_workbook(file_path, max_sample_rows=5, sample_strategy="first"))
        except Exception:
            summaries.append({"file_name": Path(file_path).name, "file_path": file_path})
    return {
        "ok": True,
        "ai_used": False,
        "files": [_classify_opening_file(summary) for summary in summaries],
    }


def _classify_opening_file(summary: dict) -> dict:
    file_name = Path(cstr(summary.get("file_path") or summary.get("file_name") or "")).name
    file_key = _fold_key(file_name)
    migration_type = "unknown"

    for key, expected_name in OPENING_FILES.items():
        if _fold_key(expected_name) == file_key:
            migration_type = key
            break

    if migration_type == "unknown":
        if "ban_ra" in file_key or "ban ra" in file_key or "hoa_don_ban" in file_key:
            migration_type = "sales_invoice"
        elif "mua_vao" in file_key or "mua vao" in file_key or "hoa_don_mua" in file_key:
            migration_type = "purchase_invoice"
        elif any(k in file_key for k in ("so_du_tai_khoan", "so du tai khoan", "so_du_tk", "bang_can_doi", "so_du_dau_ky_tk")):
            migration_type = "account_balance"
        elif any(k in file_key for k in ("cong_no_khach_hang", "cong_no_kh", "phai_thu_kh", "phai_thu_khach")):
            migration_type = "customer_balance"
        elif any(k in file_key for k in ("cong_no_nha_cung_cap", "cong_no_ncc", "phai_tra_ncc", "phai_tra_nha_cung")):
            migration_type = "supplier_balance"
        elif any(k in file_key for k in ("cong_no_nhan_vien", "cong_no_nv", "tam_ung_nhan_vien", "tam_ung_nv")):
            migration_type = "employee_balance"
        elif any(k in file_key for k in ("ngan_hang", "tien_gui", "so_du_ngan_hang", "tk_ngan_hang")):
            migration_type = "bank_balance"
        elif any(k in file_key for k in ("vat_tu_hang_hoa", "ton_kho", "hang_ton", "vthh", "kiem_ke_kho", "chi_tiet_kho", "ds_ton", "danh_sach_ton")):
            migration_type = "stock_detail"
        elif any(k in file_key for k in ("tai_san_co_dinh", "tscd", "tai_san_cd")):
            migration_type = "fixed_asset"
        elif any(k in file_key for k in ("cong_cu_dung_cu", "ccdc", "cong_cu_dc")):
            migration_type = "tools"
        elif any(k in file_key for k in ("chi_phi_tra_truoc", "cptt", "tra_truoc", "cho_ky_sau")):
            migration_type = "prepaid"
        elif any(k in file_key for k in ("chi_tiet_cac_tai_khoan", "chi_tiet_tk", "so_chi_tiet_tk")):
            migration_type = "gl_detail"

    sheet = (summary.get("sheets") or [{}])[0] if isinstance(summary.get("sheets"), list) else {}
    return {
        "file_name": file_name or cstr(summary.get("file_name") or ""),
        "file_path": summary.get("file_path"),
        "migration_type": migration_type,
        "handler": _handler_for_migration_type(migration_type),
        "header_row_number": HEADER_ROWS.get(migration_type) or sheet.get("detected_header_row"),
        "row_count": sheet.get("max_row") or 0,
        "confidence": 92 if migration_type != "unknown" else 20,
        "reason": "Nhận diện theo tên file chuẩn." if migration_type != "unknown" else "Chưa nhận diện được loại file.",
    }


def _handler_for_migration_type(migration_type: str) -> str:
    if migration_type in {
        "account_balance",
        "customer_balance",
        "supplier_balance",
        "employee_balance",
        "bank_balance",
    }:
        return "opening_journal"
    if migration_type == "sales_invoice":
        return "sales_invoice"
    if migration_type == "purchase_invoice":
        return "purchase_invoice"
    if migration_type in {"stock_detail", "stock_balance", "tools"}:
        return "stock_reconciliation"
    if migration_type in {"fixed_asset", "prepaid", "deferred_revenue", "general_journal", "gl_detail"}:
        return "preview_only"
    return "ignored"


def execute_ai_journal_files(
    import_doc,
    posting_date: str | None = None,
    submit: bool | int | str = False,
    force: bool | int | str = False,
) -> dict:
    """Create Journal Entries (Opening Entry) from AI-generated column_plan for preview_only files."""
    company = _company(import_doc)
    posting_date = str(getdate(posting_date or "2026-01-01"))

    def _to_bool(v):
        if isinstance(v, bool):
            return v
        return str(v).strip().lower() in ("1", "true", "yes")

    submit = _to_bool(submit)
    force = _to_bool(force)

    analysis: dict = {}
    if getattr(import_doc, "analysis_json", None):
        try:
            analysis = frappe.parse_json(import_doc.analysis_json) or {}
        except Exception:
            pass

    if not analysis:
        frappe.throw(_("Chưa có kết quả phân tích. Vui lòng chạy 'AI phân tích file' trước."))

    ai_files = [
        f for f in (analysis.get("files") or [])
        if isinstance(f, dict) and f.get("handler") == "ai_journal"
    ]
    if not ai_files:
        return {
            "ok": True,
            "created": 0,
            "skipped": 0,
            "failed": 0,
            "message": _("Không có file nào được AI tạo kế hoạch import."),
            "journal_entries": [],
            "errors": [],
        }

    result: dict = {
        "ok": True,
        "created": 0,
        "skipped": 0,
        "failed": 0,
        "journal_entries": [],
        "errors": [],
    }

    for file_meta in ai_files:
        file_path = cstr(file_meta.get("file_path") or "").strip()
        column_plan = file_meta.get("column_plan") or {}
        file_name = file_meta.get("file_name") or (Path(file_path).name if file_path else file_meta.get("migration_type", "?"))

        if not file_path or not column_plan.get("is_feasible"):
            result["skipped"] += 1
            continue

        try:
            je_name = _execute_single_ai_journal_file(
                company, file_path, file_meta, column_plan, posting_date, submit
            )
            result["created"] += 1
            result["journal_entries"].append(je_name)
        except Exception as exc:
            frappe.db.rollback()
            result["failed"] += 1
            result["errors"].append({
                "file": file_name,
                "error": _clean_error_message(exc, limit=300),
            })

    if result["failed"]:
        result["ok"] = False

    _mark_ai_journal_summary(import_doc, result)
    frappe.db.commit()
    result["message"] = _(
        "Đã tạo {0}, bỏ qua {1}, lỗi {2} Journal Entry từ AI plan."
    ).format(result["created"], result["skipped"], result["failed"])
    return result


def _execute_single_ai_journal_file(
    company: str,
    file_path: str,
    file_meta: dict,
    column_plan: dict,
    posting_date: str,
    submit: bool,
) -> str:
    """Create one Journal Entry from an AI-generated column_plan."""
    migration_type = file_meta.get("migration_type", "")
    file_name = file_meta.get("file_name") or Path(file_path).name
    header_row_raw = file_meta.get("header_row_number")
    if header_row_raw is not None:
        try:
            header_row = int(header_row_raw)
        except (TypeError, ValueError):
            header_row = HEADER_ROWS.get(migration_type, 3)
    else:
        header_row = HEADER_ROWS.get(migration_type, 3)

    debit_acc_num = cstr(column_plan.get("debit_account") or "").strip()
    credit_acc_num = cstr(column_plan.get("credit_account") or "").strip()
    # amount_col / name_col may be "|"-separated candidate names
    amount_col_candidates = [c.strip() for c in cstr(column_plan.get("amount_col") or "").split("|") if c.strip()]
    name_col_candidates = [c.strip() for c in cstr(column_plan.get("name_col") or "").split("|") if c.strip()]

    if debit_acc_num == "__temporary_opening__":
        debit_account = _ensure_temporary_opening_account(company)
    else:
        debit_account = _resolve_leaf_or_child_account_by_number(debit_acc_num, company) if debit_acc_num else None
    if credit_acc_num == "__temporary_opening__":
        credit_account = _ensure_temporary_opening_account(company)
    else:
        credit_account = _resolve_leaf_or_child_account_by_number(credit_acc_num, company) if credit_acc_num else None

    if not debit_account:
        frappe.throw(
            _("Không tìm thấy tài khoản Nợ '{0}' trong hệ thống (file: {1})").format(debit_acc_num or "?", file_name)
        )
    if not credit_account:
        frappe.throw(
            _("Không tìm thấy tài khoản Có '{0}' trong hệ thống (file: {1})").format(credit_acc_num or "?", file_name)
        )
    if not amount_col_candidates:
        frappe.throw(_("Cột số tiền chưa được xác định trong kế hoạch AI (file: {0})").format(file_name))

    rows = extract_records(file_path, None, header_row)
    je_accounts = []

    for row in rows:
        # Try each candidate column name in order; use first with a non-zero value
        amount = 0.0
        used_amount_col = amount_col_candidates[0]
        for _ac in amount_col_candidates:
            _v = _amount(row.get(_ac))
            if _v:
                amount = _v
                used_amount_col = _ac
                break
        if not amount or amount <= 0:
            continue

        remark_parts = [file_name]
        name_val = None
        for _nc in name_col_candidates:
            name_val = _text(row.get(_nc))
            if name_val:
                break
        if name_val:
            remark_parts.append(name_val)
        remark = " | ".join(remark_parts)

        je_accounts.append({
            "account": debit_account,
            "debit_in_account_currency": amount,
            "credit_in_account_currency": 0,
            "user_remark": remark,
        })
        je_accounts.append({
            "account": credit_account,
            "debit_in_account_currency": 0,
            "credit_in_account_currency": amount,
            "user_remark": remark,
        })

    if not je_accounts:
        frappe.throw(
            _("Không có dòng dữ liệu hợp lệ trong file '{0}' (cột số tiền thử: '{1}')").format(
                file_name, " | ".join(amount_col_candidates))
        )

    je = frappe.new_doc("Journal Entry")
    je.voucher_type = "Opening Entry"
    je.is_opening = "Yes"
    je.company = company
    je.posting_date = posting_date
    note = column_plan.get("note") or ""
    je.user_remark = f"[AI Opening Import] {file_name}" + (f" — {note}" if note else "")
    for acc_row in je_accounts:
        je.append("accounts", acc_row)

    je.insert(ignore_permissions=True)
    if submit:
        je.submit()
    frappe.db.commit()
    return je.name


def _company(import_doc) -> str:
    company = cstr(getattr(import_doc, "company", "")).strip()
    if company:
        return company
    company = frappe.db.get_value("Company", {}, "name")
    if not company:
        frappe.throw(_("Chưa có Company để import số dư đầu kỳ."))
    return company


def _scan_opening_files(import_doc) -> list[str]:
    folder_path = (getattr(import_doc, "folder_path", "") or "").strip()
    if not folder_path:
        frappe.throw(_("Vui lòng nhập đường dẫn thư mục chứa file số dư đầu kỳ trước khi chạy bước này."))
    try:
        files = scan_excel_files(
            folder_path,
            "*.xlsx,*.xls",
            recursive=bool(getattr(import_doc, "recursive", True)),
        )
    except Exception:
        frappe.log_error(frappe.get_traceback(), "Opening Balance Scan Failed")
        files = []
    if not files:
        frappe.throw(_("Không tìm thấy file Excel nào trong thư mục: {0}").format(folder_path))
    return files


def _opening_file_map(import_doc, discovered_files: list[str] | None = None) -> dict[str, str]:
    by_name: dict[str, str] = {}
    for row in getattr(import_doc, "files", []) or []:
        file_name = cstr(getattr(row, "file_name", "")).strip()
        file_path = cstr(getattr(row, "file_path", "")).strip()
        if file_name and file_path:
            by_name[file_name] = file_path

    # Always prefer the current folder contents so newly added/replaced files are
    # visible without requiring a full AI analysis pass.
    for file_path in discovered_files if discovered_files is not None else _scan_opening_files(import_doc):
        path = Path(file_path)
        by_name[path.name] = str(path)

    return {
        key: by_name.get(file_name)
        for key, file_name in OPENING_FILES.items()
        if by_name.get(file_name)
    }


def _opening_file_map_from_slots(import_doc) -> dict[str, str]:
    """Primary source of truth: read file paths from file_slots_json field."""
    slots: dict = {}
    if getattr(import_doc, "file_slots_json", None):
        try:
            slots = frappe.parse_json(import_doc.file_slots_json) or {}
        except Exception:
            slots = {}
    if not isinstance(slots, dict):
        slots = {}
    return {k: v for k, v in slots.items() if k in OPENING_FILES and v and Path(v).exists()}


def _opening_file_map_from_classified_files(files: list[dict]) -> dict[str, str]:
    file_map: dict[str, str] = {}
    for item in files or []:
        if not isinstance(item, dict):
            continue
        migration_type = cstr(item.get("migration_type")).strip()
        file_path = cstr(item.get("file_path")).strip()
        if migration_type in OPENING_FILES and file_path:
            file_map[migration_type] = file_path
    return file_map


def _opening_file_map_from_saved_analysis(import_doc, discovered_files: list[str] | None = None) -> dict[str, str]:
    if getattr(import_doc, "analysis_json", None):
        try:
            parsed = frappe.parse_json(import_doc.analysis_json)
        except Exception:
            parsed = {}
        if isinstance(parsed, dict) and isinstance(parsed.get("files"), list):
            file_map = _opening_file_map_from_classified_files(parsed.get("files") or [])
            if file_map:
                return file_map
    return _opening_file_map(import_doc, discovered_files=discovered_files)


def _opening_analysis_message(file_count: int, ai_fallback: bool, master_plan: dict | None) -> str:
    message = (
        _("AI chưa kết nối được; đã phân tích {0} file đầu kỳ bằng rule local.").format(file_count)
        if ai_fallback
        else _("Đã phân tích {0} file đầu kỳ.").format(file_count)
    )
    master_plan = master_plan or {}
    missing = int(master_plan.get("missing") or 0)
    failed = int(master_plan.get("failed") or 0)
    if missing:
        message += " " + _("Phát hiện {0} Customer/Supplier/Employee còn thiếu; cần user xác nhận trước khi tạo.").format(missing)
    if failed:
        message += " " + _("Có {0} dòng master chưa phân tích được, xem chi tiết lỗi.").format(failed)
    return message


def _opening_master_create_message(result: dict) -> str:
    return _(
        "Đã tạo {0}, đã có sẵn {1}, bỏ qua {2}, lỗi {3} Customer/Supplier/Employee."
    ).format(
        int(result.get("created") or 0),
        int(result.get("existing") or 0),
        int(result.get("skipped") or 0),
        int(result.get("failed") or 0),
    )


def _empty_party_auto_master_bucket() -> dict:
    return {
        "created": 0,
        "existing": 0,
        "missing": 0,
        "skipped": 0,
        "failed": 0,
        "records": [],
        "created_names": [],
        "errors": [],
    }


def _inspect_opening_missing_parties(file_map: dict[str, str]) -> dict:
    result = _process_opening_party_candidates(file_map, create=False)
    bank_result = _process_opening_bank_accounts(file_map, create=False)
    result["banks"] = bank_result
    result["missing"] = int(result.get("missing") or 0) + int(bank_result.get("missing") or 0)
    return result


def _process_opening_party_candidates(
    file_map: dict[str, str],
    create: bool = False,
    company: str | None = None,
    posting_date: str | date | None = None,
) -> dict:
    """Inspect or create minimal party masters for opening migration.

    In analysis mode this only produces a confirmation plan. In create mode it
    inserts the missing Customer/Supplier/Employee records after the user has
    explicitly approved the action.
    """
    result = {
        "mode": "create_masters" if create else "preview_masters",
        "requires_confirmation": not create,
        "created": 0,
        "existing": 0,
        "missing": 0,
        "skipped": 0,
        "failed": 0,
        "scanned": 0,
        "customers": _empty_party_auto_master_bucket(),
        "suppliers": _empty_party_auto_master_bucket(),
        "employees": _empty_party_auto_master_bucket(),
        "errors": [],
    }
    if not file_map:
        return result

    seen: set[tuple[str, str, str, str]] = set()
    for index, candidate in enumerate(_opening_party_candidates(file_map), start=1):
        doctype = candidate.get("doctype")
        if doctype not in OPENING_PARTY_BUCKETS:
            continue

        bucket = result[OPENING_PARTY_BUCKETS[doctype]]
        code = _text(candidate.get("code"))
        label = _text(candidate.get("label"))
        tax_id = _text(candidate.get("tax_id"))
        if not code and not label:
            result["skipped"] += 1
            bucket["skipped"] += 1
            continue

        dedupe_key = (
            doctype,
            _party_match_key(code),
            _party_match_key(label),
            _party_match_key(tax_id),
        )
        if dedupe_key in seen:
            continue
        seen.add(dedupe_key)
        result["scanned"] += 1

        existing = _find_existing_party(
            doctype,
            code=code,
            label=label,
            tax_id=tax_id,
            company=company,
            allow_label_fallback=not bool(code),
        )
        if existing:
            result["existing"] += 1
            bucket["existing"] += 1
            continue

        if not create:
            _record_opening_party_missing(result, bucket, candidate)
            continue

        try:
            party_name = _create_opening_party_with_savepoint(
                candidate,
                index,
                company=company,
                posting_date=posting_date,
            )
        except Exception as exc:
            if not _is_duplicate_error(exc):
                _record_opening_party_error(result, bucket, candidate, exc)
                # frappe.throw() (e.g. Customer.validate_name_with_customer_group())
                # queues its message to frappe.message_log before raising —
                # catching the exception here doesn't clear that queue, so
                # every failed row leaves a stray popup for the browser even
                # though it's already recorded as a handled failure above.
                frappe.clear_messages()
                continue

            # If the database collation rejected a visually similar docname,
            # retry with a deterministic MIG suffix instead of treating it as
            # a real duplicate.
            existing = _find_existing_party(
                doctype,
                code=code,
                label=label,
                tax_id=tax_id,
                company=company,
                allow_label_fallback=not bool(code),
            )
            if existing:
                result["existing"] += 1
                bucket["existing"] += 1
                continue
            try:
                party_name = _create_opening_party_with_savepoint(
                    candidate,
                    index,
                    company=company,
                    posting_date=posting_date,
                    force_collision_name=True,
                )
            except Exception as retry_exc:
                _record_opening_party_error(result, bucket, candidate, retry_exc)
                frappe.clear_messages()
                continue

        result["created"] += 1
        bucket["created"] += 1
        if party_name and len(bucket["created_names"]) < 20:
            bucket["created_names"].append(party_name)

    return result


def _process_opening_bank_accounts(
    file_map: dict[str, str],
    create: bool = False,
    company: str | None = None,
) -> dict:
    """Inspect or create Bank Account master records for opening bank balance migration."""
    result = {
        "mode": "create_masters" if create else "preview_masters",
        "created": 0,
        "existing": 0,
        "missing": 0,
        "failed": 0,
        "errors": [],
        "created_names": [],
    }
    if not file_map or "bank_balance" not in file_map:
        return result

    resolved_company = (
        company
        or frappe.defaults.get_user_default("Company")
        or frappe.db.get_single_value("Global Defaults", "default_company")
        or ""
    )

    seen: set[str] = set()
    for row in _bank_opening_rows(resolved_company, file_map):
        bank_no = row.bank_account_no
        if not bank_no or bank_no in seen:
            continue
        seen.add(bank_no)

        if row.bank_account:
            result["existing"] += 1
            continue

        if not row.account:
            # GL Account not found either — nothing to link to
            result["missing"] += 1
            continue

        if not create:
            result["missing"] += 1
            continue

        savepoint = f"bank_account_{bank_no}"
        frappe.db.savepoint(savepoint)
        try:
            account_name = row.account or ""
            # account full name format: "1121.20 - TIỀN VND TẠI NH MB...- DCNET"
            # strip the company suffix and account number prefix to get a readable label
            parts = account_name.split(" - ")
            label = row.label or (parts[1] if len(parts) >= 2 else parts[0])

            bank_doc = frappe.new_doc("Bank Account")
            bank_doc.account_name = label[:140]
            bank_doc.bank_account_no = bank_no
            bank_doc.account = row.account
            if frappe.get_meta("Bank Account").get_field("company"):
                bank_doc.company = resolved_company
            bank_doc.insert(ignore_permissions=True, ignore_mandatory=True)
            result["created"] += 1
            if len(result["created_names"]) < 20:
                result["created_names"].append(bank_doc.name)
        except Exception as exc:
            frappe.db.rollback(save_point=savepoint)
            result["failed"] += 1
            result["errors"].append(str(exc))

    return result


def _opening_party_candidates(file_map: dict[str, str]) -> list[dict]:
    candidates: list[dict] = []
    party_balance_specs = [
        ("customer_balance", "Customer", "Mã khách hàng", "Tên khách hàng"),
        ("supplier_balance", "Supplier", "Mã nhà cung cấp", "Tên nhà cung cấp"),
        ("employee_balance", "Employee", "Mã nhân viên", "Tên nhân viên"),
    ]
    for key, doctype, code_field, label_field in party_balance_specs:
        try:
            source_records = _records(file_map, key)
        except Exception:
            frappe.log_error(frappe.get_traceback(), f"Opening Auto Party Read Failed: {key}")
            continue
        for source_index, row in enumerate(source_records, start=4):
            if _is_total_row(row):
                continue
            code = _text(row.get(code_field))
            label = _text(row.get(label_field))
            if not code and not label:
                continue
            candidates.append({
                "doctype": doctype,
                "code": code,
                "label": label,
                "tax_id": _party_tax_id_from_row(row),
                "source": OPENING_FILES[key],
                "source_row": source_index,
            })

    for invoice_type in ("sales_invoice", "purchase_invoice"):
        doctype = "Customer" if invoice_type == "sales_invoice" else "Supplier"
        start_row = (HEADER_ROWS.get(invoice_type) or 4) + 1
        try:
            source_records = _records(file_map, invoice_type)
        except Exception:
            frappe.log_error(frappe.get_traceback(), f"Opening Auto Party Read Failed: {invoice_type}")
            continue
        for source_index, row in enumerate(source_records, start=start_row):
            if not _is_invoice_line(row, invoice_type):
                continue
            label = _invoice_party_name(row, invoice_type)
            if not label:
                continue
            candidates.append({
                "doctype": doctype,
                "code": "",
                "label": label,
                "tax_id": _invoice_tax_id(row, invoice_type),
                "source": OPENING_FILES[invoice_type],
                "source_row": source_index,
            })

    return candidates


def _party_tax_id_from_row(row: dict) -> str:
    for fieldname in (
        "Mã số thuế",
        "MST",
        "Mã số thuế/CCCD",
        "Mã số thuế CCCD",
        "Mã số thuế/CCCD chủ hộ",
        "Tax ID",
    ):
        tax_id = _text(row.get(fieldname))
        if tax_id:
            return tax_id
    return ""


def _create_opening_party_with_savepoint(
    candidate: dict,
    index: int,
    company: str | None = None,
    posting_date: str | date | None = None,
    force_collision_name: bool = False,
) -> str:
    savepoint = f"opening_party_{index}{'_retry' if force_collision_name else ''}"
    frappe.db.savepoint(savepoint)
    try:
        party_name = _insert_opening_party(
            candidate["doctype"],
            code=candidate.get("code"),
            label=candidate.get("label"),
            tax_id=candidate.get("tax_id"),
            company=company,
            posting_date=posting_date,
            force_collision_name=force_collision_name,
        )
        frappe.db.release_savepoint(savepoint)
        return party_name
    except Exception:
        frappe.db.rollback(save_point=savepoint)
        raise


def _insert_opening_party(
    doctype: str,
    code: str | None = None,
    label: str | None = None,
    tax_id: str | None = None,
    company: str | None = None,
    posting_date: str | date | None = None,
    force_collision_name: bool = False,
) -> str:
    code = _text(code)
    label = _text(label) or code
    tax_id = _text(tax_id)
    existing = _find_existing_party(
        doctype,
        code=code,
        label=label,
        tax_id=tax_id,
        company=company,
        allow_label_fallback=not bool(code),
    )
    if existing:
        return existing

    party = frappe.new_doc(doctype)
    clash_forced_name = None
    if doctype == "Customer":
        party.customer_name = label or _("Khách hàng migration")
        # Same collision _get_or_create_customer() already guards against
        # (used by the invoice-import flow): ERPNext refuses to create a
        # Customer whose docname (== customer_name here) matches an existing
        # Customer Group. This code path (opening Journal Entry / "Tạo master
        # thiếu") builds its own Customer doc instead of calling
        # _get_or_create_customer(), so without this it hit the same
        # "Customer Group exists with same name" error uncaught.
        clash_forced_name, matching_group = _resolve_customer_group_name_clash(party.customer_name)
        party.customer_group = matching_group or _default_customer_group()
        party.territory = _ensure_group_doc("Territory", "All Territories")
        if party.meta.get_field("customer_type"):
            party.customer_type = "Company"
        if code and party.meta.get_field("customer_code"):
            party.customer_code = code
    elif doctype == "Supplier":
        party.supplier_name = label or _("Nhà cung cấp migration")
        party.supplier_group = _default_supplier_group()
        if party.meta.get_field("supplier_type"):
            party.supplier_type = "Company"
        if code and party.meta.get_field("supplier_code"):
            party.supplier_code = code
    elif doctype == "Employee":
        party.first_name = label or code or _("Nhân viên migration")
        if party.meta.get_field("employee_name"):
            party.employee_name = label or code or _("Nhân viên migration")
        if code and party.meta.get_field("employee_number"):
            party.employee_number = code
        if party.meta.get_field("company"):
            party.company = company or frappe.db.get_value("Company", {}, "name")
        if party.meta.get_field("status"):
            party.status = "Active"
        if party.meta.get_field("date_of_joining"):
            party.date_of_joining = getdate(posting_date or "2026-01-01")
    else:
        frappe.throw(_("Không hỗ trợ tự tạo master cho {0}.").format(doctype))

    if tax_id and party.meta.get_field("tax_id"):
        party.tax_id = tax_id

    docname = (
        _opening_party_collision_docname(doctype, code or label)
        if force_collision_name
        else (clash_forced_name or _safe_opening_party_docname(code))
    )
    if docname:
        party.name = docname
        party.flags.name_set = True

    party.flags.ignore_mandatory = True
    party.insert(ignore_permissions=True, ignore_mandatory=True)
    return party.name


def _record_opening_party_missing(result: dict, bucket: dict, candidate: dict) -> None:
    result["missing"] += 1
    bucket["missing"] += 1
    if len(bucket["records"]) >= 50:
        return
    bucket["records"].append({
        "doctype": candidate.get("doctype"),
        "source": candidate.get("source"),
        "source_row": candidate.get("source_row"),
        "code": candidate.get("code"),
        "label": candidate.get("label"),
        "tax_id": candidate.get("tax_id"),
    })


def _record_opening_party_error(result: dict, bucket: dict, candidate: dict, exc: Exception) -> None:
    result["failed"] += 1
    bucket["failed"] += 1
    error = {
        "doctype": candidate.get("doctype"),
        "source": candidate.get("source"),
        "source_row": candidate.get("source_row"),
        "code": candidate.get("code"),
        "label": candidate.get("label"),
        "error": _clean_error_message(exc, limit=500),
    }
    if len(bucket["errors"]) < 20:
        bucket["errors"].append(error)
    if len(result["errors"]) < 30:
        result["errors"].append(error)


def _find_existing_party(
    doctype: str,
    code: str | None = None,
    label: str | None = None,
    tax_id: str | None = None,
    company: str | None = None,
    allow_label_fallback: bool = True,
) -> str | None:
    code = _text(code)
    label = _text(label)
    tax_id = _text(tax_id)
    if doctype not in OPENING_PARTY_BUCKETS:
        return None

    if code:
        for candidate_name in _opening_party_name_candidates(doctype, code):
            existing = _get_existing_by_field_exact(doctype, "name", candidate_name)
            if existing:
                return existing
        code_field = {
            "Customer": "customer_code",
            "Supplier": "supplier_code",
            "Employee": "employee_number",
        }.get(doctype)
        existing = _get_existing_by_field_exact(doctype, code_field, code)
        if existing:
            return existing
    else:
        code_field = None

    if tax_id and doctype in {"Customer", "Supplier"}:
        existing = _get_existing_by_field_exact(doctype, "tax_id", tax_id)
        if existing:
            return existing

    if label and (
        allow_label_fallback
        or not code
        or (code_field and not _doctype_has_field(doctype, code_field))
    ):
        label_field = {
            "Customer": "customer_name",
            "Supplier": "supplier_name",
            "Employee": "employee_name",
        }.get(doctype)
        existing = _get_existing_by_field_exact(doctype, label_field, label)
        if existing:
            return existing
        if doctype == "Employee":
            existing = _get_existing_by_field_exact(doctype, "first_name", label)
            if existing:
                return existing

    return None


def _opening_party_name_candidates(doctype: str, value: str | None) -> list[str]:
    """Names that may represent the same source party code in ERPNext.

    Source codes can contain characters such as "/" that we sanitise before
    assigning ``doc.name``. Duplicate retries can also add a deterministic MIG
    suffix. Existence checks must mirror that naming logic; otherwise the
    preview says a party is missing even though the created Customer/Supplier
    already exists under the sanitised name.
    """
    raw = _text(value)
    candidates: list[str] = []
    for candidate in (
        raw,
        _safe_opening_party_docname(raw),
        _opening_party_collision_docname(doctype, raw) if raw else "",
    ):
        if candidate and candidate not in candidates:
            candidates.append(candidate)
    return candidates


def _doctype_has_field(doctype: str, fieldname: str | None) -> bool:
    fieldname = _text(fieldname)
    if not fieldname:
        return False
    try:
        return bool(frappe.get_meta(doctype).get_field(fieldname))
    except Exception:
        return False


def _get_existing_by_field_exact(doctype: str, fieldname: str | None, value: str | None) -> str | None:
    value = _text(value)
    fieldname = _text(fieldname)
    if not value or not fieldname:
        return None
    try:
        if fieldname == "name":
            existing_name = frappe.db.get_value(doctype, value, "name")
            return existing_name if _strict_text_equal(existing_name, value) else None

        meta = frappe.get_meta(doctype)
        if not meta.get_field(fieldname):
            return None
        rows = frappe.get_all(
            doctype,
            filters={fieldname: value},
            fields=["name", fieldname],
            limit_page_length=50,
        )
    except Exception:
        return None

    for row in rows:
        if _strict_text_equal(row.get(fieldname), value):
            return row.get("name")
    return None


def _strict_text_equal(left: Any, right: Any) -> bool:
    left_text = unicodedata.normalize("NFC", cstr(left or "").strip()).casefold()
    right_text = unicodedata.normalize("NFC", cstr(right or "").strip()).casefold()
    return bool(left_text) and left_text == right_text


def _party_match_key(value: str | None) -> str:
    return unicodedata.normalize("NFC", _text(value)).casefold()


def _safe_opening_party_docname(value: str | None) -> str:
    value = _text(value)
    if not value:
        return ""
    value = " ".join(value.split())
    for char in ('"', "'", "`", "\\", "/", "#", "?", "%", "\t", "\n", "\r"):
        value = value.replace(char, "-")
    value = value.strip(" -.")[:140].strip()
    if len(value) <= 120:
        return value
    digest = hashlib.sha1(value.encode("utf-8")).hexdigest()[:8].upper()
    return f"{value[:111].rstrip(' -')}-MIG-{digest}"


def _opening_party_collision_docname(doctype: str, value: str | None) -> str:
    base = _safe_opening_party_docname(value) or doctype
    digest = hashlib.sha1(f"{doctype}|{_text(value)}".encode("utf-8")).hexdigest()[:8].upper()
    suffix = f" - MIG-{digest}"
    return f"{base[:140 - len(suffix)].rstrip(' -')}{suffix}"


def _is_duplicate_error(exc: Exception) -> bool:
    text = " ".join(cstr(arg) for arg in (getattr(exc, "args", ()) or ())) or cstr(exc)
    return (
        exc.__class__.__name__ == "DuplicateEntryError"
        or "Duplicate entry" in text
        or "DuplicateEntryError" in text
        or "IntegrityError" in text and "1062" in text
    )


def _unrecognized_file_summary(discovered_files: list[str]) -> list[dict]:
    opening_file_names = set(OPENING_FILES.values())
    return [
        {"file_name": Path(file_path).name, "file_path": file_path}
        for file_path in discovered_files
        if Path(file_path).name not in opening_file_names
    ]


def _file_presence_summary(file_map: dict[str, str]) -> list[dict]:
    return [
        {
            "key": key,
            "file_name": file_name,
            "found": bool(file_map.get(key)),
            "file_path": file_map.get(key),
        }
        for key, file_name in OPENING_FILES.items()
    ]


def _records(file_map: dict[str, str], key: str) -> list[dict]:
    file_path = file_map.get(key)
    if not file_path:
        return []
    return extract_records(file_path, None, HEADER_ROWS[key])


def _build_opening_journal_plan(company: str, file_map: dict[str, str]) -> dict:
    missing_files = [
        OPENING_FILES[key]
        for key in ["account_balance", "customer_balance", "supplier_balance", "employee_balance", "bank_balance"]
        if not file_map.get(key)
    ]
    if missing_files:
        frappe.throw(_("Thiếu file số dư đầu kỳ bắt buộc: {0}").format(", ".join(missing_files)))

    detail_rows = _detail_opening_rows(company, file_map)
    overridden_accounts = _expand_with_parents({
        row.account_number
        for row in detail_rows
        if row.account_number
    })

    skipped_stock_rows: list[OpeningRow] = []
    account_rows = _account_opening_rows(company, file_map, overridden_accounts, skipped_stock_rows)
    rows_before_split = account_rows + detail_rows
    stock_offset_row = _stock_opening_offset_row(company, skipped_stock_rows)
    if stock_offset_row:
        rows_before_split.append(stock_offset_row)
    rows = [split_row.as_dict() for row in rows_before_split for split_row in _split_two_sided_row(row)]

    missing_links = _missing_links(rows)
    total_debit = round(sum(flt(row.get("debit")) for row in rows), 2)
    total_credit = round(sum(flt(row.get("credit")) for row in rows), 2)

    return {
        "rows": rows,
        "row_count": len(rows),
        "total_debit": total_debit,
        "total_credit": total_credit,
        "difference": round(total_debit - total_credit, 2),
        "missing_links": missing_links,
        "replaced_accounts": sorted(overridden_accounts),
        "skipped_stock_accounts": [row.as_dict() for row in skipped_stock_rows],
        "stock_adjustment_account": stock_offset_row.account if stock_offset_row else None,
        "source_breakdown": _source_breakdown(rows),
        "_debug": {
            "account_rows_count": len(account_rows),
            "detail_rows_count": len(detail_rows),
            "overridden_accounts": sorted(overridden_accounts),
            "skipped_stock_count": len(skipped_stock_rows),
            "rows_before_split": len(rows_before_split),
            "rows_after_split": len(rows),
            "note": "overridden_accounts includes parent codes auto-expanded from sub-accounts",
        },
    }


def _account_opening_rows(
    company: str,
    file_map: dict[str, str],
    overridden_accounts: set[str],
    skipped_stock_rows: list[OpeningRow] | None = None,
) -> list[OpeningRow]:
    source_rows = _records(file_map, "account_balance")
    source_rows = [row for index, row in enumerate(source_rows, start=4) if _is_real_account_balance_row(row)]
    leaf_rows = _leaf_account_rows(source_rows)
    rows: list[OpeningRow] = []
    for row in leaf_rows:
        account_number = _text(_col(row, "Số tài khoản", "Số TK", "Mã TK"))
        if account_number in overridden_accounts:
            continue
        account = _resolve_account(account_number, company)

        # If the matched account is a group (cannot be used in GL entries), try to
        # resolve it to the primary leaf descendant using VN account numbering convention.
        if account and frappe.db.get_value("Account", account, "is_group"):
            resolved = _find_primary_leaf_account(account, company)
            if resolved:
                account = resolved

        opening_row = OpeningRow(
            source=OPENING_FILES["account_balance"],
            source_row=int(flt(row.get("STT"))) + 3 if flt(row.get("STT")) else 0,
            account_number=account_number,
            account=account,
            debit=_amount(_col(row, "Dư Nợ", "Dư nợ", "Dư nọ", "Số dư nợ")),
            credit=_amount(_col(row, "Dư Có", "Dư có", "Số dư có")),
            label=_text(_col(row, "Tên tài khoản", "Tên TK")),
        )
        if _is_stock_account(account):
            if skipped_stock_rows is not None:
                skipped_stock_rows.append(opening_row)
            continue
        # Skip Receivable/Payable accounts — these are covered by customer/supplier/employee
        # balance files with per-party lines. A bulk account entry without party would fail
        # ERPNext validation when account_type is Receivable or Payable.
        if account and frappe.db.get_value("Account", account, "account_type") in ("Receivable", "Payable"):
            continue
        rows.append(opening_row)
    return rows


def _stock_opening_offset_row(company: str, skipped_stock_rows: list[OpeningRow]) -> OpeningRow | None:
    stock_net = round(
        sum(flt(row.debit) - flt(row.credit) for row in skipped_stock_rows),
        2,
    )
    if abs(stock_net) < 0.5:
        return None

    adjustment_account = _stock_opening_adjustment_account(company)
    return OpeningRow(
        source="Stock Reconciliation offset",
        source_row=0,
        account_number="STOCK-OPENING-OFFSET",
        account=adjustment_account,
        debit=stock_net if stock_net > 0 else 0,
        credit=abs(stock_net) if stock_net < 0 else 0,
        label=_("Bù trừ số dư tồn kho đầu kỳ; tài khoản Stock sẽ nhập bằng Stock Reconciliation."),
    )


def _detail_opening_rows(company: str, file_map: dict[str, str]) -> list[OpeningRow]:
    rows: list[OpeningRow] = []
    rows.extend(_party_opening_rows(company, file_map, "customer_balance", "Customer", "Mã khách hàng", "Tên khách hàng"))
    rows.extend(_party_opening_rows(company, file_map, "supplier_balance", "Supplier", "Mã nhà cung cấp", "Tên nhà cung cấp"))
    rows.extend(_party_opening_rows(company, file_map, "employee_balance", "Employee", "Mã nhân viên", "Tên nhân viên"))
    rows.extend(_bank_opening_rows(company, file_map))
    return rows


def _party_opening_rows(
    company: str,
    file_map: dict[str, str],
    key: str,
    party_type: str,
    code_field: str,
    label_field: str,
) -> list[OpeningRow]:
    rows: list[OpeningRow] = []
    for source_index, row in enumerate(_records(file_map, key), start=4):
        account_number = _text(_col(row, "Số tài khoản", "TK công nợ", "Số TK", "Mã TK"))
        if _is_total_row(row) or not _text(_col(row, code_field)) or not account_number:
            continue
        party_code = _text(_col(row, code_field))
        rows.append(
            OpeningRow(
                source=OPENING_FILES[key],
                source_row=source_index,
                account_number=account_number,
                account=_resolve_account(account_number, company),
                debit=_amount(_col(row, "Dư Nợ", "Dư nợ", "Dư nọ", "Số dư nợ")),
                credit=_amount(_col(row, "Dư Có", "Dư có", "Số dư có")),
                party_type=party_type,
                party_code=party_code,
                party=_resolve_party(party_type, party_code, _text(_col(row, label_field)), company=company),
                label=_text(_col(row, label_field)),
            )
        )
    return rows


def _bank_opening_rows(company: str, file_map: dict[str, str]) -> list[OpeningRow]:
    rows: list[OpeningRow] = []
    for source_index, row in enumerate(_records(file_map, "bank_balance"), start=4):
        bank_no = _bank_account_no(_col(row, "Số TK ngân hàng", "Tài khoản ngân hàng", "Số tài khoản ngân hàng", "STK ngân hàng"))
        if _is_total_row(row) or not bank_no:
            continue
        account_number = _text(_col(row, "Số tài khoản", "TK", "Mã TK"))
        rows.append(
            OpeningRow(
                source=OPENING_FILES["bank_balance"],
                source_row=source_index,
                account_number=account_number,
                account=_resolve_account(account_number, company),
                debit=_amount(_col(row, "Dư Nợ", "Dư nợ", "Số dư nợ")),
                credit=_amount(_col(row, "Dư Có", "Dư có", "Số dư có")),
                bank_account_no=bank_no,
                bank_account=_resolve_bank_account(bank_no, company),
                label=_text(_col(row, "Tên ngân hàng", "Tên NH")),
            )
        )
    return rows


def _is_real_account_balance_row(row: dict) -> bool:
    return bool(_text(_col(row, "Số tài khoản", "Số TK", "Mã TK"))) and not _is_total_row(row)


def _leaf_account_rows(rows: list[dict]) -> list[dict]:
    account_numbers = [_text(_col(row, "Số tài khoản", "Số TK", "Mã TK")) for row in rows if _text(_col(row, "Số tài khoản", "Số TK", "Mã TK"))]
    return [
        row for row in rows
        if not any(_is_account_parent(_text(other), _text(_col(row, "Số tài khoản", "Số TK", "Mã TK"))) for other in account_numbers)
    ]


def _is_account_parent(child: str, parent: str) -> bool:
    if not child or not parent or child == parent:
        return False
    if "." in child:
        return child.startswith(parent + ".") or child.rsplit(".", 1)[0] == parent
    return child.startswith(parent) and len(child) > len(parent)


def _split_two_sided_row(row: OpeningRow) -> list[OpeningRow]:
    """Collapse a two-sided row into its net direction.

    A party can have both Dư Nợ and Dư Có in the source file.
    We keep only the net amount so the JE has one clean line per party
    instead of two offsetting lines — this produces correct aging and
    party-ledger reports.
    """
    net = row.debit - row.credit
    if net > 0:
        return [OpeningRow(**{**row.__dict__, "debit": net, "credit": 0})]
    if net < 0:
        return [OpeningRow(**{**row.__dict__, "debit": 0, "credit": -net})]
    return []


def _missing_links(rows: list[dict]) -> list[dict]:
    missing = []
    for index, row in enumerate(rows, start=1):
        if not row.get("account"):
            missing.append({
                "row": index,
                "type": "Account",
                "value": row.get("account_number"),
                "source": row.get("source"),
                "source_row": row.get("source_row"),
            })
        if row.get("party_type") and row.get("party_code") and not row.get("party"):
            missing.append({
                "row": index,
                "type": row.get("party_type"),
                "value": row.get("party_code"),
                "label": row.get("label"),
                "source": row.get("source"),
                "source_row": row.get("source_row"),
            })
        if row.get("bank_account_no") and not row.get("bank_account"):
            missing.append({
                "row": index,
                "type": "Bank Account",
                "value": row.get("bank_account_no"),
                "label": row.get("label"),
                "source": row.get("source"),
                "source_row": row.get("source_row"),
            })
    return missing


def _source_breakdown(rows: list[dict]) -> list[dict]:
    by_source: dict[str, dict] = {}
    for row in rows:
        item = by_source.setdefault(row["source"], {"source": row["source"], "rows": 0, "debit": 0.0, "credit": 0.0})
        item["rows"] += 1
        item["debit"] += flt(row.get("debit"))
        item["credit"] += flt(row.get("credit"))
    return [
        {
            **item,
            "debit": round(item["debit"], 2),
            "credit": round(item["credit"], 2),
        }
        for item in by_source.values()
    ]


def _related_file_summary(file_map: dict[str, str]) -> dict:
    return {
        "stock_opening": _count_stock_opening_rows(file_map.get("stock_detail")),
        "fixed_asset_file_found": bool(file_map.get("fixed_asset")),
        "tools_file_found": bool(file_map.get("tools")),
        "prepaid_file_found": bool(file_map.get("prepaid")),
    }


def _count_stock_opening_rows(file_path: str | None) -> dict:
    if not file_path:
        return {"found": False, "rows": 0}
    records = extract_records(file_path, None, 4)
    rows = [row for row in records if _is_stock_opening_source_row(row)]
    return {
        "found": True,
        "rows": len(rows),
        "note": "Không nhập bằng Opening Journal Entry; xử lý bằng Stock Reconciliation để ghi đúng Stock Ledger và tài khoản kho.",
    }


def _stock_opening_summary(company: str, file_map: dict[str, str]) -> dict:
    plan = _build_stock_opening_plan(company, file_map, limit=0, preview=True)
    account_balance_stock_value = _stock_like_account_balance_net(company, file_map)
    return {
        "found": bool(file_map.get("stock_detail")),
        "row_count": len(plan["rows"]),
        "source_rows": plan["source_rows"],
        "total_qty": plan["total_qty"],
        "total_value": plan["total_value"],
        "account_balance_stock_value": account_balance_stock_value,
        "balance_difference": round(plan["total_value"] - account_balance_stock_value, 2),
        "missing_items": plan["missing_items"],
        "missing_warehouses": plan["missing_warehouses"],
        "missing_uoms": plan["missing_uoms"],
        "stock_accounts": plan["stock_accounts"],
        "stock_adjustment_account": _stock_opening_adjustment_account(company),
        "errors": plan["errors"][:30],
        "handler": "stock_reconciliation",
        "doctype": "Stock Reconciliation",
        "note": _(
            "Tồn kho đầu kỳ sẽ được nhập bằng Stock Reconciliation để ERPNext ghi Stock Ledger "
            "và GL vào tài khoản kho như 1561; Temporary Opening chỉ là tài khoản đối ứng."
        ),
    }


def _build_stock_opening_plan(
    company: str,
    file_map: dict[str, str],
    limit: int = 0,
    preview: bool = False,
) -> dict:
    rows: list[dict] = []
    grouped: dict[tuple[str, str], dict] = {}
    errors: list[dict] = []
    source_rows = 0
    missing_items: set[str] = set()
    missing_warehouses: set[str] = set()
    missing_uoms: set[str] = set()
    stock_accounts: set[str] = set()

    # stock_balance (summary list) and stock_detail (ledger with Diễn giải filter) are alternative
    # sources of the same data — prefer stock_balance when both are uploaded.
    _vthh_source = "stock_balance" if file_map.get("stock_balance") else "stock_detail"
    _stock_sources = [
        (mt, HEADER_ROWS.get(mt, 4))
        for mt in (_vthh_source, "tools")
        if file_map.get(mt)
    ]
    _all_stock_rows = []
    for _mt, _hrow in _stock_sources:
        for _i, _r in enumerate(_records(file_map, _mt), start=(_hrow + 1)):
            _all_stock_rows.append((_i, _r))

    for source_index, source_row in _all_stock_rows:
        if not _is_stock_opening_source_row(source_row):
            continue
        source_rows += 1

        item_code = _text(source_row.get("Mã hàng"))
        warehouse_label = _text(source_row.get("Tên kho") or source_row.get("Mã kho"))
        qty = _stock_opening_qty(source_row)
        value = _stock_opening_value(source_row)
        uom = _text(source_row.get("ĐVT chính (ĐVC)") or source_row.get("ĐVT") or "Nos")

        if not item_code or not warehouse_label:
            errors.append(_stock_opening_error(source_index, item_code, warehouse_label, _("Thiếu mã hàng hoặc kho.")))
            continue
        if qty < 0:
            errors.append(_stock_opening_error(source_index, item_code, warehouse_label, _("Tồn kho đầu kỳ không được âm.")))
            continue
        if qty == 0 and value == 0:
            continue
        if qty == 0 and value:
            errors.append(_stock_opening_error(source_index, item_code, warehouse_label, _("Có giá trị tồn nhưng số lượng bằng 0.")))
            continue

        stock_account = _stock_opening_account_for_row(source_row, company)
        if not stock_account:
            # COA chưa import → dùng số TK ưu tiên làm placeholder, resolve lúc thực thi
            stock_account = _preferred_stock_account_number(source_row)
            errors.append(_stock_opening_error(
                source_index, item_code, warehouse_label,
                _("TK {0} chưa có trong hệ thống (COA chưa import?). Sẽ tự gán khi thực thi.").format(stock_account),
                severity="warning",
            ))
        stock_accounts.add(stock_account)

        key = (item_code, warehouse_label)
        item = grouped.setdefault(key, {
            "source": OPENING_FILES["stock_detail"],
            "source_rows": [],
            "item_code": item_code,
            "item_name": _text(source_row.get("Tên hàng")) or item_code,
            "item_group_label": _text(source_row.get("Tên nhóm VTHH") or source_row.get("Mã nhóm VTHH") or source_row.get("Nhóm VTHH")),
            "warehouse_label": warehouse_label,
            "uom": uom,
            "qty": 0.0,
            "value": 0.0,
            "stock_account": stock_account,
        })
        if item.get("stock_account") != stock_account:
            errors.append(_stock_opening_error(
                source_index,
                item_code,
                warehouse_label,
                _("Cùng mã hàng/kho nhưng khác tài khoản kho: {0} và {1}.").format(item.get("stock_account"), stock_account),
            ))
            continue
        item["source_rows"].append(source_index)
        item["qty"] += qty
        item["value"] += value

        if preview:
            if not frappe.db.exists("Item", item_code):
                missing_items.add(item_code)
            if not _find_opening_stock_warehouse(company, warehouse_label):
                missing_warehouses.add(warehouse_label)
            if uom and not frappe.db.exists("UOM", uom) and not frappe.db.get_value("UOM", {"uom_name": uom}, "name"):
                missing_uoms.add(uom)

        if limit and len(grouped) >= limit:
            break

    for item in grouped.values():
        qty = flt(item.get("qty"))
        value = flt(item.get("value"))
        item["qty"] = qty
        item["value"] = round(value, 2)
        item["valuation_rate"] = round(value / qty, 6) if qty else 0
        rows.append(item)

    return {
        "rows": rows,
        "source_rows": source_rows,
        "total_qty": round(sum(flt(row.get("qty")) for row in rows), 6),
        "total_value": round(sum(flt(row.get("value")) for row in rows), 2),
        "missing_items": len(missing_items),
        "missing_warehouses": len(missing_warehouses),
        "missing_uoms": len(missing_uoms),
        "stock_accounts": sorted(stock_accounts),
        "errors": errors,
    }


def _is_stock_opening_source_row(row: dict) -> bool:
    if not _text(row.get("Mã hàng")):
        return False
    dien_giai = row.get("Diễn giải")
    # File có cột Diễn giải → chỉ lấy dòng "Số dư đầu kỳ" (sổ chi tiết có nhiều loại dòng)
    # File không có cột Diễn giải → đây là danh sách tồn kho thuần, mọi dòng có Mã hàng đều hợp lệ
    if dien_giai is not None:
        return _fold_key(dien_giai) == "so du dau ky"
    return True


def _stock_opening_qty(row: dict) -> float:
    for fieldname in ("column_22", "Tồn", "Số lượng tồn", "Tồn đầu kỳ", "Số lượng theo ĐVC", "Số lượng"):
        value = _amount(row.get(fieldname))
        if value:
            return value
    return 0.0


def _stock_opening_value(row: dict) -> float:
    for fieldname in ("column_23", "Giá trị tồn", "Giá trị", "Thành tiền", "Tổng tiền"):
        value = _amount(row.get(fieldname))
        if value:
            return value
    qty = _stock_opening_qty(row)
    rate = _amount(row.get("Đơn giá theo ĐVC")) or _amount(row.get("Đơn giá"))
    return qty * rate


def _preferred_stock_account_number(row: dict) -> str:
    """Return the preferred stock TK NUMBER (bare, not full ERPNext account name) for a row.

    Used as a placeholder when the account doesn't exist in DB yet (COA not imported).
    Mirrors the priority order of _stock_opening_account_for_row.
    """
    warehouse_label = _text(row.get("Tên kho") or row.get("Kho") or row.get("Mã kho"))
    if warehouse_label:
        for pattern, prefixes in _WAREHOUSE_ACCOUNT_HINTS:
            if pattern.search(warehouse_label):
                return prefixes[0]
    return STOCK_OPENING_DEFAULT_ACCOUNT_PREFIXES[0]  # "1561"


def _stock_opening_account_for_row(row: dict, company: str) -> str | None:
    # 1. Explicit TK from source file takes highest priority.
    account_number = _text(row.get("TK Kho") or row.get("Tài khoản kho"))
    account = _resolve_leaf_account_by_number(account_number, company) if account_number else None
    if account and _is_stock_account(account):
        return account

    # 2. Infer TK from warehouse name (e.g. "Kho NVL" → 152, "Kho CCDC" → 1531).
    warehouse_label = _text(row.get("Tên kho") or row.get("Kho") or row.get("Mã kho"))
    if warehouse_label:
        for pattern, prefixes in _WAREHOUSE_ACCOUNT_HINTS:
            if pattern.search(warehouse_label):
                for prefix in prefixes:
                    account = _first_leaf_account_by_number_prefix(prefix, company)
                    if account and _is_stock_account(account):
                        return account
                break

    # 3. Global default prefix list (1561 → 156 → 155 → …).
    for prefix in STOCK_OPENING_DEFAULT_ACCOUNT_PREFIXES:
        account = _first_leaf_account_by_number_prefix(prefix, company)
        if account and _is_stock_account(account):
            return account

    # 4. Last resort: any stock-type leaf account on this company.
    return frappe.db.get_value("Account", {"company": company, "account_type": "Stock", "is_group": 0}, "name")


def _stock_like_account_balance_net(company: str, file_map: dict[str, str]) -> float:
    source_rows = _records(file_map, "account_balance")
    source_rows = [row for row in source_rows if _is_real_account_balance_row(row)]
    leaf_rows = _leaf_account_rows(source_rows)
    total = 0.0
    for row in leaf_rows:
        account_number = _text(row.get("Số tài khoản"))
        if not account_number.startswith(("151", "152", "153", "155", "156", "157")):
            continue
        total += _amount(row.get("Dư Nợ")) - _amount(row.get("Dư Có"))
    return round(total, 2)


def _stock_opening_error(source_row: int, item_code: str, warehouse: str, error: str,
                          severity: str = "error") -> dict:
    return {
        "source": OPENING_FILES["stock_detail"],
        "source_row": source_row,
        "item_code": item_code,
        "warehouse": warehouse,
        "error": error,
        "severity": severity,  # "error" | "warning"
    }


def _invoice_summary(file_map: dict[str, str], invoice_type: str) -> dict:
    groups = _group_invoice_rows(file_map, invoice_type)
    return {
        "found": bool(file_map.get(invoice_type)),
        "invoice_count": len(groups),
        "line_count": sum(len(group["rows"]) for group in groups),
        "net_total": round(sum(group["net_total"] for group in groups), 2),
        "tax_total": round(sum(group["tax_total"] for group in groups), 2),
        "grand_total": round(sum(group["grand_total"] for group in groups), 2),
        "handler": invoice_type,
        "doctype": "Sales Invoice" if invoice_type == "sales_invoice" else "Purchase Invoice",
    }


def _group_invoice_rows(file_map: dict[str, str], invoice_type: str) -> list[dict]:
    file_path = file_map.get(invoice_type)
    if not file_path:
        return []

    records = _records(file_map, invoice_type)
    grouped: dict[str, dict] = {}
    for source_index, row in enumerate(records, start=(HEADER_ROWS.get(invoice_type) or 4) + 1):
        if not _is_invoice_line(row, invoice_type):
            continue

        invoice_no = _text(row.get("Số hóa đơn"))
        voucher_no = _text(row.get("Số chứng từ"))
        serial = _text(row.get("Ký hiệu HĐ"))
        key = "|".join([serial, invoice_no, voucher_no])
        if not key.strip("|"):
            continue

        group = grouped.setdefault(key, {
            "source": OPENING_FILES[invoice_type],
            "source_key": key,
            "source_rows": [],
            "rows": [],
            "invoice_no": invoice_no,
            "voucher_no": voucher_no,
            "serial": serial,
            "posting_date": _date(row.get("Ngày hạch toán") or row.get("Ngày hóa đơn")),
            "bill_date": _date(row.get("Ngày hóa đơn") or row.get("Ngày chứng từ")),
            "party_name": _invoice_party_name(row, invoice_type),
            "tax_id": _invoice_tax_id(row, invoice_type),
            "remarks": _text(row.get("Diễn giải")),
            "net_total": 0.0,
            "tax_total": 0.0,
            "grand_total": 0.0,
            "tax_account_number": _text(row.get("Tài khoản thuế")),
        })
        group["source_rows"].append(source_index)
        group["rows"].append({**row, "__source_row_number": source_index})
        net = _invoice_net_amount(row, invoice_type)
        tax = _invoice_tax_amount(row, invoice_type)
        group["net_total"] += net
        group["tax_total"] += tax
        group["grand_total"] += net + tax
        if not group.get("tax_account_number"):
            group["tax_account_number"] = _text(row.get("Tài khoản thuế"))

    return list(grouped.values())


def _is_invoice_line(row: dict, invoice_type: str) -> bool:
    if _is_total_row(row):
        return False
    if _text(row.get("Ký hiệu mẫu HĐ")).startswith("Nhóm"):
        return False
    if not _text(row.get("Số hóa đơn")) and not _text(row.get("Số chứng từ")):
        return False
    if not _invoice_party_name(row, invoice_type):
        return False
    return _invoice_net_amount(row, invoice_type) > 0 or _invoice_tax_amount(row, invoice_type) > 0


def _invoice_party_name(row: dict, invoice_type: str) -> str:
    fieldname = "Tên người mua" if invoice_type == "sales_invoice" else "Tên người bán"
    return _text(row.get(fieldname))


def _invoice_tax_id(row: dict, invoice_type: str) -> str:
    fieldname = "Mã số thuế người mua" if invoice_type == "sales_invoice" else "Mã số thuế người bán"
    return _text(row.get(fieldname))


def _invoice_net_amount(row: dict, invoice_type: str) -> float:
    fieldname = (
        "Doanh số bán chưa có thuế GTGT"
        if invoice_type == "sales_invoice"
        else "Giá trị HHDV mua vào chưa có thuế"
    )
    return _amount(row.get(fieldname))


def _invoice_tax_amount(row: dict, invoice_type: str) -> float:
    return _amount(row.get("Thuế GTGT"))


def _build_migration_invoice(company: str, invoice_type: str, group: dict):
    doctype = "Sales Invoice" if invoice_type == "sales_invoice" else "Purchase Invoice"
    invoice = frappe.new_doc(doctype)
    invoice.company = company
    invoice.set_posting_time = 1
    invoice.posting_date = str(group.get("posting_date") or getdate())
    invoice.due_date = invoice.posting_date
    invoice.remarks = _invoice_remark(group)

    if invoice_type == "sales_invoice":
        invoice.customer = _get_or_create_customer(group["party_name"], group.get("tax_id"))
        invoice.debit_to = _resolve_leaf_or_child_account_by_number("131", company)
    else:
        invoice.supplier = _get_or_create_supplier(group["party_name"], group.get("tax_id"))
        invoice.bill_no = group.get("invoice_no") or group.get("voucher_no")
        invoice.bill_date = str(group.get("bill_date") or group.get("posting_date") or getdate())
        invoice.posting_date = str(max(_date(invoice.posting_date), _date(invoice.bill_date)))
        invoice.due_date = str(max(_date(invoice.due_date), _date(invoice.bill_date)))
        invoice.credit_to = _resolve_leaf_or_child_account_by_number("331", company)

    item_code = _ensure_migration_service_item(company)
    for row in group["rows"]:
        amount = _invoice_net_amount(row, invoice_type)
        if amount <= 0:
            continue
        source_qty = _amount(row.get("Số lượng"))
        qty = 1
        item_label = _text(row.get("Mặt hàng")) or group.get("remarks") or item_code
        description = item_label
        if source_qty and source_qty != 1:
            description = f"{item_label}\n\nSố lượng nguồn: {source_qty:g}"
        item_row = {
            "item_code": item_code,
            "item_name": _truncate_for_field(f"{doctype} Item", "item_name", item_label),
            "description": description,
            "qty": qty,
            "rate": amount,
            "amount": amount,
        }
        account = (
            _default_sales_income_account(company)
            if invoice_type == "sales_invoice"
            else _default_purchase_expense_account(company)
        )
        if invoice_type == "sales_invoice" and account:
            item_row["income_account"] = account
        elif invoice_type == "purchase_invoice" and account:
            item_row["expense_account"] = account

        cost_center = _default_cost_center(company)
        if cost_center:
            item_row["cost_center"] = cost_center
        invoice.append("items", item_row)

    tax_amount = flt(group.get("tax_total"))
    if tax_amount:
        tax_account = _resolve_leaf_or_child_account_by_number(group.get("tax_account_number"), company)
        if not tax_account:
            tax_account = (
                _resolve_leaf_or_child_account_by_number("33311", company)
                if invoice_type == "sales_invoice"
                else _resolve_leaf_or_child_account_by_number("1331", company)
            )
        if tax_account:
            invoice.append("taxes", {
                "charge_type": "Actual",
                "account_head": tax_account,
                "tax_amount": tax_amount,
                "description": f"VAT {group.get('tax_account_number') or ''}".strip(),
            })

    return invoice


def _find_existing_migration_invoice(doctype: str, company: str, source_key: str) -> str | None:
    marker = f"Source Invoice Key: {source_key}"
    rows = frappe.get_all(
        doctype,
        filters={
            "company": company,
            "docstatus": ["!=", 2],
        },
        fields=["name", "remarks"],
        limit_page_length=100000,
    )
    for row in rows:
        remark_lines = {
            cstr(line).strip()
            for line in cstr(row.get("remarks")).splitlines()
            if cstr(line).strip()
        }
        if marker in remark_lines:
            return row.get("name")
    return None


def _stock_opening_source_key(company: str, file_map: dict[str, str], posting_date: str) -> str:
    file_path = _text(file_map.get("stock_detail"))
    file_name = Path(file_path).name if file_path else OPENING_FILES["stock_detail"]
    digest = hashlib.sha1(f"{company}|{posting_date}|{file_name}".encode("utf-8")).hexdigest()[:12].upper()
    return f"{posting_date}|{file_name}|{digest}"


def _stock_opening_comment(source_key: str, file_map: dict[str, str], plan: dict) -> str:
    return "\n".join([
        STOCK_OPENING_SOURCE_MARKER,
        f"Source Key: {source_key}",
        f"Source File: {Path(_text(file_map.get('stock_detail'))).name or OPENING_FILES['stock_detail']}",
        f"Source Rows: {plan.get('source_rows') or 0}",
        f"Total Value: {plan.get('total_value') or 0}",
    ])


def _find_existing_opening_stock_reconciliation(company: str, source_key: str) -> str | None:
    marker = f"Source Key: {source_key}"
    reconciliations = frappe.get_all(
        "Stock Reconciliation",
        filters={
            "company": company,
            "purpose": "Opening Stock",
            "docstatus": ["!=", 2],
        },
        pluck="name",
        limit_page_length=1000,
    )
    if not reconciliations:
        return None

    comments = frappe.get_all(
        "Comment",
        filters={
            "reference_doctype": "Stock Reconciliation",
            "reference_name": ["in", reconciliations],
            "comment_type": "Comment",
        },
        fields=["reference_name", "content"],
        limit_page_length=5000,
    )
    for comment in comments:
        lines = {
            cstr(line).strip()
            for line in strip_html(cstr(comment.get("content"))).splitlines()
            if cstr(line).strip()
        }
        if STOCK_OPENING_SOURCE_MARKER in lines and marker in lines:
            return comment.get("reference_name")
    return None


def _invoice_remark(group: dict) -> str:
    return "\n".join([
        "Import Auto Opening Migration",
        f"Source File: {group.get('source')}",
        f"Source Invoice Key: {group.get('source_key')}",
        f"Source Rows: {', '.join(str(row) for row in group.get('source_rows') or [])}",
        cstr(group.get("remarks") or "").strip(),
    ]).strip()


def _get_or_create_customer(customer_name: str, tax_id: str | None = None) -> str:
    customer_name = _text(customer_name) or _("Khách hàng migration")
    tax_id = _text(tax_id)
    existing = _find_existing_party("Customer", label=customer_name, tax_id=tax_id)
    if existing:
        return existing

    customer = frappe.new_doc("Customer")
    customer.customer_name = customer_name
    customer.territory = _ensure_group_doc("Territory", "All Territories")
    if customer.meta.get_field("customer_type"):
        customer.customer_type = "Company"
    if tax_id and customer.meta.get_field("tax_id"):
        customer.tax_id = tax_id
    customer.flags.ignore_mandatory = True

    forced_name, matching_group = _resolve_customer_group_name_clash(customer_name)
    customer.customer_group = matching_group or _default_customer_group()
    if forced_name:
        customer.name = forced_name
        # set_new_name() wipes any pre-set doc.name back to None unless this
        # flag is set (see frappe/model/naming.py) — scope it tightly so we
        # don't change behaviour for anything else running in this request.
        previous_flag = frappe.flags.in_import
        frappe.flags.in_import = True
        try:
            customer.insert(ignore_permissions=True)
        finally:
            frappe.flags.in_import = previous_flag
    else:
        customer.insert(ignore_permissions=True)
    return customer.name


def _resolve_customer_group_name_clash(customer_name: str) -> tuple[str | None, str | None]:
    """Handle ERPNext's Customer.validate_name_with_customer_group(): it
    hard-throws ("A Customer Group exists with same name...") if a Customer
    Group happens to have the exact same name as the Customer being created.
    Returns ``(forced_docname, matching_customer_group)`` — both ``None`` if
    there's no clash.

    That check only ever fires when Selling Settings > Customer Naming By =
    "Customer Name" (docname == customer_name) — Naming Series/Auto Name
    modes never collide, since their docname is never the raw customer name.

    A same-name Customer Group isn't just an obstacle to dodge — it's real
    data: it almost certainly IS this customer's group in the source file, so
    ``matching_customer_group`` is returned for the caller to assign as
    ``customer.customer_group`` (unless it's a parent/group node, which
    ERPNext refuses to assign directly to a Customer — caller falls back to
    the site's default leaf group in that case). The Customer itself still
    needs a disambiguated docname to satisfy ERPNext's check; customer_name
    (what users actually see) is left untouched.
    """
    if frappe.defaults.get_global_default("cust_master_name") != "Customer Name":
        return None, None
    group = frappe.db.get_value("Customer Group", customer_name, ["name", "is_group"], as_dict=True)
    if not group:
        return None, None

    candidate = f"{customer_name} (KH)"
    suffix = 2
    while frappe.db.exists("Customer", candidate) or frappe.db.exists("Customer Group", candidate):
        candidate = f"{customer_name} (KH {suffix})"
        suffix += 1

    matching_group = group.name if not group.is_group else None
    return candidate, matching_group


def _get_or_create_supplier(supplier_name: str, tax_id: str | None = None) -> str:
    supplier_name = _text(supplier_name) or _("Nhà cung cấp migration")
    tax_id = _text(tax_id)
    existing = _find_existing_party("Supplier", label=supplier_name, tax_id=tax_id)
    if existing:
        return existing

    supplier = frappe.new_doc("Supplier")
    supplier.supplier_name = supplier_name
    supplier.supplier_group = _default_supplier_group()
    if supplier.meta.get_field("supplier_type"):
        supplier.supplier_type = "Company"
    if tax_id and supplier.meta.get_field("tax_id"):
        supplier.tax_id = tax_id
    supplier.flags.ignore_mandatory = True
    supplier.insert(ignore_permissions=True)
    return supplier.name


def _default_customer_group() -> str:
    """Return a leaf (non-group) Customer Group, creating one if the site has none.

    ERPNext rejects ``Customer.customer_group`` pointing at a group node ("Cannot
    select a Group type Customer Group..."). "All Customer Groups" is always
    ``is_group=1``, so it must never be assigned directly here.
    """
    for name in ("Commercial", "Khách hàng", "Retail", "Individual", "General"):
        row = frappe.db.get_value("Customer Group", {"customer_group_name": name, "is_group": 0}, "name")
        if row:
            return row

    row = frappe.db.get_value("Customer Group", {"is_group": 0}, "name")
    if row:
        return row

    doc = frappe.new_doc("Customer Group")
    doc.customer_group_name = "General"
    doc.parent_customer_group = _ensure_group_doc("Customer Group", "All Customer Groups")
    doc.is_group = 0
    doc.flags.ignore_mandatory = True
    doc.insert(ignore_permissions=True)
    return doc.name


def _default_supplier_group() -> str:
    """Return a leaf (non-group) Supplier Group, creating one if the site has none.

    Mirrors :func:`_default_customer_group` — "All Supplier Groups" is always
    ``is_group=1`` and must never be assigned to ``Supplier.supplier_group`` directly.
    """
    for name in ("Services", "Nhà cung cấp", "Raw Material", "Distributor", "Local", "General"):
        row = frappe.db.get_value("Supplier Group", {"supplier_group_name": name, "is_group": 0}, "name")
        if row:
            return row

    row = frappe.db.get_value("Supplier Group", {"is_group": 0}, "name")
    if row:
        return row

    doc = frappe.new_doc("Supplier Group")
    doc.supplier_group_name = "General"
    doc.parent_supplier_group = _ensure_group_doc("Supplier Group", "All Supplier Groups")
    doc.is_group = 0
    doc.flags.ignore_mandatory = True
    doc.insert(ignore_permissions=True)
    return doc.name


def _ensure_group_doc(doctype: str, label: str) -> str:
    if frappe.db.exists(doctype, label):
        return label

    label_field = {
        "Customer Group": "customer_group_name",
        "Supplier Group": "supplier_group_name",
        "Territory": "territory_name",
        "Item Group": "item_group_name",
    }.get(doctype)
    parent_field = {
        "Customer Group": "parent_customer_group",
        "Supplier Group": "parent_supplier_group",
        "Territory": "parent_territory",
        "Item Group": "parent_item_group",
    }.get(doctype)
    doc = frappe.new_doc(doctype)
    if label_field:
        setattr(doc, label_field, label)
    if doc.meta.get_field("is_group"):
        doc.is_group = 1
    if parent_field and label not in {
        "All Customer Groups",
        "All Supplier Groups",
        "All Territories",
        "All Item Groups",
    }:
        setattr(doc, parent_field, _ensure_group_doc(doctype, f"All {doctype}s"))
    doc.flags.ignore_mandatory = True
    doc.insert(ignore_permissions=True)
    return doc.name


def _ensure_uom(uom: str) -> str:
    uom = _text(uom) or "Nos"
    if frappe.db.exists("UOM", uom):
        return uom
    existing = frappe.db.get_value("UOM", {"uom_name": uom}, "name")
    if existing:
        return existing
    doc = frappe.new_doc("UOM")
    doc.uom_name = uom
    doc.insert(ignore_permissions=True)
    return doc.name


def _ensure_migration_service_item(company: str) -> str:
    item_code = "MIG-SERVICE"
    if frappe.db.exists("Item", item_code):
        return item_code
    item = frappe.new_doc("Item")
    item.item_code = item_code
    item.item_name = "Dịch vụ migration"
    item.item_group = _ensure_group_doc("Item Group", "All Item Groups")
    item.stock_uom = _ensure_uom("Nos")
    item.is_stock_item = 0
    income_account = _default_sales_income_account(company)
    expense_account = _default_purchase_expense_account(company)
    if item.meta.get_field("item_defaults"):
        default_row = {"company": company}
        if income_account:
            default_row["income_account"] = income_account
        if expense_account:
            default_row["expense_account"] = expense_account
        item.append("item_defaults", default_row)
    item.insert(ignore_permissions=True)
    return item.name


def _ensure_opening_stock_item(row: dict) -> tuple[str, bool, bool]:
    item_code = _text(row.get("item_code"))
    item_name = _text(row.get("item_name")) or item_code
    uom, uom_created = _ensure_uom_with_created(row.get("uom") or "Nos")
    if not item_code:
        frappe.throw(_("Thiếu mã hàng khi tạo tồn kho đầu kỳ."))

    if frappe.db.exists("Item", item_code):
        is_stock_item = frappe.db.get_value("Item", item_code, "is_stock_item")
        if not int(is_stock_item or 0):
            frappe.throw(_("Item {0} đang không phải stock item, không thể nhập tồn kho đầu kỳ.").format(item_code))
        return item_code, False, uom_created

    item = frappe.new_doc("Item")
    item.item_code = item_code
    item.item_name = _truncate_for_field("Item", "item_name", item_name)
    item.item_group = _ensure_opening_item_group(row.get("item_group_label"))
    item.stock_uom = uom
    item.is_stock_item = 1
    if item.meta.get_field("description") and item_name and item.item_name != item_name:
        item.description = item_name
    item.flags.ignore_mandatory = True
    item.insert(ignore_permissions=True, ignore_mandatory=True)
    return item.name, True, uom_created


def _ensure_opening_item_group(label: str | None) -> str:
    label = _text(label)
    if label:
        existing = frappe.db.get_value("Item Group", {"item_group_name": label}, "name")
        if existing:
            return existing

        parent = _ensure_group_doc("Item Group", "All Item Groups")
        doc = frappe.new_doc("Item Group")
        doc.item_group_name = label
        doc.parent_item_group = parent
        doc.is_group = 0
        doc.flags.ignore_mandatory = True
        doc.insert(ignore_permissions=True, ignore_mandatory=True)
        return doc.name

    return _ensure_group_doc("Item Group", "All Item Groups")


def _ensure_uom_with_created(uom: str | None) -> tuple[str, bool]:
    uom = _text(uom) or "Nos"
    if frappe.db.exists("UOM", uom):
        return uom, False
    existing = frappe.db.get_value("UOM", {"uom_name": uom}, "name")
    if existing:
        return existing, False
    doc = frappe.new_doc("UOM")
    doc.uom_name = uom
    doc.insert(ignore_permissions=True)
    return doc.name, True


def _ensure_opening_stock_warehouse(
    company: str,
    warehouse_label: str,
    stock_account: str | None = None,
) -> tuple[str, bool, bool]:
    warehouse_label = _text(warehouse_label)
    if not warehouse_label:
        frappe.throw(_("Thiếu kho khi tạo tồn kho đầu kỳ."))

    # Resolve bare account numbers (placeholders stored during analysis when COA wasn't imported yet)
    if stock_account and str(stock_account).strip().isdigit():
        resolved = _resolve_leaf_or_child_account_by_number(stock_account, company)
        stock_account = resolved or None  # use None if still not found → warehouse created without account

    warehouse = _find_opening_stock_warehouse(company, warehouse_label)
    if warehouse:
        current = frappe.db.get_value("Warehouse", warehouse, ["account", "is_group"], as_dict=True) or {}
        if int(current.get("is_group") or 0):
            frappe.throw(_("Warehouse {0} là group warehouse, không thể nhập tồn kho trực tiếp.").format(warehouse))
        if stock_account:
            current_account = _text(current.get("account"))
            if current_account and current_account != stock_account:
                frappe.throw(
                    _("Warehouse {0} đang gắn account {1}, khác tài khoản kho cần import {2}.").format(
                        warehouse,
                        current_account,
                        stock_account,
                    )
                )
            if not current_account:
                frappe.db.set_value("Warehouse", warehouse, "account", stock_account, update_modified=False)
                return warehouse, False, True
        return warehouse, False, False

    doc = frappe.new_doc("Warehouse")
    doc.warehouse_name = _truncate_for_field("Warehouse", "warehouse_name", warehouse_label)
    doc.company = company
    doc.is_group = 0
    doc.parent_warehouse = _ensure_opening_warehouse_root(company)
    if stock_account:
        doc.account = stock_account
    doc.flags.ignore_mandatory = True
    doc.insert(ignore_permissions=True, ignore_mandatory=True)
    return doc.name, True, False


def _find_opening_stock_warehouse(company: str, warehouse_label: str) -> str | None:
    warehouse_label = _text(warehouse_label)
    if not warehouse_label:
        return None

    abbr = frappe.db.get_value("Company", company, "abbr")
    candidates = [warehouse_label]
    if abbr and not warehouse_label.endswith(f" - {abbr}"):
        candidates.append(f"{warehouse_label} - {abbr}")
    for candidate in candidates:
        if frappe.db.exists("Warehouse", candidate):
            return candidate

    return frappe.db.get_value("Warehouse", {"company": company, "warehouse_name": warehouse_label}, "name")


def _ensure_opening_warehouse_root(company: str) -> str | None:
    existing = frappe.db.get_value(
        "Warehouse",
        {
            "company": company,
            "is_group": 1,
            "parent_warehouse": ["is", "not set"],
        },
        "name",
    )
    if existing:
        return existing

    doc = frappe.new_doc("Warehouse")
    doc.warehouse_name = "All Warehouses"
    doc.company = company
    doc.is_group = 1
    doc.flags.ignore_mandatory = True
    doc.insert(ignore_permissions=True, ignore_mandatory=True)
    return doc.name


def _truncate_for_field(doctype: str, fieldname: str, value: str | None) -> str:
    value = _text(value)
    length = _field_max_length(doctype, fieldname)
    if not length or len(value) <= length:
        return value
    digest = hashlib.sha1(value.encode("utf-8")).hexdigest()[:8].upper()
    suffix = f"-{digest}"
    return f"{value[: max(1, length - len(suffix))].rstrip(' -')}{suffix}"


def _field_max_length(doctype: str, fieldname: str) -> int:
    try:
        field = frappe.get_meta(doctype).get_field(fieldname)
        length = int(getattr(field, "length", 0) or 0)
    except Exception:
        length = 0
    if length:
        return length

    try:
        table_name = f"tab{doctype}"
        row = frappe.db.sql(
            """
            SELECT CHARACTER_MAXIMUM_LENGTH
            FROM information_schema.COLUMNS
            WHERE TABLE_SCHEMA = DATABASE()
              AND TABLE_NAME = %s
              AND COLUMN_NAME = %s
            LIMIT 1
            """,
            (table_name, fieldname),
            as_dict=True,
        )
        return int((row[0] or {}).get("CHARACTER_MAXIMUM_LENGTH") or 0) if row else 0
    except Exception:
        return 0


def _clean_error_message(exc: Exception, limit: int = 500) -> str:
    raw = " ".join(cstr(arg) for arg in (getattr(exc, "args", ()) or ())) or cstr(exc)
    text = html.unescape(strip_html(raw))
    text = re.sub(r"\s+", " ", text).strip()
    return text[:limit]


def _default_sales_income_account(company: str) -> str | None:
    return (
        _resolve_leaf_or_child_account_by_number("5113", company)
        or _resolve_leaf_or_child_account_by_number("5111", company)
        or _resolve_leaf_or_child_account_by_number("511", company)
        or frappe.db.get_value("Account", {"company": company, "account_type": "Income Account", "is_group": 0}, "name")
        or frappe.db.get_value("Account", {"company": company, "root_type": "Income", "is_group": 0}, "name")
    )


def _default_purchase_expense_account(company: str) -> str | None:
    return (
        _resolve_leaf_or_child_account_by_number("6427", company)
        or _resolve_leaf_or_child_account_by_number("642", company)
        or _resolve_leaf_or_child_account_by_number("641", company)
        or frappe.db.get_value("Account", {"company": company, "account_type": "Expense Account", "is_group": 0}, "name")
        or frappe.db.get_value("Account", {"company": company, "root_type": "Expense", "is_group": 0}, "name")
    )


def _ensure_coa_account_types(company: str) -> None:
    """Ensure key COA accounts have the correct account_type for invoice posting.

    ERPNext validates account_type on Sales Invoice (debit_to must be Receivable)
    and Purchase Invoice (credit_to must be Payable). This auto-corrects any
    accounts that were imported from COA CSV without account_type set.
    """
    # account_number → required account_type (per VN TT200 COA v2)
    required: dict[str, str] = {
        "111": "Cash", "1111": "Cash", "1112": "Cash", "1113": "Cash",
        "112": "Bank", "1121": "Bank", "1122": "Bank", "1123": "Bank",
        "113": "Bank", "1131": "Bank", "1132": "Bank",
        "131": "Receivable",
        "133": "Tax", "1331": "Tax", "1332": "Tax",
        "136": "Receivable", "1361": "Receivable", "1362": "Receivable",
        "1363": "Receivable", "1368": "Receivable",
        "138": "Receivable", "1381": "Receivable", "1385": "Receivable", "1388": "Receivable",
        "151": "Stock Received But Not Billed", "152": "Stock",
        "154": "Temporary", "155": "Stock", "1551": "Stock", "1557": "Stock",
        "156": "Stock", "1561": "Stock", "1562": "Expenses Included In Asset Valuation",
        "1565": "Stock",
        "214": "Accumulated Depreciation", "2141": "Accumulated Depreciation",
        "2142": "Accumulated Depreciation", "2143": "Accumulated Depreciation",
        "2147": "Accumulated Depreciation",
        "241": "Capital Work in Progress",
        "331": "Payable",
        "333": "Tax", "3331": "Tax", "33311": "Tax", "33312": "Tax",
        "3332": "Tax", "3333": "Tax", "3334": "Tax", "3335": "Tax",
        "3336": "Tax", "3337": "Tax", "3338": "Tax", "33381": "Tax", "33382": "Tax",
        "3339": "Tax",
        # 334/335/336 are payroll/accrual/inter-company accounts — NOT used as credit_to
        # in Purchase Invoices, so they must NOT be typed Payable (would block JE without party)
        "4119": "Round Off",
        "632": "Cost of Goods Sold", "6329": "Stock Adjustment",
    }
    account_numbers = list(required.keys())
    rows = frappe.get_all(
        "Account",
        filters={"company": company, "account_number": ["in", account_numbers]},
        fields=["name", "account_number", "account_type"],
    )
    fixed = 0
    for row in rows:
        expected = required.get(row.account_number)
        if expected and row.account_type != expected:
            frappe.db.set_value("Account", row.name, "account_type", expected, update_modified=False)
            fixed += 1
    if fixed:
        frappe.db.commit()


def _ensure_coa_balance_type(company: str) -> None:
    """Clear wrong balance_must_be constraints that block opening balance posting.

    ERPNext enforces balance_must_be='Debit' on some VN accounts that are
    Liability/Equity/Income (should have Credit balance) and 'Credit' on some
    Asset/Expense accounts (should have Debit balance). These block GL entries
    during opening balance import.
    """
    wrong_debit = frappe.db.sql(
        """
        SELECT name FROM `tabAccount`
        WHERE company = %s
          AND balance_must_be = 'Debit'
          AND root_type IN ('Liability', 'Equity', 'Income')
        """,
        company,
    )
    wrong_credit = frappe.db.sql(
        """
        SELECT name FROM `tabAccount`
        WHERE company = %s
          AND balance_must_be = 'Credit'
          AND root_type IN ('Asset', 'Expense')
        """,
        company,
    )
    fixed = 0
    for (name,) in list(wrong_debit) + list(wrong_credit):
        frappe.db.set_value("Account", name, "balance_must_be", "", update_modified=False)
        frappe.clear_document_cache("Account", name)
        fixed += 1
    if fixed:
        frappe.db.commit()


def _ensure_company_round_off_settings(company: str) -> str | None:
    """Ensure ERPNext can post rounded totals for migration invoices."""
    existing = frappe.db.get_value("Company", company, "round_off_account")
    if existing and _is_leaf_account(existing):
        return existing

    account = _round_off_account(company)
    if not account:
        return None

    updates = {"round_off_account": account}
    if frappe.get_meta("Company").get_field("round_off_cost_center"):
        cost_center = frappe.db.get_value("Company", company, "round_off_cost_center") or _default_cost_center(company)
        if cost_center:
            updates["round_off_cost_center"] = cost_center

    frappe.db.set_value("Company", company, updates, update_modified=False)
    return account


def _ensure_company_purchase_invoice_settings(company: str) -> None:
    """Fill Company defaults that Purchase Invoice validates in ERPNext."""
    company_meta = frappe.get_meta("Company")
    updates = {}

    if company_meta.get_field("stock_received_but_not_billed"):
        existing = frappe.db.get_value("Company", company, "stock_received_but_not_billed")
        if not _is_leaf_account(existing):
            account = _stock_received_but_not_billed_account(company)
            if account:
                updates["stock_received_but_not_billed"] = account

    if company_meta.get_field("default_inventory_account"):
        existing = frappe.db.get_value("Company", company, "default_inventory_account")
        if not _is_leaf_account(existing):
            account = _resolve_leaf_or_child_account_by_number("1561", company)
            if account:
                updates["default_inventory_account"] = account

    if company_meta.get_field("default_expense_account"):
        existing = frappe.db.get_value("Company", company, "default_expense_account")
        if not _is_leaf_account(existing):
            account = (
                _resolve_leaf_or_child_account_by_number("632", company)
                or _default_purchase_expense_account(company)
            )
            if account:
                updates["default_expense_account"] = account

    if company_meta.get_field("default_payable_account"):
        existing = frappe.db.get_value("Company", company, "default_payable_account")
        if not _is_leaf_account(existing):
            account = _resolve_leaf_or_child_account_by_number("331", company)
            if account:
                updates["default_payable_account"] = account

    if updates:
        frappe.db.set_value("Company", company, updates, update_modified=False)
        frappe.clear_document_cache("Company", company)


def _stock_received_but_not_billed_account(company: str) -> str | None:
    existing = frappe.db.get_value(
        "Account",
        {"company": company, "account_type": "Stock Received But Not Billed", "is_group": 0},
        "name",
    )
    if existing:
        return existing

    account_name = "Hàng nhận chưa có hóa đơn"
    existing = frappe.db.get_value(
        "Account",
        {"company": company, "account_name": account_name, "is_group": 0},
        "name",
    )
    if existing:
        return existing

    parent_account = _liability_parent_account(company)
    if not parent_account:
        return None

    account = frappe.new_doc("Account")
    account.account_name = account_name
    account.company = company
    account.parent_account = parent_account
    account.is_group = 0
    account.root_type = "Liability"
    account.report_type = "Balance Sheet"
    if account.meta.get_field("account_type"):
        account.account_type = "Stock Received But Not Billed"
    if account.meta.get_field("account_currency"):
        account.account_currency = frappe.db.get_value("Company", company, "default_currency") or "VND"
    account.insert(ignore_permissions=True, ignore_mandatory=True)
    return account.name


def _liability_parent_account(company: str) -> str | None:
    return (
        frappe.db.get_value(
            "Account",
            {
                "company": company,
                "account_name": "Nợ phải trả",
                "is_group": 1,
                "root_type": "Liability",
                "report_type": "Balance Sheet",
            },
            "name",
        )
        or frappe.db.get_value(
            "Account",
            {
                "company": company,
                "is_group": 1,
                "root_type": "Liability",
                "parent_account": ["is", "not set"],
            },
            "name",
        )
        or frappe.db.get_value(
            "Account",
            {"company": company, "is_group": 1, "root_type": "Liability"},
            "name",
        )
    )


def _round_off_account(company: str) -> str | None:
    existing = frappe.db.get_value(
        "Account",
        {"company": company, "account_type": "Round Off", "is_group": 0},
        "name",
    )
    if existing:
        return existing

    for account_number in ("635", "811", "6428"):
        account = _resolve_leaf_or_child_account_by_number(account_number, company)
        if account:
            return account

    parent_account = _round_off_parent_account(company)
    if not parent_account:
        return None

    account_name = "Làm tròn số"
    existing = frappe.db.get_value(
        "Account",
        {"company": company, "account_name": account_name, "is_group": 0},
        "name",
    )
    if existing:
        return existing

    account = frappe.new_doc("Account")
    account.account_name = account_name
    account.company = company
    account.parent_account = parent_account
    account.is_group = 0
    account.root_type = "Expense"
    account.report_type = "Profit and Loss"
    if account.meta.get_field("account_type"):
        account.account_type = "Round Off"
    if account.meta.get_field("account_currency"):
        account.account_currency = frappe.db.get_value("Company", company, "default_currency") or "VND"
    account.insert(ignore_permissions=True, ignore_mandatory=True)
    return account.name


def _round_off_parent_account(company: str) -> str | None:
    return (
        frappe.db.get_value(
            "Account",
            {
                "company": company,
                "account_name": "Chi phí",
                "is_group": 1,
                "root_type": "Expense",
                "report_type": "Profit and Loss",
            },
            "name",
        )
        or frappe.db.get_value(
            "Account",
            {
                "company": company,
                "is_group": 1,
                "root_type": "Expense",
                "parent_account": ["is", "not set"],
            },
            "name",
        )
        or frappe.db.get_value(
            "Account",
            {"company": company, "is_group": 1, "root_type": "Expense"},
            "name",
        )
    )


def _is_leaf_account(account: str | None) -> bool:
    account = _text(account)
    if not account:
        return False
    try:
        return not bool(frappe.db.get_value("Account", account, "is_group"))
    except Exception:
        return False


def _stock_opening_adjustment_account(company: str) -> str | None:
    return _ensure_temporary_opening_account(company)


def _ensure_temporary_opening_account(company: str) -> str | None:
    """Return a Balance Sheet account usable for opening stock offsets.

    ERPNext blocks Profit and Loss accounts in Opening Journal Entries and also
    expects opening stock difference accounts to be Balance Sheet accounts
    (commonly named "Temporary Opening"). Create it deterministically when the
    imported COA does not provide one.
    """
    for account_name in (
        "Temporary Opening",
        "Tài khoản tạm nhập số dư đầu kỳ",
        "Chênh lệch nhập số dư đầu kỳ",
    ):
        existing = frappe.db.get_value(
            "Account",
            {
                "company": company,
                "account_name": account_name,
                "is_group": 0,
                "report_type": "Balance Sheet",
            },
            "name",
        )
        if existing:
            return existing

    parent_account = _temporary_opening_parent_account(company)
    if not parent_account:
        return None

    account = frappe.new_doc("Account")
    account.account_name = "Temporary Opening"
    account.company = company
    account.parent_account = parent_account
    account.is_group = 0
    account.root_type = "Equity"
    account.report_type = "Balance Sheet"
    if account.meta.get_field("account_currency"):
        account.account_currency = frappe.db.get_value("Company", company, "default_currency") or "VND"
    account.insert(ignore_permissions=True, ignore_mandatory=True)
    return account.name


def _temporary_opening_parent_account(company: str) -> str | None:
    return (
        frappe.db.get_value(
            "Account",
            {
                "company": company,
                "account_name": "Vốn chủ sở hữu",
                "is_group": 1,
                "root_type": "Equity",
                "report_type": "Balance Sheet",
            },
            "name",
        )
        or frappe.db.get_value(
            "Account",
            {
                "company": company,
                "is_group": 1,
                "root_type": "Equity",
                "parent_account": ["is", "not set"],
            },
            "name",
        )
        or frappe.db.get_value(
            "Account",
            {
                "company": company,
                "is_group": 1,
                "root_type": "Equity",
            },
            "name",
        )
    )


def _first_leaf_account(company: str, extra_filters: dict) -> str | None:
    filters = {"company": company, "is_group": 0}
    filters.update(extra_filters or {})
    rows = frappe.get_all(
        "Account",
        filters=filters,
        fields=["name"],
        order_by="account_number asc, name asc",
        limit_page_length=1,
    )
    return rows[0].get("name") if rows else None


def _first_leaf_account_by_number_prefix(prefix: str, company: str) -> str | None:
    prefix = _text(prefix)
    if not prefix:
        return None
    return _first_leaf_account(company, {"account_number": ["like", f"{prefix}%"]})


def _resolve_leaf_account_by_number(account_number: str | None, company: str) -> str | None:
    account_number = _text(account_number)
    if not account_number:
        return None
    return frappe.db.get_value(
        "Account",
        {"company": company, "account_number": account_number, "is_group": 0},
        "name",
    )


def _resolve_leaf_or_child_account_by_number(account_number: str | None, company: str) -> str | None:
    """Return a posting account for an account number.

    Invoice rows cannot use group accounts. VN COA mappings often point to a
    parent such as 5113/642/3331, so resolve the exact leaf first and otherwise
    use the first child leaf under that number.
    """
    account_number = _text(account_number)
    if not account_number:
        return None
    return (
        _resolve_leaf_account_by_number(account_number, company)
        or _first_leaf_account_by_number_prefix(account_number, company)
    )


def _resolve_account_by_number(account_number: str | None, company: str) -> str | None:
    account_number = _text(account_number)
    if not account_number:
        return None
    return frappe.db.get_value("Account", {"company": company, "account_number": account_number}, "name")


def _default_cost_center(company: str) -> str | None:
    company_meta = frappe.get_meta("Company")
    if company_meta.get_field("cost_center"):
        cost_center = frappe.db.get_value("Company", company, "cost_center")
        if cost_center:
            return cost_center
    return frappe.db.get_value("Cost Center", {"company": company, "is_group": 0}, "name")


def _resolve_account(account_number: str, company: str) -> str | None:
    account_number = _text(account_number)
    if not account_number:
        return None
    try:
        return frappe.db.get_value("Account", {"account_number": account_number, "company": company}, "name")
    except Exception:
        return None


def _is_stock_account(account: str | None) -> bool:
    account = _text(account)
    if not account:
        return False
    try:
        return frappe.db.get_value("Account", account, "account_type") == "Stock"
    except Exception:
        return False


def _find_primary_leaf_account(account_name: str, company: str) -> str | None:
    """For a group account, find the best leaf descendant.

    In Vietnamese COA (TT200), primary sub-accounts follow the convention that
    the first child ends with "1" (e.g., 111 → 1111 VND, 333 → 3331 VAT payable).
    We walk down the tree, preferring the child whose number = parent + "1".

    Returns the leaf account name, or None if the tree has no leaves at all.
    """
    is_group = frappe.db.get_value("Account", account_name, "is_group")
    if not is_group:
        return account_name

    group_number = frappe.db.get_value("Account", account_name, "account_number") or ""
    children = frappe.get_all(
        "Account",
        filters={"parent_account": account_name, "company": company},
        fields=["name", "account_number", "is_group"],
        order_by="account_number asc",
    )
    if not children:
        return None

    leaf_children = [c for c in children if not c["is_group"]]
    if leaf_children:
        # Prefer child whose account_number = parent_number + "1" (VN convention)
        primary = next((c for c in leaf_children if (c["account_number"] or "") == group_number + "1"), None)
        return (primary or leaf_children[0])["name"]

    # No direct leaf children — recurse into the first group child
    group_children = [c for c in children if c["is_group"]]
    for child in group_children:
        result = _find_primary_leaf_account(child["name"], company)
        if result:
            return result
    return None


def _resolve_party(party_type: str, code: str, label: str | None = None, company: str | None = None) -> str | None:
    code = _text(code)
    if not code:
        return None
    if party_type in OPENING_PARTY_BUCKETS:
        return _find_existing_party(
            party_type,
            code=code,
            label=label,
            company=company,
            allow_label_fallback=True,
        )
    if _get_existing_by_field_exact(party_type, "name", code):
        return code

    meta = frappe.get_meta(party_type)
    candidates = []
    if party_type == "Customer":
        candidates.extend([("customer_code", code), ("customer_name", label)])
    elif party_type == "Supplier":
        candidates.extend([("supplier_code", code), ("supplier_name", label)])
    elif party_type == "Employee":
        candidates.extend([("employee_number", code), ("employee_name", label)])

    for fieldname, value in candidates:
        value = _text(value)
        if not value or not meta.get_field(fieldname):
            continue
        found = frappe.db.get_value(party_type, {fieldname: value}, "name")
        if found:
            return found
    return None


def _resolve_bank_account(bank_account_no: str, company: str) -> str | None:
    bank_account_no = _bank_account_no(bank_account_no)
    if not bank_account_no:
        return None
    filters = {"bank_account_no": bank_account_no}
    if frappe.get_meta("Bank Account").get_field("company"):
        filters["company"] = company
    return frappe.db.get_value("Bank Account", filters, "name") or frappe.db.get_value(
        "Bank Account", {"bank_account_no": bank_account_no}, "name"
    )


def _existing_opening_entries(company: str) -> list[dict]:
    rows = frappe.get_all(
        "Journal Entry",
        filters={
            "company": company,
            "voucher_type": "Opening Entry",
        },
        fields=["name", "posting_date", "docstatus", "total_debit", "total_credit", "user_remark"],
        order_by="creation desc",
        limit_page_length=100,
    )
    return [
        {
            "name": row.get("name"),
            "posting_date": row.get("posting_date"),
            "docstatus": row.get("docstatus"),
            "total_debit": row.get("total_debit"),
            "total_credit": row.get("total_credit"),
        }
        for row in rows
        if cstr(row.get("user_remark")).strip().startswith("Import Auto Opening Balance")
    ][:20]


def _mark_opening_balance_summary(import_doc, journal_entry: str, plan: dict, posting_date: str, submitted: bool) -> None:
    summary = {}
    if getattr(import_doc, "summary_json", None):
        try:
            summary = frappe.parse_json(import_doc.summary_json)
        except Exception:
            summary = {}
    if not isinstance(summary, dict):
        summary = {}
    summary["opening_balance_import"] = {
        "journal_entry": journal_entry,
        "posting_date": posting_date,
        "submitted": bool(submitted),
        "rows": plan["row_count"],
        "total_debit": plan["total_debit"],
        "total_credit": plan["total_credit"],
        "created_on": now_datetime(),
    }
    import_doc.summary_json = frappe.as_json(summary, indent=2)
    if hasattr(import_doc, "files"):
        _update_parent_status(import_doc)
    else:
        import_doc.status = "Completed"
    import_doc.save(ignore_permissions=True)


def _mark_ai_journal_summary(import_doc, result: dict) -> None:
    summary = {}
    if getattr(import_doc, "summary_json", None):
        try:
            summary = frappe.parse_json(import_doc.summary_json)
        except Exception:
            summary = {}
    if not isinstance(summary, dict):
        summary = {}

    imported = summary.setdefault("imported", {})
    imported["ai_journal"] = {
        "created": result.get("created") or 0,
        "skipped": result.get("skipped") or 0,
        "failed": result.get("failed") or 0,
        "journal_entries": result.get("journal_entries") or [],
        "updated_on": now_datetime(),
    }
    imported["total_created"] = sum(
        int(value.get("created") or 0)
        for key, value in imported.items()
        if isinstance(value, dict)
    )
    import_doc.status = "Partial" if result.get("failed") else "Completed"
    import_doc.summary_json = frappe.as_json(summary, indent=2)
    import_doc.save(ignore_permissions=True)


def _mark_invoice_import_summary(import_doc, invoice_type: str, result: dict) -> None:
    summary = {}
    if getattr(import_doc, "summary_json", None):
        try:
            summary = frappe.parse_json(import_doc.summary_json)
        except Exception:
            summary = {}
    if not isinstance(summary, dict):
        summary = {}

    imported = summary.setdefault("imported", {})
    imported[invoice_type] = {
        "created": result.get("created") or 0,
        "skipped": result.get("skipped") or 0,
        "failed": result.get("failed") or 0,
        "created_names": result.get("created_names") or [],
        "updated_on": now_datetime(),
    }
    imported["total_created"] = sum(
        int(value.get("created") or 0)
        for key, value in imported.items()
        if isinstance(value, dict)
    )
    import_doc.status = "Partial" if result.get("failed") else "Completed"
    import_doc.summary_json = frappe.as_json(summary, indent=2)
    import_doc.save(ignore_permissions=True)


def _mark_opening_stock_summary(import_doc, result: dict) -> None:
    summary = {}
    if getattr(import_doc, "summary_json", None):
        try:
            summary = frappe.parse_json(import_doc.summary_json)
        except Exception:
            summary = {}
    if not isinstance(summary, dict):
        summary = {}

    imported = summary.setdefault("imported", {})
    imported["opening_stock"] = {
        "stock_reconciliation": result.get("stock_reconciliation"),
        "created": 1 if result.get("stock_reconciliation") else 0,
        "rows": result.get("rows") or 0,
        "source_rows": result.get("source_rows") or 0,
        "total_qty": result.get("total_qty") or 0,
        "total_value": result.get("total_value") or 0,
        "account_balance_stock_value": result.get("account_balance_stock_value") or 0,
        "balance_difference": result.get("balance_difference") or 0,
        "submitted": bool(result.get("submitted")),
        "created_items": result.get("created_items") or 0,
        "created_warehouses": result.get("created_warehouses") or 0,
        "updated_warehouses": result.get("updated_warehouses") or 0,
        "updated_on": now_datetime(),
    }
    imported["total_created"] = sum(
        int(value.get("created") or 0)
        for value in imported.values()
        if isinstance(value, dict)
    )
    import_doc.status = "Completed"
    import_doc.summary_json = frappe.as_json(summary, indent=2)
    import_doc.save(ignore_permissions=True)


def _mark_opening_master_summary(import_doc, result: dict, refreshed_plan: dict) -> None:
    summary = {}
    if getattr(import_doc, "summary_json", None):
        try:
            summary = frappe.parse_json(import_doc.summary_json)
        except Exception:
            summary = {}
    if not isinstance(summary, dict):
        summary = {}

    summary["opening_master_data"] = {
        "created": result.get("created") or 0,
        "existing": result.get("existing") or 0,
        "skipped": result.get("skipped") or 0,
        "failed": result.get("failed") or 0,
        "customers_created": (result.get("customers") or {}).get("created") or 0,
        "suppliers_created": (result.get("suppliers") or {}).get("created") or 0,
        "employees_created": (result.get("employees") or {}).get("created") or 0,
        "updated_on": now_datetime(),
    }

    analysis = {}
    if getattr(import_doc, "analysis_json", None):
        try:
            analysis = frappe.parse_json(import_doc.analysis_json)
        except Exception:
            analysis = {}
    if not isinstance(analysis, dict):
        analysis = {}
    analysis["master_plan"] = refreshed_plan
    analysis["auto_master"] = refreshed_plan

    if result.get("failed"):
        import_doc.status = "Partial"
    elif getattr(import_doc, "status", None) in {None, "", "Draft"}:
        import_doc.status = "Analyzed"
    import_doc.summary_json = frappe.as_json(summary, indent=2)
    import_doc.analysis_json = frappe.as_json(analysis, indent=2)
    import_doc.save(ignore_permissions=True)


def _opening_remark(import_doc, posting_date: str) -> str:
    label = cstr(getattr(import_doc, "display_name", "") or getattr(import_doc, "name", "")).strip()
    return f"Import Auto Opening Balance - {label} - {posting_date}"


def _row_remark(row: dict) -> str:
    parts = [
        row.get("source"),
        f"row {row.get('source_row')}" if row.get("source_row") else "",
        row.get("account_number"),
        row.get("party_code") or row.get("bank_account_no") or row.get("label"),
    ]
    return " | ".join(cstr(part).strip() for part in parts if cstr(part).strip())


_TOTAL_PHRASES = {"tong", "cong", "tong cong", "tongcong", "tong cong cac loai", "total", "subtotal", "grand total"}

def _is_total_row(row: dict) -> bool:
    for value in row.values():
        folded = _fold_key(value).strip()
        if folded in _TOTAL_PHRASES:
            return True
    return False


def _text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return cstr(value).strip()


def _bank_account_no(value: Any) -> str:
    return _text(value).replace(" ", "").replace(".", "").replace("-", "")


def _expand_with_parents(account_numbers: set[str]) -> set[str]:
    """Expand a set of account numbers to also include all ancestor codes.

    When detail files (bank, customer…) use sub-accounts like "1121.20" or
    "11215", their aggregate parent "112" (present in account_balance) must
    also be treated as overridden — otherwise account_balance rows for the
    parent get double-counted alongside the detailed sub-account rows.

    Ancestry is inferred by trimming one digit at a time down to 3-digit roots
    (the minimum meaningful VN account level), and by stripping dot-notation
    suffixes first (e.g. "1121.20" → base "1121").
    """
    expanded = set(account_numbers)
    for num in account_numbers:
        base = num.split(".")[0] if "." in num else num
        while len(base) > 3:
            base = base[:-1]
            expanded.add(base)
    return expanded


def _col(row: dict, *candidates: str):
    """Case-insensitive column lookup, tries multiple candidate names in order."""
    lowered = {(k or "").strip().lower(): v for k, v in row.items()}
    for name in candidates:
        val = lowered.get(name.strip().lower())
        if val is not None and val != "":
            return val
    return None


def _amount(value: Any) -> float:
    if value in (None, ""):
        return 0.0
    if isinstance(value, str):
        value = value.replace(",", "").strip()
    return flt(value)


def _date(value: Any, fallback: str | date | None = None) -> date:
    if value in (None, ""):
        return getdate(fallback or "2026-01-01")
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    if isinstance(value, (int, float)):
        return date(1899, 12, 30) + timedelta(days=int(value))
    text = _text(value)
    if text.replace(".", "", 1).isdigit():
        return date(1899, 12, 30) + timedelta(days=int(flt(text)))
    return getdate(text)


def _fold_key(value: Any) -> str:
    text = normalize_key(value)
    text = unicodedata.normalize("NFD", text)
    text = "".join(char for char in text if unicodedata.category(char) != "Mn")
    return text.replace("đ", "d").replace("Đ", "D")


def _file_based_kpis(file_map: dict[str, str], invoices: dict) -> dict:
    """Compute KPI summary from the Excel files being imported (not from ERPNext GL).

    - revenue: grand_total from sales invoice file
    - expenses: grand_total from purchase invoice file
    - ar: net (Dư Nợ - Dư Có) per customer, sum positive only
    - ap: net (Dư Có - Dư Nợ) per supplier, sum positive only
    """
    try:
        si = invoices.get("sales_invoice") or {}
        pi = invoices.get("purchase_invoice") or {}
        revenue = float(si.get("grand_total") or 0)
        expenses = float(pi.get("grand_total") or 0)
        ar = _sum_party_balance(file_map, "customer_balance", "debit")
        ap = _sum_party_balance(file_map, "supplier_balance", "credit")
        return {"revenue": revenue, "expenses": expenses, "ar": ar, "ap": ap}
    except Exception:
        frappe.log_error(frappe.get_traceback(), "Opening Preview File KPI Failed")
        return {"revenue": 0.0, "expenses": 0.0, "ar": 0.0, "ap": 0.0}


def _sum_party_balance(file_map: dict[str, str], key: str, side: str) -> float:
    """Sum net party balance from a file.

    For AR (side='debit'):  net = Dư Nợ - Dư Có per party, sum only positive net.
    For AP (side='credit'): net = Dư Có - Dư Nợ per party, sum only positive net.
    Mirrors the GL result after _split_two_sided_row + JE is posted.
    """
    try:
        total = 0.0
        for row in _records(file_map, key):
            if _is_total_row(row):
                continue
            dr = _amount(_col(row, "Dư Nợ", "Dư nợ", "Dư nọ", "Số dư nợ"))
            cr = _amount(_col(row, "Dư Có", "Dư có", "Số dư có"))
            net = (dr - cr) if side == "debit" else (cr - dr)
            if net > 0:
                total += net
        return round(total, 2)
    except Exception:
        return 0.0
