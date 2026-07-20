"""Whitelisted APIs for the Excel Print Template Builder."""

from __future__ import annotations

import io
import json
import os
import re
import unicodedata
from typing import Any

import frappe
from frappe import _
from frappe.utils.file_manager import save_file

from vn_accounting.excel_printing.constants import (
    FIELD_GROUPS,
    MAX_COLUMNS,
    MAX_IMPORT_BYTES,
    MAX_ROWS,
    SUPPORTED_DOCTYPES,
)
from vn_accounting.excel_printing.engine import (
    evaluate_preview_formulas,
    load_xlsx,
    render_state,
    state_to_workbook,
    validate_state,
    workbook_to_state,
)
from vn_accounting.branch_cash.ai_invoice_parser import (
    _call_llm,
    _extract_message_content,
    _parse_json_payload,
    get_settings,
)


@frappe.whitelist(methods=["GET"])
def get_builder_bootstrap(template_name: str | None = None, document_type: str | None = None) -> dict:
    """Return templates, supported DocTypes, fields and optional workbook state."""
    frappe.has_permission("Excel Print Template", "read", throw=True)
    template = None
    if template_name:
        template = frappe.get_doc("Excel Print Template", template_name)
        template.check_permission("read")
        document_type = template.document_type

    if document_type:
        _validate_supported_doctype(document_type)

    templates = frappe.get_list(
        "Excel Print Template",
        fields=["name", "template_name", "document_type", "is_default", "disabled", "modified"],
        order_by="document_type asc, is_default desc, template_name asc",
        limit_page_length=500,
    )
    return {
        "supported_doctypes": list(SUPPORTED_DOCTYPES),
        "templates": templates,
        "fields": get_placeholder_fields(document_type) if document_type else [],
        "template": _template_payload(template) if template else None,
    }


@frappe.whitelist(methods=["GET"])
def get_placeholder_fields(document_type: str) -> list[dict[str, Any]]:
    """Return curated document and child-table fields for the builder sidebar."""
    _validate_supported_doctype(document_type)
    frappe.has_permission(document_type, "read", throw=True)
    meta = frappe.get_meta(document_type)
    fields = []
    curated = set(FIELD_GROUPS["document"] + FIELD_GROUPS["totals"])

    for field in meta.fields:
        if field.fieldtype in {"Section Break", "Column Break", "Tab Break", "HTML", "Button", "Table MultiSelect"}:
            continue
        if field.fieldtype == "Table" and field.options:
            fields.extend(_child_placeholder_fields(field.fieldname, field.label, field.options))
        elif field.fieldname in curated or field.in_standard_filter or field.reqd:
            fields.append(
                {
                    "key": field.fieldname,
                    "token": "{{" + field.fieldname + "}}",
                    "label": field.label or field.fieldname,
                    "group": _("Thông tin chứng từ"),
                    "fieldtype": field.fieldtype,
                }
            )

    existing = {item["key"] for item in fields}
    for fieldname in ("name", "owner", "creation", "modified"):
        if fieldname not in existing:
            fields.insert(
                0,
                {
                    "key": fieldname,
                    "token": "{{" + fieldname + "}}",
                    "label": frappe.unscrub(fieldname),
                    "group": _("Thông tin chứng từ"),
                    "fieldtype": "Data",
                },
            )
    return fields


