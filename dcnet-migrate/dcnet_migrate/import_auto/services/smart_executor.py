"""Execute a plan returned by ``smart_planner.build_smart_plan``.

Before inserting, source-backed preview steps are expanded by applying their
``row_template`` to every Excel row in Python. Each step then inserts records
via ``frappe.get_doc(record).insert()``. Each source row runs inside its own
SAVEPOINT so a bad row can be rolled back without losing records that were
already imported. Re-running the same plan is safe because master data steps
skip existing records.
"""

from __future__ import annotations

import hashlib
import json
import re
import unicodedata
from typing import Any

import frappe
from frappe import _
from frappe.utils import cstr, flt

from dcnet_migrate.import_auto.services.utils import GROUP_LINK_CONFIG, normalize_key


LINK_CANDIDATE_LIMIT = 20000
IMPORT_REPORT_DETAIL_LIMIT = 500

AUTO_CREATE_LINK_DOCTYPES = {
    "Asset Category",
    "Bank",
    "Customer Group",
    "Item Group",
    "Location",
    "Supplier Group",
    "Territory",
    "UOM",
    "Warehouse",
}
COMPANY_SCOPED_LINK_DOCTYPES = {"Account", "Cost Center", "Project", "Warehouse"}
TABLE_FIELDTYPES = {"Table", "Table MultiSelect"}
PRESERVE_PAYLOAD_NAME_DOCTYPES = {"Customer", "Supplier"}
STRICT_IDENTITY_DOCTYPES = {"Bank Account", "Customer", "Item", "Supplier", "UOM"}
STRICT_IDENTITY_FIELDS = {
    "Bank Account": ["bank_account_no", "name"],
    "Customer": ["customer_name", "tax_id", "name"],
    "Item": ["item_code", "name"],
    "Supplier": ["supplier_name", "tax_id", "name"],
    "UOM": ["uom_name", "name"],
}


REQUIRED_MASTER_LABEL_FIELDS = {
    "Bank": "bank_name",
    "Customer": "customer_name",
    "Customer Group": "customer_group_name",
    "Item": "item_name",
    "Item Group": "item_group_name",
    "Project": "project_name",
    "Supplier": "supplier_name",
    "Supplier Group": "supplier_group_name",
    "Territory": "territory_name",
    "UOM": "uom_name",
}

COMMON_LINK_LABEL_FIELDS = {
    "Account": ["account_number", "account_name", "name"],
    "Asset Category": ["asset_category_name", "name"],
    "Bank": ["bank_name", "name"],
    "Brand": ["brand", "name"],
    "Company": ["company_name", "abbr", "name"],
    "Cost Center": ["cost_center_name", "name"],
    "Customer": ["customer_name", "name"],
    "Customer Group": ["customer_group_name", "name"],
    "Department": ["department_name", "name"],
    "Item": ["item_code", "item_name", "name"],
    "Item Group": ["item_group_name", "name"],
    "Location": ["location_name", "name"],
    "Project": ["project_name", "name"],
    "Supplier": ["supplier_name", "name"],
    "Supplier Group": ["supplier_group_name", "name"],
    "Territory": ["territory_name", "name"],
    "UOM": ["uom_name", "name"],
    "Warehouse": ["warehouse_name", "name"],
}

MASTER_UNIQUE_FIELDS = {
    "Account": ["account_number", "account_name"],
    "Address": ["address_title", "address_line1"],
    "Asset Category": ["asset_category_name"],
    "Bank Account": ["bank_account_no", "account_name"],
    "Bank": ["bank_name"],
    "Brand": ["brand"],
    "Company": ["company_name", "abbr"],
    "Cost Center": ["cost_center_name"],
    "Customer": ["customer_name", "tax_id"],
    "Customer Group": ["customer_group_name"],
    "Department": ["department_name"],
    "Item": ["item_code"],
    "Item Group": ["item_group_name"],
    "Location": ["location_name"],
    "Project": ["project_name"],
    "Supplier": ["supplier_name", "tax_id"],
    "Supplier Group": ["supplier_group_name"],
    "Territory": ["territory_name"],
    "UOM": ["uom_name"],
    "Warehouse": ["warehouse_name"],
}

ITEM_MASTER_VALUE_FIELDS = {
    "opening_stock",
    "standard_rate",
    "valuation_rate",
    "last_purchase_rate",
}

ITEM_TEXT_FIELD_MAX_LENGTHS = {
    "item_code": 140,
    "item_name": 140,
}

ASSET_TEXT_FIELD_MAX_LENGTHS = {
    "asset_name": 140,
}

# Address.name = "{address_title}-{address_type}". On a name collision,
# Address.autoname() falls back to make_autoname(name + "-.#") to
# disambiguate — and empirically THAT call itself raises "Data too long for
# column 'name'" once the combined title+type string reaches ~100 characters,
# well before the column's actual VARCHAR(140) limit (verified directly
# against this site's make_autoname()). So the safe budget for the combined
# "{address_title}-{address_type}" string is much tighter than 140.
ADDRESS_NAME_SAFE_TOTAL_LENGTH = 90
# Supplier/Customer name is also the PK (VARCHAR 140)
PARTY_NAME_MAX_LENGTH = 140

ANALYSIS_EXPAND_DOCTYPES = {
    "Bank",
    "Bank Account",
    "Customer",
    "Department",
    "Item",
    "Item Group",
    "Project",
    "Supplier",
    "UOM",
    "Warehouse",
}


def _append_item_description_note(payload: dict, note: str) -> None:
    note = cstr(note).strip()
    if not note:
        return

    description = cstr(payload.get("description")).strip()
    if note in description:
        return
    payload["description"] = f"{note}\n\n{description}" if description else note


def _sanitise_item_code_value(value: str) -> str:
    original = cstr(value).strip()
    if not original:
        return ""

    item_code = original
    item_code = item_code.replace("->", "-to-").replace("<-", "-from-")
    item_code = item_code.replace(">", "-").replace("<", "-")
    item_code = re.sub(r"\s+", " ", item_code).strip(" -")
    item_code = re.sub(r"-{2,}", "-", item_code)

    if not item_code:
        digest = hashlib.sha1(original.encode("utf-8")).hexdigest()[:8]
        item_code = f"ITEM-{digest}"

    max_length = ITEM_TEXT_FIELD_MAX_LENGTHS["item_code"]
    if len(item_code) > max_length:
        digest = hashlib.sha1(item_code.encode("utf-8")).hexdigest()[:8]
        item_code = f"{item_code[: max_length - 9].rstrip(' -')}-{digest}"

    return item_code


def _normalise_item_code(payload: dict) -> None:
    original_code = cstr(payload.get("item_code")).strip()
    if not original_code:
        return

    item_code = _sanitise_item_code_value(original_code)
    payload["item_code"] = item_code
    if item_code != original_code:
        _append_item_description_note(payload, f"Mã nguồn: {original_code}")


def _normalise_item_payload(payload: dict) -> None:
    """Keep Item imports as master data and preserve long names safely."""
    for fieldname in ITEM_MASTER_VALUE_FIELDS:
        payload.pop(fieldname, None)

    _normalise_item_code(payload)

    if not payload.get("item_name") and payload.get("item_code"):
        payload["item_name"] = cstr(payload.get("item_code")).strip()

    item_name = cstr(payload.get("item_name")).strip()
    max_length = ITEM_TEXT_FIELD_MAX_LENGTHS["item_name"]
    if len(item_name) > max_length:
        full_item_name = item_name
        payload["item_name"] = full_item_name[:max_length].rstrip()
        _append_item_description_note(payload, full_item_name)
    elif item_name:
        payload["item_name"] = item_name


def _normalise_address_payload(payload: dict) -> None:
    """Truncate address_title so "{title}-{address_type}" stays within the
    budget where Frappe's own name-collision dedup logic (make_autoname)
    still works — see ADDRESS_NAME_SAFE_TOTAL_LENGTH."""
    address_type = cstr(payload.get("address_type") or "Billing").strip()
    budget = max(1, ADDRESS_NAME_SAFE_TOTAL_LENGTH - len(address_type) - 1)  # "-" separator
    title = cstr(payload.get("address_title")).strip()
    if len(title) > budget:
        payload["address_title"] = title[:budget].rstrip()


def _normalise_party_name_payload(target_doctype: str, payload: dict) -> None:
    """Truncate supplier_name / customer_name to the column's VARCHAR(140) limit."""
    field = "supplier_name" if target_doctype == "Supplier" else "customer_name"
    value = cstr(payload.get(field)).strip()
    if len(value) > PARTY_NAME_MAX_LENGTH:
        payload[field] = value[:PARTY_NAME_MAX_LENGTH].rstrip()


def _normalise_asset_payload(payload: dict) -> None:
    asset_name = cstr(payload.get("asset_name") or payload.get("item_name") or payload.get("item_code")).strip()
    max_length = ASSET_TEXT_FIELD_MAX_LENGTHS["asset_name"]
    if len(asset_name) > max_length:
        asset_name = asset_name[:max_length].rstrip()
    if asset_name:
        payload["asset_name"] = asset_name


def _default_item_stock_uom() -> str:
    for value in ("Nos", "Cái", "Cai", "Unit"):
        try:
            if frappe.db.exists("UOM", value):
                return value
            existing = frappe.db.get_value("UOM", {"uom_name": value}, "name")
            if existing:
                return existing
        except Exception:
            pass
    return "Nos"


def _default_customer_group() -> str:
    """Return the first leaf (non-group) Customer Group, falling back to 'Commercial'."""
    for name in ("Commercial", "Khách hàng", "Retail", "General"):
        try:
            row = frappe.db.get_value("Customer Group", {"customer_group_name": name, "is_group": 0}, "name")
            if row:
                return row
        except Exception:
            pass
    try:
        return frappe.db.get_value("Customer Group", {"is_group": 0}, "name") or "Commercial"
    except Exception:
        return "Commercial"


def _default_supplier_group() -> str:
    """Return the first leaf (non-group) Supplier Group, falling back to 'All Supplier Groups'."""
    for name in ("Services", "Raw Material", "Nhà cung cấp", "Local", "General"):
        try:
            row = frappe.db.get_value("Supplier Group", {"supplier_group_name": name, "is_group": 0}, "name")
            if row:
                return row
        except Exception:
            pass
    try:
        return frappe.db.get_value("Supplier Group", {"is_group": 0}, "name") or "All Supplier Groups"
    except Exception:
        return "All Supplier Groups"


# ERPNext blocks creating a Customer whenever a Customer Group of the exact
# same name already exists (Customer.validate_name_with_customer_group()).
# That collision isn't a real data problem — it's self-inflicted: resolving
# some OTHER row's customer_group/supplier_group column (via GROUP_LINK_CONFIG
# in _resolve_link_field_value) auto-creates a leaf Group for whatever string
# didn't match an existing one, and across a big customer/supplier file it's
# common for that string to coincidentally equal ANOTHER row's own company
# name. The fix generalises to any company's data (no hardcoded names): right
# before inserting a Customer/Supplier, if a same-named Group already exists
# but has zero real Customers/Suppliers filed under it, it's not a real
# category — nothing depends on it — so it's safe to drop and let this row's
# own record take that name.
_GROUP_NAME_COLLISION_CONFIG = {
    "Customer": ("Customer Group", "customer_name", "customer_group"),
    "Supplier": ("Supplier Group", "supplier_name", "supplier_group"),
}


def _clear_stale_group_name_collision(target_doctype: str, payload: dict) -> None:
    config = _GROUP_NAME_COLLISION_CONFIG.get(target_doctype)
    if not config:
        return
    group_doctype, name_field, group_field = config
    name = cstr(payload.get(name_field)).strip()
    if not name or not frappe.db.exists(group_doctype, name):
        return
    try:
        if frappe.db.get_value(group_doctype, name, "is_group"):
            return  # a real parent/category node — never touch
        if frappe.db.count(target_doctype, {group_field: name}):
            return  # actually used by existing records — real data, keep it
        frappe.delete_doc(group_doctype, name, ignore_permissions=True, force=True)
    except Exception:
        frappe.log_error(frappe.get_traceback(), f"Clear stale {group_doctype}: {name}")


