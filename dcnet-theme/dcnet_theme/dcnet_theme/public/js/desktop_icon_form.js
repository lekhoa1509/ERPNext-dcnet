/**
 * Desktop Icon form extension — syncs client-side desktop data after save.
 *
 * Root cause: frappe.boot.desktop_icons is loaded once at page load.
 * The desktop page reads from desktopPage.data (populated from Desktop Layout
 * document or localStorage). Neither is refreshed when a Desktop Icon is saved.
 *
 * Fix: after_save calls refresh_desktop_icons to get fresh data from DB,
 * then patches all three stale sources:
 *   1. frappe.boot.desktop_icons
 *   2. frappe.desktop_icons
 *   3. frappe.pages["desktop"].desktop_page.data
 *
 * If the user is currently on the desktop page, triggers a full re-render.
 */
frappe.ui.form.on("Desktop Icon", {
  after_save: function (frm) {
    frappe.call({
      method: "dcnet_theme.dcnet_theme.boot.refresh_desktop_icons",
      callback: function (r) {
        if (!r || !r.message) return;
        var freshIcons = r.message;

        // 1. Replace boot data so SPA navigations use fresh icons
        frappe.boot.desktop_icons = freshIcons;

        // Helper: patch one icon entry in an array by name
        function patchList(list) {
          if (!Array.isArray(list)) return;
          freshIcons.forEach(function (updated) {
            var idx = list.findIndex(function (i) {
              return i.name === updated.name;
            });
            if (idx !== -1) {
              Object.assign(list[idx], updated);
            }
          });
        }

        // 2. Patch frappe.desktop_icons (current render source)
        patchList(frappe.desktop_icons);

        // 3. Patch or reset desktopPage.data
        var desktopPage =
          frappe.pages["desktop"] &&
          frappe.pages["desktop"].desktop_page;

        if (desktopPage) {
          if (Array.isArray(desktopPage.data)) {
            // data is a full icon array — patch in-place to preserve ordering
            patchList(desktopPage.data);
          } else {
            // data is {} or null — reset so sync_layout falls back to boot data
            desktopPage.data = {};
          }
        }

        // 4. Re-render if currently on desktop page
        var route = frappe.get_route();
        if (route && route[0] === "desktop" && desktopPage) {
          desktopPage.update();
          setTimeout(function () {
            window.DCNetTheme && window.DCNetTheme.applyDesktopCustomizations();
            // Re-inject sprite icons after re-render (update() rebuilds DOM
            // from scratch, so sprite replacements must run again)
            window.DCNetIconOverride && window.DCNetIconOverride.applyDesktopSpriteIcons();
            window.DCNetIconOverride && window.DCNetIconOverride.applySidebarHeaderIcon();
          }, 0);
        }

        frappe.show_alert({ message: __("Desktop icon updated"), indicator: "green" });
      },
    });
  },
});
