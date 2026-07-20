"""Beneficiary Payable — cash-basis "phải trả phía khách" worklist.

Lists every PAKD Beneficiary Line where state=Pending AND the underlying
billing schedule row is Paid (PE submitted). These are the kickback /
markup / referral entries the accountant should post next via the
beneficiary cell-action "Đăng JE ngay".

Kind scope: Manager Services / Add Costs / Referral (per v0.2.0 §3.3).

For Per Period rows, eligibility = any BS row Paid on the same contract
(the engine in events._post_pakd_commission_lines walks all Paid BS
rows). For One-off rows (Referral), eligibility = the first Paid BS
period (month_index=1 typically).
"""

import frappe
from frappe import _


def execute(filters=None):
	filters = filters or {}
	columns = _columns()
	data = _query(filters)
	return columns, data


def _columns():
	return [
		{"label": _("PAKD"), "fieldname": "pakd", "fieldtype": "Link",
		 "options": "Phuong An Kinh Doanh", "width": 140},
		{"label": _("PAKD trạng thái"), "fieldname": "pakd_state", "fieldtype": "Data", "width": 130},
		{"label": _("Hợp đồng"), "fieldname": "contract", "fieldtype": "Link",
		 "options": "DCNet Contract", "width": 140},
		{"label": _("Loại"), "fieldname": "kind", "fieldtype": "Data", "width": 150},
		{"label": _("Người nhận"), "fieldname": "recipient_name", "fieldtype": "Data", "width": 180},
		{"label": _("MST/CCCD"), "fieldname": "recipient_id", "fieldtype": "Data", "width": 110},
		{"label": _("Tỷ lệ"), "fieldname": "rate_pct", "fieldtype": "Percent", "width": 70},
		{"label": _("Số tiền/kỳ"), "fieldname": "amount_per_period", "fieldtype": "Currency", "width": 130},
		{"label": _("TNCN"), "fieldname": "pit_amount", "fieldtype": "Currency", "width": 100},
		{"label": _("Net"), "fieldname": "net_amount", "fieldtype": "Currency", "width": 130},
		{"label": _("Chu kỳ"), "fieldname": "recurrence", "fieldtype": "Data", "width": 90},
		{"label": _("Khách hàng"), "fieldname": "customer", "fieldtype": "Link",
		 "options": "Customer", "width": 180},
	]


def _query(filters):
	conditions = ["bl.state = 'Pending'"]
	args = []
	# Only show beneficiaries whose contract has at least 1 Paid BS row
	# (cash-basis posting rule).
	conditions.append("""EXISTS (
		SELECT 1 FROM `tabDCNet Contract Billing Schedule` bs
		WHERE bs.parent = p.contract_ref AND bs.state = 'Paid'
	)""")
	if filters.get("pakd"):
		conditions.append("bl.parent = %s")
		args.append(filters["pakd"])
	if filters.get("kind"):
		conditions.append("bl.kind = %s")
		args.append(filters["kind"])
	if filters.get("with_recipient_only"):
		conditions.append("bl.recipient_name IS NOT NULL AND bl.recipient_name != ''")

	where = " AND ".join(conditions)
	return frappe.db.sql(
		f"""
		SELECT
			bl.parent AS pakd,
			p.workflow_state AS pakd_state,
			p.contract_ref AS contract,
			bl.kind,
			bl.recipient_name,
			bl.recipient_id,
			bl.rate_pct,
			bl.amount_per_period,
			bl.pit_amount,
			bl.net_amount,
			bl.recurrence,
			p.customer
		FROM `tabPAKD Beneficiary Line` bl
		JOIN `tabPhuong An Kinh Doanh` p ON p.name = bl.parent
		WHERE {where}
		ORDER BY bl.kind, bl.parent
		""",
		args,
		as_dict=True,
	)
