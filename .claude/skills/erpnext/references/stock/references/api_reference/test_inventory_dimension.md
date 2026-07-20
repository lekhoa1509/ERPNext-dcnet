# API Reference: test_inventory_dimension.py

**Language**: Python

**Source**: `doctype/inventory_dimension/test_inventory_dimension.py`

---

## Classes

### TestInventoryDimension

**Inherits from**: IntegrationTestCase

#### Methods

##### setUp(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_validate_inventory_dimension(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_delete_inventory_dimension(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_inventory_dimension(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_inventory_dimension_for_purchase_receipt_and_delivery_note(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_check_standard_dimensions(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_check_mandatory_dimensions(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_check_mandatory_depends_on_dimensions(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_for_purchase_sales_and_stock_transaction(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_inter_transfer_return_against_inventory_dimension(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_validate_negative_stock_for_inventory_dimension(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_validate_negative_stock_with_multiple_dimension(self)

**Decorators**: `@change_settings('Stock Settings', {'allow_negative_stock': 0})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### get_voucher_sl_entries(voucher_no, fields)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| voucher_no | None | - | - |
| fields | None | - | - |

**Returns**: (none)



### create_store_dimension()

**Returns**: (none)



### prepare_test_data()

**Returns**: (none)



### create_inventory_dimension()

**Returns**: (none)



### prepare_data_for_internal_transfer()

**Returns**: (none)


