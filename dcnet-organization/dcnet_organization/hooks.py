from . import __version__ as app_version

app_name = "dcnet_organization"
app_title = "DCNET Organization"
app_publisher = "DCNet"
app_description = "Company / Branch / Department / Designation linkage for Frappe/ERPNext"
app_email = "admin@dcnet.vn"
app_license = "MIT"

# ── Install / Migrate ────────────────────────────────────────────────────────
# Tạo/cập nhật Custom Field cơ cấu tổ chức trên mỗi lần cài & migrate.
after_install = "dcnet_organization.install.after_install"
after_migrate = "dcnet_organization.install.after_migrate"

# ── Client scripts (link filtering / UX khi save) ────────────────────────────
doctype_js = {
    "Department": "public/js/department.js",
    "Designation": "public/js/designation.js",
    "Branch": "public/js/branch.js",
}

# ── List view scripts (refresh list ngay sau khi thêm mới) ───────────────────
doctype_list_js = {
    "Department": "public/js/department_list.js",
    "Designation": "public/js/designation_list.js",
    "Branch": "public/js/branch_list.js",
}

# ── Server-side validation khi save ──────────────────────────────────────────
doc_events = {
    "Department": {
        "validate": "dcnet_organization.overrides.validate_department",
    },
    "Designation": {
        "validate": "dcnet_organization.overrides.validate_designation",
    },
}
