"""Re-classification helpers — Phase 2b.

Item 1: reclassify_je_row(source_je, source_row, project, stage)
  → KTT pick 1 JE Account row đã post (vd Payroll JE Dr 622) + chọn project +
  stage → engine sinh JE bù Dr 154 (project, stage) / Cr <source row.account>.
  Cost re-attribute từ TK chung sang TK 154 công trình.

Item 3: on_salary_slip_submit
  → khi Salary Slip submit với project tag, auto sinh JE bù
  Dr 154 (project, stage) / Cr 622 (default direct labor account).
  Idempotent qua marker.
"""
from __future__ import annotations

import frappe
from frappe import _
from frappe.utils import flt

_MARKER_PREFIX = "PROJECT_COSTING"
_TYPE_RECLASSIFY = "JE_RECLASSIFY"
_TYPE_SALARY = "SALARY_REALLOCATE"


# ─────────────────────────────────────────────────────────────────────────────
# Item 1 — JE row re-classify helper
# ─────────────────────────────────────────────────────────────────────────────

def _marker_reclassify(project: str, source_row: str) -> str:
    return f"[{_MARKER_PREFIX}:{project}][TYPE:{_TYPE_RECLASSIFY}][SRC:JEA:{source_row}]"


def _validate_stage_not_invoiced(stage: str):
    """Guard 1: block reclassify to a stage that already has COGS recognized."""
    stage_data = frappe.db.get_value(
        "Project Costing Stage", stage,
        ["status", "cogs_je", "sales_invoice"],
        as_dict=True,
    )
    if not stage_data:
        return  # stage doesn't exist yet — allow (will be created)
    if stage_data.cogs_je:
        frappe.throw(
            _("Giai đoạn {0} đã xuất hóa đơn ({1}) và giá vốn đã được ghi nhận. "
              "Không thể thêm chi phí vào giai đoạn đã đóng sổ. "
              "Hủy hóa đơn trước nếu cần điều chỉnh chi phí.").format(
                stage, stage_data.sales_invoice or stage_data.cogs_je
            ),
            title=_("Giai đoạn đã khóa"),
        )


def _validate_row_not_already_reclassified(source_row: str):
    """Guard 2: block if source JE row already has a reclassify-bù JE (any project/stage)."""
    existing = frappe.db.get_value(
        "Journal Entry",
        {
            "user_remark": ["like", f"%[SRC:JEA:{source_row}]%"],
            "docstatus": 1,
        },
        ["name", "user_remark"],
        as_dict=True,
    )
    if existing:
        frappe.throw(
            _("Dòng bút toán này đã được phân bổ vào công trình (JE bù: {0}). "
              "Mỗi dòng chỉ được phân bổ 1 lần. "
              "Hủy JE bù cũ trước nếu cần chuyển sang công trình/giai đoạn khác.").format(
                existing.name
            ),
            title=_("Đã phân bổ"),
        )


