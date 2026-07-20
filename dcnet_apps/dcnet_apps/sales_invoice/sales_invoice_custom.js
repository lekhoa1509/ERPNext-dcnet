/* eslint-disable */
// Unified Client Script for Sales Invoice

frappe.ui.form.on('Sales Invoice', {
    onload(frm) {
        frm.trigger('setup_order_info');
    },
    refresh(frm) {
        frm.trigger('setup_order_info');
    },
    custom_order_type(frm) {
        // Only run logic if field is editable
        if (!frm.df.read_only && !frm.get_field('custom_order_type').df.read_only) {
            frm.trigger('update_sales_channel_by_type');
        }
    },
    setup_order_info(frm) {
        // Check if any item is linked to a Sales Order
        const so_item = (frm.doc.items || []).find(item => item.sales_order);
        const so_name = so_item ? so_item.sales_order : null;

        if (so_name) {
            frappe.call({
                method: "frappe.client.get_value",
                args: {
                    doctype: "Sales Order",
                    filters: { name: so_name },
                    fieldname: ["order_type", "custom_sales_channel"]
                },
                callback: function(r) {
                    if (r.message) {
                        // Sync values from Sales Order and set as read-only
                        frm.set_value('custom_order_type', r.message.order_type);
                        frm.set_value('custom_sales_channel', r.message.custom_sales_channel);

                        frm.set_df_property('custom_order_type', 'read_only', 1);
                        frm.set_df_property('custom_sales_channel', 'read_only', 1);
                    }
                }
            });
        } else {
            // Not linked to Sales Order: Allow manual editing
            frm.set_df_property('custom_order_type', 'read_only', 0);
            frm.set_df_property('custom_sales_channel', 'read_only', 0);
            
            // Apply business logic for manual selection
            frm.trigger('update_sales_channel_by_type');
        }
    },
    update_sales_channel_by_type(frm) {
        const retail_types = ['Sales', 'Utility Items', 'Fitting'];
        const is_retail = retail_types.includes(frm.doc.custom_order_type);
        
        frm.set_value('custom_sales_channel', is_retail ? 'Retail' : '');
    }
});
