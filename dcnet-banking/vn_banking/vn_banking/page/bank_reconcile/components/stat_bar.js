(function () {
  if (!window.vn_banking) window.vn_banking = {};

  vn_banking.init_stat_bar = function (page, state) { /* no-op */ };

  vn_banking.render_stats = function (page, state) {
    const $stats = $('#br-stats').empty();
    const txns = state.transactions || [];
    if (!txns.length) {
      $stats.hide();
      return;
    }
    $stats.show();
    const count = (c) => txns.filter((t) => (t.match_confidence || 'None') === c).length;
    const reconciled = txns.filter((t) => t.status === 'Reconciled').length;
    const with_pe = txns.filter((t) => t.existing_pe).length;
    let html =
      '<b>' + txns.length + '</b> ' + __('transactions') + ' · ' +
      '<span class="br-confidence-high">' + count('High') + ' ' + __('matched') + '</span> · ' +
      '<span class="br-confidence-medium">' + (count('Medium') + count('Low')) + ' ' + __('suggested') + '</span> · ' +
      '<span class="br-confidence-none">' + count('None') + ' ' + __('unmatched') + '</span> · ' +
      '<span class="br-confidence-high">' + reconciled + ' ' + __('reconciled') + '</span>';
    if (with_pe) {
      html += ' · <b>' + with_pe + '</b> ' + __('existing PE found');
    }
    $stats.html(html);
  };
})();
