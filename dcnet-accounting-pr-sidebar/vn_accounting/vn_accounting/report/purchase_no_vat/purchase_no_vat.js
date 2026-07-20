// Copyright (c) 2026, Long and Contributors
// License: GNU General Public License v3. See license.txt

frappe.query_reports["Purchase No VAT"] = {
    filters: [
        {
            fieldname: "company",
            label: __("Company"),
            fieldtype: "Link",
            options: "Company",
            default: frappe.defaults.get_user_default("Company"),
            reqd: 1,
        },
        {
            fieldname: "view_mode",
            label: __("Chế độ xem"),
            fieldtype: "Select",
            options: ["Không có HĐ VAT", "Có HĐ VAT"].join("\n"),
            default: "Không có HĐ VAT",
            reqd: 1,
        },
        {
            fieldname: "from_date",
            label: __("Từ ngày"),
            fieldtype: "Date",
            default: frappe.datetime.add_months(frappe.datetime.get_today(), -3),
            reqd: 1,
        },
        {
            fieldname: "to_date",
            label: __("Đến ngày"),
            fieldtype: "Date",
            default: frappe.datetime.get_today(),
            reqd: 1,
        },
        {
            fieldname: "department",
            label: __("Phòng ban đề xuất"),
            fieldtype: "MultiSelectList",
            get_data: function (txt) {
                return frappe.db.get_link_options("Department", txt, {
                    company: frappe.query_report.get_filter_value("company"),
                });
            },
        },
        {
            fieldname: "supplier",
            label: __("Nhà cung cấp"),
            fieldtype: "Link",
            options: "Supplier",
        },
    ],

    onload: function (report) {
        report.page.add_inner_button(__("Tạo hóa đơn mua hàng mới"), function () {
            frappe.new_doc("Purchase Invoice");
        });
    },
};
