// EInvoice Inward — List view color indicators
// Frappe v16 listview_settings — màu sắc theo tct_status (KQPhanTich) + lifecycle.
//
// Mapping:
//   🔴 Red    — "Hóa đơn có sai sót" (KQPhanTich invalid → kế toán phải review)
//   🟢 Green  — "Hóa đơn hợp lệ" + lifecycle "Hóa đơn mới"
//   🟡 Yellow — lifecycle "Hóa đơn đã bị thay thế / đã bị điều chỉnh" (HĐ đã bị invalid hóa)
//   🔵 Blue   — lifecycle "Hóa đơn thay thế / điều chỉnh" (HĐ thay thế HĐ khác)
//   ⚪ Gray   — Unknown / chưa phân tích

frappe.listview_settings["EInvoice Inward"] = {
    add_fields: ["tct_status", "lifecycle_status", "status", "attach_status", "pdf_file", "xml_file", "attach_error"],

    onload(listview) {
        // Realtime refresh when any attach job reports progress (once per listview mount)
        frappe.realtime.on("einvoice_attach_progress", function () {
            listview.refresh();
        });
    },

    refresh: function (listview) {
        // Bulk action: attach files for selected records
        listview.page.add_inner_button(__("Tải file đính kèm cho HĐ đã chọn"), function () {
            const checked = listview.get_checked_items();
            if (!checked || !checked.length) {
                frappe.msgprint(__("Vui lòng chọn ít nhất 1 hóa đơn"));
                return;
            }
            const names = checked.map(function (d) { return d.name; });
            frappe.call({
                method: "einvoice.einvoice.services.attach.enqueue_attach_files",
                args: { invoice_names: names },
                callback: function (r) {
                    if (!r.exc) {
                        frappe.show_alert({
                            message: __("Đã enqueue {0} hóa đơn, theo dõi cột Đính kèm", [names.length]),
                            indicator: "blue",
                        });
                        listview.refresh();
                    }
                },
            });
        }, __("Hành động"));

        listview.page.add_inner_button(
            __("Cập nhật Hóa đơn đầu vào mới"),
            function () {
                frappe.call({
                    method: "einvoice.einvoice.api.sync_inward_invoices",
                    freeze: true,
                    freeze_message: __("Đang đồng bộ hóa đơn từ nhà cung cấp..."),
                    callback: function (r) {
                        if (r.message) {
                            const res = r.message;
                            let msg = `Đồng bộ hoàn tất: Tìm thấy ${res.fetched || 0} hóa đơn.`;
                            if (res.new > 0) msg += ` (Thêm mới: ${res.new})`;
                            if (res.dup > 0) msg += ` (Trùng: ${res.dup})`;
                            if (res.errors > 0) msg += ` (Lỗi: ${res.errors})`;
                            frappe.msgprint({
                                title: __("Kết quả đồng bộ"),
                                message: msg,
                                indicator: res.new > 0 ? "green" : "orange",
                            });
                            listview.refresh();
                        }
                    },
                });
            }
        );
    },

    get_indicator(doc) {
        // Ưu tiên 1: HĐ có sai sót → đỏ (cảnh báo kế toán)
        if (doc.tct_status === "Hóa đơn có sai sót") {
            return [__("Có sai sót"), "red", "tct_status,=,Hóa đơn có sai sót"];
        }

        // Ưu tiên 2: HĐ đã bị thay thế / đã bị điều chỉnh → vàng (HĐ này không còn hiệu lực, đừng tạo PI)
        if (doc.lifecycle_status === "Hóa đơn đã bị thay thế" ||
            doc.lifecycle_status === "Hóa đơn đã bị điều chỉnh") {
            return [__(doc.lifecycle_status), "yellow", "lifecycle_status,=," + doc.lifecycle_status];
        }

        // Ưu tiên 3: HĐ thay thế / điều chỉnh → xanh dương (cần đối chiếu HĐ gốc)
        if (doc.lifecycle_status === "Hóa đơn thay thế" ||
            doc.lifecycle_status === "Hóa đơn điều chỉnh") {
            return [__(doc.lifecycle_status), "blue", "lifecycle_status,=," + doc.lifecycle_status];
        }

        // Ưu tiên 4: HĐ hợp lệ + Mới → xanh lá
        if (doc.tct_status === "Hóa đơn hợp lệ") {
            return [__("Hợp lệ"), "green", "tct_status,=,Hóa đơn hợp lệ"];
        }

        // Default: chưa rõ
        return [__("Chưa phân tích"), "gray", "tct_status,=,Unknown"];
    },

    formatters: {
        attach_status(value, df, doc) {
            if (!value) return "";
            const icons = {
                "Chưa tải": "⬜",
                "Đang tải": "🔄",
                "Đã đính kèm": "✅",
                "Một phần": "⚠️",
                "Lỗi": "❌",
            };
            const icon = icons[value] || "❓";
            const title = doc.attach_error ? doc.attach_error : value;
            return `<span title="${frappe.utils.escape_html(title)}">${icon} ${__(value)}</span>`;
        },
    },
};
