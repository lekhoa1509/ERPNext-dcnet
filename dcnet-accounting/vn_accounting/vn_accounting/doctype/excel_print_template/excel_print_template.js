frappe.ui.form.on("Excel Print Template", {
    refresh(frm) {
        if (frm.is_new() || !frm.perm[0]?.write) return;
        frm.add_custom_button(__("Mở trình soạn mẫu"), () => {
            frappe.route_options = { template: frm.doc.name };
            frappe.set_route("excel-print-template-builder");
        });
    },
});
