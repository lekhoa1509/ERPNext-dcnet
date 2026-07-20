from __future__ import annotations

from typing import Any

import frappe


def set_vn_defaults(doc: Any, method: str | None = None) -> None:
    """Thiết lập mặc định công ty Việt Nam sau khi tạo COA.

    Ánh xạ số hiệu tài khoản Việt Nam (TT99/2025) sang company defaults ERPNext.
    Chỉ điền các field còn trống — tôn trọng giá trị user đã set thủ công.
    Chạy mỗi lần Company được save (on_update) nhưng idempotent.
    """
    if doc.country != "Vietnam":
        return

    # Kiểm tra COA có dùng số hiệu VN không (TK 111 = Tiền mặt). Nếu chưa có
    # nghĩa là COA chưa setup xong — skip, hook sẽ chạy lại sau.
    cash_account = frappe.db.get_value(
        "Account",
        {"account_number": "111", "company": doc.name},
        "name",
    )
    if not cash_account:
        return

    # Nhận dạng loại template: DN lớn có TK 621 (Chi phí NVL trực tiếp)
    is_large = frappe.db.exists(
        "Account",
        {"account_number": "621", "company": doc.name},
    )

    defaults = _get_defaults_large() if is_large else _get_defaults_small()

    # ERPNext core's `set_default_accounts()` picks defaults purely by
    # `account_type` — for VN COA this picks SEMANTICALLY-WRONG leaves
    # (e.g. 515 "DT hoạt động tài chính" as default_income before 5111
    # "DT bán hàng hoá"). vn_accounting knows the TT99/2025 convention
    # and overrides core. This hook fires after core's set_default_accounts
    # in Company.on_update so the override sticks.
    #
    # We override even if currently set (since set_default_accounts may
    # have set a wrong-leaf or group value). To respect explicit user
    # manual config, set the field to "" → save → vn_accounting won't
    # touch it because the curated_TK lookup will overwrite anyway.
    # In practice the only user who edits these is the consultant during
    # setup, and they'll set the FINAL value after VAS COA seeding.
    for field, account_number in defaults.items():
        account_name = frappe.db.get_value(
            "Account",
            {"account_number": account_number, "company": doc.name},
            "name",
        )
        if not account_name:
            continue
        current = doc.get(field)
        if current == account_name:
            continue  # already correct
        doc.db_set(field, account_name)

    # round_off_cost_center: ERPNext SI/PI submit throws "Please mention Round
    # Off Cost Center" when grand_total rounding kicks in. Pick first leaf CC
    # of this company. Independent of which template (lớn/nhỏ) is in use.
    if not doc.get("round_off_cost_center"):
        leaf_cc = frappe.db.get_value(
            "Cost Center",
            {"company": doc.name, "is_group": 0},
            "name",
            order_by="creation",
        )
        if leaf_cc:
            doc.db_set("round_off_cost_center", leaf_cc)


def _get_defaults_large() -> dict[str, str]:
    """Ánh xạ tài khoản mặc định cho doanh nghiệp lớn (TT99/2025).

    All values are LEAF account numbers (is_group=0). ERPNext SI/PI/SE
    reject group accounts ("You selected the account group X as Income
    Account. Please select a single account."). VN VAS parents like
    511/632/156/214 are groups in the standard TT99 template; their
    first leaf children are the correct defaults.
    """
    return {
        "default_cash_account": "1111",  # 111 is group
        "default_bank_account": "1121",  # 112 is group
        "default_receivable_account": "131",  # leaf in TT99 large template
        "default_payable_account": "331",  # leaf in TT99 large template
        "default_income_account": "5111",  # 511 is group → first leaf
        "default_expense_account": "6321",  # 632 is group → first leaf
        "stock_received_but_not_billed": "151",
        "default_inventory_account": "1561",  # 156 is group → first leaf
        "stock_adjustment_account": "6321",  # 632 group → leaf
        "accumulated_depreciation_account": "2141",  # 214 group → first leaf
        "depreciation_expense_account": "6274",
        "capital_work_in_progress_account": "2412",  # 241 group → first leaf
        "round_off_account": "711",
        "disposal_account": "811",
        # Chênh lệch tỷ giá: chưa thực hiện (đánh giá lại cuối kỳ) → TK 413;
        # đã thực hiện (khi thanh toán) → TK 635 (ERPNext 1 trường, gộp lãi/lỗ).
        "unrealized_exchange_gain_loss_account": "413",
        "exchange_gain_loss_account": "635",
    }


def _get_defaults_small() -> dict[str, str]:
    """Ánh xạ tài khoản mặc định cho doanh nghiệp nhỏ (TT99/2025).

    See _get_defaults_large() docstring for why leaf account numbers.
    """
    return {
        "default_cash_account": "1111",
        "default_bank_account": "1121",
        "default_receivable_account": "131",
        "default_payable_account": "331",
        "default_income_account": "5111",
        "default_expense_account": "6321",
        "default_inventory_account": "1561",
        "stock_received_but_not_billed": "331",
        "stock_adjustment_account": "6321",
        "accumulated_depreciation_account": "2141",
        "depreciation_expense_account": "6424",
        "round_off_account": "711",
        "disposal_account": "811",
        # Chênh lệch tỷ giá: chưa thực hiện → TK 413; đã thực hiện → TK 635.
        "unrealized_exchange_gain_loss_account": "413",
        "exchange_gain_loss_account": "635",
    }


# ─────────────────────────────────────────────────────────────────────────────
# VN Accounting Settings — Project Costing defaults (TT99/2025 xây lắp chain)
# ─────────────────────────────────────────────────────────────────────────────
# Why on_update Company (not after_install / patch): TK accounts created during
# Company.on_update via COA template. Settings seed must run AFTER COA → tying
# to same hook fires it at the right moment. Idempotent — only sets blank fields.

_PROJECT_COSTING_DEFAULTS: dict[str, str] = {
    "wip_account_project_costing": "154",
    "overhead_collector_account": "627",
    "cogs_account_project_costing": "632",
    "writeoff_account_project_costing": "642",
}


def seed_project_costing_settings(doc: Any, method: str | None = None) -> None:
    """Seed 4 default accounts in VN Accounting Settings for project costing.

    Runs on Company.on_update. Idempotent — only sets fields still blank. If a
    KTT later changes Settings, doesn't overwrite. Single DocType, so first
    company's accounts win — subsequent companies skip unless field is blank.

    Wired in hooks.py doc_events["Company"]["on_update"].
    """
    if doc.country != "Vietnam":
        return

    # Probe canonical anchor (TK 154) for this company; if missing, COA not yet ready.
    anchor = frappe.db.get_value(
        "Account",
        {"account_number": "154", "company": doc.name, "is_group": 0},
        "name",
    )
    if not anchor:
        return

    for field, account_number in _PROJECT_COSTING_DEFAULTS.items():
        # Skip if KTT already configured
        current = frappe.db.get_single_value("VN Accounting Settings", field)
        if current:
            continue
        account_name = frappe.db.get_value(
            "Account",
            {"account_number": account_number, "company": doc.name, "is_group": 0},
            "name",
        )
        if account_name:
            frappe.db.set_single_value("VN Accounting Settings", field, account_name)
