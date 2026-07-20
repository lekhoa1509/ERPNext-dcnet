"""Ensure Company defaults required by Phase 4 transaction handlers.

B3 + B4 fix for the real-data E2E findings:

- Sales Invoice needs Company.default_receivable_account = TK 131 leaf
  (otherwise the SI fails with "Income Account None cannot be same as
  Debit To None")
- Purchase Invoice needs Company.default_payable_account = TK 331 leaf
- PI with update_stock=1 needs Company.stock_received_but_not_billed =
  TK 3388 / 1561 / similar suspense account
- Stock Entry needs Company.stock_adjustment_account (already covered
  by importers/nkc_handlers/stock_entry.py:_ensure_stock_adjustment_account)
- Various other Phase 4 docs use Company.cost_center as default

`ensure_company_defaults_for_misa(company)` idempotently sets each of
these to the best-matching VN COA TK leaf. Called from
phase_4_orchestrator.run_phase_4_post at start of post.

Pattern: only SET if currently unset. Operator's manual configuration
always wins.
"""

from __future__ import annotations

from typing import Any

import frappe


# Company field → (priority list of TKs to try as fallback)
_DEFAULTS_MAP: dict[str, tuple[str, ...]] = {
    "default_receivable_account":     ("131",),
    "default_payable_account":        ("331",),
    "default_employee_advance_account": ("141",),
    "default_income_account":         ("511", "5111"),
    "default_expense_account":        ("642", "6421", "6427"),
    "default_inventory_account":      ("156", "1561", "152", "155"),
    "stock_received_but_not_billed":  ("3388", "3318", "338"),
    "stock_adjustment_account":       ("632",),
    "cost_of_goods_sold_account":     ("632",),
    "round_off_account":              ("711", "811"),
    "write_off_account":              ("811",),
    "default_deferred_revenue_account": ("3387",),
    "default_deferred_expense_account": ("242",),
}


def _find_leaf(company: str, tk: str) -> str | None:
    """Resolve TK to a leaf Account.name on the given Company."""
    return frappe.db.get_value(
        "Account",
        {"account_number": tk, "company": company, "is_group": 0},
        "name",
    )


def _ensure_cost_center(company: str) -> str | None:
    """Pick a non-group Cost Center for the company."""
    cc = frappe.db.get_value(
        "Cost Center",
        {"company": company, "is_group": 0, "disabled": 0},
        "name",
    )
    return cc


def ensure_uoms_allow_fractional(uoms: tuple[str, ...] = (
    "Nos", "Unit", "Pair", "Set", "Box",
)) -> list[str]:
    """Toggle `must_be_whole_number=0` on UOMs that Misa items default to.

    Misa source data has fractional qty (e.g. 22.5) on items whose
    UOM defaults to 'Nos' or 'Unit'. ERPNext rejects with
    UOMMustBeIntegerError. Disabling the whole-number flag is the
    ERPNext-recommended path when the UOM is a generic counter
    (vs. a true integer-only unit like 'Box of 12').

    Idempotent: only clears when currently set. Returns list of UOMs
    actually changed.
    """
    changed: list[str] = []
    for uom in uoms:
        cur = frappe.db.get_value("UOM", uom, "must_be_whole_number")
        if cur:
            frappe.db.set_value("UOM", uom, "must_be_whole_number", 0,
                                update_modified=False)
            changed.append(uom)
    if changed:
        frappe.db.commit()
    return changed


# Warehouse-name → inventory-account-TK heuristic mapping.
# Order matters: most-specific patterns FIRST. Each tuple is
# (regex pattern, list of fallback TK codes to try). The first
# leaf found from the candidate list wins. Case-insensitive,
# Vietnamese-aware (diacritics matter on Misa naming).
_WAREHOUSE_ACCOUNT_HEURISTICS: tuple[tuple[str, tuple[str, ...]], ...] = (
    # CCDC / Tools & Equipment → TK 1531
    (r"(c[ôo]ng[\s_]*c[ụu]|ccdc|thu[\s_]*h[ồo]i|thuhoi)", ("1531", "153")),
    # Raw materials → TK 152
    (r"(nguy[êe]n[\s_]*v[ậa]t[\s_]*li[ệe]u|v[ậa]t[\s_]*t[ưu]|nvl)", ("152", "1521")),
    # Finished goods → TK 155
    (r"(th[àa]nh[\s_]*ph[ẩa]m|\btp\b|finished)", ("155", "1551")),
    # Goods in transit / consignment → TK 157
    (r"(g[ửu]i[\s_]*b[áa]n|h[àa]ng[\s_]*g[ửu]i|in[\s_]*transit)", ("157",)),
    # Goods at duty-free bonded warehouse → TK 158
    (r"(b[ảa]o[\s_]*thu[ếe]|bonded)", ("158",)),
    # Default: merchandise → TK 1561
    (r".*", ("1561", "156")),
)


