from __future__ import annotations

import hashlib
import json

import frappe
from frappe import _
from frappe.utils import add_days, cint, date_diff, now, today, validate_email_address


PERMISSION_MANAGER_ACCESS_ROLE = "DCNET Permission Manager"
ADMIN_ROLES = {"System Manager", "DCNET Permission Admin"}
PROTECTED_ROLES = {"Administrator", "System Manager"}
STANDARD_USERS = {"Administrator", "Guest"}
DEFAULT_INITIAL_PASSWORD = "123456"
DEFAULT_FORCE_PASSWORD_RESET_DAYS = 36500
USER_PERMISSION_ROLE_PREFIX = "DCNET User Permission - "
DOCTYPE_PERMISSION_FIELDS = [
    "select",
    "read",
    "write",
    "create",
    "delete",
    "submit",
    "cancel",
    "amend",
    "report",
    "export",
    "print",
    "email",
]
REPORT_PERMISSION_FIELDS = ["read"]
PERMISSION_COLUMNS = [
    {"key": "read", "label": "Read"},
    {"key": "create", "label": "Create"},
    {"key": "write", "label": "Write"},
    {"key": "delete", "label": "Delete"},
    {"key": "submit", "label": "Submit"},
    {"key": "cancel", "label": "Cancel"},
    {"key": "report", "label": "Report"},
    {"key": "export", "label": "Export"},
    {"key": "print", "label": "Print"},
]
GROUP_LABELS = {
    "Thiết lập kế toán": "Accounting Setup",
    "Tiền & ngân hàng": "Cash & Banking",
    "Sổ kế toán": "Accounting Ledger",
    "Bán hàng & công nợ phải thu": "Sales & Receivables",
    "Mua hàng & công nợ phải trả": "Buying & Payables",
    "Kho liên quan kế toán": "Accounting-related Stock",
    "Tài sản": "Assets",
    "Tổ chức & nhân viên": "Organization & Employees",
    "Vòng đời nhân sự": "Employee Lifecycle",
    "Chấm công": "Attendance",
    "Nghỉ phép": "Leave",
    "Chi phí nhân sự": "Employee Expenses",
    "Khách hàng": "Customers",
    "Thiết lập bán hàng": "Selling Setup",
    "Sản phẩm & giá": "Products & Pricing",
    "Bán hàng": "Sales",
    "Giao hàng": "Delivery",
    "Nhà cung cấp": "Suppliers",
    "Mua hàng": "Buying",
    "Kho hàng": "Stock",
    "Nhập xuất kho": "Stock Movement",
    "Sổ kho": "Stock Ledger",
    "Thiết lập kho": "Stock Setup",
    "CSKH": "Customer Support",
    "Support": "Customer Support",
    "Dự án": "Projects",
}
ACCOUNTING_DOCTYPE_SPECS = [
    {"name": "Account", "label": "Tài khoản kế toán", "group": "Thiết lập kế toán"},
    {"name": "Accounts Settings", "label": "Cài đặt kế toán ERPNext", "group": "Thiết lập kế toán"},
    {"name": "VN Accounting Settings", "label": "Cài đặt kế toán Việt Nam", "group": "Thiết lập kế toán"},
    {"name": "Cost Center", "label": "Trung tâm chi phí", "group": "Thiết lập kế toán"},
    {"name": "Company", "label": "Công ty", "group": "Thiết lập kế toán"},
    {"name": "Payment Terms Template", "label": "Điều khoản thanh toán", "group": "Thiết lập kế toán"},
    {"name": "Payment Term", "label": "Kỳ hạn thanh toán", "group": "Thiết lập kế toán"},
    {"name": "Bank Account", "label": "Tài khoản ngân hàng", "group": "Tiền & ngân hàng"},
    {"name": "Bank Transaction", "label": "Giao dịch ngân hàng", "group": "Tiền & ngân hàng"},
    {"name": "Payment Entry", "label": "Phiếu thu/chi", "group": "Tiền & ngân hàng"},
    {"name": "Journal Entry", "label": "Bút toán kế toán", "group": "Sổ kế toán"},
    {"name": "GL Entry", "label": "GL Entry", "group": "Sổ kế toán", "readonly": True},
    {"name": "Customer", "label": "Khách hàng", "group": "Bán hàng & công nợ phải thu"},
    {"name": "Quotation", "label": "Báo giá", "group": "Bán hàng & công nợ phải thu"},
    {"name": "Sales Order", "label": "Đơn bán hàng", "group": "Bán hàng & công nợ phải thu"},
    {"name": "Sales Invoice", "label": "Hóa đơn bán hàng", "group": "Bán hàng & công nợ phải thu"},
    {"name": "Delivery Note", "label": "Phiếu giao hàng", "group": "Bán hàng & công nợ phải thu"},
    {"name": "Supplier", "label": "Nhà cung cấp", "group": "Mua hàng & công nợ phải trả"},
    {"name": "Purchase Order", "label": "Đơn mua hàng", "group": "Mua hàng & công nợ phải trả"},
    {"name": "Purchase Receipt", "label": "Phiếu nhập mua", "group": "Mua hàng & công nợ phải trả"},
    {"name": "Purchase Invoice", "label": "Hóa đơn mua hàng", "group": "Mua hàng & công nợ phải trả"},
    {"name": "Item", "label": "Sản phẩm", "group": "Kho liên quan kế toán"},
    {"name": "Stock Entry", "label": "Phiếu kho", "group": "Kho liên quan kế toán"},
    {"name": "Asset", "label": "Tài sản cố định", "group": "Tài sản"},
    {"name": "Asset Movement", "label": "Điều chuyển tài sản", "group": "Tài sản"},
]
HR_DOCTYPE_SPECS = [
    {"name": "Department", "label": "Phòng ban", "group": "Tổ chức & nhân viên"},
    {"name": "Branch", "label": "Chi nhánh", "group": "Tổ chức & nhân viên"},
    {"name": "Designation", "label": "Chức vụ", "group": "Tổ chức & nhân viên"},
    {"name": "Employee Grade", "label": "Cấp bậc nhân viên", "group": "Tổ chức & nhân viên"},
    {"name": "Employment Type", "label": "Loại hình nhân sự", "group": "Tổ chức & nhân viên"},
    {"name": "Employee", "label": "Nhân viên", "group": "Tổ chức & nhân viên"},
    {"name": "Employee Onboarding", "label": "Tiếp nhận nhân viên", "group": "Vòng đời nhân sự"},
    {"name": "Employee Transfer", "label": "Điều chuyển nhân viên", "group": "Vòng đời nhân sự"},
    {"name": "Employee Promotion", "label": "Thăng chức nhân viên", "group": "Vòng đời nhân sự"},
    {"name": "Employee Separation", "label": "Nghỉ việc", "group": "Vòng đời nhân sự"},
    {"name": "Attendance", "label": "Chấm công", "group": "Chấm công"},
    {"name": "Attendance Request", "label": "Yêu cầu chấm công", "group": "Chấm công"},
    {"name": "Employee Checkin", "label": "Check-in nhân viên", "group": "Chấm công"},
    {"name": "Shift Type", "label": "Ca làm việc", "group": "Chấm công"},
    {"name": "Holiday List", "label": "Lịch nghỉ", "group": "Chấm công"},
    {"name": "Leave Type", "label": "Loại nghỉ phép", "group": "Nghỉ phép"},
    {"name": "Leave Period", "label": "Kỳ nghỉ phép", "group": "Nghỉ phép"},
    {"name": "Leave Policy", "label": "Chính sách nghỉ phép", "group": "Nghỉ phép"},
    {"name": "Leave Policy Assignment", "label": "Gán chính sách nghỉ phép", "group": "Nghỉ phép"},
    {"name": "Leave Allocation", "label": "Cấp phát nghỉ phép", "group": "Nghỉ phép"},
    {"name": "Leave Application", "label": "Đơn nghỉ phép", "group": "Nghỉ phép"},
    {"name": "Leave Ledger Entry", "label": "Sổ nghỉ phép", "group": "Nghỉ phép", "readonly": True},
    {"name": "Expense Claim", "label": "Đề nghị thanh toán chi phí", "group": "Chi phí nhân sự"},
    {"name": "Employee Advance", "label": "Tạm ứng nhân viên", "group": "Chi phí nhân sự"},
]
SALES_DOCTYPE_SPECS = [
    {"name": "Lead", "label": "Lead", "group": "CRM"},
    {"name": "Opportunity", "label": "Cơ hội bán hàng", "group": "CRM"},
    {"name": "Campaign", "label": "Chiến dịch", "group": "CRM"},
    {"name": "Customer", "label": "Khách hàng", "group": "Khách hàng"},
    {"name": "Contact", "label": "Liên hệ", "group": "Khách hàng"},
    {"name": "Address", "label": "Địa chỉ", "group": "Khách hàng"},
    {"name": "Customer Group", "label": "Nhóm khách hàng", "group": "Thiết lập bán hàng"},
    {"name": "Territory", "label": "Khu vực", "group": "Thiết lập bán hàng"},
    {"name": "Sales Person", "label": "Nhân viên bán hàng", "group": "Thiết lập bán hàng"},
    {"name": "Sales Partner", "label": "Đối tác bán hàng", "group": "Thiết lập bán hàng"},
    {"name": "Price List", "label": "Bảng giá", "group": "Sản phẩm & giá"},
    {"name": "Item Price", "label": "Giá sản phẩm", "group": "Sản phẩm & giá"},
    {"name": "Item", "label": "Sản phẩm", "group": "Sản phẩm & giá"},
    {"name": "Quotation", "label": "Báo giá", "group": "Bán hàng"},
    {"name": "Sales Order", "label": "Đơn bán hàng", "group": "Bán hàng"},
    {"name": "Sales Invoice", "label": "Hóa đơn bán hàng", "group": "Bán hàng"},
    {"name": "Delivery Note", "label": "Phiếu giao hàng", "group": "Giao hàng"},
]
BUYING_DOCTYPE_SPECS = [
    {"name": "Supplier", "label": "Nhà cung cấp", "group": "Nhà cung cấp"},
    {"name": "Supplier Group", "label": "Nhóm nhà cung cấp", "group": "Nhà cung cấp"},
    {"name": "Material Request", "label": "Yêu cầu vật tư", "group": "Mua hàng"},
    {"name": "Request for Quotation", "label": "Yêu cầu báo giá", "group": "Mua hàng"},
    {"name": "Supplier Quotation", "label": "Báo giá nhà cung cấp", "group": "Mua hàng"},
    {"name": "Purchase Order", "label": "Đơn mua hàng", "group": "Mua hàng"},
    {"name": "Purchase Receipt", "label": "Phiếu nhập mua", "group": "Mua hàng"},
    {"name": "Purchase Invoice", "label": "Hóa đơn mua hàng", "group": "Mua hàng"},
    {"name": "Item", "label": "Sản phẩm", "group": "Sản phẩm & giá"},
    {"name": "Item Price", "label": "Giá sản phẩm", "group": "Sản phẩm & giá"},
    {"name": "Price List", "label": "Bảng giá", "group": "Sản phẩm & giá"},
]
STOCK_DOCTYPE_SPECS = [
    {"name": "Item", "label": "Sản phẩm", "group": "Kho hàng"},
    {"name": "Warehouse", "label": "Kho", "group": "Kho hàng"},
    {"name": "Material Request", "label": "Yêu cầu vật tư", "group": "Kho hàng"},
    {"name": "Purchase Receipt", "label": "Phiếu nhập mua", "group": "Nhập xuất kho"},
    {"name": "Delivery Note", "label": "Phiếu giao hàng", "group": "Nhập xuất kho"},
    {"name": "Stock Entry", "label": "Phiếu kho", "group": "Nhập xuất kho"},
    {"name": "Stock Reconciliation", "label": "Kiểm kê kho", "group": "Nhập xuất kho"},
    {"name": "Stock Ledger Entry", "label": "Sổ kho", "group": "Sổ kho", "readonly": True},
    {"name": "Stock Settings", "label": "Cài đặt kho", "group": "Thiết lập kho"},
]
SUPPORT_DOCTYPE_SPECS = [
    {"name": "Issue", "label": "Yêu cầu hỗ trợ", "group": "Support"},
    {"name": "Warranty Claim", "label": "Bảo hành", "group": "Support"},
    {"name": "Maintenance Schedule", "label": "Lịch bảo trì", "group": "Support"},
    {"name": "Maintenance Visit", "label": "Lần bảo trì", "group": "Support"},
    {"name": "Customer", "label": "Khách hàng", "group": "Khách hàng"},
    {"name": "Contact", "label": "Liên hệ", "group": "Khách hàng"},
    {"name": "Address", "label": "Địa chỉ", "group": "Khách hàng"},
]
PROJECT_DOCTYPE_SPECS = [
    {"name": "Project", "label": "Dự án", "group": "Dự án"},
    {"name": "Task", "label": "Công việc", "group": "Dự án"},
    {"name": "Timesheet", "label": "Bảng chấm giờ", "group": "Dự án"},
    {"name": "ToDo", "label": "Việc cần làm", "group": "Dự án"},
]


