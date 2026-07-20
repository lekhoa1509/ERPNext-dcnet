import frappe
from frappe import _
from frappe.utils import getdate, today
from dateutil.relativedelta import relativedelta

def validate_custom_dob(doc, method):
    """Validate date_of_birth for any DocType that has this field."""
    dob = doc.get("custom_date_of_birth")
    if not dob:
        return

    dob = getdate(dob)
    current_date = getdate(today())

    if dob > current_date:
        frappe.throw(_("Date of Birth cannot be in the future."))

    age = relativedelta(current_date, dob).years

    if age < 4 or age > 90:
        frappe.throw(_("Please enter a valid Date of Birth (age between 4 and 90)."))
