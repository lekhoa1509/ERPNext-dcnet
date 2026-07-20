# API Reference: query.py

**Language**: Python

**Source**: `database/query.py`

---

## Classes

### Engine

**Inherits from**: (none)

#### Methods

##### get_query(self, table: str | Table, fields: str | list | tuple | set | None = None, filters: dict[str, FilterValue] | FilterValue | list[list | FilterValue] | None = None, order_by: str | None = None, group_by: str | None = None, limit: int | None = None, offset: int | None = None, distinct: bool = False, for_update: bool = False, update: bool = False, into: bool = False, delete: bool = False) → QueryBuilder

Build a query with optional compatibility mode for legacy db_query behavior.

Args:
        db_query_compat: When True, uses legacy db_query behavior for sorting and filtering.
        This is kept optional to not break existing code that relies on the original query builder behaviour.
        ignore_user_permissions: Ignore user permissions for the query.
                Useful for link search queries when the link field has `ignore_user_permissions` set.
        validate_filters: DEPRECATED. Will be removed in future versions.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| table | str | Table | - | - |
| fields | str | list | tuple | set | None | None | - |
| filters | dict[str, FilterValue] | FilterValue | list[list | FilterValue] | None | None | - |
| order_by | str | None | None | - |
| group_by | str | None | None | - |
| limit | int | None | None | - |
| offset | int | None | None | - |
| distinct | bool | False | - |
| for_update | bool | False | - |
| update | bool | False | - |
| into | bool | False | - |
| delete | bool | False | - |

**Returns**: `QueryBuilder`


##### validate_doctype(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### apply_fields(self, fields)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| fields | None | - | - |


##### apply_filters(self, filters: dict[str, FilterValue] | FilterValue | list[list | FilterValue] | None = None, collect: list | None = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| filters | dict[str, FilterValue] | FilterValue | list[list | FilterValue] | None | None | - |
| collect | list | None | None | - |


##### apply_or_filters(self, or_filters: dict[str, FilterValue] | FilterValue | list[list | FilterValue] | None = None)

Apply OR filters - all conditions are combined with OR operator.

Example:
        or_filters={"name": "User", "module": "Core"}
        → Collects: [Criterion(name='User'), Criterion(module='Core')]
        → Combines: Criterion(name='User') | Criterion(module='Core')
        → Result: WHERE name='User' OR module='Core'

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| or_filters | dict[str, FilterValue] | FilterValue | list[list | FilterValue] | None | None | - |


##### apply_list_filters(self, filter: list, collect: list | None = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| filter | list | - | - |
| collect | list | None | None | - |


##### apply_dict_filters(self, filters: dict[str, FilterValue | list], collect: list | None = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| filters | dict[str, FilterValue | list] | - | - |
| collect | list | None | None | - |


##### _apply_filter(self, field: str | Field, value: FilterValue | list | set | None, operator: str = '=', doctype: str | None = None, collect: list | None = None)

Applies a simple filter condition to the query.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| field | str | Field | - | - |
| value | FilterValue | list | set | None | - | - |
| operator | str | '=' | - |
| doctype | str | None | None | - |
| collect | list | None | None | - |


##### _build_criterion_for_simple_filter(self, field: str | Field, value: FilterValue | Field | list | set | None, operator: str = '=', doctype: str | None = None) → 'Criterion | None'

Builds a pypika Criterion object for a simple filter condition.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| field | str | Field | - | - |
| value | FilterValue | Field | list | set | None | - | - |
| operator | str | '=' | - |
| doctype | str | None | None | - |

**Returns**: `'Criterion | None'`


##### _parse_nested_filters(self, nested_list: list | tuple) → 'Criterion | None'

Parses a nested filter list like [cond1, 'and', cond2, 'or', cond3, ...] into a pypika Criterion.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| nested_list | list | tuple | - | - |

**Returns**: `'Criterion | None'`


##### _condition_to_criterion(self, condition: list | tuple) → 'Criterion'

Converts a single condition (simple filter list or nested list) into a pypika Criterion.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| condition | list | tuple | - | - |

**Returns**: `'Criterion'`


##### _validate_and_prepare_filter_field(self, field: str | Field, doctype: str | None = None) → Field

Validate field name for filters and return a pypika Field object. Handles dynamic fields.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| field | str | Field | - | - |
| doctype | str | None | None | - |

**Returns**: `Field`


##### _check_field_permission(self, doctype: str, fieldname: str, parent_doctype: str | None = None)

Check if the user has permission to access the given field

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doctype | str | - | - |
| fieldname | str | - | - |
| parent_doctype | str | None | None | - |


##### _get_cached_permitted_fields(self, doctype: str, parenttype: str | None, permission_type: str) → set

