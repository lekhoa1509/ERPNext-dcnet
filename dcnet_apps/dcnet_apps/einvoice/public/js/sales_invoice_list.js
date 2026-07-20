/**
 * EInvoice — Sales Invoice List Script
 *
 * Adds "Xuất hóa đơn đỏ hàng loạt" action to the list view.
 */
frappe.listview_settings["Sales Invoice"] =
    frappe.listview_settings["Sales Invoice"] || {};

const _original_onload = frappe.listview_settings["Sales Invoice"].onload;

frappe.listview_settings["Sales Invoice"].onload = function (listview) {
    // Call original onload if exists
    if (_original_onload) {
        _original_onload(listview);
    }

    // Add bulk action
    listview.page.add_action_item(__("Xuất hóa đơn đỏ hàng loạt"), () => {
        const selected = listview.get_checked_items();

        if (!selected.length) {
            frappe.msgprint("Vui lòng chọn ít nhất một Sales Invoice.");
            return;
        }

        // Filter: only submitted + not yet issued
        const valid = selected.filter(
            (row) => row.docstatus === 1 && !row.einvoice_issued
        );

        if (!valid.length) {
            frappe.msgprint("Không có Sales Invoice nào hợp lệ (phải Submitted và chưa xuất HĐ đỏ).");
            return;
        }

        const si_names = valid.map((row) => row.name);

        // Ensure all selected invoices belong to the same company
        const companies = [...new Set(valid.map((r) => r.company))];
        if (companies.length > 1) {
            frappe.msgprint("Vui lòng chỉ chọn hóa đơn của cùng một công ty khi xuất hàng loạt.");
            return;
        }

        // Fetch providers filtered by company
        frappe.call({
            method: "dcnet_apps.einvoice.api.get_providers",
            args: { company: companies[0] },
            callback(r) {
                const providers = r.message || [];
                if (!providers.length) {
                    frappe.msgprint("Chưa có nhà cung cấp HĐĐT nào được cấu hình.");
                    return;
                }

                const d = new frappe.ui.Dialog({
                    title: `Xuất hóa đơn đỏ hàng loạt (${si_names.length} hóa đơn)`,
                    fields: [
                        {
                            fieldname: "info_html",
                            fieldtype: "HTML",
                            options: `
                                <div class="alert alert-info">
                                    Sẽ xuất <strong>${si_names.length}</strong> hóa đơn đỏ.
                                    ${selected.length !== valid.length
                                    ? `<br><small>${selected.length - valid.length} hóa đơn bị bỏ qua (chưa submit hoặc đã xuất).</small>`
                                    : ""}
                                </div>
                            `,
                        },
                        {
                            fieldname: "provider",
                            fieldtype: "Select",
                            label: "Nhà cung cấp HĐĐT",
                            options: providers.map((p) => p.name).join("\n"),
                            default: providers[0].name,
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
                        { fieldtype: "Section Break" },
                        {
                            fieldname: "pattern",
                            fieldtype: "Data",
                            label: "Ký hiệu mẫu số",
                            default: providers[0].default_invoice_pattern || "1",
                        },
                        { fieldtype: "Column Break" },
                        {
                            fieldname: "serial",
                            fieldtype: "Data",
                            label: "Ký hiệu hóa đơn",
                            default: providers[0].default_invoice_serial || "",
                        },
                    ],
                    primary_action_label: "Xác nhận xuất hàng loạt",
                    primary_action(values) {
                        d.hide();
                        frappe.call({
                            method: "dcnet_apps.einvoice.api.issue_bulk_invoices",
                            args: {
                                sales_invoices: JSON.stringify(si_names),
                                provider: values.provider,
                                pattern: values.pattern,
                                serial: values.serial,
                                issue_mode: values.issue_mode,
                            },
                            freeze: true,
                            freeze_message: `Đang xử lý ${si_names.length} hóa đơn...`,
                            callback(r) {
                                const msg = r.message;
                                if (msg && msg.background) {
                                    frappe.show_alert({
                                        message: msg.message,
                                        indicator: "blue",
                                    });
                                } else if (msg && msg.results) {
                                    einvoice_show_bulk_results(msg);
                                }
                                listview.refresh();
                            },
                        });
                    },
                });
                d.show();
            },
        });
    });
};


function einvoice_show_bulk_results(data) {
    let rows = "";
    for (const r of data.results || []) {
        const icon = r.status === "Success" ? "✅" : "❌";
        const detail = r.status === "Success"
            ? (r.detail?.invoice_number || "")
            : (r.detail || "");
        rows += `<tr>
            <td>${r.sales_invoice}</td>
            <td>${icon} ${r.status}</td>
            <td>${detail}</td>
        </tr>`;
    }

    frappe.msgprint({
        title: "Kết quả xuất hóa đơn đỏ hàng loạt",
        indicator: "blue",
        message: `
            <p>${data.message}</p>
            <table class="table table-bordered table-sm" style="font-size: 12px;">
                <thead><tr>
                    <th>Sales Invoice</th>
                    <th>Trạng thái</th>
                    <th>Chi tiết</th>
                </tr></thead>
                <tbody>${rows}</tbody>
            </table>
        `,
    });
}