def specs_in_groups(specs, *groups):
    """Return profile specs belonging to the requested business groups."""
    allowed_groups = set(groups)
    return [spec for spec in specs if spec.get("group") in allowed_groups]


BUSINESS_PERMISSION_PROFILES = [
    {
        "key": "accounting",
        "label": "Kế toán - Toàn bộ",
        "department_keywords": ["kế toán", "accounting"],
        "role_names": {"Accounts User", "Accounts Manager"},
        "doctype_specs": ACCOUNTING_DOCTYPE_SPECS,
        "report_modules": ["VN Accounting"],
    },
    {
        "key": "hr",
        "label": "Nhân sự - Toàn bộ",
        "department_keywords": ["nhân sự", "hành chính nhân sự", "hr", "human resource"],
        "role_names": {"HR User", "HR Manager", "Leave Approver", "Expense Approver"},
        "doctype_specs": HR_DOCTYPE_SPECS,
        "report_modules": ["HR"],
    },
    {
        "key": "sales",
        "label": "Bán hàng - Toàn bộ",
        "department_keywords": ["sales", "bán hàng", "kinh doanh"],
        "role_names": {"Sales User", "Sales Manager", "Sales Master Manager"},
        "doctype_specs": SALES_DOCTYPE_SPECS,
        "report_modules": ["CRM", "Selling"],
    },
    {
        "key": "buying",
        "label": "Mua hàng - Toàn bộ",
        "department_keywords": ["mua hàng", "purchase", "buying", "procurement"],
        "role_names": {"Purchase User", "Purchase Manager", "Purchase Master Manager"},
        "doctype_specs": BUYING_DOCTYPE_SPECS,
        "report_modules": ["Buying"],
    },
    {
        "key": "stock",
        "label": "Kho - Toàn bộ",
        "department_keywords": ["kho", "warehouse", "stock", "logistics"],
        "role_names": {"Stock User", "Stock Manager"},
        "doctype_specs": STOCK_DOCTYPE_SPECS,
        "report_modules": ["Stock"],
    },
    {
        "key": "support",
        "label": "Chăm sóc khách hàng",
        "department_keywords": ["support", "cskh", "chăm sóc khách hàng", "bảo hành", "maintenance"],
        "role_names": {"Support Team", "Maintenance User", "Maintenance Manager"},
        "doctype_specs": SUPPORT_DOCTYPE_SPECS,
        "report_modules": ["Support"],
    },
    {
        "key": "projects",
        "label": "Dự án",
        "department_keywords": ["project", "projects", "dự án"],
        "role_names": {"Projects User", "Projects Manager"},
        "doctype_specs": PROJECT_DOCTYPE_SPECS,
        "report_modules": ["Projects"],
    },
    # Granular cross-department catalogs. These profiles have no automatic
    # department/role matching; an administrator must explicitly add them to
    # a permission scope.
    {
        "key": "accounting_setup",
        "label": "Kế toán - Thiết lập",
        "doctype_specs": specs_in_groups(ACCOUNTING_DOCTYPE_SPECS, "Thiết lập kế toán"),
        "report_modules": [],
    },
    {
        "key": "accounting_cash_banking",
        "label": "Kế toán - Tiền và ngân hàng",
        "doctype_specs": specs_in_groups(ACCOUNTING_DOCTYPE_SPECS, "Tiền & ngân hàng"),
        "report_modules": [],
    },
    {
        "key": "accounting_ledger",
        "label": "Kế toán - Sổ kế toán",
        "doctype_specs": specs_in_groups(ACCOUNTING_DOCTYPE_SPECS, "Sổ kế toán"),
        "report_modules": [],
    },
    {
        "key": "accounting_receivables",
        "label": "Kế toán - Bán hàng và công nợ phải thu",
        "doctype_specs": specs_in_groups(ACCOUNTING_DOCTYPE_SPECS, "Bán hàng & công nợ phải thu"),
        "report_modules": [],
    },
    {
        "key": "accounting_payables",
        "label": "Kế toán - Mua hàng và công nợ phải trả",
        "doctype_specs": specs_in_groups(ACCOUNTING_DOCTYPE_SPECS, "Mua hàng & công nợ phải trả"),
        "report_modules": [],
    },
    {
        "key": "accounting_assets",
        "label": "Kế toán - Tài sản",
        "doctype_specs": specs_in_groups(ACCOUNTING_DOCTYPE_SPECS, "Tài sản"),
        "report_modules": [],
    },
    {
        "key": "hr_organization",
        "label": "Nhân sự - Tổ chức và vòng đời",
        "doctype_specs": specs_in_groups(HR_DOCTYPE_SPECS, "Tổ chức & nhân viên", "Vòng đời nhân sự"),
        "report_modules": [],
    },
    {
        "key": "hr_attendance",
        "label": "Nhân sự - Chấm công",
        "doctype_specs": specs_in_groups(HR_DOCTYPE_SPECS, "Chấm công"),
        "report_modules": [],
    },
    {
        "key": "hr_leave",
        "label": "Nhân sự - Nghỉ phép",
        "doctype_specs": specs_in_groups(HR_DOCTYPE_SPECS, "Nghỉ phép"),
        "report_modules": [],
    },
    {
        "key": "hr_expenses",
        "label": "Nhân sự - Chi phí nhân viên",
        "doctype_specs": specs_in_groups(HR_DOCTYPE_SPECS, "Chi phí nhân sự"),
        "report_modules": [],
    },
    {
        "key": "sales_crm",
        "label": "Bán hàng - CRM",
        "doctype_specs": specs_in_groups(SALES_DOCTYPE_SPECS, "CRM", "Khách hàng"),
        "report_modules": [],
    },
    {
        "key": "sales_pricing",
        "label": "Bán hàng - Sản phẩm và bảng giá",
        "doctype_specs": specs_in_groups(SALES_DOCTYPE_SPECS, "Sản phẩm & giá", "Thiết lập bán hàng"),
        "report_modules": [],
    },
    {
        "key": "sales_orders",
        "label": "Bán hàng - Đơn hàng và giao hàng",
        "doctype_specs": specs_in_groups(SALES_DOCTYPE_SPECS, "Bán hàng", "Giao hàng"),
        "report_modules": [],
    },
    {
        "key": "buying_procurement",
        "label": "Mua hàng - Nghiệp vụ mua",
        "doctype_specs": specs_in_groups(BUYING_DOCTYPE_SPECS, "Nhà cung cấp", "Mua hàng"),
        "report_modules": [],
    },
    {
        "key": "stock_operations",
        "label": "Kho - Vận hành kho",
        "doctype_specs": STOCK_DOCTYPE_SPECS,
        "report_modules": [],
    },
]
GRANULAR_PROFILE_PARENT = {
    "accounting_setup": "accounting",
    "accounting_cash_banking": "accounting",
    "accounting_ledger": "accounting",
    "accounting_receivables": "accounting",
    "accounting_payables": "accounting",
    "accounting_assets": "accounting",
    "hr_organization": "hr",
    "hr_attendance": "hr",
    "hr_leave": "hr",
    "hr_expenses": "hr",
    "sales_crm": "sales",
    "sales_pricing": "sales",
    "sales_orders": "sales",
    "buying_procurement": "buying",
    "stock_operations": "stock",
}
BUSINESS_DOCTYPE_SPECS = (
    ACCOUNTING_DOCTYPE_SPECS
    + HR_DOCTYPE_SPECS
    + SALES_DOCTYPE_SPECS
    + BUYING_DOCTYPE_SPECS
    + STOCK_DOCTYPE_SPECS
    + SUPPORT_DOCTYPE_SPECS
    + PROJECT_DOCTYPE_SPECS
)
ACCOUNTING_USER_SETUP_BASELINES = {
    "Account": {"select": 1, "read": 1, "report": 1, "export": 1, "print": 1},
    "Cost Center": {"select": 1, "read": 1, "report": 1, "export": 1, "print": 1},
    "Company": {"select": 1, "read": 1, "report": 1, "export": 1, "print": 1},
    "Payment Terms Template": {"select": 1, "read": 1, "report": 1, "export": 1, "print": 1},
    "Payment Term": {"select": 1, "read": 1, "report": 1, "export": 1, "print": 1},
    "Accounts Settings": {},
    "VN Accounting Settings": {},
}


