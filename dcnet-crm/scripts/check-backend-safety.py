"""Static release guard for high-risk Frappe API patterns."""

from pathlib import Path


API_PATH = Path("dcnet_crm/api.py")
SOURCE = API_PATH.read_text(encoding="utf-8")

violations = []
if "allow_guest=True" in SOURCE:
    violations.append("Public guest API detected")

for function_name in (
    "create_so_action",
    "create_sales_order",
    "save_care_card",
    "update_sales_order",
    "update_so_items",
):
    marker = f"def {function_name}("
    start = SOURCE.index(marker)
    next_function = SOURCE.find("\ndef ", start + len(marker))
    next_whitelist = SOURCE.find("\n@frappe.whitelist", start + len(marker))
    boundaries = [value for value in (next_function, next_whitelist) if value >= 0]
    end = min(boundaries) if boundaries else len(SOURCE)
    body = SOURCE[start:end]
    for forbidden in ("ignore_validate", "ignore_mandatory", "frappe.db.commit"):
        if forbidden in body:
            violations.append(f"{function_name}: forbidden {forbidden}")

if violations:
    raise SystemExit("\n".join(violations))

print("Backend safety checks passed.")
