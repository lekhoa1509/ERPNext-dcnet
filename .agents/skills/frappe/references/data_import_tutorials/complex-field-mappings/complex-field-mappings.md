# How To: Handling Complex Field Mappings

**Difficulty**: Advanced
**Estimated Time**: 45 minutes
**Tags**: field-mapping, import, customization

## Overview

Learn how to handle complex field mapping scenarios including non-standard headers, multiple child tables, dynamic field mapping, and Link field resolution.

## Prerequisites

- Understanding of Frappe DocType structure
- Basic Data Import experience
- Python programming knowledge

## Step-by-Step Guide

### Step 1: Understanding Field Mapping Basics

Frappe maps columns to fields using these patterns:

```python
# Pattern 1: Field Label
"Customer Name" -> customer_name

# Pattern 2: Fieldname
"customer_name" -> customer_name

# Pattern 3: Child Table with Label
"Item Code (Items)" -> items.item_code

# Pattern 4: Child Table with DocType
"Sales Order Item:item_code" -> items.item_code
```

### Step 2: Custom Column Mapping

Override automatic mapping with explicit configuration.

```python
import frappe
from frappe.core.doctype.data_import.importer import ImportFile

def import_with_custom_mapping(doctype, file_path):
    """Import with custom column to field mapping."""

    # Define custom mapping
    column_mapping = {
        "Cust ID": "customer",
        "Order Date": "transaction_date",
        "Ship Date": "delivery_date",
        "Product": "item_code",
        "Quantity": "qty",
        "Unit Price": "rate"
    }

    import_file = ImportFile(
        doctype=doctype,
        file=file_path,
        template_options={"column_to_field_map": column_mapping}
    )

    import_file.parse_data_from_template()

    # Verify mapping
    for col in import_file.columns:
        print(f"'{col.header}' -> {col.df.fieldname if col.df else 'UNMAPPED'}")

    return import_file
```

### Step 3: Handle Multiple Child Tables

Map fields for DocTypes with multiple child tables.

```python
def map_multiple_child_tables():
    """
    Example: Sales Invoice has Items, Taxes, and Payment Schedule
    """
    column_mapping = {
        # Parent fields
        "Customer": "customer",
        "Posting Date": "posting_date",
        "Due Date": "due_date",

        # Items child table
        "Item Code (Items)": "items.item_code",
        "Qty (Items)": "items.qty",
        "Rate (Items)": "items.rate",

        # Taxes child table
        "Tax Account (Taxes)": "taxes.account_head",
        "Tax Rate (Taxes)": "taxes.rate",

        # Payment Schedule child table
        "Due Date (Payment Schedule)": "payment_schedule.due_date",
        "Amount (Payment Schedule)": "payment_schedule.payment_amount"
    }

    return column_mapping
```

### Step 4: Dynamic Link Field Resolution

Resolve Link fields by alternative identifiers.

```python
import frappe

def resolve_link_by_name_or_code(value, link_doctype, search_fields):
    """
    Resolve link field value by searching multiple fields.

    Args:
        value: Value from CSV
        link_doctype: Target DocType
        search_fields: List of fields to search

    Returns:
        Document name or None
    """
    # Direct match
    if frappe.db.exists(link_doctype, value):
        return value

    # Search by alternative fields
    for field in search_fields:
        result = frappe.db.get_value(
            link_doctype,
            {field: value},
            "name"
        )
        if result:
            return result

    return None

# Usage example
def preprocess_customer_import(data):
    """Preprocess to resolve customer by name or tax_id."""
    for row in data:
        customer_value = row.get("customer")
        resolved = resolve_link_by_name_or_code(
            customer_value,
            "Customer",
            ["customer_name", "tax_id"]
        )
        if resolved:
            row["customer"] = resolved

    return data
```

### Step 5: Handle Nested Field References

Map fields that reference nested structures.

```python
def map_address_fields():
    """
    Map address fields for Customer import.
    Addresses are stored in separate DocType linked via Dynamic Link.
    """
    # Primary address fields in CSV
    address_mapping = {
        "Address Line 1": "address_line1",
        "City": "city",
        "State": "state",
        "Country": "country",
        "Pincode": "pincode"
    }

    return address_mapping

def import_customer_with_address(file_path):
    """Import customers and create linked addresses."""
    import csv

    with open(file_path, "r") as f:
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

        # Create Address if provided
        if row.get("Address Line 1"):
            address = frappe.get_doc({
                "doctype": "Address",
                "address_title": customer.customer_name,
                "address_line1": row["Address Line 1"],
                "city": row.get("City"),
                "state": row.get("State"),
                "country": row.get("Country", "Vietnam"),
                "pincode": row.get("Pincode"),
                "links": [{
                    "link_doctype": "Customer",
                    "link_name": customer.name
                }]
            })
            address.insert()

    frappe.db.commit()
```

### Step 6: Transform Values During Mapping

Apply transformations during import.

