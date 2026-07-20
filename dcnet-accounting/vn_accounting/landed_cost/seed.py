from __future__ import annotations

import frappe

# 12 default expense types per TT99/2025 practice.
# "Stock account" entries have no default_expense_account here — account is
# resolved at LCV time from the item's inventory account (per-Company).
_DEFAULT_EXPENSE_TYPES = [
    {
        "expense_type_key": "shipping",
        "expense_type": "Vận chuyển",
        "default_expense_account": "",
        "is_import_only": 0,
        "allocation_method": "Weight",
    },
    {
        "expense_type_key": "handling",
        "expense_type": "Bốc xếp",
        "default_expense_account": "",
        "is_import_only": 0,
        "allocation_method": "Amount",
    },
    {
        "expense_type_key": "insurance",
        "expense_type": "Bảo hiểm hàng hóa",
        "default_expense_account": "",
        "is_import_only": 0,
        "allocation_method": "Amount",
    },
    {
        "expense_type_key": "storage",
        "expense_type": "Lưu kho, lưu bãi",
        "default_expense_account": "",
        "is_import_only": 0,
        "allocation_method": "Amount",
    },
    {
        "expense_type_key": "commission",
        "expense_type": "Hoa hồng mua hàng",
        "default_expense_account": "",
        "is_import_only": 0,
        "allocation_method": "Amount",
    },
    {
        "expense_type_key": "import_duty",
        "expense_type": "Thuế nhập khẩu",
        "default_expense_account": "",   # TK 3333 — resolved per-company at seed time
        "is_import_only": 1,
        "allocation_method": "Amount",
    },
    {
        "expense_type_key": "special_consumption_tax",
        "expense_type": "Thuế tiêu thụ đặc biệt nhập khẩu",
        "default_expense_account": "",   # TK 3332 — resolved per-company at seed time
        "is_import_only": 1,
        "allocation_method": "Amount",
    },
    # NOTE: "VAT NK khấu trừ" was intentionally removed from LCV expense types.
    # LCV mechanism always capitalizes (Dr inventory / Cr expense_account) — but
    # per VAS, VAT NK khấu trừ does NOT belong in inventory cost; it's an offset
    # to VAT payable: Dr 1331 / Cr 33312. KTT creates that JE separately via
    # the "Tạo phiếu VAT NK khấu trừ" button on the LCV form.
    {
        "expense_type_key": "import_vat_non_deductible",
        "expense_type": "VAT nhập khẩu (không khấu trừ)",
        "default_expense_account": "",
        "is_import_only": 1,
        "allocation_method": "Amount",
    },
    {
        "expense_type_key": "customs_fee",
        "expense_type": "Phí hải quan, kiểm dịch",
        "default_expense_account": "",
        "is_import_only": 1,
        "allocation_method": "Amount",
    },
    {
        "expense_type_key": "container_demurrage",
        "expense_type": "Phí lưu cont, lưu bãi",
        "default_expense_account": "",
        "is_import_only": 1,
        "allocation_method": "Amount",
    },
    {
        "expense_type_key": "customs_agent_fee",
        "expense_type": "Phí đại lý hải quan",
        "default_expense_account": "",
        "is_import_only": 1,
        "allocation_method": "Amount",
    },
]


def seed_lcv_allocation_settings():
    """Seed LCV Allocation Settings with 12 default expense types + backfill
    the inventory-split flags introduced for VAS TT99/2025 (FB-2026-00836).

    Two responsibilities:
    1. First-time install: populate expense_types table.
    2. Idempotent backfill: ensure auto_create_inventory_split_je = 1 if the
       field has never been set (existing Single docs created before the field
       existed don't auto-pick up the field's default).
    """
    settings = frappe.get_single("LCV Allocation Settings")

    dirty = False
    if not settings.expense_types:
        for row_data in _DEFAULT_EXPENSE_TYPES:
            settings.append("expense_types", row_data)
        dirty = True

    # Backfill: existing Single docs created before VAS TT99/2025 fields were
    # added don't have auto_create_inventory_split_je set; default it ON to
    # match the field-level default.
    if not settings.get("auto_create_inventory_split_je"):
        # Use db.set_value to bypass validation on Single — the value can stay
        # null only because the column existed before the field had a default.
        frappe.db.set_value(
            "LCV Allocation Settings",
            "LCV Allocation Settings",
            "auto_create_inventory_split_je",
            1,
            update_modified=False,
        )

    if dirty:
        settings.flags.ignore_validate = True
        settings.save(ignore_permissions=True)
    frappe.db.commit()


# Mapping: expense_type_key → TT99/2025 account number to look up in COA.
# All non-tax service costs default to 331 (Phải trả người bán) — the vendor
# payable. Tax-specific rows map to their tax payable accounts.
_KEY_TO_ACCOUNT_NUMBER = {
    "shipping": "331",
    "handling": "331",
    "insurance": "331",
    "storage": "331",
    "commission": "331",
    "import_duty": "3333",
    "special_consumption_tax": "3332",
    # import_vat_deductible removed — handled via separate JE button on LCV form
    "import_vat_non_deductible": "33312",
    "customs_fee": "331",
    "container_demurrage": "331",
    "customs_agent_fee": "331",
}


def resolve_default_accounts(company: str | None = None, overwrite: bool = False) -> dict:
    """Fill default_expense_account on each LCV Expense Type Setting row.

    Looks up each TT99/2025 account number in the COA (filtered by Company), and
    sets it on the matching row in LCV Allocation Settings.

    Args:
        company: Company name to source accounts from. If None, picks the first
                 Vietnam Company found (single-Company deployments — typical
                 dcnet/das clients).
        overwrite: if False, only fills rows where default_expense_account is empty.

    Returns:
        Dict summarizing what was set/skipped per key.

    Note: LCV Allocation Settings is a Singleton, so accounts are tied to ONE
    Company. Multi-Company deployments should refactor to per-Company settings.
    """
    if not company:
        # Prefer Vietnam Companies first
        company = frappe.db.get_value(
            "Company", {"country": "Vietnam"}, "name", order_by="creation"
        )
        if not company:
            company = frappe.db.get_value("Company", {}, "name", order_by="creation")
    if not company:
        return {"error": "No Company found in DB; cannot resolve accounts."}

    settings = frappe.get_single("LCV Allocation Settings")
    result = {"company": company, "set": {}, "skipped": {}, "missing": {}}

    for row in settings.expense_types or []:
        key = row.expense_type_key
        account_num = _KEY_TO_ACCOUNT_NUMBER.get(key)
        if not account_num:
            continue
        if row.default_expense_account and not overwrite:
            result["skipped"][key] = row.default_expense_account
            continue
        account_name = frappe.db.get_value(
            "Account",
            {"account_number": account_num, "company": company, "is_group": 0},
            "name",
        )
        if account_name:
            row.default_expense_account = account_name
            result["set"][key] = account_name
        else:
            result["missing"][key] = f"No account with number {account_num} found in {company}"

    settings.flags.ignore_validate = True
    settings.save(ignore_permissions=True)
    frappe.db.commit()
    return result
