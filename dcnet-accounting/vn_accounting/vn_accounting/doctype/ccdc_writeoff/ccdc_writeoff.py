import frappe
from frappe import _
from frappe.model.document import Document


class CCDCWriteoff(Document):
    def before_save(self):
        self._calc_remaining()
        if not self.accounting_entries:
            self._autofill_entries()

    def validate(self):
        if not self.ccdc_item:
            frappe.throw(_("CCDC Item is required"))
        status = frappe.db.get_value("CCDC Item", self.ccdc_item, "status")
        if status == "Đã ghi giảm":
            frappe.throw(_("CCDC Item đã được ghi giảm trước đó"))

    def on_submit(self):
        if not self.accounting_entries:
            self._autofill_entries()
        self._post_je()
        self._cancel_pending_schedules()
        frappe.db.set_value("CCDC Item", self.ccdc_item, "status", "Đã ghi giảm",
                            update_modified=False)
        frappe.db.commit()

    def on_cancel(self):
        if self.posted_je:
            try:
                je = frappe.get_doc("Journal Entry", self.posted_je)
                if je.docstatus == 1:
                    je.cancel()
            except frappe.DoesNotExistError:
                pass
        # Skip back-link check — JE reverse GL entries inherit reference_type/reference_name
        self.flags.ignore_links = True

    def _calc_remaining(self):
        # Under the VAS-correct CCDC purchase shape (Dr 153 / Cr 331, Dr 242 / Cr 153),
        # the full cost lands in TK 242 at purchase time and TK 153 acts as transit
        # (net 0). Writeoff therefore clears TK 242 exclusively.
        #
        # Two cases:
        #   - "Mới mua" (no allocation schedule yet): all cost still sits in TK 242
        #   - in-use (schedule exists): remaining 242 = sum of pending allocations
        pending = frappe.db.sql(
            """
            SELECT COALESCE(SUM(ae.allocation_amount), 0)
            FROM `tabCCDC Allocation Entry` ae
            JOIN `tabCCDC Allocation Schedule` s ON ae.parent = s.name
            WHERE s.ccdc_item = %s AND ae.status = 'Pending'
            """,
            self.ccdc_item,
        )
        pending_242 = pending[0][0] if pending else 0

        item_status = frappe.db.get_value("CCDC Item", self.ccdc_item, "status")
        if item_status == "Mới mua":
            cost = frappe.db.get_value("CCDC Item", self.ccdc_item, "cost") or 0
            self.remaining_242_amount = cost
        else:
            self.remaining_242_amount = pending_242

        self.remaining_153_amount = 0

    def _autofill_entries(self):
        from vn_accounting.utils.accounting_posting import build_default_entries
        company = frappe.db.get_value("CCDC Item", self.ccdc_item, "company")
        if not company:
            return
        rows = build_default_entries(
            "CCDC Writeoff",
            None,
            0,
            False,
            10,
            company,
            remaining_242=float(self.remaining_242_amount or 0),
            remaining_153=float(self.remaining_153_amount or 0),
            compensation_amount=float(self.compensation_amount or 0),
        )
        self.accounting_entries = []
        for r in rows:
            self.append("accounting_entries", r)

    def _post_je(self):
        from vn_accounting.utils.accounting_posting import post_je_from_entries, resolve_cost_center
        ccdc_item = frappe.get_doc("CCDC Item", self.ccdc_item)
        company = ccdc_item.company
        posting_date = self.writeoff_date or frappe.utils.today()
        remark = "Ghi giảm CCDC {0} — {1}".format(
            self.ccdc_item, ccdc_item.item_name or ccdc_item.item_code or ""
        )
        cost_center = resolve_cost_center(ccdc_item, company)
        je_name = post_je_from_entries(
            self.accounting_entries,
            company,
            posting_date,
            remark,
            "CCDC Writeoff",
            self.name,
            submit=True,
            cost_center=cost_center,
            source_key="vn_accounting.ccdc.writeoff",
        )
        self.db_set("posted_je", je_name, update_modified=False)

    def _cancel_pending_schedules(self):
        schedules = frappe.get_all(
            "CCDC Allocation Schedule",
            filters={"ccdc_item": self.ccdc_item, "status": "Active"},
            fields=["name"],
        )
        for sched in schedules:
            frappe.db.set_value("CCDC Allocation Schedule", sched.name, "status", "Cancelled",
                                update_modified=False)
            frappe.db.sql(
                "UPDATE `tabCCDC Allocation Entry` SET status='Cancelled' WHERE parent=%s AND status='Pending'",
                sched.name,
            )


@frappe.whitelist()
def get_writeoff_preview(ccdc_item):
    """Return remaining 242/153 amounts for the given CCDC Item."""
    if not ccdc_item:
        return {"remaining_242_amount": 0, "remaining_153_amount": 0}

    pending = frappe.db.sql(
        """
        SELECT COALESCE(SUM(ae.allocation_amount), 0)
        FROM `tabCCDC Allocation Entry` ae
        JOIN `tabCCDC Allocation Schedule` s ON ae.parent = s.name
        WHERE s.ccdc_item = %s AND ae.status = 'Pending'
        """,
        ccdc_item,
    )
    remaining_242 = float(pending[0][0]) if pending else 0.0

    item = frappe.db.get_value(
        "CCDC Item", ccdc_item, ["status", "cost"], as_dict=True
    )
    if item and item.status == "Mới mua":
        remaining_153 = float(item.cost or 0)
    else:
        remaining_153 = 0.0

    return {
        "remaining_242_amount": remaining_242,
        "remaining_153_amount": remaining_153,
    }
