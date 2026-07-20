"""Quick Detail Frame — server endpoints.

Two whitelisted methods:

- get_frame_data(doctype, name, child_field=None)
    Resolve the focal child table for a parent document and return:
    parent meta + child rows + per-cell editable matrix.

- set_cell(parent_doctype, parent_name, child_doctype, row_name,
          fieldname, value, version)
    Apply a single-cell edit with optimistic lock, full Frappe
    permission rules, validate() trigger, and parent.save().

Spec: docs/specs/2026-05-13-quick-detail-frame-design.md  section 5.4.
Feedback origin: FB-2026-00601.
"""

from __future__ import annotations

import json
from typing import Any

import frappe
from frappe import _

__all__ = ["get_frame_data", "get_frame_batch", "set_cell", "resolve_child_field", "get_boot_payload"]


# Built-in registry — kept in Python (single source of truth) and also
# emitted to client via boot.dcnet_qdf so the JS bundle can resolve
# without a round-trip on toggle-on.
REGISTRY: dict[str, str] = {
    # Bán hàng
    "Sales Invoice": "items",
    "Sales Order": "items",
    "Delivery Note": "items",
    "Quotation": "items",
    # Mua hàng
    "Purchase Invoice": "items",
    "Purchase Order": "items",
    "Purchase Receipt": "items",
    "Supplier Quotation": "items",
    "Material Request": "items",
    # Kho
    "Stock Entry": "items",
    "Pick List": "locations",
    "Stock Reconciliation": "items",
    # Tài chính
    "Journal Entry": "accounts",
    "Payment Entry": "references",
    "Bank Transaction": "payment_entries",
    "Expense Claim": "expenses",
    # Tài sản
    "Asset Movement": "assets",
    # HR
    "Salary Slip": "earnings",
    # CRM
    "Opportunity": "items",
}

# Per-DocType default label fields for the frame header bar.
# Fallback below picks (title_field, status, first currency field).
LABEL_FIELDS: dict[str, list[str]] = {
    "Sales Invoice": ["customer_name", "status", "grand_total"],
    "Purchase Invoice": ["supplier_name", "status", "grand_total"],
    "Sales Order": ["customer_name", "status", "grand_total"],
    "Purchase Order": ["supplier_name", "status", "grand_total"],
    "Delivery Note": ["customer_name", "status", "grand_total"],
    "Purchase Receipt": ["supplier_name", "status", "grand_total"],
    "Quotation": ["party_name", "status", "grand_total"],
    "Supplier Quotation": ["supplier", "status", "grand_total"],
    "Material Request": ["material_request_type", "status", "transaction_date"],
    "Stock Entry": ["stock_entry_type", "posting_date", "total_amount"],
    "Pick List": ["purpose", "status", "company"],
    "Stock Reconciliation": ["purpose", "posting_date", "difference_amount"],
    "Journal Entry": ["voucher_type", "posting_date", "total_debit"],
    "Payment Entry": ["party_name", "payment_type", "paid_amount"],
    "Bank Transaction": ["date", "party", "deposit"],
    "Expense Claim": ["employee_name", "approval_status", "total_claimed_amount"],
    "Asset Movement": ["purpose", "transaction_date", "company"],
    "Salary Slip": ["employee_name", "status", "net_pay"],
    "Opportunity": ["customer_name", "status", "opportunity_amount"],
}


# ───────────────────────────────────────────────────────────────────────────────
# Public endpoints
# ───────────────────────────────────────────────────────────────────────────────


