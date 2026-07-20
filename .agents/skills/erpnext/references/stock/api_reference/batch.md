# API Reference: batch.py

**Language**: Python

**Source**: `doctype/batch/batch.py`

---

## Classes

### UnableToSelectBatchError

**Inherits from**: frappe.ValidationError



### Batch

**Inherits from**: Document

#### Methods

##### autoname(self)

Generate random ID for batch if not specified

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### onload(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### after_delete(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### item_has_batch_enabled(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### recalculate_batch_qty(self)

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_batchwise_valuation(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### before_save(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_expiry_date(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_name_from_naming_series(self)

Get a name generated for a Batch from the Batch's naming series.
:return: The string that was generated.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### get_name_from_hash()

Get a name for a Batch by generating a unique hash.
:return: The hash that was generated.

**Returns**: (none)



### batch_uses_naming_series()

Verify if the Batch is to be named using a naming series
:return: bool

**Returns**: (none)



### _get_batch_prefix()

Get the naming series prefix set in Stock Settings.

It does not do any sanity checks so make sure to use it after checking if the Batch
is set to use naming series.
:return: The naming series.

**Returns**: (none)



### _make_naming_series_key(prefix)

Make naming series key for a Batch.

Naming series key is in the format [prefix].[#####]
:param prefix: Naming series prefix gotten from Stock Settings
:return: The derived key. If no prefix is given, an empty string is returned

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| prefix | None | - | - |

**Returns**: (none)



### get_batch_naming_series()

Get naming series key for a Batch.

Naming series key is in the format [prefix].[#####]
:return: The naming series or empty string if not available

**Returns**: (none)



### get_batch_qty(batch_no = None, warehouse = None, item_code = None, creation = None, posting_datetime = None, posting_date = None, posting_time = None, ignore_voucher_nos = None, for_stock_levels = False, consider_negative_batches = False, do_not_check_future_batches = False, ignore_reserved_stock = False)

Returns batch actual qty if warehouse is passed,
        or returns dict of qty by warehouse if warehouse is None

The user must pass either batch_no or batch_no + warehouse or item_code + warehouse

:param batch_no: Optional - give qty for this batch no
:param warehouse: Optional - give qty for this warehouse
:param item_code: Optional - give qty for this item
:param for_stock_levels: True consider expired batches

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| batch_no | None | None | - |
| warehouse | None | None | - |
| item_code | None | None | - |
| creation | None | None | - |
| posting_datetime | None | None | - |
| posting_date | None | None | - |
| posting_time | None | None | - |
| ignore_voucher_nos | None | None | - |
| for_stock_levels | None | False | - |
| consider_negative_batches | None | False | - |
| do_not_check_future_batches | None | False | - |
| ignore_reserved_stock | None | False | - |

**Returns**: (none)



### get_batches_by_oldest(item_code, warehouse)

Returns the oldest batch and qty for the given item_code and warehouse

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item_code | None | - | - |
| warehouse | None | - | - |

**Returns**: (none)



### split_batch(batch_no: str, item_code: str, warehouse: str, qty: float, new_batch_id: str | None = None)

Split the batch into a new batch

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| batch_no | str | - | - |
| item_code | str | - | - |
| warehouse | str | - | - |
| qty | float | - | - |
| new_batch_id | str | None | None | - |

**Returns**: (none)



### make_batch_bundle(item_code: str, warehouse: str, batches: dict[str, float], company: str, type_of_transaction: str, qty: float)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item_code | str | - | - |
| warehouse | str | - | - |
| batches | dict[str, float] | - | - |
| company | str | - | - |
| type_of_transaction | str | - | - |
| qty | float | - | - |

**Returns**: (none)



### get_batches(item_code, warehouse, qty = 1, throw = False, serial_no = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item_code | None | - | - |
| warehouse | None | - | - |
| qty | None | 1 | - |
| throw | None | False | - |
| serial_no | None | None | - |

**Returns**: (none)



### validate_serial_no_with_batch(serial_nos, item_code)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| serial_nos | None | - | - |
| item_code | None | - | - |

**Returns**: (none)



### make_batch(kwargs)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| kwargs | None | - | - |

**Returns**: (none)



### get_pos_reserved_batch_qty(filters)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | None | - | - |

**Returns**: (none)



### get_available_batches(kwargs)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| kwargs | None | - | - |

**Returns**: (none)



### get_batch_no(bundle_id)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| bundle_id | None | - | - |

**Returns**: (none)


