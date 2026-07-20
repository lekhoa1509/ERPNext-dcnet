frappe.ui.form.on('Bank Statement Settings', {
  refresh(frm) {
    // Show helper link to re-run match on last import
    frm.add_custom_button(__('Test on last import'), () => {
      frappe.call({
        method: 'vn_banking.api.reconcile.test_matching_on_last_import',
        callback: (r) => {
          if (r.message && !r.message.error) {
            const fmt = (arr) => (arr || []).map((r) => `${r.match_confidence || 'None'}: ${r.c}`).join(', ');
            frappe.msgprint({
              title: __('Match Preview'),
              message: `${__('Before')}: ${fmt(r.message.before)}<br>${__('After')}: ${fmt(r.message.after)}`,
            });
          } else {
            frappe.msgprint(__('No previous import to test against.'));
          }
        },
      });
    });

    // Broadcast settings change so open Bank Reconcile pages can re-run match
    frm.add_custom_button(__('Notify open reconcile pages'), () => {
      frappe.realtime.publish('bank_statement_settings_updated', {});
      frappe.show_alert({ message: __('Notified'), indicator: 'blue' });
    });
  },

  after_save(frm) {
    frappe.realtime.publish('bank_statement_settings_updated', {});
  },
});
