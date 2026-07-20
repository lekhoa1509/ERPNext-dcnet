import frappe
from frappe.utils import nowdate, getdate, get_first_day, get_last_day


@frappe.whitelist()
def get_active_contracts(filters=None):
	return frappe.db.count("DCNet Contract", {"status": "Active", "docstatus": 1})


@frappe.whitelist()
def get_total_monthly_revenue(filters=None):
	today = getdate(nowdate())
	first_day = get_first_day(today)
	last_day = get_last_day(today)
	result = frappe.db.sql("""
		SELECT COALESCE(SUM(bs.amount), 0) as total
		FROM `tabDCNet Contract Billing Schedule` bs
		JOIN `tabDCNet Contract` c ON c.name = bs.parent
		WHERE c.docstatus = 1
		  AND bs.period_start >= %s
		  AND bs.period_end <= %s
		  AND bs.state IN ('Projected', 'Invoiced', 'Paid')
	""", (first_day, last_day), as_dict=True)
	return result[0].total if result else 0


@frappe.whitelist()
def get_overdue_amount(filters=None):
	result = frappe.db.sql("""
		SELECT COALESCE(SUM(bs.amount), 0) as total
		FROM `tabDCNet Contract Billing Schedule` bs
		JOIN `tabDCNet Contract` c ON c.name = bs.parent
		WHERE c.docstatus = 1
		  AND bs.state = 'Overdue'
	""", as_dict=True)
	return result[0].total if result else 0


@frappe.whitelist()
def get_contracts_expiring_this_month(filters=None):
	today = getdate(nowdate())
	first_day = get_first_day(today)
	last_day = get_last_day(today)
	return frappe.db.count("DCNet Contract", {
		"status": "Active",
		"docstatus": 1,
		"end_date": ["between", [first_day, last_day]],
	})


@frappe.whitelist()
def get_overdue_billing_count(filters=None):
	"""Number of billing schedule rows currently in Overdue state across all active contracts."""
	result = frappe.db.sql("""
		SELECT COUNT(*) as cnt
		FROM `tabDCNet Contract Billing Schedule` bs
		JOIN `tabDCNet Contract` c ON c.name = bs.parent
		WHERE c.docstatus = 1 AND bs.state = 'Overdue'
	""", as_dict=True)
	return result[0].cnt if result else 0


@frappe.whitelist()
def get_contracts_outstanding_total(filters=None):
	"""Sum of outstanding amount from Sales Invoices linked to active contracts."""
	result = frappe.db.sql("""
		SELECT COALESCE(SUM(si.outstanding_amount), 0) as total
		FROM `tabSales Invoice` si
		WHERE si.docstatus = 1
		  AND si.outstanding_amount > 0
		  AND si.name IN (
		    SELECT DISTINCT sales_invoice
		    FROM `tabDCNet Contract Billing Schedule`
		    WHERE sales_invoice IS NOT NULL AND sales_invoice != ''
		  )
	""", as_dict=True)
	return result[0].total if result else 0


@frappe.whitelist()
def get_pakd_pending_approval(filters=None):
	"""Count of PAKDs currently awaiting approval at any workflow step."""
	pending_states = [
		"Pending Sales Director",
		"Pending General Dept",
		"Pending Branch Director",
		"Pending Board",
	]
	return frappe.db.count("Phuong An Kinh Doanh", {
		"workflow_state": ["in", pending_states],
	})
