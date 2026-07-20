app_name = "dcnet_apps.einvoice"
app_title = "EInvoice"
app_publisher = "DCNet"
app_description = "Multi-provider E-Invoice Integration for ERPNext v16"
app_email = "info@dcnet.vn"
app_license = "MIT"
required_apps = ["frappe", "erpnext"]

# --------------------------------------------------------------------------
# App UI
# --------------------------------------------------------------------------
add_to_apps_screen = [
    {
        "name": "dcnet_apps.einvoice",
        "logo": "/assets/dcnet_apps/images/logo.png",
        "title": "Hóa đơn điện tử",
        "route": "/app/einvoice-settings",
        "has_permission": "dcnet_apps.einvoice.api.has_app_permission",
    }
]

# --------------------------------------------------------------------------
# DocType JS overrides
# --------------------------------------------------------------------------
doctype_js = {
    "Sales Invoice": "public/js/sales_invoice.js",
    "EInvoice Provider": "public/js/einvoice_provider.js",
}

doctype_list_js = {
    "Sales Invoice": "public/js/sales_invoice_list.js",
}

# --------------------------------------------------------------------------
# Custom Fields — installed on setup
# --------------------------------------------------------------------------
# Defined via fixtures or install hooks; see dcnet_apps.einvoice/install.py

# --------------------------------------------------------------------------
# Scheduler Events
# --------------------------------------------------------------------------
scheduler_events = {
    "cron": {
        "*/15 * * * *": [
            "dcnet_apps.einvoice.tasks.sync_inward_invoices.run_if_frequency_match",
        ],
    },
    "hourly": [
        "dcnet_apps.einvoice.tasks.sync_inward_invoices.run_if_frequency_match",
    ],
    "daily": [
        "dcnet_apps.einvoice.tasks.sync_inward_invoices.run_if_frequency_match",
    ],
    "weekly": [
        "dcnet_apps.einvoice.tasks.sync_inward_invoices.run_if_frequency_match",
    ],
}

# --------------------------------------------------------------------------
# Installation
# --------------------------------------------------------------------------
after_install = "dcnet_apps.einvoice.install.after_install"
after_uninstall = "dcnet_apps.einvoice.install.after_uninstall"

# --------------------------------------------------------------------------
# Fixtures (export workspace)
# --------------------------------------------------------------------------
fixtures = [
    {
        "dt": "Workspace",
        "filters": [["module", "=", "EInvoice"]],
    },
]
