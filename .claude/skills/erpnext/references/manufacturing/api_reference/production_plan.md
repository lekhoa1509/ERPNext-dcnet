# API Reference: production_plan.py

**Language**: Python

**Source**: `doctype/production_plan/production_plan.py`

---

## Classes

### ProductionPlan

**Inherits from**: Document

#### Methods

##### onload(self)

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


##### enable_auto_reserve_stock(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_material_request_type(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_sales_orders(self, sales_order = None)

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| sales_order | None | None | - |


##### set_pending_qty_in_row_without_reference(self)

Set Pending Qty in independent rows (not from SO or MR).

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### calculate_total_planned_qty(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_data(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _rename_temporary_references(self)

po_items and sub_assembly_items items are both constructed client side without saving.

Attempt to fix linkages by using temporary names to map final row names.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_open_sales_orders(self)

Pull sales orders  which are pending to deliver based on criteria selected

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### add_so_in_table(self, open_so)

Add sales orders in the table

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| open_so | None | - | - |


##### get_pending_material_requests(self)

Pull Material Requests that are pending based on criteria selected

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### add_mr_in_table(self, pending_mr)

Add Material Requests in the table

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| pending_mr | None | - | - |


##### combine_so_items(self)

**Decorators**: `@frappe.whitelist()`

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


##### get_so_mr_list(self, field, table)

Returns a list of Sales Orders or Material Requests from the respective tables

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| field | None | - | - |
| table | None | - | - |


##### get_bom_item_condition(self)

