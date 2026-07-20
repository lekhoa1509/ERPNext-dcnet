"""
DCNET Fixtures Setup - Main orchestration logic for importing sample data

Import Order (dependencies matter):
1. Master Data: Item Groups → Warehouses → Customer/Supplier Groups → Items → Customers → Suppliers
2. CRM Data: Leads → Opportunities
3. Transactions: PO → Stock Entry → SO → DN → SI → PI → PE
4. Accounting: Journal Entries, Employees
"""

import json
import os
from pathlib import Path
from datetime import datetime, timedelta
from random import randint, choice

import frappe
from frappe import _
from frappe.utils import now_datetime, getdate, add_days


# Path to fixtures directory
FIXTURES_DIR = Path(__file__).parent / "fixtures"


# =============================================================================
# MAIN FUNCTIONS
# =============================================================================

def install_all_fixtures(skip_transactions=False):
    """Install all fixtures in correct order"""
    frappe.flags.in_import = True

    try:
        print("\n" + "=" * 60)
        print("DCNET Fixtures Installation")
        print("=" * 60)

        # Step 1: Master Data
        print("\n[1/5] Installing Master Data...")
        install_module("master")

        # Step 2: CRM Data
        print("\n[2/5] Installing CRM Data...")
        install_module("crm")

        if not skip_transactions:
            # Step 3: Transactions
            print("\n[3/5] Installing Transaction Data...")
            install_module("transactions")

            # Step 4: Accounting
            print("\n[4/5] Installing Accounting Data...")
            install_module("accounting")
        else:
            print("\n[3/5] Skipping Transaction Data...")
            print("[4/5] Skipping Accounting Data...")

        # Step 5: Fitting (always install if module exists)
        print("\n[5/5] Installing Fitting Data...")
        install_module("fitting")

        print("\n" + "=" * 60)
        print("Installation Complete!")
        print("=" * 60 + "\n")

    finally:
        frappe.flags.in_import = False


def install_module(module_name):
    """Install fixtures for a specific module"""
    # Special handling for fitting module (uses generator, not JSON)
    if module_name == "fitting":
        install_fitting_module()
        return

    module_dir = FIXTURES_DIR / module_name

    if not module_dir.exists():
        frappe.throw(_(f"Module directory not found: {module_name}"))

    # Get all JSON files sorted by number prefix
    json_files = sorted(module_dir.glob("*.json"))

    for json_file in json_files:
        print(f"  Loading {json_file.name}...")
        data = load_json_file(json_file)

        if isinstance(data, list):
            for record in data:
                create_record(record)
        elif isinstance(data, dict) and "doctype" in data:
            create_record(data)

        frappe.db.commit()


def install_fitting_module():
    """Install Fitting module sample data using generator"""
    try:
        from dcnet_fixtures.dcnet_fixtures.generators.fitting import generate_full_fitting_data
        generate_full_fitting_data(session_count=50, submit=False)
    except ImportError as e:
        print(f"  ⚠️  Fitting generator not found: {e}")
    except Exception as e:
        print(f"  ⚠️  Error installing Fitting data: {str(e)}")


def clear_all_fixtures():
    """Clear all fixtures in reverse order"""
    print("\n" + "=" * 60)
    print("Clearing DCNET Fixtures")
    print("=" * 60)

    # Clear in reverse order of dependencies (fitting first as it depends on customers/leads)
    print("\n[1/5] Clearing Fitting Data...")
    clear_module("fitting")

    print("\n[2/5] Clearing Accounting Data...")
    clear_module("accounting")

    print("\n[3/5] Clearing Transaction Data...")
    clear_module("transactions")

    print("\n[4/5] Clearing CRM Data...")
    clear_module("crm")

    print("\n[5/5] Clearing Master Data...")
    clear_module("master")

    print("\n" + "=" * 60)
    print("Cleared!")
    print("=" * 60 + "\n")


def clear_module(module_name):
    """Clear fixtures for a specific module"""
    # Special handling for fitting module
    if module_name == "fitting":
        clear_fitting_module()
        return

    module_dir = FIXTURES_DIR / module_name

    if not module_dir.exists():
        return

    # Get all JSON files sorted in reverse order
    json_files = sorted(module_dir.glob("*.json"), reverse=True)

    for json_file in json_files:
        print(f"  Clearing {json_file.name}...")
        data = load_json_file(json_file)

        if isinstance(data, list):
            for record in reversed(data):
                delete_record(record)
        elif isinstance(data, dict) and "doctype" in data:
            delete_record(data)

        frappe.db.commit()


