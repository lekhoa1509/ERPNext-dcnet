frappe.query_reports["So Quy Chi Nhanh"] = {
	onload(report) {
		applyUserBranchFilter(report);
	},

	filters: [
		{
			fieldname: "company",
			label: __("Công ty"),
			fieldtype: "Link",
			options: "Company",
			default: frappe.defaults.get_user_default("Company"),
			reqd: 1,
		},
		{
			fieldname: "from_date",
			label: __("Từ ngày"),
			fieldtype: "Date",
			default: frappe.datetime.add_months(frappe.datetime.get_today(), -1),
			reqd: 1,
		},
		{
			fieldname: "to_date",
			label: __("Đến ngày"),
			fieldtype: "Date",
			default: frappe.datetime.get_today(),
			reqd: 1,
		},
		{
			fieldname: "branch",
			label: __("Chi nhánh"),
			fieldtype: "Link",
			options: "Branch",
		},
		{
			fieldname: "accounting_unit",
			label: __("Đơn vị hạch toán"),
			fieldtype: "Link",
			options: "Cost Center",
			get_query() {
				return {
					filters: {
						company: frappe.query_report.get_filter_value("company"),
						is_group: 0,
					},
				};
			},
		},
		{
			fieldname: "posting_scope",
			label: __("Phạm vi ghi nhận"),
			fieldtype: "Select",
			options: "\nOfficial\nInternal",
		},
		{
			fieldname: "view_mode",
			label: __("Chế độ xem"),
			fieldtype: "Select",
			default: "Detail",
			options: "Detail\nSummary",
		},
	],
};

let branchContextPromise;

async function applyUserBranchFilter(report) {
	const context = await getCurrentUserBranchContext();
	const branchFilter = report.get_filter("branch");

	if (!context.is_privileged && !context.branch) {
		frappe.msgprint(__("User hiện tại chưa được gán chi nhánh trên hồ sơ User."));
		return;
	}

	report.page.add_inner_button(__("Tạo phiếu quỹ chi nhánh"), () => {
		frappe.new_doc("Branch Cash Entry");
	});

	const branchQuery = () => {
		if (context.is_privileged || !context.branch) {
			return {};
		}

		return {
			filters: {
				name: context.branch,
			},
		};
	};
	branchFilter.get_query = branchQuery;
	branchFilter.df.get_query = branchQuery;

	if (!context.is_privileged && context.branch) {
		report.set_filter_value("branch", context.branch);
		branchFilter.df.read_only = 1;
		branchFilter.refresh();
		return;
	}

	branchFilter.df.read_only = 0;
	branchFilter.refresh();
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