def get_dashboard():
    assert_permission_manager_access()
    scopes = get_scopes_for_user()
    department_catalog = get_department_catalog(scopes)
    departments = [department["name"] for department in department_catalog]
    managed_departments = sorted({scope["department"] for scope in scopes if scope.get("department")})
    users = get_managed_users(scopes)
    employees = get_employee_catalog(scopes)
    roles = get_available_roles(scopes)
    permission_policy = get_role_permission_policy(scopes)

    return {
        "can_configure": is_permission_admin(),
        "can_manage_role_permissions": bool(scopes),
        "has_employee_doctype": frappe.db.exists("DocType", "Employee"),
        "scopes": scopes,
        "departments": departments,
        "managed_departments": managed_departments,
        "department_catalog": department_catalog,
        "employees": employees,
        "roles": roles,
        "users": users,
        "permission_policy": permission_policy,
        "stats": {
            "departments": len(departments),
            "users": len(users),
            "enabled_users": len([user for user in users if cint(user.get("enabled"))]),
            "roles": len(roles),
            "permission_items": len(permission_policy["items"]),
        },
        "generated_at": now(),
    }


def get_department_catalog(scopes):
    scope_departments = sorted({scope["department"] for scope in scopes if scope.get("department")})
    if not frappe.db.exists("DocType", "Department"):
        return [
            {
                "name": department,
                "label": department,
                "department_name": department,
                "company": None,
                "is_configured": 1,
            }
            for department in scope_departments
        ]

    filters = {}
    department_meta = frappe.get_meta("Department")
    if department_meta.has_field("is_group"):
        filters["is_group"] = 0
    if department_meta.has_field("disabled"):
        filters["disabled"] = 0
    if not is_permission_admin():
        filters["name"] = ["in", scope_departments or [""]]

    fields = ["name", "department_name", "company"]
    rows = frappe.get_all("Department", filters=filters, fields=fields, order_by="name asc")
    configured = set(scope_departments)
    departments = [
        {
            "name": row.name,
            "label": row.department_name or row.name,
            "department_name": row.department_name or row.name,
            "company": row.company,
            "is_configured": 1 if row.name in configured else 0,
        }
        for row in rows
    ]

    existing_names = {department["name"] for department in departments}
    for department in scope_departments:
        if department not in existing_names:
            departments.append(
                {
                    "name": department,
                    "label": department,
                    "department_name": department,
                    "company": None,
                    "is_configured": 1,
                }
            )

    return sorted(
        departments,
        key=lambda department: (
            0 if cint(department.get("is_configured")) else 1,
            (department.get("label") or department.get("name") or "").lower(),
            department.get("name") or "",
        ),
    )


def save_managed_user(data):
    data = parse_payload(data)
    email = normalize_email(data.get("email"))
    first_name = (data.get("first_name") or "").strip()
    last_name = (data.get("last_name") or "").strip()
    department = (data.get("department") or "").strip()
    employee_provided = "employee" in data
    employee = (data.get("employee") or "").strip() if employee_provided else None
    requested_roles = normalize_roles(data.get("roles"))
    enabled = 1 if cint(data.get("enabled", 1)) else 0

    if not email:
        frappe.throw(_("Email is required."))
    if not first_name:
        frappe.throw(_("First name is required."))
    if not department:
        frappe.throw(_("Department is required."))
    if not requested_roles and not get_existing_user_permission_role(email):
        frappe.throw(_("At least one role is required."))
    if email in STANDARD_USERS:
        frappe.throw(_("Standard users cannot be managed from this tool."), frappe.PermissionError)

    validate_email_address(email, throw=True)
    access = assert_department_access(department, requested_roles)

    user_exists = frappe.db.exists("User", email)
    if user_exists:
        assert_existing_user_can_be_managed(email, access["manageable_departments"])
        user = frappe.get_doc("User", email)
        is_new = False
    else:
        user = frappe.new_doc("User")
        user.email = email
        user.name = email
        is_new = True

    user.first_name = first_name
    user.last_name = last_name
    user.enabled = enabled
    user.user_type = access.get("user_type") or "System User"
    user.send_welcome_email = 0
    user.flags.ignore_permlevel_for_fields = ["roles"]
    if is_new:
        user.new_password = DEFAULT_INITIAL_PASSWORD
        user.last_password_reset_date = get_first_login_password_reset_date()
        user.flags.ignore_password_policy = True

    current_roles = {row.role for row in user.get("roles", []) if row.role}
    personal_role = get_existing_user_permission_role(email)
    has_personal_permissions = bool(personal_role and personal_role in current_roles)
    if has_personal_permissions:
        requested_roles = []

    allowed_roles = set(access["allowed_roles"])
    preserved_roles = current_roles - allowed_roles - {PERMISSION_MANAGER_ACCESS_ROLE}
    final_roles = sorted(preserved_roles | set(requested_roles))
    final_roles = apply_permission_manager_access_role(email, final_roles)

    user.set("roles", [])
    for role in final_roles:
        user.append("roles", {"role": role})

    if is_new:
        user.insert(ignore_permissions=True)
    else:
        user.save(ignore_permissions=True)

    sync_department_permission(email, department, access["manageable_departments"])
    if employee_provided:
        sync_employee_link(email, employee, department, access["manageable_departments"])
    add_audit_comment(
        email,
        department,
        requested_roles,
        "created" if is_new else "updated",
        employee=employee if employee_provided else get_employee_for_user(email).get("name"),
    )
    frappe.clear_cache(user=email)

    return get_user_summary(email, scopes=get_scopes_for_user())


def revoke_managed_department_access(user, department):
    user = normalize_email(user)
    if not user:
        frappe.throw(_("User is required."))
    if not department:
        frappe.throw(_("Department is required."))
    if user in STANDARD_USERS:
        frappe.throw(_("Standard users cannot be managed from this tool."), frappe.PermissionError)

    assert_user_is_manageable(user)
    scopes = get_scopes_for_user()
    assert_department_access(department, [])

    # Roles exclusive to this department (not shared with other managed depts)
    target_roles = set(get_allowed_roles_for_department(department, scopes))
    shared_roles = set()
    for scope in scopes:
        if scope.get("department") != department:
            shared_roles.update(r["role"] for r in scope.get("allowed_roles", []) if r.get("role"))
    roles_to_remove = (target_roles - shared_roles) - PROTECTED_ROLES

    personal_role = get_existing_user_permission_role(user)

    # Clean up personal role's Custom DocPerm entries that belong to THIS department's scope.
    # Do NOT blindly remove the personal role — it may hold permissions for other departments too.
    if personal_role:
        extra_profiles = get_extra_profile_keys_for_department(department, scopes)
        dept_items = get_permission_items(
            department=department,
            roles=list(target_roles),
            profile_keys=extra_profiles,
        )
        for item in dept_items:
            if item["type"] == "doctype":
                apply_doctype_role_permissions(item["name"], personal_role, {})
            elif item["type"] == "report":
                apply_report_role_permission(item, personal_role, 0)

        # Only remove personal role from user if no permissions remain at all
        has_remaining = bool(
            frappe.get_all("Custom DocPerm", filters={"role": personal_role, "permlevel": 0, "if_owner": 0}, limit=1)
            or frappe.get_all("Has Role", filters={"role": personal_role, "parenttype": "Custom Role"}, limit=1)
        )
        if not has_remaining:
            roles_to_remove.add(personal_role)

    doc = frappe.get_doc("User", user)
    current_roles = {row.role for row in doc.get("roles", []) if row.role}
    new_roles = apply_permission_manager_access_role(user, sorted(current_roles - roles_to_remove))
    doc.set("roles", [])
    for role_name in new_roles:
        doc.append("roles", {"role": role_name})
    doc.flags.ignore_permlevel_for_fields = ["roles"]
    doc.save(ignore_permissions=True)

    # Remove User Permission for this department
    existing_permissions = frappe.get_all(
        "User Permission",
        filters={"user": user, "allow": "Department", "for_value": department},
        pluck="name",
    )
    for name in existing_permissions:
        frappe.delete_doc("User Permission", name, force=True, ignore_permissions=True)

    add_audit_comment(user, department, [], "department access revoked")
    frappe.clear_cache(user=user)
    return get_dashboard()


def disable_managed_user(user):
    user = normalize_email(user)
    if not user:
        frappe.throw(_("User is required."))
    if user == frappe.session.user:
        frappe.throw(_("You cannot disable your own account from this tool."))
    if user in STANDARD_USERS:
        frappe.throw(_("Standard users cannot be disabled from this tool."), frappe.PermissionError)

    assert_user_is_manageable(user)
    scopes = get_scopes_for_user()
    frappe.db.set_value("User", user, "enabled", 0, update_modified=True)
    add_audit_comment(user, get_user_department(user, scopes=scopes), [], "disabled")
    frappe.clear_cache(user=user)
    return get_user_summary(user, scopes=scopes)