def clear_fitting_module():
    """Clear Fitting module sample data"""
    try:
        from dcnet_fixtures.dcnet_fixtures.generators.fitting import clear_fitting_data
        clear_fitting_data()
    except ImportError as e:
        print(f"  ⚠️  Fitting generator not found: {e}")
    except Exception as e:
        print(f"  ⚠️  Error clearing Fitting data: {str(e)}")


def get_fixtures_status():
    """Get current fixtures status"""
    status = {
        "master": {},
        "crm": {},
        "transactions": {},
        "accounting": {},
        "fitting": {}
    }

    # Master data counts
    status["master"]["Item Group"] = frappe.db.count("Item Group", {"name": ["like", "GOLF-%"]})
    status["master"]["Item"] = frappe.db.count("Item", {"item_code": ["like", "GOLF-%"]})
    status["master"]["Customer"] = frappe.db.count("Customer", {"customer_name": ["like", "%Golf%"]}) + \
                                   frappe.db.count("Customer", {"customer_group": ["like", "%Golf%"]})
    status["master"]["Supplier"] = frappe.db.count("Supplier", {"supplier_group": ["like", "%Golf%"]})
    status["master"]["Warehouse"] = frappe.db.count("Warehouse", {"warehouse_name": ["like", "GOLF-%"]})

    # Order Schedule
    try:
        status["master"]["Order Schedule"] = frappe.db.count("Order Schedule")
    except Exception:
        status["master"]["Order Schedule"] = 0

    # CRM counts
    status["crm"]["Lead"] = frappe.db.count("Lead", {"company": ["like", "%Golf%"]})
    status["crm"]["Opportunity"] = frappe.db.count("Opportunity", {"opportunity_from": "Lead"})

    # Transaction counts - count by naming series or date range
    status["transactions"]["Purchase Order"] = frappe.db.count("Purchase Order")
    status["transactions"]["Sales Order"] = frappe.db.count("Sales Order")
    status["transactions"]["Sales Invoice"] = frappe.db.count("Sales Invoice")
    status["transactions"]["Purchase Invoice"] = frappe.db.count("Purchase Invoice")
    status["transactions"]["Payment Entry"] = frappe.db.count("Payment Entry")

    # Accounting counts
    status["accounting"]["Journal Entry"] = frappe.db.count("Journal Entry")
    status["accounting"]["Employee"] = frappe.db.count("Employee")

    # Fitting counts
    try:
        status["fitting"]["Fitting Session"] = frappe.db.count("Fitting Session")
    except Exception:
        status["fitting"]["Fitting Session"] = 0  # DocType may not exist

    return status


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def load_json_file(file_path):
    """Load JSON file and return data"""
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def create_record(data):
    """Create a single record from data dict"""
    # Make a copy to avoid modifying original data
    data = dict(data)

    doctype = data.get("doctype")
    if not doctype:
        return

    try:
        # Check if record already exists
        name_field = get_name_field(doctype, data)
        if name_field and frappe.db.exists(doctype, name_field):
            print(f"    Skipping {doctype}: {name_field} (already exists)")
            return

        # Auto-set company for documents that need it
        if doctype in ["Sales Order", "Purchase Order", "Sales Invoice", "Purchase Invoice",
                       "Delivery Note", "Purchase Receipt", "Payment Entry", "Stock Entry",
                       "Quotation", "Journal Entry", "Lead", "Opportunity"]:
            if "company" not in data or not data["company"]:
                data["company"] = get_company()

        # Handle notes field - remove for doctypes that don't support it
        if doctype in ["Lead", "Opportunity"] and "notes" in data:
            # These doctypes don't have a simple notes field in ERPNext v16
            data.pop("notes", None)

        # Handle Opportunity party_name resolution
        # party_name in fixture uses display name, but needs to be document name
        if doctype == "Opportunity" and data.get("party_name"):
            resolved_name = resolve_opportunity_party_name(
                data.get("opportunity_from"),
                data.get("party_name")
            )
            if resolved_name:
                data["party_name"] = resolved_name
            else:
                print(f"    Error creating {doctype}: {data.get('opportunity_from')} '{data.get('party_name')}' not found")
                return

        # Add default warehouse for items in PO/SO
        if doctype in ["Purchase Order", "Sales Order"] and "items" in data:
            default_warehouse = get_default_warehouse()
            for item in data.get("items", []):
                if "warehouse" not in item and default_warehouse:
                    item["warehouse"] = default_warehouse

        # Create document
        doc = frappe.get_doc(data)
        doc.flags.ignore_permissions = True
        doc.flags.ignore_mandatory = True
        doc.flags.ignore_links = True

        doc.insert(ignore_permissions=True)

        # Submit if submittable
        if doc.meta.is_submittable and data.get("docstatus") == 1:
            doc.submit()

        print(f"    Created {doctype}: {doc.name}")

    except frappe.DuplicateEntryError:
        print(f"    Skipping {doctype}: duplicate entry")
    except Exception as e:
        print(f"    Error creating {doctype}: {str(e)}")
        # Don't raise, continue with other records


