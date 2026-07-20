import json
import os
import re

import frappe
from frappe import _
from frappe.utils import cint, flt, now_datetime
from frappe.utils.xlsxutils import make_xlsx

from dcnet_crm.install import CRM_PAGE_ROLES, CRM_SALES_STAGE_PROBABILITY


def _set_if(doc, data, field, src_key=None):
    """Set doc.field from data[src_key] if value is truthy."""
    value = data.get(src_key or field)
    if value:
        setattr(doc, field, value)


RESOURCE_CONFIG = {
    "leads": {
        "doctype": "Lead",
        "title_field": "lead_name",
        "search_fields": ["name", "lead_name", "email_id", "phone", "mobile_no", "company_name"],
        "fields": [
            "name", "lead_name", "first_name", "last_name", "salutation",
            "status", "email_id", "phone", "mobile_no", "lead_owner",
            "source", "custom_lead_type", "company_name", "job_title",
            "custom_received_on", "custom_last_contact_date", "custom_total_interactions",
            "creation", "modified", "owner",
        ],
        "default_order": "modified desc",
    },
    "opportunities": {
        "doctype": "Opportunity",
        "title_field": "title",
        "search_fields": ["name", "title", "customer_name", "contact_email", "contact_mobile"],
        "fields": [
            "name",
            "title",
            "opportunity_from",
            "party_name",
            "customer_name",
            "contact_person",
            "contact_display",
            "contact_email",
            "contact_mobile",
            "status",
            "opportunity_type",
            "sales_stage",
            "opportunity_amount",
            "currency",
            "probability",
            "expected_closing",
            "opportunity_owner",
            "creation",
            "modified",
        ],
        "default_order": "modified desc",
    },
    "customers": {
        "doctype": "Customer",
        "title_field": "customer_name",
        "search_fields": ["name", "customer_name", "mobile_no", "email_id", "tax_id"],
        "fields": [
            "name",
            "customer_name",
            "customer_type",
            "customer_group",
            "territory",
            "tax_id",
            "mobile_no",
            "email_id",
            "default_price_list",
            "account_manager",
            "creation",
            "modified",
        ],
        "default_order": "modified desc",
    },
    "contacts": {
        "doctype": "Contact",
        "title_field": "full_name",
        "search_fields": ["name", "full_name", "email_id", "mobile_no", "phone"],
        "fields": [
            "name",
            "salutation",
            "full_name",
            "designation",
            "department",
            "email_id",
            "mobile_no",
            "phone",
            "company_name",
            "status",
            "modified",
        ],
        "default_order": "modified desc",
    },
    "quotations": {
        "doctype": "Quotation",
        "title_field": "name",
        "search_fields": ["name", "party_name", "customer_name", "contact_display"],
        "fields": [
            "name",
            "quotation_to",
            "party_name",
            "customer_name",
            "contact_person",
            "contact_display",
            "transaction_date",
            "valid_till",
            "order_type",
            "status",
            "currency",
            "total",
            "net_total",
            "total_taxes_and_charges",
            "discount_amount",
            "grand_total",
            "company",
            "owner",
            "modified",
        ],
        "default_order": "transaction_date desc, modified desc",
    },
    "orders": {
        "doctype": "Sales Order",
        "title_field": "name",
        "search_fields": ["name", "customer", "customer_name", "po_no", "title"],
        "fields": [
            "name", "customer", "customer_name", "title",
            "transaction_date", "delivery_date",
            "docstatus", "status", "delivery_status", "billing_status",
            "per_billed", "per_delivered",
            "currency", "grand_total", "owner", "modified", "company",
            "custom_revenue_status", "custom_revenue_recognition_date",
            "custom_execution_status",
        ],
        "default_order": "transaction_date desc, modified desc",
    },
    "accounts": {
        "doctype": "DCNET Service Account",
        "title_field": "account_code",
        "search_fields": ["account_code", "customer", "item_code", "item_name", "a_end", "z_end"],
        "fields": [
            "account_code", "customer", "item_code", "item_name",
            "a_end", "z_end", "uom", "is_active", "creation", "modified",
        ],
        "default_order": "account_code asc",
    },
    "care_cards": {
        "doctype": "CRM Care Card",
        "title_field": "customer_name",
        "search_fields": ["name", "customer", "customer_name", "tax_id", "mobile_no", "email_id"],
        "fields": [
            "name", "customer", "customer_name", "tax_id",
            "mobile_no", "email_id", "address", "layout",
            "status", "satisfaction_level", "care_date",
            "country", "ward", "owner", "creation", "modified",
        ],
        "default_order": "modified desc",
    },
}

CONTACT_EXPORT_LABELS = {
    "name": "Mã liên hệ",
    "salutation": "Xưng hô",
    "full_name": "Họ và tên",
    "designation": "Chức danh",
    "mobile_no": "ĐT di động",
    "phone": "ĐT cơ quan",
    "email_id": "Email",
    "company_name": "Tổ chức",
    "department": "Phòng ban",
    "status": "Trạng thái",
    "modified": "Cập nhật cuối",
}


def can_access_crm():
    """Allow CRM only to Sales roles and system administrators."""
    user = frappe.session.user
    if user == "Guest":
        return False
    if user == "Administrator":
        return True
    return bool(set(frappe.get_roles(user)) & set(CRM_PAGE_ROLES))


def _get_resource(resource):
    config = RESOURCE_CONFIG.get(resource)
    if not config:
        frappe.throw(_("Unsupported CRM resource"), frappe.ValidationError)
    return config


def _get_available_fields(config):
    """Return configured fields that exist on the standard DocType."""
    meta = frappe.get_meta(config["doctype"])
    standard_fields = {"name", "owner", "creation", "modified", "modified_by", "docstatus", "idx"}
    return [
        fieldname
        for fieldname in config["fields"]
        if fieldname in standard_fields or meta.has_field(fieldname)
    ]


def _get_available_search_fields(config):
    """Return searchable fields that exist on the standard DocType."""
    meta = frappe.get_meta(config["doctype"])
    return [
        fieldname
        for fieldname in config["search_fields"]
        if fieldname == "name" or meta.has_field(fieldname)
    ]


def _parse_json(value, default):
    if value in (None, ""):
        return default
    if isinstance(value, (dict, list)):
        return value
    try:
        return json.loads(value)
    except (TypeError, ValueError):
        frappe.throw(_("Invalid JSON request data"), frappe.ValidationError)


def _display_notes_value(value):
    """Return a readable note value for fields that may be child tables."""
    if not isinstance(value, list):
        return value or ""
    notes = []
    for row in value:
        if isinstance(row, dict) or hasattr(row, "get"):
            note = row.get("note") or row.get("content") or row.get("description")
            if note:
                notes.append(str(note))
        elif row:
            notes.append(str(row))
    return "\n".join(notes)


def _check_permission(doctype, permission_type="read", name=None):
    if not frappe.has_permission(doctype, permission_type, name):
        frappe.throw(
            _("You are not permitted to access {0}").format(doctype),
            frappe.PermissionError,
        )


@frappe.whitelist(methods=["GET"])
def can_open_accounting_document(doctype, name):
    """Return whether the current user may open an accounting document.

    CRM related-record navigation currently allows only Sales Invoice to leave
    the CRM workspace. Keep the allow-list server-side so the client cannot use
    this endpoint to probe permissions for arbitrary DocTypes.
    """
    if doctype != "Sales Invoice" or not name:
        return {"allowed": False}
    return {
        "allowed": bool(frappe.has_permission(doctype, "read", doc=name)),
    }


def _permission_aware_count(doctype, filters=None):
    rows = frappe.get_list(
        doctype,
        fields=[{"COUNT": "name", "as": "total"}],
        filters=filters or {},
    )
    return cint(rows[0].total if rows else 0)


@frappe.whitelist(methods=["GET"])
def get_boot():
    """Return navigation metadata for the CRM workspace."""
    if not can_access_crm():
        frappe.throw(_("You are not permitted to access CRM"), frappe.PermissionError)

    resources = {}
    for key, config in RESOURCE_CONFIG.items():
        if not frappe.has_permission(config["doctype"], "read"):
            continue
        resources[key] = {
            "doctype": config["doctype"],
            "title_field": config["title_field"],
            "fields": _get_available_fields(config),
            "can_create": frappe.has_permission(config["doctype"], "create"),
        }

    return {
        "user": frappe.session.user,
        "full_name": frappe.utils.get_fullname(frappe.session.user),
        "show_unready_features": bool(
            cint(frappe.conf.get("dcnet_crm_show_unready_features", 0))
        ),
        "resources": resources,
    }


@frappe.whitelist(methods=["GET"])
def get_list(
    resource,
    search=None,
    filters=None,
    page=1,
    page_length=30,
    sort_field=None,
    sort_direction=None,
):
    """Return a permission-aware, paginated CRM list."""
    config = _get_resource(resource)
    doctype = config["doctype"]
    _check_permission(doctype)

    page = max(cint(page), 1)
    page_length = min(max(cint(page_length), 10), 100)
    parsed_filters = _parse_json(filters, {})
    or_filters = {}
    if search and search.strip():
        value = ["like", f"%{search.strip()}%"]
        or_filters = {
            field: value for field in _get_available_search_fields(config)
        }

    available_fields = _get_available_fields(config)
    order_by = config["default_order"]
    if sort_field:
        if sort_field not in available_fields:
            frappe.throw(_("Invalid sort field"), frappe.ValidationError)
        direction = "asc" if str(sort_direction).lower() == "asc" else "desc"
        order_by = f"{sort_field} {direction}"

    query_args = {
        "filters": parsed_filters,
        "order_by": order_by,
    }
    if or_filters:
        query_args["or_filters"] = or_filters

    rows = frappe.get_list(
        doctype,
        **query_args,
        fields=available_fields,
        start=(page - 1) * page_length,
        page_length=page_length,
    )
    if resource == "orders":
        for row in rows:
            row.update(_get_sales_order_display_status(row))
    totals = frappe.get_list(
        doctype,
        **query_args,
        fields=[{"COUNT": "name", "as": "total"}],
    )
    return {
        "data": rows,
        "total": cint(totals[0].total if totals else 0),
        "page": page,
        "page_length": page_length,
    }


def _get_sales_order_display_status(doc):
    """Derive CRM labels from ERPNext's authoritative Sales Order lifecycle.

    The legacy custom status fields can remain stale after submit, billing or
    delivery. These values are display-only and deliberately do not write back
    to the Sales Order.
    """
    docstatus = cint(doc.get("docstatus"))
    status = doc.get("status") or ""
    per_billed = flt(doc.get("per_billed"))
    per_delivered = flt(doc.get("per_delivered"))
    billing_status = doc.get("billing_status") or ""
    delivery_status = doc.get("delivery_status") or ""

    if docstatus == 2:
        return {
            "display_order_status": "Đã hủy",
            "display_revenue_status": "Hủy",
            "display_execution_status": "Đã hủy",
        }

    if docstatus == 0:
        return {
            "display_order_status": "Đơn nháp",
            "display_revenue_status": "Đơn nháp",
            "display_execution_status": "Chưa thực hiện",
        }

    status_labels = {
        "To Deliver and Bill": "Chờ giao hàng và xuất hóa đơn",
        "To Deliver": "Chờ giao hàng",
        "To Bill": "Chờ xuất hóa đơn",
        "Completed": "Hoàn thành",
        "Closed": "Đã đóng",
        "On Hold": "Tạm dừng",
    }
    execution_status = status_labels.get(status, status or "Đang thực hiện")

    # In the CRM revenue workflow, submitting the Sales Order is the posting
    # action. Billing is a later accounting step and must not keep a submitted
    # order in "Chưa ghi" while it is waiting for an invoice.
    fully_billed = per_billed >= 99.99 or billing_status == "Fully Billed"
    revenue_status = "Đã ghi"

    fully_delivered = per_delivered >= 99.99 or delivery_status == "Fully Delivered"
    if fully_delivered and status not in {"Completed", "Closed"}:
        execution_status = "Chờ xuất hóa đơn" if not fully_billed else "Hoàn thành"

    return {
        "display_order_status": execution_status,
        "display_revenue_status": revenue_status,
        "display_execution_status": execution_status,
    }


@frappe.whitelist(methods=["GET"])
def export_resource(
    resource,
    search=None,
    filters=None,
    fields=None,
    sort_field=None,
    sort_direction=None,
):
    """Download a permission-filtered CRM resource as an Excel workbook."""
    config = _get_resource(resource)
    doctype = config["doctype"]
    _check_permission(doctype)

    available_fields = _get_available_fields(config)
    requested_fields = _parse_json(fields, [])
    if not isinstance(requested_fields, list):
        frappe.throw(_("Invalid export fields"), frappe.ValidationError)

    export_fields = []
    for fieldname in requested_fields or available_fields:
        if not isinstance(fieldname, str) or fieldname not in available_fields:
            frappe.throw(_("Invalid export field"), frappe.ValidationError)
        if fieldname not in export_fields:
            export_fields.append(fieldname)

    parsed_filters = _parse_json(filters, {})
    if not isinstance(parsed_filters, (dict, list)):
        frappe.throw(_("Invalid export filters"), frappe.ValidationError)

    or_filters = {}
    search_value = str(search or "").strip()
    if search_value:
        value = ["like", f"%{search_value}%"]
        or_filters = {
            field: value for field in _get_available_search_fields(config)
        }

    order_by = config["default_order"]
    if sort_field:
        if sort_field not in available_fields:
            frappe.throw(_("Invalid sort field"), frappe.ValidationError)
        direction = "asc" if str(sort_direction).lower() == "asc" else "desc"
        order_by = f"{sort_field} {direction}"

    query_args = {
        "filters": parsed_filters,
        "fields": export_fields,
        "order_by": order_by,
        "limit_page_length": 0,
    }
    if or_filters:
        query_args["or_filters"] = or_filters

    rows = frappe.get_list(doctype, **query_args)
    meta = frappe.get_meta(doctype)
    labels = {
        field.fieldname: field.label
        for field in meta.fields
        if field.fieldname in export_fields
    }
    labels["name"] = _("Mã")
    data = [[CONTACT_EXPORT_LABELS.get(field) or labels.get(field) or field for field in export_fields]]
    data.extend([[row.get(field) for field in export_fields] for row in rows])

    sheet_title = _("Danh sách {0}").format(_(doctype))
    xlsx_file = make_xlsx(data, sheet_title[:31])
    timestamp = now_datetime().strftime("%Y%m%d_%H%M%S")
    frappe.response["type"] = "binary"
    frappe.response["filename"] = f"dcnet_crm_{resource}_{timestamp}.xlsx"
    frappe.response["filecontent"] = xlsx_file.getvalue()


@frappe.whitelist(methods=["GET"])
def export_contacts(search=None, filters=None, fields=None, sort_field=None, sort_direction=None):
    """Backward-compatible Contact export endpoint."""
    return export_resource(
        "contacts", search, filters, fields, sort_field, sort_direction
    )


@frappe.whitelist(methods=["GET"])
def get_document(resource, name):
    """Return a permitted CRM document and its recent activity."""
    config = _get_resource(resource)
    doctype = config["doctype"]
    _check_permission(doctype, name=name)
    doc = frappe.get_doc(doctype, name)

    result = {
        "document": {
            fieldname: doc.get(fieldname)
            for fieldname in _get_available_fields(config)
        },
        "timeline": _get_timeline(doctype, name),
    }
    if resource == "opportunities":
        result["items"] = [
            {
                "item_code": item.item_code,
                "item_name": item.item_name,
                "qty": item.qty,
                "uom": item.uom,
                "rate": item.rate,
                "amount": item.amount,
            }
            for item in doc.get("items", [])
        ]
    return result


@frappe.whitelist(methods=["GET"])
def get_opportunity_form_options():
    """Return permission-aware options for the internal Opportunity form."""
    _check_permission("Opportunity", "create")

    def options(doctype, fields, order_by="name asc", page_length=500):
        if not frappe.has_permission(doctype, "read"):
            return []
        return frappe.get_list(
            doctype,
            fields=fields,
            order_by=order_by,
            page_length=page_length,
        )

    return {
        "customers": options("Customer", ["name", "customer_name", "customer_group"]),
        "contacts": options("Contact", ["name", "full_name", "email_id", "mobile_no"]),
        "sources": options("UTM Source", ["name"]),
        "opportunity_types": options("Opportunity Type", ["name"]),
        "sales_stages": options("Sales Stage", ["name"]),
        "companies": options("Company", ["name"]),
        "territories": options("Territory", ["name"]),
        "countries": options("Country", ["name"]),
        "items": options("Item", ["name", "item_name", "stock_uom", "item_group"], page_length=2000),
        "item_groups": options("Item Group", ["name"]),
        "branches": options("Branch", ["name"]),
        "default_company": frappe.defaults.get_user_default("Company")
        or frappe.defaults.get_global_default("company"),
    }


def _get_opportunity_stage_history(doc):
    """Build a compact sales-stage history for the CRM detail sales tab."""
    amount = flt(doc.get("opportunity_amount"))
    probability = flt(doc.get("probability"))
    current_row = {
        "name": f"{doc.name}-current",
        "stage": doc.get("sales_stage") or _("Không chọn"),
        "amount": amount,
        "probability": probability,
        "expected_revenue": amount * probability / 100,
        "expected_closing": doc.get("expected_closing"),
        "modified": doc.get("modified"),
        "modified_by": doc.get("modified_by") or doc.get("owner"),
    }

    rows = [current_row]
    if not frappe.has_permission("Version", "read"):
        return rows

    versions = frappe.get_all(
        "Version",
        filters={"ref_doctype": "Opportunity", "docname": doc.name},
        fields=["name", "data", "creation", "owner"],
        order_by="creation desc",
        limit_page_length=20,
    )
    tracked_fields = {"sales_stage", "opportunity_amount", "probability", "expected_closing"}
    for version in versions:
        try:
            data = json.loads(version.data or "{}")
        except (TypeError, ValueError):
            continue
        changed = data.get("changed") or []
        changes = {
            item[0]: item
            for item in changed
            if isinstance(item, list) and len(item) >= 3 and item[0] in tracked_fields
        }
        if not changes:
            continue

        row_amount = flt(changes.get("opportunity_amount", [None, None, amount])[2])
        row_probability = flt(changes.get("probability", [None, None, probability])[2])
        rows.append({
            "name": version.name,
            "stage": changes.get("sales_stage", [None, None, current_row["stage"]])[2] or _("Không chọn"),
            "amount": row_amount,
            "probability": row_probability,
            "expected_revenue": row_amount * row_probability / 100,
            "expected_closing": changes.get("expected_closing", [None, None, current_row["expected_closing"]])[2],
            "modified": version.creation,
            "modified_by": version.owner,
        })

    return rows


def _get_opportunity_purchase_requests(name):
    """Return purchase requests linked from the custom Opportunity action when available."""
    if not frappe.db.exists("DocType", "Purchase Request"):
        return []
    if not frappe.has_permission("Purchase Request", "read"):
        return []
    if not frappe.get_meta("Purchase Request").has_field("custom_opportunity"):
        return []
    return frappe.get_list(
        "Purchase Request",
        filters={"custom_opportunity": name, "docstatus": ["<", 2]},
        fields=["name", "transaction_date", "schedule_date", "status", "company", "owner", "modified"],
        order_by="modified desc",
        page_length=20,
    )


@frappe.whitelist(methods=["GET"])
def get_opportunity_detail(name):
    """Return all data needed to render the internal Opportunity detail page."""
    _check_permission("Opportunity", name=name)
    doc = frappe.get_doc("Opportunity", name)

    # ── Items ────────────────────────────────────────────────
    items = [
        {
            "idx": item.idx,
            "item_code": item.item_code or "",
            "item_name": item.item_name or "",
            "description": item.description or "",
            "qty": item.qty,
            "uom": item.uom or "",
            "rate": item.rate,
            "amount": item.amount,
            "custom_discount_percentage": flt(item.get("custom_discount_percentage")),
            "custom_discount_amount": flt(item.get("custom_discount_amount")),
            "custom_net_rate": flt(item.get("custom_net_rate")),
            "custom_net_amount": flt(item.get("custom_net_amount")),
            "custom_installation_point_a_end": item.get("custom_installation_point_a_end") or "",
            "custom_installation_point_z_end": item.get("custom_installation_point_z_end") or "",
        }
        for item in doc.get("items", [])
    ]

    # ── Timeline (Communications + Comments for Activity tab) ─
    timeline = _get_timeline("Opportunity", name)

    # ── Comments for Trao đổi tab ─────────────────────────────
    comments = []
    if frappe.has_permission("Comment", "read"):
        comments = frappe.get_list(
            "Comment",
            filters={
                "reference_doctype": "Opportunity",
                "reference_name": name,
                "comment_type": "Comment",
            },
            fields=["name", "comment_by", "comment_by_fullname", "content", "creation"],
            order_by="creation asc",
        )

    # ── Activities (ToDo + Events) ────────────────────────────
    activities = []
    if frappe.has_permission("ToDo", "read"):
        todos = frappe.get_list(
            "ToDo",
            filters={"reference_type": "Opportunity", "reference_name": name},
            fields=["name", "description", "date", "status", "priority", "assigned_by_full_name", "owner", "modified"],
            order_by="date asc",
        )
        for t in todos:
            t["activity_doctype"] = "ToDo"
        activities.extend(todos)

    if frappe.has_permission("Event", "read"):
        event_names = frappe.get_all(
            "Event Participants",
            filters={"reference_doctype": "Opportunity", "reference_docname": name},
            pluck="parent",
        )
        if event_names:
            events = frappe.get_list(
                "Event",
                filters={"name": ["in", list(set(event_names))]},
                fields=["name", "subject", "event_category", "starts_on", "ends_on", "status", "owner", "modified"],
                order_by="starts_on asc",
            )
            for e in events:
                e["activity_doctype"] = "Event"
            activities.extend(events)

    activities.sort(key=lambda x: str(x.get("date") or x.get("starts_on") or ""))

    # ── Contacts ──────────────────────────────────────────────
    contacts = []
    if frappe.has_permission("Contact", "read"):
        contact_names = [doc.contact_person] if doc.contact_person else []
        if doc.party_name and doc.opportunity_from == "Customer":
            linked = frappe.get_all(
                "Dynamic Link",
                filters={"parenttype": "Contact", "link_doctype": "Customer", "link_name": doc.party_name},
                pluck="parent",
            )
            contact_names = list(set(contact_names + linked))
        if contact_names:
            contacts = frappe.get_list(
                "Contact",
                filters={"name": ["in", contact_names]},
                fields=[
                    "name", "full_name", "email_id", "mobile_no", "phone",
                    "designation", "company_name", "salutation",
                ],
            )
            for contact in contacts:
                contact["address"] = _format_word_address(_get_linked_address("Contact", contact["name"]))

    # ── Related sales docs ────────────────────────────────────
    quotations, orders, invoices = [], [], []
    customer = doc.party_name if doc.opportunity_from == "Customer" else None

    if customer and frappe.has_permission("Quotation", "read"):
        quotations = frappe.get_list(
            "Quotation",
            filters={"party_name": customer, "opportunity": name, "docstatus": ["<", 2]},
            fields=["name", "transaction_date", "status", "grand_total", "currency"],
            order_by="transaction_date desc",
            page_length=20,
        )
    sales_order_meta = frappe.get_meta("Sales Order")
    if (
        customer
        and frappe.has_permission("Sales Order", "read")
        and sales_order_meta.has_field("custom_opportunity")
    ):
        orders = frappe.get_list(
            "Sales Order",
            filters={
                "customer": customer,
                "custom_opportunity": name,
                "docstatus": ["<", 2],
            },
            fields=["name", "transaction_date", "status", "grand_total", "currency", "company", "owner"],
            order_by="transaction_date desc",
            page_length=20,
        )
    order_names = [order.name for order in orders]
    if order_names and frappe.has_permission("Sales Invoice", "read"):
        invoice_names = frappe.get_all(
            "Sales Invoice Item",
            filters={"sales_order": ["in", order_names]},
            pluck="parent",
        )
        invoice_names = list(set(invoice_names))
    else:
        invoice_names = []
    if invoice_names:
        invoices = frappe.get_list(
            "Sales Invoice",
            filters={
                "name": ["in", invoice_names],
                "customer": customer,
                "is_return": 0,
                "docstatus": ["<", 2],
            },
            fields=["name", "posting_date", "status", "grand_total", "outstanding_amount"],
            order_by="posting_date desc",
            page_length=20,
        )

    stage_history = _get_opportunity_stage_history(doc)
    purchase_requests = _get_opportunity_purchase_requests(name)

    # ── Attachments ───────────────────────────────────────────
    attachments = []
    if frappe.has_permission("File", "read"):
        attachments = frappe.get_all(
            "File",
            filters={"attached_to_doctype": "Opportunity", "attached_to_name": name},
            fields=["name", "file_name", "file_url", "file_size", "is_private", "creation", "owner"],
            order_by="creation desc",
        )

    document = {
        f: doc.get(f)
        for f in [
            "name", "title", "opportunity_from", "party_name", "customer_name",
            "contact_person", "contact_display", "contact_mobile", "contact_email",
            "status", "sales_stage", "probability", "opportunity_amount", "currency",
            "expected_closing", "opportunity_type", "source", "campaign_name",
            "territory", "company", "opportunity_owner",
            "custom_opportunity_code", "custom_shipping_address",
            "custom_shipping_country", "custom_shipping_state",
            "custom_shipping_county", "custom_shipping_ward",
            "custom_shipping_address_line1", "custom_shipping_pincode",
            "custom_is_shared", "custom_referral_partner",
            "custom_item_category", "custom_branch", "custom_sales_process",
            "custom_related_person", "custom_result_other_reason",
            "creation", "modified", "owner", "modified_by",
        ]
    }
    document["notes"] = _display_notes_value(doc.get("notes"))
    document["lost_reasons"] = [row.lost_reason for row in doc.get("lost_reasons", [])]
    document["customer_group"] = (
        frappe.db.get_value("Customer", doc.party_name, "customer_group")
        if doc.opportunity_from == "Customer" and doc.party_name
        else None
    )
    document["owner_full_name"] = frappe.utils.get_fullname(document.get("owner")) or document.get("owner")
    document["modified_by_full_name"] = (
        frappe.utils.get_fullname(document.get("modified_by")) or document.get("modified_by")
    )

    return {
        "can_write": frappe.has_permission("Opportunity", "write", doc=name),
        "document": document,
        "items": items,
        "timeline": timeline,
        "comments": comments,
        "activities": activities,
        "contacts": contacts,
        "quotations": quotations,
        "orders": orders,
        "invoices": invoices,
        "stage_history": stage_history,
        "purchase_requests": purchase_requests,
        "attachments": attachments,
    }


@frappe.whitelist(methods=["POST"])
def update_opportunity(name, data):
    """Update editable fields on an Opportunity (called from detail page Sửa mode)."""
    _check_permission("Opportunity", "write", name=name)
    if isinstance(data, str):
        data = json.loads(data)

    ALLOWED = {
        "title", "party_name", "contact_person", "sales_stage", "probability",
        "expected_closing", "opportunity_type", "source", "territory", "company",
        "opportunity_owner", "opportunity_amount",
        # NOTE: "notes" is intentionally excluded — Opportunity.notes is a Table field
        # (child doctype "CRM Note"), not free text. Assigning a plain string to it
        # crashes inside Frappe's `doc.set()` (`'str' object does not support item
        # assignment`). The CRM only ever displays a flattened read-only preview of it.
        # "lost_reasons" is also a Table field, but the closing dialog always sends
        # it as a list of {"lost_reason": ...} rows, which doc.set() accepts fine.
        "lost_reasons", "custom_result_other_reason",
        "custom_shipping_country", "custom_shipping_state", "custom_shipping_county",
        "custom_shipping_ward", "custom_shipping_address_line1", "custom_shipping_pincode",
        "custom_shipping_address", "custom_is_shared", "custom_referral_partner",
        "custom_item_category", "custom_branch", "custom_sales_process", "custom_related_person",
    }
    doc = frappe.get_doc("Opportunity", name)
    for k, v in data.items():
        if k in ALLOWED:
            doc.set(k, v)

    # Đổi giai đoạn thì tự set lại Tỷ lệ thành công theo giai đoạn mới,
    # trừ khi caller đã tự truyền probability riêng.
    if "sales_stage" in data and "probability" not in data:
        stage_probability = CRM_SALES_STAGE_PROBABILITY.get(data["sales_stage"])
        if stage_probability is not None:
            doc.set("probability", stage_probability)

    doc.save(ignore_permissions=False)
    return {"name": doc.name, "modified": str(doc.modified)}


@frappe.whitelist(methods=["POST"])
def add_opportunity_tag(name, tag):
    """Add a Frappe tag to an Opportunity from the CRM workspace."""
    _check_permission("Opportunity", "write", name=name)
    tag = (tag or "").strip()
    if not tag:
        frappe.throw(_("Tag is required"), frappe.ValidationError)

    doc = frappe.get_doc("Opportunity", name)
    doc.add_tag(tag)
    return {"tags": doc.get("_user_tags")}


@frappe.whitelist(methods=["POST"])
def add_opportunity_attachment_link(name, url, title=None):
    """Attach an external URL to an Opportunity as a standard File record."""
    _check_permission("Opportunity", "write", name=name)
    url = _normalize_external_url(url)

    file_doc = frappe.get_doc(
        {
            "doctype": "File",
            "file_url": url,
            "file_name": (title or "").strip() or url,
            "attached_to_doctype": "Opportunity",
            "attached_to_name": name,
        }
    )
    file_doc.insert(ignore_permissions=False)
    return {"name": file_doc.name}