def save_role_permissions(data):
    data = parse_payload(data)
    department = (data.get("department") or "").strip()
    role = (data.get("role") or "").strip()
    entries = data.get("entries") or []

    assert_role_permission_access(department, role)
    scopes = get_scopes_for_user()
    extra_profiles = get_extra_profile_keys_for_department(department, scopes)
    allowed_items = {
        item["key"]: item
        for item in get_permission_items(department=department, roles=[role], profile_keys=extra_profiles)
    }

    for entry in entries:
        key = (entry.get("key") or "").strip()
        if key not in allowed_items:
            frappe.throw(_("Permission item is outside the delegated scope: {0}").format(frappe.bold(key)))

        item = allowed_items[key]
        permissions = normalize_permission_payload(entry.get("permissions"), item)
        if item["type"] == "doctype":
            apply_doctype_role_permissions(item["name"], role, permissions)
        elif item["type"] == "report":
            apply_report_role_permission(item, role, cint(permissions.get("read")))

    frappe.clear_cache()
    return get_dashboard()


def get_user_permissions(user, department=None):
    user = normalize_email(user)
    if not user:
        frappe.throw(_("User is required."))

    assert_user_is_manageable(user)
    scopes = get_scopes_for_user()
    department = (department or "").strip() or get_user_department(user, scopes=scopes)
    role_names = get_permission_source_roles_for_user(user, department, scopes)
    department_roles = get_allowed_roles_for_department(department, scopes)
    extra_profiles = get_extra_profile_keys_for_department(department, scopes)
    items = get_permission_items(
        department=department,
        roles=role_names + department_roles,
        profile_keys=extra_profiles,
    )
    permissions = {
        item["key"]: get_item_permissions_for_roles(item, role_names)
        for item in items
    }

    return {
        "user": get_user_summary(user, department=department, scopes=scopes),
        "department": department,
        "mode": "user" if get_existing_user_permission_role(user) in role_names else "role",
        "source_roles": role_names,
        "columns": PERMISSION_COLUMNS,
        "items": items,
        "permissions": permissions,
    }


def save_user_permissions(data):
    data = parse_payload(data)
    user = normalize_email(data.get("user"))
    entries = data.get("entries") or []

    if not user:
        frappe.throw(_("User is required."))
    if user == frappe.session.user:
        frappe.throw(_("You cannot edit your own detailed permissions from this tool."))
    if not entries:
        frappe.throw(_("Permission entries are required."))

    assert_user_is_manageable(user)
    scopes = get_scopes_for_user()
    department = (data.get("department") or "").strip() or get_user_department(user, scopes=scopes)
    access = assert_department_access(department, [])
    role = ensure_user_permission_role(user)
    sync_department_permission(user, department, access["manageable_departments"])
    assign_user_permission_role(user, role, department, scopes)
    department_roles = get_allowed_roles_for_department(department, scopes)
    extra_profiles = get_extra_profile_keys_for_department(department, scopes)
    allowed_items = {
        item["key"]: item
        for item in get_permission_items(
            department=department,
            roles=department_roles,
            profile_keys=extra_profiles,
        )
    }
    cleanup_personal_role_permissions_outside_items(role, allowed_items.values())

    for entry in entries:
        key = (entry.get("key") or "").strip()
        if key not in allowed_items:
            frappe.throw(_("Permission item is outside the delegated scope: {0}").format(frappe.bold(key)))

        item = allowed_items[key]
        permissions = normalize_permission_payload(entry.get("permissions"), item)
        if item["type"] == "doctype":
            apply_doctype_role_permissions(item["name"], role, permissions)
        elif item["type"] == "report":
            apply_report_role_permission(item, role, cint(permissions.get("read")))

    has_remaining = bool(
        frappe.get_all("Custom DocPerm", filters={"role": role, "permlevel": 0, "if_owner": 0}, limit=1)
        or frappe.get_all("Has Role", filters={"role": role, "parenttype": "Custom Role"}, limit=1)
    )
    if not has_remaining:
        revoke_personal_permissions(user, role, department)
        add_audit_comment(user, department, [], "user permissions cleared")
    else:
        add_audit_comment(user, department, [role], "user permissions updated")
    frappe.clear_cache(user=user)
    frappe.clear_cache()
    return get_dashboard()


def revoke_personal_permissions(user, role, department):
    """Remove personal role assignment and User Permission when all permissions are cleared."""
    doc = frappe.get_doc("User", user)
    current_roles = {row.role for row in doc.get("roles", []) if row.role}
    if role in current_roles:
        new_roles = sorted(current_roles - {role})
        new_roles = apply_permission_manager_access_role(user, new_roles)
        doc.set("roles", [])
        for role_name in new_roles:
            doc.append("roles", {"role": role_name})
        doc.flags.ignore_permlevel_for_fields = ["roles"]
        doc.save(ignore_permissions=True)

    existing = frappe.get_all(
        "User Permission",
        filters={"user": user, "allow": "Department", "for_value": department},
        pluck="name",
    )
    for name in existing:
        frappe.delete_doc("User Permission", name, force=True, ignore_permissions=True)


def get_scopes_for_user(user: str | None = None):
    user = user or frappe.session.user
    user_roles = set(frappe.get_roles(user))
    filters = {"enabled": 1}
    fields = [
        "name",
        "scope_name",
        "department",
        "manager_role",
        "manager_user",
        "user_type",
    ]

    scope_names = []
    if user_roles & ADMIN_ROLES or user == "Administrator":
        scope_names = frappe.get_all("DCNET Permission Scope", filters=filters, pluck="name")
    else:
        role_scopes = frappe.get_all(
            "DCNET Permission Scope",
            filters={**filters, "manager_role": ["in", list(user_roles) or [""]]},
            pluck="name",
        )
        user_scopes = frappe.get_all(
            "DCNET Permission Scope",
            filters={**filters, "manager_user": user},
            pluck="name",
        )
        scope_names = sorted(set(role_scopes + user_scopes))

    scopes = []
    for name in scope_names:
        doc = frappe.get_doc("DCNET Permission Scope", name)
        row = {field: doc.get(field) for field in fields}
        row["allowed_roles"] = [
            {
                "role": role.role,
                "is_default": cint(role.is_default),
                "notes": role.notes,
            }
            for role in doc.allowed_roles
            if role.role
        ]
        row["extra_permission_profiles"] = [
            {
                "profile": normalize_profile_key(profile.profile),
                "label": get_permission_profile_label(profile.profile),
                "notes": profile.notes,
            }
            for profile in doc.get("extra_permission_profiles", [])
            if normalize_profile_key(profile.profile)
        ]
        scopes.append(row)

    return sorted(scopes, key=lambda item: (item.get("department") or "", item.get("scope_name") or ""))


def get_role_permission_policy(scopes):
    role_names = sorted(
        {
            role["role"]
            for scope in scopes
            for role in scope.get("allowed_roles", [])
            if role.get("role") and role.get("role") not in PROTECTED_ROLES
        }
    )
    items = get_permission_items_for_scopes(scopes)
    role_permissions = {}

    for role in role_names:
        role_permissions[role] = {item["key"]: get_item_role_permissions(item, role) for item in items}

    return {
        "columns": PERMISSION_COLUMNS,
        "items": items,
        "role_permissions": role_permissions,
    }


def get_permission_items_for_scopes(scopes):
    profile_keys = set()
    for scope in scopes or []:
        roles = [row["role"] for row in scope.get("allowed_roles", []) if row.get("role")]
        extra_profiles = [row["profile"] for row in scope.get("extra_permission_profiles", []) if row.get("profile")]
        for profile in get_permission_profiles(scope.get("department"), roles, extra_profiles):
            profile_keys.add(profile["key"])

    if not profile_keys:
        return []

    profiles = [profile for profile in BUSINESS_PERMISSION_PROFILES if profile["key"] in profile_keys]
    return get_permission_items(profiles=profiles)


def get_permission_items(department=None, roles=None, profiles=None, profile_keys=None):
    profiles = profiles if profiles is not None else get_permission_profiles(department, roles, profile_keys)
    if not profiles:
        return []

    items = []
    seen_doctypes = set()
    for spec in get_profile_doctype_specs(profiles):
        if not frappe.db.exists("DocType", spec["name"]):
            continue
        if spec["name"] in seen_doctypes:
            continue

        meta = frappe.get_meta(spec["name"])
        if cint(meta.istable):
            continue

        permission_fields = get_allowed_permission_fields(meta, spec)
        items.append(
            {
                "key": make_permission_item_key("doctype", spec["name"]),
                "type": "doctype",
                "name": spec["name"],
                "label": source_label(spec["label"], spec["name"]),
                "group": source_group(spec["group"]),
                "module": meta.module,
                "is_submittable": cint(meta.is_submittable),
                "permission_fields": permission_fields,
            }
        )
        seen_doctypes.add(spec["name"])

    report_modules = get_profile_report_modules(profiles)
    if not report_modules:
        return items

    for report in frappe.get_all(
        "Report",
        filters={"module": ["in", report_modules], "disabled": 0},
        fields=["name", "module", "ref_doctype", "report_type"],
        order_by="module asc, name asc",
    ):
        items.append(
            {
                "key": make_permission_item_key("report", report.name),
                "type": "report",
                "name": report.name,
                "label": report.name,
                "group": get_report_group(report.module),
                "module": report.module,
                "ref_doctype": report.ref_doctype,
                "report_type": report.report_type,
                "permission_fields": REPORT_PERMISSION_FIELDS,
            }
        )

    return items


def get_permission_profiles(department=None, roles=None, profile_keys=None):
    department_text = normalize_match_text(department)
    role_names = set(roles or [])
    explicit_keys = {normalize_profile_key(profile_key) for profile_key in profile_keys or []}
    explicit_keys.discard("")
    profiles = []

    for profile in BUSINESS_PERMISSION_PROFILES:
        profile_roles = set(profile.get("role_names") or [])
        explicit_match = profile.get("key") in explicit_keys
        role_matches = bool(role_names & profile_roles)
        department_matches = any(
            normalize_match_text(keyword) in department_text
            for keyword in profile.get("department_keywords", [])
            if keyword
        )
        if explicit_match or role_matches or department_matches:
            profiles.append(profile)

    return profiles


def get_extra_profile_keys_for_department(department, scopes):
    keys = set()
    for scope in scopes or []:
        if scope.get("department") != department:
            continue
        keys.update(
            normalize_profile_key(row.get("profile"))
            for row in scope.get("extra_permission_profiles", [])
            if row.get("profile")
        )
    keys.discard("")
    return sorted(keys)


