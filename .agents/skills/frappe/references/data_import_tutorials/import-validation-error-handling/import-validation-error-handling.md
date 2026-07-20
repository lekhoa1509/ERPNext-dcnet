# How To: Import Validation and Error Handling

**Difficulty**: Intermediate
**Estimated Time**: 35 minutes
**Tags**: validation, error-handling, import

## Overview

Learn how to implement comprehensive validation and error handling for data imports. Covers pre-import validation, runtime error handling, and error reporting.

## Prerequisites

- Basic Data Import experience
- Understanding of Frappe validation
- Python programming knowledge

## Validation Strategies

### 1. Pre-Import Validation

```python
import frappe
from frappe.core.doctype.data_import.importer import Importer

def validate_before_import(doctype, file_path):
    """
    Comprehensive pre-import validation.
    """
    importer = Importer(doctype, file_path=file_path)
    preview = importer.get_data_for_import_preview()

    validation_result = {
        "valid": True,
        "errors": [],
        "warnings": preview.warnings,
        "stats": {
            "total_rows": len(preview.data),
            "columns": len(preview.columns)
        }
    }

    # Check for required columns
    required_errors = check_required_columns(doctype, preview.columns)
    validation_result["errors"].extend(required_errors)

    # Check for unmapped columns
    unmapped = [
        col["header"] for col in preview.columns
        if not col.get("df")
    ]
    if unmapped:
        validation_result["warnings"].append({
            "type": "unmapped_columns",
            "columns": unmapped,
            "message": f"Columns will be ignored: {', '.join(unmapped)}"
        })

    # Validate data types
    type_errors = validate_data_types(doctype, preview)
    validation_result["errors"].extend(type_errors)

    # Validate links
    link_errors = validate_link_fields(doctype, preview)
    validation_result["errors"].extend(link_errors)

    validation_result["valid"] = len(validation_result["errors"]) == 0

    return validation_result

def check_required_columns(doctype, columns):
    """Check if all required fields have columns."""
    meta = frappe.get_meta(doctype)
    errors = []

    required_fields = [
        df.fieldname for df in meta.fields
        if df.reqd and df.fieldname not in ["name", "doctype"]
    ]

    mapped_fields = [
        col.get("fieldname") for col in columns
        if col.get("df")
    ]

    for field in required_fields:
        if field not in mapped_fields:
            df = meta.get_field(field)
            errors.append({
                "type": "missing_required",
                "field": field,
                "label": df.label if df else field,
                "message": f"Required field '{df.label if df else field}' not found in import file"
            })

    return errors
```

### 2. Data Type Validation

```python
def validate_data_types(doctype, preview):
    """Validate data types match field types."""
    errors = []

    for col in preview.columns:
        if not col.get("df"):
            continue

        df = col["df"]
        col_index = col["index"]

        for row_idx, row in enumerate(preview.data):
            value = row[col_index] if col_index < len(row) else None
            if not value:
                continue

            error = validate_value_type(value, df, row_idx + 2)
            if error:
                errors.append(error)

    return errors

def validate_value_type(value, df, row_num):
    """Validate a single value against field type."""

    fieldtype = df.fieldtype

    # Numeric fields
    if fieldtype in ["Int", "Float", "Currency", "Percent"]:
        try:
            if fieldtype == "Int":
                int(value)
            else:
                float(str(value).replace(",", ""))
        except ValueError:
            return {
                "type": "invalid_type",
                "row": row_num,
                "field": df.fieldname,
                "value": value,
                "message": f"Row {row_num}: '{value}' is not a valid {fieldtype}"
            }

    # Date fields
    elif fieldtype in ["Date", "Datetime"]:
        from frappe.utils import getdate
        try:
            getdate(value)
        except:
            return {
                "type": "invalid_date",
                "row": row_num,
                "field": df.fieldname,
                "value": value,
                "message": f"Row {row_num}: Cannot parse date '{value}'"
            }

    # Select fields
    elif fieldtype == "Select" and df.options:
        options = df.options.split("\n")
        if value not in options:
            return {
                "type": "invalid_option",
                "row": row_num,
                "field": df.fieldname,
                "value": value,
                "options": options,
                "message": f"Row {row_num}: '{value}' is not a valid option for {df.label}"
            }

    return None
```

### 3. Link Field Validation

