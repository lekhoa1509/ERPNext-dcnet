import frappe
from frappe.desk.desktop import get_workspace_sidebar_items as _original_fn


@frappe.whitelist()
def get_workspace_sidebar_items():
    # Native get_workspace_sidebar_items skips module filtering for Workspace Manager
    # (has_access → filters=[]) so blocked pages still appear in their sidebar.
    # We intentionally strip them here so Workspace Manager cannot see or navigate
    # to modules the user is blocked from — consistent with the rest of the desk.
    result = _original_fn()
    if not result:
        return result

    user_doc = frappe.get_cached_doc("User", frappe.session.user)
    blocked = user_doc.get_blocked_modules()
    if not blocked:
        return result

    blocked_set = set(blocked)
    result["pages"] = [
        p for p in (result.get("pages") or [])
        if not (p.get("module") and p["module"] in blocked_set)
    ]
    return result
