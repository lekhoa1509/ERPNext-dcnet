app_name = "dcnet_contract"
app_title = "DCNet Contract"
app_publisher = "DCNet"
app_description = "DCNet Contract management - recurring + one-off, billing schedule, cash flow"
app_email = "dev@dcnet.vn"
app_license = "mit"

required_apps = ["frappe", "erpnext"]

after_install = "dcnet_contract.install.after_install"
after_migrate = "dcnet_contract.install.after_migrate"

fixtures = []

# Scheduler
scheduler_events = {
    "daily": [
        "dcnet_contract.dcnet_contract.tasks.run_auto_invoice",
        "dcnet_contract.dcnet_contract.tasks.run_overdue_check",
        "dcnet_contract.dcnet_contract.tasks.run_expire_contracts",
    ],
}

# Document Events
doc_events = {
    "Payment Entry": {
        "on_submit": "dcnet_contract.dcnet_contract.events.on_payment_entry_submit",
        "on_cancel": "dcnet_contract.dcnet_contract.events.on_payment_entry_cancel",
    },
}

# Permission Query Conditions — hide shadow SOs from non-admin
permission_query_conditions = {
    "Sales Order": "dcnet_contract.dcnet_contract.permissions.so_permission_query",
}

# Cash Flow Forecast provider
cash_flow_forecast_providers = [
    "dcnet_contract.forecast.get_contract_forecast"
]
