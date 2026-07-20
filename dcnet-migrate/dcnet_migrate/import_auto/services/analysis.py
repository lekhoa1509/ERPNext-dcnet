import json

import frappe

from dcnet_migrate.import_auto.services.ai_client import analyze_with_ai
from dcnet_migrate.import_auto.services.doctype_metadata import (
    field_exists,
    get_default_values,
    get_direct_mappings,
    get_doctype_schema,
    infer_import_file,
    missing_required_context,
)


def analyze_file(doc, summary: dict, user_feedback: str | None = None) -> dict:
    hint = infer_import_file(summary.get("file_name", ""), first_sheet(summary).get("sheet_name"))
    target_doctype = hint.get("target_doctype")
    schema = get_doctype_schema(target_doctype) if target_doctype and frappe.db.exists("DocType", target_doctype) else None
    feedback = (user_feedback or "").strip()
    local_result = heuristic_analysis(doc, summary, hint)

    if not feedback:
        if _is_fast_local_result(local_result, hint):
            return local_result
        if hint.get("known_file_type") and not hint.get("is_supported"):
            return local_result

    ai_result = None
    ai_failed = False
    try:
        ai_result = analyze_with_ai(doc, summary, hint, schema, user_feedback=feedback)
    except Exception:
        frappe.log_error(frappe.get_traceback(), "Import Auto Analysis Error")
        ai_failed = True

    if ai_result:
        return sanitize_analysis(ai_result, doc, summary, hint)

    if ai_failed:
        ai_note = "AI gặp lỗi khi phân tích — đang dùng kết quả heuristic thay thế."
        existing_note = local_result.get("reason") or ""
        local_result["reason"] = f"{existing_note}\n{ai_note}".strip() if existing_note else ai_note

    return local_result


def _is_fast_local_result(result: dict, hint: dict) -> bool:
    """Use deterministic mappings when they are already strong enough.

    Batch analysis may cover dozens of files. Avoiding an AI call for known
    master-data files keeps the UI responsive while still leaving the AI
    resolution button available for unknown or failed files.
    """
    return bool(
        hint.get("is_supported")
        and result.get("source") == "heuristic"
        and result.get("safety_status") == "Safe"
        and result.get("target_doctype")
        and result.get("mappings")
        and float(result.get("confidence") or 0) >= 60
    )


def sanitize_analysis(ai_result: dict, doc, summary: dict, hint: dict) -> dict:
    target_doctype = ai_result.get("target_doctype") or hint.get("target_doctype")
    safety_status = ai_result.get("safety_status") or ("Safe" if hint.get("is_supported") else "Error")

    if not target_doctype or not frappe.db.exists("DocType", target_doctype):
        return error_analysis(summary, hint, ai_result.get("reason") or hint.get("note"))

    context_error = missing_required_context(target_doctype, doc.company)
    if context_error:
        return error_analysis(summary, hint, context_error, target_doctype=target_doctype)

    mappings = []
    for mapping in ai_result.get("mappings") or []:
        source_column = mapping.get("source_column")
        target_field = mapping.get("target_field")
        if not source_column or not target_field or not field_exists(target_doctype, target_field):
            continue
        mappings.append(
            {
                "source_column": source_column,
                "target_field": target_field,
                "default": mapping.get("default"),
                "transform": mapping.get("transform") or "direct",
            }
        )

    if safety_status == "Safe" and not mappings:
        return error_analysis(summary, hint, "AI không trả về mapping field hợp lệ.", target_doctype=target_doctype)

    resolved_sheet_name = ai_result.get("sheet_name") or first_sheet(summary).get("sheet_name")
    defaults = get_default_values(target_doctype, doc.company, resolved_sheet_name)
    for key, value in (ai_result.get("defaults") or {}).items():
        if value not in (None, "") and field_exists(target_doctype, key):
            defaults[key] = value

    return {
        "source": "ai",
        "safety_status": "Safe" if safety_status == "Safe" else "Error",
        "target_doctype": target_doctype,
        "import_order": int(ai_result.get("import_order") or hint.get("import_order") or 999),
        "confidence": float(ai_result.get("confidence") or 0),
        "sheet_name": resolved_sheet_name,
        "header_row_number": int(ai_result.get("header_row_number") or first_sheet(summary).get("detected_header_row") or 1),
        "mappings": mappings,
        "defaults": defaults,
        "reason": ai_result.get("reason") or hint.get("note"),
        "raw_ai_response": ai_result,
    }


def heuristic_analysis(doc, summary: dict, hint: dict) -> dict:
    target_doctype = hint.get("target_doctype")
    if not hint.get("is_supported") or not target_doctype:
        return error_analysis(summary, hint, hint.get("note"))

    if not frappe.db.exists("DocType", target_doctype):
        return error_analysis(summary, hint, f"ERPNext không có DocType {target_doctype}.")

    context_error = missing_required_context(target_doctype, doc.company)
    if context_error:
        return error_analysis(summary, hint, context_error, target_doctype=target_doctype)

    sheet = first_sheet(summary)
    mappings = get_direct_mappings(target_doctype, sheet.get("detected_headers") or [])
    if not mappings:
        return error_analysis(
            summary,
            hint,
            "Chưa có AI key hoặc AI lỗi, và hệ thống không tìm được mapping cột nguồn an toàn.",
            target_doctype=target_doctype,
        )

    total_headers = len([h for h in (sheet.get("detected_headers") or []) if h and not str(h).startswith("column_")])
    coverage = len(mappings) / total_headers if total_headers else 0
    # Cap confidence below 60 when coverage < 50% so AI fills in the unmapped columns.
    raw_confidence = min(90, 45 + len(mappings) * 8)
    confidence = raw_confidence if coverage >= 0.5 else min(55, raw_confidence)

    return {
        "source": "heuristic",
        "safety_status": "Safe",
        "target_doctype": target_doctype,
        "import_order": int(hint.get("import_order") or 999),
        "confidence": confidence,
        "sheet_name": sheet.get("sheet_name"),
        "header_row_number": sheet.get("detected_header_row") or 1,
        "mappings": mappings,
        "defaults": get_default_values(target_doctype, doc.company, sheet.get("sheet_name")),
        "reason": hint.get("note"),
    }


def error_analysis(summary: dict, hint: dict, reason: str | None, target_doctype: str | None = None) -> dict:
    sheet = first_sheet(summary)
    return {
        "source": "rule",
        "safety_status": "Error",
        "target_doctype": target_doctype,
        "import_order": int(hint.get("import_order") or 999),
        "confidence": 0,
        "sheet_name": sheet.get("sheet_name"),
        "header_row_number": sheet.get("detected_header_row") or 1,
        "mappings": [],
        "defaults": {},
        "reason": reason or "Không thể import tự động vào ERPNext.",
    }


def first_sheet(summary: dict) -> dict:
    sheets = summary.get("sheets") or []
    return sheets[0] if sheets else {}


def analysis_to_json(analysis: dict) -> str:
    return json.dumps(analysis, ensure_ascii=False, indent=2, default=str)