def _get_opportunity_for_action(name, permission_type="read"):
    name = (name or "").strip()
    if not name:
        frappe.throw(_("Opportunity is required"), frappe.ValidationError)
    _check_permission("Opportunity", permission_type, name=name)
    return frappe.get_doc("Opportunity", name)


@frappe.whitelist(methods=["POST"])
def create_opportunity_handoff(name, assigned_to, due_date=None, description=None):
    """Create a ToDo that hands over an Opportunity to another user."""
    opp = _get_opportunity_for_action(name, "read")
    _check_permission("ToDo", "create")
    assigned_to = (assigned_to or "").strip()
    if not assigned_to or not frappe.db.exists("User", assigned_to):
        frappe.throw(_("Vui lòng chọn người nhận hợp lệ"), frappe.ValidationError)

    todo = frappe.new_doc("ToDo")
    todo.allocated_to = assigned_to
    todo.reference_type = "Opportunity"
    todo.reference_name = opp.name
    todo.description = (description or "").strip() or _("Bàn giao theo dõi cơ hội {0}").format(opp.title or opp.name)
    todo.date = due_date or frappe.utils.today()
    todo.status = "Open"
    todo.priority = "Medium"
    todo.insert(ignore_permissions=False)

    opp.add_comment(
        "Info",
        _("Đã bàn giao công việc cho {0}: {1}").format(assigned_to, todo.description),
    )
    return {"name": todo.name}


@frappe.whitelist(methods=["POST"])
def request_opportunity_approval(name):
    """Mark an Opportunity as sent for approval by creating a review ToDo and audit comment."""
    opp = _get_opportunity_for_action(name, "read")
    _check_permission("ToDo", "create")

    approver = opp.get("opportunity_owner") or opp.owner or frappe.session.user
    if not frappe.db.exists("User", approver):
        approver = opp.owner or frappe.session.user

    todo = frappe.new_doc("ToDo")
    todo.allocated_to = approver
    todo.reference_type = "Opportunity"
    todo.reference_name = opp.name
    todo.description = _("Phê duyệt cơ hội {0}").format(opp.title or opp.name)
    todo.date = frappe.utils.today()
    todo.status = "Open"
    todo.priority = "High"
    todo.insert(ignore_permissions=False)

    opp.add_comment(
        "Info",
        _("Đã gửi phê duyệt cơ hội cho {0}").format(approver),
    )
    return {"name": todo.name, "assigned_to": approver}


@frappe.whitelist(methods=["POST"])
def create_purchase_request_from_opportunity(name):
    """Create a Purchase Request from Opportunity line items."""
    opp = _get_opportunity_for_action(name, "read")
    if not frappe.db.exists("DocType", "Purchase Request"):
        frappe.throw(
            _("Chưa có DocType Purchase Request trên site này. Vui lòng cài/cấu hình module mua hàng trước."),
            frappe.ValidationError,
        )
    _check_permission("Purchase Request", "create")

    rows = [row for row in (opp.get("items") or []) if row.get("item_code")]
    if not rows:
        frappe.throw(_("Cơ hội chưa có hàng hóa để tạo yêu cầu mua hàng"), frappe.ValidationError)

    company = (
        opp.get("company")
        or frappe.defaults.get_user_default("Company")
        or frappe.db.get_single_value("Global Defaults", "default_company")
    )
    if not company:
        frappe.throw(_("Không tìm thấy công ty mặc định để tạo yêu cầu mua hàng"), frappe.ValidationError)

    schedule_date = opp.get("expected_closing") or frappe.utils.today()
    doc = frappe.new_doc("Purchase Request")
    doc.company = company
    if doc.meta.has_field("transaction_date"):
        doc.transaction_date = frappe.utils.today()
    if doc.meta.has_field("schedule_date"):
        doc.schedule_date = schedule_date
    if doc.meta.has_field("custom_opportunity"):
        doc.custom_opportunity = opp.name

    for row in rows:
        item = {
            "item_code": row.get("item_code"),
            "item_name": row.get("item_name"),
            "description": row.get("description") or row.get("item_name") or row.get("item_code"),
            "qty": flt(row.get("qty") or 1),
            "uom": row.get("uom"),
            "schedule_date": schedule_date,
        }
        doc.append("items", {k: v for k, v in item.items() if v not in (None, "")})

    doc.insert(ignore_permissions=False)
    opp.add_comment("Info", _("Đã tạo yêu cầu mua hàng {0}").format(doc.name))
    return {"name": doc.name}


@frappe.whitelist(methods=["POST"])
def create_care_card_from_opportunity(name):
    """Create a CRM Care Card for the Opportunity customer."""
    opp = _get_opportunity_for_action(name, "read")
    _check_permission("CRM Care Card", "create")

    customer = opp.get("party_name")
    if not customer or not frappe.db.exists("Customer", customer):
        frappe.throw(_("Cơ hội này chưa gắn khách hàng nên chưa thể sinh thẻ tư vấn"), frappe.ValidationError)

    doc = frappe.new_doc("CRM Care Card")
    doc.customer = customer
    doc.status = "Chưa chăm sóc"
    doc.care_date = frappe.utils.today()
    doc.description = _("Sinh từ cơ hội {0}: {1}").format(opp.name, opp.title or "")

    customer_doc = frappe.get_cached_doc("Customer", customer)
    doc.tax_id = customer_doc.get("tax_id")
    doc.mobile_no = opp.get("contact_mobile") or customer_doc.get("mobile_no")
    doc.email_id = opp.get("contact_email") or customer_doc.get("email_id")

    first_item = next((row for row in (opp.get("items") or []) if row.get("item_code")), None)
    if first_item:
        doc.item = first_item.get("item_code")
        doc.item_type = first_item.get("item_group") or first_item.get("item_name")

    doc.insert(ignore_permissions=False)
    opp.add_comment("Info", _("Đã sinh thẻ tư vấn {0}").format(doc.name))
    return {"name": doc.name}


@frappe.whitelist(methods=["GET"])
def get_so_items(name):
    """Return line items of a Sales Order for the CRM detail panel."""
    _check_permission("Sales Order", name=name)
    doc = frappe.get_doc("Sales Order", name)
    account_fallbacks = _get_service_account_fallbacks(doc.customer, doc.get("items", []))
    return [
        {
            "item_code": item.item_code or "",
            "item_name": item.item_name or "",
            "description": item.get("description") or "",
            "qty": item.qty,
            "uom": item.uom or "",
            "rate": item.rate,
            "amount": item.amount,
            "net_rate": item.get("net_rate") or item.rate,
            "net_amount": item.get("net_amount") or item.amount,
            "custom_a_end": item.get("custom_a_end") or "",
            "custom_z_end": item.get("custom_z_end") or "",
            "custom_dcnet_account_id": (
                item.get("custom_dcnet_account_id")
                or account_fallbacks.get(item.name, "")
            ),
        }
        for item in doc.get("items", [])
    ]


@frappe.whitelist(methods=["GET"])
def get_quotation_items(name):
    """Return line items of a Quotation for the CRM detail panel."""
    _check_permission("Quotation", name=name)
    doc = frappe.get_doc("Quotation", name)
    return [
        {
            "item_code": item.item_code or "",
            "item_name": item.item_name or "",
            "description": item.get("description") or "",
            "qty": item.qty,
            "uom": item.uom or "",
            "rate": item.rate,
            "amount": item.amount,
            "net_rate": item.get("net_rate") or item.rate,
            "net_amount": item.get("net_amount") or item.amount,
        }
        for item in doc.get("items", [])
    ]


@frappe.whitelist(methods=["GET"])
def get_quotation_quick_stats():
    """Aggregate real Quotation figures for the list page's "Thống kê nhanh" panel."""
    if not frappe.has_permission("Quotation", "read"):
        frappe.throw(_("You are not permitted to access Quotation"), frappe.PermissionError)

    rows = frappe.get_all(
        "Quotation",
        fields=["status", "grand_total"],
        filters={"docstatus": ["<", 2]},
    )
    total_count = len(rows)
    total_value = sum(flt(row.grand_total) for row in rows)

    by_status = {}
    for row in rows:
        status = row.status or "Draft"
        bucket = by_status.setdefault(status, {"status": status, "count": 0, "value": 0})
        bucket["count"] += 1
        bucket["value"] += flt(row.grand_total)

    return {
        "total_count": total_count,
        "total_value": total_value,
        "by_status": sorted(by_status.values(), key=lambda row: row["count"], reverse=True),
    }


@frappe.whitelist(methods=["POST"])
def add_quotation_tag(name, tag):
    """Add a Frappe tag to a Quotation from the CRM workspace."""
    _check_permission("Quotation", "write", name=name)
    tag = (tag or "").strip()
    if not tag:
        frappe.throw(_("Tag is required"), frappe.ValidationError)

    doc = frappe.get_doc("Quotation", name)
    doc.add_tag(tag)
    return {"tags": frappe.db.get_value("Quotation", name, "_user_tags")}


@frappe.whitelist(methods=["GET"])
def get_quotation_stock_levels(name):
    """Aggregate real stock-on-hand per item for the "Tra cứu số lượng tồn" popup."""
    _check_permission("Quotation", name=name)
    doc = frappe.get_doc("Quotation", name)

    aggregated = {}
    for item in doc.get("items", []):
        if not item.item_code:
            continue
        bucket = aggregated.setdefault(item.item_code, {
            "item_code": item.item_code,
            "description": item.item_name or item.get("description") or item.item_code,
            "uom": item.uom or "",
            "warehouse": item.get("warehouse") or "",
            "qty": 0,
        })
        bucket["qty"] += flt(item.qty)

    rows = []
    can_read_bin = frappe.has_permission("Bin", "read")
    for item_code, bucket in aggregated.items():
        stock_qty = 0
        if can_read_bin:
            bin_filters = {"item_code": item_code}
            if bucket["warehouse"]:
                bin_filters["warehouse"] = bucket["warehouse"]
            stock_qty = sum(
                flt(row.actual_qty)
                for row in frappe.get_all("Bin", filters=bin_filters, fields=["actual_qty"])
            )
        rows.append({
            **bucket,
            # A Quotation is never itself delivered — only Sales Orders/Delivery
            # Notes made from it are, so this is genuinely always 0 here.
            "delivered_qty": 0,
            "stock_qty": stock_qty,
        })
    return rows


@frappe.whitelist(methods=["GET"])
def get_quotation_detail(name):
    """Return the permission-aware data for the CRM Quotation detail page."""
    _check_permission("Quotation", name=name)
    doc = frappe.get_doc("Quotation", name)

    item_tax_map = {}
    for tax in doc.get("taxes", []):
        detail = tax.get("item_wise_tax_detail")
        if not detail:
            continue
        try:
            detail = json.loads(detail) if isinstance(detail, str) else detail
        except (TypeError, ValueError):
            continue
        for item_code, value in (detail or {}).items():
            rate = flt(value[0]) if isinstance(value, (list, tuple)) and value else 0
            amount = flt(value[1]) if isinstance(value, (list, tuple)) and len(value) > 1 else 0
            current = item_tax_map.setdefault(item_code, {"rate": 0, "amount": 0})
            current["rate"] = max(current["rate"], rate)
            current["amount"] += amount

    items = []
    for item in doc.get("items", []):
        price_list_rate = flt(item.get("price_list_rate")) or flt(item.rate)
        gross_amount = price_list_rate * flt(item.qty)
        net_amount = flt(item.get("net_amount")) or flt(item.amount)
        tax_info = item_tax_map.get(item.item_code, {})
        tax_amount = flt(tax_info.get("amount"))
        items.append({
            "idx": item.idx,
            "name": item.name,
            "item_code": item.item_code or "",
            "item_name": item.item_name or "",
            "description": item.get("description") or "",
            "a_end": (
                item.get("custom_a_end")
                or item.get("custom_installation_point_a_end")
                or ""
            ),
            "z_end": (
                item.get("custom_z_end")
                or item.get("custom_installation_point_z_end")
                or ""
            ),
            "uom": item.uom or "",
            "qty": flt(item.qty),
            "price_list_rate": price_list_rate,
            "gross_amount": gross_amount,
            "discount_percentage": flt(item.get("discount_percentage")),
            "discount_amount": max(gross_amount - net_amount, 0),
            "net_rate": flt(item.get("net_rate")) or flt(item.rate),
            "net_amount": net_amount,
            "tax_rate": flt(tax_info.get("rate")),
            "tax_amount": tax_amount,
            "total_with_tax": net_amount + tax_amount,
        })

    customer_tax_id = ""
    if (
        doc.quotation_to == "Customer"
        and doc.party_name
        and frappe.has_permission("Customer", "read", doc=doc.party_name)
    ):
        customer_tax_id = frappe.db.get_value("Customer", doc.party_name, "tax_id") or ""

    comments = []
    if frappe.has_permission("Comment", "read"):
        comments = frappe.get_list(
            "Comment",
            filters={
                "reference_doctype": "Quotation",
                "reference_name": name,
                "comment_type": "Comment",
            },
            fields=["name", "comment_by_fullname", "content", "creation"],
            order_by="creation desc",
            page_length=100,
        )

    attachments = []
    if frappe.has_permission("File", "read"):
        attachments = frappe.get_list(
            "File",
            filters={"attached_to_doctype": "Quotation", "attached_to_name": name},
            fields=["name", "file_name", "file_url", "file_size", "owner", "creation"],
            order_by="creation desc",
            page_length=100,
        )

    activities = []
    if frappe.has_permission("ToDo", "read"):
        activities = frappe.get_list(
            "ToDo",
            filters={"reference_type": "Quotation", "reference_name": name},
            fields=["name", "description", "status", "priority", "date", "owner"],
            order_by="date desc, creation desc",
            page_length=100,
        )

    orders = []
    if frappe.has_permission("Sales Order", "read"):
        order_names = frappe.get_all(
            "Sales Order Item",
            filters={"prevdoc_docname": name},
            pluck="parent",
        )
        if order_names:
            orders = frappe.get_list(
                "Sales Order",
                filters={"name": ["in", list(set(order_names))], "docstatus": ["<", 2]},
                fields=["name", "transaction_date", "status", "grand_total", "currency"],
                order_by="transaction_date desc",
                page_length=100,
            )

    document_fields = [
        "name", "title", "quotation_to", "party_name", "customer_name",
        "contact_person", "contact_display", "contact_mobile", "contact_email",
        "opportunity", "status", "order_type", "transaction_date", "valid_till",
        "payment_terms_template", "currency", "company", "territory", "owner",
        "creation", "modified", "modified_by", "total_qty", "net_total",
        "total_taxes_and_charges", "grand_total", "terms",
        "custom_installation_zone", "custom_internal_notes",
        "custom_implementation_time", "custom_sla", "custom_is_shared",
        "custom_approval_requested",
    ]
    document = {
        field: doc.get(field)
        for field in document_fields
        if doc.meta.has_field(field) or field in {"name", "owner", "creation", "modified", "modified_by"}
    }

    return {
        "document": document,
        "customer_tax_id": customer_tax_id,
        "items": items,
        "comments": comments,
        "attachments": attachments,
        "activities": activities,
        "orders": orders,
        "can_write": frappe.has_permission("Quotation", "write", doc=doc),
        "can_create_order": frappe.has_permission("Sales Order", "create"),
        "can_create_activity": frappe.has_permission("ToDo", "create"),
    }


@frappe.whitelist(methods=["POST"])
def create_quotation_activity(name, activity=None):
    """Create a CRM task linked to a Quotation."""
    _check_permission("Quotation", name=name)
    _check_permission("ToDo", "create")
    values = _parse_json(activity, {})
    description = (values.get("description") or "").strip()
    if not description:
        frappe.throw(_("Nội dung công việc là bắt buộc"), frappe.ValidationError)

    priority = values.get("priority") or "Medium"
    if priority not in {"Low", "Medium", "High", "Urgent"}:
        frappe.throw(_("Mức độ ưu tiên không hợp lệ"), frappe.ValidationError)

    todo = frappe.new_doc("ToDo")
    todo.description = description
    todo.reference_type = "Quotation"
    todo.reference_name = name
    todo.status = "Open"
    todo.priority = priority
    todo.date = values.get("date") or frappe.utils.today()
    todo.allocated_to = frappe.session.user
    todo.insert(ignore_permissions=False)
    return {
        "name": todo.name,
        "description": todo.description,
        "status": todo.status,
        "priority": todo.priority,
        "date": todo.date,
    }


@frappe.whitelist(methods=["POST"])
def set_quotation_approval_requested(name, requested):
    """Toggle the "Yêu cầu duyệt"/"Thu hồi phê duyệt" flag on a Quotation."""
    _check_permission("Quotation", "write", name=name)
    doc = frappe.get_doc("Quotation", name)
    doc.custom_approval_requested = 1 if int(requested) else 0
    doc.save(ignore_permissions=False)
    return {"name": doc.name, "custom_approval_requested": doc.custom_approval_requested}


def _get_address_doc(address_name):
    """Return an Address document when the link is still valid."""
    if not address_name or not frappe.db.exists("Address", address_name):
        return None
    return frappe.get_doc("Address", address_name)


def _format_word_address(address):
    if not address:
        return ""
    parts = []
    for fieldname in (
        "address_line1", "address_line2", "county", "city", "state", "pincode", "country",
    ):
        value = (address.get(fieldname) or "").strip()
        if value and value not in parts:
            parts.append(value)
    return ", ".join(parts)


def _get_linked_address(link_doctype, link_name):
    if not link_name:
        return None
    address_names = frappe.get_all(
        "Dynamic Link",
        filters={
            "parenttype": "Address",
            "link_doctype": link_doctype,
            "link_name": link_name,
        },
        pluck="parent",
    )
    if not address_names:
        return None
    preferred = frappe.get_all(
        "Address",
        filters={"name": ["in", address_names], "disabled": 0},
        fields=["name", "is_primary_address", "is_shipping_address", "modified"],
        order_by="is_primary_address desc, is_shipping_address desc, modified desc",
        limit=1,
    )
    return _get_address_doc(preferred[0].name) if preferred else None


def _get_default_bank_account(filters):
    if not frappe.db.exists("DocType", "Bank Account"):
        return frappe._dict()
    row = frappe.db.get_value(
        "Bank Account",
        {**filters, "is_default": 1},
        ["bank_account_no", "bank"],
        as_dict=True,
    )
    return row or frappe._dict()


def _build_sales_order_word_data(doc, contract_utils):
    """Map an ERPNext Sales Order onto the dcnet-contract Word placeholders."""
    format_currency = contract_utils._format_currency
    format_date = contract_utils._format_date_vi
    number_to_words = contract_utils._number_to_words_vi

    customer = frappe.get_doc("Customer", doc.customer) if doc.customer else frappe._dict()
    if doc.contact_person and frappe.db.exists("Contact", doc.contact_person):
        contact = frappe.get_doc("Contact", doc.contact_person)
    else:
        contact = frappe._dict()

    customer_address = _get_address_doc(doc.customer_address) or _get_linked_address(
        "Customer", doc.customer,
    )
    shipping_address = _get_address_doc(doc.shipping_address_name) or customer_address
    company = frappe.get_doc("Company", doc.company) if doc.company else frappe._dict()
    company_address = _get_linked_address("Company", doc.company)
    company_bank = _get_default_bank_account({
        "company": doc.company,
        "is_company_account": 1,
    }) if doc.company else frappe._dict()
    customer_bank = _get_default_bank_account({
        "party_type": "Customer",
        "party": doc.customer,
    }) if doc.customer else frappe._dict()

    item_names = [
        row.item_name or row.item_code
        for row in doc.get("items", [])
        if row.item_name or row.item_code
    ]
    first_item = (doc.get("items") or [frappe._dict()])[0]
    monthly_fee = flt(doc.net_total)
    monthly_vat = flt(doc.total_taxes_and_charges)
    monthly_total = flt(doc.grand_total)

    values = {
        "contract_number": doc.name,
        "contract_date": format_date(doc.transaction_date),
        "customer_name": doc.customer_name or customer.get("customer_name") or doc.customer or "",
        "customer_address": _format_word_address(customer_address),
        "customer_phone": contact.get("mobile_no") or contact.get("phone") or customer.get("mobile_no") or "",
        "customer_fax": contact.get("fax") or "",
        "customer_tax_id": customer.get("tax_id") or "",
        "customer_representative": contact.get("full_name") or "",
        "customer_representative_title": contact.get("designation") or "",
        "customer_id_number": customer.get("custom_id_number") or "",
        "customer_id_date": "",
        "customer_id_place": "",
        "customer_dob": "",
        "customer_email": contact.get("email_id") or customer.get("email_id") or "",
        "customer_bank_account": customer_bank.get("bank_account_no") or "",
        "service_type": ", ".join(dict.fromkeys(item_names)),
        "package_name": ", ".join(dict.fromkeys(item_names)),
        "installation_address": _format_word_address(shipping_address),
        "setup_fee": format_currency(0),
        "setup_fee_vat": format_currency(0),
        "setup_fee_total": format_currency(0),
        "setup_fee_words": number_to_words(0),
        "monthly_fee": format_currency(monthly_fee),
        "monthly_fee_vat": format_currency(monthly_vat),
        "monthly_fee_total": format_currency(monthly_total),
        "monthly_fee_words": number_to_words(round(monthly_total)),
        "package_term": str(doc.get("custom_contract_duration") or ""),
        "acceptance_date": format_date(doc.get("custom_acceptance_date") or doc.delivery_date),
        "end_date": format_date(doc.get("custom_contract_expiry")) if doc.get("custom_contract_expiry") else "",
        "bandwidth": first_item.get("custom_bandwidth") or "",
        "point_a": first_item.get("custom_a_end") or "",
        "point_b": first_item.get("custom_z_end") or "",
        "sla_restore_hours": str(doc.get("custom_sla_restore_hours") or ""),
        "company_name_b": company.get("company_name") or doc.company or "",
        "company_address_b": _format_word_address(company_address),
        "company_phone_b": company.get("phone_no") or "",
        "company_fax_b": company.get("fax") or "",
        "company_tax_id_b": company.get("tax_id") or "",
        "company_representative_b": company.get("representative") or "",
        "company_representative_title_b": company.get("representative_title") or "",
        "company_bank_account_b": company_bank.get("bank_account_no") or "",
        "company_bank_b": company_bank.get("bank") or "",
    }
    items = [{
        "item_stt": str(index),
        "item_label": row.item_name or row.item_code or "",
        "item_qty": str(row.qty or 0),
        "item_uom": row.uom or "",
        "item_price": format_currency(row.rate),
        "item_amount": format_currency(row.amount),
    } for index, row in enumerate(doc.get("items", []), 1)]
    return values, items


def _get_sales_order_contract_template(template_name):
    """Resolve a dcnet-contract template selected from the Sales Order print dialog."""
    if not frappe.db.exists("DocType", "DCNet Contract Template"):
        frappe.throw(
            _("Chưa cài đặt ứng dụng dcnet-contract để sử dụng mẫu in."),
            frappe.ValidationError,
        )
    if not template_name or not frappe.db.exists("DCNet Contract Template", template_name):
        frappe.throw(_("Không tìm thấy mẫu in đã chọn."), frappe.ValidationError)
    return frappe.get_doc("DCNet Contract Template", template_name)


@frappe.whitelist(methods=["GET"])
def get_sales_order_print_templates(name):
    """List dcnet-contract Word templates available to a Sales Order."""
    _check_permission("Sales Order", name=name)
    if not frappe.db.exists("DocType", "DCNet Contract Template"):
        return []
    rows = frappe.get_all(
        "DCNet Contract Template",
        fields=[
            "name", "template_name", "template_category", "service_type",
            "status", "template_file",
        ],
        order_by="template_name asc",
    )
    for row in rows:
        row["can_delete"] = bool(frappe.has_permission("DCNet Contract Template", "delete", doc=row.name))
    return rows


@frappe.whitelist(methods=["POST"])
def delete_sales_order_print_template(template_name):
    """Delete a dcnet-contract Word template from the CRM print dialog."""
    if not frappe.db.exists("DCNet Contract Template", template_name):
        frappe.throw(_("Không tìm thấy mẫu in"), frappe.DoesNotExistError)
    doc = frappe.get_doc("DCNet Contract Template", template_name)
    doc.check_permission("delete")
    doc.delete()


@frappe.whitelist(methods=["POST"])
def preview_sales_order_print_template(name, template_name):
    """Render a selected contract template with Sales Order data for preview/print."""
    _check_permission("Sales Order", name=name)
    template = _get_sales_order_contract_template(template_name)

    try:
        from dcnet_contract.dcnet_contract.utils import docx_generator as contract_utils
    except ImportError:
        frappe.throw(
            _("Không thể tải bộ sinh tài liệu của dcnet-contract."),
            frappe.ValidationError,
        )

    html = template.get("template_html") or template.get("boilerplate_text") or ""
    if not html and template.template_file:
        try:
            from dcnet_contract.dcnet_contract.api import _docx_to_styled_html
            template_file = frappe.get_doc("File", {"file_url": template.template_file})
            html = _docx_to_styled_html(template_file.get_full_path())
        except Exception:
            frappe.log_error(frappe.get_traceback(), "Sales Order print template preview")

    if not html:
        return {
            "html": "<p>Mẫu này chưa có nội dung xem trước.</p>",
            "template_name": template.template_name,
        }

    doc = frappe.get_doc("Sales Order", name)
    values, items = _build_sales_order_word_data(doc, contract_utils)
    html = contract_utils._fill_html_template(html, values, items)
    for key, value in values.items():
        html = html.replace("{{" + key + "}}", str(value or ""))

    return {
        "html": html,
        "template_name": template.template_name,
        "order_name": doc.name,
    }


@frappe.whitelist(methods=["POST"])
def generate_sales_order_word(name, template_name):
    """Fill the selected dcnet-contract Word template and attach it to a Sales Order."""
    _check_permission("Sales Order", name=name)
    template = _get_sales_order_contract_template(template_name)

    if not template.template_file:
        frappe.throw(_("Mẫu đã chọn chưa có file Word."), frappe.ValidationError)

    try:
        from dcnet_contract.dcnet_contract.utils import docx_generator as contract_utils
    except ImportError:
        frappe.throw(
            _("Không thể tải bộ sinh tài liệu của dcnet-contract."),
            frappe.ValidationError,
        )

    doc = frappe.get_doc("Sales Order", name)
    template_file = frappe.get_doc("File", {"file_url": template.template_file})
    values, items = _build_sales_order_word_data(doc, contract_utils)
    generated_path = None
    try:
        generated_path = contract_utils._fill_docx(template_file.get_full_path(), values, items)
        with open(generated_path, "rb") as source:
            content = source.read()
        safe_name = re.sub(r"[^\w.-]", "_", f"{doc.name}-{template.template_name}.docx")
        attachment = frappe.get_doc({
            "doctype": "File",
            "file_name": safe_name,
            "content": content,
            "attached_to_doctype": "Sales Order",
            "attached_to_name": doc.name,
            "is_private": 1,
        })
        attachment.save(ignore_permissions=True)
        return {"file_url": attachment.file_url, "file_name": attachment.file_name}
    finally:
        if generated_path:
            try:
                os.unlink(generated_path)
            except OSError:
                pass


