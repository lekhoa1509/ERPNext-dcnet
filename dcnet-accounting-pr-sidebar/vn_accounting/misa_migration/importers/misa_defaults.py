"""Misa Default Account importer — Danh_sach_tai_khoan_ngam_dinh.xlsx.

Each Misa row is `(Loại, TK Nợ, TK Có)` — e.g.
  ("Phiếu thu tiền khách hàng",   "1111", "131")
  ("Mua hàng trong nước - Ủy nhiệm chi", "", "11215")
  ("Phiếu chi trả lương nhân viên", "3341", "1111")
  ("Hạch toán thuế TNDN phải nộp", "8211", "3334")

Each TK in either Dr or Cr position is a candidate for one of:
  - ERPNext `Company.default_*` field (cash/bank/receivable/payable/income/expense/payroll/...)
  - vn_accounting `VN Accounting Settings` field (CIT/loan/interest/retained-earnings/911/WIP/...)

We do NOT trust a single row — Misa exports 165 rows with many phrasings
of the same operation, and a given TK shows up across many. We
**aggregate by frequency** and pick the most-common TK per target field
across the WHOLE batch (after parsing all rows). Each Misa Migration Row
records the candidate it contributed; the actual Company/Settings write
is a per-batch finalize step run after the per-row loop completes.

Pipeline shape:
  * `preview_row()`: classify the row (Loại + TKs → target candidates).
    Marks Ready when at least one TK maps to a known field; Skipped
    when both TKs are blank or neither maps; Invalid on data errors.
  * `post_row()`: write the row's candidate(s) to a transient per-batch
    `_candidates` collector. Always returns "Posted" (the actual GL
    side-effect is deferred). Mark with target_name = the field(s)
    populated, for audit.
  * `finalize()`: aggregate `_candidates`, pick majority TK per target
    field, resolve to Account.name on company, write to Company doc +
    VN Accounting Settings doc, log results.

The orchestrator calls `finalize()` after post_row loop via a new
`run_post_finalize` hook (added to PHASE_1_2 path).
"""

from __future__ import annotations

import json
import re
from collections import Counter
from typing import Any

import frappe

from vn_accounting.misa_migration.importers.base import BaseImporter


# ----------------------------------------------------------------------
# TK code → (target_doctype, fieldname) mapping
#
# Both ERPNext Company.default_* fields and VN Accounting Settings fields
# are Link → Account. We map by Misa TK exactly (with prefix-strip for
# bank sub-accounts like 11215 → 1121 family).
#
# Priority rule: if multiple TKs feed the same target, the MOST FREQUENT
# in the file wins. This auto-handles the common Misa pattern where a
# company uses TK 11215 (Bank in-transit) for outgoing payments AND TK
# 1121 for bank deposits — frequency picks the right one.
# ----------------------------------------------------------------------

# Company.default_X fields. Each TK can map to AT MOST ONE Company field
# (otherwise we'd overwrite back-and-forth as rows iterate).
TK_TO_COMPANY_FIELD: dict[str, str] = {
    # Cash
    "111": "default_cash_account",
    "1111": "default_cash_account",
    "1112": "default_cash_account",
    "1113": "default_cash_account",
    # Bank
    "112": "default_bank_account",
    "1121": "default_bank_account",
    "1122": "default_bank_account",
    "1123": "default_bank_account",
    "11215": "default_bank_account",   # Misa "Tiền gửi NH đang chuyển"
    # Party
    "131": "default_receivable_account",
    "331": "default_payable_account",
    # Income / Expense
    "511": "default_income_account",
    "5111": "default_income_account",   # Doanh thu bán hàng hóa
    "5112": "default_income_account",   # Doanh thu bán thành phẩm
    "5113": "default_income_account",   # Doanh thu bán dịch vụ
    "632": "default_expense_account",
    "6321": "default_expense_account",
    "642": "default_expense_account",
    "6421": "default_expense_account",
    "6422": "default_expense_account",
    # Payroll / Advance
    "334": "default_payroll_payable_account",
    "3341": "default_payroll_payable_account",
    "141": "default_employee_advance_account",
    # Sales returns / discount
    "521": "default_discount_account",
    "5211": "default_discount_account",
    "5212": "default_discount_account",
    "5213": "default_discount_account",
}

