// DCNET Theme Settings — Live Preview Panel
// Renders color swatches + mini UI mockup when the user changes the preset dropdown.

frappe.ui.form.on("DCNET Theme Settings", {
  refresh(frm) {
    frm._preview_rendered = false;
    render_preview(frm);
  },

  active_preset(frm) {
    render_preview(frm);
  },

  after_save(frm) {
    frappe.show_alert({ message: __("Theme updated, reloading..."), indicator: "green" });
    setTimeout(() => window.location.reload(true), 1000);
  },
});

function render_preview(frm) {
  const wrapper = frm.fields_dict.theme_preview_html;
  if (!wrapper || !wrapper.$wrapper) return;

  const preset_name = frm.doc.active_preset;
  if (!preset_name) {
    wrapper.$wrapper.html(
      '<div style="padding:24px;color:var(--text-muted);text-align:center;">' +
        "Select a preset above to see a live preview." +
        "</div>",
    );
    return;
  }

  // Show loading state
  wrapper.$wrapper.html(
    '<div style="padding:24px;text-align:center;">' +
      '<span class="text-muted">Loading preview...</span>' +
      "</div>",
  );

  frappe.call({
    method:
      "dcnet_theme.dcnet_theme.doctype.dcnet_theme_settings.dcnet_theme_settings.get_preset_preview",
    args: { preset_name: preset_name },
    callback(r) {
      if (r.message) {
        render_preview_panel(wrapper.$wrapper, r.message);
      }
    },
  });
}

/**
 * Render the full preview panel with color swatches + mini UI mockup.
 */
function render_preview_panel($container, data) {
  const cs = data.component_styles || {};
  const sidebar = cs.sidebar || {};
  const navbar = cs.navbar || {};
  const btn_primary = cs.buttons_primary || {};
  const btn_default = cs.buttons_default || {};
  const cards = cs.cards || {};
  const inputs = cs.inputs || {};

  // Color palette entries
  const colors = [
    { label: "Primary", value: data.primary_color, field: "primary_color" },
    { label: "Accent", value: data.accent_color, field: "accent_color" },
    {
      label: "Secondary",
      value: data.secondary_color,
      field: "secondary_color",
    },
    { label: "Dark", value: data.dark_color, field: "dark_color" },
    { label: "Light BG", value: data.light_bg_color, field: "light_bg_color" },
    { label: "Text", value: data.text_color, field: "text_color" },
    { label: "Muted", value: data.muted_text_color, field: "muted_text_color" },
    { label: "Link", value: data.link_color, field: "link_color" },
    { label: "Border", value: data.border_color, field: "border_color" },
    {
      label: "Highlight",
      value: data.highlight_color,
      field: "highlight_color",
    },
  ];

  // Build color swatches HTML
  let swatches_html = colors
    .filter((c) => c.value)
    .map(
      (c) =>
        `<div style="display:flex;flex-direction:column;align-items:center;gap:4px;">
        <div style="width:44px;height:44px;border-radius:8px;background:${c.value};
          border:1px solid rgba(0,0,0,0.1);box-shadow:0 1px 3px rgba(0,0,0,0.08);"></div>
        <span style="font-size:10px;color:var(--text-muted);font-weight:500;">${c.label}</span>
        <span style="font-size:9px;color:var(--text-light);font-family:monospace;">${c.value}</span>
      </div>`,
    )
    .join("");

  // Flag gradient bar
  const flag_html = data.flag_colors
    ? `<div style="height:6px;border-radius:3px;background:${data.flag_colors};margin-bottom:8px;"></div>`
    : "";

  // Mini UI mockup
  const mockup_html = build_mockup_html(
    data,
    sidebar,
    navbar,
    btn_primary,
    btn_default,
    cards,
    inputs,
  );

  const html = `
    <div class="dcnet-theme-preview" style="border:1px solid var(--border-color);border-radius:8px;
      overflow:hidden;background:var(--fg-color, #fff);">

      <!-- Header -->
      <div style="padding:12px 16px;border-bottom:1px solid var(--border-color);
        display:flex;align-items:center;gap:12px;">
        ${flag_html ? `<div style="flex:0 0 60px;">${flag_html}</div>` : ""}
        <div>
          <div style="font-weight:600;font-size:14px;">${frappe.utils.escape_html(data.preset_name || "")}</div>
          <div style="font-size:11px;color:var(--text-muted);">${frappe.utils.escape_html(data.description || "")}</div>
        </div>
        <div style="margin-left:auto;font-size:11px;color:var(--text-muted);">
          ${data.font_family ? data.font_family.split(",")[0].replace(/'/g, "") : ""}
          &middot; ${data.font_size_base || "13px"}
          &middot; radius ${data.border_radius || "8px"}
        </div>
      </div>

      <!-- Color Swatches -->
      <div style="padding:16px;border-bottom:1px solid var(--border-color);">
        <div style="font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:0.5px;
          color:var(--text-muted);margin-bottom:10px;">Color Palette</div>
        <div style="display:flex;gap:14px;flex-wrap:wrap;">
          ${swatches_html}
        </div>
      </div>

      <!-- Mini UI Mockup -->
      <div style="padding:16px;">
        <div style="font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:0.5px;
          color:var(--text-muted);margin-bottom:10px;">UI Preview</div>
        ${mockup_html}
      </div>
    </div>
  `;

  $container.html(html);
}

/**
 * Build a mini UI mockup showing sidebar, navbar, card, buttons, and input.
 */
