# API Reference: test_sales_invoice.py

**Language**: Python

**Source**: `doctype/sales_invoice/test_sales_invoice.py`

---

## Classes

### TestSalesInvoice

**Inherits from**: ERPNextTestSuite

#### Methods

##### setUp(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_invalid_rate_without_override(self)

**Decorators**: `@change_settings('Accounts Settings', {'maintain_same_internal_transaction_rate': 1, 'maintain_same_rate_action': 'Stop'})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### tearDown(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### make(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### setUpClass(cls)

**Decorators**: `@classmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| cls | None | - | - |


##### tearDownClass(self)

**Decorators**: `@classmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_sales_invoice_qty(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_timestamp_change(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_sales_invoice_change_naming_series(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_add_terms_after_save(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_sales_invoice_calculation_base_currency(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_payment_entry_unlink_against_invoice(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_payment_entry_unlink_against_standalone_credit_note(self)

**Decorators**: `@IntegrationTestCase.change_settings('Accounts Settings', {'unlink_payment_on_cancellation_of_invoice': 1})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_sales_invoice_calculation_export_currency(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_sales_invoice_with_discount_and_inclusive_tax(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_sales_invoice_discount_amount(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_discount_amount_gl_entry(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_tax_calculation_with_multiple_items(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_tax_calculation_with_item_tax_template(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_tax_calculation_with_multiple_items_and_discount(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_inclusive_rate_validations(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_sales_invoice_calculation_base_currency_with_tax_inclusive_price(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_sales_invoice_calculation_export_currency_with_tax_inclusive_price(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_outstanding(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_rounded_total_with_cash_discount(self)

**Decorators**: `@IntegrationTestCase.change_settings('Accounts Settings', {'add_taxes_from_item_tax_template': 0, 'add_taxes_from_taxes_and_charges_template': 0})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_payment(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_outstanding_on_cost_center_allocation(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_sales_invoice_gl_entry_without_perpetual_inventory(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_pos_gl_entry_with_perpetual_inventory(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_pos_returns_with_repayment(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_pos_change_amount(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_auto_write_off_amount(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_ledger_entries_of_return_pos_invoice(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_pos_with_no_gl_entry_for_change_amount(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_pos_gl_entry(self, si, pos, cash_amount, validate_without_change_gle = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| si | None | - | - |
| pos | None | - | - |
| cash_amount | None | - | - |
| validate_without_change_gle | None | False | - |


##### test_bin_details_of_packed_item(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_pos_si_without_payment(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_sales_invoice_gl_entry_with_perpetual_inventory_no_item_code(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_sales_invoice_gl_entry_with_perpetual_inventory_non_stock_item(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _insert_purchase_receipt(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _insert_delivery_note(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_sales_invoice_with_advance(self)

**Decorators**: `@IntegrationTestCase.change_settings('Accounts Settings', {'unlink_payment_on_cancellation_of_invoice': 1})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_serialized(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_serialized_cancel(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_serial_numbers_against_delivery_note(self)

check if the sales invoice item serial numbers and the delivery note items
serial numbers are same

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_return_sales_invoice(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_zero_qty_return_invoice_with_stock_effect(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_return_invoice_with_account_mismatch(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_gle_made_when_asset_is_returned(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_incoming_rate_for_stand_alone_credit_note(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_discount_on_net_total(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_multi_currency_gle(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_gle_in_transaction_currency(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_invalid_currency(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_create_so_with_margin(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_outstanding_amount_after_advance_jv_cancellation(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_outstanding_amount_after_advance_payment_entry_cancellation(self)

Test impact of advance PE submission/cancellation on SI and SO.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_multiple_uom_in_selling(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_item_wise_tax_breakup(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### create_si_to_test_tax_breakup(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_company_monthly_sales(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_rounding_adjustment(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_rounding_adjustment_2(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_rounding_adjustment_3(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_sales_invoice_with_shipping_rule(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_create_invoice_without_terms(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_duplicate_due_date_in_terms(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_credit_note(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_sales_invoice_with_cost_center(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_sales_invoice_with_project_link(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_sales_invoice_without_cost_center(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_deferred_revenue(self)

**Decorators**: `@IntegrationTestCase.change_settings('Accounts Settings', {'book_deferred_entries_based_on': 'Days', 'book_deferred_entries_via_journal_entry': 0})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_deferred_revenue_missing_account(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_fixed_deferred_revenue(self)

**Decorators**: `@IntegrationTestCase.change_settings('Accounts Settings', {'book_deferred_entries_based_on': 'Months', 'book_deferred_entries_via_journal_entry': 0})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_validate_inter_company_transaction_address_links(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_inter_company_transaction(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_inter_company_transaction_without_default_warehouse(self)

Check mapping (expense account) of inter company SI to PI in absence of default warehouse.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_sle_for_target_warehouse(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_internal_transfer_gl_entry(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_internal_transfer_gl_precision_issues(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_item_tax_net_range(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_item_tax_template_change_with_grand_total_discount(self)

Test that when item tax template changes due to discount on Grand Total,
the tax calculations are consistent.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_sales_invoice_with_discount_accounting_enabled(self)

**Decorators**: `@IntegrationTestCase.change_settings('Selling Settings', {'enable_discount_accounting': 1})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_additional_discount_for_sales_invoice_with_discount_accounting_enabled(self)

**Decorators**: `@IntegrationTestCase.change_settings('Selling Settings', {'enable_discount_accounting': 1})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_asset_depreciation_on_sale_with_pro_rata(self)

Tests if an Asset set to depreciate yearly on June 30, that gets sold on Sept 30, creates an additional depreciation entry on its date of sale.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_asset_depreciation_on_sale_without_pro_rata(self)

Tests if an Asset set to depreciate yearly on Dec 31, that gets sold on Dec 31 after two years, created an additional depreciation entry on its date of sale.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_sales_invoice_against_supplier(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_sales_invoice_against_supplier_usd_with_dimensions(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_sales_invoice_cancel_with_common_party_advance_jv(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_payment_statuses(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_update_invoice_status(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_sales_commission(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_sales_invoice_submission_post_account_freezing_date(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_over_billing_case_against_delivery_note(self)

Test a case where duplicating the item with qty = 1 in the invoice
allows overbilling even if it is disabled

**Decorators**: `@IntegrationTestCase.change_settings('Accounts Settings', {'over_billing_allowance': 0})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_multi_currency_deferred_revenue_via_journal_entry(self)

**Decorators**: `@IntegrationTestCase.change_settings('Accounts Settings', {'book_deferred_entries_via_journal_entry': 1, 'submit_journal_entries': 1})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_standalone_serial_no_return(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_sales_invoice_with_disabled_account(self)

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


##### test_batch_expiry_for_sales_invoice_return(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_sales_invoice_with_payable_tax_account(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_advance_entries_as_liability(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_sales_invoice_without_customer_group_and_territory(self)

**Decorators**: `@IntegrationTestCase.change_settings('Selling Settings', {'customer_group': None, 'territory': None})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_sales_return_negative_rate(self)

**Decorators**: `@IntegrationTestCase.change_settings('Selling Settings', {'allow_negative_rates_for_items': 0})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_partial_allocation_on_advance_as_liability(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_loyalty_points_redemption_with_shopping_cart(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_pulling_advance_based_on_debit_to(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_taxes_merging_from_delivery_note(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_pos_returns_without_update_outstanding_for_self(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_validation_on_opening_invoice_with_rounding(self)

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


##### test_opening_invoice_with_rounding_adjustment(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _create_opening_invoice_with_inclusive_tax(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_rounding_validation_for_opening_with_inclusive_tax(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_ledger_entries_on_opening_invoice_with_rounding_loss_by_inclusive_tax(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_common_party_with_foreign_currency_jv(self)

**Decorators**: `@IntegrationTestCase.change_settings('Accounts Settings', {'enable_common_party_accounting': True})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_common_party_with_different_currency_in_debtor_and_creditor(self)

**Decorators**: `@IntegrationTestCase.change_settings('Accounts Settings', {'enable_common_party_accounting': True})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_invoice_remarks(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_gl_voucher_subtype(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_total_billed_amount(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_total_billed_amount_with_different_projects(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_pos_returns_with_party_account_currency(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_create_return_invoice_for_self_update(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_prevents_fully_returned_invoice_with_zero_quantity(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_pos_sales_invoice_creation_during_pos_invoice_mode(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_stand_alone_credit_note_valuation(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_stand_alone_credit_note_zero_valuation(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_system_generated_exchange_gain_or_loss_je_after_repost(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_non_batchwise_valuation_for_moving_average(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_zero_valuation_for_standalone_credit_note_with_expired_batch(self)

**Decorators**: `@change_settings('Selling Settings', {'set_zero_rate_for_expired_batch': True})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### make_item_for_si(item_code, properties = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item_code | None | - | - |
| properties | None | None | - |

**Returns**: (none)



### set_advance_flag(company, flag, default_account)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| company | None | - | - |
| flag | None | - | - |
| default_account | None | - | - |

**Returns**: (none)



### check_gl_entries(doc, voucher_no, expected_gle, posting_date, voucher_type = 'Sales Invoice')

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |
| voucher_no | None | - | - |
| expected_gle | None | - | - |
| posting_date | None | - | - |
| voucher_type | None | 'Sales Invoice' | - |

**Returns**: (none)



### create_sales_invoice()

**Returns**: (none)



### create_sales_invoice_against_cost_center()

**Returns**: (none)



### get_outstanding_amount(against_voucher_type, against_voucher, account, party, party_type)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| against_voucher_type | None | - | - |
| against_voucher | None | - | - |
| account | None | - | - |
| party | None | - | - |
| party_type | None | - | - |

**Returns**: (none)



### get_taxes_and_charges()

**Returns**: (none)



### create_internal_parties()

**Returns**: (none)



### create_internal_supplier(supplier_name, represents_company, allowed_to_interact_with)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| supplier_name | None | - | - |
| represents_company | None | - | - |
| allowed_to_interact_with | None | - | - |

**Returns**: (none)



### setup_accounts()

**Returns**: (none)



### add_taxes(doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |

**Returns**: (none)



### _validate_address_link(address, link_doctype, link_name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| address | None | - | - |
| link_doctype | None | - | - |
| link_name | None | - | - |

**Returns**: (none)


