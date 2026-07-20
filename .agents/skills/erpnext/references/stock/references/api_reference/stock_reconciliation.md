# API Reference: stock_reconciliation.py

**Language**: Python

**Source**: `doctype/stock_reconciliation/stock_reconciliation.py`

---

## Classes

### OpeningEntryAccountError

**Inherits from**: frappe.ValidationError



### EmptyStockReconciliationItemsError

**Inherits from**: frappe.ValidationError



### StockReconciliation

**Inherits from**: StockController

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


##### on_update(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_inventory_dimension(self)

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


##### make_bundle_for_current_qty(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_current_serial_and_batch_bundle(self, voucher_detail_no = None, save = False) → None

Set Serial and Batch Bundle for each item

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| voucher_detail_no | None | None | - |
| save | None | False | - |

**Returns**: `None`


##### get_bundle_for_specific_serial_batch(self, row) → str

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| row | None | - | - |

**Returns**: `str`


##### has_change_in_serial_batch(self, row) → bool

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| row | None | - | - |

**Returns**: `bool`


##### set_new_serial_and_batch_bundle(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_existing_serial_and_batch_bundle(self, item)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| item | None | - | - |


##### remove_items_with_no_change(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### calculate_difference_amount(self, item, item_dict)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| item | None | - | - |
| item_dict | None | - | - |


##### validate_data(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### change_row_indexes(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_item(self, item_code, row)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| item_code | None | - | - |
| row | None | - | - |


##### validate_reserved_stock(self) → None

Raises an exception if there is any reserved stock for the items in the Stock Reconciliation.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `None`


##### update_stock_ledger(self, allow_negative_stock = False)

find difference between current and expected entries
and create stock ledger entries based on the difference

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| allow_negative_stock | None | False | - |


##### make_adjustment_entry(self, row, sl_entries)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| row | None | - | - |
| sl_entries | None | - | - |


##### get_sle_for_serialized_items(self, row, sl_entries)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| row | None | - | - |
| sl_entries | None | - | - |


##### update_valuation_rate_for_serial_no(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_valuation_rate_for_serial_nos(self, row, serial_nos)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| row | None | - | - |
| serial_nos | None | - | - |


##### get_sle_for_items(self, row, serial_nos = None, current_bundle = True)

Insert Stock Ledger Entries

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| row | None | - | - |
| serial_nos | None | None | - |
| current_bundle | None | True | - |


##### make_sle_on_cancel(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### merge_similar_item_serial_nos(self, sl_entries)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| sl_entries | None | - | - |


##### get_gl_entries(self, inventory_account_map = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| inventory_account_map | None | None | - |


##### validate_expense_account(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_zero_value_for_customer_provided_items(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_total_qty_and_amount(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_items_for(self, warehouse)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| warehouse | None | - | - |


##### submit(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### cancel(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### recalculate_current_qty(self, voucher_detail_no, sle_creation, add_new_sle = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| voucher_detail_no | None | - | - |
| sle_creation | None | - | - |
| add_new_sle | None | False | - |


##### add_missing_stock_ledger_entry(self, row, voucher_detail_no, sle_creation)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| row | None | - | - |
| voucher_detail_no | None | - | - |
| sle_creation | None | - | - |


##### has_negative_stock_allowed(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_current_qty_for_serial_or_batch(self, row, sle_creation)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| row | None | - | - |
| sle_creation | None | - | - |


##### get_current_qty_for_serial_nos(self, doc, sle_creation)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doc | None | - | - |
| sle_creation | None | - | - |


##### get_current_qty_for_batch_nos(self, doc, sle_creation)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doc | None | - | - |
| sle_creation | None | - | - |




## Functions

### get_batch_qty_for_stock_reco(item_code, warehouse, batch_no, posting_date, posting_time, voucher_no, sle_creation)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item_code | None | - | - |
| warehouse | None | - | - |
| batch_no | None | - | - |
| posting_date | None | - | - |
| posting_time | None | - | - |
| voucher_no | None | - | - |
| sle_creation | None | - | - |

**Returns**: (none)



### get_items(warehouse, posting_date, posting_time, company, item_code = None, ignore_empty_stock = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| warehouse | None | - | - |
| posting_date | None | - | - |
| posting_time | None | - | - |
| company | None | - | - |
| item_code | None | None | - |
| ignore_empty_stock | None | False | - |

**Returns**: (none)



### get_item_and_warehouses(item_code, warehouse)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item_code | None | - | - |
| warehouse | None | - | - |

**Returns**: (none)



### get_items_for_stock_reco(warehouse, company)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| warehouse | None | - | - |
| company | None | - | - |

**Returns**: (none)



### get_item_data(row, qty, valuation_rate, serial_no = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| row | None | - | - |
| qty | None | - | - |
| valuation_rate | None | - | - |
| serial_no | None | None | - |

**Returns**: (none)



### get_itemwise_batch(warehouse, posting_date, company, item_code = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| warehouse | None | - | - |
| posting_date | None | - | - |
| company | None | - | - |
| item_code | None | None | - |

**Returns**: (none)



### get_stock_balance_for(item_code: str, warehouse: str, posting_date, posting_time, batch_no: str | None = None, with_valuation_rate: bool = True, inventory_dimensions_dict = None, row = None, company = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item_code | str | - | - |
| warehouse | str | - | - |
| posting_date | None | - | - |
| posting_time | None | - | - |
| batch_no | str | None | None | - |
| with_valuation_rate | bool | True | - |
| inventory_dimensions_dict | None | None | - |
| row | None | None | - |
| company | None | None | - |

**Returns**: (none)



### get_difference_account(purpose, company)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| purpose | None | - | - |
| company | None | - | - |

**Returns**: (none)



### _changed(item)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item | None | - | - |

**Returns**: (none)



### _get_msg(row_num, msg)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| row_num | None | - | - |
| msg | None | - | - |

**Returns**: (none)



### validate_serial_batch_items()

**Returns**: (none)


