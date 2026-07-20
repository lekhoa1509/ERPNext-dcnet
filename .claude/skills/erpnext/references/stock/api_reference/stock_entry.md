# API Reference: stock_entry.py

**Language**: Python

**Source**: `doctype/stock_entry/stock_entry.py`

---

## Classes

### FinishedGoodError

**Inherits from**: frappe.ValidationError



### IncorrectValuationRateError

**Inherits from**: frappe.ValidationError



### DuplicateEntryForWorkOrderError

**Inherits from**: frappe.ValidationError



### OperationsNotCompleteError

**Inherits from**: frappe.ValidationError



### MaxSampleAlreadyRetainedError

**Inherits from**: frappe.ValidationError



### StockEntry

**Inherits from**: StockController, SubcontractingInwardController

#### Methods

##### __init__(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### onload(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### before_insert(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### before_validate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_repack_entry(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_raw_materials_exists(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_serial_batch_for_disassembly(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_submit(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_cancel(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_update(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_job_card_data(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_job_card_fg_item(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_job_card_item(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_work_order_status(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_purpose(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### delete_linked_stock_entry(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### delink_asset_repair_sabb(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_transfer_qty(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_cost_in_project(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_item(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_fg_completed_qty(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_difference_account(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_warehouse(self)

perform various (sometimes conditional) validations on warehouse

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_work_order(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### check_if_operations_completed(self)

Check if Time Sheets are completed against before manufacturing to capture operating costs.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### check_duplicate_entry_for_work_order(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_actual_qty(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_component_and_quantities(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_same_source_target_warehouse_during_material_transfer(self)

Validate Material Transfer entries where source and target warehouses are identical.

For Material Transfer purpose, if an item has the same source and target warehouse,
require that at least one inventory dimension (if configured) differs between source
and target to ensure a meaningful transfer is occurring.

Raises:
frappe.ValidationError: If warehouses are same and no inventory dimensions differ

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_matched_items(self, item_code)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| item_code | None | - | - |


##### get_consumed_items(self)

Get all raw materials consumed through consumption entries

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_stock_and_rate(self)

Updates rate and availability of all the items.
Called from Update Rate and Availability button.

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### calculate_rate_and_amount(self, reset_outgoing_rate = True, raise_error_if_no_rate = True)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| reset_outgoing_rate | None | True | - |
| raise_error_if_no_rate | None | True | - |


##### set_basic_rate(self, reset_outgoing_rate = True, raise_error_if_no_rate = True)

Set rate for outgoing, scrapped and finished items

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| reset_outgoing_rate | None | True | - |
| raise_error_if_no_rate | None | True | - |


##### set_rate_for_outgoing_items(self, reset_outgoing_rate = True, raise_error_if_no_rate = True)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| reset_outgoing_rate | None | True | - |
| raise_error_if_no_rate | None | True | - |


##### get_args_for_incoming_rate(self, item)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| item | None | - | - |


##### get_basic_rate_for_repacked_items(self, finished_item_qty, outgoing_items_cost)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| finished_item_qty | None | - | - |
| outgoing_items_cost | None | - | - |


##### get_basic_rate_for_manufactured_item(self, finished_item_qty, outgoing_items_cost = 0) → float

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| finished_item_qty | None | - | - |
| outgoing_items_cost | None | 0 | - |

**Returns**: `float`


##### distribute_additional_costs(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_valuation_rate(self, reset_outgoing_rate = True)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| reset_outgoing_rate | None | True | - |


##### set_total_incoming_outgoing_value(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_total_amount(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_stock_entry_type(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_purpose_for_stock_entry(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### make_serial_and_batch_bundle_for_outward(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_serial_batch_fields_for_subcontracting_inward(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_subcontract_order(self)

Throw exception if more raw material is transferred against Subcontract Order than in
the raw materials supplied table

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_bom(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_purchase_order(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_closed_subcontracting_order(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### mark_finished_and_scrap_items(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_finished_item(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_finished_goods(self)

1. Check if FG exists (mfg, repack)
2. Check if Multiple FG Items are present (mfg)
3. Check FG Item and Qty against WO if present (mfg)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_stock_ledger(self, allow_negative_stock = False, via_landed_cost_voucher = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| allow_negative_stock | None | False | - |
| via_landed_cost_voucher | None | False | - |


##### get_finished_item_row(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_serial_batch_bundle_type(self, serial_and_batch_bundle)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| serial_and_batch_bundle | None | - | - |


##### get_sle_for_source_warehouse(self, sl_entries, finished_item_row)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| sl_entries | None | - | - |
| finished_item_row | None | - | - |


##### make_serial_and_batch_bundle_for_transfer(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_sle_for_target_warehouse(self, sl_entries, finished_item_row)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| sl_entries | None | - | - |
| finished_item_row | None | - | - |


##### get_gl_entries(self, inventory_account_map)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| inventory_account_map | None | - | - |


##### set_gl_entries_for_landed_cost_voucher(self, gl_entries, inventory_account_map)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| gl_entries | None | - | - |
| inventory_account_map | None | - | - |


##### update_work_order(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_disassembled_order(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### make_stock_reserve_for_wip_and_fg(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### reserve_stock_for_subcontracting(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### cancel_stock_reserve_for_wip_and_fg(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### is_stock_reserve_for_work_order(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_item_details(self, args: ItemDetailsCtx = None, for_update = False)

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| args | ItemDetailsCtx | None | - |
| for_update | None | False | - |


##### set_items_for_stock_in(self)

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_items_for_disassembly(self)

Get items for Disassembly Order

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _add_items_for_disassembly_from_work_order(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _add_items_for_disassembly_from_bom(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_items_from_manufacture_entry(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_items(self)

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_serial_batch_from_reserved_entry(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_available_reserved_materials(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_reserved_materials(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_scrap_items(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_process_loss_qty(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_work_order_details(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### load_items_from_bom(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_batchwise_finished_goods(self, args, item)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| args | None | - | - |
| item | None | - | - |


##### add_batchwise_finished_good(self, batches, args, item)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| batches | None | - | - |
| args | None | - | - |
| item | None | - | - |


##### add_finished_goods(self, args, item)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| args | None | - | - |
| item | None | - | - |


##### get_bom_raw_materials(self, qty)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| qty | None | - | - |


##### get_bom_scrap_material(self, qty)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| qty | None | - | - |


##### get_scrap_items_from_job_card(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_completed_job_card_qty(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_used_scrap_items(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_unconsumed_raw_materials(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### add_transfered_raw_materials_in_items(self) → None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `None`


##### update_batches_to_be_consume(self, batches, row, qty)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| batches | None | - | - |
| row | None | - | - |
| qty | None | - | - |


##### update_item_in_stock_entry_detail(self, row, item, qty) → None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| row | None | - | - |
| item | None | - | - |
| qty | None | - | - |

**Returns**: `None`


##### get_serial_nos_based_on_transferred_batch(batch_no, serial_nos) → list

**Decorators**: `@staticmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| batch_no | None | - | - |
| serial_nos | None | - | - |

**Returns**: `list`


##### get_pending_raw_materials(self, backflush_based_on = None)

issue (item quantity) that is pending to issue or desire to transfer,
whichever is less

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| backflush_based_on | None | None | - |


##### get_pro_order_required_items(self, backflush_based_on = None)

Gets Work Order Required Items only if Stock Entry purpose is **Material Transferred for Manufacture**.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| backflush_based_on | None | None | - |


##### get_job_card_item_codes(self, job_card = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| job_card | None | None | - |


##### add_to_stock_entry_detail(self, item_dict, bom_no = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| item_dict | None | - | - |
| bom_no | None | None | - |


##### validate_with_material_request(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_batch(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_subcontract_order_supplied_items(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_transferred_qty(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_quality_inspection(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_material_request_transfer_status(self, status)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| status | None | - | - |


##### set_serial_no_batch_for_finished_good(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_available_serial_nos(self) → list[str]

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `list[str]`


##### update_subcontracting_order_status(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_pick_list_status(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_missing_values(self)

Updates rate and availability of all the items of mapped doc.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### move_sample_to_retention_warehouse(company, items)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| company | None | - | - |
| items | None | - | - |

**Returns**: (none)



### make_stock_in_entry(source_name, target_doc = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| source_name | None | - | - |
| target_doc | None | None | - |

**Returns**: (none)



### get_work_order_details(work_order, company)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| work_order | None | - | - |
| company | None | - | - |

**Returns**: (none)



### get_consumed_operating_cost(wo_name, bom_no)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| wo_name | None | - | - |
| bom_no | None | - | - |

**Returns**: (none)



### get_operating_cost_per_unit(work_order = None, bom_no = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| work_order | None | None | - |
| bom_no | None | None | - |

**Returns**: (none)



### get_used_alternative_items(subcontract_order = None, subcontract_order_field = 'subcontracting_order', work_order = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| subcontract_order | None | None | - |
| subcontract_order_field | None | 'subcontracting_order' | - |
| work_order | None | None | - |

**Returns**: (none)



### get_valuation_rate_for_finished_good_entry(work_order)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| work_order | None | - | - |

**Returns**: (none)



### get_uom_details(item_code, uom, qty)

Returns dict `{"conversion_factor": [value], "transfer_qty": qty * [value]}`
:param args: dict with `item_code`, `uom` and `qty`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item_code | None | - | - |
| uom | None | - | - |
| qty | None | - | - |

**Returns**: (none)



### get_expired_batch_items()

**Returns**: (none)



### get_expired_batches()

**Returns**: (none)



### get_warehouse_details(args)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| args | None | - | - |

**Returns**: (none)



### validate_sample_quantity(item_code, sample_quantity, qty, batch_no = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item_code | None | - | - |
| sample_quantity | None | - | - |
| qty | None | - | - |
| batch_no | None | None | - |

**Returns**: (none)



### get_supplied_items(subcontract_order, rm_detail_field = 'sco_rm_detail', subcontract_order_field = 'subcontracting_order')

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| subcontract_order | None | - | - |
| rm_detail_field | None | 'sco_rm_detail' | - |
| subcontract_order_field | None | 'subcontracting_order' | - |

**Returns**: (none)



### get_items_from_subcontract_order(source_name, target_doc = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| source_name | None | - | - |
| target_doc | None | None | - |

**Returns**: (none)



### get_available_materials(work_order, stock_entry_doc = None) → dict

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| work_order | None | - | - |
| stock_entry_doc | None | None | - |

**Returns**: `dict`



### get_stock_entry_data(work_order, stock_entry_doc = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| work_order | None | - | - |
| stock_entry_doc | None | None | - |

**Returns**: (none)



### create_serial_and_batch_bundle(parent_doc, row, child, type_of_transaction = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| parent_doc | None | - | - |
| row | None | - | - |
| child | None | - | - |
| type_of_transaction | None | None | - |

**Returns**: (none)



### get_batchwise_serial_nos(item_code, row)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item_code | None | - | - |
| row | None | - | - |

**Returns**: (none)



### get_transferred_qty(material_request)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| material_request | None | - | - |

**Returns**: (none)



### set_missing_values(source, target)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| source | None | - | - |
| target | None | - | - |

**Returns**: (none)



### update_item(source_doc, target_doc, source_parent)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| source_doc | None | - | - |
| target_doc | None | - | - |
| source_parent | None | - | - |

**Returns**: (none)



### _validate_work_order(pro_doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| pro_doc | None | - | - |

**Returns**: (none)


