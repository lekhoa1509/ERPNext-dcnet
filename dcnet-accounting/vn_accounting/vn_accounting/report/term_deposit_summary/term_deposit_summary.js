// Copyright (c) 2026, Long and Contributors
// License: GNU General Public License v3. See license.txt

frappe.query_reports["Term Deposit Summary"] = {
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
            options: [
                "Đang gửi tại ngày",
                "Phát sinh trong kỳ",
                "Đáo hạn trong kỳ",
            ].join("\n"),
            default: "Đang gửi tại ngày",
            reqd: 1,
        },
        {
            fieldname: "from_date",
            label: __("Từ ngày"),
            fieldtype: "Date",
            default: frappe.datetime.add_months(frappe.datetime.get_today(), -1),
        },
        {
            fieldname: "to_date",
            label: __("Đến ngày"),
            fieldtype: "Date",
            default: frappe.datetime.get_today(),
            reqd: 1,
        },
        {
            fieldname: "status",
            label: __("Trạng thái"),
            fieldtype: "MultiSelectList",
            get_data: function () {
                return [
                    { value: "Active", description: "Đang gửi" },
                    { value: "Matured", description: "Đáo hạn (chưa rút)" },
                    { value: "Settled", description: "Đã tất toán" },
                    { value: "Early Settled", description: "Tất toán trước hạn" },
                ];
            },
            default: ["Active", "Matured"],
        },
        {
            fieldname: "bank",
            label: __("Ngân hàng"),
            fieldtype: "Link",
            options: "Bank",
        },
    ],

    formatter: function (value, row, column, data, default_formatter) {
        value = default_formatter(value, row, column, data);
        if (column.fieldname === "days_to_maturity" && data) {
            const d = data.days_to_maturity;
            if (d !== undefined && d !== null) {
                if (d < 0) {
                    value = `<span style="color: var(--text-on-red); background: var(--red-100); padding: 2px 6px; border-radius: 4px;">${d}</span>`;
                } else if (d <= 30) {
                    value = `<span style="color: var(--text-on-orange); background: var(--orange-100); padding: 2px 6px; border-radius: 4px;">${d}</span>`;
                }
            }
        }
        return value;
    },

    onload: function (report) {
        report.page.add_inner_button(__("Tạo phiếu gửi tiền mới"), function () {
            frappe.new_doc("Term Deposit");
        });
    },
};
