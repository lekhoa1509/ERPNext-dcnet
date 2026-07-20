"""Project Cost Collection — Bảng tập hợp chi phí công trình.

UNION 5 cost sources (PI/SE/DN/EC/Timesheet) tagged to project, joined với
Project Costing Stage để derive stage_name/status. Filterable by company,
project, stage, cost_type, date range.
"""
from __future__ import annotations

import frappe
from frappe import _
from frappe.utils import flt


def execute(filters=None):
    filters = filters or {}
    columns = _columns()
    data = _fetch(filters)
    # Manual total — only sum amount column
    if data:
        total = sum(flt(r.get("amount")) for r in data)
        data.append({
            "project": "",
            "stage_name": "",
            "cost_type": "",
            "source_doctype": "",
            "source_name": "",
            "posting_date": None,
            "description": _("TỔNG"),
            "amount": total,
        })
    return columns, data


def _columns():
    return [
        {"fieldname": "project", "label": _("Công trình"), "fieldtype": "Link", "options": "Project", "width": 150},
        {"fieldname": "stage_name", "label": _("Giai đoạn"), "fieldtype": "Data", "width": 140},
        {"fieldname": "cost_type", "label": _("Loại CP"), "fieldtype": "Data", "width": 90},
        {"fieldname": "source_doctype", "label": _("Loại chứng từ"), "fieldtype": "Data", "width": 120},
        {"fieldname": "source_name", "label": _("Chứng từ"), "fieldtype": "Dynamic Link", "options": "source_doctype", "width": 140},
        {"fieldname": "posting_date", "label": _("Ngày"), "fieldtype": "Date", "width": 100},
        {"fieldname": "description", "label": _("Diễn giải"), "fieldtype": "Data", "width": 240},
        {"fieldname": "amount", "label": _("Số tiền"), "fieldtype": "Currency", "options": "currency", "width": 130},
    ]


