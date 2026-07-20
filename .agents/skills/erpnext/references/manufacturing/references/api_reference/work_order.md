# API Reference: work_order.py

**Language**: Python

**Source**: `doctype/work_order/work_order.py`

---

## Classes

### OverProductionError

**Inherits from**: frappe.ValidationError



### CapacityError

**Inherits from**: frappe.ValidationError



### StockOverProductionError

**Inherits from**: frappe.ValidationError



### OperationTooLongError

**Inherits from**: frappe.ValidationError



### ItemHasVariantError

**Inherits from**: frappe.ValidationError



### SerialNoQtyError

**Inherits from**: frappe.ValidationError



### WorkOrder

**Inherits from**: Document

#### Methods

##### onload(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### show_create_job_card_button(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_discard(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_dates(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_fg_warehouse_for_reservation(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_reserve_stock(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### enable_auto_reserve_stock(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_operations_sequence(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_subcontracting_inward_order(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_warehouses(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### reset_use_multi_level_bom(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_workstation_type(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_sales_order(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### check_sales_order_on_hold_or_close(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_default_warehouse(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### check_wip_warehouse_skip(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_warehouse_belongs_to_company(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### calculate_operating_cost(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_work_order_against_so(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_status(self, status = None)

Update status of work order if unknown

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| status | None | None | - |


##### get_status(self, status = None)

Return the status based on stock entries against this work order

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| status | None | None | - |


##### update_work_order_qty(self)

