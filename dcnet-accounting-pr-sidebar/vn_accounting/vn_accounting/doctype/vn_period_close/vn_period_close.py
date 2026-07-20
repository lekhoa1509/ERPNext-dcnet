"""VN Period Close — monthly/quarterly/yearly P&L close to TK 911 → 4212.

Misa-style: at end of each accounting period, all revenue (5xx, 7xx) and
expense (6xx, 8xx) TKs must close to 911 (income summary) then 911's net
moves to 4212 (current-year retained earnings).

ERPNext stock Period Closing Voucher only supports YEAR-END close; this
DocType adds Monthly/Quarterly modes plus idempotent re-submit semantics.

Workflow:
  1. Pick period_end + period_type → click Preview
  2. System scans GL Entry NET (Dr-Cr) at period_end for each TK listed in
     VN Accounting Settings.revenue_accounts_to_close + expense_accounts_to_close_periodic
  3. Preview lines populated; user inspects
  4. Submit → builds + posts JE with N+1 legs:
       - For each revenue TK with Cr balance: Dr <TK>, Cr 911
       - For each expense TK with Dr balance: Cr <TK>, Dr 911
       - Net to 4212: Cr 4212 (if profit) or Dr 4212 (if loss)
     JE.naming uses voucher_no = "<naming_series>" — idempotent via
     unique (company, period_end) check.
  5. Cancel → cancels JE → status Reversed
"""
from __future__ import annotations

from typing import Any

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt, getdate


