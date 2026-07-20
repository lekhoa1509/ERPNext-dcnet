# API Reference: test_sales_order.py

**Language**: Python

**Source**: `doctype/sales_order/test_sales_order.py`

---

## Classes

### TestSalesOrder

**Inherits from**: AccountsTestMixin, IntegrationTestCase

#### Methods

##### setUpClass(cls)

**Decorators**: `@classmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| cls | None | - | - |


##### tearDownClass(cls) → None

**Decorators**: `@classmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| cls | None | - | - |

**Returns**: `None`


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


##### test_sales_order_with_negative_rate(self)

Test if negative rate is allowed in Sales Order via doc submission and update items

**Decorators**: `@IntegrationTestCase.change_settings('Selling Settings', {'allow_negative_rates_for_items': 1})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_sales_order_qty(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_sales_order_zero_qty(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_make_material_request(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_make_delivery_note(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_make_sales_invoice(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_so_billed_amount_against_return_entry(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_make_sales_invoice_with_terms(self)

**Decorators**: `@IntegrationTestCase.change_settings('Accounts Settings', {'automatically_fetch_payment_terms': 1})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_auto_fetch_terms_enable(self)

**Decorators**: `@IntegrationTestCase.change_settings('Accounts Settings', {'automatically_fetch_payment_terms': 1})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_auto_fetch_terms_disable(self)

**Decorators**: `@IntegrationTestCase.change_settings('Accounts Settings', {'automatically_fetch_payment_terms': 0})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_update_qty(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_return_against_sales_order(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_reserved_qty_for_partial_delivery(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_reserved_qty_for_over_delivery(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_reserved_qty_for_over_delivery_via_sales_invoice(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_reserved_qty_for_partial_delivery_with_packing_list(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_sales_order_on_hold(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_reserved_qty_for_over_delivery_with_packing_list(self)

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


##### test_update_child(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_update_child_with_precision(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_update_child_perm(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_update_child_qty_rate_with_workflow(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_material_request_for_product_bundle(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_bin_details_of_packed_item(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_update_child_product_bundle(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_update_child_with_tax_template(self)

Test Action: Create a SO with one item having its tax account head already in the SO.
Add the same item + new item with tax template via Update Items.
Expected result: First Item's tax row is updated. New tax row is added for second Item.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_warehouse_user(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_block_delivery_note_against_cancelled_sales_order(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_service_type_product_bundle(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_mix_type_product_bundle(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_auto_insert_price(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_update_existing_item_price(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_drop_shipping(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_drop_shipping_partial_order(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_drop_shipping_full_for_default_suppliers(self)

Test if multiple POs are generated in one go against different default suppliers.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_product_bundles_in_so_are_replaced_with_bundle_items_in_po(self)

Tests if the the Product Bundles in the Items table of Sales Orders are replaced with
their child items(from the Packed Items table) on creating a Purchase Order from it.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_purchase_order_updates_packed_item_ordered_qty(self)

Tests if the packed item's `ordered_qty` is updated with the quantity of the Purchase Order

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_reserved_qty_for_closing_so(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_create_so_with_margin(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_terms_auto_added(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_terms_not_copied(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_terms_copied(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_make_work_order(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_advance_payment_entry_unlink_against_sales_order(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_advance_paid_upon_payment_cancellation(self)

**Decorators**: `@IntegrationTestCase.change_settings('Accounts Settings', {'unlink_advance_payment_on_cancelation_of_order': 1})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_cancel_sales_order_after_cancel_payment_entry(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_work_order_pop_up_from_sales_order(self)

Test `get_work_order_items` in Sales Order picks the right BOM for items to manufacture.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_request_for_raw_materials(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_so_optional_blanket_order(self)

Expected result: Blanket order Ordered Quantity should only be affected on Sales Order with against_blanket_order = 1.
Second Sales Order should not add on to Blanket Orders Ordered Quantity.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_so_cancellation_when_si_drafted(self)

Test to check if Sales Order gets cancelled if Sales Invoice is in Draft state
Expected result: sales order should not get cancelled

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_so_cancellation_after_si_submission(self)

Test to check if Sales Order gets cancelled when linked Sales Invoice has been Submitted
Expected result: Sales Order should not get cancelled

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_so_cancellation_after_dn_submission(self)

Test to check if Sales Order gets cancelled when linked Delivery Note has been Submitted
Expected result: Sales Order should not get cancelled

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_so_cancellation_after_maintenance_schedule_submission(self)

Expected result: Sales Order should not get cancelled

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_so_cancellation_after_maintenance_visit_submission(self)

Expected result: Sales Order should not get cancelled

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_so_cancellation_after_work_order_submission(self)

Expected result: Sales Order should not get cancelled

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_payment_terms_are_fetched_when_creating_sales_invoice(self)

**Decorators**: `@IntegrationTestCase.change_settings('Accounts Settings', {'automatically_fetch_payment_terms': 1})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_zero_amount_sales_order_billing_status(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_so_billing_status_with_crnote_against_sales_return(self)

| Step | Document creation                    |                               |
|------+--------------------------------------+-------------------------------|
|    1 | SO -> DN -> SI                       | SO Fully Billed and Completed |
|    2 | DN -> Sales Return(Partial)          | SO 50% Delivered, 100% billed |
|    3 | Sales Return(Partial) -> Credit Note | SO 50% Delivered, 50% billed  |

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_so_back_updated_from_wo_via_mr(self)

SO -> MR (Manufacture) -> WO. Test if WO Qty is updated in SO.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_sales_order_with_shipping_rule(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_sales_order_partial_advance_payment(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_delivered_item_material_request(self)

SO -> MR (Manufacture) -> WO. Test if WO Qty is updated in SO.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_packed_items_for_partial_sales_order(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_expired_rate_for_packed_item(self)

**Decorators**: `@IntegrationTestCase.change_settings('Selling Settings', {'editable_bundle_item_rates': 1})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_sales_order_advance_payment_status(self, mocked_get_payment_url)

**Decorators**: `@patch('erpnext.accounts.doctype.payment_request.payment_request.PaymentRequest.get_payment_url', return_value=None)`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| mocked_get_payment_url | None | - | - |


##### test_pick_list_without_rejected_materials(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_pick_list_for_batch(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_auto_update_price_list(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_delivery_note_rate_on_change_of_warehouse(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_credit_limit_on_so_reopning(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_warehouse_mapping_based_on_stock_reservation(self)

**Decorators**: `@IntegrationTestCase.change_settings('Stock Settings', {'enable_stock_reservation': True})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_deliver_zero_qty_purchase_order(self)

Test the flow of a Unit Price SO and DN creation against it until completion.
Flow:
SO Qty 0 -> Deliver +5 -> Update SO Qty +10 -> Deliver +5 -> SO is 100% delivered

**Decorators**: `@IntegrationTestCase.change_settings('Selling Settings', {'allow_zero_qty_in_sales_order': 1})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_bill_zero_qty_sales_order(self)

**Decorators**: `@IntegrationTestCase.change_settings('Selling Settings', {'allow_zero_qty_in_sales_order': 1})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_item_tax_transfer_from_sales_to_purchase(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_pending_quantity_after_update_item_during_invoice_creation(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### compare_payment_schedules(doc, doc1, doc2)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |
| doc1 | None | - | - |
| doc2 | None | - | - |

**Returns**: (none)



### make_sales_order()

**Returns**: (none)



### create_dn_against_so(so, delivered_qty = 0, do_not_submit = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| so | None | - | - |
| delivered_qty | None | 0 | - |
| do_not_submit | None | False | - |

**Returns**: (none)



### get_reserved_qty(item_code = '_Test Item', warehouse = '_Test Warehouse - _TC')

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item_code | None | '_Test Item' | - |
| warehouse | None | '_Test Warehouse - _TC' | - |

**Returns**: (none)



### make_sales_order_workflow()

**Returns**: (none)


