import csv
import io
import json
from pathlib import Path

import frappe
from frappe import _
from frappe.core.doctype.data_import.importer import Importer
from frappe.utils.file_manager import save_file

from dcnet_migrate.import_auto.services.doctype_metadata import (
    DEPARTMENT_BRANCH_SHEETS,
    resolve_branch_by_label,
)
from dcnet_migrate.import_auto.services.excel import extract_records
from dcnet_migrate.import_auto.services.utils import normalize_key


def prepare_data_import(docname: str, file_row_name: str) -> dict:
    doc, row = _get_doc_and_row(docname, file_row_name)
    _validate_row_for_import(row)

    if row.data_import and frappe.db.exists("Data Import", row.data_import):
        return _preview_response(doc, row, warning_count=0)

    analysis = json.loads(row.analysis_json or "{}")
    target_doctype = analysis.get("target_doctype")
    _apply_department_branch_link(analysis, row.sheet_name, doc.company)
    records = extract_records(row.file_path, analysis.get("sheet_name"), analysis.get("header_row_number"))
    rows = _transform_records(records, analysis)
    if not rows:
        frappe.throw(_("No importable rows found for this file."))

    data_import = frappe.new_doc("Data Import")
    data_import.reference_doctype = target_doctype
    data_import.import_type = "Insert New Records"
    data_import.submit_after_import = False
    data_import.mute_emails = True
    data_import.insert(ignore_permissions=True)

    file_doc = save_file(
        _generated_filename(doc.name, row.file_name, target_doctype),
        _build_csv(rows).encode("utf-8-sig"),
        "Data Import",
        data_import.name,
        is_private=1,
    )
    data_import.import_file = file_doc.file_url
    data_import.save(ignore_permissions=True)

    importer = Importer(doctype=target_doctype, data_import=data_import)
    data_import.set_payload_count(importer)
    data_import.save(ignore_permissions=True)
    preview = importer.get_data_for_import_preview()
    warnings = getattr(preview, "warnings", []) or []
    if warnings:
        data_import.db_set("template_warnings", frappe.as_json(warnings))

    row.data_import = data_import.name
    row.generated_file = file_doc.name
    row.status = "Data Import Created"
    row.row_count = len(rows)
    doc.save(ignore_permissions=True)
    frappe.db.commit()

    return _preview_response(doc, row, warning_count=len(warnings))


def confirm_data_import(docname: str, file_row_name: str) -> dict:
    doc, row = _get_doc_and_row(docname, file_row_name)
    _validate_row_for_import(row)

    if not row.data_import or not frappe.db.exists("Data Import", row.data_import):
        prepare_data_import(docname, file_row_name)
        doc, row = _get_doc_and_row(docname, file_row_name)

    data_import = frappe.get_doc("Data Import", row.data_import)
    importer = Importer(doctype=data_import.reference_doctype, data_import=data_import)
    importer.import_data()
    data_import.reload()
    counts = _get_import_counts(data_import.name)
    warnings = frappe.parse_json(data_import.template_warnings or "[]")

    if warnings:
        pending_count = max(int(data_import.payload_count or row.row_count or 0) - counts["imported_records"], 0)
        counts["failed_records"] = max(counts["failed_records"], pending_count)
        data_import.db_set("status", "Error")

    row.imported_records = counts["imported_records"]
    row.failed_records = counts["failed_records"]
    row.imported_on = frappe.utils.now_datetime()
    if warnings:
        row.status = "Partial" if counts["imported_records"] else "Failed"
        row.error_detail = _("Data Import still has warnings. Open the Data Import document to review details.")
    else:
        row.status = "Partial" if counts["failed_records"] else "Imported"
        row.error_detail = None if not counts["failed_records"] else _("Some rows failed. Open Data Import for details.")

    _update_parent_status(doc)
    doc.save(ignore_permissions=True)
    frappe.db.commit()

    return {
        "data_import": data_import.name,
        "imported_records": counts["imported_records"],
        "failed_records": counts["failed_records"],
        "status": row.status,
    }


def _get_doc_and_row(docname: str, file_row_name: str):
    doc = frappe.get_doc("Import Auto", docname)
    doc.check_permission("write")
    for row in doc.files:
        if row.name == file_row_name:
            return doc, row
    frappe.throw(_("File row not found."))


def _validate_row_for_import(row):
    if row.status == "Imported":
        frappe.throw(_("This file has already been imported."))
    if row.safety_status not in ("Safe", "Warning"):
        frappe.throw(_("This file is not safe to import: {0}").format(row.error_detail or row.analysis_note or ""))
    if not row.analysis_json:
        frappe.throw(_("Analyze this file before importing."))


