from __future__ import annotations

import frappe


def seed_period_closing_account_settings() -> None:
    """Seed VN Accounting Settings period-closing fields with TT99/2025 defaults.
    Idempotent: only seeds if pnl_account_911 is empty.
    """
    settings = frappe.get_single("VN Accounting Settings")
    if settings.pnl_account_911:
        return  # already configured

    company = _get_vn_company()
    if not company:
        return

    # Seed single-account fields
    account_map = {
        "pnl_account_911": "911",
        "retained_earnings_current_year": "4212",
        "retained_earnings_prior_year": "4211",
        "corporate_income_tax_account": "821",
    }
    for field, prefix in account_map.items():
        account = _lookup_account_by_prefix(company, prefix)
        if account:
            settings.set(field, account)

    # Seed revenue accounts (511, 512, 515, 711)
    revenue_prefixes = ["511", "512", "515", "711"]
    if not settings.revenue_accounts_to_close:
        for prefix in revenue_prefixes:
            account = _lookup_account_by_prefix(company, prefix)
            if account:
                settings.append("revenue_accounts_to_close", {"account": account})

    # Seed periodic expense accounts (632, 635, 641, 642, 811) — excludes 821
    expense_prefixes = ["632", "635", "641", "642", "811"]
    if not settings.expense_accounts_to_close_periodic:
        for prefix in expense_prefixes:
            account = _lookup_account_by_prefix(company, prefix)
            if account:
                settings.append("expense_accounts_to_close_periodic", {"account": account})

    # ignore_links flag (NOT a save() kwarg — that kwarg doesn't exist on frappe
    # version-16's Document._save and raises TypeError). VN Accounting Settings is a
    # Single shared with the project-costing seed (setup/company_defaults.py); its
    # "first company wins" logic can leave a dangling Account link (e.g.
    # wip_account_project_costing pointing at a company whose COA was later removed),
    # which would make _validate_links() throw here and abort the whole after_migrate
    # — blocking migrate for EVERY app on the site. This seed only writes accounts it
    # verified exist (guarded by `if account`), so skipping link validation loses
    # nothing. The clear_dangling_settings_account_links patch heals the stored value.
    settings.flags.ignore_validate = True
    settings.flags.ignore_links = True
    settings.save(ignore_permissions=True)
    frappe.db.commit()


def _get_vn_company() -> str | None:
    company = frappe.defaults.get_defaults().get("company")
    if company:
        return company
    companies = frappe.get_all("Company", filters={"country": "Vietnam"}, limit=1)
    return companies[0].name if companies else None


def _lookup_account_by_prefix(company: str, prefix: str) -> str | None:
    # fallback default TT99/2025
    return frappe.db.get_value(
        "Account",
        {
            "account_number": ["like", f"{prefix}%"],
            "company": company,
            "is_group": 0,
        },
        "name",
    )
