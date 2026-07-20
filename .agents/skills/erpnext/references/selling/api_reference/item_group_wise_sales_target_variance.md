# API Reference: item_group_wise_sales_target_variance.py

**Language**: Python

**Source**: `report/sales_partner_target_variance_based_on_item_group/item_group_wise_sales_target_variance.py`

---

## Functions

### get_data_column(filters, partner_doctype)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | None | - | - |
| partner_doctype | None | - | - |

**Returns**: (none)



### get_data(filters, period_list, partner_doctype)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | None | - | - |
| period_list | None | - | - |
| partner_doctype | None | - | - |

**Returns**: (none)



### get_columns(filters, period_list, partner_doctype)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | None | - | - |
| period_list | None | - | - |
| partner_doctype | None | - | - |

**Returns**: (none)



### prepare_data(filters, sales_users_data, sales_user_wise_item_groups, actual_data, date_field, period_list, sales_field)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | None | - | - |
| sales_users_data | None | - | - |
| sales_user_wise_item_groups | None | - | - |
| actual_data | None | - | - |
| date_field | None | - | - |
| period_list | None | - | - |
| sales_field | None | - | - |

**Returns**: (none)



### get_item_group_parent_child_map()

Returns a dict of all item group parents and leaf children associated with them.

**Returns**: (none)



### get_actual_data(filters, sales_users_or_territory_data, date_field, sales_field)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | None | - | - |
| sales_users_or_territory_data | None | - | - |
| date_field | None | - | - |
| sales_field | None | - | - |

**Returns**: (none)



### get_parents_data(filters, partner_doctype)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | None | - | - |
| partner_doctype | None | - | - |

**Returns**: (none)


