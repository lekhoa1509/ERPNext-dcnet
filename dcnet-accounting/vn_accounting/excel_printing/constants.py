"""Shared configuration for Excel print templates."""

SUPPORTED_DOCTYPES = (
    "Asset",
    "Asset Movement",
    "Asset Repair",
    "BOM",
    "Delivery Note",
    "Delivery Trip",
    "Employee Advance",
    "Expense Claim",
    "Job Card",
    "Journal Entry",
    "Material Request",
    "Payment Entry",
    "Purchase Invoice",
    "Purchase Order",
    "Purchase Receipt",
    "Quotation",
    "Request for Quotation",
    "Sales Invoice",
    "Sales Order",
    "Stock Entry",
    "Stock Reconciliation",
    "Subcontracting Order",
    "Subcontracting Receipt",
    "Supplier Quotation",
    "Work Order",
)

WORKBOOK_SCHEMA_VERSION = 1
MAX_IMPORT_BYTES = 20 * 1024 * 1024
MAX_SHEETS = 20
MAX_ROWS = 1000
MAX_COLUMNS = 80

FIELD_GROUPS = {
    "document": (
        "name", "title", "company", "posting_date", "transaction_date",
        "due_date", "customer", "customer_name", "supplier", "supplier_name",
        "party", "party_name", "currency", "conversion_rate", "remarks",
        "contact_display", "address_display", "billing_address", "shipping_address",
    ),
    "totals": (
        "total_qty", "total", "net_total", "total_taxes_and_charges",
        "discount_amount", "grand_total", "rounded_total", "outstanding_amount",
        "in_words", "base_grand_total",
    ),
    "items": (
        "item_code", "item_name", "description", "qty", "uom", "stock_uom",
        "rate", "amount", "net_rate", "net_amount", "warehouse", "batch_no",
        "serial_no", "expense_account", "income_account", "cost_center",
    ),
    "accounting_rows": (
        "account", "party_type", "party", "debit_in_account_currency",
        "credit_in_account_currency", "debit", "credit", "reference_type",
        "reference_name", "user_remark",
    ),
    "payment_references": (
        "reference_doctype", "reference_name", "total_amount", "outstanding_amount",
        "allocated_amount", "exchange_rate",
    ),
    "expense_rows": (
        "expense_type", "description", "amount", "sanctioned_amount",
        "expense_date", "cost_center", "project",
    ),
    "manufacturing_rows": (
        "item_code", "item_name", "source_warehouse", "s_warehouse",
        "target_warehouse", "t_warehouse", "required_qty", "transferred_qty",
        "consumed_qty", "operation", "workstation",
    ),
}
