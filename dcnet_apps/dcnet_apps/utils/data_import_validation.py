"""
Data Import Row Limit Validation for DCNET Apps

Validates that import files do not exceed the maximum row limit (5000 rows)
to ensure system performance and prevent timeouts.
"""

import os

import frappe
from frappe import _

DEFAULT_MAX_IMPORT_ROWS = 5000
MAX_IMPORT_ROWS_CONF_KEY = "dcnet_max_import_rows"
MAX_IMPORT_ROWS_ENV_KEY = "DCNET_MAX_IMPORT_ROWS"


def validate_import_row_limit(doc, method):
    """
    Validate that import file does not exceed maximum row limit.
    
    This hook is applied globally via doc_events on 'Data Import' doctype.
    It runs during the validate event, after Frappe's built-in set_payload_count()
    has determined the number of rows in the import file.
    
    Args:
        doc: Data Import document
        method: Event method name ("validate")
    """
    if not doc.import_file:
        return
    
    max_rows = get_max_import_rows()

    # payload_count is set by DataImport.set_payload_count() before this hook
    if doc.payload_count and doc.payload_count > max_rows:
        frappe.throw(
            _("Import file contains {0} rows which exceeds the maximum limit of {1} rows. Please split your file into smaller batches.").format(
                frappe.bold(doc.payload_count),
                frappe.bold(max_rows)
            ),
            title=_("Import Row Limit Exceeded")
        )


def get_max_import_rows() -> int:
    """Return configured import row limit, falling back to the DCNET default."""
    configured_value = frappe.conf.get(MAX_IMPORT_ROWS_CONF_KEY) or os.environ.get(MAX_IMPORT_ROWS_ENV_KEY)

    if configured_value in (None, ""):
        return DEFAULT_MAX_IMPORT_ROWS

    try:
        max_rows = int(configured_value)
    except (TypeError, ValueError):
        frappe.log_error(
            _("Invalid {0}: {1}. Falling back to {2}.").format(
                MAX_IMPORT_ROWS_CONF_KEY,
                configured_value,
                DEFAULT_MAX_IMPORT_ROWS,
            ),
            "Data Import Row Limit",
        )
        return DEFAULT_MAX_IMPORT_ROWS

    return max_rows if max_rows > 0 else DEFAULT_MAX_IMPORT_ROWS
