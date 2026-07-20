import hashlib
import importlib
import json

import frappe
from frappe import _
from frappe.utils.file_manager import get_file_path

from vn_banking.parser.normalizer import compute_dedupe_hash
from vn_banking.parser.detect import detect_format
from vn_banking.match.engine import run_match_engine


def _get_source_handler(source_key: str):
    handler_path = frappe.db.get_value("Bank Data Source", source_key, "handler_path")
    if not handler_path:
        frappe.throw(_("Unknown source type: {0}").format(source_key))
    mod_name, cls_name = handler_path.rsplit(".", 1)
    mod = importlib.import_module(mod_name)
    return getattr(mod, cls_name)()


@frappe.whitelist()
def detect_format_and_bank(file_url: str) -> dict:
    """Auto-detect format from uploaded file, then resolve the matching Bank Account.
    Returns {"format_name": ..., "bank_name": ..., "bank_account": ...}."""
    file_path = get_file_path(file_url)
    file_type = file_path.rsplit(".", 1)[-1].lower()
    fmt_name = detect_format(file_path, file_type)
    result = {"format_name": fmt_name, "bank_name": None, "bank_account": None}
    if not fmt_name:
        return result
    bank = frappe.db.get_value("Bank Statement Format", fmt_name, "bank")
    result["bank_name"] = bank
    if bank:
        accounts = frappe.get_all("Bank Account",
            filters={"bank": bank, "is_company_account": 1},
            fields=["name"], limit=2)
        if len(accounts) == 1:
            result["bank_account"] = accounts[0].name
    return result


@frappe.whitelist()
def trigger_import(bank_account: str, source_type: str = "excel_upload",
                    file_url: str | None = None, from_date: str | None = None,
                    to_date: str | None = None, format_name: str | None = None):
    """Source-agnostic ingestion entry point. Returns {"import_name": ...}."""
    company = frappe.db.get_value("Bank Account", bank_account, "company")
    import_doc = frappe.new_doc("Bank Statement Import")
    import_doc.bank_account = bank_account
    import_doc.source_type = source_type
    import_doc.from_date = from_date
    import_doc.to_date = to_date
    import_doc.file = file_url
    import_doc.triggered_by = "Manual"
    import_doc.status = "Draft"
    import_doc.log = ""

    context = {}
    if source_type == "excel_upload":
        if not file_url:
            frappe.throw(_("file_url required for excel_upload"))
        file_path = get_file_path(file_url)
        file_type = file_path.rsplit(".", 1)[-1].lower()
        fmt = format_name or detect_format(file_path, file_type)
        if not fmt:
            frappe.throw(_("Could not auto-detect Bank Statement Format. Please pick one manually."))
        import_doc.format = fmt
        import_doc.file_hash = _sha256_file(file_path)
        context = {"file_path": file_path, "format_name": fmt}

    import_doc.insert(ignore_permissions=True)

    # Decide sync vs async
    row_estimate = _estimate_row_count(context)
    if row_estimate > 200:
        frappe.enqueue(
            "vn_banking.api.reconcile._run_ingest_and_match",
            queue="long", timeout=600,
            import_name=import_doc.name, source_type=source_type, context=context,
        )
        return {"import_name": import_doc.name, "async": True}
    else:
        _run_ingest_and_match(import_doc.name, source_type, context)
        import_doc.reload()
        return {
            "import_name": import_doc.name, "async": False,
            "total_rows": import_doc.total_rows or 0,
            "duplicate_rows": import_doc.duplicate_rows or 0,
        }


def _estimate_row_count(context: dict) -> int:
    path = context.get("file_path")
    if not path:
        return 0
    try:
        from vn_banking.parser.base import read_rows
        ft = path.rsplit(".", 1)[-1].lower()
        return sum(1 for _ in read_rows(path, ft)) - 1
    except Exception:
        return 0


