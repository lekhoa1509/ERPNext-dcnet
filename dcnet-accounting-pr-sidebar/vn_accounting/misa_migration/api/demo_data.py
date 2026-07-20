"""Demo data detection + wipe API.

Phase E commit 1. When a DCNet site has dcnet_sample data already
installed, the Misa migration flow needs a decision point: wipe and
replace, coexist (risky), or migrate into a separate Company.

This module exposes:

  * `detect_demo_data(company=None)` — count dcnet_sample artifacts in
    the target company; consumed by DemoDataDialog.vue.
  * `wipe_demo_data(confirm=...)` — invoke dcnet_sample.setup.teardown_all
    after explicit confirmation. Synchronous (foreground); for a 5-15k
    row teardown this is acceptable but Phase E may move to enqueue.

Detection strategy: dcnet_sample sets `dcnet_sample_data_created='1'` via
`frappe.db.set_default` after a successful `setup_all` and clears it after
`teardown_all`. We use that flag as the canonical truth, complemented by
DocType row counts for visibility.

Safety: wipe_demo_data REQUIRES the literal string "WIPE-DEMO-DATA" as
the confirm arg. Mistyped or omitted → frappe.throw before touching
anything. Phase E may add a server-side delay/cooldown.
"""

from __future__ import annotations

from typing import Any

import frappe
from frappe import _


# DocTypes counted for the dialog. Order = display order in the UI list.
_DEMO_DOCTYPES = (
    "Customer", "Supplier", "Item",
    "Sales Invoice", "Purchase Invoice", "Payment Entry",
    "Journal Entry", "Stock Entry",
    "Project", "Cost Center",
)

_WIPE_CONFIRM_TOKEN = "WIPE-DEMO-DATA"


def _dcnet_sample_installed() -> bool:
    try:
        return "dcnet_sample" in frappe.get_installed_apps()
    except Exception:
        return False


def _demo_flag_set() -> bool:
    """True iff dcnet_sample.setup_all has run (and teardown hasn't)."""
    try:
        return frappe.db.get_default("dcnet_sample_data_created") == "1"
    except Exception:
        return False


def _company_or_default(company: str | None) -> str | None:
    if company:
        return company
    return (
        frappe.defaults.get_global_default("company")
        or frappe.db.get_value("Company", {}, "name")
    )


@frappe.whitelist()
def detect_demo_data(company: str | None = None) -> dict[str, Any]:
    """Detect dcnet_sample data on the target Company.

    Returns:
      {
        "dcnet_sample_installed": bool,
        "demo_flag_set": bool,
        "company": str | None,
        "counts": {DocType: int},
        "total": int,
        "has_demo_data": bool,    # True if installed AND (flag OR counts non-zero)
        "wipe_available": bool,    # True iff installed (function importable)
      }
    """
    company = _company_or_default(company)
    installed = _dcnet_sample_installed()
    flag = _demo_flag_set()

    counts: dict[str, int] = {}
    # company_scoped_total = sum of records that actually live inside the
    # target Company. global_masters_total = Customer/Supplier/Item which
    # are site-wide in ERPNext (no `company` field) and therefore CAN'T
    # be attributed to a specific company. Demo data in those tables only
    # affects this migration if it was seeded against the target company
    # via the company-scoped DocTypes (vouchers, projects, cost centers).
    # If those are all 0, demo data lives on another company and is
    # irrelevant to migrating DCNET TEST.
    company_scoped_total = 0
    global_masters_total = 0
    if company:
        for dt in _DEMO_DOCTYPES:
            try:
                if frappe.get_meta(dt).has_field("company"):
                    n = frappe.db.count(dt, {"company": company})
                    counts[dt] = n
                    company_scoped_total += n
                else:
                    n = frappe.db.count(dt)
                    counts[dt] = n
                    global_masters_total += n
            except Exception:
                counts[dt] = 0

    total = sum(counts.values())
    # has_demo_data = True ONLY when the target company has demo data of
    # its own. Site-wide flag + global masters are informational; they
    # don't block this migration.
    has_demo_data = installed and company_scoped_total > 0

    return {
        "dcnet_sample_installed": installed,
        "demo_flag_set": flag,
        "company": company,
        "counts": counts,
        "total": total,
        "company_scoped_total": company_scoped_total,
        "global_masters_total": global_masters_total,
        "has_demo_data": has_demo_data,
        "wipe_available": installed,
    }


@frappe.whitelist()
def wipe_demo_data(confirm: str = "") -> dict[str, Any]:
    """Wipe dcnet_sample data by calling dcnet_sample.setup.teardown_all.

    Args:
      confirm: must be the literal `_WIPE_CONFIRM_TOKEN`. Anything else
               raises before any teardown work.

    Returns:
      {"wiped": True, "after_counts": {DocType: 0}, "message": "..."}

    The actual teardown is synchronous; a busy site may take 30-120s.
    """
    if confirm != _WIPE_CONFIRM_TOKEN:
        frappe.throw(_("Cần xác nhận với chuỗi {0}").format(_WIPE_CONFIRM_TOKEN))

    if not _dcnet_sample_installed():
        frappe.throw(_("App dcnet_sample chưa được cài đặt — không có gì để xóa."))

    try:
        from dcnet_sample.setup import teardown_all
    except ImportError as exc:
        frappe.throw(_("Không import được dcnet_sample.setup.teardown_all: {0}")
                     .format(str(exc)))

    teardown_all()
    frappe.db.commit()

    after = detect_demo_data()
    return {
        "wiped": True,
        "after_counts": after["counts"],
        "remaining_total": after["total"],
        "demo_flag_set": after["demo_flag_set"],
        "message": _("Đã xóa toàn bộ dữ liệu mẫu. Có thể bắt đầu import Misa."),
    }
