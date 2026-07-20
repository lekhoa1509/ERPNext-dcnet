"""Server-side validation cho liên kết cơ cấu tổ chức.

Đảm bảo dữ liệu nhất quán khi lưu (override tính năng save của Frappe/ERP):
  - Department.branch (nếu có chọn) phải thuộc đúng Department.company.
  - Designation.department (nếu có chọn) phải là phòng ban còn hoạt động.
"""

import frappe
from frappe import _


def validate_department(doc, method=None):
    """Chi nhánh của phòng ban phải cùng công ty với phòng ban."""
    branch = doc.get("branch")
    company = doc.get("company")
    if not branch or not company:
        return

    branch_company = frappe.db.get_value("Branch", branch, "company")
    if branch_company and branch_company != company:
        frappe.throw(
            _("Chi nhánh {0} thuộc công ty {1}, không khớp với công ty {2} của phòng ban.").format(
                frappe.bold(branch), frappe.bold(branch_company), frappe.bold(company)
            ),
            title=_("Liên kết chi nhánh không hợp lệ"),
        )


def validate_designation(doc, method=None):
    """Phòng ban gán cho chức vụ (nếu có) phải chưa bị vô hiệu hoá."""
    department = doc.get("department")
    if not department:
        return

    if frappe.db.get_value("Department", department, "disabled"):
        frappe.throw(
            _("Phòng ban {0} đã bị vô hiệu hoá, không thể gán cho chức vụ.").format(
                frappe.bold(department)
            ),
            title=_("Phòng ban không hợp lệ"),
        )