def _default_item_group() -> str:
    for value in ("All Item Groups", "Products", "Sản phẩm"):
        try:
            if frappe.db.exists("Item Group", value):
                return value
            existing = frappe.db.get_value("Item Group", {"item_group_name": value}, "name")
            if existing:
                return existing
        except Exception:
            pass
    try:
        return frappe.db.get_value("Item Group", {"is_group": 1}, "name") or ""
    except Exception:
        return ""


def _default_asset_location(context: dict | None = None) -> str:
    context = context or {}
    company = _context_company(context)
    candidates = [
        company,
        "Trụ sở chính",
        "Tru so chinh",
        "Main Location",
    ]
    for value in candidates:
        value = cstr(value).strip()
        if not value:
            continue
        try:
            if frappe.db.exists("Location", value):
                return value
            existing = frappe.db.get_value("Location", {"location_name": value}, "name")
            if existing:
                return existing
        except Exception:
            pass
    try:
        return frappe.db.get_value("Location", {}, "name") or (company or "Main Location")
    except Exception:
        return company or "Main Location"


def _default_asset_cost_center(context: dict | None = None) -> str:
    context = context or {}
    company = _context_company(context)
    if not company:
        return ""

    try:
        company_default = frappe.db.get_value("Company", company, "depreciation_cost_center")
        if company_default and frappe.db.exists("Cost Center", company_default):
            is_group = frappe.db.get_value("Cost Center", company_default, "is_group")
            if not is_group:
                return company_default
    except Exception:
        pass

    try:
        existing_leaf = frappe.db.get_value(
            "Cost Center",
            {"company": company, "is_group": 0, "disabled": 0},
            "name",
        )
        if existing_leaf:
            return existing_leaf
    except Exception:
        pass

    if not context.get("dry_run"):
        return _ensure_default_cost_center(context) or ""
    return ""


def _ensure_item_import_prerequisites(plan: dict, context: dict) -> None:
    """Create tiny Item/Asset dependencies before row-level savepoints.

    Link auto-create also happens per row, but row failures roll back everything
    created after that row's SAVEPOINT. Item imports commonly depend on the root
    Item Group and UOM values such as ``All Item Groups`` and ``Nos``. CCDC
    opening files also depend on Asset Category and Location. Creating them once
    up front keeps the whole file from failing repeatedly when the site has just
    been reset.
    """
    if context.get("dry_run") or not isinstance(plan, dict):
        return

    item_steps = [
        step for step in plan.get("steps") or []
        if isinstance(step, dict) and step.get("target_doctype") == "Item"
    ]
    asset_steps = [
        step for step in plan.get("steps") or []
        if isinstance(step, dict) and step.get("target_doctype") == "Asset"
    ]
    if not item_steps and not asset_steps:
        return

    item_groups = {"All Item Groups"}
    uoms = {_default_item_stock_uom() or "Nos"}
    asset_categories: set[str] = set()
    locations: set[str] = set()
    cost_centers: set[str] = set()

    for step in item_steps:
        for record in step.get("records") or []:
            if not isinstance(record, dict):
                continue

            item_group = cstr(record.get("item_group")).strip()
            if item_group:
                item_groups.add(item_group)

            asset_category = cstr(record.get("asset_category")).strip()
            if asset_category:
                asset_categories.add(asset_category)

            for fieldname in ("stock_uom", "purchase_uom", "sales_uom", "uom"):
                uom = cstr(record.get(fieldname)).strip()
                if uom:
                    uoms.add(uom)

            for row in record.get("uoms") or []:
                if isinstance(row, dict):
                    uom = cstr(row.get("uom")).strip()
                    if uom:
                        uoms.add(uom)

    for step in asset_steps:
        for record in step.get("records") or []:
            if not isinstance(record, dict):
                continue
            asset_category = cstr(record.get("asset_category")).strip()
            if asset_category:
                asset_categories.add(asset_category)
            location = cstr(record.get("location")).strip()
            if location:
                locations.add(location)
            cost_center = cstr(record.get("cost_center")).strip()
            if cost_center:
                cost_centers.add(cost_center)

    for item_group in sorted(item_groups):
        _create_missing_group("Item Group", item_group, context)

    for uom in sorted(uoms):
        _create_missing_uom(uom, context)

    for asset_category in sorted(asset_categories):
        _create_missing_asset_category(asset_category, context)

    if asset_steps and not locations:
        locations.add(_default_asset_location(context))
    for location in sorted(locations):
        _create_missing_location(location, context)

    if asset_steps:
        default_cost_center = _ensure_default_cost_center(context)
        if default_cost_center:
            cost_centers.add(default_cost_center)
    for cost_center in sorted(cost_centers):
        _create_missing_cost_center(cost_center, context)


def _apply_payload_defaults(target_doctype: str, payload: dict, context: dict | None = None) -> None:
    context = context or {}

    if target_doctype == "Asset":
        gross_purchase_amount = payload.pop("gross_purchase_amount", None)
        if not _is_blank(gross_purchase_amount):
            if _is_blank(payload.get("purchase_amount")):
                payload["purchase_amount"] = gross_purchase_amount
            if _is_blank(payload.get("net_purchase_amount")):
                payload["net_purchase_amount"] = gross_purchase_amount

        quantity = payload.pop("quantity", None)
        if not _is_blank(quantity) and _is_blank(payload.get("asset_quantity")):
            payload["asset_quantity"] = quantity

        if _is_blank(payload.get("location")):
            payload["location"] = _default_asset_location(context)
        if _is_blank(payload.get("cost_center")):
            cost_center = _default_asset_cost_center(context)
            if cost_center:
                payload["cost_center"] = cost_center
        if _is_blank(payload.get("asset_owner")):
            payload["asset_owner"] = "Company"
        if _is_blank(payload.get("asset_owner_company")) and not _is_blank(payload.get("company")):
            payload["asset_owner_company"] = payload.get("company")
        if _is_blank(payload.get("is_existing_asset")):
            payload["is_existing_asset"] = 1
        if _is_blank(payload.get("calculate_depreciation")):
            payload["calculate_depreciation"] = 0
        _normalise_asset_payload(payload)
        return

    if target_doctype == "Customer":
        cg = cstr(payload.get("customer_group")).strip()
        # Resolve group-type or missing customer_group to a leaf group
        if not cg or _is_blank(cg):
            payload["customer_group"] = _default_customer_group()
        else:
            try:
                if frappe.db.get_value("Customer Group", cg, "is_group"):
                    payload["customer_group"] = _default_customer_group()
            except Exception:
                payload["customer_group"] = _default_customer_group()
        return

    if target_doctype == "Supplier":
        sg = cstr(payload.get("supplier_group")).strip()
        if not sg or _is_blank(sg):
            payload["supplier_group"] = _default_supplier_group()
        else:
            try:
                if frappe.db.get_value("Supplier Group", sg, "is_group"):
                    payload["supplier_group"] = _default_supplier_group()
            except Exception:
                payload["supplier_group"] = _default_supplier_group()
        return

    if target_doctype != "Item":
        return
    if _is_blank(payload.get("stock_uom")):
        payload["stock_uom"] = _default_item_stock_uom()
    if _is_blank(payload.get("item_group")):
        item_group = _default_item_group()
        if item_group:
            payload["item_group"] = item_group
    for fieldname in ("is_stock_item", "is_sales_item", "is_purchase_item"):
        if _is_blank(payload.get(fieldname)):
            payload[fieldname] = 1


def _normalise_business_payload_with_reason(target_doctype: str, payload: dict) -> tuple[bool, str, str]:
    """Return whether a payload should be imported plus a user-facing skip reason."""
    if _is_total_payload(payload):
        return False, "Dòng tổng/cộng, không import.", "total_row"

    if target_doctype == "Item":
        _normalise_item_payload(payload)
    elif target_doctype == "UOM":
        _normalise_uom_payload(payload)
    elif target_doctype == "Address":
        _normalise_address_payload(payload)
    elif target_doctype in ("Supplier", "Customer"):
        _normalise_party_name_payload(target_doctype, payload)

    required_label = REQUIRED_MASTER_LABEL_FIELDS.get(target_doctype)
    if required_label and _is_blank(payload.get(required_label)):
        return False, f"Thiếu giá trị bắt buộc `{required_label}`.", "missing_required"

    if target_doctype == "Address" and not _is_importable_address_payload(payload):
        return False, "Địa chỉ thiếu nội dung hoặc thiếu liên kết đối tượng.", "not_importable"

    if target_doctype == "Contact" and not _is_importable_contact_payload(payload):
        return False, "Liên hệ thiếu số điện thoại/email hoặc thiếu liên kết đối tượng.", "not_importable"

    if target_doctype == "Item":
        return True, "", ""

    if target_doctype == "Item Price" and flt(payload.get("price_list_rate")) <= 0:
        return False, "Giá bán không lớn hơn 0.", "not_importable"

    if target_doctype == "Stock Reconciliation":
        items = payload.get("items")
        if not isinstance(items, list):
            return True, "", ""

        valid_items = []
        for item in items:
            if not isinstance(item, dict):
                continue
            if flt(item.get("qty")) and flt(item.get("valuation_rate")) <= 0:
                continue
            valid_items.append(item)

        payload["items"] = valid_items
        if not valid_items:
            return False, "Không có dòng tồn kho hợp lệ hoặc thiếu valuation_rate.", "not_importable"

    return True, "", ""


def _normalise_uom_payload(payload: dict) -> None:
    if not _is_blank(payload.get("uom_name")):
        return
    for fieldname in ("name", "uom", "UOM", "unit", "unit_name"):
        value = cstr(payload.get(fieldname)).strip()
        if value:
            payload["uom_name"] = value
            return


def execute_plan(doc, file_row, plan: dict, dry_run: bool = False, progress_callback=None) -> dict:
    if not isinstance(plan, dict) or not plan.get("steps"):
        frappe.throw(_("Plan rỗng, không có bước nào để thực thi."))

    plan = _expand_sampled_plan_from_analysis(doc, file_row, plan)
    _apply_pre_execution_plan_invariants(doc, plan)

    results: list[dict] = []
    total_inserted = 0
    total_skipped = 0
    total_failed = 0
    link_context = _make_link_context(doc, dry_run=dry_run)
    _ensure_item_import_prerequisites(plan, link_context)
    total_records = sum(len(step.get("records") or []) for step in plan.get("steps") or [])
    processed_before = 0

    try:
        for step in plan["steps"]:
            records_in_step = len(step.get("records") or [])
            _safe_progress_callback(progress_callback, {
                "stage": "executing",
                "percent": _execution_percent(processed_before, total_records),
                "message": _("Đang bắt đầu bước {0}: {1}").format(
                    step.get("step") or len(results) + 1,
                    step.get("title") or step.get("target_doctype") or "",
                ),
                "current_step": step.get("step") or len(results) + 1,
                "current_step_title": step.get("title") or "",
                "target_doctype": step.get("target_doctype"),
                "step_processed": 0,
                "step_total": records_in_step,
                "total_processed": processed_before,
                "total_records": total_records,
                "inserted": total_inserted,
                "skipped": total_skipped,
                "failed": total_failed,
            })
            step_result = _run_step(
                doc,
                file_row,
                step,
                dry_run=dry_run,
                link_context=link_context,
                progress_callback=progress_callback,
                progress_state={
                    "total_records": total_records,
                    "processed_before": processed_before,
                    "inserted_before": total_inserted,
                    "skipped_before": total_skipped,
                    "failed_before": total_failed,
                },
            )
            results.append(step_result)
            total_inserted += step_result["inserted"]
            total_skipped += step_result["skipped"]
            total_failed += step_result["failed"]
            processed_before += records_in_step

        if not dry_run:
            frappe.db.commit()
    except Exception as exc:
        if not dry_run:
            if total_inserted:
                frappe.db.commit()
            else:
                frappe.db.rollback()
        failed_result = next((r for r in results if r.get("failed")), {})
        return {
            "ok": False,
            "dry_run": dry_run,
            "error": str(exc),
            "results": results,
            "total_inserted": total_inserted,
            "total_skipped": total_skipped,
            "total_failed": total_failed,
            "failed_step_index": failed_result.get("step"),
            "failed_step_title": failed_result.get("title"),
            "failed_target_doctype": failed_result.get("target_doctype"),
            "failed_row_index": failed_result.get("failed_row_index"),
            "failed_record": failed_result.get("failed_record"),
            "error_type": failed_result.get("error_type"),
            "partial_committed": bool(total_inserted),
            "rollback_scope": "committed_before_unhandled_error" if total_inserted else "request_rollback",
            "can_resume": bool(total_inserted),
        }

    return {
        "ok": True,
        "dry_run": dry_run,
        "results": results,
        "total_inserted": total_inserted,
        "total_skipped": total_skipped,
        "total_failed": total_failed,
        "partial": bool(total_skipped or total_failed),
        "rollback_scope": "failed_rows_only" if total_failed else "none",
    }


