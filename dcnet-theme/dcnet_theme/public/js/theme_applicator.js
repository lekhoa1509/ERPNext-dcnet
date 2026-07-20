/**
 * DCNET Theme Applicator — injects theme CSS from bootinfo into <head>.
 *
 * The CSS comes via bootinfo.dcnet_theme_css (set by boot.py).
 * This ensures the theme is always fresh after a theme switch,
 * unlike a static CSS file which gets browser-cached.
 *
 * Transition scoping: adds .theme-transitioning to <body> only during
 * active theme switches so color transitions don't fire on page load.
 *
 * Per-company override: if bootinfo.dcnet_theme_company_overrides exists,
 * listens for company default changes and swaps theme CSS accordingly.
 */
(function () {
  const STYLE_ID = "dcnet-theme-css";
  const TRANSITION_CLASS = "theme-transitioning";
  const TRANSITION_DURATION = 500; // ms — matches CSS 0.3s + buffer
  const SAFETY_TIMEOUT = 1000; // ms — guaranteed cleanup

  /** Track whether the initial theme has been applied (page load). */
  let initialApplyDone = false;

  /** Track the currently active preset key. */
  let currentPresetKey = null;

  /** Remove the transitioning class from body. */
  function removeTransitionClass() {
    document.body && document.body.classList.remove(TRANSITION_CLASS);
  }

  /**
   * Enable transitions temporarily during a theme switch.
   * Adds .theme-transitioning to <body>, removes after TRANSITION_DURATION.
   * Safety timeout at SAFETY_TIMEOUT guarantees removal even on failure.
   */
  function enableTransitions() {
    if (!document.body) return;
    document.body.classList.add(TRANSITION_CLASS);

    // Normal removal after transitions complete
    setTimeout(removeTransitionClass, TRANSITION_DURATION);
    // Safety net — always remove even if something goes wrong
    setTimeout(removeTransitionClass, SAFETY_TIMEOUT);
  }

  /**
   * Apply theme CSS to the page.
   * @param {string} css — the CSS string to inject
   * @param {boolean} isSwitch — true when called from a theme switch (not page load)
   */
  function applyCSS(css, isSwitch) {
    if (!css) return;

    // Enable transitions only for active theme switches, not initial page load
    if (isSwitch && initialApplyDone) {
      enableTransitions();
    }

    // Remove existing theme style if present
    let style = document.getElementById(STYLE_ID);
    if (style) {
      style.textContent = css;
    } else {
      style = document.createElement("style");
      style.id = STYLE_ID;
      style.textContent = css;
      document.head.appendChild(style);
    }

    initialApplyDone = true;

    // Re-apply desktop icon customizations after theme CSS change.
    // Theme changes can reset inline styles on .icon-container elements.
    setTimeout(applyDesktopCustomizations, 0);
  }

  /**
   * Apply theme from bootinfo (page load / SPA navigation).
   * @param {boolean} isSwitch — true for active theme switch
   */
  function applyTheme(isSwitch) {
    const css = frappe.boot && frappe.boot.dcnet_theme_css;
    if (!css) return;

    currentPresetKey = frappe.boot.dcnet_theme_preset || null;
    applyCSS(css, isSwitch);
  }

  /**
   * Resolve the correct preset key for a given company using the overrides map.
   * @param {string} company — company name
   * @returns {string|null} — preset key or null (use global)
   */
  function resolvePresetForCompany(company) {
    var overrides = frappe.boot && frappe.boot.dcnet_theme_company_overrides;
    if (!overrides || !company) return null;
    return overrides[company] || null;
  }

  /**
   * Handle company context switch: fetch and apply the correct theme CSS.
   * Called when the user changes their default company.
   * @param {string} company — the new company name
   */
  function onCompanySwitch(company) {
    if (!company) return;

    var targetPreset = resolvePresetForCompany(company);

    // If no override for this company, we need the global preset
    // If the target is the same as current, no action needed
    if (targetPreset && targetPreset === currentPresetKey) return;
    if (!targetPreset && !frappe.boot.dcnet_theme_company_overrides) return;

    // Fetch CSS for the target company from server
    frappe.call({
      method: "dcnet_theme.dcnet_theme.boot.get_theme_css_for_company",
      args: { company: company },
      async: true,
      callback: function (r) {
        if (!r || !r.message) return;
        var result = r.message;
        if (result.css) {
          currentPresetKey = result.preset_key;
          // Update bootinfo so subsequent SPA navigations use the right CSS
          frappe.boot.dcnet_theme_css = result.css;
          frappe.boot.dcnet_theme_preset = result.preset_key;
          applyCSS(result.css, true);
        }
      },
    });
  }

  // Apply on page load (no transitions)
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", function () {
      applyTheme(false);
    });
  } else {
    applyTheme(false);
  }

  // ---------------------------------------------------------------------------
  // Desktop icon customizations: bg_color + custom_label
  // ---------------------------------------------------------------------------

  /**
   * Apply bg_color from Desktop Icon records to .icon-container elements.
   *
   * Frappe only uses bg_color in the letter-fallback render path. When an
   * icon_image or a pre-built app asset is displayed, the background color
   * is never set. This function forces the color onto .icon-container
   * regardless of which render path was used.
   */
  function applyDesktopIconColors(root) {
    var icons = frappe.boot && frappe.boot.desktop_icons;
    if (!icons || !icons.length) return;

    var isSolid = frappe.boot.desktop_icon_style === "Solid";
    var scope = root || document;
    var themePrimary = getComputedStyle(document.documentElement)
      .getPropertyValue("--primary").trim() || null;

    icons.forEach(function (icon) {
      var safeId = icon.label.replace(/\\/g, "\\\\").replace(/"/g, '\\"');
      // querySelectorAll to cover icons in folder thumbnails AND modal
      var iconEls = scope.querySelectorAll('.desktop-icon[data-id="' + safeId + '"]');
      iconEls.forEach(function (iconEl) {
        var el = iconEl.querySelector(":scope > .icon-container");
        if (!el) return;

        // Apply bg_color — if not set, fall back to theme primary color
        var bgSource = icon.bg_color || (!icon.bg_color && themePrimary ? themePrimary : null);
        if (bgSource) {
          var hexColor =
            (frappe.utils.desktop_pallete && frappe.utils.desktop_pallete[bgSource]) ||
            (/^#[0-9A-Fa-f]{3,8}$/.test(bgSource) ? bgSource : null);
          if (hexColor) {
            el.style.backgroundColor = isSolid ? hexColor : hexColor + "1A";
          }
        }

        // Apply icon_color — default to #ffffff when not set
        var iconColor = (icon.icon_color && /^#[0-9A-Fa-f]{3,8}$/.test(icon.icon_color))
          ? icon.icon_color
          : "#ffffff";
        var svg = el.querySelector("svg");
        if (svg) {
          svg.style.setProperty("--icon-stroke", iconColor);
          svg.style.color = iconColor;
          svg.style.stroke = iconColor;
        }
      });
    });
  }

  /**
   * Apply custom_label to desktop icon titles.
   *
   * If a Desktop Icon record has a custom_label value (injected by boot.py),
   * replace the visible .icon-title text with it. Falls back to label if unset.
   */
  function applyDesktopIconLabels() {
    var icons = frappe.boot && frappe.boot.desktop_icons;
    if (!icons || !icons.length) return;

    icons.forEach(function (icon) {
      if (!icon.custom_label) return;

      var selector =
        '.desktop-icon[data-id="' +
        icon.label.replace(/\\/g, "\\\\").replace(/"/g, '\\"') +
        '"] .icon-title';
      var el = document.querySelector(selector);
      if (!el) return;

      el.textContent = icon.custom_label;
      el.setAttribute("data-original-title", icon.custom_label);
    });
  }

  /** Run all desktop icon customizations in one pass. */
  function applyDesktopCustomizations() {
    applyDesktopIconColors();
    applyDesktopIconLabels();
  }

  // Patch desktopPage render method so applyDesktopCustomizations runs immediately after
  // icons are added to the DOM — covers both the async first-load path (frappe.call
  // callback) and the synchronous SPA-navigation path.
  // Frappe v16 stable renamed `render()` → `update()` on the DesktopPage class. Handle both.
  function patchDesktopRender() {
    var desktopPage = frappe.pages && frappe.pages["desktop"] && frappe.pages["desktop"].desktop_page;
    if (!desktopPage || desktopPage._dcnet_colorPatched) return;

    var methodName = typeof desktopPage.render === "function" ? "render"
                   : typeof desktopPage.update === "function" ? "update"
                   : null;
    if (!methodName) return;

    desktopPage._dcnet_colorPatched = true;
    var origMethod = desktopPage[methodName].bind(desktopPage);
    desktopPage[methodName] = function () {
      var ret = origMethod.apply(this, arguments);
      applyDesktopCustomizations();
      return ret;
    };
  }

  // Re-apply after Frappe route change (SPA navigation) — no transitions
  if (typeof frappe !== "undefined") {
    $(document).on("page-change", function () {
      applyTheme(false);
      patchDesktopRender();
    });

    // Icons inside groups are rendered lazily in a modal when the group is clicked.
    // Re-apply colors scoped to the modal body after it finishes showing.
    $(document).on("shown.bs.modal", ".desktop-modal", function () {
      var modalBody = this.querySelector(".desktop-modal-body");
      if (modalBody) applyDesktopIconColors(modalBody);
    });

    // Listen for company default changes (Frappe's default switcher)
    // frappe.defaults triggers this event when user changes their default company
    $(document).on("change:default:Company", function (_e, company) {
      onCompanySwitch(company);
    });

    // Also hook into frappe.xcall for set_default which Frappe uses internally
    // when user picks a different company from the sidebar company switcher
    var _origSetDefault = frappe.defaults && frappe.defaults.set_default;
    if (_origSetDefault) {
      frappe.defaults.set_default = function (key, value) {
        var result = _origSetDefault.apply(this, arguments);
        if (key === "Company" && value) {
          onCompanySwitch(value);
        }
        return result;
      };
    }
  }

  // Patch frappe.utils.desktop_pallete to support direct hex color values
  // stored in Desktop Icon.bg_color (Color fieldtype returns hex e.g. "#CB2929")
  function patchDesktopPalette() {
    if (
      !frappe ||
      !frappe.utils ||
      !frappe.utils.desktop_pallete ||
      frappe.utils._dcnet_palette_patched
    )
      return;
    frappe.utils._dcnet_palette_patched = true;
    frappe.utils.desktop_pallete = new Proxy(frappe.utils.desktop_pallete, {
      get(target, key) {
        if (key in target) return target[key];
        if (typeof key === "string" && /^#[0-9A-Fa-f]{3,8}$/.test(key))
          return key;
        return undefined;
      },
    });
  }

  $(document).on("page-change", patchDesktopPalette);
  if (typeof frappe !== "undefined" && frappe.utils && frappe.utils.desktop_pallete) {
    patchDesktopPalette();
  }

  // Expose for programmatic theme switching
  // Usage: window.DCNetTheme.applyWithTransition() after updating frappe.boot.dcnet_theme_css
  window.DCNetTheme = {
    /** Re-apply current boot CSS with smooth transitions. */
    applyWithTransition: function () {
      applyTheme(true);
    },
    /** Re-apply desktop icon bg_color and custom_label (called after data refresh). */
    applyDesktopCustomizations: applyDesktopCustomizations,
    /** Inject arbitrary CSS with transitions (for live preview). */
    applyCSS: function (css) {
      if (!css) return;
      enableTransitions();
      var style = document.getElementById(STYLE_ID);
      if (style) {
        style.textContent = css;
      } else {
        style = document.createElement("style");
        style.id = STYLE_ID;
        style.textContent = css;
        document.head.appendChild(style);
      }
    },
    /** Switch theme for a specific company (programmatic). */
    switchCompany: function (company) {
      onCompanySwitch(company);
    },
    /** Get the currently active preset key. */
    getCurrentPreset: function () {
      return currentPresetKey;
    },
  };
})();
