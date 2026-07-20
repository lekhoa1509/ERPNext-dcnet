# How To: Importing Linked Documents

**Difficulty**: Advanced
**Estimated Time**: 45 minutes
**Tags**: import, linked-documents, relationships

## Overview

Learn how to import documents with relationships to other DocTypes, including Link fields, Dynamic Links, and cascading imports where parent documents must be created before children.

## Prerequisites

- Understanding of Frappe DocType relationships
- Basic Data Import experience
- Knowledge of Link and Dynamic Link fields

## Step-by-Step Guide

### Step 1: Understanding Document Relationships

Frappe has several relationship types:

```
1. Link Field: Direct reference to another DocType
   - Customer -> Territory
   - Sales Order -> Customer

2. Dynamic Link: Reference to any DocType
   - Address -> link_doctype + link_name

3. Child Table: Embedded related documents
   - Sales Order -> Sales Order Item (child)

4. Virtual Link: Computed relationship
   - Journal Entry -> Reference documents
```

### Step 2: Import with Link Field Dependencies

Ensure linked documents exist before importing.

```python
import frappe
from frappe.core.doctype.data_import.importer import Importer

def import_with_link_validation(doctype, file_path):
    """
    Import documents after validating all Link fields exist.
    """
    importer = Importer(doctype, file_path=file_path)
    preview = importer.get_data_for_import_preview()

    # Find Link fields
    meta = frappe.get_meta(doctype)
    link_fields = [df for df in meta.fields if df.fieldtype == "Link"]

    missing_links = []

    for col in preview.columns:
        if col.get("df") and col["df"].fieldtype == "Link":
            link_doctype = col["df"].options
            col_index = col["index"]

            # Check each value
            for i, row in enumerate(preview.data):
                value = row[col_index] if col_index < len(row) else None
                if value and not frappe.db.exists(link_doctype, value):
                    missing_links.append({
                        "row": i + 2,
                        "column": col["header"],
                        "doctype": link_doctype,
                        "value": value
                    })

    if missing_links:
        return {
            "can_import": False,
            "missing_links": missing_links
        }

    # Proceed with import
    import_log = importer.import_data()
    return {"can_import": True, "import_log": import_log}
```

### Step 3: Cascading Import - Create Parents First

Import in dependency order.

```python
import frappe
import csv

def cascading_import(file_paths):
    """
    Import multiple DocTypes in dependency order.

    Args:
        file_paths: Dict of {doctype: file_path} in import order
    """
    # Define dependency order
    import_order = [
        "Territory",      # No dependencies
        "Customer Group", # No dependencies
        "Customer",       # Depends on Territory, Customer Group
        "Item Group",     # No dependencies
        "Item",           # Depends on Item Group
        "Sales Order"     # Depends on Customer, Item
    ]

    results = {}

    for doctype in import_order:
        if doctype in file_paths:
            print(f"Importing {doctype}...")
            result = import_doctype(doctype, file_paths[doctype])
            results[doctype] = result

            if result["failed"] > 0:
                print(f"Warning: {result['failed']} {doctype} failed to import")

    return results

def import_doctype(doctype, file_path):
    """Import a single DocType."""
    from frappe.core.doctype.data_import.importer import Importer

    importer = Importer(doctype, file_path=file_path)
    import_log = importer.import_data()

    success = sum(1 for log in import_log if log.success)
    failed = len(import_log) - success

    return {"success": success, "failed": failed}
```

### Step 4: Import with Auto-Create Missing Links

Automatically create missing linked documents.

```python
import frappe

def import_with_auto_create(doctype, file_path, auto_create_config):
    """
    Import with automatic creation of missing linked documents.

    Args:
        doctype: Main DocType to import
        file_path: Import file path
        auto_create_config: Dict of {link_field: {defaults}} for auto-creation
    """
    import csv

    with open(file_path, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        data = list(reader)

    meta = frappe.get_meta(doctype)

    for row in data:
        # Check and auto-create linked documents
        for df in meta.fields:
            if df.fieldtype == "Link" and df.fieldname in auto_create_config:
                value = row.get(df.fieldname) or row.get(df.label)
                if value and not frappe.db.exists(df.options, value):
                    # Auto-create
                    defaults = auto_create_config[df.fieldname]
                    create_linked_doc(df.options, value, defaults)

        # Now create main document
        row["doctype"] = doctype
        try:
            doc = frappe.get_doc(row)
            doc.insert()
        except Exception as e:
            print(f"Error: {e}")

    frappe.db.commit()

def create_linked_doc(doctype, name, defaults):
    """Create a linked document with defaults."""
    doc_data = {"doctype": doctype}
    doc_data.update(defaults)

    # Set name field based on autoname
    meta = frappe.get_meta(doctype)
    if meta.autoname and meta.autoname.startswith("field:"):
        fieldname = meta.autoname.replace("field:", "")
        doc_data[fieldname] = name
    else:
        doc_data["name"] = name

    doc = frappe.get_doc(doc_data)
    doc.insert()
    print(f"Auto-created {doctype}: {doc.name}")

# Usage
auto_create_config = {
    "customer": {
        "customer_type": "Individual",
        "customer_group": "All Customer Groups",
        "territory": "All Territories"
    },
    "territory": {
        "parent_territory": "All Territories"
    }
}

import_with_auto_create("Sales Order", "/path/to/orders.csv", auto_create_config)
```

