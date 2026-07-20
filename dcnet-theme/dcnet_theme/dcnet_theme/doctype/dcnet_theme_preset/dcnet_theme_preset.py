import json
import colorsys
import frappe
from frappe.model.document import Document


# =========================================================
# DOCUMENT CONTROLLER
# =========================================================

class DCNETThemePreset(Document):

    def before_save(self):
        self.component_styles = None
        self.dark_component_styles = None
        self.dark_vars = None
        _auto_populate_styles(self)

    def before_delete(self):

        if self.is_system:
            frappe.throw("System presets cannot be deleted")

        active = frappe.db.get_single_value(
            "DCNET Theme Settings",
            "active_preset"
        )

        if self.name == active:
            frappe.throw(
                "Cannot delete the active preset."
            )

    def on_update(self):

        active = frappe.db.get_single_value(
            "DCNET Theme Settings",
            "active_preset"
        )

        if self.name == active:

            from dcnet_theme.dcnet_theme.theme_utils import (
                generate_and_write_css
            )

            settings = frappe.get_single(
                "DCNET Theme Settings"
            )

            generate_and_write_css(settings)

            frappe.cache.delete_value("dcnet_theme_css")

            frappe.clear_cache()

            frappe.publish_realtime(
                event="dcnet_theme_updated",
                message={"preset": self.name},
                after_commit=True,
            )


# =========================================================
# AUTO STYLE GENERATOR
# =========================================================

def _auto_populate_styles(doc):

    p  = doc.primary_color      or "#2563eb"
    ac = doc.accent_color       or "#14b8a6"
    sc = doc.secondary_color    or _darken(p, 0.2)

    dk = doc.dark_color         or "#0f172a"
    lb = doc.light_bg_color     or "#ffffff"

    tx = doc.text_color         or "#0f172a"
    bd = doc.border_color       or "#e2e8f0"
    hl = doc.highlight_color    or _lighten(lb, 0.05)
    cs = doc.card_shadow        or None


    if not doc.component_styles:

        doc.component_styles = json.dumps(

            _build_light_components(
                p, ac, sc, dk,
                lb, tx, bd, hl, cs
            ),

            indent=2
        )


    dark_bg, dark_fg, dark_ctrl, dark_border, dark_text, dark_muted = \
        _derive_dark_palette(dk)


    if not doc.dark_component_styles:

        doc.dark_component_styles = json.dumps(

            _build_dark_components(
                p, ac,
                dark_bg,
                dark_fg,
                dark_ctrl,
                dark_border,
                dark_text,
                dark_muted,
                cs
            ),

            indent=2
        )


    if not doc.dark_vars:

        doc.dark_vars = json.dumps(

            _build_dark_vars(
                dark_bg,
                dark_fg,
                dark_ctrl,
                dark_border,
                dark_text,
                dark_muted
            ),

            indent=2
        )


# =========================================================
# COLOR ENGINE
# =========================================================

def _hex_to_rgb(hex_color):

    hex_color = hex_color.lstrip("#")

    if len(hex_color) == 3:

        hex_color = "".join(c * 2 for c in hex_color)

    return tuple(
        int(hex_color[i:i+2], 16) / 255
        for i in (0, 2, 4)
    )


def _rgb_to_hex(rgb):

    return "#{:02x}{:02x}{:02x}".format(

        int(rgb[0] * 255),
        int(rgb[1] * 255),
        int(rgb[2] * 255),

    )



def _adjust_lightness(hex_color, factor):

    r, g, b = _hex_to_rgb(hex_color)

    h, l, s = colorsys.rgb_to_hls(r, g, b)

    l = max(0.05, min(0.95, l * factor))

    r, g, b = colorsys.hls_to_rgb(h, l, s)

    return _rgb_to_hex((r, g, b))


def _lighten(hex_color, amount=0.15):

    return _adjust_lightness(hex_color, 1 + amount)


def _darken(hex_color, amount=0.15):

    return _adjust_lightness(hex_color, 1 - amount)

def _mix(color1, color2, ratio=0.5):

    r1, g1, b1 = _hex_to_rgb(color1)
    r2, g2, b2 = _hex_to_rgb(color2)

    r = r1 * (1 - ratio) + r2 * ratio
    g = g1 * (1 - ratio) + g2 * ratio
    b = b1 * (1 - ratio) + b2 * ratio

    return _rgb_to_hex((r, g, b))