class VNPeriodClose(Document):
    def validate(self):
        if not self.income_summary_account:
            self.income_summary_account = self._settings_value("pnl_account_911")
        if not self.retained_earnings_account:
            self.retained_earnings_account = self._settings_value("retained_earnings_current_year")
        for fld, lbl in [("income_summary_account", "TK 911"),
                          ("retained_earnings_account", "TK 4212")]:
            if not self.get(fld):
                frappe.throw(_("{0} chưa được cấu hình — mở <b>Cài đặt kế toán</b> để chọn.").format(lbl))
        # Idempotency check: only ONE Posted close per (company, period_end)
        dup = frappe.db.sql_list(
            """SELECT name FROM `tabVN Period Close`
               WHERE company=%s AND period_end=%s AND status='Posted'
                 AND docstatus=1 AND name != %s""",
            (self.company, self.period_end, self.name or ""),
        )
        if dup:
            frappe.throw(_("Đã có Phiếu kết chuyển khác được ghi sổ cho công ty {0} kỳ kết thúc {1}: {2}")
                         .format(self.company, self.period_end, dup[0]))

    def _settings_value(self, fieldname: str) -> str | None:
        return frappe.db.get_value("VN Accounting Settings",
            "VN Accounting Settings", fieldname)

    def _settings_table(self, child_table_fieldname: str, value_field: str) -> list[str]:
        rows = frappe.db.sql(
            """SELECT {f} FROM `tabVN Accounting Settings Revenue Closing Account` rca
               WHERE rca.parent='VN Accounting Settings' AND rca.parentfield=%s""".format(f=value_field),
            (child_table_fieldname,), as_dict=True,
        )
        return [r[value_field] for r in rows if r.get(value_field)]

    def _accounts_to_close(self) -> tuple[list[str], list[str]]:
        """Return (revenue_accounts, expense_accounts) lists from Settings.

        Falls back to root_type Income / Expense scan if Settings tables empty.
        """
        company = self.company
        settings = frappe.get_single("VN Accounting Settings")
        # Read child tables
        rev = [r.account for r in (settings.revenue_accounts_to_close or [])
                if getattr(r, "account", None)]
        exp = [r.account for r in (settings.expense_accounts_to_close_periodic or [])
                if getattr(r, "account", None)]
        # Filter to company
        rev = [a for a in rev if frappe.db.get_value("Account", a, "company") == company]
        exp = [a for a in exp if frappe.db.get_value("Account", a, "company") == company]

        # Fallback: scan all leaves under root_type Income / Expense
        if not rev:
            rev = frappe.db.sql_list(
                """SELECT name FROM `tabAccount`
                   WHERE company=%s AND is_group=0 AND root_type='Income'""",
                (company,),
            )
        if not exp:
            exp = frappe.db.sql_list(
                """SELECT name FROM `tabAccount`
                   WHERE company=%s AND is_group=0 AND root_type='Expense'
                     AND name != %s""",
                (company, self.income_summary_account or ""),
            )
        return rev, exp

    @frappe.whitelist()
    def preview(self) -> dict:
        """Scan GL Entry per TK at period_end. Populate preview_lines."""
        if self.docstatus != 0:
            frappe.throw(_("Chỉ xem trước khi đang ở trạng thái Nháp."))
        self.preview_lines = []
        rev, exp = self._accounts_to_close()
        total_rev = total_exp = 0.0

        for acc in sorted(rev):
            net = self._gl_net(acc)
            # Revenue: typically Cr balance → close by debiting
            if abs(net) < 0.5:
                continue
            self.append("preview_lines", {
                "account": acc, "side": "Revenue",
                "net_amount": net, "to_close_amount": abs(net),
            })
            total_rev += -net  # net is Dr-Cr; for Cr balance, -net is positive
        for acc in sorted(exp):
            net = self._gl_net(acc)
            if abs(net) < 0.5:
                continue
            self.append("preview_lines", {
                "account": acc, "side": "Expense",
                "net_amount": net, "to_close_amount": abs(net),
            })
            total_exp += net

        self.total_revenue_closed = total_rev
        self.total_expense_closed = total_exp
        self.net_profit = total_rev - total_exp
        self.status = "Previewed"
        self.save()
        return {"revenue_total": total_rev, "expense_total": total_exp,
                "net_profit": total_rev - total_exp,
                "lines": len(self.preview_lines)}

    def _gl_net(self, account: str) -> float:
        row = frappe.db.sql(
            """SELECT COALESCE(SUM(debit - credit), 0) AS net FROM `tabGL Entry`
               WHERE company=%s AND account=%s AND is_cancelled=0
                 AND posting_date<=%s""",
            (self.company, account, self.period_end), as_dict=True,
        )
        return float(row[0]["net"]) if row else 0.0

    def before_submit(self):
        # Auto-preview if not done
        if not self.preview_lines:
            self.preview()
        if not self.preview_lines:
            frappe.throw(_("Không có tài khoản nào có số dư để kết chuyển tại Ngày kết thúc kỳ {0}.").format(self.period_end))

    def on_submit(self):
        """Build + post the closing JE."""
        je = frappe.new_doc("Journal Entry")
        je.voucher_type = "Journal Entry"
        je.company = self.company
        je.posting_date = self.period_end
        je.user_remark = _("Kết chuyển {0} đến ngày {1} — Period Close {2}").format(
            _(self.period_type), self.period_end, self.name)

        # net_amount stored as Dr-Cr (positive=Dr, negative=Cr).
        # Closing must FLIP based on sign of net, not just side. Normal:
        #   Revenue net<0 (Cr): Dr account, Cr 911 — zeroes account
        #   Expense net>0 (Dr): Cr account, Dr 911 — zeroes account
        # Abnormal (sales returns, expense reversals):
        #   Revenue net>0 (Dr): Cr account, Dr 911
        #   Expense net<0 (Cr): Dr account, Cr 911
        # OLD bug: hardcoded Dr-account for Revenue regardless of net sign →
        # revenue with Dr balance got Dr-INCREASED instead of zeroed,
        # leaving P&L residual after close.
        total_rev = total_exp = 0.0
        for line in self.preview_lines:
            net = flt(line.net_amount)
            amt = abs(net)
            if net > 0:
                # Dr balance → close with Cr account / Dr 911
                acc_dr, acc_cr, sum_dr, sum_cr = 0, amt, amt, 0
            else:
                # Cr balance → close with Dr account / Cr 911
                acc_dr, acc_cr, sum_dr, sum_cr = amt, 0, 0, amt
            je.append("accounts", {
                "account": line.account,
                "debit_in_account_currency": acc_dr,
                "credit_in_account_currency": acc_cr,
            })
            je.append("accounts", {
                "account": self.income_summary_account,
                "debit_in_account_currency": sum_dr,
                "credit_in_account_currency": sum_cr,
            })
            # 911 net Cr accumulates revenue; 911 net Dr accumulates expense
            if line.side == "Revenue":
                total_rev += sum_cr - sum_dr  # +amt normal, -amt abnormal
            else:
                total_exp += sum_dr - sum_cr

        # Net to 4212: total_rev (911 Cr) - total_exp (911 Dr) = profit if positive
        net_profit = total_rev - total_exp
        if abs(net_profit) > 0.5:
            if net_profit > 0:
                # Profit: close 911 Cr balance → Dr 911 / Cr 4212
                je.append("accounts", {
                    "account": self.income_summary_account,
                    "debit_in_account_currency": net_profit,
                    "credit_in_account_currency": 0,
                })
                je.append("accounts", {
                    "account": self.retained_earnings_account,
                    "debit_in_account_currency": 0,
                    "credit_in_account_currency": net_profit,
                })
            else:
                # Loss: close 911 Dr balance → Cr 911 / Dr 4212
                je.append("accounts", {
                    "account": self.income_summary_account,
                    "debit_in_account_currency": 0,
                    "credit_in_account_currency": -net_profit,
                })
                je.append("accounts", {
                    "account": self.retained_earnings_account,
                    "debit_in_account_currency": -net_profit,
                    "credit_in_account_currency": 0,
                })
        je.flags.ignore_permissions = True
        je.insert()
        je.submit()

        self.posted_je = je.name
        self.status = "Posted"
        self.total_revenue_closed = total_rev
        self.total_expense_closed = total_exp
        self.net_profit = net_profit
        self.db_update()
        # No save() to avoid infinite recursion on submit

    def on_cancel(self):
        if self.posted_je:
            je = frappe.get_doc("Journal Entry", self.posted_je)
            if je.docstatus == 1:
                je.cancel()
        self.status = "Reversed"
        self.db_update()
