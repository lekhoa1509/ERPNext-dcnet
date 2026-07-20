frappe.pages['bank-reconcile'].on_page_load = function (wrapper) {
  const page = frappe.ui.make_app_page({
    parent: wrapper,
    title: __('Bank Reconcile'),
    single_column: true,
  });

  page.main.html(frappe.render_template('bank_reconcile_main', {}));

  const state = {
    bank_account: null,
    import_name: null,
    transactions: [],
    filter: 'all',
    selected_names: [],
  };

  // Bank account picker
  frappe.db.get_list('Bank Account', { fields: ['name', 'account_name'], limit: 100 }).then((rows) => {
    const $sel = $('#br-bank-account-select');
    rows.forEach((r) => {
      $sel.append(`<option value="${r.name}">${r.account_name || r.name}</option>`);
    });
  });
  $(document).on('change', '#br-bank-account-select', function () {
    state.bank_account = $(this).val();
  });

  page.set_primary_action(__('Upload Statement'), () => {
    vn_banking.open_upload_dialog(state, page);
  });

  page.set_secondary_action(__('Re-run Match'), () => {
    if (!state.import_name) {
      frappe.msgprint(__('No import loaded'));
      return;
    }
    frappe.call({
      method: 'vn_banking.api.reconcile.trigger_rematch',
      args: { import_name: state.import_name },
      callback: () => vn_banking.load_transactions(state, page),
    });
  });

  // Load components
  vn_banking.init_txn_table(page, state);
  vn_banking.init_bulk_actions(page, state);

  // Realtime listeners
  frappe.realtime.on('vn_banking.import_progress', (data) => {
    if (data.import_name === state.import_name) {
      vn_banking.update_progress(page, data);
    }
  });
  frappe.realtime.on('vn_banking.import_done', (data) => {
    if (data.import_name === state.import_name) {
      vn_banking.load_transactions(state, page);
    }
  });
};

// Namespace stub
window.vn_banking = window.vn_banking || {};

// Stat bar (inline)
if (!vn_banking.init_stat_bar) {
  vn_banking.init_stat_bar = function () {};
}
if (!vn_banking.render_stats) {
  vn_banking.render_stats = function (page, state) {
    const $stats = $('#br-stats').empty();
    const txns = state.transactions || [];
    if (!txns.length) {
      $stats.html('');
      return;
    }
    const count = (c) => txns.filter((t) => (t.match_confidence || 'None') === c).length;
    const reconciled = txns.filter((t) => t.status === 'Reconciled').length;
    const with_pe = txns.filter((t) => t.existing_pe).length;
    $stats.html(
      '<b>' + txns.length + '</b> ' + __('transactions') + ' · ' +
      '<span class="br-confidence-high">' + count('High') + ' ' + __('matched') + '</span> · ' +
      '<span class="br-confidence-medium">' + (count('Medium') + count('Low')) + ' ' + __('suggested') + '</span> · ' +
      '<span class="br-confidence-none">' + count('None') + ' ' + __('unmatched') + '</span> · ' +
      '<span class="br-confidence-high">' + reconciled + ' ' + __('reconciled') + '</span>' +
      (with_pe ? ' · <b>' + with_pe + '</b> ' + __('existing PE found') : '')
    );
  };
}

// Bulk actions bar — primary impl in components/bulk_actions_bar.js. This
// fallback only fires if the component file failed to load.
if (!vn_banking.init_bulk_actions) {
  vn_banking.init_bulk_actions = function (page, state) {
    const $bar = $('#br-bulk-bar').empty();
    const $draft = $('<button class="btn btn-sm btn-primary mr-2">' + __('Create draft PEs for High matches') + '</button>');
    const $submit = $('<button class="btn btn-sm btn-success">' + __('Submit all draft PEs') + '</button>');
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
}
