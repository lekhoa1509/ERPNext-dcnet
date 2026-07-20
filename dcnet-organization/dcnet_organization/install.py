"""Install / migrate hooks cho dcnet_organization.

Custom Field được tạo bằng code (không dùng fixtures) để:
  - Là nguồn sự thật duy nhất, dễ review qua git.
  - Tự sửa/upsert trên mọi `bench migrate` (update=True).
  - Không crash nếu site chưa cài ERPNext/HRMS (guard theo DocType tồn tại).
"""

import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

from dcnet_organization.organization_customization import CUSTOM_FIELDS


def after_install():
    """Chạy 1 lần khi cài app lần đầu."""
    ensure_organization_custom_fields()


def after_migrate():
    """Chạy trên mỗi `bench migrate` — đảm bảo field luôn tồn tại/đúng cấu hình."""
    ensure_organization_custom_fields()


def ensure_organization_custom_fields():
    """Tạo/cập nhật các Custom Field cơ cấu tổ chức.

    Chỉ áp dụng cho những DocType thực sự tồn tại trên site (Branch/Department/
    Designation có thể nằm trong erpnext hoặc hrms tuỳ phiên bản). Nếu chưa cài
    thì bỏ qua, không raise — giúp app cài được độc lập.
    """
    fields = {
        doctype: definitions
        for doctype, definitions in CUSTOM_FIELDS.items()
        if frappe.db.exists("DocType", doctype)
    }

    missing = [dt for dt in CUSTOM_FIELDS if dt not in fields]
    if missing:
        frappe.msgprint(
            "dcnet_organization: bỏ qua các DocType chưa cài đặt: "
            + ", ".join(missing),
            alert=True,
        )

    if fields:
        create_custom_fields(fields, update=True)
        frappe.db.commit()
