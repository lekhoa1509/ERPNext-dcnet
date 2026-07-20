# API Reference: bom_update_tool.py

**Language**: Python

**Source**: `doctype/bom_update_tool/bom_update_tool.py`

---

## Classes

### BOMUpdateTool

**Inherits from**: Document



## Functions

### enqueue_replace_bom(boms: dict | str | None = None, args: dict | str | None = None) → 'BOMUpdateLog'

Returns a BOM Update Log (that queues a job) for BOM Replacement.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| boms | dict | str | None | None | - |
| args | dict | str | None | None | - |

**Returns**: `'BOMUpdateLog'`



### enqueue_update_cost() → 'BOMUpdateLog'

Returns a BOM Update Log (that queues a job) for BOM Cost Updation.

**Returns**: `'BOMUpdateLog'`



### auto_update_latest_price_in_all_boms() → None

Called via hooks.py.

**Returns**: `None`



### is_older_log(log: dict) → bool

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| log | dict | - | - |

**Returns**: `bool`



### create_bom_update_log(boms: dict[str, str] | None = None, update_type: Literal['Replace BOM', 'Update Cost'] = 'Replace BOM') → 'BOMUpdateLog'

Creates a BOM Update Log that handles the background job.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| boms | dict[str, str] | None | None | - |
| update_type | Literal['Replace BOM', 'Update Cost'] | 'Replace BOM' | - |

**Returns**: `'BOMUpdateLog'`


