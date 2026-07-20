app_name = "dcnet_pakd"
app_title = "DCNET PAKD"
app_publisher = "DCNET"
app_description = "DCNET PAKD - Sales commission worksheet (Phuong An Kinh Doanh)"
app_email = "dev@dcnet.vn"
app_license = "mit"

required_apps = ["frappe", "erpnext", "dcnet_contract", "hrms"]

after_install = "dcnet_pakd.install.after_install"
after_migrate = "dcnet_pakd.install.after_migrate"

extend_bootinfo = "dcnet_pakd.dcnet_pakd.boot.boot_session"

fixtures = [
    {"dt": "Workspace", "filters": [["module", "=", "DCNET PAKD"]]},
    {"dt": "Report", "filters": [["module", "=", "DCNET PAKD"]]},
    {"dt": "Print Format", "filters": [["module", "=", "DCNET PAKD"]]},
]

# vn_help integration — register PAKD section + doctype mapping
vn_help_sources = {
    "sidebar_items": {
        "PAKD": "Phuong An Kinh Doanh",
        "Phương án kinh doanh": "Phuong An Kinh Doanh",
    },
    "doctype_mapping": {
        "Phuong An Kinh Doanh": {
            "section": "PAKD",
            "title": "Phương án kinh doanh",
            "content_dir": "help/pakd",
            "default_article": "index",
        },
        "PAKD Settings": {
            "section": "PAKD",
            "title": "Cài đặt PAKD",
            "content_dir": "help/pakd",
            "default_article": "hoa-hong",
        },
        "PAKD Reminder Log": {
            "section": "PAKD",
            "title": "Lịch sử nhắc duyệt",
            "content_dir": "help/pakd",
            "default_article": "quy-trinh-duyet",
        },
    },
    "report_mapping": {
        "Pending PAKD Aging": {
            "section": "PAKD",
            "title": "PAKD chờ xử lý",
            "content_dir": "help/pakd",
            "default_article": "quy-trinh-duyet",
        },
        "Commission Register": {
            "section": "PAKD",
            "title": "Sổ chi tiết hoa hồng",
            "content_dir": "help/pakd",
            "default_article": "hoa-hong",
        },
    },
}

doc_events = {
	"Payment Entry": {
		"on_submit": "dcnet_pakd.dcnet_pakd.events.on_payment_entry_submit",
		"on_cancel": "dcnet_pakd.dcnet_pakd.events.on_payment_entry_cancel",
	},
	"DCNET Contract": {
		"on_cancel": "dcnet_pakd.dcnet_pakd.events.on_contract_cancel",
	},
	"Phuong An Kinh Doanh": {
		"on_update": "dcnet_pakd.dcnet_pakd.events.on_pakd_update",
	},
}

# Cash Flow Forecast provider
cash_flow_forecast_providers = [
    "dcnet_pakd.forecast.get_pakd_forecast"
]

# Auto Generated Doc Registry (vn_accounting) — 2 source_keys cho proportional
# auto-post từ PE button "Tạo draft hoa hồng PAKD".
auto_generated_doc_sources = {
    "dcnet_pakd.pe_proportional_commission": {
        "label": "Hoa hồng + License Fee + MS + AC theo tỷ lệ thanh toán",
        "doctype": "Journal Entry",
        "needs_approval": True,
        "action_draft": "Duyệt và ghi sổ",
        "description": "Hệ thống tự sinh khi KTT click 'Tạo draft hoa hồng PAKD' trên Phiếu thu/chi đã link PAKD. Tỷ lệ = PE.paid_amount / PAKD.total_revenue_contract. Mỗi commission_line Pending sinh 1 draft JE incremental × tỷ lệ.",
    },
    "dcnet_pakd.pe_proportional_beneficiary": {
        "label": "Chi cho người nhận MS/AC/Referral theo tỷ lệ thanh toán",
        "doctype": "Journal Entry",
        "needs_approval": True,
        "action_draft": "Duyệt và ghi sổ",
        "description": "Hệ thống tự sinh khi KTT click 'Tạo draft hoa hồng PAKD'. Mỗi beneficiary_line Pending có recipient sinh 1 draft JE 2/3-leg (TNCN khấu trừ nếu có) × tỷ lệ.",
    },
}

# PE form button "Tạo draft hoa hồng PAKD" — hiện khi PE.linked_pakd + docstatus=1.
doctype_js = {
    "Payment Entry": "public/js/payment_entry_pakd_button.js",
}
