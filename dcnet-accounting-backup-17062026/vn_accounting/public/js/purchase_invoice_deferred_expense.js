/**
 * Purchase Invoice — tích hợp Lịch phân bổ Chi phí trả trước (TK 242).
 *
 * Khi nào dùng?
 *   Khi công ty trả tiền trước cho khoản chi phí kéo dài nhiều kỳ
 *   (thuê văn phòng/kho 6–12 tháng, bảo hiểm cả năm, giấy phép phần mềm,
 *   hợp đồng bảo trì). Hạch toán ban đầu trên PI là Nợ TK 242 / Có TK 331
 *   — sau đó cần phân bổ chi phí sang TK 6xx từng kỳ.
 *
 * Tích hợp:
 *   1. Nút "+ Tạo lịch phân bổ CP trả trước" trên PI đã ghi sổ
 *   2. Bảng "Lịch phân bổ CP trả trước đã liên kết" hiển thị schedule
 *      trỏ về PI này.
 */
frappe.ui.form.on("Purchase Invoice", {
    refresh: function (frm) {
        if (frm.doc.docstatus !== 1) return;

        frm.add_custom_button(
            __("+ Lịch phân bổ CP trả trước"),
            function () { _open_create_des_dialog(frm); },
            __("Hành động"),
        );

        _show_linked_des_schedules(frm);
    },
});

function _open_create_des_dialog(frm) {
    frappe.db.get_value(
        "VN Accounting Settings", "VN Accounting Settings",
        ["deferred_expense_account"],
        function (s) {
            const default_deferred = (s && s.deferred_expense_account) || "";

            const d = new frappe.ui.Dialog({
                title: __("Tạo lịch phân bổ Chi phí trả trước"),
                fields: [
                    {
                        fieldtype: "HTML", fieldname: "intro",
                        options: `<div class='text-muted small'>
                            ${__("Chi phí trả trước cho nhiều kỳ — hệ thống sẽ tạo lịch phân bổ Nợ TK 6xx / Có TK 242 mỗi kỳ.")}
                        </div>`,
                    },
                    {
                        fieldtype: "Date", fieldname: "start_date", reqd: 1,
                        label: __("Ngày bắt đầu"),
                        default: frm.doc.posting_date,
                    },
                    {
                        fieldtype: "Date", fieldname: "end_date", reqd: 1,
                        label: __("Ngày kết thúc"),
                    },
                    { fieldtype: "Column Break" },
                    {
                        fieldtype: "Currency", fieldname: "total_amount", reqd: 1,
                        label: __("Tổng số tiền chờ phân bổ"),
                        default: frm.doc.base_grand_total || frm.doc.grand_total,
                        description: __("Mặc định = tổng tiền hóa đơn. Có thể sửa nếu chỉ một phần là trả trước."),
                    },
                    {
                        fieldtype: "Select", fieldname: "amortization_method", reqd: 1,
                        label: __("Phương pháp phân bổ"),
                        options: "Monthly\nQuarterly\nDaily\nOne-shot",
                        default: "Monthly",
                    },
                    { fieldtype: "Section Break" },
                    {
                        fieldtype: "Link", fieldname: "expense_account", reqd: 1,
                        label: __("TK chi phí sẽ ghi nhận"),
                        options: "Account",
                        description: __("TK chi phí (ví dụ 6322, 6323, 6427, 6421 ...) — nơi sẽ ghi Nợ khi phân bổ từng kỳ."),
                        get_query: function () {
                            return {
                                filters: {
                                    company: frm.doc.company,
                                    is_group: 0,
                                    root_type: "Expense",
                                },
                            };
                        },
                    },
                    {
                        fieldtype: "Link", fieldname: "deferred_account", reqd: 1,
                        label: __("TK chi phí chờ phân bổ"),
                        options: "Account",
                        default: default_deferred,
                        description: __("Mặc định TK 242 (từ Cài đặt kế toán)."),
                        get_query: function () {
                            return {
                                filters: {
                                    company: frm.doc.company,
                                    is_group: 0,
                                },
                            };
                        },
                    },
                ],
                primary_action_label: __("Tạo lịch + Sinh các kỳ"),
                primary_action: function (vals) {
                    frappe.call({
                        method: "vn_accounting.vn_accounting.doctype.vn_deferred_expense_schedule.vn_deferred_expense_schedule.create_from_purchase_invoice",
                        args: {
                            purchase_invoice: frm.doc.name,
                            start_date: vals.start_date,
                            end_date: vals.end_date,
                            total_amount: vals.total_amount,
                            amortization_method: vals.amortization_method,
                            expense_account: vals.expense_account,
                            deferred_account: vals.deferred_account,
                        },
                        callback: function (r) {
                            if (r.message) {
                                d.hide();
                                frappe.show_alert({
                                    message: __("Đã tạo lịch <b>{0}</b> với {1} kỳ", [r.message.name, r.message.lines]),
                                    indicator: "green",
                                });
                                frappe.set_route("Form", "VN Deferred Expense Schedule", r.message.name);
                            }
                        },
                    });
                },
            });
            d.show();
        },
    );
}

function _show_linked_des_schedules(frm) {
    frappe.call({
        method: "frappe.client.get_list",
        args: {
            doctype: "VN Deferred Expense Schedule",
            filters: [
                ["reference_invoice", "=", frm.doc.name],
                ["docstatus", "!=", 2],
            ],
            fields: ["name", "status", "total_amount", "recognized_amount",
                     "remaining_amount", "start_date", "end_date", "amortization_method"],
            order_by: "creation desc",
        },
        callback: function (r) {
            $(frm.layout.wrapper).find(".vn-des-linked-wrapper").remove();
            const rows = r.message || [];
            if (!rows.length) return;

            const html = `<div class="vn-des-linked-wrapper form-section">
                <div class="section-head">${__("Lịch phân bổ Chi phí trả trước đã liên kết")}</div>
                <div class="form-column" style="padding: 0 15px;">
                    <table class="table table-bordered table-condensed" style="margin-bottom: 0;">
                        <thead><tr>
                            <th>${__("Mã lịch")}</th>
                            <th>${__("Từ ngày")}</th>
                            <th>${__("Đến ngày")}</th>
                            <th>${__("Phương pháp")}</th>
                            <th class="text-right">${__("Tổng tiền")}</th>
                            <th class="text-right">${__("Đã phân bổ")}</th>
                            <th class="text-right">${__("Còn lại")}</th>
                            <th>${__("Trạng thái")}</th>
                        </tr></thead>
                        <tbody>
                        ${rows.map(r => `<tr>
                            <td><a href="/app/vn-deferred-expense-schedule/${encodeURIComponent(r.name)}">${frappe.utils.escape_html(r.name)}</a></td>
                            <td>${frappe.format(r.start_date, {fieldtype: "Date"})}</td>
                            <td>${frappe.format(r.end_date, {fieldtype: "Date"})}</td>
                            <td>${__(r.amortization_method)}</td>
                            <td class="text-right">${format_currency(r.total_amount, frm.doc.currency)}</td>
                            <td class="text-right">${format_currency(r.recognized_amount, frm.doc.currency)}</td>
                            <td class="text-right">${format_currency(r.remaining_amount, frm.doc.currency)}</td>
                            <td><span class="indicator-pill ${r.status === 'Completed' ? 'green' : r.status === 'Active' ? 'blue' : 'gray'}">${__(r.status)}</span></td>
                        </tr>`).join("")}
                        </tbody>
                    </table>
                </div>
            </div>`;
            const $details = $(frm.layout.wrapper).find(".tab-pane").first();
            $details.append(html);
        },
    });
}
