# API Reference: quotation.py

**Language**: Python

**Source**: `doctype/quotation/quotation.py`

---

## Classes

### Quotation

**Inherits from**: SellingController

#### Methods

##### set_indicator(self)

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


##### before_submit(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_valid_till(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_has_alternative_item(self)

Mark 'Has Alternative Item' for rows.

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


##### get_ordered_status(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_valid_items(self)

Filters out items in an alternatives set that were not ordered.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### is_fully_ordered(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### is_partially_ordered(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_lead(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_customer_name(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_opportunity(self, status)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| status | None | - | - |


##### update_opportunity_status(self, status, opportunity = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| status | None | - | - |
| opportunity | None | None | - |


##### declare_enquiry_lost(self, lost_reasons_list, competitors, detailed_reason = None)

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| lost_reasons_list | None | - | - |
| competitors | None | - | - |
| detailed_reason | None | None | - |


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


##### print_other_charges(self, docname)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| docname | None | - | - |


##### on_recurring(self, reference_doc, auto_repeat_doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| reference_doc | None | - | - |
| auto_repeat_doc | None | - | - |


##### get_rows_with_alternatives(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### get_list_context(context = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| context | None | None | - |

**Returns**: (none)



### make_sales_order(source_name: str, target_doc = None, args = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| source_name | str | - | - |
| target_doc | None | None | - |
| args | None | None | - |

**Returns**: (none)



### _make_sales_order(source_name, target_doc = None, ignore_permissions = False, args = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| source_name | None | - | - |
| target_doc | None | None | - |
| ignore_permissions | None | False | - |
| args | None | None | - |

**Returns**: (none)



### set_expired_status()

**Returns**: (none)



### make_sales_invoice(source_name, target_doc = None, args = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| source_name | None | - | - |
| target_doc | None | None | - |
| args | None | None | - |

**Returns**: (none)



### _make_sales_invoice(source_name, target_doc = None, ignore_permissions = False, args = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| source_name | None | - | - |
| target_doc | None | None | - |
| ignore_permissions | None | False | - |
| args | None | None | - |

**Returns**: (none)



### _make_customer(source_name, ignore_permissions = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| source_name | None | - | - |
| ignore_permissions | None | False | - |

**Returns**: (none)



### create_customer_from_lead(lead_name, ignore_permissions = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| lead_name | None | - | - |
| ignore_permissions | None | False | - |

**Returns**: (none)



### create_customer_from_prospect(prospect_name, ignore_permissions = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| prospect_name | None | - | - |
| ignore_permissions | None | False | - |

**Returns**: (none)



### handle_mandatory_error(e, customer, lead_name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| e | None | - | - |
| customer | None | - | - |
| lead_name | None | - | - |

**Returns**: (none)



### get_ordered_items(quotation: str)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| quotation | str | - | - |

**Returns**: (none)



### is_unit_price_row(source) → bool

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| source | None | - | - |

**Returns**: `bool`



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



### can_map_row(item) → bool

Row mapping from Quotation to Sales order:
1. If no selections, map all non-alternative rows (that sum up to the grand total)
2. If selections: Is Alternative Item/Has Alternative Item: Map if selected and adequate qty
3. If no selections: Simple row: Map if adequate qty

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item | None | - | - |

**Returns**: `bool`



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



### is_in_sales_order(row)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| row | None | - | - |

**Returns**: (none)



### can_map(row) → bool

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| row | None | - | - |

**Returns**: `bool`


