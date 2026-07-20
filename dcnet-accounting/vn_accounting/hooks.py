app_name = "vn_accounting"
app_title = "VN Accounting"
app_publisher = "DCNET"
app_description = "Kế toán Việt Nam cho ERPNext v16 — Hệ thống tài khoản TT99/2025, thiết lập mặc định, workspace, sidebar, dashboard"
app_email = "info@dcnet.vn"
app_license = "mit"

required_apps = ["frappe", "erpnext"]


fixtures = [
    {"dt": "Print Format", "filters": [["doc_type", "=", "Cash Count"]]},
    {"dt": "Print Format", "filters": [["doc_type", "=", "Asset Disposal"]]},
    {"dt": "Property Setter", "filters": [
        ["doc_type", "in", ["Asset", "Asset Repair", "Journal Entry Account"]]
    ]},
    {"dt": "Custom Field", "filters": [
        ["module", "in", ["VN Accounting", "Misa Migration"]]
    ]},
]

# Sidebar role-gating + module-aware selection live in dcnet_theme (merged
# from the standalone dcnet_sidebar_routing app). Install dcnet_theme alongside.
app_include_js = [
    "dashboard_charts.bundle.js",
    "form_utils.bundle.js",
    "general_ledger_branch_filter.bundle.js",
    "party_report_defaults.bundle.js",
    "phieu_chi_subtype_dialog.bundle.js",
    "realtime_reports.bundle.js",
]
app_include_css = [
    "vn_accounting.bundle.css",
]

doctype_js = {
    "Branch Cash Entry": "public/js/branch_cash_entry.js",
    "Internal Summary Entry": "public/js/internal_summary_entry.js",
    "VN Accounting Branch Menu Access": "public/js/vn_accounting_branch_menu_access.js",
    "Asset Depreciation Schedule": "public/js/asset_depreciation_schedule.js",
    "Asset Repair": "public/js/asset_repair.bundle.js",
    "Landed Cost Voucher": "public/js/landed_cost_voucher.js",
    "Cost Allocation Run": "public/js/cost_allocation_run.js",
    "CCDC Allocation Schedule": "public/js/ccdc_allocation_schedule.js",
    "Sales Invoice": "public/js/sales_invoice_deferred_revenue.js",
    "Purchase Invoice": "public/js/purchase_invoice_deferred_expense.js",
    "Period Closing Voucher": "public/js/period_closing_voucher_vn_hint.js",
}

doctype_list_js = {
    "Journal Entry": "public/js/journal_entry_list.js",
}

# Đăng ký COA — thêm templates Việt Nam khi chọn country = Vietnam
# Dùng override_whitelisted_methods vì get_charts_for_country không có @erpnext.allow_regional
override_whitelisted_methods = {
    "frappe.desk.query_report.run": "vn_accounting.query_report.run",
    "erpnext.accounts.doctype.account.chart_of_accounts.chart_of_accounts.get_charts_for_country":
        "vn_accounting.chart_of_accounts.coa_registry.get_charts_for_country"
}

permission_query_conditions = {
    "Branch Cash Entry": "vn_accounting.branch_cash.service.get_branch_cash_entry_permission_query_conditions",
    "Internal Summary Entry":
        "vn_accounting.vn_accounting.doctype.internal_summary_entry.internal_summary_entry.get_internal_summary_entry_permission_query_conditions",
}

has_permission = {
    "Branch Cash Entry": "vn_accounting.branch_cash.service.has_branch_cash_entry_permission",
    "Internal Summary Entry":
        "vn_accounting.vn_accounting.doctype.internal_summary_entry.internal_summary_entry.has_internal_summary_entry_permission",
}