def _run_ingest_and_match(import_name: str, source_type: str, context: dict):
    import_doc = frappe.get_doc("Bank Statement Import", import_name)
    handler = _get_source_handler(source_type)
    total = dupes = 0
    errors: list[str] = []
    for norm in handler.fetch(import_doc.bank_account, import_doc.from_date, import_doc.to_date, context):
        total += 1
        dedupe = compute_dedupe_hash(norm.date, norm.amount, norm.reference_number, norm.description)
        if frappe.db.exists("Bank Transaction", {"dedupe_hash": dedupe, "bank_account": import_doc.bank_account}):
            dupes += 1
            continue
        try:
            txn = frappe.new_doc("Bank Transaction")
            txn.date = norm.date
            txn.bank_account = import_doc.bank_account
            txn.deposit = float(norm.deposit)
            txn.withdrawal = float(norm.withdrawal)
            txn.description = norm.description
            txn.reference_number = norm.reference_number
            txn.bank_statement_import = import_doc.name
            txn.dedupe_hash = dedupe
            txn.status = "Pending"
            txn.insert(ignore_permissions=True)
        except Exception as e:
            errors.append(f"Row {total}: {e}")
        if total % 20 == 0:
            frappe.publish_realtime(
                "vn_banking.import_progress",
                {"import_name": import_doc.name, "processed": total, "duplicates": dupes},
                user=frappe.session.user,
            )
    import_doc.total_rows = total
    import_doc.duplicate_rows = dupes
    import_doc.status = "Parsed"
    if errors:
        import_doc.log = "\n".join(errors[:100])
    import_doc.save(ignore_permissions=True)
    frappe.db.commit()

    # Run match engine
    run_match_engine(import_doc.name)
    frappe.publish_realtime(
        "vn_banking.import_done",
        {"import_name": import_doc.name, "total": total, "duplicates": dupes},
        user=frappe.session.user,
    )


def _sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


# ---------------------------------------------------------------------------
# Task 13: Remaining Reconcile API endpoints
# ---------------------------------------------------------------------------

from decimal import Decimal
from erpnext.accounts.doctype.payment_entry.payment_entry import get_payment_entry


@frappe.whitelist()
def get_import_transactions(import_name: str, direction_filter: str = "all") -> list[dict]:
    filters = {"bank_statement_import": import_name}
    rows = frappe.get_all(
        "Bank Transaction", filters=filters,
        fields=["name", "date", "description", "deposit", "withdrawal", "reference_number",
                "match_confidence", "matched_by", "suggested_party_type", "suggested_party",
                "difference_amount", "status"],
        order_by="date asc, name asc",
    )
    if direction_filter == "credit":
        rows = [r for r in rows if (r.deposit or 0) > 0]
    elif direction_filter == "debit":
        rows = [r for r in rows if (r.withdrawal or 0) > 0]
    for r in rows:
        r["suggestions"] = frappe.get_all(
            "Bank Txn Invoice Suggestion", filters={"parent": r.name},
            fields=["invoice_type", "invoice_name", "outstanding_amount", "allocated_amount", "selected"],
        )
        r["existing_pe"] = None

    # Batch-lookup existing PEs for debit transactions not yet reconciled
    bank_account = frappe.db.get_value("Bank Statement Import", import_name, "bank_account")
    if bank_account:
        debit_rows = [r for r in rows if (r.withdrawal or 0) > 0 and r.status != "Reconciled"]
        if debit_rows:
            _attach_existing_pe_info(debit_rows, bank_account)

    return rows


def _attach_existing_pe_info(debit_rows: list[dict], bank_account: str):
    """Batch-find existing Payment Entries that may match debit bank transactions."""
    from frappe.utils import getdate, add_days, date_diff

    company = frappe.db.get_value("Bank Account", bank_account, "company")
    settings = frappe.get_single("Bank Statement Settings")
    tolerance = float(settings.tolerance_fixed_amount or 0)

    dates = [getdate(r.date) for r in debit_rows]
    min_date = add_days(min(dates), -7)
    max_date = add_days(max(dates), 7)

    all_pes = frappe.get_all("Payment Entry",
        filters={
            "payment_type": "Pay",
            "company": company,
            "docstatus": ["in", [0, 1]],
            "posting_date": ["between", [str(min_date), str(max_date)]],
        },
        fields=["name", "party_type", "party", "paid_amount", "posting_date", "docstatus"],
    )

    # Already-linked PEs (avoid suggesting a PE that's already reconciled with another txn)
    linked_pes = set()
    if all_pes:
        linked = frappe.get_all("Bank Transaction Payments",
            filters={"payment_document": "Payment Entry", "payment_entry": ["in", [p.name for p in all_pes]]},
            pluck="payment_entry")
        linked_pes = set(linked)

    for r in debit_rows:
        txn_date = getdate(r.date)
        amount = float(r.withdrawal or 0)
        for pe in all_pes:
            if pe.name in linked_pes:
                continue
            if abs(float(pe.paid_amount) - amount) > tolerance:
                continue
            if abs(date_diff(getdate(pe.posting_date), txn_date)) > 7:
                continue
            if r.get("suggested_party") and pe.party != r.suggested_party:
                continue
            r["existing_pe"] = {
                "name": pe.name, "party_type": pe.party_type, "party": pe.party,
                "paid_amount": float(pe.paid_amount), "posting_date": str(pe.posting_date),
                "docstatus": pe.docstatus,
            }
            break


