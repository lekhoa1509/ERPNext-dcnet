"""Post-migration health check — analyzes Balance Sheet for sign anomalies,
missing OB lines, and 4 other diagnostic checks. Returns categorized findings
+ suggested actions so operator can route remediation back to source
(re-export from Misa) vs adjust-by-JE post-import.

Read-only — never mutates GL/voucher data. Safe to re-run anytime.
"""

from __future__ import annotations

import json
from typing import Any

import frappe
from frappe import _


@frappe.whitelist()
def run_health_check(batch_name: str) -> dict[str, Any]:
    """Run all anomaly checks on the company's posted GL state after migration.

    Returns:
      {
        "batch": <name>,
        "company": <name>,
        "balance_sheet_balanced": bool,
        "n_anomalies": int,
        "anomalies": [
          {"account": "1551 - Thành phẩm chính - DCT", "root_type": "Asset",
           "net": -49055000, "expected_sign": "Dr",
           "findings": [{"severity": "high"|"medium"|"info", "type": "<id>", "msg": "..."}],
           "actions": [...]},
          ...
        ],
        "bs_summary": {"assets": <num>, "liabilities": <num>, "equity": <num>, "pnl": <num>},
      }
    """
    company = frappe.db.get_value("Misa Migration Batch", batch_name, "company")
    if not company:
        frappe.throw(_("Không tìm thấy batch: {0}").format(batch_name))

    # 1. Sum all leaf account GL Entry → check sign convention
    accounts = frappe.db.sql(
        """SELECT a.name, a.account_name, a.root_type, a.account_type, a.account_number,
                  COALESCE(SUM(gle.debit), 0) AS dr,
                  COALESCE(SUM(gle.credit), 0) AS cr,
                  COUNT(gle.name) AS n_entries
           FROM `tabAccount` a
           LEFT JOIN `tabGL Entry` gle ON gle.account = a.name
                                     AND gle.company = %s
                                     AND gle.is_cancelled = 0
           WHERE a.company = %s AND a.is_group = 0
           GROUP BY a.name
           HAVING dr > 0 OR cr > 0
           ORDER BY a.name""",
        (company, company), as_dict=True,
    )

    anomalies = []
    bs_summary = {"assets": 0, "liabilities": 0, "equity": 0, "pnl": 0}

    for acc in accounts:
        net = float(acc["dr"]) - float(acc["cr"])
        rt = acc["root_type"]
        if rt == "Asset":
            bs_summary["assets"] += net
            expected_sign = "Dr"
            anomaly_sign = net < -1.0
        elif rt == "Liability":
            bs_summary["liabilities"] += -net  # credit-positive convention for display
            expected_sign = "Cr"
            anomaly_sign = net > 1.0
        elif rt == "Equity":
            bs_summary["equity"] += -net
            expected_sign = "Cr"
            anomaly_sign = net > 1.0
        elif rt == "Income":
            bs_summary["pnl"] += -net
            expected_sign = "Cr"
            anomaly_sign = net > 1.0
        elif rt == "Expense":
            bs_summary["pnl"] -= net
            expected_sign = "Dr"
            anomaly_sign = net < -1.0
        else:
            continue

        # Skip 214 Accumulated Depreciation — contra-asset, naturally Cr
        if acc["account_type"] == "Accumulated Depreciation" and net < 0:
            anomaly_sign = False

        if not anomaly_sign:
            continue

        findings = []
        actions = []

        # CHECK 1: Was this account's OB included in Misa OB Account Balance?
        prefix = acc["account_name"].split(" - ")[0]  # "1551"
        ob_present = frappe.db.sql(
            """SELECT 1 FROM `tabMisa Migration Row`
               WHERE file_type='OB Account Balance' AND batch=%s
                 AND raw_payload LIKE %s LIMIT 1""",
            (batch_name, f'%"{prefix}"%'),
        )
        if not ob_present:
            findings.append({
                "severity": "high",
                "type": "missing_ob",
                "msg": _("Misa file 'Danh_sach_so_du_tai_khoan.xlsx' không có dòng OB cho TK {0}").format(prefix),
            })
            actions.append(_("Yêu cầu kế toán export lại file số dư tài khoản (Danh_sach_so_du_tai_khoan.xlsx) đầy đủ TK"))
            actions.append(_("HOẶC nhập bổ sung qua 1 JE 'OB Adjustment' tại ngày OB"))

        # CHECK 2: Voucher_type dominance — find which voucher type drives the imbalance
        vt_summary = frappe.db.sql(
            """SELECT voucher_type, SUM(debit) AS dr, SUM(credit) AS cr, COUNT(*) AS n
               FROM `tabGL Entry`
               WHERE company=%s AND account=%s AND is_cancelled=0
               GROUP BY voucher_type ORDER BY n DESC""",
            (company, acc["name"]), as_dict=True,
        )
        if vt_summary:
            for vt in vt_summary:
                vt_net = float(vt["dr"]) - float(vt["cr"])
                # If a single voucher type drives the wrong-sign imbalance > 50%
                if (rt in ("Asset", "Expense") and vt_net < -0.5 * abs(net)) or \
                   (rt in ("Liability", "Equity", "Income") and vt_net > 0.5 * abs(net)):
                    findings.append({
                        "severity": "medium",
                        "type": "voucher_dominance",
                        "msg": _("{0} đẩy chính: {1} bút toán, Dr={2:,.0f} Cr={3:,.0f}").format(
                            vt["voucher_type"], vt["n"], vt["dr"], vt["cr"]),
                    })

        # CHECK 3: Date pattern — clustered at month-end (closing entries)?
        date_pattern = frappe.db.sql(
            """SELECT DATE_FORMAT(posting_date, '%%Y-%%m') AS m,
                      SUM(debit) AS dr, SUM(credit) AS cr
               FROM `tabGL Entry`
               WHERE company=%s AND account=%s AND is_cancelled=0
               GROUP BY m ORDER BY m""",
            (company, acc["name"]), as_dict=True,
        )
        if date_pattern:
            # Find months with the biggest wrong-sign push
            for d in date_pattern:
                m_net = float(d["dr"]) - float(d["cr"])
                if abs(m_net) > 0.2 * abs(net):
                    if (rt in ("Asset", "Expense") and m_net < 0) or \
                       (rt in ("Liability", "Equity", "Income") and m_net > 0):
                        findings.append({
                            "severity": "info",
                            "type": "month_cluster",
                            "msg": _("Tháng {0}: Dr={1:,.0f} Cr={2:,.0f} (lệch -{3:,.0f})").format(
                                d["m"], d["dr"], d["cr"], abs(m_net)),
                        })

        # CHECK 4: For Stock accounts (152/153/155/156), SE vs JE mismatch
        if acc["account_type"] in ("Stock", "Inventory"):
            se_net = sum(float(v["dr"]) - float(v["cr"])
                        for v in vt_summary if v["voucher_type"] == "Stock Entry")
            je_net = sum(float(v["dr"]) - float(v["cr"])
                        for v in vt_summary if v["voucher_type"] == "Journal Entry")
            if abs(je_net) > 2 * abs(se_net) and abs(je_net) > 1_000_000:
                findings.append({
                    "severity": "medium",
                    "type": "stock_je_without_se",
                    "msg": _("JE ảnh hưởng kho ({0:,.0f}) lớn hơn Stock Entry ({1:,.0f}) — Misa có thể chỉ export GL").format(je_net, se_net),
                })
                actions.append(_("Kiểm tra file Sổ chi tiết vật tư hàng hóa (SCT) trong Misa có khớp với JE không"))

        # CHECK 5: AR/AP party reconciliation (TK 131, 331)
        if prefix in ("131", "331") and acc["account_type"] in ("Receivable", "Payable"):
            # Sum outstanding from related invoices
            target_dt = "Sales Invoice" if prefix == "131" else "Purchase Invoice"
            inv_outstanding = frappe.db.sql(
                """SELECT COALESCE(SUM(outstanding_amount), 0) FROM `tab{0}`
                   WHERE company=%s AND docstatus=1 AND misa_voucher_no IS NOT NULL""".format(target_dt),
                (company,),
            )[0][0] or 0
            inv_outstanding = float(inv_outstanding)
            if abs(inv_outstanding - abs(net)) > 1_000_000:
                findings.append({
                    "severity": "medium",
                    "type": "ar_ap_mismatch",
                    "msg": _("Số dư GL ({0:,.0f}) khác outstanding invoices ({1:,.0f})").format(abs(net), inv_outstanding),
                })

        if findings:
            anomalies.append({
                "account": acc["name"],
                "account_name": acc["account_name"],
                "root_type": rt,
                "net": net,
                "expected_sign": expected_sign,
                "n_entries": acc["n_entries"],
                "findings": findings,
                "actions": list(dict.fromkeys(actions)),  # dedupe preserving order
            })

    # Balance check: assets should = liabilities + equity + (revenue - expense)
    total_lhs = bs_summary["assets"]
    total_rhs = bs_summary["liabilities"] + bs_summary["equity"] + bs_summary["pnl"]
    balanced = abs(total_lhs - total_rhs) < 1.0

    return {
        "batch": batch_name,
        "company": company,
        "balance_sheet_balanced": balanced,
        "imbalance": total_lhs - total_rhs,
        "n_anomalies": len(anomalies),
        "anomalies": anomalies,
        "bs_summary": {k: round(v, 0) for k, v in bs_summary.items()},
    }
