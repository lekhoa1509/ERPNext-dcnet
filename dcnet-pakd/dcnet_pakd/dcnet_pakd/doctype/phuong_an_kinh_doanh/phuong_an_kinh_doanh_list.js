// PAKD list customization — surface workflow_state as a coloured indicator
// (the field is hidden=1 in the JSON so users see the pill, not the raw text)
// + extra columns fetched on every row.

frappe.listview_settings["Phuong An Kinh Doanh"] = {
	add_fields: [
		"workflow_state",
		"contract_ref",
		"customer",
		"pakd_type",
		"branch",
		"total_revenue_contract",
		"margin_pct",
		"has_pending_revision",
		"has_referral_pending",
	],

	get_indicator: function (doc) {
		const state = doc.workflow_state || doc.status || "Draft";
		const colour_by_state = {
			"Draft": "gray",
			"Pending Sales Director": "orange",
			"Pending General Dept": "orange",
			"Pending Branch Director": "orange",
			"Pending Board": "orange",
			"Approved": "green",
			"Rejected": "red",
			"Cancelled": "darkgrey",
		};
		const filter_value = state;
		return [
			__(state),
			colour_by_state[state] || "blue",
			"workflow_state,=," + filter_value,
		];
	},

	formatters: {
		// Highlight PAKDs that have flagged items (phụ lục pending or Referral chờ)
		// so the list shows a small badge column even when the user doesn't open
		// the row.
		has_pending_revision: function (value) {
			return value ? '<span class="indicator-pill orange">' + __("Phụ lục chờ") + "</span>" : "";
		},
		has_referral_pending: function (value) {
			return value ? '<span class="indicator-pill yellow">' + __("Referral chờ") + "</span>" : "";
		},
		margin_pct: function (value) {
			if (value == null) return "";
			const n = Number(value);
			let cls = "green";
			if (n < 15) cls = "red";
			else if (n < 25) cls = "orange";
			return '<span class="indicator-pill ' + cls + '">' + n.toFixed(1) + "%</span>";
		},
	},
};
