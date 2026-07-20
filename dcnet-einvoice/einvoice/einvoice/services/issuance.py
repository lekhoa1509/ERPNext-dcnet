"""
Invoice Issuance Service.

Handles single and bulk outward invoice issuance via providers.
Extracted from api.py for testability and separation of concerns.
"""

import json

import frappe
from frappe.utils import now_datetime, flt

from einvoice.einvoice.exceptions import (
    EInvoiceProviderError,
    EInvoiceProviderNotReady,
)


def log_einvoice_error(title, message, provider=None):
    """Log error with [EInvoice] prefix for easy filtering."""
    frappe.log_error(
        title=f"[EInvoice] {title}",
        message=message,
        reference_doctype="EInvoice Provider" if provider else None,
        reference_name=provider,
    )


class IssuanceService:
    """Service class for invoice issuance operations."""

    @staticmethod
    def issue_single(sales_invoice, provider=None, pattern=None, serial=None,
                     issue_mode=None, send_email=None):
        """
        Xuất hóa đơn điện tử cho 1 Sales Invoice. Dispatcher theo
        provider.OUTWARD_CAPABILITY:
          - "direct"     → tự ký (HSM/pre-signed) → issue_outward_invoice()
          - "push-draft" → ERP đẩy nháp, user ký USB ngoài → push_draft_invoice()

        Một entry point duy nhất, UI chỉ cần "Xuất hóa đơn điện tử" — không cần biết
        flow nào. Trả về dict: {success, message, invoice_number, lookup_code, pdf_url, ikey, status_text}.

        `send_email`: chỉ có hiệu lực ở chế độ "Publish" + capability "direct" (đã ký, có
        PDF). Khi truthy + phát hành thành công → gửi email PDF cho khách. Không áp dụng
        cho push-draft (chưa ký, chưa có PDF).
        """
        si_doc = frappe.get_doc("Sales Invoice", sales_invoice)

        # Validations
        if si_doc.docstatus != 1:
            return {"success": False, "message": "Chỉ có thể xuất hóa đơn điện tử cho Sales Invoice đã Submit."}
        if si_doc.einvoice_issued:
            return {"success": False, "message": "Sales Invoice này đã xuất hóa đơn điện tử rồi."}
        if si_doc.get("einvoice_pushed"):
            return {"success": False, "message": "Sales Invoice này đã đẩy lên provider, đang chờ ký."}

        settings = frappe.get_single("EInvoice Settings")
        provider_doc = _resolve_provider(si_doc, provider, settings)
        provider_name = provider_doc.name

        if pattern:
            provider_doc.default_invoice_pattern = pattern
        if serial:
            provider_doc.default_invoice_serial = serial
        if issue_mode:
            settings.default_issue_mode = issue_mode

        try:
            provider_instance = provider_doc.get_provider_instance()
            provider_instance.authenticate()
            capability = getattr(provider_instance, "OUTWARD_CAPABILITY", "direct")

            if capability == "push-draft":
                payload = provider_instance.map_sales_invoice_to_payload(si_doc, settings)
                result = provider_instance.push_draft_invoice(payload)
            else:  # "direct" — legacy path
                payload = provider_instance.map_sales_invoice_to_payload(si_doc, settings)
                result = provider_instance.issue_outward_invoice(payload)
        except EInvoiceProviderNotReady as e:
            return {"success": False, "message": e.message}
        except EInvoiceProviderError as e:
            log_einvoice_error(
                f"Issue failed - {sales_invoice}",
                f"{e.message}\n{e.detail or ''}",
                provider=provider_name,
            )
            _create_issuance_log(provider_name, sales_invoice, "Failed", error=str(e.message))
            return {"success": False, "message": f"Lỗi provider: {e.message}"}

        if not result.get("success"):
            error_msg = result.get("error", "Lỗi không xác định")
            _create_issuance_log(provider_name, sales_invoice, "Failed", error=error_msg)
            return {"success": False, "message": f"Xuất hóa đơn điện tử thất bại: {error_msg}"}

        # Branch theo capability để cập nhật fields đúng — push-draft chỉ set
        # einvoice_pushed (chờ ký), direct set einvoice_issued (đã ký xong).
        if capability == "push-draft":
            ikey = result.get("ikey", "")
            status_text = result.get("status_text", "Đã đẩy, chờ ký")
            frappe.db.set_value("Sales Invoice", sales_invoice, {
                "einvoice_pushed": 1,
                "einvoice_ikey": ikey,
                "einvoice_status_text": status_text,
                "einvoice_pushed_at": now_datetime(),
                "einvoice_provider": provider_name,
            }, update_modified=False)
            _create_issuance_log(
                provider_name, sales_invoice, "Pushed Pending Sign",
                invoice_number=ikey,
            )
            frappe.db.commit()
            return {
                "success": True,
                "message": f"Đã đẩy lên {provider_name}. Vào web admin của provider để ký USB.",
                "ikey": ikey,
                "status_text": status_text,
            }

        # capability == "direct"
        _create_issuance_log(
            provider_name, sales_invoice, "Success",
            invoice_number=result.get("invoice_number", ""),
            lookup_code=result.get("lookup_code", ""),
            pdf_url=result.get("pdf_url", ""),
        )
        frappe.db.set_value("Sales Invoice", sales_invoice, {
            "einvoice_issued": 1,
            "einvoice_provider": provider_name,
            "einvoice_number": result.get("invoice_number", ""),
            "einvoice_lookup_code": result.get("lookup_code", ""),
            "einvoice_pdf_url": result.get("pdf_url", ""),
            "einvoice_issued_at": now_datetime(),
        }, update_modified=False)
        frappe.db.commit()

        email_status = ""
        if send_email and (issue_mode or "").lower() in ("publish", "phát hành"):
            email_status = _email_einvoice_pdf_to_customer(si_doc, result, provider_name)

        return {
            "success": True,
            "message": "Xuất hóa đơn điện tử thành công!" + (f" {email_status}" if email_status else ""),
            "invoice_number": result.get("invoice_number"),
            "lookup_code": result.get("lookup_code"),
            "pdf_url": result.get("pdf_url"),
        }

    @staticmethod
    def push_draft(sales_invoice, provider=None):
        """Push a submitted Sales Invoice to EasyInvoice as an unsigned draft.

        Returns dict: {success, message, ikey, status_text}
        """
        si_doc = frappe.get_doc("Sales Invoice", sales_invoice)

        if si_doc.docstatus != 1:
            return {"success": False, "message": "Chỉ có thể đẩy Sales Invoice đã Submit."}
        if si_doc.get("einvoice_pushed"):
            return {"success": False, "message": "Sales Invoice này đã được đẩy lên EasyInvoice rồi."}

        settings = frappe.get_single("EInvoice Settings")
        provider_doc = _resolve_provider(si_doc, provider, settings)
        provider_name = provider_doc.name

        try:
            provider_instance = provider_doc.get_provider_instance()
            provider_instance.authenticate()
            payload = provider_instance.map_sales_invoice_to_payload(si_doc, settings)
            result = provider_instance.push_draft_invoice(payload)
        except EInvoiceProviderNotReady as e:
            return {"success": False, "message": e.message}
        except EInvoiceProviderError as e:
            log_einvoice_error(
                f"Push draft failed - {sales_invoice}",
                f"{e.message}\n{e.detail or ''}",
                provider=provider_name,
            )
            _create_issuance_log(provider_name, sales_invoice, "Failed", error=str(e.message))
            return {"success": False, "message": f"Lỗi: {e.message}"}

        if result.get("success"):
            ikey = result.get("ikey", "")
            status_text = result.get("status_text", "Đã đẩy, chờ ký")
            frappe.db.set_value("Sales Invoice", sales_invoice, {
                "einvoice_pushed": 1,
                "einvoice_ikey": ikey,
                "einvoice_status_text": status_text,
                "einvoice_pushed_at": now_datetime(),
                "einvoice_provider": provider_name,
            }, update_modified=False)
            _create_issuance_log(
                provider_name, sales_invoice, "Pushed Pending Sign",
                invoice_number=ikey,
            )
            frappe.db.commit()
            return {
                "success": True,
                "message": "Đã đẩy lên EasyInvoice. Vào app.easyinvoice.vn để ký số.",
                "ikey": ikey,
                "status_text": status_text,
            }
        else:
            error_msg = result.get("error") or "Lỗi không xác định"
            _create_issuance_log(provider_name, sales_invoice, "Failed", error=error_msg)
            return {"success": False, "message": f"Đẩy thất bại: {error_msg}"}

    @staticmethod
    def issue_bulk(sales_invoices, provider=None, pattern=None, serial=None,
                   issue_mode=None, send_email=None):
        """
        Issue outward e-invoices for multiple Sales Invoices.

        Args:
            sales_invoices: JSON string or list of Sales Invoice names

        Returns:
            dict with keys: success, message, results, background
        """
        if isinstance(sales_invoices, str):
            sales_invoices = json.loads(sales_invoices)

        settings = frappe.get_single("EInvoice Settings")
        limit = settings.bulk_issuance_limit or 50

        if len(sales_invoices) > limit:
            return {
                "success": False,
                "message": f"Số lượng tối đa là {limit} hóa đơn/lần. Bạn đã chọn {len(sales_invoices)}.",
            }

        if len(sales_invoices) > 5:
            frappe.enqueue(
                _process_bulk_issuance,
                queue="long",
                timeout=1200,
                sales_invoices=sales_invoices,
                provider=provider,
                pattern=pattern,
                serial=serial,
                issue_mode=issue_mode,
                send_email=send_email,
            )
            return {
                "success": True,
                "message": f"Đang xử lý {len(sales_invoices)} hóa đơn ở chế độ nền. "
                           f"Kiểm tra kết quả tại EInvoice Issuance Log.",
                "background": True,
            }

        return _process_bulk_issuance(sales_invoices, provider, pattern, serial, issue_mode, send_email)


