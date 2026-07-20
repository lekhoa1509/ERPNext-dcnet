# HTKK Frontend Page
# Accessible at /htkk

import frappe

no_cache = 1

def get_context(context):
    context.no_cache = 1
    # Không dùng standard layout của Frappe
    context.no_header = 1
    context.no_breadcrumbs = 1
    context.no_sidebar = 1
    context.show_footer = 0

    # Lấy declaration_id từ query string nếu có
    context.declaration_id = frappe.form_dict.get("id", "")

    return context
