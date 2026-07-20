"""Duplicate detection for Import Auto.

After AI/heuristic analysis, scan the source records and compare them with
existing rows in the target DocType by exact identity fields only. If matches
are found we downgrade the row's ``safety_status`` from ``Safe`` to
``Warning`` so the user is alerted that importing will skip rows already in
the system.
"""

from __future__ import annotations

import json
import unicodedata

import frappe

from dcnet_migrate.import_auto.services.excel import extract_records
from dcnet_migrate.import_auto.services.utils import normalize_key


MATCH_RULES: dict[str, dict] = {
    "UOM": {"exact_fields": ["uom_name"]},
    "Item Group": {"exact_fields": ["item_group_name"]},
    "Bank": {"exact_fields": ["bank_name"]},
    "Warehouse": {"exact_fields": ["warehouse_name"]},
    "Customer": {"exact_fields": ["customer_name", "tax_id"]},
    "Supplier": {"exact_fields": ["supplier_name", "tax_id"]},
    "Item": {"exact_fields": ["item_code"]},
    "Bank Account": {"exact_fields": ["bank_account_no"]},
    "Department": {"exact_fields": ["department_name"]},
    "Branch": {"exact_fields": ["branch"]},
    "Project": {"exact_fields": ["project_name"]},
    "Account": {"exact_fields": ["account_number"]},
}

SAMPLE_LIMIT = 25
EXISTING_INDEX_LIMIT = 5000


def check_duplicates_for_row(doc, row) -> dict:
    """Return a duplicate-check report for one Import Auto File row."""
    if not row.analysis_json:
        return _empty_report("Chưa phân tích tệp này nên chưa thể đối chiếu dữ liệu.")

    try:
        analysis = json.loads(row.analysis_json)
    except Exception:
        return _empty_report("Không đọc được kết quả phân tích để đối chiếu.")

    target_doctype = analysis.get("target_doctype")
    if not target_doctype or not frappe.db.exists("DocType", target_doctype):
        return _empty_report("Không có DocType đích để đối chiếu trong cơ sở dữ liệu.")

    rule = MATCH_RULES.get(target_doctype)
    if not rule:
        return _empty_report(f"Chưa hỗ trợ đối chiếu trùng cho DocType '{target_doctype}'.")

    mappings = analysis.get("mappings") or []
    field_to_source = {
        mapping.get("target_field"): mapping.get("source_column")
        for mapping in mappings
        if mapping.get("target_field") and mapping.get("source_column")
    }

    exact_fields = [f for f in rule.get("exact_fields", []) if f in field_to_source]

    if not exact_fields:
        return _empty_report("Tệp này không có cột nào trùng với khóa nhận diện của DocType đích.")

    try:
        records = extract_records(
            row.file_path,
            analysis.get("sheet_name"),
            analysis.get("header_row_number"),
        )
    except Exception as exc:
        frappe.log_error(frappe.get_traceback(), "Import Auto Duplicate Read Failed")
        return _empty_report(f"Không đọc được tệp Excel để đối chiếu: {exc}")

    if not records:
        return _empty_report("Tệp không có dữ liệu để đối chiếu.")

    existing_index = _build_existing_index(target_doctype, exact_fields, getattr(doc, "company", None))
    matches: list[dict] = []
    exact_count = 0

    for record_index, record in enumerate(records, start=1):
        record_lookup = {normalize_key(key): key for key in record.keys()}
        per_field_values: dict = {}
        for field in set(exact_fields):
            source_column = field_to_source.get(field)
            if not source_column:
                continue
            actual_key = source_column if source_column in record else record_lookup.get(normalize_key(source_column))
            value = record.get(actual_key) if actual_key else None
            per_field_values[field] = value

        match = _find_match(per_field_values, exact_fields, existing_index)
        if not match:
            continue

        exact_count += 1

        if len(matches) < SAMPLE_LIMIT:
            matches.append(
                {
                    "row_number": record_index,
                    "match_type": match["match_type"],
                    "matched_field": match["field"],
                    "matched_value": match["value"],
                    "existing_name": match["existing_name"],
                    "existing_label": match["existing_label"],
                    "source_values": {
                        field: per_field_values.get(field)
                        for field in set(exact_fields)
                        if per_field_values.get(field) not in (None, "")
                    },
                }
            )

    total_matches = exact_count
    return {
        "target_doctype": target_doctype,
        "total_records": len(records),
        "exact_match_count": exact_count,
        "fuzzy_match_count": 0,
        "total_matches": total_matches,
        "sample_limit": SAMPLE_LIMIT,
        "existing_index_limit": EXISTING_INDEX_LIMIT,
        "samples": matches,
        "exact_fields": exact_fields,
        "fuzzy_fields": [],
        "checked_on": frappe.utils.now_datetime().isoformat(),
        "note": _summary_note(total_matches, exact_count, target_doctype),
    }


