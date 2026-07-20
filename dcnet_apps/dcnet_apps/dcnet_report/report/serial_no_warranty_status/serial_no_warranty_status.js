// Copyright (c) 2026, DCNET Cloud and contributors
// For license information, please see license.txt

frappe.query_reports["Serial No Warranty Status"] = {
	filters: [
		{
			fieldname: "item_code",
			label: __("Item Code"),
			fieldtype: "Link",
			options: "Item",
		},
		{
			fieldname: "item_group",
			label: __("Item Group"),
			fieldtype: "Link",
			options: "Item Group",
		},
		{
			fieldname: "brand",
			label: __("Brand"),
			fieldtype: "Link",
			options: "Brand",
		},
		{
			fieldname: "warehouse",
			label: __("Warehouse"),
			fieldtype: "Link",
			options: "Warehouse",
		},
		{
			fieldname: "status",
			label: __("Status"),
			fieldtype: "Select",
			options: "\nActive\nInactive\nDelivered\nExpired",
		},
		{
			fieldname: "customer",
			label: __("Customer"),
			fieldtype: "Link",
			options: "Customer",
		},
		{
			fieldname: "batch_no",
			label: __("Batch No"),
			fieldtype: "Link",
			options: "Batch",
		},
		{
			fieldname: "maintenance_status",
			label: __("Maintenance Status"),
			fieldtype: "Select",
			options: "\nUnder Warranty\nOut of Warranty\nUnder AMC\nOut of AMC",
		},
		{
			fieldname: "sales_invoice_no",
			label: __("Sales Invoice No"),
			fieldtype: "Link",
			options: "Sales Invoice",
		},
	],
	formatter: function (value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);
		
		if (data && data.warranty_expiry_date) {
			let expiry_date = data.warranty_expiry_date;
			let today = frappe.datetime.get_today();
			
			if (expiry_date < today) {
				value = `<span style="color:red; font-weight:500;">${value}</span>`;
			}
		}

		return value;
	}
};
