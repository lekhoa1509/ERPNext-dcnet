# API Reference: test_purchase_order.py

**Language**: Python

**Source**: `doctype/purchase_order/test_purchase_order.py`

---

## Classes

### TestPurchaseOrder

**Inherits from**: IntegrationTestCase

#### Methods

##### test_purchase_order_qty(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_purchase_order_zero_qty(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_make_purchase_receipt(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_ordered_qty(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_ordered_qty_against_pi_with_update_stock(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_update_remove_child_linked_to_mr(self)

Test impact on linked PO and MR on deleting/updating row.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_update_child(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_update_child_adding_new_item(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_update_child_removing_item(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_update_child_perm(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_update_child_with_tax_template(self)

Test Action: Create a PO with one item having its tax account head already in the PO.
Add the same item + new item with tax template via Update Items.
Expected result: First Item's tax row is updated. New tax row is added for second Item.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_update_qty(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_return_against_purchase_order(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_purchase_order_invoice_receipt_workflow(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_make_purchase_invoice(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_purchase_order_on_hold(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_make_purchase_invoice_with_terms(self)

**Decorators**: `@IntegrationTestCase.change_settings('Accounts Settings', {'automatically_fetch_payment_terms': 1})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_warehouse_company_validation(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_uom_integer_validation(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_ordered_qty_for_closing_po(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_group_same_items(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_make_po_without_terms(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_po_for_blocked_supplier_all(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_po_for_blocked_supplier_invoices(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_po_for_blocked_supplier_payments(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_po_for_blocked_supplier_payments_with_today_date(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_po_for_blocked_supplier_payments_past_date(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_default_payment_terms(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_terms_are_not_copied_if_automatically_fetch_payment_terms_is_unchecked(self)

**Decorators**: `@IntegrationTestCase.change_settings('Accounts Settings', {'automatically_fetch_payment_terms': 0})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_terms_copied(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_advance_payment_entry_unlink_against_purchase_order(self)

**Decorators**: `@IntegrationTestCase.change_settings('Accounts Settings', {'unlink_advance_payment_on_cancelation_of_order': 1})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### create_account(self, account_name, company, currency, parent)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| account_name | None | - | - |
| company | None | - | - |
| currency | None | - | - |
| parent | None | - | - |


##### test_advance_payment_with_separate_party_account_enabled(self)

Test "Advance Paid" on Purchase Order, when "Book Advance Payments in Separate Party Account" is enabled and
the payment entry linked to the Order is allocated to Purchase Invoice.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_advance_paid_upon_payment_entry_cancellation(self)

**Decorators**: `@IntegrationTestCase.change_settings('Accounts Settings', {'unlink_advance_payment_on_cancelation_of_order': 1})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_schedule_date(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_po_optional_blanket_order(self)

Expected result: Blanket order Ordered Quantity should only be affected on Purchase Order with against_blanket_order = 1.
Second Purchase Order should not add on to Blanket Orders Ordered Quantity.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_blanket_order_on_po_close_and_open(self)

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


##### test_internal_transfer_flow(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_variant_item_po(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_update_items_for_subcontracting_purchase_order(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_new_sc_flow(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_auto_create_subcontracting_order(self)

**Decorators**: `@IntegrationTestCase.change_settings('Buying Settings', {'auto_create_subcontracting_order': 1})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_purchase_order_advance_payment_status(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_po_billed_amount_against_return_entry(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_receive_zero_qty_purchase_order(self)

Test the flow of a Unit Price PO and PR creation against it until completion.
Flow:
PO Qty 0 -> Receive +5 -> Receive +5 -> Update PO Qty +10 -> PO is 100% received

**Decorators**: `@IntegrationTestCase.change_settings('Buying Settings', {'allow_zero_qty_in_purchase_order': 1})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_bill_zero_qty_purchase_order(self)

**Decorators**: `@IntegrationTestCase.change_settings('Buying Settings', {'allow_zero_qty_in_purchase_order': 1})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_purchase_invoice_creation_with_partial_qty(self)

**Decorators**: `@IntegrationTestCase.change_settings('Buying Settings', {'maintain_same_rate': 0})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_multiple_advances_against_purchase_order_are_allocated_across_partial_purchase_invoices(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### create_po_for_sc_testing()

**Returns**: (none)



### prepare_data_for_internal_transfer()

**Returns**: (none)



### make_pr_against_po(po, received_qty = 0)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| po | None | - | - |
| received_qty | None | 0 | - |

**Returns**: (none)



### get_same_items()

**Returns**: (none)



### create_purchase_order()

**Returns**: (none)



### create_pr_against_po(po, received_qty = 4)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| po | None | - | - |
| received_qty | None | 4 | - |

**Returns**: (none)



### get_ordered_qty(item_code = '_Test Item', warehouse = '_Test Warehouse - _TC')

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item_code | None | '_Test Item' | - |
| warehouse | None | '_Test Warehouse - _TC' | - |

**Returns**: (none)



### get_requested_qty(item_code = '_Test Item', warehouse = '_Test Warehouse - _TC')

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item_code | None | '_Test Item' | - |
| warehouse | None | '_Test Warehouse - _TC' | - |

**Returns**: (none)



### update_items(po, qty)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| po | None | - | - |
| qty | None | - | - |

**Returns**: (none)


