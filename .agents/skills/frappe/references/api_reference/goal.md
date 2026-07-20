# API Reference: goal.py

**Language**: Python

**Source**: `utils/goal.py`

---

## Functions

### get_monthly_results(goal_doctype: str, goal_field: str, date_col: str, filters: dict, aggregation: str = 'sum') → dict

Get monthly aggregation values for given field of doctype

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| goal_doctype | str | - | - |
| goal_field | str | - | - |
| date_col | str | - | - |
| filters | dict | - | - |
| aggregation | str | 'sum' | - |

**Returns**: `dict`



### get_monthly_goal_graph_data(title: str, doctype: str, docname: str, goal_value_field: str, goal_total_field: str, goal_history_field: str, goal_doctype: str, goal_doctype_link: str, goal_field: str, date_field: str, aggregation: str = 'sum', filters: str | dict | None = None) → dict

Get month-wise graph data for a doctype based on aggregation values of a field in the goal doctype

:param title: Graph title
:param doctype: doctype of graph doc
:param docname: of the doc to set the graph in
:param goal_value_field: goal field of doctype
:param goal_total_field: current month value field of doctype
:param goal_history_field: cached history field
:param goal_doctype: doctype the goal is based on
:param goal_doctype_link: doctype link field in goal_doctype
:param goal_field: field from which the goal is calculated
:param aggregation: a value like 'count', 'sum', 'avg'
:param filters: optional filters

:return: dict of graph data

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| title | str | - | - |
| doctype | str | - | - |
| docname | str | - | - |
| goal_value_field | str | - | - |
| goal_total_field | str | - | - |
| goal_history_field | str | - | - |
| goal_doctype | str | - | - |
| goal_doctype_link | str | - | - |
| goal_field | str | - | - |
| date_field | str | - | - |
| aggregation | str | 'sum' | - |
| filters | str | dict | None | None | - |

**Returns**: `dict`