Update **Manufactured Qty** and **Material Transferred for Qty** in Work Order
based on Stock Entry

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_additional_transferred_qty(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_disassembled_qty(self, qty, is_cancel = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| qty | None | - | - |
| is_cancel | None | False | - |


##### get_transferred_or_manufactured_qty(self, purpose, fieldname)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| purpose | None | - | - |
| fieldname | None | - | - |


##### set_process_loss_qty(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_production_plan_status(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_warehouse(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### before_submit(self)

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


##### on_close_or_cancel(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_stock_reservation(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_qty_change(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_subcontracting_inward_order_received_items(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### create_serial_no_batch_no(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### create_batch_for_finished_good(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### delete_auto_created_batch_and_serial_no(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### make_serial_nos(self, args)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| args | None | - | - |


##### create_job_card(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### prepare_data_for_job_card(self, row, idx, plan_days, enable_capacity_planning)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| row | None | - | - |
| idx | None | - | - |
| plan_days | None | - | - |
| enable_capacity_planning | None | - | - |


##### set_operation_start_end_time(self, row, idx)

Set start and end time for given operation. If first operation, set start as
`planned_start_date`, else add time diff to end time of earlier operation.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| row | None | - | - |
| idx | None | - | - |


##### validate_cancel(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_planned_qty(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_produced_qty_for_sub_assembly_item(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_ordered_qty(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_work_order_qty_in_so(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_work_order_qty_in_combined_so(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_completed_qty_in_material_request(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_work_order_operations(self)

Fetch operations from BOM and set in 'Work Order'

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### calculate_time(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_holidays(self, workstation)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| workstation | None | - | - |


##### update_operation_status(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_actual_dates(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_lead_time(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### delete_job_card(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_production_item(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_qty(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_transfer_against(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_operation_time(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_required_items(self)

update bin reserved_qty_for_production
called from Stock Entry for production, after submit, cancel

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_reserved_qty_for_production(self, items = None)

update reserved_qty_for_production in bins

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| items | None | None | - |


##### get_items_and_operations_from_bom(self)

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_available_qty(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_required_items(self, reset_only_qty = False, reset_source_warehouse = False)

set required_items for production to keep track of reserved qty

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| reset_only_qty | None | False | - |
| reset_source_warehouse | None | False | - |


##### update_transferred_qty_for_required_items(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_qty_in_stock_reservation(self, row, transferred_qty, row_wise_serial_batch)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| row | None | - | - |
| transferred_qty | None | - | - |
| row_wise_serial_batch | None | - | - |


##### update_returned_qty(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_consumed_qty_for_required_items(self)

Update consumed qty from submitted stock entries
against a work order for each stock item

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_consumed_qty_in_stock_reservation(self, item, consumed_qty, wip_warehouse)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| item | None | - | - |
| consumed_qty | None | - | - |
| wip_warehouse | None | - | - |


##### validate_reserved_qty(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### make_bom(self)

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_reserved_qty_for_wip_and_fg(self, stock_entry)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| stock_entry | None | - | - |


##### get_list_of_materials_for_reservation(self, stock_entry)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| stock_entry | None | - | - |


##### get_finished_goods_for_reservation(self, stock_entry)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| stock_entry | None | - | - |


##### get_wo_details(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_scio_details(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_so_details(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_voucher_details(self, stock_entry)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| stock_entry | None | - | - |


##### cancel_reserved_qty_for_wip_and_fg(self, ste_doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| ste_doc | None | - | - |


##### remove_additional_items(self, stock_entry)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| stock_entry | None | - | - |


##### add_additional_items(self, stock_entry)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| stock_entry | None | - | - |




## Functions

### make_stock_reservation_entries(doc, items = None, is_transfer = True, notify = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |
| items | None | None | - |
| is_transfer | None | True | - |
| notify | None | False | - |

**Returns**: (none)



### cancel_stock_reservation_entries(doc, sre_list)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |
| sre_list | None | - | - |

**Returns**: (none)



### get_sre_details(work_order)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| work_order | None | - | - |

**Returns**: (none)



### get_consumed_qty(work_order, item_code)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| work_order | None | - | - |
| item_code | None | - | - |

**Returns**: (none)



### get_bom_operations(doctype, txt, searchfield, start, page_len, filters)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| txt | None | - | - |
| searchfield | None | - | - |
| start | None | - | - |
| page_len | None | - | - |
| filters | None | - | - |

**Returns**: (none)



### get_item_details(item, project = None, skip_bom_info = False, throw = True)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item | None | - | - |
| project | None | None | - |
| skip_bom_info | None | False | - |
| throw | None | True | - |

**Returns**: (none)



### make_work_order(bom_no, item, qty = 0, project = None, variant_items = None, use_multi_level_bom = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| bom_no | None | - | - |
| item | None | - | - |
| qty | None | 0 | - |
| project | None | None | - |
| variant_items | None | None | - |
| use_multi_level_bom | None | None | - |

**Returns**: (none)



### add_variant_item(variant_items, wo_doc, bom_no, table_name = 'items')

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| variant_items | None | - | - |
| wo_doc | None | - | - |
| bom_no | None | - | - |
| table_name | None | 'items' | - |

**Returns**: (none)



### get_template_rm_item(wo_doc, item_code)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| wo_doc | None | - | - |
| item_code | None | - | - |

**Returns**: (none)



### check_if_scrap_warehouse_mandatory(bom_no)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| bom_no | None | - | - |

**Returns**: (none)



### set_work_order_ops(name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| name | None | - | - |

**Returns**: (none)



### make_stock_entry(work_order_id, purpose, qty = None, target_warehouse = None, is_additional_transfer_entry = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| work_order_id | None | - | - |
| purpose | None | - | - |
| qty | None | None | - |
| target_warehouse | None | None | - |
| is_additional_transfer_entry | None | False | - |

**Returns**: (none)



### get_default_warehouse(company)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| company | None | - | - |

**Returns**: (none)



### stop_unstop(work_order, status)

Called from client side on Stop/Unstop event

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| work_order | None | - | - |
| status | None | - | - |

**Returns**: (none)



### query_sales_order(doctype, txt, searchfield, start, page_len, filters) → list[str]

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| txt | None | - | - |
| searchfield | None | - | - |
| start | None | - | - |
| page_len | None | - | - |
| filters | None | - | - |

**Returns**: `list[str]`



### make_job_card(work_order, operations)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| work_order | None | - | - |
| operations | None | - | - |

**Returns**: (none)



### get_operation_details(name, work_order)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| name | None | - | - |
| work_order | None | - | - |

**Returns**: (none)



### close_work_order(work_order, status)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| work_order | None | - | - |
| status | None | - | - |

**Returns**: (none)



### split_qty_based_on_batch_size(wo_doc, row, qty)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| wo_doc | None | - | - |
| row | None | - | - |
| qty | None | - | - |

**Returns**: (none)



### get_serial_nos_for_job_card(row, wo_doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| row | None | - | - |
| wo_doc | None | - | - |

**Returns**: (none)



### get_serial_nos_for_work_order(work_order, production_item)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| work_order | None | - | - |
| production_item | None | - | - |

**Returns**: (none)



### validate_operation_data(row)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| row | None | - | - |

**Returns**: (none)



### create_job_card(work_order, row, enable_capacity_planning = False, auto_create = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| work_order | None | - | - |
| row | None | - | - |
| enable_capacity_planning | None | False | - |
| auto_create | None | False | - |

**Returns**: (none)



### get_work_order_operation_data(work_order, operation, workstation)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| work_order | None | - | - |
| operation | None | - | - |
| workstation | None | - | - |

**Returns**: (none)



### create_pick_list(source_name, target_doc = None, for_qty = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| source_name | None | - | - |
| target_doc | None | None | - |
| for_qty | None | None | - |

**Returns**: (none)



### get_reserved_qty_for_production(item_code: str, warehouse: str, non_completed_production_plans: list | None = None, check_production_plan: bool = False) → float

Get total reserved quantity for any item in specified warehouse

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item_code | str | - | - |
| warehouse | str | - | - |
| non_completed_production_plans | list | None | None | - |
| check_production_plan | bool | False | - |

**Returns**: `float`



### make_stock_return_entry(work_order)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| work_order | None | - | - |

**Returns**: (none)



### get_row_wise_serial_batch(work_order, purpose = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| work_order | None | - | - |
| purpose | None | None | - |

**Returns**: (none)



### get_hour_rate(workstation)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| workstation | None | - | - |

**Returns**: (none)



### update_item_quantity(source, target, source_parent)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| source | None | - | - |
| target | None | - | - |
| source_parent | None | - | - |

**Returns**: (none)



### _get_operations(bom_no, qty = 1)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| bom_no | None | - | - |
| qty | None | 1 | - |

**Returns**: (none)


