import frappe
from frappe import _
from frappe.model.document import Document


class OpeningBalanceImport(Document):
    """Deterministic migration entry point for opening balances and invoices."""

    def validate(self):
        if not self.status:
            self.status = "Draft"
        if not self.api_base_url:
            self.api_base_url = "https://khoaapi.duckdns.org/v1"
        if not self.model:
            self.model = "cx/gpt-5.5"
        if not self.timeout_seconds:
            self.timeout_seconds = 90
        if not self.posting_date:
            self.posting_date = "2026-01-01"

    @frappe.whitelist()
    def analyze_files(self):
        self.check_permission("write")
        frappe.db.set_value(
            "Opening Balance Import",
            self.name,
            {"status": "Analyzing", "analysis_json": None},
            update_modified=True,
        )
        frappe.db.commit()

        job_id = f"import_auto::{self.name}::ob_analyze"
        frappe.enqueue(
            "dcnet_migrate.import_auto.doctype.opening_balance_import.opening_balance_import._run_analyze_background",
            queue="long",
            job_id=job_id,
            docname=self.name,
            triggered_by=frappe.session.user,
            timeout=300,
            enqueue_after_commit=True,
            now=frappe.flags.in_test,
        )
        return {"job_id": job_id, "enqueued": True, "status": "Analyzing"}

    @frappe.whitelist()
    def preview_migration(self):
        self.check_permission("read")
        from dcnet_migrate.import_auto.services.opening_balance import (
            preview_opening_migration,
        )

        return preview_opening_migration(self)

    @frappe.whitelist()
    def create_missing_masters(self):
        self.check_permission("write")
        from dcnet_migrate.import_auto.services.opening_balance import (
            create_opening_missing_masters,
        )

        return create_opening_missing_masters(self)

    @frappe.whitelist()
    def execute_opening_journal(self, posting_date: str | None = None, submit=0, force=0, balance_account: str | None = None):
        self.check_permission("write")
        from dcnet_migrate.import_auto.services.opening_balance import (
            execute_opening_balances,
        )

        return execute_opening_balances(
            self,
            posting_date=posting_date or self.posting_date,
            submit=submit,
            force=force,
            balance_account=balance_account or None,
        )

    @frappe.whitelist()
    def execute_opening_stock(
        self,
        posting_date: str | None = None,
        submit=0,
        force=0,
        allow_difference=0,
        limit=None,
    ):
        self.check_permission("write")
        from dcnet_migrate.import_auto.services.opening_balance import (
            execute_opening_stock_reconciliation,
        )

        return execute_opening_stock_reconciliation(
            self,
            posting_date=posting_date or self.posting_date,
            submit=submit,
            force=force,
            allow_difference=allow_difference,
            limit=limit,
        )

    @frappe.whitelist()
    def execute_invoices(self, invoice_type: str, submit=0, force=0, limit=None):
        """Enqueue invoice import as a background job (queue="long").

        The invoice set can run to thousands of documents; running it inline in
        the web request exceeded the 120s proxy/gunicorn timeout (→ 504) and, on
        retry, overlapping runs contended on shared rows (Company defaults /
        Accounts) → "Lock wait timeout" + savepoint cascade. Backgrounding it (and
        letting the browser wait on a realtime completion event) removes the HTTP
        ceiling entirely. Mirrors `analyze_files` above.
        """
        self.check_permission("write")
        invoice_type = str(invoice_type).strip()

        # Document-level guard: only one invoice import per document at a time
        # (auto-expiring cache flag — shared across workers, and can never wedge
        # the feature the way a status field with no TTL would). The sequential
        # Sales-then-Purchase caller awaits each completion, so this never blocks
        # the normal flow — only genuine double-invocations.
        lock_key = f"ob_invoice_import_running::{self.name}"
        if frappe.cache().get_value(lock_key):
            frappe.throw(_("Đang import hóa đơn cho tài liệu này, vui lòng đợi lượt hiện tại hoàn tất."))
        frappe.cache().set_value(lock_key, frappe.session.user, expires_in_sec=3600)
        frappe.db.set_value(
            "Opening Balance Import",
            self.name,
            {"status": "Importing"},
            update_modified=False,
        )
        frappe.db.commit()

        job_id = f"import_auto::{self.name}::ob_invoices::{invoice_type}"
        try:
            frappe.enqueue(
                "dcnet_migrate.import_auto.doctype.opening_balance_import.opening_balance_import._run_invoice_import_background",
                queue="long",
                job_id=job_id,
                timeout=3600,
                deduplicate=True,
                enqueue_after_commit=True,
                now=frappe.flags.in_test,
                docname=self.name,
                invoice_type=invoice_type,
                submit=submit,
                force=force,
                limit=limit,
                lock_key=lock_key,
                triggered_by=frappe.session.user,
            )
        except Exception:
            frappe.cache().delete_value(lock_key)
            raise
        return {
            "enqueued": True,
            "job_id": job_id,
            "status": "Importing",
            "invoice_type": invoice_type,
            "realtime_event": "opening_invoice_import_complete",
        }

    @frappe.whitelist()
    def execute_ai_journal(self, posting_date: str | None = None, submit=0, force=0):
        self.check_permission("write")
        from dcnet_migrate.import_auto.services.opening_balance import execute_ai_journal_files

        return execute_ai_journal_files(
            self,
            posting_date=posting_date or self.posting_date,
            submit=submit,
            force=force,
        )

    @frappe.whitelist()
    def save_file_slot(self, migration_type: str, file_path: str):
        """Save an uploaded file path to a specific migration_type slot."""
        self.check_permission("write")
        from dcnet_migrate.import_auto.services.opening_balance import OPENING_FILES

        migration_type = frappe.utils.cstr(migration_type).strip()
        file_path = frappe.utils.cstr(file_path).strip()
        if migration_type not in OPENING_FILES:
            frappe.throw(_("Migration type không hợp lệ: {0}").format(migration_type))

        slots = {}
        if self.file_slots_json:
            try:
                slots = frappe.parse_json(self.file_slots_json) or {}
            except Exception:
                slots = {}
        if not isinstance(slots, dict):
            slots = {}

        slots[migration_type] = file_path
        frappe.db.set_value(
            "Opening Balance Import",
            self.name,
            {
                "file_slots_json": frappe.as_json(slots, indent=2),
                "analysis_json": None,
                "status": "Draft",
            },
            update_modified=True,
        )
        frappe.db.commit()
        return {"ok": True, "slots": slots}

    @frappe.whitelist()
    def clear_file_slot(self, migration_type: str):
        """Remove a file slot."""
        self.check_permission("write")
        migration_type = frappe.utils.cstr(migration_type).strip()

        slots = {}
        if self.file_slots_json:
            try:
                slots = frappe.parse_json(self.file_slots_json) or {}
            except Exception:
                slots = {}
        if not isinstance(slots, dict):
            slots = {}

        slots.pop(migration_type, None)
        frappe.db.set_value(
            "Opening Balance Import",
            self.name,
            {
                "file_slots_json": frappe.as_json(slots, indent=2) if slots else None,
                "analysis_json": None,
                "status": "Draft",
            },
            update_modified=True,
        )
        frappe.db.commit()
        return {"ok": True, "slots": slots}


