import frappe


def _finish_revenue_requests(doc, status):
    """Finish outstanding CRM revenue requests with the Sales Order."""
    from dcnet_crm import api

    requests = api._get_open_so_revenue_requests(doc.name)
    for request in requests:
        todo = frappe.get_doc("ToDo", request.name)
        related_users = api._parse_todo_related_users(todo)
        todo.status = status
        todo.save(ignore_permissions=True)
        api._retract_todo_notifications(todo, related_users)

        for user in related_users:
            try:
                frappe.share.remove("ToDo", todo.name, user=user)
            except Exception:
                frappe.log_error(
                    frappe.get_traceback(),
                    "CRM ToDo Share Retraction Error",
                )
            frappe.publish_realtime(
                "notification",
                user=user,
                after_commit=True,
            )


def on_submit(doc, method=None):
    """A submitted Sales Order is posted revenue in the CRM workflow."""
    if frappe.get_meta("Sales Order").has_field("custom_revenue_status"):
        frappe.db.set_value(
            "Sales Order",
            doc.name,
            "custom_revenue_status",
            "Đã ghi",
            update_modified=False,
        )
    _finish_revenue_requests(doc, "Closed")


def on_cancel(doc, method=None):
    """Keep the legacy custom status aligned when a posted order is cancelled."""
    if frappe.get_meta("Sales Order").has_field("custom_revenue_status"):
        frappe.db.set_value(
            "Sales Order",
            doc.name,
            "custom_revenue_status",
            "Hủy",
            update_modified=False,
        )
    _finish_revenue_requests(doc, "Cancelled")
