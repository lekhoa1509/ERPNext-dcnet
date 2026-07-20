# API Reference: test_payment_entry.py

**Language**: Python

**Source**: `doctype/payment_entry/test_payment_entry.py`

---

## Classes

### TestPaymentEntry

**Inherits from**: IntegrationTestCase

#### Methods

##### tearDown(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_journals_for(self, voucher_type: str, voucher_no: str) → list

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| voucher_type | str | - | - |
| voucher_no | str | - | - |

**Returns**: `list`


##### test_payment_entry_against_order(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_payment_against_sales_order_usd_to_inr(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_payment_entry_for_blocked_supplier_invoice(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_payment_entry_for_blocked_supplier_payments(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_payment_entry_for_blocked_supplier_payments_today_date(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_payment_entry_for_blocked_supplier_payments_past_date(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_payment_entry_against_si_usd_to_usd(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_payment_entry_against_pi(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_payment_against_sales_invoice_to_check_status(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_payment_entry_against_payment_terms(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_payment_entry_against_payment_terms_with_discount_on_pi(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_payment_entry_against_payment_terms_with_discount(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_payment_entry_against_payment_terms_with_discount_amount(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_payment_entry_multicurrency_si_with_base_currency_accounting_early_payment_discount(self)

1. Multi-currency SI with single currency accounting (company currency)
2. PE with early payment discount
3. Test if Paid Amount is calculated in company currency
4. Test if deductions are calculated in company currency

SI is in USD to document agreed amounts that are in USD, but the accounting is in base currency.

**Decorators**: `@IntegrationTestCase.change_settings('Accounts Settings', {'allow_multi_currency_invoices_against_single_party_account': 1, 'book_tax_discount_loss': 1})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_payment_entry_multicurrency_accounting_si_with_early_payment_discount(self)

1. Multi-currency SI with multi-currency accounting
2. PE with early payment discount and also exchange loss
3. Test if Paid Amount is calculated in transaction currency
4. Test if deductions are calculated in base/company currency
5. Test if exchange loss is reflected in difference

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_payment_against_purchase_invoice_to_check_status(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_payment_entry_against_si_usd_to_inr(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_payment_entry_against_si_usd_to_usd_with_deduction_in_base_currency(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_payment_entry_retrieves_last_exchange_rate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_internal_transfer_usd_to_inr(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_payment_against_negative_sales_invoice(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_gl_entries(self, voucher_no, expected_gle)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| voucher_no | None | - | - |
| expected_gle | None | - | - |


##### get_gle(self, voucher_no)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| voucher_no | None | - | - |


##### test_payment_entry_write_off_difference(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_payment_entry_exchange_gain_loss(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_payment_entry_against_sales_invoice_with_cost_centre(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_payment_entry_against_purchase_invoice_with_cost_center(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_payment_entry_account_and_party_balance_with_cost_center(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_gl_of_multi_currency_payment_transaction(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_multi_currency_payment_entry_with_taxes(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_gl_of_multi_currency_payment_with_taxes(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_payment_entry_against_onhold_purchase_invoice(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_payment_entry_for_employee(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_duplicate_payment_entry_allocate_amount(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_duplicate_payment_entry_partial_allocate_amount(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_details_update_on_reference_table(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_overallocation_validation_on_payment_terms(self)

Validate Allocation on Payment Entry based on Payment Schedule. Upon overallocation, validation error must be thrown.

**Decorators**: `@IntegrationTestCase.change_settings('Accounts Settings', {'unlink_payment_on_cancellation_of_invoice': 1, 'delete_linked_ledger_entries': 1, 'allow_multi_currency_invoices_against_single_party_account': 1})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_overallocation_validation_shouldnt_misfire(self)

Overallocation validation shouldn't fire for Template without "Allocate Payment based on Payment Terms" enabled

**Decorators**: `@IntegrationTestCase.change_settings('Accounts Settings', {'unlink_payment_on_cancellation_of_invoice': 1, 'delete_linked_ledger_entries': 1, 'allow_multi_currency_invoices_against_single_party_account': 1})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_allocation_validation_for_sales_order(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_outstanding_invoices_api(self)

Test if `get_outstanding_reference_documents` fetches invoices in the right order.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_receive_payment_from_payable_party_type(self)

Checks GL entries generated while receiving payments from a Payable Party Type.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_payment_against_partial_return_invoice(self)

Checks GL entries generated for partial return invoice payments.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_ledger_entries_for_advance_as_liability(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_advance_as_liability_against_order(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_payment_entry_merges_gl_entries_with_same_account_head(self)

Test that Payment Entry merges GL entries with same account head
when 'Merge Similar Account Heads' setting is enabled.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_payment_entry_does_not_merge_gl_entries_when_setting_disabled(self)

Test that Payment Entry does NOT merge GL entries
when 'Merge Similar Account Heads' is disabled.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### check_pl_entries(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### check_gl_entries(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_reverse_payment_reconciliation(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_advance_reverse_payment_reconciliation(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_opening_flag_for_advance_as_liability(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_delete_linked_exchange_gain_loss_journal(self)

**Decorators**: `@IntegrationTestCase.change_settings('Accounts Settings', {'delete_linked_ledger_entries': 1})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### create_payment_entry()

**Returns**: (none)



### create_payment_terms_template()

**Returns**: (none)



### create_payment_terms_template_with_discount(name = None, discount_type = None, discount = None, template_name = None)

Create a Payment Terms Template with %  or amount discount.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| name | None | None | - |
| discount_type | None | None | - |
| discount | None | None | - |
| template_name | None | None | - |

**Returns**: (none)



### create_payment_term(name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| name | None | - | - |

**Returns**: (none)



### create_customer(name = '_Test Customer 2 USD', currency = 'USD')

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| name | None | '_Test Customer 2 USD' | - |
| currency | None | 'USD' | - |

**Returns**: (none)