# VN Accounting Settings fields — VN-specific defaults that ERPNext core
# doesn't model. These coexist with Company.default_* (no overlap).
TK_TO_VN_SETTINGS_FIELD: dict[str, str] = {
    # Short-term loans
    "341": "default_loan_account",
    "3411": "default_loan_account",
    "3412": "default_loan_account",
    # Interest income (financial activity)
    "515": "default_interest_income_account",
    # Corporate income tax (expense side 821/8211 — the payable 3334 is
    # NOT in Settings; it's auto-pulled by ERPNext via account_type='Tax')
    "8211": "corporate_income_tax_account",
    "821": "corporate_income_tax_account",
    # Retained earnings — TT99/2025 renamed but codes stable
    "4211": "retained_earnings_prior_year",
    "4212": "retained_earnings_current_year",
    # P&L determination
    "911": "pnl_account_911",
    # Other income
    "711": "other_income_account",
    # Project costing — TT99/2025 mandates 627→154→632 chain for
    # construction/service. The WIP collector is 154.
    "154": "wip_account_project_costing",
    # G&A / overhead expense
    "627": "overhead_collector_account",
}


# ----------------------------------------------------------------------
# Account-nature analyzer (uses Tính chất column from CoA file). Sets
# Account.account_type for known nature → ERPNext account_type mapping.
# Run by AccountImporter as a post-import sweep; included here for
# completeness/documentation. Not directly invoked from this file.
# ----------------------------------------------------------------------
NATURE_TO_ACCOUNT_TYPE: dict[str, str] = {
    # Misa Tính chất → ERPNext Account.account_type
    "tiền mặt": "Cash",
    "tiền gửi ngân hàng": "Bank",
    "phải thu của khách hàng": "Receivable",
    "phải trả cho người bán": "Payable",
    "hàng tồn kho": "Stock",
    "nguyên liệu, vật liệu": "Stock",
    "tài sản cố định": "Fixed Asset",
    "hao mòn tscđ": "Accumulated Depreciation",
    "chi phí khấu hao tscđ": "Depreciation",
}


def _normalize_tk(raw: Any) -> str:
    """Return cleaned-up Misa TK string; '' for blank/None."""
    if raw is None:
        return ""
    s = str(raw).strip()
    return s


def _resolve_account_on_company(tk: str, company: str) -> str | None:
    """TK number → ERPNext Account.name on a given company."""
    if not tk or not company:
        return None
    return frappe.db.get_value(
        "Account",
        {"account_number": tk, "company": company, "is_group": 0},
        "name",
    )


