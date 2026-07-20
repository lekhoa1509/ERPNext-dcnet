"""AI-driven smart import planner.

Some Excel files cannot be mapped to a single ERPNext DocType (e.g. bank
opening balances need Bank + Bank Account + Opening Journal Entry).  Instead
of forcing the user to split files manually, this module asks the AI to
produce an ordered multi-step script plan.  Each source-backed step contains:

- ``records``: up to 10 preview records generated from a random sample, and
- ``row_template``: a transformation template that the Python backend applies
  to every source row during execution.

The output is intentionally explicit so the UI can render a preview (tree
or table) for each step before the user approves the import. AI never receives
or imports the full data set.
"""

from __future__ import annotations

import hashlib
import json
import re
import unicodedata
from typing import Any

import frappe
from frappe import _
from frappe.utils import flt

from dcnet_migrate.import_auto.services.ai_client import (
    _chat_completion,
    _get_ai_config,
    _parse_json_response,
)
from dcnet_migrate.import_auto.services.doctype_metadata import get_default_values
from dcnet_migrate.import_auto.services.excel import (
    AI_SAMPLE_ROWS,
    extract_records,
    sample_records as sample_excel_records,
    summarize_workbook,
)
from dcnet_migrate.import_auto.services.utils import GROUP_LINK_CONFIG, normalize_key, truncate_text


HIERARCHICAL_DOCTYPES = {
    "Account": "parent_account",
    "Item Group": "parent_item_group",
    "Cost Center": "parent_cost_center",
    "Department": "parent_department",
    "Warehouse": "parent_warehouse",
    "Territory": "parent_territory",
    "Customer Group": "parent_customer_group",
    "Supplier Group": "parent_supplier_group",
}

ADDRESS_LINK_CONFIG = {
    "Customer": {
        "title_field": "customer_name",
        "name_fields": ("name", "customer_name"),
        "address_fields": ("address_line1", "customer_details", "address", "primary_address"),
    },
    "Supplier": {
        "title_field": "supplier_name",
        "name_fields": ("name", "supplier_name"),
        "address_fields": ("address_line1", "supplier_details", "address", "primary_address"),
    },
}

CONTACT_LINK_CONFIG = ADDRESS_LINK_CONFIG

MAX_PLAN_RECORDS_PER_STEP = 5000
SAMPLE_ROWS_FOR_AI = AI_SAMPLE_ROWS
SMART_PREVIEW_RECORD_LIMIT = 10
SMART_PLAN_TIMEOUT_FLOOR = 300  # 5 minutes minimum for smart plans

# Fields the AI is allowed to fill/overwrite when fixing a failed plan.
# Anything outside this whitelist is considered "important data" of the source
# file and must NOT be touched (account_number, account_name, amounts, etc.).
SMART_FIX_ALLOWED_FIELDS = {
    "parent_account",
    "parent_item_group",
    "parent_cost_center",
    "parent_department",
    "parent_warehouse",
    "parent_territory",
    "parent_customer_group",
    "parent_supplier_group",
    "is_group",
    "root_type",
    "report_type",
    "account_currency",
    "asset_category",
    "company",
    "cost_center",
    "disabled",
    "location",
    "stock_uom",
    "item_group",
    "is_stock_item",
    "is_purchase_item",
    "is_sales_item",
    "customer_group",
    "supplier_group",
    "territory",
}

# Fields the AI MUST NEVER modify when fixing — source of truth from Excel.
SMART_FIX_PROTECTED_FIELDS = {
    "account_number",
    "account_name",
    "item_code",
    "item_name",
    "customer_name",
    "supplier_name",
    "bank_name",
    "opening_balance",
    "balance",
    "debit",
    "credit",
    "amount",
    "qty",
    "rate",
    "voucher_no",
    "voucher_type",
}

TEXT_CODE_FIELDS = {
    "account_number",
    "item_code",
    "customer",
    "customer_name",
    "supplier",
    "supplier_name",
    "voucher_no",
    "voucher_type",
    "bank_account",
    "bank_account_no",
    "parent_account",
}

SMART_FIX_MAX_SAMPLE_RECORDS = AI_SAMPLE_ROWS
SMART_FIX_TIMEOUT_FLOOR = 240

# DocTypes whose missing master data the AI is allowed to PROPOSE inserting
# when fixing a failed import. The user must still confirm in the UI before
# anything is actually written. Transactional DocTypes (Sales Invoice, Stock
# Entry, Journal Entry, Payment Entry, ...) are intentionally NOT here — they
# must never be auto-created.
SMART_FIX_DEPENDENCY_ALLOWED_DOCTYPES = {
    # HR
    "Department", "Designation", "Employee Grade", "Branch",
    "Employment Type", "Holiday List", "Shift Type", "Leave Type",
    # Selling / Buying
    "Customer Group", "Supplier Group", "Territory", "Sales Person",
    # Items
    "Item Group", "Brand", "UOM", "Item Attribute",
    # Stock
    "Warehouse",
    # Assets / CCDC opening balances
    "Asset Category", "Location",
    # Accounting
    "Cost Center", "Account", "Mode of Payment", "Currency",
    # Projects
    "Project", "Project Type",
    # Generic
    "Country",
}

# Max records the AI can suggest creating per single dependency step.
# Anything beyond this is almost certainly a misclassification.
SMART_FIX_MAX_DEPENDENCY_RECORDS = 200

ANALYSIS_EXPAND_DOCTYPES = {
    "Bank",
    "Bank Account",
    "Customer",
    "Department",
    "Item",
    "Item Group",
    "Project",
    "Supplier",
    "UOM",
    "Warehouse",
}

ITEM_MASTER_VALUE_FIELDS = {
    "opening_stock",
    "standard_rate",
    "valuation_rate",
    "last_purchase_rate",
}

ITEM_TEXT_FIELD_MAX_LENGTHS = {
    "item_code": 140,
    "item_name": 140,
}





def _append_item_description_note(record: dict, note: str) -> None:
    note = frappe.as_unicode(note or "").strip()
    if not note:
        return

    description = frappe.as_unicode(record.get("description") or "").strip()
    if note in description:
        return
    record["description"] = f"{note}\n\n{description}" if description else note


def _normalise_item_code(record: dict) -> None:
    original_code = frappe.as_unicode(record.get("item_code") or "").strip()
    if not original_code:
        return

    item_code = original_code
    item_code = item_code.replace("->", "-to-").replace("<-", "-from-")
    item_code = item_code.replace(">", "-").replace("<", "-")
    item_code = re.sub(r"\s+", " ", item_code).strip(" -")
    item_code = re.sub(r"-{2,}", "-", item_code)

    if not item_code:
        digest = hashlib.sha1(original_code.encode("utf-8")).hexdigest()[:8]
        item_code = f"ITEM-{digest}"

    max_length = ITEM_TEXT_FIELD_MAX_LENGTHS["item_code"]
    if len(item_code) > max_length:
        digest = hashlib.sha1(item_code.encode("utf-8")).hexdigest()[:8]
        item_code = f"{item_code[: max_length - 9].rstrip(' -')}-{digest}"

    record["item_code"] = item_code
    if item_code != original_code:
        _append_item_description_note(record, f"Mã nguồn: {original_code}")


def _normalise_item_master_record(record: dict) -> bool:
    """Keep Item master records valid for ERPNext's controller constraints."""
    for fieldname in ITEM_MASTER_VALUE_FIELDS:
        record.pop(fieldname, None)

    _normalise_item_code(record)

    if not record.get("item_name") and record.get("item_code"):
        record["item_name"] = frappe.as_unicode(record.get("item_code")).strip()

    item_name = frappe.as_unicode(record.get("item_name") or "").strip()
    max_length = ITEM_TEXT_FIELD_MAX_LENGTHS["item_name"]
    if len(item_name) > max_length:
        full_item_name = item_name
        record["item_name"] = full_item_name[:max_length].rstrip()

        _append_item_description_note(record, full_item_name)
    elif item_name:
        record["item_name"] = item_name

    return bool(record.get("item_code") and record.get("item_name"))


def _is_coa_file(file_row, analysis: dict, headers: list[str]) -> bool:
    """Detect whether the smart plan is for a Chart of Accounts file.

    Triggers when:
    - analysis already mapped it to ``Account``, OR
    - filename contains the Vietnamese phrase ``tai_khoan`` / ``he_thong_tai_khoan``, OR
    - headers contain both ``account_number`` and ``parent_account``.
    """
    if (analysis or {}).get("target_doctype") == "Account":
        return True

    name_key = normalize_key(getattr(file_row, "file_name", "") or "").replace(" ", "_")
    if "he_thong_tai_khoan" in name_key or "chart_of_accounts" in name_key:
        return True

    header_keys = {normalize_key(h).replace(" ", "_") for h in (headers or [])}
    if "account_number" in header_keys and "parent_account" in header_keys:
        return True

    return False


def _company_coa_context(company_name: str | None) -> dict | None:
    """Provide AI with concrete COA context for the target Company:
    - company abbr (needed to suffix parent_account)
    - which root accounts already exist
    """
    if not company_name or not frappe.db.exists("Company", company_name):
        return None

    abbr = frappe.db.get_value("Company", company_name, "abbr") or ""

    existing_roots = frappe.get_all(
        "Account",
        filters={"company": company_name, "parent_account": ["in", ["", None]]},
        fields=["name", "account_name", "root_type", "report_type", "is_group"],
    )

    return {
        "company_name": company_name,
        "company_abbr": abbr,
        "existing_root_accounts": existing_roots,
        "expected_vn_root_account_names": [
            {"account_name": "Tài sản", "root_type": "Asset", "report_type": "Balance Sheet"},
            {"account_name": "Nợ phải trả", "root_type": "Liability", "report_type": "Balance Sheet"},
            {"account_name": "Vốn chủ sở hữu", "root_type": "Equity", "report_type": "Balance Sheet"},
            {"account_name": "Thu nhập", "root_type": "Income", "report_type": "Profit and Loss"},
            {"account_name": "Chi phí", "root_type": "Expense", "report_type": "Profit and Loss"},
        ],
    }


COA_SYSTEM_PROMPT_ADDON = (
    "\n\n=== CHART OF ACCOUNTS SPECIAL RULES ===\n"
    "This file is the company's Chart of Accounts (Hệ thống tài khoản TT200). "
    "You MUST follow these ERPNext-specific rules:\n"
    "1. EVERY non-root row must produce ONE Account record with fields: "
    "account_name, account_number, parent_account, is_group, root_type, report_type, "
    "account_type (if available), balance_must_be (if available), company, disabled.\n"
    "2. CRITICAL — parent_account format: ERPNext appends ' - {company_abbr}' to every account name. "
    "Look up company_abbr from the provided coa_context. "
    "Excel column 'parent_account' may be either:\n"
    "   (a) a Vietnamese root name like 'Tài sản', 'Nợ phải trả', 'Vốn chủ sở hữu', 'Thu nhập', 'Chi phí' "
    "       → output parent_account = '{vn_root} - {company_abbr}'.\n"
    "   (b) a numbered parent like '111 - Tiền mặt' "
    "       → output parent_account = '{value_from_excel} - {company_abbr}'.\n"
    "3. CRITICAL — order of records: this is a hierarchical tree. Sort records so EACH parent "
    "appears before its children in the records list (topological order). "
    "If a child references parent_account='1121' and account_number='1121' exists anywhere "
    "in the same Excel file, that parent is NOT missing master data; do not create a separate "
    "dependency for it. Keep the parent row in the Account import and sort it before children. "
    "Return a row_template AND set step.preview_format='tree' "
    "with parent_field='parent_account' and label_field='account_name'; the Python backend will "
    "sort topologically after materialising all rows. Still emit the topological-sort instruction "
    "explicitly in plan_summary so the user knows.\n"
    "4. CRITICAL — root accounts: if the source has top-level rows whose parent is a "
    "Vietnamese root name (Tài sản / Nợ phải trả / ...), and that root is NOT in "
    "coa_context.existing_root_accounts, you MUST emit a PRECEDING step that inserts the "
    "missing roots first. Each root record: "
    "{account_name: 'Tài sản', is_group: 1, root_type: 'Asset', report_type: 'Balance Sheet', "
    "company: <company_name>, parent_account: ''}. Use coa_context.expected_vn_root_account_names "
    "to know the right root_type/report_type for each VN root.\n"
    "5. is_group: copy from Excel (1 for parent/group, 0 for leaf).\n"
    "6. Map balance_must_be: 'Dư Nợ' → 'Debit', 'Dư Có' → 'Credit', otherwise empty.\n"
    "7. Map disabled: 'Ngừng sử dụng' → 1, 'Đang sử dụng' → 0.\n"
    "8. account_type values must be one of ERPNext's allowed values "
    "(Bank, Cash, Receivable, Payable, Tax, Stock, Fixed Asset, Accumulated Depreciation, "
    "Expense Account, Income Account, Temporary, ...). If Excel value is empty or unknown, leave it empty.\n"
    "9. Set company=<company_name> for every Account record.\n"
    "10. unique_key for Account step should be 'account_number' (since names collide).\n"
    "11. ignore_duplicates=true so re-running the plan is safe.\n"
    "=== END CHART OF ACCOUNTS RULES ===\n"
)

def build_smart_plan(doc, file_row, user_feedback: str | None = None) -> dict:
    """Ask the AI to produce mapping/script steps from a small random sample."""
    sample_seed = _sample_seed(file_row)
    summary = summarize_workbook(
        file_row.file_path,
        max_sample_rows=SAMPLE_ROWS_FOR_AI,
        sample_strategy="random",
        sample_seed=sample_seed,
    )

    analysis: dict[str, Any] = {}
    if file_row.analysis_json:
        try:
            analysis = json.loads(file_row.analysis_json)
        except Exception:
            analysis = {}

    sampled_records: list[dict] = []
    sheet_name = analysis.get("sheet_name") or _first_sheet_name(summary)
    header_row = analysis.get("header_row_number") or _first_header_row(summary)
    try:
        if sheet_name and header_row:
            sampled_records = sample_excel_records(
                file_row.file_path,
                sheet_name,
                header_row,
                sample_size=SAMPLE_ROWS_FOR_AI,
                seed=sample_seed,
            )
    except Exception:
        frappe.log_error(frappe.get_traceback(), "Smart Planner Sample Failed")

    config = _get_ai_config(doc)
    if not config.api_key or not config.enabled:
        return {"error": "Chưa cấu hình AI hoặc API key trống."}

    total_source_records = _source_row_count(summary, sheet_name, header_row)
    has_many_rows = total_source_records > SAMPLE_ROWS_FOR_AI

    headers = _first_headers(summary)
    is_coa = _is_coa_file(file_row, analysis, headers)
    coa_context = _company_coa_context(doc.company) if is_coa else None

    system_prompt = _build_system_prompt(has_many_rows, bool(user_feedback))
    if is_coa:
        system_prompt += COA_SYSTEM_PROMPT_ADDON

    user_payload = {
        "company": doc.company,
        "file_name": file_row.file_name,
        "analysis_target_doctype": analysis.get("target_doctype"),
        "analysis_reason": analysis.get("reason"),
        "user_feedback": (user_feedback or "").strip() or None,
        "headers": headers,
        "sheet_name": sheet_name,
        "sample_strategy": "random",
        "sample_row_limit": SAMPLE_ROWS_FOR_AI,
        "total_records": total_source_records,
        "records_sample": sampled_records,
        "is_chart_of_accounts": is_coa,
        "coa_context": coa_context,
        "required_json_schema": _schema_hint(has_many_rows),
    }

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": truncate_text(
            json.dumps(user_payload, ensure_ascii=False, default=str),
            max_length=20000,
        )},
    ]

    timeout_seconds = max(int(config.timeout_seconds or 60), SMART_PLAN_TIMEOUT_FLOOR)
    fallback_doctype = (
        analysis.get("target_doctype")
        or getattr(file_row, "target_doctype", None)
        or None
    )

    try:
        raw = _chat_completion(
            config.api_base_url,
            config.model,
            config.api_key,
            messages,
            timeout_seconds,
        )
        try:
            plan = _parse_json_response(raw)
        except Exception as parse_exc:
            plan = _repair_plan_json(
                raw,
                parse_exc,
                config,
                timeout_seconds,
                fallback_doctype,
                has_many_rows,
            )
    except Exception as exc:
        frappe.log_error(frappe.get_traceback(), "Smart Planner AI Failed")
        return {"error": f"AI không tạo được kế hoạch: {exc}"}

    normalised = _normalise_plan(
        plan,
        sampled_records,
        doc,
        fallback_doctype=fallback_doctype,
        fallback_analysis=analysis,
        source_record_count=total_source_records,
    )
    if not normalised.get("error"):
        _post_process_coa_plan(normalised, doc)
        _post_process_bank_account_plan(normalised, doc)
        _post_process_group_link_plan(normalised)
        _post_process_address_plan(normalised)
        _post_process_contact_plan(normalised)
        _post_process_item_catalog_plan(normalised)
        _post_process_department_branch_plan(normalised, doc, sheet_name)
        _refresh_plan_totals(normalised)
    return normalised


def build_smart_plan_from_analysis(doc, file_row) -> dict:
    """Build an executable Python import plan from saved analyze-file mappings.

    The analyze step already asks AI/heuristics to map source columns from 10
    random rows. This converts that saved mapping to the same smart-plan shape
    used by ``smart_executor`` so the UI can import directly after analysis.
    """
    try:
        analysis = json.loads(getattr(file_row, "analysis_json", None) or "{}")
    except Exception:
        analysis = {}

    fallback_doctype = (
        analysis.get("target_doctype")
        or getattr(file_row, "target_doctype", None)
        or None
    )
    if not fallback_doctype or not analysis.get("mappings"):
        return {"error": "Analysis chưa có mapping field đủ để tạo script import."}

    sample_seed = _sample_seed(file_row)
    summary = summarize_workbook(
        file_row.file_path,
        max_sample_rows=SAMPLE_ROWS_FOR_AI,
        sample_strategy="random",
        sample_seed=sample_seed,
    )
    sheet_name = analysis.get("sheet_name") or _first_sheet_name(summary)
    header_row = analysis.get("header_row_number") or _first_header_row(summary)

    sampled_records: list[dict] = []
    try:
        if sheet_name and header_row:
            sampled_records = sample_excel_records(
                file_row.file_path,
                sheet_name,
                header_row,
                sample_size=SAMPLE_ROWS_FOR_AI,
                seed=sample_seed,
            )
    except Exception:
        frappe.log_error(frappe.get_traceback(), "Smart Planner Analysis Sample Failed")

    total_source_records = _source_row_count(summary, sheet_name, header_row)
    normalised = _normalise_plan(
        analysis,
        sampled_records,
        doc,
        fallback_doctype=fallback_doctype,
        fallback_analysis=analysis,
        source_record_count=total_source_records,
    )
    if not normalised.get("error"):
        normalised["plan_source"] = "analysis"
        normalised["cached_from_analysis"] = True
        _post_process_coa_plan(normalised, doc)
        _post_process_bank_account_plan(normalised, doc)
        _post_process_group_link_plan(normalised)
        _post_process_address_plan(normalised)
        _post_process_contact_plan(normalised)
        _post_process_item_catalog_plan(normalised)
        _post_process_department_branch_plan(normalised, doc, sheet_name)
        _refresh_plan_totals(normalised)
    return normalised


