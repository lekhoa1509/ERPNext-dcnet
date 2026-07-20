# API Reference: pick_list.py

**Language**: Python

**Source**: `doctype/pick_list/pick_list.py`

---

## Classes

### PickList

**Inherits from**: TransactionBase

#### Methods

##### __init__(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### onload(self) → None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `None`


##### validate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### before_save(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_stock_qty(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### check_serial_no_status(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_with_previous_doc(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_sales_order_percentage(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### before_submit(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_sales_order(self)

Raises an exception if the `Sales Order` has reserved stock.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_picked_items(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_submit(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_expired_batches(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### make_bundle_using_old_serial_batch_fields(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_update_after_submit(self) → None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `None`


##### on_cancel(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### delink_serial_and_batch_bundle(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_update(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### linked_serial_and_batch_bundle(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_trash(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### remove_serial_and_batch_bundle(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_serial_and_batch_bundle(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_status(self, status = None, update_modified = True)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| status | None | None | - |
| update_modified | None | True | - |


##### stock_entry_exists(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_reference_qty(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_packed_items_qty(self, packed_items)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| packed_items | None | - | - |


##### update_sales_order_item_qty(self, so_items)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| so_items | None | - | - |


##### update_sales_order_picking_status(self) → None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `None`


##### create_stock_reservation_entries(self, notify = True) → None

Creates Stock Reservation Entries for Sales Order Items against Pick List.

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| notify | None | True | - |

**Returns**: `None`


##### cancel_stock_reservation_entries(self, notify = True) → None

Cancel Stock Reservation Entries for Sales Order Items created against Pick List.

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| notify | None | True | - |

**Returns**: `None`


##### validate_picked_qty(self, data)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| data | None | - | - |


##### set_item_locations(self, save = False)

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| save | None | False | - |


##### aggregate_item_qty(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_for_qty(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### before_print(self, settings = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| settings | None | None | - |


##### group_similar_items(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_bundle_picked_qty(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_picked_items_details(self, items)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| items | None | - | - |


##### update_picked_item_from_current_pick_list(self, picked_items)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| picked_items | None | - | - |


##### _get_pick_list_items(self, items)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| items | None | - | - |


##### _get_product_bundles(self) → dict[str, str]

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `dict[str, str]`


##### _get_product_bundle_qty_map(self, bundles) → dict[str, dict[str, float]]

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| bundles | None | - | - |

**Returns**: `dict[str, dict[str, float]]`


##### _compute_picked_qty_for_bundle(self, bundle_row, bundle_items) → int

Compute how many full bundles can be created from picked items.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| bundle_row | None | - | - |
| bundle_items | None | - | - |

**Returns**: `int`


##### has_unreserved_stock(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### has_reserved_stock(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### update_pick_list_status(pick_list)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| pick_list | None | - | - |

**Returns**: (none)



### get_picked_items_qty(items, contains_packed_items = False) → list[dict]

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| items | None | - | - |
| contains_packed_items | None | False | - |

**Returns**: `list[dict]`



### validate_item_locations(pick_list)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| pick_list | None | - | - |

**Returns**: (none)



### get_items_with_location_and_quantity(item_doc, item_location_map, docstatus)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item_doc | None | - | - |
| item_location_map | None | - | - |
| docstatus | None | - | - |

**Returns**: (none)



### get_available_item_locations(item_code, from_warehouses, required_qty, company, ignore_validation = False, picked_item_details = None, consider_rejected_warehouses = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item_code | None | - | - |
| from_warehouses | None | - | - |
| required_qty | None | - | - |
| company | None | - | - |
| ignore_validation | None | False | - |
| picked_item_details | None | None | - |
| consider_rejected_warehouses | None | False | - |

**Returns**: (none)



### get_locations_based_on_required_qty(locations, required_qty)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| locations | None | - | - |
| required_qty | None | - | - |

**Returns**: (none)



### validate_picked_materials(item_code, required_qty, locations, picked_item_details = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item_code | None | - | - |
| required_qty | None | - | - |
| locations | None | - | - |
| picked_item_details | None | None | - |

**Returns**: (none)



### filter_locations_by_picked_materials(locations, picked_item_details) → list[dict]

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| locations | None | - | - |
| picked_item_details | None | - | - |

**Returns**: `list[dict]`



### get_available_item_locations_for_serial_and_batched_item(item_code, from_warehouses, required_qty, company, consider_rejected_warehouses = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item_code | None | - | - |
| from_warehouses | None | - | - |
| required_qty | None | - | - |
| company | None | - | - |
| consider_rejected_warehouses | None | False | - |

**Returns**: (none)



### get_available_item_locations_for_serialized_item(item_code, from_warehouses, company, consider_rejected_warehouses = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item_code | None | - | - |
| from_warehouses | None | - | - |
| company | None | - | - |
| consider_rejected_warehouses | None | False | - |

**Returns**: (none)



### get_available_item_locations_for_batched_item(item_code, from_warehouses, consider_rejected_warehouses = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item_code | None | - | - |
| from_warehouses | None | - | - |
| consider_rejected_warehouses | None | False | - |

**Returns**: (none)



### get_available_item_locations_for_other_item(item_code, from_warehouses, company, consider_rejected_warehouses = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item_code | None | - | - |
| from_warehouses | None | - | - |
| company | None | - | - |
| consider_rejected_warehouses | None | False | - |

**Returns**: (none)



### create_delivery_note(source_name, target_doc = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| source_name | None | - | - |
| target_doc | None | None | - |

**Returns**: (none)



### create_dn_wo_so(pick_list, delivery_note = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| pick_list | None | - | - |
| delivery_note | None | None | - |

**Returns**: (none)



### create_dn_for_pick_lists(source_name, target_doc = None, kwargs = None)

Get Items from Multiple Pick Lists and create a Delivery Note for filtered customer

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| source_name | None | - | - |
| target_doc | None | None | - |
| kwargs | None | None | - |

**Returns**: (none)



### create_dn_with_so(sales_dict, pick_list)

Create Delivery Note for each customer (based on SO) in a Pick List.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| sales_dict | None | - | - |
| pick_list | None | - | - |

**Returns**: (none)



### create_dn_from_so(pick_list, sales_order_list, delivery_note = None, kwargs = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| pick_list | None | - | - |
| sales_order_list | None | - | - |
| delivery_note | None | None | - |
| kwargs | None | None | - |

**Returns**: (none)



### map_pl_locations(pick_list, item_mapper, delivery_note, sales_order = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| pick_list | None | - | - |
| item_mapper | None | - | - |
| delivery_note | None | - | - |
| sales_order | None | None | - |

**Returns**: (none)



### add_product_bundles_to_delivery_note(pick_list: 'PickList', delivery_note, item_mapper, sales_order = None) → None

Add product bundles found in pick list to delivery note.

When mapping pick list items, the bundle item itself isn't part of the
locations. Dynamically fetch and add parent bundle item into DN.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| pick_list | 'PickList' | - | - |
| delivery_note | None | - | - |
| item_mapper | None | - | - |
| sales_order | None | None | - |

**Returns**: `None`



### create_stock_entry(pick_list)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| pick_list | None | - | - |

**Returns**: (none)



### get_pending_work_orders(doctype, txt, searchfield, start, page_length, filters, as_dict)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| txt | None | - | - |
| searchfield | None | - | - |
| start | None | - | - |
| page_length | None | - | - |
| filters | None | - | - |
| as_dict | None | - | - |

**Returns**: (none)



### get_item_details(item_code, uom = None, warehouse = None, company = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item_code | None | - | - |
| uom | None | None | - |
| warehouse | None | None | - |
| company | None | None | - |

**Returns**: (none)



### get_actual_qty(item_code, warehouse)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item_code | None | - | - |
| warehouse | None | - | - |

**Returns**: (none)



### update_delivery_note_item(source, target, delivery_note)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| source | None | - | - |
| target | None | - | - |
| delivery_note | None | - | - |

**Returns**: (none)



### get_cost_center(for_item, from_doctype, company)

Returns Cost Center for Item or Item Group

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| for_item | None | - | - |
| from_doctype | None | - | - |
| company | None | - | - |

**Returns**: (none)



### set_delivery_note_missing_values(target)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| target | None | - | - |

**Returns**: (none)



### stock_entry_exists(pick_list_name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| pick_list_name | None | - | - |

**Returns**: (none)



### update_stock_entry_based_on_work_order(pick_list, stock_entry)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| pick_list | None | - | - |
| stock_entry | None | - | - |

**Returns**: (none)



### update_stock_entry_based_on_material_request(pick_list, stock_entry)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| pick_list | None | - | - |
| stock_entry | None | - | - |

**Returns**: (none)



### update_stock_entry_items_with_no_reference(pick_list, stock_entry)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| pick_list | None | - | - |
| stock_entry | None | - | - |

**Returns**: (none)



### update_common_item_properties(item, location)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item | None | - | - |
| location | None | - | - |

**Returns**: (none)



### get_rejected_warehouses()

**Returns**: (none)



### get_pick_list_query(doctype, txt, searchfield, start, page_len, filters)

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



### select_item(d)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| d | None | - | - |

**Returns**: (none)


