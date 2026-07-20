// Filter asset Link field: only show assets without a submitted depreciation schedule.
frappe.ui.form.on("Asset Depreciation Schedule", {
	setup(frm) {
		frm.set_query("asset", () => ({
			query: "vn_accounting.asset.depreciation_filters.assets_without_schedule",
			filters: frm.doc.company ? { company: frm.doc.company } : {},
		}));
	},
});
