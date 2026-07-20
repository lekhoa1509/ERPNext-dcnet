# API Reference: test_stock_entry.py

**Language**: Python

**Source**: `doctype/stock_entry/test_stock_entry.py`

---

## Classes

### TestStockEntry

**Inherits from**: IntegrationTestCase

#### Methods

##### tearDown(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_stock_entry_qty(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_fifo(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_auto_material_request(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_barcode_item_stock_entry(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_auto_material_request_for_variant(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_auto_material_request_for_warehouse_group(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _test_auto_material_request(self, item_code, material_request_type = 'Purchase', warehouse = '_Test Warehouse - _TC')

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| item_code | None | - | - |
| material_request_type | None | 'Purchase' | - |
| warehouse | None | '_Test Warehouse - _TC' | - |


##### test_add_to_transit_entry(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_material_receipt_gl_entry(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_material_issue_gl_entry(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_material_transfer_gl_entry(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_repack_multiple_fg(self)

Test `is_finished_item` for one item repacked into two items.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_repack_no_change_in_valuation(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_repack_with_additional_costs(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### check_stock_ledger_entries(self, voucher_type, voucher_no, expected_sle)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| voucher_type | None | - | - |
| voucher_no | None | - | - |
| expected_sle | None | - | - |


##### check_gl_entries(self, voucher_type, voucher_no, expected_gl_entries)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| voucher_type | None | - | - |
| voucher_no | None | - | - |
| expected_gl_entries | None | - | - |


##### test_serial_no_not_reqd(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_serial_no_reqd(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_serial_no_qty_less(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_serial_no_transfer_in(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_serial_by_series(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_serial_move(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_serial_cancel(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_serial_batch_item_stock_entry(self)

Behaviour: 1) Submit Stock Entry (Receipt) with Serial & Batched Item
2) Cancel same Stock Entry
Expected Result: 1) Batch is created with Reference in Serial No
2) Batch is deleted and Serial No is Inactive

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_warehouse_company_validation(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_warehouse_user(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_freeze_stocks(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_work_order(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_work_order_manufacture_with_material_consumption(self)

**Decorators**: `@IntegrationTestCase.change_settings('Manufacturing Settings', {'material_consumption': 1})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_variant_work_order(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_nagative_stock_for_batch(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_quality_check_for_scrap_item(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_quality_check(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_customer_provided_parts_se(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_zero_incoming_rate(self)

Make sure incoming rate of 0 is allowed while consuming.

qty  | rate | valuation rate
 1   | 100  | 100
 1   | 0    | 50
-1   | 100  | 0
-1   | 0  <--- assert this

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_gle_for_opening_stock_entry(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_total_basic_amount_zero(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_conversion_factor_change(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_additional_cost_distribution_manufacture(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_additional_cost_distribution_non_manufacture(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_independent_manufacture_entry(self)

Test FG items and incoming rate calculation in Maniufacture Entry without WO or BOM linked.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_future_negative_sle(self)

**Decorators**: `@IntegrationTestCase.change_settings('Stock Settings', {'allow_negative_stock': 0})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_future_negative_sle_batch(self)

**Decorators**: `@IntegrationTestCase.change_settings('Stock Settings', {'allow_negative_stock': 0})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_multi_batch_value_diff(self)

Test value difference on stock entry in case of multi-batch.
| Stock entry | batch | qty | rate | value diff on SE             |
| ---         | ---   | --- | ---  | ---                          |
| receipt     | A     | 1   | 10   | 30                           |
| receipt     | B     | 1   | 20   |                              |
| issue       | A     | -1  | 10   | -30 (to assert after submit) |
| issue       | B     | -1  | 20   |                              |

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_transfer_qty_validation(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_mapped_stock_entry(self)

Check if rate and stock details are populated in mapped SE given warehouse.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_stock_entry_item_details(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_reposting_for_depedent_warehouse(self)

**Decorators**: `@IntegrationTestCase.change_settings('Stock Reposting Settings', {'item_based_reposting': 0})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_batch_expiry(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_negative_stock_reco(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_negative_batch(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_auto_reorder_level(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_auto_reorder_level_with_lead_time_days(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_use_serial_and_batch_fields(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_serial_batch_bundle_type_of_transaction(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_stock_entry_for_same_posting_date_and_time(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_stock_entry_amount(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_use_batch_wise_valuation_for_moving_average_item(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_periodic_accounting_entries(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_batch_item_additional_cost_for_material_transfer_entry(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_prevent_reuse_delivered_serial_no_in_repack(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_transferred_qty_in_material_transfer(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_manufacture_entry_without_wo(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_disassemble_entry_without_wo(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_sample_retention_stock_entry(self)

**Decorators**: `@IntegrationTestCase.change_settings('Stock Settings', {'sample_retention_warehouse': '_Test Warehouse 1 - _TC'})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_raw_material_missing_validation(self)

**Decorators**: `@IntegrationTestCase.change_settings('Manufacturing Settings', {'material_consumption': 0})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_validation_as_per_bom_with_continuous_raw_material_consumption(self)

**Decorators**: `@IntegrationTestCase.change_settings('Manufacturing Settings', {'material_consumption': 1, 'backflush_raw_materials_based_on': 'BOM', 'validate_components_quantities_per_bom': 1})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### get_sle()

**Returns**: (none)



### make_serialized_item(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: (none)



### get_qty_after_transaction()

**Returns**: (none)



### get_multiple_items()

**Returns**: (none)



### initialize_records_for_future_negative_sle_test(item_code, batch_no, warehouses, opening_qty, posting_date)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item_code | None | - | - |
| batch_no | None | - | - |
| warehouses | None | - | - |
| opening_qty | None | - | - |
| posting_date | None | - | - |

**Returns**: (none)



### create_stock_entries(sequence_of_entries)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| sequence_of_entries | None | - | - |

**Returns**: (none)


