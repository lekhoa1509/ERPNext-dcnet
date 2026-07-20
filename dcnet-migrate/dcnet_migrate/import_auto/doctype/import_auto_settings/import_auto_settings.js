frappe.ui.form.on("Import Auto Settings", {
    refresh(frm) {
        frm.page.set_title(__("Cài Đặt Import Danh Mục (Master Data Import Settings)"));
        frm.dashboard.clear_headline();
        frm.dashboard.set_headline(__("AI settings are shared by all automatic import documents."));
    },

    test_connection_btn(frm) {
        frappe.call({
            method: "dcnet_migrate.import_auto.doctype.import_auto_settings.import_auto_settings.test_ai_connection",
            freeze: true,
            freeze_message: __("Checking AI connection..."),
        }).then(() => frm.reload_doc());
    },
});
