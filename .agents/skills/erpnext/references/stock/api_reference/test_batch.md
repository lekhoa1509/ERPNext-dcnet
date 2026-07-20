# API Reference: test_batch.py

**Language**: Python

**Source**: `doctype/batch/test_batch.py`

---

## Classes

### TestBatch

**Inherits from**: IntegrationTestCase

#### Methods

##### test_item_has_batch_enabled(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### make_batch_item(cls, item_name = None)

**Decorators**: `@classmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| cls | None | - | - |
| item_name | None | None | - |


##### test_purchase_receipt(self, batch_qty = 100)

Test automated batch creation from Purchase Receipt

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| batch_qty | None | 100 | - |


##### test_batch_stock_levels(self, batch_qty = 100)

Test automated batch creation from Purchase Receipt

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| batch_qty | None | 100 | - |


##### test_stock_entry_incoming(self)

Test batch creation via Stock Entry (Work Order)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_delivery_note(self)

Test automatic batch selection for outgoing items

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_batch_negative_stock_error(self)

Test automatic batch selection for outgoing items

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_stock_entry_outgoing(self)

Test automatic batch selection for outgoing stock entry

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_batch_split(self)

Test batch splitting

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_get_batch_qty(self)

Test getting batch quantities by batch_numbers, item_code or warehouse

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_ignore_reserved_qty(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_total_batch_qty(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### make_new_batch_and_entry(cls, item_name, batch_name, warehouse)

Make a new stock entry for given target warehouse and batch name of item

**Decorators**: `@classmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| cls | None | - | - |
| item_name | None | - | - |
| batch_name | None | - | - |
| warehouse | None | - | - |


##### test_batch_name_with_naming_series(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### make_new_batch(self, item_name = None, batch_id = None, do_not_insert = 0)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| item_name | None | None | - |
| batch_id | None | None | - |
| do_not_insert | None | 0 | - |


##### test_batch_wise_item_price(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_basic_batch_wise_valuation(self, batch_qty = 100)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| batch_qty | None | 100 | - |


##### test_update_batch_properties(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_autocreation_of_batches(self)

Test if auto created Serial No excludes existing serial numbers

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### create_batch(item_code, rate, create_item_price_for_batch)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item_code | None | - | - |
| rate | None | - | - |
| create_item_price_for_batch | None | - | - |

**Returns**: (none)



### create_price_list_for_batch(item_code, batch, rate)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item_code | None | - | - |
| batch | None | - | - |
| rate | None | - | - |

**Returns**: (none)



### make_new_batch()

**Returns**: (none)


