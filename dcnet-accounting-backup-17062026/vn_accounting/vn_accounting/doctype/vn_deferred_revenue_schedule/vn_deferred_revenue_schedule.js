frappe.ui.form.on("VN Deferred Revenue Schedule", {
    refresh: function (frm) {
        if (frm.doc.docstatus === 0) {
            frm.add_custom_button(__("Sinh lịch tự động"), function () {
                frappe.confirm(
                    __("Sinh lại lịch ghi nhận (sẽ xóa các dòng hiện tại)?"),
                    function () {
                        frm.call("generate_lines").then(r => {
                            if (r.message) {
                                frappe.show_alert({message: __("Đã sinh {0} kỳ", [r.message]), indicator: "green"});
                                frm.reload_doc();
                            }
                        });
                    }
                );
            }, __("Hành động")).addClass("btn-primary");
        }
        if (frm.doc.docstatus === 1 && frm.doc.status === "Active") {
            frm.add_custom_button(__("Ghi nhận tất cả kỳ đến hạn"), function () {
                frappe.prompt({
                    fieldname: "as_of",
                    label: __("Ghi nhận đến ngày"),
                    fieldtype: "Date",
                    default: frappe.datetime.get_today(),
                    reqd: 1,
                }, function (vals) {
                    frm.call("recognize_all_due", { as_of_date: vals.as_of }).then(r => {
                        if (r.message) {
                            frappe.msgprint({
                                title: __("Kết quả"),
                                indicator: "green",
                                message: __("Đã post {0} phiếu kế toán.", [r.message.count]),
                            });
                            frm.reload_doc();
                        }
                    });
                }, __("Ghi nhận đến hạn"));
            }, __("Hành động")).addClass("btn-primary");
        }
        // Inline tip on top of form
        if (frm.doc.docstatus === 0 && !frm.doc.schedule_lines?.length) {
            frm.dashboard.add_comment(
                __("👉 Sau khi điền <i>Ngày bắt đầu, Ngày kết thúc, Tổng số tiền hoãn lại</i> + 2 tài khoản, bấm <b>Hành động → Sinh lịch tự động</b> để tạo các kỳ ghi nhận."),
                "blue", true
            );
        }
    },

    company: function (frm) {
        // Auto-fill accounts from VN Accounting Settings
        if (!frm.doc.deferred_account || !frm.doc.recognition_account) {
            frappe.db.get_value("VN Accounting Settings", "VN Accounting Settings",
                ["deferred_revenue_account"], function (s) {
                    if (s && s.deferred_revenue_account && !frm.doc.deferred_account) {
                        frm.set_value("deferred_account", s.deferred_revenue_account);
                    }
                });
        }
    },
});
