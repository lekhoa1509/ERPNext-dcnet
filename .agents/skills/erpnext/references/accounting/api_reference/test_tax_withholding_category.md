# API Reference: test_tax_withholding_category.py

**Language**: Python

**Source**: `doctype/tax_withholding_category/test_tax_withholding_category.py`

---

## Classes

### TestTaxWithholdingCategory

**Inherits from**: IntegrationTestCase

#### Methods

##### setUpClass(cls)

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


##### validate_tax_withholding_entries(self, doctype, docname, expected_entries)

Validate tax withholding entries for a document

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doctype | None | - | - |
| docname | None | - | - |
| expected_entries | None | - | - |


##### get_tax_withholding_entry(self)

Create a tax withholding entry with consistent field ordering

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### setup_party_with_category(self, party_type, party_name, category_name)

Setup party with tax withholding category

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| party_type | None | - | - |
| party_name | None | - | - |
| category_name | None | - | - |


##### validate_tax_deduction(self, invoice, expected_amount)

Validate invoice tax deduction and grand total

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| invoice | None | - | - |
| expected_amount | None | - | - |


##### cleanup_invoices(self, invoice_list)

Clean up invoices in reverse order to avoid dependency issues

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| invoice_list | None | - | - |


##### test_cumulative_threshold_tds(self)

Tax withholding entries for cumulative threshold TDS with Tax on excess without single threshold

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_cumulative_threshold_tds_with_account_change(self)