@frappe.whitelist(methods=["GET"])
def get_so_detail(name):
    """Return all data needed to render the internal Sales Order detail page."""
    _check_permission("Sales Order", name=name)
    doc = frappe.get_doc("Sales Order", name)
    account_fallbacks = _get_service_account_fallbacks(doc.customer, doc.get("items", []))

    # ── Per-line tax breakup (rate + amount) from order taxes ─
    item_tax_map = {}
    for tax in doc.get("taxes", []):
        detail = tax.get("item_wise_tax_detail")
        if not detail:
            continue
        try:
            detail = json.loads(detail) if isinstance(detail, str) else detail
        except (ValueError, TypeError):
            continue
        for code, value in (detail or {}).items():
            # value is typically [rate, tax_amount]
            rate = flt(value[0]) if isinstance(value, (list, tuple)) and value else 0
            amount = flt(value[1]) if isinstance(value, (list, tuple)) and len(value) > 1 else 0
            agg = item_tax_map.setdefault(code, {"rate": 0, "amount": 0})
            agg["rate"] = max(agg["rate"], rate)
            agg["amount"] += amount

    # ── Items ────────────────────────────────────────────────
    items = []
    for item in doc.get("items", []):
        price_list_rate = flt(item.get("price_list_rate")) or flt(item.rate)
        gross_amount = flt(price_list_rate) * flt(item.qty)
        net_amount = flt(item.get("net_amount")) or flt(item.amount)
        tax_info = item_tax_map.get(item.item_code, {})
        tax_rate = flt(tax_info.get("rate"))
        tax_amount = flt(tax_info.get("amount"))
        items.append({
            "idx": item.idx,
            "name": item.name,
            "item_code": item.item_code or "",
            "item_name": item.item_name or "",
            "description": item.get("description") or "",
            "qty": item.qty,
            "uom": item.uom or "",
            "price_list_rate": price_list_rate,
            "gross_amount": gross_amount,
            "rate": item.rate,
            "amount": item.amount,
            "net_rate": item.get("net_rate") or item.rate,
            "net_amount": net_amount,
            "discount_percentage": flt(item.get("discount_percentage")),
            "discount_amount": flt(item.get("discount_amount")),
            "tax_rate": tax_rate,
            "tax_amount": tax_amount,
            "total_with_tax": net_amount + tax_amount,
            "warehouse": item.get("warehouse") or "",
            "delivered_qty": flt(item.get("delivered_qty")),
            "billed_amt": flt(item.get("billed_amt")),
            "custom_a_end": item.get("custom_a_end") or "",
            "custom_z_end": item.get("custom_z_end") or "",
            "custom_dcnet_account_id": (
                item.get("custom_dcnet_account_id")
                or account_fallbacks.get(item.name, "")
            ),
        })

    # ── Timeline (Communications + Comments + ToDos) ─────────
    timeline = _get_timeline("Sales Order", name)

    # ── Comments for Trao đổi tab ─────────────────────────────
    comments = []
    if frappe.has_permission("Comment", "read"):
        comments = frappe.get_list(
            "Comment",
            filters={
                "reference_doctype": "Sales Order",
                "reference_name": name,
                "comment_type": "Comment",
            },
            fields=["name", "comment_by", "comment_by_fullname", "content", "creation"],
            order_by="creation asc",
        )

    # ── Activities (ToDo + Events) ────────────────────────────
    activities = []
    if frappe.has_permission("ToDo", "read"):
        todos = frappe.get_list(
            "ToDo",
            filters={"reference_type": "Sales Order", "reference_name": name},
            fields=[
                "name", "description", "date", "status", "priority",
                "assigned_by_full_name", "owner", "custom_task_type",
                "custom_related_users",
            ],
            order_by="date asc",
        )
        for t in todos:
            t["activity_doctype"] = "ToDo"
        activities.extend(todos)

    if frappe.has_permission("Event", "read"):
        event_names = frappe.get_all(
            "Event Participants",
            filters={"reference_doctype": "Sales Order", "reference_docname": name},
            pluck="parent",
        )
        if event_names:
            events = frappe.get_list(
                "Event",
                filters={"name": ["in", list(set(event_names))]},
                fields=["name", "subject", "event_category", "starts_on", "ends_on", "status", "owner"],
                order_by="starts_on asc",
            )
            for e in events:
                e["activity_doctype"] = "Event"
            activities.extend(events)

    activities.sort(key=lambda x: str(x.get("date") or x.get("starts_on") or ""))

    # ── Contacts ──────────────────────────────────────────────
    contacts = []
    if frappe.has_permission("Contact", "read"):
        contact_names = []
        if doc.contact_person:
            contact_names.append(doc.contact_person)
        if doc.customer:
            linked = frappe.get_all(
                "Dynamic Link",
                filters={"parenttype": "Contact", "link_doctype": "Customer", "link_name": doc.customer},
                pluck="parent",
            )
            contact_names = list(set(contact_names + linked))
        if contact_names:
            contacts = frappe.get_list(
                "Contact",
                filters={"name": ["in", contact_names]},
                fields=["name", "full_name", "email_id", "mobile_no", "designation", "company_name"],
            )

    # ── Related sales docs ────────────────────────────────────
    quotation_links = [d.prevdoc_docname for d in doc.get("items", []) if d.get("prevdoc_docname")]
    quotations = []
    if quotation_links and frappe.has_permission("Quotation", "read"):
        quotations = frappe.get_list(
            "Quotation",
            filters={"name": ["in", list(set(quotation_links))]},
            fields=["name", "transaction_date", "status", "grand_total", "currency"],
            order_by="transaction_date desc",
        )

    delivery_notes = []
    if frappe.has_permission("Delivery Note", "read"):
        dn_links = frappe.get_all(
            "Delivery Note Item",
            filters={"against_sales_order": name, "docstatus": ["<", 2]},
            pluck="parent",
        )
        if dn_links:
            delivery_notes = frappe.get_list(
                "Delivery Note",
                filters={"name": ["in", list(set(dn_links))]},
                fields=["name", "posting_date", "status", "grand_total", "currency"],
                order_by="posting_date desc",
            )

    # The linked-invoice count is derived from the child-item link table (not
    # gated by Sales Invoice permission) so the "Hóa đơn" badge can always
    # show how many exist; only the actual rows (amounts, dates...) require
    # real read permission on Sales Invoice.
    si_links = frappe.get_all(
        "Sales Invoice Item",
        filters={"sales_order": name, "docstatus": ["<", 2]},
        pluck="parent",
    )
    si_links = list(set(si_links))
    invoices_count = len(si_links)

    invoices = []
    if si_links and frappe.has_permission("Sales Invoice", "read"):
        invoices = frappe.get_list(
            "Sales Invoice",
            filters={"name": ["in", si_links]},
            fields=["name", "posting_date", "status", "grand_total", "outstanding_amount", "currency"],
            order_by="posting_date desc",
        )

    sales_returns = []
    if si_links and frappe.has_permission("Sales Invoice", "read"):
        sales_returns = frappe.get_list(
            "Sales Invoice",
            filters={"name": ["in", list(set(si_links))], "is_return": 1},
            fields=["name", "posting_date", "status", "grand_total", "return_against", "currency"],
            order_by="posting_date desc",
        )

    # ── Khác tab: Ghi nhận doanh số ────────────────────────────
    # Only Ngày/Nhân viên/Tình trạng have a real data source today (the
    # revenue-request ToDo workflow, extended with custom_revenue_* fields).
    revenue_recognition_requests = []
    if frappe.has_permission("ToDo", "read"):
        revenue_recognition_requests = frappe.get_list(
            "ToDo",
            filters={
                "reference_type": "Sales Order",
                "reference_name": name,
                "custom_task_type": _SO_REVENUE_REQUEST_TASK_TYPE,
                "status": ["!=", "Cancelled"],
            },
            fields=[
                "name", "owner", "status", "creation",
                "custom_revenue_item", "custom_revenue_department",
                "custom_revenue_recognized_amount", "custom_revenue_achieved_amount",
                "custom_revenue_note",
            ],
            order_by="creation desc",
        )
        item_names = {r.custom_revenue_item for r in revenue_recognition_requests if r.custom_revenue_item}
        item_labels = {
            i.name: i.item_name for i in frappe.get_all(
                "Item", filters={"name": ["in", list(item_names)]}, fields=["name", "item_name"]
            )
        } if item_names else {}
        dept_names = {r.custom_revenue_department for r in revenue_recognition_requests if r.custom_revenue_department}
        dept_labels = {
            d.name: d.department_name for d in frappe.get_all(
                "Department", filters={"name": ["in", list(dept_names)]}, fields=["name", "department_name"]
            )
        } if dept_names else {}
        for row in revenue_recognition_requests:
            row["revenue_item_label"] = item_labels.get(row.custom_revenue_item, row.custom_revenue_item or "")
            row["revenue_department_label"] = dept_labels.get(row.custom_revenue_department, row.custom_revenue_department or "")

    # ── Khác tab: Yêu cầu mua hàng ──────────────────────────────
    purchase_requests = []
    if frappe.has_permission("Material Request", "read"):
        mr_links = frappe.get_all(
            "Material Request Item",
            filters={"sales_order": name, "docstatus": ["<", 2]},
            pluck="parent",
        )
        if mr_links:
            purchase_requests = frappe.get_list(
                "Material Request",
                filters={"name": ["in", list(set(mr_links))]},
                fields=["name", "transaction_date", "status", "material_request_type"],
                order_by="transaction_date desc",
            )

    payment_entries = []
    if frappe.has_permission("Payment Entry", "read"):
        pe_links = frappe.get_all(
            "Payment Entry Reference",
            filters={"reference_doctype": "Sales Order", "reference_name": name, "docstatus": ["<", 2]},
            pluck="parent",
        )
        if pe_links:
            payment_entries = frappe.get_list(
                "Payment Entry",
                filters={"name": ["in", list(set(pe_links))]},
                fields=["name", "posting_date", "paid_amount", "mode_of_payment", "status", "payment_type"],
                order_by="posting_date desc",
            )

    # ── Support tab: Phiếu bảo hành / Thẻ chăm sóc ─────────────
    warranty_claims = []
    if frappe.has_permission("Warranty Claim", "read"):
        warranty_claims = frappe.get_list(
            "Warranty Claim",
            filters={"custom_sales_order": name},
            fields=["name", "complaint", "status", "complaint_date", "warranty_amc_status"],
            order_by="complaint_date desc",
        )

    care_cards = []
    if frappe.has_permission("CRM Care Card", "read"):
        care_cards = frappe.get_list(
            "CRM Care Card",
            filters={"sales_order": name},
            fields=["name", "item", "status", "care_date", "satisfaction_level"],
            order_by="creation desc",
        )

    # ── Attachments ───────────────────────────────────────────
    attachments = []
    if frappe.has_permission("File", "read"):
        attachments = frappe.get_all(
            "File",
            filters={"attached_to_doctype": "Sales Order", "attached_to_name": name},
            fields=["name", "file_name", "file_url", "file_size", "is_private", "creation", "owner"],
            order_by="creation desc",
        )

    # ── Customer / payment / shipping extras for sidebar cards ─
    customer_tax_id = ""
    if doc.customer:
        customer_tax_id = frappe.db.get_value("Customer", doc.customer, "tax_id") or ""

    payment_due_date = None
    schedule = doc.get("payment_schedule") or []
    if schedule:
        due_dates = [row.due_date for row in schedule if row.get("due_date")]
        if due_dates:
            payment_due_date = min(due_dates)
    if not payment_due_date:
        payment_due_date = doc.delivery_date

    grand_total = flt(doc.grand_total)
    paid_amount = flt(doc.advance_paid)
    outstanding_amount = grand_total - paid_amount

    payment = {
        "status": doc.get("custom_payment_status") or ("Đã thanh toán" if outstanding_amount <= 0 and grand_total else "Chưa thanh toán"),
        "due_date": str(payment_due_date) if payment_due_date else None,
        "paid": paid_amount,
        "outstanding": outstanding_amount,
        "grand_total": grand_total,
    }

    shipping = {
        "recipient": doc.get("contact_display") or doc.get("customer_name") or "",
        "phone": doc.get("contact_mobile") or doc.get("contact_phone") or "",
        "address": doc.get("shipping_address") or doc.get("address_display") or "",
        "delivery_date": str(doc.delivery_date) if doc.delivery_date else None,
    }

    document = {
        f: doc.get(f)
        for f in [
            "name", "docstatus", "title", "customer", "customer_name", "customer_group",
            "contact_person", "contact_display", "contact_mobile", "contact_email",
            "contact_phone", "customer_address", "shipping_address_name",
            "status", "order_type", "transaction_date", "delivery_date",
            "po_no", "po_date", "campaign", "currency", "conversion_rate",
            "selling_price_list", "payment_terms_template", "taxes_and_charges",
            "territory", "company", "owner", "creation", "modified",
            "total_qty", "base_total", "total", "base_net_total", "net_total",
            "discount_amount", "base_discount_amount", "total_taxes_and_charges",
            "base_grand_total", "grand_total", "rounded_total",
            "advance_paid", "per_billed", "per_delivered", "delivery_status",
            "billing_status", "tc_name", "terms",
            "custom_revenue_status", "custom_revenue_recognition_date",
            "custom_installation_zone", "custom_contract_duration", "custom_contract_expiry",
            "custom_execution_status", "custom_acceptance_status", "custom_payment_status",
        ]
    }
    document.update(_get_sales_order_display_status(document))
    revenue_requests = (
        _get_open_so_revenue_requests(name)
        if cint(document.get("docstatus")) == 0
        else []
    )
    document["revenue_request_pending"] = bool(revenue_requests)
    document["revenue_request_todo"] = revenue_requests[0].name if revenue_requests else None
    if revenue_requests and document["display_revenue_status"] != "Đã ghi":
        document["display_revenue_status"] = "Đề nghị ghi"

    return {
        "can_write": frappe.has_permission("Sales Order", "write", doc=name),
        "payment": payment,
        "shipping": shipping,
        "customer_tax_id": customer_tax_id,
        "document": document,
        "items": items,
        "timeline": timeline,
        "comments": comments,
        "activities": activities,
        "activity_users": (
            frappe.get_list(
                "User",
                filters={"enabled": 1, "user_type": "System User"},
                fields=["name", "full_name"],
                order_by="full_name asc",
                page_length=200,
            )
            if frappe.has_permission("User", "read")
            else []
        ),
        "contacts": contacts,
        "quotations": quotations,
        "delivery_notes": delivery_notes,
        "invoices": invoices,
        "invoices_count": invoices_count,
        "sales_returns": sales_returns,
        "revenue_recognition_requests": revenue_recognition_requests,
        "purchase_requests": purchase_requests,
        "payment_entries": payment_entries,
        "warranty_claims": warranty_claims,
        "care_cards": care_cards,
        "attachments": attachments,
    }


@frappe.whitelist(methods=["POST"])
def add_so_attachment_link(name, url, title=None):
    """Attach an external link as a File to a Sales Order."""
    _check_permission("Sales Order", "write", name=name)
    url = _normalize_external_url(url)

    file_doc = frappe.get_doc(
        {
            "doctype": "File",
            "file_url": url,
            "file_name": (title or "").strip() or url,
            "attached_to_doctype": "Sales Order",
            "attached_to_name": name,
        }
    )
    file_doc.insert(ignore_permissions=False)
    return {"name": file_doc.name}


@frappe.whitelist(methods=["POST"])
def delete_so_attachment(file_name):
    """Delete a File attached to a Sales Order."""
    file_doc = frappe.get_doc("File", file_name)
    if file_doc.attached_to_doctype != "Sales Order":
        frappe.throw(_("Tệp không thuộc đơn hàng"))
    _check_permission("Sales Order", "write", name=file_doc.attached_to_name)
    file_doc.delete()


@frappe.whitelist(methods=["POST"])
def save_so_activity(sales_order, activity=None):
    """Create or update a task, meeting or call linked to a Sales Order."""
    _check_permission("Sales Order", name=sales_order)
    values = _parse_json(activity, {})
    activity_type = values.get("activity_type") or "task"
    if activity_type not in {"task", "meeting", "call"}:
        frappe.throw(_("Unsupported activity type"), frappe.ValidationError)

    doctype = "ToDo" if activity_type == "task" else "Event"
    document_name = values.get("name")
    if document_name:
        _check_permission(doctype, "write", document_name)
        doc = frappe.get_doc(doctype, document_name)
    else:
        _check_permission(doctype, "create")
        doc = frappe.new_doc(doctype)

    subject = (values.get("subject") or "").strip()
    if not subject:
        frappe.throw(_("Activity subject is required"), frappe.ValidationError)

    if doctype == "ToDo":
        doc.description = subject
        doc.reference_type = "Sales Order"
        doc.reference_name = sales_order
        doc.date = values.get("due_date") or None
        doc.status = values.get("status") or "Open"
        doc.priority = values.get("priority") or "Medium"
        doc.allocated_to = values.get("allocated_to") or frappe.session.user
    else:
        doc.subject = subject
        doc.description = values.get("description") or subject
        doc.event_category = "Call" if activity_type == "call" else "Meeting"
        doc.event_type = "Private"
        doc.starts_on = values.get("starts_on") or frappe.utils.now_datetime()
        doc.ends_on = values.get("ends_on") or None
        doc.status = values.get("status") or "Open"
        doc.reference_doctype = "Sales Order"
        doc.reference_docname = sales_order
        if not any(
            participant.reference_doctype == "Sales Order"
            and participant.reference_docname == sales_order
            for participant in doc.event_participants
        ):
            doc.append(
                "event_participants",
                {"reference_doctype": "Sales Order", "reference_docname": sales_order},
            )
        allocated_to = values.get("allocated_to") or frappe.session.user
        doc.set(
            "event_participants",
            [
                participant
                for participant in doc.event_participants
                if participant.reference_doctype != "User"
            ],
        )
        doc.append(
            "event_participants",
            {"reference_doctype": "User", "reference_docname": allocated_to},
        )

    doc.save()
    return {"doctype": doctype, "name": doc.name}


@frappe.whitelist(methods=["POST"])
def add_so_warranty_claim(sales_order, complaint):
    """Create a Warranty Claim for the order's Hỗ trợ > Phiếu bảo hành tab.

    Customer/company are derived from the Sales Order itself so the CRM form
    only has to ask for the actual complaint text.
    """
    _check_permission("Sales Order", name=sales_order)
    _check_permission("Warranty Claim", "create")
    complaint = (complaint or "").strip()
    if not complaint:
        frappe.throw(_("Nội dung khiếu nại/bảo hành is required"), frappe.ValidationError)

    so = frappe.get_doc("Sales Order", sales_order)
    doc = frappe.get_doc({
        "doctype": "Warranty Claim",
        "naming_series": "SER-WRN-.YYYY.-",
        "customer": so.customer,
        "company": so.company,
        "complaint": complaint,
        "custom_sales_order": sales_order,
    })
    doc.insert()
    return {"name": doc.name}


@frappe.whitelist(methods=["GET"])
def get_so_stock_balance(name):
    """Return stock balance (per warehouse) for each item of a Sales Order.

    Powers the "Tra cứu số lượng tồn" popup on the CRM order detail page.
    For every order line we expose the ordered qty, delivered qty and the
    real stock balance broken down by warehouse (from ``Bin``).
    """
    _check_permission("Sales Order", name=name)
    doc = frappe.get_doc("Sales Order", name)

    # Aggregate ordered / delivered qty per item code (an item may appear on
    # several lines). Keep the first description / uom we encounter.
    by_code = {}
    order_codes = []
    for item in doc.get("items", []):
        code = item.item_code or ""
        if not code:
            continue
        row = by_code.get(code)
        if row is None:
            row = {
                "item_code": code,
                "item_name": item.item_name or item.get("description") or code,
                "uom": item.uom or item.get("stock_uom") or "",
                "qty": 0.0,
                "delivered_qty": 0.0,
                "warehouses": [],
                "balance_qty": 0.0,
            }
            by_code[code] = row
            order_codes.append(code)
        row["qty"] += flt(item.qty)
        row["delivered_qty"] += flt(item.get("delivered_qty"))

    # Pull per-warehouse balances for all involved items in one query.
    if order_codes:
        bins = frappe.get_all(
            "Bin",
            filters={"item_code": ["in", order_codes], "actual_qty": ["!=", 0]},
            fields=["item_code", "warehouse", "actual_qty", "reserved_qty", "projected_qty"],
            order_by="item_code asc, warehouse asc",
        )
        for b in bins:
            row = by_code.get(b.item_code)
            if not row:
                continue
            actual = flt(b.actual_qty)
            row["warehouses"].append({
                "warehouse": b.warehouse,
                "actual_qty": actual,
                "reserved_qty": flt(b.reserved_qty),
                "projected_qty": flt(b.projected_qty),
            })
            row["balance_qty"] += actual

    items = [by_code[code] for code in order_codes]
    return {
        "name": doc.name,
        "items": items,
    }


@frappe.whitelist(methods=["GET"])
def get_so_planned_expenses(sales_order):
    """List "Dự kiến chi" (planned expense) rows for the order's Thu chi tab."""
    _check_permission("Sales Order", name=sales_order)
    _check_permission("SO Planned Expense")
    rows = frappe.get_all(
        "SO Planned Expense",
        filters={"sales_order": sales_order},
        fields=["name", "description", "percentage", "amount", "planned_date", "department"],
        order_by="planned_date asc, creation asc",
    )
    departments = {row.department for row in rows if row.department}
    department_names = {}
    if departments:
        department_names = {
            d.name: d.department_name
            for d in frappe.get_all(
                "Department", filters={"name": ["in", list(departments)]}, fields=["name", "department_name"]
            )
        }
    for row in rows:
        row["department_name"] = department_names.get(row.department, row.department or "")
    return rows


@frappe.whitelist(methods=["POST"])
def add_so_planned_expense(sales_order, description, percentage=None, amount=None, planned_date=None, department=None):
    """Create a "Dự kiến chi" row from the order's Thu chi > Dự kiến chi tab."""
    _check_permission("Sales Order", "write", name=sales_order)
    _check_permission("SO Planned Expense", "create")
    description = (description or "").strip()
    if not description:
        frappe.throw(_("Nội dung chi is required"), frappe.ValidationError)

    doc = frappe.get_doc({
        "doctype": "SO Planned Expense",
        "sales_order": sales_order,
        "description": description,
        "percentage": flt(percentage),
        "amount": flt(amount),
        "planned_date": planned_date or None,
        "department": department or None,
    })
    doc.insert()
    return {"name": doc.name}


@frappe.whitelist(methods=["GET"])
def get_org_unit_children(node_type="root", parent=None):
    """Lazy-load one level of the Company → Chi nhánh → Phòng ban tree used by
    the "Đơn vị" picker on the Dự kiến chi dialog.

    node_type/parent describe the node being expanded: "root" lists companies,
    "company" lists its branches, "branch" lists that branch's top-level
    departments, and "department" lists child departments (Department is a
    native Frappe tree via parent_department/is_group).
    """
    if node_type == "root":
        companies = frappe.get_all("Company", fields=["name"], order_by="name asc")
        return [{"value": c.name, "title": c.name, "node_type": "company", "expandable": True, "selectable": False} for c in companies]

    if not parent:
        return []

    if node_type == "company":
        _check_permission("Branch")
        branches = frappe.get_all("Branch", filters={"company": parent}, fields=["name"], order_by="name asc")
        return [{"value": b.name, "title": b.name, "node_type": "branch", "expandable": True, "selectable": False} for b in branches]

    if node_type == "branch":
        _check_permission("Department")
        # ERPNext always roots every Department under the single company-wide
        # "All Departments" node, so a department scoped to this branch is
        # never truly parent-less — it's "top of this branch's subtree" when
        # its own parent isn't itself another department in the same branch.
        depts = frappe.get_all(
            "Department",
            filters={"branch": parent},
            fields=["name", "department_name", "parent_department", "is_group"],
        )
        names_in_branch = {d.name for d in depts}
        top_level = sorted(
            (d for d in depts if d.parent_department not in names_in_branch),
            key=lambda d: d.department_name or d.name,
        )
        return [{"value": r.name, "title": r.department_name or r.name, "node_type": "department", "expandable": bool(r.is_group), "selectable": True} for r in top_level]

    if node_type == "department":
        _check_permission("Department")
        rows = frappe.get_all(
            "Department",
            filters={"parent_department": parent},
            fields=["name", "department_name", "is_group"],
            order_by="department_name asc",
        )
        return [{"value": r.name, "title": r.department_name or r.name, "node_type": "department", "expandable": bool(r.is_group), "selectable": True} for r in rows]

    return []


@frappe.whitelist(methods=["POST"])
def update_sales_order(name, data):
    """Update header fields + items on a Sales Order from the CRM edit form."""
    _check_permission("Sales Order", "write", name=name)
    if isinstance(data, str):
        data = json.loads(data)

    doc = frappe.get_doc("Sales Order", name)

    # ── Header fields (same short-key → DocType mapping as create_sales_order) ──
    _set_if(doc, data, "title")
    _set_if(doc, data, "delivery_date")
    _set_if(doc, data, "po_no")
    _set_if(doc, data, "po_date")
    _set_if(doc, data, "contact_person")
    _set_if(doc, data, "order_type")
    _set_if(doc, data, "selling_price_list")
    _set_if(doc, data, "currency")
    _set_if(doc, data, "payment_terms_template")
    _set_if(doc, data, "taxes_and_charges")
    _set_if(doc, data, "territory")
    _set_if(doc, data, "company")
    _set_if(doc, data, "utm_campaign", src_key="campaign")

    # Custom fields — Hợp đồng
    _set_if(doc, data, "custom_contract_duration",   src_key="contract_duration")
    _set_if(doc, data, "custom_contract_expiry",     src_key="contract_expiry")
    _set_if(doc, data, "custom_contract_type",       src_key="contract_type")
    _set_if(doc, data, "custom_installation_zone",   src_key="installation_zone")
    _set_if(doc, data, "custom_internal_notes",      src_key="note")
    _set_if(doc, data, "custom_parent_order",        src_key="parent_order")
    _set_if(doc, data, "custom_days_receivable",     src_key="credit_days")
    _set_if(doc, data, "custom_referral_partner",    src_key="referral_partner")

    # Custom fields — Cơ hội
    opportunity = (data.get("opportunity") or "").strip()
    if opportunity and frappe.db.exists("Opportunity", opportunity):
        doc.custom_opportunity = opportunity

    # Custom fields — Tình trạng thực hiện
    _set_if(doc, data, "custom_execution_status",          src_key="execution_status")
    _set_if(doc, data, "custom_revenue_recognition_date",  src_key="revenue_recognition_date")
    _set_if(doc, data, "custom_revenue_status",            src_key="revenue_status")
    _set_if(doc, data, "custom_payment_due_date",          src_key="payment_due_date")
    _set_if(doc, data, "custom_acceptance_date",           src_key="acceptance_date")
    _set_if(doc, data, "custom_liquidation_date",          src_key="liquidation_date")
    _set_if(doc, data, "custom_liquidation_value",         src_key="liquidation_value")
    _set_if(doc, data, "custom_sync_price",                src_key="sync_price")

    # Custom fields — Hóa đơn & Giao hàng
    _set_if(doc, data, "custom_billing_customer",    src_key="billing_customer")
    _set_if(doc, data, "custom_billing_address",     src_key="billing_address")
    _set_if(doc, data, "custom_billing_district",    src_key="billing_district")
    _set_if(doc, data, "custom_billing_ward",        src_key="billing_ward")
    _set_if(doc, data, "custom_billing_street",      src_key="billing_street")
    _set_if(doc, data, "custom_billing_zipcode",     src_key="billing_zipcode")
    _set_if(doc, data, "custom_shipping_recipient",  src_key="shipping_recipient")
    _set_if(doc, data, "custom_shipping_address",    src_key="shipping_address")
    _set_if(doc, data, "custom_shipping_district",   src_key="shipping_district")
    _set_if(doc, data, "custom_shipping_ward",       src_key="shipping_ward")
    _set_if(doc, data, "custom_shipping_street",     src_key="shipping_street")
    _set_if(doc, data, "custom_shipping_zipcode",    src_key="shipping_zipcode")

    # ── Items (when sent from the full edit form) ─────────────────────
    raw_items = data.get("items") if isinstance(data, dict) else None
    if raw_items:
        valid_items = [it for it in raw_items if (it.get("item_code") or "").strip()]
        if not valid_items:
            frappe.throw(_("Cần ít nhất một hàng hóa"), frappe.ValidationError)

        delivery_date = doc.delivery_date or frappe.utils.add_days(doc.transaction_date, 7)
        delivery_date = frappe.utils.getdate(delivery_date).isoformat()

        if doc.docstatus == 1:
            from erpnext.controllers.accounts_controller import update_child_qty_rate

            trans_items = []
            for idx, item in enumerate(valid_items, start=1):
                item_delivery_date = item.get("delivery_date") or delivery_date
                if not isinstance(item_delivery_date, str):
                    item_delivery_date = frappe.utils.getdate(item_delivery_date).isoformat()
                row = {
                    "item_code": (item.get("item_code") or "").strip(),
                    "qty": flt(item.get("qty") or 1),
                    "rate": flt(item.get("rate") or 0),
                    "uom": item.get("uom") or "Cái",
                    "conversion_factor": flt(item.get("conversion_factor")) or 1,
                    "delivery_date": item_delivery_date,
                    "description": item.get("description") or "",
                    "idx": idx,
                }
                docname = item.get("name") or item.get("docname")
                if docname:
                    row["docname"] = docname
                trans_items.append(row)

            update_child_qty_rate("Sales Order", json.dumps(trans_items), name)
            doc.reload()
            return {"name": doc.name, "modified": str(doc.modified)}
        else:
            # Draft: rewrite items wholesale
            doc.set("items", [])
            for item in valid_items:
                item_delivery_date = item.get("delivery_date") or delivery_date
                a_end = item.get("a_end") or item.get("custom_a_end") or ""
                z_end = item.get("z_end") or item.get("custom_z_end") or ""
                item_code = (item.get("item_code") or "").strip()
                if doc.order_type != "Maintenance" and item_code:
                    account_id = _resolve_service_account(doc.customer, item_code, a_end, z_end)
                else:
                    account_id = item.get("account_id") or item.get("custom_dcnet_account_id") or ""
                doc.append("items", {
                    "item_code": item_code,
                    "item_name": item.get("item_name") or item.get("item_code"),
                    "description": item.get("description") or "",
                    "qty": flt(item.get("qty") or 1),
                    "uom": item.get("uom") or "Cái",
                    "conversion_factor": flt(item.get("conversion_factor")) or 1,
                    "price_list_rate": flt(item.get("price_list_rate") or 0),
                    "discount_percentage": flt(item.get("discount_percentage") or 0),
                    "rate": flt(item.get("rate") or 0),
                    "delivery_date": item_delivery_date,
                    "warehouse": item.get("warehouse") or "",
                    "custom_a_end": a_end,
                    "custom_z_end": z_end,
                    "custom_dcnet_account_id": account_id,
                })

    doc.save(ignore_permissions=False)
    return {"name": doc.name, "modified": str(doc.modified)}



