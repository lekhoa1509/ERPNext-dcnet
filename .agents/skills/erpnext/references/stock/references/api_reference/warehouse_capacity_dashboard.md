# API Reference: warehouse_capacity_dashboard.py

**Language**: Python

**Source**: `dashboard/warehouse_capacity_dashboard.py`

---

## Functions

### get_data(item_code = None, warehouse = None, parent_warehouse = None, company = None, start = 0, sort_by = 'stock_capacity', sort_order = 'desc')

Return data to render the warehouse capacity dashboard.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item_code | None | None | - |
| warehouse | None | None | - |
| parent_warehouse | None | None | - |
| company | None | None | - |
| start | None | 0 | - |
| sort_by | None | 'stock_capacity' | - |
| sort_order | None | 'desc' | - |

**Returns**: (none)



### get_filters(item_code = None, warehouse = None, parent_warehouse = None, company = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item_code | None | None | - |
| warehouse | None | None | - |
| parent_warehouse | None | None | - |
| company | None | None | - |

**Returns**: (none)



### get_warehouse_filter_based_on_permissions(filters)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | None | - | - |

**Returns**: (none)



### get_warehouse_capacity_data(filters, start)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | None | - | - |
| start | None | - | - |

**Returns**: (none)