def _row_savepoint_name(step_index, record_index: int) -> str:
    step_text = re.sub(r"[^0-9A-Za-z_]+", "_", cstr(step_index or "0"))
    return f"smart_import_row_{step_text}_{int(record_index)}"


def _execution_percent(processed: int, total: int) -> int:
    if not total:
        return 95
    return max(30, min(98, 30 + round((processed / total) * 68)))


def _safe_progress_callback(progress_callback, payload: dict) -> None:
    if not progress_callback:
        return
    try:
        progress_callback(payload)
    except Exception:
        frappe.log_error(frappe.get_traceback(), "Smart Import Progress Callback Failed")


def _compact_record_for_report(record: dict | None) -> dict:
    if not isinstance(record, dict):
        return {}
    compact = {}
    for key, value in record.items():
        if key.startswith("__"):
            continue
        if isinstance(value, (dict, list)):
            continue
        if value in (None, ""):
            continue
        compact[key] = value
        if len(compact) >= 8:
            break
    return compact


def _run_step(
    doc,
    file_row,
    step: dict,
    dry_run: bool = False,
    link_context: dict | None = None,
    progress_callback=None,
    progress_state: dict | None = None,
) -> dict:
    target_doctype = step.get("target_doctype")
    if not target_doctype or not frappe.db.exists("DocType", target_doctype):
        error = (
            "Thiếu target_doctype."
            if not target_doctype
            else f"DocType '{target_doctype}' không tồn tại."
        )
        return {
            "step": step.get("step"),
            "title": step.get("title"),
            "target_doctype": target_doctype,
            "inserted": 0,
            "skipped": 0,
            "failed": len(step.get("records") or []),
            "errors": [{"row": idx + 1, "error": error} for idx in range(len(step.get("records") or []))],
            "error": error,
            "error_type": "MissingDocType" if not target_doctype else "InvalidDocType",
        }

    if step.get("records_are_preview") and isinstance(step.get("row_template"), dict) and step["row_template"].get("field_map"):
        error = (
            "Bước import vẫn đang ở dạng preview 10 dòng; backend chưa mở rộng được "
            "row_template sang toàn bộ Excel. Vui lòng kiểm tra sheet/header và chạy lại phân tích."
        )
        failed_count = int(step.get("record_count") or len(step.get("records") or []) or 0)
        return {
            "step": step.get("step"),
            "title": step.get("title"),
            "target_doctype": target_doctype,
            "inserted": 0,
            "skipped": 0,
            "failed": failed_count,
            "errors": [{"row": 1, "error": error}],
            "error": error,
            "error_type": "UnexpandedScriptTemplate",
        }

    inserted = 0
    skipped = 0
    failed = 0
    errors: list[dict] = []
    skipped_rows: list[dict] = []
    skipped_by_type: dict[str, int] = {}
    inserted_names: list[str] = []
    created_records = link_context.setdefault("created_records", {})
    unique_key = step.get("unique_key") or "name"
    ignore_duplicates = bool(step.get("ignore_duplicates", True))
    link_context = link_context or _make_link_context(doc, dry_run=dry_run)
    link_action_start = len(link_context["actions"])
    progress_state = progress_state or {}
    records = step.get("records") or []
    record_total = len(records)
    progress_batch_size = 200

    def add_skipped_row(row_index: int, source_row, reason: str, reason_type: str, record: dict, existing_name: str | None = None):
        skipped_by_type[reason_type] = skipped_by_type.get(reason_type, 0) + 1
        if len(skipped_rows) >= IMPORT_REPORT_DETAIL_LIMIT:
            return
        skipped_rows.append({
            "row": row_index,
            "source_row": source_row or row_index,
            "reason": reason,
            "reason_type": reason_type,
            "existing_name": existing_name,
            "record": _compact_record_for_report(record),
        })

    def duplicate_skip_details(existing_name: str | None) -> tuple[str, str]:
        created_source_row = created_records.get((target_doctype, existing_name)) if existing_name else None
        if created_source_row:
            return (
                f"Trùng mã trong cùng file/lần import: đã tạo ở dòng nguồn {created_source_row} ({existing_name}).",
                "source_duplicate",
            )
        return (f"Đã tồn tại trong DCNET: {existing_name}.", "duplicate")

    for record_index, record in enumerate(records, start=1):
        row_savepoint = None
        row_ok = False
        payload: dict = {}
        source_row = record_index
        try:
            if not dry_run:
                savepoint_name = _row_savepoint_name(step.get("step"), record_index)
                frappe.db.savepoint(savepoint_name)
                row_savepoint = savepoint_name

            payload = dict(record)
            source_row = payload.pop("__source_row_number", None) or record_index
            for key in list(payload):
                if cstr(key).startswith("__"):
                    payload.pop(key, None)
            payload["doctype"] = target_doctype
            _apply_payload_defaults(target_doctype, payload, link_context)
            _normalise_payload_links(target_doctype, payload, link_context)
            is_importable, skip_reason, skip_type = _normalise_business_payload_with_reason(target_doctype, payload)
            if not is_importable:
                skipped += 1
                add_skipped_row(record_index, source_row, skip_reason, skip_type, payload)
                row_ok = True
                continue

            existing_name = _find_existing_record_name(target_doctype, payload, unique_key, link_context)
            if existing_name and (ignore_duplicates or _is_master_doctype(target_doctype)):
                skipped += 1
                skip_reason, skip_type = duplicate_skip_details(existing_name)
                add_skipped_row(
                    record_index,
                    source_row,
                    skip_reason,
                    skip_type,
                    payload,
                    existing_name=existing_name,
                )
                row_ok = True
                continue

            if dry_run:
                inserted += 1
                row_ok = True
                continue

            _clear_stale_group_name_collision(target_doctype, payload)
            new_doc = frappe.get_doc(payload)
            if _should_preserve_payload_name(target_doctype, payload):
                new_doc.flags.name_set = True
            if step.get("ignore_mandatory") or target_doctype == "Account":
                new_doc.flags.ignore_mandatory = True
            _auto_create_missing_link_masters(new_doc)
            new_doc.insert(ignore_permissions=False)
            inserted += 1
            inserted_names.append(new_doc.name)
            created_records[(target_doctype, new_doc.name)] = source_row
            _create_success_import_log(doc, file_row, step, target_doctype, record_index, new_doc.name)
            _clear_link_cache_for_doctype(link_context, target_doctype)
            row_ok = True
        except Exception as exc:
            if row_savepoint:
                frappe.db.rollback(save_point=row_savepoint)
                row_savepoint = None
            duplicate_existing_name = _existing_name_from_duplicate_exception(
                exc,
                target_doctype,
                payload if payload else (record if isinstance(record, dict) else {}),
                unique_key,
                link_context,
            )
            if (
                _classify_exception(exc) == "DuplicateEntryError"
                and target_doctype == "UOM"
                and not duplicate_existing_name
            ):
                recovered_uom = _recover_uom_collation_duplicate(
                    payload if payload else (record if isinstance(record, dict) else {}),
                    link_context,
                )
                if recovered_uom:
                    inserted += 1
                    inserted_names.append(recovered_uom)
                    created_records[(target_doctype, recovered_uom)] = source_row
                    _create_success_import_log(doc, file_row, step, target_doctype, record_index, recovered_uom)
                    _clear_link_cache_for_doctype(link_context, target_doctype)
                    continue
            if duplicate_existing_name and (ignore_duplicates or _is_master_doctype(target_doctype)):
                skipped += 1
                skip_reason, skip_type = duplicate_skip_details(duplicate_existing_name)
                add_skipped_row(
                    record_index,
                    source_row,
                    skip_reason,
                    skip_type,
                    payload if payload else (record if isinstance(record, dict) else {}),
                    existing_name=duplicate_existing_name,
                )
                _clear_link_cache_for_doctype(link_context, target_doctype)
                continue
            failed += 1
            source_row = record.get("__source_row_number") if isinstance(record, dict) else record_index
            errors.append({
                "row": record_index,
                "source_row": source_row or record_index,
                "error": str(exc)[:500],
                "record": _compact_record_for_report(record),
                "error_type": _classify_exception(exc),
            })
            continue
        finally:
            if row_savepoint and row_ok:
                try:
                    frappe.db.release_savepoint(row_savepoint)
                except Exception:
                    pass
            if (
                progress_callback
                and (
                    record_index == 1
                    or record_index == record_total
                    or record_index % progress_batch_size == 0
                )
            ):
                total_processed = int(progress_state.get("processed_before") or 0) + record_index
                total_records = int(progress_state.get("total_records") or record_total)
                _safe_progress_callback(progress_callback, {
                    "stage": "executing",
                    "percent": _execution_percent(total_processed, total_records),
                    "message": _("Đang import {0}/{1} bản ghi ở bước {2} ({3}).").format(
                        record_index,
                        record_total,
                        step.get("step") or "",
                        step.get("target_doctype") or "",
                    ),
                    "current_step": step.get("step"),
                    "current_step_title": step.get("title") or "",
                    "target_doctype": target_doctype,
                    "step_processed": record_index,
                    "step_total": record_total,
                    "total_processed": total_processed,
                    "total_records": total_records,
                    "inserted": int(progress_state.get("inserted_before") or 0) + inserted,
                    "skipped": int(progress_state.get("skipped_before") or 0) + skipped,
                    "failed": int(progress_state.get("failed_before") or 0) + failed,
                    "batch_size": progress_batch_size,
                })

    result = {
        "step": step.get("step"),
        "title": step.get("title"),
        "target_doctype": target_doctype,
        "inserted": inserted,
        "skipped": skipped,
        "failed": failed,
        "errors": errors,
        "skipped_rows": skipped_rows,
        "skipped_row_count": skipped,
        "skipped_rows_truncated": skipped > len(skipped_rows),
        "skipped_by_type": skipped_by_type,
        "inserted_names": inserted_names,
        "link_resolution": _link_resolution_summary(link_context, link_action_start),
    }
    if errors:
        first_error = errors[0]
        result.update({
            "error": f"Lỗi {failed} dòng; các dòng lỗi đã được bỏ qua để import tiếp.",
            "failed_row_index": first_error.get("row"),
            "failed_record": first_error.get("record"),
            "error_type": first_error.get("error_type"),
        })
    return result