@frappe.whitelist(methods=["POST"])
def update_so_items(name, items):
    """Update the line items of a Sales Order from the CRM "Cập nhật hàng hóa" popup.

    - Draft orders (docstatus 0): rewrite the items child table directly and let
      the standard Sales Order controller recompute totals/taxes.
    - Submitted orders (docstatus 1): delegate to ERPNext's official
      ``update_child_qty_rate`` so existing rows are matched by child docname and
      the update-after-submit rules (delivered/billed qty, etc.) are respected.
    """
    _check_permission("Sales Order", "write", name=name)
    if isinstance(items, str):
        items = json.loads(items)
    items = items or []

    valid_items = [it for it in items if (it.get("item_code") or "").strip()]
    if not valid_items:
        frappe.throw(_("Cần ít nhất một hàng hóa"), frappe.ValidationError)

    doc = frappe.get_doc("Sales Order", name)
    delivery_date = doc.delivery_date or frappe.utils.add_days(doc.transaction_date, 7)
    delivery_date = frappe.utils.getdate(delivery_date).isoformat()

    if doc.docstatus == 1:
        from erpnext.controllers.accounts_controller import update_child_qty_rate

        trans_items = []
        for idx, item in enumerate(valid_items, start=1):
            item_delivery_date = item.get("delivery_date") or delivery_date
            if not isinstance(item_delivery_date, str):
                item_delivery_date = frappe.utils.getdate(item_delivery_date).isoformat()
            row = {
                "item_code": (item.get("item_code") or "").strip(),
                "qty": flt(item.get("qty") or 1),
                "rate": flt(item.get("rate") or 0),
                "uom": item.get("uom") or "Cái",
                "conversion_factor": flt(item.get("conversion_factor")) or 1,
                "delivery_date": item_delivery_date,
                "description": item.get("description") or "",
                "idx": idx,
            }
            docname = item.get("name") or item.get("docname")
            if docname:
                row["docname"] = docname
            trans_items.append(row)

        update_child_qty_rate("Sales Order", json.dumps(trans_items), name)
        doc.reload()
        return {"name": doc.name, "modified": str(doc.modified)}

    # Draft order — safe to rewrite the child table wholesale.
    doc.set("items", [])
    for item in valid_items:
        a_end = item.get("a_end") or item.get("custom_a_end") or ""
        z_end = item.get("z_end") or item.get("custom_z_end") or ""
        item_code = (item.get("item_code") or "").strip()
        if doc.order_type != "Maintenance" and item_code:
            account_id = _resolve_service_account(doc.customer, item_code, a_end, z_end)
        else:
            account_id = item.get("account_id") or item.get("custom_dcnet_account_id") or ""
        doc.append("items", {
            "item_code": item_code,
            "item_name": item.get("item_name") or item.get("item_code"),
            "description": item.get("description") or "",
            "qty": flt(item.get("qty") or 1),
            "uom": item.get("uom") or "Cái",
            "conversion_factor": flt(item.get("conversion_factor")) or 1,
            "price_list_rate": flt(item.get("price_list_rate") or 0),
            "discount_percentage": flt(item.get("discount_percentage") or 0),
            "rate": flt(item.get("rate") or 0),
            "delivery_date": item.get("delivery_date") or delivery_date,
            "warehouse": item.get("warehouse") or "",
            "custom_a_end": a_end,
            "custom_z_end": z_end,
            "custom_dcnet_account_id": account_id,
        })

    doc.save(ignore_permissions=False)
    return {"name": doc.name, "modified": str(doc.modified)}

@frappe.whitelist(methods=["GET"])
def get_so_form_options(customer=None):
    """Return all dropdown options needed for the Sales Order inline form."""
    _check_permission("Sales Order", "create")

    def opts(doctype, fields, order_by="name asc", page_length=500, filters=None):
        if not frappe.has_permission(doctype, "read"):
            return []
        try:
            return frappe.get_list(
                doctype,
                fields=fields,
                filters=filters or {},
                order_by=order_by,
                page_length=page_length,
            )
        except Exception:
            return []

    items = opts(
        "Item", ["name", "item_name", "stock_uom", "item_group"],
        order_by="item_name asc", page_length=2000, filters={"disabled": 0, "is_sales_item": 1},
    )

    opportunities = []
    contacts = []
    if customer:
        if frappe.has_permission("Opportunity", "read"):
            opportunities = frappe.get_list(
                "Opportunity",
                filters={"opportunity_from": "Customer", "party_name": customer, "status": ["!=", "Closed"]},
                fields=["name", "title"],
                order_by="modified desc",
                page_length=100,
            )
        if frappe.has_permission("Contact", "read"):
            contact_names = frappe.get_all(
                "Dynamic Link",
                filters={"parenttype": "Contact", "link_doctype": "Customer", "link_name": customer},
                pluck="parent",
            )
            if contact_names:
                contacts = frappe.get_list(
                    "Contact",
                    filters={"name": ["in", contact_names]},
                    fields=["name", "full_name", "mobile_no"],
                    order_by="full_name asc",
                    page_length=100,
                )

    return {
        "items": items,
        "customers": opts(
            "Customer", ["name", "customer_name", "tax_id", "mobile_no", "primary_address"],
            order_by="customer_name asc", page_length=2000,
        ),
        "opportunities": opportunities,
        "contacts": contacts,
        "price_lists": opts("Price List", ["name"], filters={"selling": 1}),
        "payment_terms": opts("Payment Terms Template", ["name"]),
        "territories": opts("Territory", ["name"]),
        "campaigns": opts("UTM Campaign", ["name"]),
        "taxes_templates": opts("Sales Taxes and Charges Template", ["name"]),
    }


def _default_selling_warehouse(company):
    """A sensible default warehouse for stock items on a CRM Sales Order."""
    if not company:
        return None
    wh = frappe.db.get_single_value("Stock Settings", "default_warehouse")
    if wh and frappe.db.get_value("Warehouse", wh, "company") == company:
        return wh
    return frappe.db.get_value("Warehouse", {"company": company, "is_group": 0}, "name")


def _apply_tax_template(doc):
    """Populate the tax table from the selected template (the JS form does this
    on the desk; we must do it server-side when inserting headlessly).

    Rows whose account head no longer exists are skipped so a mis-configured
    template never blocks order creation."""
    if not (doc.get("taxes_and_charges") and not doc.get("taxes")):
        return
    try:
        from erpnext.controllers.accounts_controller import get_taxes_and_charges
        rows = get_taxes_and_charges("Sales Taxes and Charges Template", doc.taxes_and_charges)
    except Exception:
        return
    for tax in rows:
        head = tax.get("account_head")
        if head and not frappe.db.exists("Account", head):
            continue
        doc.append("taxes", tax)
    # If every row was skipped, drop the template link so validation stays clean.
    if not doc.get("taxes"):
        doc.taxes_and_charges = ""


@frappe.whitelist(methods=["POST"])
def create_sales_order(data):
    """Create a Sales Order from the inline CRM form."""
    _check_permission("Sales Order", "create")
    if isinstance(data, str):
        data = json.loads(data)

    customer = (data.get("customer") or "").strip()
    if not customer:
        frappe.throw(_("Khách hàng là bắt buộc"), frappe.ValidationError)

    transaction_date = data.get("transaction_date") or frappe.utils.today()
    delivery_date = data.get("delivery_date") or frappe.utils.add_days(transaction_date, 7)

    doc = frappe.new_doc("Sales Order")
    doc.customer = customer
    doc.transaction_date = transaction_date
    doc.delivery_date = delivery_date
    doc.order_type = data.get("order_type") or "Sales"
    doc.po_no = data.get("po_no") or ""
    doc.po_date = data.get("po_date") or None
    doc.contact_person = data.get("contact_person") or ""
    doc.title = data.get("title") or ""

    # Standard optional fields
    _set_if(doc, data, "company")
    _set_if(doc, data, "currency")
    _set_if(doc, data, "selling_price_list")
    _set_if(doc, data, "territory")
    _set_if(doc, data, "payment_terms_template")
    _set_if(doc, data, "taxes_and_charges")
    _set_if(doc, data, "utm_campaign", src_key="campaign")

    # Custom fields — Hợp đồng
    _set_if(doc, data, "custom_contract_duration", src_key="contract_duration")
    _set_if(doc, data, "custom_contract_expiry", src_key="contract_expiry")
    _set_if(doc, data, "custom_installation_zone", src_key="installation_zone")
    _set_if(doc, data, "custom_internal_notes", src_key="note")

    # Custom fields — Cơ hội
    opportunity = data.get("opportunity") or ""
    if opportunity and frappe.db.exists("Opportunity", opportunity):
        doc.custom_opportunity = opportunity

    # Custom fields — Tình trạng thực hiện
    doc.custom_execution_status = data.get("execution_status") or "Chưa thực hiện"
    _set_if(doc, data, "custom_revenue_recognition_date", src_key="revenue_recognition_date")
    _set_if(doc, data, "custom_payment_due_date", src_key="payment_due_date")

    # Custom fields — Hóa đơn & Giao hàng
    _set_if(doc, data, "custom_billing_customer", src_key="billing_customer")
    _set_if(doc, data, "custom_billing_address", src_key="billing_address")
    _set_if(doc, data, "custom_shipping_recipient", src_key="shipping_recipient")
    _set_if(doc, data, "custom_shipping_address", src_key="shipping_address")

    order_type = doc.order_type
    default_wh = _default_selling_warehouse(doc.company)
    items = data.get("items") or []
    for item in items:
        item_code = (item.get("item_code") or "").strip()
        if not item_code:
            continue
        item_delivery_date = item.get("delivery_date") or delivery_date
        a_end = item.get("a_end") or ""
        z_end = item.get("z_end") or ""
        # Service accounts are created only here (on save), not while editing the form.
        if order_type != "Maintenance":
            account_id = _resolve_service_account(customer, item_code, a_end, z_end)
        else:
            account_id = item.get("account_id") or ""
        # Stock items need a delivery warehouse — fall back to the company default.
        is_stock = frappe.get_cached_value("Item", item_code, "is_stock_item")
        warehouse = item.get("warehouse") or (default_wh if is_stock else "")
        doc.append("items", {
            "item_code": item_code,
            "item_name": item.get("item_name") or item_code,
            "description": item.get("description") or "",
            "qty": flt(item.get("qty") or 1),
            "uom": item.get("uom") or "Cái",
            "conversion_factor": flt(item.get("conversion_factor")) or 1,
            "price_list_rate": flt(item.get("price_list_rate") or 0),
            "discount_percentage": flt(item.get("discount_percentage") or 0),
            "rate": flt(item.get("rate") or 0),
            "delivery_date": item_delivery_date,
            "warehouse": warehouse,
            "custom_a_end": a_end,
            "custom_z_end": z_end,
            "custom_dcnet_account_id": account_id,
            "prevdoc_docname": item.get("prevdoc_docname") or None,
        })

    if not doc.items:
        frappe.throw(_("Cần ít nhất một sản phẩm"), frappe.ValidationError)

    _apply_tax_template(doc)

    # Populate the mandatory currency / exchange-rate fields so the Sales Order
    # passes validation (Tỷ giá, Tiền tệ Bảng giá, Tỷ giá bảng giá).
    company_currency = frappe.get_cached_value("Company", doc.company, "default_currency") if doc.company else None
    doc.currency = doc.currency or company_currency or "VND"
    if not flt(doc.conversion_rate):
        if company_currency and doc.currency != company_currency:
            try:
                from erpnext.setup.utils import get_exchange_rate
                doc.conversion_rate = get_exchange_rate(doc.currency, company_currency, doc.transaction_date) or 1
            except Exception:
                doc.conversion_rate = 1
        else:
            doc.conversion_rate = 1
    doc.price_list_currency = doc.price_list_currency or doc.currency
    if not flt(doc.plc_conversion_rate):
        doc.plc_conversion_rate = doc.conversion_rate if doc.price_list_currency == doc.currency else 1

    doc.insert(ignore_permissions=False)
    return {"name": doc.name, "grand_total": doc.grand_total}

@frappe.whitelist(methods=["GET"])
def get_quotation_form_options(customer=None):
    """Return dropdown options for the inline Quotation form."""
    _check_permission("Quotation", "create")

    def opts(doctype, fields, order_by="name asc", page_length=500, filters=None):
        if not frappe.has_permission(doctype, "read"):
            return []
        try:
            return frappe.get_list(
                doctype,
                fields=fields,
                filters=filters or {},
                order_by=order_by,
                page_length=page_length,
            )
        except Exception:
            return []

    items = opts(
        "Item", ["name", "item_name", "stock_uom", "item_group"],
        order_by="item_name asc", page_length=2000, filters={"disabled": 0, "is_sales_item": 1},
    )

    opportunities = []
    contacts = []
    if customer:
        if frappe.has_permission("Opportunity", "read"):
            opportunities = frappe.get_list(
                "Opportunity",
                filters={"opportunity_from": "Customer", "party_name": customer, "status": ["!=", "Closed"]},
                fields=["name", "title"],
                order_by="modified desc",
                page_length=100,
            )
        if frappe.has_permission("Contact", "read"):
            contact_names = frappe.get_all(
                "Dynamic Link",
                filters={"parenttype": "Contact", "link_doctype": "Customer", "link_name": customer},
                pluck="parent",
            )
            if contact_names:
                contacts = frappe.get_list(
                    "Contact",
                    filters={"name": ["in", contact_names]},
                    fields=["name", "full_name", "mobile_no"],
                    order_by="full_name asc",
                    page_length=100,
                )

    return {
        "items": items,
        "customers": opts(
            "Customer", ["name", "customer_name", "tax_id", "mobile_no", "primary_address"],
            order_by="customer_name asc", page_length=2000,
        ),
        "opportunities": opportunities,
        "contacts": contacts,
        "price_lists": opts("Price List", ["name"], filters={"selling": 1}),
        "payment_terms": opts("Payment Terms Template", ["name"]),
        "territories": opts("Territory", ["name"]),
        "campaigns": opts("UTM Campaign", ["name"]),
        "taxes_templates": opts("Sales Taxes and Charges Template", ["name"]),
    }

@frappe.whitelist(methods=["POST"])
def create_quotation(data):
    """Create a Quotation from the inline CRM form (mẫu báo giá DVVT)."""
    _check_permission("Quotation", "create")
    if isinstance(data, str):
        data = json.loads(data)

    customer = (data.get("customer") or "").strip()
    if not customer:
        frappe.throw(_("Khách hàng là bắt buộc"), frappe.ValidationError)
    _check_permission("Customer", name=customer)

    transaction_date = data.get("transaction_date") or frappe.utils.today()

    doc = frappe.new_doc("Quotation")
    doc.quotation_to = "Customer"
    doc.party_name = customer
    doc.transaction_date = transaction_date
    doc.valid_till = data.get("valid_till") or None
    doc.order_type = data.get("order_type") or "Sales"
    doc.contact_person = data.get("contact_person") or ""

    _set_if(doc, data, "company")
    _set_if(doc, data, "currency")
    _set_if(doc, data, "selling_price_list")
    _set_if(doc, data, "territory")
    _set_if(doc, data, "payment_terms_template")
    _set_if(doc, data, "taxes_and_charges")
    _set_if(doc, data, "utm_campaign", src_key="campaign")

    quotation_meta = frappe.get_meta("Quotation")

    if quotation_meta.has_field("title"):
        doc.title = data.get("title") or ""
    if quotation_meta.has_field("opportunity") and data.get("opportunity"):
        doc.opportunity = data.get("opportunity")

    # Optional custom fields — only set when they already exist on the DocType
    optional_custom = {
        "custom_installation_zone": data.get("installation_zone"),
        "custom_contract_duration": data.get("contract_duration"),
        "custom_internal_notes": data.get("note"),
        "custom_implementation_time": data.get("implementation_time"),
        "custom_sla": data.get("sla"),
        "custom_is_shared": data.get("shared_flag"),
        "custom_opportunity": data.get("opportunity"),
    }
    for fieldname, value in optional_custom.items():
        if not quotation_meta.has_field(fieldname):
            continue
        if fieldname == "custom_is_shared":
            doc.set(fieldname, cint(value))
        elif value:
            doc.set(fieldname, value)

    item_meta = frappe.get_meta("Quotation Item")
    item_optional = ("custom_a_end", "custom_z_end", "custom_dcnet_account_id")
    for item in (data.get("items") or []):
        item_code = (item.get("item_code") or "").strip()
        if not item_code:
            continue
        row = {
            "item_code": item_code,
            "item_name": item.get("item_name") or item_code,
            "description": item.get("description") or "",
            "qty": flt(item.get("qty") or 1),
            "uom": item.get("uom") or "Cái",
            "conversion_factor": flt(item.get("conversion_factor")) or 1,
            "price_list_rate": flt(item.get("price_list_rate") or 0),
            "discount_percentage": flt(item.get("discount_percentage") or 0),
            "rate": flt(item.get("rate") or 0),
        }
        src = {"custom_a_end": item.get("a_end"), "custom_z_end": item.get("z_end"),
               "custom_dcnet_account_id": item.get("account_id")}
        for fieldname in item_optional:
            if item_meta.has_field(fieldname) and src.get(fieldname):
                row[fieldname] = src[fieldname]
        doc.append("items", row)

    if not doc.items:
        frappe.throw(_("Cần ít nhất một sản phẩm"), frappe.ValidationError)

    _apply_tax_template(doc)

    company_currency = frappe.get_cached_value("Company", doc.company, "default_currency") if doc.company else None
    doc.currency = doc.currency or company_currency or "VND"
    if not flt(doc.conversion_rate):
        if company_currency and doc.currency != company_currency:
            try:
                from erpnext.setup.utils import get_exchange_rate
                doc.conversion_rate = get_exchange_rate(doc.currency, company_currency, doc.transaction_date) or 1
            except Exception:
                doc.conversion_rate = 1
        else:
            doc.conversion_rate = 1
    doc.price_list_currency = doc.price_list_currency or doc.currency
    if not flt(doc.plc_conversion_rate):
        doc.plc_conversion_rate = doc.conversion_rate if doc.price_list_currency == doc.currency else 1

    doc.insert(ignore_permissions=False)
    return {"name": doc.name, "grand_total": doc.grand_total}



@frappe.whitelist(methods=["POST"])
def save_opportunity(opportunity=None):
    """Create an Opportunity from the internal CRM workspace."""
    _check_permission("Opportunity", "create")
    values = _parse_json(opportunity, {})

    party_name = (values.get("party_name") or "").strip()
    if not party_name:
        frappe.throw(_("Customer is required"), frappe.ValidationError)
    _check_permission("Customer", name=party_name)

    doc = frappe.new_doc("Opportunity")
    doc.opportunity_from = "Customer"
    doc.party_name = party_name
    doc.company = values.get("company") or frappe.defaults.get_user_default("Company")
    doc.transaction_date = values.get("transaction_date") or frappe.utils.today()
    doc.expected_closing = values.get("expected_closing") or None
    doc.opportunity_type = values.get("opportunity_type") or None
    doc.sales_stage = values.get("sales_stage") or None
    doc.probability = flt(values.get("probability") or 0)
    doc.contact_person = values.get("contact_person") or None
    doc.territory = values.get("territory") or None
    doc.utm_source = values.get("utm_source") or None
    doc.opportunity_owner = values.get("opportunity_owner") or frappe.session.user
    # `notes` on Opportunity is a child table (CRM Note), not a text field.
    # Capture the description text here and append it as a row before insert.
    note_text = (values.get("notes") or "").strip()

    opportunity_meta = frappe.get_meta("Opportunity")
    custom_values = {
        "custom_auto_increase_duplicate_qty": values.get("custom_auto_increase_duplicate_qty"),
        "custom_shipping_country": values.get("custom_shipping_country"),
        "custom_shipping_state": values.get("custom_shipping_state"),
        "custom_shipping_county": values.get("custom_shipping_county"),
        "custom_shipping_ward": values.get("custom_shipping_ward"),
        "custom_shipping_address_line1": values.get("custom_shipping_address_line1"),
        "custom_shipping_pincode": values.get("custom_shipping_pincode"),
        "custom_shipping_address": values.get("custom_shipping_address"),
        "custom_is_shared": values.get("custom_is_shared"),
        "custom_referral_partner": values.get("custom_referral_partner"),
    }
    for fieldname, value in custom_values.items():
        if opportunity_meta.has_field(fieldname):
            if fieldname in {
                "custom_auto_increase_duplicate_qty",
                "custom_is_shared",
            }:
                doc.set(fieldname, cint(value))
            else:
                doc.set(fieldname, value or None)

    title = (values.get("title") or "").strip()
    if title and opportunity_meta.has_field("title"):
        doc.title = title

    item_meta = frappe.get_meta("Opportunity Item")
    for item in _parse_json(values.get("items"), []):
        item_code = (item.get("item_code") or "").strip()
        item_name = (item.get("item_name") or "").strip()
        if not item_code and not item_name:
            continue
        row = doc.append("items", {})
        if item_code:
            row.item_code = item_code
        row.item_name = item_name or item_code
        row.description = item.get("description") or item_name or item_code
        row.qty = flt(item.get("qty") or 1)
        row.uom = item.get("uom") or None
        row.rate = flt(item.get("rate") or 0)
        if item_meta.has_field("amount"):
            row.amount = row.qty * row.rate
        if item_meta.has_field("custom_installation_point_a_end"):
            row.custom_installation_point_a_end = (
                item.get("custom_installation_point_a_end") or None
            )
        if item_meta.has_field("custom_installation_point_z_end"):
            row.custom_installation_point_z_end = (
                item.get("custom_installation_point_z_end") or None
            )

    doc.opportunity_amount = sum(flt(row.amount) for row in doc.get("items", []))

    if note_text:
        note_row = {"note": note_text}
        crm_note_meta = frappe.get_meta("CRM Note")
        if crm_note_meta.has_field("added_by"):
            note_row["added_by"] = frappe.session.user
        if crm_note_meta.has_field("added_on"):
            note_row["added_on"] = frappe.utils.now()
        doc.append("notes", note_row)

    for table_field in doc.meta.get_table_fields():
        if doc.get(table_field.fieldname) is None:
            doc.set(table_field.fieldname, [])

    doc.insert()
    if opportunity_meta.has_field("custom_opportunity_code"):
        doc.db_set("custom_opportunity_code", doc.name, update_modified=False)
    return {"name": doc.name}


@frappe.whitelist(methods=["GET"])
def get_lead_form_options():
    """Return dropdown options for the Lead create/edit form."""
    _check_permission("Lead", "create")

    def options(doctype, fields, order_by="name asc", page_length=500, filters=None):
        if not frappe.has_permission(doctype, "read"):
            return []
        return frappe.get_list(doctype, fields=fields, order_by=order_by, page_length=page_length, filters=filters)

    return {
        "salutations": options("Salutation", ["name"]),
        "sources": options("UTM Source", ["name"]),
        "industries": options("Industry Type", ["name"]),
        "countries": options("Country", ["name"]),
        "companies": options("Company", ["name"]),
        "items": options(
            "Item",
            ["name", "item_name", "stock_uom", "item_group"],
            order_by="item_name asc",
            page_length=2000,
            filters={"disabled": 0, "is_sales_item": 1},
        ),
    }


def _get_reference_activities(reference_doctype, reference_name):
    """Return permission-filtered ToDo and Event rows for a CRM document."""
    activities = []
    if frappe.has_permission("ToDo", "read"):
        todos = frappe.get_list(
            "ToDo",
            filters={
                "reference_type": reference_doctype,
                "reference_name": reference_name,
            },
            fields=[
                "name", "description", "date", "status", "priority",
                "allocated_to", "owner", "creation", "modified",
            ],
            order_by="date desc, modified desc",
            page_length=200,
        )
        for todo in todos:
            performed_by = todo.allocated_to or todo.owner
            activities.append(
                {
                    **todo,
                    "subject": todo.description,
                    "activity_type": "task",
                    "due_date": todo.date,
                    "starts_on": None,
                    "ends_on": None,
                    "performed_by": performed_by,
                    "performed_by_name": frappe.utils.get_fullname(performed_by),
                }
            )

    if frappe.has_permission("Event", "read"):
        event_names = frappe.get_all(
            "Event Participants",
            filters={
                "parenttype": "Event",
                "reference_doctype": reference_doctype,
                "reference_docname": reference_name,
            },
            pluck="parent",
        )
        event_filters = {"name": ["in", list(set(event_names))]} if event_names else {
            "reference_doctype": reference_doctype,
            "reference_docname": reference_name,
        }
        events = frappe.get_list(
            "Event",
            filters=event_filters,
            fields=[
                "name", "subject", "description", "event_category", "starts_on",
                "ends_on", "status", "owner", "creation", "modified",
            ],
            order_by="starts_on desc, modified desc",
            page_length=200,
        )
        assigned_users = {}
        if events:
            participants = frappe.get_all(
                "Event Participants",
                filters={
                    "parenttype": "Event",
                    "parent": ["in", [event.name for event in events]],
                    "reference_doctype": "User",
                },
                fields=["parent", "reference_docname"],
            )
            assigned_users = {
                participant.parent: participant.reference_docname
                for participant in participants
            }
        for event in events:
            performed_by = assigned_users.get(event.name) or event.owner
            activities.append(
                {
                    **event,
                    "activity_type": "call" if event.event_category == "Call" else "meeting",
                    "due_date": event.starts_on,
                    "performed_by": performed_by,
                    "performed_by_name": frappe.utils.get_fullname(performed_by),
                }
            )

    return sorted(
        activities,
        key=lambda row: str(row.get("due_date") or row.get("modified") or ""),
        reverse=True,
    )


def _get_lead_activities(lead):
    """Return activities linked to a Lead."""
    return _get_reference_activities("Lead", lead)


def _get_contact_activities(contact):
    """Return activities linked to a Contact."""
    return _get_reference_activities("Contact", contact)


@frappe.whitelist(methods=["GET"])
def get_lead_detail(name):
    """Return all data needed to render the Lead detail page."""
    _check_permission("Lead", name=name)
    doc = frappe.get_doc("Lead", name)
    lead_meta = frappe.get_meta("Lead")
    all_fields = [
        "name", "lead_name", "salutation", "first_name", "last_name", "middle_name",
        "email_id", "mobile_no", "phone", "source", "utm_source", "status", "lead_owner",
        "company_name", "job_title", "department", "industry", "territory",
        "country", "state", "city", "pincode", "address_line1", "address_line2",
        "notes", "creation", "modified", "owner",
        "custom_lead_type", "custom_zalo", "custom_work_email", "custom_tax_id",
        "custom_bank_account", "custom_bank_name", "custom_founding_date",
        "custom_business_type", "custom_sector", "custom_district", "custom_ward",
        "custom_full_address", "custom_is_shared",
    ]
    document = {
        f: doc.get(f)
        for f in all_fields
        if f in {"name", "creation", "modified", "owner"} or lead_meta.has_field(f)
    }
    if "notes" in document:
        document["notes"] = _display_notes_value(document.get("notes"))

    comments = []
    if frappe.has_permission("Comment", "read"):
        comments = frappe.get_list(
            "Comment",
            filters={
                "reference_doctype": "Lead",
                "reference_name": name,
                "comment_type": "Comment",
            },
            fields=["name", "comment_by", "comment_by_fullname", "content", "creation"],
            order_by="creation asc",
        )

    activities = _get_lead_activities(name)
    timeline = [
        row for row in _get_timeline("Lead", name)
        if row.get("activity_type") != "task"
    ]
    timeline.extend(
        {
            **row,
            "content": row.get("description") or row.get("subject"),
            "creation": row.get("creation") or row.get("starts_on") or row.get("due_date"),
        }
        for row in activities
    )
    timeline = sorted(
        timeline,
        key=lambda row: str(row.get("creation") or ""),
        reverse=True,
    )[:100]
    attachments = []
    if frappe.has_permission("File", "read"):
        attachments = frappe.get_all(
            "File",
            filters={"attached_to_doctype": "Lead", "attached_to_name": name},
            fields=["name", "file_name", "file_url", "is_private", "file_size", "owner", "creation"],
            order_by="creation desc",
            limit_page_length=100,
        )
    return {
        "document": document,
        "timeline": timeline,
        "activities": activities,
        "comments": comments,
        "activity_campaigns": (
            frappe.get_list(
                "UTM Campaign",
                fields=["name"],
                order_by="name asc",
                page_length=200,
            )
            if frappe.has_permission("UTM Campaign", "read")
            else []
        ),
        "activity_users": (
            frappe.get_list(
                "User",
                filters={"enabled": 1, "user_type": "System User"},
                fields=["name", "full_name"],
                order_by="full_name asc",
                page_length=200,
            )
            if frappe.has_permission("User", "read")
            else [{
                "name": frappe.session.user,
                "full_name": frappe.utils.get_fullname(frappe.session.user),
            }]
        ),
        "attachments": attachments,
        "can_write": frappe.has_permission("Lead", "write", doc=name),
        "can_create_activity": (
            frappe.has_permission("ToDo", "create")
            or frappe.has_permission("Event", "create")
        ),
    }


