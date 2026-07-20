"""DCNET Theme Settings controller — generates CSS and updates branding on save."""

import json

import frappe
from frappe.model.document import Document


class DCNETThemeSettings(Document):
    def validate(self):
        """Validate fields before save."""
        self._validate_company_overrides()

    def on_update(self):
        """Generate CSS and update branding when settings change."""
        if self.active_preset:
            self._generate_css()
            self._update_branding()

        # Invalidate Redis CSS caches for all presets (global + per-company)
        self._invalidate_css_caches()
        frappe.clear_cache()

    def _validate_company_overrides(self):
        """Validate company_theme_overrides JSON format."""
        raw = self.company_theme_overrides
        if not raw:
            return

        try:
            overrides = json.loads(raw)
        except json.JSONDecodeError as e:
            frappe.throw(
                f"Company Theme Overrides must be valid JSON: {e}",
                title="Invalid JSON",
            )

        if not isinstance(overrides, dict):
            frappe.throw(
                "Company Theme Overrides must be a JSON object (dict), "
                'e.g. {"Company Name": "preset_key"}',
                title="Invalid Format",
            )

        for company_name, preset_key in overrides.items():
            if not isinstance(preset_key, str):
                frappe.throw(
                    f"Preset value for '{company_name}' must be a string",
                    title="Invalid Format",
                )
            if not frappe.db.exists("Company", company_name):
                frappe.throw(
                    f"Company '{company_name}' does not exist",
                    title="Invalid Company",
                )
            if not frappe.db.exists("DCNET Theme Preset", preset_key):
                frappe.throw(
                    f"Preset '{preset_key}' does not exist (for company '{company_name}')",
                    title="Invalid Preset",
                )

    def _invalidate_css_caches(self):
        """Clear all dcnet_theme_css:* cache keys."""
        # Clear the global preset cache
        if self.active_preset:
            frappe.cache.delete_value(f"dcnet_theme_css:{self.active_preset}")

        # Clear per-company preset caches
        raw = self.company_theme_overrides
        if raw:
            try:
                overrides = json.loads(raw)
                for preset_key in overrides.values():
                    frappe.cache.delete_value(f"dcnet_theme_css:{preset_key}")
            except (json.JSONDecodeError, AttributeError):
                pass

        # Also clear the legacy key for backward compat
        frappe.cache.delete_value("dcnet_theme_css")

    def _generate_css(self):
        """Generate the theme CSS file from active preset."""
        from dcnet_theme.dcnet_theme.theme_utils import generate_and_write_css

        generate_and_write_css(self)

    def _update_branding(self):
        """Update Frappe system branding from DCNET Theme Settings."""
        if self.logo_url:
            frappe.db.set_single_value("Navbar Settings", "app_logo", self.logo_url)
            frappe.db.set_single_value("Website Settings", "app_logo", self.logo_url)

        if self.favicon_url:
            frappe.db.set_single_value("Website Settings", "favicon", self.favicon_url)


@frappe.whitelist()
def export_theme():
    """Export the active theme as a JSON download."""
    import json

    settings = frappe.get_single("DCNET Theme Settings")
    if not settings.active_preset:
        frappe.throw("No active theme to export")

    preset = frappe.get_doc("DCNET Theme Preset", settings.active_preset)

    export_data = {
        "dcnet_theme_version": "1.0",
        "preset": {
            field: getattr(preset, field, None)
            for field in [
                "preset_name", "preset_key", "description", "flag_colors",
                "google_font_url", "primary_color", "accent_color",
                "secondary_color", "dark_color", "light_bg_color",
                "text_color", "muted_text_color", "link_color",
                "border_color", "highlight_color", "font_family",
                "heading_font_family", "font_size_base", "heading_weight",
                "line_height", "border_radius", "card_shadow", "spacing_unit",
                "component_styles", "dark_component_styles", "custom_css",
            ]
        },
        "settings": {
            "dark_mode": settings.dark_mode,
            "custom_css_override": settings.custom_css_override,
            "app_title": settings.app_title,
        },
    }

    frappe.response["filename"] = f"dcnet_theme_{preset.preset_key}.json"
    frappe.response["filecontent"] = json.dumps(export_data, indent=2, ensure_ascii=False)
    frappe.response["type"] = "download"


@frappe.whitelist()
def import_theme():
    """Import a theme from uploaded JSON file."""
    import json

    file_data = frappe.request.data
    if not file_data:
        frappe.throw("No file data received")

    # Size limit: 1MB
    if len(file_data) > 1_000_000:
        frappe.throw("Theme file too large (max 1MB)")

    try:
        data = json.loads(file_data)
    except json.JSONDecodeError as e:
        frappe.throw(f"Invalid JSON: {e}")

    if "dcnet_theme_version" not in data:
        frappe.throw("Invalid theme file: missing dcnet_theme_version")

    if "preset" not in data:
        frappe.throw("Invalid theme file: missing preset data")

    preset_data = data["preset"]
    required_fields = ["preset_name", "preset_key"]
    for field in required_fields:
        if not preset_data.get(field):
            frappe.throw(f"Invalid theme file: missing {field}")

    key = preset_data["preset_key"]

    # Create or update preset
    if frappe.db.exists("DCNET Theme Preset", key):
        doc = frappe.get_doc("DCNET Theme Preset", key)
        doc.update(preset_data)
        doc.is_system = 0  # Imported presets are not system presets
        doc.save(ignore_permissions=True)
        action = "updated"
    else:
        doc = frappe.get_doc({
            "doctype": "DCNET Theme Preset",
            **preset_data,
            "is_system": 0,
        })
        doc.insert(ignore_permissions=True)
        action = "created"

    frappe.db.commit()

    return {
        "message": f"Theme '{preset_data['preset_name']}' {action} successfully",
        "preset_key": key,
        "action": action,
    }


@frappe.whitelist()
def get_preset_preview(preset_name):
    """Return preset color and component data for live preview.

    Args:
        preset_name: Name (primary key) of the DCNET Theme Preset document.

    Returns:
        dict with color fields, component_styles, flag_colors, and description.
    """
    if not frappe.db.exists("DCNET Theme Preset", preset_name):
        frappe.throw(f"Preset '{preset_name}' not found")

    doc = frappe.get_doc("DCNET Theme Preset", preset_name)

    color_fields = [
        "preset_name", "preset_key", "description", "flag_colors",
        "primary_color", "accent_color", "secondary_color",
        "dark_color", "light_bg_color", "text_color",
        "muted_text_color", "link_color", "border_color",
        "highlight_color", "font_family", "heading_font_family",
        "font_size_base", "border_radius", "card_shadow",
    ]

    data = {field: getattr(doc, field, None) for field in color_fields}

    # Parse component_styles JSON for sidebar/navbar/button colors
    raw = getattr(doc, "component_styles", None)
    if raw:
        import json
        try:
            data["component_styles"] = json.loads(raw) if isinstance(raw, str) else raw
        except (json.JSONDecodeError, TypeError):
            data["component_styles"] = {}
    else:
        data["component_styles"] = {}

    return data


@frappe.whitelist()
def activate_preset(preset_key):
    """Activate a preset from the gallery page."""
    if not frappe.db.exists("DCNET Theme Preset", preset_key):
        frappe.throw(f"Preset '{preset_key}' not found")

    settings = frappe.get_single("DCNET Theme Settings")
    settings.active_preset = preset_key
    settings.save(ignore_permissions=True)
    frappe.db.commit()

    return {"message": f"Theme activated: {preset_key}"}