function build_mockup_html(
  data,
  sidebar,
  navbar,
  btn_primary,
  btn_default,
  cards,
  inputs,
) {
  // Sidebar items
  const sidebar_items = [
    { label: "Dashboard", icon: "&#x2302;", active: false },
    { label: "Sales Order", icon: "&#x1F4C4;", active: true },
    { label: "Customers", icon: "&#x1F465;", active: false },
    { label: "Reports", icon: "&#x1F4CA;", active: false },
  ];

  const sidebar_items_html = sidebar_items
    .map((item) => {
      const bg = item.active
        ? sidebar.active_bg || data.primary_color
        : "transparent";
      const text_color = item.active
        ? sidebar.active_text || "#fff"
        : sidebar.text || "#ccc";
      const radius = sidebar.border_radius || data.border_radius || "6px";
      return `<div style="padding:${sidebar.item_padding || "8px 12px"};border-radius:${radius};
        background:${bg};color:${text_color};font-size:${sidebar.font_size || "12px"};
        cursor:default;display:flex;align-items:center;gap:6px;
        ${item.active ? "font-weight:500;" : ""}">
        <span style="font-size:12px;">${item.icon}</span> ${item.label}
      </div>`;
    })
    .join("");

  return `
    <div style="display:flex;border-radius:${data.border_radius || "8px"};overflow:hidden;
      border:1px solid ${data.border_color || "#e5e5e5"};height:220px;
      box-shadow:${data.card_shadow || "0 2px 8px rgba(0,0,0,0.06)"};">

      <!-- Sidebar -->
      <div style="width:160px;flex-shrink:0;background:${sidebar.bg || data.dark_color || "#1a1a2e"};
        padding:10px 8px;display:flex;flex-direction:column;gap:2px;
        ${sidebar.shadow ? "box-shadow:" + sidebar.shadow + ";" : ""}">
        <div style="color:${sidebar.text || "#ccc"};font-size:10px;font-weight:600;
          text-transform:uppercase;letter-spacing:0.5px;padding:4px 12px 8px;opacity:0.6;">
          Modules
        </div>
        ${sidebar_items_html}
      </div>

      <!-- Main content area -->
      <div style="flex:1;display:flex;flex-direction:column;background:${data.light_bg_color || "#f8f8f8"};">

        <!-- Navbar mockup -->
        <div style="height:${navbar.height || "40px"};background:${navbar.bg || "#fff"};
          border-bottom:${navbar.border_bottom || "1px solid " + (data.border_color || "#e5e5e5")};
          display:flex;align-items:center;padding:0 12px;gap:8px;flex-shrink:0;
          ${navbar.shadow ? "box-shadow:" + navbar.shadow + ";" : ""}">
          <span style="font-weight:${navbar.font_weight || "600"};font-size:13px;
            color:${navbar.text || data.text_color || "#333"};">
            Sales Order
          </span>
          <span style="margin-left:auto;font-size:10px;color:${data.muted_text_color || "#999"};">
            SO-2026-00042
          </span>
        </div>

        <!-- Card + buttons mockup -->
        <div style="padding:12px;flex:1;overflow:hidden;">
          <div style="background:${cards.bg || "#fff"};border-radius:${cards.border_radius || data.border_radius || "8px"};
            padding:${cards.padding || "14px"};
            border:1px solid ${cards.border_color || data.border_color || "#e5e5e5"};
            box-shadow:${cards.shadow || "none"};">

            <!-- Form fields mockup -->
            <div style="display:flex;gap:10px;margin-bottom:12px;">
              <div style="flex:1;">
                <div style="font-size:10px;color:${data.muted_text_color || "#999"};margin-bottom:3px;">Customer</div>
                <div style="height:${inputs.height || "28px"};background:${inputs.bg || "#fff"};
                  border:1px solid ${inputs.border_color || data.border_color || "#ddd"};
                  border-radius:${inputs.border_radius || "6px"};padding:${inputs.padding || "4px 8px"};
                  font-size:11px;color:${data.text_color || "#333"};display:flex;align-items:center;">
                  Công ty A
                </div>
              </div>
              <div style="flex:1;">
                <div style="font-size:10px;color:${data.muted_text_color || "#999"};margin-bottom:3px;">Status</div>
                <div style="display:inline-block;padding:2px 10px;border-radius:10px;font-size:10px;
                  font-weight:500;background:${data.highlight_color || "#e8f5e9"};
                  color:${data.primary_color || "#4caf50"};">
                  To Deliver
                </div>
              </div>
            </div>

            <!-- Buttons -->
            <div style="display:flex;gap:8px;align-items:center;">
              <div style="padding:${btn_primary.padding || "5px 14px"};
                background:${btn_primary.bg || data.primary_color || "#1a73e8"};
                color:${btn_primary.text || "#fff"};
                border-radius:${btn_primary.border_radius || data.border_radius || "6px"};
                font-size:11px;font-weight:${btn_primary.font_weight || "600"};
                cursor:default;display:inline-block;
                ${btn_primary.shadow ? "box-shadow:" + btn_primary.shadow + ";" : ""}">
                Submit
              </div>
              <div style="padding:${btn_default.padding || "5px 14px"};
                background:${btn_default.bg || "#fff"};
                color:${btn_default.text || data.text_color || "#333"};
                border:1px solid ${btn_default.border_color || data.border_color || "#ddd"};
                border-radius:${btn_default.border_radius || data.border_radius || "6px"};
                font-size:11px;cursor:default;display:inline-block;">
                Save
              </div>
              <span style="font-size:10px;color:${data.link_color || data.primary_color || "#1a73e8"};
                margin-left:4px;cursor:default;text-decoration:underline;">
                Add Comment
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  `;
}
