"""DCNET Theme CSS generation engine — converts preset data to CSS file."""

import json
import math
import frappe

# Component → CSS selector mapping (data-driven, all in one place)
# NOTE: Selectors must be specific enough to override dcnet_theme.css which uses
# .body-sidebar .standard-sidebar-item with !important. We use equally specific
# selectors + !important where needed to win the cascade.
COMPONENT_SELECTORS = {
    "sidebar": {
        # Target only the LEFT sidebar (not .layout-side-section.right which is the form sidebar)
        # "bg": (".layout-side-section:not(.right)", "background"),
        "text": (".body-sidebar-top .standard-sidebar-item .item-anchor", "color !important"),
        "active_bg": (
            ".body-sidebar-top .standard-sidebar-item.selected,"
            " .body-sidebar-top .standard-sidebar-item.active-sidebar",
            "background !important",
        ),
        "active_text": (
            ".body-sidebar-top .standard-sidebar-item.selected .item-anchor,"
            " .body-sidebar-top .standard-sidebar-item.active-sidebar .item-anchor",
            "color !important"
        ),
        "active_icon_stroke": (
            ".body-sidebar-top .standard-sidebar-item.selected .item-anchor svg,"
            " .body-sidebar-top .standard-sidebar-item.active-sidebar .item-anchor svg",
            "stroke !important"
        ),
        "hover_bg": (".body-sidebar-top .standard-sidebar-item:hover", "background !important"),
        "hover_text": (".body-sidebar-top .standard-sidebar-item:hover .item-anchor", "color !important"),
        "border_radius": (".body-sidebar-top .standard-sidebar-item", "border-radius"),
        # "width": (".layout-side-section:not(.right)", "width"),
        "font_size": (".body-sidebar-top .standard-sidebar-item", "font-size"),
        "item_padding": (".body-sidebar-top .standard-sidebar-item", "padding"),
        # "shadow": (".layout-side-section:not(.right)", "box-shadow"),
    },
    "navbar": {
        "bg": ("header.navbar", "background"),
        "text": ("header.navbar .navbar-nav .nav-link", "color"),
        "height": ("header.navbar", "height"),
        "shadow": ("header.navbar", "box-shadow"),
        "border_bottom": ("header.navbar", "border-bottom"),
        "font_weight": ("header.navbar .navbar-nav .nav-link", "font-weight"),
    },
    "buttons_primary": {
        "bg": (".btn-primary, .btn-primary-dark", "background-color"),
        "text": (".btn-primary, .btn-primary-dark", "color"),
        "border_radius": (".btn-primary, .btn-primary-dark", "border-radius"),
        "shadow": (".btn-primary, .btn-primary-dark", "box-shadow"),
        "hover_bg": (".btn-primary:hover, .btn-primary-dark:hover", "background-color"),
        "padding": (".btn-primary, .btn-primary-dark", "padding"),
        "font_weight": (".btn-primary, .btn-primary-dark", "font-weight"),
    },
    "buttons_default": {
        "bg": ("button.btn-default, a.btn-default, .btn.btn-default", "background-color !important"),
        "text": ("button.btn-default, a.btn-default, .btn.btn-default", "color !important"),
        "border_color": ("button.btn-default, a.btn-default, .btn.btn-default", "border-color !important"),
        "border_radius": (".btn-default", "border-radius"),
        "shadow": (".btn-default", "box-shadow"),
        "height": (".btn-default", "height"),
        "hover_bg": ("button.btn-default:hover, a.btn-default:hover, .btn.btn-default:hover", "background-color !important"),
    },
    "buttons_secondary": {
        "bg": ("button.btn-secondary, a.btn-secondary, .btn.btn-secondary", "background-color !important"),
        "text": ("button.btn-secondary, a.btn-secondary, .btn.btn-secondary", "color !important"),
        "border_color": ("button.btn-secondary, a.btn-secondary, .btn.btn-secondary", "border-color !important"),
        "border_radius": (".btn-secondary", "border-radius"),
        "shadow": (".btn-secondary", "box-shadow"),
        "height": (".btn-secondary", "height"),
        "hover_bg": ("button.btn-secondary:hover, a.btn-secondary:hover, .btn.btn-secondary:hover", "background-color !important"),
    },
    "cards": {
        "bg": (".widget-box, .frappe-card", "background !important"),
        "border_radius": (".widget-box, .frappe-card", "border-radius !important"),
        "shadow": (
            ".widget-box, .widget[class*='-widget-box'],"
            " .widget.dashboard-widget-box",
            "box-shadow !important"
        ),
        "border_color": (
            ".widget-box, .frappe-card, .widget[class*='-widget-box']",
            "border-color !important"
        ),
        "padding": (".widget-box, .frappe-card", "padding !important"),
        "hover_shadow": (".widget-box:hover, .frappe-card:hover", "box-shadow !important"),
    },
    "inputs": {
        "bg": (".control-input input:not([type='checkbox']):not([type='radio']), .control-input .link-btn, .input-group input:not([type='checkbox']):not([type='radio']), .awesomplete .input-with-feedback,  .filter-box input:not([type='checkbox']):not([type='radio']), .filter-box select, .form-group select, .form-group input:not([type='checkbox']):not([type='radio']), .form-control, .desktop-navbar-modal-search",  "background-color !important"),
        "border_color": (".control-input input:not([type='checkbox']):not([type='radio']), .control-input select, .desktop-search-wrapper", "border-color"),
        "border_width": (".desktop-search-wrapper", "border-width"),
        "border_style": (".desktop-search-wrapper", "border-style"),
        "border_radius": (".control-input input:not([type='checkbox']):not([type='radio']), .control-input select , .desktop-search-wrapper", "border-radius"),
        "height": (".control-input input:not([type='checkbox']):not([type='radio']), .control-input select", "height"),
        "focus_border": (".control-input input:not([type='checkbox']):not([type='radio']):focus, .control-input select:focus", "border-color"),
        # "focus_shadow": (".control-input input:not([type='checkbox']):not([type='radio']):focus, .control-input select:focus", "box-shadow"),
        "padding": (".control-input input:not([type='checkbox']):not([type='radio']), .control-input select", "padding"),
    },
    "page_head": {
        "bg": (".page-head", "background"),
        "height": (".page-head", "height"),
        "border_bottom": (".page-head", "border-bottom"),
        "title_font_size": (".page-head .page-title .title-text", "font-size"),
        "title_font_weight": (".page-head .page-title .title-text", "font-weight"),
    },
    "lists": {
        "row_hover_bg": (".list-row:hover", "background"),
        "row_border": (".list-row", "border-bottom-color"),
        "row_padding": (".list-row .list-row-container", "padding"),
        "header_bg": (".list-row-head", "background"),
        "header_height": (".list-row-head", "height"),
        "header_font_weight": (".list-row-head .list-header-subject", "font-weight"),
    },
    "modals": {
        "bg": (".modal-content", "background"),
        "border_radius": (".modal-content", "border-radius"),
        "shadow": (".modal-content", "box-shadow"),
        "overlay_color": (".modal-backdrop", "background-color"),
        "header_bg": (".modal-header", "background"),
    },
}

