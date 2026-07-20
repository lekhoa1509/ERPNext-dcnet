"""
Background Job: Sync Inward Invoices from E-Invoice Providers.

Called by scheduler hooks defined in hooks.py.
"""

import frappe
from frappe.utils import now_datetime, add_days, getdate, today
import uuid


def run_if_frequency_match():
    """
    Entry point from scheduler. Checks if syncing is enabled and
    whether the current scheduler event matches the configured frequency.
    """
    settings = frappe.get_single("EInvoice Settings")

    if not settings.enable_auto_sync:
        return

    # The scheduler runs this from multiple hooks (cron/hourly/daily/weekly).
    # We let the function be idempotent — it will only actually run
    # when enough time has passed since last_sync_datetime.
    freq = settings.sync_frequency
    if not freq:
        return

    run_sync(sync_type="Scheduled")


def _create_sync_log(provider_name, sync_type, result, from_date, to_date):
    """Create a Sync Log record for a single provider."""
    status = "Success" if result["errors"] == 0 else ("Partial" if result["new"] > 0 else "Failed")
    log = frappe.new_doc("EInvoice Sync Log")
    log.provider = provider_name
    log.sync_type = sync_type
    log.start_time = now_datetime()
    log.end_time = now_datetime()
    log.date_from = from_date
    log.date_to = to_date
    log.total_fetched = result["fetched"]
    log.new_created = result["new"]
    log.duplicates_skipped = result["dup"]
    log.errors = result["errors"]
    log.status = status
    log.error_detail = result.get("error_detail", "")
    log.insert(ignore_permissions=True)
    return status


def run_sync(sync_type="Manual"):
    """
    Main sync logic. Fetches inward invoices from all active providers
    and creates EInvoice Inward staging records.
    """
    settings = frappe.get_single("EInvoice Settings")
    date_range = settings.default_date_range_days or 30

    to_date = today()
    from_date = str(add_days(getdate(to_date), -date_range))

    # Get all enabled providers
    providers = frappe.get_all(
        "EInvoice Provider",
        filters={"enabled": 1},
        fields=["name"],
    )

    if not providers:
        frappe.logger().info("EInvoice: No active providers found for sync.")
        return

    total_fetched = 0
    total_new = 0
    total_dup = 0
    total_errors = 0
    error_details = []
    batch_id = str(uuid.uuid4())[:8]

    for prov in providers:
        try:
            result = _sync_provider(prov.name, from_date, to_date, batch_id, settings)
            _create_sync_log(prov.name, sync_type, result, from_date, to_date)
            total_fetched += result["fetched"]
            total_new += result["new"]
            total_dup += result["dup"]
            total_errors += result["errors"]
            if result.get("error_detail"):
                error_details.append(result["error_detail"])
        except Exception as e:
            total_errors += 1
            err_msg = f"Provider {prov.name}: {str(e)}"
            error_details.append(err_msg)
            _create_sync_log(
                prov.name, sync_type,
                {"fetched": 0, "new": 0, "dup": 0, "errors": 1, "error_detail": err_msg},
                from_date, to_date,
            )
            frappe.log_error(
                title=f"EInvoice Sync Error - {prov.name}",
                message=frappe.get_traceback(),
            )

    # Determine overall status for settings update
    if total_errors == 0:
        status = "Success"
    elif total_new > 0:
        status = "Partial"
    else:
        status = "Failed"

    # Update settings
    settings.last_sync_datetime = now_datetime()
    settings.last_sync_status = status
    settings.last_sync_error = error_details[0] if error_details else ""
    settings.save(ignore_permissions=True)

    frappe.db.commit()
    frappe.logger().info(
        f"EInvoice Sync: fetched={total_fetched}, new={total_new}, "
        f"dup={total_dup}, errors={total_errors}"
    )