def _save_crm_activity(reference_doctype, reference_name, activity=None):
    """Create a standard ToDo, meeting or call linked to a CRM document."""
    _check_permission(reference_doctype, "write", name=reference_name)
    values = _parse_json(activity, {})
    activity_type = values.get("activity_type") or "task"
    if activity_type not in {"task", "meeting", "call"}:
        frappe.throw(_("Loại hoạt động không được hỗ trợ"), frappe.ValidationError)

    subject = (values.get("subject") or "").strip()
    if not subject:
        frappe.throw(_("Tiêu đề là bắt buộc"), frappe.ValidationError)

    doctype = "ToDo" if activity_type == "task" else "Event"
    _check_permission(doctype, "create")
    doc = frappe.new_doc(doctype)
    allocated_to = values.get("allocated_to") or frappe.session.user
    status = values.get("status") or "Open"
    if status == "Completed":
        status = "Closed"

    if doctype == "ToDo":
        doc.description = subject
        doc.reference_type = reference_doctype
        doc.reference_name = reference_name
        doc.date = values.get("due_date") or None
        doc.status = status if status in {"Open", "Closed", "Cancelled"} else "Open"
        doc.priority = values.get("priority") or "Medium"
        doc.allocated_to = allocated_to
        optional_fields = {
            "custom_task_type": values.get("task_type"),
            "custom_campaign": values.get("campaign"),
            "custom_related_user": values.get("related_to"),
            "custom_due_time": values.get("due_time"),
        }
        for fieldname, value in optional_fields.items():
            if value and doc.meta.has_field(fieldname):
                doc.set(fieldname, value)
    else:
        starts_on = values.get("starts_on") or frappe.utils.now_datetime()
        ends_on = values.get("ends_on") or None
        if ends_on and frappe.utils.get_datetime(ends_on) < frappe.utils.get_datetime(starts_on):
            frappe.throw(_("Ngày kết thúc phải sau ngày bắt đầu"), frappe.ValidationError)
        description = (values.get("description") or "").strip()
        call_result = (values.get("call_result") or "").strip()
        call_type = (values.get("call_type") or "").strip()
        if call_type:
            description = f"{description}\nLoại cuộc gọi: {call_type}".strip()
        if call_result:
            description = f"{description}\nKết quả gọi điện: {call_result}".strip()
        doc.subject = subject
        doc.description = description or subject
        doc.event_category = "Call" if activity_type == "call" else "Meeting"
        doc.event_type = "Private"
        doc.starts_on = starts_on
        doc.ends_on = ends_on
        doc.status = status if status in {"Open", "Closed", "Cancelled"} else "Open"
        doc.reference_doctype = reference_doctype
        doc.reference_docname = reference_name
        if doc.meta.has_field("all_day"):
            doc.all_day = cint(values.get("all_day") or 0)
        if doc.meta.has_field("location"):
            doc.location = (values.get("location") or "").strip()
        doc.append(
            "event_participants",
            {
                "reference_doctype": reference_doctype,
                "reference_docname": reference_name,
            },
        )
        doc.append(
            "event_participants",
            {"reference_doctype": "User", "reference_docname": allocated_to},
        )
        campaign = (values.get("campaign") or "").strip()
        if campaign:
            doc.append(
                "event_participants",
                {"reference_doctype": "UTM Campaign", "reference_docname": campaign},
            )
        related_to = (values.get("related_to") or "").strip()
        if related_to and related_to != allocated_to:
            doc.append(
                "event_participants",
                {"reference_doctype": "User", "reference_docname": related_to},
            )
        optional_fields = {
            "custom_call_type": call_type,
            "custom_call_result": call_result,
            "custom_campaign": campaign,
            "custom_related_user": related_to,
        }
        for fieldname, value in optional_fields.items():
            if value and doc.meta.has_field(fieldname):
                doc.set(fieldname, value)

    doc.insert(ignore_permissions=False)
    return {"doctype": doctype, "name": doc.name}


@frappe.whitelist(methods=["POST"])
def save_lead_activity(lead, activity=None):
    """Create a standard ToDo, meeting or call linked to a Lead."""
    return _save_crm_activity("Lead", lead, activity)


@frappe.whitelist(methods=["POST"])
def save_contact_activity(contact, activity=None):
    """Create a standard ToDo, meeting or call linked to a Contact."""
    return _save_crm_activity("Contact", contact, activity)


def _normalize_external_url(url):
    """Return an external URL with HTTPS as the default scheme."""
    url = (url or "").strip()
    if not url:
        frappe.throw(_("Liên kết là bắt buộc"), frappe.ValidationError)
    if not url.lower().startswith(("http://", "https://")):
        url = f"https://{url.lstrip('/')}"
    if url.lower() in {"http://", "https://"}:
        frappe.throw(_("Liên kết không hợp lệ"), frappe.ValidationError)
    return url


@frappe.whitelist(methods=["POST"])
def add_lead_attachment_link(name, url, title=None):
    """Attach an external URL to a Lead as a standard File record."""
    _check_permission("Lead", "write", name=name)
    url = _normalize_external_url(url)

    file_doc = frappe.get_doc(
        {
            "doctype": "File",
            "file_url": url,
            "file_name": (title or "").strip() or url,
            "attached_to_doctype": "Lead",
            "attached_to_name": name,
        }
    )
    file_doc.insert(ignore_permissions=False)
    return {"name": file_doc.name}


def _append_note_value(doc, table_fieldname, content):
    """Append text to a Frappe note child table, or set a plain field fallback."""
    content = (content or "").strip()
    if not content:
        return

    field = doc.meta.get_field(table_fieldname)
    if not field:
        return
    if field.fieldtype != "Table":
        doc.set(table_fieldname, content)
        return

    row = {"note": content}
    child_meta = frappe.get_meta(field.options)
    if child_meta.has_field("added_by"):
        row["added_by"] = frappe.session.user
    if child_meta.has_field("added_on"):
        row["added_on"] = frappe.utils.now()
    doc.append(table_fieldname, row)


@frappe.whitelist(methods=["POST"])
def save_lead(lead=None):
    """Create a new Lead from the internal CRM form."""
    _check_permission("Lead", "create")
    values = _parse_json(lead, {})
    first_name = (values.get("first_name") or "").strip()
    if not first_name:
        frappe.throw(_("Tên là bắt buộc"), frappe.ValidationError)
    mobile_no = (values.get("mobile_no") or "").strip()
    if not mobile_no:
        frappe.throw(_("ĐT di động là bắt buộc"), frappe.ValidationError)

    doc = frappe.new_doc("Lead")
    lead_meta = frappe.get_meta("Lead")
    simple_fields = [
        "salutation", "first_name", "last_name", "middle_name",
        "email_id", "mobile_no", "phone", "source", "utm_source", "status", "lead_owner",
        "company_name", "job_title", "department", "industry", "territory",
        "country", "state", "city", "pincode", "address_line1", "address_line2",
        "custom_lead_type", "custom_zalo", "custom_work_email", "custom_tax_id",
        "custom_bank_account", "custom_bank_name", "custom_founding_date",
        "custom_business_type", "custom_sector", "custom_district", "custom_ward",
        "custom_full_address",
    ]
    for f in simple_fields:
        v = values.get(f)
        if v is not None and (f in {"name", "creation", "modified"} or lead_meta.has_field(f)):
            doc.set(f, v or None)
    if lead_meta.has_field("custom_is_shared"):
        doc.set("custom_is_shared", cint(values.get("custom_is_shared") or 0))
    _append_note_value(doc, "notes", values.get("notes"))
    doc.status = values.get("status") or "Lead"
    doc.insert()
    _delete_auto_created_lead_contacts(doc.name)
    return {"name": doc.name}


def _delete_auto_created_lead_contacts(lead_name):
    """Keep DCNET Leads out of the Contact list until explicitly approved."""
    contact_names = frappe.get_all(
        "Dynamic Link",
        filters={
            "parenttype": "Contact",
            "link_doctype": "Lead",
            "link_name": lead_name,
        },
        pluck="parent",
    )
    for contact_name in contact_names:
        links = frappe.get_all(
            "Dynamic Link",
            filters={"parenttype": "Contact", "parent": contact_name},
            fields=["link_doctype", "link_name"],
        )
        if any(link.link_doctype != "Lead" or link.link_name != lead_name for link in links):
            continue
        frappe.delete_doc("Contact", contact_name, ignore_permissions=True, force=True)


@frappe.whitelist(methods=["POST"])
def update_lead(name, data):
    """Update editable fields on a Lead."""
    _check_permission("Lead", "write", name=name)
    if isinstance(data, str):
        data = json.loads(data)
    ALLOWED = {
        "salutation", "first_name", "last_name", "middle_name",
        "email_id", "mobile_no", "phone", "source", "utm_source", "status", "lead_owner",
        "company_name", "job_title", "department", "industry", "territory",
        "country", "state", "city", "pincode", "address_line1", "address_line2",
        "custom_lead_type", "custom_zalo", "custom_work_email", "custom_tax_id",
        "custom_bank_account", "custom_bank_name", "custom_founding_date",
        "custom_business_type", "custom_sector", "custom_district", "custom_ward",
        "custom_full_address", "custom_is_shared",
    }
    doc = frappe.get_doc("Lead", name)
    lead_meta = frappe.get_meta("Lead")
    note_text = data.pop("notes", None)
    for k, v in data.items():
        if k in ALLOWED and (lead_meta.has_field(k) or k in {"name"}):
            if k == "custom_is_shared":
                doc.set(k, cint(v))
            else:
                doc.set(k, v)
    _append_note_value(doc, "notes", note_text)
    doc.save(ignore_permissions=False)
    return {"name": doc.name, "modified": str(doc.modified)}


@frappe.whitelist(methods=["POST"])
def convert_lead(name, create_customer=1, create_opportunity=1):
    """Convert a Lead using ERPNext mappings without losing its timeline."""
    _check_permission("Lead", "write", name=name)
    lead = frappe.get_doc("Lead", name)
    if lead.status == "Converted":
        frappe.throw(_("Lead đã được chuyển đổi"), frappe.ValidationError)

    create_customer = cint(create_customer)
    create_opportunity = cint(create_opportunity)
    if not create_customer and not create_opportunity:
        frappe.throw(_("Chọn ít nhất Customer hoặc Opportunity"), frappe.ValidationError)

    result = {"lead": lead.name, "customer": None, "opportunity": None}

    if create_customer:
        _check_permission("Customer", "create")
        customer_name = (lead.company_name or lead.lead_name or "").strip()
        existing_customer = frappe.db.get_value(
            "Customer", {"customer_name": customer_name}, "name"
        )
        if existing_customer:
            _check_permission("Customer", name=existing_customer)
            result["customer"] = existing_customer
        else:
            from erpnext.crm.doctype.lead.lead import make_customer

            customer = make_customer(lead.name)
            customer.insert(ignore_permissions=False)
            result["customer"] = customer.name

    if create_opportunity:
        _check_permission("Opportunity", "create")
        existing_opportunity = frappe.db.get_value(
            "Opportunity",
            {
                "opportunity_from": "Lead",
                "party_name": lead.name,
                "status": ["not in", ["Lost", "Closed"]],
            },
            "name",
        )
        if existing_opportunity:
            _check_permission("Opportunity", name=existing_opportunity)
            result["opportunity"] = existing_opportunity
        else:
            from erpnext.crm.doctype.lead.lead import make_opportunity

            opportunity = make_opportunity(lead.name)
            opportunity.insert(ignore_permissions=False)
            result["opportunity"] = opportunity.name

    # Customer creation copies the Lead email. Running Lead.validate() again at
    # this point makes cross-app duplicate rules reject the newly created
    # Customer. Permission was checked above and this update remains part of
    # the request transaction, so later failures still roll it back.
    frappe.db.set_value("Lead", lead.name, "status", "Converted")
    return result


def _get_customer_credit_limit(customer):
    """Resolve the customer's credit limit for its default company (falls back to
    Customer Group and Company defaults via ERPNext's own get_credit_limit)."""
    from erpnext.selling.doctype.customer.customer import get_credit_limit

    company = frappe.defaults.get_user_default("Company") or frappe.defaults.get_global_default("company")
    if not company:
        return 0
    return flt(get_credit_limit(customer.name, company))


@frappe.whitelist(methods=["GET"])
def get_customer_workspace(name):
    """Return the Customer detail panels used by the CRM list workspace."""
    _check_permission("Customer", name=name)
    customer = frappe.get_doc("Customer", name)

    orders = []
    if frappe.has_permission("Sales Order", "read"):
        orders = frappe.get_list(
            "Sales Order",
            filters={"customer": name, "docstatus": ["<", 2]},
            fields=[
                "name",
                "transaction_date",
                "status",
                "grand_total",
                "currency",
                "modified",
            ],
            order_by="transaction_date desc, modified desc",
            page_length=30,
        )
        if orders:
            order_accounts = {}
            for row in frappe.get_all(
                "Sales Order Item",
                filters={"parent": ["in", [order.name for order in orders]]},
                fields=["parent", "custom_dcnet_account_id", "custom_a_end", "custom_z_end"],
            ):
                if not row.custom_dcnet_account_id:
                    continue
                seen = order_accounts.setdefault(row.parent, {})
                if row.custom_dcnet_account_id not in seen:
                    seen[row.custom_dcnet_account_id] = {
                        "code": row.custom_dcnet_account_id,
                        "a_end": row.custom_a_end,
                        "z_end": row.custom_z_end,
                    }
            for order in orders:
                order["accounts"] = list(order_accounts.get(order.name, {}).values())

    contacts = []
    if frappe.has_permission("Contact", "read"):
        contact_names = frappe.get_all(
            "Dynamic Link",
            filters={
                "parenttype": "Contact",
                "link_doctype": "Customer",
                "link_name": name,
            },
            pluck="parent",
        )
        if contact_names:
            contacts = frappe.get_list(
                "Contact",
                filters={"name": ["in", list(set(contact_names))]},
                fields=[
                    "name",
                    "first_name",
                    "middle_name",
                    "last_name",
                    "full_name",
                    "salutation",
                    "gender",
                    "status",
                    "department",
                    "designation",
                    "email_id",
                    "mobile_no",
                    "phone",
                    "company_name",
                    "is_primary_contact",
                    "modified",
                ],
                order_by="modified desc",
                page_length=max(len(contact_names), 1),
            )

    addresses = []
    if frappe.has_permission("Address", "read"):
        address_names = frappe.get_all(
            "Dynamic Link",
            filters={
                "parenttype": "Address",
                "link_doctype": "Customer",
                "link_name": name,
            },
            pluck="parent",
        )
        if address_names:
            addresses = frappe.get_list(
                "Address",
                filters={"name": ["in", list(set(address_names))]},
                fields=[
                    "name",
                    "address_title",
                    "address_type",
                    "address_line1",
                    "address_line2",
                    "city",
                    "county",
                    "state",
                    "country",
                    "pincode",
                    "email_id",
                    "phone",
                    "is_primary_address",
                    "is_shipping_address",
                ],
                order_by="is_primary_address desc, is_shipping_address desc, modified desc",
                page_length=20,
            )

    related = {
        "quotations": _get_customer_transactions(
            "Quotation",
            name,
            ["name", "transaction_date", "status", "grand_total", "currency", "modified"],
            {"party_name": name, "quotation_to": "Customer", "docstatus": ["<", 2]},
            "transaction_date desc, modified desc",
        ),
        "invoices": _get_customer_transactions(
            "Sales Invoice",
            name,
            ["name", "posting_date", "status", "grand_total", "outstanding_amount", "currency"],
            {"customer": name, "is_return": 0, "docstatus": ["<", 2]},
            "posting_date desc, modified desc",
        ),
        "sales_returns": _get_customer_transactions(
            "Sales Invoice",
            name,
            ["name", "posting_date", "status", "return_against", "grand_total", "currency"],
            {"customer": name, "is_return": 1, "docstatus": ["<", 2]},
            "posting_date desc, modified desc",
        ),
        "opportunities": _get_customer_transactions(
            "Opportunity",
            name,
            ["name", "title", "status", "sales_stage", "opportunity_amount", "currency", "modified"],
            {"opportunity_from": "Customer", "party_name": name},
            "modified desc",
        ),
        "files": _get_customer_transactions(
            "File",
            name,
            ["name", "file_name", "file_url", "file_size", "owner", "creation"],
            {"attached_to_doctype": "Customer", "attached_to_name": name, "is_folder": 0},
            "creation desc",
        ),
    }
    purchased_items = _get_customer_purchased_items(name)
    activities = _get_customer_activities(name)
    activity_users = [
        {
            "name": frappe.session.user,
            "full_name": frappe.utils.get_fullname(frappe.session.user),
        }
    ]
    if frappe.has_permission("User", "read"):
        activity_users = frappe.get_list(
            "User",
            filters={"enabled": 1, "user_type": "System User"},
            fields=["name", "full_name"],
            order_by="full_name asc",
            page_length=200,
        )

    detail_fields = [
        "name",
        "customer_name",
        "ten_viet_tat",
        "customer_type",
        "customer_group",
        "territory",
        "tax_id",
        "mobile_no",
        "email_id",
        "misa_mobile",
        "misa_email",
        "nguon_goc",
        "customer_primary_contact",
        "customer_primary_address",
        "primary_address",
        "image",
        "gender",
        "industry",
        "loai_hinh",
        "nganh_nghe",
        "market_segment",
        "default_price_list",
        "account_manager",
        "tai_khoan_ngan_hang",
        "mo_tai_ngan_hang",
        "ngay_thanh_lap",
        "la_kh_tu",
        "quy_mo_doanh_thu",
        "quy_mo_nhan_su",
        "loai_han_muc_no",
        "so_ngay_duoc_no",
        "website",
        "customer_details",
        "dung_chung",
        "la_kh_ca_nhan",
        "la_doi_tac_ctv",
        "doi_tac_gioi_thieu",
        "loyalty_program",
        "loyalty_program_tier",
        "_user_tags",
        "modified",
        "modified_by",
        "creation",
        "owner",
    ]
    customer_meta = frappe.get_meta("Customer")
    standard_detail_fields = {"name", "owner", "creation", "modified", "modified_by", "_user_tags"}

    return {
        "document": {
            fieldname: customer.get(fieldname)
            for fieldname in detail_fields
            if fieldname in standard_detail_fields or customer_meta.has_field(fieldname)
        },
        "timeline": _get_timeline("Customer", name),
        "orders": orders,
        "contacts": contacts,
        "addresses": addresses,
        "activities": activities,
        "activity_users": activity_users,
        "purchased_items": purchased_items,
        "subsidiaries": [],
        **related,
        "summary": {
            "order_count": len(orders),
            "order_value": sum(flt(order.grand_total) for order in orders),
            "invoice_count": len(related["invoices"]),
            "outstanding": sum(flt(invoice.outstanding_amount) for invoice in related["invoices"]),
            "credit_limit": _get_customer_credit_limit(customer),
        },
        "can_write": frappe.has_permission("Customer", "write", name),
        "can_create_contact": frappe.has_permission("Contact", "create"),
        "can_write_contact": frappe.has_permission("Contact", "write"),
        "can_create_activity": (
            frappe.has_permission("ToDo", "create")
            or frappe.has_permission("Event", "create")
        ),
        "can_create_order": frappe.has_permission("Sales Order", "create"),
    }


@frappe.whitelist(methods=["POST"])
def add_customer_tag(name, tag):
    """Add a Frappe tag to a Customer from the CRM workspace."""
    _check_permission("Customer", "write", name)
    tag = (tag or "").strip()
    if not tag:
        frappe.throw(_("Tag is required"))

    doc = frappe.get_doc("Customer", name)
    doc.add_tag(tag)
    return {"tags": doc.get("_user_tags")}


@frappe.whitelist(methods=["POST"])
def add_customer_attachment_link(name, url, title=None):
    """Attach an external link as a File to a Customer."""
    _check_permission("Customer", "write", name)
    url = _normalize_external_url(url)

    file_doc = frappe.get_doc(
        {
            "doctype": "File",
            "file_url": url,
            "file_name": (title or "").strip() or url,
            "attached_to_doctype": "Customer",
            "attached_to_name": name,
        }
    )
    file_doc.insert(ignore_permissions=False)
    return {"name": file_doc.name}


@frappe.whitelist(methods=["POST"])
def delete_customer_attachment(file_name):
    """Delete a File attached to a Customer."""
    file_doc = frappe.get_doc("File", file_name)
    if file_doc.attached_to_doctype != "Customer":
        frappe.throw(_("Tệp không thuộc khách hàng"))
    _check_permission("Customer", "write", file_doc.attached_to_name)
    file_doc.delete()


@frappe.whitelist(methods=["POST"])
def save_customer_contact(customer, contact=None):
    """Create or update a Contact linked to a Customer."""
    _check_permission("Customer", name=customer)
    values = _parse_json(contact, {})
    contact_name = values.get("name")

    if contact_name:
        _check_permission("Contact", "write", contact_name)
        contact_doc = frappe.get_doc("Contact", contact_name)
        if not any(
            link.link_doctype == "Customer" and link.link_name == customer
            for link in contact_doc.links
        ):
            frappe.throw(_("Contact is not linked to this Customer"), frappe.ValidationError)
    else:
        _check_permission("Contact", "create")
        contact_doc = frappe.new_doc("Contact")
        contact_doc.append(
            "links",
            {"link_doctype": "Customer", "link_name": customer},
        )

    allowed_fields = {
        "first_name",
        "middle_name",
        "last_name",
        "salutation",
        "gender",
        "status",
        "department",
        "designation",
        "company_name",
        "is_primary_contact",
    }
    contact_meta = frappe.get_meta("Contact")
    for fieldname, value in values.items():
        if fieldname in allowed_fields and contact_meta.has_field(fieldname):
            contact_doc.set(fieldname, value or None)

    if not contact_doc.first_name:
        frappe.throw(_("Contact first name is required"), frappe.ValidationError)

    _set_primary_contact_email(contact_doc, values)
    _set_primary_contact_phone(contact_doc, values, "mobile_no", "is_primary_mobile_no")
    _set_primary_contact_phone(contact_doc, values, "phone", "is_primary_phone")
    contact_doc.save()

    customer_doc = frappe.get_doc("Customer", customer)
    should_be_primary = bool(cint(values.get("is_primary_contact")))
    if should_be_primary and customer_doc.customer_primary_contact != contact_doc.name:
        _check_permission("Customer", "write", customer)
        customer_doc.customer_primary_contact = contact_doc.name
        customer_doc.save()
    elif (
        "is_primary_contact" in values
        and not should_be_primary
        and customer_doc.customer_primary_contact == contact_doc.name
    ):
        _check_permission("Customer", "write", customer)
        customer_doc.customer_primary_contact = None
        customer_doc.save()

    return {"name": contact_doc.name}


@frappe.whitelist(methods=["GET"])
def search_customer_contacts(customer, search=None, page_length=20):
    """Find Contacts that can be linked to a Customer."""
    _check_permission("Customer", name=customer)
    _check_permission("Contact")
    linked_names = frappe.get_all(
        "Dynamic Link",
        filters={
            "parenttype": "Contact",
            "link_doctype": "Customer",
            "link_name": customer,
        },
        pluck="parent",
    )
    filters = {"name": ["not in", linked_names]} if linked_names else {}
    or_filters = {}
    if search and search.strip():
        value = ["like", f"%{search.strip()}%"]
        or_filters = {
            "name": value,
            "full_name": value,
            "email_id": value,
            "mobile_no": value,
            "phone": value,
        }
    return frappe.get_list(
        "Contact",
        filters=filters,
        or_filters=or_filters,
        fields=["name", "full_name", "email_id", "mobile_no", "phone", "company_name"],
        order_by="modified desc",
        page_length=min(max(cint(page_length), 1), 100),
    )


@frappe.whitelist(methods=["POST"])
def link_customer_contact(customer, contact):
    """Link an existing Contact to a Customer."""
    _check_permission("Customer", name=customer)
    _check_permission("Contact", "write", contact)
    contact_doc = frappe.get_doc("Contact", contact)
    if not any(
        link.link_doctype == "Customer" and link.link_name == customer
        for link in contact_doc.links
    ):
        contact_doc.append(
            "links",
            {"link_doctype": "Customer", "link_name": customer},
        )
        contact_doc.save()
    return {"name": contact_doc.name}


@frappe.whitelist(methods=["POST"])
def save_customer_activity(customer, activity=None):
    """Create or update a task, meeting or call linked to a Customer."""
    _check_permission("Customer", name=customer)
    values = _parse_json(activity, {})
    activity_type = values.get("activity_type") or "task"
    if activity_type not in {"task", "meeting", "call"}:
        frappe.throw(_("Unsupported activity type"), frappe.ValidationError)

    doctype = "ToDo" if activity_type == "task" else "Event"
    document_name = values.get("name")
    if document_name:
        _check_permission(doctype, "write", document_name)
        doc = frappe.get_doc(doctype, document_name)
    else:
        _check_permission(doctype, "create")
        doc = frappe.new_doc(doctype)

    subject = (values.get("subject") or "").strip()
    if not subject:
        frappe.throw(_("Activity subject is required"), frappe.ValidationError)

    if doctype == "ToDo":
        doc.description = subject
        doc.reference_type = "Customer"
        doc.reference_name = customer
        doc.date = values.get("due_date") or None
        doc.status = values.get("status") or "Open"
        doc.priority = values.get("priority") or "Medium"
        doc.allocated_to = values.get("allocated_to") or frappe.session.user
    else:
        doc.subject = subject
        doc.description = values.get("description") or subject
        doc.event_category = "Call" if activity_type == "call" else "Meeting"
        doc.event_type = "Private"
        doc.starts_on = values.get("starts_on") or frappe.utils.now_datetime()
        doc.ends_on = values.get("ends_on") or None
        doc.status = values.get("status") or "Open"
        doc.reference_doctype = "Customer"
        doc.reference_docname = customer
        if not any(
            participant.reference_doctype == "Customer"
            and participant.reference_docname == customer
            for participant in doc.event_participants
        ):
            doc.append(
                "event_participants",
                {"reference_doctype": "Customer", "reference_docname": customer},
            )
        allocated_to = values.get("allocated_to") or frappe.session.user
        doc.set(
            "event_participants",
            [
                participant
                for participant in doc.event_participants
                if participant.reference_doctype != "User"
            ],
        )
        doc.append(
            "event_participants",
            {"reference_doctype": "User", "reference_docname": allocated_to},
        )

    doc.save()
    return {"doctype": doctype, "name": doc.name}


@frappe.whitelist(methods=["POST"])
def update_customer_details(name, customer=None, contact=None, address=None):
    """Update Customer, its primary Contact and primary Address with validation."""
    _check_permission("Customer", "write", name)
    customer_values = _parse_json(customer, {})
    contact_values = _parse_json(contact, {})
    address_values = _parse_json(address, {})

    allowed_customer_fields = {
        "customer_name",
        "ten_viet_tat",
        "customer_type",
        "customer_group",
        "territory",
        "tax_id",
        "misa_mobile",
        "misa_email",
        "nguon_goc",
        "gender",
        "industry",
        "loai_hinh",
        "nganh_nghe",
        "market_segment",
        "default_price_list",
        "account_manager",
        "tai_khoan_ngan_hang",
        "mo_tai_ngan_hang",
        "ngay_thanh_lap",
        "la_kh_tu",
        "quy_mo_doanh_thu",
        "quy_mo_nhan_su",
        "loai_han_muc_no",
        "so_ngay_duoc_no",
        "website",
        "customer_details",
        "dung_chung",
        "la_kh_ca_nhan",
        "la_doi_tac_ctv",
        "doi_tac_gioi_thieu",
    }
    customer_doc = frappe.get_doc("Customer", name)
    customer_meta = frappe.get_meta("Customer")
    for fieldname, value in customer_values.items():
        if fieldname in allowed_customer_fields and customer_meta.has_field(fieldname):
            customer_doc.set(fieldname, value or None)
    customer_doc.save(ignore_version=False)

    contact_doc = _update_customer_contact(customer_doc, contact_values)
    address_doc = _update_customer_address(customer_doc, address_values)

    return {
        "name": customer_doc.name,
        "contact": contact_doc.name if contact_doc else None,
        "address": address_doc.name if address_doc else None,
    }


def _update_customer_contact(customer, values):
    allowed_fields = {"first_name", "last_name", "designation"}
    clean_values = {
        fieldname: value or None
        for fieldname, value in values.items()
        if fieldname in allowed_fields
    }
    if not clean_values and not any(
        fieldname in values for fieldname in {"mobile_no", "phone", "email_id"}
    ):
        return None

    contact_name = values.get("name") or customer.customer_primary_contact
    if contact_name and frappe.db.exists("Contact", contact_name):
        _check_permission("Contact", "write", contact_name)
        contact = frappe.get_doc("Contact", contact_name)
    else:
        _check_permission("Contact", "create")
        contact = frappe.new_doc("Contact")
        contact.first_name = clean_values.get("first_name") or customer.customer_name
        contact.append(
            "links",
            {"link_doctype": "Customer", "link_name": customer.name},
        )

    contact.update(clean_values)
    _set_primary_contact_email(contact, values)
    _set_primary_contact_phone(contact, values, "mobile_no", "is_primary_mobile_no")
    _set_primary_contact_phone(contact, values, "phone", "is_primary_phone")
    contact.save(ignore_version=False)
    if customer.customer_primary_contact != contact.name:
        customer.customer_primary_contact = contact.name
        frappe.db.set_value("Customer", customer.name, "customer_primary_contact", contact.name, update_modified=False)
    return contact


def _set_primary_contact_email(contact, values):
    if "email_id" not in values:
        return

    email = (values.get("email_id") or "").strip()
    primary = next(
        (row for row in contact.email_ids if row.is_primary),
        contact.email_ids[0] if contact.email_ids else None,
    )
    if email:
        if not primary:
            primary = contact.append("email_ids", {})
        primary.email_id = email
        primary.is_primary = 1
        for row in contact.email_ids:
            if row is not primary:
                row.is_primary = 0
    elif primary:
        contact.remove(primary)


def _set_primary_contact_phone(contact, values, fieldname, primary_flag):
    if fieldname not in values:
        return

    phone = (values.get(fieldname) or "").strip()
    primary = next(
        (row for row in contact.phone_nos if row.get(primary_flag)),
        None,
    )
    other_flag = (
        "is_primary_phone"
        if primary_flag == "is_primary_mobile_no"
        else "is_primary_mobile_no"
    )
    if phone:
        if primary and primary.get(other_flag) and primary.phone != phone:
            primary.set(primary_flag, 0)
            primary = None
        if not primary:
            primary = contact.append("phone_nos", {})
        primary.phone = phone
        primary.set(primary_flag, 1)
        for row in contact.phone_nos:
            if row is not primary:
                row.set(primary_flag, 0)
    elif primary:
        if primary.get(other_flag):
            primary.set(primary_flag, 0)
        else:
            contact.remove(primary)