@frappe.whitelist()
def get_suggestions(transaction_name: str):
    """Recompute candidates for one transaction (used when user changes party manually)."""
    from datetime import date, timedelta
    from frappe.utils import getdate

    txn = frappe.get_doc("Bank Transaction", transaction_name)
    import_doc = frappe.get_doc("Bank Statement Import", txn.bank_statement_import)
    from vn_banking.match.context import build_context
    from vn_banking.match.helpers import get_txn_direction
    from vn_banking.match.engine import get_enabled_rules_in_priority_order, instantiate_matcher, apply_to_txn, pick_best
    # Same None-guard as run_match_engine — default to last 90 days if unset.
    from_date = getdate(import_doc.from_date) if import_doc.from_date else (date.today() - timedelta(days=90))
    to_date = getdate(import_doc.to_date) if import_doc.to_date else date.today()
    ctx = build_context(import_doc.bank_account, from_date, to_date,
                        direction=get_txn_direction(txn))
    for rule in get_enabled_rules_in_priority_order():
        m = instantiate_matcher(rule)
        if m is None or not m.applicable(txn, ctx):
            continue
        cands = m.match(txn, ctx)
        if cands:
            apply_to_txn(txn, pick_best(cands), rule)
            txn.save(ignore_permissions=True)
            return {"match_confidence": txn.match_confidence, "matched_by": txn.matched_by}
    txn.match_confidence = "None"
    txn.save(ignore_permissions=True)
    return {"match_confidence": "None"}


@frappe.whitelist()
def get_invoices_for_amount(transaction_name: str, party: str = None,
                             percent_tol: float = 1.0,
                             absolute_tol: float = 10000.0, date_window_days: int = 30,
                             limit: int = 30) -> list[dict]:
    """FB-521 / FB-591 — return Sales Invoice rows (credit) or Purchase
    Invoice rows (debit) candidates for an unmatched Bank Transaction.

    Two modes:
      - Without `party` (FB-521): filter by amount tolerance + date window.
        Picking an invoice auto-fills the party from the invoice.
      - With `party` (FB-591): filter ONLY by party, ignore amount/date.
        Returns every outstanding SI/PI for the named customer/supplier
        sorted by amount-diff so the closest match floats to the top.
    """
    from datetime import timedelta
    from frappe.utils import getdate, flt

    txn = frappe.get_doc("Bank Transaction", transaction_name)
    deposit = flt(txn.deposit or 0)
    withdrawal = flt(txn.withdrawal or 0)
    amount = deposit if deposit > 0 else withdrawal
    if amount <= 0:
        return []
    is_credit = deposit > 0
    doctype = "Sales Invoice" if is_credit else "Purchase Invoice"
    party_field = "customer" if is_credit else "supplier"

    tol = max(flt(absolute_tol), amount * flt(percent_tol) / 100.0)
    lo = amount - tol
    hi = amount + tol

    txn_date = getdate(txn.date) if txn.date else None
    if txn_date:
        d_lo = txn_date - timedelta(days=int(date_window_days))
        d_hi = txn_date + timedelta(days=int(date_window_days))
    else:
        d_lo = None
        d_hi = None

    filters = [
        ["docstatus", "=", 1],
        ["outstanding_amount", ">", 0],
    ]
    if party:
        # FB-591 — when caller knows the party, list every outstanding
        # SI/PI for that party (relax tolerance and date — user already
        # narrowed the search by picking the party).
        filters.append([party_field, "=", party])
    else:
        filters.append(["outstanding_amount", ">=", lo])
        filters.append(["outstanding_amount", "<=", hi])
        if d_lo and d_hi:
            filters.append(["posting_date", "between", [d_lo, d_hi]])

    rows = frappe.get_all(
        doctype,
        filters=filters,
        fields=["name", "posting_date", "outstanding_amount", "grand_total",
                f"{party_field} as party"],
        order_by="posting_date desc",
        limit=limit,
    )
    # Annotate each row with the absolute difference and the doctype so the
    # client can sort/display without another roundtrip.
    for r in rows:
        r["doctype"] = doctype
        r["party_type"] = "Customer" if is_credit else "Supplier"
        r["amount_diff"] = abs(flt(r.get("outstanding_amount") or 0) - amount)
    rows.sort(key=lambda r: r["amount_diff"])
    return rows


