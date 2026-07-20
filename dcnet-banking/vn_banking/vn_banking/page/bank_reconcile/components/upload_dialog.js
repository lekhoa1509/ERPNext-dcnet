(function () {
  if (!window.vn_banking) window.vn_banking = {};

  vn_banking.open_upload_dialog = function (state, page) {
    const d = new frappe.ui.Dialog({
      title: __('Upload Bank Statement'),
      fields: [
        { fieldname: 'help_section', fieldtype: 'HTML',
          options: `<div class="text-muted small" style="margin-bottom: 12px; padding: 8px 12px; background: var(--bg-light-gray); border-radius: var(--border-radius);">
            <p style="margin-bottom: 4px;"><strong>${__('Supported banks')}:</strong> BIDV, MB Bank, Sacombank, PG Bank</p>
            <p style="margin-bottom: 4px;">${__('Upload the Excel file (.xls/.xlsx) exported from your bank\'s website. The bank and format are auto-detected.')}</p>
            <p style="margin-bottom: 0;">${__('For other banks')}: <a href="/app/bank-statement-format/new" target="_blank">${__('create a Format config')}</a> ${__('to map your file\'s columns.')}</p>
          </div>` },
        { fieldname: 'file', label: __('File'), fieldtype: 'Attach', reqd: 1 },
        { fieldname: 'bank_account', label: __('Bank Account'), fieldtype: 'Link',
          options: 'Bank Account',
          description: __('Auto-detected from file. Only change if detection is wrong.'),
          get_query: () => ({ filters: { is_company_account: 1 } }) },
        { fieldname: 'col_break_dates', fieldtype: 'Column Break' },
        { fieldname: 'from_date', label: __('From Date'), fieldtype: 'Date' },
        { fieldname: 'to_date', label: __('To Date'), fieldtype: 'Date' },
        { fieldname: 'format', label: __('Format'), fieldtype: 'Link',
          options: 'Bank Statement Format', read_only: 1,
          description: __('Auto-detected from file content.') },
      ],
      primary_action_label: __('Upload and Match'),
      primary_action(values) {
        const bank_account = values.bank_account || state.bank_account;
        if (!bank_account) {
          frappe.msgprint(__('Could not detect Bank Account. Please select one manually.'));
          return;
        }
        d.hide();
        // Update page-level state
        state.bank_account = bank_account;
        $('#br-bank-account-select').val(bank_account);

        frappe.show_progress(__('Parsing'), 0, 100, __('Starting...'));
        frappe.call({
          method: 'vn_banking.api.reconcile.trigger_import',
          args: {
            bank_account: bank_account,
            source_type: 'excel_upload',
            file_url: values.file,
            from_date: values.from_date,
            to_date: values.to_date,
            format_name: values.format,
          },
          callback: (r) => {
            state.import_name = r.message.import_name;
            if (!r.message.async) {
              frappe.hide_progress();
              const total = r.message.total_rows || 0;
              const dupes = r.message.duplicate_rows || 0;
              const newRows = total - dupes;
              if (total > 0 && newRows === 0) {
                frappe.show_alert({
                  message: __('All {0} rows already exist (duplicates). Showing previous import data.', [total]),
                  indicator: 'orange',
                }, 7);
                // Load transactions from the ORIGINAL import that has these txns
                _load_original_import(state, page, values.bank_account || bank_account);
              } else {
                if (total > 0) {
                  frappe.show_alert({
                    message: __('Imported {0} new rows ({1} duplicates skipped)', [newRows, dupes]),
                    indicator: 'green',
                  }, 5);
                }
                vn_banking.load_transactions(state, page);
              }
            }
          },
          error: (err) => {
            frappe.hide_progress();
            frappe.msgprint({ title: __('Upload failed'), message: err.message || err, indicator: 'red' });
          },
        });
      },
    });

    // Auto-detect format and bank account when file is attached
    d.fields_dict.file.$input && d.fields_dict.file.$input.on('change', function () {
      setTimeout(() => _try_auto_detect(d, state), 500);
    });
    // Also listen for the attach complete event
    d.fields_dict.file.df.change = function () {
      setTimeout(() => _try_auto_detect(d, state), 300);
    };

    d.show();
  };

  function _load_original_import(state, page, bank_account) {
    // When all rows are dupes, find the latest import that HAS transactions for this bank account
    frappe.db.get_list('Bank Statement Import', {
      filters: { bank_account: bank_account, status: ['in', ['Parsed', 'Reviewed']] },
      fields: ['name', 'total_rows', 'duplicate_rows'],
      order_by: 'modified desc',
      limit: 10,
    }).then((imports) => {
      // Pick the first import where total_rows > duplicate_rows (has real txns)
      const good = imports.find((i) => (i.total_rows || 0) > (i.duplicate_rows || 0));
      if (good) {
        state.import_name = good.name;
        vn_banking.load_transactions(state, page);
      } else if (imports.length) {
        // Fallback: just load the most recent one
        state.import_name = imports[0].name;
        vn_banking.load_transactions(state, page);
      }
    });
  }

  function _try_auto_detect(dialog, state) {
    const file_url = dialog.get_value('file');
    if (!file_url) return;
    frappe.call({
      method: 'vn_banking.api.reconcile.detect_format_and_bank',
      args: { file_url: file_url },
      async: true,
      callback: (r) => {
        if (!r.message) return;
        const { format_name, bank_account, bank_name } = r.message;
        if (format_name) {
          dialog.set_value('format', format_name);
        }
        if (bank_account) {
          dialog.set_value('bank_account', bank_account);
        }
        if (bank_name && !bank_account) {
          dialog.fields_dict.bank_account.set_description(
            __('Bank detected: {0}, but no matching Bank Account found. Please select or create one.', [bank_name])
          );
        }
      },
    });
  }

  vn_banking.update_progress = function (page, data) {
    const pct = Math.min(99, Math.round((data.processed / (data.total || data.processed + 1)) * 100));
    frappe.show_progress(__('Parsing'), pct, 100,
      __('Processed {0} rows ({1} duplicates)', [data.processed, data.duplicates]));
  };
})();
