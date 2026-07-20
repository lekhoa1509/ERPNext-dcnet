"""
Lead to Customer Field Mapping
Copy custom fields from Lead to Customer when converting
"""
import frappe

# Định nghĩa mapping: lead_field -> customer_field
# Thêm các custom fields cần copy ở đây
LEAD_TO_CUSTOMER_FIELD_MAP = {
    "custom_date_of_birth": "custom_date_of_birth",
}


def after_customer_created_from_lead(customer_doc, method=None):
    """
    Hook vào Customer.after_insert để copy custom fields từ Lead.
    Được gọi khi Customer được tạo từ Lead qua make_customer().
    """
    if not customer_doc.lead_name:
        return
    
    try:
        lead = frappe.get_doc("Lead", customer_doc.lead_name)
    except frappe.DoesNotExistError:
        return
    
    updated = False
    
    for lead_field, customer_field in LEAD_TO_CUSTOMER_FIELD_MAP.items():
        lead_value = getattr(lead, lead_field, None)
        if lead_value:
            setattr(customer_doc, customer_field, lead_value)
            updated = True
    
    if updated:
        customer_doc.db_update()
