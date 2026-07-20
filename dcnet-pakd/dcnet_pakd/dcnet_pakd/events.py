"""Document event handlers for DCNet PAKD integration."""

import frappe
from frappe import _
from frappe.utils import getdate


def on_payment_entry_submit(doc, method):
	"""When PE is submitted and pays an SI linked to a billing_schedule row,
	find the matching Approved PAKD and post its commission_lines."""
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
		_post_commission_for_si(si_name, doc)


def on_payment_entry_cancel(doc, method):
	"""When PE is cancelled, reverse commission_lines + beneficiary_lines that
	were posted by this PE.
	"""
	if doc.payment_type != "Receive":
		return

	posted_commission = frappe.get_all(
		"PAKD Commission Line",
		filters={"payment_entry": doc.name, "state": "Posted"},
		fields=["name", "parent", "additional_salary", "journal_entry", "component"],
	)
	posted_beneficiary = frappe.get_all(
		"PAKD Beneficiary Line",
		filters={"payment_entry": doc.name, "state": "Posted"},
		fields=["name", "parent", "journal_entry", "kind"],
	)
	if not posted_commission and not posted_beneficiary:
		return

	affected_pakds = set()
	for line in posted_commission:
		_cancel_commission_line(line)
		affected_pakds.add(line.parent)

	for line in posted_beneficiary:
		_cancel_beneficiary_line(line)
		affected_pakds.add(line.parent)

	# Try to cancel the Additional Salary if fully unused (all Sales Commission lines cancelled)
	for pakd_name in affected_pakds:
		_maybe_cancel_additional_salary(pakd_name, doc.name)


def on_pakd_update(doc, method):
	"""Auto-post commission when PAKD transitions into Approved.

	When PAKD Settings.commission_post_on_approval is on, catch up any
	commission lines whose billing-schedule row is already Paid but never
	posted (e.g. PE submitted before the PAKD got approved). Failures here
	don't block the approval — the user can fall back to the manual
	"Đăng hoa hồng" button surfaced in the summary card.
	"""
	if doc.workflow_state != "Approved":
		return
	if not doc.has_value_changed("workflow_state"):
		return

	settings = frappe.get_cached_doc("PAKD Settings", "PAKD Settings")
	if not int(settings.commission_post_on_approval or 0):
		return

	try:
		_auto_post_on_approval(doc)
	except Exception as e:
		frappe.log_error(frappe.get_traceback(), f"PAKD auto-post on approval failed: {doc.name}")
		frappe.msgprint(
			_("Tự động đăng hoa hồng thất bại: {0}. Dùng nút 'Đăng hoa hồng' để đăng thủ công.").format(str(e)),
			title=_("Cảnh báo"),
			indicator="orange",
		)


def on_contract_cancel(doc, method):
	"""When a DCNet Contract is cancelled, cancel all Pending commission_lines on linked PAKDs."""
	pakds = frappe.get_all(
		"Phuong An Kinh Doanh",
		filters={"contract_ref": doc.name, "workflow_state": "Approved"},
		fields=["name"],
	)
	for pakd in pakds:
		_cancel_pending_lines(pakd.name)


# ─── Internals ────────────────────────────────────────────────────────────────


def _post_commission_for_si(si_name: str, pe_doc):
	"""Find the billing_schedule row paid by this SI, then post PAKD commission lines."""
	# Find which contract billing rows this SI belongs to
	bs_rows = frappe.get_all(
		"DCNet Contract Billing Schedule",
		filters={"sales_invoice": si_name, "state": "Paid"},
		fields=["name", "parent", "month_index"],
	)
	if not bs_rows:
		return

	for row in bs_rows:
		contract_name = row.parent
		# Find Approved PAKDs linked to this contract
		pakds = frappe.get_all(
			"Phuong An Kinh Doanh",
			filters={"contract_ref": contract_name, "workflow_state": "Approved"},
			fields=["name"],
		)
		for pakd_ref in pakds:
			_post_pakd_commission_lines(pakd_ref.name, row.month_index, pe_doc)


