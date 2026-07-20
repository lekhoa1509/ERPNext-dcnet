frappe.ui.form.on('Sales Invoice', {
    refresh(frm) {
        if (!frm.doc.name || frm.doc.docstatus === 0) return;

        frm.add_custom_button(__('Warranty Status'), () => {
            frappe.set_route('query-report', 'Serial No Warranty Status', {
                sales_invoice_no: frm.doc.name
            });
        }, __('View'));
    }
});