def _create_success_import_log(import_doc, file_row, step: dict, target_doctype: str, row_index: int, docname: str) -> None:
    """Record successful smart-import inserts in the standard Data Import Log list."""
    try:
        messages = {
            "source": "Import Auto",
            "method": "Smart Import",
            "import_auto": getattr(import_doc, "name", None),
            "import_auto_title": getattr(import_doc, "display_name", None),
            "import_auto_file": getattr(file_row, "name", None),
            "file_name": getattr(file_row, "file_name", None),
            "target_doctype": target_doctype,
            "step": step.get("step"),
            "step_title": step.get("title"),
        }
        frappe.get_doc(
            {
                "doctype": "Data Import Log",
                "row_indexes": json.dumps([row_index], ensure_ascii=False),
                "success": 1,
                "docname": docname,
                "messages": json.dumps(messages, ensure_ascii=False),
                "log_index": row_index,
            }
        ).insert(ignore_permissions=True)
    except Exception:
        frappe.log_error(frappe.get_traceback(), "Import Auto Success Log Failed")


def _exists_by_field(doctype: str, fieldname: str, value) -> bool:
    if value in (None, ""):
        return False
    if fieldname == "name":
        return bool(frappe.db.exists(doctype, value))
    try:
        return bool(frappe.db.exists(doctype, {fieldname: value}))
    except Exception:
        return False


def _expand_sampled_plan_from_analysis(doc, file_row, plan: dict) -> dict:
    """Expand AI sample-only script steps to all Excel rows using Python.

    The UI preview plan intentionally carries only sample records. Execution
    must still import the whole source file, so we apply each step's
    ``row_template`` to the Excel rows here. If an older plan lacks
    ``row_template``, we fall back to the saved analyze-file mappings.
    """
    if not file_row or not isinstance(plan, dict) or not plan.get("steps"):
        return plan

    try:
        analysis = json.loads(file_row.analysis_json or "{}")
    except Exception:
        analysis = {}

    target_doctype = analysis.get("target_doctype")
    steps = plan.get("steps") or []
    has_step_templates = any(
        isinstance(step, dict)
        and isinstance(step.get("row_template"), dict)
        and step.get("row_template", {}).get("field_map")
        for step in steps
    )
    has_analysis_template = (
        target_doctype in ANALYSIS_EXPAND_DOCTYPES
        and bool(analysis.get("mappings"))
    )
    if not has_step_templates and not has_analysis_template:
        return plan

    try:
        from dcnet_migrate.import_auto.services.excel import extract_records
        from dcnet_migrate.import_auto.services.smart_planner import (
            _materialise_records,
            _mappings_to_field_map,
            _normalise_record,
            _row_template_is_source_backed,
            _post_process_coa_plan,
            _post_process_address_plan,
            _post_process_bank_account_plan,
            _post_process_contact_plan,
            _post_process_group_link_plan,
            _post_process_item_catalog_plan,
        )

        raw_records = extract_records(
            file_row.file_path,
            analysis.get("sheet_name") or getattr(file_row, "sheet_name", None),
            analysis.get("header_row_number") or getattr(file_row, "header_row_number", None),
        )
    except Exception:
        frappe.log_error(frappe.get_traceback(), "Smart Executor Plan Expansion Failed")
        return plan

    if not raw_records:
        return plan

    field_map = _mappings_to_field_map(analysis.get("mappings") or [])

    expanded_any = False
    for step in steps:
        if not isinstance(step, dict):
            continue

        current_records = step.get("records") or []
        row_template = step.get("row_template") or {}
        if not (
            isinstance(row_template, dict)
            and row_template.get("field_map")
            and _row_template_is_source_backed(row_template)
        ):
            if not _can_expand_step_from_analysis(
                step,
                current_records,
                target_doctype,
                field_map,
                raw_records,
            ):
                continue
            row_template = {
                "source_filter": analysis.get("source_filter") or "skip_totals",
                "field_map": field_map,
            }
        elif (
            step.get("records_are_preview") is False
            and isinstance(current_records, list)
            and len(current_records) > 0
        ):
            continue

        if not (
            isinstance(row_template, dict)
            and row_template.get("field_map")
            and _row_template_is_source_backed(row_template)
        ):
            continue

        materialised = _materialise_records(row_template, raw_records, [])
        clean_records = []
        for source_index, materialised_record in enumerate(materialised, start=1):
            if not isinstance(materialised_record, dict):
                continue
            normalised = _normalise_record(materialised_record)
            if not normalised:
                continue
            normalised["__source_row_number"] = source_index
            clean_records.append(normalised)

        for defaults in (analysis.get("defaults") or {}, step.get("fixed_values") or {}):
            if isinstance(defaults, dict):
                for rec in clean_records:
                    for key, value in defaults.items():
                        rec.setdefault(key, value)

        step["records"] = clean_records
        step["record_count"] = len(clean_records)
        step["records_are_preview"] = False
        step["source_record_count"] = len(clean_records)
        expanded_any = True

    if expanded_any:
        _post_process_coa_plan(plan, doc)
        _post_process_bank_account_plan(plan, doc)
        _post_process_group_link_plan(plan)
        _post_process_address_plan(plan)
        _post_process_contact_plan(plan)
        _post_process_item_catalog_plan(plan)
        plan["total_records"] = sum(len(step.get("records") or []) for step in plan.get("steps") or [])
        plan["total_steps"] = len(plan.get("steps") or [])

    return plan


def _apply_pre_execution_plan_invariants(doc, plan: dict) -> None:
    """Run deterministic safety fixes for plans that were opened before a patch.

    Smart Import dialogs can keep an older plan JSON in the browser. This pass
    makes execution resilient even when the user clicks "Thực thi" without
    regenerating the AI plan.
    """
    try:
        from dcnet_migrate.import_auto.services.smart_planner import (
            _post_process_coa_plan,
            _post_process_address_plan,
            _post_process_bank_account_plan,
            _post_process_contact_plan,
            _post_process_group_link_plan,
            _post_process_item_catalog_plan,
        )

        _post_process_coa_plan(plan, doc)
        _post_process_bank_account_plan(plan, doc)
        _post_process_group_link_plan(plan)
        _post_process_address_plan(plan)
        _post_process_contact_plan(plan)
        _post_process_item_catalog_plan(plan)
    except Exception:
        frappe.log_error(frappe.get_traceback(), "Smart Executor Plan Invariants Failed")


def _is_master_doctype(doctype: str) -> bool:
    return doctype in MASTER_UNIQUE_FIELDS or doctype in COMMON_LINK_LABEL_FIELDS


def _can_expand_step_from_analysis(
    step: dict,
    current_records: list,
    target_doctype: str | None,
    field_map: dict,
    raw_records: list[dict],
) -> bool:
    """Decide whether an old step without row_template may use saved mappings.

    Some deterministic dependency steps share the same DocType as the source
    data. COA is the sharp edge: the backend inserts a small "Vietnamese root
    accounts" step before the real Account import. Expanding that root step
    with the file mappings turns it into a duplicate full-file Account import.
    """
    if step.get("target_doctype") != target_doctype or not field_map:
        return False
    if not isinstance(current_records, list) or len(current_records) >= len(raw_records):
        return False
    if step.get("_origin") == "smart_fix_dependency":
        return False
    if step.get("target_doctype") == "Account" and _looks_like_coa_root_step(current_records):
        return False

    if (
        step.get("records_are_preview") is True
        or step.get("execution_mode") == "python_row_template"
        or int(step.get("source_record_count") or 0) > len(current_records)
        or int(step.get("record_count") or 0) > len(current_records)
    ):
        return True

    # Empty source step from older plans: safe to rebuild from analysis.
    if not current_records:
        return True

    return False


def _looks_like_coa_root_step(records: list) -> bool:
    if not records:
        return False

    vn_root_names = {
        "Tài sản",
        "Nợ phải trả",
        "Vốn chủ sở hữu",
        "Thu nhập",
        "Chi phí",
    }
    root_like = 0
    for rec in records:
        if not isinstance(rec, dict):
            return False
        if rec.get("account_number"):
            return False
        account_name = cstr(rec.get("account_name") or rec.get("name")).strip()
        parent_account = cstr(rec.get("parent_account")).strip()
        if account_name in vn_root_names and not parent_account:
            root_like += 1

    return root_like == len(records)


def _find_existing_record_name(
    doctype: str,
    payload: dict,
    unique_key: str | None,
    context: dict,
) -> str | None:
    """Return the existing doc name for master data records.

    AI dependency steps may say "create UOM Cái" although the site already
    has ``UOM.name == Cái``.  We check the document name, declared unique key,
    and common human-label fields before attempting an insert.
    """
    if not doctype or not _doctype_exists(doctype, context):
        return None

    if doctype == "Account":
        return _find_existing_account_name(payload, context)
    if doctype == "Address":
        return _find_existing_address_name(payload)
    if doctype == "Asset":
        return _find_existing_asset_name(payload, context)
    if doctype == "Contact":
        return _find_existing_contact_name(payload)
    if doctype in GROUP_LINK_CONFIG:
        return _find_existing_group_name(doctype, payload, context)

    fields: list[str] = []
    if doctype in STRICT_IDENTITY_FIELDS:
        fields.extend(STRICT_IDENTITY_FIELDS[doctype])
    elif unique_key:
        fields.append(unique_key)
    if doctype not in STRICT_IDENTITY_FIELDS:
        fields.extend(MASTER_UNIQUE_FIELDS.get(doctype, []))
        fields.extend(COMMON_LINK_LABEL_FIELDS.get(doctype, []))
    fields.append("name")

    meta = frappe.get_meta(doctype)
    seen_fields: set[str] = set()
    for fieldname in fields:
        if not fieldname or fieldname in seen_fields:
            continue
        seen_fields.add(fieldname)
        if fieldname != "name" and not meta.get_field(fieldname):
            continue

        value = payload.get(fieldname)
        if _is_blank(value):
            continue
        value = cstr(value).strip()

        existing = _get_existing_by_field(doctype, fieldname, value, context)
        if existing:
            return existing

        # Some master DocTypes use the label itself as name (UOM, Item Group,
        # Brand, Territory...). Check that direct name before creating.
        if fieldname != "name":
            existing = _get_existing_by_field(doctype, "name", value, context)
            if existing:
                return existing

    # Party/item master rows can legitimately share long prefixes, e.g.
    # "CÔNG TY ..." and "CHI NHÁNH CÔNG TY ...". Import execution must only
    # skip these records on exact identity fields, never on fuzzy matches.
    if doctype in STRICT_IDENTITY_DOCTYPES:
        return None

    return None


def _account_company(context: dict, payload: dict | None = None) -> str | None:
    return (payload or {}).get("company") or _context_company(context)


def _account_company_abbr(company: str | None) -> str | None:
    if not company:
        return None
    try:
        return frappe.db.get_value("Company", company, "abbr")
    except Exception:
        return None


def _predicted_account_name(payload: dict, context: dict) -> str | None:
    account_name = cstr(payload.get("account_name")).strip()
    if not account_name:
        return None

    company = _account_company(context, payload)
    abbr = _account_company_abbr(company)
    if not abbr:
        return None

    account_number = cstr(payload.get("account_number")).strip()
    parts = [account_name, abbr]
    if account_number:
        parts.insert(0, account_number)
    return " - ".join(parts)


def _account_number_from_reference(value: str) -> str | None:
    text = cstr(value).strip()
    if not text:
        return None
    match = re.match(r"^([0-9][0-9A-Za-z]*(?:\.[0-9A-Za-z]+)*)\b", text)
    return match.group(1) if match else None


