# API Reference: bom_update_log.py

**Language**: Python

**Source**: `doctype/bom_update_log/bom_update_log.py`

---

## Classes

### BOMMissingError

**Inherits from**: frappe.ValidationError



### BOMUpdateLog

**Inherits from**: Document

#### Methods

##### clear_old_logs(days = None)

**Decorators**: `@staticmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| days | None | None | - |


##### validate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_discard(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_boms_are_specified(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_same_bom(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_bom_items(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_bom_cost_update_in_progress(self)

If another Cost Updation Log is still in progress, dont make new ones.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_submit(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### run_replace_bom_job(doc: 'BOMUpdateLog', boms: dict[str, str] | None = None) → None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | 'BOMUpdateLog' | - | - |
| boms | dict[str, str] | None | None | - |

**Returns**: `None`



### process_boms_cost_level_wise(update_doc: 'BOMUpdateLog', parent_boms: list[str] | None = None) → None | tuple

Queue jobs at the start of new BOM Level in 'Update Cost' Jobs.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| update_doc | 'BOMUpdateLog' | - | - |
| parent_boms | list[str] | None | None | - |

**Returns**: `None | tuple`



### queue_bom_cost_jobs(current_boms_list: list[str], update_doc: 'BOMUpdateLog', current_level: int) → None

Queue batches of 20k BOMs of the same level to process parallelly

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| current_boms_list | list[str] | - | - |
| update_doc | 'BOMUpdateLog' | - | - |
| current_level | int | - | - |

**Returns**: `None`



### resume_bom_cost_update_jobs()

1. Checks for In Progress BOM Update Log.
2. Checks if this job has completed the _current level_.
3. If current level is complete, get parent BOMs and start next level.
4. If no parents, mark as Complete.
5. If current level is WIP, skip the Log.

Called every 5 minutes via Cron job.

**Returns**: (none)



### get_processed_current_boms(log: dict[str, Any], bom_batches: dict[str, Any]) → tuple[list[str], dict[str, Any]]

Aggregate all BOMs from BOM Update Batch rows into 'processed_boms' field
and into current boms list.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| log | dict[str, Any] | - | - |
| bom_batches | dict[str, Any] | - | - |

**Returns**: `tuple[list[str], dict[str, Any]]`


