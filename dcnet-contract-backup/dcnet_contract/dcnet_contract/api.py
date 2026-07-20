"""Whitelisted endpoints for the DCNet Contract summary header card (FB-505 follow-up)."""

import frappe
from frappe import _
from frappe.utils import getdate, today


@frappe.whitelist()
def get_contract_commission_states(contract: str) -> dict:
	"""Return {billing_period_idx: aggregated_commission_state} for a contract's
	PAKDs — used by the "Hóa đơn & Thanh toán" HTML section on both the
	DCNet Contract form and the PAKD form.

	PAKD Commission Line is a child DocType (istable=1) with an empty
	permissions array — a direct `frappe.db.get_list("PAKD Commission Line")`
	from the browser returns 403 PermissionError even for Administrator.
	This server-side endpoint does the query via `frappe.db.sql` so the
	browser only ever talks to a whitelisted parent-level method.

	Aggregation: highest-priority state per period wins
	(Posted > Pending > Skipped > Cancelled).
	"""
	if not contract:
		return {}
	pakds = frappe.get_all(
		"Phuong An Kinh Doanh",
		filters={"contract_ref": contract},
		pluck="name",
	)
	if not pakds:
		return {}
	rows = frappe.db.sql(
		"""
		SELECT billing_schedule_idx, state
		FROM `tabPAKD Commission Line`
		WHERE parent IN %(pakds)s
		""",
		{"pakds": pakds},
		as_dict=True,
	)
	order = {"Posted": 3, "Pending": 2, "Skipped": 1, "Cancelled": 0}
	by_period: dict[int, str] = {}
	for r in rows:
		idx = r.billing_schedule_idx
		cur = by_period.get(idx)
		if cur is None or order.get(r.state, -1) > order.get(cur, -1):
			by_period[idx] = r.state
	# Frappe serialises dict keys as strings over JSON anyway; keep int keys here.
	return by_period


@frappe.whitelist()
def get_summary_kpis(contract_name: str) -> dict:
	"""Return everything the summary header card needs in one round-trip.

	Aggregates billing schedule + linked Sales Invoices + Payment Entries via
	single SQL queries (no Python iteration over child docs). Target latency
	< 300ms on contracts with ≤120 billing rows.

	Returns dict with keys:
		status, contract_type, service_type, customer, customer_name,
		sales_person_name, branch, grand_total, total_billed, total_collected,
		outstanding, overdue_count, contract_date, acceptance_date, end_date,
		days_remaining, snapshot_date, next_action: {text, button_label,
		button_action, button_args}.
	"""
	if not contract_name or not frappe.db.exists("DCNet Contract", contract_name):
		frappe.throw(_("Contract not found: {0}").format(contract_name))

	contract = frappe.get_cached_doc("DCNet Contract", contract_name)

	# Aggregate Sales Invoice totals via SI names from billing schedule
	si_names = frappe.db.sql_list(
		"""SELECT DISTINCT sales_invoice
		   FROM `tabDCNet Contract Billing Schedule`
		   WHERE parent=%s AND sales_invoice IS NOT NULL AND sales_invoice != ''""",
		contract_name,
	)

	total_billed = 0.0
	total_collected = 0.0
	outstanding = 0.0
	if si_names:
		row = frappe.db.sql(
			"""SELECT
				IFNULL(SUM(grand_total), 0) AS billed,
				IFNULL(SUM(grand_total - outstanding_amount), 0) AS collected,
				IFNULL(SUM(outstanding_amount), 0) AS outstanding
			   FROM `tabSales Invoice`
			   WHERE name IN %(names)s AND docstatus=1""",
			{"names": tuple(si_names)},
			as_dict=True,
		)
		if row:
			total_billed = float(row[0].billed or 0)
			total_collected = float(row[0].collected or 0)
			outstanding = float(row[0].outstanding or 0)

	# Overdue billing rows
	overdue_count = frappe.db.count(
		"DCNet Contract Billing Schedule",
		{"parent": contract_name, "state": "Overdue"},
	)

	# Dates
	end_date = contract.end_date
	days_remaining = None
	if end_date:
		days_remaining = (getdate(end_date) - getdate(today())).days

	# Next action decision tree
	next_action = _contract_next_action(contract, overdue_count, days_remaining)

	return {
		"status": contract.status,
		"contract_type": contract.contract_type,
		"service_type": contract.service_type,
		"customer": contract.customer,
		"customer_name": contract.customer_name,
		"sales_person_name": contract.sales_person_name,
		"branch": contract.branch,
		"grand_total": float(contract.grand_total or 0),
		"total_billed": total_billed,
		"total_collected": total_collected,
		"outstanding": outstanding,
		"overdue_count": overdue_count,
		"contract_date": contract.contract_date,
		"acceptance_date": contract.acceptance_date,
		"end_date": end_date,
		"days_remaining": days_remaining,
		"snapshot_date": contract.contract_date,
		"is_empty": not contract.items or (contract.grand_total or 0) == 0,
		"next_action": next_action,
	}