def get_permission_profile_keys():
    return [profile["key"] for profile in BUSINESS_PERMISSION_PROFILES]


def get_permission_profile_label(profile_key):
    normalized = normalize_profile_key(profile_key)
    for profile in BUSINESS_PERMISSION_PROFILES:
        if profile["key"] == normalized:
            return profile.get("label") or profile["key"]
    return profile_key or ""


def get_inherent_permission_profile_keys(department=None, roles=None):
    """Return catalogs already supplied by a scope's department and roles."""
    matched_parent_keys = {
        profile["key"]
        for profile in get_permission_profiles(department=department, roles=roles)
        if profile["key"] not in GRANULAR_PROFILE_PARENT
    }
    return {
        profile["key"]
        for profile in BUSINESS_PERMISSION_PROFILES
        if profile["key"] in matched_parent_keys
        or GRANULAR_PROFILE_PARENT.get(profile["key"]) in matched_parent_keys
    }


def get_available_extra_permission_profiles(department=None, roles=None):
    """Return cross-department catalogs that are not inherent to the scope."""
    inherent_keys = get_inherent_permission_profile_keys(department, roles)
    return [
        {"key": profile["key"], "label": profile["label"]}
        for profile in BUSINESS_PERMISSION_PROFILES
        if profile["key"] not in inherent_keys
    ]


@frappe.whitelist(methods=["GET"])
def get_extra_permission_profile_options(department=None, roles=None):
    """Return permitted extra catalogs for the Permission Scope form."""
    if not is_permission_admin():
        frappe.throw(_("Only permission administrators can configure scopes."), frappe.PermissionError)
    parsed_roles = roles
    if isinstance(roles, str):
        try:
            parsed_roles = json.loads(roles)
        except (TypeError, ValueError):
            frappe.throw(_("Invalid role list."), frappe.ValidationError)
    if not isinstance(parsed_roles, (list, tuple, set)):
        parsed_roles = []
    return get_available_extra_permission_profiles(department, parsed_roles)


def normalize_profile_key(value):
    text = normalize_match_text(value)
    # Keep old combined labels readable after switching UI source strings to English.
    aliases = {
        "accounting / kế toán": "accounting",
        "kế toán / accounting": "accounting",
        "ke toan / accounting": "accounting",
        "ke toan": "accounting",
        "kế toán": "accounting",
        "accounts": "accounting",
        "kế toán - toàn bộ": "accounting",
        "hr - attendance": "hr",
        "hr / nhân sự - chấm công": "hr",
        "nhân sự - chấm công / hr - attendance": "hr",
        "nhan su - cham cong / hr - attendance": "hr",
        "nhan su": "hr",
        "nhân sự": "hr",
        "human resources": "hr",
        "nhân sự - toàn bộ": "hr",
        "accounting - setup": "accounting_setup",
        "kế toán - thiết lập": "accounting_setup",
        "accounting - cash & banking": "accounting_cash_banking",
        "kế toán - tiền và ngân hàng": "accounting_cash_banking",
        "accounting - ledger": "accounting_ledger",
        "kế toán - sổ kế toán": "accounting_ledger",
        "accounting - sales & receivables": "accounting_receivables",
        "kế toán - bán hàng và công nợ phải thu": "accounting_receivables",
        "accounting - buying & payables": "accounting_payables",
        "kế toán - mua hàng và công nợ phải trả": "accounting_payables",
        "accounting - assets": "accounting_assets",
        "kế toán - tài sản": "accounting_assets",
        "hr - organization & lifecycle": "hr_organization",
        "nhân sự - tổ chức và vòng đời": "hr_organization",
        "hr - attendance only": "hr_attendance",
        "nhân sự - chấm công": "hr_attendance",
        "hr - leave": "hr_leave",
        "nhân sự - nghỉ phép": "hr_leave",
        "hr - employee expenses": "hr_expenses",
        "nhân sự - chi phí nhân viên": "hr_expenses",
        "sales - crm": "sales_crm",
        "bán hàng - crm": "sales_crm",
        "sales - products & pricing": "sales_pricing",
        "bán hàng - sản phẩm và bảng giá": "sales_pricing",
        "sales - orders & delivery": "sales_orders",
        "bán hàng - đơn hàng và giao hàng": "sales_orders",
        "buying - procurement": "buying_procurement",
        "mua hàng - nghiệp vụ mua": "buying_procurement",
        "stock - warehouse operations": "stock_operations",
        "kho - vận hành kho": "stock_operations",
        "sales / bán hàng": "sales",
        "bán hàng / sales": "sales",
        "ban hang / sales": "sales",
        "ban hang": "sales",
        "bán hàng": "sales",
        "kinh doanh": "sales",
        "bán hàng - toàn bộ": "sales",
        "buying / mua hàng": "buying",
        "mua hàng / buying": "buying",
        "mua hang / buying": "buying",
        "mua hang": "buying",
        "mua hàng": "buying",
        "purchase": "buying",
        "mua hàng - toàn bộ": "buying",
        "stock / kho": "stock",
        "kho / stock": "stock",
        "kho": "stock",
        "warehouse": "stock",
        "kho - toàn bộ": "stock",
        "support / cskh": "support",
        "cskh / support": "support",
        "chăm sóc khách hàng": "support",
        "cham soc khach hang": "support",
        "customer support": "support",
        "chăm sóc khách hàng": "support",
        "projects / dự án": "projects",
        "dự án / projects": "projects",
        "du an / projects": "projects",
        "du an": "projects",
        "dự án": "projects",
    }
    return aliases.get(text, text)


def source_label(vietnamese_label, english_label):
    vietnamese_label = str(vietnamese_label or "").strip()
    english_label = str(english_label or "").strip()
    return english_label or vietnamese_label


def source_group(group_label):
    group_label = str(group_label or "").strip()
    english_label = GROUP_LABELS.get(group_label)
    return source_label(group_label, english_label)


def get_profile_doctype_specs(profiles):
    specs = []
    for profile in profiles or []:
        specs.extend(profile.get("doctype_specs") or [])
    return specs


def get_profile_report_modules(profiles):
    modules = []
    for profile in profiles or []:
        modules.extend(profile.get("report_modules") or [])
    return sorted(set(modules))


def get_report_group(module):
    labels = {
        "VN Accounting": "Vietnam Accounting Reports",
        "HR": "HR Reports",
        "CRM": "CRM Reports",
        "Selling": "Selling Reports",
        "Buying": "Buying Reports",
        "Stock": "Stock Reports",
        "Support": "Support Reports",
        "Projects": "Project Reports",
    }
    return labels.get(module) or _("Reports")


def normalize_match_text(value):
    return str(value or "").strip().casefold()


def get_allowed_permission_fields(meta, spec):
    if spec.get("readonly"):
        return ["select", "read", "report", "export", "print"]

    fields = list(DOCTYPE_PERMISSION_FIELDS)
    if cint(meta.issingle):
        fields = [field for field in fields if field not in {"create", "delete", "submit", "cancel", "amend"}]
    if not cint(meta.is_submittable):
        fields = [field for field in fields if field not in {"submit", "cancel", "amend"}]
    return fields


def get_item_role_permissions(item, role):
    if item["type"] == "report":
        return {"read": cint(role in get_report_roles(item["name"]))}

    permissions = get_effective_doctype_permissions(item["name"], role)
    return {field: cint(permissions.get(field)) for field in item["permission_fields"]}


def get_item_permissions_for_roles(item, roles):
    out = {field: 0 for field in item["permission_fields"]}
    for role in roles:
        role_permissions = get_item_role_permissions(item, role)
        for field in out:
            out[field] = 1 if out[field] or cint(role_permissions.get(field)) else 0
    return out


def get_permission_source_roles_for_user(user, department, scopes):
    personal_role = get_existing_user_permission_role(user)
    explicit_roles = set(get_user_role_names(user))
    if personal_role and personal_role in explicit_roles:
        return [personal_role]

    allowed_roles = set(get_allowed_roles_for_department(department, scopes))
    return sorted(explicit_roles & allowed_roles)


def get_effective_doctype_permissions(doctype, role):
    if frappe.db.exists("Custom DocPerm", {"parent": doctype}):
        source_doctype = "Custom DocPerm"
    else:
        source_doctype = "DocPerm"

    rows = frappe.get_all(
        source_doctype,
        filters={"parent": doctype, "role": role, "permlevel": 0, "if_owner": 0},
        fields=DOCTYPE_PERMISSION_FIELDS,
        limit=1,
    )
    return rows[0] if rows else {}


def assert_role_permission_access(department, role):
    if not department:
        frappe.throw(_("Department is required."))
    if not role:
        frappe.throw(_("Role is required."))
    if role in PROTECTED_ROLES:
        frappe.throw(_("Role {0} cannot be managed from this tool.").format(frappe.bold(role)), frappe.PermissionError)

    scopes = get_scopes_for_user()
    matching_scopes = [scope for scope in scopes if scope.get("department") == department]
    allowed_roles = {
        row["role"]
        for scope in matching_scopes
        for row in scope.get("allowed_roles", [])
        if row.get("role")
    }
    if role not in allowed_roles:
        frappe.throw(
            _("You do not have permission to manage role {0} in department {1}.").format(
                frappe.bold(role), frappe.bold(department)
            ),
            frappe.PermissionError,
        )


def normalize_permission_payload(permissions, item):
    permissions = frappe._dict(permissions or {})
    allowed = set(item["permission_fields"])
    values = {field: 1 if cint(permissions.get(field)) else 0 for field in allowed}

    write_like = {"write", "create", "delete", "submit", "cancel", "amend", "report", "export", "print", "email"}
    if any(values.get(field) for field in write_like):
        values["read"] = 1
    if values.get("amend") and "cancel" in allowed:
        values["cancel"] = 1
    if values.get("cancel") and "submit" in allowed:
        values["submit"] = 1
    if values.get("submit") or values.get("cancel") or values.get("amend"):
        values["write"] = 1
        values["read"] = 1
    if values.get("read") and "select" in allowed:
        values["select"] = 1

    return values


