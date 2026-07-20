"""Nation-inspired theme presets for DCNET Theme."""

import json

PRESETS = [
    # ─────────────────────────────────────────────────────────────────────
    # 1. Vietnam — Bold red sidebar, golden accents, warm backgrounds
    # ─────────────────────────────────────────────────────────────────────
    {
        "doctype": "DCNET Theme Preset",
        "preset_key": "vietnam",
        "preset_name": "Vietnam",
        "description": "Bold red sidebar, golden accents, warm backgrounds",
        "flag_colors": "linear-gradient(135deg, #da251d 50%, #ffcd00 50%)",
        "is_system": 1,
        "google_font_url": "https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;600;700&display=swap",
        "primary_color": "#da251d",
        "accent_color": "#ffcd00",
        "secondary_color": "#b71c1c",
        "dark_color": "#1a1a2e",
        "light_bg_color": "#ffffff",
        "text_color": "#1a1a2e",
        "muted_text_color": "#6b7280",
        "link_color": "#da251d",
        "border_color": "#e5e0d5",
        "highlight_color": "#ECEEF5",
        "font_family": "'Be Vietnam Pro', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
        "heading_font_family": "'Be Vietnam Pro', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
        "font_size_base": "13px",
        "heading_weight": "600",
        "line_height": "1.5",
        "border_radius": "6px",
        "card_shadow": "rgba(149, 157, 165, 0.2) 0px 8px 24px",
        "spacing_unit": "16px",
        "component_styles": json.dumps({
            "sidebar": {
                "bg": "#1a1a2e",
                "text": "#525252",
                "active_bg": "#da251d",
                "active_text": "#ffffff",
                "active_icon_stroke": "#ffffff",
                "hover_bg": "#edeff5",
                "hover_text": "#525252",
                "border_radius": "8px",
                "width": "240px",
                "font_size": "13px",
                "item_padding": "0px",
                "shadow": "2px 0 12px rgba(26, 26, 46, 0.15)"
            },
            "navbar": {
                "bg": "#ffffff",
                "text": "#1a1a2e",
                "height": "52px",
                "shadow": "0 1px 4px rgba(26, 26, 46, 0.06)",
                "border_bottom": "2px solid #ffcd00",
                "font_weight": "500"
            },
            "buttons_primary": {
                "bg": "#da251d",
                "text": "#ffffff",
                "border_radius": "8px",
                "shadow": "0 2px 6px rgba(218, 37, 29, 0.3)",
                "hover_bg": "#b71c1c",
                "padding": "8px 20px",
                "font_weight": "400"
            },
            "buttons_default": {
                "bg": "#EDEFF5",
                "text": "#1a1a2e",
                "border_color": "#e5e0d5",
                "border_radius": "8px",
                "shadow": "none",
                "height": "auto",
                "hover_bg": "#fffdf5"
            },
            "buttons_secondary": {
                "bg": "#b71c1c",
                "text": "#ffffff"
            },
            "cards": {
                "bg": "#ffffff",
                "subtle_accent": "#ECEEF5",
                "border_radius": "10px",
                "shadow": "rgba(149, 157, 165, 0.2) 0px 8px 24px",
                "border_color": "none",
                "padding": "20px",
                "hover_shadow": "0 4px 16px rgba(26, 26, 46, 0.12)"
            },
            "inputs": {
                "bg": "#ECEEF5",
                "border_color": "#e5e0d5",
                "border_width": "1px",
                "border_style": "solid",
                "border_radius": "8px",
                "height": "36px",
                "focus_border": "#da251d",
                "focus_shadow": "0 0 0 3px rgba(218, 37, 29, 0.12)",
                "padding": "8px 12px"
            },
            "page_head": {
                "bg": "#ffffff",
                "height": "60px",
                "border_bottom": "1px solid #e5e0d5",
                "title_font_size": "16px",
                "title_font_weight": "700"
            },
            "lists": {
                "row_hover_bg": "#fffdf5",
                "row_border": "1px solid #f0ebe0",
                "row_padding": "12px 16px",
                "header_bg": "#faf7f0",
                "header_height": "40px",
                "header_font_weight": "600"
            },
            "modals": {
                "bg": "#ffffff",
                "border_radius": "12px",
                "shadow": "0 8px 32px rgba(26, 26, 46, 0.2)",
                "overlay_color": "rgba(26, 26, 46, 0.5)",
                "header_bg": "#fffdf5"
            }
        }),
        "dark_component_styles": json.dumps({
            "sidebar": {
                "bg": "#0f0f1e",
                "text": "#c8bfa8",
                "active_bg": "#ffcd00",
                "active_text": "#ffffff",
                "active_icon_stroke": "#ffffff",
                "hover_bg": "#1e1e38",
                "hover_text": "#edeff5",
                "border_radius": "8px",
                "width": "240px",
                "font_size": "13px",
                "item_padding": "0px",
                "shadow": "2px 0 12px rgba(0, 0, 0, 0.3)"
            },
            "navbar": {
                "bg": "#1a1a2e",
                "text": "#e0d8c8",
                "height": "52px",
                "shadow": "0 1px 4px rgba(0, 0, 0, 0.2)",
                "border_bottom": "2px solid #b8960a",
                "font_weight": "500"
            },
            "buttons_primary": {
                "bg": "#da251d",
                "text": "#ffffff",
                "border_radius": "8px",
                "shadow": "0 2px 6px rgba(218, 37, 29, 0.4)",
                "hover_bg": "#ef4444",
                "padding": "8px 20px",
                "font_weight": "400"
            },
            "buttons_default": {
                "bg": "#1e1e38",
                "text": "#e0d8c8",
                "border_color": "#2e2e4e",
                "border_radius": "8px",
                "shadow": "none",
                "height": "auto",
                "hover_bg": "#2a2a4a"
            },
            "buttons_secondary": {
                "bg": "#b71c1c",
                "text": "#ffffff"
            },
            "cards": {
                "bg": "#0f0f1e",
                "subtle_accent": "#1e1e40",
                "border_radius": "10px",
                "shadow": "rgba(149, 157, 165, 0.2) 0px 8px 24px",
                "border_color": "none",
                "padding": "20px",
                "hover_shadow": "0 4px 16px rgba(0, 0, 0, 0.35)"
            },
            "inputs": {
                "bg": "#000000",
                "border_color": "#2e2e4e",
                "border_width": "1px",
                "border_style": "solid",
                "border_radius": "8px",
                "height": "36px",
                "focus_border": "#da251d",
                "focus_shadow": "0 0 0 3px rgba(218, 37, 29, 0.2)",
                "padding": "8px 12px"
            },
            "page_head": {
                "bg": "#0f0f1e",
                "height": "60px",
                "border_bottom": "1px solid #2e2e4e",
                "title_font_size": "16px",
                "title_font_weight": "700"
            },
            "lists": {
                "row_hover_bg": "#1e1e38",
                "row_border": "1px solid #252545",
                "row_padding": "12px 16px",
                "header_bg": "#141426",
                "header_height": "40px",
                "header_font_weight": "600"
            },
            "modals": {
                "bg": "#1a1a30",
                "border_radius": "12px",
                "shadow": "0 8px 32px rgba(0, 0, 0, 0.5)",
                "overlay_color": "rgba(0, 0, 0, 0.7)",
                "header_bg": "#161628"
            }
        }),
        "dark_vars": json.dumps({
            "--bg-color": "#1a1a2e",
            "--fg-color": "#0f0f1e",
            "--control-bg": "#1a1a30",
            "--border-color": "#2e2e4e",
            "--text-color": "#c8bfa8",
            "--text-muted": "#9090a8",
            "--st-text": "#c8bfa8",
            "--st-muted-text": "#9090a8",
            "--st-border": "#2e2e4e",
            "--st-light-bg": "#1a1a30",
        }),
        "custom_css": "",
    },

    # ─────────────────────────────────────────────────────────────────────
    # 2. Italy — Elegant Mediterranean greens, warm terracotta accents
    # ─────────────────────────────────────────────────────────────────────
    {
        "doctype": "DCNET Theme Preset",
        "preset_key": "italy",
        "preset_name": "Italy",
        "description": "Elegant Mediterranean greens with warm terracotta red accents",
        "flag_colors": "linear-gradient(135deg, #009246 33%, #ffffff 33%, #ffffff 66%, #ce2b37 66%)",
        "is_system": 1,
        "google_font_url": "https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500;600;700&family=Source+Sans+3:wght@400;500;600&display=swap",
        "primary_color": "#009246",
        "accent_color": "#ce2b37",
        "secondary_color": "#1b6b3a",
        "dark_color": "#1c2e1c",
        "light_bg_color": "#ffffff",
        "text_color": "#2c3e2c",
        "muted_text_color": "#6b7c6b",
        "link_color": "#009246",
        "border_color": "#d4cfc5",
        "highlight_color": "#f0f8f0",
        "font_family": "'Source Sans 3', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
        "heading_font_family": "'Playfair Display', Georgia, 'Times New Roman', serif",
        "font_size_base": "14px",
        "heading_weight": "600",
        "line_height": "1.6",
        "border_radius": "6px",
        "card_shadow": "rgba(149, 157, 165, 0.2) 0px 8px 24px",
        "spacing_unit": "16px",
        "component_styles": json.dumps({
            "sidebar": {
                "bg": "#1c2e1c",
                "text": "#525252",
                "active_bg": "#009246",
                "active_text": "#ffffff",
                "active_icon_stroke": "#ffffff",
                "hover_bg": "#2a4a2a",
                "hover_text": "#edeff5",
                "border_radius": "6px",
                "width": "250px",
                "font_size": "13px",
                "item_padding": "0px",
                "shadow": "2px 0 10px rgba(28, 46, 28, 0.12)"
            },
            "navbar": {
                "bg": "#ffffff",
                "text": "#2c3e2c",
                "height": "54px",
                "shadow": "0 1px 3px rgba(28, 46, 28, 0.05)",
                "border_bottom": "1px solid #d4cfc5",
                "font_weight": "500"
            },
            "buttons_primary": {
                "bg": "#009246",
                "text": "#ffffff",
                "border_radius": "6px",
                "shadow": "0 2px 4px rgba(0, 146, 70, 0.2)",
                "hover_bg": "#1b6b3a",
                "padding": "8px 22px",
                "font_weight": "400"
            },
            "buttons_default": {
                "bg": "#EDEFF5",
                "text": "#1a1a2e",
                "border_color": "#e5e0d5",
                "border_radius": "8px",
                "shadow": "none",
                "height": "auto",
                "hover_bg": "#f0f8f0"
            },
            "buttons_secondary": {
                "bg": "#1b6b3a",
                "text": "#ffffff"
            },
            "cards": {
                "bg": "#ffffff",
                "subtle_accent": "#f0f8f0",
                "border_radius": "8px",
                "shadow": "rgba(149, 157, 165, 0.2) 0px 8px 24px",
                "border_color": "none",
                "padding": "22px",
                "hover_shadow": "0 3px 12px rgba(28, 46, 28, 0.1)"
            },
            "inputs": {
                "bg": "#edeff5",
                "border_color": "#d4cfc5",
                "border_width": "1px",
                "border_style": "solid",
                "border_radius": "6px",
                "height": "38px",
                "focus_border": "#009246",
                "focus_shadow": "0 0 0 3px rgba(0, 146, 70, 0.1)",
                "padding": "8px 14px"
            },
            "page_head": {
                "bg": "#ffffff",
                "height": "62px",
                "border_bottom": "1px solid #d4cfc5",
                "title_font_size": "16px",
                "title_font_weight": "600"
            },
            "lists": {
                "row_hover_bg": "#f0f8f0",
                "row_border": "1px solid #e8e4dc",
                "row_padding": "12px 18px",
                "header_bg": "#faf9f6",
                "header_height": "40px",
                "header_font_weight": "600"
            },
            "modals": {
                "bg": "#ffffff",
                "border_radius": "10px",
                "shadow": "0 6px 28px rgba(28, 46, 28, 0.18)",
                "overlay_color": "rgba(28, 46, 28, 0.45)",
                "header_bg": "#faf9f6"
            }
        }),
        "dark_component_styles": json.dumps({
            "sidebar": {
                "bg": "#0e1a0e",
                "text": "#a8c0a8",
                "active_bg": "#ce2b37",
                "active_text": "#ffffff",
                "active_icon_stroke": "#ffffff",
                "hover_bg": "#1a2e1a",
                "hover_text": "#edeff5",
                "border_radius": "6px",
                "width": "250px",
                "font_size": "13.5px",
                "item_padding": "0px",
                "shadow": "2px 0 10px rgba(0, 0, 0, 0.3)"
            },
            "navbar": {
                "bg": "#141e14",
                "text": "#c8d8c8",
                "height": "54px",
                "shadow": "0 1px 3px rgba(0, 0, 0, 0.2)",
                "border_bottom": "1px solid #2a3e2a",
                "font_weight": "500"
            },
            "buttons_primary": {
                "bg": "#ce2b37",
                "text": "#ffffff",
                "border_radius": "6px",
                "shadow": "0 2px 4px rgba(0, 146, 70, 0.3)",
                "hover_bg": "#00a854",
                "padding": "8px 22px",
                "font_weight": "400"
            },
            "buttons_default": {
                "bg": "#1a2e1a",
                "text": "#c8d8c8",
                "border_color": "#2a4a2a",
                "border_radius": "6px",
                "shadow": "none",
                "height": "auto",
                "hover_bg": "#223822"
            },
            "buttons_secondary": {
                "bg": "#1b6b3a",
                "text": "#ffffff"
            },
            "cards": {
                "bg": "#162016",
                "subtle_accent": "#1c2a1c",
                "border_radius": "8px",
                "shadow": "rgba(149, 157, 165, 0.2) 0px 8px 24px",
                "border_color": "none",
                "padding": "22px",
                "hover_shadow": "0 3px 12px rgba(0, 0, 0, 0.35)"
            },
            "inputs": {
                "bg": "#000000",
                "border_color": "#2a3e2a",
                "border_width": "1px",
                "border_style": "solid",
                "border_radius": "6px",
                "height": "38px",
                "focus_border": "#ce2b37",
                "focus_shadow": "0 0 0 3px rgba(0, 146, 70, 0.2)",
                "padding": "8px 14px"
            },
            "page_head": {
                "bg": "#141e14",
                "height": "62px",
                "border_bottom": "1px solid #2a3e2a",
                "title_font_size": "16px",
                "title_font_weight": "600"
            },
            "lists": {
                "row_hover_bg": "#1a2e1a",
                "row_border": "1px solid #223222",
                "row_padding": "12px 18px",
                "header_bg": "#121c12",
                "header_height": "40px",
                "header_font_weight": "600"
            },
            "modals": {
                "bg": "#162016",
                "border_radius": "10px",
                "shadow": "0 6px 28px rgba(0, 0, 0, 0.5)",
                "overlay_color": "rgba(0, 0, 0, 0.7)",
                "header_bg": "#141e14"
            }
        }),
        "dark_vars": json.dumps({
            "--bg-color": "#1c2e1c",
            "--fg-color": "#141e14",
            "--control-bg": "#162016",
            "--border-color": "#2a3e2a",
            "--text-color": "#c8d8c8",
            "--text-muted": "#a8c0a8",
            "--st-text": "#c8d8c8",
            "--st-muted-text": "#a8c0a8",
            "--st-border": "#2a3e2a",
            "--st-light-bg": "#162016",
        }),
        "custom_css": "",
    },

    # ─────────────────────────────────────────────────────────────────────
    # 3. Germany — Engineering-precise, dark efficiency
    # ─────────────────────────────────────────────────────────────────────
    {
        "doctype": "DCNET Theme Preset",
        "preset_key": "germany",
        "preset_name": "Germany",
        "description": "Engineering-precise with dark sidebar and bold accent stripes",
        "flag_colors": "linear-gradient(180deg, #1a1a1a 33%, #dd0000 33%, #dd0000 66%, #ffcc00 66%)",
        "is_system": 1,
        "google_font_url": "https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600;700&display=swap",
        "primary_color": "#1a1a1a",
        "accent_color": "#dd0000",
        "secondary_color": "#ffcc00",
        "dark_color": "#111111",
        "light_bg_color": "#f8f8f8",
        "text_color": "#1a1a1a",
        "muted_text_color": "#6b6b6b",
        "link_color": "#dd0000",
        "border_color": "#d1d1d1",
        "highlight_color": "#fff9e6",
        "font_family": "'IBM Plex Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
        "heading_font_family": "'IBM Plex Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
        "font_size_base": "13px",
        "heading_weight": "600",
        "line_height": "1.5",
        "border_radius": "6px",
        "card_shadow": "rgba(149, 157, 165, 0.2) 0px 8px 24px",
        "spacing_unit": "16px",
        "component_styles": json.dumps({
            "sidebar": {
                "bg": "#111111",
                "text": "#525252",
                "active_bg": "#dd0000",
                "active_text": "#ffffff",
                "active_icon_stroke": "#ffffff",
                "hover_bg": "#222222",
                "hover_text": "#edeff5",
                "border_radius": "3px",
                "width": "230px",
                "font_size": "13px",
                "item_padding": "0px",
                "shadow": "2px 0 8px rgba(0, 0, 0, 0.15)"
            },
            "navbar": {
                "bg": "#ffffff",
                "text": "#1a1a1a",
                "height": "50px",
                "shadow": "none",
                "border_bottom": "2px solid #1a1a1a",
                "font_weight": "600"
            },
            "buttons_primary": {
                "bg": "#1a1a1a",
                "text": "#ffffff",
                "border_radius": "8px",
                "shadow": "none",
                "hover_bg": "#333333",
                "padding": "8px 20px",
                "font_weight": "400"
            },
            "buttons_default": {
                "bg": "#EDEFF5",
                "text": "#1a1a2e",
                "border_color": "#e5e0d5",
                "border_radius": "8px",
                "shadow": "none",
                "height": "auto",
                "hover_bg": "#f0f0f0"
            },
            "buttons_secondary": {
                "bg": "#ffcc00",
                "text": "#ffffff"
            },
            "cards": {
                "bg": "#ffffff",
                "subtle_accent": "#fff9e6",
                "border_radius": "4px",
                "shadow": "rgba(149, 157, 165, 0.2) 0px 8px 24px",
                "border_color": "none",
                "padding": "20px",
                "hover_shadow": "0 2px 8px rgba(0, 0, 0, 0.12)"
            },
            "inputs": {
                "bg": "#edeff5",
                "border_color": "#d1d1d1",
                "border_width": "1px",
                "border_style": "solid",
                "border_radius": "4px",
                "height": "36px",
                "focus_border": "#1a1a1a",
                "focus_shadow": "0 0 0 2px rgba(26, 26, 26, 0.08)",
                "padding": "8px 12px"
            },
            "page_head": {
                "bg": "#ffffff",
                "height": "56px",
                "border_bottom": "1px solid #1a1a1a",
                "title_font_size": "16px",
                "title_font_weight": "600"
            },
            "lists": {
                "row_hover_bg": "#f4f4f4",
                "row_border": "1px solid #e5e5e5",
                "row_padding": "11px 16px",
                "header_bg": "#f8f8f8",
                "header_height": "40px",
                "header_font_weight": "600"
            },
            "modals": {
                "bg": "#ffffff",
                "border_radius": "4px",
                "shadow": "0 4px 24px rgba(0, 0, 0, 0.2)",
                "overlay_color": "rgba(0, 0, 0, 0.5)",
                "header_bg": "#f8f8f8"
            }
        }),
        "dark_component_styles": json.dumps({
            "sidebar": {
                "bg": "#0a0a0a",
                "text": "#909090",
                "active_bg": "#ffcc00",
                "active_text": "#ffffff",
                "active_icon_stroke": "#ffffff",
                "hover_bg": "#1a1a1a",
                "hover_text": "#edeff5",
                "border_radius": "3px",
                "width": "230px",
                "font_size": "13px",
                "item_padding": "0px",
                "shadow": "2px 0 8px rgba(0, 0, 0, 0.4)"
            },
            "navbar": {
                "bg": "#111111",
                "text": "#d0d0d0",
                "height": "50px",
                "shadow": "none",
                "border_bottom": "2px solid #dd0000",
                "font_weight": "600"
            },
            "buttons_primary": {
                "bg": "#ffcc00",
                "text": "#ffffff",
                "border_radius": "4px",
                "shadow": "none",
                "hover_bg": "#ff2222",
                "padding": "8px 20px",
                "font_weight": "400"
            },
            "buttons_default": {
                "bg": "#1a1a1a",
                "text": "#d0d0d0",
                "border_color": "#333333",
                "border_radius": "4px",
                "shadow": "none",
                "height": "auto",
                "hover_bg": "#252525"
            },
            "buttons_secondary": {
                "bg": "#ffcc00",
                "text": "#ffffff"
            },
            "cards": {
                "bg": "#151515",
                "subtle_accent": "#1f1f1f",
                "border_radius": "4px",
                "shadow": "rgba(149, 157, 165, 0.2) 0px 8px 24px",
                "border_color": "none",
                "padding": "20px",
                "hover_shadow": "0 2px 8px rgba(0, 0, 0, 0.4)"
            },
            "inputs": {
                "bg": "#000000",
                "border_color": "#2a2a2a",
                "border_width": "1px",
                "border_style": "solid",
                "border_radius": "4px",
                "height": "36px",
                "focus_border": "#ffcc00",
                "focus_shadow": "0 0 0 2px rgba(221, 0, 0, 0.15)",
                "padding": "8px 12px"
            },
            "page_head": {
                "bg": "#111111",
                "height": "56px",
                "border_bottom": "1px solid #2a2a2a",
                "title_font_size": "16px",
                "title_font_weight": "600"
            },
            "lists": {
                "row_hover_bg": "#1a1a1a",
                "row_border": "1px solid #222222",
                "row_padding": "11px 16px",
                "header_bg": "#0e0e0e",
                "header_height": "40px",
                "header_font_weight": "600"
            },
            "modals": {
                "bg": "#151515",
                "border_radius": "4px",
                "shadow": "0 4px 24px rgba(0, 0, 0, 0.6)",
                "overlay_color": "rgba(0, 0, 0, 0.75)",
                "header_bg": "#111111"
            }
        }),
        "dark_vars": json.dumps({
            "--bg-color": "#0a0a0a",
            "--fg-color": "#111111",
            "--control-bg": "#151515",
            "--border-color": "#2a2a2a",
            "--text-color": "#d0d0d0",
            "--text-muted": "#909090",
            "--st-text": "#d0d0d0",
            "--st-muted-text": "#909090",
            "--st-border": "#2a2a2a",
            "--st-light-bg": "#151515",
        }),
        "custom_css": "",
    },

    # ─────────────────────────────────────────────────────────────────────
    # 4. France — Royal blue elegance, clean and authoritative
    # ─────────────────────────────────────────────────────────────────────
    {
        "doctype": "DCNET Theme Preset",
        "preset_key": "france",
        "preset_name": "France",
        "description": "Royal blue elegance with clean, authoritative lines",
        "flag_colors": "linear-gradient(135deg, #002395 33%, #ffffff 33%, #ffffff 66%, #ed2939 66%)",
        "is_system": 1,
        "google_font_url": "https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap",
        "primary_color": "#002395",
        "accent_color": "#ed2939",
        "secondary_color": "#1a3fad",
        "dark_color": "#0a1628",
        "light_bg_color": "#f7f8fc",
        "text_color": "#0a1628",
        "muted_text_color": "#6b7494",
        "link_color": "#002395",
        "border_color": "#d0d5e8",
        "highlight_color": "#eef1ff",
        "font_family": "'Poppins', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
        "heading_font_family": "'Poppins', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
        "font_size_base": "13px",
        "heading_weight": "600",
        "line_height": "1.55",
        "border_radius": "6px",
        "card_shadow": "rgba(149, 157, 165, 0.2) 0px 8px 24px",
        "spacing_unit": "16px",
        "component_styles": json.dumps({
            "sidebar": {
                "bg": "#0a1628",
                "text": "#525252",
                "active_bg": "#002395",
                "active_text": "#ffffff",
                "active_icon_stroke": "#ffffff",
                "hover_bg": "#142240",
                "hover_text": "#edeff5",
                "border_radius": "10px",
                "width": "245px",
                "font_size": "13px",
                "item_padding": "0px",
                "shadow": "2px 0 14px rgba(10, 22, 40, 0.12)"
            },
            "navbar": {
                "bg": "#ffffff",
                "text": "#0a1628",
                "height": "54px",
                "shadow": "0 1px 4px rgba(10, 22, 40, 0.05)",
                "border_bottom": "1px solid #d0d5e8",
                "font_weight": "500"
            },
            "buttons_primary": {
                "bg": "#002395",
                "text": "#ffffff",
                "border_radius": "8px",
                "shadow": "0 2px 8px rgba(0, 35, 149, 0.25)",
                "hover_bg": "#1a3fad",
                "padding": "8px 24px",
                "font_weight": "400"
            },
            "buttons_default": {
                "bg": "#EDEFF5",
                "text": "#1a1a2e",
                "border_color": "#e5e0d5",
                "border_radius": "8px",
                "shadow": "none",
                "height": "auto",
                "hover_bg": "#eef1ff"
            },
            "buttons_secondary": {
                "bg": "#1a3fad",
                "text": "#ffffff"
            },
            "cards": {
                "bg": "#ffffff",
                "subtle_accent": "#eef1ff",
                "border_radius": "12px",
                "shadow": "rgba(149, 157, 165, 0.2) 0px 8px 24px",
                "border_color": "none",
                "padding": "22px",
                "hover_shadow": "0 6px 20px rgba(10, 22, 40, 0.1)"
            },
            "inputs": {
                "bg": "#edeff5",
                "border_color": "#d0d5e8",
                "border_width": "1px",
                "border_style": "solid",
                "border_radius": "10px",
                "height": "38px",
                "focus_border": "#002395",
                "focus_shadow": "0 0 0 3px rgba(0, 35, 149, 0.1)",
                "padding": "8px 14px"
            },
            "page_head": {
                "bg": "#f7f8fc",
                "height": "60px",
                "border_bottom": "1px solid #d0d5e8",
                "title_font_size": "16px",
                "title_font_weight": "600"
            },
            "lists": {
                "row_hover_bg": "#eef1ff",
                "row_border": "1px solid #e4e8f4",
                "row_padding": "12px 18px",
                "header_bg": "#f7f8fc",
                "header_height": "40px",
                "header_font_weight": "600"
            },
            "modals": {
                "bg": "#ffffff",
                "border_radius": "14px",
                "shadow": "0 8px 36px rgba(10, 22, 40, 0.18)",
                "overlay_color": "rgba(10, 22, 40, 0.45)",
                "header_bg": "#f7f8fc"
            }
        }),
        "dark_component_styles": json.dumps({
            "sidebar": {
                "bg": "#060e1c",
                "text": "#8898be",
                "active_bg": "#002395",
                "active_text": "#ffffff",
                "active_icon_stroke": "#ffffff",
                "hover_bg": "#0e1830",
                "hover_text": "#edeff5",
                "border_radius": "10px",
                "width": "245px",
                "font_size": "13px",
                "item_padding": "0px",
                "shadow": "2px 0 14px rgba(0, 0, 0, 0.3)"
            },
            "navbar": {
                "bg": "#0e1628",
                "text": "#b0bcd8",
                "height": "54px",
                "shadow": "0 1px 4px rgba(0, 0, 0, 0.2)",
                "border_bottom": "1px solid #1e2e4e",
                "font_weight": "500"
            },
            "buttons_primary": {
                "bg": "#002395",
                "text": "#ffffff",
                "border_radius": "10px",
                "shadow": "0 2px 8px rgba(0, 35, 149, 0.4)",
                "hover_bg": "#0038cc",
                "padding": "8px 24px",
                "font_weight": "400"
            },
            "buttons_default": {
                "bg": "#142240",
                "text": "#b0bcd8",
                "border_color": "#1e2e4e",
                "border_radius": "10px",
                "shadow": "none",
                "height": "auto",
                "hover_bg": "#1a2e50"
            },
            "buttons_secondary": {
                "bg": "#1a3fad",
                "text": "#ffffff"
            },
            "cards": {
                "bg": "#101e34",
                "subtle_accent": "#14243c",
                "border_radius": "12px",
                "shadow": "rgba(149, 157, 165, 0.2) 0px 8px 24px",
                "border_color": "none",
                "padding": "22px",
                "hover_shadow": "0 6px 20px rgba(0, 0, 0, 0.35)"
            },
            "inputs": {
                "bg": "#000000",
                "border_color": "#1e2e4e",
                "border_width": "1px",
                "border_style": "solid",
                "border_radius": "10px",
                "height": "38px",
                "focus_border": "#002395",
                "focus_shadow": "0 0 0 3px rgba(0, 35, 149, 0.2)",
                "padding": "8px 14px"
            },
            "page_head": {
                "bg": "#0e1628",
                "height": "60px",
                "border_bottom": "1px solid #1e2e4e",
                "title_font_size": "16px",
                "title_font_weight": "600"
            },
            "lists": {
                "row_hover_bg": "#142240",
                "row_border": "1px solid #182840",
                "row_padding": "12px 18px",
                "header_bg": "#0a1220",
                "header_height": "40px",
                "header_font_weight": "600"
            },
            "modals": {
                "bg": "#101e34",
                "border_radius": "14px",
                "shadow": "0 8px 36px rgba(0, 0, 0, 0.5)",
                "overlay_color": "rgba(0, 0, 0, 0.7)",
                "header_bg": "#0e1628"
            }
        }),
        "dark_vars": json.dumps({
            "--bg-color": "#060e1c",
            "--fg-color": "#0e1628",
            "--control-bg": "#101e34",
            "--border-color": "#1e2e4e",
            "--text-color": "#b0bcd8",
            "--text-muted": "#8898be",
            "--st-text": "#b0bcd8",
            "--st-muted-text": "#8898be",
            "--st-border": "#1e2e4e",
            "--st-light-bg": "#101e34",
        }),
        "custom_css": "",
    },

    # ─────────────────────────────────────────────────────────────────────
    # 5. Brazil — Vibrant tropical greens, sunny yellow, ocean blue
    # ─────────────────────────────────────────────────────────────────────
    {
        "doctype": "DCNET Theme Preset",
        "preset_key": "brazil",
        "preset_name": "Brazil",
        "description": "Vibrant tropical greens with sunny yellow and ocean blue accents",
        "flag_colors": "linear-gradient(135deg, #009c3b 40%, #ffdf00 40%, #ffdf00 60%, #002776 60%)",
        "is_system": 1,
        "google_font_url": "https://fonts.googleapis.com/css2?family=Rubik:wght@400;500;600;700&display=swap",
        "primary_color": "#009c3b",
        "accent_color": "#ffdf00",
        "secondary_color": "#002776",
        "dark_color": "#0c2818",
        "light_bg_color": "#f5faf5",
        "text_color": "#1a2e1a",
        "muted_text_color": "#5a7a5a",
        "link_color": "#007a2f",
        "border_color": "#c8e0c8",
        "highlight_color": "#fffde0",
        "font_family": "'Rubik', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
        "heading_font_family": "'Rubik', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
        "font_size_base": "13.5px",
        "heading_weight": "600",
        "line_height": "1.5",
        "border_radius": "6px",
        "card_shadow": "rgba(149, 157, 165, 0.2) 0px 8px 24px",
        "spacing_unit": "16px",
        "component_styles": json.dumps({
            "sidebar": {
                "bg": "#0c2818",
                "text": "#525252",
                "active_bg": "#009c3b",
                "active_text": "#ffffff",
                "active_icon_stroke": "#ffffff",
                "hover_bg": "#14401e",
                "hover_text": "#edeff5",
                "border_radius": "12px",
                "width": "245px",
                "font_size": "13.5px",
                "item_padding": "0px",
                "shadow": "2px 0 16px rgba(12, 40, 24, 0.15)"
            },
            "navbar": {
                "bg": "#ffffff",
                "text": "#1a2e1a",
                "height": "54px",
                "shadow": "0 2px 6px rgba(12, 40, 24, 0.06)",
                "border_bottom": "3px solid #ffdf00",
                "font_weight": "500"
            },
            "buttons_primary": {
                "bg": "#009c3b",
                "text": "#ffffff",
                "border_radius": "12px",
                "shadow": "0 3px 10px rgba(0, 156, 59, 0.3)",
                "hover_bg": "#007a2f",
                "padding": "9px 22px",
                "font_weight": "400"
            },
            "buttons_default": {
                "bg": "#EDEFF5",
                "text": "#1a1a2e",
                "border_color": "#e5e0d5",
                "border_radius": "8px",
                "shadow": "none",
                "height": "auto",
                "hover_bg": "#eaf8ea"
            },
            "buttons_secondary": {
                "bg": "#002776",
                "text": "#ffffff"
            },
            "cards": {
                "bg": "#ffffff",
                "subtle_accent": "#fffde0",
                "border_radius": "14px",
                "shadow": "rgba(149, 157, 165, 0.2) 0px 8px 24px",
                "border_color": "none",
                "padding": "22px",
                "hover_shadow": "0 6px 24px rgba(12, 40, 24, 0.12)"
            },
            "inputs": {
                "bg": "#edeff5",
                "border_color": "#c8e0c8",
                "border_width": "1px",
                "border_style": "solid",
                "border_radius": "12px",
                "height": "38px",
                "focus_border": "#009c3b",
                "focus_shadow": "0 0 0 3px rgba(0, 156, 59, 0.12)",
                "padding": "8px 14px"
            },
            "page_head": {
                "bg": "#f5faf5",
                "height": "60px",
                "border_bottom": "1px solid #c8e0c8",
                "title_font_size": "16px",
                "title_font_weight": "700"
            },
            "lists": {
                "row_hover_bg": "#eaf8ea",
                "row_border": "1px solid #d8ecd8",
                "row_padding": "12px 18px",
                "header_bg": "#f0f8f0",
                "header_height": "40px",
                "header_font_weight": "600"
            },
            "modals": {
                "bg": "#ffffff",
                "border_radius": "16px",
                "shadow": "0 10px 40px rgba(12, 40, 24, 0.2)",
                "overlay_color": "rgba(12, 40, 24, 0.45)",
                "header_bg": "#f5faf5"
            }
        }),
        "dark_component_styles": json.dumps({
            "sidebar": {
                "bg": "#061410",
                "text": "#70b070",
                "active_bg": "#009c3b",
                "active_text": "#ffffff",
                "active_icon_stroke": "#ffffff",
                "hover_bg": "#0e2418",
                "hover_text": "#edeff5",
                "border_radius": "12px",
                "width": "245px",
                "font_size": "13.5px",
                "item_padding": "0px",
                "shadow": "2px 0 16px rgba(0, 0, 0, 0.3)"
            },
            "navbar": {
                "bg": "#0c1e14",
                "text": "#a0d4a0",
                "height": "54px",
                "shadow": "0 2px 6px rgba(0, 0, 0, 0.2)",
                "border_bottom": "3px solid #b89e00",
                "font_weight": "500"
            },
            "buttons_primary": {
                "bg": "#009c3b",
                "text": "#ffffff",
                "border_radius": "12px",
                "shadow": "0 3px 10px rgba(0, 156, 59, 0.4)",
                "hover_bg": "#00b848",
                "padding": "9px 22px",
                "font_weight": "400"
            },
            "buttons_default": {
                "bg": "#0e2418",
                "text": "#a0d4a0",
                "border_color": "#1a3e24",
                "border_radius": "12px",
                "shadow": "none",
                "height": "auto",
                "hover_bg": "#143020"
            },
            "buttons_secondary": {
                "bg": "#002776",
                "text": "#ffffff"
            },
            "cards": {
                "bg": "#0e2018",
                "subtle_accent": "#122616",
                "border_radius": "14px",
                "shadow": "rgba(149, 157, 165, 0.2) 0px 8px 24px",
                "border_color": "none",
                "padding": "22px",
                "hover_shadow": "0 6px 24px rgba(0, 0, 0, 0.4)"
            },
            "inputs": {
                "bg": "#000000",
                "border_color": "#1a3e24",
                "border_width": "1px",
                "border_style": "solid",
                "border_radius": "12px",
                "height": "38px",
                "focus_border": "#009c3b",
                "focus_shadow": "0 0 0 3px rgba(0, 156, 59, 0.2)",
                "padding": "8px 14px"
            },
            "page_head": {
                "bg": "#0c1e14",
                "height": "60px",
                "border_bottom": "1px solid #1a3e24",
                "title_font_size": "16px",
                "title_font_weight": "700"
            },
            "lists": {
                "row_hover_bg": "#0e2418",
                "row_border": "1px solid #14301e",
                "row_padding": "12px 18px",
                "header_bg": "#081610",
                "header_height": "40px",
                "header_font_weight": "600"
            },
            "modals": {
                "bg": "#0e2018",
                "border_radius": "16px",
                "shadow": "0 10px 40px rgba(0, 0, 0, 0.55)",
                "overlay_color": "rgba(0, 0, 0, 0.7)",
                "header_bg": "#0c1e14"
            }
        }),
        "dark_vars": json.dumps({
            "--bg-color": "#061410",
            "--fg-color": "#0c1e14",
            "--control-bg": "#0e2018",
            "--border-color": "#1a3e24",
            "--text-color": "#a0d4a0",
            "--text-muted": "#70b070",
            "--st-text": "#a0d4a0",
            "--st-muted-text": "#70b070",
            "--st-border": "#1a3e24",
            "--st-light-bg": "#0e2018",
        }),
        "custom_css": "",
    },

    # ─────────────────────────────────────────────────────────────────────
    # 6. South Korea — Modern, tech-forward, clean whites and blues
    # ─────────────────────────────────────────────────────────────────────
    {
        "doctype": "DCNET Theme Preset",
        "preset_key": "south_korea",
        "preset_name": "South Korea",
        "description": "Modern tech-forward design with clean whites and dynamic blue-red accents",
        "flag_colors": "linear-gradient(135deg, #003478 45%, #ffffff 45%, #ffffff 55%, #cd2e3a 55%)",
        "is_system": 1,
        "google_font_url": "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap",
        "primary_color": "#003478",
        "accent_color": "#cd2e3a",
        "secondary_color": "#0050b5",
        "dark_color": "#0a1a30",
        "light_bg_color": "#f9fafb",
        "text_color": "#111827",
        "muted_text_color": "#6b7280",
        "link_color": "#003478",
        "border_color": "#e5e7eb",
        "highlight_color": "#eff6ff",
        "font_family": "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
        "heading_font_family": "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
        "font_size_base": "13px",
        "heading_weight": "600",
        "line_height": "1.5",
        "border_radius": "6px",
        "card_shadow": "rgba(149, 157, 165, 0.2) 0px 8px 24px",
        "spacing_unit": "16px",
        "component_styles": json.dumps({
            "sidebar": {
                "bg": "#ffffff",
                "text": "#525252",
                "active_bg": "#003478",
                "active_text": "#ffffff",
                "active_icon_stroke": "#ffffff",
                "hover_bg": "#f3f4f6",
                "hover_text": "#525252",
                "border_radius": "8px",
                "width": "240px",
                "font_size": "13px",
                "item_padding": "0px",
                "shadow": "1px 0 4px rgba(0, 0, 0, 0.04)"
            },
            "navbar": {
                "bg": "#ffffff",
                "text": "#111827",
                "height": "52px",
                "shadow": "0 1px 2px rgba(0, 0, 0, 0.04)",
                "border_bottom": "1px solid #e5e7eb",
                "font_weight": "500"
            },
            "buttons_primary": {
                "bg": "#003478",
                "text": "#ffffff",
                "border_radius": "8px",
                "shadow": "0 1px 4px rgba(0, 52, 120, 0.2)",
                "hover_bg": "#0050b5",
                "padding": "8px 20px",
                "font_weight": "400"
            },
            "buttons_default": {
                "bg": "#EDEFF5",
                "text": "#1a1a2e",
                "border_color": "#e5e0d5",
                "border_radius": "8px",
                "shadow": "none",
                "height": "auto",
                "hover_bg": "#fffdf5"
            },
            "buttons_secondary": {
                "bg": "#0050b5",
                "text": "#ffffff"
            },
            "cards": {
                "bg": "#ffffff",
                "subtle_accent": "#eff6ff",
                "border_radius": "10px",
                "shadow": "rgba(149, 157, 165, 0.2) 0px 8px 24px",
                "border_color": "none",
                "padding": "20px",
                "hover_shadow": "0 4px 12px rgba(0, 0, 0, 0.08)"
            },
            "inputs": {
                "bg": "#edeff5",
                "border_color": "#e5e7eb",
                "border_width": "1px",
                "border_style": "solid",
                "border_radius": "8px",
                "height": "36px",
                "focus_border": "#003478",
                "focus_shadow": "0 0 0 3px rgba(0, 52, 120, 0.1)",
                "padding": "8px 12px"
            },
            "page_head": {
                "bg": "#ffffff",
                "height": "58px",
                "border_bottom": "1px solid #e5e7eb",
                "title_font_size": "16px",
                "title_font_weight": "600"
            },
            "lists": {
                "row_hover_bg": "#f9fafb",
                "row_border": "1px solid #f3f4f6",
                "row_padding": "11px 16px",
                "header_bg": "#f9fafb",
                "header_height": "40px",
                "header_font_weight": "600"
            },
            "modals": {
                "bg": "#ffffff",
                "border_radius": "12px",
                "shadow": "0 8px 30px rgba(0, 0, 0, 0.12)",
                "overlay_color": "rgba(17, 24, 39, 0.4)",
                "header_bg": "#f9fafb"
            }
        }),
        "dark_component_styles": json.dumps({
            "sidebar": {
                "bg": "#0a1220",
                "text": "#94a3b8",
                "active_bg": "#cd2e3a",
                "active_text": "#ffffff",
                "active_icon_stroke": "#ffffff",
                "hover_bg": "#111d30",
                "hover_text": "#edeff5",
                "border_radius": "8px",
                "width": "240px",
                "font_size": "13px",
                "item_padding": "0px",
                "shadow": "1px 0 4px rgba(0, 0, 0, 0.3)"
            },
            "navbar": {
                "bg": "#0e1826",
                "text": "#e2e8f0",
                "height": "52px",
                "shadow": "0 1px 2px rgba(0, 0, 0, 0.2)",
                "border_bottom": "1px solid #1e2d42",
                "font_weight": "500"
            },
            "buttons_primary": {
                "bg": "#cd2e3a",
                "text": "#ffffff",
                "border_radius": "8px",
                "shadow": "0 1px 4px rgba(0, 52, 120, 0.4)",
                "hover_bg": "#0050b5",
                "padding": "8px 20px",
                "font_weight": "400"
            },
            "buttons_default": {
                "bg": "#111d30",
                "text": "#94a3b8",
                "border_color": "#1e2d42",
                "border_radius": "8px",
                "shadow": "none",
                "height": "auto",
                "hover_bg": "#182640"
            },
            "buttons_secondary": {
                "bg": "#0050b5",
                "text": "#ffffff"
            },
            "cards": {
                "bg": "#0e1826",
                "subtle_accent": "#14202e",
                "border_radius": "10px",
                "shadow": "rgba(149, 157, 165, 0.2) 0px 8px 24px",
                "border_color": "none",
                "padding": "20px",
                "hover_shadow": "0 4px 12px rgba(0, 0, 0, 0.35)"
            },
            "inputs": {
                "bg": "#000000",
                "border_color": "#1e2d42",
                "border_width": "1px",
                "border_style": "solid",
                "border_radius": "8px",
                "height": "36px",
                "focus_border": "#003478",
                "focus_shadow": "0 0 0 3px rgba(0, 52, 120, 0.2)",
                "padding": "8px 12px"
            },
            "page_head": {
                "bg": "#0e1826",
                "height": "58px",
                "border_bottom": "1px solid #1e2d42",
                "title_font_size": "16px",
                "title_font_weight": "600"
            },
            "lists": {
                "row_hover_bg": "#111d30",
                "row_border": "1px solid #162236",
                "row_padding": "11px 16px",
                "header_bg": "#0a1018",
                "header_height": "40px",
                "header_font_weight": "600"
            },
            "modals": {
                "bg": "#0e1826",
                "border_radius": "12px",
                "shadow": "0 8px 30px rgba(0, 0, 0, 0.5)",
                "overlay_color": "rgba(0, 0, 0, 0.7)",
                "header_bg": "#0a1220"
            }
        }),
        "dark_vars": json.dumps({
            "--bg-color": "#0a1a30",
            "--fg-color": "#0e1826",
            "--control-bg": "#0e1826",
            "--border-color": "#1e2d42",
            "--text-color": "#e2e8f0",
            "--text-muted": "#94a3b8",
            "--st-text": "#e2e8f0",
            "--st-muted-text": "#94a3b8",
            "--st-border": "#1e2d42",
            "--st-light-bg": "#0e1826",
        }),
        "custom_css": "",
    },

    # ─────────────────────────────────────────────────────────────────────
    # 7. Pastel #1 — Soft blue-purple pastel with warm red accent
    # ─────────────────────────────────────────────────────────────────────
    {
        "doctype": "DCNET Theme Preset",
        "preset_key": "pastel1",
        "preset_name": "Pastel #1",
        "description": "Bộ màu pastel",
        "flag_colors": "linear-gradient(135deg, #2563eb 50%, #0ea5a4 50%)",
        "is_system": 0,
        "google_font_url": "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap",
        "primary_color": "#516ff0",
        "accent_color": "#CB2929",
        "secondary_color": "#a4baf5",
        "dark_color": "#0E161F",
        "light_bg_color": "#FEFEFE",
        "text_color": "#0f172a",
        "muted_text_color": "#64748b",
        "link_color": "#ECAD4B",
        "border_color": "#d3dae3",
        "highlight_color": "#eef4ff",
        "font_family": "",
        "heading_font_family": "",
        "font_size_base": "16",
        "heading_weight": "600",
        "line_height": "",
        "border_radius": "8",
        "card_shadow": "rgba(149, 157, 165, 0.2) 0px 8px 24px",
        "spacing_unit": "",
        "component_styles": json.dumps({
            "sidebar": {
                "bg": "#0E161F",
                "text": "#64748b",
                "active_bg": "#516ff0",
                "active_text": "#ffffff",
                "hover_bg": "#f2f2f2",
                "hover_text": "#0f172a"
            },
            "navbar": {
                "bg": "#FEFEFE",
                "text": "#0f172a",
                "border_bottom": "2px solid #CB2929"
            },
            "buttons_primary": {
                "bg": "#516ff0",
                "text": "#ffffff",
                "hover_bg": "#a4baf5"
            },
            "buttons_secondary": {
                "bg": "#a4baf5",
                "text": "#ffffff"
            },
            "buttons_default": {
                "bg": "#f2f2f2",
                "text": "#0f172a",
                "border_color": "#d3dae3",
                "hover_bg": "#eeeeee",
                "height": "auto"
            },
            "cards": {
                "bg": "#FEFEFE",
                "subtle_accent": "#eef4ff",
                "shadow": "rgba(149, 157, 165, 0.2) 0px 8px 24px"
            },
            "inputs": {
                "bg": "#f2f2f2",
                "border_color": "#d3dae3",
                "focus_border": "#516ff0",
                "height": "38px"
            },
            "lists": {
                "row_hover_bg": "#f2f2f2",
                "header_bg": "#eef4ff",
                "header_height": "40px"
            },
            "modals": {
                "bg": "#FEFEFE",
                "header_bg": "#eef4ff"
            }
        }),
        "dark_component_styles": json.dumps({
            "sidebar": {
                "bg": "#070c11",
                "text": "#94a3b8",
                "active_bg": "#CB2929",
                "active_text": "#ffffff"
            },
            "navbar": {
                "bg": "#101923",
                "text": "#e5e7eb",
                "border_bottom": "2px solid #8e1c1c"
            },
            "buttons_primary": {
                "bg": "#CB2929",
                "text": "#ffffff",
                "hover_bg": "#d84040"
            },
            "buttons_default": {
                "bg": "#070c11",
                "text": "#e5e7eb",
                "border_color": "#121c28",
                "hover_bg": "#101923",
                "height": "auto"
            },
            "cards": {
                "bg": "#0E161F",
                "subtle_accent": "#101923",
                "shadow": "rgba(149, 157, 165, 0.2) 0px 8px 24px"
            },
            "inputs": {
                "bg": "#070c11",
                "border_color": "#121c28",
                "height": "38px"
            },
            "lists": {
                "row_hover_bg": "#101923",
                "header_bg": "#070c11",
                "header_height": "40px"
            },
            "modals": {
                "bg": "#0E161F",
                "header_bg": "#070c11"
            }
        }),
        "dark_vars": json.dumps({
            "--bg-color": "#0E161F",
            "--fg-color": "#0E161F",
            "--control-bg": "#070c11",
            "--border-color": "#121c28",
            "--text-color": "#e5e7eb",
            "--text-muted": "#94a3b8",
            "--st-text": "#e5e7eb",
            "--st-muted-text": "#94a3b8",
            "--st-border": "#121c28",
            "--st-light-bg": "#101923",
        }),
        "custom_css": "",
    },

    # ─────────────────────────────────────────────────────────────────────
    # 8. Default — Polished neutral baseline, professional gray-blue
    # ─────────────────────────────────────────────────────────────────────
    {
        "doctype": "DCNET Theme Preset",
        "preset_key": "default",
        "preset_name": "Default",
        "description": "Polished neutral baseline with professional gray-blue tones",
        "flag_colors": "linear-gradient(135deg, #374151 50%, #3b82f6 50%)",
        "is_system": 1,
        "google_font_url": "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap",
        "primary_color": "#374151",
        "accent_color": "#3b82f6",
        "secondary_color": "#1f2937",
        "dark_color": "#111827",
        "light_bg_color": "#f9fafb",
        "text_color": "#111827",
        "muted_text_color": "#6b7280",
        "link_color": "#3b82f6",
        "border_color": "#e5e7eb",
        "highlight_color": "#eff6ff",
        "font_family": "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
        "heading_font_family": "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
        "font_size_base": "13px",
        "heading_weight": "600",
        "line_height": "1.5",
        "border_radius": "6px",
        "card_shadow": "rgba(149, 157, 165, 0.2) 0px 8px 24px",
        "spacing_unit": "16px",
        "component_styles": json.dumps({
            "sidebar": {
                "bg": "#111827",
                "text": "#525252",
                "active_bg": "#3b82f6",
                "active_text": "#ffffff",
                "active_icon_stroke": "#ffffff",
                "hover_bg": "#1f2937",
                "hover_text": "#edeff5",
                "border_radius": "6px",
                "width": "240px",
                "font_size": "13px",
                "item_padding": "0px",
                "shadow": "1px 0 6px rgba(0, 0, 0, 0.1)"
            },
            "navbar": {
                "bg": "#ffffff",
                "text": "#111827",
                "height": "52px",
                "shadow": "0 1px 2px rgba(0, 0, 0, 0.04)",
                "border_bottom": "1px solid #e5e7eb",
                "font_weight": "500"
            },
            "buttons_primary": {
                "bg": "#3b82f6",
                "text": "#ffffff",
                "border_radius": "6px",
                "shadow": "0 1px 3px rgba(59, 130, 246, 0.2)",
                "hover_bg": "#2563eb",
                "padding": "8px 18px",
                "font_weight": "400"
            },
            "buttons_default": {
                "bg": "#EDEFF5",
                "text": "#1a1a2e",
                "border_color": "#e5e0d5",
                "border_radius": "8px",
                "shadow": "none",
                "height": "auto",
                "hover_bg": "#f9fafb"
            },
            "buttons_secondary": {
                "bg": "#1f2937",
                "text": "#ffffff"
            },
            "cards": {
                "bg": "#ffffff",
                "subtle_accent": "#f3f4f6",
                "border_radius": "8px",
                "shadow": "rgba(149, 157, 165, 0.2) 0px 8px 24px",
                "border_color": "none",
                "padding": "20px",
                "hover_shadow": "0 4px 12px rgba(0, 0, 0, 0.08)"
            },
            "inputs": {
                "bg": "#edeff5",
                "border_color": "#e5e7eb",
                "border_width": "1px",
                "border_style": "solid",
                "border_radius": "6px",
                "height": "36px",
                "focus_border": "#3b82f6",
                "focus_shadow": "0 0 0 3px rgba(59, 130, 246, 0.1)",
                "padding": "8px 12px"
            },
            "page_head": {
                "bg": "#ffffff",
                "height": "56px",
                "border_bottom": "1px solid #e5e7eb",
                "title_font_size": "16px",
                "title_font_weight": "600"
            },
            "lists": {
                "row_hover_bg": "#f9fafb",
                "row_border": "1px solid #f3f4f6",
                "row_padding": "11px 16px",
                "header_bg": "#f9fafb",
                "header_height": "40px",
                "header_font_weight": "600"
            },
            "modals": {
                "bg": "#ffffff",
                "border_radius": "10px",
                "shadow": "0 6px 24px rgba(0, 0, 0, 0.12)",
                "overlay_color": "rgba(17, 24, 39, 0.4)",
                "header_bg": "#f9fafb"
            }
        }),
        "dark_component_styles": json.dumps({
            "sidebar": {
                "bg": "#0a0f1a",
                "text": "#6b7280",
                "active_bg": "#3b82f6",
                "active_text": "#ffffff",
                "active_icon_stroke": "#ffffff",
                "hover_bg": "#111827",
                "hover_text": "#edeff5",
                "border_radius": "6px",
                "width": "240px",
                "font_size": "13px",
                "item_padding": "0px",
                "shadow": "1px 0 6px rgba(0, 0, 0, 0.3)"
            },
            "navbar": {
                "bg": "#0f1520",
                "text": "#d1d5db",
                "height": "52px",
                "shadow": "0 1px 2px rgba(0, 0, 0, 0.2)",
                "border_bottom": "1px solid #1f2937",
                "font_weight": "500"
            },
            "buttons_primary": {
                "bg": "#3b82f6",
                "text": "#ffffff",
                "border_radius": "6px",
                "shadow": "0 1px 3px rgba(59, 130, 246, 0.3)",
                "hover_bg": "#60a5fa",
                "padding": "8px 18px",
                "font_weight": "400"
            },
            "buttons_default": {
                "bg": "#1f2937",
                "text": "#d1d5db",
                "border_color": "#374151",
                "border_radius": "6px",
                "shadow": "none",
                "height": "auto",
                "hover_bg": "#283548"
            },
            "buttons_secondary": {
                "bg": "#1f2937",
                "text": "#ffffff"
            },
            "cards": {
                "bg": "#111827",
                "subtle_accent": "#1a2333",
                "border_radius": "8px",
                "shadow": "rgba(149, 157, 165, 0.2) 0px 8px 24px",
                "border_color": "none",
                "padding": "20px",
                "hover_shadow": "0 4px 12px rgba(0, 0, 0, 0.35)"
            },
            "inputs": {
                "bg": "#000000",
                "border_color": "#1f2937",
                "border_width": "1px",
                "border_style": "solid",
                "border_radius": "6px",
                "height": "36px",
                "focus_border": "#3b82f6",
                "focus_shadow": "0 0 0 3px rgba(59, 130, 246, 0.15)",
                "padding": "8px 12px"
            },
            "page_head": {
                "bg": "#0f1520",
                "height": "56px",
                "border_bottom": "1px solid #1f2937",
                "title_font_size": "16px",
                "title_font_weight": "600"
            },
            "lists": {
                "row_hover_bg": "#1f2937",
                "row_border": "1px solid #1a2332",
                "row_padding": "11px 16px",
                "header_bg": "#0d1218",
                "header_height": "40px",
                "header_font_weight": "600"
            },
            "modals": {
                "bg": "#111827",
                "border_radius": "10px",
                "shadow": "0 6px 24px rgba(0, 0, 0, 0.5)",
                "overlay_color": "rgba(0, 0, 0, 0.7)",
                "header_bg": "#0f1520"
            }
        }),
        "dark_vars": json.dumps({
            "--bg-color": "#0a0f1a",
            "--fg-color": "#0f1520",
            "--control-bg": "#111827",
            "--border-color": "#1f2937",
            "--text-color": "#d1d5db",
            "--text-muted": "#6b7280",
            "--st-text": "#d1d5db",
            "--st-muted-text": "#6b7280",
            "--st-border": "#1f2937",
            "--st-light-bg": "#111827",
        }),
        "custom_css": "",
    },
]
