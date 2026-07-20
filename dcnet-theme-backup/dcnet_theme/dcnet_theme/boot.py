"""DCNET Theme boot session hook — injects theme CSS into bootinfo.

The CSS is injected via bootinfo instead of app_include_css because
/files/ URLs have no cache-busting mechanism in Frappe. Since bootinfo
is fetched fresh on every page load (not HTTP-cached), the theme CSS
is always up-to-date after a theme switch.

The client-side theme_applicator.js reads bootinfo.dcnet_theme_css
and injects it as a <style> tag in <head>.

Per-company override: if company_theme_overrides is configured and the
current user's default company matches an entry, that company's preset
is used instead of the global active_preset.
"""

import json
import frappe


def boot_session(bootinfo):
    """Inject DCNET Theme CSS into bootinfo for client-side application.

    Also injects company_theme_overrides map so theme_applicator.js can
    swap themes when the user switches company context.

    Enriches desktop_icons with custom_label so theme_applicator.js can
    override the displayed icon title without modifying core templates.

    Also emits sidebar-routing bootinfo (merged from dcnet_sidebar_routing
    v0.3.0): user_allowed_modules + workspace_sidebar_modules — consumed
    by sidebar.bundle.js for context-primary workspace selection.
    """
    preset_key = _resolve_preset_for_user()
    if preset_key:
        css = _get_cached_css(preset_key)
        if css:
            bootinfo["dcnet_theme_css"] = css
            bootinfo["dcnet_theme_preset"] = preset_key

    # Send the overrides map to client so theme_applicator.js can handle
    # company switches without a full page reload.
    overrides = _get_company_overrides()
    if overrides:
        bootinfo["dcnet_theme_company_overrides"] = overrides

    # Enrich desktop_icons list with custom_label field (not in core field list).
    _inject_custom_labels(bootinfo)

    # Sidebar routing bootinfo (merged from dcnet_sidebar_routing v0.3.0)
    bootinfo["user_allowed_modules"] = get_allowed_modules(frappe.session.user)
    bootinfo["workspace_sidebar_modules"] = _get_workspace_sidebar_modules()

    # Quick Detail Frame (spec docs/specs/2026-05-13-quick-detail-frame-design.md)
    try:
        from dcnet_theme.dcnet_theme.api.quick_detail import get_boot_payload
        bootinfo["dcnet_qdf"] = get_boot_payload()
    except Exception:
        # Never let QDF boot enrichment crash the boot session
        pass


def get_allowed_modules(user):
    """Modules user can access = all modules - User.block_modules.

    Administrator bypasses block_modules.
    """
    all_modules = [m.name for m in frappe.get_all("Module Def", fields=["name"])]
    if user == "Administrator":
        return all_modules

    try:
        user_doc = frappe.get_doc("User", user)
        blocked = {b.module for b in (user_doc.block_modules or []) if getattr(b, "module", None)}
    except Exception:
        blocked = set()

    return [m for m in all_modules if m not in blocked]


def _get_workspace_sidebar_modules():
    """Map of {sidebar_name: module} for JS module filtering."""
    rows = frappe.get_all("Workspace Sidebar", fields=["name", "module"])
    return {r.name: r.module for r in rows if r.module}


def _inject_custom_labels(bootinfo):
    """Add custom_label / icon_color values into the desktop_icons boot list.

    These are custom fields added by dcnet_theme fixtures. On a fresh install
    before `bench migrate` runs they may not exist yet — all errors are silently
    swallowed so boot never breaks on another developer's machine.
    """
    try:
        icons = bootinfo.get("desktop_icons")
        if not icons:
            return

        names = [i.get("name") for i in icons if i.get("name")]
        if not names:
            return

        # Try fetching both custom fields; fall back gracefully if either is absent.
        try:
            rows = frappe.db.get_all(
                "Desktop Icon",
                filters={"name": ["in", names]},
                fields=["name", "custom_label", "icon_color"],
            )
            has_icon_color = True
        except Exception:
            try:
                rows = frappe.db.get_all(
                    "Desktop Icon",
                    filters={"name": ["in", names]},
                    fields=["name", "custom_label"],
                )
                has_icon_color = False
            except Exception:
                # custom_label field also missing — nothing to inject
                return

        custom_map = {r.name: r for r in rows}

        for icon in icons:
            row = custom_map.get(icon.get("name"))
            if not row:
                continue
            if row.get("custom_label"):
                icon["custom_label"] = row.custom_label
            if has_icon_color and row.get("icon_color"):
                icon["icon_color"] = row.icon_color

    except Exception:
        # Never let boot enrichment crash the boot session
        pass