@frappe.whitelist(methods=["POST"])
def import_excel_template(file_url: str, document_type: str, mapping_mode: str = "manual") -> dict:
    """Read an attached XLSX file and return canonical workbook state."""
    frappe.has_permission("Excel Print Template", "create", throw=True)
    _validate_supported_doctype(document_type)
    file_doc = frappe.get_doc("File", {"file_url": file_url})
    file_doc.check_permission("read")
    path = file_doc.get_full_path()
    extension = os.path.splitext(path)[1].lower()
    if extension not in {".xlsx", ".xlsm"}:
        frappe.throw(_("Chỉ hỗ trợ file .xlsx hoặc .xlsm."))
    if os.path.getsize(path) > MAX_IMPORT_BYTES:
        frappe.throw(_("File Excel vượt quá giới hạn 20 MB."))

    try:
        state = workbook_to_state(load_xlsx(path))
    except Exception:
        frappe.log_error(frappe.get_traceback(), "Excel Print Template Import")
        frappe.throw(_("Không đọc được file Excel. Hãy kiểm tra file không bị hỏng hoặc đặt mật khẩu."))

    mapped_count = 0
    mapping_method = "manual"
    if mapping_mode in {"auto", "ai"}:
        fields = get_placeholder_fields(document_type)
        state, mapped_count, mapping_method = _map_imported_state(state, fields, document_type)
    return {"workbook_state": state, "mapped_count": mapped_count, "mapping_method": mapping_method}


@frappe.whitelist(methods=["POST"])
def save_template(
    template_name: str,
    document_type: str,
    workbook_state: str | dict,
    name: str | None = None,
    source_file: str | None = None,
    is_default: int = 0,
) -> dict:
    """Create or update an Excel print template from canonical workbook state."""
    _validate_supported_doctype(document_type)
    state = validate_state(workbook_state)
    if name:
        doc = frappe.get_doc("Excel Print Template", name)
        doc.check_permission("write")
    else:
        frappe.has_permission("Excel Print Template", "create", throw=True)
        doc = frappe.new_doc("Excel Print Template")

    doc.template_name = (template_name or "").strip()
    doc.document_type = document_type
    doc.workbook_state = json.dumps(state, ensure_ascii=False, separators=(",", ":"))
    doc.source_file = source_file or doc.source_file
    doc.is_default = int(is_default or 0)
    doc.disabled = 0
    doc.save()
    return {"name": doc.name, "template_name": doc.template_name, "document_type": doc.document_type}


@frappe.whitelist(methods=["GET"])
def get_templates_for_document(document_type: str) -> dict:
    """Return enabled templates and management permissions for a document form."""
    _validate_supported_doctype(document_type)
    frappe.has_permission(document_type, "read", throw=True)
    if not frappe.has_permission("Excel Print Template", "read"):
        return {"templates": [], "can_manage": False}
    return {
        "templates": frappe.get_list(
            "Excel Print Template",
            filters={"document_type": document_type, "disabled": 0},
            fields=["name", "template_name", "is_default", "source_file", "modified"],
            order_by="is_default desc, template_name asc",
            limit_page_length=100,
        ),
        "can_manage": bool(frappe.has_permission("Excel Print Template", "create")),
    }


@frappe.whitelist(methods=["POST"])
def delete_excel_template(template_name: str) -> None:
    """Delete a saved Excel template after an explicit client confirmation."""
    if not template_name:
        frappe.throw(_("Thiếu tên mẫu in Excel."))
    template = frappe.get_doc("Excel Print Template", template_name)
    template.check_permission("delete")
    template.delete()


@frappe.whitelist(methods=["POST"])
def preview_excel_template_grid(
    template_name: str | None = None,
    workbook_state: str | dict | None = None,
    document_type: str | None = None,
    document_name: str | None = None,
) -> dict:
    """Return a filled, style-preserving workbook grid for print preview."""
    state, document_type = _resolve_state(template_name, workbook_state, document_type)
    document = _get_preview_document(document_type, document_name)
    rendered = render_state(state, document)
    rendered = evaluate_preview_formulas(rendered)
    return {"workbook_state": rendered, "document_type": document_type, "document_name": document_name}