# Thiết lập mặc định công ty sau khi tạo COA
# Dùng on_update vì tài khoản được tạo trong on_update, không phải after_insert
doc_events = {
    "Company": {
        "on_update": [
            "vn_accounting.setup.company_defaults.set_vn_defaults",
            "vn_accounting.setup.company_defaults.seed_project_costing_settings",
            "vn_accounting.financial_reporting.bctc_mapping_lifecycle.ensure_bctc_mapping_for_company",
        ]
    },
    "Journal Entry": {
        "after_insert": "vn_accounting.auto_source.classify_and_register_je",
        "validate": "vn_accounting.non_deductible.je_hooks.validate_non_deductible",
        "on_submit": [
            "vn_accounting.treasury.je_hooks.on_je_submit",
            "vn_accounting.non_deductible.je_hooks.propagate_to_gl_entry",
        ],
        "on_cancel": "vn_accounting.treasury.je_hooks.on_je_cancel",
        "on_trash": "vn_accounting.auto_source.cleanup_orphan_on_delete",
    },
    "Sales Invoice": {
        # GỘP: trước đây có 2 block "Sales Invoice" trùng key → block sau ghi đè
        # block trước, làm MẤT after_insert (auto-source) + on_trash (cleanup).
        # Gộp đủ 4 sự kiện vào 1 block.
        "after_insert": "vn_accounting.auto_source.classify_and_register_si",
        "on_submit": "vn_accounting.project_costing.services.cogs_engine.on_sales_invoice_submit",
        "on_cancel": "vn_accounting.project_costing.services.cogs_engine.on_sales_invoice_cancel",
        "on_trash": "vn_accounting.auto_source.cleanup_orphan_on_delete",
    },
    "Asset Repair": {
        "on_validate": "vn_accounting.asset.repair_hooks.on_validate",
        "on_submit": "vn_accounting.asset.repair_hooks.on_submit",
        "on_cancel": "vn_accounting.asset.repair_hooks.on_cancel",
    },
    "Purchase Invoice": {
        "validate": [
            "vn_accounting.project_costing.services.stage_lock_guard.validate_stage_not_locked",
            "vn_accounting.non_deductible.source_hooks.on_purchase_invoice_validate",
        ],
        "on_submit": [
            "vn_accounting.asset.pi_hooks.on_purchase_invoice_submit",
            "vn_accounting.project_costing.services.wip_override_engine.on_purchase_invoice_submit",
            "vn_accounting.non_deductible.source_hooks.on_purchase_invoice_submit",
        ],
        "on_cancel": "vn_accounting.project_costing.services.wip_override_engine.on_purchase_invoice_cancel",
    },
    "Stock Entry": {
        "validate": "vn_accounting.project_costing.services.stage_lock_guard.validate_stage_not_locked",
        "on_submit": "vn_accounting.project_costing.services.wip_override_engine.on_stock_entry_submit",
        "on_cancel": "vn_accounting.project_costing.services.wip_override_engine.on_stock_entry_cancel",
    },
    "Delivery Note": {
        "validate": "vn_accounting.project_costing.services.stage_lock_guard.validate_stage_not_locked",
        "on_submit": "vn_accounting.project_costing.services.wip_override_engine.on_delivery_note_submit",
        "on_cancel": "vn_accounting.project_costing.services.wip_override_engine.on_delivery_note_cancel",
    },
    "Expense Claim": {
        "validate": "vn_accounting.project_costing.services.stage_lock_guard.validate_stage_not_locked",
        "on_submit": [
            "vn_accounting.project_costing.services.wip_override_engine.on_expense_claim_submit",
            "vn_accounting.non_deductible.source_hooks.on_expense_claim_submit",
        ],
        "on_cancel": "vn_accounting.project_costing.services.wip_override_engine.on_expense_claim_cancel",
    },
    "Salary Slip": {
        "on_submit": [
            "vn_accounting.project_costing.services.reclassify_engine.on_salary_slip_submit",
            "vn_accounting.non_deductible.source_hooks.on_salary_slip_submit",
        ],
        "on_cancel": "vn_accounting.project_costing.services.reclassify_engine.on_salary_slip_cancel",
    },
    "Landed Cost Voucher": {
        "before_validate": "vn_accounting.landed_cost.lcv_hooks.lcv_apply_default_expense_account",
        "validate": "vn_accounting.landed_cost.lcv_hooks.lcv_validate_import_vat_split",
        "on_submit": "vn_accounting.landed_cost.lcv_hooks.lcv_create_inventory_split_je",
        "on_cancel": "vn_accounting.landed_cost.lcv_hooks.lcv_cancel_inventory_split_je",
    },
    "Period Closing Voucher": {
        "validate": "vn_accounting.period_closing.pcv_hooks.pcv_validate_vn_requirements",
        "on_submit": "vn_accounting.period_closing.pcv_hooks.pcv_on_submit",
        "on_cancel": "vn_accounting.period_closing.pcv_hooks.pcv_on_cancel",
    },
}

# (Đã gỡ block permission_query_conditions + has_permission TRÙNG y hệt ở đây —
#  bản gốc khai báo phía trên đã đủ; bản dưới chỉ là lặp lại gây nhầm lẫn.)

# Workspace sidebar persistence — inject defaults into boot data
boot_session = "vn_accounting.boot.boot_session"

# Register help content with vn_help portal.
# Ưu tiên cao: khi vn_accounting cùng đăng ký 1 key với app khác (dcnet_pakd,
# dcnet_contract), help của vn_accounting THẮNG. App khác vẫn dùng được độc lập
# khi không cài vn_accounting (mặc định priority 0).
vn_help_priority = 100

