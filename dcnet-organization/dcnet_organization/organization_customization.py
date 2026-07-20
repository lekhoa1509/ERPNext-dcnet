"""Custom Field definitions cho cơ cấu tổ chức DCNET.

App này override cách Frappe/ERPNext lưu liên kết:

    Company ── Branch ── Department ── Designation

Frappe gốc chỉ có: Department -> Company. Không có liên kết Branch/Designation.
App bổ sung 3 Custom Field (nguồn sự thật duy nhất, tạo bằng code trong install.py):

    1. Branch.company       (Link -> Company)    — tuỳ chọn: chi nhánh có thể thuộc công ty
    2. Department.branch     (Link -> Branch)     — tuỳ chọn (không bắt buộc)
    3. Designation.department(Link -> Department) — tuỳ chọn (không bắt buộc)
"""

# Định dạng dict theo chuẩn của frappe...create_custom_fields()
CUSTOM_FIELDS = {
    # 1 — Chi nhánh thuộc công ty nào (tuỳ chọn)
    "Branch": [
        {
            "fieldname": "company",
            "label": "Company",
            "fieldtype": "Link",
            "options": "Company",
            "insert_after": "branch",
            "reqd": 0,
            "in_list_view": 1,
            "in_standard_filter": 1,
            "allow_in_quick_entry": 1,
            "translatable": 0,
            "description": "Tuỳ chọn — công ty mà chi nhánh này trực thuộc.",
        }
    ],
    # 2 — Phòng ban có thể gắn vào một chi nhánh (tuỳ chọn)
    "Department": [
        {
            "fieldname": "branch",
            "label": "Branch",
            "fieldtype": "Link",
            "options": "Branch",
            "insert_after": "company",
            "reqd": 0,
            "in_list_view": 1,
            "in_standard_filter": 1,
            "translatable": 0,
            "description": "Tuỳ chọn — chi nhánh mà phòng ban này trực thuộc.",
        }
    ],
    # 3 — Chức vụ có thể gắn vào một phòng ban (tuỳ chọn)
    "Designation": [
        {
            "fieldname": "department",
            "label": "Department",
            "fieldtype": "Link",
            "options": "Department",
            "insert_after": "designation_name",
            "reqd": 0,
            "in_list_view": 1,
            "in_standard_filter": 1,
            "allow_in_quick_entry": 1,
            "translatable": 0,
            "description": "Tuỳ chọn — phòng ban mà chức vụ này thuộc về.",
        }
    ],
}
