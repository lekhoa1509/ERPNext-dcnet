function render_summary_row(frm) {
    const counts = {"Còn nguyên": 0, "Hỏng": 0, "Mất": 0, "Thiếu": 0};
    (frm.doc.stocktake_items || []).forEach((it) => {
        const s = it.physical_status;
        if (counts[s] !== undefined) counts[s]++;
    });
    const wrapper = frm.fields_dict.stocktake_items
        && frm.fields_dict.stocktake_items.$wrapper;
    if (!wrapper) return;
    wrapper.find(".stocktake-summary").remove();
    const html = `<div class="stocktake-summary" style="margin-top:8px; padding:8px;`
        + ` background:#f5f5f5; border-radius:4px; font-size:13px;">`
        + `<strong>${__("Tổng kết")}:</strong> `
        + `${__("Còn nguyên")}: <strong>${counts["Còn nguyên"]}</strong> · `
        + `${__("Hỏng")}: <strong>${counts["Hỏng"]}</strong> · `
        + `${__("Mất")}: <strong>${counts["Mất"]}</strong> · `
        + `${__("Thiếu")}: <strong>${counts["Thiếu"]}</strong>`
        + `</div>`;
    wrapper.append(html);
}

frappe.ui.form.on("Asset Stocktake", {
    onload(frm) {
        if (frm.is_new() && !frm.doc.company) {
            frm.set_value("company", frappe.defaults.get_user_default("Company"));
        }
    },
    refresh(frm) {
        if (frm.doc.docstatus === 0) {
            frm.add_custom_button(__("Tải danh sách"), () => {
                if (!frm.doc.scope) {
                    frappe.msgprint(__("Chọn phạm vi (TSCĐ / CCDC) trước"));
                    return;
                }
                frm.call("load_items").then(r => {
                    frm.refresh();
                    const count = r.message || 0;
                    frappe.show_alert({message: __("Đã tải {0} mục", [count]), indicator: "green"});
                });
            }, __("Hành động"));
        }
        if (frm.doc.status === "Completed" && frm.doc.docstatus === 0) {
            frm.add_custom_button(__("Duyệt kiểm kê"), () => {
                frappe.confirm(
                    __("Xác nhận duyệt kiểm kê? Các mục 'Mất' sẽ tạo bút toán ghi nhận."),
                    () => frm.call("approve").then(() => frm.refresh())
                );
            }, __("Hành động"));
        }
        render_summary_row(frm);
    }
});

frappe.ui.form.on("Asset Stocktake Item", {
    physical_status(frm) {
        render_summary_row(frm);
    },
    stocktake_items_remove(frm) {
        render_summary_row(frm);
    }
});
