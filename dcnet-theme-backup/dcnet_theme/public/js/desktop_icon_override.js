/**
 * Patches to make Desktop Icon custom image fields (logo_url, icon_image, icon)
 * work correctly on the Desk home page and sidebar header.
 *
 * ROOT CAUSE — F5 resets icons:
 *   DesktopPage.sync_layout() sets frappe.desktop_icons from #desktop-layout, a
 *   server-rendered snapshot of the Desktop Layout doctype. The snapshot is stale
 *   (saved before the user set logo_url), so logo_url is null. The template then
 *   renders the default SVG instead of the custom image.
 *
 * ROOT CAUSE — icon field ignored:
 *   desktop_icon.html only uses: SVG-on-disk → logo_url/icon_image → letter-circle.
 *   The icon field (Frappe sprite icon name, e.g. "accounting") is never rendered.
 *
 * PATCHES:
 *   1. sync_layout() — merge fresh logo_url / icon_image / icon from boot data
 *      into frappe.desktop_icons before the template renders.
 *   2. get_desktop_icon() — return null when logo_url, icon_image, or icon is set,
 *      so the SVG-on-disk branch is skipped and we control the render.
 *   3. applyDesktopSpriteIcons() — post-render DOM fix: inject frappe.utils.icon()
 *      HTML for icons that use the icon field (no logo_url / icon_image).
 *   4. applySidebarHeaderIcon() — post-render DOM fix for the sidebar header:
 *      apply logo_url / icon_image / icon and bg_color from fresh boot data.
 *      (SidebarHeader.header_stroke_color is never set by Frappe, so bg_color
 *      renders as var(undefined) — we apply it directly.)
 */
