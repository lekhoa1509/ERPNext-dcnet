import frappe
from frappe import _


ORDER_KEYWORDS = ("sales order", "đơn hàng", "đơn bán hàng", "don hang", "don ban hang")


def _is_order_notification(notification):
    haystack = " ".join(
        [
            notification.get("subject") or "",
            notification.get("document_type") or "",
            notification.get("document_name") or "",
        ]
    ).lower()
    return any(keyword in haystack for keyword in ORDER_KEYWORDS)


@frappe.whitelist(methods=["GET"])
def get_unread_summary(limit: int = 1):
    """Return unread bell count and latest unread notification for current Desk user."""
    if frappe.session.user == "Guest":
        frappe.throw(_("Not permitted"), frappe.PermissionError)

    limit = max(1, min(frappe.utils.cint(limit), 5))
    filters = {"for_user": frappe.session.user, "read": 0}

    unread_count = frappe.db.count("Notification Log", filters)
    latest = frappe.get_all(
        "Notification Log",
        filters=filters,
        fields=[
            "name",
            "subject",
            "type",
            "document_type",
            "document_name",
            "link",
            "creation",
            "from_user",
        ],
        order_by="creation desc",
        limit=limit,
    )

    for item in latest:
        item["is_order_notification"] = _is_order_notification(item)

    return {
        "unread_count": unread_count,
        "latest": latest[0] if latest else None,
    }