class MisaDefaultAccountImporter(BaseImporter):
    file_type = "Misa Default Account"
    entity_type = "Default Account"
    target_doctype = "Company"   # not really created; we update existing

    column_map = {
        "_loai": "Loại",
        "_tk_no": "TK Nợ",
        "_tk_co": "TK Có",
    }

    def __init__(self, batch_name: str):
        super().__init__(batch_name)
        self._company = frappe.db.get_value(
            "Misa Migration Batch", batch_name, "company"
        )

    def dedupe_key(self, normalized):
        # Loại name is the natural dedupe key; Misa exports occasionally
        # have duplicate Loại rows (e.g. "Bán hàng đại lý bán đúng giá -
        # Chưa thanh toán" appears twice on DCNet export). Keep both —
        # frequency-based aggregation will still produce the right answer.
        loai = (normalized.get("_loai") or "").strip()
        dr = _normalize_tk(normalized.get("_tk_no"))
        cr = _normalize_tk(normalized.get("_tk_co"))
        return f"{loai}|{dr}|{cr}"

    def validate(self, normalized):
        errs = []
        if not (normalized.get("_loai") or "").strip():
            errs.append("Thiếu 'Loại'")
        if not self._company:
            errs.append("Batch không có Company")
        return errs

    def lookup_existing(self, normalized):
        # No DB-level existing record for these — always treat as Ready/Skipped
        return None

    def build_doc(self, normalized):
        # Required by BaseImporter ABC but not used: this importer doesn't
        # create a new document per row — it collects candidates in
        # post_row and writes Company/Settings in finalize(). Returning
        # an empty dict satisfies the abstract method.
        return {}

    def _row_candidates(self, normalized: dict) -> list[tuple[str, str, str]]:
        """Return list of (target_doctype, fieldname, tk) candidates for this row.

        A row contributes ONE candidate per non-blank TK that maps to a
        known field. Up to 2 candidates per row (Dr + Cr).
        """
        out: list[tuple[str, str, str]] = []
        for tk_raw in (normalized.get("_tk_no"), normalized.get("_tk_co")):
            tk = _normalize_tk(tk_raw)
            if not tk:
                continue
            if tk in TK_TO_COMPANY_FIELD:
                out.append(("Company", TK_TO_COMPANY_FIELD[tk], tk))
            if tk in TK_TO_VN_SETTINGS_FIELD:
                out.append(("VN Accounting Settings", TK_TO_VN_SETTINGS_FIELD[tk], tk))
        return out

    def preview_row(self, row_doc):
        raw = self._load_raw(row_doc)
        if raw is None:
            self.counts["invalid"] += 1
            return "Invalid"
        normalized = self.normalize(raw)
        errors = self.validate(normalized)
        if errors:
            self._mark(row_doc, "Invalid", "; ".join(errors), normalized)
            self.counts["invalid"] += 1
            return "Invalid"

        candidates = self._row_candidates(normalized)
        if not candidates:
            # Both TKs blank, or neither maps to a known field
            self._mark(row_doc, "Skipped", "Không có TK nào ánh xạ được", normalized)
            self.counts["skipped"] = self.counts.get("skipped", 0) + 1
            return "Skipped"

        # Encode the candidates into target_name for the operator to see
        # what this row WILL contribute toward (final winner is per-field
        # majority, decided at finalize time).
        target_hint = "; ".join(f"{fld}={tk}" for _, fld, tk in candidates)
        self._mark(row_doc, "Ready", None, normalized, target_name=target_hint[:140])
        self.counts["ready"] += 1
        return "Ready"

    def post_row(self, row_doc):
        """Collect candidates into the importer's transient bin. Always Posted.

        Final write happens in finalize() after the per-row loop ends.
        """
        if row_doc.status not in ("Ready",):
            return row_doc.status
        try:
            normalized = json.loads(row_doc.parsed_payload or "{}")
        except (ValueError, TypeError):
            normalized = {}
        candidates = self._row_candidates(normalized)
        if not candidates:
            self._mark(row_doc, "Skipped", "No mappable TK", normalized)
            return "Skipped"
        bin_ = self.__dict__.setdefault("_candidates", [])
        for dt, fld, tk in candidates:
            bin_.append((dt, fld, tk))
        # Audit trail — write what THIS row contributed
        applied = "; ".join(f"{fld}={tk}" for _, fld, tk in candidates)
        self._mark(row_doc, "Posted", None, normalized, target_name=applied[:140])
        self.counts["posted"] += 1
        return "Posted"

    # ------------------------------------------------------------------
    # Per-batch finalize — aggregate + write Company + VN Settings
    # ------------------------------------------------------------------
    def finalize(self) -> dict:
        """Aggregate collected candidates by (doctype, field), pick
        majority TK per slot, resolve, and write to Company + VN
        Accounting Settings. Returns a summary dict for the operator."""
        bin_ = self.__dict__.get("_candidates") or []
        if not bin_:
            return {"applied": [], "skipped": [], "summary": "Không có ứng viên nào"}
        if not self._company:
            return {"applied": [], "skipped": [{"reason": "Batch không có Company"}]}

        # (dt, fld) → Counter(tk → count)
        per_slot: dict[tuple[str, str], Counter] = {}
        for dt, fld, tk in bin_:
            per_slot.setdefault((dt, fld), Counter())[tk] += 1

        applied, skipped = [], []
        company_updates: dict[str, str] = {}
        settings_updates: dict[str, str] = {}

        for (dt, fld), counter in per_slot.items():
            # Pick most common TK; tie-break by lexicographic ascending
            ranked = counter.most_common()
            top_count = ranked[0][1]
            tied = sorted(tk for tk, c in ranked if c == top_count)
            winner_tk = tied[0]
            acct = _resolve_account_on_company(winner_tk, self._company)
            if not acct:
                skipped.append({
                    "doctype": dt, "field": fld, "tk": winner_tk,
                    "reason": f"TK {winner_tk} không tồn tại trên công ty {self._company}",
                    "vote_count": top_count,
                })
                continue
            applied.append({
                "doctype": dt, "field": fld, "tk": winner_tk,
                "account": acct, "vote_count": top_count,
                "candidates": dict(counter),
            })
            if dt == "Company":
                company_updates[fld] = acct
            elif dt == "VN Accounting Settings":
                settings_updates[fld] = acct

        # Write Company defaults
        if company_updates:
            try:
                for fld, val in company_updates.items():
                    # Use set_value to bypass validate() which can throw on
                    # role-based "Cannot edit Company" guards in some sites.
                    frappe.db.set_value(
                        "Company", self._company, fld, val,
                        update_modified=False,
                    )
                frappe.db.commit()
            except Exception as exc:
                frappe.log_error(
                    title=f"Misa defaults Company write failed: {self._company}",
                    message=str(exc),
                )

        # Write VN Accounting Settings (Single)
        if settings_updates:
            try:
                doc = frappe.get_single("VN Accounting Settings")
                changed = False
                for fld, val in settings_updates.items():
                    if doc.get(fld) != val:
                        doc.set(fld, val)
                        changed = True
                if changed:
                    doc.flags.ignore_permissions = True
                    doc.save()
                    frappe.db.commit()
            except Exception as exc:
                frappe.log_error(
                    title="Misa defaults VN Settings write failed",
                    message=str(exc),
                )

        return {
            "applied": applied,
            "skipped": skipped,
            "company": self._company,
            "company_writes": company_updates,
            "settings_writes": settings_updates,
        }
