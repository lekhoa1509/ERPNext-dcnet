"""
Whitelisted API endpoints for EInvoice.

Called from client-side JS for issuing invoices (single & bulk).
"""

import frappe
from frappe.utils import now_datetime, flt


def has_app_permission():
    """Permission check for apps screen."""
    return "System Manager" in frappe.get_roles() or "Accounts Manager" in frappe.get_roles()


def _resolve_provider(si_doc, provider_name, settings):
    """Resolve provider, ưu tiên theo company của Sales Invoice."""
    company = si_doc.company
    if provider_name:
        provider_doc = frappe.get_doc("EInvoice Provider", provider_name)
        if provider_doc.company != company:
            frappe.throw(
                f"Provider '{provider_name}' thuộc công ty '{provider_doc.company}', "
                f"không khớp với công ty '{company}' của hóa đơn."
            )
        return provider_doc
    # Auto-resolve: tìm provider enabled cho company này
    candidates = frappe.get_all(
        "EInvoice Provider",
        filters={"enabled": 1, "company": company},
        pluck="name",
    )
    if len(candidates) == 1:
        return frappe.get_doc("EInvoice Provider", candidates[0])
    if len(candidates) > 1:
        # Fallback: dùng default_provider nếu nó thuộc đúng company
        if settings.default_provider:
            dp = frappe.get_doc("EInvoice Provider", settings.default_provider)
            if dp.company == company and dp.enabled:
                return dp
        frappe.throw(f"Công ty '{company}' có nhiều provider. Vui lòng chọn provider cụ thể.")
    frappe.throw(f"Không tìm thấy provider nào được bật cho công ty '{company}'.")


@frappe.whitelist()
def issue_single_invoice(sales_invoice, provider=None, pattern=None, serial=None, issue_mode=None):
    """
    Issue a single outward e-invoice from a submitted Sales Invoice.

    Args:
        sales_invoice: Name of the Sales Invoice
        provider: Name of the EInvoice Provider (optional, uses default)
        pattern: Invoice pattern override (optional)
        serial: Invoice serial override (optional)
        issue_mode: 'Draft' or 'Publish' override (optional)
    """
    si_doc = frappe.get_doc("Sales Invoice", sales_invoice)

    # Validations
    if si_doc.docstatus != 1:
        frappe.throw("Chỉ có thể xuất hóa đơn đỏ cho Sales Invoice đã Submit.")
    if si_doc.einvoice_issued:
        frappe.throw("Sales Invoice này đã xuất hóa đơn đỏ rồi.")

    settings = frappe.get_single("EInvoice Settings")

    provider_doc = _resolve_provider(si_doc, provider, settings)
    provider_name = provider_doc.name
    provider_instance = provider_doc.get_provider_instance()

    # Override pattern/serial if provided
    if pattern:
        provider_doc.default_invoice_pattern = pattern
    if serial:
        provider_doc.default_invoice_serial = serial
    if issue_mode:
        settings.default_issue_mode = issue_mode

    # Authenticate and issue
    provider_instance.authenticate()
    payload = provider_instance.map_sales_invoice_to_payload(si_doc, settings)
    result = provider_instance.issue_outward_invoice(payload)

    # Create Issuance Log
    log = frappe.new_doc("EInvoice Issuance Log")
    log.provider = provider_name
    log.sales_invoice = sales_invoice
    log.issued_at = now_datetime()

    if result.get("success"):
        log.status = "Success"
        log.provider_invoice_number = result.get("invoice_number", "")
        log.provider_lookup_code = result.get("lookup_code", "")
        log.provider_pdf_url = result.get("pdf_url", "")
        log.insert(ignore_permissions=True)

        # Update Sales Invoice custom fields
        frappe.db.set_value("Sales Invoice", sales_invoice, {
            "einvoice_issued": 1,
            "einvoice_provider": provider_name,
            "einvoice_number": result.get("invoice_number", ""),
            "einvoice_lookup_code": result.get("lookup_code", ""),
            "einvoice_pdf_url": result.get("pdf_url", ""),
            "einvoice_issued_at": now_datetime(),
        }, update_modified=False)

        frappe.db.commit()
        return {
            "success": True,
            "message": "Xuất hóa đơn đỏ thành công!",
            "invoice_number": result.get("invoice_number"),
            "lookup_code": result.get("lookup_code"),
            "pdf_url": result.get("pdf_url"),
        }
    else:
        log.status = "Failed"
        log.error_detail = result.get("error", str(result.get("raw_response", "")))
        log.insert(ignore_permissions=True)
        frappe.db.commit()

        frappe.throw(f"Xuất hóa đơn đỏ thất bại: {result.get('error', 'Lỗi không xác định')}")


@frappe.whitelist()
def issue_bulk_invoices(sales_invoices, provider=None, pattern=None, serial=None, issue_mode=None):
    """
    Issue outward e-invoices for multiple Sales Invoices.

    Args:
        sales_invoices: JSON string of list of Sales Invoice names
    """
    import json

    if isinstance(sales_invoices, str):
        sales_invoices = json.loads(sales_invoices)

    settings = frappe.get_single("EInvoice Settings")
    limit = settings.bulk_issuance_limit or 50

    if len(sales_invoices) > limit:
        frappe.throw(f"Số lượng tối đa là {limit} hóa đơn/lần. Bạn đã chọn {len(sales_invoices)}.")

    # If more than 5, enqueue as background job
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
        )
        return {
            "success": True,
            "message": f"Đang xử lý {len(sales_invoices)} hóa đơn ở chế độ nền. Kiểm tra kết quả tại EInvoice Issuance Log.",
            "background": True,
        }

    # Process inline for small batches
    return _process_bulk_issuance(sales_invoices, provider, pattern, serial, issue_mode)


def _process_bulk_issuance(sales_invoices, provider=None, pattern=None, serial=None, issue_mode=None):
    """Process bulk issuance sequentially."""
    results = []
    for si_name in sales_invoices:
        try:
            result = issue_single_invoice(
                sales_invoice=si_name,
                provider=provider,
                pattern=pattern,
                serial=serial,
                issue_mode=issue_mode,
            )
            results.append({"sales_invoice": si_name, "status": "Success", "detail": result})
        except Exception as e:
            results.append({"sales_invoice": si_name, "status": "Failed", "detail": str(e)})

    success_count = sum(1 for r in results if r["status"] == "Success")
    fail_count = len(results) - success_count

    return {
        "success": True,
        "message": f"Hoàn tất: {success_count} thành công, {fail_count} lỗi.",
        "results": results,
        "background": False,
    }


@frappe.whitelist()
def get_providers(company=None):
    """Get list of enabled providers for the dropdown."""
    filters = {"enabled": 1}
    if company:
        filters["company"] = company
    return frappe.get_all(
        "EInvoice Provider",
        filters=filters,
        fields=["name", "provider_name", "provider_type", "default_invoice_pattern", "default_invoice_serial"],
    )
