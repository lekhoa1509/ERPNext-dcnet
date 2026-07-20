"""Document event handlers for DCNet Contract integration."""

import frappe


def si_autofill_contract(doc, method):
	"""Auto-fill Sales Invoice.dcnet_contract + dcnet_pakd + billing_period_idx
	from the DCNet Contract Billing Schedule row that points at this SI.

	dcnet_pakd is derived from the contract (1 HD = 1 PAKD per D3 unique
	constraint). If multiple PAKDs ever exist for a contract (legacy or
	temporarily Draft+Approved transition), the active Approved one wins.
	"""
	if not doc.dcnet_contract:
		bs = frappe.db.get_value(
			"DCNet Contract Billing Schedule",
			{"sales_invoice": doc.name},
			["parent", "month_index"],
			as_dict=True,
		)
		if bs:
			doc.dcnet_contract = bs.parent
			doc.billing_period_idx = bs.month_index or 0
	# Derive dcnet_pakd from dcnet_contract (always — refresh on resave so a
	# new Approved PAKD picks up old SIs once the workflow flips).
	if doc.dcnet_contract and not doc.dcnet_pakd:
		doc.dcnet_pakd = _resolve_active_pakd(doc.dcnet_contract)


def pe_autofill_contract(doc, method):
	"""Auto-fill Payment Entry.dcnet_contract + dcnet_pakd + billing_period_idx
	from the first Sales Invoice reference. dcnet_pakd is preserved from the
	SI itself (not re-derived) so a PE always matches its underlying SI's
	PAKD even after a workflow change.
	"""
	if not doc.dcnet_contract:
		for ref in doc.references or []:
			if ref.reference_doctype != "Sales Invoice" or not ref.reference_name:
				continue
			ct, pakd, idx = frappe.db.get_value(
				"Sales Invoice", ref.reference_name,
				["dcnet_contract", "dcnet_pakd", "billing_period_idx"],
			) or (None, None, None)
			if ct:
				doc.dcnet_contract = ct
				doc.dcnet_pakd = pakd or None
				doc.billing_period_idx = idx or 0
				break
	# Fallback: if dcnet_contract is set but dcnet_pakd isn't (legacy SI
	# created before the dcnet_pakd field existed), resolve now.
	if doc.dcnet_contract and not doc.dcnet_pakd:
		doc.dcnet_pakd = _resolve_active_pakd(doc.dcnet_contract)


def _resolve_active_pakd(contract_name: str) -> str | None:
	"""Pick the Approved PAKD for this contract; fall back to any non-Cancelled
	one. Returns None if the contract has no PAKDs yet (auto-fill stays blank
	until a PAKD is created)."""
	pakd = frappe.db.get_value(
		"Phuong An Kinh Doanh",
		{"contract_ref": contract_name, "workflow_state": "Approved"},
		"name",
	)
	if pakd:
		return pakd
	return frappe.db.get_value(
		"Phuong An Kinh Doanh",
		{"contract_ref": contract_name, "workflow_state": ["!=", "Cancelled"]},
		"name",
	)


def on_payment_entry_submit(doc, method):
    """When a Payment Entry is submitted, check if it pays a Sales Invoice linked to a billing schedule row.

    Transitions: Invoiced → Paid (only if SI fully paid).
    For Prepay contracts, all billing_schedule rows linked to the same SI flip together.
    """
    if doc.payment_type != "Receive":
        return

    # Find all SI references in this PE
    si_names = set()
    for ref in doc.references:
        if ref.reference_doctype == "Sales Invoice" and ref.reference_name:
            si_names.add(ref.reference_name)

    if not si_names:
        return

    for si_name in si_names:
        _process_si_payment(si_name, doc.name)


def on_payment_entry_cancel(doc, method):
    """When a Payment Entry is cancelled, revert billing_schedule rows Paid → Invoiced."""
    if doc.payment_type != "Receive":
        return

    si_names = {
        ref.reference_name
        for ref in doc.references
        if ref.reference_doctype == "Sales Invoice" and ref.reference_name
    }
    if not si_names:
        return

    for si_name in si_names:
        bs_rows = frappe.get_all(
            "DCNet Contract Billing Schedule",
            filters={"sales_invoice": si_name, "state": "Paid", "payment_entry": doc.name},
            fields=["name"],
        )
        for row in bs_rows:
            frappe.db.set_value(
                "DCNet Contract Billing Schedule",
                row.name,
                {"state": "Invoiced", "payment_entry": None},
                update_modified=False,
            )


def _process_si_payment(si_name: str, pe_name: str):
    """Check if SI is fully paid, then update linked billing schedule rows."""
    try:
        si = frappe.get_doc("Sales Invoice", si_name)
    except frappe.DoesNotExistError:
        frappe.log_error(
            f"Sales Invoice {si_name} không tồn tại — bỏ qua xử lý billing schedule",
            "DCNet Contract PE Hook",
        )
        return

    # Don't flip to Paid if there's still outstanding
    if si.outstanding_amount > 0:
        return

    # Find billing schedule rows linked to this SI
    bs_rows = frappe.get_all(
        "DCNet Contract Billing Schedule",
        filters={"sales_invoice": si_name, "state": ["in", ["Invoiced", "Overdue"]]},
        fields=["name", "parent"],
    )

    if not bs_rows:
        return

    contract_names = set()
    for row in bs_rows:
        frappe.db.set_value(
            "DCNet Contract Billing Schedule",
            row.name,
            {"state": "Paid", "payment_entry": pe_name},
            update_modified=False,
        )
        contract_names.add(row.parent)

    # Fire event for each affected contract (for future PAKD integration)
    for contract_name in contract_names:
        frappe.publish_realtime(
            "dcnet_contract.billing_period_paid",
            {"contract": contract_name, "sales_invoice": si_name, "payment_entry": pe_name},
        )
