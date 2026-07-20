"""Pivot Tool server endpoints — 4 whitelisted methods per tech mapping §7.

get_pivot_data(costing_name)         → full layout for UI render
pin_cost_to_stage(source, row, stage)→ update project_costing_stage CF on source row
recalculate_stage_price(stage_name)  → re-derive price_suggested via markup_calc
generate_stage_si(stage_name)        → create SI draft for stage
"""
from __future__ import annotations

import frappe
from frappe import _
from frappe.utils import flt

from vn_accounting.project_costing.services.markup_calc import calculate_price


# ─────────────────────────────────────────────────────────────────────────────
# Cost source listing — walks PI/SE/DN/EC/Timesheet for project-tagged rows
# ─────────────────────────────────────────────────────────────────────────────


def _list_costs_for_project(project: str) -> list[dict]:
    """Return all cost rows tagged to this project (across 5 source DocTypes).

    Each row shape:
      {source_doctype, source_name, source_row, amount, posting_date,
       description, stage}
    `stage` = None for unpinned (Common Pool).
    """
    out: list[dict] = []

    # PI Items — parent.project (Accounting Dimension header) WINS over Item.project.
    # ERPNext auto-fills Item.project from Item Default but doesn't re-propagate
    # when user sets project on PI header later. User's header tag is the
    # authoritative intent — so we prefer it. If parent.project is blank,
    # fallback to Item.project (legacy item-row tagging).
    for r in frappe.db.sql("""
        SELECT pi.name AS parent, pii.name AS row_name,
               pi.posting_date, pi.supplier AS party,
               pii.item_code AS item, pii.item_name AS item_name,
               pii.base_net_amount AS amount,
               pii.project_costing_stage AS stage,
               pii.project AS item_project, pi.project AS parent_project
        FROM `tabPurchase Invoice Item` pii
        JOIN `tabPurchase Invoice` pi ON pi.name = pii.parent
        WHERE pi.docstatus = 1
          AND COALESCE(NULLIF(pi.project, ''), pii.project) = %s
    """, (project,), as_dict=True):
        # Warn user if Item.project differs from parent — likely auto-fill leak
        warn = ""
        if r.item_project and r.parent_project and r.item_project != r.parent_project:
            warn = f" ⚠ Item.project={r.item_project}"
        out.append({
            "source_doctype": "Purchase Invoice",
            "source_name": r.parent,
            "source_row": r.row_name,
            "amount": flt(r.amount),
            "posting_date": r.posting_date,
            "description": f"{r.party or ''} — {r.item_name or r.item or ''}{warn}",
            "stage": r.stage,
        })

    # Stock Entry — Material Issue. Parent SE.project ưu tiên; nếu parent
    # blank, fallback child Stock Entry Detail.project.
    # Output: 1 row per SE (parent-level UX). Mixed-project SE → warning.
    for r in frappe.db.sql("""
        SELECT se.name, se.posting_date, se.total_outgoing_value AS total,
               se.stock_entry_type, se.project_costing_stage AS stage,
               se.project AS parent_project,
               GROUP_CONCAT(DISTINCT NULLIF(sed.project, '')) AS row_projects,
               SUM(CASE WHEN sed.project = %(project)s THEN sed.amount ELSE 0 END) AS matched_row_amount
        FROM `tabStock Entry` se
        LEFT JOIN `tabStock Entry Detail` sed ON sed.parent = se.name
        WHERE se.docstatus = 1
          AND se.stock_entry_type = 'Material Issue'
          AND (
            se.project = %(project)s
            OR ((se.project IS NULL OR se.project = '') AND sed.project = %(project)s)
          )
        GROUP BY se.name
    """, {"project": project}, as_dict=True):
        # Amount: parent matched → use total_outgoing_value; row-only match →
        # use sum of matching rows
        if r.parent_project == project:
            amt = flt(r.total)
        else:
            amt = flt(r.matched_row_amount)

        warn = ""
        if r.row_projects and r.parent_project and r.row_projects != r.parent_project:
            warn = f" ⚠ rows.project={r.row_projects}"

        out.append({
            "source_doctype": "Stock Entry",
            "source_name": r.name,
            "source_row": None,
            "amount": amt,
            "posting_date": r.posting_date,
            "description": _("Xuất kho {0}{1}").format(r.name, warn),
            "stage": r.stage,
        })

    # DN Items — COALESCE(item.project, parent.project) — same reason as PI
    for r in frappe.db.sql("""
        SELECT dn.name AS parent, dni.name AS row_name,
               dn.posting_date, dn.customer AS party,
               dni.item_code AS item, dni.item_name AS item_name,
               dni.base_net_amount AS amount,
               dni.project_costing_stage AS stage
        FROM `tabDelivery Note Item` dni
        JOIN `tabDelivery Note` dn ON dn.name = dni.parent
        WHERE dn.docstatus = 1
          AND COALESCE(NULLIF(dn.project, ''), dni.project) = %s
    """, (project,), as_dict=True):
        out.append({
            "source_doctype": "Delivery Note",
            "source_name": r.parent,
            "source_row": r.row_name,
            "amount": flt(r.amount),
            "posting_date": r.posting_date,
            "description": f"{r.party or ''} — {r.item_name or r.item or ''}",
            "stage": r.stage,
        })

    # Expense Claim — parent.project ưu tiên; nếu blank, fallback child rows.
    for r in frappe.db.sql("""
        SELECT ec.name, ec.posting_date, ec.total_claimed_amount AS total,
               ec.employee, ec.employee_name, ec.project_costing_stage AS stage,
               ec.project AS parent_project,
               GROUP_CONCAT(DISTINCT NULLIF(ecd.project, '')) AS row_projects,
               SUM(CASE WHEN ecd.project = %(project)s THEN ecd.amount ELSE 0 END) AS matched_row_amount
        FROM `tabExpense Claim` ec
        LEFT JOIN `tabExpense Claim Detail` ecd ON ecd.parent = ec.name
        WHERE ec.docstatus = 1
          AND (
            ec.project = %(project)s
            OR ((ec.project IS NULL OR ec.project = '') AND ecd.project = %(project)s)
          )
        GROUP BY ec.name
    """, {"project": project}, as_dict=True):
        amt = flt(r.total) if r.parent_project == project else flt(r.matched_row_amount)
        warn = ""
        if r.row_projects and r.parent_project and r.row_projects != r.parent_project:
            warn = f" ⚠ rows.project={r.row_projects}"
        out.append({
            "source_doctype": "Expense Claim",
            "source_name": r.name,
            "source_row": None,
            "amount": amt,
            "posting_date": r.posting_date,
            "description": _("Hoàn ứng {0}{1}").format(
                r.employee_name or r.employee or r.name, warn),
            "stage": r.stage,
        })

    # Journal Entry Account (row-level) — KTT post Dr <WIP/expense> trực tiếp
    # với project tag (vd: thanh toán đặt cọc thầu phụ chưa qua PI, JE bù tay).
    # Loại trừ JE do engine tự sinh (reference_type IN project costing types) để
    # tránh đếm trùng với CAR allocation và WIP override.
    for r in frappe.db.sql("""
        SELECT je.name AS parent, jea.name AS row_name,
               je.posting_date,
               jea.account AS account,
               jea.debit_in_account_currency AS debit,
               jea.credit_in_account_currency AS credit,
               jea.project_costing_stage AS stage
        FROM `tabJournal Entry Account` jea
        JOIN `tabJournal Entry` je ON je.name = jea.parent
        WHERE je.docstatus = 1
          AND jea.project = %s
          AND jea.debit_in_account_currency > 0
          AND COALESCE(jea.reference_type, '') NOT IN ('Project Costing', 'Cost Allocation Run')
    """, (project,), as_dict=True):
        out.append({
            "source_doctype": "Journal Entry",
            "source_name": r.parent,
            "source_row": r.row_name,
            "amount": flt(r.debit),
            "posting_date": r.posting_date,
            "description": _("JE thủ công — TK {0}").format(r.account.split(' - ')[0] if r.account else ''),
            "stage": r.stage,
        })

    # Cost Allocation Run output JE rows — chi phí gián tiếp (TK 627) đã
    # phân bổ vào TK 154 per project qua CAR. Stage tag set tại CAR Share;
    # NULL = vào Tập hợp chi phí chưa gắn (KTT pin sau qua Pivot).
    # Đây là CHỨC NĂNG VAS chuẩn: chi phí gián tiếp phải vào COGS/154 trước
    # khi recognize doanh thu, không được để "treo" cuối kỳ.
    for r in frappe.db.sql("""
        SELECT je.name AS parent, jea.name AS row_name,
               je.posting_date,
               jea.account AS account,
               jea.debit_in_account_currency AS amount,
               jea.project_costing_stage AS stage,
               jea.reference_name AS car_name
        FROM `tabJournal Entry Account` jea
        JOIN `tabJournal Entry` je ON je.name = jea.parent
        WHERE je.docstatus = 1
          AND jea.project = %s
          AND jea.debit_in_account_currency > 0
          AND jea.reference_type = 'Cost Allocation Run'
    """, (project,), as_dict=True):
        acc_code = (r.account.split(' - ')[0] if r.account else '').strip()
        out.append({
            "source_doctype": "Journal Entry",
            "source_name": r.parent,
            "source_row": r.row_name,
            "amount": flt(r.amount),
            "posting_date": r.posting_date,
            "description": _("Phân bổ CP gián tiếp — TK {0} (từ {1})").format(
                acc_code, r.car_name or "?"
            ),
            "stage": r.stage,
        })

    # Asset Repair — sửa thiết bị thi công tag project (parent-level)
    for r in frappe.db.sql("""
        SELECT name AS source_name, completion_date AS posting_date,
               asset_name, total_repair_cost AS amount,
               project_costing_stage AS stage
        FROM `tabAsset Repair`
        WHERE docstatus = 1
          AND project = %s
          AND repair_status = 'Completed'
    """, (project,), as_dict=True):
        out.append({
            "source_doctype": "Asset Repair",
            "source_name": r.source_name,
            "source_row": None,
            "amount": flt(r.amount),
            "posting_date": r.posting_date,
            "description": _("Sửa chữa {0}").format(r.asset_name or r.source_name),
            "stage": r.stage,
        })

    # NOTE: Timesheet đã được LOẠI khỏi nguồn chi phí (Phase 1.1 fix).
    # Timesheet là labor TRACKING (đo giờ), KHÔNG phát sinh GL Entry. Lương
    # kỹ sư on-site hạch toán qua Salary Slip (Dr 622 / Cr 334) — không qua
    # Timesheet. Phase 2 sẽ thêm Salary Slip cost source.
    # Tham chiếu: BL spec R3.3 sẽ được update.

    return out


