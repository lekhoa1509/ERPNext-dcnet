app_name = "dcnet_contract"
app_title = "DCNET Contract"
app_publisher = "DCNET"
app_description = "DCNET Contract management - recurring + one-off, billing schedule, cash flow"
app_email = "dev@dcnet.vn"
app_license = "mit"

required_apps = ["frappe", "erpnext"]

after_install = "dcnet_contract.install.after_install"
after_migrate = "dcnet_contract.install.after_migrate"

fixtures = [
    {
        "doctype": "Custom Field",
        "filters": [["module", "=", "DCNet Contract"]],
    },
]

# vn_help integration — register Contract section + doctype mapping
vn_help_sources = {
    "sidebar_items": {
        "Hợp đồng": "DCNet Contract",
    },
    "doctype_mapping": {
        "DCNet Contract": {
            "section": "Hợp đồng",
            "title": "Hợp đồng",
            "content_dir": "help/hop-dong",
            "default_article": "index",
        },
        "DCNet Contract Template": {
            "section": "Hợp đồng",
            "title": "Mẫu hợp đồng",
            "content_dir": "help/hop-dong",
            "default_article": "mau-hop-dong",
        },
    },
    "report_mapping": {
        "Contract Expiry Report": {
            "section": "Hợp đồng",
            "title": "Hợp đồng sắp hết hạn",
            "content_dir": "help/hop-dong",
            "default_article": "index",
        },
        "Overdue Billing Periods": {
            "section": "Hợp đồng",
            "title": "Kỳ thu tiền quá hạn",
            "content_dir": "help/hop-dong",
            "default_article": "lich-thu-tien",
        },
        "Outstanding Receivables by Contract": {
            "section": "Hợp đồng",
            "title": "Công nợ theo hợp đồng",
            "content_dir": "help/hop-dong",
            "default_article": "lich-thu-tien",
        },
    },
}

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
    "Sales Invoice": {
        "before_save": "dcnet_contract.dcnet_contract.events.si_autofill_contract",
    },
    "Payment Entry": {
        "before_save": "dcnet_contract.dcnet_contract.events.pe_autofill_contract",
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
