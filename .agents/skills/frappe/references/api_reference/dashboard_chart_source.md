# API Reference: dashboard_chart_source.py

**Language**: Python

**Source**: `desk/doctype/dashboard_chart_source/dashboard_chart_source.py`

---

## Classes

### DashboardChartSource

**Inherits from**: Document

#### Methods

##### on_update(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_trash(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### read_config(self) → str

Return the config JS file for this dashboard chart source.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `str`


##### delete_folder(self)

Delete the folder for this dashboard chart source.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_folder_path(self) → Path

Return the path of the folder for this dashboard chart source.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `Path`




## Functions

### get_config(name: str) → str

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| name | str | - | - |

**Returns**: `str`


