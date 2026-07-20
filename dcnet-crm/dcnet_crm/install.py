import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields


CRM_PAGE_ROLES = ("Sales Manager", "Sales User", "System Manager")
OPPORTUNITY_CUSTOM_FIELDS = {
    "Opportunity": [
        {
            "fieldname": "custom_auto_increase_duplicate_qty",
            "label": "Tự động tăng SL khi chọn trùng",
            "fieldtype": "Check",
            "insert_after": "items",
            "default": "0",
        },
        {
            "fieldname": "custom_shipping_country",
            "label": "Quốc gia (Giao hàng)",
            "fieldtype": "Link",
            "options": "Country",
            "insert_after": "notes",
            "default": "Vietnam",
        },
        {
            "fieldname": "custom_shipping_state",
            "label": "Tỉnh/Thành phố (Giao hàng)",
            "fieldtype": "Data",
            "insert_after": "custom_shipping_country",
        },
        {
            "fieldname": "custom_shipping_county",
            "label": "Quận/Huyện (Giao hàng)",
            "fieldtype": "Data",
            "insert_after": "custom_shipping_state",
        },
        {
            "fieldname": "custom_shipping_ward",
            "label": "Phường/Xã (Giao hàng)",
            "fieldtype": "Data",
            "insert_after": "custom_shipping_county",
        },
        {
            "fieldname": "custom_shipping_address_line1",
            "label": "Số nhà, Đường phố (Giao hàng)",
            "fieldtype": "Data",
            "insert_after": "custom_shipping_ward",
        },
        {
            "fieldname": "custom_shipping_pincode",
            "label": "Mã vùng (Giao hàng)",
            "fieldtype": "Data",
            "insert_after": "custom_shipping_address_line1",
        },
        {
            "fieldname": "custom_shipping_address",
            "label": "Địa chỉ (Giao hàng)",
            "fieldtype": "Small Text",
            "insert_after": "custom_shipping_pincode",
        },
        {
            "fieldname": "custom_is_shared",
            "label": "Dùng chung",
            "fieldtype": "Check",
            "insert_after": "custom_shipping_address",
            "default": "0",
        },
        {
            "fieldname": "custom_opportunity_code",
            "label": "Mã cơ hội",
            "fieldtype": "Data",
            "insert_after": "custom_is_shared",
            "read_only": 1,
            "no_copy": 1,
        },
        {
            "fieldname": "custom_referral_partner",
            "label": "Đối tác/CTV giới thiệu",
            "fieldtype": "Link",
            "options": "Customer",
            "insert_after": "custom_opportunity_code",
        },
        {
            "fieldname": "custom_item_category",
            "label": "Loại hàng hóa",
            "fieldtype": "Link",
            "options": "Item Group",
            "insert_after": "custom_referral_partner",
        },
        {
            "fieldname": "custom_branch",
            "label": "Đơn vị",
            "fieldtype": "Link",
            "options": "Branch",
            "insert_after": "custom_item_category",
        },
        {
            "fieldname": "custom_sales_process",
            "label": "Quy trình bán hàng",
            "fieldtype": "Data",
            "insert_after": "custom_branch",
        },
        {
            "fieldname": "custom_related_person",
            "label": "Người liên quan",
            "fieldtype": "Small Text",
            "insert_after": "custom_sales_process",
        },
        {
            "fieldname": "custom_result_other_reason",
            "label": "Lý do khác",
            "fieldtype": "Small Text",
            "insert_after": "lost_reasons",
        },
    ],
    "Opportunity Item": [
        {
            "fieldname": "custom_installation_point_a_end",
            "label": "Điểm lắp đặt A-End",
            "fieldtype": "Data",
            "insert_after": "description",
        },
        {
            "fieldname": "custom_installation_point_z_end",
            "label": "Điểm lắp đặt Z-End",
            "fieldtype": "Data",
            "insert_after": "custom_installation_point_a_end",
        },
        {
            "fieldname": "custom_discount_percentage",
            "label": "Tỷ lệ chiết khấu",
            "fieldtype": "Float",
            "insert_after": "amount",
            "default": "0",
        },
        {
            "fieldname": "custom_discount_amount",
            "label": "Tiền chiết khấu",
            "fieldtype": "Currency",
            "insert_after": "custom_discount_percentage",
            "default": "0",
            "read_only": 1,
        },
        {
            "fieldname": "custom_net_rate",
            "label": "Đơn giá sau CK",
            "fieldtype": "Currency",
            "insert_after": "custom_discount_amount",
            "default": "0",
            "read_only": 1,
        },
        {
            "fieldname": "custom_net_amount",
            "label": "Thành tiền sau CK",
            "fieldtype": "Currency",
            "insert_after": "custom_net_rate",
            "default": "0",
            "read_only": 1,
        },
    ],
}