def _build_system_prompt(has_many_rows: bool, has_feedback: bool) -> str:
    base = (
        "Bạn là chuyên gia lập kế hoạch migration dữ liệu từ MISA ERP sang ERPNext v16 cho doanh nghiệp Việt Nam.\n"
        "Nhận file Excel tiếng Việt + TỐI ĐA 10 SAMPLE ROWS NGẪU NHIÊN → tạo plan import nhiều bước.\n"
        "Trả về STRICT JSON only — không markdown, không text ngoài JSON.\n"
        "Chỉ dùng fieldname ERPNext có thực. KHÔNG bịa fieldname.\n"
        "AI KHÔNG được import dữ liệu trực tiếp, KHÔNG liệt kê toàn bộ dataset.\n"
        "Với mọi step có source_data, phải có row_template.field_map — backend sẽ áp dụng cho toàn bộ file.\n"
        "Mảng records chỉ là preview tối đa 10 ví dụ từ sample.\n\n"
        "QUY TẮC DỮ LIỆU VIỆT NAM:\n"
        "• Bỏ hàng tổng: 'Tổng', 'Tổng cộng', 'Cộng', 'Total', dòng chỉ 1 ô có giá trị.\n"
        "• Số Việt Nam: 1.234.567,89 → 1234567.89 (dấu chấm = phân cách nghìn, dấu phẩy = thập phân).\n"
        "• Số điện thoại: loại bỏ +84, ký tự thừa → chuẩn 10 chữ số.\n"
        "• Mã đối tượng/Mã KH/Mã NCC: KHÔNG chỉnh sửa — dùng nguyên để unique_key.\n\n"
        "MAPPING MẶC ĐỊNH CHO DANH MỤC MISA → ERPNext:\n"
        "┌─ Customer ──────────────────────────────────────────────────────────────────┐\n"
        "│ Mã KH / Mã đối tượng → customer_id (unique_key cho Customer)               │\n"
        "│ Tên KH / Tên đối tượng → customer_name                                     │\n"
        "│ MST / Mã số thuế → tax_id                                                  │\n"
        "│ Nhóm KH / Nhóm khách hàng → customer_group (default: 'All Customer Groups')│\n"
        "│ Loại: 'Công ty'/'Cty' → 'Company', còn lại → 'Individual' (customer_type)  │\n"
        "│ Địa chỉ → Address.address_line1 (step riêng)                               │\n"
        "│ SĐT / Điện thoại → Contact.phone (step riêng)                              │\n"
        "│ Email → Contact.email_id (step riêng)                                      │\n"
        "├─ Supplier ──────────────────────────────────────────────────────────────────┤\n"
        "│ Mã NCC → supplier_id (unique_key)                                           │\n"
        "│ Tên NCC → supplier_name                                                    │\n"
        "│ MST → tax_id                                                               │\n"
        "│ Nhóm NCC → supplier_group (default: 'All Supplier Groups')                 │\n"
        "│ Địa chỉ / SĐT → Address + Contact (step riêng như Customer)               │\n"
        "├─ Item ──────────────────────────────────────────────────────────────────────┤\n"
        "│ Mã hàng / Mã VTHH → item_code (unique_key)                                 │\n"
        "│ Tên hàng / Tên hàng hóa → item_name                                        │\n"
        "│ ĐVT / Đơn vị tính → stock_uom (phải tồn tại trong UOM)                     │\n"
        "│ Nhóm hàng / Nhóm VTHH → item_group (default: 'All Item Groups')            │\n"
        "│ Loại hàng: 'Hàng hóa'/'Thành phẩm' → is_stock_item=1, else 0              │\n"
        "│ KHÔNG đặt opening_stock/valuation_rate/price trên Item — dùng step riêng  │\n"
        "├─ Employee ──────────────────────────────────────────────────────────────────┤\n"
        "│ Mã NV / Mã nhân viên → employee_number (unique_key)                        │\n"
        "│ Tên NV / Họ và tên → employee_name                                         │\n"
        "│ Phòng ban → department                                                     │\n"
        "│ Chức vụ / Chức danh → designation                                          │\n"
        "│ Ngày sinh → date_of_birth (format DD/MM/YYYY → YYYY-MM-DD)                │\n"
        "│ Giới tính: 'Nam' → 'Male', 'Nữ' → 'Female'                                │\n"
        "├─ Warehouse ─────────────────────────────────────────────────────────────────┤\n"
        "│ Mã kho / Tên kho → warehouse_name (unique_key)                              │\n"
        "│ parent_warehouse: nếu có kho cha, gán; không thì dùng root company warehouse│\n"
        "└─────────────────────────────────────────────────────────────────────────────┘\n\n"
        "QUY TẮC MULTI-STEP:\n"
        "• Customer/Supplier: Step 1 = tạo master, Step 2 = Address (nếu có địa chỉ), Step 3 = Contact (nếu có SĐT/email).\n"
        "• Address: address_title=Tên KH, address_type='Billing', link_doctype='Customer', link_name=customer_id.\n"
        "• Contact: first_name=Tên KH, phone_nos[0].phone=SĐT, links[0].link_doctype='Customer'.\n"
        "• Các step sau có thể reference record từ step trước.\n\n"
        "QUY TẮC ITEM:\n"
        "• Item = master data only. KHÔNG tạo Stock Reconciliation / Opening Stock trừ khi file CÓ CẢ số lượng VÀ đơn giá thực.\n"
        "• Item Price: chỉ tạo khi có cột price_list_rate > 0 rõ ràng.\n\n"
        "TRANSFORM SUPPORTED: direct | number | strip | split:before:Tên: | regex:pattern | date:DD/MM/YYYY | phone_vn\n"
        "Dùng 'derived_fields' cho logic phức tạp hơn.\n"
    )
    if has_feedback:
        base += (
            "\nNGƯỜI DÙNG CÓ PHẢN HỒI CỤ THỂ CHO FILE NÀY — ưu tiên tối cao:\n"
            "Áp dụng phản hồi trước tất cả quy tắc trên. Ghi rõ phản hồi đã ảnh hưởng thế nào vào plan_summary.\n"
        )
    return base


def _schema_hint(has_many_rows: bool) -> dict:
    schema = {
        "plan_summary": "Vietnamese summary shown to the user before execution.",
        "steps": [
            {
                "title": "Vietnamese label of this step",
                "description": "Why this step is needed (Vietnamese)",
                "target_doctype": "ERPNext DocType",
                "mode": "insert",
                "unique_key": "fieldname used to identify the record (defaults to name)",
                "preview_format": "table or tree",
                "parent_field": "parent fieldname when preview_format = tree",
                "label_field": "fieldname to show as label",
                "ignore_duplicates": True,
                "deduplicate_by": ["fieldname"],
                "fixed_values": {"fieldname": "value"},
                "row_template": {
                    "source_filter": "skip_totals or all",
                    "field_map": {
                        "target_fieldname": {
                            "source_column": "Excel header",
                            "transform": "direct | number | strip | split:before:Tên: | regex:pattern",
                            "default": None,
                            "value": "literal value (use instead of source_column)",
                        }
                    },
                },
                "records": [
                    {"fieldname": "preview value from the 10-row sample only"}
                ],
            }
        ],
    }
    return schema


def _repair_plan_json(
    raw_response: str,
    parse_error: Exception,
    config,
    timeout_seconds: int,
    fallback_doctype: str | None,
    has_many_rows: bool,
) -> dict:
    """Ask the AI to repair malformed Smart Plan JSON once.

    We keep this separate from planning: the model must not reinterpret the
    file, only fix JSON syntax and preserve/compact the existing intent.
    """
    repair_payload = {
        "parse_error": str(parse_error),
        "fallback_target_doctype": fallback_doctype,
        "required_json_schema": _schema_hint(has_many_rows),
        "malformed_response": truncate_text(raw_response or "", max_length=26000),
    }
    repair_messages = [
        {
            "role": "system",
            "content": (
                "You repair malformed JSON for an ERPNext Smart Import plan. "
                "Return ONLY valid JSON. Do not use markdown. "
                "Preserve the original import intent and fieldnames. "
                "The output must be an object with a 'steps' array. "
                "If the original tried to list too many records, compact it into a row_template "
                "with at most 5 sample records."
            ),
        },
        {
            "role": "user",
            "content": truncate_text(
                json.dumps(repair_payload, ensure_ascii=False, default=str),
                max_length=30000,
            ),
        },
    ]
    repaired = _chat_completion(
        config.api_base_url,
        config.model,
        config.api_key,
        repair_messages,
        timeout_seconds,
    )
    try:
        return _parse_json_response(repaired)
    except Exception as repair_exc:
        frappe.log_error(
            title="Smart Planner JSON Repair Failed",
            message=(
                f"Original parse error: {parse_error}\n"
                f"Repair parse error: {repair_exc}\n\n"
                f"Original response excerpt:\n{truncate_text(raw_response or '', max_length=4000)}\n\n"
                f"Repaired response excerpt:\n{truncate_text(repaired or '', max_length=4000)}"
            ),
        )
        raise repair_exc


def _normalise_plan(
    plan: dict,
    raw_records: list[dict],
    doc,
    fallback_doctype: str | None = None,
    fallback_analysis: dict | None = None,
    source_record_count: int | None = None,
) -> dict:
    plan = _coerce_plan_response(plan, fallback_doctype)
    if not isinstance(plan, dict) or not plan.get("steps"):
        return {"error": "AI không trả về danh sách bước hợp lệ."}

    source_record_count = int(source_record_count or len(raw_records or []))
    normalised_steps: list[dict] = []
    for index, step in enumerate(plan.get("steps") or [], start=1):
        if not isinstance(step, dict):
            return {"error": f"Bước {index}: step không phải object."}
        step = _coerce_step_mapping(step)
        target_doctype = _resolve_step_target_doctype(step, fallback_doctype)
        if not target_doctype:
            return {
                "error": (
                    f"Bước {index}: thiếu target_doctype. "
                    "AI cần trả về target_doctype hoặc doctype cho từng bước."
                )
            }
        if not frappe.db.exists("DocType", target_doctype):
            return {"error": f"Bước {index}: DocType '{target_doctype}' không tồn tại trong DCNET."}

        records = step.get("records") or []
        if isinstance(records, dict):
            records = [records]
        if not isinstance(records, list):
            return {"error": f"Bước {index}: trường records không phải list."}

        row_template = step.get("row_template") or {}
        if (
            not (isinstance(row_template, dict) and row_template.get("field_map"))
            and _should_expand_from_analysis(target_doctype, records, raw_records, fallback_analysis)
        ):
            row_template = _row_template_from_analysis(fallback_analysis)
            if row_template and not step.get("fixed_values") and isinstance(fallback_analysis.get("defaults"), dict):
                step["fixed_values"] = fallback_analysis.get("defaults")

        has_row_template = (
            isinstance(row_template, dict)
            and bool(row_template.get("field_map"))
            and _row_template_is_source_backed(row_template)
        )
        materialised = list(records)
        if has_row_template:
            materialised = _materialise_records(row_template, raw_records, materialised)

        clean_records = [
            _normalise_record(rec)
            for rec in materialised
            if isinstance(rec, dict) and not _is_total_row(rec)
        ]
        clean_records = [rec for rec in clean_records if rec]

        deduplicate_by = step.get("deduplicate_by") or []
        if deduplicate_by:
            clean_records = _dedupe(clean_records, deduplicate_by)

        if not has_row_template and len(clean_records) > MAX_PLAN_RECORDS_PER_STEP:
            return {
                "error": (
                    f"Bước {index}: số bản ghi sau xử lý ({len(clean_records)}) "
                    f"vượt quá giới hạn {MAX_PLAN_RECORDS_PER_STEP}/bước. "
                    "Vui lòng tách file nhỏ hơn hoặc liên hệ admin."
                )
            }

        fixed_values = step.get("fixed_values") or {}
        if isinstance(fixed_values, dict):
            for rec in clean_records:
                for key, value in fixed_values.items():
                    rec.setdefault(key, value)

        if doc.company and _meta_has_field(target_doctype, "company"):
            for rec in clean_records:
                rec.setdefault("company", doc.company)

        preview_format = (step.get("preview_format") or "").lower()
        if preview_format not in {"tree", "table"}:
            preview_format = "tree" if target_doctype in HIERARCHICAL_DOCTYPES else "table"

        parent_field = step.get("parent_field") or HIERARCHICAL_DOCTYPES.get(target_doctype)
        label_field = step.get("label_field") or _guess_label_field(target_doctype, clean_records)

        if parent_field and clean_records:
            clean_records = _topological_sort_records(clean_records, parent_field, label_field)

        if has_row_template:
            clean_records = clean_records[:SMART_PREVIEW_RECORD_LIMIT]

        step_record_count = source_record_count if has_row_template else len(clean_records)

        normalised_steps.append(
            {
                "step": index,
                "title": step.get("title") or f"Bước {index}: {target_doctype}",
                "description": step.get("description") or "",
                "target_doctype": target_doctype,
                "mode": (step.get("mode") or "insert").lower(),
                "unique_key": step.get("unique_key") or _guess_unique_key(target_doctype),
                "preview_format": preview_format,
                "parent_field": parent_field,
                "label_field": label_field,
                "ignore_duplicates": bool(step.get("ignore_duplicates", True)),
                "row_template": row_template if has_row_template else {},
                "records_are_preview": has_row_template,
                "source_record_count": step_record_count,
                "execution_mode": "python_row_template" if has_row_template else "python_records",
                "records": clean_records,
                "record_count": step_record_count,
            }
        )

    if not normalised_steps:
        return {"error": "Kế hoạch không có bước hợp lệ nào."}

    return {
        "plan_summary": plan.get("plan_summary") or "",
        "total_steps": len(normalised_steps),
        "total_records": sum(step["record_count"] for step in normalised_steps),
        "source_record_count": source_record_count,
        "ai_sample_row_count": len(raw_records or []),
        "ai_sample_strategy": "random",
        "execution_mode": "python_script",
        "uses_ai_for_import": False,
        "steps": normalised_steps,
    }


def _should_expand_from_analysis(
    target_doctype: str,
    records: list[dict],
    raw_records: list[dict],
    analysis: dict | None,
) -> bool:
    if not raw_records or not analysis:
        return False
    if target_doctype not in ANALYSIS_EXPAND_DOCTYPES:
        return False
    if _clean_doctype_value(analysis.get("target_doctype")) != target_doctype:
        return False
    if not analysis.get("mappings"):
        return False
    return len(records or []) < len(raw_records)


def _row_template_from_analysis(analysis: dict | None) -> dict:
    if not analysis:
        return {}
    field_map = _mappings_to_field_map(analysis.get("mappings") or [])
    if not field_map:
        return {}
    return {
        "source_filter": analysis.get("source_filter") or "skip_totals",
        "field_map": field_map,
    }


def _row_template_is_source_backed(row_template: dict) -> bool:
    field_map = row_template.get("field_map") or {}
    if not isinstance(field_map, dict):
        return False
    for mapping in field_map.values():
        if isinstance(mapping, dict) and mapping.get("source_column"):
            return True
    return False


def _post_process_item_catalog_plan(plan: dict) -> None:
    """Keep product-catalog imports as Item master data.

    ERPNext's Item controller treats ``opening_stock`` as an instruction to
    create opening stock and therefore requires valuation rate. DCNET imports
    product catalogs first; prices and valued opening stock come from separate
    files, so we strip those fields from Item and drop zero-valued downstream
    price/stock records.
    """
    if not plan or not isinstance(plan.get("steps"), list):
        return

    for step in plan["steps"]:
        target_doctype = step.get("target_doctype")
        records = step.get("records") or []
        if not isinstance(records, list):
            continue

        if target_doctype == "Item":
            cleaned_items = []
            for rec in records:
                if isinstance(rec, dict) and _normalise_item_master_record(rec):
                    cleaned_items.append(rec)
            step["records"] = cleaned_items

        elif target_doctype == "Item Price":
            step["records"] = [
                rec for rec in records
                if isinstance(rec, dict) and flt(rec.get("price_list_rate")) > 0
            ]

        elif target_doctype == "Stock Reconciliation":
            cleaned_records = []
            for rec in records:
                if not isinstance(rec, dict):
                    continue
                items = rec.get("items")
                if not isinstance(items, list):
                    cleaned_records.append(rec)
                    continue

                valid_items = [
                    item for item in items
                    if (
                        isinstance(item, dict)
                        and flt(item.get("qty"))
                        and flt(item.get("valuation_rate")) > 0
                    )
                ]
                if valid_items:
                    rec["items"] = valid_items
                    cleaned_records.append(rec)
            step["records"] = cleaned_records

        step["record_count"] = len(step.get("records") or [])

    plan["total_records"] = sum(s.get("record_count", 0) for s in plan["steps"])
    plan["total_steps"] = len(plan["steps"])