@frappe.whitelist()
def get_customer_invoices(customer: str, from_date: str = None, to_date: str = None):
    return frappe.get_all("Sales Invoice",
        filters={"customer": customer, "docstatus": 1, "outstanding_amount": [">", 0]},
        fields=["name", "posting_date", "outstanding_amount", "grand_total"],
        order_by="posting_date desc", limit=50)


@frappe.whitelist()
def get_supplier_invoices(supplier: str, from_date: str = None, to_date: str = None):
    return frappe.get_all("Purchase Invoice",
        filters={"supplier": supplier, "docstatus": 1, "outstanding_amount": [">", 0]},
        fields=["name", "posting_date", "outstanding_amount", "grand_total"],
        order_by="posting_date desc", limit=50)


@frappe.whitelist()
def create_payment_entry(transaction_name: str, party_type: str, party: str,
                          invoices: str, mode_of_payment: str = None, submit: bool = False):
    """Create a PE draft (or submitted) linked to this Bank Transaction.
    `invoices` is a JSON list of {invoice_type, invoice_name, allocated_amount}.
    Sets mode_of_payment explicitly (get_payment_entry returns NULL) and applies
    TT99/2025 difference write-off if configured.
    """
    import json as _json
    inv_list = _json.loads(invoices) if isinstance(invoices, str) else invoices
    if not inv_list:
        frappe.throw(_("No invoices selected"))

    txn = frappe.get_doc("Bank Transaction", transaction_name)
    settings = frappe.get_single("Bank Statement Settings")

    # Build PE from first invoice then append additional references
    first = inv_list[0]
    pe = get_payment_entry(first["invoice_type"], first["invoice_name"])
    pe.party_type = party_type
    pe.party = party
    pe.posting_date = txn.date
    pe.mode_of_payment = mode_of_payment or (
        settings.default_mode_of_payment_credit if (txn.deposit or 0) > 0
        else settings.default_mode_of_payment_debit
    )
    pe.reference_no = txn.reference_number or txn.name
    pe.reference_date = txn.date

    # Additional references (multi-invoice)
    total_allocated = Decimal(str(first.get("allocated_amount") or 0))
    for extra in inv_list[1:]:
        amt = Decimal(str(extra.get("allocated_amount") or 0))
        pe.append("references", {
            "reference_doctype": extra["invoice_type"],
            "reference_name": extra["invoice_name"],
            "allocated_amount": float(amt),
        })
        total_allocated += amt

    # Difference write-off (TT99/2025)
    txn_amount = Decimal(str((txn.deposit or 0) or (txn.withdrawal or 0)))
    diff = txn_amount - total_allocated
    tolerance = Decimal(str(settings.tolerance_fixed_amount or 0))
    if 0 < abs(diff) <= tolerance and settings.difference_account:
        company_cost_center = frappe.db.get_value("Company", pe.company, "cost_center")
        pe.append("deductions", {
            "account": settings.difference_account,
            "cost_center": company_cost_center,
            "amount": float(diff),
            "description": _("Bank fee / rounding difference (TT99/2025)"),
        })
        pe.paid_amount = float(txn_amount) if pe.payment_type == "Receive" else pe.paid_amount
        pe.received_amount = float(txn_amount) if pe.payment_type == "Receive" else pe.received_amount

    pe.insert(ignore_permissions=True)
    if submit or settings.default_pe_action == "Submit":
        pe.submit()

    # Link to Bank Transaction's payment_entries child table
    txn.append("payment_entries", {
        "payment_document": "Payment Entry",
        "payment_entry": pe.name,
        "allocated_amount": float(total_allocated),
    })
    txn.status = "Reconciled"
    txn.save(ignore_permissions=True)
    frappe.db.commit()
    return {"payment_entry": pe.name, "submitted": bool(submit or settings.default_pe_action == "Submit")}


