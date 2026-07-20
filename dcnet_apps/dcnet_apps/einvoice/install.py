import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields


CUSTOM_FIELDS = {
    "Purchase Invoice": [
        {
            "fieldname": "einvoice_section",
            "label": "Hóa đơn điện tử",
            "fieldtype": "Section Break",
            "insert_after": "terms",
            "collapsible": 1,
        },
        {
            "fieldname": "einvoice_inward",
            "label": "HĐ mua vào (Staging)",
            "fieldtype": "Link",
            "options": "EInvoice Inward",
            "insert_after": "einvoice_section",
            "read_only": 1,
        },
        {
            "fieldname": "einvoice_lookup_code",
            "label": "Mã tra cứu",
            "fieldtype": "Data",
            "insert_after": "einvoice_inward",
            "read_only": 1,
        },
    ],
    "Sales Invoice": [
        {
            "fieldname": "einvoice_section",
            "label": "Hóa đơn điện tử",
            "fieldtype": "Section Break",
            "insert_after": "terms",
            "collapsible": 1,
        },
        {
            "fieldname": "einvoice_issued",
            "label": "Đã xuất HĐ đỏ",
            "fieldtype": "Check",
            "insert_after": "einvoice_section",
            "read_only": 1,
            "default": "0",
            "in_list_view": 1,
            "in_standard_filter": 1,
        },
        {
            "fieldname": "einvoice_col1",
            "fieldtype": "Column Break",
            "insert_after": "einvoice_issued",
        },
        {
            "fieldname": "einvoice_provider",
            "label": "Nhà cung cấp HĐĐT",
            "fieldtype": "Link",
            "options": "EInvoice Provider",
            "insert_after": "einvoice_col1",
            "read_only": 1,
        },
        {
            "fieldname": "einvoice_sb2",
            "fieldtype": "Section Break",
            "insert_after": "einvoice_provider",
        },
        {
            "fieldname": "einvoice_number",
            "label": "Số HĐ đỏ",
            "fieldtype": "Data",
            "insert_after": "einvoice_sb2",
            "read_only": 1,
        },
        {
            "fieldname": "einvoice_lookup_code",
            "label": "Mã tra cứu",
            "fieldtype": "Data",
            "insert_after": "einvoice_number",
            "read_only": 1,
        },
        {
            "fieldname": "einvoice_col2",
            "fieldtype": "Column Break",
            "insert_after": "einvoice_lookup_code",
        },
        {
            "fieldname": "einvoice_pdf_url",
            "label": "Link PDF HĐ đỏ",
            "fieldtype": "Data",
            "insert_after": "einvoice_col2",
            "length": 1000,
            "read_only": 1,
            "options": "URL",
        },
        {
            "fieldname": "einvoice_issued_at",
            "label": "Thời điểm xuất",
            "fieldtype": "Datetime",
            "insert_after": "einvoice_pdf_url",
            "read_only": 1,
        },
    ],
}


# --------------------------------------------------------------------------
# Number Card Definitions
# --------------------------------------------------------------------------
NUMBER_CARDS = [
    {
        "name": "EInvoice - HĐ mua vào chưa ghép",
        "label": "HĐ mua vào - Chưa ghép",
        "document_type": "EInvoice Inward",
        "function": "Count",
        "aggregate_function_based_on": "",
        "filters_json": '[["EInvoice Inward","status","=","New"]]',
        "color": "#FF6F61",
        "show_percentage_stats": 0,
        "is_standard": 1,
        "module": "EInvoice",
    },
    {
        "name": "EInvoice - HĐ mua vào đã ghép",
        "label": "HĐ mua vào - Đã ghép",
        "document_type": "EInvoice Inward",
        "function": "Count",
        "aggregate_function_based_on": "",
        "filters_json": '[["EInvoice Inward","status","in",["Matched","PI Created"]]]',
        "color": "#28a745",
        "show_percentage_stats": 0,
        "is_standard": 1,
        "module": "EInvoice",
    },
    {
        "name": "EInvoice - SI chưa xuất HĐ đỏ",
        "label": "SI chưa xuất HĐ đỏ",
        "document_type": "Sales Invoice",
        "function": "Count",
        "aggregate_function_based_on": "",
        "filters_json": '[["Sales Invoice","docstatus","=","1"],["Sales Invoice","einvoice_issued","=","0"]]',
        "color": "#e74c3c",
        "show_percentage_stats": 0,
        "is_standard": 1,
        "module": "EInvoice",
    },
    {
        "name": "EInvoice - SI đã xuất HĐ đỏ",
        "label": "SI đã xuất HĐ đỏ",
        "document_type": "Sales Invoice",
        "function": "Count",
        "aggregate_function_based_on": "",
        "filters_json": '[["Sales Invoice","docstatus","=","1"],["Sales Invoice","einvoice_issued","=","1"]]',
        "color": "#3498db",
        "show_percentage_stats": 0,
        "is_standard": 1,
        "module": "EInvoice",
    },
]


