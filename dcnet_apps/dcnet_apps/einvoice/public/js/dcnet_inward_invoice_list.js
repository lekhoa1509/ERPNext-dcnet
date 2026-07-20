
frappe.listview_settings['EInvoice Inward'] = {
    refresh: function(listview) {
        listview.page.add_inner_button(__('Cập nhật Hóa đơn đầu vào mới'), function() {
            frappe.call({
                method: 'dcnet_apps.einvoice.api.sync_inward_invoices',
                freeze: true,
                freeze_message: __('Đang đồng bộ hóa đơn từ nhà cung cấp...'),
                callback: function(r) {
                    if (r.message) {
                        const res = r.message;
                        let msg = `Đồng bộ hoàn tất: Tìm thấy ${res.fetched} hóa đơn.`;
                        if (res.new > 0) msg += ` (Thêm mới: ${res.new})`;
                        if (res.dup > 0) msg += ` (Trùng: ${res.dup})`;
                        if (res.errors > 0) msg += ` (Lỗi: ${res.errors})`;
                        
                        frappe.msgprint({
                            title: __('Kết quả đồng bộ'),
                            message: msg,
                            indicator: res.new > 0 ? 'green' : 'orange'
                        });
                        listview.refresh();
                    }
                }
            });
        });
    }
};