vn_help_sources = {
    "doctype_mapping": {
        "Cash Count": {
            "section": "Tiền mặt",
            "title": "Kiểm kê quỹ",
            "content_dir": "help/tien-mat",
            "default_article": "kiem-ke-quy",
        },
        "Branch Cash Entry": {
            "section": "Tiền mặt",
            "title": "Phiếu quỹ chi nhánh",
            "content_dir": "help/tien-mat",
            "default_article": "phieu-quy-chi-nhanh",
        },
        "Payment Entry": {
            "section": "Tiền mặt",
            "title": "Phiếu thanh toán",
            "content_dir": "help/tien-mat",
            "default_article": "thu-thanh-toan",
        },
        "Journal Entry": {
            "section": "Ngân hàng",
            "title": "Bút toán kế toán",
            "content_dir": "help/ngan-hang",
            "default_article": "but-toan-ngan-hang",
        },
        "Term Deposit": {
            "section": "Ngân hàng",
            "title": "Tiền gửi có kỳ hạn",
            "content_dir": "help/ngan-hang",
            "default_article": "tien-gui-co-ky-han",
        },
        "Bank Loan": {
            "section": "Ngân hàng",
            "title": "Khoản vay ngân hàng",
            "content_dir": "help/ngan-hang",
            "default_article": "khoan-vay-ngan-hang",
        },
        "Purchase Order": {
            "section": "Mua hàng",
            "title": "Đơn mua hàng",
            "content_dir": "help/mua-hang",
            "default_article": "don-mua-hang",
        },
        "Purchase Invoice": {
            "section": "Mua hàng",
            "title": "Hoá đơn mua hàng",
            "content_dir": "help/mua-hang",
            "default_article": "hoa-don-mua-hang",
        },
        "Purchase Receipt": {
            "section": "Mua hàng",
            "title": "Nhập kho mua hàng",
            "content_dir": "help/mua-hang",
            "default_article": "nhap-kho-mua-hang",
        },
        "Payment Terms Template": {
            "section": "Bán hàng",
            "title": "Điều khoản thanh toán",
            "content_dir": "help/ban-hang",
            "default_article": "dieu-khoan-thanh-toan",
        },
        "Quotation": {
            "section": "Bán hàng",
            "title": "Báo giá",
            "content_dir": "help/ban-hang",
            "default_article": "bao-gia",
        },
        "Sales Order": {
            "section": "Bán hàng",
            "title": "Đơn bán hàng",
            "content_dir": "help/ban-hang",
            "default_article": "don-ban-hang",
        },
        "Sales Invoice": {
            "section": "Bán hàng",
            "title": "Hoá đơn bán hàng",
            "content_dir": "help/ban-hang",
            "default_article": "hoa-don-ban-hang",
        },
        "VN Deferred Revenue Schedule": {
            "section": "Bán hàng",
            "title": "Doanh thu chưa thực hiện (3387)",
            "content_dir": "help/ban-hang",
            "default_article": "doanh-thu-chua-thuc-hien",
        },
        "Delivery Note": {
            "section": "Bán hàng",
            "title": "Phiếu xuất kho",
            "content_dir": "help/ban-hang",
            "default_article": "phieu-xuat-kho",
        },
        "DCNet Contract": {
            "section": "Hợp đồng & PAKD",
            "title": "Danh sách hợp đồng",
            "content_dir": "help/hop-dong-pakd",
            "default_article": "danh-sach-hop-dong",
        },
        "Phuong An Kinh Doanh": {
            "section": "Hợp đồng & PAKD",
            "title": "Phương án kinh doanh",
            "content_dir": "help/hop-dong-pakd",
            "default_article": "phuong-an-kinh-doanh",
        },
        "Stock Entry": {
            "section": "Kho",
            "title": "Nhập xuất kho",
            "content_dir": "help/kho",
            "default_article": "nhap-xuat-kho",
        },
        "Stock Reconciliation": {
            "section": "Kho",
            "title": "Kiểm kê kho",
            "content_dir": "help/kho",
            "default_article": "kiem-ke-kho",
        },
        "Batch": {
            "section": "Kho",
            "title": "Số lô",
            "content_dir": "help/kho",
            "default_article": "so-lo",
        },
        "Serial No": {
            "section": "Kho",
            "title": "Số seri",
            "content_dir": "help/kho",
            "default_article": "so-seri",
        },
        "Product Bundle": {
            "section": "Kho",
            "title": "Gói sản phẩm",
            "content_dir": "help/kho",
            "default_article": "goi-san-pham",
        },
        "Asset": {
            "section": "TSCĐ",
            "title": "Tài sản cố định",
            "content_dir": "help/tscd",
            "default_article": "danh-sach",
        },
        "Asset Depreciation Schedule": {
            "section": "TSCĐ",
            "title": "Tính khấu hao",
            "content_dir": "help/tscd",
            "default_article": "tinh-khau-hao",
        },
        "Asset Repair": {
            "section": "TSCĐ",
            "title": "Sửa chữa",
            "content_dir": "help/tscd",
            "default_article": "sua-chua",
        },
        "Asset Handover": {
            "section": "TSCĐ",
            "title": "Bàn giao tài sản",
            "content_dir": "help/tscd",
            "default_article": "ban-giao",
        },
        "Asset Stocktake": {
            "section": "TSCĐ",
            "title": "Kiểm kê tài sản",
            "content_dir": "help/tscd",
            "default_article": "kiem-ke",
        },
        "Asset Disposal": {
            "section": "TSCĐ",
            "title": "Thanh lý tài sản",
            "content_dir": "help/tscd",
            "default_article": "thanh-ly",
        },
        "CCDC Item": {
            "section": "CCDC",
            "title": "Danh sách CCDC",
            "content_dir": "help/ccdc",
            "default_article": "danh-sach-ccdc",
        },
        "CCDC Allocation Schedule": {
            "section": "CCDC",
            "title": "Lịch phân bổ CCDC",
            "content_dir": "help/ccdc",
            "default_article": "lich-phan-bo-ccdc",
        },
        "CCDC Writeoff": {
            "section": "CCDC",
            "title": "Ghi giảm CCDC",
            "content_dir": "help/ccdc",
            "default_article": "ghi-giam-ccdc",
        },
        "Attendance": {
            "section": "Tiền lương",
            "title": "Bảng chấm công",
            "content_dir": "help/tien-luong",
            "default_article": "bang-cham-cong",
        },
        "Timesheet": {
            "section": "Tiền lương",
            "title": "Bảng giờ công",
            "content_dir": "help/tien-luong",
            "default_article": "bang-gio-cong",
        },
        "Payroll Entry": {
            "section": "Tiền lương",
            "title": "Bảng lương",
            "content_dir": "help/tien-luong",
            "default_article": "bang-luong",
        },
        "Salary Slip": {
            "section": "Tiền lương",
            "title": "Phiếu lương",
            "content_dir": "help/tien-luong",
            "default_article": "phieu-luong",
        },
        "Salary Structure": {
            "section": "Tiền lương",
            "title": "Cơ cấu lương",
            "content_dir": "help/tien-luong",
            "default_article": "co-cau-luong",
        },
        "Salary Component": {
            "section": "Tiền lương",
            "title": "Thành phần lương",
            "content_dir": "help/tien-luong",
            "default_article": "thanh-phan-luong",
        },
        "Salary Structure Assignment": {
            "section": "Tiền lương",
            "title": "Gán cơ cấu lương",
            "content_dir": "help/tien-luong",
            "default_article": "gan-co-cau-luong",
        },
        "Additional Salary": {
            "section": "Tiền lương",
            "title": "Lương bổ sung",
            "content_dir": "help/tien-luong",
            "default_article": "luong-bo-sung",
        },
        "Employee": {
            "section": "Danh mục",
            "title": "Nhân viên",
            "content_dir": "help/danh-muc",
            "default_article": "nhan-vien",
        },
        "Landed Cost Voucher": {
            "section": "Giá thành",
            "title": "Phân bổ chi phí mua hàng",
            "content_dir": "help/giathanh",
            "default_article": "lcv-co-ban",
        },
        "VN Deferred Expense Schedule": {
            "section": "Giá thành",
            "title": "Lịch phân bổ CP trả trước (242)",
            "content_dir": "help/giathanh",
            "default_article": "vn-deferred-expense-schedule",
        },
        "Project Costing": {
            "section": "Giá thành",
            "title": "Dự án — Giá thành",
            "content_dir": "help/giathanh",
            "default_article": "project-costing-tinh-gia-thanh",
        },
        "Cost Allocation Run": {
            "section": "Giá thành",
            "title": "Kết chuyển CP SXC (627→154)",
            "content_dir": "help/giathanh",
            "default_article": "project-costing-allocation-run",
        },
        "Inventory Cost Reallocation": {
            "section": "Giá thành",
            "title": "Phân bổ phụ phí vào giá vốn",
            "content_dir": "help/giathanh",
            "default_article": "inventory-cost-reallocation",
        },
        "LCV Allocation Settings": {
            "section": "Giá thành",
            "title": "Cấu hình phân bổ chi phí mua hàng",
            "content_dir": "help/giathanh",
            "default_article": "lcv-allocation-settings",
        },
        "EInvoice Inward": {
            "section": "Thuế",
            "title": "HĐ GTGT đầu vào",
            "content_dir": "help/thue",
            "default_article": "hd-gtgt-dau-vao",
        },
        "Sales Taxes and Charges Template": {
            "section": "Thuế",
            "title": "Mẫu thuế bán hàng",
            "content_dir": "help/thue",
            "default_article": "mau-thue-ban-hang",
        },
        "Purchase Taxes and Charges Template": {
            "section": "Thuế",
            "title": "Mẫu thuế mua hàng",
            "content_dir": "help/thue",
            "default_article": "mau-thue-mua-hang",
        },
        "Item Tax Template": {
            "section": "Thuế",
            "title": "Mẫu thuế hàng hoá",
            "content_dir": "help/thue",
            "default_article": "mau-thue-hang-hoa",
        },
        "Exchange Rate Revaluation": {
            "section": "Tổng hợp",
            "title": "Đánh giá lại ngoại tệ",
            "content_dir": "help/tong-hop",
            "default_article": "danh-gia-lai-ngoai-te",
        },
        "VN Period Close": {
            "section": "Tổng hợp",
            "title": "Phiếu kết chuyển định kỳ (911→4212)",
            "content_dir": "help/tong-hop",
            "default_article": "phieu-ket-chuyen-dinh-ky",
        },
        "Period Closing Voucher": {
            "section": "Tổng hợp",
            "title": "Khoá sổ kỳ kế toán",
            "content_dir": "help/tong-hop",
            "default_article": "khoa-so-ky",
        },
        "Accounting Period": {
            "section": "Thiết lập",
            "title": "Kỳ kế toán",
            "content_dir": "help/thiet-lap",
            "default_article": "ky-ke-toan",
        },
        "BCTC Mapping": {
            "section": "Báo cáo tài chính",
            "title": "Cấu hình BCTC Mapping",
            "content_dir": "help/bctc",
            "default_article": "bctc-mapping",
        },
        "Account": {
            "section": "Danh mục",
            "title": "Hệ thống tài khoản",
            "content_dir": "help/danh-muc",
            "default_article": "he-thong-tai-khoan",
        },
        "Customer": {
            "section": "Danh mục",
            "title": "Khách hàng",
            "content_dir": "help/danh-muc",
            "default_article": "khach-hang",
        },
        "Supplier": {
            "section": "Danh mục",
            "title": "Nhà cung cấp",
            "content_dir": "help/danh-muc",
            "default_article": "nha-cung-cap",
        },
        "Item": {
            "section": "Danh mục",
            "title": "Hàng hoá, vật tư",
            "content_dir": "help/danh-muc",
            "default_article": "hang-hoa-vat-tu",
        },
        "Warehouse": {
            "section": "Danh mục",
            "title": "Kho",
            "content_dir": "help/danh-muc",
            "default_article": "kho",
        },
        "BOM": {
            "section": "Danh mục",
            "title": "Định mức vật tư (BOM)",
            "content_dir": "help/danh-muc",
            "default_article": "dinh-muc-vat-tu",
        },
        "DCNet Contract Template": {
            "section": "Thiết lập",
            "title": "Mẫu hợp đồng",
            "content_dir": "help/thiet-lap",
            "default_article": "mau-hop-dong",
        },
        "DCNet Contract Settings": {
            "section": "Thiết lập",
            "title": "Cài đặt Hợp đồng",
            "content_dir": "help/thiet-lap",
            "default_article": "cai-dat-hop-dong",
        },
        "Chart of Accounts Importer": {
            "section": "Thiết lập",
            "title": "Import cây tài khoản",
            "content_dir": "help/thiet-lap",
            "default_article": "import-cay-tai-khoan",
        },
        "PAKD Commission Rule Template": {
            "section": "Thiết lập",
            "title": "Mẫu quy tắc hoa hồng",
            "content_dir": "help/thiet-lap",
            "default_article": "mau-quy-tac-hoa-hong",
        },
        "Fiscal Year": {
            "section": "Thiết lập",
            "title": "Năm tài chính",
            "content_dir": "help/thiet-lap",
            "default_article": "nam-tai-chinh",
        },
        "PAKD Settings": {
            "section": "Thiết lập",
            "title": "Cài đặt PAKD",
            "content_dir": "help/thiet-lap",
            "default_article": "cai-dat-pakd",
        },
        "PAKD Reminder Log": {
            "section": "Thiết lập",
            "title": "Lịch sử nhắc duyệt PAKD",
            "content_dir": "help/thiet-lap",
            "default_article": "lich-su-nhac-duyet-pakd",
        },
        "Cost Center": {
            "section": "Thiết lập",
            "title": "Trung tâm chi phí",
            "content_dir": "help/thiet-lap",
            "default_article": "trung-tam-chi-phi",
        },
        "Project": {
            "section": "Thiết lập",
            "title": "Dự án",
            "content_dir": "help/thiet-lap",
            "default_article": "du-an",
        },
        "Budget": {
            "section": "Thiết lập",
            "title": "Ngân sách",
            "content_dir": "help/thiet-lap",
            "default_article": "ngan-sach",
        },
        "Stock Settings": {
            "section": "Thiết lập",
            "title": "Cài đặt kho",
            "content_dir": "help/thiet-lap",
            "default_article": "cai-dat-kho",
        },
        "VN Accounting Settings": {
            "section": "Thiết lập",
            "title": "Cài đặt kế toán",
            "content_dir": "help/thiet-lap",
            "default_article": "cai-dat-ke-toan",
        },
        "Misa Migration Batch": {
            "section": "Công cụ Import",
            "title": "Lịch sử chuyển dữ liệu",
            "content_dir": "help/cong-cu-import",
            "default_article": "lich-su-migration",
        },
    },
    "report_mapping": {
        "Cash Receipts": {
            "section": "Tiền mặt",
            "title": "Phiếu thu",
            "content_dir": "help/tien-mat",
            "default_article": "phieu-thu",
        },
        "Cash Payments": {
            "section": "Tiền mặt",
            "title": "Phiếu chi",
            "content_dir": "help/tien-mat",
            "default_article": "phieu-chi",
        },
        "Cash Book": {
            "section": "Tiền mặt",
            "title": "Sổ quỹ tiền mặt",
            "content_dir": "help/tien-mat",
            "default_article": "so-quy-tien-mat",
        },
        "So Noi Bo": {
            "section": "Tiền mặt",
            "title": "Sổ quỹ chi nhánh",
            "content_dir": "help/tien-mat",
            "default_article": "so-quy-chi-nhanh",
        },
        "Bank Receipts": {
            "section": "Ngân hàng",
            "title": "Thu ngân hàng",
            "content_dir": "help/ngan-hang",
            "default_article": "thu-ngan-hang",
        },
        "Bank Payments": {
            "section": "Ngân hàng",
            "title": "Chi ngân hàng",
            "content_dir": "help/ngan-hang",
            "default_article": "chi-ngan-hang",
        },
        "Bank Account Book": {
            "section": "Ngân hàng",
            "title": "Sổ Tài khoản ngân hàng",
            "content_dir": "help/ngan-hang",
            "default_article": "so-tai-khoan-ngan-hang",
        },
        "Internal Transfer": {
            "section": "Ngân hàng",
            "title": "Điều chuyển nội bộ",
            "content_dir": "help/ngan-hang",
            "default_article": "dieu-chuyen-noi-bo",
        },
        "Term Deposit Summary": {
            "section": "Ngân hàng",
            "title": "Tổng hợp tiền gửi có kỳ hạn",
            "content_dir": "help/ngan-hang",
            "default_article": "tong-hop-tien-gui-co-ky-han",
        },
        "Bank Loan Summary": {
            "section": "Ngân hàng",
            "title": "Tổng hợp khoản vay ngân hàng",
            "content_dir": "help/ngan-hang",
            "default_article": "tong-hop-khoan-vay-ngan-hang",
        },
        "Accounts Payable": {
            "section": "Mua hàng",
            "title": "Công nợ phải trả",
            "content_dir": "help/mua-hang",
            "default_article": "cong-no-phai-tra",
        },
        "Accounts Payable Summary": {
            "section": "Mua hàng",
            "title": "Bảng tổng hợp công nợ NCC",
            "content_dir": "help/mua-hang",
            "default_article": "tong-hop-cong-no-ncc",
        },
        "Purchase Analytics": {
            "section": "Mua hàng",
            "title": "BC mua hàng",
            "content_dir": "help/mua-hang",
            "default_article": "bc-mua-hang",
        },
        "Item-wise Purchase Register": {
            "section": "Mua hàng",
            "title": "BC theo mặt hàng",
            "content_dir": "help/mua-hang",
            "default_article": "bc-theo-mat-hang",
        },
        "Purchase No VAT": {
            "section": "Mua hàng",
            "title": "Mua không VAT",
            "content_dir": "help/mua-hang",
            "default_article": "mua-khong-vat",
        },
        "Accounts Receivable": {
            "section": "Bán hàng",
            "title": "Công nợ phải thu",
            "content_dir": "help/ban-hang",
            "default_article": "cong-no-phai-thu",
        },
        "Accounts Receivable Summary": {
            "section": "Bán hàng",
            "title": "Bảng tổng hợp công nợ KH",
            "content_dir": "help/ban-hang",
            "default_article": "tong-hop-cong-no-kh",
        },
        "Sales Analytics": {
            "section": "Bán hàng",
            "title": "BC bán hàng",
            "content_dir": "help/ban-hang",
            "default_article": "bc-ban-hang",
        },
        "Invoices to Post": {
            "section": "Hợp đồng & PAKD",
            "title": "Hóa đơn cần ghi sổ",
            "content_dir": "help/hop-dong-pakd",
            "default_article": "hoa-don-can-ghi-so",
        },
        "Invoices Overdue by Contract": {
            "section": "Hợp đồng & PAKD",
            "title": "Hóa đơn quá hạn cần đôn thúc",
            "content_dir": "help/hop-dong-pakd",
            "default_article": "hoa-don-qua-han-don-thuc",
        },
        "Payments by Contract": {
            "section": "Hợp đồng & PAKD",
            "title": "Thu tiền theo hợp đồng",
            "content_dir": "help/hop-dong-pakd",
            "default_article": "thu-tien-theo-hop-dong",
        },
        "Commission Register": {
            "section": "Hợp đồng & PAKD",
            "title": "Sổ hoa hồng NVKD",
            "content_dir": "help/hop-dong-pakd",
            "default_article": "so-hoa-hong-nvkd",
        },
        "Beneficiary Payable": {
            "section": "Hợp đồng & PAKD",
            "title": "Phải trả phía khách",
            "content_dir": "help/hop-dong-pakd",
            "default_article": "phai-tra-phia-khach",
        },
        "Outstanding Receivables by Contract": {
            "section": "Hợp đồng & PAKD",
            "title": "Công nợ theo hợp đồng",
            "content_dir": "help/hop-dong-pakd",
            "default_article": "cong-no-theo-hop-dong",
        },
        "Overdue Billing Periods": {
            "section": "Hợp đồng & PAKD",
            "title": "Kỳ thu tiền quá hạn",
            "content_dir": "help/hop-dong-pakd",
            "default_article": "ky-thu-tien-qua-han",
        },
        "Stock Balance": {
            "section": "Kho",
            "title": "BC nhập xuất tồn",
            "content_dir": "help/kho",
            "default_article": "bc-nhap-xuat-ton",
        },
        "Stock Ageing": {
            "section": "Kho",
            "title": "BC tuổi kho",
            "content_dir": "help/kho",
            "default_article": "bc-tuoi-kho",
        },
        "Stock Ledger": {
            "section": "Kho",
            "title": "Sổ chi tiết kho",
            "content_dir": "help/kho",
            "default_article": "so-chi-tiet-kho",
        },
        "Itemwise Recommended Reorder Level": {
            "section": "Kho",
            "title": "Định mức tồn kho",
            "content_dir": "help/kho",
            "default_article": "dinh-muc-ton-kho",
        },
        "S21-DN": {
            "section": "TSCĐ",
            "title": "Sổ S21-DN",
            "content_dir": "help/tscd",
            "default_article": "so-s21-dn",
        },
        "Asset Depreciation Ledger": {
            "section": "TSCĐ",
            "title": "Lịch sử khấu hao",
            "content_dir": "help/tscd",
            "default_article": "lich-su-khau-hao",
        },
        "S22-DN Theo Doi TSCD CCDC": {
            "section": "CCDC",
            "title": "Sổ S22-DN",
            "content_dir": "help/ccdc",
            "default_article": "so-s22-dn",
        },
        "Landed Cost Pending Allocation": {
            "section": "Giá thành",
            "title": "Chi phí chờ phân bổ",
            "content_dir": "help/giathanh",
            "default_article": "landed-cost-pending-allocation",
        },
        "Project Invoicing Progress": {
            "section": "Giá thành",
            "title": "Tiến độ xuất hóa đơn",
            "content_dir": "help/giathanh",
            "default_article": "project-invoicing-progress",
        },
        "vat_return_01_gtgt": {
            "section": "Thuế",
            "title": "Tờ khai thuế GTGT (01/GTGT)",
            "content_dir": "help/thue",
            "default_article": "to-khai-gtgt",
        },
        "S03a-DN So Nhat Ky Chung": {
            "section": "Tổng hợp",
            "title": "Sổ nhật ký chung (S03a-DN)",
            "content_dir": "help/tong-hop",
            "default_article": "so-nhat-ky-chung",
        },
        "S03b-DN So Cai": {
            "section": "Tổng hợp",
            "title": "Sổ cái (S03b-DN)",
            "content_dir": "help/tong-hop",
            "default_article": "so-cai",
        },
        "Account Detail Ledger": {
            "section": "Tổng hợp",
            "title": "Sổ chi tiết tài khoản",
            "content_dir": "help/tong-hop",
            "default_article": "so-chi-tiet-tai-khoan",
        },
        "Trial Balance Sheet": {
            "section": "Tổng hợp",
            "title": "Bảng cân đối số phát sinh",
            "content_dir": "help/tong-hop",
            "default_article": "trial-balance",
        },
        "Auto Generated Docs Pending": {
            "section": "Tổng hợp",
            "title": "Tài liệu tự động chờ duyệt",
            "content_dir": "help/tong-hop",
            "default_article": "tai-lieu-tu-dong",
        },
        "B01-DN Bao Cao Tinh Hinh Tai Chinh": {
            "section": "Báo cáo tài chính",
            "title": "Báo cáo tình hình tài chính (B01-DN)",
            "content_dir": "help/bctc",
            "default_article": "b01-cau-truc",
        },
        "B02-DN Bao Cao KQHDKD": {
            "section": "Báo cáo tài chính",
            "title": "Báo cáo kết quả HĐKD (B02-DN)",
            "content_dir": "help/bctc",
            "default_article": "b02-ket-qua-kinh-doanh",
        },
        "B03-DN Bao Cao LCTT": {
            "section": "Báo cáo tài chính",
            "title": "Báo cáo lưu chuyển tiền tệ (B03-DN)",
            "content_dir": "help/bctc",
            "default_article": "b03-luu-chuyen-tien-te",
        },
        "Quyet Toan TNDN Reconciliation": {
            "section": "Báo cáo tài chính",
            "title": "Quyết toán TNDN (Form 03)",
            "content_dir": "help/bctc",
            "default_article": "quyet-toan-tndn",
        },
        "Bao Cao Chi Phi Khong Duoc Tru": {
            "section": "Báo cáo tài chính",
            "title": "Chi phí không được trừ (B4)",
            "content_dir": "help/bctc",
            "default_article": "chi-phi-khong-duoc-tru",
        },
        "Profitability Analysis": {
            "section": "Báo cáo tài chính",
            "title": "Phân tích lợi nhuận",
            "content_dir": "help/bctc",
            "default_article": "phan-tich-loi-nhuan",
        },
        "Budget Variance Report": {
            "section": "Báo cáo tài chính",
            "title": "So sánh ngân sách",
            "content_dir": "help/bctc",
            "default_article": "so-sanh-ngan-sach",
        },
        "Profit and Loss Statement": {
            "section": "Báo cáo tài chính",
            "title": "BC lãi lỗ quản trị",
            "content_dir": "help/bctc",
            "default_article": "lai-lo-quan-tri",
        },
        "Project Summary": {
            "section": "Báo cáo tài chính",
            "title": "Tóm tắt Dự án",
            "content_dir": "help/bctc",
            "default_article": "tom-tat-du-an",
        },
        "Bang Can Doi So Phat Sinh": {
            "section": "Báo cáo tài chính",
            "title": "Bảng cân đối số phát sinh (TT99/2025)",
            "content_dir": "help/bctc",
            "default_article": "bang-can-doi-so-phat-sinh",
        },
    },
    "page_mapping": {
        "vn-accounting-dashboard": {
            "section": "Tổng quan",
            "title": "Tổng quan Kế toán (Dashboard)",
            "content_dir": "help/tong-quan",
            "default_article": "index",
        },
        "bank-reconcile": {
            "section": "Ngân hàng",
            "title": "Đối soát sao kê",
            "content_dir": "help/ngan-hang",
            "default_article": "doi-soat-sao-ke",
        },
        "cash-flow-forecast": {
            "section": "Ngân hàng",
            "title": "Dự báo dòng tiền",
            "content_dir": "help/ngan-hang",
            "default_article": "du-bao-dong-tien",
        },
        "b09-dn-generator": {
            "section": "Báo cáo tài chính",
            "title": "Thuyết minh BCTC (B09-DN)",
            "content_dir": "help/bctc",
            "default_article": "b09-thuyet-minh",
        },
        "misa-migration-hub": {
            "section": "Công cụ Import",
            "title": "Trung tâm chuyển dữ liệu Misa",
            "content_dir": "help/cong-cu-import",
            "default_article": "misa-migration-hub",
        },
    },
}