# Reuses ERPNext's stock "Opportunity Lost Reason" master (+ its Table MultiSelect
# child "Opportunity Lost Reason Detail") for BOTH Won and Lost closing reasons,
# distinguished by this custom Select field, instead of introducing new DocTypes.
OPPORTUNITY_LOST_REASON_CUSTOM_FIELDS = {
    "Opportunity Lost Reason": [
        {
            "fieldname": "custom_reason_type",
            "label": "Loại kết quả",
            "fieldtype": "Select",
            "options": "\nThắng\nThua",
            "insert_after": "lost_reason",
            "reqd": 1,
        },
    ],
}

# ⚠️ Cần clarify với khách hàng để xác nhận danh sách lý do kết thúc thắng/thua chính thức.
OPPORTUNITY_RESULT_REASONS = (
    ("Giá cả và chính sách bán hàng tốt", "Thắng"),
    ("Dịch vụ chăm sóc khách hàng của công ty tốt", "Thắng"),
    ("Tin tưởng thương hiệu của Công ty", "Thắng"),
    ("Giá cả và chính sách bán hàng chưa tốt", "Thua"),
    ("Dịch vụ chăm sóc khách hàng của công ty chưa tốt", "Thua"),
    ("Thương hiệu công ty không có uy tín", "Thua"),
)

QUOTATION_CUSTOM_FIELDS = {
    "Quotation": [
        {
            "fieldname": "custom_approval_requested",
            "label": "Đã gửi yêu cầu duyệt",
            "fieldtype": "Check",
            "insert_after": "status",
            "default": "0",
            "no_copy": 1,
        },
    ],
}

# ERPNext's stock Warranty Claim doctype only links to Customer/Serial No/Item —
# this field lets the CRM order detail page's "Phiếu bảo hành" tab scope claims
# to the Sales Order they were raised against.
WARRANTY_CLAIM_CUSTOM_FIELDS = {
    "Warranty Claim": [
        {
            "fieldname": "custom_sales_order",
            "label": "Đơn hàng",
            "fieldtype": "Link",
            "options": "Sales Order",
            "insert_after": "customer",
        },
    ],
}

LEAD_CUSTOM_FIELDS = {
    "Lead": [
        {"fieldname": "custom_lead_type", "label": "Loại tiềm năng", "fieldtype": "Select",
         "options": "\nKH viễn thông\nKH CNTT\nKH hộ gia đình\nKH mua bán thi công\nKH mua bán",
         "insert_after": "source"},
        {"fieldname": "custom_zalo", "label": "Zalo", "fieldtype": "Data", "insert_after": "custom_lead_type"},
        {"fieldname": "custom_work_email", "label": "Email cơ quan", "fieldtype": "Data", "insert_after": "custom_zalo"},
        {"fieldname": "custom_tax_id", "label": "Mã số thuế", "fieldtype": "Data", "insert_after": "custom_work_email"},
        {"fieldname": "custom_bank_account", "label": "Tài khoản ngân hàng", "fieldtype": "Data", "insert_after": "custom_tax_id"},
        {"fieldname": "custom_bank_name", "label": "Mở tại ngân hàng", "fieldtype": "Data", "insert_after": "custom_bank_account"},
        {"fieldname": "custom_founding_date", "label": "Ngày thành lập", "fieldtype": "Date", "insert_after": "custom_bank_name"},
        {"fieldname": "custom_business_type", "label": "Loại hình", "fieldtype": "Select",
         "options": "\nDoanh nghiệp tư nhân\nCông ty TNHH\nCông ty cổ phần\nHộ kinh doanh\nCá nhân",
         "insert_after": "custom_founding_date"},
        {"fieldname": "custom_sector", "label": "Lĩnh vực", "fieldtype": "Data", "insert_after": "custom_business_type"},
        {"fieldname": "custom_district", "label": "Quận/Huyện", "fieldtype": "Data", "insert_after": "state"},
        {"fieldname": "custom_ward", "label": "Phường/Xã", "fieldtype": "Data", "insert_after": "custom_district"},
        {"fieldname": "custom_full_address", "label": "Địa chỉ", "fieldtype": "Small Text", "insert_after": "city"},
        {"fieldname": "custom_is_shared", "label": "Dùng chung", "fieldtype": "Check", "insert_after": "custom_full_address", "default": "0"},
    ]
}

