// PE form button: "Tạo draft hoa hồng PAKD" — proportional auto-post.
// Hiện khi PE có Custom Field linked_pakd (set qua bank-reconcile dialog) +
// docstatus=1. KTT click → API tính tỷ lệ PE/PAKD.total → tạo draft JE cho mỗi
// commission_line + beneficiary_line Pending (incremental theo auto_posted_pct).
// Mỗi draft JE register vào Auto Generated Doc Registry.

frappe.ui.form.on('Payment Entry', {
    refresh(frm) {
        if (frm.doc.docstatus !== 1) return;
        if (!frm.doc.linked_pakd) return;

        frm.add_custom_button(__('Tạo draft hoa hồng PAKD'), () => {
            frappe.confirm(
                __('Tạo draft JE proportional cho PAKD {0}? Tỷ lệ = {1} / total_revenue PAKD. ' +
                   'Mỗi draft JE sẽ register vào Auto Generated Doc Registry để KTT review + ghi sổ.',
                   [frm.doc.linked_pakd, frappe.format(frm.doc.paid_amount, {fieldtype: 'Currency'})]),
                () => {
                    frappe.call({
                        method: 'dcnet_pakd.dcnet_pakd.api.auto_post_pakd_proportional',
                        args: { payment_entry: frm.doc.name },
                        freeze: true, freeze_message: __('Đang tạo draft JE...'),
                        callback: (r) => {
                            const msg = r.message || {};
                            const je_count = (msg.je_names || []).length;
                            if (je_count === 0) {
                                frappe.msgprint({
                                    title: __('Không có line nào để đăng'),
                                    message: __('Tất cả Pending lines đã đạt 100% hoặc bỏ qua. Skipped: {0}',
                                                [(msg.skipped || []).join('<br>') || '(không có)']),
                                    indicator: 'orange',
                                });
                                return;
                            }
                            const je_links = msg.je_names.map(n =>
                                `<a href="/app/journal-entry/${encodeURIComponent(n)}" target="_blank">${n}</a>`
                            ).join('<br>');
                            frappe.msgprint({
                                title: __('Đã tạo {0} draft JE ({1}%)', [je_count, msg.pct]),
                                message: __('PAKD: {0}<br>Lines processed: {1}<br>JEs:<br>{2}',
                                            [msg.pakd, msg.lines_processed, je_links]),
                                indicator: 'green',
                            });
                        },
                    });
                }
            );
        }, __('PAKD'));
    },
});