@frappe.whitelist()
def reclassify_je_row(
    source_je: str, source_row: str,
    project: str, stage: str | None = None,
    amount: float | None = None,
) -> dict:
    """Create bù JE: Dr 154 (project, stage) / Cr <source_row.account>.

    Source row giữ nguyên. Bù JE độc lập, marker để cancel sau này.

    Guards:
    1. Stage đã xuất HĐ (cogs_je != NULL) → block
    2. Source row đã reclassify vào stage khác → block (prevent double-count)
    """
    if not (source_je and source_row and project):
        frappe.throw(_("Thiếu source_je / source_row / project"))

    # Guard 1: block reclassify to invoiced stage
    if stage:
        _validate_stage_not_invoiced(stage)

    # Guard 2: block if source row already reclassified to ANY project/stage
    _validate_row_not_already_reclassified(source_row)

    src = frappe.db.get_value(
        "Journal Entry Account", source_row,
        ["name", "parent", "account", "debit_in_account_currency",
         "credit_in_account_currency"],
        as_dict=True,
    )
    if not src or src.parent != source_je:
        frappe.throw(_("Row {0} không thuộc JE {1}").format(source_row, source_je))
    # Company lives on parent JE
    src.company = frappe.db.get_value("Journal Entry", source_je, "company")

    # Idempotency: existing bù JE for this source row + same project?
    marker = _marker_reclassify(project, source_row)
    existing = frappe.db.get_value(
        "Journal Entry",
        {"user_remark": ["like", f"%{marker}%"], "docstatus": 1},
        "name",
    )
    if existing:
        return {"je": existing, "status": "already_reclassified"}

    src_amount = flt(amount or src.debit_in_account_currency or src.credit_in_account_currency)
    if src_amount <= 0:
        frappe.throw(_("Số tiền phải > 0"))

    from vn_accounting.utils.account_resolver import resolve_account

    wip = resolve_account("wip_account_project_costing", src.company)
    if not wip:
        frappe.throw(_("VN Accounting Settings: chưa cấu hình TK WIP công trình"))

    # Auto-create Project Costing if missing
    from vn_accounting.project_costing.services.wip_override_engine import (
        _ensure_project_costing,
    )
    _ensure_project_costing(project)

    je = frappe.new_doc("Journal Entry")
    je.posting_date = frappe.utils.today()
    je.company = src.company
    je.voucher_type = "Journal Entry"
    je.user_remark = (
        f"{marker} "
        + _("Re-classify chi phí từ {0} sang công trình {1}").format(src.account, project)
    )
    je.append("accounts", {
        "account": wip,
        "debit_in_account_currency": src_amount,
        "project": project,
        "project_costing_stage": stage,
        "reference_type": "Project Costing",
        "reference_name": project,
        "user_remark": _("Tập hợp chi phí công trình {0}").format(project),
    })
    je.append("accounts", {
        "account": src.account,
        "credit_in_account_currency": src_amount,
        "reference_type": "Journal Entry",
        "reference_name": source_je,
        "user_remark": _("Đảo TK {0} từ JE {1}").format(src.account.split(" - ")[0], source_je),
    })
    je.flags.ignore_permissions = True
    je.insert()
    je.submit()

    return {"je": je.name, "status": "created", "amount": src_amount}


@frappe.whitelist()
def check_row_reclassify_status(source_row: str) -> dict:
    """Check if a JE Account row can be reclassified. Used by frontend for visual indicators."""
    existing = frappe.db.get_value(
        "Journal Entry",
        {"user_remark": ["like", f"%[SRC:JEA:{source_row}]%"], "docstatus": 1},
        "name",
    )
    return {
        "can_reclassify": not existing,
        "existing_je": existing,
    }


@frappe.whitelist()
def cancel_reclassify_for_je(source_je: str) -> int:
    """Cancel all reclassify-bù JEs whose marker references source_je rows."""
    rows = frappe.db.sql_list(
        """SELECT name FROM `tabJournal Entry`
           WHERE docstatus = 1 AND user_remark LIKE %s""",
        (f"%[TYPE:{_TYPE_RECLASSIFY}][SRC:JEA:%",),
    )
    n = 0
    for name in rows:
        # Check if any JEA row from source_je referenced
        if frappe.db.exists("Journal Entry Account",
                           {"parent": name, "reference_name": source_je}):
            doc = frappe.get_doc("Journal Entry", name)
            doc.flags.ignore_permissions = True
            doc.cancel()
            n += 1
    return n


# ─────────────────────────────────────────────────────────────────────────────
# Item 3 — Salary Slip on_submit bù engine
# ─────────────────────────────────────────────────────────────────────────────

def _marker_salary(project: str, ss_name: str) -> str:
    return f"[{_MARKER_PREFIX}:{project}][TYPE:{_TYPE_SALARY}][SS:{ss_name}]"


