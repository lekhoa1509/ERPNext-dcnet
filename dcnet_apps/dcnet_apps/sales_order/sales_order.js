/* eslint-disable */
// Custom Client Script for Sales Order

frappe.ui.form.on('Sales Order', {
    onload: function(frm) {
        if (frm.is_new() && frm.doc.order_type) {
            update_custom_sales_channel(frm);
        }
    },
    order_type: function(frm) {
        update_custom_sales_channel(frm);
    }
});

function update_custom_sales_channel(frm) {
    const retail_types = ['Sales', 'Utility Items', 'Fitting'];
    
    // Set custom_sales_channel: Retail if order_type matches, else empty ("")
    const channel = retail_types.includes(frm.doc.order_type) ? 'Retail' : '';
    
    frm.set_value('custom_sales_channel', channel);
}
