import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields


BANK_TRANSACTION_FIELDS = [
    {"fieldname": "bank_statement_import", "label": "Bank Statement Import",
     "fieldtype": "Link", "options": "Bank Statement Import",
     "insert_after": "status", "read_only": 1},
    {"fieldname": "dedupe_hash", "label": "Dedupe Hash",
     "fieldtype": "Data", "insert_after": "bank_statement_import",
     "read_only": 1, "hidden": 1, "unique": 0},
    {"fieldname": "match_confidence", "label": "Match Confidence",
     "fieldtype": "Select", "options": "\nHigh\nMedium\nLow\nNone",
     "insert_after": "dedupe_hash"},
    {"fieldname": "matched_by", "label": "Matched By",
     "fieldtype": "Select",
     "options": "\nInvoice No\nInvoice+Amount\nParty+Amount\nName+Amount\nNameOnly\nManual\nNone",
     "insert_after": "match_confidence"},
    {"fieldname": "suggested_party_type", "label": "Suggested Party Type",
     "fieldtype": "Link", "options": "DocType", "insert_after": "matched_by"},
    {"fieldname": "suggested_party", "label": "Suggested Party",
     "fieldtype": "Dynamic Link", "options": "suggested_party_type",
     "insert_after": "suggested_party_type"},
    {"fieldname": "suggested_invoices", "label": "Suggested Invoices",
     "fieldtype": "Table", "options": "Bank Txn Invoice Suggestion",
     "insert_after": "suggested_party"},
    {"fieldname": "difference_amount", "label": "Difference Amount",
     "fieldtype": "Currency", "insert_after": "suggested_invoices"},
    {"fieldname": "reconcile_notes", "label": "Reconcile Notes",
     "fieldtype": "Small Text", "insert_after": "difference_amount"},
]


BANK_ACCOUNT_FIELDS = [
    {"fieldname": "section_api_v2", "label": "API Sync (v2)",
     "fieldtype": "Section Break", "insert_after": "iban", "collapsible": 1},
    {"fieldname": "api_source", "label": "API Source",
     "fieldtype": "Link", "options": "Bank Data Source",
     "insert_after": "section_api_v2"},
    {"fieldname": "api_credentials", "label": "API Credentials",
     "fieldtype": "Password", "insert_after": "api_source"},
    {"fieldname": "api_config_json", "label": "API Config JSON",
     "fieldtype": "Small Text", "insert_after": "api_credentials"},
    {"fieldname": "api_last_sync_at", "label": "API Last Sync At",
     "fieldtype": "Datetime", "insert_after": "api_config_json", "read_only": 1},
    {"fieldname": "api_last_cursor", "label": "API Last Cursor",
     "fieldtype": "Data", "insert_after": "api_last_sync_at", "read_only": 1},
]


def create_all():
    create_custom_fields({
        "Bank Transaction": BANK_TRANSACTION_FIELDS,
        "Bank Account": BANK_ACCOUNT_FIELDS,
    }, update=True)
