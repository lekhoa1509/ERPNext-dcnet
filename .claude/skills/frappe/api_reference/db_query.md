# API Reference: db_query.py

**Language**: Python

**Source**: `model/db_query.py`

---

## Classes

### DatabaseQuery

**Inherits from**: (none)

#### Methods

##### __init__(self, doctype, user = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doctype | None | - | - |
| user | None | None | - |


##### doctype_meta(self)

**Decorators**: `@cached_property`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_meta(self, doctype: str)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doctype | str | - | - |


##### query_tables(self)

**Decorators**: `@property`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### execute(self, fields = None, filters: FilterSignature | str | None = None, or_filters: FilterSignature | None = None, docstatus = None, group_by = None, order_by = DefaultOrderBy, limit_start = False, limit_page_length = None, as_list = False, with_childnames = False, debug = False, ignore_permissions = False, user = None, with_comment_count = False, join = 'left join', distinct = False, start = None, page_length = None, limit = None, ignore_ifnull = False, save_user_settings = False, save_user_settings_fields = False, update = None, user_settings = None, reference_doctype = None, run = True, strict = True, pluck = None, ignore_ddl = False) → list

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| fields | None | None | - |
| filters | FilterSignature | str | None | None | - |
| or_filters | FilterSignature | None | None | - |
| docstatus | None | None | - |
| group_by | None | None | - |
| order_by | None | DefaultOrderBy | - |
| limit_start | None | False | - |
| limit_page_length | None | None | - |
| as_list | None | False | - |
| with_childnames | None | False | - |
| debug | None | False | - |
| ignore_permissions | None | False | - |
| user | None | None | - |
| with_comment_count | None | False | - |
| join | None | 'left join' | - |
| distinct | None | False | - |
| start | None | None | - |
| page_length | None | None | - |
| limit | None | None | - |
| ignore_ifnull | None | False | - |
| save_user_settings | None | False | - |
| save_user_settings_fields | None | False | - |
| update | None | None | - |
| user_settings | None | None | - |
| reference_doctype | None | None | - |
| run | None | True | - |
| strict | None | True | - |
| pluck | None | None | - |
| ignore_ddl | None | False | - |

**Returns**: `list`


##### mask_fields(self, result)

Mask fields in the result based on the doctype's masked fields

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| result | None | - | - |


##### get_masked_fields(self)

Get masked fields for the doctype

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### build_and_run(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### prepare_args(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### prepare_select_args(self, args)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| args | None | - | - |


##### parse_args(self)

Convert fields and filters from strings to list, dicts.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### sanitize_fields(self)

regex : ^.*[,();].*
purpose : The regex will look for malicious patterns like `,`, '(', ')', '@', ;' in each
                field which may leads to sql injection.
example :
        field = "`DocType`.`issingle`, version()"
As field contains `,` and mysql function `version()`, with the help of regex
the system will filter out this field.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### extract_tables(self)

extract tables from fields

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### append_table(self, table_name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| table_name | None | - | - |


##### append_link_table(self, doctype, fieldname)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doctype | None | - | - |
| fieldname | None | - | - |


##### check_read_permission(self, doctype: str, parent_doctype: str | None = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doctype | str | - | - |
| parent_doctype | str | None | None | - |


##### _set_permission_map(self, doctype: str, parent_doctype: str | None = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doctype | str | - | - |
| parent_doctype | str | None | None | - |


##### set_field_tables(self)

If there are more than one table, the fieldname must not be ambiguous.
If the fieldname is not explicitly mentioned, set the default table

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### cast_name_fields(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_table_columns(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_optional_columns(self)

Removes optional columns like `_user_tags`, `_comments` etc. if not in table

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### build_conditions(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### build_filter_conditions(self, filters: Filters, conditions: list, ignore_permissions = None)

build conditions from user filters

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| filters | Filters | - | - |
| conditions | list | - | - |
| ignore_permissions | None | None | - |


##### remove_field(self, idx: int)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| idx | int | - | - |


##### apply_fieldlevel_read_permissions(self)

Apply fieldlevel read permissions to the query

Note: Does not apply to `frappe.model.core_doctype_list`

Remove fields that user is not allowed to read. If `fields=["*"]` is passed, only permitted fields will
be returned.

