frappe.pages["theme-gallery"].on_page_load = function (wrapper) {
  const page = frappe.ui.make_app_page({
    parent: wrapper,
    title: "Theme Gallery",
    single_column: true,
  });

  page.set_secondary_action("Settings", () => {
    frappe.set_route("app", "dcnet-theme-settings");
  });

  $(`
		<div class="theme-gallery-container" style="padding: 16px;">
			<p class="text-muted" style="margin-bottom: 24px;">
				Choose a theme for your workspace
			</p>
			<div class="theme-gallery-grid"></div>
		</div>
	`).appendTo(page.body);

  // Older Frappe versions don't reliably fire on_page_show on first nav from URL.
  // Load presets here so the grid renders on first visit too.
  load_presets($(page.body).find(".theme-gallery-grid"));
  $(wrapper).data("dcnet-just-loaded", true);
};

frappe.pages["theme-gallery"].on_page_show = function (wrapper) {
  // Skip first show — on_page_load already loaded — but refresh on subsequent revisits.
  if ($(wrapper).data("dcnet-just-loaded")) {
    $(wrapper).data("dcnet-just-loaded", false);
    return;
  }
  const $grid = $(wrapper).find(".theme-gallery-grid");
  if ($grid.length) {
    load_presets($grid);
  }
};

function load_presets($grid) {
  $grid.html(`
		<div class="skeleton-grid" style="display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:20px;">
			${Array(6).fill('<div style="height:220px;background:var(--gray-100);border-radius:8px;animation:pulse 1.5s ease-in-out infinite;"></div>').join("")}
		</div>
		<style>@keyframes pulse{0%,100%{opacity:1}50%{opacity:0.5}}</style>
	`);

  frappe.call({
    method: "frappe.client.get_list",
    args: {
      doctype: "DCNET Theme Preset",
      fields: [
        "name",
        "preset_name",
        "preset_key",
        "description",
        "flag_colors",
        "is_system",
        "primary_color",
        "accent_color",
        "secondary_color",
        "dark_color",
        "light_bg_color",
      ],
      order_by: "preset_name asc",
      limit_page_length: 0,
    },
    callback: function (r) {
      if (!r.message || r.message.length === 0) {
        $grid.html(`
					<div style="text-align:center;padding:60px 20px;">
						<p class="text-muted">No presets installed. Run <code>bench migrate</code> to seed presets.</p>
					</div>
				`);
        return;
      }

      frappe.call({
        method: "frappe.client.get_value",
        args: {
          doctype: "DCNET Theme Settings",
          fieldname: "active_preset",
        },
        callback: function (settings_r) {
          const active = settings_r.message?.active_preset || "";
          render_cards($grid, r.message, active);
        },
      });
    },
  });
}

function render_cards($grid, presets, active_key) {
  const cards = presets.map((p) => {
    const is_active = p.preset_key === active_key;
    const swatches = [
      p.primary_color,
      p.accent_color,
      p.secondary_color,
      p.dark_color,
      p.light_bg_color,
    ]
      .filter(Boolean)
      .map(
        (c) =>
          `<div class="swatch" style="background:${c};" aria-label="${c}" title="${c}"></div>`,
      )
      .join("");

    return `
			<div class="theme-card ${is_active ? "active" : ""}"
				 data-preset="${p.preset_key}"
				 role="button"
				 aria-label="${p.preset_name} theme"
				 tabindex="0">
				<div class="flag-stripe" style="background:${p.flag_colors || "var(--gray-300)"};"></div>
				<div class="card-body">
					<div class="card-header-row">
						<h3 class="preset-name">${p.preset_name}</h3>
						${is_active ? '<span class="active-badge">&#10003; Active</span>' : ""}
					</div>
					<div class="swatches">${swatches}</div>
					<p class="description">${p.description || ""}</p>
					<button class="btn ${is_active ? "btn-default" : "btn-primary"} btn-sm activate-btn"
							${is_active ? "disabled" : ""}
							data-preset="${p.preset_key}">
						${is_active ? "Active" : "Activate"}
					</button>
				</div>
			</div>
		`;
  });

  $grid.html(`
		<div class="preset-grid">${cards.join("")}</div>
		<style>
			.preset-grid {
				display: grid;
				grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
				gap: 20px;
			}
			.theme-card {
				border: 2px solid var(--border-color, #e5e7eb);
				border-radius: 12px;
				overflow: hidden;
				background: var(--card-bg, #fff);
				transition: border-color 0.2s, box-shadow 0.2s;
				cursor: pointer;
			}
			.theme-card:hover {
				border-color: var(--gray-400);
				box-shadow: 0 4px 12px rgba(0,0,0,0.08);
			}
			.theme-card:focus-visible {
				outline: 2px solid var(--primary);
				outline-offset: 2px;
			}
			.theme-card.active {
				border-color: var(--primary, #374151);
				box-shadow: 0 0 0 1px var(--primary, #374151);
			}
			.flag-stripe {
				height: 8px;
				width: 100%;
			}
			.card-body {
				padding: 20px;
			}
			.card-header-row {
				display: flex;
				align-items: center;
				justify-content: space-between;
				margin-bottom: 12px;
			}
			.preset-name {
				margin: 0;
				font-size: 16px;
				font-weight: 600;
			}
			.active-badge {
				background: var(--green-100, #dcfce7);
				color: var(--green-700, #15803d);
				padding: 2px 10px;
				border-radius: 12px;
				font-size: 12px;
				font-weight: 500;
			}
			.swatches {
				display: flex;
				gap: 6px;
				margin-bottom: 12px;
			}
			.swatch {
				width: 28px;
				height: 28px;
				border-radius: 50%;
				border: 2px solid rgba(0,0,0,0.08);
			}
			.description {
				color: var(--text-muted);
				font-size: 13px;
				margin-bottom: 16px;
				min-height: 20px;
			}
			.activate-btn {
				min-width: 100px;
				min-height: 38px;
			}
			@media (max-width: 768px) {
				.preset-grid {
					grid-template-columns: 1fr;
				}
			}
			@media (min-width: 769px) and (max-width: 1199px) {
				.preset-grid {
					grid-template-columns: repeat(2, 1fr);
				}
			}
		</style>
	`);

  // Click handler for Activate button
  $grid.find(".activate-btn:not([disabled])").on("click", function (e) {
    e.stopPropagation();
    const preset_key = $(this).data("preset");
    activate_theme(preset_key);
  });

  // Keyboard support: Enter/Space on card
  $grid.find(".theme-card").on("keydown", function (e) {
    if (e.key === "Enter" || e.key === " ") {
      e.preventDefault();
      const preset_key = $(this).data("preset");
      if (preset_key !== active_key) {
        activate_theme(preset_key);
      }
    }
  });
}

function activate_theme(preset_key) {
  frappe.show_alert({
    message: `Applying theme...`,
    indicator: "blue",
  });

  frappe.call({
    method:
      "dcnet_theme.dcnet_theme.doctype.dcnet_theme_settings.dcnet_theme_settings.activate_preset",
    args: { preset_key },
    callback: function () {
      frappe.show_alert({
        message: "Theme applied! Refreshing...",
        indicator: "green",
      });
      // Hard reload to bypass browser CSS cache
      setTimeout(() => window.location.reload(true), 1500);
    },
    error: function () {
      frappe.show_alert({
        message: "Failed to activate theme",
        indicator: "red",
      });
    },
  });
}