def _update_stage_cost_pinned(stage_name: str):
    """Sum costs pinned to stage → write to Stage.cost_pinned + recompute price."""
    parent_costing = frappe.db.get_value("Project Costing Stage", stage_name, "parent_costing")
    if not parent_costing:
        return
    project = frappe.db.get_value("Project Costing", parent_costing, "project")
    if not project:
        return
    costs = _list_costs_for_project(project)
    pinned_sum = sum(c["amount"] for c in costs if c["stage"] == stage_name)

    # Pre-compute price via markup_calc (pure function)
    stage = frappe.db.get_value(
        "Project Costing Stage", stage_name,
        ["markup_method", "markup_value"], as_dict=True
    )
    price = calculate_price(
        method=stage.markup_method,
        markup_value=stage.markup_value,
        cost_pinned=pinned_sum,
        parent_costing=parent_costing,
    ) if stage else 0

    frappe.db.set_value(
        "Project Costing Stage", stage_name,
        {"cost_pinned": pinned_sum, "price_suggested": price},
        update_modified=False,
    )


# ─────────────────────────────────────────────────────────────────────────────
# Whitelisted endpoints
# ─────────────────────────────────────────────────────────────────────────────


@frappe.whitelist()
def get_pivot_data(costing_name: str) -> dict:
    """Full data dump for Pivot Tool render.

    Returns:
        {
          "costing": {name, project, customer, company, status},
          "stages":  [{...stage fields..., "pinned_total": float, "items": []}],
          "common_pool": [...],   # items with stage = None
          "settings":  {wip, overhead, cogs, writeoff}
        }
    """
    costing = frappe.db.get_value(
        "Project Costing", costing_name,
        ["name", "project", "project_name", "customer", "company", "status",
         "contract", "markup_default_method", "closed_on", "writeoff_je"],
        as_dict=True,
    )
    if not costing:
        return {}

    stages = frappe.db.get_all(
        "Project Costing Stage",
        filters={"parent_costing": costing_name},
        fields=["name", "stage_order", "stage_name", "status",
                "expected_invoice_date", "markup_method", "markup_value",
                "planned_amount", "cost_pinned", "price_suggested",
                "price_override", "override_reason", "override_by", "override_on",
                "sales_invoice", "cogs_je"],
        order_by="stage_order asc",
    )

    costs = _list_costs_for_project(costing.project)

    # Group by stage
    by_stage: dict[str, list[dict]] = {}
    common_pool: list[dict] = []
    for c in costs:
        if c["stage"]:
            by_stage.setdefault(c["stage"], []).append(c)
        else:
            common_pool.append(c)

    # All SIs linked per stage (multi-SI support — chia hóa đơn theo đợt thu tiền)
    stage_names = [s["name"] for s in stages]
    si_by_stage: dict[str, list[dict]] = {}
    if stage_names:
        placeholders = ",".join(["%s"] * len(stage_names))
        for r in frappe.db.sql(
            f"""SELECT name, project_costing_stage AS stage, base_grand_total AS amount,
                       docstatus, status, posting_date
                FROM `tabSales Invoice`
                WHERE project_costing_stage IN ({placeholders}) AND docstatus < 2
                ORDER BY posting_date DESC, name DESC""",
            stage_names,
            as_dict=True,
        ):
            si_by_stage.setdefault(r["stage"], []).append(r)

    for s in stages:
        s["items"] = by_stage.get(s["name"], [])
        s["pinned_total"] = sum(it["amount"] for it in s["items"])
        s["invoices"] = si_by_stage.get(s["name"], [])
        s["invoiced_total"] = sum(flt(si["amount"]) for si in s["invoices"])

    from vn_accounting.utils.account_resolver import resolve_account

    _company = costing.get("company") or frappe.defaults.get_user_default("Company")
    settings = {
        "wip": resolve_account("wip_account_project_costing", _company),
        "overhead": resolve_account("overhead_collector_account", _company),
        "cogs": resolve_account("cogs_account_project_costing", _company),
        "writeoff": resolve_account("writeoff_account_project_costing", _company),
    }

    return {
        "costing": costing,
        "stages": stages,
        "common_pool": common_pool,
        "settings": settings,
    }