def bind_warehouse_accounts_to_misa_inventory(
    company: str,
    only_unset: bool = True,
) -> dict[str, Any]:
    """Bind each Warehouse.account based on Misa-style name heuristics.

    Misa source ships flat Warehouse list without per-warehouse account
    mapping. ERPNext perpetual-inventory chain requires each warehouse to
    bind to ONE inventory account, and silently substitutes a PI line's
    expense_account to the warehouse's account on submit when they differ.
    Result: a CCDC line (TK 1531) into a 1561-bound warehouse posts to
    1561, losing the per-class GL split.

    This helper walks every warehouse on the company and binds an account
    based on Vietnamese name patterns:
      - 'CÔNG CỤ', 'CCDC', 'THU HỒI'   → TK 1531  (Tools & Equipment)
      - 'NGUYÊN VẬT LIỆU', 'NVL'       → TK 152
      - 'THÀNH PHẨM'                    → TK 155
      - default                         → TK 1561

    Args:
      company: target Company.
      only_unset: when True (default), only binds warehouses with
        Warehouse.account=NULL. Existing operator config is preserved.

    Returns: {"changed": N, "skipped": M, "missing_account": K, "binds": [...]}
    """
    import re
    from frappe.utils import flt as _flt  # noqa: F401 (silence unused warn)

    counts = {"changed": 0, "skipped": 0, "missing_account": 0, "binds": []}
    compiled: list[tuple[re.Pattern, tuple[str, ...]]] = [
        (re.compile(p, re.I), tks) for p, tks in _WAREHOUSE_ACCOUNT_HEURISTICS
    ]

    warehouses = frappe.db.sql(
        """SELECT name, warehouse_name, account
           FROM `tabWarehouse`
           WHERE company=%s AND is_group=0""",
        (company,),
        as_dict=True,
    )

    for w in warehouses:
        if only_unset and w.get("account"):
            counts["skipped"] += 1
            continue
        # match against both warehouse_name (no suffix) and name (with " - DCT")
        label = (w.get("warehouse_name") or w["name"] or "")
        chosen_tks: tuple[str, ...] = ("1561", "156")  # safety fallback
        for pattern, tks in compiled:
            if pattern.search(label):
                chosen_tks = tks
                break
        # Resolve to a leaf account on the company
        account = None
        for tk in chosen_tks:
            account = _find_leaf(company, tk)
            if account:
                break
        if not account:
            counts["missing_account"] += 1
            continue
        frappe.db.set_value(
            "Warehouse", w["name"], "account", account,
            update_modified=False,
        )
        counts["changed"] += 1
        counts["binds"].append({"warehouse": w["name"], "account": account})

    frappe.db.commit()
    return counts


def ensure_allow_negative_stock() -> dict[str, Any]:
    """Enable Stock Settings.allow_negative_stock during Misa migration.

    Misa PI handler uses a stock-eligible placeholder Item, so the real
    item codes referenced by SE Material Issue (PX) often have zero
    prior stock in the warehouse → ERPNext rejects with `NegativeStockError`.
    The PN/PI ↔ SE PX item mapping is architecturally split (PI uses
    placeholder, SE PX uses real items from SCT); during migration we
    accept this gap by allowing negative stock.

    Idempotent: only flips when currently 0. Returns {"changed": bool,
    "was": 0|1}. Caller may use the "was" value to restore the original
    setting after migration if needed (we recommend leaving it ON for
    sandbox/dev sites since Misa data inherently lacks the SLE chain).
    """
    current = frappe.db.get_single_value("Stock Settings", "allow_negative_stock")
    was = int(current or 0)
    if was:
        return {"changed": False, "was": was}
    frappe.db.set_single_value("Stock Settings", "allow_negative_stock", 1)
    frappe.db.commit()
    return {"changed": True, "was": was}


