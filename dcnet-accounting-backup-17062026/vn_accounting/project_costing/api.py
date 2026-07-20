"""Project Costing form summary API.

Whitelisted endpoint feeding the "Thông tin chính" tab KPI dashboard on
Project Costing form. Aggregates costs collected, invoiced revenue, WIP
balance on TK 154, gross profit/margin, stage counts, last activity.
"""
from __future__ import annotations

import frappe
from frappe import _
from frappe.utils import flt, getdate

from vn_accounting.project_costing.services.pivot_service import _list_costs_for_project


@frappe.whitelist()
def stage_link_query(doctype, txt, searchfield, start, page_len, filters):
    """Server-side Link query: stages belonging to the row's chosen project.

    Used by Cost Allocation Share `project_costing_stage` dropdown — filters
    candidate stages to those whose `parent_costing.project` matches the
    project picked on the share row.
    """
    project = (filters or {}).get("project")
    if not project:
        return []
    rows = frappe.db.sql(
        """
        SELECT s.name, CONCAT(s.stage_order, ' — ', s.stage_name)
        FROM `tabProject Costing Stage` s
        JOIN `tabProject Costing` pc ON pc.name = s.parent_costing
        WHERE pc.project = %(project)s
          AND (s.name LIKE %(txt)s OR s.stage_name LIKE %(txt)s)
        ORDER BY s.stage_order
        LIMIT %(start)s, %(page_len)s
        """,
        {
            "project": project,
            "txt": f"%{txt or ''}%",
            "start": int(start or 0),
            "page_len": int(page_len or 20),
        },
    )
    return rows


@frappe.whitelist()
def get_project_summary(project_costing: str) -> dict:
    if not project_costing:
        frappe.throw(_("project_costing is required"))

    pc = frappe.db.get_value(
        "Project Costing",
        project_costing,
        ["project", "company", "status", "closed_on"],
        as_dict=True,
    )
    if not pc:
        frappe.throw(_("Project Costing không tồn tại: {0}").format(project_costing))

    project = pc.project

    total_collected = sum(flt(r.get("amount")) for r in _list_costs_for_project(project))

    total_invoiced = flt(
        frappe.db.sql(
            """
            SELECT COALESCE(SUM(base_grand_total), 0)
            FROM `tabSales Invoice`
            WHERE docstatus = 1 AND project = %s AND company = %s
            """,
            (project, pc.company),
        )[0][0]
    )

    wip_account = frappe.db.get_single_value(
        "VN Accounting Settings", "wip_account_project_costing"
    )
    wip_balance = 0.0
    if wip_account:
        wip_balance = flt(
            frappe.db.sql(
                """
                SELECT COALESCE(SUM(debit - credit), 0)
                FROM `tabGL Entry`
                WHERE is_cancelled = 0
                  AND account = %s
                  AND project = %s
                  AND company = %s
                """,
                (wip_account, project, pc.company),
            )[0][0]
        )

    gross_profit = total_invoiced - total_collected
    margin_pct = (gross_profit / total_invoiced * 100.0) if total_invoiced else 0.0

    stage_rows = frappe.db.sql(
        """
        SELECT status, COUNT(*) AS n
        FROM `tabProject Costing Stage`
        WHERE parent_costing = %s
        GROUP BY status
        """,
        (project_costing,),
        as_dict=True,
    )
    stage_counts = {"done": 0, "in_progress": 0, "pending": 0, "total": 0}
    for r in stage_rows:
        stage_counts["total"] += r.n
        s = (r.status or "").strip()
        if s in ("Đã xuất HĐ", "Đã thu tiền"):
            stage_counts["done"] += r.n
        elif s in ("Đang thi công", "Chờ xuất HĐ", "Đã có SI draft"):
            stage_counts["in_progress"] += r.n
        else:
            stage_counts["pending"] += r.n

    last_activity = frappe.db.sql(
        """
        SELECT MAX(d) FROM (
            SELECT MAX(modified) AS d FROM `tabProject Costing Stage` WHERE parent_costing = %(pc)s
            UNION ALL
            SELECT MAX(posting_date) AS d FROM `tabSales Invoice`
                WHERE docstatus = 1 AND project = %(project)s
            UNION ALL
            SELECT MAX(posting_date) AS d FROM `tabPurchase Invoice`
                WHERE docstatus = 1 AND COALESCE(NULLIF(project, ''), '') = %(project)s
        ) t
        """,
        {"pc": project_costing, "project": project},
    )[0][0]

    return {
        "project": project,
        "company": pc.company,
        "status": pc.status,
        "closed_on": pc.closed_on,
        "total_collected": total_collected,
        "total_invoiced": total_invoiced,
        "wip_balance": wip_balance,
        "wip_account": wip_account,
        "gross_profit": gross_profit,
        "margin_pct": margin_pct,
        "stage_counts": stage_counts,
        "last_activity": last_activity,
    }