### Step 5: Import Dynamic Link Documents

Handle Address and Contact with Dynamic Links.

```python
import frappe
import csv

def import_customer_with_contacts(file_path):
    """
    Import customers with associated contacts.

    CSV format:
    Customer Name, Customer Type, Contact First Name, Contact Email, Contact Phone
    """
    with open(file_path, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        data = list(reader)

    for row in data:
        # Create Customer
        customer = frappe.get_doc({
            "doctype": "Customer",
            "customer_name": row["Customer Name"],
            "customer_type": row.get("Customer Type", "Company")
        })
        customer.insert()

        # Create Contact with Dynamic Link
        if row.get("Contact First Name"):
            contact = frappe.get_doc({
                "doctype": "Contact",
                "first_name": row["Contact First Name"],
                "email_id": row.get("Contact Email"),
                "phone": row.get("Contact Phone"),
                "links": [{
                    "link_doctype": "Customer",
                    "link_name": customer.name
                }]
            })
            contact.insert()

            # Set as primary contact
            customer.customer_primary_contact = contact.name
            customer.save()

    frappe.db.commit()
```

### Step 6: Import with Reference Resolution

Import documents that reference each other.

```python
import frappe

def import_with_references(file_path):
    """
    Import documents with cross-references.

    Example: Import Sales Orders that reference Quotations
    """
    import csv

    with open(file_path, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        data = list(reader)

    # First pass: Create all documents with temporary references
    temp_to_real = {}

    for row in data:
        temp_id = row.get("temp_id")
        quotation_ref = row.get("quotation_reference")

        # Create Sales Order
        so = frappe.get_doc({
            "doctype": "Sales Order",
            "customer": row["customer"],
            "transaction_date": row["transaction_date"],
            "items": [{
                "item_code": row["item_code"],
                "qty": row["qty"],
                "rate": row["rate"]
            }]
        })
        so.insert()

        if temp_id:
            temp_to_real[temp_id] = so.name

    # Second pass: Update references
    for row in data:
        temp_id = row.get("temp_id")
        ref_temp_id = row.get("reference_temp_id")

        if temp_id and ref_temp_id and ref_temp_id in temp_to_real:
            real_name = temp_to_real[temp_id]
            ref_real_name = temp_to_real[ref_temp_id]

            frappe.db.set_value(
                "Sales Order",
                real_name,
                "po_no",  # Example reference field
                ref_real_name
            )

    frappe.db.commit()
```

### Step 7: Validate and Report Missing Links

Generate a report of all missing links before import.

```python
import frappe

def validate_links_report(doctype, file_path):
    """
    Generate comprehensive report of missing links.
    """
    import csv

    with open(file_path, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        data = list(reader)
        headers = reader.fieldnames

    meta = frappe.get_meta(doctype)
    link_fields = {df.fieldname: df.options for df in meta.fields if df.fieldtype == "Link"}

    # Also check child tables
    for table_df in meta.get_table_fields():
        child_meta = frappe.get_meta(table_df.options)
        for df in child_meta.fields:
            if df.fieldtype == "Link":
                key = f"{table_df.fieldname}.{df.fieldname}"
                link_fields[key] = df.options

    report = {
        "total_rows": len(data),
        "link_fields_checked": list(link_fields.keys()),
        "missing_by_doctype": {},
        "missing_by_row": []
    }

    for i, row in enumerate(data):
        row_missing = []

        for fieldname, link_doctype in link_fields.items():
            # Get column header that maps to this field
            value = row.get(fieldname) or row.get(fieldname.replace("_", " ").title())

            if value and not frappe.db.exists(link_doctype, value):
                row_missing.append({
                    "field": fieldname,
                    "doctype": link_doctype,
                    "value": value
                })

                # Track by DocType
                if link_doctype not in report["missing_by_doctype"]:
                    report["missing_by_doctype"][link_doctype] = set()
                report["missing_by_doctype"][link_doctype].add(value)

        if row_missing:
            report["missing_by_row"].append({
                "row": i + 2,
                "missing": row_missing
            })

    # Convert sets to lists for JSON serialization
    for dt in report["missing_by_doctype"]:
        report["missing_by_doctype"][dt] = list(report["missing_by_doctype"][dt])

    return report
```

