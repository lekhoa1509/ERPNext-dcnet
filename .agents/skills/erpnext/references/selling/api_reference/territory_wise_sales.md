# API Reference: territory_wise_sales.py

**Language**: Python

**Source**: `report/territory_wise_sales/territory_wise_sales.py`

---

## Functions

### execute(filters = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | None | None | - |

**Returns**: (none)



### get_columns()

**Returns**: (none)



### get_data(filters = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | None | None | - |

**Returns**: (none)



### get_opportunities(filters)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | None | - | - |

**Returns**: (none)



### get_quotations(opportunities)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| opportunities | None | - | - |

**Returns**: (none)



### get_sales_orders(quotations)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| quotations | None | - | - |

**Returns**: (none)



### get_sales_invoice(sales_orders)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| sales_orders | None | - | - |

**Returns**: (none)



### _get_total(doclist, amount_field = 'base_grand_total')

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doclist | None | - | - |
| amount_field | None | 'base_grand_total' | - |

**Returns**: (none)


