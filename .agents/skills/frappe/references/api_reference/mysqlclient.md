# API Reference: mysqlclient.py

**Language**: Python

**Source**: `database/mariadb/mysqlclient.py`

---

## Classes

### MariaDBExceptionUtil

**Inherits from**: (none)

#### Methods

##### is_deadlocked(e: MySQLdb.Error) → bool

**Decorators**: `@staticmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| e | MySQLdb.Error | - | - |

**Returns**: `bool`


##### is_timedout(e: MySQLdb.Error) → bool

**Decorators**: `@staticmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| e | MySQLdb.Error | - | - |

**Returns**: `bool`


##### is_read_only_mode_error(e: MySQLdb.Error) → bool

**Decorators**: `@staticmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| e | MySQLdb.Error | - | - |

**Returns**: `bool`


##### is_table_missing(e: MySQLdb.Error) → bool

**Decorators**: `@staticmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| e | MySQLdb.Error | - | - |

**Returns**: `bool`


##### is_missing_table(e: MySQLdb.Error) → bool

**Decorators**: `@staticmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| e | MySQLdb.Error | - | - |

**Returns**: `bool`


##### is_missing_column(e: MySQLdb.Error) → bool

**Decorators**: `@staticmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| e | MySQLdb.Error | - | - |

**Returns**: `bool`


##### is_duplicate_fieldname(e: MySQLdb.Error) → bool

**Decorators**: `@staticmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| e | MySQLdb.Error | - | - |

**Returns**: `bool`


##### is_duplicate_entry(e: MySQLdb.Error) → bool

**Decorators**: `@staticmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| e | MySQLdb.Error | - | - |

**Returns**: `bool`


##### is_access_denied(e: MySQLdb.Error) → bool

**Decorators**: `@staticmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| e | MySQLdb.Error | - | - |

**Returns**: `bool`


##### cant_drop_field_or_key(e: MySQLdb.Error) → bool

**Decorators**: `@staticmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| e | MySQLdb.Error | - | - |

**Returns**: `bool`


##### is_syntax_error(e: MySQLdb.Error) → bool

**Decorators**: `@staticmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| e | MySQLdb.Error | - | - |

**Returns**: `bool`


##### is_statement_timeout(e: MySQLdb.Error) → bool

**Decorators**: `@staticmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| e | MySQLdb.Error | - | - |

**Returns**: `bool`


##### is_data_too_long(e: MySQLdb.Error) → bool

**Decorators**: `@staticmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| e | MySQLdb.Error | - | - |

**Returns**: `bool`


##### is_db_table_size_limit(e: MySQLdb.Error) → bool

**Decorators**: `@staticmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| e | MySQLdb.Error | - | - |

**Returns**: `bool`


##### is_primary_key_violation(e: MySQLdb.Error) → bool

**Decorators**: `@staticmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| e | MySQLdb.Error | - | - |

**Returns**: `bool`


##### is_unique_key_violation(e: MySQLdb.Error) → bool

**Decorators**: `@staticmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| e | MySQLdb.Error | - | - |

**Returns**: `bool`


##### is_interface_error(e: MySQLdb.Error)

**Decorators**: `@staticmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| e | MySQLdb.Error | - | - |




### MariaDBConnectionUtil

**Inherits from**: (none)

#### Methods

##### get_connection(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _get_connection(self) → 'MySQLdb.Connection'

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `'MySQLdb.Connection'`


##### create_connection(self)

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


##### get_connection_settings(self) → dict

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `dict`




### MariaDBDatabase

**Inherits from**: MariaDBConnectionUtil, MariaDBExceptionUtil, Database

#### Methods

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


##### log_query(self, query, query_type, values, debug)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| query | None | - | - |
| query_type | None | - | - |
| values | None | - | - |
| debug | None | - | - |


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

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doctype | str | - | - |
| column | str | - | - |
| type | str | - | - |
| nullable | bool | False | - |

**Returns**: `list | tuple`


##### rename_column(self, doctype: str, old_column_name, new_column_name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doctype | str | - | - |
| old_column_name | None | - | - |
| new_column_name | None | - | - |


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

This differs from db.has_index because it doesn't rely on index name but columns inside an
index.

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
Index name will be `fieldname1_fieldname2_index`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doctype | str | - | - |
| fields | list | - | - |
| index_name | str | None | None | - |


##### add_unique(self, doctype, fields, constraint_name = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doctype | None | - | - |
| fields | None | - | - |
| constraint_name | None | None | - |


##### updatedb(self, doctype, meta = None)

Syncs a `DocType` to the table
* creates if required
* updates columns
* updates indices

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


##### unbuffered_cursor(self)

**Decorators**: `@contextmanager`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### estimate_count(self, doctype: str)

Get estimated count of total rows in a table.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doctype | str | - | - |




## Functions

### escape_frozenset(obj, mapping = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| obj | None | - | - |
| mapping | None | None | - |

**Returns**: (none)



### escape_timedelta(obj, mapping = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| obj | None | - | - |
| mapping | None | None | - |

**Returns**: (none)



### escape_dict(obj, mapping = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| obj | None | - | - |
| mapping | None | None | - |

**Returns**: (none)


