# API Reference: test_work_order.py

**Language**: Python

**Source**: `doctype/work_order/test_work_order.py`

---

## Classes

### TestWorkOrder

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


##### check_planned_qty(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_over_production(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_planned_operating_cost(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_reserved_qty_for_partial_completion(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_production_item(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_reserved_qty_for_production_submit(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_reserved_qty_for_production_cancel(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_reserved_qty_for_production_on_stock_entry(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_reserved_qty_for_production_closed(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_backflush_qty_for_overpduction_manufacture(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_reserved_qty_for_stopped_production(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_scrap_material_qty(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_allow_overproduction(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_over_production_for_sales_order(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_work_order_with_non_stock_item(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_job_card(self)

**Decorators**: `@timeout(seconds=60)`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_work_order_material_transferred_qty_with_process_loss(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_capcity_planning(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_work_order_with_non_transfer_item(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_cost_center_for_manufacture(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_operation_time_with_batch_size(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_batch_size_for_fg_item(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_partial_material_consumption(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_extra_material_transfer(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_make_stock_entry_for_customer_provided_item(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_valuation_rate_missing_on_make_stock_entry(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_wo_completion_with_pl_bom(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_job_card_scrap_item(self)

**Decorators**: `@timeout(seconds=60)`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_close_work_order(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_fix_time_operations(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_partial_manufacture_entries(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_auto_batch_creation(self)

**Decorators**: `@IntegrationTestCase.change_settings('Manufacturing Settings', {'make_serial_no_batch_from_work_order': 1})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_auto_serial_no_creation(self)

**Decorators**: `@IntegrationTestCase.change_settings('Manufacturing Settings', {'make_serial_no_batch_from_work_order': 1})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_auto_serial_no_batch_creation(self)

**Decorators**: `@IntegrationTestCase.change_settings('Manufacturing Settings', {'make_serial_no_batch_from_work_order': 1})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_serial_nos_for_fg(self, work_order)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| work_order | None | - | - |


##### test_manufacture_entry_mapped_idx_with_exploded_bom(self)

Test if WO containing BOM with partial exploded items and scrap items, maps idx correctly.

**Decorators**: `@IntegrationTestCase.change_settings('Manufacturing Settings', {'backflush_raw_materials_based_on': 'Material Transferred for Manufacture'})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_work_order_multiple_material_transfer(self)

Test transferring multiple RMs in separate Stock Entries.

**Decorators**: `@IntegrationTestCase.change_settings('Manufacturing Settings', {'backflush_raw_materials_based_on': 'Material Transferred for Manufacture'})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_backflushed_batch_raw_materials_based_on_transferred(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_backflushed_serial_no_raw_materials_based_on_transferred(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_backflushed_serial_no_batch_raw_materials_based_on_transferred(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_backflushed_batch_raw_materials_based_on_transferred_autosabb(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_backflushed_serial_no_raw_materials_based_on_transferred_autosabb(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_backflushed_serial_no_batch_raw_materials_based_on_transferred_autosabb(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_non_consumed_material_return_against_work_order(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_workstation_type_for_work_order(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_job_card_extra_qty(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_operating_cost_account(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_op_cost_and_scrap_based_on_sub_assemblies(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_get_rm_cost_from_consumption_entry(self)

**Decorators**: `@IntegrationTestCase.change_settings('Manufacturing Settings', {'material_consumption': 1, 'get_rm_cost_from_consumption_entry': 1})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_capcity_planning_for_workstation(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_partial_material_consumption_with_batch(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_disassemby_order(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_disassembly_order_with_qty_behavior(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_disassembly_with_multiple_manufacture_entries(self)

Test that disassembly does not create duplicate items when manufacturing
is done in multiple batches (multiple manufacture stock entries).

Scenario:
1. Create Work Order for 10 units
2. Transfer raw materials
3. Manufacture in 2 parts (3 units, then 7 units) - creates 2 stock entries
4. Create Disassembly for 4 units
5. Verify no duplicate items in the disassembly stock entry

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_disassembly_with_additional_rm_not_in_bom(self)

Test that disassembly correctly handles additional raw materials that were
manually added during manufacturing (not part of the BOM).

Scenario:
1. Create Work Order for 10 units with 2 raw materials in BOM
2. Transfer raw materials for manufacture
3. Manufacture in 2 parts (3 units, then 7 units)
4. In each manufacture entry, manually add an extra consumable item
   (not in BOM) in proportion to the manufactured qty
5. Create Disassembly for 4 units
6. Verify that the additional RM is included in disassembly with proportional qty

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_components_alternate_item_for_bom_based_manufacture_entry(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_components_qty_for_bom_based_manufacture_entry(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_components_as_per_bom_for_manufacture_entry(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_wip_skip(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_serial_no_status_for_stock_entry(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_stock_reservation_for_serialized_raw_material(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_stock_reservation_for_batched_raw_material(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_auto_stock_reservation_for_batched_raw_material(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_work_order_valuation_auto_pick(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_operations_time_planning_calculation(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_allow_additional_material_transfer(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_req_qty_clamping_in_manufacture_entry(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_overproduction_allowed_qty(self)

Test overproduction allowed qty in work order

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_reserved_serial_batch(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_phantom_bom_item_not_in_additional_cost(self)

Test that phantom BOMs are not added to additional costs,
but regular non-stock items in the FG BOM are added.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_phantom_bom_explosion(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_reserved_qty_for_pp_with_extra_material_transfer(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### get_reserved_entries(voucher_no, warehouse = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| voucher_no | None | - | - |
| warehouse | None | None | - |

**Returns**: (none)



### make_stock_in_entries_and_get_batches(rm_item, source_warehouse, wip_warehouse)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| rm_item | None | - | - |
| source_warehouse | None | - | - |
| wip_warehouse | None | - | - |

**Returns**: (none)



### make_operation()

**Returns**: (none)



### make_workstation()

**Returns**: (none)



### prepare_boms_for_sub_assembly_test()

**Returns**: (none)



### prepare_data_for_workstation_type_check()

**Returns**: (none)



### prepare_data_for_backflush_based_on_materials_transferred()

**Returns**: (none)



### update_job_card(job_card, jc_qty = None, days = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| job_card | None | - | - |
| jc_qty | None | None | - |
| days | None | None | - |

**Returns**: (none)



### get_scrap_item_details(bom_no)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| bom_no | None | - | - |

**Returns**: (none)



### allow_overproduction(fieldname, percentage)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| fieldname | None | - | - |
| percentage | None | - | - |

**Returns**: (none)



### make_wo_order_test_record()

**Returns**: (none)


