/**
 * Sales Invoice — tích hợp Lịch ghi nhận Doanh thu chưa thực hiện (TK 3387).
 *
 * Khi nào dùng?
 *   Khi khách thanh toán trước cho dịch vụ kéo dài nhiều kỳ (cước Internet,
 *   hosting, giấy phép phần mềm trả 6–12 tháng). Hạch toán ban đầu trên SI
 *   là Nợ TK 131 / Có TK doanh thu (5xx) hoặc Có TK 3387 — sau đó cần
 *   phân bổ doanh thu sang TK 5xx từng kỳ.
 *
 * Tích hợp:
 *   1. Nút "+ Tạo lịch ghi nhận DT chưa thực hiện" trên SI đã ghi sổ
 *      → mở hộp thoại nhập Ngày bắt đầu / Ngày kết thúc / TK doanh thu sẽ
 *      ghi nhận → tạo Schedule với reference_invoice = SI.name.
 *   2. Bảng "Lịch ghi nhận DT chưa thực hiện đã liên kết" hiển thị tất cả
 *      Schedule trỏ về SI này — bấm để mở chi tiết.
 */
frappe.ui.form.on("Sales Invoice", {
    refresh: function (frm) {
        if (frm.doc.docstatus !== 1) return;

        frm.add_custom_button(
            __("+ Lịch ghi nhận DT chưa thực hiện"),
            function () { _open_create_schedule_dialog(frm); },
            __("Hành động"),
        );

        _show_linked_schedules(frm);
    },
});

function _open_create_schedule_dialog(frm) {
    frappe.db.get_value(
        "VN Accounting Settings", "VN Accounting Settings",
        ["deferred_revenue_account"],
        function (s) {
            const default_deferred = (s && s.deferred_revenue_account) || "";

            const d = new frappe.ui.Dialog({
                title: __("Tạo lịch ghi nhận Doanh thu chưa thực hiện"),
                fields: [
                    {
                        fieldtype: "HTML", fieldname: "intro",
                        options: `<div class='text-muted small'>
                            ${__("Dịch vụ trả trước nhiều kỳ — hệ thống sẽ tạo lịch phân bổ doanh thu Nợ TK 3387 / Có TK doanh thu mỗi kỳ.")}
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
                        label: __("Tổng số tiền hoãn lại"),
                        default: frm.doc.base_grand_total || frm.doc.grand_total,
                        description: __("Mặc định = tổng tiền hóa đơn. Có thể sửa nếu chỉ một phần là dịch vụ trả trước."),
                    },
                    {
                        fieldtype: "Select", fieldname: "amortization_method", reqd: 1,
                        label: __("Phương pháp phân bổ"),
                        options: "Monthly\nQuarterly\nDaily\nOne-shot",
                        default: "Monthly",
                    },
                    { fieldtype: "Section Break" },
                    {
                        fieldtype: "Link", fieldname: "recognition_account", reqd: 1,
                        label: __("TK doanh thu sẽ ghi nhận"),
                        options: "Account",
                        description: __("TK doanh thu (ví dụ 5111, 51131-51136 ...) — nơi sẽ ghi Có khi ghi nhận từng kỳ."),
                        get_query: function () {
                            return {
                                filters: {
                                    company: frm.doc.company,
                                    is_group: 0,
                                    root_type: "Income",
                                },
                            };
                        },
                    },
                    {
                        fieldtype: "Link", fieldname: "deferred_account", reqd: 1,
                        label: __("TK doanh thu chưa thực hiện"),
                        options: "Account",
                        default: default_deferred,
                        description: __("Mặc định TK 3387 (từ Cài đặt kế toán)."),
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
                        method: "vn_accounting.vn_accounting.doctype.vn_deferred_revenue_schedule.vn_deferred_revenue_schedule.create_from_sales_invoice",
                        args: {
                            sales_invoice: frm.doc.name,
                            start_date: vals.start_date,
                            end_date: vals.end_date,
                            total_amount: vals.total_amount,
                            amortization_method: vals.amortization_method,
                            recognition_account: vals.recognition_account,
                            deferred_account: vals.deferred_account,
                        },
                        callback: function (r) {
                            if (r.message) {
                                d.hide();
                                frappe.show_alert({
                                    message: __("Đã tạo lịch <b>{0}</b> với {1} kỳ", [r.message.name, r.message.lines]),
                                    indicator: "green",
                                });
                                frappe.set_route("Form", "VN Deferred Revenue Schedule", r.message.name);
                            }
                        },
                    });
                },
            });
            d.show();
        },
    );
}

function _show_linked_schedules(frm) {
    frappe.call({
        method: "frappe.client.get_list",
        args: {
            doctype: "VN Deferred Revenue Schedule",
            filters: [
                ["reference_invoice", "=", frm.doc.name],
                ["docstatus", "!=", 2],
            ],
            fields: ["name", "status", "total_amount", "recognized_amount",
                     "remaining_amount", "start_date", "end_date", "amortization_method"],
            order_by: "creation desc",
        },
        callback: function (r) {
            $(frm.layout.wrapper).find(".vn-drs-linked-wrapper").remove();
            const rows = r.message || [];
            if (!rows.length) return;

            const html = `<div class="vn-drs-linked-wrapper form-section">
                <div class="section-head">${__("Lịch ghi nhận Doanh thu chưa thực hiện đã liên kết")}</div>
                <div class="form-column" style="padding: 0 15px;">
                    <table class="table table-bordered table-condensed" style="margin-bottom: 0;">
                        <thead><tr>
                            <th>${__("Mã lịch")}</th>
                            <th>${__("Từ ngày")}</th>
                            <th>${__("Đến ngày")}</th>
                            <th>${__("Phương pháp")}</th>
                            <th class="text-right">${__("Tổng tiền")}</th>
                            <th class="text-right">${__("Đã ghi nhận")}</th>
                            <th class="text-right">${__("Còn lại")}</th>
                            <th>${__("Trạng thái")}</th>
                        </tr></thead>
                        <tbody>
                        ${rows.map(r => `<tr>
                            <td><a href="/app/vn-deferred-revenue-schedule/${encodeURIComponent(r.name)}">${frappe.utils.escape_html(r.name)}</a></td>
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