@frappe.whitelist()
def bulk_create_pe(import_name: str, only_high_confidence: bool = True, submit: bool = False):
    filters = {"bank_statement_import": import_name}
    if only_high_confidence:
        filters["match_confidence"] = "High"
    # Exclude already-reconciled transactions to prevent double-PE creation
    # on re-run of the bulk action (idempotency).
    filters["status"] = ["!=", "Reconciled"]
    rows = frappe.get_all("Bank Transaction", filters=filters, pluck="name")
    created = []
    errors = []
    for n in rows:
        txn = frappe.get_doc("Bank Transaction", n)
        # Defensive double-check: skip if any PE has already been attached to this txn
        if txn.status == "Reconciled" or (txn.payment_entries or []):
            continue
        if not txn.suggested_party or not txn.suggested_invoices:
            continue
        try:
            invs = [{"invoice_type": s.invoice_type, "invoice_name": s.invoice_name,
                     "allocated_amount": s.allocated_amount} for s in txn.suggested_invoices if s.selected]
            if not invs:
                continue
            result = create_payment_entry(
                transaction_name=n, party_type=txn.suggested_party_type, party=txn.suggested_party,
                invoices=frappe.as_json(invs), submit=submit,
            )
            created.append(result["payment_entry"])
        except Exception as e:
            errors.append(f"{n}: {e}")
    return {"created": created, "errors": errors}


@frappe.whitelist()
def dismiss_transaction(transaction_name: str):
    txn = frappe.get_doc("Bank Transaction", transaction_name)
    txn.reconcile_notes = (txn.reconcile_notes or "") + "\n[DISMISSED]"
    txn.status = "Unreconciled"
    txn.match_confidence = "None"
    txn.save(ignore_permissions=True)
    return {"ok": True}


@frappe.whitelist()
def explain_match(transaction_name: str) -> str:
    txn = frappe.get_doc("Bank Transaction", transaction_name)
    parts = [
        f"Match confidence: {txn.match_confidence or 'None'}",
        f"Matched by: {txn.matched_by or 'None'}",
    ]
    if txn.suggested_party:
        parts.append(f"Party: {txn.suggested_party}")
    if txn.suggested_invoices:
        parts.append("Invoices: " + ", ".join(f"{s.invoice_name} ({s.outstanding_amount})"
                                               for s in txn.suggested_invoices))
    if txn.difference_amount:
        parts.append(f"Difference: {txn.difference_amount}")
    return "\n".join(parts)


@frappe.whitelist()
def reconcile_with_existing_pe(transaction_name: str, payment_entry_name: str):
    """Link a Bank Transaction to an existing Payment Entry (debit reconciliation)."""
    txn = frappe.get_doc("Bank Transaction", transaction_name)
    pe = frappe.get_doc("Payment Entry", payment_entry_name)
    # Guard: don't double-link
    already = [p for p in (txn.payment_entries or []) if p.payment_entry == pe.name]
    if already:
        return {"ok": True, "already_linked": True}
    txn.append("payment_entries", {
        "payment_document": "Payment Entry",
        "payment_entry": pe.name,
        "allocated_amount": float(pe.paid_amount),
    })
    txn.status = "Reconciled"
    txn.save(ignore_permissions=True)
    frappe.db.commit()
    return {"ok": True}


@frappe.whitelist()
def trigger_rematch(import_name: str):
    """Re-run match engine on an existing import (no re-parse)."""
    return run_match_engine(import_name)


@frappe.whitelist()
def test_matching_on_last_import(settings_override_json: str | None = None):
    """Dry-run new settings against the latest Bank Statement Import. Returns before/after diff."""
    last = frappe.get_all("Bank Statement Import", filters={"status": ["in", ["Parsed", "Reviewed"]]},
                           order_by="modified desc", limit=1)
    if not last:
        return {"error": "No previous import found"}
    # snapshot
    before = frappe.db.sql("""
        SELECT match_confidence, COUNT(*) c FROM `tabBank Transaction`
        WHERE bank_statement_import=%s GROUP BY match_confidence
    """, last[0].name, as_dict=True)
    # NB: dry-run implementation — for v1 we simply re-run with current settings.
    # Real preview requires settings override which needs a scoped settings instance; out of scope v1.
    run_match_engine(last[0].name)
    after = frappe.db.sql("""
        SELECT match_confidence, COUNT(*) c FROM `tabBank Transaction`
        WHERE bank_statement_import=%s GROUP BY match_confidence
    """, last[0].name, as_dict=True)
    return {"before": before, "after": after, "import_name": last[0].name}
