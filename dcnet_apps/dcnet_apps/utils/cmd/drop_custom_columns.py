import re
import frappe

# Regex: chỉ cho phép ký tự chữ, số, dấu gạch dưới và khoảng trắng (cho tên DocType)
SAFE_IDENTIFIER_RE = re.compile(r"^[A-Za-z0-9_ ]+$")


def _validate_identifiers(values, label):
    """Validate danh sách identifier để ngăn SQL injection.
    Tên bảng/cột chỉ được chứa chữ cái, số, dấu gạch dưới và khoảng trắng."""
    for v in values:
        if not SAFE_IDENTIFIER_RE.match(v):
            frappe.throw(f"Invalid {label}: '{v}'. Only alphanumeric, underscores, and spaces are allowed.")


# Run with this command:
# bench --site flow.local execute dcnet_apps.utils.cmd.drop_custom_columns.exec_drop_custom_columns --args "[['Lead','Customer'], ['custom_created_at','custom_age']]"
def exec_drop_custom_columns(
    doctypes=("Lead", "Customer"),
    to_drop=("custom_created_at", "custom_age")):
    # Validate input trước khi đưa vào SQL
    _validate_identifiers(doctypes, "doctype")
    _validate_identifiers(to_drop, "column name")

    messages = []

    for doctype in doctypes:
        table_name = f"tab{doctype}"
        # nosemgrep: identifier đã được validate ở trên
        columns = frappe.db.sql(f"DESC `{table_name}`", as_dict=True)
        existing = {c["Field"] for c in columns}

        cols_to_drop = [c for c in to_drop if c in existing]
        if not cols_to_drop:
            messages.append(f"{table_name}: no columns to drop.")
            continue

        for col in cols_to_drop:
            # nosemgrep: identifier đã được validate ở trên
            frappe.db.sql(f"ALTER TABLE `{table_name}` DROP COLUMN `{col}`")

        messages.append(f"{table_name}: dropped {', '.join(cols_to_drop)}")

    frappe.db.commit()
    print("\n".join(messages))
