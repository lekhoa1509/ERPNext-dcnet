# API Reference: Error Handling Classes

**Language**: Python

**Source**: `frappe/core/doctype/data_import/importer.py`

---

## Overview

Error handling in Data Import covers validation errors, parsing errors, and import failures. This reference documents error types, exception handling, and recovery strategies.

## Error Types

### Import Errors

| Error Type | Class | Description |
|------------|-------|-------------|
| Validation Error | `frappe.ValidationError` | Field validation failed |
| Mandatory Error | `frappe.MandatoryError` | Required field missing |
| Link Validation Error | `frappe.LinkValidationError` | Link target doesn't exist |
| Duplicate Entry | `frappe.DuplicateEntryError` | Record already exists |
| Permission Error | `frappe.PermissionError` | User lacks permission |
| Data Error | `frappe.DataError` | Data type mismatch |

### Parse Errors

| Error Type | Description |
|------------|-------------|
| File Format Error | Invalid CSV/Excel format |
| Encoding Error | Character encoding issues |
| Column Mapping Error | Header doesn't match fields |
| Date Parse Error | Invalid date format |

## Exception Handling

### In Importer Class

```python
def import_data(self):
    """Import data with comprehensive error handling."""
    for doc, rows, row_indexes in self.import_file.get_payloads_for_import():
        try:
            self.process_doc(doc)
            self.create_success_log(doc, row_indexes)

        except frappe.ValidationError as e:
            self.create_failure_log(row_indexes, str(e), traceback.format_exc())

        except frappe.DuplicateEntryError as e:
            self.create_failure_log(row_indexes, f"Duplicate entry: {e}", traceback.format_exc())

        except Exception as e:
            self.create_failure_log(row_indexes, str(e), traceback.format_exc())
            if self.console:
                print(f"Error at row {row_indexes}: {e}")
```

### Custom Error Handler

```python
import frappe
from frappe.core.doctype.data_import.importer import Importer

class CustomImporter(Importer):
    def process_doc(self, doc):
        """Override to add custom error handling."""
        try:
            # Pre-process validation
            self.validate_business_rules(doc)

            # Call parent implementation
            super().process_doc(doc)

        except BusinessRuleError as e:
            # Custom error handling
            self.log_business_error(doc, e)
            raise

    def validate_business_rules(self, doc):
        """Custom business validation."""
        if doc.get("doctype") == "Sales Order":
            if doc.get("grand_total", 0) > 1000000:
                raise BusinessRuleError("Order exceeds credit limit")
```

## Error Log Structure

### Import Log Entry

```python
{
    "log_index": 5,
    "success": False,
    "docname": None,
    "messages": [
        "Validation Error",
        "Customer Name is required"
    ],
    "exception": "Traceback (most recent call last):\n  File ...\nfrappe.MandatoryError: ...",
    "row_indexes": "5,6"  # For multi-row documents
}
```

### Warning Structure

```python
{
    "row": 5,
    "col": 2,
    "field": "status",
    "message": "Value 'Invalid' is not a valid option for Status"
}
```

## Error Recovery

### Export Errored Rows

```python
def export_errored_rows(self):
    """Export rows that failed import for correction."""
    errored_row_indexes = set()

    for log in self.data_import.import_log:
        if not log.success:
            indexes = log.row_indexes.split(",") if log.row_indexes else []
            errored_row_indexes.update(int(i) for i in indexes)

    # Build CSV with only errored rows
    csv_data = [self.import_file.header.as_list()]  # Header

    for i, row in enumerate(self.import_file.data):
        if i in errored_row_indexes:
            csv_data.append(row.as_list())

    return csv_data
```

### Retry Failed Import

```python
def retry_failed_rows(data_import_name):
    """
    Retry importing only the failed rows.
    """
    import frappe
    from frappe.core.doctype.data_import.importer import Importer

    data_import = frappe.get_doc("Data Import", data_import_name)

    # Get original importer
    importer = Importer(
        data_import.reference_doctype,
        data_import=data_import
    )

    # Export errored rows
    errored_csv = importer.export_errored_rows()

    if len(errored_csv) <= 1:  # Only header
        return {"message": "No errored rows to retry"}

    # Create new import with errored rows
    from io import StringIO
    import csv

    output = StringIO()
    writer = csv.writer(output)
    writer.writerows(errored_csv)

    # Save as new file and create new import
    file_content = output.getvalue()
    new_file = frappe.get_doc({
        "doctype": "File",
        "file_name": f"retry_{data_import_name}.csv",
        "content": file_content,
        "is_private": 1
    }).insert()

    new_import = frappe.new_doc("Data Import")
    new_import.reference_doctype = data_import.reference_doctype
    new_import.import_type = data_import.import_type
    new_import.import_file = new_file.file_url
    new_import.insert()

    return {"new_import": new_import.name}
```

## Error Messages

### Common Validation Errors

