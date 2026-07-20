// Refresh Desk when dcnet_permission updates the current user's access.
(function () {
  const EVENT_NAME = "dcnet_permission_user_access_changed";

  function reloadForAccessChange(message) {
    if (!message || message.user !== frappe.session.user) return;

    if (window.cur_frm && cur_frm.is_dirty()) {
      frappe.show_alert({
        message: __("Quyền đã đổi — lưu hoặc đóng form rồi tải lại Desk để áp dụng."),
        indicator: "orange",
      }, 7);
      return;
    }

    if (frappe.show_alert) {
      frappe.show_alert({
        message: __("Quyền truy cập đã được cập nhật. Đang tải lại giao diện..."),
        indicator: "blue",
      }, 2);
    }

    setTimeout(function () {
      window.location.reload();
    }, 600);
  }

  function registerListener() {
    if (!window.frappe || !frappe.realtime || !frappe.session) return false;
    if (frappe._dcnet_permission_access_reload_registered) return true;

    frappe._dcnet_permission_access_reload_registered = true;
    frappe.realtime.on(EVENT_NAME, reloadForAccessChange);
    return true;
  }

  if (!registerListener()) {
    document.addEventListener("DOMContentLoaded", registerListener);

    let attempts = 0;
    const timer = setInterval(function () {
      attempts += 1;
      if (registerListener() || attempts >= 20) {
        clearInterval(timer);
      }
    }, 250);
  }
})();
