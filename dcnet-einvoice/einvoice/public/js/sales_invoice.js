/**
 * EInvoice — Sales Invoice Form Script
 *
 * Adds "Xuất hóa đơn điện tử" button on submitted Sales Invoices
 * that have not yet been issued.
 */
frappe.ui.form.on("Sales Invoice", {
    refresh(frm) {
        // 1 nút duy nhất "Xuất hóa đơn điện tử" — backend dispatcher route theo
        // provider.OUTWARD_CAPABILITY: direct (HSM/pre-signed) hoặc push-draft.
        if (frm.doc.docstatus === 1 && !frm.doc.einvoice_issued && !frm.doc.einvoice_pushed) {
            frm.add_custom_button(
                __("Xuất hóa đơn điện tử"),
                () => einvoice_show_issue_dialog(frm),
                __("Hóa đơn điện tử")
            );
        }

        // Status indicator for pushed-but-not-yet-signed SI
        if (frm.doc.einvoice_pushed && !frm.doc.einvoice_issued) {
            const status_text = frm.doc.einvoice_status_text || "Đã đẩy, chờ ký";
            frm.dashboard.set_headline_alert(
                `<span style="color:var(--orange-500)">⏳ ${status_text}</span>` +
                (frm.doc.einvoice_ikey ? ` &nbsp;·&nbsp; ikey: <code>${frm.doc.einvoice_ikey}</code>` : ""),
                "orange"
            );
            frm.add_custom_button(
                __("Đồng bộ trạng thái"),
                () => einvoice_sync_outward(frm),
                __("Hóa đơn điện tử")
            );
        }

        // Show issued status + links
        if (frm.doc.einvoice_issued) {
            let links = [];
            if (frm.doc.einvoice_pdf_url) {
                links.push(`<a href="${frm.doc.einvoice_pdf_url}" target="_blank">PDF</a>`);
            }
            if (frm.doc.einvoice_link_view) {
                links.push(`<a href="${frm.doc.einvoice_link_view}" target="_blank">Tra cứu</a>`);
            }
            const link_html = links.length ? ` &nbsp;·&nbsp; ${links.join(" | ")}` : "";
            frm.dashboard.set_headline_alert(
                `<span style="color:var(--green-500)">✓ Đã phát hành HĐĐT</span>` +
                (frm.doc.einvoice_number ? ` số <strong>${frm.doc.einvoice_number}</strong>` : "") +
                link_html,
                "green"
            );
        }
    },
});


function einvoice_sync_outward(frm) {
    frappe.call({
        method: "einvoice.einvoice.api.sync_outward_states_now",
        args: { provider: frm.doc.einvoice_provider || null },
        freeze: true,
        freeze_message: "Đang đồng bộ trạng thái...",
        callback(r) {
            if (r.exc) return;
            const res = r.message || {};
            frappe.show_alert({
                message: `Đã kiểm tra ${res.checked || 0} hóa đơn, cập nhật ${res.updated || 0}.`,
                indicator: "blue",
            });
            frm.reload_doc();
        },
    });
}


function einvoice_show_issue_dialog(frm) {
    // Fetch available providers filtered by this invoice's company
    frappe.call({
        method: "einvoice.einvoice.api.get_providers",
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
                title: "Xuất hóa đơn điện tử",
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
                        options: "Nháp\nPhát hành",
                        default: "Nháp",
                    },
                    {
                        fieldname: "send_email",
                        fieldtype: "Check",
                        label: "Gửi email cho khách sau khi phát hành",
                        default: 1,
                        depends_on: "eval:doc.issue_mode === 'Phát hành'",
                        description:
                            "Khi phát hành thành công, hệ thống gửi email đính kèm PDF hóa đơn tới " +
                            "địa chỉ liên hệ khách hàng. Bỏ tick nếu muốn gửi thủ công sau.",
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
                    // Dialog hiển thị tiếng Việt; backend vẫn dùng "Draft"/"Publish".
                    const issue_mode =
                        { "Nháp": "Draft", "Phát hành": "Publish" }[values.issue_mode] || "Draft";
                    // send_email chỉ áp dụng khi Phát hành (đã ký, có PDF).
                    const send_email = issue_mode === "Publish" ? (values.send_email ? 1 : 0) : 0;
                    frappe.call({
                        method: "einvoice.einvoice.api.issue_single_invoice",
                        args: {
                            sales_invoice: frm.doc.name,
                            provider: values.provider,
                            pattern: values.pattern,
                            serial: values.serial,
                            issue_mode,
                            send_email,
                        },
                        freeze: true,
                        freeze_message: "Đang xuất hóa đơn điện tử...",
                        callback(r) {
                            if (r.exc) return;
                            if (r.message && !r.message.success) {
                                frappe.msgprint({
                                    title: __("Lỗi"),
                                    message: r.message.message,
                                    indicator: "red",
                                });
                                return;
                            }
                            if (r.message) {
                                frappe.show_alert({
                                    message: r.message.message || "Thành công!",
                                    indicator: "green",
                                });
                            }
                            frm.reload_doc();
                        },
                    });
                },
            });
            d.show();
        },
    });
}
