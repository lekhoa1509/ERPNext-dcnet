// Hide Desktop Icons whose target module is blocked on the current User.
(function () {
  function blockedModules() {
    return new Set(frappe.boot?.dcnet_permission_blocked_modules || []);
  }

  function iconModuleMap() {
    return frappe.boot?.dcnet_permission_desktop_icon_modules || {};
  }

  function iconKeys(icon) {
    if (!icon) return [];
    return [icon.name, icon.label, icon.custom_label, icon.link_to, icon.link].filter(Boolean);
  }

  function isBlockedIcon(icon) {
    const blocked = blockedModules();
    if (!blocked.size) return false;

    const modules = iconModuleMap();
    return iconKeys(icon).some((key) => blocked.has(modules[key]));
  }

  function filterIconList(list) {
    if (!Array.isArray(list)) return list;
    return list.filter((icon) => !isBlockedIcon(icon));
  }

  function filterDesktopData() {
    if (!window.frappe || !frappe.boot) return;

    frappe.boot.desktop_icons = filterIconList(frappe.boot.desktop_icons);
    frappe.desktop_icons = filterIconList(frappe.desktop_icons);
    frappe.new_desktop_icons = filterIconList(frappe.new_desktop_icons);

    const desktopPage = frappe.pages?.desktop?.desktop_page;
    if (desktopPage?.data && typeof desktopPage.data === "object") {
      desktopPage.data = filterIconList(desktopPage.data);
    }
  }

  function filterSavedLocalStorageLayout() {
    if (!window.frappe?.session?.user) return;

    const key = `${frappe.session.user}:desktop`;
    const raw = localStorage.getItem(key);
    if (!raw || raw === "null" || raw === "undefined") return;

    try {
      const layout = JSON.parse(raw);
      const filtered = filterIconList(layout);
      if (Array.isArray(filtered) && filtered.length !== layout.length) {
        localStorage.setItem(key, JSON.stringify(filtered));
      }
    } catch (error) {
      // Ignore invalid localStorage values; Frappe handles these separately.
    }
  }

  function removeBlockedDomIcons() {
    const blocked = blockedModules();
    if (!blocked.size) return;

    const modules = iconModuleMap();
    document.querySelectorAll(".desktop-icon[data-id]").forEach((el) => {
      const label = el.getAttribute("data-id");
      if (label && blocked.has(modules[label])) {
        el.remove();
      }
    });
  }

  function patchDesktopSyncLayout() {
    const desktopPage = frappe.pages?.desktop?.desktop_page;
    if (!desktopPage || desktopPage._dcnet_permission_sync_patched) return;
    if (typeof desktopPage.sync_layout !== "function") return;

    desktopPage._dcnet_permission_sync_patched = true;
    const originalSyncLayout = desktopPage.sync_layout.bind(desktopPage);

    desktopPage.sync_layout = function () {
      filterSavedLocalStorageLayout();
      originalSyncLayout();
      filterDesktopData();
    };
  }

  function applyFilter() {
    filterSavedLocalStorageLayout();
    filterDesktopData();
    patchDesktopSyncLayout();
    setTimeout(function () {
      filterDesktopData();
      removeBlockedDomIcons();
    }, 0);
  }

  $(document).on("page-change", applyFilter);

  if (document.readyState !== "loading") {
    applyFilter();
  } else {
    document.addEventListener("DOMContentLoaded", applyFilter);
  }
})();