# Quick-edit field → CSS variable mapping
QUICK_EDIT_VARS = {
    "primary_color": "--st-primary",
    "accent_color": "--st-accent",
    "secondary_color": "--st-secondary",
    "dark_color": "--st-dark",
    "light_bg_color": "--st-light-bg",
    "text_color": "--st-text",
    "muted_text_color": "--st-muted-text",
    "link_color": "--st-link",
    "border_color": "--st-border",
    "highlight_color": "--st-highlight",
    "font_family": "--st-font-family",
    "heading_font_family": "--st-heading-font",
    "font_size_base": "--st-font-size-base",
    "heading_weight": "--st-heading-weight",
    "line_height": "--st-line-height",
    "border_radius": "--st-border-radius",
    "card_shadow": "--st-card-shadow",
    "spacing_unit": "--st-spacing",
}

# Scoped transition selectors — only animate during active theme switch
# Each is prefixed with .theme-transitioning so transitions only fire
# when theme_applicator.js adds that class to <body>
TRANSITION_SELECTORS = [
    "header.navbar",
    ".layout-side-section",
    ".standard-sidebar-item",
    ".btn-primary",
    ".btn-default",
    ".widget-box",
    ".frappe-card",
    ".form-control",
    ".page-head",
    ".modal-content",
]