def _update_customer_address(customer, values):
    allowed_fields = {
        "address_title",
        "address_type",
        "address_line1",
        "address_line2",
        "city",
        "county",
        "state",
        "country",
        "pincode",
        "email_id",
        "phone",
        "is_primary_address",
        "is_shipping_address",
    }
    clean_values = {
        fieldname: value
        for fieldname, value in values.items()
        if fieldname in allowed_fields
    }
    if not clean_values or not any(
        value not in (None, "", 0, False)
        for fieldname, value in clean_values.items()
        if fieldname not in {"is_primary_address", "is_shipping_address"}
    ):
        return None

    address_name = values.get("name") or customer.customer_primary_address
    if address_name and frappe.db.exists("Address", address_name):
        _check_permission("Address", "write", address_name)
        address_doc = frappe.get_doc("Address", address_name)
    else:
        _check_permission("Address", "create")
        address_doc = frappe.new_doc("Address")
        address_doc.address_title = clean_values.get("address_title") or customer.customer_name
        address_doc.address_type = clean_values.get("address_type") or "Billing"
        address_doc.append(
            "links",
            {"link_doctype": "Customer", "link_name": customer.name},
        )

    address_doc.update(clean_values)
    # city and address_line1 are mandatory in ERPNext Address; default when omitted
    if not address_doc.city:
        address_doc.city = address_doc.state or address_doc.county or "-"
    if not address_doc.address_line1:
        # Build a meaningful fallback from ward + province
        parts = [p for p in [address_doc.county, address_doc.state] if p and p != "-"]
        address_doc.address_line1 = ", ".join(parts) if parts else "-"
    address_doc.save(ignore_version=False)
    if address_doc.is_primary_address and customer.customer_primary_address != address_doc.name:
        customer.customer_primary_address = address_doc.name
        frappe.db.set_value("Customer", customer.name, "customer_primary_address", address_doc.name, update_modified=False)
    return address_doc


def _parse_customer_names(customers):
    names = _parse_json(customers, [])
    if isinstance(names, str):
        names = [name.strip() for name in names.split(",") if name.strip()]
    if not isinstance(names, list):
        frappe.throw(_("Invalid customer list"), frappe.ValidationError)
    clean_names = []
    for name in names:
        if not isinstance(name, str) or not name.strip():
            continue
        if not frappe.db.exists("Customer", name.strip()):
            frappe.throw(_("Customer {0} does not exist").format(name), frappe.DoesNotExistError)
        clean_names.append(name.strip())
    return list(dict.fromkeys(clean_names))


def _normalise_customer_duplicate_value(value, keep_only_alnum=False):
    text = " ".join(str(value or "").split()).casefold()
    if keep_only_alnum:
        return "".join(char for char in text if char.isalnum())
    return text


def _customer_duplicate_key(row):
    tax_id = _normalise_customer_duplicate_value(row.get("tax_id"), keep_only_alnum=True)
    if tax_id:
        return f"tax:{tax_id}"
    customer_name = _normalise_customer_duplicate_value(row.get("customer_name") or row.get("name"))
    return f"name:{customer_name}" if customer_name else None


@frappe.whitelist(methods=["POST"])
def bulk_update_customer_address(customers, address):
    """Update or create the primary address for selected Customers."""
    names = _parse_customer_names(customers)
    if not names:
        frappe.throw(_("Please select at least one Customer"), frappe.ValidationError)

    address_values = _parse_json(address, {})
    if not isinstance(address_values, dict):
        frappe.throw(_("Invalid address data"), frappe.ValidationError)

    updated = 0
    errors = []
    for name in names:
        try:
            _check_permission("Customer", "write", name)
            customer = frappe.get_doc("Customer", name)
            values = dict(address_values)
            values.setdefault("country", "Vietnam")
            values.setdefault("address_type", "Billing")
            if values.get("address_type") != "Shipping":
                values["is_primary_address"] = 1
            address_doc = _update_customer_address(customer, values)
            if address_doc:
                updated += 1
        except Exception as exc:
            errors.append({"name": name, "error": str(exc)})

    return {"updated": updated, "errors": errors}


@frappe.whitelist(methods=["POST"])
def bulk_manage_customer_tags(customers, tag, action="add"):
    """Add or remove a tag for selected Customers."""
    names = _parse_customer_names(customers)
    if not names:
        frappe.throw(_("Please select at least one Customer"), frappe.ValidationError)

    tag = (tag or "").strip()
    if not tag:
        frappe.throw(_("Tag is required"), frappe.ValidationError)

    action = (action or "add").strip().lower()
    if action not in {"add", "remove"}:
        frappe.throw(_("Invalid tag action"), frappe.ValidationError)

    tagged = 0
    errors = []
    for name in names:
        try:
            _check_permission("Customer", "write", name)
            doc = frappe.get_doc("Customer", name)
            if action == "remove":
                doc.remove_tag(tag)
            else:
                doc.add_tag(tag)
            tagged += 1
        except Exception as exc:
            errors.append({"name": name, "error": str(exc)})

    return {"tagged": tagged, "errors": errors}


@frappe.whitelist(methods=["POST"])
def auto_merge_duplicate_customers(customers=None):
    """Merge duplicate Customers by Tax ID first, then by normalized customer name."""
    names = _parse_customer_names(customers or "[]")
    filters = {"name": ["in", names]} if names else {}
    rows = frappe.get_list(
        "Customer",
        filters=filters,
        fields=["name", "customer_name", "tax_id", "creation"],
        order_by="creation asc, name asc",
        limit_page_length=0,
    )
    groups = {}
    for row in rows:
        key = _customer_duplicate_key(row)
        if key:
            groups.setdefault(key, []).append(row)

    duplicate_groups = [group for group in groups.values() if len(group) > 1]
    merged = 0
    errors = []
    for group_index, group in enumerate(duplicate_groups, start=1):
        group = sorted(group, key=lambda row: (row.get("creation"), row.get("name")))
        target = group[0]
        try:
            _check_permission("Customer", "write", target.name)
        except Exception as exc:
            errors.append({"name": target.name, "error": str(exc)})
            continue

        for source in group[1:]:
            save_point = f"crm_customer_merge_{group_index}_{merged + 1}"
            frappe.db.savepoint(save_point)
            try:
                _check_permission("Customer", "write", source.name)
                frappe.rename_doc(
                    "Customer",
                    source.name,
                    target.name,
                    force=True,
                    merge=True,
                    show_alert=False,
                    validate=False,
                )
                merged += 1
            except Exception as exc:
                frappe.db.rollback(save_point=save_point)
                errors.append({"source": source.name, "target": target.name, "error": str(exc)})

    return {"groups": len(duplicate_groups), "merged": merged, "errors": errors}


def _get_customer_transactions(doctype, customer, fields, filters, order_by):
    """Return related records only when the user can read their DocType."""
    if not frappe.has_permission(doctype, "read"):
        return []
    meta = frappe.get_meta(doctype)
    available_fields = [
        fieldname
        for fieldname in fields
        if fieldname == "name" or meta.has_field(fieldname)
    ]
    return frappe.get_list(
        doctype,
        filters=filters,
        fields=available_fields,
        order_by=order_by,
        page_length=50,
    )


def _customer_todos(customer, fields, order_by="date desc, modified desc"):
    """All ToDos relevant to a customer: those referencing the Customer directly
    plus those referencing the customer's sales documents (Sales Order, Quotation,
    Sales Invoice). De-duplicated. Used by every "Hoạt động" tab in the CRM."""
    if not (customer and frappe.has_permission("ToDo", "read")):
        return []
    if "name" not in fields:
        fields = ["name", *fields]
    ref_map = {
        "Customer": [customer],
        "Sales Order": frappe.get_all("Sales Order", filters={"customer": customer}, pluck="name"),
        "Quotation": frappe.get_all("Quotation", filters={"party_name": customer, "quotation_to": "Customer"}, pluck="name"),
        "Sales Invoice": frappe.get_all("Sales Invoice", filters={"customer": customer}, pluck="name"),
    }
    out, seen = [], set()
    for ref_type, names in ref_map.items():
        if not names:
            continue
        for todo in frappe.get_list(
            "ToDo", filters={"reference_type": ref_type, "reference_name": ["in", names]},
            fields=fields, order_by=order_by, page_length=200,
        ):
            if todo.name in seen:
                continue
            seen.add(todo.name)
            out.append(todo)
    return out


def _get_customer_activities(customer):
    activities = []
    todo_fields = [
        "name", "description", "date", "status", "priority",
        "allocated_to", "modified", "reference_type", "reference_name",
    ]
    for todo in _customer_todos(customer, todo_fields):
        activities.append({
            **todo,
            "subject": todo.description,
            "activity_type": "task",
            "due_date": todo.date,
            "ends_on": None,
            "performed_by": todo.allocated_to,
            "performed_by_name": frappe.utils.get_fullname(todo.allocated_to)
            if todo.allocated_to else "",
        })

    if frappe.has_permission("Event", "read"):
        event_names = frappe.get_all(
            "Event Participants",
            filters={
                "parenttype": "Event",
                "reference_doctype": "Customer",
                "reference_docname": customer,
            },
            pluck="parent",
        )
        event_filters = {"name": ["in", list(set(event_names))]} if event_names else {
            "reference_doctype": "Customer",
            "reference_docname": customer,
        }
        events = frappe.get_list(
            "Event",
            filters=event_filters,
            fields=[
                "name",
                "subject",
                "description",
                "event_category",
                "starts_on",
                "ends_on",
                "status",
                "owner",
                "modified",
            ],
            order_by="starts_on desc, modified desc",
            page_length=200,
        )
        assigned_users = {}
        if events:
            participants = frappe.get_all(
                "Event Participants",
                filters={
                    "parenttype": "Event",
                    "parent": ["in", [event.name for event in events]],
                    "reference_doctype": "User",
                },
                fields=["parent", "reference_docname"],
            )
            assigned_users = {
                participant.parent: participant.reference_docname
                for participant in participants
            }
        for event in events:
            performed_by = assigned_users.get(event.name) or event.owner
            activities.append(
                {
                    **event,
                    "activity_type": "call"
                    if event.event_category == "Call"
                    else "meeting",
                    "due_date": event.starts_on,
                    "performed_by": performed_by,
                    "performed_by_name": frappe.utils.get_fullname(performed_by),
                }
            )

    return sorted(
        activities,
        key=lambda row: str(row.get("due_date") or row.get("modified") or ""),
        reverse=True,
    )


def _get_customer_purchased_items(customer):
    if not frappe.has_permission("Sales Invoice", "read"):
        return []

    invoice_names = frappe.get_list(
        "Sales Invoice",
        filters={
            "customer": customer,
            "docstatus": 1,
            "is_return": 0,
        },
        pluck="name",
        page_length=500,
    )
    if not invoice_names:
        return []

    rows = frappe.get_all(
        "Sales Invoice Item",
        filters={"parent": ["in", invoice_names]},
        fields=[
            "item_code",
            "item_name",
            "item_group",
            {"SUM": "qty", "as": "qty"},
            {"SUM": "amount", "as": "amount"},
        ],
        group_by="item_code, item_name, item_group",
        order_by="amount desc",
        limit_page_length=500,
    )
    return rows


def _get_timeline(doctype, name):
    communications = frappe.get_list(
        "Communication",
        filters={"reference_doctype": doctype, "reference_name": name},
        fields=["name", "communication_type", "subject", "content", "sender", "creation"],
        order_by="creation desc",
        page_length=20,
    )
    comments = frappe.get_list(
        "Comment",
        filters={
            "reference_doctype": doctype,
            "reference_name": name,
            "comment_type": ["in", ["Comment", "Info"]],
        },
        fields=["name", "comment_type", "content", "comment_email", "creation"],
        order_by="creation desc",
        page_length=20,
    )
    todos = frappe.get_list(
        "ToDo",
        filters={"reference_type": doctype, "reference_name": name},
        fields=["name", "description", "status", "allocated_to", "date", "creation"],
        order_by="creation desc",
        page_length=20,
    )

    items = []
    items.extend({**row, "activity_type": "communication"} for row in communications)
    items.extend({**row, "activity_type": "comment"} for row in comments)
    items.extend({**row, "activity_type": "task"} for row in todos)
    return sorted(
        items,
        key=lambda row: str(row.get("creation") or ""),
        reverse=True,
    )[:30]


@frappe.whitelist(methods=["POST"])
def add_note(resource, name, content):
    """Add a timeline note to a CRM document."""
    config = _get_resource(resource)
    doctype = config["doctype"]
    _check_permission(doctype, "write", name)
    if not content or not content.strip():
        frappe.throw(_("Note content is required"))

    comment = frappe.get_doc(
        {
            "doctype": "Comment",
            "comment_type": "Comment",
            "reference_doctype": doctype,
            "reference_name": name,
            "content": content.strip(),
        }
    )
    comment.insert()
    return {"name": comment.name}


@frappe.whitelist(methods=["POST"])
def add_customer_conversation(name, content):
    """Add a customer exchange as Communication, separate from internal notes."""
    _check_permission("Customer", "write", name)
    content = (content or "").strip()
    if not content:
        frappe.throw(_("Nội dung trao đổi là bắt buộc"), frappe.ValidationError)
    _check_permission("Communication", "create")

    communication = frappe.get_doc(
        {
            "doctype": "Communication",
            "communication_type": "Communication",
            "communication_medium": "Other",
            "sent_or_received": "Sent",
            "subject": _("Trao đổi khách hàng"),
            "content": content,
            "sender": frappe.session.user,
            "sender_full_name": frappe.utils.get_fullname(frappe.session.user),
            "reference_doctype": "Customer",
            "reference_name": name,
            "status": "Linked",
        }
    )
    communication.insert(ignore_permissions=False)
    return {"name": communication.name}


@frappe.whitelist(methods=["POST"])
def add_contact_attachment_link(name, url, title=None):
    """Attach an external link as a File to a Contact."""
    _check_permission("Contact", "write", name)
    url = _normalize_external_url(url)

    file_doc = frappe.get_doc(
        {
            "doctype": "File",
            "file_url": url,
            "file_name": (title or "").strip() or url,
            "attached_to_doctype": "Contact",
            "attached_to_name": name,
        }
    )
    file_doc.insert(ignore_permissions=False)
    return {"name": file_doc.name}


@frappe.whitelist(methods=["POST"])
def delete_contact_attachment(file_name):
    """Delete a File attached to a Contact."""
    file_doc = frappe.get_doc("File", file_name)
    if file_doc.attached_to_doctype != "Contact":
        frappe.throw(_("Tệp không thuộc liên hệ"))
    _check_permission("Contact", "write", file_doc.attached_to_name)
    file_doc.delete()
    return {"ok": True}


@frappe.whitelist(methods=["POST"])
def link_opportunity_to_contact(contact, opportunity):
    """Map an Opportunity to a Contact (set its contact_person)."""
    _check_permission("Contact", "read", contact)
    _check_permission("Opportunity", "write", opportunity)
    frappe.db.set_value("Opportunity", opportunity, "contact_person", contact)
    return {"ok": True}


@frappe.whitelist(methods=["POST"])
def unlink_opportunity_from_contact(opportunity):
    """Remove the Contact mapping from an Opportunity."""
    _check_permission("Opportunity", "write", opportunity)
    frappe.db.set_value("Opportunity", opportunity, "contact_person", None)
    return {"ok": True}


@frappe.whitelist(methods=["GET"])
def get_linkable_opportunities(contact=None, search=None, page=1, page_length=20):
    """Paginated list of Opportunities for the contact-mapping picker."""
    _check_permission("Opportunity", "read")
    page = int(page or 1)
    page_length = int(page_length or 20)
    start = (page - 1) * page_length

    or_filters = None
    if search and search.strip():
        like = "%{0}%".format(search.strip())
        or_filters = [
            ["title", "like", like],
            ["name", "like", like],
            ["customer_name", "like", like],
            ["contact_display", "like", like],
        ]

    rows = frappe.get_list(
        "Opportunity",
        or_filters=or_filters,
        fields=["name", "title", "contact_display", "opportunity_amount", "currency",
                "sales_stage", "expected_closing", "opportunity_type", "opportunity_owner", "creation"],
        start=start,
        page_length=page_length,
        order_by="creation desc",
    )
    total = len(frappe.get_all("Opportunity", or_filters=or_filters, pluck="name", limit_page_length=0))
    return {"rows": rows, "total": total}


@frappe.whitelist(methods=["POST"])
def link_opportunities_to_contact(contact, opportunities):
    """Map several Opportunities to a Contact at once."""
    _check_permission("Contact", "read", contact)
    if isinstance(opportunities, str):
        opportunities = json.loads(opportunities)
    for opp in opportunities or []:
        _check_permission("Opportunity", "write", opp)
        frappe.db.set_value("Opportunity", opp, "contact_person", contact)
    return {"count": len(opportunities or [])}


@frappe.whitelist(methods=["GET"])
def get_dashboard(from_date=None, to_date=None):
    """Return CRM KPI cards and opportunity funnel data."""
    if not can_access_crm():
        frappe.throw(_("You are not permitted to access CRM"), frappe.PermissionError)

    date_filters = {}
    if from_date:
        date_filters["creation"] = [">=", from_date]
    if to_date:
        date_filters["creation"] = [
            "between",
            [from_date or "2000-01-01", to_date],
        ]

    order_filters = {"docstatus": ["<", 2]}
    if from_date or to_date:
        order_filters["transaction_date"] = [
            "between",
            [from_date or "2000-01-01", to_date or frappe.utils.today()],
        ]

    order_data = []
    if frappe.has_permission("Sales Order", "read"):
        order_data = frappe.get_list(
            "Sales Order",
            filters=order_filters,
            fields=[
                {"COUNT": "name", "as": "count"},
                {"SUM": "grand_total", "as": "amount"},
            ],
        )

    funnel = []
    if frappe.has_permission("Opportunity", "read"):
        funnel = frappe.get_list(
            "Opportunity",
            fields=[
                "sales_stage as stage",
                {"COUNT": "name", "as": "count"},
                {"SUM": "opportunity_amount", "as": "amount"},
            ],
            filters=date_filters,
            group_by="sales_stage",
            order_by="count desc",
        )

    return {
        "kpis": {
            "leads": (
                _permission_aware_count("Lead", date_filters)
                if frappe.has_permission("Lead", "read")
                else 0
            ),
            "opportunities": (
                _permission_aware_count("Opportunity", date_filters)
                if frappe.has_permission("Opportunity", "read")
                else 0
            ),
            "customers": (
                _permission_aware_count("Customer", date_filters)
                if frappe.has_permission("Customer", "read")
                else 0
            ),
            "orders": cint(order_data[0].count if order_data else 0),
            "order_value": flt(order_data[0].amount if order_data else 0),
        },
        "funnel": funnel,
    }


# ─── Service Account APIs ────────────────────────────────────────────────────

def _generate_next_account_code():
    """Generate next Acc-0001 … Acc-9999 → Acc-10000 code."""
    import re

    last = frappe.db.sql(
        "SELECT account_code FROM `tabDCNET Service Account` ORDER BY creation DESC LIMIT 1",
        as_dict=True,
    )
    if not last:
        return "Acc-0001"
    m = re.match(r"Acc-(\d+)$", last[0].account_code or "")
    if m:
        n = int(m.group(1)) + 1
        return f"Acc-{n:04d}" if n <= 9999 else f"Acc-{n}"
    count = frappe.db.count("DCNET Service Account")
    return f"Acc-{count + 1:04d}"


def _find_service_account(customer, item_code="", a_end="", z_end=""):
    """Return an existing DCNET Service Account row for the key combo, or None."""
    if not customer:
        return None
    rows = frappe.get_list(
        "DCNET Service Account",
        filters={
            "customer": customer,
            "item_code": item_code or "",
            "a_end": a_end or "",
            "z_end": z_end or "",
        },
        fields=["name", "account_code", "a_end", "z_end", "is_active"],
        limit=1,
    )
    return rows[0] if rows else None


def _get_service_account_fallbacks(customer, items):
    """Map legacy Sales Order Item rows to existing service accounts.

    Older orders can have an empty ``custom_dcnet_account_id`` even though an
    account already exists for the same customer, item and endpoints. This is a
    read-only fallback: it never creates or updates an account while rendering
    an order. If endpoints are absent, an account is returned only when the
    customer/item pair has exactly one active match, avoiding ambiguous links.
    """
    unresolved = [
        item
        for item in (items or [])
        if item.get("item_code") and not item.get("custom_dcnet_account_id")
    ]
    if (
        not customer
        or not unresolved
        or not frappe.has_permission("DCNET Service Account", "read")
    ):
        return {}

    item_codes = sorted({item.get("item_code") for item in unresolved})
    accounts = frappe.get_list(
        "DCNET Service Account",
        filters={
            "customer": customer,
            "item_code": ["in", item_codes],
            "is_active": 1,
        },
        fields=["account_code", "item_code", "a_end", "z_end"],
        order_by="account_code asc",
        limit=1000,
    )

    accounts_by_item = {}
    for account in accounts:
        accounts_by_item.setdefault(account.get("item_code"), []).append(account)

    def endpoint(value):
        return str(value or "").strip().casefold()

    result = {}
    for item in unresolved:
        candidates = accounts_by_item.get(item.get("item_code"), [])
        a_end = endpoint(item.get("custom_a_end"))
        z_end = endpoint(item.get("custom_z_end"))
        exact = [
            account
            for account in candidates
            if endpoint(account.get("a_end")) == a_end
            and endpoint(account.get("z_end")) == z_end
        ]
        if exact:
            result[item.name] = exact[0].get("account_code") or ""
        elif not a_end and not z_end and len(candidates) == 1:
            result[item.name] = candidates[0].get("account_code") or ""

    return result


def _resolve_service_account(customer, item_code="", a_end="", z_end=""):
    """Return existing account_code, or CREATE one and persist it. Use on save."""
    if not customer:
        return ""
    existing = _find_service_account(customer, item_code, a_end, z_end)
    if existing:
        return existing["account_code"]
    _check_permission("DCNET Service Account", "create")
    code = _generate_next_account_code()
    doc = frappe.new_doc("DCNET Service Account")
    doc.account_code = code
    doc.customer = customer
    doc.item_code = item_code or ""
    doc.a_end = a_end or ""
    doc.z_end = z_end or ""
    doc.is_active = 1
    doc.insert(ignore_permissions=False)
    return code


@frappe.whitelist(methods=["GET"])
def preview_service_account(customer, item_code="", a_end="", z_end=""):
    """Preview the service account for a line WITHOUT creating it.

    Returns the existing account_code if the combo already exists, otherwise the
    next code that *would* be generated, flagged is_new. Nothing is persisted —
    the account is only created on save (see _resolve_service_account)."""
    if not customer:
        return {}
    _check_permission("Customer", name=customer)
    _check_permission("DCNET Service Account")
    existing = _find_service_account(customer, item_code, a_end, z_end)
    if existing:
        return {"account_code": existing["account_code"], "is_new": False}
    return {"account_code": _generate_next_account_code(), "is_new": True}


@frappe.whitelist(methods=["POST"])
def get_or_create_service_account(customer, item_code="", a_end="", z_end=""):
    """Return existing or create new DCNET Service Account for the key combo."""
    if not customer:
        frappe.throw(_("customer is required"))
    _check_permission("Customer", name=customer)

    existing = _find_service_account(customer, item_code, a_end, z_end)
    if existing:
        return existing

    code = _resolve_service_account(customer, item_code, a_end, z_end)
    return {
        "name": code,
        "account_code": code,
        "a_end": a_end,
        "z_end": z_end,
        "is_active": 1,
    }


@frappe.whitelist(methods=["GET"])
def get_customer_service_accounts(customer, item_code=None):
    """Suggestions: all accounts for a customer (optionally filtered by item_code)."""
    if not customer:
        return []
    _check_permission("Customer", name=customer)
    _check_permission("DCNET Service Account")
    filters = {"customer": customer, "is_active": 1}
    if item_code:
        filters["item_code"] = item_code
    return frappe.get_list(
        "DCNET Service Account",
        filters=filters,
        fields=["account_code", "item_code", "a_end", "z_end"],
        order_by="account_code asc",
        limit=200,
    )


@frappe.whitelist(methods=["GET"])
def get_service_accounts_list(search=None, page=1, page_length=20):
    """Paginated list for the Accounts management tab."""
    _check_permission("DCNET Service Account")
    page = max(cint(page), 1)
    page_length = min(max(cint(page_length), 10), 100)
    filters = {}
    or_filters = {}
    search_value = str(search or "").strip()
    if search_value:
        value = ["like", f"%{search_value}%"]
        or_filters = {
            field: value
            for field in ("account_code", "customer", "item_code", "item_name", "a_end", "z_end")
        }

    query_args = {"filters": filters}
    if or_filters:
        query_args["or_filters"] = or_filters
    total_rows = frappe.get_list(
        "DCNET Service Account",
        **query_args,
        fields=[{"COUNT": "name", "as": "total"}],
    )
    rows = frappe.get_list(
        "DCNET Service Account",
        **query_args,
        fields=["account_code", "customer", "item_code", "item_name", "a_end", "z_end", "is_active"],
        limit=page_length,
        start=(page - 1) * page_length,
        order_by="account_code asc",
    )
    return {"data": rows, "total": cint(total_rows[0].total if total_rows else 0)}


@frappe.whitelist(methods=["GET"])
def get_service_account_detail(account_code):
    """Detail for one account including linked Sales Orders."""
    _check_permission("DCNET Service Account", name=account_code)
    doc = frappe.get_doc("DCNET Service Account", account_code)
    linked_sos = []
    if frappe.has_permission("Sales Order", "read"):
        linked_sos = frappe.get_list(
            "Sales Order",
            filters=[
                ["Sales Order", "docstatus", "<", 2],
                ["Sales Order Item", "custom_dcnet_account_id", "=", account_code],
            ],
            fields=[
                "name",
                "customer_name",
                "transaction_date",
                "grand_total",
                "status",
                "docstatus",
            ],
            distinct=True,
            order_by="transaction_date desc",
            page_length=100,
        )
    return {
        "account_code": doc.account_code,
        "customer": doc.customer,
        "item_code": doc.item_code,
        "item_name": doc.item_name,
        "a_end": doc.a_end,
        "z_end": doc.z_end,
        "is_active": doc.is_active,
        "can_write": bool(doc.has_permission("write")),
        "sales_orders": linked_sos,
    }


@frappe.whitelist(methods=["POST"])
def update_service_account(account_code, data=None):
    """Update user-editable service account fields with document permissions."""
    if not account_code:
        frappe.throw(_("account_code is required"))
    doc = frappe.get_doc("DCNET Service Account", account_code)
    doc.check_permission("write")
    values = frappe.parse_json(data) if isinstance(data, str) else (data or {})
    allowed_fields = ("customer", "item_code", "a_end", "z_end", "is_active")
    if values.get("customer") and values.get("customer") != doc.customer:
        _check_permission("Customer", name=values.get("customer"))
    if values.get("item_code") and values.get("item_code") != doc.item_code:
        _check_permission("Item", name=values.get("item_code"))
    for field in allowed_fields:
        if field in values:
            doc.set(field, values.get(field))
    doc.save()
    return get_service_account_detail(doc.name)


@frappe.whitelist(methods=["GET"])
def get_contact_create_options():
    """Return reference options for the Thêm Liên hệ form.

    Designation and department are deliberately excluded because they describe
    the customer's organization and must remain free-text Contact fields.
    """
    _check_permission("Contact", "create")

    def opts(doctype, fields, order_by="name asc", page_length=500, filters=None):
        if not frappe.has_permission(doctype, "read"):
            return []
        try:
            return frappe.get_list(
                doctype,
                fields=fields,
                filters=filters or {},
                order_by=order_by,
                page_length=page_length,
            )
        except Exception:
            return []

    return {
        "salutations": opts("Salutation", ["name"]),
        "genders": opts("Gender", ["name"]),
        "customers": opts("Customer", ["name", "customer_name"], order_by="customer_name asc", page_length=1000),
        "territories": opts("Territory", ["name"]),
        "countries": opts("Country", ["name"]),
    }

@frappe.whitelist(methods=["POST"])
def create_contact_standalone(data):
    """Create a standalone Contact from the CRM internal form.
    Optionally links to a Customer via dynamic link.
    """
    _check_permission("Contact", "create")
    if isinstance(data, str):
        data = json.loads(data)

    first_name = (data.get("first_name") or "").strip()
    if not first_name:
        frappe.throw(_("Tên là bắt buộc"), frappe.ValidationError)

    doc = frappe.new_doc("Contact")
    doc.first_name = first_name
    for field in ("middle_name", "last_name", "salutation", "designation",
                  "company_name", "department", "gender"):
        val = data.get(field)
        if val:
            doc.set(field, val)

    _set_primary_contact_email(doc, data)
    _set_primary_contact_phone(doc, data, "mobile_no", "is_primary_mobile_no")
    _set_primary_contact_phone(doc, data, "phone", "is_primary_phone")

    customer = (data.get("customer") or "").strip()
    if customer and frappe.db.exists("Customer", customer):
        _check_permission("Customer", name=customer)
        doc.append("links", {"link_doctype": "Customer", "link_name": customer})

    doc.insert(ignore_permissions=False)

    # Billing address
    billing = data.get("billing_address") or {}
    if isinstance(billing, str):
        billing = json.loads(billing)
    if any(billing.get(f) for f in ("address_line1", "state", "county")):
        addr = frappe.new_doc("Address")
        addr.address_title = doc.first_name + (" " + doc.last_name if doc.last_name else "")
        addr.address_type = "Billing"
        addr.is_primary_address = 1
        addr.address_line1 = billing.get("address_line1") or "-"
        addr.city = billing.get("state") or billing.get("county") or "-"
        addr.state = billing.get("state") or ""
        addr.county = billing.get("county") or ""
        addr.country = billing.get("country") or "Vietnam"
        addr.pincode = billing.get("pincode") or ""
        addr.append("links", {"link_doctype": "Contact", "link_name": doc.name})
        if customer:
            addr.append("links", {"link_doctype": "Customer", "link_name": customer})
        addr.insert(ignore_permissions=False)

    return {"name": doc.name, "full_name": doc.get_fullname() if hasattr(doc, "get_fullname") else doc.first_name}


