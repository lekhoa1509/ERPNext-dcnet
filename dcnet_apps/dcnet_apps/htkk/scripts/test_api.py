"""
Test script để debug API.
Chạy: bench --site flow.local execute dcnet_apps.htkk.scripts.test_api.run
"""

import frappe
import os


def run():
    # Test frappe.get_app_path
    app_path = frappe.get_app_path("dcnet_apps")
    print(f"App path: {app_path}")

    xsd_path = frappe.get_app_path(
        "dcnet_apps", "htkk", "schemas", "htkk_template", "xsd", "01_GTGT_TT80_283.xsd"
    )
    print(f"XSD path: {xsd_path}")
    print(f"Exists: {os.path.exists(xsd_path)}")

    # List files in directory
    xsd_dir = frappe.get_app_path(
        "dcnet_apps", "htkk", "schemas", "htkk_template", "xsd"
    )
    print(f"\nXSD directory: {xsd_dir}")
    print(f"Dir exists: {os.path.exists(xsd_dir)}")
    if os.path.exists(xsd_dir):
        print(f"Files: {os.listdir(xsd_dir)}")
