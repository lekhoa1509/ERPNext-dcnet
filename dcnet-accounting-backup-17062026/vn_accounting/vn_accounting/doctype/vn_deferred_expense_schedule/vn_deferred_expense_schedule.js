frappe.ui.form.on("VN Deferred Expense Schedule", {
    refresh: function (frm) {
        if (frm.doc.docstatus === 0) {
            frm.add_custom_button(__("Sinh lịch tự động"), function () {
                frappe.confirm(__("Sinh lại lịch phân bổ (sẽ xoá các dòng hiện tại)?"), function () {
                    frm.call("generate_lines").then(r => {
                        if (r.message) {
                            frappe.show_alert({message: __("Đã sinh {0} kỳ", [r.message]), indicator: "green"});
                            frm.reload_doc();
                        }
                    });
                });
            }, __("Hành động")).addClass("btn-primary");
        }
        if (frm.doc.docstatus === 1 && frm.doc.status === "Active") {
            frm.add_custom_button(__("Phân bổ tất cả kỳ đến hạn"), function () {
                frappe.prompt({
                    fieldname: "as_of", label: __("Phân bổ đến ngày"),
                    fieldtype: "Date", default: frappe.datetime.get_today(), reqd: 1,
                }, function (vals) {
                    frm.call("recognize_all_due", { as_of_date: vals.as_of }).then(r => {
                        if (r.message) {
                            frappe.msgprint({title: __("Kết quả"), indicator: "green",
                                message: __("Đã post {0} phiếu kế toán.", [r.message.count])});
                            frm.reload_doc();
                        }
                    });
                }, __("Phân bổ đến hạn"));
            }, __("Hành động")).addClass("btn-primary");
        }
        if (frm.doc.docstatus === 0 && !frm.doc.schedule_lines?.length) {
            frm.dashboard.add_comment(
                __("👉 Sau khi điền <i>Ngày bắt đầu, Ngày kết thúc, Tổng số tiền chờ phân bổ</i> + 2 tài khoản, bấm <b>Hành động → Sinh lịch tự động</b>."),
                "blue", true
            );
        }
    },
    company: function (frm) {
        if (!frm.doc.deferred_account) {
            frappe.db.get_value("VN Accounting Settings", "VN Accounting Settings",
                ["deferred_expense_account"], function (s) {
                    if (s && s.deferred_expense_account) {
                        frm.set_value("deferred_account", s.deferred_expense_account);
                    }
                });
        }
    },
});
