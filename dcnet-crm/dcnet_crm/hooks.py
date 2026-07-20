app_name = "dcnet_crm"
app_title = "DCNET CRM"
app_publisher = "DCNET"
app_description = "CRM workspace extending standard ERPNext CRM"
app_email = "admin@dcnet.vn"
app_license = "MIT"

required_apps = ["frappe", "erpnext"]

add_to_apps_screen = [
    {
        "name": "dcnet_crm",
        "logo": "/assets/dcnet_crm/images/crm.svg",
        "title": "CRM",
        "route": "/app/dcnet-crm",
        "has_permission": "dcnet_crm.api.can_access_crm",
    }
]

page_js = {
    "dcnet-crm": "public/dist/crm.bundle.js",
}

doc_events = {
    "Sales Order": {
        "on_submit": "dcnet_crm.sales_order_events.on_submit",
        "on_cancel": "dcnet_crm.sales_order_events.on_cancel",
    },
}

after_install = "dcnet_crm.install.after_install"
after_migrate = "dcnet_crm.install.after_migrate"