@frappe.whitelist()
def get_frame_data(doctype: str, name: str, child_field: str | None = None) -> dict:
    """Load focal child table + per-cell editable matrix for one parent doc.

    Returns dict per spec §5.4. Errors raised as Frappe permission/validation
    errors so client sees standard 4xx response bodies.
    """
    if not doctype or not name:
        frappe.throw(_("Thiếu doctype hoặc name"), frappe.ValidationError)

    # Doctype-level read permission. Soft return so client can show a friendly
    # message in the frame body instead of a stacked error popup.
    if not frappe.has_permission(doctype, "read"):
        return {
            "parent": None,
            "child": None,
            "reason": _("Bạn không có quyền xem {0}").format(doctype),
        }

    # Quick existence check via DB (cheap, no perm side effect) so that we can
    # return a soft 404 instead of letting `frappe.get_doc` raise.
    if not frappe.db.exists(doctype, name):
        return {
            "parent": None,
            "child": None,
            "reason": _("Không tìm thấy chứng từ {0}/{1}.").format(doctype, name),
        }

    try:
        parent = frappe.get_doc(doctype, name)
    except frappe.DoesNotExistError:
        return {
            "parent": None,
            "child": None,
            "reason": _("Không tìm thấy chứng từ {0}/{1}.").format(doctype, name),
        }

    if not parent.has_permission("read"):
        return {
            "parent": None,
            "child": None,
            "reason": _("Bạn không có quyền xem chứng từ này"),
        }

    resolved_field = child_field or resolve_child_field(doctype, parent)

    parent_label = _build_parent_header(parent)

    if not resolved_field:
        return {
            "parent": parent_label,
            "child": None,
            "reason": _("DocType này không có bảng con phù hợp để xem nhanh"),
        }

    field_meta = parent.meta.get_field(resolved_field)
    if not field_meta or field_meta.fieldtype != "Table":
        return {
            "parent": parent_label,
            "child": None,
            "reason": _("Field {0} không phải bảng con").format(resolved_field),
        }

    child_doctype = field_meta.options
    rows_raw = parent.get(resolved_field) or []
    child_meta = frappe.get_meta(child_doctype)

    fields = _serialize_child_fields(child_meta)
    rows = _serialize_child_rows(
        rows_raw, child_meta, fields, parent_docstatus=parent.docstatus
    )

    return {
        "parent": parent_label,
        "child": {
            "table_field": resolved_field,
            "doctype": child_doctype,
            "fields": fields,
            "rows": rows,
        },
    }


@frappe.whitelist()
def get_frame_batch(pairs):
    """Bulk variant of get_frame_data for viewport prefetch.

    pairs: JSON-encoded list of {doctype, name} dicts. Cap 20 per call.
    Returns a dict keyed by "<doctype>::<name>" → same payload shape as
    `get_frame_data` (or {parent: None, reason: ...} on per-pair failure).
    Per-pair errors don't fail the whole batch — the client can decide what
    to do with each entry.
    """
    if isinstance(pairs, str):
        try:
            pairs = json.loads(pairs)
        except json.JSONDecodeError:
            frappe.throw(_("pairs phải là JSON list"), frappe.ValidationError)
    if not isinstance(pairs, list):
        frappe.throw(_("pairs phải là list"), frappe.ValidationError)
    if len(pairs) > 20:
        frappe.throw(_("Tối đa 20 doc / lần"), frappe.ValidationError)

    out: dict[str, dict] = {}
    for p in pairs:
        doctype = (p or {}).get("doctype")
        name = (p or {}).get("name")
        if not doctype or not name:
            continue
        key = f"{doctype}::{name}"
        try:
            out[key] = get_frame_data(doctype, name)
        except Exception as e:
            out[key] = {
                "parent": None,
                "child": None,
                "reason": str(e),
            }
    return out