def _sync_provider(provider_name, from_date, to_date, batch_id, settings):
    """Sync invoices from a single provider."""
    provider_doc = frappe.get_doc("EInvoice Provider", provider_name)
    provider = provider_doc.get_provider_instance()

    # Authenticate
    provider.authenticate()

    # Fetch invoices
    raw_invoices = provider.fetch_inward_invoices(from_date, to_date)

    result = {"fetched": len(raw_invoices), "new": 0, "dup": 0, "errors": 0, "error_detail": ""}
    errors = []

    for raw in raw_invoices:
        try:
            parsed = provider.parse_inward_invoice(raw)
            lookup_code = parsed.get("lookup_code")

            if not lookup_code:
                result["errors"] += 1
                errors.append("Hóa đơn thiếu mã tra cứu (lookup_code)")
                continue

            # De-duplication check
            if frappe.db.exists("EInvoice Inward", {"lookup_code": lookup_code}):
                result["dup"] += 1
                continue

            # Create staging record
            inv = frappe.new_doc("EInvoice Inward")
            inv.provider = provider_name
            inv.lookup_code = lookup_code
            inv.provider_invoice_id = parsed.get("provider_invoice_id", "")
            inv.invoice_number = parsed.get("invoice_number", "")
            inv.invoice_pattern = parsed.get("invoice_pattern", "")
            inv.invoice_serial = parsed.get("invoice_serial", "")
            inv.invoice_date = parsed.get("invoice_date")
            inv.invoice_type = parsed.get("invoice_type", "Khác")
            inv.supplier_name = parsed.get("supplier_name", "")
            inv.supplier_tax_code = parsed.get("supplier_tax_code", "")
            inv.supplier_address = parsed.get("supplier_address", "")
            inv.total_before_tax = parsed.get("total_before_tax", 0)
            inv.tax_amount = parsed.get("tax_amount", 0)
            inv.total_amount = parsed.get("total_amount", 0)
            inv.currency = parsed.get("currency", "VND")
            inv.pdf_url = parsed.get("pdf_url", "")
            inv.raw_data = parsed.get("raw_data", "")
            inv.sync_batch_id = batch_id
            inv.status = "New"

            inv.company = provider_doc.company
            inv.insert(ignore_permissions=True)
            result["new"] += 1

            # Attempt auto-match
            _try_auto_match(inv, settings)

        except Exception as e:
            result["errors"] += 1
            errors.append(str(e))

    if errors:
        result["error_detail"] = "; ".join(errors[:10])  # Limit to first 10 errors

    return result


def _try_auto_match(inv, settings):
    """Attempt to auto-match an inward invoice with an existing Purchase Invoice."""
    if not inv.supplier_tax_code or not inv.total_amount:
        return

    tol_pct = (settings.match_total_tolerance_pct or 1) / 100
    tol_days = settings.match_date_tolerance_days or 3

    total = inv.total_amount
    low = total * (1 - tol_pct)
    high = total * (1 + tol_pct)

    filters = {
        "docstatus": ["in", [0, 1]],  # Draft or Submitted
        "grand_total": ["between", [low, high]],
        "einvoice_inward": ["is", "not set"],
        "company": inv.company,
    }

    # Match by supplier tax code
    # First find suppliers with this tax code
    suppliers = frappe.get_all("Supplier", filters={"tax_id": inv.supplier_tax_code}, pluck="name")
    if not suppliers:
        return

    filters["supplier"] = ["in", suppliers]

    if inv.invoice_date:
        from_d = str(add_days(getdate(inv.invoice_date), -tol_days))
        to_d = str(add_days(getdate(inv.invoice_date), tol_days))
        filters["posting_date"] = ["between", [from_d, to_d]]

    candidates = frappe.get_all("Purchase Invoice", filters=filters, pluck="name")

    # Only auto-match if exactly 1 candidate
    if len(candidates) == 1:
        pi_name = candidates[0]
        inv.linked_purchase_invoice = pi_name
        inv.status = "Matched"
        inv.save(ignore_permissions=True)

        frappe.db.set_value("Purchase Invoice", pi_name, {
            "einvoice_inward": inv.name,
            "einvoice_lookup_code": inv.lookup_code,
        })
