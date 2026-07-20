# API Reference: cogs_by_item_group.py

**Language**: Python

**Source**: `report/cogs_by_item_group/cogs_by_item_group.py`

---

## Functions

### execute(filters: Filters) → tuple[Columns, Data]

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | Filters | - | - |

**Returns**: `tuple[Columns, Data]`



### update_filters_with_account(filters: Filters) → None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | Filters | - | - |

**Returns**: `None`



### validate_filters(filters: Filters) → None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | Filters | - | - |

**Returns**: `None`



### get_columns() → Columns

**Returns**: `Columns`



### get_data(filters: Filters) → Data

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | Filters | - | - |

**Returns**: `Data`



### get_filtered_entries(filters: Filters) → FilteredEntries

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | Filters | - | - |

**Returns**: `FilteredEntries`



### get_stock_value_difference_list(filtered_entries: FilteredEntries) → SVDList

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filtered_entries | FilteredEntries | - | - |

**Returns**: `SVDList`



### get_leveled_dict() → OrderedDict

**Returns**: `OrderedDict`



### assign_self_values(leveled_dict: OrderedDict, svd_list: SVDList) → None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| leveled_dict | OrderedDict | - | - |
| svd_list | SVDList | - | - |

**Returns**: `None`



### assign_agg_values(leveled_dict: OrderedDict) → None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| leveled_dict | OrderedDict | - | - |

**Returns**: `None`



### get_row(name: str, value: float, is_bold: int, indent: int) → Row

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| name | str | - | - |
| value | float | - | - |
| is_bold | int | - | - |
| indent | int | - | - |

**Returns**: `Row`



### assign_item_groups_to_svd_list(svd_list: SVDList) → None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| svd_list | SVDList | - | - |

**Returns**: `None`



### get_item_groups_map(svd_list: SVDList) → dict[str, str]

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| svd_list | SVDList | - | - |

**Returns**: `dict[str, str]`



### get_item_groups_dict() → ItemGroupsDict

**Returns**: `ItemGroupsDict`



### update_leveled_dict(leveled_dict: OrderedDict) → None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| leveled_dict | OrderedDict | - | - |

**Returns**: `None`


