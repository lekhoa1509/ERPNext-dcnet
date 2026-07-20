// Copyright (c) 2026, Long and Contributors
// License: GNU General Public License v3. See license.txt

frappe.query_reports["Bank Loan Summary"] = {
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
                "Lịch trả nợ trong kỳ",
                "Đang vay (toàn cảnh)",
                "Đáo hạn trong kỳ",
            ].join("\n"),
            default: "Lịch trả nợ trong kỳ",
            reqd: 1,
            // No on_change: Frappe auto-refreshes Script Reports on filter change.
            // An explicit refresh() in on_change races with URL/state update —
            // the result table lags behind the displayed mode, showing stale rows.
        },
        {
            fieldname: "from_date",
            label: __("Từ ngày"),
            fieldtype: "Date",
            default: frappe.datetime.get_today(),
        },
        {
            fieldname: "to_date",
            label: __("Đến ngày"),
            fieldtype: "Date",
            default: frappe.datetime.add_days(frappe.datetime.get_today(), 15),
            reqd: 1,
        },
        {
            fieldname: "status",
            label: __("Trạng thái khoản vay"),
            fieldtype: "MultiSelectList",
            get_data: function () {
                return [
                    { value: "Active", description: "Đang vay" },
                    { value: "Matured", description: "Đến hạn (chưa tất toán)" },
                    { value: "Settled", description: "Đã tất toán" },
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
        if (column.fieldname === "days_to_due" && data) {
            const d = data.days_to_due;
            if (d !== undefined && d !== null) {
                if (d < 0 && data.repayment_status !== "Booked") {
                    value = `<span title="Quá hạn ${-d} ngày" style="color: var(--text-on-red); background: var(--red-100); padding: 2px 6px; border-radius: 4px;">⚠ ${d}</span>`;
                } else if (d <= 7) {
                    value = `<span style="color: var(--text-on-orange); background: var(--orange-100); padding: 2px 6px; border-radius: 4px;">${d}</span>`;
                }
            }
        }
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
        report.page.add_inner_button(__("Tạo khoản vay mới"), function () {
            frappe.new_doc("Bank Loan");
        });
    },
};