## Complete Example

```python
import frappe
import csv

class LinkedDocumentImporter:
    """
    Import documents with full link handling.
    """

    def __init__(self, doctype, file_path):
        self.doctype = doctype
        self.file_path = file_path
        self.auto_create = {}
        self.link_resolvers = {}
        self.results = {"success": 0, "failed": 0, "auto_created": {}}

    def set_auto_create(self, link_field, defaults):
        """Enable auto-creation for missing links."""
        self.auto_create[link_field] = defaults

    def set_link_resolver(self, link_field, resolver_func):
        """Set custom resolver for link field."""
        self.link_resolvers[link_field] = resolver_func

    def validate_and_report(self):
        """Validate all links and return report."""
        return validate_links_report(self.doctype, self.file_path)

    def resolve_or_create_link(self, fieldname, value, link_doctype):
        """Resolve link or create if configured."""
        if not value:
            return value

        # Check if exists
        if frappe.db.exists(link_doctype, value):
            return value

        # Try custom resolver
        if fieldname in self.link_resolvers:
            resolved = self.link_resolvers[fieldname](value)
            if resolved:
                return resolved

        # Auto-create if configured
        if fieldname in self.auto_create:
            return self.create_link(link_doctype, value, fieldname)

        return value

    def create_link(self, doctype, value, fieldname):
        """Create missing linked document."""
        defaults = self.auto_create[fieldname]

        doc_data = {"doctype": doctype}
        doc_data.update(defaults)

        # Set name/primary field
        meta = frappe.get_meta(doctype)
        if meta.autoname and "field:" in meta.autoname:
            field = meta.autoname.split(":")[-1]
            doc_data[field] = value
        else:
            # Find first Data field
            for df in meta.fields:
                if df.fieldtype == "Data" and df.reqd:
                    doc_data[df.fieldname] = value
                    break

        doc = frappe.get_doc(doc_data)
        doc.insert()

        # Track auto-created
        if doctype not in self.results["auto_created"]:
            self.results["auto_created"][doctype] = []
        self.results["auto_created"][doctype].append(doc.name)

        return doc.name

    def import_data(self):
        """Run the import."""
        with open(self.file_path, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            data = list(reader)

        meta = frappe.get_meta(self.doctype)
        link_fields = {df.fieldname: df.options for df in meta.fields if df.fieldtype == "Link"}

        for i, row in enumerate(data):
            try:
                # Resolve all links
                for fieldname, link_doctype in link_fields.items():
                    if fieldname in row:
                        row[fieldname] = self.resolve_or_create_link(
                            fieldname, row[fieldname], link_doctype
                        )

                # Create document
                row["doctype"] = self.doctype
                doc = frappe.get_doc(row)
                doc.insert()
                self.results["success"] += 1

            except Exception as e:
                self.results["failed"] += 1
                print(f"Row {i+2} error: {e}")

        frappe.db.commit()
        return self.results


# Usage
importer = LinkedDocumentImporter("Sales Order", "/path/to/orders.csv")

# Configure auto-creation
importer.set_auto_create("customer", {
    "customer_type": "Individual",
    "customer_group": "Retail",
    "territory": "Vietnam"
})

# Configure custom resolver
importer.set_link_resolver(
    "customer",
    lambda v: frappe.db.get_value("Customer", {"customer_name": v}, "name")
)

# Validate first
report = importer.validate_and_report()
print(f"Missing links: {report['missing_by_doctype']}")

# Import
results = importer.import_data()
print(f"Imported: {results['success']}, Failed: {results['failed']}")
print(f"Auto-created: {results['auto_created']}")
```

## Next Steps

- [Bulk Import with Background Jobs](../bulk-import-background-jobs/bulk-import-background-jobs.md)
- [Import Validation and Error Handling](../import-validation-error-handling/import-validation-error-handling.md)

---

*Last updated: 2026-02-04*
