// BCTC Mapping form — helper buttons for copy + restore
frappe.ui.form.on("BCTC Mapping", {
    refresh(frm) {
        if (!frm.doc.__islocal) {
            frm.add_custom_button(__("Sao chép từ công ty khác"), () => _copy_from_company_dialog(frm), __("Thao tác"));
            frm.add_custom_button(__("Khôi phục mặc định TT99/2025"), () => _restore_defaults_dialog(frm), __("Thao tác"));
        }
    }
});

function _copy_from_company_dialog(frm) {
    const d = new frappe.ui.Dialog({
        title: __("Sao chép mapping từ công ty khác"),
        fields: [
            {
                fieldtype: "HTML",
                options: `<p class="text-muted">${__("Chọn công ty nguồn để sao chép cấu hình B01/B02/B03. Dữ liệu mapping hiện tại sẽ bị ghi đè.")}</p>`
            },
            {
                fieldtype: "Link",
                fieldname: "source_company",
                label: __("Công ty nguồn"),
                options: "Company",
                reqd: 1,
                filters: { country: "Vietnam" },
                description: __("Chỉ hiển thị công ty Việt Nam có BCTC Mapping sẵn có.")
            }
        ],
        primary_action_label: __("Sao chép"),
        primary_action(values) {
            if (values.source_company === frm.doc.company) {
                frappe.msgprint(__("Không thể sao chép từ chính công ty này."));
                return;
            }
            frappe.confirm(
                __("Sao chép mapping từ <b>{0}</b> vào <b>{1}</b>? Mapping hiện tại sẽ bị ghi đè hoàn toàn.", [values.source_company, frm.doc.company]),
                () => {
                    frappe.call({
                        method: "copy_from_company",
                        doc: frm.doc,
                        args: { source_company: values.source_company },
                        callback(r) {
                            if (!r.exc) {
                                frappe.show_alert({ message: __("Đã sao chép mapping từ {0}.", [values.source_company]), indicator: "green" });
                                frm.reload_doc();
                                d.hide();
                            }
                        }
                    });
                }
            );
        }
    });
    d.show();
}

function _restore_defaults_dialog(frm) {
    const d = new frappe.ui.Dialog({
        title: __("Khôi phục mặc định TT99/2025"),
        fields: [
            {
                fieldtype: "HTML",
                options: `<p class="text-muted">${__("Khôi phục cấu hình B01/B02/B03 về mặc định Thông tư 99/2025/TT-BTC. Có thể khôi phục toàn bộ hoặc chỉ một báo cáo.")}</p>`
            },
            {
                fieldtype: "Select",
                fieldname: "report",
                label: __("Khôi phục báo cáo"),
                options: ["Tất cả", "B01-DN (Tình hình tài chính)", "B02-DN (Kết quả HĐKD)", "B03-DN (Lưu chuyển tiền tệ)"],
                default: "Tất cả",
                description: __("Chọn báo cáo cần khôi phục. Chọn 'Tất cả' để khôi phục đồng thời cả 3 báo cáo.")
            }
        ],
        primary_action_label: __("Khôi phục"),
        primary_action(values) {
            const report_map = {
                "B01-DN (Tình hình tài chính)": "b01",
                "B02-DN (Kết quả HĐKD)": "b02",
                "B03-DN (Lưu chuyển tiền tệ)": "b03"
            };
            const reports = values.report === "Tất cả"
                ? ["b01", "b02", "b03"]
                : [report_map[values.report]];

            frappe.confirm(
                __("Khôi phục {0} về cấu hình TT99/2025? Các điều chỉnh thủ công sẽ bị mất.", [values.report]),
                () => {
                    const promises = reports.map(rpt => frappe.xcall("frappe.client.run_doc_method", {
                        dt: frm.doctype,
                        dn: frm.docname,
                        method: "restore_from_template",
                        args: { report: rpt, line_codes: null }
                    }));

                    Promise.all(promises)
                        .then(() => {
                            frappe.show_alert({ message: __("Đã khôi phục mặc định TT99/2025 thành công."), indicator: "green" });
                            frm.reload_doc();
                            d.hide();
                        })
                        .catch(() => {
                            frappe.msgprint(__("Khôi phục thất bại. Kiểm tra xem template TT99/2025 đã được cài đặt chưa."));
                        });
                }
            );
        }
    });
    d.show();
}