def on_salary_slip_submit(doc, method=None):
    """If SS has project tag → post bù JE Dr 154 (project) / Cr 622.

    Amount = SS.net_pay. Reflects VAS TT99 xây lắp: lương → 154 SPDD.
    Assumes Payroll Entry later posts standard Dr 622 / Cr 334 — bù JE
    Cr 622 cancels Dr 622 → net cost moves to 154.
    """
    if doc.docstatus != 1:
        return
    project = (doc.get("project") or "").strip()
    if not project:
        return
    stage = doc.get("project_costing_stage")

    # Guard: block if target stage already invoiced
    if stage:
        stage_data = frappe.db.get_value(
            "Project Costing Stage", stage, ["cogs_je"], as_dict=True,
        )
        if stage_data and stage_data.cogs_je:
            frappe.log_error(
                title="Salary reclassify blocked — stage invoiced",
                message=f"SS {doc.name}: stage {stage} already has cogs_je {stage_data.cogs_je}",
            )
            return

    amount = flt(doc.net_pay or doc.gross_pay or 0)
    if amount <= 0:
        return

    # Idempotent
    marker = _marker_salary(project, doc.name)
    if frappe.db.exists(
        "Journal Entry",
        {"user_remark": ["like", f"%{marker}%"], "docstatus": 1},
    ):
        return

    from vn_accounting.utils.account_resolver import resolve_account

    _company = doc.company
    wip = resolve_account("wip_account_project_costing", _company)
    direct_labor = resolve_account("direct_labor_account_project_costing", _company)
    if not (wip and direct_labor):
        frappe.log_error(
            title="Salary Slip reclassify skipped",
            message=(
                f"SS {doc.name}: VN Accounting Settings missing "
                f"wip_account_project_costing or direct_labor_account_project_costing"
            ),
        )
        return

    from vn_accounting.project_costing.services.wip_override_engine import (
        _ensure_project_costing,
    )
    _ensure_project_costing(project)

    je = frappe.new_doc("Journal Entry")
    je.posting_date = doc.posting_date or frappe.utils.today()
    je.company = doc.company
    je.voucher_type = "Journal Entry"
    je.user_remark = (
        f"{marker} "
        + _("Phân bổ lương {0} vào công trình {1}").format(doc.name, project)
    )
    je.append("accounts", {
        "account": wip,
        "debit_in_account_currency": amount,
        "project": project,
        "project_costing_stage": stage,
        "reference_type": "Project Costing",
        "reference_name": project,
        "user_remark": _("Tập hợp lương vào TK WIP công trình {0}").format(project),
    })
    je.append("accounts", {
        "account": direct_labor,
        "credit_in_account_currency": amount,
        "reference_type": "Journal Entry",
        "reference_name": doc.name,
        "user_remark": _("Đảo TK lương trực tiếp"),
    })
    je.flags.ignore_permissions = True
    je.insert()
    je.submit()


def on_salary_slip_cancel(doc, method=None):
    """Cancel matching bù JE on SS cancel."""
    project = (doc.get("project") or "").strip()
    if not project:
        return
    marker = _marker_salary(project, doc.name)
    je_name = frappe.db.get_value(
        "Journal Entry",
        {"user_remark": ["like", f"%{marker}%"], "docstatus": 1},
        "name",
    )
    if not je_name:
        return
    je = frappe.get_doc("Journal Entry", je_name)
    je.flags.ignore_permissions = True
    je.cancel()


# ─────────────────────────────────────────────────────────────────────────────
# Item 2 — CAR autofill shares from Timesheet
# ─────────────────────────────────────────────────────────────────────────────

@frappe.whitelist()
def autofill_shares_from_timesheet(
    employee: str, period_start: str, period_end: str,
) -> list[dict]:
    """SUM(Timesheet Detail.hours) grouped by project for an employee in period.

    Returns list of {project, hours, percent} normalized so Σ percent = 100.
    KTT applies returned shares to Cost Allocation Run.shares table client-side.
    """
    if not (employee and period_start and period_end):
        frappe.throw(_("Thiếu employee / period"))

    rows = frappe.db.sql("""
        SELECT td.project AS project, SUM(td.hours) AS hours
        FROM `tabTimesheet Detail` td
        JOIN `tabTimesheet` ts ON ts.name = td.parent
        WHERE ts.docstatus = 1
          AND ts.employee = %(emp)s
          AND td.project IS NOT NULL AND td.project != ''
          AND COALESCE(DATE(td.from_time), ts.start_date) BETWEEN %(start)s AND %(end)s
        GROUP BY td.project
        ORDER BY hours DESC
    """, {"emp": employee, "start": period_start, "end": period_end}, as_dict=True)

    total = sum(flt(r.hours) for r in rows)
    if total <= 0:
        return []

    shares = []
    cum_pct = 0.0
    for i, r in enumerate(rows):
        if i == len(rows) - 1:
            # Last row absorbs residue
            pct = round(100.0 - cum_pct, 2)
        else:
            pct = round(flt(r.hours) / total * 100, 2)
            cum_pct += pct
        shares.append({
            "project": r.project,
            "hours": flt(r.hours),
            "percent": pct,
        })
    return shares
