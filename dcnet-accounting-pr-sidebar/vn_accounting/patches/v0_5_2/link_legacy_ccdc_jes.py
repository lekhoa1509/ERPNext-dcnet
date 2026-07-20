"""Link legacy CCDC purchase Journal Entries to their parent CCDC Items.

CCDC Items submitted before v1.3.0 had their purchase JE created via the old
`create_ccdc_purchase_je` helper which set `user_remark = "CCDC ghi nhận 242: <item_name> — <name>"`
but did NOT set `parent.posted_je`. This patch reverse-engineers the link by
matching the embedded item name in user_remark to find legacy JE → set
`CCDC Item.posted_je`.

Then re-runs the entries backfill helper (same logic as
backfill_accounting_entries_from_je) to populate inline rows from the JE.

Idempotent: skips items where posted_je is already set.
"""
from __future__ import annotations

import re

import frappe

from vn_accounting.patches.v0_5_2.backfill_accounting_entries_from_je import _backfill_one


_REMARK_RE = re.compile(r"CCDC ghi nhận 242:\s*(\S+)")


def execute() -> None:
    if not frappe.db.exists("DocType", "CCDC Item"):
        return

    items = frappe.db.sql(
        """SELECT name FROM `tabCCDC Item`
           WHERE docstatus = 1 AND (posted_je IS NULL OR posted_je = '')""",
        as_dict=True,
    )
    if not items:
        return

    legacy_jes = frappe.db.sql(
        """SELECT name, user_remark FROM `tabJournal Entry`
           WHERE user_remark LIKE 'CCDC ghi nhận 242:%%' AND docstatus = 1""",
        as_dict=True,
    )
    je_by_item: dict[str, str] = {}
    for je in legacy_jes:
        m = _REMARK_RE.search(je.user_remark or "")
        if m:
            je_by_item.setdefault(m.group(1), je.name)

    linked = 0
    backfilled_rows = 0
    for it in items:
        je_name = je_by_item.get(it.name)
        if not je_name:
            continue
        frappe.db.set_value("CCDC Item", it.name, "posted_je", je_name, update_modified=False)
        linked += 1
        try:
            backfilled_rows += _backfill_one("CCDC Item", it.name, je_name)
        except Exception as exc:
            frappe.log_error(
                f"v0_5_2 link_legacy_ccdc {it.name}: {exc}", "v0_5_2 backfill"
            )

    if linked:
        frappe.db.commit()
        print(
            f"v0_5_2: linked {linked} legacy CCDC JEs, backfilled {backfilled_rows} entry rows"
        )
