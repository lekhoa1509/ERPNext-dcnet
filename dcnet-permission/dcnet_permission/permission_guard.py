from __future__ import annotations

import frappe
from frappe.utils import cint

from dcnet_permission.permission_manager import (
    ACCOUNTING_USER_SETUP_BASELINES,
    ADMIN_ROLES,
    BUSINESS_DOCTYPE_SPECS,
    DOCTYPE_PERMISSION_FIELDS,
    get_effective_doctype_permissions,
    get_existing_user_permission_role,
    get_user_department,
    get_user_role_names,
)


WRITE_LIKE_PERMISSION_TYPES = {
    "write",
    "create",
    "delete",
    "submit",
    "cancel",
    "amend",
    "import",
}
ACCOUNTING_MANAGER_ROLES = {"Accounts Manager", "System Manager", "DCNET Permission Admin"}


def has_permission(doc, ptype=None, user=None, **kwargs):
    user = user or frappe.session.user
    doctype = getattr(doc, "doctype", None)

    if not doctype or not ptype or user == "Administrator":
        return True
    if doctype not in get_guarded_doctypes():
        return True

    roles = set(frappe.get_roles(user))
    if roles & ADMIN_ROLES:
        return True
    if not is_delegated_scope_user(user):
        return True

    personal_role = get_assigned_personal_role(user)
    if personal_role and not personal_role_allows(doctype, personal_role, ptype):
        return False

    if (
        not personal_role
        and doctype in ACCOUNTING_USER_SETUP_BASELINES
        and ptype in WRITE_LIKE_PERMISSION_TYPES
        and not roles & ACCOUNTING_MANAGER_ROLES
    ):
        return False

    return True


def get_guarded_doctypes():
    return {spec["name"] for spec in BUSINESS_DOCTYPE_SPECS} | set(ACCOUNTING_USER_SETUP_BASELINES)


def is_delegated_scope_user(user):
    if get_assigned_personal_role(user):
        return True

    department = get_user_department(user)
    if not department:
        return False

    return bool(
        frappe.db.exists(
            "DCNET Permission Scope",
            {
                "department": department,
                "enabled": 1,
            },
        )
    )


def get_assigned_personal_role(user):
    personal_role = get_existing_user_permission_role(user)
    if not personal_role:
        return None

    return personal_role if personal_role in get_user_role_names(user) else None


def personal_role_allows(doctype, role, ptype):
    permissions = get_effective_doctype_permissions(doctype, role)
    if ptype == "select" and cint(permissions.get("read")):
        return True
    if ptype not in DOCTYPE_PERMISSION_FIELDS:
        return True

    return bool(cint(permissions.get(ptype)))
