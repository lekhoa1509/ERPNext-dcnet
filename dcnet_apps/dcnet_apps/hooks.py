app_name = "dcnet_apps"
app_title = "DCNET Apps"
app_publisher = "DCNET Cloud"
app_description = """Custom Business Modules for DCNET Flow - Fitting, Lead Management, Coaching, and more"""
app_icon = "fa fa-puzzle-piece"
app_color = "#0080ff"
app_email = "info@dcnet.cloud"
app_license = "Proprietary"
source_link = "https://github.com/dcnet-cloud/flow_next"
app_logo_url = "/assets/dcnet_apps/images/dcnet-logo.png"
app_home = "/app/home"

develop_version = "1.4.1"

# Boot Session
# ------------
boot_session = "dcnet_apps.boot.boot_session"

# add de ko xay ra loi
add_to_apps_screen = [
    {
        "name": "DCNET",
        "icon": "octicon octicon-rocket",
        "label": "DCNET",
        "route": "/app",
    }
]

# Website Branding
# ------------------
website_context = {
    "favicon": "/assets/dcnet_apps/images/favicon.png",
    "splash_image": "/assets/dcnet_apps/images/dcnet-logo.png",
}

# Fixtures (Update Custom Field)
# --------
fixtures = [
    {
        "doctype": "Custom Field",
        "filters": [
            [
                "dt",
                "in",
                [
                    "Lead",
                    "Sales Order",
                    "Sales Order Item",
                    "Sales Invoice",
                    "Opportunity",
                    "Quotation",
                    "Customer",
                    "Warehouse",
                    "Stock Reconciliation",
                    "Stock Reconciliation Item",
                    "Item",
                    "Batch",
                    "Workspace Sidebar Item"
                ],
            ]
        ],
    },
    {
        "doctype": "Property Setter",
        "filters": [
            [
                "doc_type",
                "in",
                [
                    "Lead",
                    "Opportunity",
                    "Quotation",
                    "Customer",
                    "Warehouse",
                    "Stock Reconciliation",
                    "Stock Reconciliation Item",
                    "Purchase Order",
                    "Item",
                    "Workspace Sidebar Item"
                ],
            ]
        ],
    },
    {
        "doctype": "Client Script",
        "filters": [["dt", "in", ["Lead", "Batch", "Purchase Receipt", "Data Import", "Customer"]]],
    },
    {
        "doctype": "Workspace",
        "filters": [["module", "in", ["EInvoice", "DCNET Report", "htkk"]]],
    },
    {
        "doctype": "Report",
        "filters": [["name", "in", ["DCNET Sales Order Trends"]]]
    },
    {
        "doctype": "Report",
        "filters": [["name", "in", ["Sales Order Trends"]]]
    },
    {
        "doctype": "Dashboard Chart",
        "filters": [
            ["name", "=", "Sales Order Trends"]
        ]
    }
]
# Includes in <head>
# ------------------
# include js, css files in header of desk.html
app_include_css = [
    f"/assets/dcnet_apps/css/dcnet_theme.css?v={develop_version}",
    f"/assets/dcnet_apps/css/item_image.css?v={develop_version}",
    f"/assets/dcnet_apps/css/workflow_diagram.css?v={develop_version}",
    f"/assets/dcnet_apps/css/purchase_order_workflow.css?v={develop_version}",
]
app_include_js = [
    f"/assets/dcnet_apps/js/menu_override.js?v={develop_version}",
    f"/assets/dcnet_apps/js/notification_badge.js?v={develop_version}",
    f"/assets/dcnet_apps/js/workflow_auto_render.js?v={develop_version}",
    f"/assets/dcnet_apps/js/sidebar_preserve.js?v={develop_version}",
    f"/assets/dcnet_apps/js/sidebar_override.js?v={develop_version}",
    f"/assets/dcnet_apps/js/htkk_workspace.js?v={develop_version}",
]
# include js, css files in header of desk.html
# app_include_js = "/assets/dcnet_apps/js/dcnet_apps.js"
# app_include_css = "/assets/dcnet_apps/css/dcnet_apps.css"