@frappe.whitelist(methods=["POST"])
def export_excel_document(template_name: str, document_type: str, document_name: str) -> dict:
    """Fill a saved template from a document and attach the generated XLSX privately."""
    _validate_supported_doctype(document_type)
    template = frappe.get_doc("Excel Print Template", template_name)
    template.check_permission("read")
    if template.document_type != document_type:
        frappe.throw(_("Mẫu in không thuộc loại chứng từ này."))
    document = frappe.get_doc(document_type, document_name)
    document.check_permission("read")

    rendered = render_state(template.workbook_state, document)
    workbook = state_to_workbook(rendered)
    output = io.BytesIO()
    workbook.save(output)
    filename = f"{frappe.scrub(template.template_name).replace('_', '-')}-{frappe.scrub(document_name)}.xlsx"
    file_doc = save_file(filename, output.getvalue(), document_type, document_name, is_private=1)
    return {"file_url": file_doc.file_url, "file_name": filename}


def _resolve_state(template_name, workbook_state, document_type):
    if template_name:
        template = frappe.get_doc("Excel Print Template", template_name)
        template.check_permission("read")
        return validate_state(template.workbook_state), template.document_type
    if not workbook_state or not document_type:
        frappe.throw(_("Thiếu mẫu hoặc dữ liệu workbook để xem trước."))
    _validate_supported_doctype(document_type)
    frappe.has_permission("Excel Print Template", "create", throw=True)
    return validate_state(workbook_state), document_type


def _get_preview_document(document_type: str, document_name: str | None):
    if document_name:
        document = frappe.get_doc(document_type, document_name)
        document.check_permission("read")
        return document
    frappe.has_permission(document_type, "read", throw=True)
    return _sample_document(document_type)


def _sample_document(document_type: str) -> dict[str, Any]:
    meta = frappe.get_meta(document_type)
    sample = {"doctype": document_type, "name": f"{frappe.scrub(document_type).upper()}-MẪU-0001"}
    for field in meta.fields:
        if field.fieldtype == "Table" and field.options:
            child_meta = frappe.get_meta(field.options)
            sample[field.fieldname] = [
                {item.fieldname: _sample_value(item) for item in child_meta.fields if item.fieldtype not in {"Section Break", "Column Break", "Button", "HTML"}},
                {item.fieldname: _sample_value(item, 2) for item in child_meta.fields if item.fieldtype not in {"Section Break", "Column Break", "Button", "HTML"}},
            ]
        elif field.fieldtype not in {"Section Break", "Column Break", "Button", "HTML", "Table"}:
            sample[field.fieldname] = _sample_value(field)
    return sample


def _sample_value(field, index: int = 1):
    if field.fieldtype in {"Currency", "Float"}:
        return 1250000 * index
    if field.fieldtype in {"Int", "Check"}:
        return index
    if field.fieldtype == "Date":
        return "2026-07-14"
    if field.fieldtype == "Datetime":
        return "2026-07-14 09:00:00"
    if field.fieldname in {"qty", "stock_qty", "required_qty"}:
        return index
    if field.fieldname in {"item_code"}:
        return f"SP-{index:03d}"
    if field.fieldname in {"item_name", "description"}:
        return f"Sản phẩm mẫu {index}"
    return field.label or frappe.unscrub(field.fieldname)


def _child_placeholder_fields(table_field: str, table_label: str, child_doctype: str) -> list[dict]:
    child_meta = frappe.get_meta(child_doctype)
    preferred = set(
        FIELD_GROUPS["items"] + FIELD_GROUPS["accounting_rows"] + FIELD_GROUPS["payment_references"]
        + FIELD_GROUPS["expense_rows"] + FIELD_GROUPS["manufacturing_rows"]
    )
    result = []
    for field in child_meta.fields:
        if field.fieldtype in {"Section Break", "Column Break", "Tab Break", "HTML", "Button", "Table"}:
            continue
        if field.fieldname not in preferred and not field.reqd and not field.in_list_view:
            continue
        result.append(
            {
                "key": f"{table_field}.{field.fieldname}",
                "token": "{{" + table_field + "." + field.fieldname + "}}",
                "label": field.label or field.fieldname,
                "group": table_label or table_field,
                "fieldtype": field.fieldtype,
                "table_field": table_field,
            }
        )
    return result


