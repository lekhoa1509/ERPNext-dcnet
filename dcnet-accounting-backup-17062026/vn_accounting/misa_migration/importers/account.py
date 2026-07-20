"""Account importer — Misa Danh_sach_he_thong_tai_khoan_ → ERPNext Account.

Misa cols: STT / Số tài khoản / Tên tài khoản / Tính chất / Tên tiếng Anh /
           Diễn giải / Trạng thái

Phase 2 of spec §4 — **3-way reconcile**:
  (a) Match:    Misa TK already exists in ERPNext (by account_number)
                AND name/type compatible → Exists. Save mapping.
  (b) New leaf: Misa TK missing from ERPNext → Ready to create. Infer
                parent via dot-split / prefix-shortening. account_type
                from Misa Tính chất + TK prefix.
  (c) Conflict: Misa TK exists in ERPNext but with different name/type →
                Conflict (user resolves).

After post: Misa Account Mapping Single is updated with {misa_code: erpnext_name}.
"""

from __future__ import annotations

import json
from typing import Any

import frappe

from vn_accounting.misa_migration.importers.base import BaseImporter


# (Misa Tính chất prefix, TK prefix) → ERPNext account_type
# Order matters: check most specific first.
_TYPE_RULES = [
    ("Dư Nợ", "33311", "Tax"),
    ("Dư Có", "33311", "Tax"),
    ("Dư Có", "3331", "Tax"),
    ("Dư Nợ", "1331", "Tax"),
    ("Dư Nợ", "111", "Cash"),
    ("Dư Nợ", "112", "Bank"),
    ("Dư Nợ", "131", "Receivable"),
    ("Dư Có", "331", "Payable"),
    ("Dư Nợ", "152", "Stock"),
    ("Dư Nợ", "153", "Stock"),
    ("Dư Nợ", "156", "Stock"),
    ("Dư Có", "214", "Accumulated Depreciation"),
    ("Dư Nợ", "21", "Fixed Asset"),
    ("Dư Nợ", "154", "Cost of Goods Sold"),
    # TT99/2025 additions — needed by AssetCategoryImporter (Depreciation)
    # and Stock-related auto-resolution (155x finished goods, 1563 trading
    # goods sub-account). Without these, those defaults silently fall back
    # to "" and ERPNext defaults to ambiguous.
    ("Dư Nợ", "6424", "Depreciation"),
    ("Dư Nợ", "6274", "Depreciation"),
    ("Dư Nợ", "6414", "Depreciation"),
    ("Dư Nợ", "155", "Stock"),
    ("Dư Nợ", "1551", "Stock"),
    ("Dư Nợ", "1561", "Stock"),
    ("Dư Nợ", "1562", "Stock"),
    ("Dư Nợ", "1563", "Stock"),
    ("Dư Nợ", "157", "Stock"),
    ("Dư Nợ", "158", "Stock"),
]


def _detect_account_type(tinh_chat: str, tk: str) -> str | None:
    """Return ERPNext account_type or None. Check most specific TK prefix first."""
    tc = (tinh_chat or "").strip()
    for tc_match, tk_prefix, atype in _TYPE_RULES:
        if tc.startswith(tc_match) and tk.startswith(tk_prefix):
            return atype
    return None


def _detect_root_type(tk: str) -> str:
    """Misa flat list → ERPNext root_type by TK first digit (VAS convention).

    1* → Asset, 2* → Asset/Liability (depends), 3* → Liability, 4* → Equity,
    5* → Income, 6* → Expense, 7* → Income, 8* → Expense, 9* (911) → Equity.
    """
    if not tk:
        return "Asset"
    first = tk[0]
    if first == "1":
        return "Asset"
    if first == "2":
        # 21* = Fixed Asset, 24*/214* = Asset; 2 only is parent group
        return "Asset"
    if first == "3":
        # 33311, 3331, 333, 34, 35 are liabilities; 4* are equity
        return "Liability"
    if first == "4":
        return "Equity"
    if first == "5":
        return "Income"
    if first == "6":
        return "Expense"
    if first == "7":
        return "Income"
    if first == "8":
        return "Expense"
    if first == "9":
        return "Equity"
    return "Asset"