def generate_theme_css(preset_doc, settings_doc):
    """Generate complete CSS string from preset + settings.

    Args:
        preset_doc: DCNET Theme Preset document
        settings_doc: DCNET Theme Settings document

    Returns:
        str: Complete CSS string

    Raises:
        frappe.ValidationError: If component_styles JSON is malformed
    """
    from datetime import datetime

    lines = []
    lines.append(f"/* === DCNET Theme: {preset_doc.preset_name} === */")
    lines.append(f"/* Generated: {datetime.now().isoformat()} — DO NOT EDIT */")
    lines.append("")

    # 1. Google Font import
    google_font_url = getattr(preset_doc, "google_font_url", None)
    if google_font_url:
        lines.append(f'@import url("{google_font_url}");')
        lines.append("")

    # 2. CSS variables from quick-edit fields
    lines.append(":root {")
    for field_name, css_var in QUICK_EDIT_VARS.items():
        value = getattr(preset_doc, field_name, None)
        if value and str(value).strip():
            # Wrap font families in quotes if they contain spaces
            if "font" in css_var and "," not in str(value) and " " in str(value):
                value = f"'{value}'"
            lines.append(f"  {css_var}: {value};")

    # Bridge: override Frappe's built-in CSS variables with our values
    # This ensures dcnet_theme.css and Frappe's own styles pick up our colors
    bridges = {
        "--primary": getattr(preset_doc, "primary_color", None),
        "--brand-color": getattr(preset_doc, "primary_color", None),
        "--sidebar-active-color": None,  # set from component_styles below
        "--sidebar-active-text": None,
        "--highlight-color": getattr(preset_doc, "highlight_color", None),
        "--text-color": getattr(preset_doc, "text_color", None),
        "--text-muted": getattr(preset_doc, "muted_text_color", None),
        "--border-color": getattr(preset_doc, "border_color", None),
        "--bg-color": getattr(preset_doc, "light_bg_color", None),
        "--fg-color": getattr(preset_doc, "light_bg_color", None),
        "--control-bg": getattr(preset_doc, "light_bg_color", None),
    }

    # Extract sidebar active color from component_styles for bridge.
    # Fall back to primary_color so .active-sidebar always follows the theme
    # even when sidebar.active_bg is not explicitly configured.
    component_styles = _parse_component_json(preset_doc, "component_styles")
    primary_color = getattr(preset_doc, "primary_color", None)
    if component_styles:
        sidebar = component_styles.get("sidebar", {})
        bridges["--sidebar-active-color"] = (
            sidebar.get("active_bg") or primary_color
        )
        bridges["--sidebar-active-text"] = sidebar.get("active_text") or "#ffffff"
        if sidebar.get("hover_bg"):
            bridges["--sidebar-hover-color"] = sidebar["hover_bg"]
        input_height = component_styles.get("inputs", {}).get("height")
        if input_height:
            bridges["--input-height"] = input_height
        cards = component_styles.get("cards", {})
        if cards.get("bg"):
            bridges["--card-bg"] = cards.get("bg")
        if cards.get("subtle_accent"):
            bridges["--subtle-accent"] = cards.get("subtle_accent")
        # Bridge btn-primary bg so Frappe's .btn.btn-primary {background-color: var(--btn-primary)}
        # picks up the preset color (direct selector loses on specificity: 1-class vs 2-class)
        btn_primary_bg = component_styles.get("buttons_primary", {}).get("bg")
        if btn_primary_bg:
            bridges["--btn-primary"] = btn_primary_bg
        elif primary_color:
            bridges["--btn-primary"] = primary_color
    elif primary_color:
        bridges["--sidebar-active-color"] = primary_color
        bridges["--sidebar-active-text"] = "#ffffff"

    for var_name, value in bridges.items():
        if value and str(value).strip():
            lines.append(f"  {var_name}: {value};")

    # Desktop icon recolor filter — computed once from primary_color
    if primary_color:
        icon_filter = _hex_to_css_filter(primary_color)
        if icon_filter:
            lines.append(f"  --st-icon-filter: {icon_filter};")

    lines.append("}")
    lines.append("")

    # 3. Component CSS from JSON (reuse already-parsed component_styles)
    if component_styles:
        lines.extend(_generate_component_css(component_styles))

    # 4. Dark mode variant — scoped under [data-theme="dark"] to match Frappe's toggle
    dark_styles = _parse_component_json(preset_doc, "dark_component_styles")
    dark_vars = _parse_component_json(preset_doc, "dark_vars")
    if dark_styles or dark_vars:
        lines.append("")
        lines.append("/* === Dark Mode === */")

    # 4a. Dark CSS variables — override Frappe built-in vars for dark backgrounds/text
    dark_auto_vars = {}
    if dark_styles:
        dark_cards = dark_styles.get("cards", {})
        if dark_cards.get("bg"):
            dark_auto_vars["--card-bg"] = dark_cards["bg"]
        if dark_cards.get("subtle_accent"):
            dark_auto_vars["--subtle-accent"] = dark_cards["subtle_accent"]
        # Bridge --btn-primary so Frappe's [data-theme="dark"] { --btn-primary: var(--gray-300) }
        # doesn't override the preset accent color
        dark_btn_primary_bg = dark_styles.get("buttons_primary", {}).get("bg")
        if dark_btn_primary_bg:
            dark_auto_vars["--btn-primary"] = dark_btn_primary_bg
        # Bridge --control-bg so btn-default and inputs share the same background in dark mode.
        # Frappe uses var(--control-bg) for both; setting it here keeps them in sync.
        dark_input_bg = dark_styles.get("inputs", {}).get("bg")
        if dark_input_bg:
            dark_auto_vars["--control-bg"] = dark_input_bg
            dark_auto_vars["--control-bg-on-gray"] = dark_input_bg

    if dark_vars or dark_auto_vars:
        lines.append("[data-theme='dark'] {")
        for var_name, value in dark_auto_vars.items():
            lines.append(f"  {var_name}: {value};")
        if dark_vars:
            for var_name, value in dark_vars.items():
                if value and str(value).strip():
                    lines.append(f"  {var_name}: {value};")
        lines.append("}")

    # 4b. Dark component rules — scoped selectors for each component
    if dark_styles:
        lines.extend(_generate_component_css(dark_styles, selector_prefix="[data-theme='dark']"))

    # 5. Hardening: fix right sidebar + solid sidebar items
    lines.append("")
    lines.append("/* Fix right form sidebar — must not inherit left sidebar colors */")
    lines.append(".layout-side-section.right { background: var(--fg-color, #fff) !important; }")
    lines.append(".layout-side-section.right .form-sidebar { color: var(--text-color, #333); }")
    lines.append("")
    
    lines.append("")
    lines.append("/* style for main section */")
    lines.append(".main-section { padding-bottom: 0 !important; background: var(--fg-color, #fff) !important;}")
    lines.append(".layout-main-section-wrapper { background: var(--fg-color, #fff) !important; }")
    lines.append(".new-timeline .activity-title { padding-left: 10px !important; }")
    lines.append("")
    
    lines.append("/* Solid sidebar items — icon color matches text, selected is bold */")
    lines.append(".body-sidebar .standard-sidebar-item .sidebar-item-icon { color: inherit !important; }")
    lines.append(".body-sidebar .standard-sidebar-item.selected .sidebar-item-icon { color: inherit !important; }")
    lines.append(".body-sidebar .standard-sidebar-item.selected { font-weight: 500; }")
    lines.append(".body-sidebar .standard-sidebar-item .item-anchor { display: flex; align-items: center; gap: 8px; width: 100%; min-height: 38px; }")
    lines.append(".body-sidebar .sidebar-header .sidebar-item-icon { color: inherit !important; padding: 2px !important; border-radius: 6px !important}")
    lines.append(".body-sidebar .sidebar-header .sidebar-item-icon .header-logo { display: flex; justify-content: center; align-items: center }")
    
    # Auto-apply secondary_color to .btn-secondary (unless overridden by component_styles)
    secondary_color = getattr(preset_doc, "secondary_color", None)
    if secondary_color and not (component_styles and component_styles.get("buttons_secondary")):
        lines.append(
            f"button.btn-secondary, a.btn-secondary, .btn.btn-secondary"
            f" {{ background-color: {secondary_color} !important;"
            f" border-color: {secondary_color} !important; }}"
        )
    lines.append(".control-input:has(> .selected-icon) input, .control-input:has(> .selected-color) input { text-indent: 15px; }")
    lines.append(".control-input:has(> .selected-color) .selected-color { top: 8px; }")
    lines.append(".desktop-container img.app-icon { width: 100%; }")
    lines.append(".header-logo img { filter: var(--st-icon-filter, none); }")
    lines.append(".header-logo img { width: 90% !important}")
    lines.append(".page-form .filter-selector .btn-group { margin: 10px 5px; }")
    lines.append(".page-form .filter-selector .btn-group { height: 30px; }")
    lines.append(".page-form .sort-selector .btn-group { margin: 10px 5px; }")
    lines.append(".page-form .sort-selector .btn-group { height: 30px; }")
    lines.append(".btn.btn-sm.filter-button.btn-default, .btn.btn-default.btn-sm.filter-x-button { display: flex; align-items: center; }")
    lines.append("/* Select placeholder & icon top — follows input height automatically */")
    lines.append(".frappe-control[data-fieldtype=Select].form-group .placeholder,")
    lines.append(".frappe-control[data-fieldtype=Select].form-group .select-icon,")
    lines.append(".select-icon {")
    lines.append("  top: calc((var(--input-height, 28px) - 24px) / 2) !important;")
    lines.append("}")

    lines.append("")

    # 6. Scoped transitions — only animate during active theme switching
    # The .theme-transitioning class is added/removed by theme_applicator.js
    lines.append("")
    lines.append("/* Scoped transitions — only during active theme switch */")
    scoped = ", ".join(f".theme-transitioning {s}" for s in TRANSITION_SELECTORS)
    lines.append(f"{scoped} {{")
    lines.append("  transition: background-color 0.3s ease, color 0.3s ease,")
    lines.append("    border-color 0.3s ease, box-shadow 0.3s ease;")
    lines.append("}")
    lines.append("")

    # 6. Preset custom CSS
    if preset_doc.custom_css:
        lines.append("/* Preset custom CSS */")
        lines.append(preset_doc.custom_css)
        lines.append("")

    # 7. Site-level custom CSS override
    if settings_doc.custom_css_override:
        lines.append("/* Site override CSS */")
        lines.append(settings_doc.custom_css_override)
        lines.append("")

    return "\n".join(lines)


def generate_and_write_css(settings_doc):
    """Generate CSS and write to sites/{site}/public/files/dcnet_theme.css.

    Args:
        settings_doc: DCNET Theme Settings document

    Raises:
        frappe.ValidationError: If preset not found or JSON malformed
        IOError: If file write fails
    """
    if not settings_doc.active_preset:
        return

    preset_doc = frappe.get_doc("DCNET Theme Preset", settings_doc.active_preset)
    css_content = generate_theme_css(preset_doc, settings_doc)

    # Write to sites/{site}/public/files/
    site_path = frappe.get_site_path("public", "files")
    file_path = f"{site_path}/dcnet_theme.css"

    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(css_content)
        frappe.logger("dcnet_theme").info(
            f"Theme CSS generated: preset={preset_doc.preset_name}, "
            f"dark_mode={settings_doc.dark_mode}, user={frappe.session.user}"
        )
    except (IOError, PermissionError) as e:
        frappe.throw(f"Cannot write theme CSS file: {e}")


def _parse_component_json(preset_doc, field_name):
    """Parse and validate component styles JSON field.

    Returns:
        dict or None
    """
    raw = getattr(preset_doc, field_name, None)
    if not raw:
        return None

    try:
        data = json.loads(raw) if isinstance(raw, str) else raw
        if not isinstance(data, dict):
            frappe.throw(f"Invalid {field_name}: expected JSON object, got {type(data).__name__}")
        return data
    except json.JSONDecodeError as e:
        frappe.throw(f"Invalid {field_name} JSON: {e}")


def _generate_component_css(component_styles, selector_prefix=None):
    """Generate CSS rules from component styles dict.

    Args:
        component_styles: dict of component styles
        selector_prefix: optional string prepended to every selector,
                         e.g. "[data-theme='dark']" for dark mode rules

    Returns:
        list of CSS lines
    """
    lines = []
    # Group by selector to avoid duplicate rules
    selector_props = {}

    for component_name, props in component_styles.items():
        mapping = COMPONENT_SELECTORS.get(component_name)
        if not mapping:
            continue

        for prop_key, value in props.items():
            if not value or not str(value).strip():  # skip empty/None/whitespace values
                continue
            selector_info = mapping.get(prop_key)
            if not selector_info:
                continue

            selector, css_prop = selector_info
            if selector not in selector_props:
                selector_props[selector] = []
            selector_props[selector].append((css_prop, value))

    # Output grouped CSS, prefixing each selector if needed
    for selector, props in selector_props.items():
        if selector_prefix:
            # Handle comma-separated selectors — prefix each part
            parts = [f"{selector_prefix} {s.strip()}" for s in selector.split(",")]
            full_selector = ", ".join(parts)
        else:
            full_selector = selector
        lines.append(f"{full_selector} {{")
        for css_prop, value in props:
            important = css_prop.endswith(" !important")
            prop_name = css_prop[: -len(" !important")] if important else css_prop
            suffix = " !important" if important else ""
            # "none" on a color property → collapse to border: none
            if str(value).strip().lower() == "none" and "color" in prop_name:
                lines.append(f"  border: none{suffix};")
            else:
                lines.append(f"  {prop_name}: {value}{suffix};")
        lines.append("}")

    return lines


