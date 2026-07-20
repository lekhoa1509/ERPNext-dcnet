"""DCNET Theme module hooks — independent module for ERPNext Desk theming.

Theme CSS is injected via boot_session (called from root boot.py) instead of
app_include_css, because /files/ URLs have no cache-busting in Frappe.
bootinfo is fetched fresh on every page load, so CSS is always up-to-date.
"""