def _find_parent_account(tk: str, company: str) -> str | None:
    """Try LONGEST-PREFIX-FIRST. For each candidate try is_group=1 then
    promote-leaf-to-group before falling to a shorter (less specific)
    candidate.

    Old strategy (two-pass: Pass 1 group, Pass 2 promote) was wrong for
    cases like 11215 where 1121 is a leaf and 112 is a group: Pass 1 hit
    112 first and returned it, skipping 1121's promotion. Result: bank
    sub-accounts under 112 instead of 1121. BCDTK validation reads
    TK 1121 closing = 0 (empty leaf) instead of bank-sub-account sum.

    New strategy interleaves: for each candidate (longest first):
      1. Try is_group=1 — return immediately.
      2. Else try is_group=0 promotable (no GL, no children) — promote +
         return.
    Only when both fail at this candidate, move to shorter prefix.
    """
    if "." in tk:
        candidates = [tk.split(".")[0]]
    else:
        candidates = []
    for i in range(len(tk) - 1, 0, -1):
        prefix = tk[:i]
        if prefix and prefix not in candidates:
            candidates.append(prefix)

    for c in candidates:
        # Try existing group first at this candidate
        match = frappe.db.get_value(
            "Account",
            {"account_number": c, "company": company, "is_group": 1},
            "name",
        )
        if match:
            return match
        # Else try promote leaf at this candidate
        leaf = frappe.db.get_value(
            "Account",
            {"account_number": c, "company": company, "is_group": 0},
            "name",
        )
        if not leaf:
            continue
        # Safe to promote only if no GL entries and no other children
        if frappe.db.count("GL Entry", {"account": leaf}):
            continue
        if frappe.db.count("Account", {"parent_account": leaf}):
            continue
        try:
            frappe.db.set_value("Account", leaf, "is_group", 1, update_modified=False)
            # Clear cache so subsequent ERPNext validate sees fresh is_group=1.
            # Without this, get_cached_doc serves stale leaf state during the
            # same request → "must be a group" fires when child inserts.
            frappe.clear_document_cache("Account", leaf)
            frappe.db.commit()
            return leaf
        except Exception:
            continue
    return None


def _find_root_account_for_type(root_type: str, company: str) -> str | None:
    """Last-resort parent: the top-level company root for a given root_type
    (Asset/Liability/Equity/Income/Expense). Every COA has these five
    placed at the very top with parent_account=NULL and is_group=1.
    Used when a Misa TK has no parent prefix that exists in this CoA
    (e.g. TK 161 'Chi sự nghiệp' — neither 16 nor 1 exists). Without
    this fallback, ERPNext rejects with 'The root account X must be a
    group' because root accounts MUST be is_group=1."""
    if not root_type or not company:
        return None
    return frappe.db.get_value(
        "Account",
        {
            "company": company,
            "root_type": root_type,
            "is_group": 1,
            "parent_account": ("is", "not set"),
        },
        "name",
    )


def _find_existing_by_number(tk: str, company: str) -> str | None:
    return frappe.db.get_value(
        "Account",
        {"account_number": tk, "company": company},
        "name",
    )