def _resolve_provider(si_doc, provider_name, settings):
    """Resolve provider, priority by company of the Sales Invoice."""
    company = si_doc.company
    if provider_name:
        provider_doc = frappe.get_doc("EInvoice Provider", provider_name)
        if provider_doc.company != company:
            frappe.throw(
                f"Provider '{provider_name}' thuộc công ty '{provider_doc.company}', "
                f"không khớp với công ty '{company}' của hóa đơn."
            )
        return provider_doc

    candidates = frappe.get_all(
        "EInvoice Provider",
        filters={"enabled": 1, "company": company, "enable_outward": 1},
        pluck="name",
    )
    if len(candidates) == 1:
        return frappe.get_doc("EInvoice Provider", candidates[0])
    if len(candidates) > 1:
        if settings.default_provider:
            dp = frappe.get_doc("EInvoice Provider", settings.default_provider)
            if dp.company == company and dp.enabled:
                return dp
        frappe.throw(f"Công ty '{company}' có nhiều provider. Vui lòng chọn provider cụ thể.")
    frappe.throw(f"Không tìm thấy provider nào được bật cho công ty '{company}'.")


def _create_issuance_log(provider_name, sales_invoice, status, invoice_number="",
                         lookup_code="", pdf_url="", error=""):
    """Create an EInvoice Issuance Log record."""
    log = frappe.new_doc("EInvoice Issuance Log")
    log.provider = provider_name
    log.sales_invoice = sales_invoice
    log.issued_at = now_datetime()
    log.status = status
    log.provider_invoice_number = invoice_number
    log.provider_lookup_code = lookup_code
    log.provider_pdf_url = pdf_url
    log.error_detail = error
    log.insert(ignore_permissions=True)


