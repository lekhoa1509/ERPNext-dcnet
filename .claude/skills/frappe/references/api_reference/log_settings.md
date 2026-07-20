# API Reference: log_settings.py

**Language**: Python

**Source**: `core/doctype/log_settings/log_settings.py`

---

## Classes

### LogType

Interface requirement for doctypes that can be cleared using log settings.

**Inherits from**: Protocol

#### Methods

##### clear_old_logs(days: int) → None

**Decorators**: `@staticmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| days | int | - | - |

**Returns**: `None`




### LogSettings

**Inherits from**: Document

#### Methods

##### validate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### remove_unsupported_doctypes(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _deduplicate_entries(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### add_default_logtypes(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### clear_logs(self)

Log settings can clear any log type that's registered to it and provides a method to delete old logs.

Check `LogDoctype` above for interface that doctypes need to implement.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### register_doctype(self, doctype: str, days = 30)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doctype | str | - | - |
| days | None | 30 | - |




## Functions

### _supports_log_clearing(doctype: str) → bool

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | str | - | - |

**Returns**: `bool`



### run_log_clean_up()

**Returns**: (none)



### has_unseen_error_log()

**Returns**: (none)



### get_log_doctypes(doctype, txt, searchfield, start, page_len, filters)

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



### clear_log_table(doctype, days = 90)

If any logtype table grows too large then clearing it with DELETE query
is not feasible in reasonable time. This command copies recent data to new
table and replaces current table with new smaller table.

ref: https://mariadb.com/kb/en/big-deletes/#deleting-more-than-half-a-table

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| days | None | 90 | - |

**Returns**: (none)


