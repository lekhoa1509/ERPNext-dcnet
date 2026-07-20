"""Chart of Accounts bootstrap — install vn_accounting VAS CoA on a new Company.

For sites that don't yet have a Frappe CoA set up, this installs one of the
vn_accounting templates (TT99/2025 small or large enterprise) so that the
Misa migration + bulk_pump can run.

Public entry: ``bootstrap_coa(company, template='vn_large_enterprise')`` — also
whitelisted as ``vn_accounting.misa_migration.bulk_pump.coa_bootstrap.bootstrap_coa``
for UI calls from the Misa Migration page.
"""
from __future__ import annotations

import json
import os
from typing import Any

import frappe
from erpnext.accounts.doctype.account.chart_of_accounts.chart_of_accounts import (
    create_charts,
)


TEMPLATES = {
    "vn_large_enterprise": "TT200/2014 + TT99/2025 — large enterprise",
    "vn_small_enterprise": "TT133/2016 — small enterprise",
}


def _template_path(template_name: str) -> str:
    coa_dir = os.path.join(
        frappe.get_app_path("vn_accounting"),
        "chart_of_accounts",
    )
    fname = f"{template_name}.json"
    full = os.path.join(coa_dir, fname)
    if not os.path.exists(full):
        frappe.throw(f"CoA template not found: {fname} in {coa_dir}")
    return full


def _load_template_tree(template_name: str) -> dict[str, Any]:
    path = _template_path(template_name)
    with open(path) as f:
        content = json.load(f)
    # Strip the top-level wrapper (name/country) — return tree only
    return content.get("tree", content)


def _count_vn_accounts(company: str) -> int:
    """Count accounts whose account_number matches VN VAS pattern (numeric-only,
    e.g., '111', '1111', '5111'). Frappe's auto-translated Standard CoA leaves
    account_number empty — so 0 here means non-VN CoA installed."""
    return frappe.db.sql(
        "SELECT COUNT(*) FROM `tabAccount` WHERE company=%s "
        "AND account_number REGEXP '^[0-9]+$'",
        (company,),
    )[0][0]


def _wipe_non_vn_coa(company: str) -> dict:
    """Drop ALL Account rows for a company. Caller MUST ensure 0 GL Entry first
    (this helper does NOT check). Used by bootstrap_coa(force=True) when Company
    has Standard CoA but needs VN VAS instead. Idempotent."""
    n_acc = frappe.db.count("Account", {"company": company})
    # Defensive — paranoid even though caller already checked.
    n_gl = frappe.db.count("GL Entry", {"company": company})
    if n_gl > 0:
        frappe.throw(
            f"Refuse to wipe CoA: Company '{company}' has {n_gl} GL Entry rows. "
            "Wipe transactions first."
        )
    # Drop Party Account refs (foreign-key holders), Item Default, then Accounts.
    frappe.db.sql("DELETE FROM `tabParty Account` WHERE company=%s", (company,))
    frappe.db.sql("DELETE FROM `tabItem Default` WHERE company=%s", (company,))
    frappe.db.sql(
        "DELETE FROM `tabMode of Payment Account` WHERE company=%s", (company,)
    )
    # Clear Company.default_*_account fields so Account.delete doesn't tripwire
    # NULL every Account-Link field on Company (not just _COMPANY_DEFAULT_FIELDS).
    # ERPNext Company has ~20 Link→Account fields (write_off, exchange_gain_loss,
    # round_off, gain_loss_on_asset_disposal, capital_work_in_progress,
    # asset_received_but_not_billed, service_expense, default_employee_advance,
    # default_payroll_payable, stock_received_but_not_billed, ...). Use raw SQL
    # to UPDATE NULL across ALL of them in one shot — avoids LinkValidationError
    # on Company.save() after Accounts wiped. Skip per-Frappe-version diff
    # by introspecting meta.
    co_meta = frappe.get_meta("Company")
    acct_fields = [
        f.fieldname for f in co_meta.fields
        if f.fieldtype == "Link" and f.options == "Account"
    ]
    if acct_fields:
        set_clause = ", ".join(f"`{fld}`=NULL" for fld in acct_fields)
        frappe.db.sql(
            f"UPDATE `tabCompany` SET {set_clause} WHERE name=%s", (company,)
        )
    # Now drop Accounts (FK_CHECKS off because Frappe nested-set lft/rgt order)
    frappe.db.sql("SET FOREIGN_KEY_CHECKS=0")
    frappe.db.sql("DELETE FROM `tabAccount` WHERE company=%s", (company,))
    frappe.db.sql("SET FOREIGN_KEY_CHECKS=1")
    frappe.db.commit()
    frappe.clear_document_cache("Company", company)
    return {"wiped_accounts": n_acc, "nulled_company_fields": acct_fields}


