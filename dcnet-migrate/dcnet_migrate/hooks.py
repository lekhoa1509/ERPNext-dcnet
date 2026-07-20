app_name = "dcnet_migrate"
app_title = "DCNET Migrate"
app_publisher = "DCNET"
app_description = "Data migration tooling for ERPNext v16"
app_email = "dev@dcnet.vn"
app_license = "MIT"

required_apps = ["frappe", "erpnext"]

after_install = "dcnet_migrate.install.after_install"
after_migrate = "dcnet_migrate.install.after_migrate"

# Workspace sidebars are loaded from this app's workspace_sidebar/ folder
# by dcnet_apps.install.sync_workspace_sidebars() at migrate time.

fixtures = []

# Inject worker-notification panel into Frappe's standard notification bell
app_include_js = ["assets/dcnet_migrate/js/worker_notification.js"]
app_include_css = ["assets/dcnet_migrate/css/worker_notification.css"]
