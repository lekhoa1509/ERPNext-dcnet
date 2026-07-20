"""Inventory Cost Reallocation — Phase 2 of VAS TT99/2025 inventory split.

When LCV runs, lcv_hooks.lcv_create_inventory_split_je moves landed cost from
1561 → 1562 at submit time. As goods are sold, ERPNext core posts:
    Dr 632 / Cr 1561 (full COGS = giá mua + landed cost)

This drives 1561 negative over time (it only received giá mua, not landed cost,
but is being credited for full COGS). Meanwhile 1562 sits at +landed cost, never
decreasing. End-of-period reconciliation:
    Dr 1561 / Cr 1562  amount = landed_cost_share_of_period_cogs

This DocType records each reconciliation event for audit trail. The actual
GL movement happens via a Journal Entry created on submit.

Method "Theo tỉ trọng COGS kỳ":
    amount = current_1562_balance × (period_cogs / cumulative_total_inventory_value)

This is an approximation acceptable to VAS audit. Per-Item precision is
deferred (would need to track landed_cost_share per Stock Ledger Entry).
"""
from __future__ import annotations

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt, getdate


class InventoryCostReallocation(Document):
    def validate(self):
        if getdate(self.from_date) > getdate(self.to_date):
            frappe.throw(_("'Từ ngày' phải nhỏ hơn hoặc bằng 'Đến ngày'."))
        if self.source_account == self.target_account:
            frappe.throw(_("TK nguồn và TK đích phải khác nhau."))
        for acc_field in ("source_account", "target_account"):
            acc = self.get(acc_field)
            company = frappe.db.get_value("Account", acc, "company")
            if company != self.company:
                frappe.throw(
                    _("{0} ({1}) không thuộc Công ty {2}.").format(
                        _(acc_field), acc, self.company
                    )
                )
        if flt(self.computed_amount) <= 0:
            frappe.throw(_("Số tiền phân bổ phải > 0. Bấm 'Tính lại' để hệ thống đề xuất."))

    def on_submit(self):
        if self.journal_entry:
            return
        je = frappe.new_doc("Journal Entry")
        je.posting_date = self.posting_date or self.to_date
        je.company = self.company
        je.voucher_type = "Journal Entry"
        je.user_remark = _(
            "Phân bổ phụ phí mua hàng vào TK kho theo VAS TT99/2025 từ {0} (kỳ {1} → {2})"
        ).format(self.name, self.from_date, self.to_date)

        amount = flt(self.computed_amount)
        je.append("accounts", {
            "account": self.target_account,
            "debit_in_account_currency": amount,
            "user_remark": _("Cộng lại giá vốn phụ phí cho kỳ {0}–{1}").format(
                self.from_date, self.to_date
            ),
        })
        je.append("accounts", {
            "account": self.source_account,
            "credit_in_account_currency": amount,
            "user_remark": _("Giảm số dư phụ phí mua hàng theo phân bổ kỳ").format(),
        })
        je.flags.ignore_permissions = True
        je.insert()
        je.submit()

        self.db_set("journal_entry", je.name)
        self.add_comment(
            comment_type="Info",
            text=_("Đã tạo Bút toán phân bổ: {0}").format(
                f'<a href="/app/journal-entry/{je.name}">{je.name}</a>'
            ),
        )

    def on_cancel(self):
        if not self.journal_entry:
            return
        je = frappe.get_doc("Journal Entry", self.journal_entry)
        if je.docstatus == 1:
            je.flags.ignore_permissions = True
            je.cancel()


