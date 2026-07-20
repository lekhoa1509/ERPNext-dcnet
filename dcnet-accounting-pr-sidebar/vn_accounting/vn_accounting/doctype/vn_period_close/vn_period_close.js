frappe.ui.form.on("VN Period Close", {
    refresh: function (frm) {
        if (frm.doc.docstatus === 0) {
            frm.add_custom_button(__("Xem trước các TK"), function () {
                frm.call("preview").then(r => {
                    if (r.message) {
                        frappe.show_alert({
                            message: __("{0} tài khoản — DT {1} — CP {2} — Lãi/Lỗ {3}", [
                                r.message.lines,
                                format_currency(r.message.revenue_total),
                                format_currency(r.message.expense_total),
                                format_currency(r.message.net_profit),
                            ]),
                            indicator: r.message.net_profit >= 0 ? "green" : "orange",
                        });
                        frm.reload_doc();
                    }
                });
            }, __("Hành động")).addClass("btn-primary");
        }
        if (frm.doc.docstatus === 1 && frm.doc.posted_je) {
            frm.add_custom_button(__("Mở phiếu kế toán kết chuyển"), function () {
                frappe.set_route("Form", "Journal Entry", frm.doc.posted_je);
            });
        }
        if (frm.doc.docstatus === 0 && !frm.doc.preview_lines?.length) {
            frm.dashboard.add_comment(
                __("👉 Sau khi điền <i>Ngày kết thúc kỳ</i>, bấm <b>Hành động → Xem trước các TK</b> để liệt kê các tài khoản sẽ kết chuyển. Sau khi kiểm tra xong, bấm <b>Ghi sổ</b> để hệ thống tự sinh phiếu kế toán."),
                "blue", true
            );
        }
    },
    company: function (frm) {
        if (!frm.doc.income_summary_account || !frm.doc.retained_earnings_account) {
            frappe.db.get_value("VN Accounting Settings", "VN Accounting Settings",
                ["pnl_account_911", "retained_earnings_current_year"], function (s) {
                    if (s) {
                        if (s.pnl_account_911 && !frm.doc.income_summary_account)
                            frm.set_value("income_summary_account", s.pnl_account_911);
                        if (s.retained_earnings_current_year && !frm.doc.retained_earnings_account)
                            frm.set_value("retained_earnings_account", s.retained_earnings_current_year);
                    }
                });
        }
    },
});
