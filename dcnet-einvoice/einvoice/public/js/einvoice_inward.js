// EInvoice Inward — Form view: attach status button + indicator + realtime listener

frappe.ui.form.on("EInvoice Inward", {
    onload(frm) {
        // Bind realtime listener once on load (not in refresh — avoids duplicate listeners)
        frappe.realtime.on("einvoice_attach_progress", function (data) {
            if (data && data.invoice_name === frm.doc.name) {
                frm.reload_doc();
            }
        });
    },

    refresh(frm) {
        const status = frm.doc.attach_status;
        const hasPdfUrl = frm.doc.pdf_url;
        const hasXmlUrl = frm.doc.xml_url;
        const hasPdfFile = frm.doc.pdf_file;
        const hasXmlFile = frm.doc.xml_file;

        // Show retry button when: status is Lỗi/Một phần/Chưa tải,
        // or status empty but URLs present (not yet attempted)
        const needsAttach =
            ["Lỗi", "Một phần", "Chưa tải"].includes(status) ||
            (!status && (hasPdfUrl || hasXmlUrl) && (!hasPdfFile || !hasXmlFile));

        if (needsAttach) {
            frm.add_custom_button(__("Tải lại file đính kèm"), function () {
                frappe.call({
                    method: "einvoice.einvoice.services.attach.enqueue_attach_files",
                    args: { invoice_names: [frm.doc.name] },
                    callback: function (r) {
                        if (!r.exc) {
                            frappe.show_alert({
                                message: __("Đã enqueue, theo dõi cột Đính kèm"),
                                indicator: "blue",
                            });
                        }
                    },
                });
            });
        }

        // Blue indicator when actively downloading
        if (status === "Đang tải") {
            frm.dashboard.add_indicator(__("Đang tải file đính kèm..."), "blue");
        }
    },
});
