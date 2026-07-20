import frappe

from dcnet_permission.permission_manager import (
    assert_permission_manager_access,
    disable_managed_user,
    get_dashboard,
    get_dept_module_permissions,
    get_user_permissions,
    revoke_managed_department_access,
    save_dept_module_permissions,
    save_managed_user,
    save_role_permissions,
    save_user_permissions,
)


@frappe.whitelist(methods=["GET", "POST"])
def dashboard():
    assert_permission_manager_access()
    return get_dashboard()


@frappe.whitelist(methods=["POST"])
def save_user(data):
    assert_permission_manager_access()
    return save_managed_user(data)


@frappe.whitelist(methods=["POST"])
def disable_user(user):
    assert_permission_manager_access()
    return disable_managed_user(user)


@frappe.whitelist(methods=["POST"])
def save_permissions(data):
    assert_permission_manager_access()
    return save_role_permissions(data)


@frappe.whitelist(methods=["POST"])
def revoke_dept_access(user, department):
    assert_permission_manager_access()
    return revoke_managed_department_access(user, department)


@frappe.whitelist(methods=["POST"])
def get_user_permission_matrix(user, department=None):
    assert_permission_manager_access()
    return get_user_permissions(user, department=department)


@frappe.whitelist(methods=["POST"])
def save_user_permission_matrix(data):
    assert_permission_manager_access()
    return save_user_permissions(data)


@frappe.whitelist(methods=["POST"])
def get_module_permissions(department):
    assert_permission_manager_access()
    return get_dept_module_permissions(department)


@frappe.whitelist(methods=["POST"])
def save_module_permissions(data):
    assert_permission_manager_access()
    return save_dept_module_permissions(data)