def _post_process_bank_account_plan(plan: dict, doc=None) -> None:
    """Make Bank Account imports executable without relying on AI-only text.

    ERPNext's Bank Account controller requires ``account_name`` and builds the
    document name as ``account_name + " - " + bank``. It also requires a GL
    Account when ``is_company_account`` is enabled. Vietnamese bank-account
    files usually contain the bank account number and owner, but not the GL
    Account link, so we import them as bank-account master data first.
    """
    if not plan or not isinstance(plan.get("steps"), list):
        return

    default_company = getattr(doc, "company", None)
    touched = False

    for step in plan["steps"]:
        if step.get("target_doctype") != "Bank Account":
            continue

        records = step.get("records") or []
        if not isinstance(records, list):
            continue

        step["unique_key"] = "bank_account_no"
        if not step.get("label_field"):
            step["label_field"] = "account_name"

        for rec in records:
            if not isinstance(rec, dict):
                continue

            account_no = _clean_bank_account_no(rec.get("bank_account_no"))
            if not account_no and rec.get("bank_account"):
                account_no = _clean_bank_account_no(rec.get("bank_account"))
                if account_no:
                    rec["bank_account_no"] = account_no
            elif account_no:
                rec["bank_account_no"] = account_no

            account_name = str(rec.get("account_name") or "").strip()
            if account_no:
                if account_name:
                    if account_no not in account_name:
                        rec["account_name"] = f"{account_name} - {account_no}"
                else:
                    rec["account_name"] = account_no

            if default_company and _should_use_default_company(rec.get("company"), default_company):
                rec["company"] = default_company

            rec["disabled"] = _normalise_disabled_value(rec.get("disabled"))

            # ERPNext validates a company bank account against a linked GL
            # Account. Source bank-account lists rarely include that field; the
            # accounting team can link it after COA import.
            if _truthy(rec.get("is_company_account")) and not rec.get("account"):
                rec["is_company_account"] = 0
            elif rec.get("is_company_account") in (None, ""):
                rec["is_company_account"] = 0

        step["record_count"] = len(records)
        touched = True

    if touched:
        plan["total_records"] = sum(s.get("record_count", 0) for s in plan["steps"])
        plan["total_steps"] = len(plan["steps"])


def _post_process_department_branch_plan(plan: dict, doc, sheet_name: str | None) -> None:
    """Apply the same branch-hierarchy defaults the plain Analyze/Data Import
    flow already gets from get_default_values() (see doctype_metadata's
    DEPARTMENT_BRANCH_SHEETS). Without this, a multi-sheet "co cau to chuc
    theo chi nhanh" workbook — one sheet listing chi nhanh, one sheet per
    chi nhanh listing its phong ban — lands every Department flat under the
    "All Departments" root because each sheet is planned in isolation and the
    AI has no idea a sibling sheet already created (or will create) the
    parent Department it should nest under.
    """
    if not sheet_name:
        return
    defaults = get_default_values("Department", doc.company, sheet_name)
    if not defaults:
        return
    for step in plan.get("steps", []):
        if step.get("target_doctype") != "Department":
            continue
        for record in step.get("records", []):
            for key, value in defaults.items():
                record.setdefault(key, value)
        row_template = step.get("row_template")
        if isinstance(row_template, dict):
            field_map = row_template.setdefault("field_map", {})
            for key, value in defaults.items():
                field_map.setdefault(key, {"value": value})


def _clean_bank_account_no(value) -> str:
    if value in (None, ""):
        return ""
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return str(value).strip()


def _should_use_default_company(value, default_company: str) -> bool:
    if value in (None, ""):
        return True
    value_text = str(value).strip()
    if value_text == default_company:
        return False
    try:
        return not bool(frappe.db.exists("Company", value_text))
    except Exception:
        return True


def _normalise_disabled_value(value) -> int:
    if value in (None, ""):
        return 0
    if value in (0, False):
        return 0
    if value in (1, True):
        return 1
    if isinstance(value, str):
        value_key = normalize_key(value)
        if value.strip() in {"0", "1"}:
            return int(value.strip())
        if "đang sử dụng" in value_key or "dang su dung" in value_key:
            return 0
        if "ngừng" in value_key or "ngung" in value_key:
            return 1
    return int(bool(value))


def _truthy(value) -> bool:
    if value in (1, True):
        return True
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "y"}
    return bool(value)


def _post_process_group_link_plan(plan: dict) -> None:
    """Ensure linked group masters exist and all references point to them.

    Smart plans often create Customer/Supplier/Item groups from source columns
    before inserting the actual master data. This pass removes blank group
    rows, maps exact labels to existing groups, and creates a group step for
    any still-missing labels. It intentionally avoids fuzzy/contains matching.
    """
    if not plan or not isinstance(plan.get("steps"), list):
        return

    requested: dict[str, set[str]] = {doctype: set() for doctype in GROUP_LINK_CONFIG}
    consumer_fields = _group_consumer_fields(plan)

    for step in plan["steps"]:
        target_doctype = step.get("target_doctype")
        records = step.get("records") or []
        if not isinstance(records, list):
            continue

        config = GROUP_LINK_CONFIG.get(target_doctype)
        if config:
            label_field = config["label_field"]
            for rec in records:
                if isinstance(rec, dict):
                    label = _clean_group_label(rec.get(label_field) or rec.get("name"))
                    if label:
                        requested[target_doctype].add(label)

        for group_doctype, fieldnames in consumer_fields.get(target_doctype, []):
            root = GROUP_LINK_CONFIG[group_doctype]["root"]
            for rec in records:
                if not isinstance(rec, dict):
                    continue
                for fieldname in fieldnames:
                    label = _clean_group_label(rec.get(fieldname))
                    if label:
                        requested[group_doctype].add(label)
                    elif rec.get(fieldname) in (None, ""):
                        rec[fieldname] = root

    mapping: dict[tuple[str, str], str] = {}
    missing: dict[str, set[str]] = {doctype: set() for doctype in GROUP_LINK_CONFIG}
    for group_doctype, labels in requested.items():
        root = GROUP_LINK_CONFIG[group_doctype]["root"]
        for label in labels:
            existing = _find_existing_group_label(group_doctype, label)
            mapped = existing or label
            mapping[(group_doctype, label)] = mapped
            if not existing and label != root:
                missing[group_doctype].add(label)

    _rewrite_group_link_values(plan, consumer_fields, mapping)
    _normalise_group_steps(plan, mapping, missing)
    _ensure_missing_group_steps(plan, consumer_fields, missing)
    _refresh_plan_totals(plan)


def _group_consumer_fields(plan: dict) -> dict[str, list[tuple[str, list[str]]]]:
    consumer_fields: dict[str, list[tuple[str, list[str]]]] = {}
    for step in plan.get("steps") or []:
        target_doctype = step.get("target_doctype")
        if not target_doctype or target_doctype in GROUP_LINK_CONFIG:
            continue
        try:
            meta = frappe.get_meta(target_doctype)
        except Exception:
            continue
        grouped: dict[str, list[str]] = {}
        for df in meta.fields:
            if df.fieldtype == "Link" and df.options in GROUP_LINK_CONFIG:
                grouped.setdefault(df.options, []).append(df.fieldname)
        if grouped:
            consumer_fields[target_doctype] = list(grouped.items())
    return consumer_fields


def _rewrite_group_link_values(
    plan: dict,
    consumer_fields: dict[str, list[tuple[str, list[str]]]],
    mapping: dict[tuple[str, str], str],
) -> None:
    for step in plan.get("steps") or []:
        target_doctype = step.get("target_doctype")
        for group_doctype, fieldnames in consumer_fields.get(target_doctype, []):
            root = GROUP_LINK_CONFIG[group_doctype]["root"]
            for rec in step.get("records") or []:
                if not isinstance(rec, dict):
                    continue
                for fieldname in fieldnames:
                    label = _clean_group_label(rec.get(fieldname))
                    rec[fieldname] = mapping.get((group_doctype, label), label or root)


def _normalise_group_steps(
    plan: dict,
    mapping: dict[tuple[str, str], str],
    missing: dict[str, set[str]],
) -> None:
    for step in list(plan.get("steps") or []):
        group_doctype = step.get("target_doctype")
        config = GROUP_LINK_CONFIG.get(group_doctype)
        if not config:
            continue

        label_field = config["label_field"]
        parent_field = config["parent_field"]
        root = config["root"]
        cleaned: list[dict] = []
        seen: set[str] = set()

        for rec in step.get("records") or []:
            if not isinstance(rec, dict):
                continue
            label = _clean_group_label(rec.get(label_field) or rec.get("name"))
            if not label:
                continue
            mapped = mapping.get((group_doctype, label), label)
            if mapped != label or _group_exists(group_doctype, mapped):
                continue
            if label in seen:
                continue
            seen.add(label)
            rec[label_field] = label
            rec[parent_field] = _clean_group_label(rec.get(parent_field)) or root
            rec["is_group"] = int(bool(rec.get("is_group"))) if rec.get("is_group") not in (None, "") else 0
            cleaned.append(rec)
            missing[group_doctype].discard(label)

        if cleaned:
            step["records"] = cleaned
            step["record_count"] = len(cleaned)
            step["unique_key"] = label_field
            step["label_field"] = label_field
            step["parent_field"] = parent_field
            step["preview_format"] = "tree"
            step["ignore_duplicates"] = True
        else:
            plan["steps"].remove(step)


def _ensure_missing_group_steps(
    plan: dict,
    consumer_fields: dict[str, list[tuple[str, list[str]]]],
    missing: dict[str, set[str]],
) -> None:
    for group_doctype, labels in missing.items():
        labels = {label for label in labels if _clean_group_label(label)}
        if not labels:
            continue

        config = GROUP_LINK_CONFIG[group_doctype]
        label_field = config["label_field"]
        parent_field = config["parent_field"]
        root = config["root"]

        step = next((s for s in plan["steps"] if s.get("target_doctype") == group_doctype), None)
        new_records = [
            {
                label_field: label,
                parent_field: root,
                "is_group": 0,
            }
            for label in sorted(labels, key=_normalise_group_match_text)
        ]

        if step is not None:
            existing_labels = {
                _clean_group_label(rec.get(label_field) or rec.get("name"))
                for rec in (step.get("records") or [])
                if isinstance(rec, dict)
            }
            step.setdefault("records", [])
            for rec in new_records:
                if rec[label_field] not in existing_labels:
                    step["records"].append(rec)
            step["record_count"] = len(step.get("records") or [])
            continue

        insert_at = _first_consumer_step_index(plan, consumer_fields, group_doctype)
        new_step = {
            "step": 0,
            "title": f"Tạo {group_doctype} còn thiếu",
            "description": f"Tự tạo các {group_doctype} chưa có trong DCNET rồi mapping lại dữ liệu nguồn.",
            "target_doctype": group_doctype,
            "mode": "insert",
            "unique_key": label_field,
            "preview_format": "tree",
            "parent_field": parent_field,
            "label_field": label_field,
            "ignore_duplicates": True,
            "records": new_records,
            "record_count": len(new_records),
        }
        plan["steps"].insert(insert_at, new_step)


def _first_consumer_step_index(
    plan: dict,
    consumer_fields: dict[str, list[tuple[str, list[str]]]],
    group_doctype: str,
) -> int:
    for idx, step in enumerate(plan.get("steps") or []):
        for linked_group, _fieldnames in consumer_fields.get(step.get("target_doctype"), []):
            if linked_group == group_doctype:
                return idx
    return 0


def _find_existing_group_label(group_doctype: str, label: str) -> str | None:
    label = _clean_group_label(label)
    if not label:
        return None
    if _group_exists(group_doctype, label):
        return label

    config = GROUP_LINK_CONFIG[group_doctype]
    label_field = config["label_field"]
    try:
        existing = frappe.db.get_value(group_doctype, {label_field: label}, "name")
        if existing:
            return existing
    except Exception:
        pass

    return None


def _group_exists(group_doctype: str, label: str) -> bool:
    try:
        return bool(frappe.db.exists(group_doctype, label))
    except Exception:
        return False


def _clean_group_label(value) -> str:
    if value in (None, ""):
        return ""
    label = str(value).strip()
    if not label:
        return ""
    if label in {"-", "—", "–"}:
        return ""
    if normalize_key(label) in {"none", "null", "na", "n a", "khong", "không"}:
        return ""
    return label


def _normalise_group_match_text(value) -> str:
    text = str(value or "").strip()
    if not text:
        return ""
    text = unicodedata.normalize("NFKD", text)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    text = text.replace("đ", "d").replace("Đ", "D")
    text = text.casefold()
    text = re.sub(r"[-_/;]+", " ", text)
    text = re.sub(r"[^\w\s]", " ", text, flags=re.UNICODE)
    return " ".join(text.split())


def _refresh_plan_totals(plan: dict) -> None:
    if not plan or not isinstance(plan.get("steps"), list):
        return
    total = 0
    for idx, step in enumerate(plan["steps"], start=1):
        step["step"] = idx
        if step.get("records_are_preview") and step.get("source_record_count") not in (None, ""):
            try:
                step["record_count"] = int(step.get("source_record_count") or 0)
            except (TypeError, ValueError):
                step["record_count"] = len(step.get("records") or [])
        else:
            step["record_count"] = len(step.get("records") or [])
        total += step["record_count"]
    plan["total_records"] = total
    plan["total_steps"] = len(plan["steps"])


def _post_process_address_plan(plan: dict) -> None:
    """Create and normalise Address records for party masters.

    ERPNext stores addresses as separate ``Address`` documents linked through
    Dynamic Link rows. Source ERP files usually keep address text directly on
    Customer/Supplier, so this pass builds/repairs the Address step and fills
    mandatory fields like ``city``.
    """
    if not plan or not isinstance(plan.get("steps"), list):
        return

    existing_keys: set[tuple[str, str, str, str]] = set()
    address_step = None
    party_link_lookup = _address_party_link_lookup(plan)

    for step in list(plan["steps"]):
        if step.get("target_doctype") != "Address":
            continue
        address_step = address_step or step
        cleaned = []
        for rec in step.get("records") or []:
            if not isinstance(rec, dict):
                continue
            normalised = _normalise_address_record(rec, party_link_lookup=party_link_lookup)
            if not normalised:
                continue
            key = _address_record_key(normalised)
            if key in existing_keys:
                continue
            existing_keys.add(key)
            cleaned.append(normalised)
        if cleaned:
            step["records"] = cleaned
            step["record_count"] = len(cleaned)
            step["unique_key"] = step.get("unique_key") or "address_title"
            step["label_field"] = "address_title"
            step["preview_format"] = "table"
            step["ignore_duplicates"] = True
        else:
            plan["steps"].remove(step)

    generated_by_insert_index: dict[int, list[dict]] = {}
    for index, step in enumerate(plan.get("steps") or []):
        party_doctype = step.get("target_doctype")
        config = ADDRESS_LINK_CONFIG.get(party_doctype)
        if not config:
            continue
        for rec in step.get("records") or []:
            if not isinstance(rec, dict):
                continue
            address_line = _party_address_line(rec, config)
            if not address_line:
                continue
            link_name = _party_link_name(rec, config)
            if not link_name:
                continue
            address_title = str(rec.get(config["title_field"]) or link_name).strip()
            address_rec = _normalise_address_record({
                "address_title": address_title,
                "address_type": "Billing",
                "address_line1": address_line,
                "country": "Vietnam",
                "is_primary_address": 1,
                "is_shipping_address": 1,
                "links": [{"link_doctype": party_doctype, "link_name": link_name}],
            })
            if not address_rec:
                continue
            key = _address_record_key(address_rec)
            if key in existing_keys:
                continue
            existing_keys.add(key)
            generated_by_insert_index.setdefault(index + 1, []).append(address_rec)

    if generated_by_insert_index:
        if address_step is not None and address_step in plan["steps"]:
            for records in generated_by_insert_index.values():
                address_step.setdefault("records", []).extend(records)
            address_step["record_count"] = len(address_step.get("records") or [])
        else:
            offset = 0
            for insert_at, records in sorted(generated_by_insert_index.items()):
                new_step = {
                    "step": 0,
                    "title": "Tạo địa chỉ",
                    "description": "Tự tách cột địa chỉ từ danh mục và tạo Address liên kết với Customer/NCC.",
                    "target_doctype": "Address",
                    "mode": "insert",
                    "unique_key": "address_title",
                    "preview_format": "table",
                    "parent_field": None,
                    "label_field": "address_title",
                    "ignore_duplicates": True,
                    "records": records,
                    "record_count": len(records),
                }
                plan["steps"].insert(insert_at + offset, new_step)
                offset += 1

    _ensure_address_steps_after_parties(plan)
    _refresh_plan_totals(plan)


def _normalise_address_record(record: dict, party_link_lookup: dict[str, str] | None = None) -> dict | None:
    rec = dict(record)
    rec.pop("name", None)

    links = _normalise_address_links(rec, party_link_lookup=party_link_lookup)
    if links:
        rec["links"] = links
    else:
        rec.pop("links", None)

    address_line1 = str(
        rec.get("address_line1")
        or rec.get("address")
        or rec.get("customer_details")
        or rec.get("supplier_details")
        or ""
    ).strip()
    if not address_line1 or _looks_like_empty_address(address_line1):
        return None
    rec["address_line1"] = address_line1

    rec["address_type"] = str(rec.get("address_type") or "Billing").strip() or "Billing"
    rec["address_title"] = str(
        rec.get("address_title")
        or (links[0].get("link_name") if links else "")
        or "Address"
    ).strip()

    parts = _parse_vietnamese_address(address_line1)
    rec["country"] = str(rec.get("country") or parts.get("country") or "Vietnam").strip()
    rec["city"] = str(rec.get("city") or parts.get("city") or "Không xác định").strip()
    if not rec.get("state") and parts.get("state"):
        rec["state"] = parts["state"]

    for source, target in (
        ("is_primary", "is_primary_address"),
        ("is_default", "is_primary_address"),
        ("is_shipping", "is_shipping_address"),
    ):
        if source in rec and target not in rec:
            rec[target] = rec.pop(source)
    rec["is_primary_address"] = _normalise_address_check(rec.get("is_primary_address"), default=1)
    rec["is_shipping_address"] = _normalise_address_check(rec.get("is_shipping_address"), default=1)

    for key in ("links.link_doctype", "links.link_name", "link_doctype", "link_name"):
        rec.pop(key, None)
    return rec


def _ensure_address_steps_after_parties(plan: dict) -> None:
    party_indices = [
        idx
        for idx, step in enumerate(plan.get("steps") or [])
        if step.get("target_doctype") in ADDRESS_LINK_CONFIG
    ]
    if not party_indices:
        return

    last_party_idx = max(party_indices)
    for step in list(plan.get("steps") or []):
        if step.get("target_doctype") != "Address":
            continue
        idx = plan["steps"].index(step)
        if idx > last_party_idx:
            continue
        plan["steps"].pop(idx)
        if idx < last_party_idx:
            last_party_idx -= 1
        plan["steps"].insert(last_party_idx + 1, step)
        last_party_idx += 1


