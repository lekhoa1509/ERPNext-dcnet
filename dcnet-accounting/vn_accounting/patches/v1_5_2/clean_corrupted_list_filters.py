"""Remove corrupted list-view filters from __UserSettings.

Frappe's `frappe.utils.generate_route` flattens an array filter value such as
`["=", 1]` into the literal string `"=,1"`. When that flattened value gets
persisted into a user's saved list filters (`__UserSettings`), the list view
reads `docstatus = "=,1"` as an equality against the literal string "=,1",
matches zero rows, and the broken filter sticks across navigations
(URL shows `docstatus=%3D%2C1`).

The sidebar route_options patch (dcnet_theme sidebar.bundle.js) now JSON-encodes
arrays so new corruption no longer occurs, but stale corrupted filters already
saved before that fix remain. This one-time patch strips them.

Idempotent: re-running finds nothing once cleaned.
"""

import json
import re

import frappe

# A flattened-array filter value looks like "=,1" / "!=,2" / "in,To Bill,..."
# i.e. an operator token immediately followed by a comma.
_FLATTENED = re.compile(r"^(=|!=|>|<|>=|<=|in|not in|like|not like|between),")


def _is_corrupt(flt):
    # flt = [doctype, fieldname, operator, value]
    if not isinstance(flt, list) or len(flt) < 4:
        return False
    value = flt[3]
    return isinstance(value, str) and bool(_FLATTENED.match(value))


def _clean_filter_list(filters):
    """Return (cleaned_list, removed_count)."""
    if not isinstance(filters, list):
        return filters, 0
    kept = [f for f in filters if not _is_corrupt(f)]
    return kept, len(filters) - len(kept)


def execute():
    rows = frappe.db.sql(
        "SELECT user, doctype, `data` FROM `__UserSettings`", as_dict=True
    )
    total_removed = 0
    affected = 0

    for r in rows:
        try:
            data = json.loads(r["data"] or "{}")
        except (ValueError, TypeError):
            continue

        changed = 0

        # top-level filters
        if isinstance(data.get("filters"), list):
            data["filters"], n = _clean_filter_list(data["filters"])
            changed += n

        # List.filters (the common location for saved list filters)
        if isinstance(data.get("List"), dict) and isinstance(
            data["List"].get("filters"), list
        ):
            data["List"]["filters"], n = _clean_filter_list(data["List"]["filters"])
            changed += n

        if changed:
            frappe.db.sql(
                "UPDATE `__UserSettings` SET `data`=%s WHERE user=%s AND doctype=%s",
                (json.dumps(data), r["user"], r["doctype"]),
            )
            total_removed += changed
            affected += 1

    if total_removed:
        frappe.db.commit()
        frappe.clear_cache()

    print(
        f"[clean_corrupted_list_filters] removed {total_removed} corrupted "
        f"filter(s) across {affected} __UserSettings row(s)."
    )