# Đảm bảo COA templates đã đăng ký sau migrate và sau cài đặt lần đầu
after_migrate = ["vn_accounting.install.after_migrate"]
after_install = "vn_accounting.install.after_install"

# Đăng ký các nguồn tài liệu kế toán do hệ thống tự sinh — báo cáo
# "Tài liệu tự động" sẽ tự dựng nhãn, hành động và phần mô tả từ đây.
# Xem vn_accounting/auto_source.py để biết cách thêm nguồn mới.
auto_generated_doc_sources = {
    # --- Các luồng do vn_accounting tự sinh, cần kế toán duyệt -----------------
    "vn_accounting.lcv_vat_deductible": {
        "label": "Thuế GTGT hàng nhập khẩu được khấu trừ",
        "doctype": "Journal Entry",
        "needs_approval": True,
        "action_draft": "Duyệt và ghi sổ",
        "description": "Hệ thống tự sinh khi ghi sổ Phiếu phân bổ chi phí mua hàng có thuế nhập khẩu. Nội dung định khoản: Nợ TK 1331 / Có TK 33312. Kế toán xem lại trước khi ghi sổ.",
    },
    "vn_accounting.treasury.deposit_interest": {
        "label": "Lãi tiền gửi định kỳ",
        "doctype": "Journal Entry",
        "needs_approval": True,
        "action_draft": "Duyệt và ghi sổ",
        "description": "Hệ thống tự sinh hàng ngày cho mỗi kỳ lãi tiền gửi đến hạn. Nếu là lãi kép thì cộng dồn vào tài khoản 1281; còn lại ghi nhận vào tài khoản 112x.",
    },
    "vn_accounting.treasury.deposit_creation": {
        "label": "Tạo tiền gửi có kỳ hạn",
        "doctype": "Journal Entry",
        "needs_approval": True,
        "action_draft": "Duyệt và ghi sổ",
        "description": "Hệ thống tự sinh khi tạo Tiền gửi có kỳ hạn mới: Nợ TK 1281 / Có TK 112x.",
    },
    "vn_accounting.treasury.deposit_settlement": {
        "label": "Tất toán tiền gửi",
        "doctype": "Journal Entry",
        "needs_approval": True,
        "action_draft": "Duyệt và ghi sổ",
        "description": "Hệ thống tự sinh khi đáo hạn hoặc tất toán sớm Tiền gửi có kỳ hạn. Nội dung định khoản: Nợ TK 112x / Có TK 1281 (cộng thêm dòng lãi nếu có).",
    },
    "vn_accounting.treasury.deposit_accrual": {
        "label": "Trích trước lãi tiền gửi",
        "doctype": "Journal Entry",
        "needs_approval": True,
        "action_draft": "Duyệt và ghi sổ",
        "description": "Hệ thống tự sinh khi trích trước lãi tiền gửi cuối kỳ kế toán.",
    },
    "vn_accounting.treasury.loan_disbursement": {
        "label": "Giải ngân khoản vay",
        "doctype": "Journal Entry",
        "needs_approval": True,
        "action_draft": "Duyệt và ghi sổ",
        "description": "Hệ thống tự sinh khi ngân hàng giải ngân khoản vay cho doanh nghiệp.",
    },
    "vn_accounting.treasury.loan_repayment": {
        "label": "Trả nợ vay ngân hàng",
        "doctype": "Journal Entry",
        "needs_approval": True,
        "action_draft": "Duyệt và ghi sổ",
        "description": "Hệ thống tự sinh hàng ngày cho mỗi kỳ trả nợ đến hạn. Tách phần gốc và phần lãi theo lịch trả nợ.",
    },
    "vn_accounting.treasury.loan_settlement": {
        "label": "Tất toán khoản vay",
        "doctype": "Journal Entry",
        "needs_approval": True,
        "action_draft": "Duyệt và ghi sổ",
        "description": "Hệ thống tự sinh khi trả nợ hết khoản vay.",
    },
    "vn_accounting.treasury.loan_accrual": {
        "label": "Trích trước lãi vay",
        "doctype": "Journal Entry",
        "needs_approval": True,
        "action_draft": "Duyệt và ghi sổ",
        "description": "Hệ thống tự sinh khi trích trước lãi vay cuối kỳ kế toán.",
    },
    # --- Các luồng từ hệ thống ERP nền (Frappe/ERPNext lõi) -------------------
    "erp.asset_depreciation": {
        "label": "Khấu hao tài sản cố định",
        "doctype": "Journal Entry",
        "needs_approval": True,
        "action_draft": "Duyệt và ghi sổ",
        "description": "Hệ thống tự sinh hàng ngày cho mỗi tài sản đến kỳ khấu hao. Nội dung định khoản: Nợ TK 6424 hoặc 642x / Có TK 2141. Bật/tắt tại Cài đặt kế toán → Tự động sinh phiếu khấu hao.",
    },
    "erp.deferred_revenue": {
        "label": "Ghi nhận doanh thu chờ phân bổ",
        "doctype": "Journal Entry",
        "needs_approval": True,
        "action_draft": "Duyệt và ghi sổ",
        "description": "Hệ thống tự sinh hàng tháng cho mỗi kỳ phân bổ doanh thu nhận trước. Chỉ xuất hiện khi bật tùy chọn sinh Phiếu kế toán phân bổ trong Cài đặt kế toán (mặc định tắt — hệ thống ghi thẳng vào sổ cái).",
    },
    "erp.deferred_expense": {
        "label": "Phân bổ chi phí trả trước",
        "doctype": "Journal Entry",
        "needs_approval": True,
        "action_draft": "Duyệt và ghi sổ",
        "description": "Hệ thống tự sinh hàng tháng cho mỗi kỳ phân bổ chi phí trả trước (TK 242). Cùng tùy chọn bật/tắt với doanh thu chờ phân bổ.",
    },
    "erp.exchange_rate_revaluation": {
        "label": "Đánh giá lại số dư ngoại tệ",
        "doctype": "Journal Entry",
        "needs_approval": True,
        "action_draft": "Duyệt và ghi sổ",
        "description": "Hệ thống tự sinh khi công ty bật tự động đánh giá lại tỷ giá. Tần suất hàng ngày, hàng tuần hoặc hàng tháng tùy cấu hình của từng công ty.",
    },
    "erp.subscription_invoice": {
        "label": "Hóa đơn từ Đăng ký dịch vụ định kỳ",
        "doctype": "Sales Invoice",
        "needs_approval": True,
        "action_draft": "Duyệt, ghi sổ và xuất hóa đơn điện tử",
        "description": "Hệ thống tự sinh từ Đăng ký dịch vụ khi đến kỳ. Chỉ xuất hiện nếu doanh nghiệp có sử dụng đăng ký dịch vụ định kỳ. Mặc định ở trạng thái nháp.",
    },
    # --- Các luồng tự ghi sổ (chỉ để theo dõi, không cần duyệt) ----------------
    "vn_accounting.ccdc.purchase": {
        "label": "Ghi nhận mua công cụ dụng cụ",
        "doctype": "Journal Entry",
        "needs_approval": False,
        "description": "Hệ thống tự sinh khi ghi sổ Công cụ dụng cụ (sau khi nhập kho): Nợ TK 242 / Có TK 153. Tự động ghi sổ ngay.",
    },
    "vn_accounting.ccdc.allocation": {
        "label": "Phân bổ công cụ dụng cụ định kỳ",
        "doctype": "Journal Entry",
        "needs_approval": False,
        "description": "Hệ thống tự sinh hàng ngày cho mỗi kỳ phân bổ Công cụ dụng cụ đến hạn: Nợ TK 6423 / Có TK 242. Tự động ghi sổ ngay.",
    },
    "vn_accounting.ccdc.writeoff": {
        "label": "Ghi giảm công cụ dụng cụ",
        "doctype": "Journal Entry",
        "needs_approval": False,
        "description": "Hệ thống tự sinh khi ghi giảm hoặc thanh lý Công cụ dụng cụ: Nợ TK 6423 hoặc 811 / Có TK 242. Tự động ghi sổ ngay.",
    },
    "vn_accounting.asset.repair": {
        "label": "Sửa chữa tài sản cố định",
        "doctype": "Journal Entry",
        "needs_approval": False,
        "description": "Hệ thống tự sinh khi ghi sổ Sửa chữa tài sản cố định (định khoản trong nội bộ). Tự động ghi sổ ngay.",
    },
}


