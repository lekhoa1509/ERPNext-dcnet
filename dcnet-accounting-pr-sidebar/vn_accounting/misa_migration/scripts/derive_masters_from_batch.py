"""Derive masters from a Misa batch's transactional content.

For scoped batches (e.g. monthly imports with only NKC/BR/MV/SCT/OB files
and no separate Phase 1/2/3 master files), the install_misa_coa pipeline
skips master importers because the file_types aren't in the batch.

This module DERIVES the needed masters by inspecting the batch's parsed
payloads:

  - Tier-5 Accounts ← OB Account Balance (TKs not in baseline CoA)
  - Warehouses ← OB Inventory (Mã kho + Tên kho)
  - Items ← OB Inventory + SCT (Mã hàng + Tên hàng + ĐVT)
  - UOM ← Item ĐVT (auto-create as needed)
  - Customers ← NKC where TK or TK đối ứng starts with 131
  - Suppliers ← NKC where TK or TK đối ứng starts with 331

Idempotent — every importer checks existence before insert.

Public entry: ``derive_masters_for_batch(batch_name)`` — also whitelisted
as ``vn_accounting.misa_migration.scripts.derive_masters_from_batch.derive_masters_for_batch``
for UI calls from the Misa Migration page.
"""
from __future__ import annotations

import json
import re
from typing import Any

import frappe

from vn_accounting.misa_migration.importers.account import (
    _find_parent_account,
    _find_root_account_for_type,
    _detect_root_type,
)


def _load_payloads(batch_name: str, file_type: str):
    """Yield raw_payload dicts for all rows of a file_type."""
    rows = frappe.db.sql(
        "SELECT raw_payload FROM `tabMisa Migration Row` WHERE batch=%s AND file_type=%s",
        (batch_name, file_type),
        as_dict=True,
    )
    for r in rows:
        try:
            yield json.loads(r["raw_payload"] or "{}")
        except (ValueError, TypeError):
            continue


def _derive_accounts(batch_name: str, company: str) -> dict[str, int]:
    """Create Tier-5 Accounts from any TK referenced in the batch.

    Sources, in priority order:
      1. OB Account Balance rows — have TK + tên (best source for naming).
      2. NKC rows — Tài khoản + TK đối ứng columns. Misa TKs not in (1)
         get a placeholder name "Tài khoản <TK>"; KTT can rename later.
      3. Bang ke BR / MV — TK đầu vào / đầu ra (optional).

    Without scanning NKC, transactions referencing TKs absent from OB
    Account Balance (which only lists balances, not pure pass-through
    accounts like 5111/5212/521x discount/return TKs) cause bulk pump
    to silently route to fallback accounts → balance corruption.
    """
    # Gather (tk → name) from all sources
    tk_names: dict[str, str] = {}

    # Priority 1: OB Account Balance (authoritative names)
    for p in _load_payloads(batch_name, "OB Account Balance"):
        tk = str(p.get("Số tài khoản") or "").strip()
        name = str(p.get("Tên tài khoản") or "").strip()
        if tk and name and tk not in tk_names:
            tk_names[tk] = name

    # Priority 2: NKC — both 'Tài khoản' and 'TK đối ứng' columns
    for p in _load_payloads(batch_name, "NKC"):
        for col in ("Tài khoản", "TK đối ứng"):
            tk = str(p.get(col) or "").strip()
            if tk and tk[0].isdigit() and tk not in tk_names:
                tk_names[tk] = f"Tài khoản {tk}"  # placeholder name

    # Sort by TK length ASC so parents process first; auto-promote them
    # when children come.
    sorted_tks = sorted(tk_names.items(), key=lambda x: (len(x[0]), x[0]))

    created = skipped = errored = 0
    for tk, name_vi in sorted_tks:
        if frappe.db.get_value(
            "Account", {"account_number": tk, "company": company}, "name"
        ):
            skipped += 1
            continue
        parent = _find_parent_account(tk, company)
        root_type = _detect_root_type(tk)
        if not parent:
            parent = _find_root_account_for_type(root_type, company)
        if not parent:
            errored += 1
            continue
        try:
            doc = frappe.get_doc({
                "doctype": "Account",
                "account_name": name_vi,
                "account_number": tk,
                "company": company,
                "is_group": 0,
                "root_type": root_type,
                "parent_account": parent,
            })
            doc.flags.ignore_permissions = True
            doc.insert()
            created += 1
        except Exception as exc:
            errored += 1
            frappe.log_error(
                title=f"derive_masters: Account {tk} failed",
                message=str(exc),
            )
    frappe.db.commit()
    return {
        "created": created,
        "skipped": skipped,
        "errored": errored,
        "found_unique_tks": len(tk_names),
    }