def _apply_department_branch_link(analysis: dict, sheet_name: str | None, company: str | None) -> None:
    """Re-resolve Department.branch for a per-branch department sheet at
    prepare time (not analyze time).

    get_default_values() already tries this lookup during Analyze, but
    Analyze runs over every sheet in one pass BEFORE any of them are
    imported — the "Chi nhánh" branch-master sheet's Branches don't exist
    yet, so the cached analysis_json.defaults never has a `branch` for the
    per-branch sheets. Re-resolve here, right before the CSV is built, by
    which point the operator should have already imported the "Chi nhánh"
    sheet.
    """
    if analysis.get("target_doctype") != "Department" or sheet_name not in DEPARTMENT_BRANCH_SHEETS:
        return
    branch_label = DEPARTMENT_BRANCH_SHEETS[sheet_name]
    branch = resolve_branch_by_label(branch_label, company)
    if not branch:
        frappe.throw(
            _(
                "Chưa import Chi nhánh '{0}' — hãy Import sheet 'Chi nhánh' trước khi import sheet '{1}'."
            ).format(branch_label, sheet_name)
        )
    analysis["defaults"] = {**(analysis.get("defaults") or {}), "branch": branch}


def _transform_records(records: list[dict], analysis: dict) -> list[dict]:
    mappings = analysis.get("mappings") or []
    defaults = analysis.get("defaults") or {}
    rows = []
    for source in records:
        source_lookup = {normalize_key(key): key for key in source}
        row = {}
        for mapping in mappings:
            source_column = mapping.get("source_column")
            target_field = mapping.get("target_field")
            if not source_column or not target_field:
                continue
            actual_source = source_column if source_column in source else source_lookup.get(normalize_key(source_column))
            value = source.get(actual_source) if actual_source else None
            fallback_column = mapping.get("fallback_column")
            if value in (None, "") and fallback_column:
                actual_fallback = (
                    fallback_column if fallback_column in source
                    else source_lookup.get(normalize_key(fallback_column))
                )
                fallback_value = source.get(actual_fallback) if actual_fallback else None
                if fallback_value not in (None, ""):
                    value = fallback_value
            if value in (None, "") and mapping.get("default") not in (None, ""):
                value = mapping.get("default")
            row[target_field] = value

        for fieldname, value in defaults.items():
            if row.get(fieldname) in (None, ""):
                row[fieldname] = value

        if any(value not in (None, "") for value in row.values()):
            rows.append(row)
    return rows


def _build_csv(rows: list[dict]) -> str:
    fieldnames = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)

    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=fieldnames, extrasaction="ignore")
    writer.writeheader()
    for row in rows:
        writer.writerow(row)
    return buffer.getvalue()


def _preview_response(doc, row, warning_count: int) -> dict:
    return {
        "file_name": row.file_name,
        "target_doctype": row.target_doctype,
        "row_count": row.row_count,
        "data_import": row.data_import,
        "warning_count": warning_count,
        "status": row.status,
    }


def _generated_filename(docname: str, file_name: str, target_doctype: str) -> str:
    stem = Path(file_name).stem.replace(" ", "_")
    doctype = target_doctype.replace(" ", "_")
    return f"{docname}-{doctype}-{stem}.csv"


def _get_import_counts(data_import_name: str) -> dict:
    base_filters = {"data_import": data_import_name}
    imported = frappe.db.count("Data Import Log", {**base_filters, "success": 1})
    failed = frappe.db.count("Data Import Log", {**base_filters, "success": 0})
    return {"imported_records": imported, "failed_records": failed}


def _update_parent_status(doc):
    statuses = [row.status for row in doc.files]
    total = len(statuses)
    imported_count = sum(1 for status in statuses if status == "Imported")
    partial_count = sum(1 for status in statuses if status == "Partial")
    failed_count = sum(1 for status in statuses if status == "Failed")
    error_count = sum(1 for status in statuses if status == "Error")
    finished_count = imported_count + partial_count + failed_count

    if total and imported_count == total:
        doc.status = "Completed"
        doc.progress_message = f"Imported {imported_count}/{total} Excel file(s)."
        doc.progress_percent = 100
    elif imported_count or partial_count:
        doc.status = "Partial"
        doc.progress_message = f"Imported {imported_count}/{total} Excel file(s)."
    elif failed_count and failed_count + error_count == total:
        doc.status = "Failed"
        doc.progress_message = f"Import failed for {failed_count}/{total} Excel file(s)."
    elif statuses:
        doc.status = "Analyzed"

    doc.excel_file_count = total
    doc.total_files = total
    doc.processed_files = finished_count

    summary = {}
    if doc.summary_json:
        try:
            summary = frappe.parse_json(doc.summary_json)
        except Exception:
            summary = {}
    if not isinstance(summary, dict):
        summary = {}
    summary.update(
        {
            "total_files": total,
            "imported_files": imported_count,
            "partial_files": partial_count,
            "failed_files": failed_count,
            "error_files": error_count,
            "ready_files": sum(1 for status in statuses if status == "Ready"),
        }
    )
    doc.summary_json = json.dumps(summary, ensure_ascii=False, indent=2, default=str)
