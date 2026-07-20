"""Project P&L Detailed — Bảng lãi/lỗ chi tiết (BL §10.3).

Per project: revenue (511), direct_cost (154 ex-CAR), allocated_cost (CAR JE),
gross_profit (rev - direct), net_profit (rev - total), common_pool (unpinned).

Data source: tabGL Entry filtered by company, date range, accounts from
VN Accounting Settings.
"""
from __future__ import annotations

import frappe
from frappe import _
from frappe.utils import flt


def execute(filters=None):
    filters = filters or {}
    columns = _columns()
    data = _fetch(filters)
    return columns, data


def _columns():
    return [
        {"fieldname": "project", "label": _("Công trình"), "fieldtype": "Link", "options": "Project", "width": 180},
        {"fieldname": "revenue", "label": _("Doanh thu"), "fieldtype": "Currency", "options": "currency", "width": 130},
        {"fieldname": "direct_cost", "label": _("CP trực tiếp"), "fieldtype": "Currency", "options": "currency", "width": 130},
        {"fieldname": "allocated_cost", "label": _("CP phân bổ"), "fieldtype": "Currency", "options": "currency", "width": 130},
        {"fieldname": "total_cost", "label": _("Tổng CP"), "fieldtype": "Currency", "options": "currency", "width": 130},
        {"fieldname": "gross_profit", "label": _("Lãi gộp"), "fieldtype": "Currency", "options": "currency", "width": 130},
        {"fieldname": "net_profit", "label": _("Lãi ròng"), "fieldtype": "Currency", "options": "currency", "width": 130},
        {"fieldname": "common_pool", "label": _("Common pool"), "fieldtype": "Currency", "options": "currency", "width": 130},
    ]


def _fetch(filters):
    company = filters.get("company")
    from_date = filters.get("from_date")
    to_date = filters.get("to_date")
    project_filter = filters.get("project")

    # Resolve TK from Settings
    from vn_accounting.utils.account_resolver import resolve_account

    wip = resolve_account("wip_account_project_costing", company)
    revenue_acc = frappe.db.get_value(
        "Account", {"account_number": "511", "company": company, "is_group": 0}, "name"
    )

    # Get all projects with any costing activity in period
    projects = frappe.db.sql_list("""
        SELECT DISTINCT project FROM `tabGL Entry`
        WHERE company = %(company)s
          AND project IS NOT NULL AND project != ''
          AND posting_date BETWEEN %(from_date)s AND %(to_date)s
          AND is_cancelled = 0
          AND (%(project_filter)s = '' OR project = %(project_filter)s)
    """, {"company": company, "from_date": from_date, "to_date": to_date,
          "project_filter": project_filter or ""})

    out = []
    for proj in projects:
        # Revenue = Cr 511 for project
        revenue = 0.0
        if revenue_acc:
            revenue = flt(frappe.db.sql("""
                SELECT IFNULL(SUM(credit), 0) - IFNULL(SUM(debit), 0)
                FROM `tabGL Entry`
                WHERE company=%s AND account=%s AND project=%s
                  AND posting_date BETWEEN %s AND %s AND is_cancelled = 0
            """, (company, revenue_acc, proj, from_date, to_date))[0][0])

        # Direct cost = Dr 154 ex-Cost Allocation Run
        direct = 0.0
        allocated = 0.0
        if wip:
            direct = flt(frappe.db.sql("""
                SELECT IFNULL(SUM(debit), 0) - IFNULL(SUM(credit), 0)
                FROM `tabGL Entry`
                WHERE company=%s AND account=%s AND project=%s
                  AND posting_date BETWEEN %s AND %s AND is_cancelled = 0
                  AND voucher_type != 'Journal Entry'
            """, (company, wip, proj, from_date, to_date))[0][0])

            # CAR allocations: Dr 154 from Journal Entry with reference_type='Cost Allocation Run'
            allocated = flt(frappe.db.sql("""
                SELECT IFNULL(SUM(jea.debit_in_account_currency), 0)
                FROM `tabJournal Entry Account` jea
                JOIN `tabJournal Entry` je ON je.name = jea.parent
                WHERE je.company=%s AND je.docstatus=1
                  AND jea.account=%s AND jea.project=%s
                  AND je.posting_date BETWEEN %s AND %s
                  AND jea.reference_type = 'Cost Allocation Run'
            """, (company, wip, proj, from_date, to_date))[0][0])
            # Direct = total - allocated
            direct = direct - allocated if direct > allocated else direct

        total_cost = direct + allocated
        gross = revenue - direct
        net = revenue - total_cost

        # Common pool = chi phí tag project nhưng chưa pin stage. Walk các nguồn
        # PI/SE/DN/EC + JE Account + Asset Repair với project tag + stage NULL.
        common_pool = _compute_common_pool(proj, company, from_date, to_date)

        out.append({
            "project": proj,
            "revenue": revenue,
            "direct_cost": direct,
            "allocated_cost": allocated,
            "total_cost": total_cost,
            "gross_profit": gross,
            "net_profit": net,
            "common_pool": common_pool,
            "currency": "VND",
        })

    out.sort(key=lambda x: -x["revenue"])
    return out


def _compute_common_pool(project: str, company: str, from_date: str, to_date: str) -> float:
    """Sum chi phí tag project nhưng project_costing_stage NULL (chưa pin)."""
    total = 0.0
    # PI Item (parent.project header wins, fallback Item.project)
    total += flt(frappe.db.sql("""
        SELECT IFNULL(SUM(pii.base_net_amount), 0)
        FROM `tabPurchase Invoice Item` pii
        JOIN `tabPurchase Invoice` pi ON pi.name = pii.parent
        WHERE pi.docstatus = 1 AND pi.company = %s
          AND COALESCE(NULLIF(pi.project, ''), pii.project) = %s
          AND (pii.project_costing_stage IS NULL OR pii.project_costing_stage = '')
          AND pi.posting_date BETWEEN %s AND %s
    """, (company, project, from_date, to_date))[0][0])
    # Stock Entry (parent + child)
    total += flt(frappe.db.sql("""
        SELECT IFNULL(SUM(
            CASE WHEN se.project IS NOT NULL AND se.project != '' THEN se.total_outgoing_value
                 ELSE COALESCE(sed_amt.amt, 0) END
        ), 0)
        FROM `tabStock Entry` se
        LEFT JOIN (
            SELECT parent, SUM(amount) AS amt FROM `tabStock Entry Detail`
            WHERE project = %s GROUP BY parent
        ) sed_amt ON sed_amt.parent = se.name
        WHERE se.docstatus = 1 AND se.company = %s
          AND se.stock_entry_type = 'Material Issue'
          AND (se.project = %s OR sed_amt.amt > 0)
          AND (se.project_costing_stage IS NULL OR se.project_costing_stage = '')
          AND se.posting_date BETWEEN %s AND %s
    """, (project, company, project, from_date, to_date))[0][0])
    # JE Account
    total += flt(frappe.db.sql("""
        SELECT IFNULL(SUM(jea.debit_in_account_currency), 0)
        FROM `tabJournal Entry Account` jea
        JOIN `tabJournal Entry` je ON je.name = jea.parent
        WHERE je.docstatus = 1 AND je.company = %s
          AND jea.project = %s
          AND jea.debit_in_account_currency > 0
          AND (jea.project_costing_stage IS NULL OR jea.project_costing_stage = '')
          AND COALESCE(jea.reference_type, '') NOT IN ('Project Costing', 'Cost Allocation Run')
          AND je.posting_date BETWEEN %s AND %s
    """, (company, project, from_date, to_date))[0][0])
    return total
