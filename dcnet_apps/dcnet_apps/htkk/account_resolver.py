"""
Resolve tài khoản theo mapping từ HTKK Settings.

Mỗi doanh nghiệp có thể cấu hình mã tài khoản khác nhau cho cùng một vai trò
trong tờ khai thuế. Module này đọc HTKK Account Mapping và resolve ra Account cụ thể.
"""

import frappe
from frappe.utils import cint


def get_accounts_for_role(company, role):
    """
    Đọc HTKK Settings → HTKK Account Mapping.
    Trả về list account names cho company + role.
    
    Nếu tài khoản trong mapping là Group (TKK Tổng hợp), 
    tự động lấy tất cả các tài khoản con (leaves) bên dưới.
    
    Bổ sung Heuristic: Nếu Mapping trống cho VAT, tự động tìm các tài khoản
    được sử dụng trong các Tax Template có tên 'VAT'.
    """
    cache_key = f"htkk_accounts_{company}_{role}"
    if hasattr(frappe.local, cache_key):
        return getattr(frappe.local, cache_key)

    mapping = _get_mapping(company)
    accounts = []
    
    base_accounts = [row.account for row in mapping if row.role == role and row.account]
    
    # Tự động bổ sung các tài khoản VAT tiềm năng từ Templates để tránh bỏ sót
    if role in ["OUTPUT_VAT", "INPUT_VAT"]:
        detected = _detect_vat_accounts_from_templates(company, role)
        if detected:
            base_accounts.extend(detected)
            base_accounts = list(set(base_accounts))

    if base_accounts:
        # Tìm tất cả account con nếu base_account là group
        for base in base_accounts:
            # Kiểm tra account có tồn tại không trước khi lấy lft/rgt
            acc_info = frappe.db.get_value("Account", base, ["is_group", "lft", "rgt"], as_dict=True)
            if not acc_info:
                continue
                
            if acc_info.is_group:
                leaves = frappe.get_all("Account", filters={
                    "company": company,
                    "lft": (">=", acc_info.lft),
                    "rgt": ("<=", acc_info.rgt),
                    "is_group": 0
                }, pluck="name")
                accounts.extend(leaves)
            else:
                accounts.append(base)

    # Đảm bảo unique list
    accounts = list(set(accounts))
    
    setattr(frappe.local, cache_key, accounts)
    return accounts


def _detect_vat_accounts_from_templates(company, role):
    """Tìm các tài khoản thuế đang dùng trong Templates mà có keyword 'VAT'."""
    direction = "Sales" if role == "OUTPUT_VAT" else "Purchase"
    template_doctype = f"{direction} Taxes and Charges Template"
    
    # 1. Tìm trong Templates
    templates = frappe.get_all(template_doctype, 
        filters={"company": company, "name": ["like", "%VAT%"]}, 
        pluck="name")
    
    found_accounts = []
    if templates:
        child_doctype = f"{direction} Taxes and Charges"
        found_accounts = frappe.get_all(child_doctype, 
            filters={"parent": ["in", templates], "parenttype": template_doctype},
            pluck="account_head")
            
    # 2. Heuristic: Tìm các tài khoản có tên chứa VAT/Thuế GTGT
    if not found_accounts:
        found_accounts = frappe.get_all("Account", filters={
            "company": company,
            "account_name": ["like", "%VAT%"],
            "is_group": 0
        }, pluck="name")
        
    return list(set(found_accounts))


def get_account_code_map(company):
    """
    Trả về dict {role: [account_codes]} cho company.
    Cache per-request.
    """
    cache_key = f"htkk_account_code_map_{company}"
    if hasattr(frappe.local, cache_key):
        return getattr(frappe.local, cache_key)

    mapping = _get_mapping(company)
    result = {}
    for row in mapping:
        if row.role not in result:
            result[row.role] = []
        result[row.role].append(row.account_code)

    setattr(frappe.local, cache_key, result)
    return result


def resolve_account(company, account_code):
    """
    Tìm Account có account_number = account_code và company = company.
    Trả về account name (full) hoặc None.
    """
    return frappe.db.get_value(
        "Account",
        {"account_number": account_code, "company": company},
        "name",
    )


def get_accounts_by_prefix(company, prefix):
    """
    Tìm tất cả Account có account_number bắt đầu bằng prefix.
    VD: prefix="33" → tất cả TK thuế phải nộp nhà nước.
    """
    return frappe.get_all(
        "Account",
        filters={
            "company": company,
            "account_number": ("like", f"{prefix}%"),
            "is_group": 0,
        },
        pluck="name",
    )


def _get_mapping(company):
    """Đọc HTKK Account Mapping từ HTKK Settings cho company."""
    settings = frappe.get_single("HTKK Settings")
    return [row for row in settings.account_mapping if row.company == company]
