"""
Whitelisted endpoints cho mobile app — bypass client-side permission issues.

URL pattern: /api/method/dcnet_apps.mobile_push.api.{function_name}
"""

from __future__ import annotations

import json
from typing import Any

import frappe


# Mapping doctype → roles có quyền duyệt.
APPROVER_ROLES = {
    "Sales Order": ["Accounts Manager", "Sales Manager", "System Manager"],
    "Purchase Order": ["Accounts Manager", "Purchase Manager", "System Manager"],
    "Stock Entry": ["Stock Manager", "Accounts Manager", "System Manager"],
}


def _assign_approval_todo_without_notification(
    doctype: str,
    name: str,
    assign_to: str,
    description: str,
) -> bool:
    """Create approval ToDo without Frappe's generic assignment notification."""
    existing_todo = frappe.db.exists(
        "ToDo",
        {
            "reference_type": doctype,
            "reference_name": name,
            "allocated_to": assign_to,
            "status": "Open",
        },
    )
    if existing_todo:
        return False

    todo = frappe.get_doc(
        {
            "doctype": "ToDo",
            "allocated_to": assign_to,
            "reference_type": doctype,
            "reference_name": name,
            "description": description,
            "priority": "Medium",
            "status": "Open",
            "date": frappe.utils.nowdate(),
            "assigned_by": frappe.session.user,
        }
    )
    todo.insert(ignore_permissions=True)

    if frappe.get_meta(doctype).get_field("assigned_to"):
        frappe.db.set_value(doctype, name, "assigned_to", assign_to)

    doc = frappe.get_doc(doctype, name)
    if not frappe.has_permission(doc=doc, user=assign_to):
        if frappe.get_system_settings("disable_document_sharing"):
            frappe.throw(
                "Người duyệt chưa có quyền xem chứng từ. "
                "Vui lòng gán quyền trước khi gửi duyệt."
            )
        frappe.share.add(doc.doctype, doc.name, assign_to)

    return True


def _approval_notification_exists(doctype: str, name: str, for_user: str) -> bool:
    return bool(
        frappe.db.exists(
            "Notification Log",
            {
                "for_user": for_user,
                "type": "Alert",
                "document_type": doctype,
                "document_name": name,
                "read": 0,
            },
        )
    )


def _get_approvers(doctype: str, exclude_user: str | None = None) -> list[dict[str, Any]]:
    roles = APPROVER_ROLES.get(doctype, [])
    if not roles:
        return []
    user_ids = frappe.get_all(
        "Has Role",
        filters={
            "parenttype": "User",
            "role": ("in", roles),
        },
        pluck="parent",
    )
    user_ids = list({u for u in user_ids if u and u != "Administrator"})
    if exclude_user:
        user_ids = [u for u in user_ids if u != exclude_user]
    if not user_ids:
        return []
    return frappe.get_all(
        "User",
        filters={"name": ("in", user_ids), "enabled": 1},
        fields=["name", "full_name"],
    )


@frappe.whitelist()
def list_approvers(doctype: str) -> list[dict[str, Any]]:
    """Trả về danh sách người duyệt cho 1 doctype — dùng để hiển thị trên app."""
    return _get_approvers(doctype, exclude_user=frappe.session.user)


