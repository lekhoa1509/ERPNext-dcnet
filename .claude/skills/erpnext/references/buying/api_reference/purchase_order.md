# API Reference: purchase_order.py

**Language**: Python

**Source**: `doctype/purchase_order/purchase_order.py`

---

## Classes

### PurchaseOrder

**Inherits from**: BuyingController

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


##### set_has_unit_price_items(self)

If permitted in settings and any item has 0 qty, the PO has unit price items.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_with_previous_doc(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_supplier(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_minimum_order_qty(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_bom_for_subcontracting_items(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_fg_item_for_subcontracting(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_schedule_dates(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_last_purchase_rate(self)

get last purchase rates for all items

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### check_on_hold_or_closed_status(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_ordered_qty(self, po_item_rows = None)

update requested qty (before ordered_qty is updated)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| po_item_rows | None | None | - |


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


##### update_status_updater(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_status_updater_if_from_pp(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_delivered_qty_in_sales_order(self)

Update delivered qty in Sales Order for drop ship

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### has_drop_ship_item(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### is_against_so(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### is_against_pp(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_received_qty_for_drop_ship_items(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_reserved_qty_for_subcontract(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_receiving_percentage(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_service_items_for_finished_goods(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### can_update_items(self) → bool

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `bool`


##### update_ordered_qty_in_so_for_removed_items(self, removed_items)

Updates ordered_qty in linked SO when item rows are removed using Update Items

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| removed_items | None | - | - |


##### auto_create_subcontracting_order(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_subcontracting_order_status(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### item_last_purchase_rate(name, conversion_rate, item_code, conversion_factor = 1.0)

get last purchase rate for an item

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| name | None | - | - |
| conversion_rate | None | - | - |
| item_code | None | - | - |
| conversion_factor | None | 1.0 | - |

**Returns**: (none)



### close_or_unclose_purchase_orders(names, status)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| names | None | - | - |
| status | None | - | - |

**Returns**: (none)



### set_missing_values(source, target)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| source | None | - | - |
| target | None | - | - |

**Returns**: (none)



### make_purchase_receipt(source_name, target_doc = None, args = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| source_name | None | - | - |
| target_doc | None | None | - |
| args | None | None | - |

**Returns**: (none)



### make_purchase_invoice(source_name, target_doc = None, args = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| source_name | None | - | - |
| target_doc | None | None | - |
| args | None | None | - |

**Returns**: (none)



### make_purchase_invoice_from_portal(purchase_order_name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| purchase_order_name | None | - | - |

**Returns**: (none)



### get_mapped_purchase_invoice(source_name, target_doc = None, ignore_permissions = False, args = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| source_name | None | - | - |
| target_doc | None | None | - |
| ignore_permissions | None | False | - |
| args | None | None | - |

**Returns**: (none)



### get_list_context(context = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| context | None | None | - |

**Returns**: (none)



### update_status(status, name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| status | None | - | - |
| name | None | - | - |

**Returns**: (none)



### make_inter_company_sales_order(source_name, target_doc = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| source_name | None | - | - |
| target_doc | None | None | - |

**Returns**: (none)



### make_subcontracting_order(source_name, target_doc = None, save = False, submit = False, notify = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| source_name | None | - | - |
| target_doc | None | None | - |
| save | None | False | - |
| submit | None | False | - |
| notify | None | False | - |

**Returns**: (none)



### is_po_fully_subcontracted(po_name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| po_name | None | - | - |

**Returns**: (none)



### get_mapped_subcontracting_order(source_name, target_doc = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| source_name | None | - | - |
| target_doc | None | None | - |

**Returns**: (none)



### is_unit_price_row(source)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| source | None | - | - |

**Returns**: (none)



### update_item(obj, target, source_parent)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| obj | None | - | - |
| target | None | - | - |
| source_parent | None | - | - |

**Returns**: (none)



### select_item(d)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| d | None | - | - |

**Returns**: (none)



### postprocess(source, target)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| source | None | - | - |
| target | None | - | - |

**Returns**: (none)



### update_item(obj, target, source_parent)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| obj | None | - | - |
| target | None | - | - |
| source_parent | None | - | - |

**Returns**: (none)



### select_item(d)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| d | None | - | - |

**Returns**: (none)



### post_process(source_doc, target_doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| source_doc | None | - | - |
| target_doc | None | - | - |

**Returns**: (none)



### get_billed_qty(po_item_name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| po_item_name | None | - | - |

**Returns**: (none)


