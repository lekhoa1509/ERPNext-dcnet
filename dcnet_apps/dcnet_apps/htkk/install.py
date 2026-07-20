"""
HTKK module installation.

Tạo HTKK Settings mặc định và seed account mapping
cho các Company VN hiện có.
"""

import frappe


def after_install():
    """Chạy sau khi install app — tạo HTKK Settings mặc định."""
    _create_default_settings()
    _seed_mappings_for_existing_companies()


def _create_default_settings():
    """Tạo HTKK Settings với giá trị mặc định."""
    if frappe.db.exists("DocType", "HTKK Settings"):
        settings = frappe.get_single("HTKK Settings")
        if not settings.default_cit_rate:
            settings.default_cit_rate = 20
            settings.save(ignore_permissions=True)


def _seed_mappings_for_existing_companies():
    """Tạo account mapping cho tất cả Company VN hiện có."""
    vn_companies = frappe.get_all(
        "Company",
        filters={"country": "Vietnam"},
        pluck="name",
    )
    for company in vn_companies:
        seed_default_mapping(company)


def seed_default_mapping(company):
    """
    Tạo mapping mặc định cho 1 company theo mã TK chuẩn TT99/2025.

    Mapping: role → account_code mặc định.
    Resolve account_code → Account name thực tế trong hệ thống.
    """
    from dcnet_apps.htkk.account_resolver import resolve_account

    default_roles = _get_default_role_mapping()
    settings = frappe.get_single("HTKK Settings")

    # Xóa mapping cũ của company này (nếu có)
    settings.account_mapping = [
        row for row in settings.account_mapping if row.company != company
    ]

    # Cập nhật account_number từ name nếu chưa có (v16 CoA import đôi khi bị thiếu)
    frappe.db.sql("""
        UPDATE `tabAccount` 
        SET account_number = SUBSTRING_INDEX(name, ' - ', 1) 
        WHERE company = %s 
          AND (account_number = '' OR account_number IS NULL) 
          AND name REGEXP '^[0-9]+ - '
    """, company)
    frappe.db.commit()

    for role, (account_code, description) in default_roles.items():
        account = resolve_account(company, account_code)
        settings.append("account_mapping", {
            "company": company,
            "role": role,
            "account_code": account_code,
            "account": account,
            "description": description,
        })

    settings.save(ignore_permissions=True)


def _get_default_role_mapping():
    """
    Trả về dict mặc định: role → (account_code, description).
    Dựa trên hệ thống tài khoản TT99/2025.
    """
    return {
        # Thuế GTGT
        "OUTPUT_VAT": ("33311", "Thuế GTGT đầu ra"),
        "OUTPUT_VAT_IMPORT": ("33312", "Thuế GTGT hàng nhập khẩu"),
        "INPUT_VAT": ("1331", "Thuế GTGT được khấu trừ của HHDV"),
        "INPUT_VAT_FIXED_ASSET": ("1332", "Thuế GTGT được khấu trừ của TSCĐ"),
        # Thuế TNDN
        "CIT_PAYABLE": ("3334", "Thuế TNDN phải nộp"),
        "CIT_EXPENSE_CURRENT": ("8211", "Chi phí thuế TNDN hiện hành"),
        "CIT_EXPENSE_DEFERRED": ("8212", "Chi phí thuế TNDN hoãn lại"),
        # Thuế TNCN
        "PIT_PAYABLE": ("3335", "Thuế TNCN phải nộp"),
        # Doanh thu
        "REVENUE": ("511", "Doanh thu bán hàng và CCDV"),
        "REVENUE_FINANCIAL": ("515", "Doanh thu hoạt động tài chính"),
        "REVENUE_DEDUCTION": ("521", "Các khoản giảm trừ doanh thu"),
        # Chi phí
        "COGS": ("632", "Giá vốn hàng bán"),
        "EXPENSE_FINANCIAL": ("635", "Chi phí tài chính"),
        "EXPENSE_SELLING": ("641", "Chi phí bán hàng"),
        "EXPENSE_ADMIN": ("642", "Chi phí quản lý doanh nghiệp"),
        # Thu nhập / chi phí khác
        "INCOME_OTHER": ("711", "Thu nhập khác"),
        "EXPENSE_OTHER": ("811", "Chi phí khác"),
        # Tiền
        "CASH": ("111", "Tiền mặt"),
        "BANK": ("112", "Tiền gửi ngân hàng"),
        "CASH_IN_TRANSIT": ("113", "Tiền đang chuyển"),
        # Công nợ
        "RECEIVABLE": ("131", "Phải thu khách hàng"),
        "PAYABLE": ("331", "Phải trả người bán"),
        # Vốn
        "EQUITY": ("411", "Vốn đầu tư của chủ sở hữu"),
        "RETAINED_EARNINGS": ("421", "LNST chưa phân phối"),
        # TSCĐ
        "FIXED_ASSET_TANGIBLE": ("211", "TSCĐ hữu hình"),
        "FIXED_ASSET_INTANGIBLE": ("213", "TSCĐ vô hình"),
        "DEPRECIATION": ("214", "Hao mòn TSCĐ"),
        # Hàng tồn kho
        "INVENTORY_RAW_MATERIAL": ("152", "Nguyên liệu, vật liệu"),
        "INVENTORY_TOOLS": ("153", "Công cụ, dụng cụ"),
        "INVENTORY_WIP": ("154", "Chi phí SXKD dở dang"),
        "INVENTORY_FINISHED_GOODS": ("155", "Thành phẩm"),
        "INVENTORY_MERCHANDISE": ("156", "Hàng hóa"),
    }
