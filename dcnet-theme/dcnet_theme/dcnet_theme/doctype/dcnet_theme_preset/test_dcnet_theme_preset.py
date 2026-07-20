"""Tests for DCNET Theme Preset DocType."""

import json
import frappe
from frappe.tests.utils import FrappeTestCase


class TestDCNETThemePreset(FrappeTestCase):
    def setUp(self):
        """Create a test preset for each test."""
        if not frappe.db.exists("DCNET Theme Preset", "test-preset"):
            frappe.get_doc({
                "doctype": "DCNET Theme Preset",
                "preset_name": "Test Preset",
                "preset_key": "test-preset",
                "description": "Test preset for unit tests",
                "primary_color": "#ff0000",
                "accent_color": "#00ff00",
                "text_color": "#111111",
                "border_color": "#cccccc",
                "font_family": "'Inter', sans-serif",
                "font_size_base": "14px",
                "heading_weight": "600",
                "line_height": "1.5",
                "border_radius": "8px",
                "card_shadow": "0 1px 3px rgba(0,0,0,0.1)",
                "spacing_unit": "16px",
                "component_styles": json.dumps({
                    "sidebar": {
                        "bg": "#1f2937",
                        "text": "#d1d5db",
                        "active_bg": "#ff0000",
                        "active_text": "#ffffff",
                    },
                    "navbar": {
                        "bg": "#ffffff",
                        "height": "50px",
                    },
                }),
                "is_system": 0,
            }).insert(ignore_permissions=True)

    def tearDown(self):
        if frappe.db.exists("DCNET Theme Preset", "test-preset"):
            frappe.delete_doc("DCNET Theme Preset", "test-preset", force=True)

    def test_system_preset_cannot_be_deleted(self):
        """is_system=1 presets should block deletion."""
        doc = frappe.get_doc({
            "doctype": "DCNET Theme Preset",
            "preset_name": "System Test",
            "preset_key": "system-test",
            "is_system": 1,
        })
        doc.insert(ignore_permissions=True)

        with self.assertRaises(frappe.ValidationError):
            frappe.delete_doc("DCNET Theme Preset", "system-test")

        # Cleanup
        frappe.db.set_value("DCNET Theme Preset", "system-test", "is_system", 0)
        frappe.delete_doc("DCNET Theme Preset", "system-test", force=True)

    def test_active_preset_cannot_be_deleted(self):
        """The currently active preset should block deletion."""
        settings = frappe.get_single("DCNET Theme Settings")
        old_active = settings.active_preset
        settings.active_preset = "test-preset"
        settings.save(ignore_permissions=True)

        with self.assertRaises(frappe.ValidationError):
            frappe.delete_doc("DCNET Theme Preset", "test-preset")

        # Restore
        settings.active_preset = old_active
        settings.save(ignore_permissions=True)

    def test_preset_unique_key(self):
        """Duplicate preset_key should raise error."""
        with self.assertRaises(frappe.DuplicateEntryError):
            frappe.get_doc({
                "doctype": "DCNET Theme Preset",
                "preset_name": "Duplicate",
                "preset_key": "test-preset",
            }).insert(ignore_permissions=True)