Cumulative threshold TDS without tax_on_excess, with account change in the middle of the year

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_single_threshold_tds(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_tax_withholding_category_checks(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_cumulative_threshold_with_party_ledger_amount_on_net_total(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_cumulative_threshold_with_tax_on_excess_amount(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_cumulative_threshold_tcs_on_gross_amount(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_tcs_on_allocated_advance_payments(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_tds_multiple_payments_adjust_only_linked(self)

Test that when multiple advance payment entries exist for the same supplier,
only the payment entry that is linked/allocated to the invoice is adjusted.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_tds_multiple_payments_with_unused_threshold(self)

Test multiple payment entries with unused threshold (tax_on_excess_amount enabled).
Only the linked payment entry should be adjusted, and threshold exemption should apply.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_tds_withholding_group_different_rates(self)

Test that Tax Withholding Group applies different rates for different groups
within the same Tax Withholding Category.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_tds_calculation_on_net_total(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_tds_calculation_on_net_total_partial_tds(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_tds_deduction_for_po_via_payment_entry(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_multi_category_single_supplier(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_tds_deductions_with_payment_entries(self)

Test tax withholding entries across different voucher types and statuses:
- Purchase Invoice: Regular invoice (Under Withheld - below threshold)
- Return Invoice: Negative amount (Under Withheld - return, no TDS)
- Payment Entry: Over Withheld (always)
- Payment Entry2: Over Withheld (always)
- Final Invoice: Settlement invoice that settles all previous entries (Settled status)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_tds_deduction_with_partial_payment_adjustment(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_lower_deduction_certificate_application(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_ldc_at_0_rate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_payment_entry_with_ldc_and_invoice_adjustment(self)

Test: Payment Entry with LDC, then Invoice, with correct tax adjustment.
- Payment Entry (advance) is made and tax is deducted at LDC rate
- Purchase Invoice is created for a higher amount
- For the portion of invoice covered by advance, tax is adjusted at LDC rate
- For the remaining invoice amount, tax is deducted at normal rate

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_payment_entry_with_ldc_and_partial_invoice_adjustment(self)

Test: Payment Entry with LDC, then Invoice, with correct tax adjustment.
- Payment Entry (advance) is made and tax is deducted at LDC rate
- Purchase Invoice is created for a higher amount
- For the portion of invoice covered by advance, tax is adjusted at LDC rate
- For the remaining invoice amount, tax is deducted at normal rate

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_previous_fy_and_tax_category(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_tds_across_fiscal_year(self)

Advance TDS on previous fiscal year should be properly allocated on Invoices in upcoming fiscal year
--||-----FY 2023-----||-----FY 2024-----||--
--||-----Advance-----||---Inv1---Inv2---||--

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_tds_payment_entry_cancellation(self)

Test payment entry cancellation clears withholding references from matched entries

**Decorators**: `@IntegrationTestCase.change_settings('Accounts Settings', {'delete_linked_ledger_entries': 1})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_tds_purchase_invoice_cancellation(self)

Test that after cancellation, new documents get automatically adjusted against remaining entries

**Decorators**: `@IntegrationTestCase.change_settings('Accounts Settings', {'delete_linked_ledger_entries': 1})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_tds_deduction_in_purchase_return(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_tds_purchase_invoice_cancellation_and_adjustment(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_tds_for_return_invoices(self)

Test TDS handling for return invoices with 3-entry cancellation approach

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_manual_tax_withholding_validation(self)

Test validation when user manually overrides tax withholding entries with incorrect amounts

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_manual_tax_adjustment_with_partial_adjustment_and_rate_change(self)

Test manual tax adjustment where tax rate is changed during adjustment between payment and invoice

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_manual_tax_adjustment_with_rate_change(self)

Test manual tax adjustment where tax rate is changed during adjustment between payment and invoice

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_manual_tax_adjustment_with_zero_rate(self)

Test manual tax adjustment where tax rate is changed to zero during adjustment

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_tds_on_journal_entry_for_supplier(self)

Test TDS deduction for Supplier in Debit Note

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_tcs_on_journal_entry_for_customer(self)

Test TCS collection for Customer in Credit Note

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_tds_with_multi_currency_invoice(self)

Test TDS calculation with multi-currency purchase invoice and payment

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_journal_entry_with_adjustment_in_invoice(self)

Test Journal Entry with amount below threshold creates Under Withheld entry
and gets settled when a new Purchase Invoice crosses the threshold

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_journal_entry_negative_amount_debit_note(self)

Test Journal Entry with negative amount (reversal of Debit Note)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_delete_draft_pi_with_tax_withholding_entries(self)

Test that draft Purchase Invoice with Tax Withholding Entries can be deleted.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_tds_rounding_with_decimal_amounts(self)

Test TDS rounding when round_off_tax_amount is enabled in category

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_tax_withholding_entry_status_determination(self)

Test that Tax Withholding Entry status is correctly determined

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_invalid_withholding_amount_validation(self)

Test that mismatched withholding amounts throw validation error on save

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### create_purchase_invoice()

**Returns**: (none)



### create_purchase_order()

**Returns**: (none)



### create_sales_invoice()

**Returns**: (none)



### create_payment_entry()

**Returns**: (none)



### make_journal_entry_with_tax_withholding(party_type, party, voucher_type, amount, cost_center = None, posting_date = None, save = True, submit = False)

Helper function to create Journal Entry for tax withholding

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| party_type | None | - | - |
| party | None | - | - |
| voucher_type | None | - | - |
| amount | None | - | - |
| cost_center | None | None | - |
| posting_date | None | None | - |
| save | None | True | - |
| submit | None | False | - |

**Returns**: (none)



### create_records()

**Returns**: (none)



### create_tax_withholding_category_records()

**Returns**: (none)



### create_tax_withholding_category(category_name, rate, from_date, to_date, account, single_threshold = 0, cumulative_threshold = 0, round_off_tax_amount = 0, tax_on_excess_amount = 0, disable_transaction_threshold = 0, tax_deduction_basis = 'Net Total')

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| category_name | None | - | - |
| rate | None | - | - |
| from_date | None | - | - |
| to_date | None | - | - |
| account | None | - | - |
| single_threshold | None | 0 | - |
| cumulative_threshold | None | 0 | - |
| round_off_tax_amount | None | 0 | - |
| tax_on_excess_amount | None | 0 | - |
| disable_transaction_threshold | None | 0 | - |
| tax_deduction_basis | None | 'Net Total' | - |

**Returns**: (none)



### create_lower_deduction_certificate(supplier, tax_withholding_category, tax_rate, certificate_no, limit, valid_from = None, valid_upto = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| supplier | None | - | - |
| tax_withholding_category | None | - | - |
| tax_rate | None | - | - |
| certificate_no | None | - | - |
| limit | None | - | - |
| valid_from | None | None | - |
| valid_upto | None | None | - |

**Returns**: (none)



### make_pan_no_field()

**Returns**: (none)



### sort_key(entry)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| entry | None | - | - |

**Returns**: (none)



### normalize_entry(entry)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| entry | None | - | - |

**Returns**: (none)



### add_company_to_fy(fy, company)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| fy | None | - | - |
| company | None | - | - |

**Returns**: (none)


