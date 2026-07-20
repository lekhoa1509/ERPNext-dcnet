// Copyright (c) 2026, DCNET Cloud and contributors
// For license information, please see license.txt

frappe.query_reports["DCNET Sales Order Trends"] = {
    filters: [
        {
            fieldname: "company",
            label: __("Công ty"),
            fieldtype: "Link",
            options: "Company",
            default: frappe.defaults.get_user_default("Company"),
            reqd: 1
        },
        {
            fieldname: "period",
            label: __("Kỳ"),
            fieldtype: "Select",
            options: [
                { value: "Daily", label: "Hàng ngày" },
                { value: "Weekly", label: "Hàng tuần" },
                { value: "Monthly", label: "Hàng tháng" },
                { value: "Quarterly", label: "Hàng quý" },
                { value: "Half-Yearly", label: "Nửa năm" },
                { value: "Yearly", label: "Hàng năm" }
            ],
            default: "Daily",
            reqd: 1
        },
        {
            fieldname: "fiscal_year",
            label: __("Năm tài chính"),
            fieldtype: "Link",
            options: "Fiscal Year",
            default: erpnext.utils.get_fiscal_year()
        },
        {
            fieldname: "date_field",
            label: __("Kỳ dựa trên"),
            fieldtype: "Select",
            options: [
                { value: "transaction_date", label: "Ngày ghi sổ" },
                { value: "delivery_date", label: "Ngày giao hàng" }
            ],
            default: "transaction_date"
        },
        {
            fieldname: "based_on",
            label: __("Dựa trên"),
            fieldtype: "Select",
            options: [
                { value: "Item", label: "Sản phẩm" },
                { value: "Customer", label: "Khách hàng" },
                { value: "Territory", label: "Khu vực" },
                { value: "Sales Person", label: "Nhân viên bán hàng" }
            ],
            default: "Item"
        },
        {
            fieldname: "group_by",
            label: __("Nhóm theo"),
            fieldtype: "Select",
            options: [
                "",
                "Item Group",
                "Customer Group",
                "Territory",
                "Sales Person"
            ]
        },
        {
            fieldname: "customer_group",
            label: __("Nhóm khách hàng"),
            fieldtype: "Link",
            options: "Customer Group",
            depends_on: "eval:doc.group_by == 'Customer Group'"
        },
        {
            fieldname: "include_closed_orders",
            label: __("Bao gồm đơn hàng đã đóng"),
            fieldtype: "Check"
        }
    ]
};