Check if Item or if its Template has a BOM.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_so_items(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_mr_items(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### add_items(self, items)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| items | None | - | - |


##### add_pp_ref(self, refs)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| refs | None | - | - |


##### calculate_total_produced_qty(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_produced_pending_qty(self, produced_qty, production_plan_item)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| produced_qty | None | - | - |
| production_plan_item | None | - | - |


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


##### update_stock_reservation(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### add_reference_to_raw_materials(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_sales_order(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_so_wise_planned_qty(sales_orders)

**Decorators**: `@staticmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| sales_orders | None | - | - |


##### update_bin_qty(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### delete_draft_work_order(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_status(self, close = None, update_bin = False)

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| close | None | None | - |
| update_bin | None | False | - |


##### update_ordered_status(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_requested_status(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_production_items(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### make_work_order(self)

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### make_work_order_for_finished_goods(self, wo_list, default_warehouses)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| wo_list | None | - | - |
| default_warehouses | None | - | - |


##### make_work_order_for_subassembly_items(self, wo_list, subcontracted_po, default_warehouses)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| wo_list | None | - | - |
| subcontracted_po | None | - | - |
| default_warehouses | None | - | - |


##### prepare_data_for_sub_assembly_items(self, row, wo_data)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| row | None | - | - |
| wo_data | None | - | - |


##### make_subcontracted_purchase_order(self, subcontracted_po, purchase_orders)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| subcontracted_po | None | - | - |
| purchase_orders | None | - | - |


##### show_list_created_message(self, doctype, doc_list = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doctype | None | - | - |
| doc_list | None | None | - |


##### create_work_order(self, item)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| item | None | - | - |


##### validate_mr_subcontracted(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### make_material_request(self)

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_sub_assembly_items(self, manufacturing_type = None)

Fetch sub assembly items and optionally combine them.

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| manufacturing_type | None | None | - |


##### set_sub_assembly_items_based_on_level(self, row, bom_data, manufacturing_type = None)

Modify bom_data, set additional details.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| row | None | - | - |
| bom_data | None | - | - |
| manufacturing_type | None | None | - |


##### set_default_supplier_for_subcontracting_order(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### combine_subassembly_items(self, sub_assembly_items_store)

Aggregate if same: Item, Warehouse, Inhouse/Outhouse Manu.g, BOM No.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| sub_assembly_items_store | None | - | - |


##### all_items_completed(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### download_raw_materials(doc, warehouses = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |
| warehouses | None | None | - |

**Returns**: (none)



### get_exploded_items(item_details, company, bom_no, include_non_stock_items, planned_qty = 1, doc = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item_details | None | - | - |
| company | None | - | - |
| bom_no | None | - | - |
| include_non_stock_items | None | - | - |
| planned_qty | None | 1 | - |
| doc | None | None | - |

**Returns**: (none)



### get_uom_conversion_factor(item_code, uom)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item_code | None | - | - |
| uom | None | - | - |

**Returns**: (none)



### get_subitems(doc, data, item_details, bom_no, company, include_non_stock_items, include_subcontracted_items, parent_qty, planned_qty = 1)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |
| data | None | - | - |
| item_details | None | - | - |
| bom_no | None | - | - |
| company | None | - | - |
| include_non_stock_items | None | - | - |
| include_subcontracted_items | None | - | - |
| parent_qty | None | - | - |
| planned_qty | None | 1 | - |

**Returns**: (none)



### get_material_request_items(doc, row, sales_order, company, ignore_existing_ordered_qty, include_safety_stock, warehouse, bin_dict, consumed_qty)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |
| row | None | - | - |
| sales_order | None | - | - |
| company | None | - | - |
| ignore_existing_ordered_qty | None | - | - |
| include_safety_stock | None | - | - |
| warehouse | None | - | - |
| bin_dict | None | - | - |
| consumed_qty | None | - | - |

**Returns**: (none)



### get_sales_orders(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: (none)



### get_bin_details(row, company, for_warehouse = None, all_warehouse = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| row | None | - | - |
| company | None | - | - |
| for_warehouse | None | None | - |
| all_warehouse | None | False | - |

**Returns**: (none)



### get_so_details(sales_order)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| sales_order | None | - | - |

**Returns**: (none)



### get_warehouse_list(warehouses)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| warehouses | None | - | - |

**Returns**: (none)



### get_items_for_material_requests(doc, warehouses = None, get_parent_warehouse_data = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |
| warehouses | None | None | - |
| get_parent_warehouse_data | None | None | - |

**Returns**: (none)



### get_materials_from_other_locations(item, warehouses, new_mr_items, company)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item | None | - | - |
| warehouses | None | - | - |
| new_mr_items | None | - | - |
| company | None | - | - |

**Returns**: (none)



### get_item_data(item_code)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item_code | None | - | - |

**Returns**: (none)



### get_sub_assembly_items(sub_assembly_items, bin_details, bom_no, bom_data, to_produce_qty, company, warehouse = None, indent = 0, skip_available_sub_assembly_item = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| sub_assembly_items | None | - | - |
| bin_details | None | - | - |
| bom_no | None | - | - |
| bom_data | None | - | - |
| to_produce_qty | None | - | - |
| company | None | - | - |
| warehouse | None | None | - |
| indent | None | 0 | - |
| skip_available_sub_assembly_item | None | False | - |

**Returns**: (none)



### set_default_warehouses(row, default_warehouses)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| row | None | - | - |
| default_warehouses | None | - | - |

**Returns**: (none)



### get_reserved_qty_for_production_plan(item_code, warehouse)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item_code | None | - | - |
| warehouse | None | - | - |

**Returns**: (none)



### get_non_completed_production_plans()

**Returns**: (none)



### get_raw_materials_of_sub_assembly_items(existing_sub_assembly_items, item_details, company, bom_no, include_non_stock_items, sub_assembly_items, planned_qty = 1)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| existing_sub_assembly_items | None | - | - |
| item_details | None | - | - |
| company | None | - | - |
| bom_no | None | - | - |
| include_non_stock_items | None | - | - |
| sub_assembly_items | None | - | - |
| planned_qty | None | 1 | - |

**Returns**: (none)



### sales_order_query(doctype = None, txt = None, searchfield = None, start = None, page_len = None, filters = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | None | - |
| txt | None | None | - |
| searchfield | None | None | - |
| start | None | None | - |
| page_len | None | None | - |
| filters | None | None | - |

**Returns**: (none)



### get_reserved_qty_for_sub_assembly(item_code, warehouse)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item_code | None | - | - |
| warehouse | None | - | - |

**Returns**: (none)



### make_stock_reservation_entries(doc, items = None, table_name = None, notify = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |
| items | None | None | - |
| table_name | None | None | - |
| notify | None | False | - |

**Returns**: (none)



### cancel_stock_reservation_entries(doc, sre_list)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |
| sre_list | None | - | - |

**Returns**: (none)



### calculate_sub_assembly_items()

**Returns**: (none)