```python
def validate_link_fields(doctype, preview):
    """Validate all link field values exist."""
    errors = []
    link_cache = {}

    meta = frappe.get_meta(doctype)

    for col in preview.columns:
        if not col.get("df") or col["df"].fieldtype != "Link":
            continue

        df = col["df"]
        link_doctype = df.options
        col_index = col["index"]

        # Collect all unique values
        values = set()
        for row in preview.data:
            value = row[col_index] if col_index < len(row) else None
            if value:
                values.add(value)

        if not values:
            continue

        # Batch check existence
        cache_key = f"{link_doctype}:{','.join(sorted(values))}"
        if cache_key not in link_cache:
            existing = set(frappe.get_all(
                link_doctype,
                filters={"name": ["in", list(values)]},
                pluck="name"
            ))
            link_cache[cache_key] = existing
        else:
            existing = link_cache[cache_key]

        # Find missing
        missing = values - existing

        # Report errors by row
        if missing:
            for row_idx, row in enumerate(preview.data):
                value = row[col_index] if col_index < len(row) else None
                if value in missing:
                    errors.append({
                        "type": "invalid_link",
                        "row": row_idx + 2,
                        "field": df.fieldname,
                        "value": value,
                        "link_doctype": link_doctype,
                        "message": f"Row {row_idx + 2}: {link_doctype} '{value}' does not exist"
                    })

    return errors
```

### 4. Custom Validation Rules

```python
def add_custom_validation(doctype, validators):
    """
    Add custom validation rules.

    Args:
        doctype: Target DocType
        validators: List of validator functions
    """
    def custom_validate(preview):
        errors = []
        for validator in validators:
            validator_errors = validator(doctype, preview)
            errors.extend(validator_errors)
        return errors

    return custom_validate

# Example validators
def validate_unique_field(field):
    """Create validator for unique field."""
    def validator(doctype, preview):
        errors = []
        values_seen = {}

        col = next(
            (c for c in preview.columns if c.get("fieldname") == field),
            None
        )
        if not col:
            return errors

        col_index = col["index"]

        for row_idx, row in enumerate(preview.data):
            value = row[col_index] if col_index < len(row) else None
            if not value:
                continue

            if value in values_seen:
                errors.append({
                    "type": "duplicate_value",
                    "row": row_idx + 2,
                    "field": field,
                    "value": value,
                    "first_row": values_seen[value],
                    "message": f"Row {row_idx + 2}: Duplicate '{value}' (first at row {values_seen[value]})"
                })
            else:
                values_seen[value] = row_idx + 2

        return errors

    return validator

def validate_email_format(doctype, preview):
    """Validate email fields."""
    import re
    errors = []

    email_pattern = re.compile(r'^[\w\.-]+@[\w\.-]+\.\w+$')

    for col in preview.columns:
        if col.get("fieldname") and "email" in col["fieldname"].lower():
            col_index = col["index"]

            for row_idx, row in enumerate(preview.data):
                value = row[col_index] if col_index < len(row) else None
                if value and not email_pattern.match(value):
                    errors.append({
                        "type": "invalid_email",
                        "row": row_idx + 2,
                        "field": col["fieldname"],
                        "value": value,
                        "message": f"Row {row_idx + 2}: Invalid email format '{value}'"
                    })

    return errors
```

### 5. Error Handling During Import

```python
import frappe
from frappe.core.doctype.data_import.importer import Importer

class ErrorHandlingImporter:
    """Importer with comprehensive error handling."""

    def __init__(self, doctype, file_path):
        self.doctype = doctype
        self.file_path = file_path
        self.errors = []
        self.warnings = []
        self.success = []

    def import_data(self, stop_on_error=False):
        """
        Import with error handling.

        Args:
            stop_on_error: Stop import on first error
        """
        importer = Importer(self.doctype, file_path=self.file_path)
        importer.import_file.parse_data_from_template()

        for doc, rows, indexes in importer.import_file.get_payloads_for_import():
            try:
                # Create document
                frappe_doc = frappe.get_doc(doc)
                frappe_doc.insert()

                self.success.append({
                    "rows": indexes,
                    "name": frappe_doc.name
                })

            except frappe.MandatoryError as e:
                self.handle_error(indexes, "mandatory", str(e))
                if stop_on_error:
                    break

            except frappe.DuplicateEntryError as e:
                self.handle_error(indexes, "duplicate", str(e))
                if stop_on_error:
                    break

            except frappe.LinkValidationError as e:
                self.handle_error(indexes, "invalid_link", str(e))
                if stop_on_error:
                    break

            except frappe.ValidationError as e:
                self.handle_error(indexes, "validation", str(e))
                if stop_on_error:
                    break

            except Exception as e:
                self.handle_error(indexes, "unknown", str(e))
                if stop_on_error:
                    break

        frappe.db.commit()

        return {
            "success": len(self.success),
            "failed": len(self.errors),
            "errors": self.errors,
            "warnings": self.warnings
        }

    def handle_error(self, row_indexes, error_type, message):
        """Handle and categorize error."""
        self.errors.append({
            "rows": row_indexes,
            "type": error_type,
            "message": message
        })
```

### 6. Error Reporting