TODO_CUSTOM_FIELDS = {
    "ToDo": [
        {
            "fieldname": "custom_related_users",
            "label": "Người liên quan",
            "fieldtype": "Small Text",
            "insert_after": "description",
        },
        {
            "fieldname": "custom_task_type",
            "label": "Loại nhiệm vụ",
            "fieldtype": "Data",
            "insert_after": "custom_related_users",
        },
        # Only populated for the "Đề nghị ghi doanh số" task type — lets the
        # Sales Order "Khác > Ghi nhận doanh số" tab show a real per-request
        # breakdown instead of just Ngày/Nhân viên/Tình trạng.
        {
            "fieldname": "custom_revenue_item",
            "label": "Hàng hóa",
            "fieldtype": "Link",
            "options": "Item",
            "insert_after": "custom_task_type",
        },
        {
            "fieldname": "custom_revenue_department",
            "label": "Đơn vị",
            "fieldtype": "Link",
            "options": "Department",
            "insert_after": "custom_revenue_item",
        },
        {
            "fieldname": "custom_revenue_recognized_amount",
            "label": "Doanh số ghi nhận",
            "fieldtype": "Currency",
            "insert_after": "custom_revenue_department",
        },
        {
            "fieldname": "custom_revenue_achieved_amount",
            "label": "Doanh số thực hiện được",
            "fieldtype": "Currency",
            "insert_after": "custom_revenue_recognized_amount",
        },
        {
            "fieldname": "custom_revenue_note",
            "label": "Ghi chú",
            "fieldtype": "Small Text",
            "insert_after": "custom_revenue_achieved_amount",
        },
    ]
}

# Fields the CRM Sales Order form/API read/write on line items (see api.py:
# item_optional + get_service_account_detail raw SQL). Must exist or the
# service-account / SO-item ISP flows raise "Unknown column" (1054).
SALES_ORDER_ITEM_CUSTOM_FIELDS = {
    "Sales Order Item": [
        {
            "fieldname": "custom_a_end",
            "label": "Điểm lắp đặt A-End",
            "fieldtype": "Data",
            "insert_after": "item_code",
        },
        {
            "fieldname": "custom_z_end",
            "label": "Điểm lắp đặt Z-End",
            "fieldtype": "Data",
            "insert_after": "custom_a_end",
        },
        {
            "fieldname": "custom_dcnet_account_id",
            "label": "Mã tài khoản dịch vụ",
            "fieldtype": "Data",
            "insert_after": "custom_z_end",
        },
    ]
}

# Vietnamese sales pipeline stages used by the Opportunity detail pipeline.
# Must match the labels rendered in features/opportunities/template.js.
CRM_SALES_STAGES = (
    "Kinh doanh lập yêu cầu",
    "P.TH check thông tin",
    "Thực hiện khảo sát",
    "Kinh doanh báo giá cho KH",
    "Kết thúc thắng",
    "Kết thúc thất bại",
)