def _resolve_preset_for_user():
    """Determine which preset to use for the current user.

    1. Check company_theme_overrides for user's default company
    2. Fall back to global active_presetbg
    """
    try:
        if not frappe.db.exists("DocType", "DCNET Theme Settings"):
            return None

        active_preset = frappe.db.get_single_value(
            "DCNET Theme Settings", "active_preset"
        )

        # Check per-company override
        overrides = _get_company_overrides()
        if overrides:
            user_company = frappe.defaults.get_user_default("Company")
            if user_company and user_company in overrides:
                override_preset = overrides[user_company]
                # Verify the preset exists
                if frappe.db.exists("DCNET Theme Preset", override_preset):
                    return override_preset

        return active_preset
    except Exception:
        return None


def _get_company_overrides():
    """Parse company_theme_overrides JSON from settings. Returns dict or None."""
    try:
        raw = frappe.db.get_single_value(
            "DCNET Theme Settings", "company_theme_overrides"
        )
        if not raw:
            return None
        overrides = json.loads(raw)
        if isinstance(overrides, dict) and overrides:
            return overrides
        return None
    except (json.JSONDecodeError, Exception):
        return None


def _get_cached_css(preset_key):
    """Get theme CSS from Redis cache, regenerating if needed.

    Cache key includes the preset_key so different presets are cached separately.
    """
    cache_key = f"dcnet_theme_css:{preset_key}"
    css = frappe.cache.get_value(cache_key)

    if css is None:
        css = _regenerate_css(preset_key)
        if css:
            frappe.cache.set_value(cache_key, css)

    return css


def _regenerate_css(preset_key):
    """Regenerate CSS for a specific preset."""
    try:
        if not preset_key:
            return None

        if not frappe.db.exists("DCNET Theme Preset", preset_key):
            return None

        from dcnet_theme.dcnet_theme.theme_utils import generate_theme_css

        preset_doc = frappe.get_doc("DCNET Theme Preset", preset_key)
        settings_doc = frappe.get_single("DCNET Theme Settings")
        return generate_theme_css(preset_doc, settings_doc)
    except Exception:
        return None


@frappe.whitelist()
def get_theme_css():
    """Return fresh CSS for the current user's active preset.

    Called by theme_applicator.js on 'dcnet_theme_updated' realtime event
    so the browser can hot-reload CSS without a full page refresh.
    """
    preset_key = _resolve_preset_for_user()
    if not preset_key:
        return ""
    # Bypass cache — preset was just saved, we want fresh CSS
    css = _regenerate_css(preset_key)
    if css:
        # Update cache with fresh CSS
        frappe.cache.set_value(f"dcnet_theme_css:{preset_key}", css)
    return css or ""


@frappe.whitelist()
def refresh_desktop_icons():
    """Return fresh desktop icon data for the current user.

    Called by Desktop Icon form after_save to sync client-side boot data
    without requiring a full page reload.

    Clears the user's Redis cache so the next bootinfo fetch gets fresh data,
    then returns the full icon list (including custom_label) direct from DB.
    """
    frappe.cache.hdel("desktop_icons", frappe.session.user)
    frappe.cache.hdel("bootinfo", frappe.session.user)

    icons = frappe.db.sql(
        """
        SELECT name, label, bg_color, `link`, link_type, app, icon_type,
               parent_icon, icon, link_to, idx, standard, logo_url,
               hidden, restrict_removal, icon_image, custom_label, icon_color
        FROM `tabDesktop Icon`
        WHERE hidden = 0
          AND (standard = 1 OR owner IN ('Administrator', %s))
        ORDER BY idx ASC
        """,
        (frappe.session.user,),
        as_dict=True,
    )
    return icons


@frappe.whitelist()
def get_theme_css_for_company(company):
    """Return theme CSS for a specific company (called client-side on company switch).

    This is a whitelisted API so theme_applicator.js can fetch CSS for a
    different company without a full page reload.
    """
    if not company:
        frappe.throw("Company is required")

    overrides = _get_company_overrides()
    preset_key = None

    if overrides and company in overrides:
        preset_key = overrides[company]
    else:
        # Fall back to global preset
        preset_key = frappe.db.get_single_value(
            "DCNET Theme Settings", "active_preset"
        )

    if not preset_key:
        return {"css": "", "preset_key": ""}

    css = _get_cached_css(preset_key)
    return {"css": css or "", "preset_key": preset_key}
