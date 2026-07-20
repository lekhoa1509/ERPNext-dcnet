# API Reference: asset_maintenance.py

**Language**: Python

**Source**: `doctype/asset_maintenance/asset_maintenance.py`

---

## Classes

### AssetMaintenance

**Inherits from**: Document

#### Methods

##### validate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_update(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### after_delete(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### sync_maintenance_tasks(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### assign_tasks(asset_maintenance_name, assign_to_member, maintenance_task, next_due_date)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| asset_maintenance_name | None | - | - |
| assign_to_member | None | - | - |
| maintenance_task | None | - | - |
| next_due_date | None | - | - |

**Returns**: (none)



### calculate_next_due_date(periodicity, start_date = None, end_date = None, last_completion_date = None, next_due_date = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| periodicity | None | - | - |
| start_date | None | None | - |
| end_date | None | None | - |
| last_completion_date | None | None | - |
| next_due_date | None | None | - |

**Returns**: (none)



### update_maintenance_log(asset_maintenance, item_code, item_name, task)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| asset_maintenance | None | - | - |
| item_code | None | - | - |
| item_name | None | - | - |
| task | None | - | - |

**Returns**: (none)



### get_team_members(doctype, txt, searchfield, start, page_len, filters)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| txt | None | - | - |
| searchfield | None | - | - |
| start | None | - | - |
| page_len | None | - | - |
| filters | None | - | - |

**Returns**: (none)



### get_maintenance_log(asset_name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| asset_name | None | - | - |

**Returns**: (none)


