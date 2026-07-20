/**
 * dcnet_menu_override.js
 * Override frappe.ui.menu để ẩn các item mong muốn
 */
(function () {
    // Đảm bảo frappe.ui.menu tồn tại
    if (!frappe.ui || !frappe.ui.menu) return;

    const original_add_menu_item = frappe.ui.menu.prototype.add_menu_item;

    const labels_to_hide = [
        "About",
        "Frappe Support"
    ];

    frappe.ui.menu.prototype.add_menu_item = function (item) {
        if (item && item.label) {
            const label = item.label.trim();

            if (labels_to_hide.includes(label)) {
                return; // skip adding
            }
        }
        return original_add_menu_item.apply(this, arguments);
    };
})();
