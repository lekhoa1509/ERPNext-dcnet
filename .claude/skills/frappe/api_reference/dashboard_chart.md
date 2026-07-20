# API Reference: dashboard_chart.py

**Language**: Python

**Source**: `desk/doctype/dashboard_chart/dashboard_chart.py`

---

## Classes

### DashboardChart

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


##### check_required_field(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### check_document_type(self)

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



### has_permission(doc, ptype, user)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |
| ptype | None | - | - |
| user | None | - | - |

**Returns**: (none)



### get(chart_name = None, chart = None, no_cache = None, filters = None, from_date = None, to_date = None, timespan = None, time_interval = None, heatmap_year = None, refresh = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| chart_name | None | None | - |
| chart | None | None | - |
| no_cache | None | None | - |
| filters | None | None | - |
| from_date | None | None | - |
| to_date | None | None | - |
| timespan | None | None | - |
| time_interval | None | None | - |
| heatmap_year | None | None | - |
| refresh | None | None | - |

**Returns**: (none)



### create_dashboard_chart(args)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| args | None | - | - |

**Returns**: (none)



### create_report_chart(args)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| args | None | - | - |

**Returns**: (none)



### add_chart_to_dashboard(args)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| args | None | - | - |

**Returns**: (none)



### get_chart_config(chart, filters, timespan, timegrain, from_date, to_date)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| chart | None | - | - |
| filters | None | - | - |
| timespan | None | - | - |
| timegrain | None | - | - |
| from_date | None | - | - |
| to_date | None | - | - |

**Returns**: (none)



### get_heatmap_chart_config(chart, filters, heatmap_year)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| chart | None | - | - |
| filters | None | - | - |
| heatmap_year | None | - | - |

**Returns**: (none)



### get_group_by_chart_config(chart, filters) → dict | None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| chart | None | - | - |
| filters | None | - | - |

**Returns**: `dict | None`



### get_aggregate_function(chart_type)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| chart_type | None | - | - |

**Returns**: (none)



### get_result(data, timegrain, from_date, to_date, chart_type)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| data | None | - | - |
| timegrain | None | - | - |
| from_date | None | - | - |
| to_date | None | - | - |
| chart_type | None | - | - |

**Returns**: (none)



### get_charts_for_user(doctype, txt, searchfield, start, page_len, filters)

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



### get_parent_doctypes(child_type: str) → list[str]

Get all parent doctypes that have the child doctype.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| child_type | str | - | - |

**Returns**: `list[str]`


