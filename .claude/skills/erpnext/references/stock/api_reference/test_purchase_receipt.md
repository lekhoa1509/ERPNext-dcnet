# API Reference: test_purchase_receipt.py

**Language**: Python

**Source**: `doctype/purchase_receipt/test_purchase_receipt.py`

---

## Classes

### TestPurchaseReceipt

**Inherits from**: IntegrationTestCase

#### Methods

##### setUp(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_purchase_receipt_qty(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_purchase_receipt_received_qty(self)

1. Test if received qty is validated against accepted + rejected
2. Test if received qty is auto set on save

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_reverse_purchase_receipt_sle(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_make_purchase_invoice(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_purchase_receipt_no_gl_entry(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_batched_serial_no_purchase(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_duplicate_serial_nos(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_purchase_receipt_gl_entry(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_serial_no_warehouse(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_rejected_warehouse_filter(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_rejected_serial_no(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_purchase_return_partial(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_purchase_return_full(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_purchase_return_for_rejected_qty(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_purchase_receipt_for_rejected_gle_without_accepted_warehouse(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_purchase_return_for_serialized_items(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_purchase_return_for_multi_uom(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_closed_purchase_receipt(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_pr_billing_status(self)

Flow:
1. PO -> PR1 -> PI
2. PO -> PI
3. PO -> PR2.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_serial_no_against_purchase_receipt(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_auto_asset_creation(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_purchase_return_with_submitted_asset(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_purchase_receipt_cost_center(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_purchase_receipt_cost_center_with_balance_sheet_account(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_make_purchase_invoice_from_pr_for_returned_qty(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_make_purchase_invoice_from_pr_with_returned_qty_duplicate_items(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_stock_transfer_from_purchase_receipt(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_stock_transfer_from_purchase_receipt_with_valuation(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_po_to_pi_and_po_to_pr_worflow_full(self)

Test following behaviour:
- Create PO
- Create PI from PO and submit
- Create PR from PO and submit

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_po_to_pi_and_po_to_pr_worflow_partial(self)

Test following behaviour:
- Create PO
- Create partial PI from PO and submit
- Create PR from PO and submit

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_purchase_receipt_with_exchange_rate_difference(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_payment_terms_are_fetched_when_creating_purchase_invoice(self)

**Decorators**: `@IntegrationTestCase.change_settings('Accounts Settings', {'automatically_fetch_payment_terms': 1})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_neg_to_positive(self)

**Decorators**: `@IntegrationTestCase.change_settings('Stock Settings', {'allow_negative_stock': 1})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_backdated_transaction_for_internal_transfer(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_backdated_transaction_for_internal_transfer_in_trasit_warehouse_for_purchase_receipt(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_backdated_transaction_for_internal_transfer_in_trasit_warehouse_for_purchase_invoice(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_batch_expiry_for_purchase_receipt(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_disable_last_purchase_rate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_validate_received_qty_for_internal_pr(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_internal_pr_gl_entries(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_internal_pr_reference(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_purchase_return_valuation_with_rejected_qty(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_return_from_rejected_warehouse(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_purchase_receipt_with_backdated_landed_cost_voucher(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_purchase_receipt_provisional_accounting(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_purchase_return_status_with_debit_note(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_purchase_return_with_zero_rate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### non_internal_transfer_purchase_receipt(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_use_serial_batch_fields_for_serial_nos(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_sle_qty_after_transaction(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_auto_set_batch_based_on_bundle(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_pr_billed_amount_against_return_entry(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_valuation_taxes_lcv_repost_after_billing(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_purchase_receipt_with_use_serial_batch_field_for_rejected_qty(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_internal_transfer_with_serial_batch_items_and_their_valuation(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_internal_transfer_with_serial_batch_items_without_use_serial_batch_fields(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_purchase_receipt_bill_for_rejected_quantity_in_purchase_invoice(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_zero_valuation_rate_for_batched_item(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_purchase_return_from_accepted_and_rejected_warehouse(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_manufacturing_and_expiry_date_for_batch(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_purchase_return_from_rejected_warehouse(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_tax_account_heads_on_lcv_and_item_repost(self)

PO -> PR -> PI
PR -> LCV
Backdated `Repost Item valuation` should not merge tax account heads into stock_rbnb

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### create_lcv(self, receipt_document_type, receipt_document, company, expense_account, charges = 50)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| receipt_document_type | None | - | - |
| receipt_document | None | - | - |
| company | None | - | - |
| expense_account | None | - | - |
| charges | None | 50 | - |


##### test_tax_account_heads_on_item_repost_without_lcv(self)

PO -> PR -> PI
Backdated `Repost Item valuation` should not merge tax account heads into stock_rbnb if Purchase Receipt was created first
This scenario is without LCV

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_do_not_use_batchwise_valuation_rate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_status_mapping(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_internal_transfer_for_batch_items_with_cancel(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_internal_transfer_for_batch_items_with_cancel_use_serial_batch_fields(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_sles_with_same_posting_datetime_and_creation(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_same_stock_and_transaction_uom_conversion_factor(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_purchase_receipt_return_valuation_without_use_serial_batch_field(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_purchase_receipt_return_valuation_with_use_serial_batch_field(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_purchase_return_partial_debit_note(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_do_not_allow_to_inward_same_serial_no_multiple_times(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_seral_no_return_validation(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_batch_no_return_validation(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_pr_status_based_on_invoices_with_update_stock(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_recreate_stock_ledgers(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_validate_recreate_stock_ledgers_for_sn_item(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_internal_pr_qty_change_only_single_batch(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_valuation_rate_for_rejected_materials(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_valuation_rate_for_rejected_materials_with_serial_no(self)

**Decorators**: `@IntegrationTestCase.change_settings('Buying Settings', {'bill_for_rejected_quantity_in_purchase_invoice': 1, 'set_valuation_rate_for_rejected_materials': 1})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_valuation_rate_for_rejected_materials_withoout_accepted_materials(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_no_valuation_rate_for_rejected_materials(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_purchase_expense_account(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_repost_gl_entries(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_lcv_for_repack_entry(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_multiple_transactions_with_same_posting_datetime(self)

**Decorators**: `@IntegrationTestCase.change_settings('Stock Settings', {'allow_negative_stock': 0})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_set_lcv_from_pi_created_against_po(self)

**Decorators**: `@IntegrationTestCase.change_settings('Buying Settings', {'set_landed_cost_based_on_purchase_invoice_rate': 1, 'maintain_same_rate': 0})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_purchase_return_with_and_without_return_against_rejected_qty(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_do_not_use_batchwise_valuation_with_fifo(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_negative_stock_error_for_purchase_return(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_internal_purchase_receipt_incoming_rate_with_lcv(self)

To test inter branch transaction incoming rate calculation with lcv after item reposting

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_negative_stock_error_for_purchase_return_when_stock_exists_in_future_date(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_purchase_return_from_different_warehouse(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### prepare_data_for_internal_transfer()

**Returns**: (none)



### get_sl_entries(voucher_type, voucher_no)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| voucher_type | None | - | - |
| voucher_no | None | - | - |

**Returns**: (none)



### get_gl_entries(voucher_type, voucher_no, skip_cancelled = False, as_dict = True)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| voucher_type | None | - | - |
| voucher_no | None | - | - |
| skip_cancelled | None | False | - |
| as_dict | None | True | - |

**Returns**: (none)



### get_taxes()

**Returns**: (none)



### get_items()

**Returns**: (none)



### make_purchase_receipt()

**Returns**: (none)



### _check_serial_no_values(serial_no, field_values)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| serial_no | None | - | - |
| field_values | None | - | - |

**Returns**: (none)



### get_sabb_qty(sabb)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| sabb | None | - | - |

**Returns**: (none)