def determine_safety_status(current_status: str | None, report: dict | None) -> str | None:
    """Downgrade Safe -> Warning when duplicates are detected."""
    if not current_status or current_status != "Safe":
        return current_status
    if not report:
        return current_status
    if (report.get("total_matches") or 0) > 0:
        return "Warning"
    return current_status


def _empty_report(reason: str) -> dict:
    return {
        "target_doctype": None,
        "total_records": 0,
        "exact_match_count": 0,
        "fuzzy_match_count": 0,
        "total_matches": 0,
        "sample_limit": SAMPLE_LIMIT,
        "existing_index_limit": EXISTING_INDEX_LIMIT,
        "samples": [],
        "exact_fields": [],
        "fuzzy_fields": [],
        "checked_on": frappe.utils.now_datetime().isoformat(),
        "note": reason,
    }


def _summary_note(total: int, exact_count: int, target_doctype: str) -> str:
    if total == 0:
        return f"Không tìm thấy bản ghi {target_doctype} nào trùng trong cơ sở dữ liệu."
    parts = [f"Phát hiện {total} dòng trùng chính xác với {target_doctype} đã có."]
    if exact_count:
        parts.append(f"Trùng chính xác: {exact_count}.")
    parts.append("Khi import, các dòng này sẽ được bỏ qua và ghi lại trong báo cáo.")
    return " ".join(parts)


def _build_existing_index(doctype: str, fields: list[str], company: str | None = None) -> dict:
    fields = [f for f in dict.fromkeys(fields) if f]
    index: dict = {f: {"by_value": {}} for f in fields}

    if not fields:
        return index

    valid_fields = [f for f in fields if _field_exists(doctype, f)]
    if not valid_fields:
        return index

    label_field = _pick_label_field(valid_fields)
    select_fields = list({"name", label_field, *valid_fields})

    filters = {}
    if company and _field_exists(doctype, "company"):
        filters["company"] = company

    try:
        rows = frappe.get_all(
            doctype,
            fields=select_fields,
            filters=filters,
            limit_page_length=EXISTING_INDEX_LIMIT,
        )
    except Exception:
        frappe.log_error(frappe.get_traceback(), "Import Auto Duplicate Index Failed")
        return index

    if len(rows) == EXISTING_INDEX_LIMIT:
        frappe.log_error(
            f"Duplicate index for {doctype} hit the {EXISTING_INDEX_LIMIT}-record cap — some existing records may not be checked for duplicates.",
            "Import Auto Duplicate Index Truncated",
        )

    for row in rows:
        label = row.get(label_field) or row.get("name")
        for field in valid_fields:
            raw = row.get(field)
            if raw in (None, ""):
                continue
            key = _exact_match_key(raw)
            if not key:
                continue
            field_index = index[field]
            field_index["by_value"].setdefault(key, []).append(
                {"name": row["name"], "label": label, "value": raw}
            )

    return index


def _find_match(values, exact_fields, existing_index):
    for field in exact_fields:
        value = values.get(field)
        if value in (None, ""):
            continue
        key = _exact_match_key(value)
        if not key:
            continue
        bucket = existing_index.get(field, {}).get("by_value", {}).get(key)
        if bucket:
            existing = bucket[0]
            return {
                "match_type": "exact",
                "field": field,
                "value": value,
                "existing_name": existing["name"],
                "existing_label": existing["label"],
            }

    return None


def _exact_match_key(value) -> str:
    text = frappe.as_unicode(value or "").strip()
    if not text:
        return ""
    return unicodedata.normalize("NFC", text).casefold()


def _field_exists(doctype: str, fieldname: str) -> bool:
    if fieldname == "name":
        return True
    try:
        meta = frappe.get_meta(doctype)
    except Exception:
        return False
    return bool(meta.get_field(fieldname))


def _pick_label_field(fields: list[str]) -> str:
    for candidate in fields:
        if candidate.endswith("_name"):
            return candidate
    return fields[0] if fields else "name"