# Tỷ lệ thành công (%) gán cố định theo giai đoạn, theo mẫu MISA AMIS CRM.
# ⚠️ Cần clarify với khách hàng để xác nhận % chính thức cho từng giai đoạn.
CRM_SALES_STAGE_PROBABILITY = {
    "Kinh doanh lập yêu cầu": 50,
    "P.TH check thông tin": 20,
    "Thực hiện khảo sát": 60,
    "Kinh doanh báo giá cho KH": 70,
    "Kết thúc thắng": 100,
    "Kết thúc thất bại": 0,
}

CRM_SIDEBAR_ITEMS = (
    {
        "label": "Bàn làm việc",
        "icon": "home",
        "link_type": "Page",
        "link_to": "dcnet-crm",
        "route_options": '{"view": "dashboard"}',
    },
    {
        "label": "Tiềm năng",
        "icon": "globe",
        "link_type": "Page",
        "link_to": "dcnet-crm",
        "route_options": '{"view": "leads"}',
    },
    {
        "label": "Liên hệ",
        "icon": "contact",
        "link_type": "Page",
        "link_to": "dcnet-crm",
        "route_options": '{"view": "contacts"}',
    },
    {
        "label": "Khách hàng",
        "icon": "organization",
        "link_type": "Page",
        "link_to": "dcnet-crm",
        "route_options": '{"view": "customers"}',
    },
    {
        "label": "Cơ hội",
        "icon": "briefcase",
        "link_type": "Page",
        "link_to": "dcnet-crm",
        "route_options": '{"view": "opportunities"}',
    },
    {
        "label": "Báo giá",
        "icon": "file-text",
        "link_type": "Page",
        "link_to": "dcnet-crm",
        "route_options": '{"view": "quotations"}',
    },
    {
        "label": "Đơn hàng",
        "icon": "shopping-cart",
        "link_type": "Page",
        "link_to": "dcnet-crm",
        "route_options": '{"view": "orders"}',
    },
    {
        "label": "Tài khoản",
        "icon": "layers",
        "link_type": "Page",
        "link_to": "dcnet-crm",
        "route_options": '{"view": "accounts"}',
    },
    {
        "label": "Hoạt động",
        "icon": "activity",
        "link_type": "Page",
        "link_to": "dcnet-crm",
        "route_options": '{"view": "activities"}',
    },
    {
        "label": "Thẻ chăm sóc",
        "icon": "heart",
        "link_type": "Page",
        "link_to": "dcnet-crm",
        "route_options": '{"view": "care"}',
    },
)


def after_install():
    """Apply CRM navigation permissions after installation."""
    ensure_lead_contact_auto_creation_disabled()
    ensure_opportunity_custom_fields()
    ensure_opportunity_lost_reason_custom_fields()
    ensure_opportunity_result_reasons()
    ensure_quotation_custom_fields()
    ensure_warranty_claim_custom_fields()
    ensure_lead_custom_fields()
    ensure_todo_custom_fields()
    ensure_sales_order_item_custom_fields()
    ensure_sales_stages()
    ensure_crm_detail_track_changes()
    ensure_page_roles()
    ensure_crm_sidebar()


def after_migrate():
    """Keep CRM page roles synchronized after migrations."""
    ensure_lead_contact_auto_creation_disabled()
    ensure_opportunity_custom_fields()
    ensure_opportunity_lost_reason_custom_fields()
    ensure_opportunity_result_reasons()
    ensure_quotation_custom_fields()
    ensure_warranty_claim_custom_fields()
    ensure_lead_custom_fields()
    ensure_todo_custom_fields()
    ensure_sales_order_item_custom_fields()
    ensure_sales_stages()
    ensure_crm_detail_track_changes()
    ensure_page_roles()
    ensure_crm_sidebar()


def ensure_lead_contact_auto_creation_disabled():
    """Keep Lead and Contact independent until a contact is created explicitly."""
    frappe.db.set_single_value("CRM Settings", "auto_creation_of_contact", 0)


def ensure_sales_stages():
    """Create the Vietnamese sales pipeline stages if they do not exist."""
    for stage in CRM_SALES_STAGES:
        if not frappe.db.exists("Sales Stage", stage):
            frappe.get_doc({"doctype": "Sales Stage", "stage_name": stage}).insert(
                ignore_permissions=True
            )


