"""Phase 0 Opening Balance — single combined JE for all balance carry-over.

Aggregates from Misa OB files:
  - OB Account Balance (general TK balances)
  - OB Customer AR (TK 131 per Customer)
  - OB Supplier AP (TK 331 per Supplier)
  - OB Bank Balance (TK 112 per Bank Account)
  - OB Employee Advance (TK 141 per Employee)
  - OB Prepaid Expense (TK 242)

Output: one Opening JE doc with N accounts[] rows + N GL Entry rows.
Posted-date = batch.ob_posting_date (typically 2024-12-31 for T1/2025).
Equity offset (TK 411 typically) is the balancing row.
"""
from __future__ import annotations

import json
import secrets
from typing import Any

import frappe
from frappe.utils import getdate

from vn_accounting.misa_migration.bulk_pump import account_resolver


def _gen_name() -> str:
    return secrets.token_hex(5)


def build_opening_je(
    batch_name: str,
    company: str,
    ob_date: str,
    posting_user: str = "Administrator",
) -> dict[str, list[dict]] | None:
    """Build a single Opening JE from all OB Misa Migration Rows."""
    now = frappe.utils.now()
    fiscal_year = ob_date[:4] if isinstance(ob_date, str) else str(getdate(ob_date).year)

    # Aggregate legs by (account, party_type, party)
    legs: dict[tuple, dict] = {}  # (account, party_type, party) → {debit, credit}

    def add_leg(account: str, debit: float = 0, credit: float = 0,
                party_type: str | None = None, party: str | None = None) -> None:
        if not account:
            return
        key = (account, party_type, party)
        cur = legs.get(key) or {"debit": 0, "credit": 0}
        cur["debit"] += float(debit or 0)
        cur["credit"] += float(credit or 0)
        legs[key] = cur

    # === Load each OB file_type and aggregate ===
    def load_ob(file_type: str) -> list[dict]:
        rows = frappe.db.sql(
            "SELECT raw_payload FROM `tabMisa Migration Row` "
            "WHERE batch=%s AND file_type=%s AND status NOT IN ('Skipped','Failed','Invalid')",
            (batch_name, file_type), as_dict=True,
        )
        out = []
        for r in rows:
            try:
                out.append(json.loads(r["raw_payload"] or "{}"))
            except (TypeError, ValueError):
                pass
        return out

    # OB Account Balance (general). Misa exports key as 'Số tài khoản'
    # (full word), not 'Số TK' — accept all forms for forward-compat.
    #
    # Two source layouts supported:
    #   - "So_du_tai_khoan" (standard): TK | Dư Nợ | Dư Có
    #   - "Bang_can_doi_tai_khoan" (with PS columns): TK | Đầu kỳ Nợ |
    #     Đầu kỳ Có | PS Nợ | PS Có | Cuối kỳ Nợ | Cuối kỳ Có. Parser
    #     stores main-header column 'Đầu kỳ' = Dr; merged sub-header for
    #     Cr becomes '_col_3' (next index). Same parser quirk affects
    #     'Cuối kỳ' / '_col_7' but we ignore those here (this is OB
    #     opening, not closing).
    #
    # SUMMARY-ROW DEDUPE: Misa Bang_can_doi lists BOTH parent (e.g. 4111)
    # AND leaves (4111, 41111) with the SAME balance — parent is an
    # aggregate display, leaves carry the actual balance. Posting both
    # double-counts. Skip any TK whose value is also represented by a
    # deeper-prefix leaf in the same file.
    ob_acct_rows = load_ob("OB Account Balance")
    ob_tks = {str(p.get("Số tài khoản") or p.get("Số TK") or p.get("Tài khoản") or "").strip()
              for p in ob_acct_rows}
    ob_tks.discard("")

    def _is_summary_of_leaf(tk: str) -> bool:
        """True if any other TK in the same file is a deeper prefix
        (e.g. tk='4111' and '41111' also present → 4111 is summary)."""
        if not tk:
            return False
        for other in ob_tks:
            if other != tk and other.startswith(tk):
                return True
        return False

    seen_acc: set[str] = set()  # first-win per resolved account
    for p in ob_acct_rows:
        tk = str(p.get("Số tài khoản") or p.get("Số TK") or p.get("Tài khoản") or "").strip()
        if _is_summary_of_leaf(tk):
            continue
        acc = account_resolver.resolve(tk, company)
        if not acc or acc in seen_acc:
            continue
        debit = float(
            p.get("Dư Nợ")
            or p.get("Nợ ĐK")
            or p.get("Dư Nợ ĐK")
            or p.get("Dư Nợ đầu kỳ")
            or p.get("Đầu kỳ")  # Bang_can_doi: Đầu kỳ main header = Dr column
            or 0
        )
        credit = float(
            p.get("Dư Có")
            or p.get("Có ĐK")
            or p.get("Dư Có ĐK")
            or p.get("Dư Có đầu kỳ")
            or p.get("_col_3")  # Bang_can_doi: Cr sub-column of Đầu kỳ
            or 0
        )
        if debit or credit:
            add_leg(acc, debit, credit)
            seen_acc.add(acc)

    # ------- Detail files = PARTY BREAKDOWN of the general TB rows -------
    # The general file (Danh_sach_so_du_tai_khoan / Bảng cân đối Đầu kỳ) is
    # the SINGLE SOURCE for GL amounts — it already carries 131/331/141/242/
    # 112.x balances and is self-balancing. Detail files only refine the
    # party dimension. Adding both DOUBLE-COUNTS (E2E round 5: TK 141 posted
    # 135,6 tỷ vs nguồn 71,9 tỷ). Strategy per prefix:
    #   - general has legs + detail rows exist → REPLACE the general legs
    #     with per-party legs; post any residual (general − Σdetail) as a
    #     partyless leg so the TB total stays exact.
    #   - no general legs (reduced set without the TB file) → detail legs
    #     post as-is (legacy behaviour).
    # Track which legs came from the general loop, keyed by TK prefix.
    def _general_keys_for(prefix: str) -> list[tuple]:
        out = []
        for key in legs:
            acc = key[0]
            num = frappe.db.get_value("Account", acc, "account_number") or ""
            if str(num).startswith(prefix):
                out.append(key)
        return out

    def _replace_general_with_detail(prefix: str, detail_legs: list[tuple]) -> None:
        """detail_legs: [(account, debit, credit, party_type, party)]"""
        if not detail_legs:
            return
        gen_keys = _general_keys_for(prefix)
        gen_dr = sum(legs[k]["debit"] for k in gen_keys)
        gen_cr = sum(legs[k]["credit"] for k in gen_keys)
        if gen_keys:
            for k in gen_keys:
                legs.pop(k, None)
        for acc, dr, cr, pt, pty in detail_legs:
            add_leg(acc, dr, cr, party_type=pt, party=pty)
        if gen_keys:
            det_dr = sum(d[1] for d in detail_legs)
            det_cr = sum(d[2] for d in detail_legs)
            res_dr = gen_dr - det_dr
            res_cr = gen_cr - det_cr
            if abs(res_dr) > 1 or abs(res_cr) > 1:
                # Residual keeps the TB total exact (detail file may miss
                # a few parties). Net the two sides into one leg.
                net = res_dr - res_cr
                acc0 = detail_legs[0][0]
                if net >= 0:
                    add_leg(acc0, net, 0)
                else:
                    add_leg(acc0, 0, -net)

    # OB Customer AR (TK 131 by customer). Skip Misa summary rows.
    TOTAL_TOKENS = {"Tổng", "Tổng cộng", "Total", "TỔNG"}
    ar_account = account_resolver.resolve("131", company)
    _ar_detail: list[tuple] = []
    for p in load_ob("OB Customer AR"):
        cust_code = p.get("Mã đối tượng") or p.get("Mã khách hàng")
        if not cust_code or cust_code.strip() in TOTAL_TOKENS:
            continue
        if not frappe.db.exists("Customer", cust_code):
            continue
        debit = float(p.get("Dư Nợ") or p.get("Dư Nợ đầu kỳ") or 0)
        credit = float(p.get("Dư Có") or p.get("Dư Có đầu kỳ") or 0)
        if (debit or credit) and ar_account:
            _ar_detail.append((ar_account, debit, credit, "Customer", cust_code))
    _replace_general_with_detail("131", _ar_detail)

    # OB Supplier AP (TK 331 by supplier). Skip Misa summary rows.
    ap_account = account_resolver.resolve("331", company)
    _ap_detail: list[tuple] = []
    for p in load_ob("OB Supplier AP"):
        sup_code = p.get("Mã đối tượng") or p.get("Mã nhà cung cấp")
        if not sup_code or sup_code.strip() in TOTAL_TOKENS:
            continue
        if not frappe.db.exists("Supplier", sup_code):
            continue
        debit = float(p.get("Dư Nợ") or p.get("Dư Nợ đầu kỳ") or 0)
        credit = float(p.get("Dư Có") or p.get("Dư Có đầu kỳ") or 0)
        if (debit or credit) and ap_account:
            _ap_detail.append((ap_account, debit, credit, "Supplier", sup_code))
    _replace_general_with_detail("331", _ap_detail)

    # OB Employee Advance (TK 141 by employee). Filter out Misa summary rows
    # ('Tổng' = total/aggregate) and rows whose party_code doesn't map to a
    # real Employee — otherwise OB doubles when Misa includes a Total row.
    emp_account = account_resolver.resolve("141", company)
    _emp_detail: list[tuple] = []
    for p in load_ob("OB Employee Advance"):
        emp_code = p.get("Mã nhân viên") or p.get("Mã đối tượng")
        if not emp_code or emp_code.strip() in ("Tổng", "Tổng cộng", "Total"):
            continue
        # Verify Employee exists in master — drops totals/orphans
        if not frappe.db.exists("Employee", emp_code):
            continue
        debit = float(p.get("Dư Nợ") or 0)
        if debit and emp_account:
            _emp_detail.append((emp_account, debit, 0, "Employee", emp_code))
    _replace_general_with_detail("141", _emp_detail)

    # OB Prepaid Expense (TK 242) — amounts only when the general TB didn't
    # already carry 242 (reduced sets); otherwise it would double-count.
    prepaid_account = account_resolver.resolve("242", company)
    if not _general_keys_for("242"):
        for p in load_ob("OB Prepaid Expense"):
            amt = float(p.get("Giá trị còn lại") or p.get("Số tiền") or 0)
            if amt and prepaid_account:
                add_leg(prepaid_account, amt, 0)

    # OB Bank Balance (TK 112 per Bank Account). Misa key is 'Số tài khoản'
    # (the GL TK for this bank), not 'Số TK'. Fall back to any 112* leaf.
    fallback_bank = (account_resolver.resolve("112", company)
                     or account_resolver.resolve("1121", company))
    for p in (load_ob("OB Bank Balance") if not _general_keys_for("112") else []):
        tk = p.get("Số tài khoản") or p.get("Số TK") or "112"
        acc = account_resolver.resolve(tk, company) or fallback_bank
        if not acc:
            continue
        debit = float(p.get("Dư Nợ") or p.get("Số dư đầu kỳ") or 0)
        credit = float(p.get("Dư Có") or 0)
        if debit or credit:
            add_leg(acc, debit, credit)

    if not legs:
        return None

    # Balance check — if not balanced, force-balance into Equity (TK 411
    # or any Equity-root leaf). Resolver may miss bare '411' when CoA only
    # has sub-accounts (4111, 4112, ...). Fall back to any Equity leaf so
    # we never discard the already-aggregated legs.
    total_debit = sum(v["debit"] for v in legs.values())
    total_credit = sum(v["credit"] for v in legs.values())
    diff = round(total_debit - total_credit, 0)
    if abs(diff) > 0.01:
        equity_account = (
            account_resolver.resolve("411", company)
            or account_resolver.resolve("4111", company)
            or account_resolver.resolve("4112", company)
            or frappe.db.get_value(
                "Account",
                {"company": company, "root_type": "Equity", "is_group": 0},
                "name", order_by="name",
            )
        )
        if not equity_account:
            # Still none — surface as an error rather than silently dropping.
            # Caller will see Phase 0 OB JE missing and can investigate.
            frappe.log_error(
                f"bulk_pump OB: no Equity account found for {company}; "
                f"cannot balance diff={diff:,.0f}. Aborting OB JE build.",
                "bulk_pump opening_balance",
            )
            return None
        if diff > 0:
            add_leg(equity_account, 0, diff)
        else:
            add_leg(equity_account, abs(diff), 0)

    # Recompute totals
    total_debit = sum(v["debit"] for v in legs.values())
    total_credit = sum(v["credit"] for v in legs.values())

    voucher_no = f"OB-{batch_name}"
    accounts_rows: list[dict] = []
    gl_rows: list[dict] = []
    for idx, ((acc, ptype, party), amts) in enumerate(legs.items()):
        if amts["debit"] == 0 and amts["credit"] == 0:
            continue
        accounts_rows.append({
            "name": _gen_name(),
            "creation": now, "modified": now, "owner": posting_user, "modified_by": posting_user,
            "docstatus": 1, "idx": idx + 1,
            "account": acc, "account_currency": "VND",
            "party_type": ptype, "party": party,
            "debit_in_account_currency": amts["debit"], "debit": amts["debit"],
            "credit_in_account_currency": amts["credit"], "credit": amts["credit"],
            "user_remark": "Opening Balance",
            "parent": voucher_no, "parenttype": "Journal Entry", "parentfield": "accounts",
        })
        gl_rows.append({
            "name": _gen_name(),
            "creation": now, "modified": now, "owner": posting_user, "modified_by": posting_user,
            "docstatus": 1, "idx": 0,
            "posting_date": ob_date, "transaction_date": ob_date,
            "fiscal_year": fiscal_year,
            "account": acc, "account_currency": "VND",
            "party_type": ptype, "party": party,
            "voucher_type": "Journal Entry", "voucher_no": voucher_no,
            "transaction_currency": "VND",
            "transaction_exchange_rate": 1.0, "reporting_currency_exchange_rate": 1.0,
            "debit": amts["debit"], "debit_in_account_currency": amts["debit"],
            "debit_in_transaction_currency": amts["debit"], "debit_in_reporting_currency": amts["debit"],
            "credit": amts["credit"], "credit_in_account_currency": amts["credit"],
            "credit_in_transaction_currency": amts["credit"], "credit_in_reporting_currency": amts["credit"],
            "company": company, "is_opening": "Yes", "is_advance": "No", "is_cancelled": 0,
            "remarks": "Opening Balance",
        })

    je_row = {
        "name": voucher_no,
        "creation": now, "modified": now, "owner": posting_user, "modified_by": posting_user,
        "docstatus": 1, "idx": 0,
        "company": company,
        "voucher_type": "Opening Entry",
        "posting_date": ob_date,
        "multi_currency": 0,
        "total_debit": total_debit, "total_credit": total_credit, "difference": 0,
        "total_amount_currency": "VND", "total_amount": total_debit,
        "user_remark": "Opening Balance (bulk_pump)",
        "remark": "Opening Balance (bulk_pump)",
        "is_opening": "Yes",
        "misa_voucher_no": voucher_no,
    }

    return {
        "Journal Entry": [je_row],
        "Journal Entry Account": accounts_rows,
        "GL Entry": gl_rows,
    }