@frappe.whitelist()
def request_approval(doctype: str, name: str, note: str | None = None) -> dict[str, Any]:
    """
    Sales/employee gửi yêu cầu duyệt 1 doc nháp.

    - Server tự fetch approvers theo role mapping.
    - Tạo ToDo để approver thấy việc cần xử lý.
    - Chỉ tạo 1 Notification Log tùy biến, tránh trùng thông báo assignment mặc định.
    - Trả về danh sách approvers đã được assign + total.

    Có thể mở rộng: theo giá trị đơn → assign cấp duyệt khác nhau.
    """
    if not frappe.db.exists(doctype, name):
        frappe.throw(f"Không tìm thấy {doctype} {name}")

    doc = frappe.get_doc(doctype, name)
    if doc.docstatus != 0:
        frappe.throw("Chỉ có thể gửi duyệt với chứng từ ở trạng thái nháp")

    approvers = _get_approvers(doctype, exclude_user=frappe.session.user)
    if not approvers:
        frappe.throw(
            "Hệ thống chưa có ai có vai trò duyệt cho loại chứng từ này. "
            "Liên hệ Quản trị viên để gán role."
        )

    description = note or f"Yêu cầu duyệt {doctype} {name}. Lập bởi {frappe.session.user}."
    created_todos = 0
    for emp in approvers:
        if _assign_approval_todo_without_notification(doctype, name, emp["name"], description):
            created_todos += 1

        if _approval_notification_exists(doctype, name, emp["name"]):
            continue

        try:
            log = frappe.new_doc("Notification Log")
            log.update(
                {
                    "subject": f"📋 Yêu cầu duyệt {doctype} {name}",
                    "for_user": emp["name"],
                    "type": "Alert",
                    "document_type": doctype,
                    "document_name": name,
                    "from_user": frappe.session.user,
                }
            )
            log.insert(ignore_permissions=True)
        except Exception:
            frappe.log_error(title="request_approval notification failed")

    return {
        "ok": True,
        "doctype": doctype,
        "name": name,
        "approvers": approvers,
        "total": len(approvers),
        "created_todos": created_todos,
    }


@frappe.whitelist()
def notify_owner_after_action(
    doctype: str,
    name: str,
    action: str,  # "approved" | "rejected" | "cancelled"
) -> dict[str, Any]:
    """Gọi sau khi approver duyệt/cancel → notify ngược lại owner."""
    if not frappe.db.exists(doctype, name):
        frappe.throw(f"Không tìm thấy {doctype} {name}")
    doc = frappe.get_doc(doctype, name)
    if not doc.owner or doc.owner == frappe.session.user:
        return {"ok": True, "skipped": "owner is current user"}

    icon = {"approved": "✅", "rejected": "❌", "cancelled": "⚠️"}.get(action, "ℹ️")
    label = {"approved": "đã được DUYỆT", "rejected": "bị TỪ CHỐI", "cancelled": "bị HỦY"}.get(
        action, "có cập nhật"
    )

    log = frappe.new_doc("Notification Log")
    log.update(
        {
            "subject": f"{icon} {doctype} {name} {label}",
            "for_user": doc.owner,
            "type": "Alert",
            "document_type": doctype,
            "document_name": name,
            "from_user": frappe.session.user,
        }
    )
    log.insert(ignore_permissions=True)

    # Đóng tất cả ToDo còn open của doc
    open_todos = frappe.get_all(
        "ToDo",
        filters={
            "reference_type": doctype,
            "reference_name": name,
            "status": "Open",
        },
        pluck="name",
    )
    for tname in open_todos:
        try:
            t = frappe.get_doc("ToDo", tname)
            t.status = "Closed"
            t.save(ignore_permissions=True)
        except Exception:
            pass

    return {"ok": True, "notified": doc.owner, "closed_todos": len(open_todos)}


@frappe.whitelist()
def my_inbox(limit: int = 30) -> dict[str, Any]:
    """Tổng hợp ToDo + Notification cho user hiện tại — 1 round trip."""
    user = frappe.session.user
    todos = frappe.get_all(
        "ToDo",
        filters={"allocated_to": user, "status": "Open"},
        fields=[
            "name",
            "reference_type",
            "reference_name",
            "description",
            "priority",
            "date",
            "modified",
        ],
        order_by="modified desc",
        limit=limit,
    )
    notifications = frappe.get_all(
        "Notification Log",
        filters={"for_user": user},
        fields=[
            "name",
            "subject",
            "type",
            "document_type",
            "document_name",
            "read",
            "creation",
            "from_user",
        ],
        order_by="creation desc",
        limit=limit,
    )
    unread = sum(1 for n in notifications if not n.get("read"))
    return {
        "todos": todos,
        "notifications": notifications,
        "unread_count": unread,
        "todo_count": len(todos),
        "total_badge": unread + len(todos),
    }
