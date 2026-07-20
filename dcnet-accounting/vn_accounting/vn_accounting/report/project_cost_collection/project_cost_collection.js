// Project Cost Collection — filters

frappe.query_reports["Project Cost Collection"] = {
    filters: [
        {
            fieldname: "company",
            label: __("Công ty"),
            fieldtype: "Link",
            options: "Company",
            default: frappe.defaults.get_user_default("Company"),
            reqd: 1,
        },
        {
            fieldname: "project",
            label: __("Công trình"),
            fieldtype: "Link",
            options: "Project",
        },
        {
            fieldname: "stage",
            label: __("Giai đoạn"),
            fieldtype: "Link",
            options: "Project Costing Stage",
            get_query: function () {
                const project = frappe.query_report.get_filter_value("project");
                if (project) {
                    return { filters: { parent_costing: project } };
                }
                return {};
            },
        },
        {
            fieldname: "cost_type",
            label: __("Loại chi phí"),
            fieldtype: "Select",
            options: "\nTrực tiếp\nPhân bổ",
        },
        {
            fieldname: "from_date",
            label: __("Từ ngày"),
            fieldtype: "Date",
            default: frappe.datetime.year_start(),
            reqd: 1,
        },
        {
            fieldname: "to_date",
            label: __("Đến ngày"),
            fieldtype: "Date",
            default: frappe.datetime.get_today(),
            reqd: 1,
        },
    ],
};
