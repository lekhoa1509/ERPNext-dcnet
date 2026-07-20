"""Per-customer payment delay calculation from historical Payment Entry data.

Calculates median days late (PE.posting_date - SI.due_date) for a customer
over the last 12 months. Used by inflow providers to adjust expected_date
to be more realistic for Vietnamese B2B payments.
"""
import frappe
from datetime import datetime, timedelta


def get_payment_delay(customer, company):
    """Return median payment delay in days for a customer.

    Args:
        customer: Customer name
        company: Company name

    Returns:
        int: median delay days (0 if on-time or no history)
    """
    delays = frappe.db.sql("""
        SELECT DATEDIFF(pe.posting_date, si.due_date) as delay
        FROM `tabPayment Entry Reference` per
        JOIN `tabPayment Entry` pe ON pe.name = per.parent
        JOIN `tabSales Invoice` si ON si.name = per.reference_name
        WHERE per.reference_doctype = 'Sales Invoice'
          AND pe.party_type = 'Customer'
          AND pe.party = %(customer)s
          AND pe.company = %(company)s
          AND pe.docstatus = 1
          AND si.due_date IS NOT NULL
          AND pe.posting_date >= DATE_SUB(CURDATE(), INTERVAL 12 MONTH)
    """, {"customer": customer, "company": company}, as_dict=True)

    if not delays:
        return 0

    values = sorted([max(0, d.delay) for d in delays])
    return values[len(values) // 2]


# In-memory cache per API call (cleared between requests)
_delay_cache = {}


def get_payment_delay_cached(customer, company):
    """Cached version — one DB query per customer per request."""
    key = f"{customer}:{company}"
    if key not in _delay_cache:
        _delay_cache[key] = get_payment_delay(customer, company)
    return _delay_cache[key]


def clear_delay_cache():
    """Call at the start of each forecast API request."""
    global _delay_cache
    _delay_cache = {}


def adjust_expected_date(expected_date_str, customer, company):
    """Adjust expected_date by customer's historical delay.

    Only for inflow — outflow providers should NOT call this.
    Returns: adjusted date as string YYYY-MM-DD.
    """
    delay = get_payment_delay_cached(customer, company)
    if delay <= 0:
        return expected_date_str

    dt = datetime.strptime(expected_date_str, "%Y-%m-%d")
    adjusted = dt + timedelta(days=delay)
    return adjusted.strftime("%Y-%m-%d")