def _post_pakd_commission_lines(pakd_name: str, month_index: int, pe_doc):
	"""Post Pending commission_lines + beneficiary_lines matching the billing period.

	v0.2.0 routing:
	- commission_lines now scope to Sales Commission + License Fee only.
	- beneficiary_lines (MS / AC / Referral) post via post_beneficiary_je, 2- or
	  3-leg depending on recipient + TNCN.
	"""
	from dcnet_pakd.dcnet_pakd.integrations.payroll import push_to_additional_salary
	from dcnet_pakd.dcnet_pakd.integrations.accounting import (
		post_beneficiary_je,
		post_journal_entry,
	)

	payment_date = getdate(pe_doc.posting_date)
	settings = frappe.get_cached_doc("PAKD Settings", "PAKD Settings")
	cutoff_day = settings.cutoff_day_of_month or 5

	# Determine payroll_month (cutoff: day <= cutoff → prev month)
	from frappe.utils import add_months
	if payment_date.day <= cutoff_day:
		ref_month = add_months(payment_date, -1)
	else:
		ref_month = payment_date
	payroll_month = ref_month.strftime("%Y-%m")

	pending_commission = frappe.get_all(
		"PAKD Commission Line",
		filters={"parent": pakd_name, "billing_schedule_idx": month_index, "state": "Pending"},
		fields=["name", "component", "amount", "billing_schedule_idx"],
	)
	pending_beneficiaries = frappe.get_all(
		"PAKD Beneficiary Line",
		filters={
			"parent": pakd_name,
			"state": "Pending",
			# Per Period rows must match this billing period; One-off rows post
			# at the first billing period only (billing_schedule_idx=1) and the
			# caller is expected to drive the first PE through that period.
			"billing_schedule_idx": ["in", [month_index, 0]],
		},
		fields=["name", "kind", "recurrence", "billing_schedule_idx"],
	)
	# Filter One-off rows so they only fire on the first paid period
	pending_beneficiaries = [
		bl for bl in pending_beneficiaries
		if bl.recurrence != "One-off" or month_index == 1
	]

	if not pending_commission and not pending_beneficiaries:
		return

	pakd_doc = frappe.get_doc("Phuong An Kinh Doanh", pakd_name)
	use_hrms = bool(settings.use_hrms_for_commission)

	# ── Pass A: commission_lines (SC + License) via legacy JE + AS path
	# JEs are created PER COMPONENT TYPE (separate JE for SC vs License Fee)
	# so they're traceable + filterable in sổ cái — different deductibility
	# profiles for CIT settlement.
	as_name = None
	je_by_component: dict = {}
	if pending_commission:
		if use_hrms:
			luong_lines = [l for l in pending_commission if l.component == "Sales Commission"]
			license_lines = [l for l in pending_commission if l.component == "License Fee"]
			if luong_lines:
				total_luong = sum(l.amount for l in luong_lines)
				as_name = push_to_additional_salary(pakd_doc, total_luong, payroll_month, pe_doc.name)
			if license_lines:
				je_by_component = post_journal_entry(pakd_doc, license_lines, payroll_month, pe_doc.name)
		else:
			je_by_component = post_journal_entry(
				pakd_doc, pending_commission, payroll_month, pe_doc.name,
				include_sales_commission=True,
			)

		for line in pending_commission:
			if use_hrms and line.component == "Sales Commission":
				line_as = as_name
				line_je = None
			else:
				line_as = None
				line_je = je_by_component.get(line.component)
			frappe.db.set_value(
				"PAKD Commission Line",
				line.name,
				{
					"state": "Posted",
					"payroll_month": payroll_month,
					"payment_entry": pe_doc.name,
					"additional_salary": line_as,
					"journal_entry": line_je,
				},
				update_modified=False,
			)

	# ── Pass B: beneficiary_lines (MS / AC / Referral) — one JE per line
	for ref in pending_beneficiaries:
		bl_doc = frappe.get_doc("PAKD Beneficiary Line", ref.name)
		bje = post_beneficiary_je(pakd_doc, bl_doc, payroll_month, pe_doc.name)
		frappe.db.set_value(
			"PAKD Beneficiary Line",
			ref.name,
			{
				"state": "Posted",
				"billing_schedule_idx": month_index if bl_doc.recurrence == "Per Period" else ref.billing_schedule_idx,
				"journal_entry": bje,
				"payment_entry": pe_doc.name,
			},
			update_modified=False,
		)