```python
def create_value_transformer(transformations):
    """
    Create a value transformer for import.

    Args:
        transformations: Dict of {fieldname: transform_function}
    """
    def transform_row(row):
        for field, transform_func in transformations.items():
            if field in row:
                row[field] = transform_func(row[field])
        return row

    return transform_row

# Define transformations
transformations = {
    "customer_type": lambda v: "Company" if v.lower() in ["company", "corporate", "b2b"] else "Individual",
    "tax_id": lambda v: v.replace("-", "").replace(" ", ""),
    "phone": lambda v: v.replace(" ", "").replace("-", ""),
    "posting_date": lambda v: parse_date(v),
    "grand_total": lambda v: float(v.replace(",", "")) if v else 0
}

transform_row = create_value_transformer(transformations)

# Apply to data
for row in import_data:
    row = transform_row(row)
```

### Step 7: Conditional Field Mapping

Map fields based on values in other columns.

```python
def conditional_mapping(row, doctype):
    """
    Apply conditional field mapping based on row data.
    """
    if doctype == "Item":
        # If is_stock_item, map warehouse fields
        if row.get("is_stock_item") == "1":
            row["default_warehouse"] = row.get("warehouse", "Stores - DC")
            row["valuation_rate"] = row.get("cost", 0)
        else:
            # Service item
            row["is_stock_item"] = 0
            row.pop("default_warehouse", None)

    elif doctype == "Customer":
        # Set default values based on customer_type
        if row.get("customer_type") == "Company":
            row["default_price_list"] = row.get("price_list", "Wholesale")
        else:
            row["default_price_list"] = row.get("price_list", "Retail")

    return row
```

## Complete Example

```python
import frappe
import csv
from frappe.core.doctype.data_import.importer import Importer, ImportFile

class AdvancedImporter:
    """
    Advanced importer with complex field mapping support.
    """

    def __init__(self, doctype, file_path):
        self.doctype = doctype
        self.file_path = file_path
        self.column_map = {}
        self.value_transforms = {}
        self.link_resolvers = {}
        self.errors = []

    def set_column_mapping(self, mapping):
        """Set custom column to field mapping."""
        self.column_map = mapping

    def set_value_transform(self, fieldname, transform_func):
        """Set value transformation for a field."""
        self.value_transforms[fieldname] = transform_func

    def set_link_resolver(self, fieldname, doctype, search_fields):
        """Set link field resolver."""
        self.link_resolvers[fieldname] = {
            "doctype": doctype,
            "search_fields": search_fields
        }

    def resolve_link(self, fieldname, value):
        """Resolve link field value."""
        if not value or fieldname not in self.link_resolvers:
            return value

        config = self.link_resolvers[fieldname]

        # Direct match
        if frappe.db.exists(config["doctype"], value):
            return value

        # Search by alternative fields
        for field in config["search_fields"]:
            result = frappe.db.get_value(
                config["doctype"],
                {field: value},
                "name"
            )
            if result:
                return result

        self.errors.append(f"Could not resolve {fieldname}: {value}")
        return value

    def transform_value(self, fieldname, value):
        """Transform field value."""
        if fieldname in self.value_transforms:
            try:
                return self.value_transforms[fieldname](value)
            except Exception as e:
                self.errors.append(f"Transform error for {fieldname}: {e}")
        return value

    def process_row(self, row):
        """Process a single row with all mappings and transforms."""
        processed = {}

        for col_header, value in row.items():
            # Apply column mapping
            fieldname = self.column_map.get(col_header, col_header)

            # Resolve links
            value = self.resolve_link(fieldname, value)

            # Transform value
            value = self.transform_value(fieldname, value)

            processed[fieldname] = value

        return processed

    def import_data(self):
        """Run the import."""
        with open(self.file_path, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            data = list(reader)

        results = {"success": 0, "failed": 0, "errors": []}

        for i, row in enumerate(data):
            try:
                processed = self.process_row(row)
                processed["doctype"] = self.doctype

                doc = frappe.get_doc(processed)
                doc.insert()

                results["success"] += 1

            except Exception as e:
                results["failed"] += 1
                results["errors"].append({
                    "row": i + 2,  # Account for header
                    "error": str(e)
                })

        frappe.db.commit()

        return results


# Usage example
importer = AdvancedImporter("Sales Order", "/path/to/orders.csv")

# Set column mapping
importer.set_column_mapping({
    "Cust ID": "customer",
    "Order Date": "transaction_date",
    "Ship Date": "delivery_date"
})

# Set link resolver for customer
importer.set_link_resolver(
    "customer",
    "Customer",
    ["customer_name", "tax_id"]
)

# Set value transforms
importer.set_value_transform(
    "transaction_date",
    lambda v: frappe.utils.getdate(v)
)

# Run import
results = importer.import_data()
print(f"Success: {results['success']}, Failed: {results['failed']}")
```

## Next Steps

- [Importing Linked Documents](../importing-linked-documents/importing-linked-documents.md)
- [Import Validation and Error Handling](../import-validation-error-handling/import-validation-error-handling.md)

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Column not mapped | Header doesn't match field | Add to column_to_field_map |
| Link field fails | Value not found in target | Add link resolver with search fields |
| Type conversion error | Invalid value format | Add value transformer |
| Child rows mixed up | Missing parent identifier | Ensure parent key in each row |

---

*Last updated: 2026-02-04*
