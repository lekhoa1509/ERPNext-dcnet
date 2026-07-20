from __future__ import annotations

from collections.abc import Iterable, Mapping
from typing import Any

import frappe
from frappe import _

WORKSPACE_SIDEBAR_NAME = "Ke Toan VN"
BRANCH_MENU_ACCESS_DOCTYPE = "VN Accounting Branch Menu Access"
BRANCH_MENU_MANAGER_ROLES = {"System Manager", "Accounts Manager"}


def is_branch_menu_manager(user: str | None = None) -> bool:
    user = user or frappe.session.user
    if user == "Administrator":
        return True
    return bool(BRANCH_MENU_MANAGER_ROLES.intersection(set(frappe.get_roles(user))))


def get_user_branch(user: str | None = None) -> str | None:
    user = user or frappe.session.user
    if not user or not frappe.db.has_column("User", "branch"):
        return None

    return frappe.db.get_value("User", user, "branch")


def build_sidebar_item_key(item: Mapping[str, Any]) -> str:
    parts = [
        item.get("type") or "",
        item.get("link_type") or "",
        item.get("link_to") or "",
        item.get("route_options") or "",
        item.get("filters") or "",
        item.get("tab") or "",
        item.get("url") or "",
    ]
    return " | ".join(str(part).strip() for part in parts)


def get_sidebar_item_catalog(sidebar_name: str = WORKSPACE_SIDEBAR_NAME) -> list[dict[str, Any]]:
    if not frappe.db.exists("Workspace Sidebar", sidebar_name):
        return []

    sidebar_doc = frappe.get_doc("Workspace Sidebar", sidebar_name)
    current_section = _("Tổng quan")
    catalog: list[dict[str, Any]] = []

    for item in sidebar_doc.items:
        if item.type == "Section Break":
            current_section = item.label or _("Khác")
            continue

        if item.type != "Link":
            continue

        item_dict = item.as_dict()
        catalog.append(
            {
                "section_label": current_section,
                "item_label": item.label,
                "link_type": item.link_type,
                "link_to": item.link_to,
                "sidebar_item_key": build_sidebar_item_key(item_dict),
            }
        )

    return catalog


def get_allowed_sidebar_item_keys(user: str | None = None) -> set[str] | None:
    user = user or frappe.session.user
    if is_branch_menu_manager(user):
        return None

    if not frappe.db.exists("DocType", BRANCH_MENU_ACCESS_DOCTYPE):
        return None

    branch = get_user_branch(user)
    if not branch or not frappe.db.exists(BRANCH_MENU_ACCESS_DOCTYPE, branch):
        return None

    access_doc = frappe.get_cached_doc(BRANCH_MENU_ACCESS_DOCTYPE, branch)
    if not access_doc.is_active or not access_doc.restrict_sidebar_items:
        return None

    return {
        row.sidebar_item_key
        for row in access_doc.menu_items or []
        if row.sidebar_item_key and row.is_allowed
    }


def filter_sidebar_items(
    items: Iterable[Mapping[str, Any]],
    allowed_keys: set[str] | None,
) -> list[dict[str, Any]]:
    items = [dict(item) for item in items]
    if allowed_keys is None:
        return items

    filtered: list[dict[str, Any]] = []
    current_section: dict[str, Any] | None = None
    current_children: list[dict[str, Any]] = []

    def flush_section() -> None:
        nonlocal current_section, current_children
        if not current_section:
            return

        allowed_children = [
            child
            for child in current_children
            if child.get("type") != "Link" or build_sidebar_item_key(child) in allowed_keys
        ]
        if allowed_children:
            filtered.append(current_section)
            filtered.extend(allowed_children)

        current_section = None
        current_children = []

    for item in items:
        if item.get("type") == "Section Break":
            flush_section()
            current_section = item
            current_children = []
            continue

        if current_section and item.get("child"):
            current_children.append(item)
            continue

        flush_section()
        if item.get("type") != "Link" or build_sidebar_item_key(item) in allowed_keys:
            filtered.append(item)

    flush_section()
    return filtered


def apply_branch_sidebar_item_access(bootinfo) -> None:
    sidebar_map = bootinfo.get("workspace_sidebar_item") or {}
    sidebar_key = WORKSPACE_SIDEBAR_NAME.lower()
    sidebar = sidebar_map.get(sidebar_key)
    if not sidebar:
        return

    allowed_keys = get_allowed_sidebar_item_keys()
    sidebar["items"] = filter_sidebar_items(sidebar.get("items", []), allowed_keys)
    sidebar_map[sidebar_key] = sidebar
    bootinfo["workspace_sidebar_item"] = sidebar_map
