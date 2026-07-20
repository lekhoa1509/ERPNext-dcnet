"""VN Deferred Expense Schedule — controller for TK 242 amortization.

Mirror of VN Deferred Revenue Schedule for the expense side.

Workflow:
  1. Original transaction (manual or PI): Dr 242 / Cr 331/112 = total_amount
  2. Schedule with deferred_account=242, expense_account=6xxx
  3. Generate lịch → fills N period lines
  4. Submit (Draft → Active)
  5. Each period: post JE Dr 6xx / Cr 242 → mark line Recognized
"""
from __future__ import annotations

from typing import Any

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt, getdate, today

# Reuse period helpers from sibling module
from vn_accounting.vn_accounting.doctype.vn_deferred_revenue_schedule.vn_deferred_revenue_schedule import (
    _month_periods, _quarter_periods,
)
from frappe.utils import add_days


class VNDeferredExpenseSchedule(Document):
    def validate(self):
        if getdate(self.end_date) < getdate(self.start_date):
            frappe.throw(_("Ngày kết thúc phải >= Ngày bắt đầu."))
        if flt(self.total_amount) <= 0:
            frappe.throw(_("Tổng số tiền chờ phân bổ phải > 0."))
        self._validate_accounts()
        self._recompute_totals()

    def _validate_accounts(self):
        for fld, lbl in [("deferred_account", "TK chi phí chờ phân bổ"),
                          ("expense_account", "TK chi phí sẽ ghi nhận")]:
            acc = self.get(fld)
            if not acc:
                continue
            row = frappe.db.get_value("Account", acc,
                ["company", "is_group"], as_dict=True)
            if not row:
                frappe.throw(_("{0}: không tìm thấy {1}").format(lbl, acc))
            if row.company != self.company:
                frappe.throw(_("{0}: tài khoản thuộc công ty khác").format(lbl))
            if row.is_group:
                frappe.throw(_("{0}: phải là TK chi tiết").format(lbl))

    def _recompute_totals(self):
        rec = sum(flt(l.amount) for l in (self.schedule_lines or [])
                   if l.status == "Recognized")
        self.recognized_amount = rec
        self.remaining_amount = flt(self.total_amount) - rec

    def before_submit(self):
        if not self.schedule_lines:
            frappe.throw(_("Bấm <b>Sinh lịch tự động</b> trước khi ghi sổ."))
        total = sum(flt(l.amount) for l in self.schedule_lines)
        if abs(total - flt(self.total_amount)) > 1:
            frappe.throw(_("Tổng các kỳ ({0:,.0f}) phải bằng tổng số tiền chờ phân bổ ({1:,.0f}).")
                         .format(total, flt(self.total_amount)))
        self.status = "Active"

    def on_cancel(self):
        for l in self.schedule_lines or []:
            if l.recognized_je and l.status == "Recognized":
                je = frappe.get_doc("Journal Entry", l.recognized_je)
                if je.docstatus == 1:
                    je.cancel()
        self.status = "Cancelled"

    @frappe.whitelist()
    def generate_lines(self):
        if self.docstatus != 0:
            frappe.throw(_("Chỉ sinh lịch khi đang ở trạng thái Nháp."))
        if not (self.start_date and self.end_date and self.total_amount):
            frappe.throw(_("Cần điền Ngày bắt đầu, Ngày kết thúc và Tổng số tiền trước."))
        self.schedule_lines = []
        method = self.amortization_method or "Monthly"
        start, end = getdate(self.start_date), getdate(self.end_date)
        total = flt(self.total_amount)

        if method == "One-shot":
            periods = [(start, end, start.isoformat())]
        elif method == "Daily":
            periods = []
            d = start
            while d <= end:
                periods.append((d, d, d.isoformat()))
                d = add_days(d, 1)
        elif method == "Monthly":
            periods = _month_periods(start, end)
        elif method == "Quarterly":
            periods = _quarter_periods(start, end)
        else:
            frappe.throw(_("Phương pháp không hỗ trợ: {0}").format(method))

        if not periods:
            frappe.throw(_("Không sinh được kỳ nào — kiểm tra Ngày bắt đầu / Ngày kết thúc."))
        per = round(total / len(periods), 0)
        assigned = 0.0
        for i, (ps, pe, lbl) in enumerate(periods):
            amt = per if i < len(periods) - 1 else (total - assigned)
            assigned += amt
            self.append("schedule_lines", {
                "period_label": lbl, "period_start": ps, "period_end": pe,
                "amount": amt, "status": "Pending",
            })
        self._recompute_totals()
        self.save()
        return len(periods)

    @frappe.whitelist()
    def recognize_line(self, line_name: str, posting_date: str | None = None) -> str:
        if self.docstatus != 1:
            frappe.throw(_("Lịch phải được ghi sổ trước khi phân bổ từng kỳ."))
        line = next((l for l in self.schedule_lines if l.name == line_name), None)
        if not line:
            frappe.throw(_("Không tìm thấy dòng {0}").format(line_name))
        if line.status == "Recognized":
            frappe.throw(_("Kỳ {0} đã phân bổ rồi.").format(line.period_label))

        pd = posting_date or line.period_end or today()
        je = frappe.new_doc("Journal Entry")
        je.voucher_type = "Journal Entry"
        je.company = self.company
        je.posting_date = pd
        je.user_remark = _("Phân bổ chi phí trả trước kỳ {0} — Schedule {1}"
                           ).format(line.period_label, self.name)
        je.append("accounts", {
            "account": self.expense_account,
            "debit_in_account_currency": flt(line.amount),
            "credit_in_account_currency": 0,
        })
        je.append("accounts", {
            "account": self.deferred_account,
            "debit_in_account_currency": 0,
            "credit_in_account_currency": flt(line.amount),
            "party_type": "Supplier" if self.supplier else None,
            "party": self.supplier or None,
            "reference_type": "Purchase Invoice" if self.reference_invoice else None,
            "reference_name": self.reference_invoice or None,
        })
        je.flags.ignore_permissions = True
        je.insert()
        je.submit()

        # Post-submit: db_set to bypass UpdateAfterSubmitError
        frappe.db.set_value(line.doctype, line.name,
            {"recognized_je": je.name, "status": "Recognized"}, update_modified=False)
        new_recognized = float(frappe.db.sql(
            """SELECT COALESCE(SUM(amount), 0) FROM `tabVN Deferred Expense Schedule Line`
               WHERE parent=%s AND status='Recognized'""",
            (self.name,))[0][0] or 0)
        new_remaining = flt(self.total_amount) - new_recognized
        upd = {"recognized_amount": new_recognized, "remaining_amount": new_remaining}
        if new_remaining <= 0.5:
            upd["status"] = "Completed"
        frappe.db.set_value(self.doctype, self.name, upd, update_modified=False)
        self.recognized_amount = new_recognized
        self.remaining_amount = new_remaining
        if "status" in upd:
            self.status = upd["status"]
        return je.name

    @frappe.whitelist()
    def recognize_all_due(self, as_of_date: str | None = None) -> dict:
        as_of = getdate(as_of_date or today())
        posted = []
        for l in self.schedule_lines:
            if l.status == "Pending" and getdate(l.period_end) <= as_of:
                je = self.recognize_line(l.name, posting_date=l.period_end)
                posted.append({"period": l.period_label, "je": je, "amount": flt(l.amount)})
        return {"posted": posted, "count": len(posted)}