# =========================================================
# DARK MODE PALETTE
# =========================================================

def _derive_dark_palette(dark_color):

    return (

        _adjust_lightness(dark_color, 0.55),

        dark_color,

        _adjust_lightness(dark_color, 1.15),

        _adjust_lightness(dark_color, 1.30),

        "#e5e7eb",

        "#94a3b8",

    )


# =========================================================
# LIGHT COMPONENTS
# =========================================================

def _build_light_components(

        primary,
        accent,
        secondary,
        dark,
        light_bg,
        text,
        border,
        highlight,
        card_shadow=None

):

    hover = _darken(light_bg, 0.025)

    input_bg = _darken(light_bg, 0.045)

    default_bg = _darken(light_bg, 0.035)

    default_hover = _darken(light_bg, 0.06)
    
    return {

        "sidebar": {

            "bg": dark,

            "text": "#64748b",

            "active_bg": primary,

            "active_text": "#ffffff",

            "hover_bg": hover,

            "hover_text": text,

        },

        "navbar": {

            "bg": light_bg,

            "text": text,

            "border_bottom": f"2px solid {accent}",

        },

        "buttons_primary": {

            "bg": primary,

            "text": "#ffffff",

            "hover_bg": secondary,

        },

        "buttons_secondary": {

            "bg": secondary,

            "text": "#ffffff",

        },

        "buttons_default": {

            "bg": default_bg,

            "text": text,

            "border_color": border,

            "hover_bg": default_hover,
            
            "height": "auto",

        },

        "cards": {

            "bg": light_bg,

            "subtle_accent": highlight,

            **({"shadow": card_shadow} if card_shadow else {}),

        },

        "inputs": {

            "bg": hover,

            "border_color": border,

            "focus_border": primary,

            "height": "38px",

        },

        "lists": {

            "row_hover_bg": hover,

            "header_bg": highlight,
            
            "header_height": "40px",

        },

        "modals": {

            "bg": light_bg,

            "header_bg": highlight,

        }

    }


# =========================================================
# DARK COMPONENTS
# =========================================================

def _build_dark_components(

        primary,
        accent,
        dark_bg,
        dark_fg,
        dark_ctrl,
        dark_border,
        dark_text,
        dark_muted,
        card_shadow=None

):

    accent_dim = _adjust_lightness(accent, 0.7)

    return {

        "sidebar": {

            "bg": dark_bg,

            "text": dark_muted,

            "active_bg": accent,

            "active_text": "#ffffff",

        },

        "navbar": {

            "bg": dark_ctrl,

            "text": dark_text,

            "border_bottom": f"2px solid {accent_dim}",

        },

        "buttons_primary": {

            "bg": accent,

            "text": "#ffffff",

            "hover_bg": _lighten(accent, 0.15),

        },

        "buttons_default": {

            "bg": dark_bg,

            "text": dark_text,

            "border_color": dark_border,

            "hover_bg": dark_ctrl,
            
            "height": "auto",

        },

        "cards": {

            "bg": dark_fg,

            "subtle_accent": dark_ctrl,
            
            **({"shadow": card_shadow} if card_shadow else {}),

        },

        "inputs": {

            "bg": dark_bg,

            "border_color": dark_border,
            
            "height": "38px",

        },

        "lists": {

            "row_hover_bg": dark_ctrl,

            "header_bg": dark_bg,
            
            "header_height": "40px",

        },

        "modals": {

            "bg": dark_fg,

            "header_bg": dark_bg,

        }

    }


# =========================================================
# DARK CSS VARS
# =========================================================

def _build_dark_vars(

        dark_bg,
        dark_fg,
        dark_ctrl,
        dark_border,
        dark_text,
        dark_muted

):

    return {

        "--bg-color": dark_fg,

        "--fg-color": dark_fg,

        "--control-bg": dark_bg,

        "--border-color": dark_border,

        "--text-color": dark_text,

        "--text-muted": dark_muted,

        "--st-text": dark_text,

        "--st-muted-text": dark_muted,

        "--st-border": dark_border,

        "--st-light-bg": dark_ctrl,

    }