app_name = "dcnet_hrm"
app_title = "DCNET HRM"
app_publisher = "DCNET"
app_description = "Vietnamese HR & Payroll compliance layer on top of Frappe HR"
app_email = "dev@dcnet.vn"
app_license = "mit"

required_apps = ["frappe", "erpnext", "hrms"]

after_install = "dcnet_hrm.install.after_install"
after_migrate = "dcnet_hrm.install.after_migrate"

# Frappe reads translations from {app}/translations/{lang}.csv automatically —
# labels/messages below are written in English, dcnet_hrm/translations/vi.csv
# carries the Vietnamese strings. Switching User/System Settings language flips
# the UI without any custom switcher.

fixtures = [
    {"doctype": "Custom Field", "filters": [["module", "=", "DCNet HRM"]]},
    {"doctype": "Property Setter", "filters": [["module", "=", "DCNet HRM"]]},
]

# === PAYROLL ===
doc_events = {
    "Salary Slip": {
        "validate": "dcnet_hrm.payroll.vn_payroll.calculate",
    },
}

# === SCHEDULER EVENTS ===
scheduler_events = {
    "daily": [
        "dcnet_hrm.dcnet_hrm.doctype.labor_contract.labor_contract.run_daily_expiry_check",
    ],
}
