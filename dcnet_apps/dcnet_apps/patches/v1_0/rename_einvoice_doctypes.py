"""
Rename DCNet E-Invoice DocTypes to EInvoice prefix

This patch runs in pre_model_sync to clean up old references
BEFORE Frappe tries to sync models.

Old Name -> New Name:
- DCNet EInvoice Provider -> EInvoice Provider
- DCNet EInvoice Settings -> EInvoice Settings
- DCNet Inward Invoice -> EInvoice Inward
- DCNet Issuance Log -> EInvoice Issuance Log
- DCNet Sync Log -> EInvoice Sync Log
- Module: DCNet EInvoice -> EInvoice
"""

import frappe


OLD_MODULE = "DCNet EInvoice"
NEW_MODULE = "EInvoice"

OLD_DOCTYPES = [
    "DCNet EInvoice Provider",
    "DCNet EInvoice Settings",
    "DCNet Inward Invoice",
    "DCNet Issuance Log",
    "DCNet Sync Log",
]


def execute():
    """
    Clean up old DCNet EInvoice references before model sync.

    This allows migrate to proceed without errors when the old
    dcnet_einvoice folder no longer exists.
    """

    # Step 1: Delete old Module Def entries
    delete_old_module_defs()

    # Step 2: Delete old DocType entries (they will be recreated with new names)
    delete_old_doctypes()

    # Step 3: Update any remaining references
    update_references()

    frappe.db.commit()
    print("✅ EInvoice rename patch completed")


def delete_old_module_defs():
    """Delete old Module Def entries that reference non-existent folders."""
    old_modules = [
        OLD_MODULE,
        "Barcode ManagementDCNet EInvoice",  # Merge error artifact
    ]

    for module_name in old_modules:
        if frappe.db.exists("Module Def", module_name):
            frappe.db.delete("Module Def", module_name)
            print(f"✅ Deleted Module Def: {module_name}")


def delete_old_doctypes():
    """
    Delete old DocType entries.

    Note: This deletes the DocType definition, not the data tables.
    The new DocTypes will be created fresh by migrate.
    If you have existing data, you'd need a more complex migration.
    """
    for doctype_name in OLD_DOCTYPES:
        if frappe.db.exists("DocType", doctype_name):
            # Delete associated records first
            try:
                # Delete Custom Fields referencing this DocType
                frappe.db.delete("Custom Field", {"dt": doctype_name})

                # Delete Property Setters
                frappe.db.delete("Property Setter", {"doc_type": doctype_name})

                # Delete the DocType itself
                frappe.db.delete("DocType", doctype_name)

                print(f"✅ Deleted DocType: {doctype_name}")
            except Exception as e:
                print(f"⚠️ Error deleting {doctype_name}: {e}")


DOCTYPE_RENAMES = {
    "DCNet Inward Invoice": "EInvoice Inward",
    "DCNet Issuance Log": "EInvoice Issuance Log",
    "DCNet Sync Log": "EInvoice Sync Log",
    "DCNet EInvoice Provider": "EInvoice Provider",
    "DCNet EInvoice Settings": "EInvoice Settings",
}

NUMBER_CARD_RENAMES = {
    "DCNet - HĐ mua vào chưa ghép": "EInvoice - HĐ mua vào chưa ghép",
    "DCNet - HĐ mua vào đã ghép": "EInvoice - HĐ mua vào đã ghép",
    "DCNet - SI chưa xuất HĐ đỏ": "EInvoice - SI chưa xuất HĐ đỏ",
    "DCNet - SI đã xuất HĐ đỏ": "EInvoice - SI đã xuất HĐ đỏ",
}


def update_references():
    """Update any remaining references in other tables."""

    # Update Workspace module references
    try:
        frappe.db.sql("""
            UPDATE `tabWorkspace`
            SET module = %s
            WHERE module = %s
        """, (NEW_MODULE, OLD_MODULE))
    except:
        pass

    # Update Workspace Sidebar module references
    try:
        frappe.db.sql("""
            UPDATE `tabWorkspace Sidebar`
            SET module = %s
            WHERE module = %s
        """, (NEW_MODULE, OLD_MODULE))
    except:
        pass

    # Update Number Card module references
    try:
        frappe.db.sql("""
            UPDATE `tabNumber Card`
            SET module = %s
            WHERE module = %s
        """, (NEW_MODULE, OLD_MODULE))
    except:
        pass

    # Update Report module references
    try:
        frappe.db.sql("""
            UPDATE `tabReport`
            SET module = %s
            WHERE module = %s
        """, (NEW_MODULE, OLD_MODULE))
    except:
        pass

    # Update Workspace Link references to renamed DocTypes
    for old_name, new_name in DOCTYPE_RENAMES.items():
        try:
            frappe.db.sql("""
                UPDATE `tabWorkspace Link`
                SET link_to = %s
                WHERE link_to = %s
            """, (new_name, old_name))
        except:
            pass

    # Update Workspace Shortcut references
    for old_name, new_name in DOCTYPE_RENAMES.items():
        try:
            frappe.db.sql("""
                UPDATE `tabWorkspace Shortcut`
                SET link_to = %s
                WHERE link_to = %s
            """, (new_name, old_name))
        except:
            pass

    # Update Workspace Shortcut stats_filter (dcnet_einvoice_issued -> einvoice_issued)
    try:
        frappe.db.sql("""
            UPDATE `tabWorkspace Shortcut`
            SET stats_filter = REPLACE(stats_filter, 'dcnet_einvoice_issued', 'einvoice_issued')
            WHERE stats_filter LIKE '%dcnet_einvoice_issued%'
        """)
    except:
        pass

    # Update Workspace Number Card references
    for old_name, new_name in NUMBER_CARD_RENAMES.items():
        try:
            frappe.db.sql("""
                UPDATE `tabWorkspace Number Card`
                SET number_card_name = %s
                WHERE number_card_name = %s
            """, (new_name, old_name))
        except:
            pass

    # Delete old Number Cards that reference non-existent DocTypes
    try:
        frappe.db.sql("""
            DELETE FROM `tabNumber Card`
            WHERE document_type = 'DCNet Inward Invoice'
        """)
    except:
        pass

    # Update Custom Field options (Purchase Invoice -> EInvoice Inward)
    try:
        frappe.db.sql("""
            UPDATE `tabCustom Field`
            SET options = 'EInvoice Inward'
            WHERE options = 'DCNet Inward Invoice'
        """)
    except:
        pass

    # Fix workspace visibility
    try:
        frappe.db.sql("""
            UPDATE `tabWorkspace`
            SET is_hidden = 0
            WHERE name = 'EInvoice' AND is_hidden = 1
        """)
    except:
        pass

    print("✅ Updated module references")
