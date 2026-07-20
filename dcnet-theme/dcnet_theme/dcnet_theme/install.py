"""DCNET Theme install/migrate hooks — seed presets and generate CSS."""

import frappe


def after_install():
    """Run on first install — seed presets and activate default."""
    frappe.reload_doc("dcnet_theme", "page", "theme_gallery", force=True)
    ensure_desktop_icon_fields()
    seed_presets()
    activate_default_preset()
    generate_active_theme_css()
    ensure_theme_gallery_page()


def after_migrate():
    """Run on every bench migrate — upsert presets and regenerate CSS."""
    if not frappe.db.exists("DocType", "DCNET Theme Settings"):
        return
    ensure_desktop_icon_fields()
    seed_presets()
    if not frappe.db.get_single_value("DCNET Theme Settings", "active_preset"):
        activate_default_preset()
    generate_active_theme_css()
    # Clear bootinfo cache so _inject_custom_labels runs fresh on next login.
    # Needed when new custom fields (e.g. custom_label) are added via migration.
    frappe.cache.delete_key("bootinfo")
    frappe.cache.delete_key("desktop_icons")
    ensure_theme_gallery_page()


def seed_presets():
    """Upsert all preset definitions from presets.py."""
    from dcnet_theme.dcnet_theme.presets import PRESETS

    if not frappe.db.table_exists("DCNET Theme Preset"):
        frappe.db.updatedb("DCNET Theme Preset")

    for preset_data in PRESETS:
        key = preset_data["preset_key"]
        try:
            if frappe.db.exists("DCNET Theme Preset", key):
                doc = frappe.get_doc("DCNET Theme Preset", key)
                doc.update(preset_data)
                doc.save(ignore_permissions=True)
            else:
                doc = frappe.get_doc({"doctype": "DCNET Theme Preset", **preset_data})
                doc.insert(ignore_permissions=True)
        except Exception as e:
            frappe.log_error(f"DCNET Theme: Failed to seed preset {key}: {e}")

    frappe.db.commit()

def ensure_theme_gallery_page():
    """Ensure Theme Gallery page exists even when page sync is skipped."""
    if frappe.db.exists("Page", "theme-gallery"):
        return

    try:
        frappe.get_doc(
            {
                "doctype": "Page",
                "page_name": "theme-gallery",
                "title": "Theme Gallery",
                "module": "DCNet Theme",
                "standard": "No",
                "system_page": 0,
            }
        ).insert(ignore_permissions=True)
        frappe.db.commit()
    except Exception as e:
        frappe.log_error(f"DCNET Theme: Failed to create theme-gallery page: {e}")
        
def activate_default_preset():
    """Set 'default' as the active preset if none is set."""
    if frappe.db.exists("DCNET Theme Preset", "default"):
        settings = frappe.get_single("DCNET Theme Settings")
        settings.active_preset = "default"
        settings.save(ignore_permissions=True)
        frappe.db.commit()


def generate_active_theme_css():
    """Generate CSS file from the active preset."""
    try:
        settings = frappe.get_single("DCNET Theme Settings")
        if settings.active_preset:
            from dcnet_theme.dcnet_theme.theme_utils import generate_and_write_css

            generate_and_write_css(settings)
    except Exception as e:
        frappe.log_error(f"DCNET Theme: Failed to generate CSS on migrate: {e}")


def ensure_desktop_icon_fields():
    """Create Desktop Icon custom fields and property setters if not present.

    Fixtures run at the same time as migrate, so on a fresh install the fixture
    import may not have run yet when after_migrate fires.  This function is the
    programmatic fallback that guarantees the fields exist regardless of fixture
    import order.

    Fields created:
      custom_label  — Data field after 'label', lets admins override icon title
      icon_color    — Color picker after 'icon', sets SVG stroke colour

    Property Setters applied:
      bg_color fieldtype → Color   (replaces the 2-option Select with a colour picker)
      bg_color options   → ""      (clears the hard-coded colour list)
    """
    # --- Custom Fields ---
    if not frappe.db.exists("Custom Field", {"dt": "Desktop Icon", "fieldname": "custom_label"}):
        try:
            frappe.get_doc({
                "doctype": "Custom Field",
                "dt": "Desktop Icon",
                "label": "Custom Label",
                "fieldname": "custom_label",
                "fieldtype": "Data",
                "insert_after": "label",
                "translatable": 1,
            }).insert(ignore_permissions=True)
        except Exception as e:
            frappe.log_error(f"DCNET Theme: Failed to create custom_label field: {e}")

    if not frappe.db.exists("Custom Field", {"dt": "Desktop Icon", "fieldname": "icon_color"}):
        try:
            frappe.get_doc({
                "doctype": "Custom Field",
                "dt": "Desktop Icon",
                "label": "Icon Color",
                "fieldname": "icon_color",
                "fieldtype": "Color",
                "insert_after": "icon",
            }).insert(ignore_permissions=True)
        except Exception as e:
            frappe.log_error(f"DCNET Theme: Failed to create icon_color field: {e}")

    # --- Property Setters for bg_color ---
    if not frappe.db.exists("Property Setter", "Desktop Icon-bg_color-fieldtype"):
        try:
            frappe.get_doc({
                "doctype": "Property Setter",
                "name": "Desktop Icon-bg_color-fieldtype",
                "doc_type": "Desktop Icon",
                "doctype_or_field": "DocField",
                "field_name": "bg_color",
                "property": "fieldtype",
                "property_type": "Select",
                "value": "Color",
            }).insert(ignore_permissions=True)
        except Exception as e:
            frappe.log_error(f"DCNET Theme: Failed to set bg_color fieldtype: {e}")

    if not frappe.db.exists("Property Setter", "Desktop Icon-bg_color-options"):
        try:
            frappe.get_doc({
                "doctype": "Property Setter",
                "name": "Desktop Icon-bg_color-options",
                "doc_type": "Desktop Icon",
                "doctype_or_field": "DocField",
                "field_name": "bg_color",
                "property": "options",
                "property_type": "Text",
                "value": "",
            }).insert(ignore_permissions=True)
        except Exception as e:
            frappe.log_error(f"DCNET Theme: Failed to clear bg_color options: {e}")

    frappe.db.commit()