(function () {

  // ---------------------------------------------------------------------------
  // Patch 1: sync_layout — merge fresh image fields before render
  // ---------------------------------------------------------------------------
  function patchSyncLayout() {
    var desktopPage =
      frappe.pages["desktop"] &&
      frappe.pages["desktop"].desktop_page;

    if (!desktopPage || desktopPage._dcnet_syncPatched) return;
    if (typeof desktopPage.sync_layout !== "function") return;
    desktopPage._dcnet_syncPatched = true;

    var origSync = desktopPage.sync_layout.bind(desktopPage);

    desktopPage.sync_layout = function () {
      origSync();

      var bootIcons = frappe.boot && frappe.boot.desktop_icons;
      if (!bootIcons || !frappe.desktop_icons) return;

      var bootMap = {};
      bootIcons.forEach(function (b) { bootMap[b.name] = b; });

      frappe.desktop_icons.forEach(function (icon) {
        var boot = bootMap[icon.name];
        if (!boot) return;
        icon.logo_url = boot.logo_url || null;
        icon.icon_image = boot.icon_image || null;
        icon.icon = boot.icon || icon.icon;
      });
    };
  }

  // ---------------------------------------------------------------------------
  // Patch 2: get_desktop_icon — skip SVG-on-disk when a custom icon is set
  // ---------------------------------------------------------------------------
  function patchGetDesktopIcon() {
    if (
      !frappe ||
      !frappe.utils ||
      !frappe.utils.get_desktop_icon ||
      !frappe.utils.get_desktop_icon_by_label ||
      frappe.utils._dcnet_icon_patched
    )
      return;

    frappe.utils._dcnet_icon_patched = true;
    var _orig = frappe.utils.get_desktop_icon;

    frappe.utils.get_desktop_icon = function (icon_name, variant) {
      var d = frappe.utils.get_desktop_icon_by_label(icon_name);
      // If any custom icon is set, skip the SVG-on-disk path so our DOM fixes
      // can render the correct icon instead.
      if (d && (d.logo_url || d.icon_image || d.icon)) return null;
      return _orig.apply(this, arguments);
    };
  }

  // ---------------------------------------------------------------------------
  // Patch 3: desktop tiles — inject Frappe sprite icon for the icon field
  //
  // Called after icons render (setTimeout 0). Replaces the letter-circle
  // .icon-container with frappe.utils.icon() HTML when the icon field is set
  // and no image URL is provided.
  // ---------------------------------------------------------------------------
  function applyDesktopSpriteIcons() {
    var bootIcons = frappe.boot && frappe.boot.desktop_icons;
    if (!bootIcons) return;

    var isSolid = frappe.boot.desktop_icon_style === "Solid";

    bootIcons.forEach(function (icon) {
      // Apply background to .folder-icon for ALL icons regardless of type
      var desktopEl = document.querySelector(
        '.desktop-icon[data-id="' +
        icon.label.replace(/\\/g, "\\\\").replace(/"/g, '\\"') + '"]'
      );
      if (desktopEl) {
        var folderIcon = desktopEl.querySelector(".folder-icon");
        if (folderIcon) {
          var bgColor = icon.bg_color ||
            getComputedStyle(document.documentElement).getPropertyValue("--primary").trim();
          if (bgColor) folderIcon.style.setProperty("--folder-icon-background-color", bgColor);
        }
      }

      if (!icon.icon) return;
      if (icon.logo_url || icon.icon_image) return; // image takes priority

      var selector =
        '.desktop-icon[data-id="' +
        icon.label.replace(/\\/g, "\\\\").replace(/"/g, '\\"') +
        '"] .icon-container';
      var container = document.querySelector(selector);
      if (!container) return;

      // Replace letter-circle with Frappe sprite icon
      container.innerHTML = frappe.utils.icon(icon.icon, "lg");

      // Apply bg_color — fall back to --primary when not set
      var bgSource = icon.bg_color ||
        getComputedStyle(document.documentElement).getPropertyValue("--primary").trim() ||
        null;
      if (bgSource) {
        var hexColor =
          (frappe.utils.desktop_pallete && frappe.utils.desktop_pallete[bgSource]) ||
          (/^#[0-9A-Fa-f]{3,8}$/.test(bgSource) ? bgSource : null);
        if (hexColor) {
          container.style.backgroundColor = isSolid ? hexColor : hexColor + "1A";
        }
      }

      // Apply icon_color — default to #ffffff when not set
      var iconColor = (icon.icon_color && /^#[0-9A-Fa-f]{3,8}$/.test(icon.icon_color))
        ? icon.icon_color
        : "#ffffff";
      var svg = container.querySelector("svg");
      if (svg) {
        svg.style.setProperty("--icon-stroke", iconColor);
        svg.style.color = iconColor;
      }
    });
  }

  // ---------------------------------------------------------------------------
  // Patch 4: sidebar header — apply image, sprite icon, and bg_color
  //
  // SidebarHeader.set_header_icon() also calls frappe.utils.get_desktop_icon().
  // The sidebar's page-change handler registers before ours (core bundle first),
  // so it may run before patchGetDesktopIcon() is applied. As a safety net, we
  // overwrite .header-logo and .sidebar-item-icon directly after render.
  //
  // bg_color: SidebarHeader.header_stroke_color is never assigned by Frappe, so
  // the template renders var(undefined) — we apply the color directly.
  // ---------------------------------------------------------------------------
  function applySidebarHeaderIcon() {
    var sidebar = frappe.app && frappe.app.sidebar;
    if (!sidebar || !sidebar.sidebar_title) return;

    var bootIcons = frappe.boot && frappe.boot.desktop_icons;
    if (!bootIcons) return;

    var icon = bootIcons.find(function (i) {
      return i.label === sidebar.sidebar_title && i.hidden != 1;
    });
    if (!icon) return;

    var headerLogo = document.querySelector(".header-logo");

    if (headerLogo) {
      if (icon.logo_url || icon.icon_image) {
        var imageUrl = icon.logo_url || icon.icon_image;
        headerLogo.innerHTML =
          '<img src="' + imageUrl + '" style="width:100%;height:100%;object-fit:contain;">';
      } else if (icon.icon) {
        headerLogo.innerHTML = frappe.utils.icon(icon.icon, "md");
        // Apply icon_color — default to #ffffff when not set
        var iconColor = (icon.icon_color && /^#[0-9A-Fa-f]{3,8}$/.test(icon.icon_color))
          ? icon.icon_color
          : "#ffffff";
        var svg = headerLogo.querySelector("svg");
        if (svg) {
          svg.style.setProperty("--icon-stroke", iconColor);
          svg.style.color = iconColor;
          svg.style.stroke = iconColor;

        }
      }
    }

    // Apply bg_color — if not set, fall back to theme primary color
    var iconContainer = document.querySelector(".sidebar-header .sidebar-item-icon");
    if (iconContainer) {
      var bgSource = icon.bg_color ||
        getComputedStyle(document.documentElement).getPropertyValue("--primary").trim() ||
        null;
      if (bgSource) {
        var hexColor =
          (frappe.utils.desktop_pallete && frappe.utils.desktop_pallete[bgSource]) ||
          (/^#[0-9A-Fa-f]{3,8}$/.test(bgSource) ? bgSource : null);
        if (hexColor) {
          var isSolid = frappe.boot.desktop_icon_style === "Solid";
          iconContainer.style.backgroundColor = isSolid ? hexColor : hexColor + "1A";
        }
      }
    }
  }

  // ---------------------------------------------------------------------------
  // Wire up — page-change fires after on_page_load (desktop_page exists) but
  // before on_page_show (sync_layout / sidebar render). Patch functions first,
  // then fix DOM after render completes (setTimeout 0).
  // ---------------------------------------------------------------------------
  $(document).on("page-change", function () {
    patchSyncLayout();
    patchGetDesktopIcon();
    setTimeout(function () {
      applyDesktopSpriteIcons();
      applySidebarHeaderIcon();
    }, 0);
  });

  // Apply patches immediately if document is already loaded
  if (document.readyState !== "loading") {
    patchSyncLayout();
    patchGetDesktopIcon();
  } else {
    document.addEventListener("DOMContentLoaded", function () {
      patchSyncLayout();
      patchGetDesktopIcon();
    });
  }

  // Expose for desktop_icon_form.js to call after save re-render
  window.DCNetIconOverride = {
    applyDesktopSpriteIcons: applyDesktopSpriteIcons,
    applySidebarHeaderIcon: applySidebarHeaderIcon,
  };
})();
