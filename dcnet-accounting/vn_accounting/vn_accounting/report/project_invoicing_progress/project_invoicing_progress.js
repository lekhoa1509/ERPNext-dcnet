frappe.query_reports["Project Invoicing Progress"] = {
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
            options: "Project Costing",
        },
        {
            fieldname: "status",
            label: __("Trạng thái"),
            fieldtype: "Select",
            options: "\nDự kiến\nĐang thi công\nChờ xuất HĐ\nĐã có SI draft\nĐã xuất HĐ\nĐã thu tiền\nĐã hủy",
        },
        {
            fieldname: "due_within_days",
            label: __("Sắp đến hạn trong (ngày)"),
            fieldtype: "Int",
        },
    ],
};
