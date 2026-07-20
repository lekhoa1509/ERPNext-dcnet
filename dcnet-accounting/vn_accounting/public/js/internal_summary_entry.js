(() => {
	let branchContextPromise;

	frappe.ui.form.on("Internal Summary Entry", {
		setup(frm) {
			frm.set_query("branch", () => getBranchQuery(frm));

			frm.set_query("accounting_unit", () => ({
				filters: {
					company: frm.doc.company,
					is_group: 0,
				},
			}));
		},

		async onload(frm) {
			await applyUserBranchContext(frm);
		},

		async refresh(frm) {
			await applyUserBranchContext(frm);
			updateIntro(frm);
		},
	});

	function getBranchQuery(frm) {
		const context = frm.__internalSummaryBranchPermissionContext;
		if (!context || context.is_privileged || !context.branch) {
			return {};
		}

		return {
			filters: {
				name: context.branch,
			},
		};
	}

	async function applyUserBranchContext(frm) {
		const context = await getCurrentUserBranchContext();
		frm.__internalSummaryBranchPermissionContext = context;

		if (context.is_privileged) {
			frm.set_df_property("branch", "read_only", 0);
			return;
		}

		if (context.branch) {
			if (!frm.doc.branch || frm.is_new()) {
				await frm.set_value("branch", context.branch);
			}
			frm.set_df_property("branch", "read_only", 1);
			return;
		}

		frm.set_df_property("branch", "read_only", 1);
		if (!frm.__internalSummaryBranchPermissionWarned) {
			frappe.msgprint(__("User hiện tại chưa được gán chi nhánh trên hồ sơ User."));
			frm.__internalSummaryBranchPermissionWarned = true;
		}
	}

	async function getCurrentUserBranchContext() {
		if (!branchContextPromise) {
			branchContextPromise = frappe.call({
				method: "vn_accounting.branch_cash.service.get_current_user_branch_context",
			});
		}

		const response = await branchContextPromise;
		return response.message || {};
	}

	function updateIntro(frm) {
		frm.set_intro(
			__("Internal summary entries only update the internal book and do not post to the general ledger."),
			"orange"
		);
	}
})();