def _fetch(filters):
    company = filters.get("company")
    project = filters.get("project")
    stage = filters.get("stage")
    cost_type = filters.get("cost_type")
    from_date = filters.get("from_date")
    to_date = filters.get("to_date")

    out: list[dict] = []

    # PI Items — effective project = item.project OR parent.project (Accounting
    # Dimension header-level fallback for service POs without item-row project).
    pi_rows = frappe.db.sql("""
        SELECT pi.name AS source_name, pi.posting_date,
               COALESCE(NULLIF(pi.project, ''), pii.project) AS project,
               pii.project_costing_stage AS stage_id,
               pii.base_net_amount AS amount,
               COALESCE(pii.item_name, pii.item_code, '') AS description,
               COALESCE(pi.cost_type, 'Trực tiếp') AS cost_type
        FROM `tabPurchase Invoice Item` pii
        JOIN `tabPurchase Invoice` pi ON pi.name = pii.parent
        WHERE pi.docstatus = 1
          AND pi.company = %(company)s
          AND COALESCE(NULLIF(pi.project, ''), pii.project) IS NOT NULL
          AND COALESCE(NULLIF(pi.project, ''), pii.project) != ''
          AND (%(project)s = '' OR COALESCE(NULLIF(pi.project, ''), pii.project) = %(project)s)
          AND pi.posting_date BETWEEN %(from_date)s AND %(to_date)s
    """, {"company": company, "project": project or "", "from_date": from_date, "to_date": to_date}, as_dict=True)
    for r in pi_rows:
        out.append({**r, "source_doctype": "Purchase Invoice"})

    # Stock Entry — parent.project header wins, fallback child Stock Entry Detail
    se_rows = frappe.db.sql("""
        SELECT se.name AS source_name, se.posting_date,
               COALESCE(NULLIF(se.project, ''), MAX(sed.project)) AS project,
               se.project_costing_stage AS stage_id,
               CASE WHEN se.project IS NOT NULL AND se.project != ''
                    THEN se.total_outgoing_value
                    ELSE SUM(CASE WHEN sed.project = COALESCE(NULLIF(se.project, ''), sed.project)
                                  THEN sed.amount ELSE 0 END)
               END AS amount,
               CONCAT('Xuất kho ', se.stock_entry_type) AS description,
               COALESCE(se.cost_type, 'Trực tiếp') AS cost_type
        FROM `tabStock Entry` se
        LEFT JOIN `tabStock Entry Detail` sed ON sed.parent = se.name
        WHERE se.docstatus = 1
          AND se.company = %(company)s
          AND se.stock_entry_type = 'Material Issue'
          AND (
            (se.project IS NOT NULL AND se.project != ''
             AND (%(project)s = '' OR se.project = %(project)s))
            OR
            ((se.project IS NULL OR se.project = '')
             AND sed.project IS NOT NULL AND sed.project != ''
             AND (%(project)s = '' OR sed.project = %(project)s))
          )
          AND se.posting_date BETWEEN %(from_date)s AND %(to_date)s
        GROUP BY se.name
    """, {"company": company, "project": project or "", "from_date": from_date, "to_date": to_date}, as_dict=True)
    for r in se_rows:
        out.append({**r, "source_doctype": "Stock Entry"})

    # DN Items — same parent-fallback as PI
    dn_rows = frappe.db.sql("""
        SELECT dn.name AS source_name, dn.posting_date,
               COALESCE(NULLIF(dn.project, ''), dni.project) AS project,
               dni.project_costing_stage AS stage_id,
               dni.base_net_amount AS amount,
               COALESCE(dni.item_name, dni.item_code, '') AS description,
               COALESCE(dn.cost_type, 'Trực tiếp') AS cost_type
        FROM `tabDelivery Note Item` dni
        JOIN `tabDelivery Note` dn ON dn.name = dni.parent
        WHERE dn.docstatus = 1
          AND dn.company = %(company)s
          AND COALESCE(NULLIF(dn.project, ''), dni.project) IS NOT NULL
          AND COALESCE(NULLIF(dn.project, ''), dni.project) != ''
          AND (%(project)s = '' OR COALESCE(NULLIF(dn.project, ''), dni.project) = %(project)s)
          AND dn.posting_date BETWEEN %(from_date)s AND %(to_date)s
    """, {"company": company, "project": project or "", "from_date": from_date, "to_date": to_date}, as_dict=True)
    for r in dn_rows:
        out.append({**r, "source_doctype": "Delivery Note"})

    # Expense Claim — parent.project header wins, fallback child Expense Claim Detail
    ec_rows = frappe.db.sql("""
        SELECT ec.name AS source_name, ec.posting_date,
               COALESCE(NULLIF(ec.project, ''), MAX(ecd.project)) AS project,
               ec.project_costing_stage AS stage_id,
               CASE WHEN ec.project IS NOT NULL AND ec.project != ''
                    THEN ec.total_claimed_amount
                    ELSE SUM(CASE WHEN ecd.project = COALESCE(NULLIF(ec.project, ''), ecd.project)
                                  THEN ecd.amount ELSE 0 END)
               END AS amount,
               CONCAT('Hoàn ứng ', COALESCE(ec.employee_name, ec.employee, '')) AS description,
               COALESCE(ec.cost_type, 'Trực tiếp') AS cost_type
        FROM `tabExpense Claim` ec
        LEFT JOIN `tabExpense Claim Detail` ecd ON ecd.parent = ec.name
        WHERE ec.docstatus = 1
          AND ec.company = %(company)s
          AND (
            (ec.project IS NOT NULL AND ec.project != ''
             AND (%(project)s = '' OR ec.project = %(project)s))
            OR
            ((ec.project IS NULL OR ec.project = '')
             AND ecd.project IS NOT NULL AND ecd.project != ''
             AND (%(project)s = '' OR ecd.project = %(project)s))
          )
          AND ec.posting_date BETWEEN %(from_date)s AND %(to_date)s
        GROUP BY ec.name
    """, {"company": company, "project": project or "", "from_date": from_date, "to_date": to_date}, as_dict=True)
    for r in ec_rows:
        out.append({**r, "source_doctype": "Expense Claim"})

    # Journal Entry Account (row-level direct posting)
    # Loại trừ JE engine tự sinh (reference_type project costing) tránh đếm trùng
    je_rows = frappe.db.sql("""
        SELECT je.name AS source_name, je.posting_date,
               jea.project AS project, jea.project_costing_stage AS stage_id,
               jea.debit_in_account_currency AS amount,
               CONCAT('JE thủ công — ', SUBSTRING_INDEX(jea.account, ' - ', 1)) AS description,
               'Trực tiếp' AS cost_type
        FROM `tabJournal Entry Account` jea
        JOIN `tabJournal Entry` je ON je.name = jea.parent
        WHERE je.docstatus = 1
          AND je.company = %(company)s
          AND jea.project IS NOT NULL AND jea.project != ''
          AND (%(project)s = '' OR jea.project = %(project)s)
          AND jea.debit_in_account_currency > 0
          AND COALESCE(jea.reference_type, '') NOT IN ('Project Costing', 'Cost Allocation Run')
          AND je.posting_date BETWEEN %(from_date)s AND %(to_date)s
    """, {"company": company, "project": project or "", "from_date": from_date, "to_date": to_date}, as_dict=True)
    for r in je_rows:
        out.append({**r, "source_doctype": "Journal Entry"})

    # Asset Repair — sửa thiết bị thi công gán project
    ar_rows = frappe.db.sql("""
        SELECT name AS source_name, completion_date AS posting_date,
               project AS project, project_costing_stage AS stage_id,
               total_repair_cost AS amount,
               CONCAT('Sửa chữa ', COALESCE(asset_name, name)) AS description,
               'Trực tiếp' AS cost_type
        FROM `tabAsset Repair`
        WHERE docstatus = 1
          AND company = %(company)s
          AND repair_status = 'Completed'
          AND project IS NOT NULL AND project != ''
          AND (%(project)s = '' OR project = %(project)s)
          AND completion_date BETWEEN %(from_date)s AND %(to_date)s
    """, {"company": company, "project": project or "", "from_date": from_date, "to_date": to_date}, as_dict=True)
    for r in ar_rows:
        out.append({**r, "source_doctype": "Asset Repair"})

    # NOTE: Timesheet đã được LOẠI khỏi nguồn chi phí. Timesheet là labor
    # TRACKING (đo giờ), KHÔNG phát sinh GL Entry. Lương kỹ sư on-site hạch
    # toán qua Salary Slip — Phase 2 sẽ cover.

    # Enrich stage_name from stage_id
    stage_ids = list({r["stage_id"] for r in out if r.get("stage_id")})
    stage_names = {}
    if stage_ids:
        for n, sn in frappe.db.sql("""
            SELECT name, stage_name FROM `tabProject Costing Stage` WHERE name IN %(ids)s
        """, {"ids": tuple(stage_ids)}):
            stage_names[n] = sn

    for r in out:
        r["stage_name"] = stage_names.get(r.get("stage_id")) or _("(Common Pool)")
        r["currency"] = "VND"  # could lookup from Company default
        del r["stage_id"]

    # Filter by stage / cost_type post-fetch (small dataset, OK)
    if stage:
        out = [r for r in out if frappe.db.get_value("Project Costing Stage", {"stage_name": r["stage_name"], "parent_costing": r["project"]}, "name") == stage]
    if cost_type:
        out = [r for r in out if r.get("cost_type") == cost_type]

    out.sort(key=lambda x: (x.get("posting_date") or "", x.get("source_name") or ""))
    return out
