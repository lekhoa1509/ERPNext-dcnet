"""Item importer — Misa Danh_sach_hang_hoa_dich_vu → ERPNext Item.

Misa cols (59 total, only essentials mapped here):
  STT / Mã / Tên / Giảm thuế / Tính chất / Nhóm VTHH / Đơn vị tính chính /
  Số lượng tồn / TK Kho / TK  Doanh thu / TK chi phí / Mã kho ngầm định /
  Thuế suất GTGT / Trạng thái / Mô tả / ...

Pipeline:
  - dedupe_key = Mã (Misa item code), doc.name = Mã (spec §15.4)
  - item_name = Tên (long Misa name, capped 140)
  - item_group fallback chain (Misa Nhóm → All Item Groups → Services)
  - stock_uom fallback chain (Misa UOM → Nos → Unit)
  - Item Defaults child table per Company with income/expense/asset
    accounts resolved via Misa Account Mapping Single (built by Phase 2),
    default_warehouse from Misa Mã kho ngầm định.

Tính chất → is_stock_item / is_fixed_asset / is_ccdc → commit C-C3.
"""

from __future__ import annotations

import json

import frappe

from vn_accounting.misa_migration.importers.base import BaseImporter


class ItemImporter(BaseImporter):
    file_type = "Item"
    entity_type = "Item"
    target_doctype = "Item"
    column_map = {
        # Header strings copied verbatim from Misa Excel — note double-space
        # in 'TK  Doanh thu' (Misa quirk; do not normalize).
        "_code": "Mã",
        "_name": "Tên",
        "_tinh_chat": "Tính chất",
        "_nhom": "Nhóm VTHH",
        "_uom": "Đơn vị tính chính",
        "_origin": "Nguồn gốc",
        "_desc": "Mô tả",
        "_tk_kho": "TK Kho",
        "_tk_doanh_thu": "TK  Doanh thu",
        "_tk_chi_phi": "TK chi phí",
        "_tk_chiet_khau": "TK chiết khấu",
        "_tk_giam_gia": "TK giảm giá",
        "_tk_tra_lai": "TK Trả lại",
        "_ma_kho": "Mã kho ngầm định",
        "_kho_name": "Kho ngầm định",
        "_vat_rate": "Thuế suất GTGT",
        "_status": "Trạng thái",
    }

    def __init__(self, batch_name: str):
        super().__init__(batch_name)
        self._company = frappe.db.get_value("Misa Migration Batch", batch_name, "company")
        # Load Misa Account Mapping once — read-mostly, populated by Phase 2.
        self._tk_to_account = self._load_account_mapping()

    def _load_account_mapping(self) -> dict:
        """Read Misa Account Mapping Single. Returns {misa_code: erpnext_account_name}."""
        try:
            doc = frappe.get_single("Misa Account Mapping")
            return json.loads(doc.mappings or "{}")
        except Exception:
            return {}

    def _resolve_account(self, misa_tk: str | None) -> str | None:
        """Misa TK → leaf Account.name, COMPANY-VERIFIED (see _account_lookup).

        The naive mapping-first lookup leaked another company's accounts on
        a fresh-company migration (the mapping Single is site-wide)."""
        from vn_accounting.misa_migration.importers.nkc_handlers._account_lookup import (
            resolve_account,
        )
        return resolve_account(misa_tk, self._tk_to_account, self._company)

    def _resolve_warehouse(self, misa_ma_kho: str | None) -> str | None:
        if not misa_ma_kho or not self._company:
            return None
        ma = str(misa_ma_kho).strip()
        if not ma:
            return None
        return frappe.db.get_value(
            "Warehouse", {"warehouse_name": ma, "company": self._company}, "name"
        )

    # Cache per-company default warehouse lookup
    _company_default_wh_cache: dict[str, str] = {}

    def _get_company_default_warehouse(self, company: str) -> str | None:
        """First non-group warehouse on the target company. Used as
        Item.default_warehouse to prevent ERPNext from auto-pulling
        Stock Settings.default_warehouse (which may belong to a
        different company on a multi-company site)."""
        cached = self._company_default_wh_cache.get(company)
        if cached is not None:
            return cached
        wh = frappe.db.get_value(
            "Warehouse",
            {"company": company, "is_group": 0, "disabled": 0},
            "name",
            order_by="creation",
        )
        self._company_default_wh_cache[company] = wh or ""
        return wh or None

    def dedupe_key(self, normalized):
        return normalized.get("_code")

    def validate(self, normalized):
        errs = []
        if not normalized.get("_code"):
            errs.append("Thiếu 'Mã' (item_code)")
        if not normalized.get("_name"):
            errs.append("Thiếu 'Tên' (item_name)")
        return errs

    @staticmethod
    def _sanitize_code(code: str) -> str:
        """Sanitize Misa item_code for Frappe naming. Must match build_doc.

        Frappe naming rejects '<' and '>' (raises NameError). Misa exports
        legit codes like "MOD_WT-QSFP28-SR4_SFP->XFP" — replace arrows with
        safe '-'. lookup_existing and build_doc MUST apply the same
        transform, else preview finds nothing and post hits duplicate-key
        on the sanitized name that's already in DB.
        """
        if not code:
            return code
        if "<" in code or ">" in code:
            return code.replace("<", "-").replace(">", "-")
        return code

    def lookup_existing(self, normalized):
        raw = normalized.get("_code")
        if not raw:
            return None
        code = self._sanitize_code(raw)
        # Item.name autoname = item_code by default in v16. Check BOTH the
        # sanitized form (matches what build_doc would insert) and the raw
        # form (covers legacy items inserted before sanitization existed).
        return (
            frappe.db.get_value("Item", code, "name")
            or frappe.db.get_value("Item", {"item_code": code}, "name")
            or (raw != code and (
                frappe.db.get_value("Item", raw, "name")
                or frappe.db.get_value("Item", {"item_code": raw}, "name")
            ))
            or None
        )

    def build_doc(self, normalized):
        code = self._sanitize_code(normalized["_code"])
        if code != normalized["_code"]:
            normalized["_code"] = code  # keep payload consistent for caller
        # item_group: prefer Misa Nhóm VTHH if a matching Item Group exists,
        # else fall back to 'All Item Groups' (root) or 'Services'.
        nhom = normalized.get("_nhom")
        item_group = None
        if nhom and frappe.db.exists("Item Group", nhom):
            item_group = nhom
        elif frappe.db.exists("Item Group", "All Item Groups"):
            item_group = "All Item Groups"
        else:
            item_group = "Services"

        # stock_uom: prefer Misa Đơn vị tính chính if a matching UOM exists,
        # else fall back to 'Nos'.
        uom = normalized.get("_uom")
        stock_uom = None
        if uom and frappe.db.exists("UOM", uom):
            stock_uom = uom
        elif frappe.db.exists("UOM", "Nos"):
            stock_uom = "Nos"
        else:
            stock_uom = "Unit"  # last resort

        # Tính chất → flag map (spec §6.2)
        tinh_chat = (normalized.get("_tinh_chat") or "").strip()
        is_stock = 1
        is_fixed_asset = 0
        if tinh_chat == "Dịch vụ":
            is_stock = 0
            # Force item_group to Services if available
            if frappe.db.exists("Item Group", "Services"):
                item_group = "Services"
        elif tinh_chat == "TSCĐ":
            is_fixed_asset = 1
            is_stock = 0  # ERPNext convention — fixed assets are not stock items
        elif tinh_chat in ("Hàng hóa", "Vật tư", "CCDC"):
            is_stock = 1
        elif not tinh_chat:
            # Blank Tính chất → safer fallback to Service (spec §6.2)
            is_stock = 0

        payload = {
            "doctype": "Item",
            "item_code": code,
            "item_name": normalized["_name"][:140],  # ERPNext item_name max
            "item_group": item_group,
            "stock_uom": stock_uom,
            "is_stock_item": is_stock,
            "is_fixed_asset": is_fixed_asset,
            "description": (normalized.get("_desc") or normalized["_name"])[:1000],
            "disabled": 1 if (normalized.get("_status") or "").strip().lower() == "ngừng sử dụng" else 0,
        }
        # Master importer fix: ERPNext auto-populates Item.default_warehouse
        # from Stock Settings (often a foreign-company warehouse like
        # "Stores - DC") if the field is empty — AND auto-populates the
        # same on item_defaults rows even for `is_stock_item=0` service
        # items. For multi-company sites, explicitly set it to a non-group
        # warehouse on the TARGET company so validation doesn't reject
        # the insert. Service items don't really use the warehouse, but
        # the field's presence prevents the bad auto-default.
        if self._company:
            company_wh = self._get_company_default_warehouse(self._company)
            if company_wh:
                payload["default_warehouse"] = company_wh
        # CCDC tag: vn_accounting doesn't ship an Item.is_ccdc custom field
        # on DCNet site, so CCDC items just import as is_stock_item=1 with
        # description marker. User can add the tag manually via Item form.
        if tinh_chat == "CCDC":
            payload["description"] = (payload.get("description", "") + " [CCDC]")[:1000]

        # Item Defaults child table (per-Company) — ALWAYS emit for the
        # target company so ERPNext's controller doesn't auto-create one
        # using `frappe.defaults.get_global_default('company')`, which
        # on multi-company sites is usually a DIFFERENT company than the
        # batch's target — causing "Warehouse X doesn't belong to Company
        # Y" validation errors at insert time.
        if self._company:
            row = {"company": self._company}
            income = self._resolve_account(normalized.get("_tk_doanh_thu"))
            expense = self._resolve_account(normalized.get("_tk_chi_phi"))
            warehouse = self._resolve_warehouse(normalized.get("_ma_kho"))
            if income:
                row["income_account"] = income
            if expense:
                row["expense_account"] = expense
            # Per-item warehouse from Misa Mã kho. Fall back to the
            # target-company default if Misa Mã kho didn't resolve to a
            # DCNET TEST warehouse — ALWAYS include a warehouse so
            # ERPNext doesn't auto-fill from Stock Settings (which is
            # the bug we're working around).
            if warehouse:
                row["default_warehouse"] = warehouse
            elif payload.get("default_warehouse"):
                row["default_warehouse"] = payload["default_warehouse"]
            else:
                # Last-resort: pick any non-group warehouse on the
                # target company. Without ANY warehouse on item_defaults,
                # ERPNext auto-populates Stock Settings default
                # → validation fail.
                fallback_wh = self._get_company_default_warehouse(self._company)
                if fallback_wh:
                    row["default_warehouse"] = fallback_wh
            # Always emit the row (even if only company+warehouse set) —
            # the entire purpose is to PREEMPT ERPNext's bad auto-default.
            payload["item_defaults"] = [row]

        return payload
