from . import __version__ as app_version

app_name = "dcnet_permission"
app_title = "DCNET Permission"
app_publisher = "DCNET"
app_description = "Department-scoped user and role delegation for DCNET Flow"
app_email = "admin@dcnet.vn"
app_license = "MIT"

required_apps = ["frappe", "erpnext"]

add_to_apps_screen = [
    {
        "name": "dcnet_permission",
        "logo": "/assets/frappe/images/frappe-framework-logo.svg",
        "title": "Department Permissions",
        "route": "/desk/dcnet-permission-manager",
        "has_permission": "dcnet_permission.permission_manager.can_access_permission_manager",
    }
]

before_install = "dcnet_permission.install.before_install"
before_migrate = ["dcnet_permission.install.before_migrate"]
after_install = "dcnet_permission.install.after_install"
after_migrate = "dcnet_permission.install.after_migrate"

page_js = {
    "dcnet-permission-manager": "public/js/dcnet_permission_manager.js",
}

app_include_js = [
    "/assets/dcnet_permission/js/user_access_reload.js",
    "/assets/dcnet_permission/js/desktop_icon_filter.js",
]

boot_session = "dcnet_permission.boot.boot_session"

doc_events = {
    "User": {
        "on_update": "dcnet_permission.user_access.on_user_update",
    },
}

extend_doctype_class = {
    "User": ["dcnet_permission.user.DCNETPermissionUserMixin"],
}

has_permission = {
    "*": "dcnet_permission.permission_guard.has_permission",
}

# KHÔNG ship Page "dcnet-permission-manager" làm fixture.
# Fixture import đi qua data_import path (import_file_by_path data_import=True) → KHÔNG set
# ignore_validate → Page.validate (frappe page.py:61 "is_new() and not developer_mode → throw")
# chạy → `bench migrate` / install-app CRASH "Not in Developer Mode" trên MỌI site non-dev
# (staging/prod). Đã gỡ ở PR#2, tái thêm ở PR#4 → gỡ lại đây.
# Page đã tự sync từ module folder page/dcnet_permission_manager/ (module sync dùng
# data_import=False → ignore_validate=True nên cài prod OK). Roles của page do
# install.setup() -> ensure_navigation_access -> set_document_roles gán, KHÔNG cần fixture.
# Nếu thật sự cần ship doc qua fixture: chỉ dùng cho doctype DATA thường (không phải
# code-managed như Page/DocType/Report/Workflow/Print Format).

override_whitelisted_methods = {
    "frappe.desk.desktop.get_workspace_sidebar_items": "dcnet_permission.desktop.get_workspace_sidebar_items",
}