def _run_analyze_background(docname: str, triggered_by: str | None = None):
    """Background job: run AI analysis and notify browser via realtime."""
    import traceback as _tb

    try:
        doc = frappe.get_doc("Opening Balance Import", docname)
        from dcnet_migrate.import_auto.services.opening_balance import analyze_opening_migration_files

        analyze_opening_migration_files(doc)

        if triggered_by:
            frappe.publish_realtime(
                "opening_analysis_complete",
                {"docname": docname, "status": "Analyzed", "ok": True},
                user=triggered_by,
            )
    except Exception:
        frappe.log_error(_tb.format_exc(), f"Opening Balance Analyze BG: {docname}")
        try:
            frappe.db.set_value("Opening Balance Import", docname, "status", "Failed")
            frappe.db.commit()
        except Exception:
            pass
        if triggered_by:
            frappe.publish_realtime(
                "opening_analysis_complete",
                {"docname": docname, "status": "Failed", "ok": False},
                user=triggered_by,
            )


def _publish_invoice_import_complete(docname, invoice_type, result, triggered_by):
    """Notify the browser that a background invoice import finished (or failed).

    The frontend keeps the progress dialog open and its `await` pending until this
    event arrives, so it MUST be published on every exit path (success and error).
    """
    if not triggered_by:
        return
    frappe.publish_realtime(
        "opening_invoice_import_complete",
        {
            "docname": docname,
            "invoice_type": invoice_type,
            "ok": bool(result.get("ok", True)),
            "result": result,
        },
        user=triggered_by,
    )


def _run_invoice_import_background(
    docname: str,
    invoice_type: str,
    submit=0,
    force=0,
    limit=None,
    lock_key: str | None = None,
    triggered_by: str | None = None,
):
    """Background job: run the (now batch-committing) invoice import and push a
    completion event. Always releases the concurrency lock in `finally`."""
    import traceback as _tb
    from dcnet_migrate.import_auto.services.opening_balance import execute_invoice_import

    if triggered_by:
        frappe.set_user(triggered_by)

    try:
        doc = frappe.get_doc("Opening Balance Import", docname)
        result = execute_invoice_import(
            doc, invoice_type=invoice_type, submit=submit, force=force, limit=limit
        )
        frappe.db.set_value(
            "Opening Balance Import", docname, {"status": "Completed"}, update_modified=False
        )
        frappe.db.commit()
        _publish_invoice_import_complete(docname, invoice_type, result, triggered_by)
    except Exception as exc:
        frappe.db.rollback()
        try:
            frappe.db.set_value(
                "Opening Balance Import", docname, {"status": "Failed"}, update_modified=False
            )
            frappe.db.commit()
        except Exception:
            pass
        frappe.log_error(_tb.format_exc(), f"Opening Balance Invoice Import BG: {docname}")
        # Surface the real reason (e.g. "Còn N khách hàng chưa có trong DB...") in
        # the dialog instead of a generic message or a silent hang.
        _publish_invoice_import_complete(
            docname,
            invoice_type,
            {"ok": False, "created": 0, "message": _("Import hóa đơn thất bại: {0}").format(str(exc)[:300])},
            triggered_by,
        )
        raise
    finally:
        if lock_key:
            frappe.cache().delete_value(lock_key)


