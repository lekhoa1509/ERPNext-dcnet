/**
 * dcnet_theme — defensive guard for frappe.model.with_doctype(undefined).
 *
 * Frappe v16 has a regression where some code path calls
 * frappe.model.with_doctype() with an undefined argument (likely from the
 * query_report viewer when ref_doctype resolution is async). Result:
 * /api/method/frappe.desk.form.load.getdoctype?with_parent=1 (no doctype) →
 * 500 TypeError on Frappe core's getdoctype signature, which kills the
 * Script Report viewer for every report on the site.
 *
 * This guard short-circuits the bad call without making the network round-trip.
 * If/when Frappe core fixes the upstream call site, this patch becomes a no-op.
 */
(function () {
	if (!window.frappe || !frappe.model || frappe.model.__dcnet_with_doctype_patched) return;
	const orig = frappe.model.with_doctype;
	frappe.model.with_doctype = function (doctype, callback, async) {
		if (!doctype) {
			// Skip the broken upstream call. Callback (if any) still runs.
			callback && callback();
			return Promise.resolve();
		}
		return orig.apply(this, arguments);
	};
	frappe.model.__dcnet_with_doctype_patched = true;
})();