```python
ERROR_MESSAGES = {
    "required": "Value required for {field}",
    "invalid_option": "'{value}' is not a valid option for {field}. Valid options: {options}",
    "link_not_found": "{doctype} '{value}' not found",
    "duplicate": "{doctype} '{value}' already exists",
    "invalid_date": "Cannot parse date '{value}'. Expected format: {format}",
    "invalid_number": "'{value}' is not a valid number for {field}",
    "permission_denied": "Not permitted to create {doctype}",
    "max_length": "Value exceeds maximum length of {max_length} for {field}"
}

def format_error(error_type, **kwargs):
    """Format error message with context."""
    template = ERROR_MESSAGES.get(error_type, "Unknown error")
    return template.format(**kwargs)
```

### Localized Error Messages

```python
import frappe

def get_localized_error(error_type, **kwargs):
    """Get localized error message."""
    from frappe import _

    messages = {
        "required": _("Value required for {0}").format(kwargs.get("field")),
        "invalid_option": _("'{0}' is not a valid option for {1}").format(
            kwargs.get("value"), kwargs.get("field")
        ),
        "link_not_found": _("{0} '{1}' not found").format(
            kwargs.get("doctype"), kwargs.get("value")
        )
    }

    return messages.get(error_type, _("Unknown error"))
```

## Bulk Error Analysis

### Analyze Import Failures

```python
def analyze_import_errors(data_import_name):
    """
    Analyze and categorize all import errors.
    """
    import frappe
    from collections import Counter

    logs = frappe.get_all(
        "Data Import Log",
        filters={"parent": data_import_name, "success": 0},
        fields=["messages", "exception"]
    )

    error_types = Counter()
    field_errors = Counter()

    for log in logs:
        messages = frappe.parse_json(log.messages or "[]")
        for msg in messages:
            msg_lower = msg.lower()

            # Categorize error type
            if "required" in msg_lower or "mandatory" in msg_lower:
                error_types["Missing Required Field"] += 1
            elif "not found" in msg_lower or "does not exist" in msg_lower:
                error_types["Invalid Link Reference"] += 1
            elif "duplicate" in msg_lower:
                error_types["Duplicate Entry"] += 1
            elif "option" in msg_lower or "invalid value" in msg_lower:
                error_types["Invalid Option/Value"] += 1
            elif "permission" in msg_lower:
                error_types["Permission Error"] += 1
            else:
                error_types["Other"] += 1

            # Extract field name if present
            import re
            field_match = re.search(r"field ['\"]?(\w+)['\"]?", msg_lower)
            if field_match:
                field_errors[field_match.group(1)] += 1

    return {
        "error_types": dict(error_types),
        "field_errors": dict(field_errors),
        "total_errors": len(logs)
    }
```

### Generate Error Report

```python
def generate_error_report(data_import_name):
    """
    Generate comprehensive error report.
    """
    import frappe

    data_import = frappe.get_doc("Data Import", data_import_name)
    analysis = analyze_import_errors(data_import_name)

    report = []
    report.append(f"# Import Error Report: {data_import_name}")
    report.append(f"\n## Summary")
    report.append(f"- DocType: {data_import.reference_doctype}")
    report.append(f"- Total Rows: {data_import.payload_count}")
    report.append(f"- Failed Rows: {analysis['total_errors']}")
    report.append(f"- Success Rate: {100 - (analysis['total_errors'] / data_import.payload_count * 100):.1f}%")

    report.append(f"\n## Error Categories")
    for error_type, count in analysis["error_types"].items():
        report.append(f"- {error_type}: {count}")

    report.append(f"\n## Most Problematic Fields")
    for field, count in sorted(analysis["field_errors"].items(), key=lambda x: -x[1])[:10]:
        report.append(f"- {field}: {count} errors")

    report.append(f"\n## Detailed Errors")
    for log in data_import.import_log[:20]:  # First 20
        if not log.success:
            report.append(f"\n### Row {log.log_index}")
            messages = frappe.parse_json(log.messages or "[]")
            for msg in messages:
                report.append(f"- {msg}")

    return "\n".join(report)
```

## Usage Examples

### Handle Import with Detailed Errors

```python
import frappe
from frappe.core.doctype.data_import.importer import Importer

def safe_import(doctype, file_path):
    """
    Import with comprehensive error handling.
    """
    errors = []
    warnings = []

    try:
        importer = Importer(doctype, file_path=file_path, console=True)

        # Get preview first
        preview = importer.get_data_for_import_preview()
        warnings.extend(preview.warnings)

        # Check for critical warnings
        critical = [w for w in warnings if w.get("level") == "error"]
        if critical:
            return {
                "success": False,
                "errors": critical,
                "warnings": warnings
            }

        # Run import
        import_log = importer.import_data()

        # Analyze results
        success_count = sum(1 for log in import_log if log.success)
        failure_count = len(import_log) - success_count

        return {
            "success": failure_count == 0,
            "imported": success_count,
            "failed": failure_count,
            "warnings": warnings,
            "errors": [log for log in import_log if not log.success]
        }

    except frappe.ValidationError as e:
        errors.append({"type": "validation", "message": str(e)})
    except Exception as e:
        errors.append({"type": "system", "message": str(e)})

    return {
        "success": False,
        "errors": errors,
        "warnings": warnings
    }
```

## Related References

- [Importer](importer.md) - Main import class
- [Data Import Log](data_import_log.md) - Log DocType
- [Validation Utils](validation_utils.md) - Validation functions

---

*Source: frappe/core/doctype/data_import/importer.py | Last updated: 2026-02-04*
