frappe.query_reports["Misa Account Conflicts"] = {
	filters: [
		{
			fieldname: "batch",
			label: __("Misa Migration Batch"),
			fieldtype: "Link",
			options: "Misa Migration Batch",
		},
	],
	onload(report) {
		report.page.add_inner_button(__("Rename selected to Misa"), () => {
			const sel = report.datatable?.rowmanager?.getCheckedRows?.() || [];
			if (!sel.length) {
				frappe.msgprint(__("Select one or more rows first (use the row checkboxes)."));
				return;
			}
			frappe.confirm(
				__("Apply Misa names to {0} accounts? This renames the Frappe Account.account_name and cascades to all GL Entries.", [sel.length]),
				async () => {
					const results = [];
					for (const idx of sel) {
						const row = report.data[idx];
						if (!row?.row) continue;
						const r = await frappe.call({
							method: "vn_accounting.misa_migration.bulk_pump.account_conflicts.rename_account_to_misa",
							args: { row_name: row.row },
						});
						results.push({ tk: row.misa_tk, ok: r.message?.ok, msg: r.message });
					}
					const ok_n = results.filter(r => r.ok).length;
					frappe.msgprint(
						__("Renamed {0} of {1} accounts. Refresh to see updated Frappe names.", [ok_n, results.length])
					);
					report.refresh();
				}
			);
		});
	},
};
