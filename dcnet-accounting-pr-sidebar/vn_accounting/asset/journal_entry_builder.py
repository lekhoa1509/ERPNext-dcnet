"""Build draft Journal Entries for asset repair capitalization (TT99/2025).

All JEs are created as Draft. Accountant reviews and submits manually.
"""
from __future__ import annotations

import frappe
from frappe import _


def _lookup_account(company: str, account_number: str) -> str:
    """Look up the leaf account by account_number for the given company."""
    result = frappe.db.get_value(
        "Account",
        {"company": company, "account_number": account_number, "is_group": 0},
        "name",
    )
    if not result:
        frappe.throw(
            _("Không tìm thấy tài khoản {0} cho công ty {1}. Kiểm tra Hệ thống tài khoản.").format(
                account_number, company
            )
        )
    return result


def _create_je(
    company: str,
    posting_date,
    accounts: list[dict],
    remark: str,
    ref_doctype: str = None,
    ref_name: str = None,
    submit: bool = True,
) -> str:
    """Create and optionally submit a Journal Entry. Returns its name."""
    cost_center = frappe.db.get_value("Company", company, "cost_center")
    for acc in accounts:
        if cost_center and "cost_center" not in acc:
            acc["cost_center"] = cost_center

    je = frappe.get_doc({
        "doctype": "Journal Entry",
        "voucher_type": "Journal Entry",
        "company": company,
        "posting_date": posting_date,
        "user_remark": remark,
        "accounts": accounts,
    })
    if ref_doctype and ref_name and je.accounts:
        je.accounts[0].reference_type = ref_doctype
        je.accounts[0].reference_name = ref_name
    je.flags.ignore_permissions = True
    je.insert()
    if submit:
        je.submit()
    frappe.db.commit()
    return je.name


def create_capitalization_je(repair_doc) -> str:
    """JE for repair capitalization: Debit TK 2413 (or 2412) / Credit TK 331.

    Per VN COA TT99/2025, account 241 is a group; the leaves are 2411/2412/2413.
    Sửa chữa lớn vốn hóa → 2413 (Sửa chữa lớn TSCĐ). Nâng cấp cải tạo → 2412 (XDCB).
    Falls back to any 241* leaf if specific code not found.
    """
    company = repair_doc.company
    repair_cost = repair_doc.repair_cost or 0
    if repair_cost <= 0:
        frappe.throw(_("Chi phí sửa chữa phải lớn hơn 0 để tạo bút toán vốn hóa"))

    target_code = "2413" if repair_doc.repair_classification == "Sửa chữa lớn vốn hóa" else "2412"
    tk_241 = (
        frappe.db.get_value("Account", {"company": company, "account_number": target_code, "is_group": 0}, "name")
        or frappe.db.get_value("Account", {"company": company, "account_number": "2413", "is_group": 0}, "name")
        or frappe.db.get_value("Account", {"company": company, "account_number": ("like", "241%"), "is_group": 0}, "name")
    )
    if not tk_241:
        frappe.throw(_("Không tìm thấy tài khoản 241x (XDCB dở dang) cho công ty {0}").format(company))
    tk_331 = _lookup_account(company, "331")

    accounts = [
        {"account": tk_241, "debit_in_account_currency": repair_cost},
        {"account": tk_331, "credit_in_account_currency": repair_cost},
    ]

    remark = "Vốn hóa sửa chữa {0} - {1} ({2})".format(
        repair_doc.name,
        repair_doc.asset_name or repair_doc.asset,
        repair_doc.repair_classification,
    )
    posting_date = (
        repair_doc.completion_date
        or repair_doc.failure_date
        or frappe.utils.today()
    )
    return _create_je(
        company,
        posting_date,
        accounts,
        remark,
        ref_doctype="Asset Repair",
        ref_name=repair_doc.name,
        submit=False,  # Draft for accountant review per design spec
    )


def create_ccdc_purchase_je(ccdc_item_doc) -> str:
    """JE: Debit TK 242 / Credit TK 153 on CCDC Item submit (TT99/2025 §4).

    Deprecated: new code should use post_je_from_entries from accounting_posting.py.
    """
    company = ccdc_item_doc.company
    posting_date = ccdc_item_doc.available_for_use_date or frappe.utils.today()
    cost = ccdc_item_doc.cost

    tk_242 = (
        ccdc_item_doc.prepayment_account
        or _lookup_account(company, "242")
    )
    tk_153 = (
        ccdc_item_doc.cost_account
        or _lookup_account(company, "153")
    )

    accounts = [
        {"account": tk_242, "debit_in_account_currency": cost},
        {"account": tk_153, "credit_in_account_currency": cost},
    ]
    remark = "CCDC ghi nhận 242: {0} — {1}".format(
        ccdc_item_doc.name,
        ccdc_item_doc.item_name or ccdc_item_doc.item_code or "",
    )
    # Note: "CCDC Item" is not in ERPNext's allowed reference_type list for JE accounts.
    # Track via user_remark only.
    return _create_je(company, posting_date, accounts, remark)


def create_ccdc_expense_je(ccdc_item_doc, entry_name: str, posting_date, amount: float) -> str:
    """JE: Debit expense account / Credit TK 242 for one allocation period.

    Deprecated: new code should use post_je_from_entries from accounting_posting.py.
    """
    company = ccdc_item_doc.company

    expense_account = (
        ccdc_item_doc.expense_account
        or _lookup_account(company, "6423")
    )
    tk_242 = (
        ccdc_item_doc.prepayment_account
        or _lookup_account(company, "242")
    )

    accounts = [
        {"account": expense_account, "debit_in_account_currency": amount},
        {"account": tk_242, "credit_in_account_currency": amount},
    ]
    remark = "Phân bổ CCDC {0} kỳ {1}".format(ccdc_item_doc.name, entry_name)
    return _create_je(company, posting_date, accounts, remark)


def create_ccdc_writeoff_je(ccdc_item_doc, remaining_242: float, remaining_153: float, posting_date) -> list[str]:
    """JEs to clear remaining 242 and 153 balances on CCDC Writeoff.

    Deprecated: new code should use post_je_from_entries from accounting_posting.py.
    """
    company = ccdc_item_doc.company
    je_names = []

    if remaining_242 > 0:
        expense_account = (
            ccdc_item_doc.expense_account
            or _lookup_account(company, "6423")
        )
        tk_242 = (
            ccdc_item_doc.prepayment_account
            or _lookup_account(company, "242")
        )
        accounts = [
            {"account": expense_account, "debit_in_account_currency": remaining_242},
            {"account": tk_242, "credit_in_account_currency": remaining_242},
        ]
        remark = "Ghi giảm CCDC {0} — xóa số dư TK 242".format(ccdc_item_doc.name)
        je_names.append(_create_je(company, posting_date, accounts, remark))

    if remaining_153 > 0:
        tk_632 = _lookup_account(company, "632")
        tk_153 = (
            ccdc_item_doc.cost_account
            or _lookup_account(company, "153")
        )
        accounts = [
            {"account": tk_632, "debit_in_account_currency": remaining_153},
            {"account": tk_153, "credit_in_account_currency": remaining_153},
        ]
        remark = "Ghi giảm CCDC {0} — xóa số dư TK 153".format(ccdc_item_doc.name)
        je_names.append(_create_je(company, posting_date, accounts, remark))

    return je_names