scheduler_events = {
    "daily": [
        "vn_accounting.treasury.scheduled.process_treasury_schedules",
        "vn_accounting.asset.ccdc_allocation.allocate_ccdc_monthly",
    ],
    "cron": {
        # Misa migration watchdog — every 5 minutes
        "*/5 * * * *": [
            "vn_accounting.misa_migration.jobs.watchdog.check_stuck_batches",
            "vn_accounting.misa_migration.jobs.watchdog.check_stuck_files",
        ],
    },
}

# Cash Flow Forecast — provider registration
cash_flow_forecast_providers = [
    "vn_accounting.forecast.treasury.get_treasury_forecast",
    "vn_accounting.forecast.erpnext_providers.get_quotation_forecast",
    "vn_accounting.forecast.erpnext_providers.get_sales_order_forecast",
    "vn_accounting.forecast.erpnext_providers.get_purchase_order_forecast",
    "vn_accounting.forecast.erpnext_providers.get_unpaid_si_forecast",
    "vn_accounting.forecast.erpnext_providers.get_unpaid_pi_forecast",
    "vn_accounting.forecast.payroll_provider.get_payroll_forecast",
    "vn_accounting.forecast.payroll_provider.get_insurance_forecast",
    "vn_accounting.forecast.tax_provider.get_tax_forecast",
    "vn_accounting.forecast.historical_projection.get_opex_forecast",
    "vn_accounting.forecast.revenue_projection.get_revenue_forecast",
]