class AccountImporter(BaseImporter):
    file_type = "Account"
    entity_type = "Account"
    target_doctype = "Account"
    column_map = {
        "_tk": "Số tài khoản",
        "_name_vi": "Tên tài khoản",
        "_tinh_chat": "Tính chất",
        "_name_en": "Tên tiếng Anh",
        "_desc": "Diễn giải",
        "_status": "Trạng thái",
    }

    def __init__(self, batch_name: str):
        super().__init__(batch_name)
        self._company = frappe.db.get_value("Misa Migration Batch", batch_name, "company")

    def dedupe_key(self, normalized):
        return None  # use lookup_existing override

    def lookup_existing(self, normalized):
        tk = str(normalized.get("_tk") or "").strip()
        if not tk:
            return None
        return _find_existing_by_number(tk, self._company)

    def validate(self, normalized):
        errs = []
        if not normalized.get("_tk"):
            errs.append("Thiếu 'Số tài khoản'")
        if not normalized.get("_name_vi"):
            errs.append("Thiếu 'Tên tài khoản'")
        if not self._company:
            errs.append("Batch không có Company")
        return errs

    def preview_row(self, row_doc):
        """Override base preview to inject Conflict detection between Exists and Ready.

        (a) tk exists + same name → Exists
        (b) tk exists + different name → Conflict (caller resolves)
        (c) tk missing → Ready
        """
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

        tk = str(normalized["_tk"]).strip()
        existing = _find_existing_by_number(tk, self._company)
        if existing:
            existing_name = frappe.db.get_value("Account", existing, "account_name")
            misa_name = str(normalized["_name_vi"]).strip()
            # Use case-insensitive substring match (Misa names vs ERPNext template names differ in case + suffix)
            if existing_name and (
                misa_name.lower() in existing_name.lower()
                or existing_name.lower() in misa_name.lower()
            ):
                self._mark(row_doc, "Exists", None, normalized, target_name=existing)
                self._save_mapping(tk, existing)
                self.counts["exists"] += 1
                return "Exists"
            # name differs significantly → Conflict
            self._mark(
                row_doc,
                "Conflict",
                f"TK {tk} đã có tên '{existing_name}' khác Misa '{misa_name}'",
                normalized,
                target_name=existing,
            )
            self.counts["conflict"] += 1
            return "Conflict"

        # New leaf
        self._mark(row_doc, "Ready", None, normalized)
        self.counts["ready"] += 1
        return "Ready"

    def build_doc(self, normalized: dict[str, Any]) -> dict[str, Any]:
        tk = str(normalized["_tk"]).strip()
        name_vi = str(normalized["_name_vi"]).strip()
        tinh_chat = str(normalized.get("_tinh_chat") or "").strip()

        parent = _find_parent_account(tk, self._company) if self._company else None
        account_type = _detect_account_type(tinh_chat, tk)
        root_type = _detect_root_type(tk)
        if not parent and self._company:
            parent = _find_root_account_for_type(root_type, self._company)

        payload = {
            "doctype": "Account",
            "account_name": name_vi,
            "account_number": tk,
            "company": self._company,
            "is_group": 0,
            "root_type": root_type,
        }
        if parent:
            payload["parent_account"] = parent
        if account_type:
            payload["account_type"] = account_type
        return payload

    def post_row(self, row_doc):
        # Standard create flow, but also write to Misa Account Mapping after
        new_status = super().post_row(row_doc)
        if new_status == "Posted":
            try:
                normalized = json.loads(row_doc.parsed_payload or "{}")
                self._save_mapping(str(normalized["_tk"]).strip(), row_doc.target_name)
            except Exception:
                pass  # mapping is best-effort; create already succeeded
        return new_status

    # ------------------------------------------------------- mapping helper

    def _save_mapping(self, misa_code: str, erpnext_name: str) -> None:
        """Append/update single Misa Account Mapping entry."""
        if not misa_code or not erpnext_name:
            return
        try:
            mapping_doc = frappe.get_single("Misa Account Mapping")
            try:
                mapping = json.loads(mapping_doc.mappings or "{}")
            except (ValueError, TypeError):
                mapping = {}
            if mapping.get(misa_code) != erpnext_name:
                mapping[misa_code] = erpnext_name
                mapping_doc.mappings = json.dumps(mapping, ensure_ascii=False, indent=2)
                mapping_doc.total_mapped = len(mapping)
                mapping_doc.last_updated = frappe.utils.now_datetime()
                mapping_doc.flags.ignore_permissions = True
                mapping_doc.save()
        except Exception as exc:
            frappe.log_error(title="Misa Account Mapping save failed", message=str(exc))