def _get_doc(docname: str | None = None, permission_type: str = "write") -> OpeningBalanceImport:
    docname = docname or frappe.form_dict.get("docname") or frappe.form_dict.get("name")
    if not docname:
        frappe.throw(_("Opening Balance Import document is required."))
    doc = frappe.get_doc("Opening Balance Import", docname)
    doc.check_permission(permission_type)
    return doc


@frappe.whitelist()
def analyze_files(docname: str | None = None):
    doc = _get_doc(docname)
    return doc.analyze_files()


@frappe.whitelist(methods=["POST"])
def upload_excel_file(
    docname: str | None = None,
    migration_type: str | None = None,
    relative_path: str | None = None,
):
    """Upload an opening-balance workbook into a specific migration_type slot."""
    from pathlib import Path as _Path
    from dcnet_migrate.import_auto.services.opening_balance import OPENING_FILES
    from dcnet_migrate.import_auto.doctype.import_auto.import_auto import save_excel_upload

    doc = _get_doc(docname)
    migration_type = frappe.utils.cstr(migration_type or "").strip()
    if not migration_type or migration_type not in OPENING_FILES:
        frappe.throw(_("Vui lòng chỉ định migration_type hợp lệ khi upload file."))

    # Build relative path as {migration_type}/{original_filename} so each slot
    # gets its own sub-folder and name collisions between slots are impossible.
    uploaded_file = frappe.request.files.get("file")
    original_name = (uploaded_file.filename if uploaded_file else None) or ""
    slot_relative = f"{migration_type}/{original_name}" if original_name else None
    result = save_excel_upload(
        f"opening-balance-{doc.name}",
        relative_path=slot_relative,
    )
    file_path = str(_Path(result["folder_path"]) / result["relative_path"])

    doc.reload()
    doc.save_file_slot(migration_type=migration_type, file_path=file_path)
    result["migration_type"] = migration_type
    result["file_path"] = file_path
    return result


@frappe.whitelist()
def preview_migration(docname: str | None = None):
    doc = _get_doc(docname, permission_type="read")
    return doc.preview_migration()


@frappe.whitelist()
def create_missing_masters(docname: str | None = None):
    doc = _get_doc(docname)
    return doc.create_missing_masters()


@frappe.whitelist()
def execute_opening_journal(
    docname: str | None = None,
    posting_date: str | None = None,
    submit=0,
    force=0,
    balance_account: str | None = None,
):
    doc = _get_doc(docname)
    return doc.execute_opening_journal(posting_date=posting_date, submit=submit, force=force, balance_account=balance_account)


@frappe.whitelist()
def execute_opening_stock(
    docname: str | None = None,
    posting_date: str | None = None,
    submit=0,
    force=0,
    allow_difference=0,
    limit=None,
):
    doc = _get_doc(docname)
    return doc.execute_opening_stock(
        posting_date=posting_date,
        submit=submit,
        force=force,
        allow_difference=allow_difference,
        limit=limit,
    )


@frappe.whitelist()
def execute_invoices(
    docname: str | None = None,
    invoice_type: str | None = None,
    submit=0,
    force=0,
    limit=None,
):
    doc = _get_doc(docname)
    return doc.execute_invoices(invoice_type=invoice_type, submit=submit, force=force, limit=limit)


@frappe.whitelist()
def execute_ai_journal(
    docname: str | None = None,
    posting_date: str | None = None,
    submit=0,
    force=0,
):
    doc = _get_doc(docname)
    return doc.execute_ai_journal(posting_date=posting_date, submit=submit, force=force)


@frappe.whitelist()
def import_chart_of_accounts(docname: str | None = None, force: bool = False, clear: bool = False):
    from dcnet_migrate.import_auto.services.opening_balance import import_chart_of_accounts as _import_coa
    doc = _get_doc(docname)
    return _import_coa(doc, force=frappe.utils.cint(force), clear=frappe.utils.cint(clear))


@frappe.whitelist()
def save_file_slot(docname: str | None = None, migration_type: str | None = None, file_path: str | None = None):
    doc = _get_doc(docname)
    return doc.save_file_slot(migration_type=migration_type, file_path=file_path)


@frappe.whitelist()
def clear_file_slot(docname: str | None = None, migration_type: str | None = None):
    doc = _get_doc(docname)
    return doc.clear_file_slot(migration_type=migration_type)
