/**
 * EInvoice — Sales Invoice Form Script
 *
 * Adds "Xuất hóa đơn đỏ" button on submitted Sales Invoices
 * that have not yet been issued.
 */
frappe.ui.form.on("Sales Invoice", {
    refresh(frm) {
        // Only show on submitted SI that hasn't been issued yet
        if (frm.doc.docstatus === 1 && !frm.doc.einvoice_issued) {
            frm.add_custom_button(
                __("Xuất hóa đơn đỏ"),
                () => einvoice_show_issue_dialog(frm),
                __("Hóa đơn điện tử")
            );
        }

        // Show PDF link if already issued
        if (frm.doc.einvoice_issued && frm.doc.einvoice_pdf_url) {
            frm.dashboard.set_headline(
                `<a href="${frm.doc.einvoice_pdf_url}" target="_blank">
                    📄 Xem hóa đơn đỏ (PDF)
                </a>`
            );
        }
    },
});


function einvoice_show_issue_dialog(frm) {
    // Fetch available providers filtered by this invoice's company
    frappe.call({
        method: "dcnet_apps.einvoice.api.get_providers",
        args: { company: frm.doc.company },
        callback(r) {
            const providers = r.message || [];
            if (!providers.length) {
                frappe.msgprint("Chưa có nhà cung cấp HĐĐT nào được cấu hình.");
                return;
            }

            const provider_options = providers.map((p) => p.name);
            const default_provider = providers[0];

            const d = new frappe.ui.Dialog({
                title: "Xuất hóa đơn đỏ",
                fields: [
                    {
                        fieldname: "provider",
                        fieldtype: "Select",
                        label: "Nhà cung cấp HĐĐT",
                        options: provider_options.join("\n"),
                        default: default_provider.name,
                        reqd: 1,
                    },
                    { fieldtype: "Column Break" },
                    {
                        fieldname: "issue_mode",
                        fieldtype: "Select",
                        label: "Chế độ",
                        options: "Draft\nPublish",
                        default: "Draft",
                    },
                    { fieldtype: "Section Break", label: "Mẫu hóa đơn" },
                    {
                        fieldname: "pattern",
                        fieldtype: "Data",
                        label: "Ký hiệu mẫu số",
                        default: default_provider.default_invoice_pattern || "1",
                    },
                    { fieldtype: "Column Break" },
                    {
                        fieldname: "serial",
                        fieldtype: "Data",
                        label: "Ký hiệu hóa đơn",
                        default: default_provider.default_invoice_serial || "",
                    },
                    { fieldtype: "Section Break", label: "Thông tin xuất" },
                    {
                        fieldname: "info_html",
                        fieldtype: "HTML",
                        options: `
                            <div style="color: var(--text-muted); font-size: var(--text-sm);">
                                <p><strong>Khách hàng:</strong> ${frm.doc.customer_name || ""}</p>
                                <p><strong>Tổng tiền:</strong> ${format_currency(frm.doc.grand_total)}</p>
                                <p><strong>Số dòng:</strong> ${(frm.doc.items || []).length}</p>
                            </div>
                        `,
                    },
                ],
                primary_action_label: "Xác nhận xuất",
                primary_action(values) {
                    d.hide();
                    frappe.call({
                        method: "dcnet_apps.einvoice.api.issue_single_invoice",
                        args: {
                            sales_invoice: frm.doc.name,
                            provider: values.provider,
                            pattern: values.pattern,
                            serial: values.serial,
                            issue_mode: values.issue_mode,
                        },
                        freeze: true,
                        freeze_message: "Đang xuất hóa đơn đỏ...",
                        callback(r) {
                            if (!r.exc && r.message) {
                                frappe.show_alert({
                                    message: r.message.message || "Thành công!",
                                    indicator: r.message.status === "Success" ? "green" : "red",
                                });
                                frm.reload_doc();
                            }
                        },
                    });
                },
            });
            d.show();
        },
    });
}