# ─────────────────────────────────────────────────────────────────────────────
# Per-tab document lists (Sales Invoices / Purchase Invoices / Stock Entries /
# TK 154 journal lines). Each RPC returns the underlying rows + a total amount
# the client can render directly in a table.
# ─────────────────────────────────────────────────────────────────────────────


def _resolve_project(project_costing: str) -> tuple[str, str]:
    pc = frappe.db.get_value(
        "Project Costing", project_costing, ["project", "company"], as_dict=True
    )
    if not pc:
        frappe.throw(_("Project Costing không tồn tại: {0}").format(project_costing))
    return pc.project, pc.company


@frappe.whitelist()
def get_sales_invoices_for_project(project_costing: str) -> dict:
    project, company = _resolve_project(project_costing)
    rows = frappe.db.sql(
        """
        SELECT name, posting_date, customer, customer_name,
               base_grand_total AS grand_total,
               outstanding_amount, status, due_date
        FROM `tabSales Invoice`
        WHERE docstatus = 1 AND project = %s AND company = %s
        ORDER BY posting_date DESC, name DESC
        """,
        (project, company),
        as_dict=True,
    )
    total = sum(flt(r["grand_total"]) for r in rows)
    outstanding = sum(flt(r["outstanding_amount"]) for r in rows)
    return {"rows": rows, "total": total, "outstanding_total": outstanding, "count": len(rows)}


@frappe.whitelist()
def get_purchase_invoices_for_project(project_costing: str) -> dict:
    project, company = _resolve_project(project_costing)
    # Parent project wins; fallback to item-row project (per project_costing rules)
    rows = frappe.db.sql(
        """
        SELECT pi.name, pi.posting_date, pi.supplier, pi.supplier_name,
               pi.base_grand_total AS grand_total,
               pi.outstanding_amount, pi.status, pi.due_date,
               COALESCE(SUM(pii.base_net_amount), 0) AS project_amount
        FROM `tabPurchase Invoice` pi
        LEFT JOIN `tabPurchase Invoice Item` pii ON pii.parent = pi.name
        WHERE pi.docstatus = 1
          AND pi.company = %(company)s
          AND (
            pi.project = %(project)s OR
            (COALESCE(pi.project, '') = '' AND pii.project = %(project)s)
          )
        GROUP BY pi.name
        ORDER BY pi.posting_date DESC, pi.name DESC
        """,
        {"project": project, "company": company},
        as_dict=True,
    )
    project_amount_total = sum(flt(r["project_amount"]) for r in rows)
    outstanding = sum(flt(r["outstanding_amount"]) for r in rows)
    return {
        "rows": rows,
        "project_amount_total": project_amount_total,
        "outstanding_total": outstanding,
        "count": len(rows),
    }


@frappe.whitelist()
def get_stock_entries_for_project(project_costing: str) -> dict:
    project, company = _resolve_project(project_costing)
    rows = frappe.db.sql(
        """
        SELECT se.name, se.posting_date, se.stock_entry_type,
               se.total_outgoing_value AS amount,
               se.from_warehouse, se.to_warehouse,
               se.purpose, se.remarks,
               CASE WHEN se.project = %(project)s
                    THEN 'parent'
                    ELSE 'rows'
               END AS source
        FROM `tabStock Entry` se
        WHERE se.docstatus = 1
          AND se.company = %(company)s
          AND (
            se.project = %(project)s OR
            (COALESCE(se.project, '') = '' AND EXISTS (
                SELECT 1 FROM `tabStock Entry Detail` sed
                WHERE sed.parent = se.name AND sed.project = %(project)s
            ))
          )
        ORDER BY se.posting_date DESC, se.name DESC
        """,
        {"project": project, "company": company},
        as_dict=True,
    )
    total = sum(flt(r["amount"]) for r in rows)
    return {"rows": rows, "total": total, "count": len(rows)}