# include js, css files in header of web template
# web_include_css = "/assets/dcnet_apps/css/dcnet_apps.css"
# web_include_js = "/assets/dcnet_apps/js/dcnet_apps.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "dcnet_apps/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {
    "Item": [
        "public/js/item_barcode.js",
        "dcnet_image_management/doctype/item_image/item_image.js",
    ],
    "Sales Order": ["public/js/safety_stock_alert.js", "sales_order/sales_order.js"],
    "Sales Invoice": [
        "einvoice/public/js/sales_invoice.js",
        "sales_invoice/sales_invoice_custom.js",
        "sales_invoice/sales_invoice_view_warranty_status.js"
    ],
    "EInvoice Provider": "einvoice/public/js/einvoice_provider.js",
}
doctype_list_js = {
    "Barcode Label": "barcode_management/doctype/barcode_label/barcode_label_list.js",
    "Sales Invoice": "einvoice/public/js/sales_invoice_list.js"
}
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "dcnet_apps/public/icons.svg"

# Home Pages
# ----------

# Redirect "/" to Desk
website_redirects = [
    {"source": "/", "target": "/app"},
]

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "dcnet_apps.utils.jinja_methods",
# 	"filters": "dcnet_apps.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "dcnet_apps.install.before_install"
after_install = "dcnet_apps.install.after_install"
before_migrate = "dcnet_apps.install.before_migrate"
after_migrate = "dcnet_apps.install.after_migrate"

# Translations
# ------------
# Make translations available for all apps (override CRM translations)
# Frappe reads from {app}/translations/{lang}.csv automatically

# Uninstallation
# ------------

# before_uninstall = "dcnet_apps.uninstall.before_uninstall"
# after_uninstall = "dcnet_apps.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "dcnet_apps.utils.before_app_install"
# after_app_install = "dcnet_apps.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "dcnet_apps.utils.before_app_uninstall"
# after_app_uninstall = "dcnet_apps.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "dcnet_apps.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
#     "Lead": {
#         "on_update": "dcnet_apps.crm.lead_handler.on_update"
#     }
# }
doc_events = {
    "Lead": {
        "validate": [
            "dcnet_apps.crm.lead.lead_validation.validate_lead_duplicate",
            "dcnet_apps.utils.custom_dob_validation.validate_custom_dob",
        ]
    },
    "Data Import": {
        "validate": "dcnet_apps.utils.data_import_validation.validate_import_row_limit"
    },
    "Customer": {
        "validate": "dcnet_apps.utils.custom_dob_validation.validate_custom_dob",
        "after_insert": "dcnet_apps.crm.lead.lead_to_customer.after_customer_created_from_lead",
    },
    "Sales Order": {
        "on_submit": "dcnet_apps.stock.safety_stock_check.check_safety_stock_on_sales_order"
    },
    "Purchase Receipt": {
        "on_submit": "dcnet_apps.purchase_order.purchase_order_workflow.update_po_from_receipt"
    },

    "Purchase Invoice": {
        "on_submit": "dcnet_apps.purchase_order.purchase_order_workflow.update_po_from_invoice"
    },
    "Notification Log": {
        "after_insert": "dcnet_apps.mobile_push.events.notification_log.send_push_for_notification"
    },
    "ToDo": {
        "after_insert": "dcnet_apps.mobile_push.events.notification_log.send_push_for_todo"
    },
}

# Scheduled Tasks
# ---------------

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
        "dcnet_apps.utils.tasks.stock_expiry_notifications.send_low_stock_summary_notification",
        "dcnet_apps.utils.tasks.stock_expiry_notifications.send_item_expiry_summary_notification",
    ],
    "weekly": [
        "dcnet_apps.einvoice.tasks.sync_inward_invoices.run_if_frequency_match",
    ],
}

# Testing
# -------

# before_tests = "dcnet_apps.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "dcnet_apps.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "dcnet_apps.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["dcnet_apps.utils.before_request"]
# after_request = ["dcnet_apps.utils.after_request"]

# Job Events
# ----------
# before_job = ["dcnet_apps.utils.before_job"]
# after_job = ["dcnet_apps.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"dcnet_apps.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }
