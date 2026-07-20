/**
 * Data Import Auto-Import Client Script
 * 
 * Automatically starts import when file is uploaded, removing the need for
 * manual "Start Import" button click.
 */

frappe.ui.form.on("Data Import", {
	import_file(frm) {
		// When import file is set and document is saved
		if (frm.doc.import_file && !frm.is_new()) {
			// Auto-start import after a short delay to ensure file is processed
			setTimeout(() => {
				frm.call({
					method: "dcnet_apps.utils.data_import_auto.auto_start_import",
					args: {
						data_import_name: frm.doc.name
					},
					btn: frm.page.btn_primary,
					callback: function(r) {
						if (r.message === true) {
							frm.disable_save();
							frappe.show_alert({
								message: __("Import started automatically"),
								indicator: "green"
							});
						}
					},
					error: function(r) {
						frappe.show_alert({
							message: __("Error starting import"),
							indicator: "red"
						});
					}
				});
			}, 500);
		}
	}
});
