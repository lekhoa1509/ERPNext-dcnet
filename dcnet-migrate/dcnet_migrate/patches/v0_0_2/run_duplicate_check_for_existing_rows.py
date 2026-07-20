"""Backfill duplicate-check report on existing Import Auto File rows.

After upgrading to the duplicate-aware Import Auto, walk every analyzed row
that is currently flagged as ``Safe`` and re-run the duplicate checker so the
UI can immediately show ``Warning`` rows instead of waiting for the next
``Analyze`` action.
"""

from __future__ import annotations

import json

import frappe


def execute() -> None:
    if not frappe.db.exists("DocType", "Import Auto File"):
        return

    rows = frappe.get_all(
        "Import Auto File",
        filters={"safety_status": ["in", ["Safe", "Warning"]]},
        fields=["name", "parent"],
    )
    if not rows:
        return

    from dcnet_migrate.import_auto.services.duplicate_checker import (
        check_duplicates_for_row,
        determine_safety_status,
    )

    for row_meta in rows:
        try:
            doc = frappe.get_doc("Import Auto", row_meta.parent)
            row = next((r for r in doc.files if r.name == row_meta.name), None)
            if not row or not row.analysis_json:
                continue

            report = check_duplicates_for_row(doc, row)
            new_safety = determine_safety_status(row.safety_status, report)
            updates = {
                "duplicate_report_json": json.dumps(report, ensure_ascii=False, indent=2, default=str),
                "duplicate_match_count": report.get("total_matches") or 0,
                "duplicate_check_status": "Warning" if (report.get("total_matches") or 0) > 0 else "Clean",
            }
            if row.safety_status in ("Safe", "Warning") and new_safety in ("Safe", "Warning"):
                updates["safety_status"] = new_safety
                if new_safety == "Warning":
                    warning_note = report.get("note") or "Phát hiện dữ liệu có khả năng trùng trong cơ sở dữ liệu."
                    updates["error_detail"] = warning_note
                elif row.safety_status == "Warning":
                    updates["error_detail"] = None
            frappe.db.set_value("Import Auto File", row.name, updates, update_modified=False)
        except Exception:
            frappe.log_error(frappe.get_traceback(), "Import Auto Backfill Duplicate Failed")

    frappe.db.commit()
