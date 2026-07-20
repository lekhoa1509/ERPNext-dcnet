/* CCDC Allocation Schedule — per-period posting buttons (TT99/2025 §4)
 *
 * Buttons:
 *   "Ghi nhận kỳ tiếp theo" — post first Pending row
 *   "Ghi nhận tất cả kỳ đến hôm nay" — post all Pending rows due today
 *   "Sổ Cái" — open Journal Entry list for all posted JEs
 */

frappe.ui.form.on("CCDC Allocation Schedule", {
	refresh(frm) {
		const entries = frm.doc.allocation_entries || [];

		// Buttons only for non-cancelled, non-completed schedules
		if (frm.doc.status !== "Cancelled") {
			const pending = entries
				.filter(r => r.status === "Pending")
				.sort((a, b) => a.period_no - b.period_no);

			if (pending.length) {
				frm.add_custom_button(__("Ghi nhận kỳ tiếp theo"), () => {
					const row = pending[0];
					frappe.call({
						method:
							"vn_accounting.asset.ccdc_allocation.post_allocation_period",
						args: {
							schedule_name: frm.doc.name,
							period_idx: row.period_no,
						},
						callback(r) {
							if (!r.message) return;
							const res = r.message;
							if (res.status === "already_posted") {
								frappe.msgprint(
									__(
										"Kỳ {0} đã ghi nhận trước: {1}",
										[res.period_idx, res.je_name]
									)
								);
							} else {
								frappe.msgprint(
									__(
										"Đã ghi nhận kỳ {0}: {1}",
										[res.period_idx, res.je_name]
									)
								);
							}
							frm.reload_doc();
						},
					});
				}, __("Hạch toán"));

				const today = frappe.datetime.get_today();
				const due = pending.filter(r => r.period_start_date <= today);

				if (due.length) {
					frm.add_custom_button(
						__("Ghi nhận tất cả kỳ đến hôm nay"),
						() => {
							frappe.confirm(
								__("Ghi nhận {0} kỳ đến hôm nay?", [due.length]),
								() => {
									let chain = Promise.resolve();
									due.forEach(row => {
										chain = chain.then(() =>
											frappe.call({
												method:
													"vn_accounting.asset.ccdc_allocation.post_allocation_period",
												args: {
													schedule_name: frm.doc.name,
													period_idx: row.period_no,
												},
											})
										);
									});
									chain.then(() => {
										frappe.msgprint(
											__(
												"Đã ghi nhận {0} kỳ.",
												[due.length]
											)
										);
										frm.reload_doc();
									});
								}
							);
						},
						__("Hạch toán")
					);
				}
			}
		}

		// Sổ Cái — show Journal Entry list for all posted entries
		const jeNames = entries.map(r => r.journal_entry).filter(Boolean);
		if (jeNames.length) {
			frm.add_custom_button(__("Sổ Cái"), () => {
				if (jeNames.length === 1) {
					frappe.set_route("query-report", "General Ledger", {
						voucher_no: jeNames[0],
					});
				} else {
					// Multiple JEs: show Journal Entry list
					frappe.route_options = { name: ["in", jeNames] };
					frappe.set_route("List", "Journal Entry");
				}
			}, __("Mở"));
		}
	},
});
