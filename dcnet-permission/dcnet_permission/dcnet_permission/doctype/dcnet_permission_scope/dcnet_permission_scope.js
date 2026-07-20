frappe.ui.form.on("DCNET Permission Scope", {
	refresh(frm) {
		set_extra_permission_profile_options(frm);
	},

	department(frm) {
		set_extra_permission_profile_options(frm);
	},

	allowed_roles_add(frm) {
		set_extra_permission_profile_options(frm);
	},

	allowed_roles_remove(frm) {
		set_extra_permission_profile_options(frm);
	},
});

frappe.ui.form.on("DCNET Permission Scope Role", {
	role(frm) {
		set_extra_permission_profile_options(frm);
	},
});

async function set_extra_permission_profile_options(frm) {
	const grid = frm.fields_dict.extra_permission_profiles?.grid;
	if (!grid) return;

	const roles = (frm.doc.allowed_roles || []).map((row) => row.role).filter(Boolean);
	const response = await frappe.call({
		method: "dcnet_permission.permission_manager.get_extra_permission_profile_options",
		args: {
			department: frm.doc.department || "",
			roles,
		},
		type: "GET",
	});
	const labels = (response.message || []).map((profile) => profile.label);
	grid.update_docfield_property("profile", "options", labels.join("\n"));
	grid.refresh();
}