def ensure_crm_detail_track_changes():
    """Enable Frappe Version logs for every document shown in a CRM detail page."""
    for doctype in (
        "Address",
        "Lead",
        "Contact",
        "Customer",
        "Opportunity",
        "Quotation",
        "Sales Order",
        "ToDo",
        "Event",
    ):
        if frappe.get_meta(doctype).track_changes:
            continue
        frappe.make_property_setter(
            {
                "doctype": doctype,
                "doctype_or_field": "DocType",
                "property": "track_changes",
                "value": 1,
                "property_type": "Check",
            }
        )
        frappe.clear_cache(doctype=doctype)


def ensure_todo_custom_fields():
    """Create custom fields on ToDo for CRM activity features."""
    create_custom_fields(TODO_CUSTOM_FIELDS, update=True)


def ensure_opportunity_custom_fields():
    """Create fields required by the internal Opportunity form."""
    create_custom_fields(OPPORTUNITY_CUSTOM_FIELDS, update=True)


def ensure_opportunity_lost_reason_custom_fields():
    """Tag the stock Opportunity Lost Reason master as Thắng/Thua so it can be
    reused for both the Won and Lost closing-reason dialogs."""
    create_custom_fields(OPPORTUNITY_LOST_REASON_CUSTOM_FIELDS, update=True)


def ensure_quotation_custom_fields():
    """Create fields required by the internal Quotation form."""
    create_custom_fields(QUOTATION_CUSTOM_FIELDS, update=True)


def ensure_warranty_claim_custom_fields():
    """Link ERPNext's Warranty Claim to the Sales Order it was raised against."""
    create_custom_fields(WARRANTY_CLAIM_CUSTOM_FIELDS, update=True)


def ensure_opportunity_result_reasons():
    """Seed the initial Won/Lost closing reasons if they do not exist yet."""
    for reason, reason_type in OPPORTUNITY_RESULT_REASONS:
        if frappe.db.exists("Opportunity Lost Reason", reason):
            continue
        frappe.get_doc(
            {
                "doctype": "Opportunity Lost Reason",
                "lost_reason": reason,
                "custom_reason_type": reason_type,
            }
        ).insert(ignore_permissions=True)


def ensure_lead_custom_fields():
    """Create fields required by the internal Lead form."""
    create_custom_fields(LEAD_CUSTOM_FIELDS, update=True)


def ensure_sales_order_item_custom_fields():
    """Create fields the CRM Sales Order form/API expect on line items."""
    create_custom_fields(SALES_ORDER_ITEM_CUSTOM_FIELDS, update=True)


def ensure_page_roles():
    """Grant the CRM page to standard selling roles."""
    if not frappe.db.exists("Page", "dcnet-crm"):
        return

    page = frappe.get_doc("Page", "dcnet-crm")
    current_roles = {row.role for row in page.roles}
    if current_roles == set(CRM_PAGE_ROLES):
        return

    page.set("roles", [{"role": role} for role in CRM_PAGE_ROLES])
    page.save(ignore_permissions=True)


def ensure_crm_sidebar():
    """Replace the ERPNext CRM sidebar with the compact DCNET navigation."""
    if not frappe.db.exists("Workspace Sidebar", "CRM"):
        return

    sidebar = frappe.get_doc("Workspace Sidebar", "CRM")
    sidebar.header_icon = "users"
    sidebar.app = "dcnet_crm"
    sidebar.module = "DCNET CRM"
    sidebar.standard = 1
    sidebar.set(
        "items",
        [
            {
                "type": "Link",
                "label": item["label"],
                "icon": item["icon"],
                "link_type": item["link_type"],
                "link_to": item.get("link_to"),
                "route_options": item.get("route_options"),
                "indent": 0,
                "child": 0,
                "collapsible": 0,
                "show_arrow": 0,
                "keep_closed": 0,
                "is_workflow_node": 0,
                "workflow_color": "auto",
            }
            for item in CRM_SIDEBAR_ITEMS
        ],
    )
    sidebar.flags.ignore_validate = True
    sidebar.save(ignore_permissions=True)