def normalize_existing_doctype_permission_dependencies(doctype):
    """Repair copied Custom DocPerm rows before Frappe validates the whole DocType.

    Some installed apps may ship DocPerm rows that are valid enough to install but
    become blockers when Frappe copies them to Custom DocPerm and validates every
    row during a permission edit. Keep this at the customization layer so the
    source app remains untouched.
    """
    if not frappe.db.exists("DocType", doctype) or not frappe.db.table_exists("Custom DocPerm"):
        return

    meta = frappe.get_meta(doctype)

    if not cint(meta.is_submittable):
        frappe.db.sql(
            """
            UPDATE `tabCustom DocPerm`
               SET `submit` = 0, `cancel` = 0, `amend` = 0
             WHERE `parent` = %s
               AND (
                   COALESCE(`submit`, 0) = 1
                OR COALESCE(`cancel`, 0) = 1
                OR COALESCE(`amend`, 0) = 1
               )
            """,
            (doctype,),
        )
    else:
        frappe.db.sql(
            """
            UPDATE `tabCustom DocPerm`
               SET `submit` = 1
             WHERE `parent` = %s
               AND COALESCE(`cancel`, 0) = 1
               AND COALESCE(`submit`, 0) = 0
            """,
            (doctype,),
        )
        frappe.db.sql(
            """
            UPDATE `tabCustom DocPerm`
               SET `cancel` = 1, `submit` = 1
             WHERE `parent` = %s
               AND COALESCE(`amend`, 0) = 1
               AND COALESCE(`cancel`, 0) = 0
            """,
            (doctype,),
        )
        frappe.db.sql(
            """
            UPDATE `tabCustom DocPerm`
               SET `write` = 1, `read` = 1
             WHERE `parent` = %s
               AND (
                   COALESCE(`submit`, 0) = 1
                OR COALESCE(`cancel`, 0) = 1
                OR COALESCE(`amend`, 0) = 1
               )
               AND COALESCE(`write`, 0) = 0
            """,
            (doctype,),
        )

    if not cint(meta.allow_import):
        frappe.db.sql(
            """
            UPDATE `tabCustom DocPerm`
               SET `import` = 0
             WHERE `parent` = %s
               AND COALESCE(`import`, 0) = 1
            """,
            (doctype,),
        )
    else:
        frappe.db.sql(
            """
            UPDATE `tabCustom DocPerm`
               SET `create` = 1, `read` = 1
             WHERE `parent` = %s
               AND COALESCE(`import`, 0) = 1
               AND COALESCE(`create`, 0) = 0
            """,
            (doctype,),
        )


def apply_doctype_role_permissions(doctype, role, permissions):
    from frappe.core.doctype.doctype.doctype import validate_permissions_for_doctype
    from frappe.permissions import setup_custom_perms

    if not frappe.db.exists("DocType", doctype):
        return

    setup_custom_perms(doctype)
    normalize_existing_doctype_permission_dependencies(doctype)
    filters = {"parent": doctype, "role": role, "permlevel": 0, "if_owner": 0}
    names = frappe.get_all("Custom DocPerm", filters=filters, pluck="name")
    values = {field: cint(permissions.get(field)) for field in DOCTYPE_PERMISSION_FIELDS}

    if not any(values.values()):
        for name in names:
            frappe.delete_doc("Custom DocPerm", name, force=True, ignore_permissions=True)
        normalize_existing_doctype_permission_dependencies(doctype)
        validate_permissions_for_doctype(doctype)
        frappe.clear_cache(doctype=doctype)
        return

    if names:
        doc = frappe.get_doc("Custom DocPerm", names[0])
    else:
        doc = frappe.new_doc("Custom DocPerm")
        doc.parent = doctype
        doc.parenttype = "DocType"
        doc.parentfield = "permissions"
        doc.role = role
        doc.permlevel = 0
        doc.if_owner = 0

    doc.update(values)
    if doc.is_new():
        doc.insert(ignore_permissions=True)
    else:
        doc.save(ignore_permissions=True)

    for duplicate in names[1:]:
        frappe.delete_doc("Custom DocPerm", duplicate, force=True, ignore_permissions=True)

    normalize_existing_doctype_permission_dependencies(doctype)
    validate_permissions_for_doctype(doctype)
    frappe.clear_cache(doctype=doctype)


def cleanup_personal_role_permissions_outside_items(role, allowed_items):
    if not is_user_permission_role(role):
        return

    allowed_doctypes = {
        item["name"]
        for item in allowed_items
        if item.get("type") == "doctype" and item.get("name")
    }
    guarded_doctypes = {spec["name"] for spec in BUSINESS_DOCTYPE_SPECS}
    changed_doctypes = set()

    for row in frappe.get_all(
        "Custom DocPerm",
        filters={"role": role, "permlevel": 0, "if_owner": 0},
        fields=["name", "parent"],
    ):
        if row.parent not in guarded_doctypes or row.parent in allowed_doctypes:
            continue
        frappe.delete_doc("Custom DocPerm", row.name, force=True, ignore_permissions=True)
        changed_doctypes.add(row.parent)

    if not changed_doctypes:
        return

    from frappe.core.doctype.doctype.doctype import validate_permissions_for_doctype

    for doctype in changed_doctypes:
        normalize_existing_doctype_permission_dependencies(doctype)
        validate_permissions_for_doctype(doctype)
        frappe.clear_cache(doctype=doctype)


def apply_report_role_permission(item, role, enabled):
    report_name = item["name"]
    report = frappe.get_doc("Report", report_name)
    standard_roles = set(get_standard_report_roles(report))
    effective_roles = set(get_report_roles(report_name))

    if enabled:
        effective_roles.add(role)
        if report.ref_doctype:
            apply_doctype_role_permissions(
                report.ref_doctype,
                role,
                {"select": 1, "read": 1, "report": 1, "export": 1, "print": 1},
            )
    else:
        effective_roles.discard(role)

    custom_role_name = frappe.db.get_value("Custom Role", {"report": report_name}, "name")
    if effective_roles == standard_roles:
        if custom_role_name:
            frappe.delete_doc("Custom Role", custom_role_name, force=True, ignore_permissions=True)
        return

    if custom_role_name:
        custom_role = frappe.get_doc("Custom Role", custom_role_name)
    else:
        custom_role = frappe.new_doc("Custom Role")
        custom_role.report = report_name
        custom_role.ref_doctype = report.ref_doctype

    custom_role.set("roles", [])
    for role_name in sorted(effective_roles):
        custom_role.append("roles", {"role": role_name, "parenttype": "Custom Role"})

    if custom_role.is_new():
        custom_role.insert(ignore_permissions=True)
    else:
        custom_role.save(ignore_permissions=True)


def apply_default_permission_baselines():
    if not frappe.db.exists("Role", "Accounts User"):
        return

    for doctype, permissions in ACCOUNTING_USER_SETUP_BASELINES.items():
        if frappe.db.exists("DocType", doctype):
            apply_doctype_role_permissions(doctype, "Accounts User", permissions)


def get_report_roles(report_name):
    custom_role_name = frappe.db.get_value("Custom Role", {"report": report_name}, "name")
    if custom_role_name:
        custom_role = frappe.get_doc("Custom Role", custom_role_name)
        return [row.role for row in custom_role.roles if row.role]

    return get_standard_report_roles(frappe.get_doc("Report", report_name))


def get_standard_report_roles(report):
    return [row.role for row in report.roles if row.role]


def make_permission_item_key(item_type, name):
    return f"{item_type}::{name}"


def ensure_user_permission_role(user):
    role_name = get_user_permission_role_name(user)
    if frappe.db.exists("Role", role_name):
        return role_name

    role = frappe.new_doc("Role")
    role.role_name = role_name
    role.desk_access = 1
    role.is_custom = 1
    role.insert(ignore_permissions=True)
    return role_name


def get_existing_user_permission_role(user):
    role_name = get_user_permission_role_name(user)
    return role_name if frappe.db.exists("Role", role_name) else None


def get_user_permission_role_name(user):
    digest = hashlib.sha1(normalize_email(user).encode("utf-8")).hexdigest()[:12]
    return f"{USER_PERMISSION_ROLE_PREFIX}{digest}"


def is_user_permission_role(role):
    return str(role or "").startswith(USER_PERMISSION_ROLE_PREFIX)


def get_user_role_names(user):
    return sorted({row.role for row in frappe.get_doc("User", user).get("roles", []) if row.role})


def assign_user_permission_role(user, role, department, scopes):
    allowed_roles = set(get_allowed_roles_for_department(department, scopes))
    doc = frappe.get_doc("User", user)
    current_roles = {row.role for row in doc.get("roles", []) if row.role}
    preserved_roles = {
        role_name
        for role_name in current_roles
        if (
            role_name not in allowed_roles
            and role_name != PERMISSION_MANAGER_ACCESS_ROLE
            and not is_user_permission_role(role_name)
        )
    }
    final_roles = sorted(preserved_roles | {role})
    final_roles = apply_permission_manager_access_role(user, final_roles)

    doc.set("roles", [])
    for role_name in final_roles:
        doc.append("roles", {"role": role_name})

    doc.flags.ignore_permlevel_for_fields = ["roles"]
    doc.save(ignore_permissions=True)


def get_available_roles(scopes):
    role_names = sorted(
        {
            role["role"]
            for scope in scopes
            for role in scope.get("allowed_roles", [])
            if role.get("role")
        }
    )
    if not role_names:
        return []

    role_rows = frappe.get_all(
        "Role",
        filters={"name": ["in", role_names]},
        fields=["name", "role_name", "desk_access", "disabled"],
        order_by="name asc",
    )
    return [role for role in role_rows if not cint(role.get("disabled"))]


def get_employee_catalog(scopes):
    if not frappe.db.exists("DocType", "Employee"):
        return []

    departments = sorted({scope["department"] for scope in scopes if scope.get("department")})
    if not departments:
        return []

    employee_meta = frappe.get_meta("Employee")
    fields = ["name", "employee_name", "department", "company", "user_id"]
    if employee_meta.has_field("status"):
        fields.append("status")

    employees = frappe.get_all(
        "Employee",
        filters={"department": ["in", departments]},
        fields=fields,
        order_by="department asc, employee_name asc, name asc",
    )

    return [
        {
            "name": employee.name,
            "employee_name": employee.employee_name,
            "department": employee.department,
            "company": employee.company,
            "status": employee.get("status"),
            "user_id": employee.user_id,
        }
        for employee in employees
    ]