def _process_bulk_issuance(sales_invoices, provider=None, pattern=None, serial=None,
                           issue_mode=None, send_email=None):
    """Process bulk issuance sequentially."""
    results = []
    for si_name in sales_invoices:
        result = IssuanceService.issue_single(
            sales_invoice=si_name,
            provider=provider,
            pattern=pattern,
            serial=serial,
            issue_mode=issue_mode,
            send_email=send_email,
        )
        results.append({"sales_invoice": si_name, "status": result.get("success"), "detail": result})

    success_count = sum(1 for r in results if r["status"])
    fail_count = len(results) - success_count

    return {
        "success": True,
        "message": f"Hoàn tất: {success_count} thành công, {fail_count} lỗi.",
        "results": results,
        "background": False,
    }


def _email_einvoice_pdf_to_customer(si_doc, result, provider_name):
    """Gửi PDF hóa đơn điện tử đã ký tới email khách hàng.

    Trả về 1 đoạn text status để gắn vào message phản hồi. KHÔNG raise — lỗi gửi mail
    chỉ ghi Issuance Log + Error Log, không làm fail luồng phát hành.
    """
    pdf_url = (result or {}).get("pdf_url") or ""
    recipient = _resolve_customer_email(si_doc)
    if not recipient:
        log_einvoice_error(
            f"Email skipped — no recipient ({si_doc.name})",
            "Không tìm thấy địa chỉ email khách hàng (contact_email / Customer primary contact).",
            provider=provider_name,
        )
        return "Bỏ qua gửi email: chưa có email khách hàng."
    if not pdf_url:
        log_einvoice_error(
            f"Email skipped — no PDF URL ({si_doc.name})",
            "Provider không trả pdf_url, không thể đính kèm.",
            provider=provider_name,
        )
        return "Bỏ qua gửi email: provider chưa trả URL PDF."

    try:
        subject = f"Hóa đơn điện tử {result.get('invoice_number') or ''} — {si_doc.company}"
        message = (
            f"<p>Kính gửi {frappe.utils.escape_html(si_doc.customer_name or si_doc.customer)},</p>"
            f"<p>Hóa đơn điện tử số <b>{frappe.utils.escape_html(result.get('invoice_number') or '')}</b> "
            f"cho hóa đơn bán hàng <b>{si_doc.name}</b> đã được phát hành.</p>"
            f"<p>Tổng tiền: <b>{frappe.utils.fmt_money(si_doc.grand_total, currency=si_doc.currency)}</b></p>"
            f"<p>Quý khách có thể tải file PDF tại: <a href='{pdf_url}'>{pdf_url}</a></p>"
            f"<p>Mã tra cứu: <code>{frappe.utils.escape_html(result.get('lookup_code') or '')}</code></p>"
            f"<p>Trân trọng,<br>{frappe.utils.escape_html(si_doc.company)}</p>"
        )
        frappe.sendmail(
            recipients=[recipient],
            subject=subject,
            message=message,
            reference_doctype="Sales Invoice",
            reference_name=si_doc.name,
            now=False,  # vào email queue, gửi async
        )
        return f"Đã xếp lịch gửi email tới {recipient}."
    except Exception as e:
        log_einvoice_error(
            f"Email send failed ({si_doc.name})",
            f"{e}",
            provider=provider_name,
        )
        return f"Lỗi gửi email: {e}"


def _resolve_customer_email(si_doc):
    """Pick a customer email address. Priority: SI.contact_email → Customer primary
    Contact's email_id → Customer.email_id (if field exists)."""
    if si_doc.get("contact_email"):
        return si_doc.contact_email
    if si_doc.customer:
        # Primary contact via Dynamic Link
        contact = frappe.db.sql(
            """SELECT c.email_id
               FROM `tabContact` c
               JOIN `tabDynamic Link` dl ON dl.parent = c.name
                 AND dl.parenttype = 'Contact'
                 AND dl.link_doctype = 'Customer'
                 AND dl.link_name = %s
               WHERE c.email_id IS NOT NULL AND c.email_id != ''
               ORDER BY c.is_primary_contact DESC, c.creation ASC
               LIMIT 1""",
            (si_doc.customer,),
        )
        if contact and contact[0][0]:
            return contact[0][0]
    return ""