@frappe.whitelist()
def pin_cost_to_stage(
    source_doctype: str,
    source_name: str,
    stage_name: str | None = None,
    source_row: str | None = None,
) -> dict:
    """Update project_costing_stage on a chứng từ row (or parent).

    Args:
        source_doctype: PI / SE / DN / EC / Timesheet
        source_name: parent name
        stage_name: stage to pin (None = unpin → Common Pool)
        source_row: child row name (None for parent-level — SE/EC)

    Returns:
        {"stage": <new stage>, "cost_pinned": float, "price_suggested": float}
    """
    # Validate stage exists (or is empty for unpin)
    if stage_name and not frappe.db.exists("Project Costing Stage", stage_name):
        frappe.throw(_("Stage {0} not found").format(stage_name))

    # Guard: block pinning TO a stage that already has COGS recognized
    if stage_name:
        cogs_je = frappe.db.get_value("Project Costing Stage", stage_name, "cogs_je")
        if cogs_je:
            frappe.throw(
                _("Giai đoạn {0} đã xuất hóa đơn và giá vốn đã khóa (COGS JE: {1}). "
                  "Không thể gắn thêm chi phí vào giai đoạn này.").format(stage_name, cogs_je),
                title=_("Giai đoạn đã khóa"),
            )

    # Guard: block unpinning FROM a stage that already has COGS recognized
    if not stage_name and source_row:
        # Find current stage of this row
        child_dt_map = {"Purchase Invoice": "Purchase Invoice Item", "Delivery Note": "Delivery Note Item",
                        "Timesheet": "Timesheet Detail", "Journal Entry": "Journal Entry Account"}
        child_dt = child_dt_map.get(source_doctype)
        if child_dt:
            cur_stage = frappe.db.get_value(child_dt, source_row, "project_costing_stage")
            if cur_stage:
                cogs_je = frappe.db.get_value("Project Costing Stage", cur_stage, "cogs_je")
                if cogs_je:
                    frappe.throw(
                        _("Chi phí này thuộc giai đoạn {0} đã xuất hóa đơn (COGS JE: {1}). "
                          "Không thể bỏ gắn hoặc chuyển sang giai đoạn khác.").format(cur_stage, cogs_je),
                        title=_("Giai đoạn đã khóa"),
                    )

    # Determine which DocType + record to update
    PARENT_LEVEL = {"Stock Entry", "Expense Claim", "Sales Invoice"}
    CHILD_MAP = {
        "Purchase Invoice": "Purchase Invoice Item",
        "Delivery Note": "Delivery Note Item",
        "Timesheet": "Timesheet Detail",
        "Journal Entry": "Journal Entry Account",
    }

    if source_doctype in PARENT_LEVEL:
        # Update parent doc directly
        if not frappe.db.exists(source_doctype, source_name):
            frappe.throw(_("{0} {1} not found").format(source_doctype, source_name))
        frappe.db.set_value(
            source_doctype, source_name,
            "project_costing_stage", stage_name,
            update_modified=False,
        )
    elif source_doctype in CHILD_MAP:
        if not source_row:
            frappe.throw(_("source_row is required for {0}").format(source_doctype))
        child_dt = CHILD_MAP[source_doctype]
        if not frappe.db.exists(child_dt, source_row):
            frappe.throw(_("{0} row {1} not found").format(child_dt, source_row))
        frappe.db.set_value(
            child_dt, source_row,
            "project_costing_stage", stage_name,
            update_modified=False,
        )
    else:
        frappe.throw(_("Unsupported source doctype: {0}").format(source_doctype))

    # Recompute affected stages
    if stage_name:
        _update_stage_cost_pinned(stage_name)

    # Find the OLD stage from this row's prior state and refresh that too.
    # (Caller may not know it — query in same record after update.)
    # For simplicity Phase 1: just recompute stage_name (new). Old stage
    # totals will refresh next time get_pivot_data is called.
    return {
        "stage": stage_name,
        "cost_pinned": frappe.db.get_value(
            "Project Costing Stage", stage_name, "cost_pinned"
        ) if stage_name else 0,
        "price_suggested": frappe.db.get_value(
            "Project Costing Stage", stage_name, "price_suggested"
        ) if stage_name else 0,
    }


