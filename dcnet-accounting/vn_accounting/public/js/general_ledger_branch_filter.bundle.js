(function () {
	const REPORT_NAME = "General Ledger";
	const IMPOSSIBLE_COST_CENTER = "__vn_accounting_branch_restricted__";
	const contextCache = new Map();

	function isGeneralLedgerRoute() {
		const route = frappe.get_route ? frappe.get_route() : [];
		return route[0] === "query-report" && route[1] === REPORT_NAME;
	}

	function normalizeValues(values) {
		if (!values) {
			return [];
		}

		if (Array.isArray(values)) {
			return values.filter(Boolean);
		}

		return [values].filter(Boolean);
	}

	function getContext(company) {
		const cacheKey = company || "__default__";
		if (!contextCache.has(cacheKey)) {
			contextCache.set(
				cacheKey,
				frappe
					.call({
						method: "vn_accounting.query_report.get_general_ledger_access_context",
						args: { company },
					})
					.then((response) => response.message || {})
			);
		}

		return contextCache.get(cacheKey);
	}

	async function applyRestriction(report) {
		const costCenterFilter = report.get_filter("cost_center");
		if (!costCenterFilter) {
			return;
		}

		const company = report.get_filter_value("company");
		const context = await getContext(company);

		if (!context.restricted) {
			costCenterFilter.df.read_only = 0;
			costCenterFilter.refresh();
			return;
		}

		const allowedCostCenters = context.allowed_cost_centers || [];
		if (!allowedCostCenters.length) {
			report.set_filter_value("cost_center", [IMPOSSIBLE_COST_CENTER]);
			if (!report.__vnaMissingBranchCostCenterNotice) {
				frappe.show_alert(
					{
						message: __("Chi nhánh này chưa được cấu hình đơn vị hạch toán để lọc Sổ cái."),
						indicator: "orange",
					},
					7
				);
				report.__vnaMissingBranchCostCenterNotice = true;
			}
			return;
		}

		costCenterFilter.df.get_data = (txt) => {
			const keyword = (txt || "").toLowerCase();
			return allowedCostCenters
				.filter((value) => value.toLowerCase().includes(keyword))
				.map((value) => ({ value, description: value }));
		};

		const currentValues = normalizeValues(report.get_filter_value("cost_center"));
		const nextValues = currentValues.length
			? currentValues.filter((value) => allowedCostCenters.includes(value))
			: allowedCostCenters;

		report.set_filter_value("cost_center", nextValues.length ? nextValues : allowedCostCenters);
		costCenterFilter.df.read_only = !context.allow_manual_subset;
		costCenterFilter.refresh();
	}

	function patchGeneralLedgerReport() {
		const reportConfig = frappe.query_reports?.[REPORT_NAME];
		if (!reportConfig || reportConfig.__vnaBranchFilterPatched) {
			return Boolean(reportConfig);
		}

		const originalOnload = reportConfig.onload;
		reportConfig.onload = async function (report) {
			if (typeof originalOnload === "function") {
				await originalOnload(report);
			}

			const companyFilter = report.get_filter("company");
			if (companyFilter && !companyFilter.__vnaBranchFilterPatched) {
				const originalOnChange = companyFilter.df.on_change;
				companyFilter.df.on_change = async function () {
					if (typeof originalOnChange === "function") {
						await originalOnChange();
					}

					await applyRestriction(report);
				};
				companyFilter.__vnaBranchFilterPatched = true;
			}

			await applyRestriction(report);
		};
		reportConfig.__vnaBranchFilterPatched = true;
		return true;
	}

	function tryPatch(retries) {
		if (retries <= 0) {
			return;
		}

		if (!isGeneralLedgerRoute()) {
			return;
		}

		if (!patchGeneralLedgerReport()) {
			setTimeout(() => tryPatch(retries - 1), 300);
		}
	}

	$(document).on("page-change", function () {
		setTimeout(() => tryPatch(15), 300);
	});

	$(document).ready(function () {
		setTimeout(() => tryPatch(15), 800);
	});
})();
