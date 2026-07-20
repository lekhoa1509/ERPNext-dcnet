"""Cost Allocation Run GL posting engine per BL §10.2 + §11.2.

On Cost Allocation Run submit:
    Dr 154 (project=A) / Cr 627    (per share, from Settings TK)
    Dr 154 (project=B) / Cr 627
    ...

Each row carries reference_type="Cost Allocation Run", reference_name=<CAR>.
Marker: [PROJECT_COSTING:<CAR>][TYPE:ALLOCATION_RUN]. CAR.generated_je stores
the JE ref for cancel reverse.

R10.5 validations on before_submit:
  - Period not within a closed PCV
  - No target project has SI submitted within run_period for this stage chain
"""
from __future__ import annotations

import frappe
from frappe import _
from frappe.utils import flt

_MARKER_PREFIX = "PROJECT_COSTING"
_TYPE = "ALLOCATION_RUN"


def _marker(car_name: str) -> str:
    return f"[{_MARKER_PREFIX}:{car_name}][TYPE:{_TYPE}]"


def _load_settings_accounts(company: str) -> dict[str, str | None]:
    """Return WIP + Overhead accounts from Settings, company-scoped."""
    from vn_accounting.utils.account_resolver import resolve_account
    return {
        "wip": resolve_account("wip_account_project_costing", company),
        "overhead": resolve_account("overhead_collector_account", company),
    }


def _ensure_project_costing_for_share(project: str):
    """Auto-create Project Costing master if not exists (per share project)."""
    if frappe.db.exists("Project Costing", project):
        return
    p = frappe.db.get_value(
        "Project", project, ["project_name", "customer", "company"], as_dict=True
    )
    if not p:
        return
    pc = frappe.new_doc("Project Costing")
    pc.project = project
    pc.project_name = p.project_name
    pc.customer = p.customer
    pc.company = p.company
    pc.flags.ignore_permissions = True
    pc.insert()


def post_allocation_je(car_doc) -> str | None:
    """Submit JE for a Cost Allocation Run. Returns JE name."""
    if car_doc.docstatus != 1:
        return None
    # Idempotent: if generated_je already submitted, skip
    if car_doc.generated_je:
        st = frappe.db.get_value("Journal Entry", car_doc.generated_je, "docstatus")
        if st == 1:
            return car_doc.generated_je

    accounts = _load_settings_accounts(car_doc.company)
    wip_acc = accounts["wip"]
    # source_credit_account on CAR overrides Settings overhead default — KTT
    # set TK 622 cho phân bổ lương, TK 6424 cho khấu hao, TK 627 default cho
    # chi phí gián tiếp chung.
    overhead_acc = car_doc.get("source_credit_account") or accounts["overhead"]
    if not (wip_acc and overhead_acc):
        frappe.throw(_("Thiếu cấu hình TK WIP / TK ghi Có cho Đợt phân bổ"))

    # Aggregate by (project, wip_account_override, stage). Stage is per-share
    # — if KTT chose a stage on the share, JE row goes to that stage; if
    # empty, JE row vào Common Pool của project.
    by_share: dict[tuple[str, str, str], float] = {}
    for share in (car_doc.shares or []):
        amt = flt(share.amount)
        if amt <= 0:
            continue
        wip = share.wip_account or wip_acc
        stage = share.get("project_costing_stage") or ""
        # Guard: block allocation to invoiced stage
        if stage:
            cogs_je = frappe.db.get_value("Project Costing Stage", stage, "cogs_je")
            if cogs_je:
                frappe.throw(
                    _("Giai đoạn {0} đã xuất hóa đơn (COGS JE: {1}). "
                      "Không thể phân bổ chi phí vào giai đoạn đã khóa.").format(stage, cogs_je),
                    title=_("Giai đoạn đã khóa"),
                )
        key = (share.project, wip, stage)
        by_share[key] = by_share.get(key, 0) + amt

    cr_total = sum(by_share.values())
    if cr_total <= 0:
        return None

    # Auto-create Project Costing for each project (idempotent)
    for project, _wip, _stage in by_share.keys():
        _ensure_project_costing_for_share(project)

    je = frappe.new_doc("Journal Entry")
    je.posting_date = car_doc.posting_date
    je.company = car_doc.company
    je.voucher_type = "Journal Entry"
    je.user_remark = (
        f"{_marker(car_doc.name)} "
        + _("Phân bổ chi phí gián tiếp kỳ {0} → {1}").format(
            car_doc.run_period_start, car_doc.run_period_end
        )
    )

    for (project, wip, stage), amt in by_share.items():
        row = {
            "account": wip,
            "debit_in_account_currency": amt,
            "project": project,
            "reference_type": "Cost Allocation Run",
            "reference_name": car_doc.name,
            "user_remark": (
                _("Phân bổ vào {0} — giai đoạn {1}").format(project, stage)
                if stage else
                _("Phân bổ vào công trình {0} (chưa gắn giai đoạn)").format(project)
            ),
        }
        if stage:
            row["project_costing_stage"] = stage
        je.append("accounts", row)
    je.append("accounts", {
        "account": overhead_acc,
        "credit_in_account_currency": cr_total,
        "reference_type": "Cost Allocation Run",
        "reference_name": car_doc.name,
        "user_remark": _("Đảo TK gom chi phí gián tiếp"),
    })
    je.flags.ignore_permissions = True
    je.insert()
    je.submit()

    # Set generated_je on CAR (using db.set_value to avoid recursive validate)
    frappe.db.set_value(
        "Cost Allocation Run", car_doc.name,
        {"generated_je": je.name},
        update_modified=False,
    )
    return je.name