def _address_party_link_lookup(plan: dict) -> dict[str, str]:
    lookup: dict[str, str] = {}
    seen_party_doctypes: set[str] = set()

    for step in plan.get("steps") or []:
        party_doctype = step.get("target_doctype")
        config = ADDRESS_LINK_CONFIG.get(party_doctype)
        if not config:
            continue
        seen_party_doctypes.add(party_doctype)
        for rec in step.get("records") or []:
            if not isinstance(rec, dict):
                continue
            for fieldname in (
                *(config.get("name_fields") or ()),
                config.get("title_field"),
            ):
                value = str(rec.get(fieldname) or "").strip()
                if value:
                    lookup[value] = party_doctype

    if len(seen_party_doctypes) == 1:
        lookup["__default_doctype__"] = next(iter(seen_party_doctypes))
    return lookup


def _post_process_contact_plan(plan: dict) -> None:
    """Normalise Contact records generated from Customer/Supplier rows.

    Contacts are optional in source Excel. Create them only when a real phone,
    mobile number, or email exists; otherwise drop the Contact row so it cannot
    rollback the main Customer/Supplier import.
    """
    if not plan or not isinstance(plan.get("steps"), list):
        return

    party_lookup, party_sequence = _contact_party_context(plan)
    touched = False

    for step in list(plan.get("steps") or []):
        if step.get("target_doctype") != "Contact":
            continue

        cleaned = []
        seen: set[tuple] = set()
        for index, rec in enumerate(step.get("records") or [], start=1):
            if not isinstance(rec, dict):
                continue
            normalised = _normalise_contact_record(
                rec,
                party_lookup=party_lookup,
                party_sequence=party_sequence,
                row_index=index,
            )
            if not normalised:
                continue
            key = _contact_record_key(normalised)
            if key in seen:
                continue
            seen.add(key)
            cleaned.append(normalised)

        if cleaned:
            step["records"] = cleaned
            step["record_count"] = len(cleaned)
            step["unique_key"] = step.get("unique_key") or "first_name"
            step["label_field"] = "first_name"
            step["preview_format"] = "table"
            step["ignore_duplicates"] = True
            touched = True
        else:
            plan["steps"].remove(step)
            touched = True

    if touched:
        _ensure_contact_steps_after_parties(plan)
        _refresh_plan_totals(plan)


def _contact_party_context(plan: dict) -> tuple[dict[str, str], list[tuple[str, str]]]:
    lookup: dict[str, str] = {}
    sequence: list[tuple[str, str]] = []
    seen_party_doctypes: set[str] = set()

    for step in plan.get("steps") or []:
        party_doctype = step.get("target_doctype")
        config = CONTACT_LINK_CONFIG.get(party_doctype)
        if not config:
            continue
        seen_party_doctypes.add(party_doctype)
        for rec in step.get("records") or []:
            if not isinstance(rec, dict):
                continue
            link_name = _party_link_name(rec, config)
            if not link_name:
                continue
            sequence.append((party_doctype, link_name))
            for fieldname in (
                *(config.get("name_fields") or ()),
                config.get("title_field"),
            ):
                value = str(rec.get(fieldname) or "").strip()
                if value:
                    lookup[value] = party_doctype

    if len(seen_party_doctypes) == 1:
        lookup["__default_doctype__"] = next(iter(seen_party_doctypes))
    return lookup, sequence


def _normalise_contact_record(
    record: dict,
    party_lookup: dict[str, str],
    party_sequence: list[tuple[str, str]],
    row_index: int,
) -> dict | None:
    rec = dict(record)
    links = _normalise_contact_links(
        rec,
        party_lookup=party_lookup,
        party_sequence=party_sequence,
        row_index=row_index,
    )
    if links:
        rec["links"] = links
    else:
        rec.pop("links", None)

    for key in ("links.link_doctype", "links.link_name", "link_doctype", "link_name"):
        rec.pop(key, None)

    first_name = str(
        rec.get("first_name")
        or rec.get("contact_name")
        or rec.get("full_name")
        or (links[0].get("link_name") if links else "")
        or ""
    ).strip()
    if _looks_like_template(first_name):
        first_name = links[0].get("link_name") if links else ""
    if not first_name:
        return None
    rec["first_name"] = first_name

    _normalise_contact_phones(rec)
    _normalise_contact_emails(rec)

    if not _contact_has_data(rec):
        return None
    if not rec.get("links"):
        return None

    rec["is_primary_contact"] = _normalise_address_check(rec.get("is_primary_contact"), default=1)
    rec["is_billing_contact"] = _normalise_address_check(rec.get("is_billing_contact"), default=1)
    return rec


def _normalise_contact_links(
    record: dict,
    party_lookup: dict[str, str],
    party_sequence: list[tuple[str, str]],
    row_index: int,
) -> list[dict]:
    links = record.get("links")
    if isinstance(links, dict):
        links = [links]
    elif isinstance(links, str):
        links = [{"link_name": links}]
    if not isinstance(links, list):
        link_doctype = record.get("links.link_doctype") or record.get("link_doctype")
        link_name = record.get("links.link_name") or record.get("link_name")
        links = [{"link_doctype": link_doctype, "link_name": link_name}] if link_name else []

    fallback = party_sequence[row_index - 1] if 0 < row_index <= len(party_sequence) else None
    cleaned = []
    seen = set()
    for link in links:
        if isinstance(link, str):
            link = {"link_name": link}
        if not isinstance(link, dict):
            continue
        link_name = str(link.get("link_name") or "").strip()
        link_doctype = str(link.get("link_doctype") or "").strip()

        if _looks_like_template(link_name):
            link_name = fallback[1] if fallback else ""
        if not link_doctype and link_name:
            link_doctype = party_lookup.get(link_name) or party_lookup.get("__default_doctype__") or ""
        if not link_doctype and fallback:
            link_doctype = fallback[0]
        if not link_name and fallback:
            link_name = fallback[1]

        if not link_doctype or not link_name or _looks_like_template(link_name):
            continue
        key = (link_doctype, link_name)
        if key in seen:
            continue
        seen.add(key)
        cleaned.append({"link_doctype": link_doctype, "link_name": link_name})
    return cleaned


def _normalise_contact_phones(record: dict) -> None:
    phones = record.get("phone_nos")
    if isinstance(phones, dict):
        phones = [phones]
    if not isinstance(phones, list):
        phones = []

    for fieldname, is_mobile in (("phone", 0), ("mobile_no", 1), ("mobile", 1), ("phone_no", 0)):
        value = str(record.get(fieldname) or "").strip()
        if value and not _looks_like_empty_address(value):
            phones.append({
                "phone": value,
                "is_primary_phone": 0 if is_mobile else 1,
                "is_primary_mobile_no": 1 if is_mobile else 0,
            })

    cleaned = []
    seen = set()
    for phone in phones:
        if isinstance(phone, str):
            phone = {"phone": phone}
        if not isinstance(phone, dict):
            continue
        value = str(phone.get("phone") or "").strip()
        if not value or _looks_like_empty_address(value):
            continue
        if value in seen:
            continue
        seen.add(value)
        cleaned.append({
            "phone": value,
            "is_primary_phone": _normalise_address_check(phone.get("is_primary_phone"), default=1 if not cleaned else 0),
            "is_primary_mobile_no": _normalise_address_check(phone.get("is_primary_mobile_no"), default=0),
        })
    if cleaned:
        record["phone_nos"] = cleaned
    else:
        record.pop("phone_nos", None)


def _normalise_contact_emails(record: dict) -> None:
    emails = record.get("email_ids")
    if isinstance(emails, dict):
        emails = [emails]
    if not isinstance(emails, list):
        emails = []

    value = str(record.get("email_id") or record.get("email") or "").strip()
    if value and "@" in value:
        emails.append({"email_id": value, "is_primary": 1})

    cleaned = []
    seen = set()
    for email in emails:
        if isinstance(email, str):
            email = {"email_id": email}
        if not isinstance(email, dict):
            continue
        value = str(email.get("email_id") or "").strip()
        if not value or "@" not in value:
            continue
        key = value.lower()
        if key in seen:
            continue
        seen.add(key)
        cleaned.append({
            "email_id": value,
            "is_primary": _normalise_address_check(email.get("is_primary"), default=1 if not cleaned else 0),
        })
    if cleaned:
        record["email_ids"] = cleaned
    else:
        record.pop("email_ids", None)


def _contact_has_data(record: dict) -> bool:
    if record.get("phone_nos") or record.get("email_ids"):
        return True
    return bool(
        str(record.get("phone") or record.get("mobile_no") or record.get("email_id") or "").strip()
    )


def _contact_record_key(record: dict) -> tuple:
    first_link = (record.get("links") or [{}])[0]
    phones = tuple(sorted(p.get("phone") for p in (record.get("phone_nos") or []) if isinstance(p, dict)))
    emails = tuple(sorted(e.get("email_id") for e in (record.get("email_ids") or []) if isinstance(e, dict)))
    return (
        first_link.get("link_doctype"),
        first_link.get("link_name"),
        normalize_key(record.get("first_name") or ""),
        phones,
        emails,
    )


def _ensure_contact_steps_after_parties(plan: dict) -> None:
    party_indices = [
        idx
        for idx, step in enumerate(plan.get("steps") or [])
        if step.get("target_doctype") in CONTACT_LINK_CONFIG
    ]
    if not party_indices:
        return

    last_party_idx = max(party_indices)
    for step in list(plan.get("steps") or []):
        if step.get("target_doctype") != "Contact":
            continue
        idx = plan["steps"].index(step)
        if idx > last_party_idx:
            continue
        plan["steps"].pop(idx)
        if idx < last_party_idx:
            last_party_idx -= 1
        plan["steps"].insert(last_party_idx + 1, step)
        last_party_idx += 1


def _looks_like_template(value) -> bool:
    return bool(re.search(r"\{\{.*?\}\}", str(value or "")))


def _normalise_address_links(
    record: dict,
    party_link_lookup: dict[str, str] | None = None,
) -> list[dict]:
    links = record.get("links")
    if isinstance(links, dict):
        links = [links]
    elif isinstance(links, str):
        link_name = links.strip()
        link_doctype = _infer_address_link_doctype(link_name, party_link_lookup)
        links = [{"link_doctype": link_doctype, "link_name": link_name}] if link_name else []
    if not isinstance(links, list):
        link_doctype = record.get("links.link_doctype") or record.get("link_doctype")
        link_name = record.get("links.link_name") or record.get("link_name")
        if link_name and not link_doctype:
            link_doctype = _infer_address_link_doctype(link_name, party_link_lookup)
        links = [{"link_doctype": link_doctype, "link_name": link_name}] if link_doctype and link_name else []

    cleaned = []
    seen = set()
    for link in links:
        if isinstance(link, str):
            link_name = link.strip()
            link_doctype = _infer_address_link_doctype(link_name, party_link_lookup)
            link = {"link_doctype": link_doctype, "link_name": link_name}
        if not isinstance(link, dict):
            continue
        link_doctype = str(link.get("link_doctype") or "").strip()
        link_name = str(link.get("link_name") or "").strip()
        if link_name and not link_doctype:
            link_doctype = _infer_address_link_doctype(link_name, party_link_lookup)
        if not link_doctype or not link_name:
            continue
        key = (link_doctype, link_name)
        if key in seen:
            continue
        seen.add(key)
        cleaned.append({"link_doctype": link_doctype, "link_name": link_name})
    return cleaned


def _infer_address_link_doctype(link_name, party_link_lookup: dict[str, str] | None = None) -> str:
    link_name = str(link_name or "").strip()
    if not link_name:
        return ""
    lookup = party_link_lookup or {}
    return lookup.get(link_name) or lookup.get("__default_doctype__") or ""


def _parse_vietnamese_address(address_line: str) -> dict:
    parts = [part.strip(" .") for part in str(address_line or "").split(",") if part.strip(" .")]
    country = "Vietnam"
    if parts and normalize_key(parts[-1]) in {"viet nam", "vietnam", "vn"}:
        parts.pop()

    city = ""
    for part in reversed(parts):
        normalised = _normalise_group_match_text(part)
        if re.search(r"\b(thanh pho|tp|tinh)\b", normalised):
            city = _strip_vietnam_admin_prefix(part)
            break

    if not city and parts:
        city = _strip_vietnam_admin_prefix(parts[-1])

    return {
        "city": city or "Không xác định",
        "state": city or "",
        "country": country,
    }


def _strip_vietnam_admin_prefix(value: str) -> str:
    text = str(value or "").strip()
    text = re.sub(r"^(thành phố|thanh pho|tp\.?|tỉnh|tinh)\s*", "", text, flags=re.IGNORECASE).strip()
    text = re.sub(r"^tp\.\s*", "", text, flags=re.IGNORECASE).strip()
    return text


def _normalise_address_check(value, default: int = 0) -> int:
    if value in (None, ""):
        return default
    if value in (0, False):
        return 0
    if value in (1, True):
        return 1
    if isinstance(value, str):
        return 1 if value.strip().lower() in {"1", "true", "yes", "y"} else 0
    return int(bool(value))


def _party_address_line(record: dict, config: dict) -> str:
    for fieldname in config.get("address_fields") or ():
        value = str(record.get(fieldname) or "").strip()
        if value and not _looks_like_empty_address(value):
            return value
    return ""


def _party_link_name(record: dict, config: dict) -> str:
    for fieldname in config.get("name_fields") or ():
        value = str(record.get(fieldname) or "").strip()
        if value:
            return value
    return ""


def _looks_like_empty_address(value: str) -> bool:
    value = str(value or "").strip()
    if not value or value in {"-", "—", "–"}:
        return True
    if normalize_key(value) in {"none", "null", "na", "n a", "khong", "không"}:
        return True
    # Phone numbers (VN: 10-11 digits starting with 0; international: +84...)
    cleaned = re.sub(r"[\s\-\.\(\)\+]", "", value)
    if re.fullmatch(r"0\d{8,10}|84\d{9,10}|\+84\d{9,10}", cleaned):
        return True
    return False


def _address_record_key(record: dict) -> tuple[str, str, str, str]:
    links = record.get("links") or []
    first_link = links[0] if links and isinstance(links[0], dict) else {}
    return (
        str(first_link.get("link_doctype") or "").strip(),
        str(first_link.get("link_name") or "").strip(),
        normalize_key(record.get("address_type") or "Billing"),
        normalize_key(record.get("address_line1") or ""),
    )


def _coerce_plan_response(plan, fallback_doctype: str | None = None):
    """Accept common AI response variants and convert them to plan schema.

    Smart Plan asks for ``{"steps": [...]}``, but models may return a top-level
    list, wrap the plan under ``plan``/``import_plan``, or fall back to the
    earlier analysis shape ``{"target_doctype": ..., "mappings": [...]}``.
    """
    if isinstance(plan, list):
        return {"steps": plan}
    if not isinstance(plan, dict):
        return plan
    if plan.get("steps"):
        if isinstance(plan.get("steps"), dict):
            plan = dict(plan)
            plan["steps"] = list(plan["steps"].values())
        return plan

    for key in (
        "plan",
        "smart_plan",
        "import_plan",
        "migration_plan",
        "data_import_plan",
        "result",
        "output",
    ):
        value = plan.get(key)
        if isinstance(value, (dict, list)):
            coerced = _coerce_plan_response(value, fallback_doctype)
            if isinstance(coerced, dict) and coerced.get("steps"):
                if not coerced.get("plan_summary") and plan.get("plan_summary"):
                    coerced["plan_summary"] = plan.get("plan_summary")
                return coerced

    for key in ("plan_steps", "import_steps", "execution_steps", "actions"):
        value = plan.get(key)
        if isinstance(value, list):
            coerced = dict(plan)
            coerced["steps"] = value
            return coerced
        if isinstance(value, dict):
            coerced = dict(plan)
            coerced["steps"] = list(value.values())
            return coerced

    analysis_plan = _analysis_response_to_plan(plan, fallback_doctype)
    if analysis_plan:
        return analysis_plan

    if _looks_like_plan_step(plan):
        return {"plan_summary": plan.get("plan_summary") or plan.get("summary") or "", "steps": [plan]}

    return plan


def _analysis_response_to_plan(response: dict, fallback_doctype: str | None = None) -> dict | None:
    """Convert old analyze-style AI JSON into a one-step smart plan."""
    target_doctype = _clean_doctype_value(
        response.get("target_doctype")
        or response.get("doctype")
        or response.get("dt")
        or fallback_doctype
    )
    mappings = (
        response.get("mappings")
        or response.get("field_mappings")
        or response.get("columns")
        or []
    )
    records = response.get("records") or []
    if isinstance(records, dict):
        records = [records]

    if not target_doctype or (not mappings and not records):
        return None

    field_map = _mappings_to_field_map(mappings)

    if not field_map and not records:
        return None

    return {
        "plan_summary": response.get("plan_summary") or response.get("reason") or "",
        "steps": [
            {
                "title": response.get("title") or f"Tạo {target_doctype}",
                "description": response.get("description") or response.get("reason") or "",
                "target_doctype": target_doctype,
                "mode": "insert",
                "unique_key": response.get("unique_key") or _guess_unique_key(target_doctype),
                "preview_format": response.get("preview_format") or "table",
                "ignore_duplicates": response.get("ignore_duplicates", True),
                "deduplicate_by": response.get("deduplicate_by") or [],
                "fixed_values": response.get("defaults") or response.get("fixed_values") or {},
                "row_template": {
                    "source_filter": response.get("source_filter") or "skip_totals",
                    "field_map": field_map,
                } if field_map else {},
                "records": records,
            }
        ],
    }


def _coerce_step_mapping(step: dict) -> dict:
    """Convert step-level ``mappings`` aliases to ``row_template.field_map``."""
    row_template = step.get("row_template") or {}
    if isinstance(row_template, dict) and row_template.get("field_map"):
        normalised_template = _normalise_row_template(row_template)
        if normalised_template.get("field_map"):
            coerced = dict(step)
            coerced["row_template"] = normalised_template
            return coerced

    row_template = _normalise_row_template(row_template)
    if row_template.get("field_map"):
        coerced = dict(step)
        coerced["row_template"] = row_template
        return coerced

    mappings = step.get("mappings") or step.get("field_mappings") or step.get("columns")
    field_map = _mappings_to_field_map(mappings)
    if not field_map:
        return step

    coerced = dict(step)
    coerced["row_template"] = {
        "source_filter": step.get("source_filter") or "skip_totals",
        "field_map": field_map,
    }
    if not coerced.get("fixed_values") and isinstance(step.get("defaults"), dict):
        coerced["fixed_values"] = step.get("defaults")
    return coerced