def _contract_next_action(contract, overdue_count: int, days_remaining):
	"""Decision tree for 'Việc cần làm' on Contract card."""
	# Draft
	if contract.status == "Draft":
		return {
			"text": _("Hoàn thành thông tin → gửi duyệt"),
			"button_label": None,
			"button_action": None,
		}

	# Active branches — order matters (first match wins)
	if contract.status == "Active":
		# Overdue invoice
		overdue_si = _find_overdue_invoice(contract.name)
		if overdue_si:
			return {
				"text": _("Theo dõi công nợ HĐ {0}: còn nợ {1}").format(
					overdue_si["name"], frappe.format_value(overdue_si["outstanding_amount"], {"fieldtype": "Currency"})
				),
				"button_label": _("Mở phiếu"),
				"button_action": "navigate",
				"button_args": {"doctype": "Sales Invoice", "name": overdue_si["name"]},
			}

		# Approaching expiry
		if days_remaining is not None and days_remaining < 60:
			return {
				"text": _("Hợp đồng sắp hết hạn ({0} ngày) — chuẩn bị gia hạn").format(days_remaining),
				"button_label": _("Tạo HĐ gia hạn"),
				"button_action": "amend_contract",
				"button_args": {"contract": contract.name},
			}

		# Projected billing row past due_date
		due_row = _find_due_billing_row(contract.name)
		if due_row:
			return {
				"text": _("Xuất hoá đơn kỳ {0} (đến hạn {1})").format(
					f"T{due_row['month_index']}",
					frappe.format_value(due_row["due_date"], {"fieldtype": "Date"}),
				),
				"button_label": _("Tạo hoá đơn"),
				"button_action": "create_invoice",
				"button_args": {"contract": contract.name, "billing_row": due_row["name"]},
			}

		# No immediate action — show next projected period
		next_row = _find_next_projected_billing_row(contract.name)
		if next_row:
			return {
				"text": _("Tự động chu kỳ tiếp theo: {0}").format(
					frappe.format_value(next_row["due_date"], {"fieldtype": "Date"})
				),
				"button_label": None,
				"button_action": None,
			}

		return {
			"text": _("Hợp đồng đang hoạt động — không có việc cần làm"),
			"button_label": None,
			"button_action": None,
		}

	if contract.status == "Suspended":
		return {
			"text": _("Hợp đồng đang tạm ngưng"),
			"button_label": _("Kích hoạt lại"),
			"button_action": "resume_contract",
			"button_args": {"name": contract.name},
		}

	if contract.status == "Expired":
		return {
			"text": _("Hợp đồng đã hết hạn — đóng hoặc gia hạn"),
			"button_label": _("Gia hạn"),
			"button_action": "amend_contract",
			"button_args": {"contract": contract.name},
		}

	if contract.status == "Cancelled":
		return {
			"text": _("Đã huỷ"),
			"button_label": None,
			"button_action": None,
		}

	if contract.status == "Revised":
		return {
			"text": _("Đã sửa đổi sang phiên bản mới"),
			"button_label": None,
			"button_action": None,
		}

	return {"text": "", "button_label": None, "button_action": None}


def _find_overdue_invoice(contract_name: str):
	"""Return first overdue SI for this contract (oldest first), or None."""
	rows = frappe.db.sql(
		"""SELECT si.name, si.outstanding_amount, si.due_date
		   FROM `tabSales Invoice` si
		   INNER JOIN `tabDCNet Contract Billing Schedule` bs
		     ON bs.sales_invoice = si.name
		   WHERE bs.parent=%s
		     AND si.docstatus=1
		     AND si.outstanding_amount > 0
		     AND si.due_date < %s
		   ORDER BY si.due_date ASC LIMIT 1""",
		(contract_name, today()),
		as_dict=True,
	)
	return rows[0] if rows else None


def _find_due_billing_row(contract_name: str):
	"""Return first Projected billing row past due_date (oldest first), or None."""
	rows = frappe.db.sql(
		"""SELECT name, month_index, due_date
		   FROM `tabDCNet Contract Billing Schedule`
		   WHERE parent=%s AND state='Projected' AND due_date <= %s
		   ORDER BY due_date ASC LIMIT 1""",
		(contract_name, today()),
		as_dict=True,
	)
	return rows[0] if rows else None


def _find_next_projected_billing_row(contract_name: str):
	"""Return next future Projected billing row, or None."""
	rows = frappe.db.sql(
		"""SELECT name, month_index, due_date
		   FROM `tabDCNet Contract Billing Schedule`
		   WHERE parent=%s AND state='Projected' AND due_date > %s
		   ORDER BY due_date ASC LIMIT 1""",
		(contract_name, today()),
		as_dict=True,
	)
	return rows[0] if rows else None
