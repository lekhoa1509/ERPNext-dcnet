"""VN Deferred Revenue Schedule — controller for TK 3387 amortization.

Models a multi-period revenue recognition schedule from a deferred-revenue
liability (TK 3387 "Doanh thu chưa thực hiện") to a recognized income TK
(51131-51136, 5111, ...).

Workflow:
  1. Original transaction (manual or from SI): Dr 131/112 / Cr 3387 = total_amount
  2. User creates this Schedule, picks recognition_account + dates + method
  3. Click "Generate lịch" → fills schedule_lines with N period rows
  4. Submit (status Draft → Active)
  5. Each period: click "Ghi nhận kỳ này" (or batch via API) →
     posts JE Dr 3387 / Cr recognition_account, marks line Recognized

When all lines Recognized → status Completed (auto).
Cancel → status Cancelled + auto-cancels any posted JEs.
"""
from __future__ import annotations

import calendar
from datetime import date, timedelta
from typing import Any

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import add_days, add_months, flt, getdate, today


class VNDeferredRevenueSchedule(Document):
    def validate(self):
        if getdate(self.end_date) < getdate(self.start_date):
            frappe.throw(_("Ngày kết thúc phải >= Ngày bắt đầu."))
        if flt(self.total_amount) <= 0:
            frappe.throw(_("Tổng số tiền hoãn lại phải > 0."))
        self._validate_accounts()
        self._recompute_totals()

    def _validate_accounts(self):
        for fld, lbl in [("deferred_account", "TK doanh thu chưa thực hiện"),
                          ("recognition_account", "TK doanh thu sẽ ghi nhận")]:
            acc = self.get(fld)
            if not acc:
                continue
            row = frappe.db.get_value("Account", acc,
                ["company", "is_group", "root_type"], as_dict=True)
            if not row:
                frappe.throw(_("{0}: không tìm thấy tài khoản {1}").format(lbl, acc))
            if row.company != self.company:
                frappe.throw(_("{0}: tài khoản {1} thuộc công ty khác").format(lbl, acc))
            if row.is_group:
                frappe.throw(_("{0}: phải là TK chi tiết (không phải group)").format(lbl))

    def _recompute_totals(self):
        recognized = sum(flt(l.amount) for l in (self.schedule_lines or [])
                         if l.status == "Recognized")
        self.recognized_amount = recognized
        self.remaining_amount = flt(self.total_amount) - recognized

    def before_submit(self):
        if not self.schedule_lines:
            frappe.throw(_("Bấm <b>Sinh lịch tự động</b> trước khi ghi sổ."))
        lines_total = sum(flt(l.amount) for l in self.schedule_lines)
        if abs(lines_total - flt(self.total_amount)) > 1:
            frappe.throw(_("Tổng các kỳ ({0:,.0f}) phải bằng tổng số tiền hoãn lại ({1:,.0f}).")
                         .format(lines_total, flt(self.total_amount)))
        self.status = "Active"

    def on_cancel(self):
        # Cancel any posted recognition JEs
        for line in self.schedule_lines or []:
            if line.recognized_je and line.status == "Recognized":
                je = frappe.get_doc("Journal Entry", line.recognized_je)
                if je.docstatus == 1:
                    je.cancel()
        self.status = "Cancelled"

    @frappe.whitelist()
    def generate_lines(self):
        """Auto-fill schedule_lines per amortization_method."""
        if self.docstatus != 0:
            frappe.throw(_("Chỉ sinh lịch khi đang ở trạng thái Nháp."))
        if not self.start_date or not self.end_date or not self.total_amount:
            frappe.throw(_("Cần điền Ngày bắt đầu, Ngày kết thúc và Tổng số tiền trước."))

        self.schedule_lines = []
        method = self.amortization_method or "Monthly"
        start = getdate(self.start_date)
        end = getdate(self.end_date)
        total = flt(self.total_amount)

        periods: list[tuple[date, date, str]] = []
        if method == "One-shot":
            periods.append((start, end, f"{start.isoformat()}"))
        elif method == "Daily":
            n_days = (end - start).days + 1
            for i in range(n_days):
                d = add_days(start, i)
                periods.append((d, d, d.isoformat()))
        elif method == "Monthly":
            periods = _month_periods(start, end)
        elif method == "Quarterly":
            periods = _quarter_periods(start, end)
        else:
            frappe.throw(_("Phương pháp phân bổ không hỗ trợ: {0}").format(method))

        if not periods:
            frappe.throw(_("Không sinh được kỳ nào — kiểm tra Ngày bắt đầu / Ngày kết thúc."))

        # Distribute amount evenly; absorb rounding into LAST period
        per = round(total / len(periods), 0)
        assigned = 0.0
        for i, (ps, pe, lbl) in enumerate(periods):
            amt = per if i < len(periods) - 1 else (total - assigned)
            assigned += amt
            self.append("schedule_lines", {
                "period_label": lbl,
                "period_start": ps,
                "period_end": pe,
                "amount": amt,
                "status": "Pending",
            })
        self._recompute_totals()
        self.save()
        return len(periods)

    @frappe.whitelist()
    def recognize_line(self, line_name: str, posting_date: str | None = None) -> str:
        """Post JE Dr 3387 / Cr recognition_account for one line. Return JE name."""
        if self.docstatus != 1:
            frappe.throw(_("Lịch phải được ghi sổ trước khi ghi nhận từng kỳ."))
        line = None
        for l in self.schedule_lines:
            if l.name == line_name:
                line = l
                break
        if not line:
            frappe.throw(_("Không tìm thấy dòng {0}").format(line_name))
        if line.status == "Recognized":
            frappe.throw(_("Kỳ {0} đã ghi nhận rồi.").format(line.period_label))

        pd = posting_date or line.period_end or today()
        je = frappe.new_doc("Journal Entry")
        je.voucher_type = "Journal Entry"
        je.company = self.company
        je.posting_date = pd
        je.user_remark = _("Ghi nhận doanh thu chưa thực hiện kỳ {0} — Schedule {1}"
                           ).format(line.period_label, self.name)
        je.append("accounts", {
            "account": self.deferred_account,
            "debit_in_account_currency": flt(line.amount),
            "credit_in_account_currency": 0,
            "party_type": "Customer" if self.customer else None,
            "party": self.customer or None,
            "reference_type": "Sales Invoice" if self.reference_invoice else None,
            "reference_name": self.reference_invoice or None,
        })
        je.append("accounts", {
            "account": self.recognition_account,
            "debit_in_account_currency": 0,
            "credit_in_account_currency": flt(line.amount),
        })
        je.flags.ignore_permissions = True
        je.insert()
        je.submit()

        # Post-submit: use db_set to bypass validate_update_after_submit
        frappe.db.set_value(line.doctype, line.name,
            {"recognized_je": je.name, "status": "Recognized"}, update_modified=False)
        # Recompute parent totals via direct SQL
        new_recognized = float(frappe.db.sql(
            """SELECT COALESCE(SUM(amount), 0) FROM `tabVN Deferred Revenue Schedule Line`
               WHERE parent=%s AND status='Recognized'""",
            (self.name,))[0][0] or 0)
        new_remaining = flt(self.total_amount) - new_recognized
        update_parent = {"recognized_amount": new_recognized,
                          "remaining_amount": new_remaining}
        if new_remaining <= 0.5:
            update_parent["status"] = "Completed"
        frappe.db.set_value(self.doctype, self.name, update_parent, update_modified=False)
        # Refresh local
        self.recognized_amount = new_recognized
        self.remaining_amount = new_remaining
        if "status" in update_parent:
            self.status = update_parent["status"]
        return je.name

    @frappe.whitelist()
    def recognize_all_due(self, as_of_date: str | None = None) -> dict:
        """Recognize all Pending lines whose period_end <= as_of_date."""
        as_of = getdate(as_of_date or today())
        posted = []
        for l in self.schedule_lines:
            if l.status == "Pending" and getdate(l.period_end) <= as_of:
                je = self.recognize_line(l.name, posting_date=l.period_end)
                posted.append({"period": l.period_label, "je": je, "amount": flt(l.amount)})
        return {"posted": posted, "count": len(posted)}


