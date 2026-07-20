# How To: Creating Custom Import Templates

**Difficulty**: Intermediate
**Estimated Time**: 30 minutes
**Tags**: templates, customization, import

## Overview

Learn how to create custom import templates for your DocTypes with specific field selections, custom headers, and pre-filled sample data.

## Prerequisites

- Frappe/ERPNext installed
- Understanding of DocType structure
- Python knowledge for advanced customization

## Step-by-Step Guide

### Step 1: Download Default Template

First, understand the default template structure.

```python
from frappe.core.doctype.data_import.data_import import download_template

# Download blank template
download_template(
    doctype="Customer",
    export_records="blank_template"
)
```

### Step 2: Create Template with Specific Fields

Select only the fields you need.

```python
from frappe.core.doctype.data_import.exporter import Exporter

def create_customer_template():
    """Create custom Customer import template."""
    exporter = Exporter(
        doctype="Customer",
        export_fields={
            "Customer": [
                "customer_name",
                "customer_type",
                "customer_group",
                "territory",
                "tax_id"
            ]
        },
        export_data=False,  # Blank template
        file_type="CSV"
    )

    csv_array = exporter.get_csv_array()
    return csv_array
```

### Step 3: Add Sample Data to Template

Include sample data to guide users.

```python
from frappe.core.doctype.data_import.exporter import Exporter

def create_template_with_samples():
    """Create template with sample data."""
    exporter = Exporter(
        doctype="Customer",
        export_fields={
            "Customer": [
                "customer_name",
                "customer_type",
                "customer_group",
                "territory"
            ]
        },
        export_data=False
    )

    csv_array = exporter.get_csv_array()

    # Add sample rows
    sample_data = [
        ["ACME Corporation", "Company", "Commercial", "Vietnam"],
        ["John Doe", "Individual", "Retail", "Vietnam"],
        ["Golf Pro Shop", "Company", "Commercial", "Ho Chi Minh City"]
    ]

    csv_array.extend(sample_data)

    return csv_array
```

### Step 4: Create Template with Child Tables

Include child table fields.

```python
def create_sales_order_template():
    """Create Sales Order template with Items child table."""
    exporter = Exporter(
        doctype="Sales Order",
        export_fields={
            "Sales Order": [
                "customer",
                "transaction_date",
                "delivery_date",
                "po_no"
            ],
            "Sales Order Item": [
                "item_code",
                "qty",
                "rate",
                "delivery_date"
            ]
        },
        export_data=False
    )

    csv_array = exporter.get_csv_array()

    # Add sample with child rows
    sample_data = [
        ["CUST-001", "2024-01-15", "2024-01-30", "PO-001", "ITEM-001", "10", "1000", "2024-01-25"],
        ["", "", "", "", "ITEM-002", "5", "2000", "2024-01-25"],  # Second item
        ["CUST-002", "2024-01-16", "2024-01-31", "PO-002", "ITEM-003", "20", "500", "2024-01-28"]
    ]

    csv_array.extend(sample_data)

    return csv_array
```

### Step 5: Add Custom Headers

Use custom column headers for user-friendly templates.

```python
def create_template_with_custom_headers():
    """Create template with Vietnamese headers."""
    exporter = Exporter(
        doctype="Customer",
        export_fields={
            "Customer": ["customer_name", "customer_type", "territory", "tax_id"]
        },
        export_data=False
    )

    csv_array = exporter.get_csv_array()

    # Replace headers with Vietnamese
    custom_headers = {
        "Customer Name": "Ten Khach Hang",
        "Customer Type": "Loai Khach Hang",
        "Territory": "Khu Vuc",
        "Tax ID": "Ma So Thue"
    }

    header = csv_array[0]
    new_header = [custom_headers.get(h, h) for h in header]
    csv_array[0] = new_header

    return csv_array
```

### Step 6: Save Template to File

Save the template for distribution.

```python
import csv
from io import StringIO

def save_template_to_file(csv_array, filename):
    """Save template to CSV file."""
    output = StringIO()
    writer = csv.writer(output)
    writer.writerows(csv_array)

    content = output.getvalue()

    # Save to Frappe Files
    file_doc = frappe.get_doc({
        "doctype": "File",
        "file_name": filename,
        "content": content.encode("utf-8"),
        "is_private": 0  # Public for download
    }).insert()

    return file_doc.file_url
```

### Step 7: Create Download Endpoint

Create a whitelisted function for download.

