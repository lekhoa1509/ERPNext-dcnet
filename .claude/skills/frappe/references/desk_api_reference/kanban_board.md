# API Reference: kanban_board.py

**Language**: Python

**Source**: `doctype/kanban_board/kanban_board.py`

---

## Classes

### KanbanBoard

**Inherits from**: Document

#### Methods

##### validate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_change(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### before_insert(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_column_name(self)

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



### get_kanban_boards(doctype)

Get Kanban Boards for doctype to show in List View

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |

**Returns**: (none)



### add_column(board_name, column_title)

Adds new column to Kanban Board

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| board_name | None | - | - |
| column_title | None | - | - |

**Returns**: (none)



### archive_restore_column(board_name, column_title, status)

Set column's status to status

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| board_name | None | - | - |
| column_title | None | - | - |
| status | None | - | - |

**Returns**: (none)



### update_order(board_name, order)

Save the order of cards in columns

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| board_name | None | - | - |
| order | None | - | - |

**Returns**: (none)



### update_order_for_single_card(board_name, docname, from_colname, to_colname, old_index, new_index)

Save the order of cards in columns

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| board_name | None | - | - |
| docname | None | - | - |
| from_colname | None | - | - |
| to_colname | None | - | - |
| old_index | None | - | - |
| new_index | None | - | - |

**Returns**: (none)



### get_kanban_column_order_and_index(board, colname)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| board | None | - | - |
| colname | None | - | - |

**Returns**: (none)



### add_card(board_name, docname, colname)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| board_name | None | - | - |
| docname | None | - | - |
| colname | None | - | - |

**Returns**: (none)



### quick_kanban_board(doctype, board_name, field_name, project = None)

Create new KanbanBoard quickly with default options

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| board_name | None | - | - |
| field_name | None | - | - |
| project | None | None | - |

**Returns**: (none)



### get_order_for_column(board, colname)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| board | None | - | - |
| colname | None | - | - |

**Returns**: (none)



### update_column_order(board_name, order)

Set the order of columns in Kanban Board

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| board_name | None | - | - |
| order | None | - | - |

**Returns**: (none)



### set_indicator(board_name, column_name, indicator)

Set the indicator color of column

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| board_name | None | - | - |
| column_name | None | - | - |
| indicator | None | - | - |

**Returns**: (none)



### save_settings(board_name: str, settings: str) → Document

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| board_name | str | - | - |
| settings | str | - | - |

**Returns**: `Document`


