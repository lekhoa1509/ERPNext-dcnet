(function () {
  if (!window.vn_banking) window.vn_banking = {};

  vn_banking.init_txn_table = function (page, state) {
    page.add_inner_button(__('All'), () => { state.filter = 'all'; vn_banking.render_txns(page, state); });
    page.add_inner_button(__('Credits'), () => { state.filter = 'credit'; vn_banking.render_txns(page, state); });
    page.add_inner_button(__('Debits'), () => { state.filter = 'debit'; vn_banking.render_txns(page, state); });

    // Select-all checkbox
    $('#br-select-all').on('change', function () {
      const checked = this.checked;
      $('#br-txn-tbody input.br-row-check').prop('checked', checked);
      state.selected_names = checked
        ? state.transactions.filter((t) => t.status !== 'Reconciled').map((t) => t.name)
        : [];
    });
  };

  vn_banking.load_transactions = function (state, page) {
    if (!state.import_name) return;
    frappe.call({
      method: 'vn_banking.api.reconcile.get_import_transactions',
      args: { import_name: state.import_name, direction_filter: state.filter },
      callback: (r) => {
        state.transactions = r.message || [];
        state.selected_names = [];
        vn_banking.render_txns(page, state);
        vn_banking.render_stats(page, state);
      },
    });
  };

  vn_banking.render_txns = function (page, state) {
    const $tbody = $('#br-txn-tbody').empty();
    const $empty = $('#br-empty-state');
    const rows = _filter_rows(state);

    if (!rows.length) {
      $empty.show();
      return;
    }
    $empty.hide();

    rows.forEach((t) => {
      const $tr = _build_row(t, state, page);
      $tbody.append($tr);
    });
  };

  function _filter_rows(state) {
    return (state.transactions || []).filter((t) => {
      if (state.filter === 'credit') return (t.deposit || 0) > 0;
      if (state.filter === 'debit') return (t.withdrawal || 0) > 0;
      return true;
    });
  }

  function _build_row(t, state, page) {
    const is_credit = (t.deposit || 0) > 0;
    const amount = is_credit ? t.deposit : t.withdrawal;
    const direction = is_credit ? '↓' : '↑';
    const amount_class = is_credit ? 'br-amount-credit' : 'br-amount-debit';
    const conf = t.match_confidence || 'None';
    const dot_class = { High: 'br-dot-high', Medium: 'br-dot-medium', Low: 'br-dot-low', None: 'br-dot-none' }[conf];
    const is_reconciled = t.status === 'Reconciled';

    const $tr = $('<tr>').toggleClass('br-row-reconciled', is_reconciled);

    // Checkbox
    const $check = $('<td class="br-col-check">');
    if (!is_reconciled) {
      $check.html(`<input type="checkbox" class="br-row-check" data-name="${frappe.utils.escape_html(t.name)}">`);
    }
    $tr.append($check);

    // Confidence dot
    $tr.append(`<td class="br-col-status"><span class="br-dot ${dot_class}" title="${conf}">●</span></td>`);

    // Date
    $tr.append(`<td class="br-col-date">${frappe.datetime.str_to_user(t.date)}</td>`);

    // Description
    const desc = frappe.utils.escape_html(t.description || '');
    $tr.append(`<td class="br-col-desc"><span class="br-desc-text" title="${desc}">${desc}</span></td>`);

    // Amount
    $tr.append(`<td class="br-col-amount"><span class="${amount_class}">${frappe.format(amount, {fieldtype: 'Currency'})} ${direction}</span></td>`);

    // Reference
    $tr.append(`<td class="br-col-ref">${frappe.utils.escape_html(t.reference_number || '')}</td>`);

    // Party (inline editable)
    const $party_td = $('<td class="br-col-party br-party-cell">');
    if (is_reconciled) {
      $party_td.text(t.suggested_party || '');
    } else {
      _render_party_control($party_td, t, is_credit, state, page);
    }
    $tr.append($party_td);

    // Invoice / PE column
    const $match_td = $('<td class="br-col-match">');
    _render_match_column($match_td, t, is_credit, state, page);
    $tr.append($match_td);

    // Actions
    const $actions_td = $('<td class="br-col-actions br-actions-cell">');
    _render_actions($actions_td, t, is_credit, state, page);
    $tr.append($actions_td);

    return $tr;
  }

  function _render_party_control($td, t, is_credit, state, page) {
    const party_type = is_credit ? 'Customer' : 'Supplier';
    // Store current party in a data attribute for reading later
    $td.attr('data-party-type', party_type);
    $td.attr('data-party', t.suggested_party || '');

    const $wrapper = $('<div>');
    $td.append($wrapper);
    // FB-519: capture value via both native change AND Awesomplete's
    // selectcomplete event. Picking a suggestion from the autocomplete
    // dropdown does NOT fire native `change`, so listening to `change`
    // alone misses the most common selection path.
    const sync_party = (val) => {
      t.suggested_party = val;
      t.suggested_party_type = party_type;
      $td.attr('data-party', val);
    };
    const ctrl = frappe.ui.form.make_control({
      df: {
        fieldtype: 'Link',
        options: party_type,
        fieldname: 'party_' + t.name,
        placeholder: __(party_type),
        change: function () {
          // Frappe Control invokes df.change(value) when set_value runs,
          // including Awesomplete autocomplete picks (covers all paths).
          sync_party(ctrl.get_value());
        },
      },
      parent: $wrapper[0],
      render_input: true,
      only_input: true,
    });
    ctrl.set_value(t.suggested_party || '');
    ctrl.$input.css({ height: '28px', 'font-size': '12px' });
    // Belt-and-suspenders: also re-sync on awesomplete-selectcomplete
    // in case df.change is short-circuited by an early `if (this.value === val) return`.
    ctrl.$input.on('change awesomplete-selectcomplete', () => {
      sync_party(ctrl.get_value());
    });
  }

  function _render_match_column($td, t, is_credit, state, page) {
    // Reconciled — show linked PE
    if (t.status === 'Reconciled') {
      $td.html(`<span class="br-reconciled-badge">✓ ${__('Reconciled')}</span>`);
      return;
    }

    // Debit with existing PE found
    if (!is_credit && t.existing_pe) {
      const pe = t.existing_pe;
      const status_label = pe.docstatus === 1 ? __('Submitted') : __('Draft');
      $td.html(`
        <span class="br-pe-found">
          <a href="/app/payment-entry/${pe.name}" target="_blank">${pe.name}</a>
          <small>(${status_label}, ${frappe.format(pe.paid_amount, {fieldtype: 'Currency'})})</small>
        </span>
      `);
      return;
    }

    // Show suggested invoices as pills
    const suggestions = (t.suggestions || []).filter((s) => s.selected);
    if (suggestions.length) {
      suggestions.forEach((s) => {
        $td.append(`<span class="br-invoice-pill">${s.invoice_name} (${frappe.format(s.allocated_amount, {fieldtype: 'Currency'})})</span> `);
      });
    } else if (t.match_confidence && t.match_confidence !== 'None') {
      // Has match but no selected invoices — show all suggestions
      (t.suggestions || []).forEach((s) => {
        $td.append(`<span class="br-invoice-pill">${s.invoice_name}</span> `);
      });
    } else {
      // FB-521 — make "Chưa khớp" clickable to open an invoice picker
      // filtered by amount tolerance + date proximity. Picking an invoice
      // auto-fills the row's party.
      const $link = $(
        `<a href="#" class="br-pick-invoice text-muted" title="${__('Pick invoice')}">${__('No match')}</a>`
      );
      $link.on('click', (e) => {
        e.preventDefault();
        _open_invoice_picker_by_amount(t, is_credit, state, page);
      });
      $td.append($link);
    }
  }

  function _open_invoice_picker_by_amount(t, is_credit, state, page) {
    // FB-591 — if the row already has a suggested_party, send it so the
    // endpoint switches to "list every outstanding invoice for THIS party"
    // mode (relaxed amount/date filter). Otherwise stay in amount-based
    // mode (the FB-521 default).
    const $row = $('#br-txn-tbody tr').filter(function () {
      return $(this).find('.br-col-party').data('party') !== undefined &&
             $(this).find('input[type=checkbox][data-name]').data('name') === t.name;
    });
    const $party_cell = $row.find('.br-col-party');
    const picked_party = $party_cell.attr('data-party') || t.suggested_party || '';
    const args = { transaction_name: t.name };
    if (picked_party) args.party = picked_party;

    frappe.call({
      method: 'vn_banking.api.reconcile.get_invoices_for_amount',
      args,
      callback: (r) => {
        const rows = r.message || [];
        if (!rows.length) {
          const empty_msg = picked_party
            ? __('No outstanding invoices for {0}.', [picked_party])
            : __('No outstanding invoices within tolerance/date window for this amount.');
          frappe.msgprint(empty_msg);
          return;
        }
        const amount = is_credit ? t.deposit : t.withdrawal;
        const doctype_label = is_credit ? __('Sales Invoice') : __('Purchase Invoice');
        const party_label = is_credit ? __('Customer') : __('Supplier');
        const fmt_amount = (n) => frappe.format(n, { fieldtype: 'Currency' });
        const row_html = (inv) => {
          const diff_pct = amount ? Math.round((inv.amount_diff / amount) * 1000) / 10 : 0;
          const diff_label = inv.amount_diff < 1
            ? `<span class="text-success">${__('exact')}</span>`
            : `${fmt_amount(inv.amount_diff)} (${diff_pct}%)`;
          return (
            `<button class="btn btn-default btn-sm br-pick-inv-btn d-block text-left mb-1 w-100" ` +
            `data-name="${frappe.utils.escape_html(inv.name)}" style="white-space:normal;">` +
            `<b>${inv.name}</b> — ${frappe.utils.escape_html(inv.party)}<br>` +
            `<small class="text-muted">${fmt_amount(inv.outstanding_amount)} · ${inv.posting_date} · ${__('diff')}: ${diff_label}</small>` +
            `</button>`
          );
        };
        const header_msg = picked_party
          ? __('Outstanding invoices for {0}. Click a row to link this transaction.', [`<b>${frappe.utils.escape_html(picked_party)}</b>`])
          : __('Click a row to link this transaction. {0} auto-fills.', [party_label]);
        const list_html =
          `<p class="text-muted">${header_msg}</p>` +
          '<div class="br-picker-list" style="max-height:340px;overflow-y:auto;">' +
          rows.map(row_html).join('') +
          '</div>';

        const title = picked_party
          ? __('Pick {0} for {1} — {2}', [doctype_label, fmt_amount(amount), picked_party])
          : __('Pick {0} for {1}', [doctype_label, fmt_amount(amount)]);
        const d = new frappe.ui.Dialog({
          title,
          fields: [{ fieldtype: 'HTML', fieldname: 'picker', options: list_html }],
        });
        d.show();
        // Each row commits immediately. Simpler UX than radio+submit.
        d.$wrapper.on('click', '.br-pick-inv-btn', function () {
          const picked = $(this).data('name');
          const inv = rows.find((r) => r.name === picked);
          if (!inv) return;
          t.suggested_party = inv.party;
          t.suggested_party_type = inv.party_type;
          t.suggestions = [{
            invoice_type: inv.doctype,
            invoice_name: inv.name,
            outstanding_amount: inv.outstanding_amount,
            allocated_amount: inv.outstanding_amount,
            selected: 1,
          }];
          t.match_confidence = t.match_confidence === 'None' ? 'Low' : t.match_confidence;
          t.matched_by = (t.matched_by && t.matched_by !== 'None') ? t.matched_by : 'Manual';
          d.hide();
          vn_banking.render_txns(page, state);
          vn_banking.render_stats(page, state);
          frappe.show_alert({
            message: __('Linked {0} → {1}', [inv.name, inv.party]),
            indicator: 'green',
          });
        });
      },
    });
  }

  function _render_actions($td, t, is_credit, state, page) {
    if (t.status === 'Reconciled') {
      $td.html(`<span class="br-reconciled-badge">✓</span>`);
      return;
    }

    // Debit with existing PE → Reconcile button
    if (!is_credit && t.existing_pe) {
      const $btn = $(`<button class="btn btn-xs btn-success">${__('Reconcile')}</button>`);
      $btn.on('click', () => {
        frappe.call({
          method: 'vn_banking.api.reconcile.reconcile_with_existing_pe',
          args: { transaction_name: t.name, payment_entry_name: t.existing_pe.name },
          callback: () => {
            frappe.show_alert({ message: __('Reconciled with {0}', [t.existing_pe.name]), indicator: 'green' });
            vn_banking.load_transactions(state, page);
          },
        });
      });
      $td.append($btn);
      // Also allow creating new PE if existing PE doesn't fit
      $td.append(' ');
      _append_create_pe_buttons($td, t, is_credit, state, page);
      return;
    }

    // Normal flow: Create PE buttons
    _append_create_pe_buttons($td, t, is_credit, state, page);
  }

  function _append_create_pe_buttons($td, t, is_credit, state, page) {
    const $draft = $(`<button class="btn btn-xs btn-primary" title="${__('Create Draft PE')}">${__('Draft')}</button>`);
    const $submit = $(`<button class="btn btn-xs btn-success" title="${__('Create & Submit PE')}">${__('Submit')}</button>`);

    const create_pe = (submit) => {
      // Read party from the row's control
      const $row = $td.closest('tr');
      const $party_cell = $row.find('.br-party-cell');
      const party_type = $party_cell.attr('data-party-type');
      const party = $party_cell.attr('data-party') || t.suggested_party;

      if (!party) {
        frappe.msgprint(__('Select a party first'));
        return;
      }

      // Build invoice list from suggestions
      const invs = (t.suggestions || []).filter((s) => s.selected).map((s) => ({
        invoice_type: s.invoice_type,
        invoice_name: s.invoice_name,
        allocated_amount: s.allocated_amount || s.outstanding_amount,
      }));

      if (!invs.length) {
        // No matched invoices — open dialog to pick manually
        _open_invoice_dialog(t, party_type, party, is_credit, submit, state, page);
        return;
      }

      frappe.call({
        method: 'vn_banking.api.reconcile.create_payment_entry',
        args: {
          transaction_name: t.name,
          party_type, party,
          invoices: JSON.stringify(invs),
          submit,
        },
        callback: (r) => {
          frappe.show_alert({ message: __('PE {0} created', [r.message.payment_entry]), indicator: 'green' });
          vn_banking.load_transactions(state, page);
        },
      });
    };

    $draft.on('click', () => create_pe(false));
    $submit.on('click', () => create_pe(true));
    $td.append($draft).append(' ').append($submit);
  }

  function _open_invoice_dialog(t, party_type, party, is_credit, submit, state, page) {
    const invoice_type = is_credit ? 'Sales Invoice' : 'Purchase Invoice';
    const method = is_credit
      ? 'vn_banking.api.reconcile.get_customer_invoices'
      : 'vn_banking.api.reconcile.get_supplier_invoices';
    const args = is_credit ? { customer: party } : { supplier: party };

    frappe.call({
      method, args,
      callback: (r) => {
        const invoices = r.message || [];
        if (!invoices.length) {
          frappe.msgprint(__('No outstanding invoices found for {0}', [party]));
          return;
        }
        const amount = is_credit ? t.deposit : t.withdrawal;
        const fields = invoices.map((inv) => ({
          fieldtype: 'Check', fieldname: 'sel_' + inv.name,
          label: `${inv.name} — ${frappe.format(inv.outstanding_amount, {fieldtype: 'Currency'})} (${inv.posting_date})`,
          default: Math.abs(inv.outstanding_amount - amount) < 1 ? 1 : 0,
        }));
        fields.unshift({
          fieldtype: 'HTML', fieldname: 'header',
          options: `<p>${__('Select invoices to allocate for')} <b>${frappe.format(amount, {fieldtype: 'Currency'})}</b></p>`,
        });

        const d = new frappe.ui.Dialog({
          title: __('Select Invoices'),
          fields,
          primary_action_label: submit ? __('Create & Submit PE') : __('Create Draft PE'),
          primary_action: (values) => {
            const selected = invoices.filter((inv) => values['sel_' + inv.name]);
            if (!selected.length) { frappe.msgprint(__('Select at least one invoice')); return; }
            const invs = selected.map((inv) => ({
              invoice_type, invoice_name: inv.name,
              allocated_amount: inv.outstanding_amount,
            }));
            frappe.call({
              method: 'vn_banking.api.reconcile.create_payment_entry',
              args: { transaction_name: t.name, party_type, party, invoices: JSON.stringify(invs), submit },
              callback: (res) => {
                d.hide();
                frappe.show_alert({ message: __('PE {0} created', [res.message.payment_entry]), indicator: 'green' });
                vn_banking.load_transactions(state, page);
              },
            });
          },
        });
        d.show();
      },
    });
  }
})();
