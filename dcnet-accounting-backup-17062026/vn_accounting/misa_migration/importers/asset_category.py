"""Asset Category importer — Misa Danh_sach_loai_tai_san_co_dinh → ERPNext Asset Category.

Misa cols: STT / Mã loại TSCĐ / Tên loại TSCĐ / TK nguyên giá / TK khấu hao /
           Trạng thái

ERPNext Asset Category REQUIRES the `accounts` child table populated
for each Company that uses fixed assets — minimum fields:
  * company_name
  * fixed_asset_account (account_type='Fixed Asset')
  * accumulated_depreciation_account (account_type='Accumulated Depreciation')
  * depreciation_expense_account (account_type='Depreciation')

Without this child table, insert fails with `MandatoryError: accounts`.
The Misa file gives us TK nguyên giá (→ fixed_asset_account) + TK khấu
hao (→ accumulated_depreciation_account). The depreciation expense
account comes from a Company default (TK 6424 in VN COA — chi phí
khấu hao TSCĐ on G&A side, with fallbacks to 6274 production or 6414
sales overhead if 6424 isn't present).
"""

from __future__ import annotations

import frappe

from vn_accounting.misa_migration.importers.base import BaseImporter


class AssetCategoryImporter(BaseImporter):
    file_type = "Asset Category"
    entity_type = "Asset Category"
    target_doctype = "Asset Category"
    column_map = {
        "_code": "Mã loại TSCĐ",
        "_long_name": "Tên loại TSCĐ",
        "_tk_nguyen_gia": "TK nguyên giá",
        "_tk_khau_hao": "TK khấu hao",
        "_status": "Trạng thái",
    }

    def __init__(self, batch_name: str):
        super().__init__(batch_name)
        self._company = frappe.db.get_value(
            "Misa Migration Batch", batch_name, "company"
        )
        self._depreciation_expense_cache: str | None = None

    def dedupe_key(self, normalized):
        return normalized.get("_code") or normalized.get("_long_name")

    def validate(self, normalized):
        errs = []
        if not normalized.get("_code") and not normalized.get("_long_name"):
            errs.append("Thiếu cả Mã và Tên loại TSCĐ")
        if not self._company:
            errs.append("Batch không có Company")
        return errs

    def _resolve_account_by_tk(self, misa_tk: str | None) -> str | None:
        """Misa TK number → ERPNext leaf Account.name on target company.

        Walks shorter prefixes if the exact TK isn't on this CoA — Misa
        SDK exports sub-codes like 21132/2143 that may not exist as
        leaves on a customer's chart but the parent (2113/214) does.
        Pick the nearest is_group=0 ancestor.
        """
        if not misa_tk or not self._company:
            return None
        tk = str(misa_tk).strip()
        if not tk:
            return None
        # Try the exact TK + progressively shorter prefixes
        candidates = [tk]
        if "." in tk:
            candidates.append(tk.split(".")[0])
        for i in range(len(tk) - 1, 0, -1):
            prefix = tk[:i]
            if prefix and prefix not in candidates:
                candidates.append(prefix)
        for c in candidates:
            name = frappe.db.get_value(
                "Account",
                {"account_number": c, "company": self._company, "is_group": 0},
                "name",
            )
            if name:
                return name
            name = frappe.db.get_value(
                "Account",
                {"name": ("like", f"{c} - %"), "company": self._company,
                 "is_group": 0},
                "name",
            )
            if name:
                return name
        return None

    def _depreciation_expense_account(self) -> str | None:
        """Find a Company-side depreciation expense account.

        VN COA convention: TK 6424 'Chi phí khấu hao TSCĐ' (G&A side)
        is the most common default. Fall back to ANY account with
        account_type='Depreciation' on the target company. Cached per
        importer instance.
        """
        if self._depreciation_expense_cache is not None:
            return self._depreciation_expense_cache or None
        for candidate_tk in ("6424", "6274", "6414"):
            n = self._resolve_account_by_tk(candidate_tk)
            if n:
                self._depreciation_expense_cache = n
                return n
        # Last-resort: any account_type='Depreciation' on this company
        n = frappe.db.get_value(
            "Account",
            {"company": self._company, "account_type": "Depreciation",
             "is_group": 0},
            "name",
        )
        self._depreciation_expense_cache = n or ""
        return n

    def build_doc(self, normalized):
        name = (normalized.get("_code") or normalized["_long_name"])[:140]
        payload: dict = {
            "doctype": "Asset Category",
            "asset_category_name": name,
        }
        if not self._company:
            return payload

        fixed_asset = self._resolve_account_by_tk(normalized.get("_tk_nguyen_gia"))
        accum_dep = self._resolve_account_by_tk(normalized.get("_tk_khau_hao"))
        dep_expense = self._depreciation_expense_account()

        # Fallback chain for missing TKs (Misa exports many
        # category-group rows that have no TK at all — e.g. row code=10
        # "Tài sản cố định hữu hình" group). Use Company defaults +
        # well-known VN COA codes (211 root for fixed asset, 214 for
        # accumulated dep). Without this fallback ERPNext rejects the
        # insert with MandatoryError: accounts.
        # Company has `accumulated_depreciation_account` + `depreciation_expense_account`
        # + `capital_work_in_progress_account` + `disposal_account` — but
        # NOT a default_fixed_asset_account (ERPNext lets per-Asset-Category
        # set it). Walk VN COA prefixes 211x to find the nearest fixed-
        # asset leaf when Misa export has no specific TK nguyên giá.
        if not fixed_asset:
            for tk_guess in ("2113", "2112", "2111", "211"):
                fixed_asset = self._resolve_account_by_tk(tk_guess)
                if fixed_asset:
                    break
        if not accum_dep:
            accum_dep = (
                frappe.db.get_value("Company", self._company,
                                    "accumulated_depreciation_account") or
                self._resolve_account_by_tk("2141") or
                self._resolve_account_by_tk("214")
            )
        if not dep_expense:
            # Company has its own depreciation_expense_account too
            dep_expense = frappe.db.get_value(
                "Company", self._company, "depreciation_expense_account"
            )

        # ERPNext REQUIRES all 3 accounts on the child row, or it
        # rejects insert with MandatoryError. If we still can't resolve
        # any of them, build the doc WITHOUT the accounts row — it will
        # fail in build_doc's caller cleanly with a clear error rather
        # than crash deeper in the controller.
        if fixed_asset and accum_dep and dep_expense:
            payload["accounts"] = [{
                "company_name": self._company,
                "fixed_asset_account": fixed_asset,
                "accumulated_depreciation_account": accum_dep,
                "depreciation_expense_account": dep_expense,
            }]
        return payload