@frappe.whitelist()
def recalculate_stage_price(stage_name: str) -> dict:
    """Recompute price_suggested for a stage based on current cost_pinned + markup config.

    Useful when KTT changes markup_method / markup_value, OR after batch pin
    operations.
    """
    if not frappe.db.exists("Project Costing Stage", stage_name):
        frappe.throw(_("Stage {0} not found").format(stage_name))
    _update_stage_cost_pinned(stage_name)
    return {
        "cost_pinned": frappe.db.get_value("Project Costing Stage", stage_name, "cost_pinned"),
        "price_suggested": frappe.db.get_value("Project Costing Stage", stage_name, "price_suggested"),
        "price_override": frappe.db.get_value("Project Costing Stage", stage_name, "price_override"),
    }


@frappe.whitelist()
def generate_stage_si(
    stage_name: str,
    amount: float | None = None,
    description: str | None = None,
) -> dict:
    """Create Sales Invoice draft from stage.

    1 item line: "[project_name] — [stage_name]", rate = `amount` if provided
    else (price_override or price_suggested - sum already-invoiced).
    Sets SI.project_costing_stage = stage_name (CF). Stage.sales_invoice points
    to the LATEST SI created (legacy field, list of all SIs available via
    get_stage_invoices RPC).

    Multiple SIs per stage are allowed (chia hóa đơn theo đợt thu tiền — vd
    30%/70% hoặc 30/30/40). Each SI submit recognizes COGS amount based on
    its own grand_total.
    """
    stage = frappe.db.get_value(
        "Project Costing Stage", stage_name,
        ["name", "stage_name", "parent_costing", "price_suggested",
         "price_override", "sales_invoice"],
        as_dict=True,
    )
    if not stage:
        frappe.throw(_("Không tìm thấy giai đoạn {0}").format(stage_name))

    parent = frappe.db.get_value(
        "Project Costing", stage.parent_costing,
        ["project", "project_name", "customer", "company"],
        as_dict=True,
    )
    if not parent or not parent.customer:
        frappe.throw(_("Công trình {0} chưa có khách hàng — không thể tạo hóa đơn").format(
            stage.parent_costing))

    # Default amount = remaining un-invoiced = stage price - sum of existing SIs
    if amount is None or flt(amount) <= 0:
        target_price = flt(stage.price_override) or flt(stage.price_suggested)
        if target_price <= 0:
            frappe.throw(_("Giai đoạn chưa có giá — cấu hình markup hoặc nhập số tiền hóa đơn trực tiếp."))
        already = flt(frappe.db.sql(
            """SELECT IFNULL(SUM(base_grand_total), 0)
               FROM `tabSales Invoice`
               WHERE docstatus < 2 AND project_costing_stage = %s""",
            (stage_name,),
        )[0][0])
        remaining = target_price - already
        if remaining <= 0:
            frappe.throw(_("Đã xuất đủ hóa đơn cho giai đoạn — tổng hiện tại {0} ≥ giá {1}. Nếu cần xuất thêm, nhập số tiền cụ thể.").format(
                frappe.utils.fmt_money(already, currency="VND"),
                frappe.utils.fmt_money(target_price, currency="VND"),
            ))
        amount = remaining

    item_code = _get_or_create_placeholder_item(parent.company)
    desc = description or f"{parent.project_name} — {stage.stage_name}"

    si = frappe.new_doc("Sales Invoice")
    si.customer = parent.customer
    si.company = parent.company
    si.project = parent.project
    si.project_costing_stage = stage_name
    si.append("items", {
        "item_code": item_code,
        "qty": 1,
        "rate": flt(amount),
        "description": desc,
        "project_costing_stage": stage_name,
        "project": parent.project,
    })
    si.flags.ignore_permissions = True
    si.insert()

    # Link back from stage (latest SI). Status: bump to "Đã có SI draft" if still
    # earlier in the flow; leave alone if already "Đã xuất HĐ" / "Đã thu tiền".
    cur_status = frappe.db.get_value("Project Costing Stage", stage_name, "status") or ""
    new_status = cur_status if cur_status in ("Đã xuất HĐ", "Đã thu tiền") else "Đã có SI draft"
    frappe.db.set_value(
        "Project Costing Stage", stage_name,
        {"sales_invoice": si.name, "status": new_status},
        update_modified=False,
    )

    return {
        "sales_invoice": si.name,
        "url": f"/app/sales-invoice/{si.name}",
    }


