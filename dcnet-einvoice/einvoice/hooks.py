app_name = "einvoice"
app_title = "EInvoice"
app_publisher = "DCNET"
app_description = "Multi-provider E-Invoice Integration for ERPNext v16"
app_email = "info@dcnet.vn"
app_license = "MIT"
required_apps = ["frappe", "erpnext"]

add_to_apps_screen = [
    {
        "name": "einvoice",
        "logo": "/assets/einvoice/images/logo.png",
        "title": "Hóa đơn điện tử",
        "route": "/app/einvoice-settings",
        "has_permission": "einvoice.einvoice.api.has_app_permission",
    }
]

doctype_js = {
    "Sales Invoice": "public/js/sales_invoice.js",
    "EInvoice Provider": "public/js/einvoice_provider.js",
    "EInvoice Inward": "public/js/einvoice_inward.js",
}

doctype_list_js = {
    "Sales Invoice": "public/js/sales_invoice_list.js",
    "EInvoice Inward": "public/js/einvoice_inward_list.js",
    "EInvoice Provider": "public/js/einvoice_provider_list.js",
}

# NOTE: Frappe registers ONE Scheduled Job Type per method (sync_jobs dedupes by
# `method` and overwrites its frequency with whichever bucket is processed last).
# Declaring the same method under cron+hourly+daily+weekly therefore collapses to
# the LAST bucket (weekly) — the job ends up firing only once a week, not every
# 15 min. So sync_inward is registered under the */15 cron ONLY; the actual cadence
# is self-gated inside run_if_frequency_match via EInvoice Settings.sync_frequency.
scheduler_events = {
    "cron": {
        "*/15 * * * *": [
            "einvoice.einvoice.tasks.sync_inward_invoices.run_if_frequency_match",
        ],
    },
    "daily": [
        "einvoice.einvoice.tasks.retry_failed_attachments.retry_failed_attachments",
    ],
}

after_install = "einvoice.einvoice.install.after_install"
after_migrate = "einvoice.einvoice.install.after_migrate"
after_uninstall = "einvoice.einvoice.install.after_uninstall"

fixtures = [
    {
        "dt": "Workspace",
        "filters": [["module", "=", "EInvoice"]],
    },
]