@frappe.whitelist()
def compute_reallocation(
    company: str,
    from_date: str,
    to_date: str,
    source_account: str,
    target_account: str | None = None,
) -> dict:
    """Preview the reallocation amount without creating any document.

    Returns: { period_cogs, source_balance, computed_amount, formula_text }

    Formula (method "Theo tỉ trọng COGS kỳ"):
        ratio = source_balance / (cumulative_inventory_dr_to_date)
        amount = period_cogs × ratio

    Where:
        period_cogs = Σ Dr on company default_expense_account (632) in [from_date, to_date]
        source_balance = Σ(Dr - Cr) on source_account up to to_date
        cumulative_inventory_dr_to_date = Σ Dr on accounts starting with '156'
            (1561 + 1562 + 1567 if any) up to to_date.

    The ratio represents "what fraction of cumulative inventory value left as
    COGS in this period" — a defensible VAS-acceptable approximation.
    """
    if not (company and from_date and to_date and source_account):
        frappe.throw(_("Thiếu tham số bắt buộc."))

    period_cogs = _query_period_debit(
        company,
        account=_get_company_cogs_account(company),
        from_date=from_date,
        to_date=to_date,
    )

    source_balance = _query_balance_to(
        company, account=source_account, to_date=to_date
    )

    cumulative_inventory_dr = _query_cumulative_debit_for_pattern(
        company, pattern="156%", to_date=to_date
    )

    if cumulative_inventory_dr <= 0:
        ratio = 0
    else:
        ratio = period_cogs / cumulative_inventory_dr

    computed_amount = round(min(source_balance, source_balance * ratio if ratio else 0), 2)
    # Cap at source_balance — never reallocate more than what's actually in 1562
    if computed_amount > source_balance:
        computed_amount = round(source_balance, 2)
    if computed_amount < 0:
        computed_amount = 0

    return {
        "period_cogs": flt(period_cogs),
        "source_balance": flt(source_balance),
        "cumulative_inventory_dr": flt(cumulative_inventory_dr),
        "ratio": flt(ratio),
        "computed_amount": flt(computed_amount),
        "formula_text": _(
            "amount = source_balance × (period_cogs / cumulative_inventory_dr)\n"
            "       = {0} × ({1} / {2})\n"
            "       = {3}"
        ).format(
            f"{source_balance:,.0f}",
            f"{period_cogs:,.0f}",
            f"{cumulative_inventory_dr:,.0f}",
            f"{computed_amount:,.0f}",
        ),
    }


def _get_company_cogs_account(company: str) -> str | None:
    return frappe.db.get_value("Company", company, "default_expense_account")


def _query_period_debit(company: str, account: str | None, from_date: str, to_date: str) -> float:
    if not account:
        return 0
    row = frappe.db.sql(
        """
        SELECT COALESCE(SUM(debit), 0) AS total_debit
        FROM `tabGL Entry`
        WHERE company = %(company)s
          AND account = %(account)s
          AND is_cancelled = 0
          AND posting_date BETWEEN %(from_date)s AND %(to_date)s
        """,
        {"company": company, "account": account, "from_date": from_date, "to_date": to_date},
        as_dict=True,
    )
    return flt(row[0].total_debit if row else 0)


def _query_balance_to(company: str, account: str, to_date: str) -> float:
    row = frappe.db.sql(
        """
        SELECT COALESCE(SUM(debit), 0) - COALESCE(SUM(credit), 0) AS balance
        FROM `tabGL Entry`
        WHERE company = %(company)s
          AND account = %(account)s
          AND is_cancelled = 0
          AND posting_date <= %(to_date)s
        """,
        {"company": company, "account": account, "to_date": to_date},
        as_dict=True,
    )
    return max(flt(row[0].balance if row else 0), 0)


def _query_cumulative_debit_for_pattern(company: str, pattern: str, to_date: str) -> float:
    row = frappe.db.sql(
        """
        SELECT COALESCE(SUM(debit), 0) AS total_debit
        FROM `tabGL Entry`
        WHERE company = %(company)s
          AND account LIKE %(pattern)s
          AND is_cancelled = 0
          AND posting_date <= %(to_date)s
        """,
        {"company": company, "pattern": pattern, "to_date": to_date},
        as_dict=True,
    )
    return flt(row[0].total_debit if row else 0)
