"""
Server hook: gửi Expo Push khi có Notification Log mới hoặc ToDo gán cho user.

Cách activate:
1. Thêm vào dcnet_apps/hooks.py (section DOC EVENTS):

    doc_events = {
        "Notification Log": {
            "after_insert": "dcnet_apps.mobile_push.events.notification_log.send_push_for_notification",
        },
        "ToDo": {
            "after_insert": "dcnet_apps.mobile_push.events.notification_log.send_push_for_todo",
        },
    }

2. bench --site flow.local migrate

Expo Push API: https://docs.expo.dev/push-notifications/sending-notifications
"""

import json

import frappe
import requests

EXPO_PUSH_URL = "https://exp.host/--/api/v2/push/send"
EXPO_TIMEOUT = 8  # seconds
APPROVAL_DOCTYPES = {"Sales Order", "Purchase Order", "Stock Entry"}


def _tokens_for_user(user_id: str) -> list[str]:
    return frappe.get_all(
        "Mobile Push Token",
        filters={"user": user_id, "enabled": 1},
        pluck="token",
    )


def _send_to_expo(messages: list[dict]) -> None:
    if not messages:
        return
    try:
        resp = requests.post(
            EXPO_PUSH_URL,
            headers={
                "Accept": "application/json",
                "Accept-encoding": "gzip, deflate",
                "Content-Type": "application/json",
            },
            data=json.dumps(messages),
            timeout=EXPO_TIMEOUT,
        )
        if resp.status_code >= 400:
            frappe.log_error(
                title="Expo Push failed",
                message=f"Status {resp.status_code} — {resp.text[:500]}",
            )
    except Exception as e:
        frappe.log_error(title="Expo Push exception", message=str(e))


def send_push_for_notification(doc, method=None):
    if not doc.for_user:
        return
    tokens = _tokens_for_user(doc.for_user)
    if not tokens:
        return

    title = doc.subject or "DCNET Flow"
    body = ""
    if doc.document_type and doc.document_name:
        body = f"{doc.document_type} {doc.document_name}"

    messages = [
        {
            "to": token,
            "sound": "default",
            "title": title,
            "body": body,
            "data": {
                "docType": doc.document_type,
                "docName": doc.document_name,
                "notificationName": doc.name,
                "type": doc.type,
            },
            "priority": "high",
            "channelId": "default",
        }
        for token in tokens
    ]
    _send_to_expo(messages)


def send_push_for_todo(doc, method=None):
    """Gửi push khi có ToDo mới được gán cho user (qua assign_to)."""
    if not doc.allocated_to or doc.status != "Open":
        return
    if doc.reference_type in APPROVAL_DOCTYPES:
        return
    tokens = _tokens_for_user(doc.allocated_to)
    if not tokens:
        return

    ref = ""
    if doc.reference_type and doc.reference_name:
        ref = f"{doc.reference_type} {doc.reference_name}"

    title = "Việc cần duyệt"
    body = (doc.description or ref or "Bạn có việc mới").replace("<", " ").replace(">", " ")[:120]

    messages = [
        {
            "to": token,
            "sound": "default",
            "title": title,
            "body": body,
            "data": {
                "docType": doc.reference_type,
                "docName": doc.reference_name,
                "todoName": doc.name,
                "type": "Assignment",
            },
            "priority": "high",
            "channelId": "default",
        }
        for token in tokens
    ]
    _send_to_expo(messages)
