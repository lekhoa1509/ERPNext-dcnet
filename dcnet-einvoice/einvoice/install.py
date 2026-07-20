"""Install hooks for the EInvoice app.

Currently provides:
- after_install: idempotent setup — creates the Desktop Icon for the EInvoice
  workspace so users see it on the Desk home page after `bench install-app`.
- after_uninstall: hook stub kept for hooks.py reference (no-op for now).
- after_migrate: re-runs after_install logic so existing sites that were
  installed before this hook existed get their Desktop Icon back.

The hooks.py at this app's root has long pointed to this module
(`einvoice.einvoice.install.after_install`) but the file did not exist,
making the hook silently fail. That's why no Desktop Icon was ever created
on sites running this app. This commit adds the missing module and ties
after_migrate to the same logic so the icon is repaired during a routine
`bench migrate` on already-installed sites.
"""

import frappe


WORKSPACE_NAME = "EInvoice"  # matches Workspace Sidebar.name shipped via fixtures
ICON_LABEL = "EInvoice"      # MUST match WORKSPACE_NAME for Frappe is_permitted lookup
ICON_NAME_VARIANTS = ("EInvoice", "Einvoice", "einvoice")


def _ensure_desktop_icon() -> None:
    """Create the EInvoice Desktop Icon (idempotent, version-aware).

    Frappe `is_permitted` (desk/doctype/desktop_icon/desktop_icon.py:107)
    looks up `bootinfo.workspace_sidebar_item[label.lower()]` — so the
    icon's `label` MUST equal the Workspace Sidebar `name` exactly.

    `link_type` is introspected from the Desktop Icon DocType meta: older
    Frappe builds accept "Workspace" / "External"; v16.17+ flipped — only
    "Workspace Sidebar" / "External". Pick whichever the current build allows.
    """
    if not frappe.db.exists("Workspace Sidebar", WORKSPACE_NAME):
        # Workspace fixture not loaded yet (e.g. install order); skip silently.
        return

    link_type_field = frappe.get_meta("Desktop Icon").get_field("link_type")
    allowed = (link_type_field.options or "").split("\n") if link_type_field else []
    link_type_value = "Workspace Sidebar" if "Workspace Sidebar" in allowed else "Workspace"

    # Drop any legacy variant (case-insensitive, accent-insensitive collation collision)
    for legacy in ICON_NAME_VARIANTS:
        if frappe.db.exists("Desktop Icon", legacy) and legacy != WORKSPACE_NAME:
            try:
                frappe.delete_doc("Desktop Icon", legacy, force=1, ignore_permissions=True)
            except Exception as e:  # pragma: no cover — best-effort cleanup
                print(f"  ⚠ Could not remove legacy Desktop Icon {legacy!r}: {e}")

    if frappe.db.exists("Desktop Icon", WORKSPACE_NAME):
        # Already created on a previous run — make fields canonical and exit.
        doc = frappe.get_doc("Desktop Icon", WORKSPACE_NAME)
        changed = False
        for field, val in (
            ("label", ICON_LABEL),
            ("link_type", link_type_value),
            ("link_to", WORKSPACE_NAME),
            ("hidden", 0),
        ):
            if doc.get(field) != val:
                doc.set(field, val)
                changed = True
        if changed:
            doc.flags.ignore_permissions = True
            doc.save()
            frappe.cache.delete_value("bootinfo")
            frappe.db.commit()
            print(f"  ↻ Desktop Icon: {WORKSPACE_NAME} updated")
        return

    doc = frappe.get_doc({
        "doctype": "Desktop Icon",
        "label": ICON_LABEL,
        "icon": "file",
        "link_type": link_type_value,
        "link_to": WORKSPACE_NAME,
        "standard": 1,
        "hidden": 0,
    })
    doc.flags.ignore_permissions = True
    doc.insert(ignore_if_duplicate=True)
    frappe.cache.delete_value("bootinfo")
    frappe.db.commit()
    print(f"  ✓ Desktop Icon: {WORKSPACE_NAME} (link_type={link_type_value})")


def after_install() -> None:
    """Frappe after_install hook — fires once on `bench install-app einvoice`."""
    _ensure_desktop_icon()


def after_migrate() -> None:
    """Frappe after_migrate hook — re-runs ensure logic on every `bench migrate`,
    so existing sites that pre-date this fix get the Desktop Icon repaired."""
    _ensure_desktop_icon()


def after_uninstall() -> None:
    """Frappe after_uninstall hook — best-effort cleanup of Desktop Icons."""
    for variant in ICON_NAME_VARIANTS:
        if frappe.db.exists("Desktop Icon", variant):
            try:
                frappe.delete_doc("Desktop Icon", variant, force=1, ignore_permissions=True)
            except Exception:  # pragma: no cover
                pass
    frappe.db.commit()