def _ensure_root_warehouse(company: str) -> str:
    """Find or create the root Warehouse group for the company."""
    parent = frappe.db.get_value(
        "Warehouse",
        {"company": company, "is_group": 1, "parent_warehouse": ("is", "not set")},
        "name",
    )
    if parent:
        return parent
    root = frappe.get_doc({
        "doctype": "Warehouse",
        "warehouse_name": company,
        "company": company,
        "is_group": 1,
    })
    root.flags.ignore_mandatory = True
    root.flags.ignore_permissions = True
    root.insert()
    return root.name


def _resolve_inventory_account(company: str, wh_code: str = "", wh_name: str = "") -> str | None:
    """Find inventory leaf for the Company, biased by warehouse type.

    SE Material Receipt routes Dr to Warehouse.account — without this,
    Warehouse.account=None → SE falls back to stock_adjustment (632) →
    TK 1561 source CB short ~1B.

    Routing heuristic by warehouse code/name:
    - "Thành phẩm" / "TP" / "KTP" / "FG" → TK 1551 (Thành phẩm nhập kho).
    - "Công cụ" / "CC" / "CCDC" → TK 1531 (Công cụ dụng cụ).
    - Default → TK 1561 (Giá mua hàng hóa).

    Without per-warehouse-type routing, FG warehouses (KTP) map to 1561
    instead of 1551 → Cr leg on PX Issue posts to 1561 not 1551 → BCDTK
    TK 1551 closing short. Real DCNET T1/2026 PX20260052 hit this.
    """
    txt = f"{wh_code} {wh_name}".upper()
    # FG indicators
    if any(k in txt for k in ("KTP", "THANH PHAM", "THÀNH PHẨM", " TP ", " FG ", "FINISHED")):
        for tk in ("1551", "155"):
            acc = frappe.db.sql(
                """SELECT name FROM `tabAccount` WHERE company=%s
                   AND account_number LIKE %s AND is_group=0
                   ORDER BY LENGTH(account_number) DESC LIMIT 1""",
                (company, tk + "%"),
            )
            if acc:
                return acc[0][0]
    # Tools/equipment (CCDC) indicators
    if any(k in txt for k in ("CCDC", " CC ", "CÔNG CỤ", "CONG CU")):
        for tk in ("1531", "153"):
            acc = frappe.db.sql(
                """SELECT name FROM `tabAccount` WHERE company=%s
                   AND account_number LIKE %s AND is_group=0
                   ORDER BY LENGTH(account_number) DESC LIMIT 1""",
                (company, tk + "%"),
            )
            if acc:
                return acc[0][0]
    # Default: goods TK 1561
    for tk in ("1561", "156"):
        acc = frappe.db.sql(
            """SELECT name FROM `tabAccount` WHERE company=%s
               AND account_number LIKE %s AND is_group=0
               ORDER BY LENGTH(account_number) DESC LIMIT 1""",
            (company, tk + "%"),
        )
        if acc:
            return acc[0][0]
    return None


def _derive_warehouses(batch_name: str, company: str) -> dict[str, int]:
    """Create Warehouses from OB Inventory (Mã kho + Tên kho).
    Sets Warehouse.account = TK 1561 leaf so SE Material Receipt posts
    Dr 1561 (not fallback 632 stock_adjustment)."""
    seen: dict[str, str] = {}
    for p in _load_payloads(batch_name, "OB Inventory"):
        code = str(p.get("Mã kho") or "").strip()
        name = str(p.get("Tên kho") or "").strip()
        if code and name:
            seen.setdefault(code, name)

    parent = _ensure_root_warehouse(company)
    created = skipped = errored = backfilled = 0
    for code, name in seen.items():
        abbr = frappe.db.get_value("Company", company, "abbr") or ""
        # Per-warehouse-type inventory account routing (FG → 1551, CCDC → 1531,
        # else 1561). Without this, KTP (FG) warehouse routes to 1561 → BCDTK
        # TK 1551 short on PX Issue Cr leg.
        inv_account = _resolve_inventory_account(company, code, name)
        # warehouse_name = "{Mã kho} - {Tên kho}" so OB handler LIKE match
        wh_name = f"{code} - {name}"
        full_name = f"{wh_name} - {abbr}" if abbr else wh_name
        if frappe.db.exists("Warehouse", full_name):
            skipped += 1
            # Backfill account on existing — handles re-run when previous
            # derive run created Warehouse without account OR with wrong
            # account (e.g. KTP currently has 1561, should be 1551).
            current_acc = frappe.db.get_value("Warehouse", full_name, "account")
            if inv_account and current_acc != inv_account:
                frappe.db.set_value("Warehouse", full_name, "account", inv_account)
                backfilled += 1
            continue
        try:
            doc = frappe.get_doc({
                "doctype": "Warehouse",
                "warehouse_name": wh_name,
                "company": company,
                "is_group": 0,
                "parent_warehouse": parent,
                "account": inv_account,  # Routes by warehouse type
            })
            doc.flags.ignore_permissions = True
            doc.insert()
            created += 1
        except Exception as exc:
            errored += 1
            frappe.log_error(
                title=f"derive_masters: Warehouse {code} failed",
                message=str(exc),
            )
    frappe.db.commit()
    return {"created": created, "skipped": skipped, "errored": errored, "found": len(seen)}