@frappe.whitelist()
def get_project_pnl(project_costing: str, from_date: str | None = None, to_date: str | None = None) -> dict:
    """P&L breakdown for a single project, native render (replaces iframe report).

    Returns:
      kpi:        {revenue, direct_cost, allocated_cost, total_cost,
                   common_pool, gross_profit, net_profit, gross_margin_pct,
                   net_margin_pct}
      breakdown:  list of labeled lines for the component-level table
      stages:     [{name, stage_order, stage_name, status, revenue, cost_pinned,
                    gross, gross_margin_pct, sales_invoice}]
      period:     {from_date, to_date}
    """
    project, company = _resolve_project(project_costing)

    # Default period = current fiscal year (Fiscal Year that contains today),
    # fallback to all-time if no FY matches.
    if not from_date or not to_date:
        today = frappe.utils.today()
        fy = frappe.db.sql(
            """SELECT year_start_date, year_end_date FROM `tabFiscal Year`
               WHERE %s BETWEEN year_start_date AND year_end_date
                 AND name NOT LIKE '_Test%%'
               ORDER BY year_start_date DESC LIMIT 1""",
            (today,),
            as_dict=True,
        )
        if fy:
            from_date = from_date or str(fy[0].year_start_date)
            to_date = to_date or str(fy[0].year_end_date)
        if not from_date:
            from_date = "1900-01-01"
        if not to_date:
            to_date = today

    from vn_accounting.utils.account_resolver import resolve_account

    wip = resolve_account("wip_account_project_costing", company)
    cogs = resolve_account("cogs_account_project_costing", company)

    # Revenue = Cr - Dr on all Income accounts for this project. Covers
    # 511 (Doanh thu BH), 515 (Doanh thu HĐ tài chính), 711 (Thu nhập khác),
    # bất cứ subaccount nào root_type='Income' KTT cấu hình.
    revenue = flt(frappe.db.sql(
        """SELECT IFNULL(SUM(gl.credit - gl.debit), 0)
           FROM `tabGL Entry` gl
           JOIN `tabAccount` a ON a.name = gl.account
           WHERE gl.company=%s AND gl.project=%s AND gl.is_cancelled=0
             AND gl.posting_date BETWEEN %s AND %s
             AND a.root_type = 'Income'""",
        (company, project, from_date, to_date),
    )[0][0])

    # COGS = Dr - Cr on TK 632 (cogs_account_project_costing). Đây là phần
    # đã recognize qua close_engine/cogs_engine khi SI submit.
    cogs_amount = 0.0
    if cogs:
        cogs_amount = flt(frappe.db.sql(
            """SELECT IFNULL(SUM(debit - credit), 0)
               FROM `tabGL Entry`
               WHERE company=%s AND account=%s AND project=%s
                 AND is_cancelled=0
                 AND posting_date BETWEEN %s AND %s""",
            (company, cogs, project, from_date, to_date),
        )[0][0])

    # Other expenses = Dr - Cr on Expense accounts EXCLUDING COGS account.
    # Bao gồm 627/641/642/6427/... khi PI/EC hạch toán trực tiếp vào expense.
    other_expenses = flt(frappe.db.sql(
        """SELECT IFNULL(SUM(gl.debit - gl.credit), 0)
           FROM `tabGL Entry` gl
           JOIN `tabAccount` a ON a.name = gl.account
           WHERE gl.company=%s AND gl.project=%s AND gl.is_cancelled=0
             AND gl.posting_date BETWEEN %s AND %s
             AND a.root_type = 'Expense'
             AND gl.account != COALESCE(%s, '__none__')""",
        (company, project, from_date, to_date, cogs),
    )[0][0])

    # WIP balance — informational, chi phí treo trên 154 chưa recognize qua COGS
    wip_balance = 0.0
    if wip:
        wip_balance = flt(frappe.db.sql(
            """SELECT IFNULL(SUM(debit - credit), 0)
               FROM `tabGL Entry`
               WHERE company=%s AND account=%s AND project=%s
                 AND is_cancelled=0
                 AND posting_date BETWEEN %s AND %s""",
            (company, wip, project, from_date, to_date),
        )[0][0])

    # CAR allocated portion of WIP — hiện cho KTT biết có bao nhiêu là gián tiếp
    allocated_cost = 0.0
    if wip:
        allocated_cost = flt(frappe.db.sql(
            """SELECT IFNULL(SUM(jea.debit_in_account_currency), 0)
               FROM `tabJournal Entry Account` jea
               JOIN `tabJournal Entry` je ON je.name = jea.parent
               WHERE je.company=%s AND je.docstatus=1
                 AND jea.account=%s AND jea.project=%s
                 AND je.posting_date BETWEEN %s AND %s
                 AND jea.reference_type = 'Cost Allocation Run'""",
            (company, wip, project, from_date, to_date),
        )[0][0])

    direct_cost = cogs_amount + other_expenses
    total_cost = direct_cost
    gross_profit = revenue - cogs_amount
    net_profit = revenue - direct_cost
    gross_margin_pct = (gross_profit / revenue * 100.0) if revenue else 0.0
    net_margin_pct = (net_profit / revenue * 100.0) if revenue else 0.0

    # Common pool = unpinned costs (still in 154 awaiting stage assignment)
    common_pool = sum(
        flt(c["amount"]) for c in _list_costs_for_project(project) if not c.get("stage")
    )

    # Per-stage P&L: revenue = SI grand_total if stage.sales_invoice set,
    # cost = stage.cost_pinned (sum of pinned source rows)
    stages = frappe.db.sql(
        """SELECT name, stage_order, stage_name, status, cost_pinned, sales_invoice
           FROM `tabProject Costing Stage`
           WHERE parent_costing = %s
           ORDER BY stage_order""",
        (project_costing,),
        as_dict=True,
    )
    si_totals = {}
    si_names = [s.sales_invoice for s in stages if s.sales_invoice]
    if si_names:
        placeholders = ",".join(["%s"] * len(si_names))
        si_rows = frappe.db.sql(
            f"""SELECT name, base_grand_total FROM `tabSales Invoice`
                WHERE name IN ({placeholders}) AND docstatus = 1""",
            si_names,
        )
        si_totals = {r[0]: flt(r[1]) for r in si_rows}

    stages_out = []
    for s in stages:
        rev = si_totals.get(s.sales_invoice, 0.0)
        cost = flt(s.cost_pinned)
        gross = rev - cost
        margin = (gross / rev * 100.0) if rev else 0.0
        stages_out.append({
            "name": s.name,
            "stage_order": s.stage_order,
            "stage_name": s.stage_name,
            "status": s.status,
            "revenue": rev,
            "cost_pinned": cost,
            "gross": gross,
            "gross_margin_pct": margin,
            "sales_invoice": s.sales_invoice,
        })

    return {
        "period": {"from_date": from_date, "to_date": to_date},
        "kpi": {
            "revenue": revenue,
            "cogs": cogs_amount,
            "other_expenses": other_expenses,
            "direct_cost": direct_cost,
            "allocated_cost": allocated_cost,
            "wip_balance": wip_balance,
            "total_cost": total_cost,
            "common_pool": common_pool,
            "gross_profit": gross_profit,
            "net_profit": net_profit,
            "gross_margin_pct": gross_margin_pct,
            "net_margin_pct": net_margin_pct,
        },
        "accounts": {"wip": wip, "cogs": cogs},
        "stages": stages_out,
    }


