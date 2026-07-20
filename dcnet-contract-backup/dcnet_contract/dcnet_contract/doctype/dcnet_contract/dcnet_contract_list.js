// DCNet Contract list customization — show service + payment shape + addendum
// flag + PAKD-link indicator inline so accountants don't need to open each HD.

frappe.listview_settings["DCNet Contract"] = {
	add_fields: [
		"status",
		"customer",
		"service_type",
		"contract_type",
		"payment_mode",
		"acceptance_date",
		"grand_total",
		"has_addendum",
		"contract_no_external",
	],

	get_indicator: function (doc) {
		const status = doc.status || "Draft";
		const colour = {
			"Draft": "gray",
			"Active": "green",
			"Submitted": "green",
			"Expired": "orange",
			"Cancelled": "red",
		}[status] || "blue";
		return [__(status), colour, "status,=," + status];
	},

	formatters: {
		has_addendum: function (value) {
			return value ? '<span class="indicator-pill blue">' + __("Có phụ lục") + "</span>" : "";
		},
		contract_type: function (value) {
			if (!value) return "";
			const colour = { Recurring: "blue", "One-off": "purple", Mixed: "yellow" }[value] || "gray";
			return '<span class="indicator-pill ' + colour + '">' + __(value) + "</span>";
		},
	},
};
