(function () {
  if (!window.vn_banking) window.vn_banking = {};

  vn_banking.init_bulk_actions = function (page, state) {
    const $bar = $('#br-bulk-bar').empty();
    const $draft = $(`<button class="btn btn-sm btn-primary mr-2">${__('Create draft PEs for High matches')}</button>`);
    const $submit = $(`<button class="btn btn-sm btn-success">${__('Submit all draft PEs')}</button>`);
    // FB-594 — "Reconcile all found PEs" removed from bulk-bar. Per-row
    // Reconcile button (debit rows with existing_pe) covers the same need.
    $bar.append($draft).append($submit);

    $draft.on('click', () => {
      if (!state.import_name) { frappe.msgprint(__('No import loaded')); return; }
      frappe.confirm(__('Create draft PE for every High-confidence row?'), () => {
        frappe.call({
          method: 'vn_banking.api.reconcile.bulk_create_pe',
          args: { import_name: state.import_name, only_high_confidence: 1, submit: 0 },
          freeze: true, freeze_message: __('Creating Payment Entries...'),
          callback: (r) => {
            frappe.show_alert({ message: __('{0} PEs created', [(r.message.created || []).length]), indicator: 'green' });
            if ((r.message.errors || []).length) {
              frappe.msgprint({ title: __('Errors'), message: r.message.errors.join('<br>'), indicator: 'orange' });
            }
            vn_banking.load_transactions(state, page);
          },
        });
      });
    });

    $submit.on('click', () => {
      if (!state.import_name) return;
      frappe.confirm(__('Submit ALL draft Payment Entries belonging to this import?'), () => {
        frappe.call({
          method: 'vn_banking.api.reconcile.bulk_create_pe',
          args: { import_name: state.import_name, only_high_confidence: 1, submit: 1 },
          freeze: true, freeze_message: __('Submitting...'),
          callback: () => vn_banking.load_transactions(state, page),
        });
      });
    });
  };
})();