def _auto_map_state(state: dict, fields: list[dict]) -> tuple[dict, int]:
    aliases = {}
    for field in fields:
        for label in {field["label"], field["key"].split(".")[-1], frappe.unscrub(field["key"].split(".")[-1])}:
            aliases[_normalize_label(label)] = field

    mapped = 0
    for sheet in state.get("sheets", []):
        cells = sheet.get("cells", {})
        for coordinate, cell in list(cells.items()):
            value = cell.get("value")
            if not isinstance(value, str) or "{{" in value:
                continue
            normalized = _normalize_label(value.rstrip(":.- "))
            field = aliases.get(normalized)
            if not field:
                continue
            match = re.fullmatch(r"([A-Z]+)(\d+)", coordinate)
            if not match:
                continue
            column, row = match.groups()
            target = _next_coordinate(column, int(row), field.get("table_field") is not None)
            target_match = re.fullmatch(r"([A-Z]+)(\d+)", target)
            if not target_match or _column_number(target_match.group(1)) > MAX_COLUMNS or int(target_match.group(2)) > MAX_ROWS:
                continue
            target_cell = cells.setdefault(target, {"value": None, "data_type": "n", "style": cell.get("style", {})})
            if target_cell.get("value") in (None, "", "_", "...") or re.fullmatch(r"[.\s_\-]+", str(target_cell.get("value") or "")):
                target_cell["value"] = field["token"]
                target_cell["data_type"] = "s"
                mapped += 1
                if target_match:
                    sheet["max_row"] = max(sheet.get("max_row", 1), int(target_match.group(2)))
    return state, mapped


def _map_imported_state(state: dict, fields: list[dict], document_type: str) -> tuple[dict, int, str]:
    """Use configured AI when available, with a deterministic label mapper fallback."""
    try:
        settings = get_settings()
        configured = all(settings.get(key) for key in ("enabled", "base_url", "model", "api_key"))
        if configured:
            mapped_state, mapped_count = _ai_map_state(state, fields, document_type, settings)
            if mapped_count:
                return mapped_state, mapped_count, "ai"
    except Exception:
        frappe.log_error(frappe.get_traceback(), "Excel Template AI Mapping Fallback")

    mapped_state, mapped_count = _auto_map_state(state, fields)
    return mapped_state, mapped_count, "heuristic" if mapped_count else "manual"


def _ai_map_state(state: dict, fields: list[dict], document_type: str, settings: dict) -> tuple[dict, int]:
    allowed_fields = {field["key"]: field for field in fields}
    visible_cells = []
    for sheet_index, sheet in enumerate(state.get("sheets", [])):
        if len(visible_cells) >= 800:
            break
        for coordinate, cell in sheet.get("cells", {}).items():
            value = cell.get("value")
            if isinstance(value, str) and value.strip() and "{{" not in value:
                visible_cells.append({"sheet": sheet_index, "cell": coordinate, "value": value[:180]})
            if len(visible_cells) >= 800:
                break

    prompt = {
        "document_type": document_type,
        "instruction": (
            "Map labels/headers to fields. Return JSON only: "
            '{"mappings":[{"sheet":0,"cell":"B2","field":"posting_date"}]}. '
            "cell is the blank/dotted value cell to receive the placeholder. "
            "For table fields, select exactly one template row. Never invent fields or coordinates."
        ),
        "allowed_fields": [{"key": item["key"], "label": item["label"]} for item in fields],
        "visible_cells": visible_cells,
    }
    payload = {
        "model": settings["model"],
        "stream": False,
        "temperature": 0,
        "messages": [
            {"role": "system", "content": "You map Vietnamese Excel voucher templates to an allowed field list. Return only valid JSON."},
            {"role": "user", "content": json.dumps(prompt, ensure_ascii=False)},
        ],
    }
    response = _call_llm(settings, payload)
    data = _parse_json_payload(_extract_message_content(response))
    mapped = 0
    table_rows: dict[tuple[int, str], int] = {}
    for mapping in data.get("mappings", []):
        if not isinstance(mapping, dict):
            continue
        field = allowed_fields.get(str(mapping.get("field") or ""))
        coordinate = str(mapping.get("cell") or "").upper().replace("$", "")
        sheet_index = mapping.get("sheet", 0)
        if not field or not isinstance(sheet_index, int) or not 0 <= sheet_index < len(state["sheets"]):
            continue
        if not re.fullmatch(r"[A-Z]{1,3}[1-9]\d*", coordinate):
            continue
        match = re.fullmatch(r"([A-Z]+)(\d+)", coordinate)
        if not match or int(match.group(2)) > MAX_ROWS or _column_number(match.group(1)) > MAX_COLUMNS:
            continue
        sheet = state["sheets"][sheet_index]
        cell = sheet.setdefault("cells", {}).setdefault(coordinate, {"value": None, "data_type": "n", "style": {}})
        current = str(cell.get("value") or "")
        if current.strip() and not re.fullmatch(r"[.\s_\-:]*", current):
            continue
        cell["value"] = field["token"]
        cell["data_type"] = "s"
        cell["style"] = cell.get("style") or {}
        sheet["max_row"] = max(int(sheet.get("max_row") or 1), int(match.group(2)))
        sheet["max_column"] = max(int(sheet.get("max_column") or 1), _column_number(match.group(1)))
        if field.get("table_field"):
            table_rows[(sheet_index, field["table_field"])] = int(match.group(2))
        mapped += 1

    _remove_repeated_sample_rows(state, table_rows)
    return state, mapped