def _find_existing_account_name(payload: dict, context: dict) -> str | None:
    """Find existing Account strictly.

    Account numbers are hierarchical codes, so fuzzy matching is dangerous:
    ``1121`` is textually close to ``112`` but must be a separate Account.
    """
    company = _account_company(context, payload)

    predicted = _predicted_account_name(payload, context)
    if predicted:
        existing = _get_existing_by_field("Account", "name", predicted, context)
        if existing:
            return existing

    explicit_name = cstr(payload.get("name")).strip()
    if explicit_name:
        existing = _get_existing_by_field("Account", "name", explicit_name, context)
        if existing:
            return existing

    account_number = cstr(payload.get("account_number")).strip()
    if account_number and company:
        try:
            existing = frappe.db.get_value(
                "Account",
                {"account_number": account_number, "company": company},
                "name",
            )
            if existing:
                return existing
        except Exception:
            pass

    return None


def _find_existing_address_name(payload: dict) -> str | None:
    links = payload.get("links") or []
    if isinstance(links, dict):
        links = [links]
    address_line = cstr(payload.get("address_line1")).strip()
    address_type = cstr(payload.get("address_type") or "Billing").strip()
    if not links or not address_line:
        return None

    for link in links:
        if not isinstance(link, dict):
            continue
        link_doctype = cstr(link.get("link_doctype")).strip()
        link_name = cstr(link.get("link_name")).strip()
        if not link_doctype or not link_name:
            continue
        try:
            candidates = frappe.get_all(
                "Dynamic Link",
                filters={
                    "parenttype": "Address",
                    "link_doctype": link_doctype,
                    "link_name": link_name,
                },
                pluck="parent",
                limit_page_length=200,
            )
        except Exception:
            candidates = []
        for address_name in candidates:
            existing = frappe.db.get_value(
                "Address",
                address_name,
                ["name", "address_line1", "address_type"],
                as_dict=True,
            )
            if not existing:
                continue
            if (
                normalize_key(existing.address_line1) == normalize_key(address_line)
                and cstr(existing.address_type or "Billing").strip() == address_type
            ):
                return existing.name
    return None


def _find_existing_asset_name(payload: dict, context: dict) -> str | None:
    explicit_name = cstr(payload.get("name")).strip()
    if explicit_name and frappe.db.exists("Asset", explicit_name):
        return explicit_name

    company = cstr(payload.get("company") or _context_company(context)).strip()
    item_code = cstr(payload.get("item_code")).strip()
    asset_name = cstr(payload.get("asset_name")).strip()
    purchase_date = cstr(payload.get("purchase_date")).split(" ", 1)[0].strip()
    if not (company and item_code and asset_name and purchase_date):
        return None

    filters = {
        "company": company,
        "item_code": item_code,
        "asset_name": asset_name,
        "purchase_date": purchase_date,
        "docstatus": ["!=", 2],
    }
    if not _is_blank(payload.get("net_purchase_amount")):
        filters["net_purchase_amount"] = flt(payload.get("net_purchase_amount"))

    try:
        return frappe.db.get_value("Asset", filters, "name")
    except Exception:
        return None


def _find_existing_contact_name(payload: dict) -> str | None:
    links = payload.get("links") or []
    if isinstance(links, dict):
        links = [links]
    if not isinstance(links, list):
        return None

    phone_values = {
        cstr(row.get("phone")).strip()
        for row in (payload.get("phone_nos") or [])
        if isinstance(row, dict) and cstr(row.get("phone")).strip()
    }
    for value in (payload.get("phone"), payload.get("mobile_no")):
        value = cstr(value).strip()
        if value:
            phone_values.add(value)

    email_values = {
        cstr(row.get("email_id")).strip().lower()
        for row in (payload.get("email_ids") or [])
        if isinstance(row, dict) and cstr(row.get("email_id")).strip()
    }
    email_id = cstr(payload.get("email_id")).strip().lower()
    if email_id:
        email_values.add(email_id)

    first_name = normalize_key(payload.get("first_name") or "")

    for link in links:
        if not isinstance(link, dict):
            continue
        link_doctype = cstr(link.get("link_doctype")).strip()
        link_name = cstr(link.get("link_name")).strip()
        if not link_doctype or not link_name:
            continue
        try:
            candidates = frappe.get_all(
                "Dynamic Link",
                filters={
                    "parenttype": "Contact",
                    "link_doctype": link_doctype,
                    "link_name": link_name,
                },
                pluck="parent",
                limit_page_length=200,
            )
        except Exception:
            candidates = []
        for contact_name in candidates:
            if phone_values:
                existing_phones = {
                    cstr(row.phone).strip()
                    for row in frappe.get_all(
                        "Contact Phone",
                        filters={"parenttype": "Contact", "parent": contact_name},
                        fields=["phone"],
                    )
                }
                if phone_values & existing_phones:
                    return contact_name
            if email_values:
                existing_emails = {
                    cstr(row.email_id).strip().lower()
                    for row in frappe.get_all(
                        "Contact Email",
                        filters={"parenttype": "Contact", "parent": contact_name},
                        fields=["email_id"],
                    )
                }
                if email_values & existing_emails:
                    return contact_name
            if first_name:
                existing_first = frappe.db.get_value("Contact", contact_name, "first_name")
                if normalize_key(existing_first or "") == first_name:
                    return contact_name
    return None


def _find_existing_group_name(doctype: str, payload: dict, context: dict) -> str | None:
    config = GROUP_LINK_CONFIG[doctype]
    label = _clean_group_label(
        payload.get(config["label_field"])
        or payload.get("name")
    )
    if not label:
        return None

    return _resolve_group_link_value(doctype, label, context)


def _get_existing_by_field(doctype: str, fieldname: str, value: str, context: dict) -> str | None:
    value_text = cstr(value).strip()
    try:
        if fieldname == "name":
            existing = frappe.db.exists(doctype, value_text)
            existing_name = (
                existing
                if isinstance(existing, str)
                else (frappe.db.get_value(doctype, value_text, "name") if existing else None)
            )
        else:
            existing_name = frappe.db.get_value(doctype, {fieldname: value_text}, "name")
    except Exception:
        return None

    if not existing_name:
        return None

    try:
        stored_value = existing_name if fieldname == "name" else frappe.db.get_value(doctype, existing_name, fieldname)
    except Exception:
        stored_value = None

    if not _strict_text_equal(stored_value, value_text):
        return None

    if _context_company(context) and _doctype_has_company_field(doctype, context):
        linked_company = frappe.db.get_value(doctype, existing_name, "company")
        if linked_company and linked_company != _context_company(context):
            return None

    return existing_name


def _strict_text_equal(left, right) -> bool:
    """Case-insensitive but accent-sensitive text equality after Unicode NFC."""
    left_text = unicodedata.normalize("NFC", cstr(left).strip()).casefold()
    right_text = unicodedata.normalize("NFC", cstr(right).strip()).casefold()
    return left_text == right_text


def _existing_name_from_duplicate_exception(
    exc: Exception,
    doctype: str,
    payload: dict,
    unique_key: str | None,
    context: dict,
) -> str | None:
    """Resolve a DuplicateEntryError back to an existing document name.

    This is a safety net for values coming from Excel with visually identical
    but differently-normalised Unicode text. The pre-insert existing check
    should catch most cases; if the database detects a duplicate later, treat it
    as a skipped duplicate for master-data imports instead of stopping the file.
    """
    if _classify_exception(exc) != "DuplicateEntryError":
        return None

    args = getattr(exc, "args", ()) or ()
    if len(args) >= 2 and cstr(args[0]).strip() == doctype:
        duplicate_name = cstr(args[1]).strip()
        if duplicate_name:
            try:
                existing = frappe.db.exists(doctype, duplicate_name)
                existing_name = (
                    existing
                    if isinstance(existing, str)
                    else (frappe.db.get_value(doctype, duplicate_name, "name") if existing else None)
                )
                if existing_name and _strict_text_equal(existing_name, duplicate_name):
                    return existing_name
            except Exception:
                pass

    # MySQL IntegrityError args[0] is the error code (1062), not the doctype.
    # Parse "Duplicate entry 'VALUE' for key 'KEY'" directly from the message.
    for arg in args:
        m = re.search(r"Duplicate entry '(.+?)' for key", cstr(arg))
        if m:
            stored_value = m.group(1).strip()
            try:
                existing = frappe.db.exists(doctype, stored_value)
                if existing:
                    return stored_value if isinstance(existing, str) else frappe.db.get_value(doctype, stored_value, "name")
            except Exception:
                pass
            break

    try:
        existing_name = _find_existing_record_name(doctype, payload, unique_key, context)
        if existing_name:
            return existing_name
    except Exception:
        pass

    for value in _duplicate_candidate_values(payload, doctype, unique_key):
        try:
            existing = frappe.db.exists(doctype, value)
            existing_name = (
                existing
                if isinstance(existing, str)
                else (frappe.db.get_value(doctype, value, "name") if existing else None)
            )
            if existing_name and _strict_text_equal(existing_name, value):
                return existing_name
        except Exception:
            pass
    return None


def _duplicate_candidate_values(payload: dict, doctype: str, unique_key: str | None) -> list[str]:
    fields = []
    if unique_key:
        fields.append(unique_key)
    fields.extend(STRICT_IDENTITY_FIELDS.get(doctype, []))
    fields.extend(MASTER_UNIQUE_FIELDS.get(doctype, []))
    fields.extend(COMMON_LINK_LABEL_FIELDS.get(doctype, []))
    fields.append("name")

    values: list[str] = []
    seen: set[str] = set()
    for fieldname in fields:
        value = cstr(payload.get(fieldname)).strip()
        if not value:
            continue
        key = unicodedata.normalize("NFC", value).casefold()
        if key in seen:
            continue
        seen.add(key)
        values.append(value)
    return values


def _normalise_business_payload(target_doctype: str, payload: dict) -> bool:
    """Apply DCNET import semantics that are stricter than generic ERPNext.

    ``Item`` is master data only in the product catalog import. Prices belong
    in ``Item Price`` and opening quantities belong in stock documents that
    have a real valuation rate.
    """
    if _is_total_payload(payload):
        return False

    if target_doctype == "Item":
        _normalise_item_payload(payload)

    required_label = REQUIRED_MASTER_LABEL_FIELDS.get(target_doctype)
    if required_label and _is_blank(payload.get(required_label)):
        return False

    if target_doctype == "Address":
        return _is_importable_address_payload(payload)

    if target_doctype == "Contact":
        return _is_importable_contact_payload(payload)

    if target_doctype == "Item":
        return True

    if target_doctype == "Item Price":
        return flt(payload.get("price_list_rate")) > 0

    if target_doctype == "Stock Reconciliation":
        items = payload.get("items")
        if not isinstance(items, list):
            return True

        valid_items = []
        for item in items:
            if not isinstance(item, dict):
                continue
            if flt(item.get("qty")) and flt(item.get("valuation_rate")) <= 0:
                continue
            valid_items.append(item)

        payload["items"] = valid_items
        return bool(valid_items)

    return True


def _is_importable_address_payload(payload: dict) -> bool:
    address_line = cstr(payload.get("address_line1")).strip()
    if not address_line:
        return False
    if address_line in {"-", "—", "–"}:
        return False
    if _normalise_match_text(address_line) in {"none", "null", "na", "n a", "khong"}:
        return False
    # Reject pure phone numbers masquerading as addresses
    _cleaned = re.sub(r"[\s\-\.\(\)\+]", "", address_line)
    if re.fullmatch(r"0\d{8,10}|84\d{9,10}|\+84\d{9,10}", _cleaned):
        return False

    links = payload.get("links")
    if isinstance(links, dict):
        links = [links]
    if not isinstance(links, list):
        return False

    for link in links:
        if not isinstance(link, dict):
            continue
        link_doctype = cstr(link.get("link_doctype")).strip()
        link_name = cstr(link.get("link_name")).strip()
        if not link_doctype or not link_name:
            continue
        try:
            if frappe.db.exists(link_doctype, link_name):
                return True
        except Exception:
            continue

    return False


