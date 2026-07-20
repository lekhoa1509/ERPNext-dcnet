# API Reference: fixed_asset_register.py

**Language**: Python

**Source**: `report/fixed_asset_register/fixed_asset_register.py`

---

## Functions

### execute(filters = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | None | None | - |

**Returns**: (none)



### get_data(filters)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | None | - | - |

**Returns**: (none)



### get_conditions(filters)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | None | - | - |

**Returns**: (none)



### prepare_chart_data(data, filters)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| data | None | - | - |
| filters | None | - | - |

**Returns**: (none)



### get_assets_linked_to_fb(filters)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | None | - | - |

**Returns**: (none)



### get_asset_depreciation_amount_map(filters, finance_book)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | None | - | - |
| finance_book | None | - | - |

**Returns**: (none)



### get_asset_value_adjustment_map(filters, finance_book)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | None | - | - |
| finance_book | None | - | - |

**Returns**: (none)



### get_group_by_data(group_by, conditions, assets_linked_to_fb, depreciation_amount_map, revaluation_amount_map)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| group_by | None | - | - |
| conditions | None | - | - |
| assets_linked_to_fb | None | - | - |
| depreciation_amount_map | None | - | - |
| revaluation_amount_map | None | - | - |

**Returns**: (none)



### get_purchase_receipt_supplier_map()

**Returns**: (none)



### get_purchase_invoice_supplier_map()

**Returns**: (none)



### get_columns(filters)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | None | - | - |

**Returns**: (none)