def _remove_repeated_sample_rows(state: dict, table_rows: dict[tuple[int, str], int]) -> None:
    """Clear repeated sample lines immediately below an AI-selected child template row."""
    for (sheet_index, table_field), template_row in table_rows.items():
        sheet = state["sheets"][sheet_index]
        for row in range(template_row + 1, min(template_row + 20, int(sheet.get("max_row") or 1)) + 1):
            row_cells = [
                (coordinate, cell)
                for coordinate, cell in sheet.get("cells", {}).items()
                if coordinate.endswith(str(row)) and re.fullmatch(r"[A-Z]+" + str(row), coordinate)
            ]
            if not row_cells:
                break
            values = [str(cell.get("value") or "") for _, cell in row_cells]
            normalized_values = " ".join(_normalize_label(value) for value in values)
            if any(keyword in normalized_values for keyword in ("tong cong", "cong tien", "thue", "nguoi lap", "nguoi ky", "ky ten")):
                break
            if any("{{" in value and not value.startswith("{{" + table_field + ".") for value in values):
                break
            if any(value.startswith("=") for value in values):
                break
            non_empty = [value for value in values if value.strip()]
            if len(non_empty) < 2 or not any(re.search(r"\d", value) for value in non_empty):
                break
            for _, cell in row_cells:
                if cell.get("value") not in (None, ""):
                    cell["value"] = ""
                    cell["data_type"] = "s"


def _column_number(name: str) -> int:
    result = 0
    for character in name:
        result = result * 26 + ord(character) - 64
    return result


def _next_coordinate(column: str, row: int, table_field: bool) -> str:
    from openpyxl.utils.cell import column_index_from_string, get_column_letter

    if table_field:
        return f"{column}{row + 1}"
    return f"{get_column_letter(column_index_from_string(column) + 1)}{row}"


def _normalize_label(value: str) -> str:
    value = unicodedata.normalize("NFD", value or "")
    value = "".join(character for character in value if unicodedata.category(character) != "Mn")
    return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()


def _validate_supported_doctype(document_type: str) -> None:
    if document_type not in SUPPORTED_DOCTYPES:
        frappe.throw(_("Loại chứng từ {0} chưa được hỗ trợ cho mẫu in Excel.").format(document_type))


def _template_payload(template) -> dict | None:
    if not template:
        return None
    return {
        "name": template.name,
        "template_name": template.template_name,
        "document_type": template.document_type,
        "source_file": template.source_file,
        "is_default": template.is_default,
        "disabled": template.disabled,
        "workbook_state": validate_state(template.workbook_state),
    }
