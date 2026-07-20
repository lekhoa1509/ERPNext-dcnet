"""
Sync Service — Inward Invoice Synchronization.

Fetches inward invoices from all active providers, creates staging records,
and attempts auto-matching with existing Purchase Invoices.

Extracted from tasks/__init__.py for testability and separation of concerns.
"""

import uuid

import frappe
from frappe.utils import now_datetime, add_days, getdate, today, flt, get_datetime

from einvoice.einvoice.exceptions import EInvoiceProviderError, EInvoiceProviderNotReady


FREQ_MAP = {
    "Every 15 Min": 900,
    "Hourly": 3600,
    "Every 6 Hours": 21600,
    "Daily": 86400,
    "Weekly": 604800,
}


def log_einvoice_error(title, message, provider=None):
    """Log error with [EInvoice] prefix for easy filtering."""
    frappe.log_error(
        title=f"[EInvoice] {title}",
        message=message,
        reference_doctype="EInvoice Provider" if provider else None,
        reference_name=provider,
    )


def run_if_frequency_match():
    """
    Entry point from scheduler hooks.

    Guards:
    - EInvoice Settings must exist
    - Auto-sync must be enabled
    - Enough time must have elapsed since last sync
    - Distributed lock prevents concurrent runs
    """
    if not frappe.db.exists("EInvoice Settings", "EInvoice Settings"):
        return

    settings = frappe.get_single("EInvoice Settings")

    if not settings.enable_auto_sync:
        return

    freq = settings.sync_frequency
    if not freq:
        return

    min_interval = FREQ_MAP.get(freq)
    if not min_interval:
        return

    # Check elapsed time since last sync.
    # last_sync_datetime can come back as a str (Single doc loaded from Redis
    # cache in worker context does not always re-cast Datetime fields), so
    # coerce via get_datetime() to avoid `datetime - str` TypeError that
    # crashed every scheduled run before it could fetch.
    if settings.last_sync_datetime:
        last_sync = get_datetime(settings.last_sync_datetime)
        elapsed = (now_datetime() - last_sync).total_seconds()
        if elapsed < min_interval:
            return

    # Distributed lock via Redis
    lock_key = "einvoice_sync_running"
    if frappe.cache.get_value(lock_key):
        return
    frappe.cache.set_value(lock_key, 1, expires_in_sec=300)

    try:
        SyncService.run_sync(sync_type="Scheduled")
    finally:
        frappe.cache.delete_key(lock_key)


class SyncService:
    """Service class for inward invoice sync operations."""

    @staticmethod
    def run_sync(sync_type="Manual"):
        """
        Main sync logic. Fetches inward invoices from all active providers
        and creates EInvoice Inward staging records.

        Returns:
            dict with keys: status, fetched, new, dup, errors
        """
        settings = frappe.get_single("EInvoice Settings")
        date_range = settings.default_date_range_days or 30

        to_date = today()
        from_date = str(add_days(getdate(to_date), -date_range))

        providers = frappe.get_all(
            "EInvoice Provider",
            filters={"enabled": 1, "enable_inward": 1},
            fields=["name"],
        )

        if not providers:
            frappe.logger().info("EInvoice: No active providers found for sync.")
            return {"status": "No providers", "fetched": 0, "new": 0, "dup": 0, "errors": 0}

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
            except EInvoiceProviderNotReady as e:
                # Skip stub providers silently during sync
                frappe.logger().info(f"EInvoice: Skipping {prov.name} — {e.message}")
            except Exception as e:
                total_errors += 1
                err_msg = f"Provider {prov.name}: {str(e)}"
                error_details.append(err_msg)
                _create_sync_log(
                    prov.name, sync_type,
                    {"fetched": 0, "new": 0, "dup": 0, "errors": 1, "error_detail": err_msg},
                    from_date, to_date,
                )
                log_einvoice_error(
                    f"Sync Error - {prov.name}",
                    frappe.get_traceback(),
                    provider=prov.name,
                )

        # Determine overall status
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

        return {
            "status": status,
            "fetched": total_fetched,
            "new": total_new,
            "dup": total_dup,
            "errors": total_errors,
        }