@frappe.whitelist()
def set_cell(
    parent_doctype: str,
    parent_name: str,
    child_doctype: str,
    row_name: str,
    fieldname: str,
    value: Any,
    version: str,
) -> dict:
    """Apply a single cell edit with optimistic lock + Frappe permission stack.

    On success returns new version + refreshed parent label fields + refreshed
    row data. On conflict (409-equivalent) raises a tagged exception so the
    client can reload the frame. Permission/validation errors raise the usual
    Frappe exceptions.
    """
    if not all([parent_doctype, parent_name, child_doctype, row_name, fieldname, version]):
        frappe.throw(_("Thiếu tham số bắt buộc"), frappe.ValidationError)

    if not frappe.has_permission(parent_doctype, "write"):
        frappe.throw(
            _("Bạn không có quyền sửa {0}").format(parent_doctype),
            frappe.PermissionError,
        )

    # Optimistic lock: compare against client's `version` token (parent.modified).
    current_modified = frappe.db.get_value(parent_doctype, parent_name, "modified")
    if not current_modified:
        frappe.throw(
            _("Chứng từ không tồn tại hoặc đã bị xoá"),
            frappe.DoesNotExistError,
        )
    if str(current_modified) != str(version):
        frappe.throw(
            _("Chứng từ đã được cập nhật bởi người khác. Tải lại để xem dữ liệu mới."),
            StaleVersionError,
        )

    parent = frappe.get_doc(parent_doctype, parent_name)
    if not parent.has_permission("write"):
        frappe.throw(
            _("Bạn không có quyền sửa chứng từ này"),
            frappe.PermissionError,
        )

    # Find the child row + verify the field is editable for this row × docstatus.
    child_meta = frappe.get_meta(child_doctype)
    field_meta = child_meta.get_field(fieldname)
    if not field_meta:
        frappe.throw(
            _("Field {0} không tồn tại trên {1}").format(fieldname, child_doctype),
            frappe.ValidationError,
        )

    target_row = None
    for row in (parent.get(_find_child_field_on_parent(parent, child_doctype)) or []):
        if row.name == row_name:
            target_row = row
            break
    if not target_row:
        frappe.throw(
            _("Dòng {0} không tồn tại trên {1}").format(row_name, parent_name),
            frappe.DoesNotExistError,
        )

    editable = _is_cell_editable(
        field_meta=field_meta,
        row=target_row,
        parent_docstatus=parent.docstatus,
        parent=parent,
    )
    if not editable:
        frappe.throw(
            _("Ô này không thể sửa ở trạng thái hiện tại"),
            frappe.PermissionError,
        )

    # Coerce value to the right Python type (mostly handled by Frappe save, but
    # JSON-decoded numbers may arrive as int when a Float is expected — that's
    # fine; Frappe will normalize).
    target_row.set(fieldname, value)

    # Re-run validate so Frappe formula fields (qty * rate → amount) recompute.
    parent.run_method("validate")
    parent.save()
    frappe.db.commit()

    new_modified = frappe.db.get_value(parent_doctype, parent_name, "modified")
    parent_refresh = frappe.get_doc(parent_doctype, parent_name)
    refreshed_row = None
    for row in (parent_refresh.get(_find_child_field_on_parent(parent_refresh, child_doctype)) or []):
        if row.name == row_name:
            refreshed_row = row
            break

    return {
        "ok": True,
        "new_version": str(new_modified),
        "parent_label_fields": _build_parent_header(parent_refresh)["label_fields"],
        "parent_docstatus": parent_refresh.docstatus,
        "row": refreshed_row.as_dict() if refreshed_row else None,
    }


# ───────────────────────────────────────────────────────────────────────────────
# Resolution helpers
# ───────────────────────────────────────────────────────────────────────────────


def resolve_child_field(doctype: str, parent_doc: Any | None = None) -> str | None:
    """Resolve the focal child table per spec §4:
    Settings override → Registry → Heuristic → Fallback first child with rows.
    """
    override = _get_override(doctype)
    if override:
        return override

    if doctype in REGISTRY:
        return REGISTRY[doctype]

    heuristic = _heuristic_pick(doctype)
    if heuristic:
        return heuristic

    if parent_doc is not None:
        return _first_child_with_rows(parent_doc)

    return _first_child_field(doctype)


def _get_override(doctype: str) -> str | None:
    overrides = _cached_overrides()
    return overrides.get(doctype)


def _cached_overrides() -> dict[str, str]:
    cached = frappe.cache.get_value("dcnet_qdf_overrides")
    if cached is not None:
        return cached

    overrides: dict[str, str] = {}
    if frappe.db.exists("DocType", "Quick Detail Frame Settings"):
        try:
            settings = frappe.get_single("Quick Detail Frame Settings")
            if settings.enabled:
                for row in settings.mappings or []:
                    if row.parent_doctype and row.child_field:
                        overrides[row.parent_doctype] = row.child_field
        except Exception:
            pass

    frappe.cache.set_value("dcnet_qdf_overrides", overrides)
    return overrides