def _ensure_uom(uom: str) -> str:
    if not uom:
        return "Nos"
    if frappe.db.exists("UOM", uom):
        return uom
    try:
        doc = frappe.get_doc({
            "doctype": "UOM",
            "uom_name": uom,
            "must_be_whole_number": 0,
        })
        doc.flags.ignore_permissions = True
        doc.insert()
        return uom
    except Exception:
        return "Nos"


def _ensure_item_group() -> str:
    if frappe.db.exists("Item Group", "All Item Groups"):
        return "All Item Groups"
    doc = frappe.get_doc({
        "doctype": "Item Group",
        "item_group_name": "All Item Groups",
        "is_group": 1,
    })
    doc.flags.ignore_mandatory = True
    doc.flags.ignore_permissions = True
    doc.insert()
    return "All Item Groups"


def _derive_items(batch_name: str, company: str) -> dict[str, int]:
    """Create Items from OB Inventory + SCT (Mã hàng + Tên hàng + ĐVT)."""
    seen: dict[str, tuple[str, str]] = {}
    for ft in ("OB Inventory", "SCT"):
        for p in _load_payloads(batch_name, ft):
            code = str(p.get("Mã hàng") or "").strip()
            name = str(p.get("Tên hàng") or "").strip()
            uom = str(p.get("ĐVT") or "").strip()
            if code and name and code not in seen:
                seen[code] = (name, uom)

    item_group = _ensure_item_group()
    created = skipped = errored = 0
    for code, (name, uom) in seen.items():
        # Sanitize code consistent with Item importer (< > → -)
        if "<" in code or ">" in code:
            code = code.replace("<", "-").replace(">", "-")
        if frappe.db.exists("Item", code):
            skipped += 1
            continue
        uom_name = _ensure_uom(uom)
        try:
            doc = frappe.get_doc({
                "doctype": "Item",
                "item_code": code,
                "item_name": name[:140],
                "item_group": item_group,
                "stock_uom": uom_name,
                "is_stock_item": 1,
                "include_item_in_manufacturing": 0,
            })
            doc.flags.ignore_permissions = True
            doc.insert()
            created += 1
        except Exception as exc:
            errored += 1
            frappe.log_error(
                title=f"derive_masters: Item {code} failed",
                message=str(exc),
            )
    frappe.db.commit()
    return {"created": created, "skipped": skipped, "errored": errored, "found": len(seen)}


def _ensure_groups() -> None:
    for dt, name, is_group in [
        ("Customer Group", "All Customer Groups", 1),
        ("Supplier Group", "All Supplier Groups", 1),
        ("Territory", "All Territories", 1),
    ]:
        if frappe.db.exists(dt, name):
            continue
        key = "customer_group_name" if dt == "Customer Group" else (
            "supplier_group_name" if dt == "Supplier Group" else "territory_name"
        )
        doc = frappe.get_doc({"doctype": dt, key: name, "is_group": is_group})
        doc.flags.ignore_permissions = True
        doc.flags.ignore_mandatory = True
        doc.insert()


