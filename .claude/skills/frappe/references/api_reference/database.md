# API Reference: database.py

**Language**: Python

**Source**: `database/sqlite/database.py`

---

## Classes

### SQLiteExceptionUtil

**Inherits from**: (none)

#### Methods

##### is_deadlocked(e: sqlite3.Error) → bool

**Decorators**: `@staticmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| e | sqlite3.Error | - | - |

**Returns**: `bool`


##### is_timedout(e: sqlite3.Error) → bool

**Decorators**: `@staticmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| e | sqlite3.Error | - | - |

**Returns**: `bool`


##### is_read_only_mode_error(e: sqlite3.Error) → bool

**Decorators**: `@staticmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| e | sqlite3.Error | - | - |

**Returns**: `bool`


##### is_table_missing(e: sqlite3.Error) → bool

**Decorators**: `@staticmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| e | sqlite3.Error | - | - |

**Returns**: `bool`


##### is_missing_column(e: sqlite3.Error) → bool

**Decorators**: `@staticmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| e | sqlite3.Error | - | - |

**Returns**: `bool`


##### is_duplicate_fieldname(e: sqlite3.Error) → bool

**Decorators**: `@staticmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| e | sqlite3.Error | - | - |

**Returns**: `bool`


##### is_duplicate_entry(e: sqlite3.Error) → bool

**Decorators**: `@staticmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| e | sqlite3.Error | - | - |

**Returns**: `bool`


##### is_access_denied(e: sqlite3.Error) → bool

**Decorators**: `@staticmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| e | sqlite3.Error | - | - |

**Returns**: `bool`


##### cant_drop_field_or_key(e: sqlite3.Error) → bool

**Decorators**: `@staticmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| e | sqlite3.Error | - | - |

**Returns**: `bool`


##### is_syntax_error(e: sqlite3.Error) → bool

**Decorators**: `@staticmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| e | sqlite3.Error | - | - |

**Returns**: `bool`


##### is_statement_timeout(e: sqlite3.Error) → bool

**Decorators**: `@staticmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| e | sqlite3.Error | - | - |

**Returns**: `bool`


##### is_data_too_long(e: sqlite3.Error) → bool

**Decorators**: `@staticmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| e | sqlite3.Error | - | - |

**Returns**: `bool`


##### is_db_table_size_limit(e: sqlite3.Error) → bool

**Decorators**: `@staticmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| e | sqlite3.Error | - | - |

**Returns**: `bool`


##### is_primary_key_violation(e: sqlite3.IntegrityError) → bool

**Decorators**: `@staticmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| e | sqlite3.IntegrityError | - | - |

**Returns**: `bool`


##### is_unique_key_violation(e: sqlite3.IntegrityError) → bool

**Decorators**: `@staticmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| e | sqlite3.IntegrityError | - | - |

**Returns**: `bool`


##### is_interface_error(e: sqlite3.Error)

**Decorators**: `@staticmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| e | sqlite3.Error | - | - |


##### is_nested_transaction_error(e: sqlite3.Error)

**Decorators**: `@staticmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| e | sqlite3.Error | - | - |




### SQLiteDatabase

**Inherits from**: SQLiteExceptionUtil, Database

#### Methods

##### get_connection(self, read_only: bool = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| read_only | bool | False | - |


##### create_connection(self, read_only: bool = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| read_only | bool | False | - |


##### get_db_path(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_execution_timeout(self, seconds: int)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| seconds | int | - | - |


##### setup_type_map(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_database_size(self)

Return database size in MB.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _clean_up(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### escape(s, percent = True)

Escape quotes and percent in given string.

**Decorators**: `@staticmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| s | None | - | - |
| percent | None | True | - |


##### is_type_number(code)

**Decorators**: `@staticmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| code | None | - | - |


##### is_type_datetime(code)

**Decorators**: `@staticmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| code | None | - | - |


##### rename_table(self, old_name: str, new_name: str) → list | tuple

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| old_name | str | - | - |
| new_name | str | - | - |

**Returns**: `list | tuple`


##### describe(self, doctype: str) → list | tuple

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doctype | str | - | - |

**Returns**: `list | tuple`


##### change_column_type(self, doctype: str, column: str, type: str, nullable: bool = False) → list | tuple

Change column type by recreating the table

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doctype | str | - | - |
| column | str | - | - |
| type | str | - | - |
| nullable | bool | False | - |

**Returns**: `list | tuple`


##### rename_column(self, doctype: str, old_column_name: str, new_column_name: str)

Rename column by recreating the table

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doctype | str | - | - |
| old_column_name | str | - | - |
| new_column_name | str | - | - |


##### create_auth_table(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### create_global_search_table(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### create_user_settings_table(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_on_duplicate_update()

**Decorators**: `@staticmethod`


##### get_table_columns_description(self, table_name)

Return list of columns with descriptions.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| table_name | None | - | - |


##### get_column_type(self, doctype, column)

Return column type from database.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doctype | None | - | - |
| column | None | - | - |


##### has_index(self, table_name, index_name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| table_name | None | - | - |
| index_name | None | - | - |


##### get_column_index(self, table_name: str, fieldname: str, unique: bool = False) → frappe._dict | None

Check if column exists for a specific fields in specified order.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| table_name | str | - | - |
| fieldname | str | - | - |
| unique | bool | False | - |

**Returns**: `frappe._dict | None`


##### add_index(self, doctype: str, fields: list, index_name: str | None = None)

Creates an index with given fields if not already created.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doctype | str | - | - |
| fields | list | - | - |
| index_name | str | None | None | - |


##### add_unique(self, doctype, fields, constraint_name = None)

Creates unique constraint on fields.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doctype | None | - | - |
| fields | None | - | - |
| constraint_name | None | None | - |


##### updatedb(self, doctype, meta = None)

Syncs a `DocType` to the table.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doctype | None | - | - |
| meta | None | None | - |


##### get_database_list(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_tables(self, cached = True)

Return list of tables.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| cached | None | True | - |


##### get_row_size(self, doctype: str) → int

Get estimated max row size of any table in bytes.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doctype | str | - | - |

**Returns**: `int`


##### execute_query(self, query, values = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| query | None | - | - |
| values | None | None | - |


##### sql(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### sql_ddl(self, query)

Execute DDL query.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| query | None | - | - |


##### begin(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### commit(self, chain = None)

Commit current transaction. Calls SQL `COMMIT`.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| chain | None | None | - |


##### rollback(self)

`ROLLBACK` current transaction. Optionally rollback to a known save_point.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_db_table_columns(self, table) → list[str]

Return list of column names from given table.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| table | None | - | - |

**Returns**: `list[str]`


##### estimate_count(self, doctype: str)

Get estimated count of total rows in a table.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doctype | str | - | - |


##### truncate(self, doctype: str)

Truncate a table.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doctype | str | - | - |


##### check_implicit_commit(self, query: str, query_type: str)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| query | str | - | - |
| query_type | str | - | - |




## Functions

### modify_query(query)

Modifies query according to the requirements of SQLite

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| query | None | - | - |

**Returns**: (none)



### replace_locate_with_instr(query: str) → str

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| query | str | - | - |

**Returns**: `str`



### regexp(expr: str, item: str) → bool

Define regexp implementation for SQLite manually

Although it works in the CLI - doesn't work through python

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| expr | str | - | - |
| item | str | - | - |

**Returns**: `bool`



### regexp_replace(item: str, pattern: str, repl: str) → str

Define regexp_replace implementation for SQLite

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item | str | - | - |
| pattern | str | - | - |
| repl | str | - | - |

**Returns**: `str`