def get_managed_users(scopes):
    departments = sorted({scope["department"] for scope in scopes if scope.get("department")})
    if not departments:
        return []

    # Build role → set of departments from scopes
    role_to_departments = {}
    for scope in scopes:
        dept = scope.get("department")
        if not dept:
            continue
        for role_row in scope.get("allowed_roles", []):
            role = role_row.get("role")
            if role:
                role_to_departments.setdefault(role, set()).add(dept)

    # user → set of ALL matching departments
    user_all_departments = {}
    # user → primary department (first by priority: User Permission, Employee, role)
    user_primary_department = {}

    # 1. Explicit User Permission assignment
    permission_rows = frappe.get_all(
        "User Permission",
        filters={"allow": "Department", "for_value": ["in", departments]},
        fields=["user", "for_value", "is_default"],
        order_by="is_default desc, modified desc",
    )
    for row in permission_rows:
        user_all_departments.setdefault(row.user, set()).add(row.for_value)
        if row.user not in user_primary_department:
            user_primary_department[row.user] = row.for_value

    # 2. Employee link
    if frappe.db.exists("DocType", "Employee"):
        employee_rows = frappe.get_all(
            "Employee",
            filters={"department": ["in", departments]},
            fields=["user_id", "department", "employee_name"],
        )
        for row in employee_rows:
            if row.user_id:
                user_all_departments.setdefault(row.user_id, set()).add(row.department)
                if row.user_id not in user_primary_department:
                    user_primary_department[row.user_id] = row.department

    # 3. Role-based placement — user appears in every department whose scope grants their roles
    all_scope_roles = sorted(role_to_departments.keys())
    if all_scope_roles:
        for row in frappe.get_all(
            "Has Role",
            filters={"parenttype": "User", "role": ["in", all_scope_roles]},
            fields=["parent", "role"],
            order_by="parent asc, role asc",
        ):
            if row.parent in STANDARD_USERS:
                continue
            for dept in role_to_departments.get(row.role, []):
                user_all_departments.setdefault(row.parent, set()).add(dept)
                if row.parent not in user_primary_department:
                    user_primary_department[row.parent] = dept

    users = []
    for user in sorted(user_all_departments):
        if not frappe.db.exists("User", user):
            continue
        user_depts = sorted(user_all_departments[user] & set(departments))
        if not user_depts:
            continue
        primary = user_primary_department.get(user) or user_depts[0]
        summary = get_user_summary(user, department=primary, scopes=scopes)
        summary["departments"] = user_depts
        users.append(summary)

    return users


def get_role_inferred_user_departments(scopes, existing_user_departments=None):
    existing_user_departments = existing_user_departments or {}
    role_departments = {}
    for scope in sorted(scopes or [], key=lambda item: (item.get("department") or "", item.get("scope_name") or "")):
        department = scope.get("department")
        if not department:
            continue
        for row in scope.get("allowed_roles", []):
            role = row.get("role")
            if role:
                role_departments.setdefault(role, []).append(department)

    if not role_departments:
        return {}

    inferred = {}
    for row in frappe.get_all(
        "Has Role",
        filters={"parenttype": "User", "role": ["in", sorted(role_departments)]},
        fields=["parent", "role"],
        order_by="parent asc, role asc",
    ):
        if row.parent in STANDARD_USERS or row.parent in existing_user_departments:
            continue
        for department in role_departments.get(row.role, []):
            inferred.setdefault(row.parent, department)
            break

    return inferred


def get_user_summary(user, department=None, scopes=None):
    scopes = scopes or get_scopes_for_user()
    department = department or get_user_department(user, scopes=scopes)
    doc = frappe.get_doc("User", user)
    employee = get_employee_for_user(user)
    allowed_roles = set(get_allowed_roles_for_department(department, scopes))
    explicit_roles = sorted({row.role for row in doc.get("roles", []) if row.role})
    personal_role = get_existing_user_permission_role(user)
    has_personal_permissions = bool(personal_role and personal_role in explicit_roles)
    visible_roles = [role for role in explicit_roles if role in allowed_roles]

    return {
        "name": doc.name,
        "email": doc.email,
        "first_name": doc.first_name,
        "last_name": doc.last_name,
        "full_name": doc.full_name,
        "enabled": cint(doc.enabled),
        "user_type": doc.user_type,
        "department": department,
        "employee": employee.get("name"),
        "employee_name": employee.get("employee_name"),
        "employee_status": employee.get("status"),
        "employee_company": employee.get("company"),
        "roles": visible_roles,
        "permission_mode": "user" if has_personal_permissions else "role",
        "personal_permission_role": personal_role if has_personal_permissions else None,
        "all_role_count": len(explicit_roles),
        "must_change_password": is_password_change_pending(doc.last_password_reset_date),
        "last_active": doc.last_active,
        "modified": doc.modified,
    }


def get_employee_for_user(user):
    if not frappe.db.exists("DocType", "Employee"):
        return frappe._dict()

    fields = ["name", "employee_name", "department", "company", "status", "user_id"]
    employee = frappe.get_all(
        "Employee",
        filters={"user_id": user},
        fields=fields,
        order_by="modified desc",
        limit=1,
    )
    return employee[0] if employee else frappe._dict()


def get_first_login_password_reset_date():
    reset_after_days = ensure_first_login_password_reset_policy()
    return add_days(today(), -(reset_after_days + 1))


def ensure_first_login_password_reset_policy():
    reset_after_days = cint(
        frappe.db.get_single_value("System Settings", "force_user_to_reset_password") or 0
    )
    if reset_after_days > 0:
        return reset_after_days

    frappe.db.set_single_value(
        "System Settings",
        "force_user_to_reset_password",
        DEFAULT_FORCE_PASSWORD_RESET_DAYS,
    )
    frappe.clear_cache(doctype="System Settings")
    return DEFAULT_FORCE_PASSWORD_RESET_DAYS


def is_password_change_pending(last_password_reset_date):
    reset_after_days = cint(
        frappe.db.get_single_value("System Settings", "force_user_to_reset_password") or 0
    )
    if not reset_after_days or not last_password_reset_date:
        return 0

    return 1 if date_diff(today(), last_password_reset_date) > reset_after_days else 0


def assert_department_access(department, requested_roles):
    scopes = get_scopes_for_user()
    matching_scopes = [scope for scope in scopes if scope.get("department") == department]
    if not matching_scopes:
        frappe.throw(
            _("You do not have permission to manage users in department {0}.").format(frappe.bold(department)),
            frappe.PermissionError,
        )

    allowed_roles = set()
    user_type = None
    for scope in matching_scopes:
        user_type = user_type or scope.get("user_type")
        allowed_roles.update(role["role"] for role in scope.get("allowed_roles", []) if role.get("role"))

    blocked_roles = set(requested_roles) - allowed_roles
    if blocked_roles:
        frappe.throw(
            _("These roles are outside your permission scope: {0}").format(", ".join(sorted(blocked_roles))),
            frappe.PermissionError,
        )

    protected = set(requested_roles) & PROTECTED_ROLES
    if protected:
        frappe.throw(
            _("These roles cannot be delegated from this tool: {0}").format(", ".join(sorted(protected))),
            frappe.PermissionError,
        )

    return {
        "allowed_roles": sorted(allowed_roles),
        "manager_roles": sorted(
            {
                scope.get("manager_role")
                for scope in matching_scopes
                if scope.get("manager_role")
            }
        ),
        "manageable_departments": sorted({scope["department"] for scope in scopes if scope.get("department")}),
        "user_type": user_type or "System User",
    }


def apply_permission_manager_access_role(user, roles, manager_roles=None):
    """Give the navigation role to users who are managers for a configured scope."""
    role_names = set(roles or [])
    if not frappe.db.exists("Role", PERMISSION_MANAGER_ACCESS_ROLE):
        return sorted(role_names)

    manager_roles = set(manager_roles or get_enabled_scope_manager_roles())
    is_explicit_manager_user = frappe.db.exists(
        "DCNET Permission Scope",
        {
            "enabled": 1,
            "manager_user": user,
        },
    )
    if is_explicit_manager_user or role_names & manager_roles:
        role_names.add(PERMISSION_MANAGER_ACCESS_ROLE)
    else:
        role_names.discard(PERMISSION_MANAGER_ACCESS_ROLE)

    return sorted(role_names)


def get_enabled_scope_manager_roles():
    if not frappe.db.table_exists("DCNET Permission Scope"):
        return []

    return sorted(
        {
            role
            for role in frappe.get_all(
                "DCNET Permission Scope",
                filters={"enabled": 1, "manager_role": ["is", "set"]},
                pluck="manager_role",
            )
            if role and frappe.db.exists("Role", role)
        }
    )


def assert_user_is_manageable(user):
    scopes = get_scopes_for_user()
    departments = {scope["department"] for scope in scopes if scope.get("department")}
    department = get_user_department(user, scopes=scopes)

    if not department or department not in departments:
        frappe.throw(
            _("You do not have permission to manage user {0}.").format(frappe.bold(user)),
            frappe.PermissionError,
        )

    if not is_permission_admin():
        protected_roles = {
            row.role for row in frappe.get_doc("User", user).get("roles", []) if row.role in PROTECTED_ROLES
        }
        if protected_roles:
            frappe.throw(
                _("User {0} has protected roles and cannot be managed from a delegated scope.").format(
                    frappe.bold(user)
                ),
                frappe.PermissionError,
            )


def assert_existing_user_can_be_managed(user, manageable_departments):
    current_department = get_user_department(user)
    if current_department and current_department not in manageable_departments and not is_permission_admin():
        frappe.throw(
            _("User {0} belongs to department {1}, outside your managed scope.").format(
                frappe.bold(user), frappe.bold(current_department)
            ),
            frappe.PermissionError,
        )

    if not is_permission_admin():
        protected_roles = {
            row.role for row in frappe.get_doc("User", user).get("roles", []) if row.role in PROTECTED_ROLES
        }
        if protected_roles:
            frappe.throw(
                _("User {0} has protected roles and cannot be managed from a delegated scope.").format(
                    frappe.bold(user)
                ),
                frappe.PermissionError,
            )