def _heuristic_pick(doctype: str) -> str | None:
    """Scan child tables of `doctype`; return the one whose field signature
    scores highest, or None.
    """
    try:
        meta = frappe.get_meta(doctype)
    except Exception:
        return None

    best_field = None
    best_score = 0

    for df in meta.fields:
        if df.fieldtype != "Table" or not df.options:
            continue
        try:
            child_meta = frappe.get_meta(df.options)
        except Exception:
            continue

        field_names = {f.fieldname for f in child_meta.fields}
        score = 0
        if "item_code" in field_names:
            score += 10
        if "account" in field_names and (
            "debit_in_account_currency" in field_names
            or "credit_in_account_currency" in field_names
        ):
            score += 10
        if "reference_doctype" in field_names and "reference_name" in field_names:
            score += 8
        if "expense_type" in field_names:
            score += 5
        if "qty" in field_names and "rate" in field_names:
            score += 3

        if score > best_score:
            best_score = score
            best_field = df.fieldname

    return best_field if best_score >= 3 else None


def _first_child_with_rows(parent_doc: Any) -> str | None:
    for df in parent_doc.meta.fields:
        if df.fieldtype != "Table":
            continue
        rows = parent_doc.get(df.fieldname) or []
        if rows:
            return df.fieldname
    return None


def _first_child_field(doctype: str) -> str | None:
    try:
        meta = frappe.get_meta(doctype)
    except Exception:
        return None
    for df in meta.fields:
        if df.fieldtype == "Table":
            return df.fieldname
    return None


# ───────────────────────────────────────────────────────────────────────────────
# Serialization
# ───────────────────────────────────────────────────────────────────────────────


# Fieldtypes worth showing as columns in the frame. Long-form types are
# excluded (frame is meant for at-a-glance scanning).
_DISPLAYABLE_FIELDTYPES = {
    "Data", "Link", "Dynamic Link", "Select", "Date", "Datetime", "Time",
    "Int", "Float", "Currency", "Percent", "Check", "Small Text",
}

_SKIP_FIELDS = {"idx", "parent", "parenttype", "parentfield", "owner",
                "creation", "modified", "modified_by", "docstatus"}


def _serialize_child_fields(child_meta: Any) -> list[dict]:
    """Pick fields to display in the frame.

    Strategy:
    1. Prefer fields with `in_list_view=1` on the child DocType (matches the
       columns shown when ERPNext expands the child grid on the form).
    2. If none flagged, fall back to first 6 displayable fields.
    """
    candidates: list[dict] = []
    for df in child_meta.fields:
        if df.fieldname in _SKIP_FIELDS:
            continue
        if df.fieldtype not in _DISPLAYABLE_FIELDTYPES:
            continue
        if df.hidden:
            continue
        candidates.append(df)

    listview_fields = [df for df in candidates if int(df.in_list_view or 0)]
    chosen = listview_fields if listview_fields else candidates[:6]

    return [
        {
            "fieldname": df.fieldname,
            "label": df.label or df.fieldname,
            "fieldtype": df.fieldtype,
            "options": df.options,
            "precision": getattr(df, "precision", None),
            "allow_on_submit": int(df.allow_on_submit or 0),
            "read_only": int(df.read_only or 0),
            "permlevel": int(df.permlevel or 0),
            "read_only_depends_on": getattr(df, "read_only_depends_on", None) or "",
            "reqd": int(df.reqd or 0),
            "columns": int(getattr(df, "columns", 0) or 0),
        }
        for df in chosen
    ]


def _serialize_child_rows(
    rows: list, child_meta: Any, fields: list[dict], parent_docstatus: int
) -> list[dict]:
    out = []
    for row in rows:
        row_dict: dict[str, Any] = {
            "name": row.name,
            "idx": row.idx,
        }
        editable: dict[str, bool] = {}
        for fdesc in fields:
            fn = fdesc["fieldname"]
            row_dict[fn] = row.get(fn)
            field_meta = child_meta.get_field(fn)
            editable[fn] = _is_cell_editable(
                field_meta=field_meta,
                row=row,
                parent_docstatus=parent_docstatus,
                parent=None,
            )
        row_dict["__editable"] = editable
        out.append(row_dict)
    return out