def _is_importable_contact_payload(payload: dict) -> bool:
    if not _contact_payload_has_data(payload):
        return False

    links = payload.get("links")
    if isinstance(links, dict):
        links = [links]
    if not isinstance(links, list):
        return False

    for link in links:
        if not isinstance(link, dict):
            continue
        link_doctype = cstr(link.get("link_doctype")).strip()
        link_name = cstr(link.get("link_name")).strip()
        if not link_doctype or not link_name or "{{" in link_name:
            continue
        try:
            if frappe.db.exists(link_doctype, link_name):
                return True
        except Exception:
            continue

    return False


def _contact_payload_has_data(payload: dict) -> bool:
    if cstr(payload.get("phone")).strip() or cstr(payload.get("mobile_no")).strip():
        return True
    if cstr(payload.get("email_id")).strip():
        return True
    for row in payload.get("phone_nos") or []:
        if isinstance(row, dict) and cstr(row.get("phone")).strip():
            return True
    for row in payload.get("email_ids") or []:
        if isinstance(row, dict) and cstr(row.get("email_id")).strip():
            return True
    return False


def _should_preserve_payload_name(target_doctype: str, payload: dict) -> bool:
    if target_doctype not in PRESERVE_PAYLOAD_NAME_DOCTYPES:
        return False
    name = cstr(payload.get("name")).strip()
    if not name:
        return False
    label_field = "customer_name" if target_doctype == "Customer" else "supplier_name"
    return bool(cstr(payload.get(label_field)).strip())


def _is_total_payload(payload: dict) -> bool:
    for value in payload.values():
        if isinstance(value, (list, dict)):
            continue
        value_norm = _normalise_match_text(value)
        if value_norm in {"tong", "tong cong", "total", "cong"}:
            return True
    return False


def _make_link_context(import_doc, dry_run: bool = False) -> dict:
    return {
        "company": getattr(import_doc, "company", None),
        "dry_run": dry_run,
        "actions": [],
        "candidate_cache": {},
        "doctype_exists_cache": {},
        "exists_cache": {},
        "resolved_cache": {},
    }


def _normalise_payload_links(doctype: str, payload: dict, context: dict) -> None:
    """Resolve Link values before Frappe validates them.

    AI plans often use human labels such as ``KHO HÀ NỘI`` while ERPNext
    stores the actual Warehouse name as ``KHO HÀ NỘI - DCNET``.  This pass
    only maps exact names/labels/identity fields; it deliberately avoids
    fuzzy/contains matching so near-duplicate source rows are still imported
    or reported as real validation errors instead of being silently merged.
    """
    if not doctype or not _doctype_exists(doctype, context):
        return

    meta = frappe.get_meta(doctype)
    for df in meta.fields:
        fieldname = df.fieldname
        if not fieldname:
            continue

        if df.fieldtype == "Link" and fieldname in payload:
            resolved = _resolve_link_value(
                df.options,
                payload.get(fieldname),
                context,
                source_doctype=doctype,
                source_field=fieldname,
            )
            payload[fieldname] = resolved
            if fieldname == "company" and resolved:
                context["company"] = resolved
            continue

        if df.fieldtype in TABLE_FIELDTYPES and isinstance(payload.get(fieldname), list):
            child_doctype = df.options
            if not child_doctype or not _doctype_exists(child_doctype, context):
                continue
            for child in payload.get(fieldname) or []:
                if not isinstance(child, dict):
                    continue
                child.setdefault("doctype", child_doctype)
                _normalise_payload_links(child_doctype, child, context)


def _resolve_link_value(
    link_doctype: str | None,
    value: Any,
    context: dict,
    source_doctype: str,
    source_field: str,
) -> Any:
    if not link_doctype or _is_blank(value) or not _doctype_exists(link_doctype, context):
        return value

    value_text = cstr(value).strip()
    if link_doctype == "Account":
        resolved_account = _resolve_account_link_value(value_text, context)
        if resolved_account:
            if resolved_account != value_text:
                context["actions"].append({
                    "type": "mapped",
                    "source_doctype": source_doctype,
                    "source_field": source_field,
                    "link_doctype": link_doctype,
                    "from": value_text,
                    "to": resolved_account,
                    "match_field": "account_number/name",
                    "score": 1.0,
                })
            return resolved_account
        return value

    if link_doctype == "Bank":
        resolved_bank = _resolve_bank_link_value(value_text, context)
        if resolved_bank:
            if resolved_bank != value_text:
                context["actions"].append({
                    "type": "mapped",
                    "source_doctype": source_doctype,
                    "source_field": source_field,
                    "link_doctype": link_doctype,
                    "from": value_text,
                    "to": resolved_bank,
                    "match_field": "bank_name/alias",
                    "score": 1.0,
                })
            return resolved_bank

    if link_doctype in GROUP_LINK_CONFIG:
        resolved_group = _resolve_group_link_value(link_doctype, value_text, context)
        if resolved_group:
            if resolved_group != value_text:
                context["actions"].append({
                    "type": "mapped",
                    "source_doctype": source_doctype,
                    "source_field": source_field,
                    "link_doctype": link_doctype,
                    "from": value_text,
                    "to": resolved_group,
                    "match_field": "group_name",
                    "score": 1.0,
                })
            return resolved_group
        if not context.get("dry_run"):
            created = _create_missing_group(link_doctype, value_text, context)
            if created:
                context["actions"].append({
                    "type": "created",
                    "source_doctype": source_doctype,
                    "source_field": source_field,
                    "link_doctype": link_doctype,
                    "from": value_text,
                    "to": created,
                })
                return created
        return value

    if link_doctype == "Item":
        sanitised_item_code = _sanitise_item_code_value(value_text)
        if sanitised_item_code and sanitised_item_code != value_text and _link_exists("Item", sanitised_item_code, context):
            context["actions"].append({
                "type": "mapped",
                "source_doctype": source_doctype,
                "source_field": source_field,
                "link_doctype": link_doctype,
                "from": value_text,
                "to": sanitised_item_code,
                "match_field": "sanitised_item_code",
                "score": 1.0,
            })
            return sanitised_item_code

    company = _context_company(context)
    cache_key = (link_doctype, value_text, company)
    if cache_key in context["resolved_cache"]:
        return context["resolved_cache"][cache_key]

    if link_doctype == "UOM":
        existing_uom = (
            _get_existing_by_field("UOM", "name", value_text, context)
            or _get_existing_by_field("UOM", "uom_name", value_text, context)
        )
        if existing_uom:
            context["resolved_cache"][cache_key] = existing_uom
            return existing_uom
        if not context.get("dry_run"):
            created = _create_missing_uom(value_text, context)
            if created:
                context["actions"].append({
                    "type": "created",
                    "source_doctype": source_doctype,
                    "source_field": source_field,
                    "link_doctype": link_doctype,
                    "from": value_text,
                    "to": created,
                })
                context["resolved_cache"][cache_key] = created
                return created
        context["resolved_cache"][cache_key] = value
        return value

    if link_doctype in STRICT_IDENTITY_DOCTYPES:
        exact_match = _find_strict_identity_link_match(link_doctype, value_text, context)
        if exact_match:
            context["actions"].append({
                "type": "mapped",
                "source_doctype": source_doctype,
                "source_field": source_field,
                "link_doctype": link_doctype,
                "from": value_text,
                "to": exact_match,
                "match_field": "exact_identity",
                "score": 1.0,
            })
            context["resolved_cache"][cache_key] = exact_match
            return exact_match
        context["resolved_cache"][cache_key] = value
        return value

    if _link_exists(link_doctype, value_text, context):
        context["resolved_cache"][cache_key] = value_text
        return value_text

    match = _find_best_link_match(link_doctype, value_text, context)
    if match:
        resolved = match["name"]
        context["actions"].append({
            "type": "mapped",
            "source_doctype": source_doctype,
            "source_field": source_field,
            "link_doctype": link_doctype,
            "from": value_text,
            "to": resolved,
            "match_field": match.get("fieldname"),
            "score": round(match["score"], 3),
        })
        context["resolved_cache"][cache_key] = resolved
        return resolved

    if link_doctype in AUTO_CREATE_LINK_DOCTYPES and not context.get("dry_run"):
        created = _create_missing_link(link_doctype, value_text, context)
        if created:
            context["actions"].append({
                "type": "created",
                "source_doctype": source_doctype,
                "source_field": source_field,
                "link_doctype": link_doctype,
                "from": value_text,
                "to": created,
            })
            context["resolved_cache"][cache_key] = created
            return created

    context["resolved_cache"][cache_key] = value
    return value


def _resolve_account_link_value(value_text: str, context: dict) -> str | None:
    """Resolve Account links without fuzzy matching."""
    value_text = cstr(value_text).strip()
    if not value_text:
        return None

    if _link_exists("Account", value_text, context):
        return value_text

    company = _context_company(context)
    account_number = _account_number_from_reference(value_text)
    if account_number and company:
        try:
            existing = frappe.db.get_value(
                "Account",
                {"account_number": account_number, "company": company},
                "name",
            )
            if existing:
                return existing
        except Exception:
            pass

    # Last exact-name convenience: "1121 - Tiền Việt Nam" + company abbr.
    if company:
        abbr = _account_company_abbr(company)
        if abbr and not value_text.endswith(f" - {abbr}"):
            suffixed = f"{value_text} - {abbr}"
            if _link_exists("Account", suffixed, context):
                return suffixed

    return None


def _resolve_bank_link_value(value_text: str, context: dict) -> str | None:
    value_text = cstr(value_text).strip()
    if not value_text:
        return None

    if _link_exists("Bank", value_text, context):
        return value_text

    for candidate in _bank_candidate_labels(value_text):
        if not candidate:
            continue
        if _link_exists("Bank", candidate, context):
            return candidate
        try:
            existing = frappe.db.get_value("Bank", {"bank_name": candidate}, "name")
            if existing:
                return existing
        except Exception:
            pass

    return None


def _resolve_group_link_value(group_doctype: str, value_text: str, context: dict) -> str | None:
    value_text = _clean_group_label(value_text)
    if not value_text:
        return None

    if _link_exists(group_doctype, value_text, context):
        return value_text

    config = GROUP_LINK_CONFIG[group_doctype]
    try:
        existing = frappe.db.get_value(group_doctype, {config["label_field"]: value_text}, "name")
        if existing:
            return existing
    except Exception:
        pass

    return None


def _link_exists(link_doctype: str, value: str, context: dict) -> bool:
    cache_key = (link_doctype, value, _context_company(context))
    if cache_key in context["exists_cache"]:
        return context["exists_cache"][cache_key]

    existing = frappe.db.exists(link_doctype, value)
    existing_name = (
        existing
        if isinstance(existing, str)
        else (frappe.db.get_value(link_doctype, value, "name") if existing else None)
    )
    exists = bool(existing_name and _strict_text_equal(existing_name, value))
    if exists and _context_company(context) and _doctype_has_company_field(link_doctype, context):
        linked_company = frappe.db.get_value(link_doctype, existing_name, "company")
        exists = not linked_company or linked_company == _context_company(context)

    context["exists_cache"][cache_key] = exists
    return exists


def _find_best_link_match(link_doctype: str, value: str, context: dict) -> dict | None:
    value_text = cstr(value).strip()
    if not value_text:
        return None

    for candidate in _get_link_candidates(link_doctype, context):
        for fieldname in _candidate_fields_for_doctype(link_doctype, context):
            candidate_value = candidate.get(fieldname)
            if _strict_text_equal(candidate_value, value_text):
                return {
                    "name": candidate.get("name"),
                    "fieldname": fieldname,
                    "score": 1.0,
                }
    return None