Get permitted fields with caching to avoid redundant lookups.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doctype | str | - | - |
| parenttype | str | None | - | - |
| permission_type | str | - | - |

**Returns**: `set`


##### parse_string_field(self, field: str)

Parses a field string into a pypika Field object.

Handles:
- *
- simple_field
- `quoted_field`
- tabDocType.simple_field
- `tabDocType`.`quoted_field`
- `tabTable Name`.`quoted_field`
- Aliases for all above formats (e.g., field as alias)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| field | str | - | - |


##### parse_fields(self, fields: str | list | tuple | set | Field | AggregateFunction | None) → 'list[Field | AggregateFunction | Criterion | DynamicTableField | ChildQuery]'

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| fields | str | list | tuple | set | Field | AggregateFunction | None | - | - |

**Returns**: `'list[Field | AggregateFunction | Criterion | DynamicTableField | ChildQuery]'`


##### _parse_single_field_item(self, field: str | Criterion | dict | Field | Term) → 'list | Criterion | Field | DynamicTableField | ChildQuery | None'

Parses a single item from the fields list/tuple. Assumes comma-separated strings have already been split.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| field | str | Criterion | dict | Field | Term | - | - |

**Returns**: `'list | Criterion | Field | DynamicTableField | ChildQuery | None'`


##### apply_group_by(self, group_by: str | None = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| group_by | str | None | None | - |


##### apply_order_by(self, order_by: str | None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| order_by | str | None | - | - |


##### _apply_default_order_by(self)

Apply default ordering based on configured DocType metadata

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _parse_backtick_field_notation(self, field_name: str) → tuple[str, str] | None

Parse backtick field notation like `tabDocType`.`fieldname` or `tabDocType`.fieldname and return (doctype_name, field_name).
Uses BACKTICK_FIELD_PARSE_REGEX for fast parsing.
Returns None if the notation is invalid.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| field_name | str | - | - |

**Returns**: `tuple[str, str] | None`


##### _validate_and_parse_field_for_clause(self, field_name: str, clause_name: str) → Field

Common helper to validate and parse field names for GROUP BY and ORDER BY clauses.

Args:
        field_name: The field name to validate and parse
        clause_name: Name of the SQL clause (for error messages) - 'Group By' or 'Order By'

Returns:
        Parsed Field object ready for use in pypika query

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| field_name | str | - | - |
| clause_name | str | - | - |

**Returns**: `Field`


##### _validate_group_by(self, group_by: str) → list[Field]

Validate the group_by string argument, apply joins for dynamic fields, and return parsed Field objects.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| group_by | str | - | - |

**Returns**: `list[Field]`


##### _validate_order_by(self, order_by: str) → list[tuple[Field | str, Order]]

Validate the order_by string argument, apply joins for dynamic fields, and return parsed Field objects with directions.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| order_by | str | - | - |

**Returns**: `list[tuple[Field | str, Order]]`


##### check_read_permission(self)

