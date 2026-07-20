// EInvoice Provider — Client Script

frappe.ui.form.on("EInvoice Provider", {
    refresh(frm) {
        // Update status indicator color
        _update_status_color(frm);

        frm.add_custom_button(__("Kiểm tra kết nối"), () => {
            _test_connection(frm);
        }, __("Thao tác"));

        frm.add_custom_button(__("Lấy mẫu hóa đơn"), () => {
            _refresh_templates(frm);
        }, __("Thao tác"));
    },

    provider_type(frm) {
        _suggest_provider_name(frm);
        // Warn about stub providers
        if (["Viettel", "MISA"].includes(frm.doc.provider_type)) {
            frappe.msgprint(
                __("Provider {0} chưa được hỗ trợ. Vui lòng liên hệ DCNet.", [frm.doc.provider_type])
            );
        }
    },

    company(frm) {
        _suggest_provider_name(frm);
    },

    // Wire the inline button fields
    test_connection_btn(frm) {
        _test_connection(frm);
    },

    refresh_templates_btn(frm) {
        _refresh_templates(frm);
    },
});

function _suggest_provider_name(frm) {
    if (!frm.is_new()) return;
    if (!frm.doc.provider_type || !frm.doc.company) return;
    frm.set_value("provider_name", `${frm.doc.provider_type} - ${frm.doc.company}`);
}

function _test_connection(frm) {
    if (frm.is_dirty()) {
        frappe.msgprint(__("Vui lòng lưu trước khi kiểm tra kết nối."), __("Chú ý"));
        return;
    }

    frappe.dom.freeze(__("Đang kiểm tra kết nối..."));

    frappe.call({
        method: "einvoice.einvoice.doctype.einvoice_provider.einvoice_provider.test_connection",
        args: { docname: frm.docname },
        callback(r) {
            frappe.dom.unfreeze();
            frm.reload_doc();
            if (!r.exc && r.message) {
                if (r.message.success) {
                    frappe.show_alert({
                        message: __(r.message.message),
                        indicator: "green",
                    });
                } else {
                    frappe.msgprint({
                        title: __("Lỗi"),
                        message: r.message.message,
                        indicator: "red",
                    });
                }
            }
        },
        error() {
            frappe.dom.unfreeze();
            frm.reload_doc();
        }
    });
}

function _refresh_templates(frm) {
    if (frm.is_dirty()) {
        frappe.msgprint(__("Vui lòng lưu trước khi lấy mẫu hóa đơn."), __("Chú ý"));
        return;
    }

    frappe.dom.freeze(__("Đang lấy mẫu hóa đơn..."));

    frappe.call({
        method: "einvoice.einvoice.doctype.einvoice_provider.einvoice_provider.refresh_templates",
        args: { docname: frm.docname },
        callback(r) {
            frappe.dom.unfreeze();
            if (!r.exc && r.message) {
                const templates = r.message;
                frappe.show_alert({
                    message: __("Đã lấy được {0} mẫu hóa đơn.", [templates.length]),
                    indicator: "blue"
                });
                if (templates.length) {
                    let rows = templates.map(t => `<tr><td>${t.pattern || ""}</td><td>${t.serial || ""}</td><td>${t.name || ""}</td></tr>`).join("");
                    frappe.msgprint({
                        title: __("Mẫu hóa đơn"),
                        message: `<table class="table table-bordered table-sm">
                            <thead><tr><th>Mẫu số</th><th>Ký hiệu</th><th>Tên</th></tr></thead>
                            <tbody>${rows}</tbody>
                        </table>`,
                    });
                }
            }
        },
        error() {
            frappe.dom.unfreeze();
        }
    });
}

function _update_status_color(frm) {
    const status = frm.doc.connection_status;
    const colors = {
        "Connected": "green",
        "Failed": "red",
        "Not Tested": "orange"
    };
    if (status) {
        frm.set_df_property("connection_status", "description",
            `<span class="indicator ${colors[status] || 'orange'}">${status}</span>`);
    }
}