def _normalise_row_template(row_template) -> dict:
    if not isinstance(row_template, dict):
        return {}
    field_map = row_template.get("field_map") or {}
    if not isinstance(field_map, dict):
        return {}

    normalised_field_map = {}
    for target_field, mapping in field_map.items():
        target_field = str(target_field or "").strip()
        if not target_field:
            continue
        if isinstance(mapping, str):
            normalised_field_map[target_field] = {
                "source_column": mapping,
                "transform": "direct",
            }
            continue
        if isinstance(mapping, dict):
            spec = dict(mapping)
            if "source_column" not in spec:
                for alias in ("source", "source_field", "column", "header"):
                    if spec.get(alias):
                        spec["source_column"] = spec.get(alias)
                        break
            spec.setdefault("transform", "direct")
            normalised_field_map[target_field] = spec

    if not normalised_field_map:
        return {}

    return {
        **row_template,
        "source_filter": row_template.get("source_filter") or "skip_totals",
        "field_map": normalised_field_map,
    }


def _mappings_to_field_map(mappings) -> dict:
    if isinstance(mappings, dict):
        mappings = [
            {"target_field": target, **(mapping if isinstance(mapping, dict) else {"source_column": mapping})}
            for target, mapping in mappings.items()
        ]
    if not isinstance(mappings, list):
        return {}

    field_map = {}
    for mapping in mappings:
        if not isinstance(mapping, dict):
            continue
        target_field = (
            mapping.get("target_field")
            or mapping.get("target_fieldname")
            or mapping.get("fieldname")
            or mapping.get("field")
        )
        target_field = str(target_field or "").strip()
        if not target_field or target_field.lower() in {"ignore", "skip", "none", "null"}:
            continue

        source_column = (
            mapping.get("source_column")
            or mapping.get("source_field")
            or mapping.get("source")
            or mapping.get("column")
            or mapping.get("header")
        )
        spec = {
            "source_column": source_column,
            "transform": mapping.get("transform") or "direct",
        }
        if mapping.get("default") not in (None, ""):
            spec["default"] = mapping.get("default")
        if mapping.get("value") not in (None, ""):
            spec["value"] = mapping.get("value")
        field_map[target_field] = spec
    return field_map


def _looks_like_plan_step(value: dict) -> bool:
    return bool(
        value.get("records")
        or value.get("row_template")
        or _clean_doctype_value(value.get("target_doctype"))
        or _clean_doctype_value(value.get("doctype"))
        or _clean_doctype_value(value.get("dt"))
    )


def _resolve_step_target_doctype(step: dict, fallback_doctype: str | None = None) -> str | None:
    """Resolve the target DocType from common AI output shapes.

    The requested schema uses ``target_doctype``, but models sometimes emit
    ``doctype`` at the step level, or only inside each record because Frappe
    documents themselves use a ``doctype`` key. Accept those shapes instead
    of failing with ``DocType 'None'``.
    """
    for key in ("target_doctype", "doctype", "dt"):
        value = _clean_doctype_value(step.get(key))
        if value:
            return value

    record_doctypes = {
        value
        for rec in (step.get("records") or [])
        if isinstance(rec, dict)
        for value in [_clean_doctype_value(rec.get("doctype"))]
        if value
    }
    if len(record_doctypes) == 1:
        return next(iter(record_doctypes))

    row_template = step.get("row_template") or {}
    if isinstance(row_template, dict):
        value = _clean_doctype_value(row_template.get("target_doctype") or row_template.get("doctype"))
        if value:
            return value

    value = _clean_doctype_value(fallback_doctype)
    if value:
        return value

    return None


def _clean_doctype_value(value) -> str | None:
    if not isinstance(value, str):
        return None
    value = value.strip()
    if not value or value.lower() in {"none", "null", "undefined"}:
        return None
    return value


def _materialise_records(row_template: dict, raw_records: list[dict], existing: list[dict]) -> list[dict]:
    """Apply ``row_template.field_map`` to every raw record to build the full
    list. ``existing`` is accepted for backwards compatibility; import data
    is generated from Python rules, not from AI-enumerated records.
    """
    field_map = row_template.get("field_map") or {}
    source_filter = (row_template.get("source_filter") or "all").lower()

    if not field_map:
        return existing or raw_records

    materialised: list[dict] = []
    for record in raw_records:
        if source_filter == "skip_totals" and _is_total_row(record):
            continue
        rendered = {}
        for target_field, mapping in field_map.items():
            if not isinstance(mapping, dict):
                continue
            if "value" in mapping and mapping["value"] not in (None, ""):
                rendered[target_field] = mapping["value"]
                continue
            source_column = mapping.get("source_column")
            value = _lookup_source(record, source_column) if source_column else None
            if value in (None, "") and mapping.get("default") not in (None, ""):
                value = mapping.get("default")
            transform = (mapping.get("transform") or "direct").strip()
            value = _apply_transform(value, transform, target_field=target_field)
            if value not in (None, ""):
                rendered[target_field] = value
        if rendered:
            materialised.append(rendered)

    return materialised


def _lookup_source(record: dict, source_column: str | None):
    if not source_column:
        return None
    if source_column in record:
        return record[source_column]
    target = normalize_key(source_column)
    for key, value in record.items():
        if normalize_key(key) == target:
            return value
    return None


def _apply_transform(value, transform: str, target_field: str | None = None):
    transform_key = normalize_key(transform or "")

    if target_field == "disabled":
        if value in (None, ""):
            return value
        if value in (0, False):
            return 0
        if value in (1, True):
            return 1
        if isinstance(value, str) and value.strip() in {"0", "1"}:
            return int(value.strip())
        value_key = normalize_key(str(value))
        if "đang sử dụng" in value_key or "dang su dung" in value_key:
            return 0
        if "ngừng" in value_key or "ngung" in value_key:
            return 1
        return 1

    if target_field == "is_stock_item":
        if value in (None, ""):
            return value
        if value in (0, False):
            return 0
        if value in (1, True):
            return 1
        if isinstance(value, str) and value.strip() in {"0", "1"}:
            return int(value.strip())
        value_key = normalize_key(str(value))
        return 0 if ("dịch vụ" in value_key or "dich vu" in value_key) else 1

    if value in (None, ""):
        return value
    transform = transform or "direct"

    if "numeric" in transform_key or "number" in transform_key or transform_key in {"int", "float"}:
        if isinstance(value, (int, float)):
            return value
        if isinstance(value, str):
            return _parse_vn_number(value)
        return value

    if transform == "direct":
        return value.strip() if isinstance(value, str) and "trim" in transform_key else value
    if transform == "strip" or "trim" in transform_key:
        return value.strip() if isinstance(value, str) else value
    if transform == "number":
        if isinstance(value, (int, float)):
            return value
        if isinstance(value, str):
            return _parse_vn_number(value)
        return value
    if transform.startswith("split:before:"):
        token = transform.split("split:before:", 1)[1]
        if isinstance(value, str) and token in value:
            return value.split(token, 1)[0].strip()
        return value
    if transform.startswith("split:after:"):
        token = transform.split("split:after:", 1)[1]
        if isinstance(value, str) and token in value:
            return value.split(token, 1)[1].strip()
        return value
    if transform.startswith("regex:"):
        pattern = transform.split("regex:", 1)[1]
        try:
            match = re.search(pattern, str(value))
            if match:
                return match.group(1) if match.groups() else match.group(0)
        except Exception:
            return value
    return value


def _is_total_row(record: dict) -> bool:
    for value in record.values():
        if isinstance(value, str):
            normalised = normalize_key(value)
            if normalised in {"tong", "tổng", "tong cong", "total", "cong", "cộng"}:
                return True
    return False


def _dedupe(records: list[dict], keys: list[str]) -> list[dict]:
    seen: set = set()
    out: list[dict] = []
    for rec in records:
        key = tuple(normalize_key(rec.get(k, "")) for k in keys)
        if key in seen:
            continue
        seen.add(key)
        out.append(rec)
    return out


def _normalise_record(record: dict) -> dict | None:
    cleaned: dict = {}
    for key, value in record.items():
        if key in {"doctype", "target_doctype", "dt"}:
            continue
        if isinstance(value, str):
            value = value.strip()
        if key not in TEXT_CODE_FIELDS and isinstance(value, str) and _looks_like_vn_number(value):
            value = _parse_vn_number(value)
        cleaned[key] = value
    if not any(value not in (None, "") for value in cleaned.values()):
        return None
    return cleaned


def _looks_like_vn_number(value: str) -> bool:
    if not value:
        return False
    stripped = value.replace(" ", "")
    if not re.fullmatch(r"-?[\d\.,]+", stripped):
        return False
    return ("." in value or "," in value) and any(char.isdigit() for char in value)


def _parse_vn_number(value: str):
    if not isinstance(value, str):
        return value
    cleaned = value.replace(" ", "")
    if "," in cleaned and "." in cleaned:
        if cleaned.rfind(",") > cleaned.rfind("."):
            cleaned = cleaned.replace(".", "").replace(",", ".")
        else:
            cleaned = cleaned.replace(",", "")
    elif "," in cleaned:
        cleaned = cleaned.replace(".", "").replace(",", ".")
    else:
        if cleaned.count(".") > 1:
            cleaned = cleaned.replace(".", "")
    try:
        if "." in cleaned:
            return float(cleaned)
        return int(cleaned)
    except Exception:
        return value


def _meta_has_field(doctype: str, fieldname: str) -> bool:
    try:
        return bool(frappe.get_meta(doctype).get_field(fieldname))
    except Exception:
        return False


def _guess_unique_key(doctype: str) -> str:
    candidates = {
        "Item": "item_code",
        "Customer": "customer_name",
        "Supplier": "supplier_name",
        "Asset Category": "asset_category_name",
        "Bank": "bank_name",
        "Bank Account": "bank_account_no",
        "Account": "account_number",
        "Item Group": "item_group_name",
        "Cost Center": "cost_center_name",
        "Department": "department_name",
        "Location": "location_name",
        "Warehouse": "warehouse_name",
        "UOM": "uom_name",
        "Project": "project_name",
    }
    return candidates.get(doctype, "name")


def _guess_label_field(doctype: str, records: list[dict]) -> str:
    candidates = ["item_name", "customer_name", "supplier_name", "bank_name",
                  "account_name", "department_name", "warehouse_name",
                  "item_group_name", "asset_category_name", "location_name",
                  "cost_center_name", "project_name", "title"]
    if records:
        for candidate in candidates:
            if candidate in records[0]:
                return candidate
    return "name"


def _first_sheet_name(summary: dict) -> str | None:
    sheets = summary.get("sheets") or []
    return sheets[0].get("sheet_name") if sheets else None


def _first_header_row(summary: dict) -> int | None:
    sheets = summary.get("sheets") or []
    return sheets[0].get("detected_header_row") if sheets else None


def _first_headers(summary: dict) -> list[str]:
    sheets = summary.get("sheets") or []
    return sheets[0].get("detected_headers") if sheets else []


def _sample_seed(file_row) -> str:
    return str(
        getattr(file_row, "source_hash", None)
        or getattr(file_row, "file_path", None)
        or getattr(file_row, "file_name", None)
        or "import-auto"
    )


def _source_row_count(summary: dict, sheet_name: str | None, header_row: int | None) -> int:
    for sheet in summary.get("sheets") or []:
        if sheet_name and sheet.get("sheet_name") != sheet_name:
            continue
        header = int(header_row or sheet.get("detected_header_row") or 1)
        return max(int(sheet.get("max_row") or 0) - header, 0)
    return 0


# ---------------------------------------------------------------------------
# Smart fix — given a failed plan + execution error, ask the AI to repair the
# offending records (e.g. fill missing parent_account derived from sibling
# rows in the same file). Returns the patched plan plus a list of explicit
# field-level changes for the UI diff.
# ---------------------------------------------------------------------------

VN_ACCOUNT_RULES = (
    "QUY TẮC HỆ THỐNG TÀI KHOẢN VIỆT NAM (TT200 / TT133):\n"
    "  • TK 3 chữ số (111, 112, 131, 331, 511, ...) = tài khoản cấp 1 (nhóm cha).\n"
    "    – parent_account = tài khoản root group đã tồn tại trong ERPNext\n"
    "      (vd '11 - Tiền và các khoản tương đương'). Nếu không tìm thấy → để null.\n"
    "    – is_group = 1.\n"
    "  • TK 4 chữ số (1111, 1112, 1121, ...) = tài khoản cấp 2.\n"
    "    – parent_account = TK 3 chữ số đầu (1111 → parent là TK 111,\n"
    "      1121 → parent là TK 112). Phải tra trong CHÍNH file Excel hoặc COA.\n"
    "    – is_group = 1 nếu file có TK con bắt đầu bằng số này, ngược lại 0.\n"
    "  • TK có dấu chấm (1121.20, 1121.21, 11210, 11211) = tài khoản chi tiết.\n"
    "    – Nếu có dấu chấm: parent = phần trước dấu chấm (1121.20 → 1121).\n"
    "    – Nếu 5 chữ số liền: parent = 4 chữ số đầu (11210 → 1121).\n"
    "    – is_group = 0 (tài khoản lá, dùng để ghi sổ).\n"
    "  • account_number, account_name, account_type, root_type, số dư đầu kỳ\n"
    "    của các dòng KHÔNG ĐƯỢC sửa. Chỉ được điền parent_account / is_group\n"
    "    / company / disabled còn thiếu.\n"
    "  • Khi suy ra parent_account: CHỈ được dùng giá trị account_number của\n"
    "    các dòng KHÁC trong cùng file Excel này. Tuyệt đối KHÔNG bịa parent\n"
    "    từ ngoài file. Nếu không tìm thấy parent phù hợp → ghi null và\n"
    "    thêm vào 'unresolved' kèm lý do.\n"
    "  • Nếu parent_account chưa tồn tại trong DB nhưng account_number đó có\n"
    "    trong cùng file Excel / cùng plan import, thì KHÔNG được tạo\n"
    "    NEW_DEPENDENCY_STEPS cho Account đó. Phải giữ dòng Account trong file\n"
    "    và sort cha trước con (vd 1121 phải đứng trước 1121.2).\n"
)


def _company_abbr_for(company: str | None) -> str:
    if not company:
        return ""
    try:
        return frappe.db.get_value("Company", company, "abbr") or ""
    except Exception:
        return ""


def _add_lookup_key(keys: set[str], value) -> None:
    text = str(value or "").strip()
    if not text:
        return
    keys.add(text)
    keys.add(normalize_key(text))


def _strip_account_company_suffix(value, company_abbr: str | None) -> str:
    text = str(value or "").strip()
    suffix = f" - {company_abbr}" if company_abbr else ""
    if suffix and text.endswith(suffix):
        return text[: -len(suffix)].strip()
    return text


def _leading_account_number(value) -> str:
    text = str(value or "").strip()
    match = re.match(r"^([0-9][0-9A-Za-z]*(?:\.[0-9A-Za-z]+)*)\b", text)
    return match.group(1) if match else ""


def _account_lookup_keys(value, company_abbr: str | None = None) -> set[str]:
    """Return tolerant lookup keys for Account link/reference values.

    Examples:
      "1121 - DCNET" -> {"1121 - DCNET", "1121", ...}
      "1121 - Tiền gửi - DCNET" -> {"1121 - Tiền gửi", "1121", ...}
    """
    keys: set[str] = set()
    text = str(value or "").strip()
    if not text:
        return keys

    candidates = {text, _strip_account_company_suffix(text, company_abbr)}
    for candidate in list(candidates):
        if " - " in candidate:
            candidates.add(candidate.split(" - ", 1)[0].strip())
        number = _leading_account_number(candidate)
        if number:
            candidates.add(number)

    for candidate in candidates:
        _add_lookup_key(keys, candidate)
    return keys


def _account_identity_keys(rec: dict, company_abbr: str | None = None) -> set[str]:
    keys: set[str] = set()
    if not isinstance(rec, dict):
        return keys

    account_number = str(rec.get("account_number") or "").strip()
    account_name = str(rec.get("account_name") or "").strip()
    explicit_name = str(rec.get("name") or "").strip()

    for value in (account_number, account_name, explicit_name):
        for key in _account_lookup_keys(value, company_abbr):
            _add_lookup_key(keys, key)

    if account_number and account_name:
        label = f"{account_number} - {account_name}"
        for key in _account_lookup_keys(label, company_abbr):
            _add_lookup_key(keys, key)
        if company_abbr:
            for key in _account_lookup_keys(f"{label} - {company_abbr}", company_abbr):
                _add_lookup_key(keys, key)
    elif account_name and company_abbr:
        for key in _account_lookup_keys(f"{account_name} - {company_abbr}", company_abbr):
            _add_lookup_key(keys, key)

    return keys


def _collect_plan_account_index(plan: dict, company: str | None = None) -> dict:
    company_abbr = _company_abbr_for(company)
    refs: set[str] = set()
    rows: list[dict] = []

    for step_idx, step in enumerate(plan.get("steps") or [], start=1):
        if not isinstance(step, dict) or step.get("target_doctype") != "Account":
            continue
        for row_idx, rec in enumerate(step.get("records") or [], start=1):
            if not isinstance(rec, dict):
                continue
            refs.update(_account_identity_keys(rec, company_abbr))
            rows.append({
                "step": step_idx,
                "row": row_idx,
                "account_number": rec.get("account_number"),
                "account_name": rec.get("account_name"),
            })

    return {"refs": refs, "rows": rows, "company_abbr": company_abbr}


def _pick_source_account_value(record: dict, candidate_headers: set[str]):
    for key, value in (record or {}).items():
        key_norm = normalize_key(key)
        if key_norm in candidate_headers:
            return value
    return None


def _build_source_account_index(raw_records: list[dict], company: str | None = None) -> dict:
    company_abbr = _company_abbr_for(company)
    number_headers = {
        "account number", "account_number", "ma tai khoan", "mã tài khoản",
        "ma tk", "mã tk", "so tai khoan", "số tài khoản",
        "so hieu tai khoan", "số hiệu tài khoản",
    }
    name_headers = {
        "account name", "account_name", "ten tai khoan", "tên tài khoản",
        "ten tk", "tên tk", "dien giai", "diễn giải",
    }

    refs: set[str] = set()
    rows: list[dict] = []
    for row_idx, record in enumerate(raw_records or [], start=1):
        if not isinstance(record, dict):
            continue
        account_number = _pick_source_account_value(record, number_headers)
        account_name = _pick_source_account_value(record, name_headers)
        compact = {
            "account_number": str(account_number or "").strip(),
            "account_name": str(account_name or "").strip(),
        }
        if not compact["account_number"] and not compact["account_name"]:
            continue
        refs.update(_account_identity_keys(compact, company_abbr))
        rows.append({"source_row": row_idx, **compact})

    return {"refs": refs, "rows": rows, "company_abbr": company_abbr}