Check if user has read permission on the doctype

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _raise_permission_error(self, doctype = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doctype | None | None | - |


##### apply_field_permissions(self)

Filter the list of fields based on permlevel.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_user_permission_conditions(self, doctype: str | None = None, table: Table | None = None) → list[Criterion]

Build conditions for user permissions.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doctype | str | None | None | - |
| table | Table | None | None | - |

**Returns**: `list[Criterion]`


##### get_doctype_link_fields(self, doctype: str | None = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doctype | str | None | None | - |


##### add_permission_conditions(self)

Logic for adding permission conditions is as follows:

If no role permissions with read/select exist:
        - apply only share permissions

If role permissions with read/select exist:
        - apply (if_owner constraints OR user permissions), AND
        - apply permission query conditions

        If if_owner / user permission / permission query constraints are applied,
        final condition = (existing conditions) OR (share condtion)
        (rationale: shared documents trump all other restrictions)

        Else, all documents are accessible based on role permissions.

For child tables (when parent_doctype is specified):
        - permissions are checked against the parent doctype
        - for non-single parent doctypes: a join to the parent table is added,
                conditions reference parent fields
        - for single parent doctypes: all permissions are already checked by has_permission,
                we exit early without adding any conditions

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_permission_conditions(self, doctype: str, table: Table) → Criterion | None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doctype | str | - | - |
| table | Table | - | - |

**Returns**: `Criterion | None`


##### get_permission_query_conditions(self, doctype: str | None = None) → list['RawCriterion']

Add permission query conditions from hooks and server scripts

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doctype | str | None | None | - |

**Returns**: `list['RawCriterion']`


##### get_permission_type(self, doctype: str, parent_doctype: str | None = None) → Literal['read', 'select']

Get permission type (select/read) based on user permissions.

Args:
        doctype: The doctype to check permissions for.
        parent_doctype: The parent of the specified doctype. If passed, we assume that `doctype` is a child table,
                                        and fall back to checking permissions from this parent.

Returns:
        The allowed permission type (read|select).

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doctype | str | - | - |
| parent_doctype | str | None | None | - |

**Returns**: `Literal['read', 'select']`


##### requires_owner_constraint(self, role_permissions)

Return True if "select" or "read" isn't available without being creator.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| role_permissions | None | - | - |


##### _is_field_nullable(self, doctype: str, fieldname: str) → bool

Check if a field can contain NULL values.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doctype | str | - | - |
| fieldname | str | - | - |

**Returns**: `bool`


##### _get_ifnull_fallback(self, doctype: str, fieldname: str) → str

Get type-appropriate fallback value for NULL comparisons.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doctype | str | - | - |
| fieldname | str | - | - |

**Returns**: `str`


##### _should_apply_ifnull(self, doctype: str, fieldname: str, operator: str, value: Any) → bool

Determine if IFNULL wrapping is needed for a filter condition.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doctype | str | - | - |
| fieldname | str | - | - |
| operator | str | - | - |
| value | Any | - | - |

**Returns**: `bool`




### DynamicTableField

**Inherits from**: (none)

#### Methods

##### __init__(self, doctype: str, fieldname: str, parent_doctype: str, alias: str | None = None) → None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doctype | str | - | - |
| fieldname | str | - | - |
| parent_doctype | str | - | - |
| alias | str | None | None | - |

**Returns**: `None`


##### __str__(self) → str

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `str`


##### parse(field: str, doctype: str, allow_tab_notation: bool = True)

**Decorators**: `@staticmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| field | str | - | - |
| doctype | str | - | - |
| allow_tab_notation | bool | True | - |


##### apply_select(self, query: QueryBuilder, engine: 'Engine' = None) → QueryBuilder

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| query | QueryBuilder | - | - |
| engine | 'Engine' | None | - |

**Returns**: `QueryBuilder`


##### apply_join(self, query: QueryBuilder, engine: 'Engine' = None) → QueryBuilder

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| query | QueryBuilder | - | - |
| engine | 'Engine' | None | - |

**Returns**: `QueryBuilder`




### ChildTableField

**Inherits from**: DynamicTableField

#### Methods

##### __init__(self, doctype: str, fieldname: str, parent_doctype: str, parent_fieldname: str | None = None, alias: str | None = None) → None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doctype | str | - | - |
| fieldname | str | - | - |
| parent_doctype | str | - | - |
| parent_fieldname | str | None | None | - |
| alias | str | None | None | - |

**Returns**: `None`


##### apply_select(self, query: QueryBuilder, engine: 'Engine' = None) → QueryBuilder

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| query | QueryBuilder | - | - |
| engine | 'Engine' | None | - |

**Returns**: `QueryBuilder`


##### apply_join(self, query: QueryBuilder, engine: 'Engine' = None) → QueryBuilder

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| query | QueryBuilder | - | - |
| engine | 'Engine' | None | - |

**Returns**: `QueryBuilder`




### LinkTableField

**Inherits from**: DynamicTableField

#### Methods

##### __init__(self, doctype: str, fieldname: str, parent_doctype: str, link_fieldname: str, alias: str | None = None) → None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doctype | str | - | - |
| fieldname | str | - | - |
| parent_doctype | str | - | - |
| link_fieldname | str | - | - |
| alias | str | None | None | - |

**Returns**: `None`


##### apply_select(self, query: QueryBuilder, engine: 'Engine' = None) → QueryBuilder

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| query | QueryBuilder | - | - |
| engine | 'Engine' | None | - |

**Returns**: `QueryBuilder`


##### apply_join(self, query: QueryBuilder, engine: 'Engine' = None) → QueryBuilder

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| query | QueryBuilder | - | - |
| engine | 'Engine' | None | - |

**Returns**: `QueryBuilder`




### ChildQuery

**Inherits from**: (none)

#### Methods

##### __init__(self, fieldname: str, fields: list, parent_doctype: str) → None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| fieldname | str | - | - |
| fields | list | - | - |
| parent_doctype | str | - | - |

**Returns**: `None`


##### get_query(self, parent_names = None) → QueryBuilder

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| parent_names | None | None | - |

**Returns**: `QueryBuilder`




### RawCriterion

A class to represent raw SQL string as a criterion.

Allows using raw SQL strings in pypika queries:
        frappe.qb.from_("DocType").where(RawCriterion("name like 'a%'"))

**Inherits from**: Term

#### Methods

##### __init__(self, sql_string: str)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| sql_string | str | - | - |


##### get_sql(self) → str

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `str`


##### __and__(self, other)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| other | None | - | - |


##### __or__(self, other)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| other | None | - | - |


##### __invert__(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




### CombinedRawCriterion

**Inherits from**: RawCriterion

#### Methods

##### __init__(self, left, right, operator)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| left | None | - | - |
| right | None | - | - |
| operator | None | - | - |


##### get_sql(self) → str

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `str`




### SQLFunctionParser

Parser for SQL function dictionaries in query builder fields.

**Inherits from**: (none)

#### Methods

##### __init__(self, engine)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| engine | None | - | - |


##### is_function_dict(self, field_dict: dict) → bool

Check if a dictionary represents a SQL function definition.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| field_dict | dict | - | - |

**Returns**: `bool`


##### is_operator_dict(self, field_dict: dict) → bool

Check if a dictionary represents an arithmetic operator expression.

Example: {"ADD": [1, 2], "as": "sum"} or {"DIV": ["total", "count"]}

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| field_dict | dict | - | - |

**Returns**: `bool`


##### _extract_dict_components(self, d: dict, valid_keys: dict, error_msg: str) → tuple

Extract name, alias, and args from function/operator dict.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| d | dict | - | - |
| valid_keys | dict | - | - |
| error_msg | str | - | - |

**Returns**: `tuple`


##### parse_function(self, function_dict: dict) → Field

Parse a SQL function dictionary into a pypika function call.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| function_dict | dict | - | - |

**Returns**: `Field`


##### parse_operator(self, operator_dict: dict) → ArithmeticExpression

Parse an arithmetic operator dictionary into a pypika ArithmeticExpression.

Operators require exactly 2 arguments (left and right operands).
Arguments can be: numbers, field names, nested functions, or nested operators.
Example: {"DIV": [1, {"NULLIF": [{"LOCATE": ["'test'", "name"]}, 0]}]}

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| operator_dict | dict | - | - |

**Returns**: `ArithmeticExpression`


##### _parse_and_validate_argument(self, arg)

Parse and validate a single function/operator argument against SQL injection.

Supports:
- Numbers: 1, 2.5, etc.
- Strings: field names or quoted literals
- Nested dicts: functions {"COUNT": "name"} or operators {"ADD": [1, 2]}

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| arg | None | - | - |


##### _validate_string_argument(self, arg: str)

Validate string arguments to prevent SQL injection.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| arg | str | - | - |


##### _is_valid_field_name(self, name: str) → bool

Check if a string is a valid field name.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| name | str | - | - |

**Returns**: `bool`


##### _validate_alias(self, alias: str)

Validate alias name for SQL injection.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| alias | str | - | - |


##### _check_function_field_permission(self, field_name: str)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| field_name | str | - | - |




## Functions

### _apply_date_field_filter_conversion(value, operator: str, doctype: str, field)

Apply datetime to date conversion for Date fieldtype filters.

This matches db_query behavior where datetime values are truncated to dates
when filtering on Date fields, for all operators (not just 'between').

Args:
        value: The filter value (can be datetime, tuple of datetimes, or other)
        operator: The operator being used (between, >, <, etc.)
        doctype: The doctype to get field metadata from
        field: The field name or pypika Field object

Returns:
        The converted value with datetimes converted to dates if field is Date type

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| value | None | - | - |
| operator | str | - | - |
| doctype | str | - | - |
| field | None | - | - |

**Returns**: (none)



### _apply_datetime_field_filter_conversion(between_values: tuple | list, doctype: str, field) → tuple

Apply date to datetime conversion for Datetime fields with 'between' operator.

Args:
        between_values: Tuple/list of two values [from, to] for between filter
        doctype: DocType name
        field: Field name or pypika Field object

Returns:
        Tuple with dates expanded to datetime ranges for Datetime fields

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| between_values | tuple | list | - | - |
| doctype | str | - | - |
| field | None | - | - |

**Returns**: `tuple`



### get_nested_set_hierarchy_result(doctype: str, name: str, hierarchy: str) → list[str]

Get matching nodes based on operator.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | str | - | - |
| name | str | - | - |
| hierarchy | str | - | - |

**Returns**: `list[str]`



### _is_function_call(field_str: str) → bool

Check if a string is a SQL function call.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| field_str | str | - | - |

**Returns**: `bool`



### _validate_select_field(field: str)

Validate a field string intended for use in a SELECT clause.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| field | str | - | - |

**Returns**: (none)



### has_permission(ptype)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| ptype | None | - | - |

**Returns**: (none)