# ─── Period helpers ──────────────────────────────────────────────────

def _month_periods(start: date, end: date) -> list[tuple[date, date, str]]:
    out = []
    cur = start
    while cur <= end:
        # Last day of cur's month
        last_day = calendar.monthrange(cur.year, cur.month)[1]
        month_end = date(cur.year, cur.month, last_day)
        period_end = min(month_end, end)
        lbl = f"Tháng {cur.month:02d}/{cur.year}"
        out.append((cur, period_end, lbl))
        # Next month start
        if month_end >= end:
            break
        cur = add_days(month_end, 1)
    return out


def _quarter_periods(start: date, end: date) -> list[tuple[date, date, str]]:
    out = []
    cur = start
    while cur <= end:
        q = (cur.month - 1) // 3 + 1
        q_end_month = q * 3
        last_day = calendar.monthrange(cur.year, q_end_month)[1]
        q_end = date(cur.year, q_end_month, last_day)
        period_end = min(q_end, end)
        lbl = f"Quý {q}/{cur.year}"
        out.append((cur, period_end, lbl))
        if q_end >= end:
            break
        cur = add_days(q_end, 1)
    return out


# ─── Quick-create from Sales Invoice ─────────────────────────────────

@frappe.whitelist()
def create_from_sales_invoice(
    sales_invoice: str,
    start_date: str,
    end_date: str,
    total_amount: float,
    amortization_method: str = "Monthly",
    recognition_account: str | None = None,
    deferred_account: str | None = None,
) -> dict:
    """Create + auto-generate + submit a Schedule from SI form button.

    Returns ``{name, lines}`` for navigation.
    """
    if not sales_invoice:
        frappe.throw(frappe._("Phải chọn Hóa đơn bán hàng nguồn."))
    si = frappe.db.get_value("Sales Invoice", sales_invoice,
        ["company", "customer", "docstatus"], as_dict=True)
    if not si:
        frappe.throw(frappe._("Không tìm thấy Hóa đơn {0}").format(sales_invoice))
    if si.docstatus != 1:
        frappe.throw(frappe._("Hóa đơn phải đã ghi sổ trước khi tạo lịch."))

    if not deferred_account:
        deferred_account = frappe.db.get_value(
            "VN Accounting Settings", "VN Accounting Settings", "deferred_revenue_account")
    if not deferred_account:
        frappe.throw(frappe._("TK doanh thu chưa thực hiện chưa cấu hình — mở Cài đặt kế toán."))

    doc = frappe.new_doc("VN Deferred Revenue Schedule")
    doc.company = si.company
    doc.customer = si.customer
    doc.reference_invoice = sales_invoice
    doc.start_date = start_date
    doc.end_date = end_date
    doc.total_amount = float(total_amount)
    doc.amortization_method = amortization_method
    doc.deferred_account = deferred_account
    doc.recognition_account = recognition_account
    doc.flags.ignore_permissions = True
    doc.insert()

    n_lines = doc.generate_lines()
    doc.submit()
    return {"name": doc.name, "lines": n_lines}


# ─── Scheduled batch recognition ─────────────────────────────────────

@frappe.whitelist()
def recognize_all_companies_due(as_of_date: str | None = None) -> dict:
    """Cron entry — batch recognize all due lines across all Active schedules."""
    as_of = getdate(as_of_date or today())
    summary = {"schedules_touched": 0, "total_posted": 0, "errors": []}
    schedules = frappe.db.sql_list(
        """SELECT name FROM `tabVN Deferred Revenue Schedule`
           WHERE docstatus=1 AND status='Active'""",
    )
    for name in schedules:
        try:
            doc = frappe.get_doc("VN Deferred Revenue Schedule", name)
            r = doc.recognize_all_due(as_of_date=as_of.isoformat())
            if r["count"] > 0:
                summary["schedules_touched"] += 1
                summary["total_posted"] += r["count"]
        except Exception as e:
            summary["errors"].append(f"{name}: {e}")
    return summary