def _get_contact_linked_records(doctype, contact, customer, fields, base_filters=None, order_by="modified desc", customer_field=None, page_length=50):
    """Return records linked to a Contact, falling back to the linked Customer when available."""
    if not frappe.has_permission(doctype, "read"):
        return []
    meta = frappe.get_meta(doctype)
    available_fields = [
        fieldname
        for fieldname in fields
        if fieldname == "name" or meta.has_field(fieldname)
    ]
    if "name" not in available_fields:
        available_fields.insert(0, "name")

    or_filters = []
    if contact and meta.has_field("contact_person"):
        or_filters.append(["contact_person", "=", contact])
    if customer and customer_field and meta.has_field(customer_field):
        or_filters.append([customer_field, "=", customer])
    if not or_filters:
        return []

    return frappe.get_list(
        doctype,
        filters=base_filters or {},
        or_filters=or_filters,
        fields=available_fields,
        order_by=order_by,
        page_length=page_length,
    )


def _get_contact_sales_invoice_names(contact, customer):
    rows = _get_contact_linked_records(
        "Sales Invoice",
        contact,
        customer,
        ["name"],
        {"docstatus": 1, "is_return": 0},
        "posting_date desc, modified desc",
        customer_field="customer",
        page_length=500,
    )
    return [row.name for row in rows]


def _get_contact_purchased_items(contact, customer):
    invoice_names = _get_contact_sales_invoice_names(contact, customer)
    if not invoice_names:
        return []
    meta = frappe.get_meta("Sales Invoice Item")
    fields = [
        "item_code",
        "item_name",
        {"SUM": "qty", "as": "qty"},
        {"SUM": "amount", "as": "amount"},
    ]
    group_by = "item_code, item_name"
    if meta.has_field("item_group"):
        fields.insert(2, "item_group")
        group_by += ", item_group"
    return frappe.get_all(
        "Sales Invoice Item",
        filters={"parent": ["in", invoice_names]},
        fields=fields,
        group_by=group_by,
        order_by="amount desc",
        limit_page_length=500,
    )


def _get_contact_tasks(contact, completed=False):
    if not frappe.has_permission("ToDo", "read"):
        return []
    status_filter = "Closed" if completed else ["!=", "Closed"]
    return frappe.get_list(
        "ToDo",
        filters={
            "reference_type": "Contact",
            "reference_name": contact,
            "status": status_filter,
        },
        fields=["name", "description", "date", "allocated_to", "assigned_by", "status", "priority", "modified"],
        order_by="date desc, modified desc",
        page_length=50,
    )


@frappe.whitelist(methods=["GET"])
def get_contact_detail(name):
    """Return a Contact's data for the detail/edit page (MISA-style)."""
    _check_permission("Contact", name=name)
    doc = frappe.get_doc("Contact", name)

    # Linked customer (first Customer dynamic link)
    customer = ""
    for link in doc.get("links", []):
        if link.link_doctype == "Customer":
            customer = link.link_name
            break

    # Primary address (prefer one linked to this contact)
    billing = {"address_line1": "", "county": "", "state": "", "country": "Vietnam", "pincode": ""}
    address_name = ""
    addr_names = frappe.get_all(
        "Dynamic Link",
        filters={"parenttype": "Address", "link_doctype": "Contact", "link_name": name},
        pluck="parent",
    )
    if addr_names:
        try:
            addr = frappe.get_doc("Address", addr_names[0])
            address_name = addr.name
            billing = {
                "address_line1": addr.address_line1 or "",
                "county": addr.county or "",
                "state": addr.state or "",
                "country": addr.country or "Vietnam",
                "pincode": addr.pincode or "",
            }
        except Exception:
            pass

    # ── Notes (Comments on this Contact) ──────────────────────
    notes = []
    if frappe.has_permission("Comment", "read"):
        notes = frappe.get_list(
            "Comment",
            filters={
                "reference_doctype": "Contact",
                "reference_name": name,
                "comment_type": "Comment",
            },
            fields=["name", "comment_by", "comment_by_fullname", "content", "creation"],
            order_by="creation desc",
        )

    # ── Attachments (Files linked to this Contact) ────────────
    attachments = []
    if frappe.has_permission("File", "read"):
        attachments = frappe.get_all(
            "File",
            filters={"attached_to_doctype": "Contact", "attached_to_name": name},
            fields=["name", "file_name", "file_url", "file_size", "is_private", "creation", "owner"],
            order_by="creation desc",
        )

    # ── Opportunities mapped to this Contact ──────────────────
    opportunities = []
    if frappe.has_permission("Opportunity", "read"):
        opportunities = frappe.get_all(
            "Opportunity",
            filters={"contact_person": name},
            fields=["name", "title", "opportunity_amount", "currency", "sales_stage",
                    "probability", "expected_closing", "opportunity_owner", "status"],
            order_by="creation desc",
        )
        for o in opportunities:
            o["expected_revenue"] = (o.get("opportunity_amount") or 0) * (o.get("probability") or 0) / 100.0

    purchased_items = _get_contact_purchased_items(name, customer)
    orders = _get_contact_linked_records(
        "Sales Order",
        name,
        customer,
        [
            "name", "customer_name", "transaction_date", "delivery_date", "grand_total",
            "currency", "status", "company", "owner", "contact_person",
            "custom_revenue_recognition_date",
        ],
        {"docstatus": ["<", 2]},
        "transaction_date desc, modified desc",
        customer_field="customer",
    )
    quotations = _get_contact_linked_records(
        "Quotation",
        name,
        customer,
        [
            "name", "transaction_date", "valid_till", "grand_total", "currency",
            "status", "title", "party_name", "contact_person",
        ],
        {"docstatus": ["<", 2]},
        "transaction_date desc, modified desc",
        customer_field="party_name",
    )
    invoices = _get_contact_linked_records(
        "Sales Invoice",
        name,
        customer,
        [
            "name", "customer_name", "posting_date", "due_date", "grand_total",
            "outstanding_amount", "currency", "status", "company", "owner",
            "contact_person", "is_return",
        ],
        {"docstatus": ["<", 2], "is_return": 0},
        "posting_date desc, modified desc",
        customer_field="customer",
        page_length=100,
    )
    activities = _get_contact_activities(name)
    active_tasks = [row for row in activities if row.get("status") == "Open"]
    done_tasks = [row for row in activities if row.get("status") != "Open"]

    return {
        "name": doc.name,
        "first_name": doc.first_name or "",
        "middle_name": doc.middle_name or "",
        "last_name": doc.last_name or "",
        "full_name": doc.full_name or "",
        "salutation": doc.salutation or "",
        "designation": doc.designation or "",
        "company_name": doc.company_name or "",
        "department": doc.department or "",
        "gender": doc.gender or "",
        "mobile_no": doc.mobile_no or "",
        "phone": doc.phone or "",
        "email_id": doc.email_id or "",
        "status": doc.status or "",
        "description": doc.get("notes") or "",
        "date_of_birth": str(doc.get("date_of_birth") or "") or "",
        "owner": doc.owner or "",
        "creation": str(doc.creation or "") or "",
        "modified": str(doc.modified or "") or "",
        "modified_by": doc.modified_by or "",
        "customer": customer,
        "address_name": address_name,
        "billing_address": billing,
        "notes": notes,
        "attachments": attachments,
        "opportunities": opportunities,
        "purchased_items": purchased_items,
        "orders": orders,
        "quotations": quotations,
        "invoices": invoices,
        "activities": activities,
        "active_tasks": active_tasks,
        "done_tasks": done_tasks,
        "activity_campaigns": (
            frappe.get_list(
                "UTM Campaign",
                fields=["name"],
                order_by="name asc",
                page_length=200,
            )
            if frappe.has_permission("UTM Campaign", "read")
            else []
        ),
        "activity_users": (
            frappe.get_list(
                "User",
                filters={"enabled": 1, "user_type": "System User"},
                fields=["name", "full_name"],
                order_by="full_name asc",
                page_length=200,
            )
            if frappe.has_permission("User", "read")
            else [{
                "name": frappe.session.user,
                "full_name": frappe.utils.get_fullname(frappe.session.user),
            }]
        ),
        "can_write": frappe.has_permission("Contact", "write", name),
        "can_create_activity": (
            frappe.has_permission("ToDo", "create")
            or frappe.has_permission("Event", "create")
        ),
    }

@frappe.whitelist(methods=["POST"])
def update_contact_standalone(name, data):
    """Update an existing Contact from the CRM detail page."""
    _check_permission("Contact", "write", name)
    if isinstance(data, str):
        data = json.loads(data)

    doc = frappe.get_doc("Contact", name)

    first_name = (data.get("first_name") or "").strip()
    if not first_name:
        frappe.throw(_("Tên là bắt buộc"), frappe.ValidationError)
    doc.first_name = first_name
    for field in ("middle_name", "last_name", "salutation", "designation",
                  "company_name", "department", "gender"):
        if field in data:
            doc.set(field, data.get(field) or None)

    _set_primary_contact_email(doc, data)
    _set_primary_contact_phone(doc, data, "mobile_no", "is_primary_mobile_no")
    _set_primary_contact_phone(doc, data, "phone", "is_primary_phone")

    # Sync linked Customer (replace existing Customer link if changed)
    customer = (data.get("customer") or "").strip()
    existing_customer_links = [l for l in doc.get("links", []) if l.link_doctype == "Customer"]
    current_customer = existing_customer_links[0].link_name if existing_customer_links else ""
    if customer != current_customer:
        doc.links = [l for l in doc.get("links", []) if l.link_doctype != "Customer"]
        if customer and frappe.db.exists("Customer", customer):
            _check_permission("Customer", name=customer)
            doc.append("links", {"link_doctype": "Customer", "link_name": customer})

    # Explicitly keep Version logging enabled. Frappe disables it implicitly
    # while running tests, which made this update path behave differently from
    # production and allowed regressions in the CRM audit timeline.
    doc.save(ignore_permissions=False, ignore_version=False)

    # Update or create the billing address
    billing = data.get("billing_address") or {}
    if isinstance(billing, str):
        billing = json.loads(billing)
    has_addr_data = any(billing.get(f) for f in ("address_line1", "state", "county", "pincode"))
    address_name = (data.get("address_name") or "").strip()
    if address_name and frappe.db.exists("Address", address_name):
        addr = frappe.get_doc("Address", address_name)
        addr.address_line1 = billing.get("address_line1") or addr.address_line1 or "-"
        addr.city = billing.get("state") or billing.get("county") or addr.city or "-"
        addr.state = billing.get("state") or ""
        addr.county = billing.get("county") or ""
        addr.country = billing.get("country") or "Vietnam"
        addr.pincode = billing.get("pincode") or ""
        addr.save(ignore_permissions=False, ignore_version=False)
    elif has_addr_data:
        addr = frappe.new_doc("Address")
        addr.address_title = doc.first_name + (" " + doc.last_name if doc.last_name else "")
        addr.address_type = "Billing"
        addr.is_primary_address = 1
        addr.address_line1 = billing.get("address_line1") or "-"
        addr.city = billing.get("state") or billing.get("county") or "-"
        addr.state = billing.get("state") or ""
        addr.county = billing.get("county") or ""
        addr.country = billing.get("country") or "Vietnam"
        addr.pincode = billing.get("pincode") or ""
        addr.append("links", {"link_doctype": "Contact", "link_name": doc.name})
        if customer:
            addr.append("links", {"link_doctype": "Customer", "link_name": customer})
        addr.insert(ignore_permissions=False)

    return {"name": doc.name, "full_name": doc.full_name or doc.first_name}


@frappe.whitelist(methods=["GET"])
def get_customer_create_options():
    """Return option lists for the customer creation form."""
    def opts(doctype, fields, order_by="name asc", page_length=500, filters=None):
        return frappe.get_list(
            doctype,
            filters=filters,
            fields=fields,
            order_by=order_by,
            page_length=page_length,
        )

    customer_meta = frappe.get_meta("Customer")

    def select_opts(fieldname):
        field = customer_meta.get_field(fieldname)
        values = (field.options or "").splitlines() if field else []
        return [{"name": value.strip()} for value in values if value.strip()]

    return {
        "customer_groups": opts("Customer Group", ["name"], filters={"is_group": 0}),
        "territories": opts("Territory", ["name"], filters={"is_group": 0}),
        "industries": opts("Industry Type", ["name"]),
        "countries": opts("Country", ["name"]),
        "market_segments": opts("Market Segment", ["name"]),
        "price_lists": opts(
            "Price List",
            ["name"],
            filters={"enabled": 1, "selling": 1},
        ),
        "sources": select_opts("nguon_goc"),
        "legal_types": select_opts("loai_hinh"),
        "business_lines": select_opts("nganh_nghe"),
    }


@frappe.whitelist(methods=["POST"])
def create_customer(customer, contact=None, billing_address=None, shipping_address=None):
    """Create a new Customer with optional contact, billing and shipping addresses."""
    _check_permission("Customer", "create")
    customer_values = _parse_json(customer, {})
    contact_values = _parse_json(contact, {})
    billing_values = _parse_json(billing_address, {})
    shipping_values = _parse_json(shipping_address, {})

    customer_name = (customer_values.get("customer_name") or "").strip()
    if not customer_name:
        frappe.throw(_("Tên khách hàng là bắt buộc"), frappe.ValidationError)

    allowed_fields = {
        "customer_name", "customer_type", "customer_group", "territory",
        "tax_id", "gender", "industry", "market_segment", "default_price_list",
        "account_manager", "website", "customer_details",
        # MISA custom fields
        "ten_viet_tat", "misa_mobile", "misa_email", "nguon_goc",
        "loai_hinh", "nganh_nghe",
        "tai_khoan_ngan_hang", "mo_tai_ngan_hang", "ngay_thanh_lap", "la_kh_tu",
        "quy_mo_doanh_thu", "quy_mo_nhan_su", "loai_han_muc_no", "so_ngay_duoc_no",
        "dung_chung", "la_kh_ca_nhan", "la_doi_tac_ctv", "doi_tac_gioi_thieu",
    }
    customer_meta = frappe.get_meta("Customer")
    doc = frappe.new_doc("Customer")
    for fieldname, value in customer_values.items():
        if fieldname in allowed_fields and customer_meta.has_field(fieldname):
            doc.set(fieldname, value or None)
    doc.customer_name = customer_name
    doc.insert()

    contact_doc = None
    if contact_values and any(v for v in contact_values.values() if v):
        contact_doc = _update_customer_contact(doc, contact_values)

    billing_doc = None
    if billing_values and any(v for v in billing_values.values() if v):
        billing_values.setdefault("address_type", "Billing")
        billing_values["is_primary_address"] = 1
        billing_doc = _update_customer_address(doc, billing_values)

    shipping_doc = None
    if shipping_values and any(v for v in shipping_values.values() if v):
        shipping_values.setdefault("address_type", "Shipping")
        shipping_values["is_shipping_address"] = 1
        shipping_doc = _update_customer_address(doc, shipping_values)

    return {
        "name": doc.name,
        "customer_name": doc.customer_name,
        "contact": contact_doc.name if contact_doc else None,
        "billing_address": billing_doc.name if billing_doc else None,
        "shipping_address": shipping_doc.name if shipping_doc else None,
    }


@frappe.whitelist(methods=["GET"])
def lookup_taxpayer(tax_code):
    """Proxy Vietnamese GDT taxpayer lookup via xinvoice public API."""
    import re
    import requests as _req

    tax_code = (tax_code or "").strip()
    if not re.match(r"^\d{10}(-\d{3})?$", tax_code):
        frappe.throw(_("Mã số thuế không hợp lệ (10 hoặc 13 chữ số)"), frappe.ValidationError)

    try:
        resp = _req.get(
            f"https://api.xinvoice.vn/gdt-api/tax-payer/{tax_code}",
            timeout=10,
            headers={"Accept": "application/json"},
        )
    except Exception as exc:
        frappe.throw(_("Không thể kết nối dịch vụ tra cứu MST: {0}").format(str(exc)))

    if resp.status_code == 404:
        return None
    if not resp.ok:
        frappe.throw(_("Dịch vụ tra cứu MST trả lỗi {0}").format(resp.status_code))

    data = resp.json()

    existing = frappe.db.get_value(
        "Customer", {"tax_id": tax_code}, ["name", "customer_name"], as_dict=True
    )
    if existing:
        data["existing_customer"] = existing

    return data


# ── Sales Order Actions ────────────────────────────────────────────────────

_SO_ACTION_LABEL = {
    "invoice": "Đề nghị xuất hóa đơn",
    "delivery": "Giao hàng",
    "return": "Đề nghị trả hàng",
    "purchase_request": "Yêu cầu mua hàng",
}

_SO_REVENUE_REQUEST_TASK_TYPE = "Đề nghị ghi doanh số"


def _get_open_so_revenue_requests(so_name):
    """Return open revenue-recognition requests linked to a Sales Order.

    The caller must check Sales Order permission first. ``get_all`` is used
    deliberately because this ToDo is also the workflow-state marker: the
    Sales Order status must not depend on whether the viewer can list ToDos.
    """
    return frappe.get_all(
        "ToDo",
        filters={
            "reference_type": "Sales Order",
            "reference_name": so_name,
            "status": "Open",
            "custom_task_type": _SO_REVENUE_REQUEST_TASK_TYPE,
        },
        fields=[
            "name", "owner", "description", "creation",
            "custom_related_users",
        ],
        order_by="creation desc",
    )

def _send_todo_notification(user_email, subject, todo_name):
    """Create a persistent Notification Log. Clicking the bell card navigates to CRM."""
    try:
        frappe.get_doc({
            "doctype": "Notification Log",
            "subject": subject,
            "for_user": user_email,
            "type": "Alert",
            # Keep an exact relation so withdrawing a request can retract only
            # the notifications created for that ToDo.
            "document_type": "ToDo",
            "document_name": todo_name,
            "link": "/desk/dcnet-crm?view=activities",
            "from_user": frappe.session.user,
        }).insert(ignore_permissions=True)
    except Exception:
        frappe.log_error(frappe.get_traceback(), "CRM Notification Error")


_ACTIVITY_TASK_TYPES = frozenset([
    "Đề nghị xuất hóa đơn", "Giao hàng", "Đề nghị trả hàng", "Yêu cầu mua hàng",
    "Gửi báo giá", "Nhắc cước đến hạn", "Check TT DVVT", "Khảo sát DVVT",
    "Triển khai DVVT", "Lập PAKD", "Nghiệm thu DVVT", "Hỗ trợ kỹ thuật",
    "Chăm sóc khách hàng", "Họp tư vấn", "Khác",
])


@frappe.whitelist(methods=["POST"])
def create_so_action(so_name, action, extra=None):
    """Create a permission-aware request task linked to a Sales Order.

    These CRM actions are requests, not accounting or stock transactions. The
    responsible ERPNext user creates and validates the resulting document in
    its native workflow after completing the task.
    """
    import json as _json
    if isinstance(extra, str):
        try:
            extra = _json.loads(extra)
        except Exception:
            extra = {}
    extra = extra or {}
    _check_permission("Sales Order", "read", name=so_name)
    _check_permission("ToDo", "create")

    _valid_actions = set(_SO_ACTION_LABEL) | {"activity"}
    if action not in _valid_actions:
        frappe.throw("Hành động không hợp lệ.")

    so = frappe.get_doc("Sales Order", so_name)
    label = _SO_ACTION_LABEL.get(action) or extra.get("task_type") or "Nhật ký hoạt động"
    if action == "activity" and label == _SO_REVENUE_REQUEST_TASK_TYPE:
        _check_permission("Sales Order", "write", name=so_name)
        if cint(so.docstatus) != 0:
            frappe.throw("Chỉ đơn nháp mới có thể đề nghị ghi doanh số.")
        if _get_open_so_revenue_requests(so_name):
            frappe.throw("Đơn hàng này đã có đề nghị ghi đang chờ xử lý.")

    customer_name = frappe.db.get_value("Customer", so.customer, "customer_name") or so.customer or ""
    from frappe.utils import formatdate
    date_str = formatdate(frappe.utils.nowdate(), "dd/MM/yyyy")
    po_ref = so.po_no or so_name
    todo = frappe.new_doc("ToDo")
    todo.owner = frappe.session.user
    custom_title = (extra.get("title") or "").strip()
    todo.description = custom_title if custom_title else f"{date_str} - {label} - {po_ref} - {customer_name}"
    todo.reference_type = "Sales Order"
    todo.reference_name = so_name
    todo.status = extra.get("status") or "Open"
    todo.date = extra.get("date") or frappe.utils.nowdate()
    todo.priority = extra.get("priority") or "Medium"
    todo.set("custom_task_type", extra.get("task_type") or label)
    if label == _SO_REVENUE_REQUEST_TASK_TYPE:
        todo.set("custom_revenue_item", extra.get("revenue_item") or None)
        todo.set("custom_revenue_department", extra.get("department") or None)
        todo.set("custom_revenue_recognized_amount", flt(extra.get("recognized_amount")))
        todo.set("custom_revenue_achieved_amount", flt(extra.get("achieved_amount")))
        todo.set("custom_revenue_note", extra.get("note") or "")
    related_users = extra.get("related_users") or []
    if related_users:
        todo.set("custom_related_users", _json.dumps([
            {"name": u["name"], "full_name": u.get("full_name", u["name"])}
            for u in related_users if isinstance(u, dict) and u.get("name")
        ]))
    todo.insert(ignore_permissions=False)

    # Share ToDo with related users and send persistent notification
    todo_title = (todo.description or label)[:80]
    current_user = frappe.session.user
    crm_url = "/desk/dcnet-crm?view=activities"
    for u in related_users:
        user_email = u.get("name") if isinstance(u, dict) else None
        if not user_email or user_email == current_user:
            continue
        if not frappe.db.exists("User", user_email):
            continue
        # Give read access so they can open the record if needed
        try:
            frappe.share.add("ToDo", todo.name, user=user_email, read=1, flags={"ignore_share_permission": True})
        except Exception:
            pass
        _send_todo_notification(
            user_email,
            f'Nhiệm vụ mới được giao: <b>{todo_title}</b> — <a href="{crm_url}">Xem trong CRM</a>',
            todo.name,
        )

    return {
        "action": action,
        "label": label,
        "doc_type": "ToDo",
        "doc_name": todo.name,
        "todo_name": todo.name,
    }


def _parse_todo_related_users(todo):
    raw = todo.get("custom_related_users") or []
    if isinstance(raw, str):
        try:
            raw = json.loads(raw)
        except (TypeError, ValueError):
            raw = []
    return [
        row.get("name")
        for row in raw
        if isinstance(row, dict) and row.get("name")
    ]


def _retract_todo_notifications(todo, related_users=None):
    """Delete notification cards created for a withdrawn ToDo request."""
    notification_names = set(frappe.get_all(
        "Notification Log",
        filters={"document_type": "ToDo", "document_name": todo.name},
        pluck="name",
    ))

    # Backward compatibility for notifications created before they were
    # linked by document_type/document_name.
    related_users = related_users or []
    if related_users and todo.get("description"):
        notification_names.update(frappe.get_all(
            "Notification Log",
            filters={
                "for_user": ["in", related_users],
                "from_user": todo.get("owner"),
                "subject": ["like", f"%{todo.get('description')[:80]}%"],
                "creation": [">=", todo.get("creation")],
            },
            pluck="name",
        ))

    for notification_name in notification_names:
        frappe.delete_doc(
            "Notification Log",
            notification_name,
            ignore_permissions=True,
        )
    return len(notification_names)


@frappe.whitelist(methods=["POST"])
def withdraw_so_revenue_request(so_name):
    """Withdraw open revenue requests and retract their user notifications."""
    _check_permission("Sales Order", "write", name=so_name)
    requests = _get_open_so_revenue_requests(so_name)
    if not requests:
        frappe.throw("Không có đề nghị ghi nào đang chờ để thu hồi.")

    retracted_notifications = 0
    cancelled_todos = []
    for request in requests:
        todo = frappe.get_doc("ToDo", request.name)
        related_users = _parse_todo_related_users(todo)
        todo.status = "Cancelled"
        # Sales Order write permission above authorizes this linked workflow
        # command even when the requester is not the current ToDo assignee.
        todo.save(ignore_permissions=True)
        cancelled_todos.append(todo.name)
        retracted_notifications += _retract_todo_notifications(todo, related_users)

        for user in related_users:
            try:
                frappe.share.remove("ToDo", todo.name, user=user)
            except Exception:
                frappe.log_error(
                    frappe.get_traceback(),
                    "CRM ToDo Share Retraction Error",
                )
            # Ask an already-open Desk session to refresh the bell list so the
            # withdrawn notification disappears without a page reload.
            frappe.publish_realtime(
                "notification",
                user=user,
                after_commit=True,
            )

    return {
        "so_name": so_name,
        "cancelled_todos": cancelled_todos,
        "retracted_notifications": retracted_notifications,
    }


# ── Activities (standalone ToDo workspace) ─────────────────────────────────

_ACTIVITY_FULL_ACCESS_ROLES = {"System Manager", "Administrator", "Sales Manager", "Sales Master Manager"}


@frappe.whitelist(methods=["GET"])
def get_activity_list(search=None, page=1, page_length=20, status=None, customer=None):
    """Paginated ToDo list. Full-access roles see all; others see own + related."""
    page = cint(page) or 1
    page_length = cint(page_length) or 20
    offset = (page - 1) * page_length

    user = frappe.session.user
    user_roles = set(frappe.get_roles(user))
    full_access = bool(user_roles & _ACTIVITY_FULL_ACCESS_ROLES)

    conditions = []
    values = {"limit": page_length, "offset": offset}

    if status and status != "all":
        conditions.append("`tabToDo`.`status` = %(status)s")
        values["status"] = status

    if search:
        conditions.append("`tabToDo`.`description` LIKE %(search)s")
        values["search"] = f"%{search}%"

    if customer:
        conditions.append(
            "("
            "(`tabToDo`.`reference_type` = 'Customer' AND `tabToDo`.`reference_name` = %(customer)s)"
            " OR (`tabToDo`.`reference_type` = 'Sales Order' AND `tabToDo`.`reference_name` IN ("
            "SELECT `name` FROM `tabSales Order` WHERE `customer` = %(customer)s))"
            ")"
        )
        values["customer"] = customer

    if not full_access:
        # Show only todos where user is owner OR user is in related_users JSON
        conditions.append(
            "(`tabToDo`.`owner` = %(user)s"
            " OR `tabToDo`.`custom_related_users` LIKE %(user_like)s)"
        )
        values["user"] = user
        values["user_like"] = f"%{user}%"

    where = ("WHERE " + " AND ".join(conditions)) if conditions else ""

    todos = frappe.db.sql(
        f"""
        SELECT name, description, date, status, priority,
               owner, assigned_by_full_name, reference_type, reference_name,
               creation, modified, custom_task_type, custom_related_users
        FROM `tabToDo`
        {where}
        ORDER BY creation DESC
        LIMIT %(limit)s OFFSET %(offset)s
        """,
        values,
        as_dict=True,
    )

    total = frappe.db.sql(
        f"SELECT COUNT(*) FROM `tabToDo` {where}",
        values,
    )[0][0]

    # Enrich with customer info and task_type
    for todo in todos:
        todo["doctype"] = "ToDo"
        todo["customer"] = None
        todo["customer_name"] = None
        ref_type = todo.get("reference_type")
        ref_name = todo.get("reference_name")
        if ref_type == "Sales Order" and ref_name:
            cust = frappe.db.get_value(
                "Sales Order", ref_name, ["customer", "customer_name"], as_dict=True
            )
            if cust:
                todo["customer"] = cust.customer
                todo["customer_name"] = cust.customer_name
        elif ref_type == "Customer" and ref_name:
            todo["customer"] = ref_name
            todo["customer_name"] = frappe.db.get_value("Customer", ref_name, "customer_name")

        stored_type = todo.get("custom_task_type") or ""
        if stored_type:
            todo["task_type"] = stored_type
        else:
            desc = todo.get("description") or ""
            parts = [p.strip() for p in desc.split(" - ")]
            todo["task_type"] = next((p for p in parts if p in _ACTIVITY_TASK_TYPES), "")

        todo["owner_full_name"] = (
            frappe.db.get_value("User", todo.get("owner"), "full_name") or todo.get("owner", "")
        )

        related_users = []
        try:
            for entry in json.loads(todo.get("custom_related_users") or "[]"):
                user_id = entry if isinstance(entry, str) else entry.get("name")
                if not user_id:
                    continue
                related_users.append({
                    "name": user_id,
                    "full_name": entry.get("full_name") if isinstance(entry, dict) else (
                        frappe.db.get_value("User", user_id, "full_name") or user_id
                    ),
                })
        except (TypeError, ValueError):
            related_users = []
        todo["related_users"] = related_users
        todo.pop("custom_related_users", None)

    return {"data": todos, "total": total}