def _account_ref_present(value, *indexes: dict) -> bool:
    if not value:
        return False
    for index in indexes:
        refs = index.get("refs") if isinstance(index, dict) else None
        if not refs:
            continue
        company_abbr = index.get("company_abbr") if isinstance(index, dict) else ""
        if _account_lookup_keys(value, company_abbr) & refs:
            return True
    return False


def _compact_account_index_for_ai(index: dict, limit: int = 200) -> dict:
    rows = index.get("rows") if isinstance(index, dict) else []
    return {
        "total_accounts_seen": len(rows or []),
        "rows": (rows or [])[:limit],
        "truncated": len(rows or []) > limit,
    }


def fix_plan_errors(doc, file_row, plan: dict, error_info: dict,
                    progress_callback=None) -> dict:
    """Ask the AI to repair a plan that failed during execution.

    To keep the AI response small (avoiding JSON truncation), we ONLY ask the
    model for a list of ``patches`` (field-level edits). The server then
    applies those patches to the original plan, enforcing the
    allowed/protected whitelists.
    """
    if not isinstance(plan, dict) or not plan.get("steps"):
        return {"error": "Plan rỗng, không có gì để sửa."}
    if not isinstance(error_info, dict):
        error_info = {}

    config = _get_ai_config(doc)
    if not config.api_key or not config.enabled:
        return {"error": "Chưa cấu hình AI hoặc API key trống."}

    def progress(stage: str, percent: int, message: str):
        if callable(progress_callback):
            try:
                progress_callback(stage=stage, percent=percent, message=message)
            except Exception:
                pass

    progress("reading", 10, "Đang đọc lại tệp Excel để có context...")

    raw_records: list[dict] = []
    sampled_sources: list[dict] = []
    try:
        sample_seed = _sample_seed(file_row)
        summary = summarize_workbook(
            file_row.file_path,
            max_sample_rows=SAMPLE_ROWS_FOR_AI,
            sample_strategy="random",
            sample_seed=sample_seed,
        )
        analysis: dict = {}
        if file_row.analysis_json:
            try:
                analysis = json.loads(file_row.analysis_json)
            except Exception:
                analysis = {}
        sheet_name = analysis.get("sheet_name") or _first_sheet_name(summary)
        header_row = analysis.get("header_row_number") or _first_header_row(summary)
        if sheet_name and header_row:
            raw_records = extract_records(file_row.file_path, sheet_name, header_row)
            sampled_sources = sample_excel_records(
                file_row.file_path,
                sheet_name,
                header_row,
                sample_size=SMART_FIX_MAX_SAMPLE_RECORDS,
                seed=sample_seed,
            )
    except Exception:
        frappe.log_error(frappe.get_traceback(), "Smart Fix Extract Failed")

    try:
        from dcnet_migrate.import_auto.services.smart_executor import (
            _apply_pre_execution_plan_invariants,
            _expand_sampled_plan_from_analysis,
        )

        plan = _expand_sampled_plan_from_analysis(doc, file_row, plan)
        _apply_pre_execution_plan_invariants(doc, plan)
    except Exception:
        frappe.log_error(frappe.get_traceback(), "Smart Fix Plan Expansion Failed")

    progress("preparing", 25, "Đang chuẩn bị bối cảnh cho AI...")

    # Compress plan context — only send id + key fields of each record, not the
    # whole record dump. This is what the AI needs to know to compute parents.
    compact_plan = _compact_plan_for_fix(plan)
    sample_sources = sampled_sources or raw_records[:SMART_FIX_MAX_SAMPLE_RECORDS]
    source_account_index = _build_source_account_index(raw_records, doc.company)
    plan_account_index = _collect_plan_account_index(plan, doc.company)

    progress("scanning", 40, "Đang phát hiện dữ liệu phụ thuộc còn thiếu...")
    dependency_hints = _detect_missing_dependencies(
        plan,
        error_info,
        doc,
        source_account_index=source_account_index,
        plan_account_index=plan_account_index,
    )

    system_prompt = _build_fix_system_prompt()
    user_payload = {
        "company": doc.company,
        "file_name": file_row.file_name,
        "error": {
            "message": error_info.get("error") or error_info.get("message") or "",
            "step": error_info.get("failed_step_index"),
            "row": error_info.get("failed_row_index"),
            "record": error_info.get("failed_record"),
            "error_type": error_info.get("error_type"),
        },
        "plan_compact": compact_plan,
        "source_sample": sample_sources,
        "source_account_index": _compact_account_index_for_ai(source_account_index),
        "plan_account_index": _compact_account_index_for_ai(plan_account_index),
        "allowed_fields": sorted(SMART_FIX_ALLOWED_FIELDS),
        "protected_fields": sorted(SMART_FIX_PROTECTED_FIELDS),
        "dependency_doctypes_allowed": sorted(SMART_FIX_DEPENDENCY_ALLOWED_DOCTYPES),
        "dependency_hints": dependency_hints,
        "output_schema": {
            "patches": [
                {
                    "step": "step index (int, 1-based)",
                    "row": "row index trong step.records (int, 1-based)",
                    "field": "fieldname trong allowed_fields",
                    "value": "giá trị mới",
                    "reason": "lý do tiếng Việt, ngắn gọn",
                }
            ],
            "new_dependency_steps": [
                {
                    "target_doctype": "ERPNext DocType (PHẢI nằm trong dependency_doctypes_allowed)",
                    "reason": "Vì sao cần tạo trước (tiếng Việt)",
                    "insert_before_step": "step index của step bị lỗi (int, 1-based)",
                    "unique_key": "fieldname dùng để khử trùng (vd: department_name)",
                    "records": [
                        {"fieldname": "value"}
                    ]
                }
            ],
            "unresolved": [
                {"step": "int", "row": "int", "reason": "lý do AI không xử lý"}
            ],
        },
    }

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": truncate_text(
            json.dumps(user_payload, ensure_ascii=False, default=str),
            max_length=30000,
        )},
    ]

    progress("thinking", 55, "AI đang phân tích lỗi và đề xuất sửa...")

    timeout_seconds = max(int(config.timeout_seconds or 60), SMART_FIX_TIMEOUT_FLOOR)
    try:
        raw = _chat_completion(
            config.api_base_url,
            config.model,
            config.api_key,
            messages,
            timeout_seconds,
        )
        response = _safe_parse_patches(raw)
    except Exception as exc:
        frappe.log_error(frappe.get_traceback(), "Smart Fix AI Failed")
        return {"error": f"AI không sửa được: {exc}"}

    progress("applying", 85, "Đang áp dụng các thay đổi vào plan...")

    merged = _apply_fix_patches(
        plan,
        response,
        doc=doc,
        source_account_index=source_account_index,
    )

    progress("complete", 100, "Đã sửa xong, đang tải bản xem so sánh...")
    return merged


def _build_fix_system_prompt() -> str:
    return (
        "Bạn là chuyên gia data migration ERPNext v16 cho Việt Nam.\n"
        "Bạn nhận: (1) plan import đã thất bại (dạng nén), (2) thông báo lỗi của Frappe, "
        "(3) tối đa 10 sample records random gốc từ file Excel, "
        "(4) source_account_index/plan_account_index cho biết tài khoản nào đã có trong file/plan, "
        "(5) danh sách 'dependency_hints' liệt kê các giá trị Link mà plan tham chiếu nhưng KHÔNG tồn tại trong DB.\n"
        "Nhiệm vụ: chọn 1 trong 3 cách sửa:\n"
        "  (A) PATCHES — sửa field-level trong records đã có (allowed_fields).\n"
        "  (B) NEW_DEPENDENCY_STEPS — tạo TRƯỚC các bản ghi master data còn thiếu "
        "      (vd: Department, Designation, UOM, Item Group...). KHÔNG được dùng cho transactional doctype.\n"
        "  (C) UNRESOLVED — không xử lý được, để user tự xử lý.\n"
        "\n"
        + VN_ACCOUNT_RULES +
        "\n"
        "RÀNG BUỘC CỨNG cho PATCHES (A):\n"
        "  1. CHỈ được patch field nằm trong 'allowed_fields'.\n"
        "  2. KHÔNG được patch field trong 'protected_fields'.\n"
        "  3. Mỗi patch phải có (step, row, field, value, reason).\n"
        "  3b. Với Item bị thiếu mandatory field, có thể fill các field master-data an toàn "
        "như stock_uom, item_group, is_stock_item/is_purchase_item/is_sales_item. "
        "Ưu tiên giá trị có trong source_sample hoặc failed_record; nếu không có, dùng "
        "giá trị master mặc định đã tồn tại/phổ biến trên ERPNext (vd stock_uom='Nos', "
        "item_group='All Item Groups') và KHÔNG sửa item_code/item_name.\n"
        "  3c. Với Customer/Supplier bị thiếu nhóm/territory, chỉ được fill "
        "customer_group/supplier_group/territory khi field hiện đang rỗng.\n"
        "\n"
        "RÀNG BUỘC CỨNG cho NEW_DEPENDENCY_STEPS (B):\n"
        "  4. target_doctype PHẢI nằm trong 'dependency_doctypes_allowed'.\n"
        "  5. Mỗi step có 'insert_before_step' = step index của step lỗi (1-based).\n"
        "  6. Records phải dùng đúng fieldname ERPNext (vd: department_name + company cho Department, "
        "     designation_name cho Designation, uom_name cho UOM, item_group_name + parent_item_group cho Item Group).\n"
        "     Với Asset Category dùng asset_category_name; nếu chưa có COA thì có thể đặt non_depreciable_category=1 "
        "để tạo placeholder trước, sau đó user gắn tài khoản kế toán sau khi import COA. "
        "Với Location dùng location_name. Với Cost Center dùng cost_center_name + company; "
        "nếu tạo cost center con thì cần parent_cost_center là root company.\n"
        "  7. Chỉ tạo các giá trị xuất hiện thực sự trong 'dependency_hints' hoặc bản ghi lỗi — "
        "     KHÔNG bịa thêm record.\n"
        "  8. 'unique_key' = fieldname dùng để khử trùng (vd: department_name).\n"
        "  9. 'reason' bằng tiếng Việt, giải thích rõ vì sao cần.\n"
        "  9b. Với DocType Account: KHÔNG được tạo dependency cho tài khoản đã xuất hiện "
        "trong source_account_index hoặc plan_account_index. Đây là lỗi thứ tự cây, "
        "không phải thiếu master data.\n"
        "\n"
        "RÀNG BUỘC CHUNG:\n"
        " 10. Record không sửa được bằng (A) hay (B) → đưa vào 'unresolved'.\n"
        " 11. Output STRICT JSON: "
        "     {\"patches\": [...], \"new_dependency_steps\": [...], \"unresolved\": [...]}\n"
        " 12. KHÔNG bọc bằng markdown, KHÔNG kèm văn bản ngoài JSON.\n"
    )


def _compact_plan_for_fix(plan: dict) -> dict:
    """Strip plan down to (step_index, target_doctype, records[i].keys_with_values).

    The AI doesn't need full record metadata — only enough to reason about
    which row needs which patch. We also include the key identifying fields
    (account_number, account_name, item_code, ...) so the AI can correlate
    rows with the source file.
    """
    compact_steps = []
    for step_idx, step in enumerate(plan.get("steps") or [], start=1):
        records = step.get("records") or []
        compact_records = []
        for row_idx, rec in enumerate(records, start=1):
            if not isinstance(rec, dict):
                continue
            # Keep only protected fields (identifiers) + currently-set allowed
            # fields so the AI sees what's already there.
            kept = {}
            for key, value in rec.items():
                if key in SMART_FIX_PROTECTED_FIELDS or key in SMART_FIX_ALLOWED_FIELDS:
                    kept[key] = value
            compact_records.append({"row": row_idx, "fields": kept})
        compact_steps.append({
            "step": step_idx,
            "title": step.get("title"),
            "target_doctype": step.get("target_doctype"),
            "record_count": len(records),
            "records_compact": compact_records[:200],  # hard cap for safety
            "records_truncated": len(compact_records) > 200,
        })
    return {
        "total_steps": len(plan.get("steps") or []),
        "steps": compact_steps,
    }


def _safe_parse_patches(raw: str) -> dict:
    """Parse AI patch response with multiple fallbacks (truncation-tolerant)."""
    import re as _re

    text = (raw or "").strip()
    if not text:
        return {"patches": [], "unresolved": []}

    # Remove common markdown fences.
    if text.startswith("```"):
        text = _re.sub(r"^```[a-zA-Z]*\n", "", text)
        if text.endswith("```"):
            text = text[:-3]
        text = text.strip()

    # Try direct parse first.
    try:
        parsed = json.loads(text)
        if isinstance(parsed, dict):
            return parsed
    except Exception:
        pass

    # Try to extract just the patches array (most resilient against truncation).
    patches_match = _re.search(r'"patches"\s*:\s*\[', text)
    if patches_match:
        start = patches_match.end() - 1  # at '['
        # Walk forward, balancing brackets, to find a complete array.
        depth = 0
        end = None
        in_str = False
        escape = False
        for i in range(start, len(text)):
            ch = text[i]
            if escape:
                escape = False
                continue
            if ch == "\\":
                escape = True
                continue
            if ch == '"':
                in_str = not in_str
                continue
            if in_str:
                continue
            if ch == "[":
                depth += 1
            elif ch == "]":
                depth -= 1
                if depth == 0:
                    end = i + 1
                    break
        if end is not None:
            try:
                patches = json.loads(text[start:end])
                return {"patches": patches, "unresolved": []}
            except Exception:
                pass
        else:
            # Truncated array — try to salvage complete objects inside.
            salvage = _salvage_objects(text[start + 1:])
            if salvage:
                return {"patches": salvage, "unresolved": [],
                        "_truncated": True}

    # Final fallback — find any JSON object in text.
    try:
        match = _re.search(r"\{.*\}", text, flags=_re.S)
        if match:
            return json.loads(match.group(0))
    except Exception:
        pass

    return {"patches": [], "unresolved": [],
            "_parse_error": "AI trả về JSON không hợp lệ (có thể đã bị cắt). Đã bỏ qua các patch không parse được."}


def _salvage_objects(text: str) -> list[dict]:
    """Extract complete top-level JSON objects from a possibly truncated string."""
    import re as _re

    out = []
    depth = 0
    obj_start = None
    in_str = False
    escape = False
    for i, ch in enumerate(text):
        if escape:
            escape = False
            continue
        if ch == "\\":
            escape = True
            continue
        if ch == '"':
            in_str = not in_str
            continue
        if in_str:
            continue
        if ch == "{":
            if depth == 0:
                obj_start = i
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0 and obj_start is not None:
                snippet = text[obj_start:i + 1]
                try:
                    parsed = json.loads(snippet)
                    if isinstance(parsed, dict):
                        out.append(parsed)
                except Exception:
                    pass
                obj_start = None
    return out


def _apply_fix_patches(
    original_plan: dict,
    response: dict,
    doc=None,
    source_account_index: dict | None = None,
) -> dict:
    """Apply patches from AI to the plan, enforcing whitelists server-side."""
    if not isinstance(response, dict):
        response = {}

    patches = response.get("patches") or []
    unresolved = response.get("unresolved") or []
    parse_warning = response.get("_parse_error")

    if not isinstance(patches, list):
        patches = []

    # Deep-copy plan so we don't mutate caller's object.
    import copy as _copy
    new_plan = _copy.deepcopy(original_plan)
    steps = new_plan.get("steps") or []

    applied: list[dict] = []
    rejected: list[dict] = []

    for patch in patches:
        if not isinstance(patch, dict):
            continue
        step_idx = patch.get("step")
        row_idx = patch.get("row")
        field = patch.get("field")
        new_value = patch.get("value")
        reason = patch.get("reason") or ""

        try:
            step_idx = int(step_idx)
            row_idx = int(row_idx)
        except (TypeError, ValueError):
            rejected.append({"step": step_idx, "row": row_idx, "field": field,
                             "reason": "step/row không phải số."})
            continue

        if not field or not isinstance(field, str):
            rejected.append({"step": step_idx, "row": row_idx, "field": field,
                             "reason": "field rỗng."})
            continue

        if field in SMART_FIX_PROTECTED_FIELDS:
            rejected.append({"step": step_idx, "row": row_idx, "field": field,
                             "reason": "Field bảo vệ (source-of-truth) — từ chối."})
            continue
        if field not in SMART_FIX_ALLOWED_FIELDS:
            rejected.append({"step": step_idx, "row": row_idx, "field": field,
                             "reason": "Field ngoài whitelist — từ chối."})
            continue

        if step_idx < 1 or step_idx > len(steps):
            rejected.append({"step": step_idx, "row": row_idx, "field": field,
                             "reason": "step index ngoài phạm vi."})
            continue
        step = steps[step_idx - 1]
        records = step.get("records") or []
        if row_idx < 1 or row_idx > len(records):
            rejected.append({"step": step_idx, "row": row_idx, "field": field,
                             "reason": "row index ngoài phạm vi."})
            continue

        record = records[row_idx - 1]
        if not isinstance(record, dict):
            rejected.append({"step": step_idx, "row": row_idx, "field": field,
                             "reason": "record không phải dict."})
            continue

        original_value = record.get(field)
        if original_value == new_value:
            continue
        # Allow overwriting parent_account / is_group even when present (often
        # the AI is replacing a wrong inferred value). Other allowed fields are
        # only filled when missing.
        if (original_value not in (None, "")
                and field not in ("parent_account", "is_group")):
            rejected.append({"step": step_idx, "row": row_idx, "field": field,
                             "reason": "Field đã có giá trị — chỉ fill khi rỗng."})
            continue

        record[field] = new_value
        applied.append({
            "step": step_idx,
            "row": row_idx,
            "field": field,
            "before": original_value,
            "after": new_value,
            "reason": reason,
        })

    # Re-run deterministic COA invariants after patches so same-file parent
    # fixes are sorted before retrying execution.
    if doc:
        _post_process_coa_plan(new_plan, doc)
        _post_process_bank_account_plan(new_plan, doc)
        _post_process_group_link_plan(new_plan)
        _post_process_address_plan(new_plan)
        _post_process_contact_plan(new_plan)
        _post_process_item_catalog_plan(new_plan)

    # Refresh per-step record counts and total.
    new_total = 0
    for step in steps:
        cnt = len(step.get("records") or [])
        step["record_count"] = cnt
        new_total += cnt
    new_plan["total_records"] = new_total
    new_plan["total_steps"] = len(steps)

    # Normalise AI-proposed dependency steps (DO NOT insert into plan yet —
    # user must confirm in UI first). The frontend will call
    # `confirm_dependency_steps` to commit.
    dep_proposals, dep_rejected = _normalise_dependency_proposals(
        response.get("new_dependency_steps") or [],
        new_plan,
        doc=doc,
        source_account_index=source_account_index,
    )

    result = {
        "plan": new_plan,
        "fixes": applied,
        "rejected": rejected + dep_rejected,
        "unresolved": unresolved if isinstance(unresolved, list) else [],
        "new_dependency_steps": dep_proposals,
    }
    if parse_warning:
        result["warning"] = parse_warning
    return result