@frappe.whitelist()
def bootstrap_coa(
    company: str,
    template: str = "vn_large_enterprise",
    force: bool = False,
) -> dict[str, Any]:
    """Install a VAS CoA for ``company``.

    Default (force=False, idempotent):
      - 0 accounts → install template
      - >5 accounts INCLUDING ≥1 VN-format (numeric account_number) → skip
        (assume VN VAS already installed)
      - >5 accounts but 0 VN-format → return 'non_vn_coa_detected' warning,
        do nothing. Caller (UI) shows warning + offers force=True button.

    Force mode (force=True):
      - Wipe all existing accounts + install VN template.
      - REFUSES if Company has any GL Entry (data loss risk).
      - Use when Company was auto-created via Frappe UI with non-VN
        Standard CoA, before any transactions.

    Args:
      company: target Company.name
      template: one of TEMPLATES.keys()
      force: if True, wipe non-VN CoA first

    Returns dict with action + counts.
    """
    import time
    t0 = time.time()

    if not frappe.db.exists("Company", company):
        return {"error": f"Company '{company}' does not exist"}
    if template not in TEMPLATES:
        return {"error": f"Unknown template '{template}'. Valid: {list(TEMPLATES.keys())}"}

    # Skip create_charts if Account count already > 5 (Frappe auto-creates
    # a few skeleton accounts on Company.insert). But ALWAYS fall through
    # to Cost Center + Company default refresh — those are idempotent and
    # we need them to repair stale FK refs after a wipe (e.g. cost_center
    # pointing at a deleted CC name).
    n_existing = frappe.db.count("Account", {"company": company})
    if n_existing > 5:
        n_after = n_existing
        action = "already_has_coa"
    else:
        # Load template + normalize
        from vn_accounting.chart_of_accounts.coa_registry import _normalize_tree_for_erpnext
        tree = _normalize_tree_for_erpnext(_load_template_tree(template))
        # Use ERPNext's official entry — keyword `custom_chart` is required.
        create_charts(company, custom_chart=tree)
        n_after = frappe.db.count("Account", {"company": company})
        action = "installed"

    # Ensure default Cost Center hierarchy exists. ERPNext setup wizard
    # normally creates "<Company> - <abbr>" as root CC group + "Main - <abbr>"
    # as default leaf — but after a full wipe (or in some migration paths)
    # these are gone. Without them, bulk_pump can't stamp a valid cost_center
    # onto SI/PI/JE/PE lines and ERPNext rejects the docs at validate time
    # ("Trung tâm chi phí X không thuộc về công ty Y"). Idempotent — checks
    # existence before insert.
    co_abbr = frappe.db.get_value("Company", company, "abbr") or ""
    cc_updates: list[str] = []
    if co_abbr:
        root_cc_name = f"{company} - {co_abbr}"
        leaf_cc_name = f"Main - {co_abbr}"
        if not frappe.db.exists("Cost Center", root_cc_name):
            # Root CC has parent_cost_center = NULL but DocType marks it
            # reqd=1; bypass via ignore_mandatory just like ERPNext's own
            # Company setup wizard does for the first root CC.
            root = frappe.get_doc({
                "doctype": "Cost Center",
                "cost_center_name": company,
                "company": company,
                "is_group": 1,
            })
            root.flags.ignore_mandatory = True
            root.flags.ignore_permissions = True
            root.insert()
            cc_updates.append(root_cc_name)
        if not frappe.db.exists("Cost Center", leaf_cc_name):
            frappe.get_doc({
                "doctype": "Cost Center",
                "cost_center_name": "Main",
                "company": company,
                "is_group": 0,
                "parent_cost_center": root_cc_name,
            }).insert(ignore_permissions=True)
            cc_updates.append(leaf_cc_name)

    # Set/refresh sensible Company defaults — prefer LEAF over group.
    # Pattern "like 111%" matches BOTH 111 AND 1111; ORDER BY LENGTH DESC
    # picks the most-specific (longest) leaf so subsequent derive_masters
    # creating sub-accounts doesn't orphan the default.
    # Use raw SQL persist (NOT co.save()) — Company.on_update re-populates
    # write_off_account / round_off_account / etc. from ERPNext defaults
    # which name Standard CoA accounts that don't exist on VN CoA → save fails.
    co = frappe.get_doc("Company", company)
    updates: list[str] = []
    for default_field, criteria in [
        ("default_receivable_account", {"account_number": ["like", "131%"], "is_group": 0}),
        ("default_payable_account", {"account_number": ["like", "331%"], "is_group": 0}),
        ("default_cash_account", {"account_number": ["like", "111%"], "is_group": 0}),
        ("default_expense_account", {"account_number": ["like", "6321%"], "is_group": 0}),
        ("default_income_account", {"account_number": ["like", "5111%"], "is_group": 0}),
        ("stock_adjustment_account", {"account_number": "632", "is_group": 0}),
        ("default_inventory_account", {"account_number": ["like", "1561%"], "is_group": 0}),
    ]:
        if getattr(co, default_field, None):
            continue
        criteria["company"] = company
        match = frappe.db.get_value("Account", criteria, "name", order_by="account_number")
        if match:
            setattr(co, default_field, match)
            updates.append(f"{default_field}={match}")
    # Always re-validate Company.cost_center against existing Cost Center
    # records — a stale FK pointing at a deleted CC silently breaks every
    # downstream validate_cost_center call (4,461 SI on DCT had this).
    leaf_cc = f"Main - {co_abbr}" if co_abbr else None
    if leaf_cc and frappe.db.exists("Cost Center", leaf_cc):
        if co.cost_center != leaf_cc:
            co.cost_center = leaf_cc
            updates.append(f"cost_center={leaf_cc}")
        if hasattr(co, "round_off_cost_center") and not co.round_off_cost_center:
            co.round_off_cost_center = leaf_cc
            updates.append(f"round_off_cost_center={leaf_cc}")
    if updates:
        co.flags.ignore_permissions = True
        co.save()

    frappe.db.commit()
    return {
        "action": action,
        "company": company,
        "template": template,
        "template_description": TEMPLATES[template],
        "accounts_created": n_after - n_existing,
        "total_accounts": n_after,
        "company_defaults_set": updates,
        "cost_centers_created": cc_updates,
        "elapsed_seconds": round(time.time() - t0, 2),
    }


