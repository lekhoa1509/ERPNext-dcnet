# API Reference: dashboard.py

**Language**: Python

**Source**: `doctype/dashboard/dashboard.py`

---

## Classes

### Dashboard

**Inherits from**: Document

#### Methods

##### on_update(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_custom_options(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### get_permission_query_conditions(user)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| user | None | - | - |

**Returns**: (none)



### get_permitted_charts(dashboard_name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| dashboard_name | None | - | - |

**Returns**: (none)



### get_permitted_cards(dashboard_name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| dashboard_name | None | - | - |

**Returns**: (none)



### get_non_standard_charts_in_dashboard(dashboard)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| dashboard | None | - | - |

**Returns**: (none)



### get_non_standard_cards_in_dashboard(dashboard)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| dashboard | None | - | - |

**Returns**: (none)



### get_non_standard_warning_message(non_standard_docs_map)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| non_standard_docs_map | None | - | - |

**Returns**: (none)



### get_html(docs, doctype)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| docs | None | - | - |
| doctype | None | - | - |

**Returns**: (none)


