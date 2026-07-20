# API Reference: test_payment_reconciliation.py

**Language**: Python

**Source**: `doctype/payment_reconciliation/test_payment_reconciliation.py`

---

## Classes

### TestPaymentReconciliation

**Inherits from**: IntegrationTestCase

#### Methods

##### setUp(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### tearDown(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### create_company(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### create_item(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### create_customer(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### create_account(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### create_sales_invoice(self, qty = 1, rate = 100, posting_date = None, do_not_save = False, do_not_submit = False)

Helper function to populate default values in sales invoice

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| qty | None | 1 | - |
| rate | None | 100 | - |
| posting_date | None | None | - |
| do_not_save | None | False | - |
| do_not_submit | None | False | - |


##### create_payment_entry(self, amount = 100, posting_date = None, customer = None)

Helper function to populate default values in payment entry

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| amount | None | 100 | - |
| posting_date | None | None | - |
| customer | None | None | - |


##### create_purchase_invoice(self, qty = 1, rate = 100, posting_date = None, do_not_save = False, do_not_submit = False)

Helper function to populate default values in sales invoice

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| qty | None | 1 | - |
| rate | None | 100 | - |
| posting_date | None | None | - |
| do_not_save | None | False | - |
| do_not_submit | None | False | - |


##### create_purchase_order(self, qty = 1, rate = 100, posting_date = None, do_not_save = False, do_not_submit = False)

Helper function to populate default values in sales invoice

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| qty | None | 1 | - |
| rate | None | 100 | - |
| posting_date | None | None | - |
| do_not_save | None | False | - |
| do_not_submit | None | False | - |


##### clear_old_entries(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### create_payment_reconciliation(self, party_is_customer = True)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| party_is_customer | None | True | - |


##### create_journal_entry(self, acc1 = None, acc2 = None, amount = 0, posting_date = None, cost_center = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| acc1 | None | None | - |
| acc2 | None | None | - |
| amount | None | 0 | - |
| posting_date | None | None | - |
| cost_center | None | None | - |


##### create_cost_center(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_filter_min_max(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_filter_posting_date(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_filter_posting_date_case2(self)

Posting date should not affect outstanding amount calculation

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_filter_invoice_limit(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_payment_against_invoice(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_payment_against_journal(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_payment_against_foreign_currency_journal(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_journal_against_invoice(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_negative_debit_or_credit_journal_against_invoice(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_journal_against_journal(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_cr_note_against_invoice(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_invoice_status_after_cr_note_cancellation(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_cr_note_partial_against_invoice(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_pr_output_foreign_currency_and_amount(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_difference_amount_via_journal_entry(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_difference_amount_via_negative_debit_or_credit_journal_entry(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_difference_amount_via_payment_entry(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_differing_cost_center_on_invoice_and_payment(self)

Cost Center filter should not affect outstanding amount calculation

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_cost_center_filter_on_vouchers(self)

Test Cost Center filter is applied on Invoices, Payment Entries and Journals

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_no_difference_amount_for_base_currency_accounts(self)

**Decorators**: `@IntegrationTestCase.change_settings('Accounts Settings', {'allow_multi_currency_invoices_against_single_party_account': 1})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_reconciliation_purchase_invoice_against_return(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_reconciliation_from_purchase_order_to_multiple_invoices(self)

Reconciling advance payment from PO/SO to multiple invoices should not cause overallocation

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_rounding_of_unallocated_amount(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_reverse_payment_against_payment_for_supplier(self)

Reconcile a payment against a reverse payment, for a supplier.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_advance_reverse_payment_against_payment_for_supplier(self)

Reconcile an Advance payment against reverse payment, for a supplier.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_advance_payment_reconciliation_date(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_advance_payment_reconciliation_date_for_older_date(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_advance_payment_reconciliation_against_journal_for_customer(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_advance_payment_reconciliation_against_journal_for_supplier(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_cr_note_payment_limit_filter(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_reconciliation_on_closed_period_payment(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_advance_reconciliation_effect_on_same_date(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_partial_advance_payment_with_closed_fiscal_year(self)

Test Advance Payment partial reconciliation before period closing and partial after period closing

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_foreign_currency_reverse_payment_entry_against_payment_entry_for_customer(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_foreign_currency_reverse_payment_entry_against_payment_entry_for_supplier(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_foreign_currency_reverse_journal_entry_against_journal_entry_for_customer(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_foreign_currency_reverse_journal_entry_against_journal_entry_for_supplier(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### make_customer(customer_name, currency = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| customer_name | None | - | - |
| currency | None | None | - |

**Returns**: (none)



### make_supplier(supplier_name, currency = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| supplier_name | None | - | - |
| currency | None | None | - |

**Returns**: (none)



### create_fiscal_year(company, year_start_date, year_end_date)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| company | None | - | - |
| year_start_date | None | - | - |
| year_end_date | None | - | - |

**Returns**: (none)



### make_period_closing_voucher(company, cost_center, posting_date = None, submit = True)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| company | None | - | - |
| cost_center | None | - | - |
| posting_date | None | None | - |
| submit | None | True | - |

**Returns**: (none)


