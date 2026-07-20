import frappe
from vn_banking.custom.custom_fields import create_all as _create_custom_fields


def after_install():
    _create_custom_fields()
    _seed_default_settings()
    _ensure_sidebar_links()


def after_migrate():
    _create_custom_fields()
    _seed_default_settings()
    _ensure_sidebar_links()


def _seed_default_settings():
    """Ensure Bank Statement Settings has default match rules wired to the 4 matcher fixtures."""
    if not frappe.db.exists("DocType", "Bank Statement Settings"):
        return
    settings = frappe.get_single("Bank Statement Settings")
    if settings.rules:
        return  # already seeded
    defaults = [
        ("invoice_no", 10),
        ("invoice_amount", 20),
        ("party_amount", 30),
        ("name_amount", 40),
    ]
    for key, prio in defaults:
        if not frappe.db.exists("Bank Matcher Type", key):
            continue
        settings.append("rules", {"rule_key": key, "enabled": 1, "priority": prio})

    # Seed default invoice number patterns if empty
    if not settings.invoice_number_patterns:
        settings.invoice_number_patterns = "\n".join([
            r"ACC-SINV-\d{4}-\d+",
            r"ACC-PINV-\d{4}-\d+",
            r"SI-\d+",
            r"PINV-\d+",
            r"ACC-SI-\d{4}-\d+",
            r"ACC-PI-\d{4}-\d+",
        ])

    settings.save(ignore_permissions=True)
    frappe.db.commit()


def _ensure_sidebar_links():
    """Ensure 'Đối soát ngân hàng' link exists on the VN Accounting sidebar.

    The VN Accounting sidebar fixture already ships this link, so this is a
    safety net for sites where the fixture didn't load (e.g., partial migrate).
    Banking/Invoicing core sidebars are intentionally NOT touched: VN users
    reach bank-reconcile via the VN Accounting sidebar; touching upstream
    sidebars creates fixture leakage into apps/erpnext on every save.
    """
    PAGE_NAME = "bank-reconcile"
    LABEL_VI = "Đối soát sao kê"

    targets = [
        # (sidebar_name, label, after_label_or_section)
        ("VN Accounting", LABEL_VI, None),
    ]

    for sidebar_name, label, after_label in targets:
        if not frappe.db.exists("Workspace Sidebar", sidebar_name):
            continue

        # Check if link already points to our page
        existing = frappe.db.get_value(
            "Workspace Sidebar Item",
            {"parent": sidebar_name, "link_to": PAGE_NAME, "link_type": "Page"},
            "name",
        )
        if existing:
            continue

        # Check if there's an old link to bank-reconciliation (Frappe built-in) → update it
        old_link = frappe.db.get_value(
            "Workspace Sidebar Item",
            {"parent": sidebar_name, "link_to": "bank-reconciliation", "link_type": "Page"},
            "name",
        )
        if old_link:
            frappe.db.set_value("Workspace Sidebar Item", old_link, {
                "link_to": PAGE_NAME,
                "label": label,
            })
            print(f"  ↻ Updated sidebar link in {sidebar_name}: → {PAGE_NAME}")
            continue

        # Add new link
        sidebar = frappe.get_doc("Workspace Sidebar", sidebar_name)
        new_idx = len(sidebar.items) + 1
        if after_label:
            for item in sidebar.items:
                if item.label == after_label:
                    new_idx = item.idx + 1
                    break

        sidebar.append("items", {
            "type": "Link",
            "link_type": "Page",
            "link_to": PAGE_NAME,
            "label": label,
            "idx": new_idx,
        })
        sidebar.save(ignore_permissions=True)
        print(f"  + Added sidebar link in {sidebar_name}: {label} → {PAGE_NAME}")

    frappe.db.commit()