def _user_can_access_todo(todo, perm="read"):
    """Return True if current user has perm via role/DocShare OR is in custom_related_users."""
    if frappe.has_permission("ToDo", perm, doc=todo):
        return True
    # Fallback: check related_users JSON
    import json as _j
    try:
        related = _j.loads(todo.get("custom_related_users") or "[]")
        emails = {u if isinstance(u, str) else u.get("name", "") for u in related}
    except Exception:
        emails = set()
    return frappe.session.user in emails


def _get_event_activity_detail(name):
    """Normalize an Event so it can be displayed in the CRM Activities workspace."""
    event = frappe.get_doc("Event", name)
    if not frappe.has_permission("Event", "read", doc=event):
        frappe.throw(f"No permission for Event {name}", frappe.PermissionError)

    participants = frappe.get_all(
        "Event Participants",
        filters={"parenttype": "Event", "parent": name},
        fields=["reference_doctype", "reference_docname"],
    )
    related_users = []
    for participant in participants:
        if participant.reference_doctype != "User" or not participant.reference_docname:
            continue
        related_users.append(
            {
                "name": participant.reference_docname,
                "full_name": (
                    frappe.db.get_value("User", participant.reference_docname, "full_name")
                    or participant.reference_docname
                ),
            }
        )

    reference_type = event.get("reference_doctype")
    reference_name = event.get("reference_docname")
    if not reference_type or not reference_name:
        reference = next(
            (
                participant
                for participant in participants
                if participant.reference_doctype != "User" and participant.reference_docname
            ),
            None,
        )
        if reference:
            reference_type = reference.reference_doctype
            reference_name = reference.reference_docname

    owner = event.owner
    return {
        "doctype": "Event",
        "name": event.name,
        "description": event.subject or event.description or "",
        "date": str(event.starts_on) if event.starts_on else None,
        "status": event.status,
        "priority": "Medium",
        "owner": owner,
        "owner_full_name": frappe.db.get_value("User", owner, "full_name") or owner,
        "assigned_by": owner,
        "assigned_by_full_name": frappe.db.get_value("User", owner, "full_name") or owner,
        "reference_type": reference_type,
        "reference_name": reference_name,
        "creation": str(event.creation) if event.creation else None,
        "modified": str(event.modified) if event.modified else None,
        "modified_by": event.modified_by,
        "modified_by_full_name": (
            frappe.db.get_value("User", event.modified_by, "full_name") or event.modified_by
            if event.modified_by else None
        ),
        "department": (
            frappe.db.get_value("Employee", {"user_id": owner}, "department")
            if owner else None
        ),
        # The current Activities edit form persists ToDo fields only. Event remains
        # read-only here instead of sending an invalid update_activity request.
        "can_write": False,
        "customer": reference_name if reference_type == "Customer" else None,
        "customer_name": (
            frappe.db.get_value("Customer", reference_name, "customer_name")
            if reference_type == "Customer" and reference_name else None
        ),
        "customer_info": None,
        "related_tasks": [],
        "related_users": related_users,
        "task_type": "Cuộc gọi" if event.event_category == "Call" else "Lịch hẹn",
    }


@frappe.whitelist(methods=["GET"])
def get_activity_detail(name, doctype=None):
    """Return one ToDo or Event for the internal CRM Activities workspace."""
    requested_doctype = doctype or "ToDo"
    if requested_doctype not in {"ToDo", "Event"}:
        frappe.throw("Unsupported activity type", frappe.ValidationError)
    if requested_doctype == "Event":
        return _get_event_activity_detail(name)

    todo = frappe.get_doc("ToDo", name)

    if not _user_can_access_todo(todo, "read"):
        frappe.throw(f"No permission for ToDo {name}", frappe.PermissionError)

    can_write = _user_can_access_todo(todo, "write")

    result = {
        "doctype": "ToDo",
        "name": todo.name,
        "description": todo.description or "",
        "date": str(todo.date) if todo.date else None,
        "status": todo.status,
        "priority": todo.priority,
        "owner": todo.owner,
        "owner_full_name": frappe.db.get_value("User", todo.owner, "full_name") or todo.owner,
        "assigned_by": todo.assigned_by,
        "assigned_by_full_name": todo.assigned_by_full_name,
        "reference_type": todo.reference_type,
        "reference_name": todo.reference_name,
        "creation": str(todo.creation) if todo.creation else None,
        "modified": str(todo.modified) if todo.modified else None,
        "modified_by": todo.modified_by,
        "modified_by_full_name": (
            frappe.db.get_value("User", todo.modified_by, "full_name") or todo.modified_by
            if todo.modified_by else None
        ),
        "department": (
            frappe.db.get_value("Employee", {"user_id": todo.owner}, "department")
            if todo.owner else None
        ),
        "can_write": can_write,
        "customer": None,
        "customer_name": None,
        "customer_info": None,
        "related_tasks": [],
    }

    # task_type: prefer custom field, fall back to scanning description segments
    stored_type = todo.get("custom_task_type") or ""
    if stored_type:
        result["task_type"] = stored_type
    else:
        desc = todo.description or ""
        parts = [p.strip() for p in desc.split(" - ")]
        result["task_type"] = next((p for p in parts if p in _ACTIVITY_TASK_TYPES), "")

    # Parse related users from custom JSON field
    raw_related = todo.get("custom_related_users") or "[]"
    try:
        related_users_raw = json.loads(raw_related) if isinstance(raw_related, str) else (raw_related or [])
    except Exception:
        related_users_raw = []
    result["related_users"] = [
        {
            "name": u if isinstance(u, str) else u.get("name", ""),
            "full_name": (
                frappe.db.get_value("User", u if isinstance(u, str) else u.get("name", ""), "full_name")
                or (u if isinstance(u, str) else u.get("name", ""))
            ),
        }
        for u in related_users_raw
    ]

    # Resolve customer
    customer_key = None
    ref_type = todo.reference_type
    ref_name = todo.reference_name
    if ref_type == "Sales Order" and ref_name:
        cust = frappe.db.get_value("Sales Order", ref_name, ["customer", "customer_name"], as_dict=True)
        if cust:
            result["customer"] = cust.customer
            result["customer_name"] = cust.customer_name
            customer_key = cust.customer
    elif ref_type == "Customer" and ref_name:
        result["customer"] = ref_name
        result["customer_name"] = frappe.db.get_value("Customer", ref_name, "customer_name")
        customer_key = ref_name

    # Customer info panel
    if customer_key and frappe.has_permission("Customer", "read"):
        try:
            cinfo = frappe.db.get_value(
                "Customer", customer_key,
                ["customer_name", "customer_type", "tax_id", "mobile_no", "industry", "customer_group"],
                as_dict=True,
            )
            result["customer_info"] = cinfo or None
        except Exception:
            pass

    # Related open tasks on same customer (via SO links)
    if customer_key and frappe.has_permission("ToDo", "read"):
        so_names = frappe.get_all(
            "Sales Order", filters={"customer": customer_key, "docstatus": ["<", 2]}, pluck="name", limit=50
        )
        if so_names:
            related = frappe.get_list(
                "ToDo",
                filters={
                    "name": ["!=", name],
                    "reference_type": "Sales Order",
                    "reference_name": ["in", list(so_names)],
                    "status": "Open",
                },
                fields=["name", "description", "date", "status", "priority"],
                limit=10,
                order_by="date asc",
            )
            result["related_tasks"] = related

    result["files"] = frappe.get_list(
        "File",
        filters={"attached_to_doctype": "ToDo", "attached_to_name": name},
        fields=["name", "file_name", "file_url", "file_size", "owner", "creation"],
        order_by="creation desc",
    )
    result["comments"] = frappe.get_list(
        "Comment",
        filters={"reference_doctype": "ToDo", "reference_name": name, "comment_type": "Comment"},
        fields=["name", "content", "comment_email", "owner", "creation"],
        order_by="creation desc",
    )
    result["communications"] = frappe.get_list(
        "Communication",
        filters={"reference_doctype": "ToDo", "reference_name": name},
        fields=["name", "content", "sender", "sender_full_name", "creation"],
        order_by="creation desc",
    )

    return result


@frappe.whitelist(methods=["POST"])
def add_activity_note(name, content):
    """Add an internal note (Comment) to a ToDo activity."""
    todo = frappe.get_doc("ToDo", name)
    if not _user_can_access_todo(todo, "write"):
        frappe.throw(f"No permission for ToDo {name}", frappe.PermissionError)
    content = (content or "").strip()
    if not content:
        frappe.throw(_("Note content is required"), frappe.ValidationError)

    comment = frappe.get_doc({
        "doctype": "Comment",
        "comment_type": "Comment",
        "reference_doctype": "ToDo",
        "reference_name": name,
        "content": content,
    })
    comment.insert(ignore_permissions=False)
    return {"name": comment.name}


@frappe.whitelist(methods=["POST"])
def add_activity_conversation(name, content):
    """Add an activity exchange as Communication, separate from internal notes."""
    todo = frappe.get_doc("ToDo", name)
    if not _user_can_access_todo(todo, "write"):
        frappe.throw(f"No permission for ToDo {name}", frappe.PermissionError)
    content = (content or "").strip()
    if not content:
        frappe.throw(_("Nội dung trao đổi là bắt buộc"), frappe.ValidationError)
    _check_permission("Communication", "create")

    communication = frappe.get_doc({
        "doctype": "Communication",
        "communication_type": "Communication",
        "communication_medium": "Other",
        "sent_or_received": "Sent",
        "subject": _("Trao đổi hoạt động"),
        "content": content,
        "sender": frappe.session.user,
        "sender_full_name": frappe.utils.get_fullname(frappe.session.user),
        "reference_doctype": "ToDo",
        "reference_name": name,
        "status": "Linked",
    })
    communication.insert(ignore_permissions=False)
    return {"name": communication.name}


@frappe.whitelist(methods=["POST"])
def add_activity_attachment_link(name, url, title=None):
    """Attach an external link as a File to a ToDo activity."""
    todo = frappe.get_doc("ToDo", name)
    if not _user_can_access_todo(todo, "write"):
        frappe.throw(f"No permission for ToDo {name}", frappe.PermissionError)
    url = _normalize_external_url(url)

    file_doc = frappe.get_doc({
        "doctype": "File",
        "file_url": url,
        "file_name": (title or "").strip() or url,
        "attached_to_doctype": "ToDo",
        "attached_to_name": name,
    })
    file_doc.insert(ignore_permissions=False)
    return {"name": file_doc.name}


@frappe.whitelist(methods=["POST"])
def delete_activity_attachment(file_name):
    """Delete a File attached to a ToDo activity."""
    file_doc = frappe.get_doc("File", file_name)
    if file_doc.attached_to_doctype != "ToDo":
        frappe.throw(_("Tệp không thuộc hoạt động này"))
    todo = frappe.get_doc("ToDo", file_doc.attached_to_name)
    if not _user_can_access_todo(todo, "write"):
        frappe.throw(f"No permission for ToDo {file_doc.attached_to_name}", frappe.PermissionError)
    file_doc.delete()


@frappe.whitelist(methods=["GET"])
def get_care_card_detail(name):
    """Return a CRM Care Card with customer info and the three MISA timelines:
    Hoạt động (activities), Mua hàng (purchases), Chăm sóc (care history)."""
    _check_permission("CRM Care Card", name=name)
    doc = frappe.get_doc("CRM Care Card", name)

    card = {
        "name": doc.name,
        "customer": doc.customer,
        "customer_name": doc.customer_name,
        "tax_id": doc.tax_id,
        "mobile_no": doc.mobile_no,
        "email_id": doc.email_id,
        "address": doc.address,
        "province": doc.province,
        "district": doc.district,
        "ward": doc.ward,
        "country": doc.country,
        "established_date": str(doc.established_date) if doc.established_date else None,
        "sales_order": doc.sales_order,
        "item": doc.item,
        "item_type": doc.item_type,
        "order_executor": doc.order_executor,
        "order_executor_name": (
            frappe.db.get_value("User", doc.order_executor, "full_name") or doc.order_executor
            if doc.order_executor else None
        ),
        "layout": doc.layout,
        "status": doc.status,
        "care_date": str(doc.care_date) if doc.care_date else None,
        "satisfaction_level": doc.satisfaction_level,
        "dissatisfaction_reason": doc.dissatisfaction_reason,
        "description": doc.description,
        "department": doc.department,
        "related_users": doc.related_users,
        "owner": doc.owner,
        "owner_full_name": frappe.db.get_value("User", doc.owner, "full_name") or doc.owner,
        "modified_by": doc.modified_by,
        "modified_by_full_name": frappe.db.get_value("User", doc.modified_by, "full_name") or doc.modified_by,
        "creation": str(doc.creation) if doc.creation else None,
        "modified": str(doc.modified) if doc.modified else None,
        "can_write": frappe.has_permission("CRM Care Card", "write", doc=doc),
    }

    customer_key = doc.customer
    customer_info = None
    if customer_key and frappe.has_permission("Customer", "read"):
        customer_info = frappe.db.get_value(
            "Customer", customer_key,
            ["customer_name", "customer_type", "tax_id", "mobile_no",
             "email_id", "industry", "customer_group", "territory"],
            as_dict=True,
        ) or None

    activities = []
    purchases = []
    care = []

    # ── Hoạt động: Communications + ToDos referencing the customer ──
    if customer_key:
        comms = frappe.get_all(
            "Communication",
            filters={"reference_doctype": "Customer", "reference_name": customer_key},
            fields=["name", "subject", "content", "communication_date",
                    "sender_full_name", "sender", "communication_medium"],
            order_by="communication_date desc",
            limit=30,
        )
        for c in comms:
            activities.append({
                "name": c.name,
                "kind": (c.communication_medium or "Email"),
                "title": c.subject or "(Không tiêu đề)",
                "content": frappe.utils.strip_html(c.content or "")[:600],
                "date": str(c.communication_date) if c.communication_date else None,
                "owner_full_name": c.sender_full_name or c.sender or "",
            })

        todos = _customer_todos(
            customer_key,
            ["name", "description", "date", "status", "owner"],
            order_by="creation desc",
        )
        for t in todos:
            activities.append({
                "name": t.name,
                "kind": "Task",
                "title": frappe.utils.strip_html(t.description or "")[:200],
                "content": "",
                "date": str(t.date) if t.date else None,
                "owner_full_name": frappe.db.get_value("User", t.owner, "full_name") or t.owner or "",
            })
        activities.sort(key=lambda x: x.get("date") or "", reverse=True)

    # ── Mua hàng: Sales Orders + Sales Invoices ──
    if customer_key and frappe.has_permission("Sales Order", "read"):
        for so in frappe.get_all(
            "Sales Order",
            filters={"customer": customer_key, "docstatus": ["<", 2]},
            fields=["name", "transaction_date", "grand_total", "status", "currency"],
            order_by="transaction_date desc", limit=30,
        ):
            purchases.append({
                "name": so.name, "kind": "Đơn hàng",
                "date": str(so.transaction_date) if so.transaction_date else None,
                "amount": so.grand_total, "currency": so.currency, "status": so.status,
            })
    if customer_key and frappe.has_permission("Sales Invoice", "read"):
        for si in frappe.get_all(
            "Sales Invoice",
            filters={"customer": customer_key, "docstatus": ["<", 2]},
            fields=["name", "posting_date", "grand_total", "status", "currency", "outstanding_amount"],
            order_by="posting_date desc", limit=30,
        ):
            purchases.append({
                "name": si.name, "kind": "Hóa đơn",
                "date": str(si.posting_date) if si.posting_date else None,
                "amount": si.grand_total, "currency": si.currency, "status": si.status,
                "outstanding": si.outstanding_amount,
            })
    purchases.sort(key=lambda x: x.get("date") or "", reverse=True)

    # ── Chăm sóc: comments + communications attached to this care card ──
    for cm in frappe.get_all(
        "Comment",
        filters={"reference_doctype": "CRM Care Card", "reference_name": name,
                 "comment_type": ["in", ["Comment", "Info"]]},
        fields=["name", "content", "creation", "comment_email", "comment_by"],
        order_by="creation desc", limit=50,
    ):
        care.append({
            "name": cm.name, "kind": "Ghi chú",
            "title": frappe.utils.strip_html(cm.content or "")[:600],
            "content": "",
            "date": str(cm.creation) if cm.creation else None,
            "owner_full_name": cm.comment_by or cm.comment_email or "",
        })
    if doc.care_date or doc.description:
        care.append({
            "name": doc.name, "kind": "Chăm sóc",
            "title": doc.description or "Chăm sóc khách hàng",
            "content": (f"Mức độ hài lòng: {doc.satisfaction_level}" if doc.satisfaction_level else ""),
            "date": str(doc.care_date) if doc.care_date else (str(doc.creation) if doc.creation else None),
            "owner_full_name": card["owner_full_name"],
        })
    care.sort(key=lambda x: x.get("date") or "", reverse=True)

    return {
        "card": card,
        "customer_info": customer_info,
        "activities": activities,
        "purchases": purchases,
        "care": care,
    }


@frappe.whitelist(methods=["POST"])
def add_care_note(name, content):
    """Add a care note (Comment) to a CRM Care Card — feeds the Chăm sóc timeline."""
    _check_permission("CRM Care Card", name=name)
    content = (content or "").strip()
    if not content:
        frappe.throw(_("Nội dung ghi chú không được để trống"))
    doc = frappe.get_doc("CRM Care Card", name)
    doc.add_comment("Comment", content)
    return {"ok": True}


_CARE_CARD_EDITABLE = (
    "customer", "tax_id", "mobile_no", "email_id",
    "province", "district", "ward", "country", "address", "established_date",
    "sales_order", "item", "item_type", "order_executor",
    "status", "care_date", "satisfaction_level", "dissatisfaction_reason",
    "description", "department", "layout", "related_users",
)


@frappe.whitelist(methods=["POST"])
def save_care_card(name=None, data=None):
    """Create (name empty) or update a CRM Care Card. Returns the new name."""
    if isinstance(data, str):
        data = json.loads(data or "{}")
    data = data or {}

    if name:
        _check_permission("CRM Care Card", name=name)
        doc = frappe.get_doc("CRM Care Card", name)
    else:
        _check_permission("CRM Care Card")
        if not data.get("customer"):
            frappe.throw(_("Vui lòng chọn Khách hàng"))
        doc = frappe.new_doc("CRM Care Card")

    for field in _CARE_CARD_EDITABLE:
        if field in data:
            doc.set(field, data[field] or None)

    doc.save(ignore_permissions=False)
    return {"name": doc.name}


@frappe.whitelist(methods=["POST"])
def update_activity(name, data):
    """Update editable fields on a ToDo and notify newly added related users."""
    if isinstance(data, str):
        data = json.loads(data)

    todo = frappe.get_doc("ToDo", name)
    if not _user_can_access_todo(todo, "write"):
        frappe.throw(f"No permission to update ToDo {name}", frappe.PermissionError)

    for field in ("description", "date", "status", "priority"):
        if field in data and data[field] is not None:
            setattr(todo, field, data[field])

    if "task_type" in data:
        todo.set("custom_task_type", data["task_type"] or "")

    # Handle related_users — store as JSON, notify newly added users
    if "related_users" in data:
        new_users = [u if isinstance(u, str) else u.get("name", "") for u in (data["related_users"] or [])]

        raw_prev = todo.get("custom_related_users") or "[]"
        try:
            prev_users = json.loads(raw_prev) if isinstance(raw_prev, str) else (raw_prev or [])
            prev_set = {u if isinstance(u, str) else u.get("name", "") for u in prev_users}
        except Exception:
            prev_set = set()

        todo.set("custom_related_users", json.dumps(new_users))

        newly_added = [u for u in new_users if u and u not in prev_set]
        title = (todo.description or name)[:80]
        crm_url = "/desk/dcnet-crm?view=activities"
        for user_email in newly_added:
            if not frappe.db.exists("User", user_email):
                continue
            try:
                frappe.share.add("ToDo", todo.name, user=user_email, read=1, flags={"ignore_share_permission": True})
            except Exception:
                pass
            _send_todo_notification(
                user_email,
                f'Bạn được thêm vào nhiệm vụ: <b>{title}</b> — <a href="{crm_url}">Xem trong CRM</a>',
                todo.name,
            )

    todo.save(ignore_permissions=True)
    return {"name": todo.name, "status": todo.status}


@frappe.whitelist()
def search_crm_users(query="", limit=10):
    """Search enabled System Users by full_name for the related-users selector."""
    query = (query or "").strip()
    filters = {"enabled": 1, "user_type": "System User"}
    users = frappe.get_list(
        "User",
        filters=filters,
        fields=["name", "full_name", "user_image"],
        or_filters={"full_name": ["like", f"%{query}%"], "name": ["like", f"%{query}%"]} if query else {},
        limit=int(limit),
        order_by="full_name asc",
    )
    return users


_CRM_AUDIT_DOCTYPES = {
    "Lead": "Tiềm năng",
    "Contact": "Liên hệ",
    "Customer": "Khách hàng",
    "Opportunity": "Cơ hội",
    "Quotation": "Báo giá",
    "Sales Order": "Đơn hàng",
    "ToDo": "Nhiệm vụ",
    "Event": "Lịch hẹn",
}


def _audit_value(value):
    """Return a compact JSON-safe value for the audit timeline."""
    if value is None or value == "":
        return None
    if isinstance(value, (str, int, float, bool)):
        text = str(value)
        return text[:500] + ("…" if len(text) > 500 else "")
    if isinstance(value, (list, tuple, dict)):
        text = frappe.as_json(value)
        return text[:500] + ("…" if len(text) > 500 else "")
    return str(value)[:500]


def _audit_change(doc, fieldname, old_value=None, new_value=None, action="changed"):
    df = doc.meta.get_field(fieldname)
    if not df or df.hidden or df.fieldtype == "Password":
        return None
    if not doc.has_permlevel_access_to(fieldname, df, "read"):
        return None
    return {
        "field": fieldname,
        "label": _(df.label or fieldname),
        "action": action,
        "old_value": _audit_value(old_value),
        "new_value": _audit_value(new_value),
    }


def _parse_audit_version(doc, version, label_prefix=None):
    try:
        data = frappe.parse_json(version.data or "{}") or {}
    except (TypeError, ValueError):
        data = {}

    changes = []
    for row in data.get("changed") or []:
        if not isinstance(row, (list, tuple)) or len(row) < 3:
            continue
        change = _audit_change(doc, row[0], row[1], row[2])
        if change:
            changes.append(change)

    for key, action in (("added", "added"), ("removed", "removed"), ("row_changed", "row_changed")):
        for row in data.get(key) or []:
            if not isinstance(row, (list, tuple)) or not row:
                continue
            fieldname = row[0]
            change = _audit_change(
                doc,
                fieldname,
                None,
                None,
                action,
            )
            if change:
                changes.append(change)

    if label_prefix:
        for change in changes:
            change["label"] = f"{label_prefix} · {change['label']}"
    return changes


def _get_related_audit_documents(doctype, name):
    """Return child documents whose changes belong in the parent CRM history."""
    if doctype not in {"Contact", "Customer"}:
        return []

    address_names = frappe.get_all(
        "Dynamic Link",
        filters={
            "parenttype": "Address",
            "link_doctype": doctype,
            "link_name": name,
        },
        pluck="parent",
    )
    related = []
    for address_name in dict.fromkeys(address_names):
        if not frappe.db.exists("Address", address_name):
            continue
        address = frappe.get_doc("Address", address_name)
        try:
            address.check_permission("read")
        except frappe.PermissionError:
            continue
        address_label = address.address_type or address.address_title or _("Địa chỉ")
        related.append((address, f"{_('Địa chỉ')} ({address_label})"))
    return related


@frappe.whitelist(methods=["GET"])
def get_document_audit_log(doctype, name, limit=50):
    """Return a permission-filtered audit timeline for CRM detail pages."""
    if doctype not in _CRM_AUDIT_DOCTYPES or not name:
        frappe.throw(_("Loại dữ liệu không hỗ trợ nhật ký"), frappe.ValidationError)

    doc = frappe.get_doc(doctype, name)
    doc.check_permission("read")
    page_length = min(max(cint(limit), 1), 100)

    # Version inherits access from its referenced document. Query it only after
    # every source document permission and field permlevel have been checked.
    sources = [(doc, None), *_get_related_audit_documents(doctype, doc.name)]
    version_sources = []
    for source_doc, label_prefix in sources:
        source_versions = frappe.get_all(
            "Version",
            filters={
                "ref_doctype": source_doc.doctype,
                "docname": str(source_doc.name),
            },
            fields=["name", "owner", "creation", "data"],
            order_by="creation desc",
            limit=page_length,
        )
        version_sources.extend(
            (source_doc, label_prefix, version) for version in source_versions
        )

    # ── Actions that don't change a field on `doc` itself (tasks, meetings,
    # calls, notes created against it) so "Nhật ký" reflects everything the
    # user does, not just tracked field diffs. ─────────────────────────────
    todo_rows = []
    if frappe.has_permission("ToDo", "read"):
        todo_rows = frappe.get_all(
            "ToDo",
            filters={"reference_type": doctype, "reference_name": name},
            fields=["name", "description", "creation", "owner", "status", "modified", "modified_by"],
        )

    event_rows = []
    if frappe.has_permission("Event", "read"):
        event_names = frappe.get_all(
            "Event Participants",
            filters={"reference_doctype": doctype, "reference_docname": name},
            pluck="parent",
        )
        if event_names:
            event_rows = frappe.get_all(
                "Event",
                filters={"name": ["in", list(set(event_names))]},
                fields=["name", "subject", "event_category", "creation", "owner", "status", "modified", "modified_by"],
            )

    comment_rows = []
    if frappe.has_permission("Comment", "read"):
        comment_rows = frappe.get_all(
            "Comment",
            filters={"reference_doctype": doctype, "reference_name": name, "comment_type": "Comment"},
            fields=["name", "content", "creation", "comment_by"],
        )

    actor_ids = {
        version.owner
        for _source_doc, _label_prefix, version in version_sources
        if version.owner
    }
    actor_ids.update(row.owner for row in todo_rows if row.owner)
    actor_ids.update(row.modified_by for row in todo_rows if row.modified_by)
    actor_ids.update(row.owner for row in event_rows if row.owner)
    actor_ids.update(row.modified_by for row in event_rows if row.modified_by)
    actor_ids.update(row.comment_by for row in comment_rows if row.comment_by)
    if doc.owner:
        actor_ids.add(doc.owner)
    actor_names = {
        user.name: user.full_name or user.name
        for user in frappe.get_all(
            "User",
            filters={"name": ["in", list(actor_ids)]},
            fields=["name", "full_name"],
        )
    } if actor_ids else {}

    entries = []
    for source_doc, label_prefix, version in version_sources:
        changes = _parse_audit_version(source_doc, version, label_prefix)
        if not changes:
            continue
        entries.append({
            "name": version.name,
            "kind": "updated",
            "actor": version.owner,
            "actor_name": actor_names.get(version.owner, version.owner),
            "creation": version.creation,
            "changes": changes,
            "source_doctype": source_doc.doctype,
            "source_name": source_doc.name,
        })

    for row in todo_rows:
        entries.append({
            "name": f"todo-{row.name}",
            "kind": "activity_created",
            "actor": row.owner,
            "actor_name": actor_names.get(row.owner, row.owner),
            "creation": row.creation,
            "summary": _("đã tạo nhiệm vụ: {0}").format(row.description or row.name),
            "changes": [],
        })
        if row.status == "Cancelled" and row.modified_by:
            entries.append({
                "name": f"todo-cancelled-{row.name}",
                "kind": "activity_cancelled",
                "actor": row.modified_by,
                "actor_name": actor_names.get(row.modified_by, row.modified_by),
                "creation": row.modified,
                "summary": _("đã thu hồi nhiệm vụ: {0}").format(row.description or row.name),
                "changes": [],
            })

    for row in event_rows:
        label = _("cuộc gọi") if row.event_category == "Call" else _("lịch hẹn")
        entries.append({
            "name": f"event-{row.name}",
            "kind": "activity_created",
            "actor": row.owner,
            "actor_name": actor_names.get(row.owner, row.owner),
            "creation": row.creation,
            "summary": _("đã tạo {0}: {1}").format(label, row.subject or row.name),
            "changes": [],
        })
        if row.status == "Cancelled" and row.modified_by:
            entries.append({
                "name": f"event-cancelled-{row.name}",
                "kind": "activity_cancelled",
                "actor": row.modified_by,
                "actor_name": actor_names.get(row.modified_by, row.modified_by),
                "creation": row.modified,
                "summary": _("đã hủy {0}: {1}").format(label, row.subject or row.name),
                "changes": [],
            })

    for row in comment_rows:
        content = frappe.utils.strip_html(row.content or "")
        entries.append({
            "name": f"comment-{row.name}",
            "kind": "commented",
            "actor": row.comment_by,
            "actor_name": actor_names.get(row.comment_by, row.comment_by),
            "creation": row.creation,
            "summary": content[:280] + ("…" if len(content) > 280 else ""),
            "changes": [],
        })

    entries.append({
        "name": f"creation-{doc.name}",
        "kind": "created",
        "actor": doc.owner,
        "actor_name": actor_names.get(doc.owner, doc.owner),
        "creation": doc.creation,
        "changes": [],
    })
    entries.sort(key=lambda entry: str(entry.get("creation") or ""), reverse=True)
    entries = entries[:page_length]
    return {
        "doctype": doctype,
        "doctype_label": _CRM_AUDIT_DOCTYPES[doctype],
        "name": doc.name,
        "title": doc.get_title() or doc.name,
        "entries": entries,
    }
