# API Reference: bom_updation_utils.py

**Language**: Python

**Source**: `doctype/bom_update_log/bom_updation_utils.py`

---

## Functions

### replace_bom(boms: dict, log_name: str) → None

Replace current BOM with new BOM in parent BOMs.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| boms | dict | - | - |
| log_name | str | - | - |

**Returns**: `None`



### update_cost_in_level(doc: 'BOMUpdateLog', bom_list: list[str], batch_name: int | str) → None

Updates Cost for BOMs within a given level. Runs via background jobs.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | 'BOMUpdateLog' | - | - |
| bom_list | list[str] | - | - |
| batch_name | int | str | - | - |

**Returns**: `None`



### get_ancestor_boms(new_bom: str, bom_list: list | None = None) → list

Recursively get all ancestors of BOM.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| new_bom | str | - | - |
| bom_list | list | None | None | - |

**Returns**: `list`



### update_new_bom_in_bom_items(unit_cost: float, current_bom: str, new_bom: str) → None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| unit_cost | float | - | - |
| current_bom | str | - | - |
| new_bom | str | - | - |

**Returns**: `None`



### get_bom_unit_cost(bom_name: str) → float

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| bom_name | str | - | - |

**Returns**: `float`



### update_cost_in_boms(bom_list: list[str]) → None

Updates cost in given BOMs. Returns current and total updated BOMs.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| bom_list | list[str] | - | - |

**Returns**: `None`



### get_next_higher_level_boms(child_boms: list[str], processed_boms: dict[str, bool]) → list[str]

Generate immediate higher level dependants with no unresolved dependencies (children).

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| child_boms | list[str] | - | - |
| processed_boms | dict[str, bool] | - | - |

**Returns**: `list[str]`



### get_leaf_boms() → list[str]

Get BOMs that have no dependencies.

**Returns**: `list[str]`



### _generate_dependence_map() → defaultdict

Generate maps such as: { BOM-1: [Dependant-BOM-1, Dependant-BOM-2, ..] }.
Here BOM-1 is the leaf/lower level node/dependency.
The list contains one level higher nodes/dependants that depend on BOM-1.

Generate and return the reverse as well.

**Returns**: `defaultdict`



### set_values_in_log(log_name: str, values: dict[str, Any], commit: bool = False) → None

Update BOM Update Log record.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| log_name | str | - | - |
| values | dict[str, Any] | - | - |
| commit | bool | False | - |

**Returns**: `None`



### handle_exception(doc: 'BOMUpdateLog') → None

Rolls back and fails BOM Update Log.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | 'BOMUpdateLog' | - | - |

**Returns**: `None`



### _all_children_are_processed(parent_bom)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| parent_bom | None | - | - |

**Returns**: (none)