```python
import frappe

@frappe.whitelist()
def download_custom_template(doctype, template_type="blank"):
    """
    Download custom import template.

    Args:
        doctype: Target DocType
        template_type: "blank" or "with_samples"
    """
    from frappe.core.doctype.data_import.exporter import Exporter

    # Get field configuration from settings (customize as needed)
    field_config = get_template_config(doctype)

    exporter = Exporter(
        doctype=doctype,
        export_fields=field_config,
        export_data=(template_type == "with_samples")
    )

    exporter.build_response()

def get_template_config(doctype):
    """Get field configuration for template."""
    configs = {
        "Customer": {
            "Customer": ["customer_name", "customer_type", "customer_group", "territory"]
        },
        "Item": {
            "Item": ["item_code", "item_name", "item_group", "stock_uom", "is_stock_item"]
        },
        "Sales Order": {
            "Sales Order": ["customer", "transaction_date", "delivery_date"],
            "Sales Order Item": ["item_code", "qty", "rate"]
        }
    }

    return configs.get(doctype, "All")
```

## Complete Example

```python
import frappe
import csv
from io import StringIO
from frappe.core.doctype.data_import.exporter import Exporter

class CustomTemplateGenerator:
    """Generate custom import templates."""

    def __init__(self, doctype, company=None):
        self.doctype = doctype
        self.company = company
        self.field_config = self.get_field_config()

    def get_field_config(self):
        """Get field configuration for DocType."""
        # Customize based on DocType
        configs = {
            "Customer": {
                "Customer": [
                    "customer_name", "customer_type", "customer_group",
                    "territory", "tax_id", "default_currency"
                ]
            },
            "Item": {
                "Item": [
                    "item_code", "item_name", "item_group", "stock_uom",
                    "is_stock_item", "is_purchase_item", "is_sales_item"
                ]
            },
            "Sales Order": {
                "Sales Order": [
                    "customer", "transaction_date", "delivery_date",
                    "po_no", "company"
                ],
                "Sales Order Item": [
                    "item_code", "qty", "rate", "delivery_date"
                ]
            }
        }
        return configs.get(self.doctype, "All")

    def generate(self, include_samples=False, vietnamese_headers=False):
        """Generate the template."""
        exporter = Exporter(
            doctype=self.doctype,
            export_fields=self.field_config,
            export_data=include_samples,
            file_type="CSV"
        )

        csv_array = exporter.get_csv_array()

        if vietnamese_headers:
            csv_array = self.apply_vietnamese_headers(csv_array)

        if include_samples and len(csv_array) == 1:
            # No existing data, add samples
            csv_array.extend(self.get_sample_data())

        return csv_array

    def apply_vietnamese_headers(self, csv_array):
        """Replace headers with Vietnamese."""
        translations = {
            "Customer Name": "Ten Khach Hang",
            "Customer Type": "Loai Khach Hang",
            "Customer Group": "Nhom Khach Hang",
            "Territory": "Khu Vuc",
            "Tax ID": "Ma So Thue",
            "Item Code": "Ma San Pham",
            "Item Name": "Ten San Pham",
            "Qty": "So Luong",
            "Rate": "Don Gia"
        }

        header = csv_array[0]
        csv_array[0] = [translations.get(h, h) for h in header]

        return csv_array

    def get_sample_data(self):
        """Get sample data for DocType."""
        samples = {
            "Customer": [
                ["Cong ty TNHH ABC", "Company", "Commercial", "Vietnam", "0123456789", "VND"],
                ["Nguyen Van A", "Individual", "Retail", "Ho Chi Minh City", "", "VND"]
            ],
            "Item": [
                ["ITEM-001", "TaylorMade Driver", "Golf Clubs", "Nos", "1", "1", "1"],
                ["ITEM-002", "Titleist Pro V1", "Golf Balls", "Box", "1", "1", "1"]
            ]
        }
        return samples.get(self.doctype, [])

    def save_to_file(self, filename=None):
        """Save template to file."""
        csv_array = self.generate(include_samples=True)

        if not filename:
            filename = f"{self.doctype.lower().replace(' ', '_')}_template.csv"

        output = StringIO()
        writer = csv.writer(output)
        writer.writerows(csv_array)

        file_doc = frappe.get_doc({
            "doctype": "File",
            "file_name": filename,
            "content": output.getvalue().encode("utf-8"),
            "is_private": 0
        }).insert()

        return file_doc.file_url


# Usage
generator = CustomTemplateGenerator("Customer")
template = generator.generate(include_samples=True, vietnamese_headers=True)
file_url = generator.save_to_file()
print(f"Template saved at: {file_url}")
```

## Next Steps

- [Complex Field Mappings](../complex-field-mappings/complex-field-mappings.md)
- [Importing Linked Documents](../importing-linked-documents/importing-linked-documents.md)
- [Bulk Import with Background Jobs](../bulk-import-background-jobs/bulk-import-background-jobs.md)

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Missing fields | Field not exportable | Check field is not hidden/read-only |
| Wrong column order | Field order in config | Reorder fields in export_fields dict |
| Encoding issues | Non-UTF8 characters | Use UTF-8-BOM encoding |

---

*Last updated: 2026-02-04*