# --------------------------------------------------------------------------
# Default Matbao Provider (Demo / Sandbox)
# --------------------------------------------------------------------------
MATBAO_PROVIDER = {
    "doctype": "EInvoice Provider",
    "provider_name": "Mắt Bão",
    "provider_type": "Matbao",
    "enabled": 1,
    "tax_code": "0302712571-999",
    "api_url": "https://demo-api-hddt.matbao.in:11443",
    "api_url_purchase": "https://demo-api-hoadondauvao.matbao.in",
    "auth_method": "Username-Password",
    "api_username": "admin",
    "api_password": "Gtybf@12sd",
    "api_token": "86bdf9d3-48ff-46d1-91f3-0756965aa3a2",
    "default_invoice_pattern": "1",
    "default_invoice_serial": "C26TCL",
    "connection_status": "Not Tested",
}


def after_install():
    """Create custom fields, Number Cards, and seed default Matbao provider."""
    create_custom_fields(CUSTOM_FIELDS, update=True)
    _create_number_cards()
    _seed_matbao_provider()
    frappe.db.commit()


def _create_number_cards():
    """Create Number Card documents for the workspace dashboard."""
    for card_def in NUMBER_CARDS:
        if not frappe.db.exists("Number Card", card_def["name"]):
            doc = frappe.new_doc("Number Card")
            doc.update(card_def)
            doc.insert(ignore_permissions=True)
            frappe.logger().info(f"EInvoice: Created Number Card '{card_def['name']}'")


def _seed_matbao_provider():
    """Create default Mắt Bão provider with demo credentials."""
    provider_name = MATBAO_PROVIDER["provider_name"]
    if frappe.db.exists("EInvoice Provider", provider_name):
        frappe.logger().info(f"EInvoice: Provider '{provider_name}' already exists, skipping.")
        return

    # Get the first company
    company = frappe.db.get_value("Company", filters={}, fieldname="name", order_by="creation asc")
    if not company:
        frappe.logger().warning("EInvoice: No company found, skipping provider seed.")
        return

    doc = frappe.new_doc("EInvoice Provider")
    doc.update(MATBAO_PROVIDER)
    doc.company = company
    doc.insert(ignore_permissions=True)
    frappe.logger().info(f"EInvoice: Created provider '{provider_name}' for company '{company}'")

    # Set as default in Settings
    settings_name = "EInvoice Settings"
    if frappe.db.exists("DocType", settings_name):
        settings = frappe.get_doc(settings_name)
        if not settings.default_provider:
            settings.default_provider = provider_name
            settings.save(ignore_permissions=True)
            frappe.logger().info(f"EInvoice: Set default provider to '{provider_name}'")


def after_uninstall():
    """Remove custom fields and Number Cards added by this app."""
    for doctype, fields in CUSTOM_FIELDS.items():
        for field in fields:
            fieldname = field.get("fieldname")
            if frappe.db.exists("Custom Field", {"dt": doctype, "fieldname": fieldname}):
                frappe.delete_doc("Custom Field", f"{doctype}-{fieldname}", force=True)

    for card_def in NUMBER_CARDS:
        if frappe.db.exists("Number Card", card_def["name"]):
            frappe.delete_doc("Number Card", card_def["name"], force=True)

    frappe.db.commit()
