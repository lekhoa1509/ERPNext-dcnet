# API Reference: test_purchase_invoice.py

**Language**: Python

**Source**: `doctype/purchase_invoice/test_purchase_invoice.py`

---

## Classes

### TestPurchaseInvoice

**Inherits from**: IntegrationTestCase, StockTestMixin

#### Methods

##### setUpClass(cls)

**Decorators**: `@classmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| cls | None | - | - |


##### tearDownClass(cls)

**Decorators**: `@classmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| cls | None | - | - |


##### tearDown(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_purchase_invoice_qty(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_purchase_invoice_received_qty(self)

1. Test if received qty is validated against accepted + rejected
2. Test if received qty is auto set on save

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_update_received_qty_in_material_request(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_gl_entries_without_perpetual_inventory(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_gl_entries_with_perpetual_inventory(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_terms_added_after_save(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_payment_entry_unlink_against_purchase_invoice(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_purchase_invoice_for_blocked_supplier(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_purchase_invoice_for_blocked_supplier_invoice(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_purchase_invoice_for_blocked_supplier_payment(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_purchase_invoice_for_blocked_supplier_payment_today_date(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_purchase_invoice_for_blocked_supplier_payment_past_date(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_purchase_invoice_blocked_invoice_must_be_in_future(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_purchase_invoice_temporary_blocked(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_purchase_invoice_explicit_block(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_gl_entries_with_perpetual_inventory_against_pr(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### check_gle_for_pi(self, pi)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| pi | None | - | - |


##### test_purchase_invoice_with_exchange_rate_difference(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_purchase_invoice_with_exchange_rate_difference_for_non_stock_item(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_purchase_invoice_change_naming_series(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_gl_entries_for_non_stock_items_with_perpetual_inventory(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_purchase_invoice_calculation(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_purchase_invoice_with_advance(self)

**Decorators**: `@IntegrationTestCase.change_settings('Accounts Settings', {'unlink_payment_on_cancellation_of_invoice': 1})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_invoice_with_advance_and_multi_payment_terms(self)

**Decorators**: `@IntegrationTestCase.change_settings('Accounts Settings', {'unlink_payment_on_cancellation_of_invoice': 1})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_total_purchase_cost_for_project(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_return_purchase_invoice_with_perpetual_inventory(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_standalone_return_using_pi(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_return_with_lcv(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_multi_currency_gle(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_purchase_invoice_update_stock_gl_entry_with_perpetual_inventory(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_purchase_invoice_for_is_paid_and_update_stock_gl_entry_with_perpetual_inventory(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_auto_batch(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_update_stock_and_purchase_return(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_rejected_serial_no(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_outstanding_amount_after_advance_jv_cancelation(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_outstanding_amount_after_advance_payment_entry_cancelation(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_purchase_invoice_with_shipping_rule(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_make_pi_without_terms(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_duplicate_due_date_in_terms(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_debit_note(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_purchase_invoice_with_cost_center(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_purchase_invoice_without_cost_center(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_purchase_invoice_with_project_link(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_deferred_expense_via_journal_entry(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_gain_loss_with_advance_entry(self)

**Decorators**: `@IntegrationTestCase.change_settings('Accounts Settings', {'unlink_payment_on_cancellation_of_invoice': 1})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_purchase_invoice_advance_taxes(self)

**Decorators**: `@IntegrationTestCase.change_settings('Accounts Settings', {'unlink_payment_on_cancellation_of_invoice': 1})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_purchase_gl_with_tax_withholding_tax(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_provisional_accounting_entry(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_provisional_accounting_entry_for_over_billing(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_provisional_accounting_entry_for_partial_billing(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_provisional_accounting_entry_multi_currency(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_adjust_incoming_rate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_adjust_incoming_rate_for_rejected_item(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_item_less_defaults(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_batch_expiry_for_purchase_invoice(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_advance_entries_as_asset(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_gl_entries_for_standalone_debit_note(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_payment_allocation_for_payment_terms(self)

**Decorators**: `@IntegrationTestCase.change_settings('Accounts Settings', {'automatically_fetch_payment_terms': 1})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_offsetting_entries_for_accounting_dimensions(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_repost_accounting_entries(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_create_purchase_invoice_without_mandatory(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_purchase_invoice_without_supplier_group(self)

**Decorators**: `@IntegrationTestCase.change_settings('Buying Settings', {'supplier_group': None})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_default_cost_center_for_purchase(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_debit_note_with_account_mismatch(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_debit_note_without_item(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_purchase_invoice_with_use_serial_batch_field_for_rejected_qty(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_make_pr_and_pi_from_po(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_adjust_incoming_rate_from_pi_with_multi_currency(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_adjust_incoming_rate_from_pi_with_multi_currency_and_partial_billing(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_pr_status_rate_adjusted_from_pi(self)

**Decorators**: `@IntegrationTestCase.change_settings('Buying Settings', {'maintain_same_rate': 0, 'set_landed_cost_based_on_purchase_invoice_rate': 1})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_opening_invoice_rounding_adjustment_validation(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _create_opening_roundoff_account(self, company_name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| company_name | None | - | - |


##### test_ledger_entries_of_opening_invoice_with_rounding_adjustment(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_last_purchase_rate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_invoice_against_returned_pr(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_trx_currency_debit_credit_for_high_precision(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_prevents_fully_returned_invoice_with_zero_quantity(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_apply_discount_on_grand_total(self)

To test if after applying discount on grand total,
the grand total is calculated correctly without any rounding errors

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_apply_discount_on_grand_total_with_previous_row_total_tax(self)

To test if after applying discount on grand total,
where the tax is calculated on previous row total, the grand total is calculated correctly

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_pr_pi_over_billing(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_discount_percentage_not_set_when_amount_is_manually_set(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_returned_item_purchase_receipt(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### set_advance_flag(company, flag, default_account)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| company | None | - | - |
| flag | None | - | - |
| default_account | None | - | - |

**Returns**: (none)



### check_gl_entries(doc, voucher_no, expected_gle, posting_date, voucher_type = 'Purchase Invoice', additional_columns = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |
| voucher_no | None | - | - |
| expected_gle | None | - | - |
| posting_date | None | - | - |
| voucher_type | None | 'Purchase Invoice' | - |
| additional_columns | None | None | - |

**Returns**: (none)



### create_tax_witholding_category(category_name, company, account)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| category_name | None | - | - |
| company | None | - | - |
| account | None | - | - |

**Returns**: (none)



### unlink_payment_on_cancel_of_invoice(enable = 1)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| enable | None | 1 | - |

**Returns**: (none)



### make_purchase_invoice()

**Returns**: (none)



### make_purchase_invoice_against_cost_center()

**Returns**: (none)



### setup_provisional_accounting()

**Returns**: (none)



### toggle_provisional_accounting_setting()

**Returns**: (none)


