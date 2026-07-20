"""Bank Account importer — Misa Danh_sach_tai_khoan_ngan_hang → ERPNext Bank Account.

Misa cols (7): STT / Số tài khoản / Tên ngân hàng / Tên chi nhánh ngân hàng /
  Chủ tài khoản / Chi nhánh / Trạng thái

Per spec §15.4 doc.name = Misa Số tài khoản. ERPNext Bank Account has no
autoname (uses Document.autoname → falls back to first reqd field
account_name); we force name explicitly via insert(set_name=).

Bank link resolution: Misa 'Tên ngân hàng' is LONG name (e.g. 'NGÂN HÀNG
TMCP ĐÔNG NAM Á - CN TP.HỒ CHÍ MINH'); Phase B BankImporter saved Bank
docs using SHORT name (Tên viết tắt) as bank_name. We attempt:
  1. Exact match on bank_name
  2. Substring match (Misa long name contains the bank's short name)
  3. Fallback: log warning + skip (mark Failed)

Account (GL link) deferred — manual linkage by accountant after import.
"""

from __future__ import annotations

import json
from typing import Any

import frappe

from vn_accounting.misa_migration.importers.base import BaseImporter


class BankAccountImporter(BaseImporter):
    file_type = "Bank Account"
    entity_type = "Bank Account"
    target_doctype = "Bank Account"
    column_map = {
        "_acc_no": "Số tài khoản",
        "_bank_name": "Tên ngân hàng",
        "_branch": "Tên chi nhánh ngân hàng",
        "_owner": "Chủ tài khoản",
        "_company_branch": "Chi nhánh",
        "_status": "Trạng thái",
    }

    def __init__(self, batch_name: str):
        super().__init__(batch_name)
        self._company = frappe.db.get_value("Misa Migration Batch", batch_name, "company")
        # Cache Bank list for fuzzy match
        self._banks = frappe.get_all("Bank", fields=["name", "bank_name"])

    def dedupe_key(self, normalized):
        return normalized.get("_acc_no")

    def validate(self, normalized):
        errs = []
        if not normalized.get("_acc_no"):
            errs.append("Thiếu 'Số tài khoản'")
        if not normalized.get("_bank_name"):
            errs.append("Thiếu 'Tên ngân hàng'")
        if not self._company:
            errs.append("Batch không có Company")
        return errs

    # Misa exports full Vietnamese bank names ("NGÂN HÀNG TMCP VIỆT NAM
    # THỊNH VƯỢNG - CN QUẬN 2") but Bank docs are typically short codes
    # (VPBank). Explicit alias table catches the cases where stripping
    # prefixes alone doesn't bridge naming convention (e.g. "Sacombank"
    # vs "SÀI GÒN THƯƠNG TÍN"). Add new mappings as discovered.
    _BANK_NAME_ALIASES: dict[str, str] = {
        "sai gon thuong tin": "Sacombank",
        "sai gon thuong tin bank": "Sacombank",
        "viet nam thinh vuong": "VPBank",
        "thinh vuong va phat trien": "VPBank",  # VPBank's longer official name
        "vpb": "VPBank",
        "vpbank": "VPBank",
        "cong thuong viet nam": "VietinBank",
        "ngoai thuong viet nam": "Vietcombank",
        "vcb": "Vietcombank",
        "dau tu va phat trien viet nam": "BIDV",
        "ky thuong viet nam": "Techcombank",
        "tcb": "Techcombank",
        "techcombank": "Techcombank",
        "nong nghiep va phat trien nong thon viet nam": "Agribank",
        "agribank": "Agribank",
        "agri": "Agribank",
        "buu dien lien viet": "LPBank",
        "lien viet post": "LPBank",
        "lpb": "LPBank",
        "hang hai viet nam": "MSB",
        "hang hai": "MSB",
        "msb": "MSB",
        "quan doi": "MB Bank",
        "mb": "MB Bank",
        "mbb": "MB Bank",
        "mbbank": "MB Bank",
        "dong nam a": "SEABank",
        "seab": "SEABank",
        "quoc te viet nam": "VIB",
        "quoc te": "VIB",
        "vib": "VIB",
        "an binh": "ABBank",
        "abb": "ABBank",
        "a chau": "ACB",
        "acb": "ACB",
        "nam a": "NamABank",
        "nab": "NamABank",
        "phuong dong": "OCB",
        "ocb": "OCB",
        "kien long": "KienLongBank",
        "klb": "KienLongBank",
        "bac a": "BacABank",
        "bab": "BacABank",
        "vietabank": "VietABank",
        "viet a": "VietABank",
        "vietcapital": "BVBank",
        "ban viet": "BVBank",
        "bvb": "BVBank",
        "viet nam thuong tin": "VietBank",
        "vbb": "VietBank",
        "saigonbank": "SaigonBank",
        "sgb": "SaigonBank",
        "petrolimex": "PGBank",
        "pgb": "PGBank",
        "xang dau petrolimex": "PGBank",
        "phat trien tp ho chi minh": "HDBank",
        "hdb": "HDBank",
        "ho chi minh city development": "HDBank",
        "hdbank": "HDBank",
        "tien phong": "TPBank",
        "tpb": "TPBank",
        "viet nam thinh vuong": "VPBank",
    }

    def _normalize_vn_bank_name(self, s: str) -> str:
        """Strip common prefixes/suffixes + diacritics for fuzzy matching."""
        import re
        import unicodedata
        if not s:
            return ""
        # Drop diacritics. Vietnamese 'Đ/đ' is LATIN LETTER D WITH STROKE
        # (a precomposed character, not base+combining-mark) — NFD does
        # NOT decompose it, so handle explicitly.
        s = s.replace("Đ", "D").replace("đ", "d")
        s = unicodedata.normalize("NFD", s)
        s = "".join(ch for ch in s if unicodedata.category(ch) != "Mn")
        s = s.lower().strip()
        # Strip branch suffix (everything after first " - " or " cn " or " pgd ")
        s = re.split(r"\s*-\s*", s, maxsplit=1)[0]
        # Strip common prefixes
        for prefix in (
            "ngan hang thuong mai co phan",
            "ngan hang tmcp",
            "ngan hang",
            "nh tmcp",
            "nh ",
            "tmcp",
        ):
            if s.startswith(prefix):
                s = s[len(prefix):].strip()
                break
        # Strip trailing "viet nam" or "vn" suffix (Vietcombank gets to stay
        # via alias table because stripping would collide with VietinBank)
        s = re.sub(r"\s*\(.*?\)\s*", "", s)
        # Collapse whitespace
        s = re.sub(r"\s+", " ", s).strip()
        return s

    def _resolve_bank(self, misa_long_name: str) -> str | None:
        """Match Misa full Vietnamese bank name → ERPNext Bank.name.

        Strategy ladder (return on first hit):
          1. Exact case-insensitive on bank_name or name
          2. Normalize Misa (strip diacritics, prefixes, branch suffix)
             then lookup in explicit alias table
          3. Normalized substring: Bank.bank_name normalized appears in
             normalized Misa, OR vice versa
        """
        if not misa_long_name:
            return None
        raw = misa_long_name.strip()
        raw_lower = raw.lower()

        # 1. Exact match (either bank_name or name)
        for b in self._banks:
            if (b.bank_name or "").strip().lower() == raw_lower:
                return b.name
            if (b.name or "").strip().lower() == raw_lower:
                return b.name

        # 2. Alias table lookup on normalized Misa name
        normalized = self._normalize_vn_bank_name(raw)
        alias_target = self._BANK_NAME_ALIASES.get(normalized)
        if alias_target and frappe.db.exists("Bank", alias_target):
            return alias_target
        # Try a few prefix variants from the normalized string
        for cut in range(len(normalized), 5, -1):
            head = normalized[:cut].strip()
            if head in self._BANK_NAME_ALIASES:
                tgt = self._BANK_NAME_ALIASES[head]
                if frappe.db.exists("Bank", tgt):
                    return tgt

        # 3. Normalized substring (bidirectional)
        for b in self._banks:
            short_norm = self._normalize_vn_bank_name(b.bank_name or b.name or "")
            if not short_norm or len(short_norm) < 2:
                continue
            if short_norm in normalized or normalized in short_norm:
                return b.name
        return None

    def lookup_existing(self, normalized):
        acc_no = normalized.get("_acc_no")
        if not acc_no:
            return None
        # Bank Account autoname is via account_name; we set name = acc_no
        # explicitly. Check both name and bank_account_no field.
        return (
            frappe.db.exists("Bank Account", acc_no)
            or frappe.db.get_value("Bank Account",
                                   {"bank_account_no": acc_no, "company": self._company},
                                   "name")
        )

    def build_doc(self, normalized: dict[str, Any]) -> dict[str, Any]:
        acc_no = normalized["_acc_no"]
        misa_bank_name = normalized.get("_bank_name", "")
        bank = self._resolve_bank(misa_bank_name)
        misa_status = (normalized.get("_status") or "").strip().lower()

        payload = {
            "doctype": "Bank Account",
            # account_name is the required display field; embed bank + acc_no
            "account_name": f"{(bank or misa_bank_name)[:50]} - {acc_no}",
            "bank": bank,  # may be None → causes validation fail; flag below
            "bank_account_no": acc_no,
            "company": self._company,
            "is_company_account": 1,
            "disabled": 1 if misa_status == "ngừng sử dụng" else 0,
        }
        # `account_type` is a Link to `Account Type` DocType (separate
        # from `Account.account_type`) that exists in some ERPNext
        # versions and not others. Only set if the DocType + entry exist.
        try:
            if frappe.db.exists("DocType", "Account Type") and \
                    frappe.db.exists("Account Type", "Current"):
                payload["account_type"] = "Current"
        except Exception:
            pass
        # `account` (GL link) is mandatory when is_company_account=1.
        # Resolve by exact match on Misa account_no first (e.g. TK
        # 04301010058291); if no leaf exists with that exact number,
        # SKIP the auto-link rather than picking a generic 1121.XX
        # which is almost certainly already taken by another Bank
        # Account → ValidationError. Without account, also flip
        # is_company_account=0 so the insert validates. Operator
        # manually links the right GL account post-import.
        gl_account = frappe.db.get_value(
            "Account",
            {"company": self._company, "account_number": acc_no,
             "is_group": 0}, "name",
        )
        if gl_account:
            # Also check it's not already linked to another Bank Account
            taken_by = frappe.db.get_value(
                "Bank Account", {"account": gl_account}, "name",
            )
            if not taken_by:
                payload["account"] = gl_account
        if not payload.get("account"):
            # No usable GL link → record-keeping only, not a company-side
            # bank account. Insert succeeds; operator can promote later.
            payload["is_company_account"] = 0
        # branch nameStr if exists
        if normalized.get("_branch"):
            payload["branch_code"] = normalized["_branch"][:140]
        return payload

    def post_row(self, row_doc):
        if row_doc.status != "Ready":
            return row_doc.status
        try:
            normalized = json.loads(row_doc.parsed_payload or "{}")
        except (ValueError, TypeError):
            normalized = {}
        try:
            payload = self.build_doc(normalized)
            if not payload.get("bank"):
                raise ValueError(
                    f"Không match được Bank cho '{normalized.get('_bank_name')}'. "
                    "Import Bank trước hoặc tạo Bank thủ công."
                )
            code = normalized.get("_acc_no")
            doc = frappe.get_doc(payload)
            doc.insert(ignore_permissions=True, set_name=code)
            self._mark(row_doc, "Posted", None, normalized, target_name=doc.name)
            self.counts["posted"] += 1
            return "Posted"
        except Exception as exc:
            err = f"{type(exc).__name__}: {exc}"
            frappe.log_error(title="Misa Migration Bank Account create failed", message=err)
            self._mark(row_doc, "Failed", err, normalized)
            self.counts["failed"] += 1
            return "Failed"
