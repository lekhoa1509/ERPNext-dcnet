app_name = "vn_banking"
app_title = "VN Banking"
app_publisher = "DCNET"
app_description = "Vietnamese bank statement import and auto-match"
app_email = "dev@dcnet.vn"
app_license = "MIT"

after_install = "vn_banking.install.after_install"
after_migrate = "vn_banking.install.after_migrate"

app_include_js = ["bank_reconcile.bundle.js"]
app_include_css = ["bank_reconcile.bundle.css"]

fixtures = [
    {"dt": "Bank Statement Format"},
    {"dt": "Bank Matcher Type"},
    {"dt": "Bank Data Source"},
    {"dt": "Custom Field", "filters": [["name", "like", "Bank Transaction-%"]]},
    {"dt": "Custom Field", "filters": [["name", "like", "Bank Account-%"]]},
]

# v2 scaffold — uncomment when API sources implemented
# scheduler_events = {
#     "hourly": ["vn_banking.tasks.sync_all_api_banks"],
# }
