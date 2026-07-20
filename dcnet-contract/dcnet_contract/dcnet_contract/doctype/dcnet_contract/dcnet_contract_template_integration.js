frappe.ui.form.on("DCNet Contract", {
	refresh(frm) {
		// Template version warning for Draft contracts
		if (frm.doc.template_ref && frm.doc.docstatus === 0 && frm.doc.template_outdated) {
			frm.dashboard.set_headline(
				__("Template has been updated. Click 'Re-apply Template' to use the latest version."),
				"orange"
			);
		}

		// Apply Template button (Draft only, template selected)
		if (frm.doc.template_ref && frm.doc.docstatus === 0) {
			frm.add_custom_button(__("Apply Template"), () => {
				let warning = "";
				if (frm.doc.contract_html_edited) {
					warning = __("You have edited the contract content. Applying template will overwrite your changes. Continue?");
				} else {
					warning = __("Apply template content to this contract?");
				}
				frappe.confirm(warning, () => {
					frappe.call({
						method: "dcnet_contract.dcnet_contract.utils.template_engine.apply_template",
						args: {
							contract_name: frm.doc.name,
							template_name: frm.doc.template_ref,
						},
						callback: () => frm.reload_doc(),
					});
				});
			}, __("Template"));
		}
	},

	template_ref(frm) {
		if (!frm.doc.template_ref) return;

		// Auto-fill from template
		frappe.call({
			method: "dcnet_contract.dcnet_contract.doctype.dcnet_contract_template.dcnet_contract_template.get_template",
			args: { template_name: frm.doc.template_ref },
			callback(r) {
				if (!r.message) return;
				const tmpl = r.message;

				// Set contract fields from template
				if (tmpl.service_type) frm.set_value("service_type", tmpl.service_type);
				if (tmpl.contract_type) frm.set_value("contract_type", tmpl.contract_type);
				if (tmpl.payment_mode) frm.set_value("payment_mode", tmpl.payment_mode);
				if (tmpl.package_term_months) frm.set_value("package_term_months", tmpl.package_term_months);

				// Copy items if empty
				if (!frm.doc.items || frm.doc.items.length === 0) {
					frm.clear_table("items");
					(tmpl.items || []).forEach((item) => {
						frm.add_child("items", item);
					});
					frm.refresh_field("items");
				}

				frm.set_value("template_version", tmpl.version || 1);
			},
		});
	},

	contract_html(frm) {
		// Track if HTML was edited by user
		if (frm.doc.template_ref && frm.doc.__original_contract_html !== undefined) {
			if (frm.doc.contract_html !== frm.doc.__original_contract_html) {
				frm.set_value("contract_html_edited", 1);
			}
		}
	},

	onload(frm) {
		// Cache original HTML for edit detection
		if (frm.doc.contract_html) {
			frm.doc.__original_contract_html = frm.doc.contract_html;
		}

		// Filter template_ref to only Approved templates
		frm.set_query("template_ref", () => ({
			filters: { status: "Approved" },
		}));
	},
});