@frappe.whitelist()
def create_from_purchase_invoice(
    purchase_invoice: str,
    start_date: str,
    end_date: str,
    total_amount: float,
    amortization_method: str = "Monthly",
    expense_account: str | None = None,
    deferred_account: str | None = None,
) -> dict:
    """Create + generate + submit a Schedule from PI form button."""
    if not purchase_invoice:
        frappe.throw(_("Phải chọn Hóa đơn mua hàng nguồn."))
    pi = frappe.db.get_value("Purchase Invoice", purchase_invoice,
        ["company", "supplier", "docstatus"], as_dict=True)
    if not pi:
        frappe.throw(_("Không tìm thấy Hóa đơn {0}").format(purchase_invoice))
    if pi.docstatus != 1:
        frappe.throw(_("Hóa đơn phải đã ghi sổ trước khi tạo lịch."))

    if not deferred_account:
        deferred_account = frappe.db.get_value(
            "VN Accounting Settings", "VN Accounting Settings", "deferred_expense_account")
    if not deferred_account:
        frappe.throw(_("TK chi phí chờ phân bổ chưa cấu hình — mở Cài đặt kế toán."))

    doc = frappe.new_doc("VN Deferred Expense Schedule")
    doc.company = pi.company
    doc.supplier = pi.supplier
    doc.reference_invoice = purchase_invoice
    doc.start_date = start_date
    doc.end_date = end_date
    doc.total_amount = float(total_amount)
    doc.amortization_method = amortization_method
    doc.deferred_account = deferred_account
    doc.expense_account = expense_account
    doc.flags.ignore_permissions = True
    doc.insert()

    n_lines = doc.generate_lines()
    doc.submit()
    return {"name": doc.name, "lines": n_lines}


@frappe.whitelist()
def recognize_all_companies_due(as_of_date: str | None = None) -> dict:
    """Cron entry — batch recognize all due expense lines."""
    as_of = getdate(as_of_date or today())
    summary = {"schedules_touched": 0, "total_posted": 0, "errors": []}
    schedules = frappe.db.sql_list(
        """SELECT name FROM `tabVN Deferred Expense Schedule`
           WHERE docstatus=1 AND status='Active'""",
    )
    for name in schedules:
        try:
            doc = frappe.get_doc("VN Deferred Expense Schedule", name)
            r = doc.recognize_all_due(as_of_date=as_of.isoformat())
            if r["count"] > 0:
                summary["schedules_touched"] += 1
                summary["total_posted"] += r["count"]
        except Exception as e:
            summary["errors"].append(f"{name}: {e}")
    return summary
