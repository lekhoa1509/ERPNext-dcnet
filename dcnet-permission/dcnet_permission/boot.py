import frappe


def boot_session(bootinfo):
    """Add module-gating metadata and filter boot desktop icons."""
    blocked_modules = _get_blocked_modules(frappe.session.user)
    bootinfo["dcnet_permission_blocked_modules"] = sorted(blocked_modules)

    if not blocked_modules:
        return

    icon_modules = _get_desktop_icon_modules()
    bootinfo["dcnet_permission_desktop_icon_modules"] = icon_modules

    if bootinfo.get("desktop_icons"):
        bootinfo["desktop_icons"] = [
            icon
            for icon in bootinfo["desktop_icons"]
            if not _is_icon_blocked(icon, blocked_modules, icon_modules)
        ]


def _get_blocked_modules(user):
    if user == "Administrator":
        return set()

    try:
        user_doc = frappe.get_cached_doc("User", user)
        return set(user_doc.get_blocked_modules() or [])
    except Exception:
        return set()


def _get_desktop_icon_modules():
    sidebar_modules = _get_workspace_sidebar_modules()
    workspace_modules = _get_workspace_modules()
    icon_modules = {}

    rows = frappe.get_all(
        "Desktop Icon",
        fields=["name", "label", "link", "link_type", "link_to"],
    )

    for row in rows:
        module = _resolve_icon_module(row, sidebar_modules, workspace_modules)
        if not module:
            continue

        for key in (row.name, row.label, row.link_to, row.link):
            if key:
                icon_modules[key] = module

    return icon_modules


def _get_workspace_sidebar_modules():
    rows = frappe.get_all("Workspace Sidebar", fields=["name", "title", "module"])
    modules = {}
    for row in rows:
        if not row.module:
            continue
        modules[row.name] = row.module
        if row.title:
            modules[row.title] = row.module
    return modules


def _get_workspace_modules():
    rows = frappe.get_all("Workspace", fields=["name", "label", "module"])
    modules = {}
    for row in rows:
        if not row.module:
            continue
        modules[row.name] = row.module
        if row.label:
            modules[row.label] = row.module
    return modules


def _resolve_icon_module(icon, sidebar_modules, workspace_modules):
    candidates = [icon.get("link_to"), icon.get("link"), icon.get("label"), icon.get("name")]

    if icon.get("link_type") == "Workspace Sidebar":
        return _first_mapping_match(candidates, sidebar_modules)
    if icon.get("link_type") == "Workspace":
        return _first_mapping_match(candidates, workspace_modules)

    return None


def _first_mapping_match(candidates, mapping):
    for candidate in candidates:
        if candidate and candidate in mapping:
            return mapping[candidate]
    return None


def _is_icon_blocked(icon, blocked_modules, icon_modules):
    for key in (icon.get("name"), icon.get("label"), icon.get("link_to"), icon.get("link")):
        if key and icon_modules.get(key) in blocked_modules:
            return True
    return False
