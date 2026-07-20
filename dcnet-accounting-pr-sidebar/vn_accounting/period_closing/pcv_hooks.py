import frappe
from frappe import _


def pcv_validate_vn_requirements(doc, method):
    """Validate VN-specific requirements before Period Closing Voucher submit."""
    # Mandatory lý do (reason)
    if not doc.get("vn_lock_unlock_reason"):
        frappe.throw(_("Vui lòng nhập Lý do khóa sổ trước khi ghi sổ Khóa kỳ kế toán."))

    # Check that user has Accounts Manager role
    if not frappe.has_role("Accounts Manager") and not frappe.has_role("System Manager"):
        frappe.throw(_("Chỉ Kế toán trưởng (Accounts Manager) mới được phép khóa/mở kỳ kế toán."))


def pcv_on_submit(doc, method):
    """Write audit log comment when Period Closing Voucher is submitted."""
    reason = doc.get("vn_lock_unlock_reason") or "—"
    frappe.get_doc({
        "doctype": "Comment",
        "comment_type": "Info",
        "reference_doctype": doc.doctype,
        "reference_name": doc.name,
        "content": f"<b>Khóa sổ kỳ kế toán</b> bởi {frappe.session.user}. "
                   f"Lý do: {reason}",
    }).insert(ignore_permissions=True)


def pcv_on_cancel(doc, method):
    """Write audit log when Period Closing Voucher is cancelled (unlocked)."""
    reason = doc.get("vn_lock_unlock_reason") or "—"
    frappe.get_doc({
        "doctype": "Comment",
        "comment_type": "Info",
        "reference_doctype": doc.doctype,
        "reference_name": doc.name,
        "content": f"<b>Mở khóa kỳ kế toán</b> bởi {frappe.session.user}. "
                   f"Lý do mở khóa: {reason}",
    }).insert(ignore_permissions=True)
