# API Reference: material_request.py

**Language**: Python

**Source**: `doctype/material_request/material_request.py`

---

## Classes

### MaterialRequest

**Inherits from**: BuyingController

#### Methods

##### __init__(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### check_if_already_pulled(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_qty_against_so(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_pp_qty(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### before_update_after_submit(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_material_request_type(self)

Validate fields in accordance with selected type

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_title(self)

Set title as comma separated list of items

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_submit(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### before_save(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### before_submit(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### before_cancel(self)

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


##### status_can_change(self, status)

validates that `status` is acceptable for the present controller status
and throws an Exception if otherwise.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| status | None | - | - |


##### on_cancel(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_mr_items_ordered_qty(self, mr_items)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| mr_items | None | - | - |


##### update_completed_qty(self, mr_items = None, update_modified = True)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| mr_items | None | None | - |
| update_modified | None | True | - |


##### update_requested_qty(self, mr_item_rows = None)

update requested qty (before ordered_qty is updated)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| mr_item_rows | None | None | - |


##### update_requested_qty_in_production_plan(self, cancel = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| cancel | None | False | - |




## Functions

### update_completed_and_requested_qty(stock_entry, method)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| stock_entry | None | - | - |
| method | None | - | - |

**Returns**: (none)



### set_missing_values(source, target_doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| source | None | - | - |
| target_doc | None | - | - |

**Returns**: (none)



### update_item(obj, target, source_parent)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| obj | None | - | - |
| target | None | - | - |
| source_parent | None | - | - |

**Returns**: (none)



### get_list_context(context = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| context | None | None | - |

**Returns**: (none)



### update_status(name, status)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| name | None | - | - |
| status | None | - | - |

**Returns**: (none)



### make_purchase_order(source_name, target_doc = None, args = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| source_name | None | - | - |
| target_doc | None | None | - |
| args | None | None | - |

**Returns**: (none)



### make_request_for_quotation(source_name, target_doc = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| source_name | None | - | - |
| target_doc | None | None | - |

**Returns**: (none)



### make_purchase_order_based_on_supplier(source_name, target_doc = None, args = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| source_name | None | - | - |
| target_doc | None | None | - |
| args | None | None | - |

**Returns**: (none)



### get_items_based_on_default_supplier(supplier)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| supplier | None | - | - |

**Returns**: (none)



### get_material_requests_based_on_supplier(doctype, txt, searchfield, start, page_len, filters)

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



### get_default_supplier_query(doctype, txt, searchfield, start, page_len, filters)

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



### make_supplier_quotation(source_name, target_doc = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| source_name | None | - | - |
| target_doc | None | None | - |

**Returns**: (none)



### make_stock_entry(source_name, target_doc = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| source_name | None | - | - |
| target_doc | None | None | - |

**Returns**: (none)



### raise_work_orders(material_request, company)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| material_request | None | - | - |
| company | None | - | - |

**Returns**: (none)



### create_pick_list(source_name, target_doc = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| source_name | None | - | - |
| target_doc | None | None | - |

**Returns**: (none)



### make_in_transit_stock_entry(source_name, in_transit_warehouse)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| source_name | None | - | - |
| in_transit_warehouse | None | - | - |

**Returns**: (none)



### postprocess(source, target_doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| source | None | - | - |
| target_doc | None | - | - |

**Returns**: (none)



### select_item(d)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| d | None | - | - |

**Returns**: (none)



### generate_field_map()

**Returns**: (none)



### postprocess(source, target_doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| source | None | - | - |
| target_doc | None | - | - |

**Returns**: (none)



### postprocess(source, target_doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| source | None | - | - |
| target_doc | None | - | - |

**Returns**: (none)



### update_item(obj, target, source_parent)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| obj | None | - | - |
| target | None | - | - |
| source_parent | None | - | - |

**Returns**: (none)



### set_missing_values(source, target)

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


