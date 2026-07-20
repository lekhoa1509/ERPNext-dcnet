# Copyright (c) 2026, DCNet and Contributors
# License: MIT

import frappe
from frappe import _
from frappe.model.document import Document


VN_WORKSPACE_NAME = "VN Accounting"


class VNAccountingSettings(Document):
    def on_update(self):
        _sync_permissions_to_docperm(self)
        _sync_workspace_role_gate(self)

    @frappe.whitelist()
    def reset_permission_matrix(self):
        """Load default permission rules from fixture JSON and overwrite permission_matrix table."""
        defaults = frappe.get_file_json(
            frappe.get_app_path("vn_accounting", "config", "asset_permission_defaults.json")
        )
        self.set("permission_matrix", [])
        for row in defaults:
            self.append("permission_matrix", {
                "enabled": 1,
                "doctype_name": row["doctype_name"],
                "role": row["role"],
                "read": row.get("read", 0),
                "write": row.get("write", 0),
                "create": row.get("create", 0),
                "submit": row.get("submit", 0),
                "cancel": row.get("cancel", 0),
                "report": row.get("report", 0),
                "if_owner": row.get("if_owner", 0),
            })
        self.save(ignore_permissions=True)
        return _("Permission matrix reset to defaults ({0} rules).").format(len(defaults))


def _sync_permissions_to_docperm(doc):
    """Sync permission_matrix rows → tabCustom DocPerm for affected DocTypes."""
    if not doc.permission_matrix:
        return

    affected_doctypes = list({row.doctype_name for row in doc.permission_matrix if row.doctype_name})
    if not affected_doctypes:
        return

    roles_in_matrix = list({row.role for row in doc.permission_matrix if row.role})

    for doctype_name in affected_doctypes:
        frappe.db.delete(
            "Custom DocPerm",
            {"parent": doctype_name, "role": ["in", roles_in_matrix]},
        )

    for row in doc.permission_matrix:
        if not row.enabled or not row.doctype_name or not row.role:
            continue
        frappe.get_doc({
            "doctype": "Custom DocPerm",
            "parent": row.doctype_name,
            "parentfield": "permissions",
            "parenttype": "DocType",
            "role": row.role,
            "permlevel": 0,
            "read": row.read or 0,
            "write": row.write or 0,
            "create": row.create or 0,
            "submit": row.submit or 0,
            "cancel": row.cancel or 0,
            "report": getattr(row, "report", 0) or 0,
            "if_owner": row.if_owner or 0,
        }).insert(ignore_permissions=True)

    for doctype_name in affected_doctypes:
        frappe.clear_cache(doctype=doctype_name)


def _sync_workspace_role_gate(doc):
    """Sync allowed_workspace_roles → tabHas Role rows for Workspace VN Accounting.

    Source of truth: VN Accounting Settings.allowed_workspace_roles + enforce_workspace_role_gate.
    Target: child rows of Workspace "VN Accounting" via tabHas Role (parenttype=Workspace).

    When enforce_workspace_role_gate=0 → wipe all roles (workspace open to all).
    When enforce_workspace_role_gate=1 → replace workspace roles with the configured list.

    Idempotent: safe to call repeatedly. Frappe core respects workspace.roles natively
    (filter in workspace switcher + 403 on direct URL access).
    """
    if not frappe.db.exists("Workspace", VN_WORKSPACE_NAME):
        return

    # Wipe existing role rows for the workspace
    frappe.db.delete(
        "Has Role",
        {"parent": VN_WORKSPACE_NAME, "parenttype": "Workspace"},
    )

    if not getattr(doc, "enforce_workspace_role_gate", 0):
        # Gate disabled — leave roles empty (open to all)
        frappe.db.set_value(
            "Workspace", VN_WORKSPACE_NAME, "modified", frappe.utils.now(),
            update_modified=False,
        )
        frappe.cache.delete_key("bootinfo")
        return

    # Insert new rows from settings
    seen = set()
    for row in doc.allowed_workspace_roles or []:
        role = row.role
        if not role or role in seen:
            continue
        seen.add(role)
        frappe.get_doc({
            "doctype": "Has Role",
            "parent": VN_WORKSPACE_NAME,
            "parenttype": "Workspace",
            "parentfield": "roles",
            "role": role,
        }).insert(ignore_permissions=True)

    # Touch workspace modified so Frappe re-imports cleanly + bust boot cache
    frappe.db.set_value(
        "Workspace", VN_WORKSPACE_NAME, "modified", frappe.utils.now(),
        update_modified=False,
    )
    frappe.cache.delete_key("bootinfo")