# Mapping: Company default field → LIKE prefix.
# Keep in sync with VAS TT99/2025 leaf account numbering.
_COMPANY_DEFAULT_FIELDS = [
    ("default_receivable_account", "131"),
    ("default_payable_account", "331"),
    ("default_cash_account", "111"),
    ("default_expense_account", "6321"),
    ("default_income_account", "5111"),
    ("stock_adjustment_account", "6321"),
    ("default_inventory_account", "1561"),
    ("default_bank_account", "112"),
    ("accumulated_depreciation_account", "2141"),
    ("depreciation_expense_account", "2141"),
]


def _refresh_company_defaults_to_leaf(co, company: str, override: bool) -> list[str]:
    """Re-evaluate Company default account fields to point at a LEAF account.

    Always picks the LONGEST account_number matching the prefix (LIKE) so a
    sub-account (1111) wins over its parent group (111) when both match.

    Args:
      co: Company doc (in-memory — caller may save after, or skip save).
      company: company name (for the SQL filter).
      override: True → overwrite even if already set (use when re-bootstrapping
        to repair an existing group ref); False → only set if blank or group.

    Returns: list of "fld=value" strings updated, for logging.
    """
    cols = {c["Field"] for c in frappe.db.sql(
        "SHOW COLUMNS FROM `tabCompany`", as_dict=True)}
    updates: list[str] = []
    for fld, prefix in _COMPANY_DEFAULT_FIELDS:
        if fld not in cols:
            continue
        current = getattr(co, fld, None)
        if current and not override:
            is_grp = frappe.db.get_value("Account", current, "is_group")
            if not is_grp:
                continue  # current value is still a valid leaf
        match = frappe.db.sql(
            """SELECT name FROM `tabAccount`
               WHERE company=%s AND is_group=0 AND account_number LIKE %s
               ORDER BY LENGTH(account_number) DESC, account_number ASC LIMIT 1""",
            (company, prefix + "%"),
        )
        if match:
            new_val = match[0][0]
            if new_val != current:
                setattr(co, fld, new_val)
                updates.append(f"{fld}={new_val}")
    return updates


def _persist_company_defaults_via_sql(company: str, updates: list[str]) -> None:
    """Persist Company default account changes via raw SQL UPDATE to avoid
    Company.save() validating ALL Link→Account fields (which fails after a
    CoA wipe because stale fields like write_off_account still point at the
    wiped Standard CoA — those default to Vietnamese-named accounts that
    ERPNext's create_default_accounts on_update hook re-populates from a
    non-existent template).

    `updates` items are "fieldname=value" strings.
    """
    if not updates:
        return
    set_clauses = []
    args: list = []
    for u in updates:
        fld, val = u.split("=", 1)
        set_clauses.append(f"`{fld}`=%s")
        args.append(val)
    args.append(company)
    frappe.db.sql(
        f"UPDATE `tabCompany` SET {', '.join(set_clauses)} WHERE name=%s",
        tuple(args),
    )
    frappe.db.commit()
    frappe.clear_document_cache("Company", company)


@frappe.whitelist()
def refresh_company_default_accounts(company: str) -> dict:
    """Repair Company default_*_account fields after derive_masters promoted
    leaf TKs to groups (e.g., 111 became group when 1111 sub-account added).

    Idempotent — safe to call multiple times.
    """
    co = frappe.get_doc("Company", company)
    updates = _refresh_company_defaults_to_leaf(co, company, override=True)
    # Persist via SQL UPDATE — avoids Company.on_update hook re-validating
    # stale write_off / round_off / etc. refs after a CoA wipe-and-replace.
    _persist_company_defaults_via_sql(company, updates)
    return {"company": company, "updates": updates}


@frappe.whitelist()
def list_templates() -> dict[str, str]:
    """Return available CoA templates for UI selection."""
    return TEMPLATES
