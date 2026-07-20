# API Reference: pos_invoice.py

**Language**: Python

**Source**: `doctype/pos_invoice/pos_invoice.py`

---

## Classes

### ProductBundleStockValidationError

**Inherits from**: frappe.ValidationError



### POSInvoice

**Inherits from**: SalesInvoice

#### Methods

##### __init__(self)

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


##### on_submit(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### before_cancel(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_cancel(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### clear_unallocated_mode_of_payments(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### create_and_add_consolidated_sales_invoice(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### create_return_sales_invoice(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### delink_serial_and_batch_bundle(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### submit_serial_batch_bundle(self, table_name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| table_name | None | - | - |


##### check_phone_payments(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_stock_availablility(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_is_pos_using_sales_invoice(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_serialised_or_batched_item(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_return_items_qty(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_mode_of_payment(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_change_account(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_change_amount(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_payment_amount(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_company_with_pos_company(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_outstanding_amount(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_loyalty_transaction(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_status(self, update = False, status = None, update_modified = True)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| update | None | False | - |
| status | None | None | - |
| update_modified | None | True | - |


##### set_pos_fields(self, for_validate = False)

Set retail related fields from POS Profiles

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| for_validate | None | False | - |


##### set_missing_values(self, for_validate = False)

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| for_validate | None | False | - |


##### reset_mode_of_payments(self)

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### create_payment_request(self)

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_new_payment_request(self, mop)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| mop | None | - | - |


##### get_existing_payment_request(self, pay)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| pay | None | - | - |


##### update_payments(self, payments)

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| payments | None | - | - |




## Functions

### get_stock_availability(item_code, warehouse)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item_code | None | - | - |
| warehouse | None | - | - |

**Returns**: (none)



### get_product_bundle_stock_availability(item_code, warehouse, item_qty)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item_code | None | - | - |
| warehouse | None | - | - |
| item_qty | None | - | - |

**Returns**: (none)



### get_bundle_availability(bundle_item_code, warehouse)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| bundle_item_code | None | - | - |
| warehouse | None | - | - |

**Returns**: (none)



### get_bin_qty(item_code, warehouse)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item_code | None | - | - |
| warehouse | None | - | - |

**Returns**: (none)



### get_pos_reserved_qty(item_code, warehouse)

Calculate total quantity reserved for the given item and warehouse.

Includes:
- Direct sales of the item in submitted POS Invoices
- Sales of the item as a component of a Product Bundle

Excludes consolidated invoices (already merged into Sales Invoices via
POS Closing Entry). Used to reflect near real-time availability in the
POS UI and to prevent overselling while multiple sessions may be active.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item_code | None | - | - |
| warehouse | None | - | - |

**Returns**: (none)



### get_pos_reserved_qty_from_table(child_table, item_code, warehouse)

Get the total reserved quantity for a given item in POS Invoices
from a specific child table.

Args:
  child_table (str): Name of the child table to query
                (e.g., "POS Invoice Item", "Packed Item").
  item_code (str): The Item Code to filter by.
  warehouse (str): The Warehouse to filter by.

Returns:
  float: The total reserved quantity for the item in the given
                warehouse from submitted, unconsolidated POS Invoices.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| child_table | None | - | - |
| item_code | None | - | - |
| warehouse | None | - | - |

**Returns**: (none)



### make_sales_return(source_name, target_doc = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| source_name | None | - | - |
| target_doc | None | None | - |

**Returns**: (none)



### make_merge_log(invoices)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| invoices | None | - | - |

**Returns**: (none)



### add_return_modes(doc, pos_profile)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |
| pos_profile | None | - | - |

**Returns**: (none)



### item_query(doctype, txt, searchfield, start, page_len, filters, as_dict = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| txt | None | - | - |
| searchfield | None | - | - |
| start | None | - | - |
| page_len | None | - | - |
| filters | None | - | - |
| as_dict | None | False | - |

**Returns**: (none)



### get_item_group(pos_profile)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| pos_profile | None | - | - |

**Returns**: (none)



### create_payments_on_invoice(doc, idx, payment_details)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |
| idx | None | - | - |
| payment_details | None | - | - |

**Returns**: (none)



### append_payment(payment_mode)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| payment_mode | None | - | - |

**Returns**: (none)