@frappe.whitelist()
def generate_project_si(
    project_costing: str,
    amount: float,
    description: str | None = None,
) -> dict:
    """Create Sales Invoice draft at PROJECT level (not tied to a stage).

    Use cases: tạm ứng/đặt cọc chung dự án, thanh toán tổng kết không theo
    giai đoạn, hóa đơn bổ sung. SI có project tag nhưng không có stage tag
    → revenue ghi nhận, COGS không tự sinh per-stage (KTT phải close_engine
    để recognize residue).
    """
    pc = frappe.db.get_value(
        "Project Costing", project_costing,
        ["project", "project_name", "customer", "company"],
        as_dict=True,
    )
    if not pc:
        frappe.throw(_("Không tìm thấy công trình {0}").format(project_costing))
    if not pc.customer:
        frappe.throw(_("Công trình {0} chưa có khách hàng — không thể tạo hóa đơn").format(project_costing))
    if flt(amount) <= 0:
        frappe.throw(_("Số tiền hóa đơn phải lớn hơn 0"))

    item_code = _get_or_create_placeholder_item(pc.company)
    desc = description or f"{pc.project_name} — Hóa đơn dự án"

    si = frappe.new_doc("Sales Invoice")
    si.customer = pc.customer
    si.company = pc.company
    si.project = pc.project
    si.append("items", {
        "item_code": item_code,
        "qty": 1,
        "rate": flt(amount),
        "description": desc,
        "project": pc.project,
    })
    si.flags.ignore_permissions = True
    si.insert()

    return {
        "sales_invoice": si.name,
        "url": f"/app/sales-invoice/{si.name}",
    }


@frappe.whitelist()
def get_stage_invoices(stage_name: str) -> list:
    """List all Sales Invoices linked to a stage (draft + submitted)."""
    return frappe.db.sql(
        """SELECT name, base_grand_total AS amount, docstatus, status, posting_date
           FROM `tabSales Invoice`
           WHERE project_costing_stage = %s AND docstatus < 2
           ORDER BY posting_date DESC, name DESC""",
        (stage_name,),
        as_dict=True,
    )


def _get_or_create_placeholder_item(company: str) -> str:
    """Return (or create) item code for stage SIs — generic 'Dịch vụ thi công'.

    Phase 1: shared item across all stages. Phase 2 could split by service type.
    """
    item_code = "DV-CONG-TRINH"
    if frappe.db.exists("Item", item_code):
        return item_code
    item = frappe.new_doc("Item")
    item.item_code = item_code
    item.item_name = "Dịch vụ thi công công trình"
    item.item_group = frappe.db.get_value("Item Group", {"is_group": 0}, "name") or "Services"
    item.is_stock_item = 0
    item.include_item_in_manufacturing = 0
    item.is_service_item = 1
    item.stock_uom = "Nos"
    item.flags.ignore_permissions = True
    item.insert()
    return item.name