def _find_strict_identity_link_match(link_doctype: str, value_text: str, context: dict) -> str | None:
    fields = STRICT_IDENTITY_FIELDS.get(
        link_doctype,
        MASTER_UNIQUE_FIELDS.get(link_doctype, []) + COMMON_LINK_LABEL_FIELDS.get(link_doctype, []),
    )
    meta = frappe.get_meta(link_doctype)
    seen_fields: set[str] = set()
    for fieldname in fields:
        if not fieldname or fieldname in seen_fields:
            continue
        seen_fields.add(fieldname)
        if fieldname != "name" and not meta.get_field(fieldname):
            continue
        existing = _get_existing_by_field(link_doctype, fieldname, value_text, context)
        if existing:
            return existing
    return None


def _get_link_candidates(link_doctype: str, context: dict) -> list[dict]:
    company = _context_company(context) if _doctype_has_company_field(link_doctype, context) else None
    cache_key = (link_doctype, company)
    if cache_key in context["candidate_cache"]:
        return context["candidate_cache"][cache_key]

    fields = _candidate_fields_for_doctype(link_doctype, context)
    filters = {}
    if company:
        filters["company"] = company
    if link_doctype == "Warehouse":
        filters["disabled"] = 0

    candidates = frappe.get_all(
        link_doctype,
        fields=fields,
        filters=filters,
        limit_page_length=LINK_CANDIDATE_LIMIT,
    )
    context["candidate_cache"][cache_key] = candidates
    return candidates


def _candidate_fields_for_doctype(link_doctype: str, context: dict) -> list[str]:
    cache_key = ("candidate_fields", link_doctype)
    if cache_key in context:
        return context[cache_key]

    meta = frappe.get_meta(link_doctype)
    fields: list[str] = ["name"]
    fields.extend(COMMON_LINK_LABEL_FIELDS.get(link_doctype, []))

    if getattr(meta, "title_field", None):
        fields.append(meta.title_field)

    for fieldname in cstr(getattr(meta, "search_fields", "")).split(","):
        if fieldname.strip():
            fields.append(fieldname.strip())

    for df in meta.fields:
        if df.fieldtype not in {"Data", "Small Text"}:
            continue
        if (
            getattr(df, "search_index", 0)
            or getattr(df, "in_global_search", 0)
            or df.fieldname.endswith("_name")
        ):
            fields.append(df.fieldname)

    valid_fields: list[str] = []
    for fieldname in fields:
        if fieldname == "name" or meta.get_field(fieldname):
            if fieldname not in valid_fields:
                valid_fields.append(fieldname)

    context[cache_key] = valid_fields
    return valid_fields


def _doctype_has_company_field(doctype: str, context: dict) -> bool:
    cache_key = ("has_company_field", doctype)
    if cache_key in context:
        return bool(context[cache_key])
    try:
        has_company = bool(frappe.get_meta(doctype).get_field("company"))
    except Exception:
        has_company = False
    context[cache_key] = has_company
    return has_company


def _create_missing_link(link_doctype: str, value: str, context: dict) -> str | None:
    if link_doctype == "Asset Category":
        return _create_missing_asset_category(value, context)
    if link_doctype == "Bank":
        return _create_missing_bank(value, context)
    if link_doctype in GROUP_LINK_CONFIG:
        return _create_missing_group(link_doctype, value, context)
    if link_doctype == "Location":
        return _create_missing_location(value, context)
    if link_doctype == "UOM":
        return _create_missing_uom(value, context)
    if link_doctype == "Warehouse":
        return _create_missing_warehouse(value, context)
    return None


def _create_missing_uom(value: str, context: dict) -> str | None:
    value = cstr(value).strip()
    if not value:
        return None

    existing = (
        _get_existing_by_field("UOM", "name", value, context)
        or _get_existing_by_field("UOM", "uom_name", value, context)
    )
    if existing:
        return existing
    collision_existing = _existing_collision_safe_master_name("UOM", value)
    if collision_existing:
        return collision_existing

    uom = frappe.new_doc("UOM")
    uom.uom_name = value
    uom.enabled = 1
    try:
        uom.insert(ignore_permissions=False)
        _clear_link_cache_for_doctype(context, "UOM")
        return uom.name
    except Exception as exc:
        if _classify_exception(exc) != "DuplicateEntryError":
            raise
        exact_existing = (
            _get_existing_by_field("UOM", "name", value, context)
            or _get_existing_by_field("UOM", "uom_name", value, context)
        )
        if exact_existing:
            return exact_existing

        collision_safe_name = (
            _existing_collision_safe_master_name("UOM", value)
            or _collision_safe_master_name("UOM", value)
        )
        if not collision_safe_name:
            raise

        uom = frappe.new_doc("UOM")
        uom.uom_name = collision_safe_name
        uom.enabled = 1
        uom.insert(ignore_permissions=False)
        _clear_link_cache_for_doctype(context, "UOM")
        return uom.name


def _collision_safe_master_name(doctype: str, label: str) -> str | None:
    """Return a deterministic label when DB collation blocks a distinct value.

    Some MariaDB collations treat Vietnamese accent variants as equal for
    unique indexes. Business import logic still needs to keep labels like
    ``bó`` and ``Bộ`` distinct, so auto-created dependency rows get a short
    migration suffix only when the exact label cannot be inserted.
    """
    label = cstr(label).strip()
    if not label:
        return None
    for candidate in _collision_safe_master_candidates(doctype, label):
        try:
            if not frappe.db.exists(doctype, candidate):
                return candidate
        except Exception:
            continue
    return None


def _existing_collision_safe_master_name(doctype: str, label: str) -> str | None:
    for candidate in _collision_safe_master_candidates(doctype, label):
        try:
            existing = frappe.db.exists(doctype, candidate)
            if existing:
                return existing if isinstance(existing, str) else candidate
        except Exception:
            continue
    return None


def _collision_safe_master_candidates(doctype: str, label: str) -> list[str]:
    label = cstr(label).strip()
    if not label:
        return []
    digest = hashlib.sha1(f"{doctype}:{label}".encode("utf-8")).hexdigest()[:6].upper()
    base = re.sub(r"\s+", " ", label).strip()
    return [
        f"{base} - MIG-{digest}",
        f"{base} MIG {digest}",
        f"{base}-{digest}",
    ]


def _recover_uom_collation_duplicate(payload: dict, context: dict) -> str | None:
    value = cstr(
        payload.get("uom_name")
        or payload.get("name")
        or payload.get("uom")
        or payload.get("unit")
        or payload.get("unit_name")
    ).strip()
    if not value:
        return None
    exact_existing = (
        _get_existing_by_field("UOM", "name", value, context)
        or _get_existing_by_field("UOM", "uom_name", value, context)
    )
    if exact_existing:
        return None
    try:
        return _create_missing_uom(value, context)
    except Exception:
        frappe.log_error(frappe.get_traceback(), "Import Auto UOM Collision Recovery Failed")
        return None


def _create_missing_asset_category(value: str, context: dict) -> str | None:
    value = cstr(value).strip()
    if not value:
        return None

    if _link_exists("Asset Category", value, context):
        return value

    existing = frappe.db.get_value("Asset Category", {"asset_category_name": value}, "name")
    if existing:
        return existing

    category = frappe.new_doc("Asset Category")
    category.asset_category_name = value
    category.non_depreciable_category = 1

    fixed_asset_account = _find_asset_category_account("fixed_asset_account", context)
    if fixed_asset_account:
        row = category.append("accounts", {})
        row.company_name = _context_company(context)
        row.fixed_asset_account = fixed_asset_account
        row.accumulated_depreciation_account = _find_asset_category_account(
            "accumulated_depreciation_account",
            context,
        )
        row.depreciation_expense_account = _find_asset_category_account(
            "depreciation_expense_account",
            context,
        )

    # Fresh migration sites may intentionally have no COA yet. We still create
    # the category as a placeholder so Item/Asset rows can be loaded; accounting
    # accounts must be filled after the COA import before submitting assets.
    category.insert(ignore_permissions=False, ignore_mandatory=not bool(fixed_asset_account))
    _clear_link_cache_for_doctype(context, "Asset Category")
    return category.name


def _find_asset_category_account(fieldname: str, context: dict) -> str | None:
    company = _context_company(context)
    if not company:
        return None

    account_types = {
        "fixed_asset_account": ("Fixed Asset",),
        "accumulated_depreciation_account": ("Accumulated Depreciation",),
        "depreciation_expense_account": ("Depreciation",),
    }.get(fieldname, ())
    if not account_types:
        return None

    try:
        return frappe.db.get_value(
            "Account",
            {
                "company": company,
                "is_group": 0,
                "account_type": ["in", account_types],
            },
            "name",
        )
    except Exception:
        return None


def _create_missing_location(value: str, context: dict) -> str | None:
    value = cstr(value).strip()
    if not value:
        return None

    if _link_exists("Location", value, context):
        return value

    existing = frappe.db.get_value("Location", {"location_name": value}, "name")
    if existing:
        return existing

    location = frappe.new_doc("Location")
    location.location_name = value
    location.is_group = 0
    location.insert(ignore_permissions=False)
    _clear_link_cache_for_doctype(context, "Location")
    return location.name


def _ensure_default_cost_center(context: dict) -> str | None:
    company = _context_company(context)
    if not company:
        return None

    existing = _default_asset_cost_center({**context, "dry_run": True})
    if existing:
        return existing

    root_name = _ensure_root_cost_center(context)
    if not root_name:
        return None

    leaf_name = _create_missing_cost_center("Main", context, parent_cost_center=root_name)
    if leaf_name:
        try:
            if not frappe.db.get_value("Company", company, "depreciation_cost_center"):
                frappe.db.set_value("Company", company, "depreciation_cost_center", leaf_name)
        except Exception:
            pass
    return leaf_name


def _ensure_root_cost_center(context: dict) -> str | None:
    company = _context_company(context)
    if not company:
        return None

    try:
        existing_root = frappe.db.get_value(
            "Cost Center",
            {"company": company, "cost_center_name": company, "is_group": 1},
            "name",
        )
        if existing_root:
            return existing_root
    except Exception:
        pass

    root = frappe.new_doc("Cost Center")
    root.cost_center_name = company
    root.company = company
    root.is_group = 1
    root.disabled = 0
    root.insert(ignore_permissions=False, ignore_mandatory=True)
    _clear_link_cache_for_doctype(context, "Cost Center")
    return root.name


def _create_missing_cost_center(
    value: str,
    context: dict,
    parent_cost_center: str | None = None,
) -> str | None:
    value = cstr(value).strip()
    company = _context_company(context)
    if not value or not company:
        return None

    if _link_exists("Cost Center", value, context):
        return value

    existing = frappe.db.get_value(
        "Cost Center",
        {"company": company, "cost_center_name": value},
        "name",
    )
    if existing:
        return existing

    if not parent_cost_center and value != company:
        parent_cost_center = _ensure_root_cost_center(context)

    cost_center = frappe.new_doc("Cost Center")
    cost_center.cost_center_name = value
    cost_center.company = company
    cost_center.disabled = 0
    cost_center.is_group = 1 if value == company and not parent_cost_center else 0
    if parent_cost_center:
        cost_center.parent_cost_center = parent_cost_center
    cost_center.insert(ignore_permissions=False)
    _clear_link_cache_for_doctype(context, "Cost Center")
    return cost_center.name