def _auto_post_on_approval(pakd_doc):
	"""For each Paid billing row on the linked contract, find a Receive PE
	and post pending commission lines for that month_index.
	"""
	if not pakd_doc.contract_ref:
		return

	paid_rows = frappe.get_all(
		"DCNet Contract Billing Schedule",
		filters={"parent": pakd_doc.contract_ref, "state": "Paid"},
		fields=["name", "month_index", "sales_invoice"],
	)
	if not paid_rows:
		return

	for row in paid_rows:
		if not row.sales_invoice:
			continue
		# Skip if no Pending lines remain for this month (already posted or none configured)
		pending_count = frappe.db.count(
			"PAKD Commission Line",
			filters={"parent": pakd_doc.name, "billing_schedule_idx": row.month_index, "state": "Pending"},
		)
		if not pending_count:
			continue
		# Find the latest submitted Receive PE referencing this SI
		pe_row = frappe.db.sql(
			"""SELECT per.parent FROM `tabPayment Entry Reference` per
			   JOIN `tabPayment Entry` pe ON pe.name = per.parent
			   WHERE per.reference_doctype = 'Sales Invoice'
			     AND per.reference_name = %s
			     AND pe.docstatus = 1
			     AND pe.payment_type = 'Receive'
			   ORDER BY pe.posting_date DESC LIMIT 1""",
			(row.sales_invoice,),
		)
		if not pe_row:
			continue
		pe_doc = frappe.get_doc("Payment Entry", pe_row[0][0])
		_post_pakd_commission_lines(pakd_doc.name, row.month_index, pe_doc)


def _cancel_commission_line(line: dict):
	"""Cancel JE if draft. AS cancellation handled separately."""
	if line.get("journal_entry"):
		je_status = frappe.db.get_value("Journal Entry", line["journal_entry"], "docstatus")
		if je_status == 0:  # Draft → delete (cannot cancel a draft)
			frappe.delete_doc("Journal Entry", line["journal_entry"], ignore_permissions=True, force=1)
		# If submitted JE: mark line cancelled but leave JE — requires manual reversal
	frappe.db.set_value(
		"PAKD Commission Line",
		line["name"],
		{"state": "Cancelled", "payment_entry": None},
		update_modified=False,
	)


def _cancel_beneficiary_line(line: dict):
	"""Cancel beneficiary JE if draft; leave submitted JE for manual reversal."""
	if line.get("journal_entry"):
		je_status = frappe.db.get_value("Journal Entry", line["journal_entry"], "docstatus")
		if je_status == 0:
			frappe.delete_doc("Journal Entry", line["journal_entry"], ignore_permissions=True, force=1)
		elif je_status == 1:
			frappe.msgprint(
				_("Beneficiary JE {0} đã được duyệt — vui lòng đảo bút toán thủ công.")
				.format(line["journal_entry"]),
				title=_("Beneficiary reversal warning"),
				indicator="orange",
			)
	frappe.db.set_value(
		"PAKD Beneficiary Line",
		line["name"],
		{"state": "Cancelled", "payment_entry": None},
		update_modified=False,
	)


def _maybe_cancel_additional_salary(pakd_name: str, pe_name: str):
	"""If all Sales Commission lines that used this PE are now cancelled, cancel the AS."""
	# Check if there are still Posted lines using this AS
	remaining = frappe.db.count(
		"PAKD Commission Line",
		filters={"parent": pakd_name, "payment_entry": None, "state": "Posted", "component": "Sales Commission"},
	)
	if remaining > 0:
		return

	# Find the AS linked to cancelled lines from this PE
	# (we stored it before cancellation)
	as_names = frappe.db.get_all(
		"PAKD Commission Line",
		filters={"parent": pakd_name, "state": "Cancelled", "component": "Sales Commission"},
		fields=["additional_salary"],
		distinct=True,
	)
	for row in as_names:
		if not row.additional_salary:
			continue
		as_doc = frappe.get_doc("Additional Salary", row.additional_salary)
		if as_doc.docstatus == 0:
			# Draft AS: delete it (cannot cancel a draft)
			frappe.delete_doc("Additional Salary", as_doc.name, ignore_permissions=True, force=1)
		elif as_doc.docstatus == 1:
			# Check if AS is in a submitted Salary Slip (payroll processed)
			in_payroll = frappe.db.exists(
				"Salary Detail",
				{"additional_salary": as_doc.name, "docstatus": 1},
			)
			if in_payroll:
				frappe.msgprint(
					_(
						"Additional Salary {0} is already in a submitted Payroll. "
						"Manual salary reversal required."
					).format(as_doc.name),
					title=_("Salary Reversal Warning"),
					indicator="orange",
				)
			else:
				as_doc.cancel()


def _cancel_pending_lines(pakd_name: str):
	"""Cancel all Pending commission_lines + beneficiary_lines for a PAKD."""
	for doctype in ("PAKD Commission Line", "PAKD Beneficiary Line"):
		pending = frappe.get_all(
			doctype,
			filters={"parent": pakd_name, "state": "Pending"},
			fields=["name"],
		)
		for line in pending:
			frappe.db.set_value(
				doctype,
				line.name,
				{"state": "Cancelled"},
				update_modified=False,
			)
