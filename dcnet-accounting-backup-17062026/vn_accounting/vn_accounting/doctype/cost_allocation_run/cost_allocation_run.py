"""Cost Allocation Run — KTT phân bổ chi phí gián tiếp ra projects.

Phase 1: skeleton with totals computation + share validation only. GL posting
(post_allocation_je / cancel_allocation_je) wires in Phase 2.
"""
from __future__ import annotations

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt


class CostAllocationRun(Document):
    def autoname(self):
        """Format: CAR-<YYYY>-<MM>-<NNNN> (sequence per month).

        Frappe's `format:` autoname doesn't render Python format-spec on Date
        fields ({date:%Y} stays literal). Hand-format here for stable names.
        """
        if not self.run_period_end:
            return
        from frappe.model.naming import make_autoname
        from frappe.utils import getdate
        end = getdate(self.run_period_end)
        prefix = f"CAR-{end.strftime('%Y')}-{end.strftime('%m')}-"
        self.name = make_autoname(prefix + ".####")

    def validate(self):
        self._recompute_total()
        self._validate_shares()

    def _recompute_total(self):
        """Sum source_costs.amount → total_amount."""
        total = sum(flt(r.amount) for r in (self.source_costs or []))
        self.total_amount = total
        # Update share amounts when method = Đều (equal split)
        if self.method == "Đều" and self.shares:
            n = len(self.shares)
            if n > 0:
                each_percent = round(100.0 / n, 4)
                each_amount = round(total / n, 2) if total else 0
                # Last row absorbs residue so Σ = 100% / total
                residue_percent = 100.0 - each_percent * (n - 1)
                residue_amount = total - each_amount * (n - 1) if total else 0
                for i, share in enumerate(self.shares):
                    if i == n - 1:
                        share.percent = residue_percent
                        share.amount = residue_amount
                    else:
                        share.percent = each_percent
                        share.amount = each_amount

        elif self.method == "Thủ công" and self.shares:
            # KTT inputs % → derive amount
            for share in self.shares:
                share.amount = round(flt(share.percent) / 100.0 * total, 2)

        self.shares_total_percent = sum(flt(r.percent) for r in (self.shares or []))
        self.shares_total_amount = sum(flt(r.amount) for r in (self.shares or []))

    def _validate_shares(self):
        if not self.shares:
            return
        if self.method == "Thủ công":
            pct_total = sum(flt(r.percent) for r in self.shares)
            if abs(pct_total - 100.0) > 0.01:
                frappe.throw(
                    _("Manual allocation: shares total must equal 100% (got {0}%)").format(
                        round(pct_total, 2)
                    )
                )

    def before_submit(self):
        from vn_accounting.project_costing.services.allocation_engine import (
            validate_period_not_closed,
            validate_targets_not_invoiced,
        )
        validate_period_not_closed(self)
        validate_targets_not_invoiced(self)
        self.status = "Đã phân bổ"

    def on_submit(self):
        from vn_accounting.project_costing.services.allocation_engine import post_allocation_je
        post_allocation_je(self)
        self._warn_627_residual()
        self._warn_154_residual_closed_projects()

    def _warn_627_residual(self):
        """Lỗ hổng VAS #2: cuối kỳ TK 627 phải = 0. Warn nếu còn số dư sau kết chuyển."""
        if not self.company or not self.run_period_end:
            return
        residual = frappe.db.sql("""
            SELECT SUM(debit - credit) AS balance
            FROM `tabGL Entry`
            WHERE company = %s
              AND account LIKE '627%%'
              AND posting_date <= %s
              AND is_cancelled = 0
        """, (self.company, self.run_period_end), as_dict=True)
        balance = flt(residual[0].balance if residual else 0)
        if abs(balance) > 1:
            frappe.msgprint(
                _("Cảnh báo VAS: TK 627 còn số dư {0:,.0f} sau kết chuyển kỳ này. "
                  "Theo TT99/2025, cuối kỳ TK 627 phải được kết chuyển hết sang TK 154 "
                  "(hoặc TK 632 nếu vượt công suất bình thường). "
                  "Kiểm tra lại các chi phí SXC chưa được đưa vào đợt kết chuyển.").format(balance),
                title=_("TK 627 chưa kết chuyển hết"),
                indicator="orange",
            )

    def _warn_154_residual_closed_projects(self):
        """Lỗ hổng VAS #3: project đã hoàn thành mà TK 154 còn số dư → cần kết chuyển 154→632."""
        if not self.company:
            return
        projects = [s.project for s in (self.shares or []) if s.project]
        if not projects:
            return
        residuals = frappe.db.sql("""
            SELECT gl.project, SUM(gl.debit - gl.credit) AS balance
            FROM `tabGL Entry` gl
            JOIN `tabProject` p ON p.name = gl.project
            WHERE gl.company = %s
              AND gl.account LIKE '154%%'
              AND gl.project IN %s
              AND gl.is_cancelled = 0
              AND p.status = 'Completed'
            GROUP BY gl.project
            HAVING ABS(SUM(gl.debit - gl.credit)) > 1
        """, (self.company, projects), as_dict=True)
        if residuals:
            lines = ", ".join(f"{r.project}: {flt(r.balance):,.0f}" for r in residuals)
            frappe.msgprint(
                _("Cảnh báo: Các dự án đã hoàn thành nhưng TK 154 còn số dư: {0}. "
                  "Cần kết chuyển 154→632 (giá vốn) hoặc write-off 154→642 (chi phí QLDN) "
                  "để đóng sổ dự án.").format(lines),
                title=_("TK 154 dự án đã hoàn thành còn số dư"),
                indicator="orange",
            )

    def on_cancel(self):
        # GL Entry uses is_cancelled column, not docstatus → Frappe's back-link
        # check sees them as docstatus=1 and blocks cancel. Whitelist GL Entry +
        # Journal Entry (per ERPNext pattern in sales_invoice.py / pcv.py).
        # MUST set BEFORE engine call so nested ops respect it.
        self.ignore_linked_doctypes = ["GL Entry", "Stock Ledger Entry", "Payment Ledger Entry"]

        from vn_accounting.project_costing.services.allocation_engine import cancel_allocation_je
        cancel_allocation_je(self)

        # Use db.set_value: nested JE.cancel() during cancel_allocation_je creates
        # save events that can swallow status changes assigned to self.
        frappe.db.set_value("Cost Allocation Run", self.name, "status", "Đã hủy",
                            update_modified=False)
        self.status = "Đã hủy"  # in-memory sync
