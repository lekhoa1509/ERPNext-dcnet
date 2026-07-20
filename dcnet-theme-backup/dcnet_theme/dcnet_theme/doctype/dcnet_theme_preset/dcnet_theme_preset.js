// DCNET Theme Preset — Live Preview
// Pure client-side rendering: reads form field values, renders inline-styled preview

frappe.ui.form.on("DCNET Theme Preset", {
  refresh(frm) {
    render_preview(frm);
  },

  after_save(frm) {
    // Reload page only if this preset is currently active so the user sees changes immediately
    frappe.call({
      method: "frappe.client.get_value",
      args: { doctype: "DCNET Theme Settings", fieldname: "active_preset" },
      callback(r) {
        if (r.message && r.message.active_preset === frm.doc.name) {
          frappe.show_alert({ message: __("Theme updated, reloading..."), indicator: "green" });
          setTimeout(() => window.location.reload(true), 1000);
        }
      },
    });
  },
  primary_color(frm) {
    render_preview(frm);
  },
  accent_color(frm) {
    render_preview(frm);
  },
  secondary_color(frm) {
    render_preview(frm);
  },
  dark_color(frm) {
    render_preview(frm);
  },
  light_bg_color(frm) {
    render_preview(frm);
  },
  text_color(frm) {
    render_preview(frm);
  },
  muted_text_color(frm) {
    render_preview(frm);
  },
  link_color(frm) {
    render_preview(frm);
  },
  border_color(frm) {
    render_preview(frm);
  },
  highlight_color(frm) {
    render_preview(frm);
  },
  font_family(frm) {
    render_preview(frm);
  },
  heading_font_family(frm) {
    render_preview(frm);
  },
  border_radius(frm) {
    render_preview(frm);
  },
  card_shadow(frm) {
    render_preview(frm);
  },
});

