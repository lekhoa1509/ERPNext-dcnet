/**
 * VN Accounting — Party Report Defaults
 *
 * FB-2026-00616: ERPNext's Accounts Payable / Receivable reports (and their
 * Summary variants) gate the `party` filter behind `party_type`, which ships
 * with no default — so the supplier/customer picker stays unusable until the
 * user discovers they must set Party Type first. For these reports the party
 * type is fixed (Payable → Supplier, Receivable → Customer), so default it on
 * open and the party picker is immediately usable.
 *
 * Follows the same external-patch pattern as general_ledger_branch_filter:
 * an IIFE in app_include_js, hooked on page-change with a short retry loop to
 * cover the report's lazy JS load. Only sets when empty, so a value coming
 * from the URL / a sidebar route_options is never overwritten.
 */
(function () {
	const PARTY_TYPE_BY_REPORT = {
		"Accounts Payable": "Supplier",
		"Accounts Payable Summary": "Supplier",
		"Accounts Receivable": "Customer",
		"Accounts Receivable Summary": "Customer",
	};

	function applyDefault(retries) {
		const route = frappe.get_route ? frappe.get_route() : [];
		if (route[0] !== "query-report") {
			return;
		}

		const party_type = PARTY_TYPE_BY_REPORT[route[1]];
		if (!party_type) {
			return;
		}

		const qr = frappe.query_report;
		const ready =
			qr &&
			qr.report_name === route[1] &&
			typeof qr.get_filter === "function" &&
			qr.get_filter("party_type", false);

		if (ready) {
			// warn=false on the getter — during retries the filter may not exist yet.
			if (!qr.get_filter_value("party_type", false)) {
				qr.set_filter_value("party_type", party_type);
			}
			return;
		}

		if (retries > 0) {
			setTimeout(() => applyDefault(retries - 1), 300);
		}
	}

	$(document).on("page-change", function () {
		setTimeout(() => applyDefault(15), 300);
	});

	$(document).ready(function () {
		setTimeout(() => applyDefault(15), 800);
	});
})();