def cancel_allocation_je(car_doc) -> bool:
    """Cancel the linked generated_je. Returns True if a JE was cancelled."""
    je_name = car_doc.generated_je
    if not je_name:
        return False
    st = frappe.db.get_value("Journal Entry", je_name, "docstatus")
    if st != 1:
        return False
    je = frappe.get_doc("Journal Entry", je_name)
    je.flags.ignore_permissions = True
    je.cancel()
    return True


# ─────────────────────────────────────────────────────────────────────────────
# Validations — wired into CAR controller before_submit
# ─────────────────────────────────────────────────────────────────────────────


def validate_period_not_closed(car_doc):
    """Reject if run_period overlaps a Period Closing Voucher for this company."""
    pcv = frappe.db.sql("""
        SELECT name, period_end_date FROM `tabPeriod Closing Voucher`
        WHERE company = %s AND docstatus = 1
          AND period_end_date >= %s
        ORDER BY period_end_date DESC LIMIT 1
    """, (car_doc.company, car_doc.run_period_start), as_dict=True)
    if pcv:
        frappe.throw(
            _("Kỳ {0}–{1} thuộc kỳ đã đóng sổ ({2}). Lùi sang kỳ sau hoặc mở lại PCV.").format(
                car_doc.run_period_start, car_doc.run_period_end, pcv[0].name
            )
        )


def validate_targets_not_invoiced(car_doc):
    """R10.5: reject if any share project has stage SI submitted within run_period.

    Phase 2 lenient version: only blocks if there's an EXISTING submitted CAR
    posting to same projects in same period (avoid duplicate posting). Full
    R10.5 stage-SI cross-check defers to Phase 3 when stage→SI link is reliable.
    """
    target_projects = [s.project for s in (car_doc.shares or [])]
    if not target_projects:
        return
    # Check for prior submitted CAR with overlapping period + overlapping projects
    placeholders = ", ".join(["%s"] * len(target_projects))
    existing = frappe.db.sql(f"""
        SELECT DISTINCT car.name
        FROM `tabCost Allocation Run` car
        JOIN `tabCost Allocation Share` cs ON cs.parent = car.name
        WHERE car.company = %s
          AND car.docstatus = 1
          AND car.name != %s
          AND car.run_period_start = %s
          AND car.run_period_end = %s
          AND cs.project IN ({placeholders})
    """, (car_doc.company, car_doc.name or "",
          car_doc.run_period_start, car_doc.run_period_end, *target_projects), as_dict=True)
    if existing:
        names = ", ".join(e.name for e in existing)
        frappe.throw(
            _("Đã có Đợt phân bổ khác cho kỳ này cùng project: {0}. "
              "Hủy đợt cũ trước hoặc đổi kỳ.").format(names)
        )