Example:
        - User has read permission only on `title` for DocType `Note`
        - Query: fields=["*"]
        - Result: fields=["title", ...] // will also include Frappe's meta field like `name`, `owner`, etc.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### prepare_filter_condition(self, ft: FilterTuple) → str

Return a filter condition in the format:

ifnull(`tabDocType`.`fieldname`, fallback) operator "value"

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| ft | FilterTuple | - | - |

**Returns**: `str`


##### build_match_conditions(self, as_condition = True) → str | list

add match conditions if applicable

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| as_condition | None | True | - |

**Returns**: `str | list`


##### get_share_condition(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### add_user_permissions(self, user_permissions)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| user_permissions | None | - | - |


##### get_permission_query_conditions(self) → str

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `str`


##### set_order_by(self, args)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| args | None | - | - |


##### validate_order_by_and_group_by(self, parameters: str)

Check order by, group by so that atleast one column is selected and does not have subquery

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| parameters | str | - | - |


##### add_limit(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### add_comment_count(self, result)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| result | None | - | - |


##### update_user_settings(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### _parse_sql(field: str) → Statement | None

Parse a given SQL statement using `sqlparse`.

Args:
        field (str): The SQL statement string to parse.

Returns:
        Statement | None: A `sqlparse.sql.Statement` object if parsing succeeds, otherwise `None`.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| field | str | - | - |

**Returns**: `Statement | None`



### cast_name(column: str) → str

Casts name field to varchar for postgres

Handles majorly 4 cases:
1. locate
2. strpos
3. ifnull
4. coalesce

Uses regex substitution.

Example:
input - "ifnull(`tabBlog Post`.`name`, '')=''"
output - "ifnull(cast(`tabBlog Post`.`name` as varchar), '')=''" 

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| column | str | - | - |

**Returns**: `str`



### get_order_by(doctype, meta)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| meta | None | - | - |

**Returns**: (none)



### has_any_user_permission_for_doctype(doctype, user, applicable_for)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| user | None | - | - |
| applicable_for | None | - | - |

**Returns**: (none)



### get_between_date_filter(value, df = None)

Handle datetime filter bounds for between filter values.

If date is passed but fieldtype is datetime then
        from part is converted to start of day and to part is converted to end of day.
If any of filter part (to or from) are missing then:
        start or end of current day is assumed as fallback.
If fieldtypes match with filter values then:
        no change is applied.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| value | None | - | - |
| df | None | None | - |

**Returns**: (none)



### _convert_type_for_between_filters(value: DateTimeLikeObject, set_time: datetime.time) → datetime.datetime

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| value | DateTimeLikeObject | - | - |
| set_time | datetime.time | - | - |

**Returns**: `datetime.datetime`



### get_additional_filter_field(additional_filters_config, f, value)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| additional_filters_config | None | - | - |
| f | None | - | - |
| value | None | - | - |

**Returns**: (none)



### get_date_range(operator: str, value: str)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| operator | str | - | - |
| value | str | - | - |

**Returns**: (none)



### requires_owner_constraint(role_permissions)

Return True if "select" or "read" isn't available without being creator.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| role_permissions | None | - | - |

**Returns**: (none)



### wrap_grave_quotes(table: str) → str

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| table | str | - | - |

**Returns**: `str`



### is_plain_field(field: str) → bool

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| field | str | - | - |

**Returns**: `bool`



### in_function(substr: str, field: str) → bool

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| substr | str | - | - |
| field | str | - | - |

**Returns**: `bool`



### strip_alias(field: str) → str

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| field | str | - | - |

**Returns**: `str`



### _find_subqueries(parsed: Statement) → list

Recursively find all subqueries in a parsed SQL statement.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| parsed | Statement | - | - |

**Returns**: `list`



### _check_sql_token(statement: Statement) → None

Checks the output of `sqlparse.parse()` to detect blocked functions and subqueries.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| statement | Statement | - | - |

**Returns**: `None`



### _raise_exception()

**Returns**: (none)



### _is_query(field)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| field | None | - | - |

**Returns**: (none)



### _in_standard_sql_methods(field)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| field | None | - | - |

**Returns**: (none)


