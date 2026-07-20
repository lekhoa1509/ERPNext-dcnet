import frappe

no_cache = 1


def get_context(context):
    """Context for HTKK list page."""
    context.no_cache = 1
    context.csrf_token = frappe.sessions.get_csrf_token()
    return context