def ensure_company_defaults_for_misa(company: str) -> dict[str, Any]:
    """Set Company default Account fields required by Misa Phase 4 handlers.

    Idempotent: only writes fields that are currently NULL/empty. Returns
    a dict {field: resolved_account} for everything set this call.
    """
    set_now: dict[str, Any] = {}
    meta = frappe.get_meta("Company")
    company_doc_fields = {f.fieldname for f in meta.fields}

    for fieldname, tk_candidates in _DEFAULTS_MAP.items():
        if fieldname not in company_doc_fields:
            # Field doesn't exist on this site's Company schema → skip
            continue
        current = frappe.db.get_value("Company", company, fieldname)
        if current:
            # Self-heal: replace group accounts with their leaf. ERPNext
            # validates these defaults at posting time and rejects groups
            # (e.g. PI line "expense_account = 156 - Hàng hoá - DCT [group]"
            # fails because update_stock=1 copies it from default_inventory_account).
            is_group = frappe.db.get_value("Account", current, "is_group")
            if not is_group:
                continue  # already set to a leaf; respect operator config
            # else: fall through to re-resolve from tk_candidates
        for tk in tk_candidates:
            acct = _find_leaf(company, tk)
            if acct:
                frappe.db.set_value(
                    "Company", company, fieldname, acct, update_modified=False,
                )
                set_now[fieldname] = acct
                break

    # Cost center default
    if "cost_center" in company_doc_fields:
        current_cc = frappe.db.get_value("Company", company, "cost_center")
        if not current_cc:
            cc = _ensure_cost_center(company)
            if cc:
                frappe.db.set_value(
                    "Company", company, "cost_center", cc, update_modified=False,
                )
                set_now["cost_center"] = cc

    frappe.db.commit()
    return set_now


def ensure_party_accounts_for_misa(company: str) -> dict[str, int]:
    """Ensure every Customer/Supplier on this site has the correct
    AR/AP account in its `accounts` child table.

    Misa Phase 4 SI/PI rely on ERPNext to auto-pick receivable_account /
    payable_account from the Customer/Supplier doc. If absent and
    Company.default_receivable_account isn't set, posting fails with
    "Debit To None" errors.

    B3 fix: this helper backfills the accounts child table on
    bulk-created Customer/Supplier stubs. Pattern: for each party
    without an `accounts` row for this company, add one pointing at
    Company.default_receivable_account / default_payable_account.

    Foreign-currency parties (default_currency != company default) are
    SKIPPED — appending a VND party account to a USD/EUR Customer would
    trigger ERPNext's "Billing currency must equal company or party
    account currency" validation popup. Operators must manually assign
    a currency-matched receivable/payable account for those.

    Returns: {customer_updated, supplier_updated, foreign_skipped}
    """
    counts = {
        "customer_updated": 0, "supplier_updated": 0,
        "foreign_skipped": 0,
    }

    receivable = frappe.db.get_value("Company", company, "default_receivable_account")
    payable = frappe.db.get_value("Company", company, "default_payable_account")
    company_currency = frappe.db.get_value("Company", company, "default_currency") or "VND"

    if receivable:
        # Find customers WITHOUT an accounts row for this company
        customers_missing = frappe.db.sql(
            """
            SELECT c.name, c.default_currency
            FROM `tabCustomer` c
            LEFT JOIN `tabParty Account` pa
                ON pa.parent = c.name AND pa.parenttype = 'Customer'
                AND pa.company = %s
            WHERE pa.name IS NULL
            """,
            (company,),
            as_dict=True,
        )
        for c in customers_missing:
            cust_ccy = (c.get("default_currency") or "").strip()
            if cust_ccy and cust_ccy != company_currency:
                # Skip foreign-currency party — would trigger billing-
                # currency-mismatch popup. Operator must assign a
                # currency-matched receivable account manually.
                counts["foreign_skipped"] += 1
                continue
            try:
                doc = frappe.get_doc("Customer", c["name"])
                doc.append("accounts", {
                    "company": company,
                    "account": receivable,
                })
                doc.flags.ignore_permissions = True
                doc.save()
                counts["customer_updated"] += 1
            except Exception:
                continue
        frappe.db.commit()

    if payable:
        suppliers_missing = frappe.db.sql(
            """
            SELECT s.name, s.default_currency
            FROM `tabSupplier` s
            LEFT JOIN `tabParty Account` pa
                ON pa.parent = s.name AND pa.parenttype = 'Supplier'
                AND pa.company = %s
            WHERE pa.name IS NULL
            """,
            (company,),
            as_dict=True,
        )
        for s in suppliers_missing:
            supp_ccy = (s.get("default_currency") or "").strip()
            if supp_ccy and supp_ccy != company_currency:
                counts["foreign_skipped"] += 1
                continue
            try:
                doc = frappe.get_doc("Supplier", s["name"])
                doc.append("accounts", {
                    "company": company,
                    "account": payable,
                })
                doc.flags.ignore_permissions = True
                doc.save()
                counts["supplier_updated"] += 1
            except Exception:
                continue
        frappe.db.commit()

    return counts