function render_preview(frm) {
  const wrapper = frm.fields_dict.preview_html;
  if (!wrapper || !wrapper.$wrapper) return;

  const c = {
    primary: frm.doc.primary_color || "#5B41C6",
    accent: frm.doc.accent_color || "#E91E63",
    secondary: frm.doc.secondary_color || "#6C757D",
    dark: frm.doc.dark_color || "#1B1B2F",
    lightBg: frm.doc.light_bg_color || "#F4F5F6",
    text: frm.doc.text_color || "#1C2126",
    muted: frm.doc.muted_text_color || "#6C757D",
    link: frm.doc.link_color || "#5B41C6",
    border: frm.doc.border_color || "#D9D9D9",
    highlight: frm.doc.highlight_color || "#FFF3CD",
  };

  const fontFamily =
    frm.doc.font_family || "'Inter', -apple-system, sans-serif";
  const headingFont = frm.doc.heading_font_family || fontFamily;
  const radius = frm.doc.border_radius || "8px";
  const shadow = frm.doc.card_shadow || "0 1px 4px rgba(0,0,0,0.08)";

  // WCAG contrast ratio calculation
  const contrast = calc_contrast(c.text, c.lightBg);
  const contrastOnPrimary = calc_contrast("#FFFFFF", c.primary);

  let contrastIcon, contrastLabel, contrastStyle;
  if (contrast >= 7) {
    contrastIcon = "\u2705";
    contrastLabel = `${contrast}:1 (AAA)`;
    contrastStyle = "color:#1a7a2e";
  } else if (contrast >= 4.5) {
    contrastIcon = "\u2705";
    contrastLabel = `${contrast}:1 (AA)`;
    contrastStyle = "color:#1a7a2e";
  } else if (contrast >= 3) {
    contrastIcon = "\u26A0\uFE0F";
    contrastLabel = `${contrast}:1 (below AA)`;
    contrastStyle = "color:#b8860b";
  } else {
    contrastIcon = "\u274C";
    contrastLabel = `${contrast}:1 (fail)`;
    contrastStyle = "color:#c0392b";
  }

  let btnContrastNote = "";
  if (contrastOnPrimary < 4.5) {
    btnContrastNote = `<span style="font-size:11px;color:#b8860b;margin-left:8px">\u26A0\uFE0F White on primary: ${contrastOnPrimary}:1</span>`;
  }

  const swatch = (color, label) =>
    `<span style="display:inline-flex;align-items:center;gap:6px;margin:0 12px 8px 0">` +
    `<span style="display:inline-block;width:28px;height:28px;border-radius:6px;background:${color};border:1px solid ${c.border};flex-shrink:0"></span>` +
    `<span style="font-size:12px;color:${c.text};font-family:${fontFamily};line-height:1.2">` +
    `${label}<br><span style="color:${c.muted};font-size:11px">${color}</span>` +
    `</span>` +
    `</span>`;

  const sidebarItem = (label, active) => {
    const bg = active ? c.primary : "transparent";
    const fg = active ? "#FFFFFF" : c.text;
    const fw = active ? "600" : "400";
    const rad = active ? radius : "0";
    return `<div style="padding:7px 12px;margin:2px 0;border-radius:${rad};background:${bg};color:${fg};font-size:10px;font-weight:${fw};font-family:${fontFamily};cursor:default;white-space:nowrap">${label}</div>`;
  };

  const html = `
<div style="background:${c.lightBg};border:1px solid ${c.border};border-radius:${radius};padding:20px;font-family:${fontFamily};max-width:780px">

	<!-- Color Palette -->
	<div style="margin-bottom:16px">
		<div style="font-size:11px;text-transform:uppercase;letter-spacing:0.8px;color:${c.muted};font-weight:600;margin-bottom:10px">Color Palette</div>
		<div style="display:flex;flex-wrap:wrap;align-items:flex-start">
			${swatch(c.primary, "Primary")}
			${swatch(c.accent, "Accent")}
			${swatch(c.secondary, "Secondary")}
			${swatch(c.dark, "Dark")}
			${swatch(c.lightBg, "Light BG")}
			${swatch(c.text, "Text")}
			${swatch(c.muted, "Muted")}
			${swatch(c.link, "Link")}
			${swatch(c.border, "Border")}
			${swatch(c.highlight, "Highlight")}
		</div>
	</div>

	<!-- UI Mockup -->
	<div style="font-size:11px;text-transform:uppercase;letter-spacing:0.8px;color:${c.muted};font-weight:600;margin-bottom:10px">UI Preview</div>
	<div style="display:flex;gap:0;border:1px solid ${c.border};border-radius:${radius};overflow:hidden;background:#FFFFFF;box-shadow:${shadow};min-height:220px">

		<!-- Sidebar -->
		<div style="width:170px;flex-shrink:0;background:${c.dark};padding:12px 10px;display:flex;flex-direction:column">
			<div style="font-size:13px;font-weight:700;color:#FFFFFF;font-family:${headingFont};margin-bottom:12px;padding:2px">DCNET Flow</div>
			${sidebarItem("Dashboard", false)}
			${sidebarItem("Sales Order", true)}
			${sidebarItem("Customers", false)}
			${sidebarItem("Reports", false)}
			<div style="margin-top:auto;padding:8px 12px;font-size:11px;color:rgba(255,255,255,0.45);border-top:1px solid rgba(255,255,255,0.1)">DCNET Theme</div>
		</div>

		<!-- Content -->
		<div style="flex:1;padding:16px 20px;display:flex;flex-direction:column;gap:14px;background:#FFFFFF">

			<!-- Title bar -->
			<div style="display:flex;align-items:center;justify-content:space-between">
				<div style="font-size:16px;font-weight:700;color:${c.text};font-family:${headingFont}">Sales Order</div>
				<div style="display:flex;gap:8px">
					<span style="display:inline-block;padding:6px 16px;border-radius:${radius};background:${c.primary};color:#FFFFFF;font-size:12px;font-weight:600;cursor:default">+ New</span>
					<span style="display:inline-block;padding:6px 16px;border-radius:${radius};background:transparent;color:${c.text};font-size:12px;font-weight:500;border:1px solid ${c.border};cursor:default">Filters</span>
				</div>
			</div>

			<!-- Cards row -->
			<div style="display:flex;gap:12px;flex-wrap:wrap">

				<!-- Card 1 -->
				<div style="flex:1;min-width:180px;padding:14px;border-radius:${radius};border:1px solid ${c.border};background:#FFFFFF;box-shadow:${shadow}">
					<div style="font-size:11px;color:${c.muted};text-transform:uppercase;letter-spacing:0.5px;margin-bottom:6px">Total Revenue</div>
					<div style="font-size:20px;font-weight:700;color:${c.text};font-family:${headingFont}">1,250,000</div>
					<div style="font-size:12px;color:${c.accent};margin-top:4px;font-weight:500">+12.5%</div>
				</div>

				<!-- Card 2 -->
				<div style="flex:1;min-width:180px;padding:14px;border-radius:${radius};border:1px solid ${c.border};background:#FFFFFF;box-shadow:${shadow}">
					<div style="font-size:11px;color:${c.muted};text-transform:uppercase;letter-spacing:0.5px;margin-bottom:6px">Open Orders</div>
					<div style="font-size:20px;font-weight:700;color:${c.text};font-family:${headingFont}">48</div>
					<div style="margin-top:6px">
						<span style="display:inline-block;padding:2px 8px;border-radius:20px;background:${c.highlight};color:${c.text};font-size:11px">3 overdue</span>
					</div>
				</div>
			</div>

			<!-- Table preview -->
			<div style="border:1px solid ${c.border};border-radius:${radius};overflow:hidden;font-size:12px">
				<div style="display:flex;background:${c.lightBg};border-bottom:1px solid ${c.border};padding:8px 12px;font-weight:600;color:${c.muted}">
					<span style="flex:2">Customer</span>
					<span style="flex:1">Status</span>
					<span style="flex:1;text-align:right">Amount</span>
				</div>
				<div style="display:flex;padding:8px 12px;border-bottom:1px solid ${c.border};color:${c.text}">
					<span style="flex:2"><span style="color:${c.link};cursor:pointer">Công ty A</span></span>
					<span style="flex:1"><span style="padding:2px 8px;border-radius:20px;background:${hex_alpha(c.primary, 0.12)};color:${c.primary};font-size:11px;font-weight:500">Active</span></span>
					<span style="flex:1;text-align:right;font-variant-numeric:tabular-nums">850,000</span>
				</div>
				<div style="display:flex;padding:8px 12px;color:${c.text}">
					<span style="flex:2"><span style="color:${c.link};cursor:pointer">Công ty B</span></span>
					<span style="flex:1"><span style="padding:2px 8px;border-radius:20px;background:${hex_alpha(c.accent, 0.12)};color:${c.accent};font-size:11px;font-weight:500">Draft</span></span>
					<span style="flex:1;text-align:right;font-variant-numeric:tabular-nums">400,000</span>
				</div>
			</div>
		</div>
	</div>

	<!-- WCAG Contrast -->
	<div style="margin-top:14px;display:flex;flex-wrap:wrap;align-items:center;gap:16px;font-size:12px;color:${c.muted};padding:10px 14px;background:#FFFFFF;border:1px solid ${c.border};border-radius:${radius}">
		<span><strong style="color:${c.text}">WCAG Contrast</strong></span>
		<span style="${contrastStyle};font-weight:500">Text / Background: ${contrastIcon} ${contrastLabel}</span>
		${btnContrastNote}
	</div>

</div>`;

  wrapper.$wrapper.html(html);
}

/* ── Contrast helpers ── */

function hex_to_rgb(hex) {
  hex = hex.replace(/^#/, "");
  if (hex.length === 3)
    hex = hex[0] + hex[0] + hex[1] + hex[1] + hex[2] + hex[2];
  const n = parseInt(hex, 16);
  return [(n >> 16) & 255, (n >> 8) & 255, n & 255];
}

function relative_luminance(hex) {
  const [r, g, b] = hex_to_rgb(hex).map((v) => {
    v = v / 255;
    return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4);
  });
  return 0.2126 * r + 0.7152 * g + 0.0722 * b;
}

function calc_contrast(fg, bg) {
  const l1 = relative_luminance(fg);
  const l2 = relative_luminance(bg);
  const lighter = Math.max(l1, l2);
  const darker = Math.min(l1, l2);
  return Math.round(((lighter + 0.05) / (darker + 0.05)) * 10) / 10;
}

function hex_alpha(hex, alpha) {
  const [r, g, b] = hex_to_rgb(hex);
  return `rgba(${r},${g},${b},${alpha})`;
}
