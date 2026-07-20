frappe.ui.form.on("DCNet Contract Template", {
	refresh(frm) {
		// Display placeholder guide
		if (frm.doc.placeholder_guide_html) {
			frm.set_df_property("placeholder_guide_html", "hidden", 0);
			frm.fields_dict.placeholder_guide_html.$wrapper.html(
				frm.doc.placeholder_guide_html
			);
		}

		// Status action buttons
		if (frm.doc.status === "Draft" && !frm.is_new()) {
			frm.add_custom_button(__("Submit for Review"), () => {
				frm.call("submit_for_review").then(() => frm.reload_doc());
			}, __("Actions"));
		}

		if (frm.doc.status === "Pending Review") {
			frm.add_custom_button(__("Approve"), () => {
				frm.call("approve_template").then(() => frm.reload_doc());
			}, __("Actions"));
			frm.add_custom_button(__("Reject"), () => {
				frm.call("reject_template").then(() => frm.reload_doc());
			}, __("Actions"));
		}

		if (frm.doc.status === "Approved") {
			frm.add_custom_button(__("Archive"), () => {
				frappe.confirm(
					__("Archive this template? It will no longer be available for new contracts."),
					() => frm.call("archive_template").then(() => frm.reload_doc())
				);
			}, __("Actions"));
			frm.add_custom_button(__("New Version"), () => {
				frm.call("create_new_version").then((r) => {
					if (r.message) {
						frappe.set_route("Form", "DCNet Contract Template", r.message);
					}
				});
			}, __("Actions"));
		}

		// Status indicator
		const status_colors = {
			"Draft": "orange",
			"Pending Review": "blue",
			"Approved": "green",
			"Archived": "grey",
		};
		if (frm.doc.status) {
			frm.page.set_indicator(__(frm.doc.status), status_colors[frm.doc.status] || "grey");
		}
	},
});
