# API Reference: sales_order.py

**Language**: Python

**Source**: `doctype/sales_order/sales_order.py`

---

## Classes

### WarehouseRequired

**Inherits from**: frappe.ValidationError



### SalesOrder

**Inherits from**: SellingController

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


##### can_update_items(self) → bool

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `bool`


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


##### validate_fg_item_for_subcontracting(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### enable_auto_reserve_stock(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_has_unit_price_items(self)

If permitted in settings and any item has 0 qty, the SO has unit price items.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_po(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_for_items(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### product_bundle_has_stock_item(self, product_bundle)

Returns true if product bundle has stock item

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| product_bundle | None | - | - |


##### validate_sales_mntc_quotation(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_delivery_date(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_proj_cust(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_warehouse(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_with_previous_doc(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_enquiry_status(self, prevdoc, flag)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| prevdoc | None | - | - |
| flag | None | - | - |


##### update_prevdoc_status(self, flag = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| flag | None | None | - |


##### validate_drop_ship(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_submit(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### delete_removed_delivery_schedule_items(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_cancel(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_project(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### check_credit_limit(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### check_nextdoc_docstatus(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### check_modified_date(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_status(self, status)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| status | None | - | - |


##### update_subcontracting_order_status(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_reserved_qty(self, so_item_rows = None)

update requested qty (before ordered_qty is updated)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| so_item_rows | None | None | - |


##### on_update_after_submit(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### before_update_after_submit(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_supplier_after_submit(self)

Check that supplier is the same after submit if PO is already made

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_delivery_status(self)

Update delivery status from Purchase Order for drop shipping

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_picking_status(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_indicator(self)

Set indicator for portal

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_recurring(self, reference_doc, auto_repeat_doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| reference_doc | None | - | - |
| auto_repeat_doc | None | - | - |


##### validate_serial_no_based_delivery(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_reserved_stock(self)

Clean reserved stock flag for non-stock Item

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### has_unreserved_stock(self) → bool

Returns True if there is any unreserved item in the Sales Order.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `bool`


##### create_stock_reservation_entries(self, items_details: list[dict] | None = None, from_voucher_type: Literal['Pick List', 'Purchase Receipt'] = None, notify = True) → None

Creates Stock Reservation Entries for Sales Order Items.

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| items_details | list[dict] | None | None | - |
| from_voucher_type | Literal['Pick List', 'Purchase Receipt'] | None | - |
| notify | None | True | - |

**Returns**: `None`


##### cancel_stock_reservation_entries(self, sre_list = None, notify = True) → None

Cancel Stock Reservation Entries for Sales Order Items.

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| sre_list | None | None | - |
| notify | None | True | - |

**Returns**: `None`


##### set_missing_values(self, for_validate = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| for_validate | None | False | - |


##### get_delivery_schedule(self, sales_order_item)

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| sales_order_item | None | - | - |


##### create_delivery_schedule(self, child_row, schedules)

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| child_row | None | - | - |
| schedules | None | - | - |


##### update_delivery_date_based_on_schedule(self, child_row, first_delivery_date)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| child_row | None | - | - |
| first_delivery_date | None | - | - |


##### delete_delivery_schedule_items(self, sales_order_item = None, ignore_names = None)

Delete delivery schedule items.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| sales_order_item | None | None | - |
| ignore_names | None | None | - |




## Functions

### get_unreserved_qty(item: object, reserved_qty_details: dict) → float

Returns the unreserved quantity for the Sales Order Item.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item | object | - | - |
| reserved_qty_details | dict | - | - |

**Returns**: `float`



### get_list_context(context = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| context | None | None | - |

**Returns**: (none)



### is_enable_cutoff_date_on_bulk_delivery_note_creation()

**Returns**: (none)



### close_or_unclose_sales_orders(names, status)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| names | None | - | - |
| status | None | - | - |

**Returns**: (none)



### get_requested_item_qty(sales_order)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| sales_order | None | - | - |

**Returns**: (none)



### make_material_request(source_name, target_doc = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| source_name | None | - | - |
| target_doc | None | None | - |

**Returns**: (none)



### make_project(source_name, target_doc = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| source_name | None | - | - |
| target_doc | None | None | - |

**Returns**: (none)



### make_delivery_note(source_name, target_doc = None, kwargs = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| source_name | None | - | - |
| target_doc | None | None | - |
| kwargs | None | None | - |

**Returns**: (none)



### make_sales_invoice(source_name, target_doc = None, ignore_permissions = False, args = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| source_name | None | - | - |
| target_doc | None | None | - |
| ignore_permissions | None | False | - |
| args | None | None | - |

**Returns**: (none)



### make_maintenance_schedule(source_name, target_doc = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| source_name | None | - | - |
| target_doc | None | None | - |

**Returns**: (none)



### make_maintenance_visit(source_name, target_doc = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| source_name | None | - | - |
| target_doc | None | None | - |

**Returns**: (none)



### get_events(start, end, filters = None)

Returns events for Gantt / Calendar view rendering.

:param start: Start date-time.
:param end: End date-time.
:param filters: Filters (JSON).

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| start | None | - | - |
| end | None | - | - |
| filters | None | None | - |

**Returns**: (none)



### make_purchase_order(source_name, selected_items = None, target_doc = None)

Creates Purchase Order for each Supplier. Returns a list of doc objects.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| source_name | None | - | - |
| selected_items | None | None | - |
| target_doc | None | None | - |

**Returns**: (none)



### set_delivery_date(items, sales_order)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| items | None | - | - |
| sales_order | None | - | - |

**Returns**: (none)



### is_product_bundle(item_code)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item_code | None | - | - |

**Returns**: (none)



### make_work_orders(items, sales_order, company, project = None)

Make Work Orders against the given Sales Order for the given `items`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| items | None | - | - |
| sales_order | None | - | - |
| company | None | - | - |
| project | None | None | - |

**Returns**: (none)



### update_status(status, name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| status | None | - | - |
| name | None | - | - |

**Returns**: (none)



### make_raw_material_request(items, company, sales_order, project = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| items | None | - | - |
| company | None | - | - |
| sales_order | None | - | - |
| project | None | None | - |

**Returns**: (none)



### make_inter_company_purchase_order(source_name, target_doc = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| source_name | None | - | - |
| target_doc | None | None | - |

**Returns**: (none)



### create_pick_list(source_name, target_doc = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| source_name | None | - | - |
| target_doc | None | None | - |

**Returns**: (none)



### update_produced_qty_in_so_item(sales_order, sales_order_item)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| sales_order | None | - | - |
| sales_order_item | None | - | - |

**Returns**: (none)



### get_work_order_items(sales_order, for_raw_material_request = 0)

Returns items with BOM that already do not have a linked work order

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| sales_order | None | - | - |
| for_raw_material_request | None | 0 | - |

**Returns**: (none)



### get_stock_reservation_status()

**Returns**: (none)



### make_subcontracting_inward_order(source_name, target_doc = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| source_name | None | - | - |
| target_doc | None | None | - |

**Returns**: (none)



### is_so_fully_subcontracted(so_name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| so_name | None | - | - |

**Returns**: (none)



### get_mapped_subcontracting_inward_order(source_name, target_doc = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| source_name | None | - | - |
| target_doc | None | None | - |

**Returns**: (none)



### postprocess(source, target)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| source | None | - | - |
| target | None | - | - |

**Returns**: (none)



### get_remaining_qty(so_item)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| so_item | None | - | - |

**Returns**: (none)



### get_remaining_packed_item_qty(so_item)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| so_item | None | - | - |

**Returns**: (none)



### update_item(source, target, source_parent)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| source | None | - | - |
| target | None | - | - |
| source_parent | None | - | - |

**Returns**: (none)



### postprocess(source, doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| source | None | - | - |
| doc | None | - | - |

**Returns**: (none)



### is_unit_price_row(source)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| source | None | - | - |

**Returns**: (none)



### select_item(d)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| d | None | - | - |

**Returns**: (none)



### set_missing_values(source, target)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| source | None | - | - |
| target | None | - | - |

**Returns**: (none)



### condition(doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |

**Returns**: (none)



### update_item(source, target, source_parent)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| source | None | - | - |
| target | None | - | - |
| source_parent | None | - | - |

**Returns**: (none)



### is_unit_price_row(source)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| source | None | - | - |

**Returns**: (none)



### postprocess(source, target)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| source | None | - | - |
| target | None | - | - |

**Returns**: (none)



### set_missing_values(source, target)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| source | None | - | - |
| target | None | - | - |

**Returns**: (none)



### update_item(source, target, source_parent)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| source | None | - | - |
| target | None | - | - |
| source_parent | None | - | - |

**Returns**: (none)



### select_item(d)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| d | None | - | - |

**Returns**: (none)



### add_self_rm(doclist)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doclist | None | - | - |

**Returns**: (none)



### set_missing_values(source, target)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| source | None | - | - |
| target | None | - | - |

**Returns**: (none)



### update_item(source, target, source_parent)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| source | None | - | - |
| target | None | - | - |
| source_parent | None | - | - |

**Returns**: (none)



### update_item_for_packed_item(source, target, _)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| source | None | - | - |
| target | None | - | - |
| _ | None | - | - |

**Returns**: (none)



### filter_items(item, supplier)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item | None | - | - |
| supplier | None | - | - |

**Returns**: (none)



### validate_sales_order()

**Returns**: (none)



### update_item_quantity(source, target, source_parent) → None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| source | None | - | - |
| target | None | - | - |
| source_parent | None | - | - |

**Returns**: `None`



### update_packed_item_qty(source, target, source_parent) → None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| source | None | - | - |
| target | None | - | - |
| source_parent | None | - | - |

**Returns**: `None`



### should_pick_order_item(item) → bool

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item | None | - | - |

**Returns**: `bool`



### post_process(source_doc, target_doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| source_doc | None | - | - |
| target_doc | None | - | - |

**Returns**: (none)



### _valid_for_reserve(item_code, warehouse)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item_code | None | - | - |
| warehouse | None | - | - |

**Returns**: (none)



### _get_delivery_date(ref_doc_delivery_date, red_doc_transaction_date, transaction_date)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| ref_doc_delivery_date | None | - | - |
| red_doc_transaction_date | None | - | - |
| transaction_date | None | - | - |

**Returns**: (none)



### get_billed_qty(so_item_name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| so_item_name | None | - | - |

**Returns**: (none)



### update_dn_item(source, target, source_parent)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| source | None | - | - |
| target | None | - | - |
| source_parent | None | - | - |

**Returns**: (none)