def get_allowed_roles_for_department(department, scopes):
    roles = []
    for scope in scopes:
        if scope.get("department") == department:
            roles.extend(role["role"] for role in scope.get("allowed_roles", []) if role.get("role"))
    return sorted(set(roles))


def get_user_department(user, scopes=None):
    permission = frappe.get_all(
        "User Permission",
        filters={"user": user, "allow": "Department"},
        fields=["for_value", "is_default", "modified"],
        order_by="is_default desc, modified desc",
        limit=1,
    )
    if permission:
        return permission[0].for_value

    if frappe.db.exists("DocType", "Employee"):
        employee = frappe.get_all(
            "Employee",
            filters={"user_id": user},
            fields=["department"],
            order_by="modified desc",
            limit=1,
        )
        if employee:
            return employee[0].department

    if scopes and is_permission_admin():
        return infer_user_department_from_roles(user, scopes)

    return None


def infer_user_department_from_roles(user, scopes):
    user_roles = set(get_user_role_names(user))
    if not user_roles:
        return None

    for scope in sorted(scopes or [], key=lambda item: (item.get("department") or "", item.get("scope_name") or "")):
        department = scope.get("department")
        allowed_roles = {row.get("role") for row in scope.get("allowed_roles", []) if row.get("role")}
        if department and user_roles & allowed_roles:
            return department

    return None


def sync_department_permission(user, department, manageable_departments):
    if manageable_departments:
        existing = frappe.get_all(
            "User Permission",
            filters={
                "user": user,
                "allow": "Department",
                "for_value": ["in", manageable_departments],
            },
            pluck="name",
        )
        for name in existing:
            frappe.delete_doc("User Permission", name, force=True, ignore_permissions=True)

    permission = frappe.new_doc("User Permission")
    permission.user = user
    permission.allow = "Department"
    permission.for_value = department
    permission.is_default = 1
    permission.apply_to_all_doctypes = 1
    permission.insert(ignore_permissions=True)


def sync_employee_link(user, employee, department, manageable_departments):
    if not frappe.db.exists("DocType", "Employee"):
        if employee:
            frappe.throw(_("Employee module is not installed."))
        return

    linked_employees = frappe.get_all(
        "Employee",
        filters={"user_id": user},
        fields=["name", "employee_name", "department", "user_id"],
    )

    if not employee:
        for linked_employee in linked_employees:
            if linked_employee.department in manageable_departments or is_permission_admin():
                clear_employee_user(linked_employee.name)
        return

    employee_row = frappe.db.get_value(
        "Employee",
        employee,
        ["name", "employee_name", "department", "user_id"],
        as_dict=True,
    )
    if not employee_row:
        frappe.throw(_("Employee {0} does not exist.").format(frappe.bold(employee)))
    if employee_row.department != department:
        frappe.throw(
            _("Employee {0} belongs to department {1}, not {2}.").format(
                frappe.bold(employee),
                frappe.bold(employee_row.department or ""),
                frappe.bold(department),
            )
        )
    if employee_row.department not in manageable_departments and not is_permission_admin():
        frappe.throw(
            _("You do not have permission to link employees in department {0}.").format(
                frappe.bold(employee_row.department)
            ),
            frappe.PermissionError,
        )
    if employee_row.user_id and normalize_email(employee_row.user_id) != user:
        frappe.throw(
            _("Employee {0} is already linked to user {1}.").format(
                frappe.bold(employee),
                frappe.bold(employee_row.user_id),
            )
        )

    for linked_employee in linked_employees:
        if linked_employee.name == employee:
            continue
        if linked_employee.department not in manageable_departments and not is_permission_admin():
            frappe.throw(
                _("User {0} is already linked to Employee {1} outside your managed scope.").format(
                    frappe.bold(user),
                    frappe.bold(linked_employee.name),
                ),
                frappe.PermissionError,
            )
        clear_employee_user(linked_employee.name)

    employee_doc = frappe.get_doc("Employee", employee)
    if employee_doc.user_id != user:
        employee_doc.user_id = user
        employee_doc.save(ignore_permissions=True)


def clear_employee_user(employee):
    employee_doc = frappe.get_doc("Employee", employee)
    if employee_doc.user_id:
        employee_doc.user_id = None
        employee_doc.save(ignore_permissions=True)


def add_audit_comment(user, department, roles, action, employee=None):
    content = "DCNET Permission {0}: department={1}, employee={2}, roles={3}".format(
        action,
        department or "",
        employee or "",
        ", ".join(sorted(roles)) if roles else "",
    )
    frappe.get_doc(
        {
            "doctype": "Comment",
            "comment_type": "Info",
            "reference_doctype": "User",
            "reference_name": user,
            "content": content,
        }
    ).insert(ignore_permissions=True)


def is_permission_admin(user: str | None = None):
    user = user or frappe.session.user
    return user == "Administrator" or bool(set(frappe.get_roles(user)) & ADMIN_ROLES)


def can_access_permission_manager(user: str | None = None):
    user = user or frappe.session.user
    if is_permission_admin(user):
        return True

    return bool(get_scopes_for_user(user))


def assert_permission_manager_access(user: str | None = None):
    if not can_access_permission_manager(user):
        frappe.throw(
            _("You do not have permission to access DCNET Permission Manager."),
            frappe.PermissionError,
        )


MODULE_LABELS_VI = {
    "Accounts": "Kế toán",
    "Assets": "Tài sản",
    "Buying": "Mua hàng",
    "CRM": "CRM",
    "HR": "Nhân sự",
    "HR Analytics": "Phân tích nhân sự",
    "Leave Management": "Nghỉ phép",
    "Attendance": "Chấm công",
    "Payroll": "Lương",
    "Manufacturing": "Sản xuất",
    "Projects": "Dự án",
    "Quality Management": "Quản lý chất lượng",
    "Selling": "Bán hàng",
    "Stock": "Kho hàng",
    "Support": "CSKH",
    "Non Profit": "Phi lợi nhuận",
    "Education": "Giáo dục",
    "Healthcare": "Y tế",
    "Hospitality": "Nhà hàng",
    "Loan Management": "Quản lý vay",
    "E-commerce": "Thương mại điện tử",
    "Retail": "Bán lẻ",
    "Website": "Website",
    "Integrations": "Tích hợp",
    "Printing": "In ấn",
    "Workflow": "Quy trình",
    "Setup": "Cài đặt",
    "Regional": "Địa phương hóa",
    "Utilities": "Tiện ích",
}

MODULE_APP_LABELS = {
    "frappe": "Frappe",
    "erpnext": "ERPNext",
    "hrms": "HR & Nhân sự",
    "dcnet_apps": "DCNET",
    "payments": "Thanh toán",
}

EXCLUDED_MODULES = {
    "Core",
    "Custom",
    "Desk",
    "Email",
    "Geo",
    "Printing",
    "Workflow",
    "Print Designer",
    "Performance Analytics",
}


def get_all_modules():
    rows = frappe.get_all(
        "Module Def",
        fields=["name", "app_name"],
        order_by="app_name asc, name asc",
    )
    result = []
    for row in rows:
        if row.name in EXCLUDED_MODULES:
            continue
        result.append(
            {
                "name": row.name,
                "app": row.app_name or "",
                "app_label": MODULE_APP_LABELS.get(row.app_name or "", row.app_name or ""),
                "label": MODULE_LABELS_VI.get(row.name, row.name),
            }
        )
    return result


def get_blocked_modules_for_users(user_names):
    if not user_names:
        return {}
    rows = frappe.get_all(
        "Block Module",
        filters={"parent": ["in", list(user_names)], "parenttype": "User"},
        fields=["parent", "module"],
    )
    result = {name: set() for name in user_names}
    for row in rows:
        if row.parent in result:
            result[row.parent].add(row.module)
    return result


def get_dept_user_names(department, scopes):
    all_users = get_managed_users(scopes)
    result = []
    for user in all_users:
        depts = user.get("departments") or ([user.get("department")] if user.get("department") else [])
        if department in depts and user.get("name") not in STANDARD_USERS:
            result.append(user["name"])
    return result


def get_dept_module_permissions(department):
    scopes = get_scopes_for_user()
    assert_department_access(department, [])

    user_names = get_dept_user_names(department, scopes)
    all_modules = get_all_modules()
    blocked_for_users = get_blocked_modules_for_users(user_names)
    total = len(user_names)

    result_modules = []
    for module in all_modules:
        mname = module["name"]
        blocked_count = sum(1 for u in user_names if mname in blocked_for_users.get(u, set()))
        result_modules.append(
            {
                **module,
                "blocked": blocked_count == total and total > 0,
                "partial": 0 < blocked_count < total,
            }
        )

    return {
        "department": department,
        "user_count": total,
        "modules": result_modules,
    }


def save_dept_module_permissions(data):
    data = parse_payload(data)
    department = (data.get("department") or "").strip()
    blocked_modules = data.get("blocked_modules") or []

    if not department:
        frappe.throw(_("Department is required."))

    scopes = get_scopes_for_user()
    assert_department_access(department, [])

    user_names = get_dept_user_names(department, scopes)
    blocked_set = set(blocked_modules)

    reloaded_users = []
    for user_name in user_names:
        if user_name in STANDARD_USERS:
            continue
        doc = frappe.get_doc("User", user_name)
        doc.set("block_modules", [])
        for mname in sorted(blocked_set):
            doc.append("block_modules", {"module": mname})
        doc.flags.ignore_permlevel_for_fields = ["block_modules"]
        doc.save(ignore_permissions=True)
        frappe.clear_cache(user=user_name)
        frappe.publish_realtime("reload", user=user_name)
        reloaded_users.append(user_name)

    result = get_dept_module_permissions(department)
    result["reloaded_users"] = reloaded_users
    return result


def normalize_email(value):
    return (value or "").strip().lower()


def normalize_roles(roles):
    if isinstance(roles, str):
        roles = json.loads(roles)
    return sorted({str(role).strip() for role in roles or [] if str(role).strip()})


def parse_payload(data):
    if isinstance(data, str):
        return frappe._dict(json.loads(data))
    return frappe._dict(data or {})
