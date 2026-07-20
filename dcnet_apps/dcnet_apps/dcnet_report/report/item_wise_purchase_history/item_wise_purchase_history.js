console.log("🔥 Item Purchase History JS loaded");

frappe.query_reports["Item-wise Purchase History"] = {

    filters: [

        {
            fieldname: "company",
            label: "Công Ty",
            fieldtype: "Link",
            options: "Company",
            default: frappe.defaults.get_user_default("Company")
        },

        {
            fieldname: "from_date",
            label: "Từ Ngày",
            fieldtype: "Date",
            default: frappe.datetime.month_start()
        },

        {
            fieldname: "to_date",
            label: "Đến Ngày",
            fieldtype: "Date",
            default: frappe.datetime.get_today()
        },

        {
            fieldname: "item_group",
            label: "Nhóm Sản Phẩm",
            fieldtype: "Link",
            options: "Item Group"
        },

        {
            fieldname: "item",
            label: "Sản Phẩm",
            fieldtype: "Link",
            options: "Item"
        },

        {
            fieldname: "supplier",
            label: "Nhà Cung Cấp",
            fieldtype: "Link",
            options: "Supplier"
        }
    ],

    format_money(value, decimals = 0) {

        console.log("Formatting money:", value);

        if (!value) return "0 ₫";

        return new Intl.NumberFormat("vi-VN", {
            minimumFractionDigits: decimals,
            maximumFractionDigits: decimals
        }).format(value) + " ₫";
    },

    format_axis(value) {

        console.log("Formatting axis value:", value);

        if (value >= 1_000_000_000)
            return (value / 1_000_000_000).toFixed(1) + "B";

        if (value >= 1_000_000)
            return (value / 1_000_000).toFixed(0) + "M";

        if (value >= 1_000)
            return (value / 1_000).toFixed(0) + "K";

        return value;
    },

    onload_post_render(report) {

        console.log("Report rendered, applying custom formatters and tooltips...");

        setTimeout(() => {

            if (!report.chart) return;

            const chart = report.chart;

            chart.update_options({

                tooltipOptions: {

                    formatTooltipX(label) {
                        return label;
                    },

                    formatTooltipY(value) {

                        return frappe.query_reports[
                            "Item-wise Purchase History"
                        ].format_money(value);
                    }
                },

                axisOptions: {

                    yAxisMode: "tick",

                    yAxisLabel: (value) => {

                        console.log("Formatting y-axis label:", value);

                        return frappe.query_reports[
                            "Item-wise Purchase History"
                        ].format_axis(value);
                    }
                }
            });

            console.log("✅ Chart formatter applied");

        }, 500);
    }
};