"""Tests for DCNET Theme Settings and CSS generation."""

import json
import os
import frappe
from frappe.tests.utils import FrappeTestCase


class TestDCNETThemeSettings(FrappeTestCase):
    def setUp(self):
        """Ensure a test preset exists."""
        if not frappe.db.exists("DCNET Theme Preset", "test-css"):
            frappe.get_doc({
                "doctype": "DCNET Theme Preset",
                "preset_name": "CSS Test",
                "preset_key": "test-css",
                "primary_color": "#da251d",
                "accent_color": "#ffcd00",
                "text_color": "#1a1a2e",
                "border_color": "#e5e7eb",
                "font_family": "'Inter', sans-serif",
                "heading_font_family": "'Inter', sans-serif",
                "font_size_base": "13px",
                "heading_weight": "600",
                "line_height": "1.5",
                "border_radius": "6px",
                "card_shadow": "0 1px 3px rgba(0,0,0,0.06)",
                "spacing_unit": "16px",
                "google_font_url": "https://fonts.googleapis.com/css2?family=Inter&display=swap",
                "component_styles": json.dumps({
                    "sidebar": {"bg": "#1a1a2e", "text": "#e0e0e0", "active_bg": "#da251d", "active_text": "#fff"},
                    "navbar": {"bg": "#ffffff", "text": "#111827", "height": "50px"},
                    "buttons_primary": {"bg": "#da251d", "text": "#ffffff", "border_radius": "6px"},
                }),
                "dark_component_styles": json.dumps({
                    "sidebar": {"bg": "#0f0f1a", "text": "#a0a0a0", "active_bg": "#b71c1c", "active_text": "#fff"},
                    "navbar": {"bg": "#1a1a2e", "text": "#e0e0e0", "height": "50px"},
                }),
                "custom_css": "/* test preset css */",
                "is_system": 0,
            }).insert(ignore_permissions=True)

    def tearDown(self):
        if frappe.db.exists("DCNET Theme Preset", "test-css"):
            frappe.delete_doc("DCNET Theme Preset", "test-css", force=True)

    def test_generate_css_produces_output(self):
        """CSS generation should produce non-empty CSS string."""
        from dcnet_theme.dcnet_theme.theme_utils import generate_theme_css

        preset = frappe.get_doc("DCNET Theme Preset", "test-css")
        settings = frappe.get_single("DCNET Theme Settings")
        settings.active_preset = "test-css"

        css = generate_theme_css(preset, settings)

        self.assertIn("--st-primary: #da251d", css)
        self.assertIn("--st-font-family:", css)
        self.assertIn("DCNET Theme: CSS Test", css)

    def test_generate_css_includes_component_selectors(self):
        """Component styles JSON should produce CSS selectors."""
        from dcnet_theme.dcnet_theme.theme_utils import generate_theme_css

        preset = frappe.get_doc("DCNET Theme Preset", "test-css")
        settings = frappe.get_single("DCNET Theme Settings")

        css = generate_theme_css(preset, settings)

        self.assertIn(".layout-side-section", css)
        self.assertIn(".standard-sidebar-item.selected", css)
        self.assertIn("header.navbar", css)
        self.assertIn(".btn-primary", css)

    def test_generate_css_includes_google_font(self):
        """Google Font URL should be included as @import."""
        from dcnet_theme.dcnet_theme.theme_utils import generate_theme_css

        preset = frappe.get_doc("DCNET Theme Preset", "test-css")
        settings = frappe.get_single("DCNET Theme Settings")

        css = generate_theme_css(preset, settings)

        self.assertIn("@import url(", css)
        self.assertIn("fonts.googleapis.com", css)

    def test_generate_css_dark_mode(self):
        """Dark mode should include dark component styles."""
        from dcnet_theme.dcnet_theme.theme_utils import generate_theme_css

        preset = frappe.get_doc("DCNET Theme Preset", "test-css")
        settings = frappe.get_single("DCNET Theme Settings")
        settings.dark_mode = 1

        css = generate_theme_css(preset, settings)

        self.assertIn("Dark Mode", css)
        self.assertIn("#0f0f1a", css)  # dark sidebar bg

    def test_generate_css_includes_custom_css(self):
        """Custom CSS from preset and settings should be appended."""
        from dcnet_theme.dcnet_theme.theme_utils import generate_theme_css

        preset = frappe.get_doc("DCNET Theme Preset", "test-css")
        settings = frappe.get_single("DCNET Theme Settings")
        settings.custom_css_override = "/* site override */"

        css = generate_theme_css(preset, settings)

        self.assertIn("/* test preset css */", css)
        self.assertIn("/* site override */", css)

    def test_generate_css_includes_scoped_transitions(self):
        """Transitions should be scoped to specific selectors."""
        from dcnet_theme.dcnet_theme.theme_utils import generate_theme_css

        preset = frappe.get_doc("DCNET Theme Preset", "test-css")
        settings = frappe.get_single("DCNET Theme Settings")

        css = generate_theme_css(preset, settings)

        self.assertIn("transition:", css)
        self.assertIn("header.navbar", css)
        self.assertNotIn("* {", css)  # NOT universal selector

    def test_malformed_json_raises(self):
        """Malformed component_styles JSON should raise error."""
        from dcnet_theme.dcnet_theme.theme_utils import generate_theme_css

        preset = frappe.get_doc("DCNET Theme Preset", "test-css")
        preset.component_styles = "{ invalid json }"
        settings = frappe.get_single("DCNET Theme Settings")

        with self.assertRaises(frappe.ValidationError):
            generate_theme_css(preset, settings)

    def test_write_css_file(self):
        """CSS should be written to sites/{site}/public/files/."""
        from dcnet_theme.dcnet_theme.theme_utils import generate_and_write_css

        settings = frappe.get_single("DCNET Theme Settings")
        settings.active_preset = "test-css"

        generate_and_write_css(settings)

        file_path = frappe.get_site_path("public", "files", "dcnet_theme.css")
        self.assertTrue(os.path.exists(file_path))

        with open(file_path, "r") as f:
            content = f.read()
        self.assertIn("--st-primary: #da251d", content)

    def test_seed_presets_idempotent(self):
        """Running seed_presets twice should produce the same result."""
        from dcnet_theme.dcnet_theme.install import seed_presets

        seed_presets()
        count_1 = frappe.db.count("DCNET Theme Preset", {"is_system": 1})

        seed_presets()
        count_2 = frappe.db.count("DCNET Theme Preset", {"is_system": 1})

        self.assertEqual(count_1, count_2)
        self.assertEqual(count_1, 7)  # 7 nation presets

    def test_export_import_roundtrip(self):
        """Export → Import should produce identical preset data."""
        preset_before = frappe.get_doc("DCNET Theme Preset", "test-css")
        original_primary = preset_before.primary_color

        # Simulate export
        export_data = {
            "dcnet_theme_version": "1.0",
            "preset": {
                "preset_name": "Roundtrip Test",
                "preset_key": "roundtrip-test",
                "primary_color": original_primary,
                "accent_color": preset_before.accent_color,
                "component_styles": preset_before.component_styles,
            },
            "settings": {},
        }

        # Simulate import
        export_json = json.dumps(export_data)
        data = json.loads(export_json)
        preset_data = data["preset"]

        doc = frappe.get_doc({
            "doctype": "DCNET Theme Preset",
            **preset_data,
            "is_system": 0,
        })
        doc.insert(ignore_permissions=True)

        # Verify
        imported = frappe.get_doc("DCNET Theme Preset", "roundtrip-test")
        self.assertEqual(imported.primary_color, original_primary)

        # Cleanup
        frappe.delete_doc("DCNET Theme Preset", "roundtrip-test", force=True)
