app_name = "dcnet_theme"
app_title = "DCNET Theme"
app_publisher = "DCNET"
app_description = "DCNET Theme — ERPNext Desk theming + context-primary workspace sidebar router"
app_version = "0.3.3"

# Install / migrate hooks
after_install = "dcnet_theme.dcnet_theme.install.after_install"
after_migrate = "dcnet_theme.dcnet_theme.install.after_migrate"

# DCNET Theme boot session hook
boot_session = "dcnet_theme.dcnet_theme.boot.boot_session"

doctype_js = {
    "Desktop Icon": "dcnet_theme/public/js/desktop_icon_form.js",
}

fixtures = [
    {"dt": "Property Setter", "filters": [["doc_type", "=", "Desktop Icon"]]},
    {"dt": "Custom Field", "filters": [["dt", "=", "Desktop Icon"]]},
]

# CSS/JS includes
app_include_css = [
    f"/assets/dcnet_theme/css/dcnet_theme.css?version={app_version}",
    f"/assets/dcnet_theme/css/quick_detail_frame.css?version={app_version}",
]
app_include_js = [
    "/assets/dcnet_theme/js/theme_applicator.js",
    "/assets/dcnet_theme/js/desktop_icon_override.js",
    "query_report_fix.bundle.js",
    "datatable_selection_summary.bundle.js",
    "sidebar.bundle.js",
    "quick_detail_frame.bundle.js",
]