def _normalise_dependency_proposals(
    raw_steps: list,
    plan: dict,
    doc=None,
    source_account_index: dict | None = None,
) -> tuple[list[dict], list[dict]]:
    """Validate AI-proposed dependency steps server-side.

    Returns (accepted_proposals, rejected_reasons). Records are NOT inserted
    into the plan here — only normalised. The UI dialog uses these to ask
    the user for confirmation; `confirm_dependency_steps` actually merges
    them into the plan.
    """
    accepted: list[dict] = []
    rejected: list[dict] = []
    plan_steps = plan.get("steps") or []
    plan_account_index = _collect_plan_account_index(
        plan,
        getattr(doc, "company", None) if doc else None,
    )
    source_account_index = source_account_index or {}

    for idx, raw in enumerate(raw_steps or [], start=1):
        if not isinstance(raw, dict):
            rejected.append({"field": "new_dependency_steps", "row": idx,
                             "reason": "Bước phụ thuộc không phải object."})
            continue

        target_doctype = (raw.get("target_doctype") or "").strip()
        if target_doctype not in SMART_FIX_DEPENDENCY_ALLOWED_DOCTYPES:
            rejected.append({"field": "new_dependency_steps", "row": idx,
                             "reason": f"DocType '{target_doctype}' không nằm trong whitelist được phép tạo tự động."})
            continue
        if not frappe.db.exists("DocType", target_doctype):
            rejected.append({"field": "new_dependency_steps", "row": idx,
                             "reason": f"DocType '{target_doctype}' không tồn tại trên site này."})
            continue

        records = raw.get("records") or []
        if not isinstance(records, list) or not records:
            rejected.append({"field": "new_dependency_steps", "row": idx,
                             "reason": "Không có record nào để tạo."})
            continue
        if len(records) > SMART_FIX_MAX_DEPENDENCY_RECORDS:
            rejected.append({"field": "new_dependency_steps", "row": idx,
                             "reason": f"Vượt giới hạn {SMART_FIX_MAX_DEPENDENCY_RECORDS} record/bước phụ thuộc."})
            continue

        unique_key = _normalise_dependency_unique_key(
            target_doctype,
            (raw.get("unique_key") or _guess_unique_key(target_doctype)).strip(),
        )
        insert_before = raw.get("insert_before_step")
        try:
            insert_before = int(insert_before) if insert_before is not None else None
        except (TypeError, ValueError):
            insert_before = None
        if insert_before is None or insert_before < 1 or insert_before > len(plan_steps):
            insert_before = max(1, len(plan_steps))

        clean_records: list[dict] = []
        seen_keys: set = set()
        for rec_idx, rec in enumerate(records, start=1):
            if not isinstance(rec, dict):
                rejected.append({"field": "new_dependency_steps", "row": f"{idx}.{rec_idx}",
                                 "reason": "Record không phải dict."})
                continue
            normalised = {}
            for k, v in rec.items():
                if not k or k.startswith("__"):
                    continue
                if isinstance(v, str):
                    v = v.strip()
                if v in (None, ""):
                    continue
                normalised[k] = v
            normalised = _normalise_dependency_record(target_doctype, normalised, doc=doc)
            if not normalised:
                continue
            # Dedup by unique_key
            key_value = normalised.get(unique_key)
            if key_value in seen_keys:
                continue
            if key_value:
                seen_keys.add(key_value)
            clean_records.append(normalised)

        if not clean_records:
            rejected.append({"field": "new_dependency_steps", "row": idx,
                             "reason": "Tất cả record sau khi chuẩn hoá đều rỗng."})
            continue

        clean_records = _prepare_dependency_records_for_doctype(target_doctype, clean_records, doc=doc)
        if not clean_records:
            rejected.append({"field": "new_dependency_steps", "row": idx,
                             "reason": "Không còn record hợp lệ sau khi chuẩn hoá theo DocType."})
            continue

        if target_doctype == "Account":
            filtered_records = []
            duplicate_accounts = []
            company_abbr = plan_account_index.get("company_abbr")
            plan_refs = plan_account_index.get("refs") or set()
            source_refs = source_account_index.get("refs") or set()
            for rec in clean_records:
                identity_keys = _account_identity_keys(rec, company_abbr)
                if identity_keys & (plan_refs | source_refs):
                    duplicate_accounts.append(
                        rec.get("account_number") or rec.get("account_name") or rec.get("name")
                    )
                    continue
                filtered_records.append(rec)

            if duplicate_accounts:
                rejected.append({
                    "field": "new_dependency_steps",
                    "row": idx,
                    "reason": (
                        "Từ chối tạo Account phụ thuộc vì tài khoản đã có trong cùng plan/file: "
                        + ", ".join(str(v) for v in duplicate_accounts[:10] if v)
                    ),
                })
            clean_records = filtered_records
            if not clean_records:
                continue

        # Filter out records that already exist in DB (no need to recreate)
        records_to_create: list[dict] = []
        records_existing: list[dict] = []
        for rec in clean_records:
            key_value = rec.get(unique_key)
            exists = False
            if key_value:
                try:
                    if unique_key == "name":
                        exists = bool(frappe.db.exists(target_doctype, key_value))
                    else:
                        exists = bool(frappe.db.exists(target_doctype, {unique_key: key_value}))
                except Exception:
                    exists = False
            if exists:
                records_existing.append(rec)
            else:
                records_to_create.append(rec)

        if not records_to_create:
            # Nothing to do — record already exists. Don't propose a step.
            continue

        # Auto-label
        label_field = _guess_label_field(target_doctype, records_to_create)

        accepted.append({
            "proposal_id": f"dep_{idx}",
            "target_doctype": target_doctype,
            "reason": (raw.get("reason") or "").strip(),
            "insert_before_step": insert_before,
            "unique_key": unique_key,
            "label_field": label_field,
            "ignore_mandatory": _dependency_step_needs_ignore_mandatory(target_doctype, records_to_create),
            "records": records_to_create,
            "record_count": len(records_to_create),
            "already_exists_count": len(records_existing),
        })

    return accepted, rejected


def _normalise_dependency_unique_key(target_doctype: str, unique_key: str) -> str:
    aliases = {
        "Asset Category": {"name", "asset_category"},
        "Location": {"name", "location"},
        "Cost Center": {"name", "cost_center"},
    }
    if unique_key in aliases.get(target_doctype, set()):
        return _guess_unique_key(target_doctype)
    return unique_key or _guess_unique_key(target_doctype)


def _normalise_dependency_record(target_doctype: str, rec: dict, doc=None) -> dict:
    rec = dict(rec or {})
    company = getattr(doc, "company", None) if doc else None

    if target_doctype == "Asset Category":
        label = (
            rec.get("asset_category_name")
            or rec.get("asset_category")
            or rec.get("name")
        )
        label = frappe.as_unicode(label or "").strip()
        if not label:
            return {}
        return {
            "asset_category_name": label,
            "non_depreciable_category": int(bool(rec.get("non_depreciable_category", 1))),
        }

    if target_doctype == "Location":
        label = rec.get("location_name") or rec.get("location") or rec.get("name")
        label = frappe.as_unicode(label or "").strip()
        if not label:
            return {}
        normalised = {"location_name": label}
        if rec.get("parent_location"):
            normalised["parent_location"] = rec.get("parent_location")
        normalised["is_group"] = int(bool(rec.get("is_group", 0)))
        return normalised

    if target_doctype == "Cost Center":
        label = rec.get("cost_center_name") or rec.get("cost_center") or rec.get("name")
        label = frappe.as_unicode(label or "").strip()
        if not label:
            return {}
        normalised = {
            "cost_center_name": label,
            "company": rec.get("company") or company,
            "disabled": int(bool(rec.get("disabled", 0))),
        }
        if rec.get("cost_center_number"):
            normalised["cost_center_number"] = rec.get("cost_center_number")
        if rec.get("parent_cost_center"):
            normalised["parent_cost_center"] = rec.get("parent_cost_center")
        if rec.get("is_group") not in (None, ""):
            normalised["is_group"] = int(bool(rec.get("is_group")))
        return normalised

    return rec


def _prepare_dependency_records_for_doctype(target_doctype: str, records: list[dict], doc=None) -> list[dict]:
    if target_doctype != "Cost Center":
        return records

    company = getattr(doc, "company", None) if doc else None
    if not company:
        return records

    abbr = _company_abbr_for(company)
    root_name = f"{company} - {abbr}" if abbr else company
    prepared: list[dict] = []
    needs_root = False
    has_root_record = False

    for rec in records:
        rec = dict(rec)
        rec.setdefault("company", company)
        cost_center_name = frappe.as_unicode(rec.get("cost_center_name") or "").strip()
        if not cost_center_name:
            continue

        if cost_center_name == company:
            has_root_record = True
            rec["is_group"] = 1
            rec.pop("parent_cost_center", None)
        else:
            needs_root = True
            rec.setdefault("parent_cost_center", root_name)
            rec.setdefault("is_group", 0)
        prepared.append(rec)

    if needs_root and not has_root_record:
        root_exists = bool(frappe.db.exists(
            "Cost Center",
            {"company": company, "cost_center_name": company},
        ))
        if not root_exists:
            prepared.insert(0, {
                "cost_center_name": company,
                "company": company,
                "is_group": 1,
                "disabled": 0,
            })

    deduped: list[dict] = []
    seen: set[tuple[str, str]] = set()
    for rec in prepared:
        key = (frappe.as_unicode(rec.get("company") or ""), frappe.as_unicode(rec.get("cost_center_name") or ""))
        if key in seen:
            continue
        seen.add(key)
        deduped.append(rec)
    return deduped


def _dependency_step_needs_ignore_mandatory(target_doctype: str, records: list[dict]) -> bool:
    if target_doctype == "Asset Category":
        return any(not rec.get("accounts") for rec in records or [])
    if target_doctype == "Cost Center":
        return any(
            rec.get("is_group") and not rec.get("parent_cost_center")
            for rec in records or []
        )
    return False


def _detect_missing_dependencies(
    plan: dict,
    error_info: dict,
    doc,
    source_account_index: dict | None = None,
    plan_account_index: dict | None = None,
) -> dict:
    """Scan the plan for Link fields whose referenced master data does NOT
    exist in the DB yet. Returns a structure the AI can use to know exactly
    which Department / Designation / etc. values are missing.

    Format::

        {
            "Department": {"missing_values": ["PHÒNG KỸ THUẬT HẠ TẦNG", ...],
                             "via_fields": ["department"],
                             "doctype_exists": true},
            ...
        }
    """
    hints: dict[str, dict] = {}
    company = doc.company
    source_account_index = source_account_index or {}
    plan_account_index = plan_account_index or _collect_plan_account_index(plan, company)
    _meta_cache: dict[str, object] = {}

    def _get_meta_cached(doctype: str):
        if doctype not in _meta_cache:
            _meta_cache[doctype] = frappe.get_meta(doctype)
        return _meta_cache[doctype]

    for step in plan.get("steps") or []:
        target_doctype = step.get("target_doctype")
        if not target_doctype or not frappe.db.exists("DocType", target_doctype):
            continue
        try:
            meta = _get_meta_cached(target_doctype)
        except Exception:
            continue

        link_fields = [
            df for df in meta.fields
            if df.fieldtype == "Link"
            and df.options in SMART_FIX_DEPENDENCY_ALLOWED_DOCTYPES
        ]
        if not link_fields:
            continue

        for rec in step.get("records") or []:
            if not isinstance(rec, dict):
                continue
            for df in link_fields:
                value = rec.get(df.fieldname)
                if value in (None, ""):
                    continue
                if not isinstance(value, str):
                    continue
                value = value.strip()
                if not value:
                    continue

                # COA imports create parent Accounts within the same plan/file.
                # If parent_account points to an Account number/name that is
                # present there, it is an ordering problem, not missing DB data.
                if (
                    df.options == "Account"
                    and _account_ref_present(value, plan_account_index, source_account_index)
                ):
                    continue

                bucket = hints.setdefault(df.options, {
                    "missing_values": [],
                    "via_fields": set(),
                    "doctype_exists": True,
                    "seen_values": set(),
                })
                bucket["via_fields"].add(df.fieldname)
                if value in bucket["seen_values"]:
                    continue
                bucket["seen_values"].add(value)

                # Check existence — consider Company-scoped DocTypes
                exists = False
                try:
                    if frappe.db.exists(df.options, value):
                        exists = True
                    elif company:
                        # Try Company-scoped lookup
                        meta_dep = _get_meta_cached(df.options)
                        has_company = any(f.fieldname == "company" for f in meta_dep.fields)
                        if has_company:
                            exists = bool(frappe.db.exists(df.options,
                                                            {"name": value, "company": company}))
                except Exception:
                    exists = False

                if not exists:
                    bucket["missing_values"].append({
                        "value": value,
                        "via_field": df.fieldname,
                    })

    # Strip sets for JSON serialisation, limit list sizes
    cleaned: dict[str, dict] = {}
    for dt, info in hints.items():
        missing = info.get("missing_values") or []
        if not missing:
            continue
        cleaned[dt] = {
            "missing_values": [m["value"] for m in missing[:50]],
            "via_fields": sorted(info.get("via_fields") or []),
            "total_missing": len(missing),
        }
    return cleaned

def _topological_sort_records(records: list[dict], parent_field: str, label_field: str | None) -> list[dict]:
    """Sort hierarchical records so each parent appears BEFORE its children.

    Cycles are broken by emitting the cycle members in their original order
    (Frappe will still raise if there's a real cycle, but we don't want to
    block the whole plan over a single bad row).
    """
    if not parent_field:
        return records

    # Build index by candidate identifier fields (name, label, account_number, ...)
    def _record_ids(rec: dict) -> list:
        ids = []
        for key in (label_field, "name", "account_number", "account_name",
                    "item_group_name", "warehouse_name", "cost_center_name",
                    "department_name", "territory_name",
                    "customer_group_name", "supplier_group_name"):
            if key and rec.get(key) not in (None, ""):
                ids.append(str(rec[key]).strip())
        return ids

    by_id: dict[str, dict] = {}
    for rec in records:
        for rid in _record_ids(rec):
            by_id.setdefault(rid, rec)

    visited: set[int] = set()
    ordered: list[dict] = []

    def visit(rec: dict, stack: set[int]):
        rec_id = id(rec)
        if rec_id in visited:
            return
        if rec_id in stack:
            return  # cycle — bail
        stack.add(rec_id)
        parent_value = rec.get(parent_field)
        if parent_value:
            parent_rec = by_id.get(str(parent_value).strip())
            if parent_rec is not None and parent_rec is not rec:
                visit(parent_rec, stack)
        stack.discard(rec_id)
        visited.add(rec_id)
        ordered.append(rec)

    for rec in records:
        visit(rec, set())

    return ordered

