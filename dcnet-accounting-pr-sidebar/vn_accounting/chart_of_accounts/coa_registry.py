from __future__ import annotations

import json
import os
from typing import Any

import frappe
from erpnext.accounts.doctype.account.chart_of_accounts.chart_of_accounts import (
    get_chart as _original_get_chart,
    get_charts_for_country as _original_get_charts,
)

# Cache VN templates loaded from JSON files
_vn_templates: dict[str, Any] | None = None


def _load_vn_templates() -> dict[str, Any]:
    """Load VN COA templates from JSON files in this directory."""
    global _vn_templates
    if _vn_templates is not None:
        return _vn_templates

    _vn_templates = {}
    charts_dir = os.path.dirname(__file__)
    for fname in sorted(os.listdir(charts_dir)):
        if fname.endswith(".json"):
            with open(os.path.join(charts_dir, fname)) as f:
                content = json.load(f)
                name = content.get("name")
                if name:
                    _vn_templates[name] = content
    return _vn_templates


def _normalize_tree_for_erpnext(node: Any) -> Any:
    """Strip duplicated account-number prefixes from VN COA keys.

    ERPNext expects the dict key to be the account name only and reads
    ``account_number`` from the node payload. Our VN templates store keys like
    ``111 - Tiền mặt`` together with ``account_number = 111``. If we return the
    raw tree, ERPNext prefixes the account number again and creates names such as
    ``111 - 111 - Tiền mặt - VAP``.
    """
    if not isinstance(node, dict):
        return node

    normalized: dict[str, Any] = {}
    for key, value in node.items():
        normalized_key = key
        if isinstance(value, dict):
            account_number = str(value.get("account_number") or "").strip()
            prefix = f"{account_number} - "
            if account_number and key.startswith(prefix):
                normalized_key = key[len(prefix):].strip()

        normalized[normalized_key] = _normalize_tree_for_erpnext(value)

    return normalized


@frappe.whitelist()
def get_charts_for_country(country: str, with_standard: bool = False) -> list[str]:
    """Trả về danh sách COA templates cho Company creation flow.

    Gọi hàm gốc của ERPNext trước, sau đó thêm templates Việt Nam
    nếu country = 'Vietnam'.
    """
    charts = _original_get_charts(country, with_standard)

    if country == "Vietnam":
        templates = _load_vn_templates()
        for name in templates:
            if name not in charts:
                charts.insert(0, name)

    return charts


def get_chart(chart_template: str, existing_company: str | None = None) -> dict[str, Any] | None:
    """Override get_chart để tìm templates VN trước, fallback về ERPNext."""
    templates = _load_vn_templates()
    if chart_template in templates:
        return _normalize_tree_for_erpnext(templates[chart_template].get("tree"))

    return _original_get_chart(chart_template, existing_company)