def _hex_to_css_filter(hex_color):
    """Convert a hex color to a CSS filter string that uniformly recolors any icon.

    The approach: grayscale → sepia (brown tint) → hue-rotate to target → saturate.
    This works regardless of the source icon color because grayscale removes all
    original hue information first.

    Returns:
        str: CSS filter value, or None if color is invalid
    """
    hex_color = hex_color.strip().lstrip("#")
    if len(hex_color) != 6:
        return None

    try:
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
    except ValueError:
        return None

    # Convert RGB to HSL
    r_norm, g_norm, b_norm = r / 255.0, g / 255.0, b / 255.0
    c_max = max(r_norm, g_norm, b_norm)
    c_min = min(r_norm, g_norm, b_norm)
    delta = c_max - c_min

    # Hue
    if delta == 0:
        hue = 0
    elif c_max == r_norm:
        hue = 60 * (((g_norm - b_norm) / delta) % 6)
    elif c_max == g_norm:
        hue = 60 * (((b_norm - r_norm) / delta) + 2)
    else:
        hue = 60 * (((r_norm - g_norm) / delta) + 4)

    # Lightness and saturation
    lightness = (c_max + c_min) / 2
    if delta == 0:
        saturation = 0
    else:
        saturation = delta / (1 - abs(2 * lightness - 1))

    # Sepia base hue is ~38°, rotate to target
    hue_rotate = hue - 38

    # Saturate to match target vibrancy (sepia starts at ~30% saturation)
    saturate_pct = int(max(100, saturation * 500))

    # Brightness adjustment based on target lightness
    # Grayscale + sepia produces ~50% lightness, adjust to target
    brightness = max(0.4, min(2.0, lightness * 2.2 + 0.1))

    return (
        f"grayscale(100%) sepia(100%) "
        f"hue-rotate({int(hue_rotate)}deg) "
        f"saturate({saturate_pct}%) "
        f"brightness({brightness:.2f})"
    )

    return lines
