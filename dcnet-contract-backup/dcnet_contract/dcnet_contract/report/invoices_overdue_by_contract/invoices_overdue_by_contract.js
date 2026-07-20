frappe.query_reports["Invoices Overdue by Contract"] = {
	filters: [
		{
			fieldname: "dcnet_contract",
			label: __("Hợp đồng"),
			fieldtype: "Link",
			options: "DCNet Contract",
		},
		{
			fieldname: "customer",
			label: __("Khách hàng"),
			fieldtype: "Link",
			options: "Customer",
		},
		{
			fieldname: "min_days_overdue",
			label: __("Quá hạn tối thiểu (ngày)"),
			fieldtype: "Int",
		},
	],
	formatter: function (value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);
		if (column.fieldname === "days_overdue" && data && data.days_overdue) {
			const d = data.days_overdue;
			let color = "orange";
			if (d >= 30) color = "red";
			else if (d < 8) color = "yellow";
			value = `<span style="color:var(--text-on-${color},#b32424);font-weight:600;">${value}</span>`;
		}
		return value;
	},
};