def _derive_parties(batch_name: str) -> dict[str, dict]:
    """Create Customer + Supplier from NKC + BR + MV files.

    Sources:
      - NKC: 'Mã đối tượng' + 'Tên đối tượng'; classify by TK (131 →
        Customer, 331 → Supplier).
      - Bang ke BR (sales register): 'Tên người mua' + 'Mã số thuế
        người mua' → Customer. Some BR rows don't have a Misa mã
        đối tượng — register name + tax code as a fallback identifier.
      - Bang ke MV (purchase register): 'Tên người bán' + 'Mã số thuế
        người bán' → Supplier.
    """
    customers: dict[str, str] = {}
    suppliers: dict[str, str] = {}

    # Source 1: NKC (classified by TK + voucher prefix)
    # Prefix rule mirrors preflight.check_supplier_master_present: any
    # party_code on a supplier-side voucher (UNC bank fee to 'VIB', PC to
    # an employee code…) must exist as Supplier even with no 331 leg —
    # TK-only classification left 16 such codes missing on a fresh site.
    _SUPPLIER_PREFIXES = ("MDV", "MH", "PN", "UNC", "PC")
    _CUSTOMER_PREFIXES = ("BH", "BC", "PT")
    for p in _load_payloads(batch_name, "NKC"):
        code = str(p.get("Mã đối tượng") or "").strip()
        name = str(p.get("Tên đối tượng") or "").strip()
        tk = str(p.get("Tài khoản") or "").strip()
        tk_doi = str(p.get("TK đối ứng") or "").strip()
        if not code or not name:
            continue
        if tk.startswith("131") or tk_doi.startswith("131"):
            customers.setdefault(code, name)
        if tk.startswith("331") or tk_doi.startswith("331"):
            suppliers.setdefault(code, name)
        m = re.match(r"^([A-Z]+)", str(p.get("Số chứng từ") or ""))
        vp = m.group(1) if m else ""
        # PNHN/PXHN are stock prefixes that also start with PN/PX — match exact.
        if vp in _SUPPLIER_PREFIXES:
            suppliers.setdefault(code, name)
        elif vp in _CUSTOMER_PREFIXES:
            customers.setdefault(code, name)

    # Source 2: Bang ke BR (sales register → customers)
    for p in _load_payloads(batch_name, "Bang ke BR"):
        name = str(p.get("Tên người mua") or "").strip()
        mst = str(p.get("Mã số thuế người mua") or "").strip()
        if not name:
            continue
        # Use MST as code if available, else slug from name (truncated)
        code = mst or name[:60].strip()
        if code and code not in customers:
            customers[code] = name

    # Source 3: Bang ke MV (purchase register → suppliers)
    for p in _load_payloads(batch_name, "Bang ke MV"):
        name = str(p.get("Tên người bán") or "").strip()
        mst = str(p.get("Mã số thuế người bán") or "").strip()
        if not name:
            continue
        code = mst or name[:60].strip()
        if code and code not in suppliers:
            suppliers[code] = name

    _ensure_groups()

    def _insert(dt: str, code: str, name: str, group_field: str, group_value: str) -> bool:
        if frappe.db.exists(dt, code):
            return False
        payload = {
            "doctype": dt,
            f"{dt.lower().replace(' ', '_')}_name": name[:140],
            group_field: group_value,
        }
        if dt == "Customer":
            payload["territory"] = "All Territories"
        d = frappe.get_doc(payload)
        d.flags.ignore_permissions = True
        d.flags.ignore_mandatory = True
        # set_name forces doc.name = Misa code even when the site's
        # cust/supp_master_name setting is "by Name" (fresh-site default
        # names the doc by full company name → preflight/bulk_pump, which
        # address parties by code, see 399 "Supplier 'X' thiếu" blockers).
        d.insert(set_name=code)
        return True

    c_created = c_skipped = c_err = 0
    for code, name in customers.items():
        try:
            if _insert("Customer", code, name, "customer_group", "All Customer Groups"):
                c_created += 1
            else:
                c_skipped += 1
        except Exception as exc:
            c_err += 1
            frappe.log_error(
                title=f"derive_masters: Customer {code} failed",
                message=str(exc),
            )

    s_created = s_skipped = s_err = 0
    for code, name in suppliers.items():
        try:
            if _insert("Supplier", code, name, "supplier_group", "All Supplier Groups"):
                s_created += 1
            else:
                s_skipped += 1
        except Exception as exc:
            s_err += 1
            frappe.log_error(
                title=f"derive_masters: Supplier {code} failed",
                message=str(exc),
            )
    frappe.db.commit()
    return {
        "Customer": {"created": c_created, "skipped": c_skipped, "errored": c_err, "found": len(customers)},
        "Supplier": {"created": s_created, "skipped": s_skipped, "errored": s_err, "found": len(suppliers)},
    }


@frappe.whitelist()
def derive_masters_for_batch(batch_name: str) -> dict[str, Any]:
    """Derive missing masters for a scoped batch.

    Use after ``install_misa_coa`` (which bootstraps baseline CoA + Cost
    Center). This adds masters that the batch's NKC/BR/MV/SCT/OB rows
    REFERENCE but which aren't in the batch as standalone Phase 1/2/3
    files.

    Idempotent. Safe to re-run.
    """
    if not batch_name:
        frappe.throw(frappe._("Phải chọn batch."))
    company = frappe.db.get_value("Misa Migration Batch", batch_name, "company")
    if not company:
        frappe.throw(frappe._("Batch không có Company."))

    return {
        "batch": batch_name,
        "company": company,
        "Account": _derive_accounts(batch_name, company),
        "Warehouse": _derive_warehouses(batch_name, company),
        "Item": _derive_items(batch_name, company),
        "Parties": _derive_parties(batch_name),
    }