def _post_process_coa_plan(plan: dict, doc) -> None:
    """For Chart of Accounts plans, enforce ERPNext-specific invariants that
    the AI may have missed:

    1. Every parent_account must be suffixed with " - {company_abbr}".
    2. The 5 Vietnamese root accounts (Tài sản, Nợ phải trả, Vốn chủ sở hữu,
       Thu nhập, Chi phí) must exist as a preceding step — and ONLY those 5.
    3. Within each Account step, topologically sort by parent so children
       come after parents.

    This function mutates ``plan`` in place. No-op for non-Account plans.
    """
    if not plan or not plan.get("steps"):
        return

    account_steps = [s for s in plan["steps"] if s.get("target_doctype") == "Account"]
    if not account_steps:
        return

    company_name = doc.company
    if not company_name:
        return

    abbr = frappe.db.get_value("Company", company_name, "abbr") or ""
    if not abbr:
        return

    vn_root_specs = {
        "Tài sản": ("Asset", "Balance Sheet"),
        "Nợ phải trả": ("Liability", "Balance Sheet"),
        "Vốn chủ sở hữu": ("Equity", "Balance Sheet"),
        "Thu nhập": ("Income", "Profit and Loss"),
        "Chi phí": ("Expense", "Profit and Loss"),
    }
    existing_root_names = {
        n for n, in frappe.db.get_values(
            "Account",
            {"company": company_name, "parent_account": ["in", ["", None]]},
            "account_name",
        ) or []
    }

    # --- 1. Normalise parent_account suffix on every record ---
    def _with_suffix(value: str) -> str:
        v = (value or "").strip()
        if not v:
            return ""
        if v.endswith(f" - {abbr}"):
            return v
        return f"{v} - {abbr}"

    def _account_display(rec: dict) -> str:
        number = str(rec.get("account_number") or "").strip()
        name = str(rec.get("account_name") or "").strip()
        if number and name:
            # ERPNext autoname: "{number} {name} - {abbr}" — space, not dash
            return f"{number} {name}"
        return name or number

    def _infer_parent_number(account_number: str) -> str:
        number = str(account_number or "").strip()
        if not number:
            return ""
        if "." in number:
            return number.rsplit(".", 1)[0].strip()
        # For digit-only accounts, parent = number with last digit trimmed
        if number.isdigit() and len(number) >= 2:
            return number[:-1]
        return ""

    def _account_class(number: str) -> tuple[str, str, str] | None:
        prefix = str(number or "").strip()[:1]
        return {
            "1": ("Asset", "Balance Sheet", "Tài sản"),
            "2": ("Liability", "Balance Sheet", "Nợ phải trả"),
            "3": ("Equity", "Balance Sheet", "Vốn chủ sở hữu"),
            "4": ("Equity", "Balance Sheet", "Vốn chủ sở hữu"),
            "5": ("Income", "Profit and Loss", "Thu nhập"),
            "6": ("Expense", "Profit and Loss", "Chi phí"),
            "7": ("Income", "Profit and Loss", "Thu nhập"),
            "8": ("Expense", "Profit and Loss", "Chi phí"),
            "9": ("Expense", "Profit and Loss", "Chi phí"),
        }.get(prefix)

    account_records = [
        rec
        for step in account_steps
        for rec in (step.get("records") or [])
        if isinstance(rec, dict)
    ]
    by_number = {
        str(rec.get("account_number") or "").strip(): rec
        for rec in account_records
        if str(rec.get("account_number") or "").strip()
    }
    parent_numbers_in_file: set[str] = set()
    for rec in account_records:
        number = str(rec.get("account_number") or "").strip()
        parent_raw = _strip_account_company_suffix(rec.get("parent_account"), abbr)
        raw_parent_number = _leading_account_number(parent_raw)
        # If the AI set parent = own number (self-ref bug), fall back to structural inference
        if not raw_parent_number or raw_parent_number == number:
            parent_number = _infer_parent_number(number)
        else:
            parent_number = raw_parent_number
        if parent_number and parent_number in by_number and parent_number != number:
            parent_numbers_in_file.add(parent_number)

    for rec in account_records:
        number = str(rec.get("account_number") or "").strip()
        parent_raw = _strip_account_company_suffix(rec.get("parent_account"), abbr)
        parent_number = _leading_account_number(parent_raw)

        if parent_number and parent_number in by_number and parent_number != number:
            rec["parent_account"] = _account_display(by_number[parent_number])
        elif not parent_raw or parent_number == number:
            # No parent set, OR AI set parent_account to the account's own number (self-ref bug)
            inferred_parent = _infer_parent_number(number)
            if inferred_parent and inferred_parent in by_number:
                rec["parent_account"] = _account_display(by_number[inferred_parent])
            else:
                account_class = _account_class(number)
                if account_class:
                    rec["parent_account"] = account_class[2]

        if number in parent_numbers_in_file:
            rec["is_group"] = 1
        else:
            rec["is_group"] = 0

        account_class = _account_class(number)
        if account_class:
            root_type, report_type, _root_name = account_class
            if rec.get("root_type") in (None, ""):
                rec["root_type"] = root_type
            if rec.get("report_type") in (None, ""):
                rec["report_type"] = report_type

    balance_map = {
        "dư nợ": "Debit", "du no": "Debit", "debit": "Debit",
        "dư có": "Credit", "du co": "Credit", "credit": "Credit",
    }
    referenced_root_names: set[str] = set()
    for step in account_steps:
        for rec in step.get("records") or []:
            # Normalise parent_account suffix
            parent = frappe.utils.cstr(rec.get("parent_account") or "").strip()
            if parent:
                base = parent[: -len(f" - {abbr}")] if parent.endswith(f" - {abbr}") else parent
                rec["parent_account"] = _with_suffix(parent)
                if base in vn_root_specs:
                    referenced_root_names.add(base)
            else:
                # ERPNext expects None for root accounts, NOT an empty string.
                rec["parent_account"] = None

            # Normalise balance_must_be: VN → EN
            bmb_raw = frappe.utils.cstr(rec.get("balance_must_be") or "").strip().lower()
            if bmb_raw in balance_map:
                rec["balance_must_be"] = balance_map[bmb_raw]
            elif bmb_raw and bmb_raw not in {"debit", "credit"}:
                # "Lưỡng tính" / unknown → clear (no constraint)
                rec["balance_must_be"] = ""

            # Normalise disabled: VN → 0/1
            dis = rec.get("disabled")
            if isinstance(dis, str):
                dis_lower = dis.strip().lower()
                if "ngừng" in dis_lower or "ngung" in dis_lower or dis_lower in {"1","true","yes"}:
                    rec["disabled"] = 1
                else:
                    rec["disabled"] = 0
            elif dis in (None, ""):
                rec["disabled"] = 0
            else:
                rec["disabled"] = int(bool(dis))

            # account_type: only allow ERPNext values, drop unknown
            allowed_types = {
                "Accumulated Depreciation","Asset Received But Not Billed","Bank","Cash","Chargeable",
                "Capital Work in Progress","Cost of Goods Sold","Depreciation","Equity",
                "Expense Account","Expenses Included In Asset Valuation","Expenses Included In Valuation",
                "Fixed Asset","Income Account","Liability","Payable","Receivable","Round Off",
                "Stock","Stock Adjustment","Stock Received But Not Billed","Service Received But Not Billed",
                "Tax","Temporary",
            }
            at = frappe.utils.cstr(rec.get("account_type") or "").strip()
            if at and at not in allowed_types:
                rec["account_type"] = ""

    # --- 2. Filter step 1 to ONLY the missing Vietnamese roots ---
    # Identify which step is the "create roots" step: the one whose records
    # all have parent_account="" or whose account_name matches a VN root.
    root_step = None
    for step in account_steps:
        recs = step.get("records") or []
        if not recs:
            continue
        if all(
            (r.get("account_name") in vn_root_specs) or not (r.get("parent_account") or "").strip()
            for r in recs
        ):
            root_step = step
            break

    missing_roots = [
        name for name in referenced_root_names if name not in existing_root_names
    ]

    if missing_roots:
        new_root_records = []
        for name in ("Tài sản", "Nợ phải trả", "Vốn chủ sở hữu", "Thu nhập", "Chi phí"):
            if name in missing_roots:
                root_type, report_type = vn_root_specs[name]
                new_root_records.append({
                    "account_name": name,
                    "is_group": 1,
                    "root_type": root_type,
                    "report_type": report_type,
                    "company": company_name,
                    "parent_account": None,
                })

        if root_step is not None:
            root_step["records"] = new_root_records
            root_step["record_count"] = len(new_root_records)
            root_step["title"] = "Tạo các tài khoản gốc tiếng Việt còn thiếu"
            root_step["unique_key"] = "account_name"
            root_step["preview_format"] = "table"
        else:
            # AI didn't include a root step — prepend one
            new_step = {
                "step": 0,
                "title": "Tạo các tài khoản gốc tiếng Việt còn thiếu",
                "description": "Bước này tự thêm bởi backend vì các root VN chưa tồn tại trong company.",
                "target_doctype": "Account",
                "mode": "insert",
                "unique_key": "account_name",
                "preview_format": "table",
                "parent_field": "parent_account",
                "label_field": "account_name",
                "ignore_duplicates": True,
                "records": new_root_records,
                "record_count": len(new_root_records),
            }
            plan["steps"].insert(0, new_step)
    elif root_step is not None:
        # All roots already exist — drop the root step entirely
        plan["steps"].remove(root_step)

    # Older/browser-cached plans can contain the same source-backed Account
    # import twice. Keep the first occurrence of each account_number across
    # Account steps so records created earlier in this same run are not later
    # reported as pre-existing DB data.
    seen_account_numbers: set[str] = set()
    duplicate_account_steps = []
    for step in plan["steps"]:
        if step.get("target_doctype") != "Account":
            continue

        recs = step.get("records") or []
        if not isinstance(recs, list) or not recs:
            continue

        has_numbered_records = any(
            isinstance(rec, dict) and str(rec.get("account_number") or "").strip()
            for rec in recs
        )
        if has_numbered_records and "tài khoản gốc" in str(step.get("title") or "").lower():
            step["title"] = "Tạo Account"

        filtered_recs = []
        current_step_numbers: set[str] = set()
        for rec in recs:
            if not isinstance(rec, dict):
                filtered_recs.append(rec)
                continue

            account_number = str(rec.get("account_number") or "").strip()
            if account_number and account_number in seen_account_numbers:
                continue
            filtered_recs.append(rec)
            if account_number:
                current_step_numbers.add(account_number)

        seen_account_numbers.update(current_step_numbers)
        step["records"] = filtered_recs
        step["record_count"] = len(filtered_recs)
        if has_numbered_records and not filtered_recs:
            duplicate_account_steps.append(step)

    for step in duplicate_account_steps:
        if step in plan["steps"]:
            plan["steps"].remove(step)

    # --- 3. Topo-sort within every Account step (already done in _normalise_plan
    #         BEFORE suffix fix, so we redo it now with corrected parent_account) ---
    for step in plan["steps"]:
        if step.get("target_doctype") != "Account":
            continue
        recs = step.get("records") or []
        if not recs:
            continue
        # Build by ERPNext display name + by account_number + by account_name
        by_id: dict[str, dict] = {}
        for r in recs:
            num = str(r.get("account_number") or "").strip()
            nam = str(r.get("account_name") or "").strip()
            for key_value in (
                # ERPNext autoname format: "{number} {name} - {abbr}"
                num and nam and f"{num} {nam} - {abbr}",
                num and nam and f"{num} {nam}",
                nam and f"{nam} - {abbr}",
                num or None,
                nam or None,
            ):
                if key_value:
                    by_id.setdefault(str(key_value).strip(), r)

        visited: set[int] = set()
        ordered: list[dict] = []

        def visit(rec, stack):
            rec_id = id(rec)
            if rec_id in visited:
                return
            if rec_id in stack:
                return
            stack.add(rec_id)
            parent = (rec.get("parent_account") or "").strip()
            if parent:
                # Strip suffix to match by_id keys
                base = parent[: -len(f" - {abbr}")] if parent.endswith(f" - {abbr}") else parent
                parent_number = _leading_account_number(base)
                parent_rec = (
                    by_id.get(parent)
                    or by_id.get(base)
                    or (parent_number and by_id.get(parent_number))
                )
                if parent_rec and parent_rec is not rec:
                    visit(parent_rec, stack)
            stack.discard(rec_id)
            visited.add(rec_id)
            ordered.append(rec)

        for r in recs:
            visit(r, set())
        step["records"] = ordered
        step["record_count"] = len(ordered)

    # Recompute totals
    plan["total_records"] = sum(s.get("record_count", 0) for s in plan["steps"])
    plan["total_steps"] = len(plan["steps"])
    # Re-number step indices
    for idx, s in enumerate(plan["steps"], start=1):
        s["step"] = idx

def merge_dependency_steps_into_plan(plan: dict, accepted_proposal_ids: list[str],
                                      all_proposals: list[dict]) -> dict:
    """Insert AI-proposed dependency steps that the USER has confirmed back
    into the plan, BEFORE their respective insert_before_step.

    Args:
        plan: the current plan dict (will be deep-copied and returned mutated).
        accepted_proposal_ids: list of `proposal_id` the user has approved in the UI.
        all_proposals: all proposals returned by ``fix_plan_errors``.

    Returns:
        Updated plan dict with new dependency steps prepended (renumbered).
    """
    import copy as _copy
    if not plan or not isinstance(plan, dict):
        return plan
    if not accepted_proposal_ids:
        return _copy.deepcopy(plan)

    accepted_lookup = {
        p.get("proposal_id"): p
        for p in (all_proposals or [])
        if isinstance(p, dict) and p.get("proposal_id") in accepted_proposal_ids
    }
    if not accepted_lookup:
        return _copy.deepcopy(plan)

    new_plan = _copy.deepcopy(plan)
    steps = new_plan.get("steps") or []

    # Convert each proposal into a real plan step
    new_steps_with_position: list[tuple[int, dict]] = []
    for pid, proposal in accepted_lookup.items():
        target_doctype = proposal.get("target_doctype")
        records = proposal.get("records") or []
        if not target_doctype or not records:
            continue
        insert_before = max(1, int(proposal.get("insert_before_step") or len(steps)))
        unique_key = proposal.get("unique_key") or _guess_unique_key(target_doctype)
        label_field = proposal.get("label_field") or _guess_label_field(target_doctype, records)
        new_step = {
            "step": 0,  # renumbered below
            "title": f"[AI gợi ý] Tạo {target_doctype} còn thiếu",
            "description": proposal.get("reason") or f"AI tự thêm bước này để giải quyết tham chiếu thiếu cho {target_doctype}.",
            "target_doctype": target_doctype,
            "mode": "insert",
            "unique_key": unique_key,
            "preview_format": "table",
            "parent_field": HIERARCHICAL_DOCTYPES.get(target_doctype),
            "label_field": label_field,
            "ignore_duplicates": True,
            "ignore_mandatory": bool(proposal.get("ignore_mandatory")),
            "records": records,
            "record_count": len(records),
            "_origin": "smart_fix_dependency",
            "_proposal_id": pid,
        }
        new_steps_with_position.append((insert_before, new_step))

    # Insert from highest position to lowest so earlier insertions don't shift later indices
    new_steps_with_position.sort(key=lambda t: -t[0])
    for insert_before, new_step in new_steps_with_position:
        # Convert 1-based "insert before this step" → 0-based list index
        steps.insert(insert_before - 1, new_step)

    # Renumber + recompute totals
    for idx, s in enumerate(steps, start=1):
        s["step"] = idx
    new_plan["steps"] = steps

    # Rewrite downstream Link references to match the predicted ERPNext name
    # of the newly-created dependency records (some DocTypes use
    # "{name} - {abbr}" autoname rule).
    _rewrite_link_refs_post_merge(new_plan)

    new_plan["total_steps"] = len(steps)
    new_plan["total_records"] = sum(len(s.get("records") or []) for s in steps)
    return new_plan


def _rewrite_link_refs_post_merge(plan: dict) -> None:
    """After merging AI-proposed dependency steps, rewrite Link-field values
    in downstream steps so they point to the actual ERPNext name of each
    new record.

    Some DocTypes (Department, Account, Cost Center, Warehouse...) autoname
    with a ``- {company_abbr}`` suffix; others (Designation, Item Group...)
    use the raw label as the name. We use ``frappe.model.naming`` rules by
    inspecting the meta's autoname.
    """
    if not plan or not plan.get("steps"):
        return

    # Build mapping: (dep_doctype, raw_value) → predicted_name
    name_map: dict[tuple[str, str], str] = {}
    for step in plan["steps"]:
        if step.get("_origin") != "smart_fix_dependency":
            continue
        target_doctype = step.get("target_doctype")
        if not target_doctype:
            continue
        for rec in step.get("records") or []:
            predicted = _predict_record_name(target_doctype, rec)
            if not predicted:
                continue
            # Index the original value the user/AI saw in the source data.
            raw_values = _candidate_raw_keys(target_doctype, rec)
            for raw in raw_values:
                if raw and predicted and raw != predicted:
                    name_map[(target_doctype, raw)] = predicted

    if not name_map:
        return

    # Now rewrite every Link field in subsequent records
    for step in plan["steps"]:
        if step.get("_origin") == "smart_fix_dependency":
            continue
        target_doctype = step.get("target_doctype")
        if not target_doctype or not frappe.db.exists("DocType", target_doctype):
            continue
        try:
            meta = frappe.get_meta(target_doctype)
        except Exception:
            continue
        link_fields = [df for df in meta.fields if df.fieldtype == "Link" and df.options]
        if not link_fields:
            continue
        for rec in step.get("records") or []:
            if not isinstance(rec, dict):
                continue
            for df in link_fields:
                value = rec.get(df.fieldname)
                if not value or not isinstance(value, str):
                    continue
                mapped = name_map.get((df.options, value.strip()))
                if mapped:
                    rec[df.fieldname] = mapped


def _candidate_raw_keys(doctype: str, rec: dict) -> list[str]:
    """Return the values from this record that downstream Link fields may
    contain (typically the human label before autoname adds a suffix).
    """
    label_map = {
        "Asset Category": "asset_category_name",
        "Department": "department_name",
        "Designation": "designation_name",
        "Branch": "branch",
        "Cost Center": "cost_center_name",
        "Location": "location_name",
        "Warehouse": "warehouse_name",
        "Item Group": "item_group_name",
        "Customer Group": "customer_group_name",
        "Supplier Group": "supplier_group_name",
        "Territory": "territory_name",
        "UOM": "uom_name",
        "Brand": "brand",
        "Account": "account_name",
        "Project": "project_name",
    }
    keys = []
    label_field = label_map.get(doctype)
    if label_field and rec.get(label_field):
        keys.append(str(rec[label_field]).strip())
    if rec.get("name"):
        keys.append(str(rec["name"]).strip())
    return keys


def _predict_record_name(doctype: str, rec: dict) -> str | None:
    """Predict the final ``name`` of an Account-like record before insertion.

    For DocTypes whose autoname is ``field:foo`` we return rec[foo]; for
    DocTypes with `{abbr}` style autoname (Department, Account, Cost
    Center, Warehouse) we ``{label} - {abbr}``.
    """
    if not frappe.db.exists("DocType", doctype):
        return None
    try:
        meta = frappe.get_meta(doctype)
    except Exception:
        return None
    autoname = (meta.autoname or "").strip()

    label_map = {
        "Asset Category": "asset_category_name",
        "Department": "department_name",
        "Designation": "designation_name",
        "Branch": "branch",
        "Cost Center": "cost_center_name",
        "Location": "location_name",
        "Warehouse": "warehouse_name",
        "Item Group": "item_group_name",
        "Customer Group": "customer_group_name",
        "Supplier Group": "supplier_group_name",
        "Territory": "territory_name",
        "UOM": "uom_name",
        "Brand": "brand",
        "Account": "account_name",
        "Project": "project_name",
    }
    label_field = label_map.get(doctype, "name")
    label = rec.get(label_field) or rec.get("name")
    if not label:
        return None
    label = str(label).strip()

    # Pattern 1: "field:<fieldname>" → return that field as-is
    if autoname.startswith("field:"):
        fname = autoname.split(":", 1)[1].strip()
        return str(rec.get(fname) or label).strip()

    # Pattern 2: company-scoped doctypes whose autoname uses {company} or {abbr}
    if any(token in autoname for token in ("{company", "{abbr}", "abbr")):
        company = rec.get("company")
        if company:
            abbr = frappe.db.get_value("Company", company, "abbr")
            if abbr:
                return f"{label} - {abbr}"

    # Pattern 3: any doctype with a `company` field but no explicit abbr token
    if rec.get("company"):
        try:
            meta_fields = {f.fieldname for f in meta.fields}
            if "company" in meta_fields:
                abbr = frappe.db.get_value("Company", rec["company"], "abbr")
                if abbr and doctype in {"Department", "Cost Center", "Warehouse", "Account"}:
                    return f"{label} - {abbr}"
        except Exception:
            pass

    return label
