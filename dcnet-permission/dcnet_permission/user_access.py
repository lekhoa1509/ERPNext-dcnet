import frappe


ACCESS_CHANGED_EVENT = "dcnet_permission_user_access_changed"


def on_user_update(doc, method=None):
    """Notify a user session when roles or blocked modules change."""
    if not _access_rows_changed(doc):
        return

    user = doc.name
    frappe.clear_cache(user=user)
    frappe.publish_realtime(
        ACCESS_CHANGED_EVENT,
        {"user": user},
        user=user,
        after_commit=True,
    )


def _access_rows_changed(doc):
    previous = doc.get_doc_before_save()
    if not previous:
        return bool(_role_set(doc) or _blocked_module_set(doc))

    return (
        _role_set(doc) != _role_set(previous)
        or _blocked_module_set(doc) != _blocked_module_set(previous)
    )


def _role_set(doc):
    return {
        row.role
        for row in (doc.roles or [])
        if getattr(row, "role", None)
    }


def _blocked_module_set(doc):
    return {
        row.module
        for row in (doc.block_modules or [])
        if getattr(row, "module", None)
    }