def _is_cell_editable(
    field_meta: Any, row: Any, parent_docstatus: int, parent: Any | None
) -> bool:
    """Evaluate per-cell editability against full Frappe rules.

    Order of checks (cheap → expensive):
      1. docstatus 2 (Cancelled) → never editable
      2. field.read_only → never editable
      3. docstatus 1 + not allow_on_submit → not editable
      4. read_only_depends_on (formula) → may lock
      5. permlevel + user write perm at that permlevel → may lock
    """
    if parent_docstatus == 2:
        return False
    if int(field_meta.read_only or 0):
        return False
    if parent_docstatus == 1 and not int(field_meta.allow_on_submit or 0):
        return False

    ro_depends = getattr(field_meta, "read_only_depends_on", None)
    if ro_depends:
        try:
            from frappe.utils.safe_exec import safe_eval
            expr = ro_depends
            if expr.startswith("eval:"):
                expr = expr[5:]
            ctx = {"doc": row}
            if safe_eval(expr, eval_locals=ctx):
                return False
        except Exception:
            pass

    permlevel = int(field_meta.permlevel or 0)
    if permlevel > 0 and parent is not None:
        if not parent.has_permlevel_access_to(field_meta.fieldname, df=field_meta, permission_type="write"):
            return False

    return True


def _build_parent_header(parent: Any) -> dict:
    doctype = parent.doctype
    label_fieldnames = LABEL_FIELDS.get(doctype) or _fallback_label_fields(parent.meta)
    label_fields: dict[str, Any] = {}
    for fn in label_fieldnames:
        val = parent.get(fn)
        if val is not None:
            label_fields[fn] = val

    return {
        "name": parent.name,
        "doctype": doctype,
        "docstatus": parent.docstatus,
        "modified": str(parent.modified),
        "label_fields": label_fields,
        "form_url": f"/app/{frappe.scrub(doctype).replace('_', '-')}/{parent.name}",
    }


def _fallback_label_fields(meta: Any) -> list[str]:
    out: list[str] = []
    if meta.title_field:
        out.append(meta.title_field)
    if "status" in {f.fieldname for f in meta.fields}:
        out.append("status")
    for df in meta.fields:
        if df.fieldtype in ("Currency", "Float"):
            out.append(df.fieldname)
            break
    return out[:3]


def _find_child_field_on_parent(parent: Any, child_doctype: str) -> str | None:
    for df in parent.meta.fields:
        if df.fieldtype == "Table" and df.options == child_doctype:
            return df.fieldname
    return None


# ───────────────────────────────────────────────────────────────────────────────
# Boot data — emitted via dcnet_theme.boot.boot_session
# ───────────────────────────────────────────────────────────────────────────────


def get_boot_payload() -> dict:
    """Called from boot_session to populate frappe.boot.dcnet_qdf.

    `enabled` defaults to True; explicit False only when the Settings Single
    doc has been saved with enabled=0. Uninitialized Single doc → True.
    """
    enabled = True
    if frappe.db.exists("DocType", "Quick Detail Frame Settings"):
        try:
            raw = frappe.db.get_single_value("Quick Detail Frame Settings", "enabled")
            # raw is None when Single doc has no row yet; treat as default-on.
            if raw is not None:
                enabled = bool(int(raw))
        except Exception:
            enabled = True

    return {
        "enabled": enabled,
        "registry": REGISTRY,
        "label_fields": LABEL_FIELDS,
        "overrides": _cached_overrides(),
    }


# ───────────────────────────────────────────────────────────────────────────────
# Error classes
# ───────────────────────────────────────────────────────────────────────────────


class StaleVersionError(frappe.ValidationError):
    """Raised when client's optimistic-lock token does not match server state."""
    http_status_code = 409