def delete_record(data):
    """Delete a single record"""
    doctype = data.get("doctype")
    if not doctype:
        return

    try:
        name_field = get_name_field(doctype, data)
        if name_field and frappe.db.exists(doctype, name_field):
            doc = frappe.get_doc(doctype, name_field)

            # Cancel if submitted
            if doc.docstatus == 1:
                doc.cancel()

            frappe.delete_doc(doctype, name_field, force=True, ignore_permissions=True)
            print(f"    Deleted {doctype}: {name_field}")

    except Exception as e:
        print(f"    Error deleting {doctype}: {str(e)}")


def get_name_field(doctype, data):
    """Get the name/identifier field for a doctype"""
    # Try common name fields
    for field in ["name", "item_code", "customer_name", "supplier_name",
                  "lead_name", "warehouse_name", "employee_name", "category_name"]:
        if field in data:
            return data[field]

    # For doctypes with autoname
    if "naming_series" in data:
        return None  # Will be auto-generated

    return data.get("name")


# =============================================================================
# DATA GENERATION HELPERS
# =============================================================================

def get_random_date(start_date, end_date):
    """Get random date between start and end"""
    if isinstance(start_date, str):
        start_date = getdate(start_date)
    if isinstance(end_date, str):
        end_date = getdate(end_date)

    delta = (end_date - start_date).days
    random_days = randint(0, delta)
    return add_days(start_date, random_days)


def get_company():
    """Get default company"""
    return frappe.db.get_single_value("Global Defaults", "default_company") or \
           frappe.db.get_value("Company", {}, "name")


def get_default_warehouse(company=None):
    """Get default warehouse for company"""
    if not company:
        company = get_company()

    return frappe.db.get_value("Warehouse",
        {"company": company, "is_group": 0},
        "name"
    ) or frappe.db.get_value("Warehouse", {"is_group": 0}, "name")


def resolve_opportunity_party_name(opportunity_from, party_name):
    """
    Resolve party_name from display name to document name.

    In fixtures, party_name uses the display name (e.g., "Hoàng Văn Long"),
    but Opportunity.party_name is a Link field that needs the actual document name
    (e.g., "CRM-LEAD-2026-00001").
    """
    if not opportunity_from or not party_name:
        return None

    # First check if party_name is already a valid document name
    if frappe.db.exists(opportunity_from, party_name):
        return party_name

    if opportunity_from == "Lead":
        # Look up Lead by lead_name (which is first_name + last_name)
        lead_name = frappe.db.get_value("Lead", {"lead_name": party_name}, "name")
        if lead_name:
            return lead_name

        # Try fuzzy match - lead_name might have different format
        # e.g., "Hoàng Văn Long" might be stored as "Hoàng Văn Long" from first_name + last_name
        lead_name = frappe.db.get_value("Lead", {"lead_name": ["like", f"%{party_name}%"]}, "name")
        return lead_name

    elif opportunity_from == "Customer":
        # Look up Customer by customer_name
        customer_name = frappe.db.get_value("Customer", {"customer_name": party_name}, "name")
        if customer_name:
            return customer_name

        # Also check the name field directly (some customers use name = customer_name)
        if frappe.db.exists("Customer", party_name):
            return party_name

        return None

    elif opportunity_from == "Prospect":
        # Look up Prospect by name or company_name
        if frappe.db.exists("Prospect", party_name):
            return party_name
        return frappe.db.get_value("Prospect", {"company_name": party_name}, "name")

    return None