def _create_missing_group(group_doctype: str, label: str, context: dict) -> str | None:
    config = GROUP_LINK_CONFIG.get(group_doctype)
    if not config:
        return None

    label = _clean_group_label(label)
    if not label:
        return None

    if _link_exists(group_doctype, label, context):
        return label

    existing = _resolve_group_link_value(group_doctype, label, context)
    if existing:
        return existing

    root_name = cstr(config.get("root")).strip()
    root_norm = _normalise_match_text(root_name)
    label_norm = _normalise_match_text(label)

    if root_name and root_norm and label_norm == root_norm:
        root = frappe.new_doc(group_doctype)
        setattr(root, config["label_field"], root_name)
        if config.get("parent_field"):
            setattr(root, config["parent_field"], None)
        if hasattr(root, "is_group"):
            root.is_group = 1
        root.insert(ignore_permissions=False)
        _clear_link_cache_for_doctype(context, group_doctype)
        return root.name

    if root_name and config.get("parent_field") and not _link_exists(group_doctype, root_name, context):
        _create_missing_group(group_doctype, root_name, context)

    group = frappe.new_doc(group_doctype)
    setattr(group, config["label_field"], label)
    if config.get("parent_field") and root_name:
        setattr(group, config["parent_field"], root_name)
    if hasattr(group, "is_group"):
        group.is_group = 0
    group.insert(ignore_permissions=False)
    _clear_link_cache_for_doctype(context, group_doctype)
    return group.name


def _clean_group_label(value) -> str:
    if value in (None, ""):
        return ""
    label = cstr(value).strip()
    if not label or label in {"-", "—", "–"}:
        return ""
    if _normalise_match_text(label) in {"none", "null", "na", "n a", "khong"}:
        return ""
    return label


def _create_missing_bank(bank_label: str, context: dict) -> str | None:
    for candidate in _bank_candidate_labels(bank_label):
        if not candidate:
            continue
        if _link_exists("Bank", candidate, context):
            return candidate
        try:
            existing = frappe.db.get_value("Bank", {"bank_name": candidate}, "name")
            if existing:
                return existing
        except Exception:
            pass

        bank = frappe.new_doc("Bank")
        bank.bank_name = candidate
        bank.insert(ignore_permissions=False)
        _clear_link_cache_for_doctype(context, "Bank")
        return bank.name

    return None


def _bank_candidate_labels(value: str) -> list[str]:
    labels: list[str] = []
    alias = _bank_alias_from_text(value)
    if alias:
        labels.append(alias)

    base = _strip_bank_branch_suffix(value)
    if base:
        labels.append(base)

    raw = cstr(value).strip()
    if raw:
        labels.append(raw)

    deduped: list[str] = []
    for label in labels:
        label = cstr(label).strip()
        if label and label not in deduped:
            deduped.append(label)
    return deduped


def _bank_alias_from_text(value: str) -> str | None:
    text = _normalise_match_text(value)
    aliases = [
        ("dong nam a", "SeABank"),
        ("phuong dong", "OCB"),
        ("hang hai", "MSB"),
        ("sai gon thuong tin", "Sacombank"),
        ("viet nam thinh vuong", "VPBank"),
        ("thinh vuong va phat trien", "PG Bank"),
        ("quoc te viet nam", "VIB"),
        ("quan doi", "MB"),
        ("dau tu va phat trien", "BIDV"),
        ("nong nghiep", "Agribank"),
        ("a chau", "ACB"),
        ("xuat nhap khau", "Eximbank"),
        ("ky thuong", "Techcombank"),
        ("sai gon ha noi", "SHB"),
        ("phat trien nha", "HDBank"),
        ("ban viet", "BVBANK"),
        ("dong a", "DongA Bank"),
    ]
    for marker, alias in aliases:
        if marker in text:
            return alias
    return None


def _strip_bank_branch_suffix(value: str) -> str:
    label = cstr(value).strip()
    if not label:
        return ""
    return re.split(
        r"\s+-\s+(?:CN|PGD|CHI NH[ÁA]NH|PH[ÒO]NG GIAO D[ỊI]CH)\b",
        label,
        maxsplit=1,
        flags=re.IGNORECASE,
    )[0].strip()


def _create_missing_warehouse(warehouse_label: str, context: dict) -> str | None:
    company = _resolve_company(_context_company(context), context)
    if not company:
        return None

    warehouse_name = _strip_company_suffix(warehouse_label, company)
    expected_name = _warehouse_docname(warehouse_name, company)
    if expected_name and _link_exists("Warehouse", expected_name, context):
        return expected_name

    warehouse = frappe.new_doc("Warehouse")
    warehouse.warehouse_name = warehouse_name
    warehouse.company = company
    warehouse.is_group = 0
    parent_warehouse = _default_parent_warehouse(company)
    if parent_warehouse and parent_warehouse != expected_name:
        warehouse.parent_warehouse = parent_warehouse
    warehouse.insert(ignore_permissions=False)
    _clear_link_cache_for_doctype(context, "Warehouse")
    return warehouse.name


def _resolve_company(company: str | None, context: dict) -> str | None:
    if not company:
        return None
    if frappe.db.exists("Company", company):
        return company

    match = _find_best_link_match("Company", company, context)
    if match:
        return match["name"]
    return None


def _strip_company_suffix(value: str, company: str) -> str:
    warehouse_name = cstr(value).strip()
    abbr = frappe.db.get_value("Company", company, "abbr")
    if abbr:
        suffix = f" - {abbr}"
        if warehouse_name.endswith(suffix):
            warehouse_name = warehouse_name[: -len(suffix)].strip()
    return warehouse_name


def _warehouse_docname(warehouse_name: str, company: str) -> str | None:
    abbr = frappe.db.get_value("Company", company, "abbr")
    if not abbr:
        return None
    suffix = f" - {abbr}"
    return warehouse_name if warehouse_name.endswith(suffix) else f"{warehouse_name}{suffix}"


def _default_parent_warehouse(company: str) -> str | None:
    abbr = frappe.db.get_value("Company", company, "abbr")
    if abbr:
        root_name = f"All Warehouses - {abbr}"
        if frappe.db.exists("Warehouse", root_name):
            return root_name

    root = frappe.get_all(
        "Warehouse",
        fields=["name"],
        filters={"company": company, "is_group": 1, "disabled": 0},
        order_by="lft asc",
        limit_page_length=1,
    )
    return root[0].name if root else None


def _normalise_match_text(value: Any) -> str:
    text = cstr(value).strip()
    if not text:
        return ""
    text = unicodedata.normalize("NFKD", text)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    text = text.replace("đ", "d").replace("Đ", "D")
    text = text.casefold()
    text = re.sub(r"[-_/]+", " ", text)
    text = re.sub(r"[^\w\s]", " ", text, flags=re.UNICODE)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _context_company(context: dict) -> str | None:
    company = context.get("company")
    return cstr(company).strip() if company else None


def _is_blank(value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, str) and not value.strip():
        return True
    return False


def _doctype_exists(doctype: str, context: dict) -> bool:
    cache = context["doctype_exists_cache"]
    if doctype not in cache:
        cache[doctype] = bool(frappe.db.exists("DocType", doctype))
    return cache[doctype]


def _clear_link_cache_for_doctype(context: dict, doctype: str) -> None:
    for cache_name in ("candidate_cache", "exists_cache", "resolved_cache"):
        cache = context.get(cache_name) or {}
        for key in list(cache):
            if isinstance(key, tuple) and key and key[0] == doctype:
                cache.pop(key, None)


def _link_resolution_summary(context: dict, start_index: int) -> dict:
    actions = context["actions"][start_index:]
    return {
        "count": len(actions),
        "sample": actions[:20],
    }


def _classify_exception(exc: Exception) -> str:
    """Map a Frappe / Python exception to a stable string identifier the AI
    fixer can branch on. Falls back to the class name."""
    if _looks_like_duplicate_exception(exc):
        return "DuplicateEntryError"

    try:
        import frappe
        mapping = (
            ("MandatoryError", getattr(frappe, "MandatoryError", None)),
            ("LinkValidationError", getattr(frappe, "LinkValidationError", None)),
            ("DuplicateEntryError", getattr(frappe, "DuplicateEntryError", None)),
            ("ValidationError", getattr(frappe, "ValidationError", None)),
            ("PermissionError", getattr(frappe, "PermissionError", None)),
        )
        for label, klass in mapping:
            if klass and isinstance(exc, klass):
                return label
    except Exception:
        pass
    return exc.__class__.__name__


def _looks_like_duplicate_exception(exc: Exception) -> bool:
    """Detect duplicate-key errors even when Frappe wraps the DB exception."""
    try:
        if getattr(frappe, "DuplicateEntryError", None) and isinstance(exc, frappe.DuplicateEntryError):
            return True
    except Exception:
        pass

    text_parts = [exc.__class__.__name__, cstr(exc)]
    for arg in getattr(exc, "args", ()) or ():
        text_parts.append(cstr(arg))
        text_parts.append(arg.__class__.__name__)
        for nested in getattr(arg, "args", ()) or ():
            text_parts.append(cstr(nested))

    text = " ".join(part for part in text_parts if part).lower()
    return (
        "duplicate entry" in text
        or "duplicateentryerror" in text
        or "integrityerror(1062" in text
        or "1062" in text and "primary" in text
    )


# ---------------------------------------------------------------------------
# Auto-create missing link master docs before insert (Frappe validates links
# before any hook runs, so we must pre-create them here, not in a hook).
# ---------------------------------------------------------------------------

_DEFAULT_DATE_OF_JOINING = "2026-01-01"


def _normalize_employee_fields(doc) -> None:
    """Fix mandatory Employee fields that migration data often leaves blank."""
    # first_name: split full name — first word = họ, rest = tên
    if not doc.get("first_name"):
        full = (doc.get("employee_name") or "").strip()
        if full:
            parts = full.split(None, 1)  # split on first whitespace
            doc.first_name = parts[0]
            if len(parts) > 1:
                doc.last_name = parts[1]
        else:
            doc.first_name = "?"

    # date_of_joining: mandatory in ERPNext — use default if absent
    if not doc.get("date_of_joining"):
        doc.date_of_joining = _DEFAULT_DATE_OF_JOINING

    # date_of_birth: not mandatory but set placeholder so it's clear it's unknown
    if not doc.get("date_of_birth"):
        doc.date_of_birth = "1900-01-01"


_LINK_AUTO_CREATE: dict[str, dict] = {
    # doctype → {field_on_parent: (link_doctype, name_field)}
    "Employee": {
        "designation": ("Designation", "designation_name"),
        "department": ("Department", "department_name"),
        "branch": ("Branch", "branch"),
        "employment_type": ("Employment Type", "employment_type"),
        "grade": ("Employee Grade", "grade_name"),
    },
}

# Normalize field values that have Vietnamese aliases → ERPNext standard names
_FIELD_VALUE_MAP: dict[str, dict[str, dict[str, str]]] = {
    "Employee": {
        "gender": {
            "nam": "Male",
            "nữ": "Female",
            "nu": "Female",
            "female": "Female",
            "male": "Male",
            "khác": "Other",
            "other": "Other",
        },
    },
}


def _auto_create_missing_link_masters(doc) -> None:
    """Normalize known field values and auto-create missing Link docs before
    insert so that Frappe's _validate_links() doesn't reject them."""
    # Step 1: normalize field values (e.g. "Nam" → "Male")
    norm_rules = _FIELD_VALUE_MAP.get(doc.doctype, {})
    for field, value_map in norm_rules.items():
        raw = doc.get(field)
        if not raw:
            continue
        normalized = value_map.get(raw.strip().lower())
        if normalized and normalized != raw:
            doc.set(field, normalized)

    # Step 2: doctype-specific field normalization
    if doc.doctype == "Employee":
        _normalize_employee_fields(doc)

    # Step 2: auto-create missing Link master docs
    rules = _LINK_AUTO_CREATE.get(doc.doctype)
    if not rules:
        return
    for field, (link_doctype, name_field) in rules.items():
        value = doc.get(field)
        if not value:
            continue
        if frappe.db.exists(link_doctype, value):
            continue
        try:
            frappe.get_doc({
                "doctype": link_doctype,
                name_field: value,
            }).insert(ignore_permissions=True, ignore_if_duplicate=True)
        except Exception:
            frappe.log_error(
                frappe.get_traceback(),
                f"Auto-create {link_doctype}: {value}",
            )