```python
def generate_error_report(validation_result, format="text"):
    """
    Generate human-readable error report.
    """
    if format == "text":
        return generate_text_report(validation_result)
    elif format == "html":
        return generate_html_report(validation_result)
    elif format == "csv":
        return generate_csv_report(validation_result)

def generate_text_report(result):
    """Generate plain text error report."""
    lines = []
    lines.append("=" * 60)
    lines.append("DATA IMPORT VALIDATION REPORT")
    lines.append("=" * 60)

    lines.append(f"\nTotal Rows: {result['stats']['total_rows']}")
    lines.append(f"Columns: {result['stats']['columns']}")
    lines.append(f"Valid: {'Yes' if result['valid'] else 'No'}")

    if result["errors"]:
        lines.append(f"\n{'='*60}")
        lines.append(f"ERRORS ({len(result['errors'])})")
        lines.append("=" * 60)

        # Group by type
        by_type = {}
        for error in result["errors"]:
            error_type = error.get("type", "unknown")
            if error_type not in by_type:
                by_type[error_type] = []
            by_type[error_type].append(error)

        for error_type, errors in by_type.items():
            lines.append(f"\n{error_type.upper()} ({len(errors)} errors)")
            lines.append("-" * 40)
            for error in errors[:10]:  # Show first 10
                lines.append(f"  Row {error.get('row', '?')}: {error.get('message', '')}")
            if len(errors) > 10:
                lines.append(f"  ... and {len(errors) - 10} more")

    if result["warnings"]:
        lines.append(f"\n{'='*60}")
        lines.append(f"WARNINGS ({len(result['warnings'])})")
        lines.append("=" * 60)
        for warning in result["warnings"]:
            lines.append(f"  - {warning.get('message', warning)}")

    return "\n".join(lines)

def generate_html_report(result):
    """Generate HTML error report."""
    html = """
    <html>
    <head>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            .error { color: red; }
            .warning { color: orange; }
            .success { color: green; }
            table { border-collapse: collapse; width: 100%; }
            th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
            th { background-color: #f4f4f4; }
        </style>
    </head>
    <body>
        <h1>Data Import Validation Report</h1>
        <p>Status: <span class="{status_class}">{status}</span></p>
        <p>Total Rows: {total_rows}</p>

        {errors_section}
        {warnings_section}
    </body>
    </html>
    """.format(
        status_class="success" if result["valid"] else "error",
        status="Valid" if result["valid"] else "Has Errors",
        total_rows=result["stats"]["total_rows"],
        errors_section=format_errors_html(result["errors"]),
        warnings_section=format_warnings_html(result["warnings"])
    )

    return html

def format_errors_html(errors):
    if not errors:
        return ""

    rows = ""
    for error in errors:
        rows += f"""
        <tr>
            <td>{error.get('row', '-')}</td>
            <td>{error.get('type', '-')}</td>
            <td>{error.get('field', '-')}</td>
            <td>{error.get('message', '-')}</td>
        </tr>
        """

    return f"""
    <h2 class="error">Errors ({len(errors)})</h2>
    <table>
        <tr><th>Row</th><th>Type</th><th>Field</th><th>Message</th></tr>
        {rows}
    </table>
    """

def format_warnings_html(warnings):
    if not warnings:
        return ""

    items = "".join(f"<li>{w.get('message', w)}</li>" for w in warnings)
    return f"""
    <h2 class="warning">Warnings ({len(warnings)})</h2>
    <ul>{items}</ul>
    """
```

## Complete Validation Workflow

```python
import frappe

class ImportValidator:
    """Complete import validation workflow."""

    def __init__(self, doctype, file_path):
        self.doctype = doctype
        self.file_path = file_path
        self.custom_validators = []

    def add_validator(self, validator_func):
        """Add custom validator."""
        self.custom_validators.append(validator_func)

    def validate(self):
        """Run complete validation."""
        result = validate_before_import(self.doctype, self.file_path)

        # Run custom validators
        importer = Importer(self.doctype, file_path=self.file_path)
        preview = importer.get_data_for_import_preview()

        for validator in self.custom_validators:
            custom_errors = validator(self.doctype, preview)
            result["errors"].extend(custom_errors)

        result["valid"] = len(result["errors"]) == 0
        return result

    def validate_and_import(self, stop_on_error=False):
        """Validate then import if valid."""
        # Pre-validation
        validation = self.validate()

        if not validation["valid"]:
            return {
                "imported": False,
                "validation": validation,
                "message": "Import cancelled due to validation errors"
            }

        # Proceed with import
        importer = ErrorHandlingImporter(self.doctype, self.file_path)
        import_result = importer.import_data(stop_on_error=stop_on_error)

        return {
            "imported": True,
            "validation": validation,
            "import_result": import_result
        }


# Usage
validator = ImportValidator("Customer", "/path/to/customers.csv")

# Add custom validators
validator.add_validator(validate_email_format)
validator.add_validator(validate_unique_field("customer_name"))

# Validate only
result = validator.validate()
print(generate_text_report(result))

# Or validate and import
result = validator.validate_and_import(stop_on_error=False)
if result["imported"]:
    print(f"Imported: {result['import_result']['success']}")
```

## Next Steps

- [Bulk Import with Background Jobs](../bulk-import-background-jobs/bulk-import-background-jobs.md)
- [Rollback and Recovery](../rollback-recovery/rollback-recovery.md)

---

*Last updated: 2026-02-04*
