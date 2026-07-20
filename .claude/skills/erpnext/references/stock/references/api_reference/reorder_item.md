# API Reference: reorder_item.py

**Language**: Python

**Source**: `reorder_item.py`

---

## Functions

### reorder_item()

Reorder item if stock reaches reorder level

**Returns**: (none)



### _reorder_item()

**Returns**: (none)



### get_items_for_reorder() → dict[str, list]

**Returns**: `dict[str, list]`



### get_reorder_levels_for_variants(itemwise_reorder)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| itemwise_reorder | None | - | - |

**Returns**: (none)



### get_item_warehouse_projected_qty(items_to_consider)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| items_to_consider | None | - | - |

**Returns**: (none)



### create_material_request(material_requests)

Create indent on reaching reorder level

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| material_requests | None | - | - |

**Returns**: (none)



### send_email_notification(company_wise_mr)

Notify user about auto creation of indent

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| company_wise_mr | None | - | - |

**Returns**: (none)



### get_email_list(company)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| company | None | - | - |

**Returns**: (none)



### get_comapny_wise_users(company)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| company | None | - | - |

**Returns**: (none)



### notify_errors(exceptions_list)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| exceptions_list | None | - | - |

**Returns**: (none)



### add_to_material_request()

**Returns**: (none)



### _log_exception(mr)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| mr | None | - | - |

**Returns**: (none)