@frappe.whitelist()
def get_tk154_entries_for_project(project_costing: str) -> dict:
    """List all JE Account rows posting to TK 154 (WIP) for this project.

    Covers: Cost Allocation Run output (Dr 154/Cr 627), WIP override JEs,
    COGS recognition (Cr 154/Dr 632), close write-off (Cr 154), manual JE
    adjustments. Stage tag visible if set.
    """
    project, company = _resolve_project(project_costing)
    from vn_accounting.utils.account_resolver import resolve_account

    wip_account = resolve_account("wip_account_project_costing", company)
    if not wip_account:
        return {"rows": [], "total_debit": 0, "total_credit": 0, "balance": 0, "count": 0,
                "wip_account": None}

    rows = frappe.db.sql(
        """
        SELECT je.name AS voucher_no, je.posting_date,
               jea.debit_in_account_currency AS debit,
               jea.credit_in_account_currency AS credit,
               jea.reference_type, jea.reference_name,
               jea.project_costing_stage AS stage,
               COALESCE(jea.user_remark, je.user_remark, '') AS remarks,
               jea.name AS jea_name
        FROM `tabJournal Entry Account` jea
        JOIN `tabJournal Entry` je ON je.name = jea.parent
        WHERE je.docstatus = 1
          AND je.company = %s
          AND jea.account = %s
          AND jea.project = %s
        ORDER BY je.posting_date DESC, je.name DESC
        """,
        (company, wip_account, project),
        as_dict=True,
    )
    # Enrich: mark rows whose stage has been invoiced (COGS recognized)
    stage_names = {r["stage"] for r in rows if r.get("stage")}
    locked_stages = set()
    if stage_names:
        locked = frappe.db.sql(
            """SELECT name FROM `tabProject Costing Stage`
               WHERE name IN %s AND cogs_je IS NOT NULL AND cogs_je != ''""",
            (list(stage_names),),
            as_dict=True,
        )
        locked_stages = {r["name"] for r in locked}

    for r in rows:
        r["stage_locked"] = r.get("stage") in locked_stages if r.get("stage") else False

    total_debit = sum(flt(r["debit"]) for r in rows)
    total_credit = sum(flt(r["credit"]) for r in rows)
    return {
        "rows": rows,
        "total_debit": total_debit,
        "total_credit": total_credit,
        "balance": total_debit - total_credit,
        "count": len(rows),
        "wip_account": wip_account,
        "locked_stages": list(locked_stages),
    }