def _sync_provider(provider_name, from_date, to_date, batch_id, settings):
    """Sync invoices from a single provider."""
    provider_doc = frappe.get_doc("EInvoice Provider", provider_name)
    provider = provider_doc.get_provider_instance()

    provider.authenticate()
    raw_invoices = provider.fetch_inward_invoices(from_date, to_date)

    result = {"fetched": len(raw_invoices), "new": 0, "dup": 0, "errors": 0, "error_detail": ""}
    errors = []
    inserted_names = []

    for raw in raw_invoices:
        try:
            parsed = provider.parse_inward_invoice(raw)
            lookup_code = parsed.get("lookup_code")
            provider_invoice_id = parsed.get("provider_invoice_id") or ""

            if not lookup_code:
                # Fallback: synthesize from provider + provider_invoice_id (handles
                # invoices Mắt Bão returns before CQT cấp MCCQT — lifecycle pre-issued
                # state). Provider prefix ensures no collision across providers.
                if provider_invoice_id:
                    lookup_code = f"{provider_name}-{provider_invoice_id}"
                else:
                    result["errors"] += 1
                    errors.append("Hóa đơn thiếu cả MCCQT và provider_invoice_id")
                    continue

            # Dedup by provider_invoice_id first (handles MCCQT-arrives-later case:
            # synthesized lookup_code → real MCCQT update on next sync).
            if provider_invoice_id:
                existing_pid = frappe.db.exists(
                    "EInvoice Inward",
                    {"provider": provider_name, "provider_invoice_id": provider_invoice_id},
                )
                if existing_pid:
                    # If new sync gave us a real MCCQT but record had synthesized one,
                    # update lookup_code to the real value.
                    cur_lookup = frappe.db.get_value("EInvoice Inward", existing_pid, "lookup_code") or ""
                    if cur_lookup.startswith(f"{provider_name}-") and not lookup_code.startswith(f"{provider_name}-"):
                        frappe.db.set_value("EInvoice Inward", existing_pid, "lookup_code", lookup_code, update_modified=False)
                    result["dup"] += 1
                    continue

            if frappe.db.exists("EInvoice Inward", {"lookup_code": lookup_code}):
                result["dup"] += 1
                continue

            inv = frappe.new_doc("EInvoice Inward")
            inv.provider = provider_name
            inv.lookup_code = lookup_code
            inv.provider_invoice_id = parsed.get("provider_invoice_id", "")
            inv.invoice_number = parsed.get("invoice_number", "")
            inv.invoice_pattern = parsed.get("invoice_pattern", "")
            inv.invoice_serial = parsed.get("invoice_serial", "")
            inv.invoice_date = parsed.get("invoice_date")
            inv.signed_date = parsed.get("signed_date")
            inv.invoice_type = parsed.get("invoice_type", "Khác")
            # Legal/TCT
            inv.tct_status = parsed.get("tct_status") or "Unknown"
            inv.lifecycle_status = parsed.get("lifecycle_status", "")
            inv.e_invoice_type = parsed.get("e_invoice_type") or ""
            inv.profile_code = parsed.get("profile_code", "")
            inv.tvan_tax_code = parsed.get("tvan_tax_code", "")
            # Supplier
            inv.supplier_name = parsed.get("supplier_name", "")
            inv.supplier_tax_code = parsed.get("supplier_tax_code", "")
            inv.supplier_address = parsed.get("supplier_address", "")
            # Amount
            inv.total_before_tax = parsed.get("total_before_tax", 0)
            inv.tax_rate = parsed.get("tax_rate", 0)
            inv.exchange_rate = parsed.get("exchange_rate", 1)
            inv.tax_amount = parsed.get("tax_amount", 0)
            inv.total_amount = parsed.get("total_amount", 0)
            inv.currency = parsed.get("currency", "VND")
            # Discount/payment
            inv.payment_method = parsed.get("payment_method", "")
            inv.trade_discount = parsed.get("trade_discount", 0)
            inv.other_reduce = parsed.get("other_reduce", 0)
            inv.total_in_words = parsed.get("total_in_words", "")
            # Links
            inv.pdf_url = parsed.get("pdf_url", "")
            inv.xml_url = parsed.get("xml_url", "")
            inv.raw_data = parsed.get("raw_data", "")
            inv.sync_batch_id = batch_id
            inv.status = "New"
            inv.company = provider_doc.company
            # Line items (DSHHDVu)
            for item_row in (parsed.get("items") or []):
                inv.append("items", item_row)
            inv.insert(ignore_permissions=True)
            inserted_names.append(inv.name)

            # Auto-fetch validation chi tiết cho HĐ "Có sai sót"
            # (chỉ records "Hợp lệ" skip — tiết kiệm API calls)
            if inv.tct_status == "Hóa đơn có sai sót" and inv.xml_url:
                try:
                    import json as _json
                    val_result = provider.fetch_invoice_validation(inv.xml_url)
                    if val_result.get("status") == "ok":
                        inv.validation_summary = val_result.get("summary", "")[:500]
                        inv.validation_issues_json = _json.dumps(val_result.get("raw", {}), ensure_ascii=False, default=str)
                        inv.validation_checked_at = now_datetime()
                        inv.save(ignore_permissions=True)
                except Exception as e:
                    log_einvoice_error(
                        f"Validation fetch fail cho {inv.name}",
                        f"{type(e).__name__}: {e}",
                        provider=provider_name,
                    )
            result["new"] += 1

            _try_auto_match(inv, settings)

        except Exception as e:
            result["errors"] += 1
            errors.append(str(e))

    if errors:
        result["error_detail"] = "; ".join(errors[:10])

    if inserted_names:
        from einvoice.einvoice.services.attach import attach_files_batch
        frappe.enqueue(
            attach_files_batch,
            queue="long",
            job_id=f"einvoice_attach:sync:{batch_id}",
            timeout=max(600, len(inserted_names) * 60),
            invoice_names=inserted_names,
            user=frappe.session.user,
            source="sync",
        )

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
        "docstatus": ["in", [0, 1]],
        "grand_total": ["between", [low, high]],
        "einvoice_inward": ["is", "not set"],
        "company": inv.company,
    }

    suppliers = frappe.get_all("Supplier", filters={"tax_id": inv.supplier_tax_code}, pluck="name")
    if not suppliers:
        return

    filters["supplier"] = ["in", suppliers]

    if inv.invoice_date:
        from_d = str(add_days(getdate(inv.invoice_date), -tol_days))
        to_d = str(add_days(getdate(inv.invoice_date), tol_days))
        filters["posting_date"] = ["between", [from_d, to_d]]

    candidates = frappe.get_all("Purchase Invoice", filters=filters, pluck="name")

    if len(candidates) == 1:
        pi_name = candidates[0]
        inv.linked_purchase_invoice = pi_name
        inv.status = "Matched"
        inv.save(ignore_permissions=True)

        frappe.db.set_value("Purchase Invoice", pi_name, {
            "einvoice_inward": inv.name,
            "einvoice_lookup_code": inv.lookup_code,
        })


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
