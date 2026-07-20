# API Reference: qb_query.py

**Language**: Python

**Source**: `model/qb_query.py`

---

## Classes

### DatabaseQuery

Copy of db_query.py DatabaseQuery, using query builder instead.

**Inherits from**: (none)

#### Methods

##### __init__(self, doctype: str) → None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doctype | str | - | - |

**Returns**: `None`


##### execute(self, fields: list[str] | tuple[str, ...] | str | None = None, filters: dict[str, FilterValue] | FilterValue | list[list | FilterValue] | None = None, or_filters: dict[str, FilterValue] | FilterValue | list[list | FilterValue] | None = None, group_by: str | None = None, order_by: str = DefaultOrderBy, limit: int | None = None, offset: int | None = None, limit_start: int = 0, limit_page_length: int | None = None, as_list: bool = False, with_childnames: bool = False, debug: bool = False, ignore_permissions: bool = False, user: str | None = None, with_comment_count: bool = False, join: str = 'left join', distinct: bool = False, start: int | None = None, page_length: int | None = None, ignore_ifnull: bool = False, save_user_settings: bool = False, save_user_settings_fields: bool = False, update: dict[str, Any] | None = None, user_settings: str | dict[str, Any] | None = None, reference_doctype: str | None = None, run: bool = True, strict: bool = True, pluck: str | None = None, ignore_ddl: bool = False) → list

Execute a database query using the Query Builder engine.

Args:
        fields: Fields to select. Can be a list, tuple, or comma-separated string.
        filters: Main filter conditions. Supports dicts, lists, and operator tuples.
        or_filters: Additional filter conditions to be combined with OR.
        group_by: Fields to group results by.
        order_by: Fields to order results by.
        limit: Maximum number of records to return.
        offset: Number of records to skip for pagination.
        limit_start: Legacy pagination start (deprecated, use offset).
        limit_page_length: Legacy pagination length (deprecated, use limit).
        as_list: Return results as list of lists instead of list of dicts.
        with_childnames: Include child document names (not implemented).
        debug: Enable debug mode for query inspection.
        ignore_permissions: Skip permission checks for the query.
        user: Execute query as specific user.
        with_comment_count: Add comment count to results (_comment_count field).
        join: Type of join for related tables (QB engine auto-determines optimal joins).
        distinct: Return only distinct results.
        start: Legacy alias for limit_start (deprecated).
        page_length: Legacy alias for limit_page_length (deprecated).
        ignore_ifnull: Skip IFNULL wrapping (QB engine handles NULL optimization automatically).
        save_user_settings: Save current query settings for user.
        save_user_settings_fields: Save field selection in user settings.
        update: Dictionary to merge into each result when as_list=False.
        user_settings: Custom user settings as JSON string or dict.
        reference_doctype: Reference doctype for contextual user permissions.
        run: Execute query immediately (True) or return query object (False).
        strict: Enable strict mode for query validation (legacy compatibility).
        pluck: Extract single field values as a simple list.
        ignore_ddl: Ignore DDL operations during query execution (legacy compatibility).
        parent_doctype: Parent doctype for child table queries.
        ignore_user_permissions: Ignore user permissions for the query.
                Useful for link search queries when the link field has `ignore_user_permissions` set.

Returns:
        Query results as list of dicts (default) or list of lists (as_list=True).
        If pluck is specified, returns list of field values.
        If run=False, returns query object instead of results.

Raises:
        ValidationError: For invalid parameters or query structure.
        PermissionError: When user lacks required permissions.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| fields | list[str] | tuple[str, ...] | str | None | None | - |
| filters | dict[str, FilterValue] | FilterValue | list[list | FilterValue] | None | None | - |
| or_filters | dict[str, FilterValue] | FilterValue | list[list | FilterValue] | None | None | - |
| group_by | str | None | None | - |
| order_by | str | DefaultOrderBy | - |
| limit | int | None | None | - |
| offset | int | None | None | - |
| limit_start | int | 0 | - |
| limit_page_length | int | None | None | - |
| as_list | bool | False | - |
| with_childnames | bool | False | - |
| debug | bool | False | - |
| ignore_permissions | bool | False | - |
| user | str | None | None | - |
| with_comment_count | bool | False | - |
| join | str | 'left join' | - |
| distinct | bool | False | - |
| start | int | None | None | - |
| page_length | int | None | None | - |
| ignore_ifnull | bool | False | - |
| save_user_settings | bool | False | - |
| save_user_settings_fields | bool | False | - |
| update | dict[str, Any] | None | None | - |
| user_settings | str | dict[str, Any] | None | None | - |
| reference_doctype | str | None | None | - |
| run | bool | True | - |
| strict | bool | True | - |
| pluck | str | None | None | - |
| ignore_ddl | bool | False | - |

**Returns**: `list`


##### _add_comment_count(self, result: list[Any]) → None

Add comment count to each result row by parsing _comments field.

This method adds a _comment_count field to each row based on the _comments field content.
It parses the JSON structure to count the number of comments.

Args:
        result: List of result dictionaries to modify

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| result | list[Any] | - | - |

**Returns**: `None`


##### _save_user_settings(self, user_settings: dict[str, Any] | None, user_settings_fields: list[str] | None, save_user_settings_fields: bool) → None

Save user settings for the current query.

This method stores user preferences for field selections and other query parameters
to provide a personalized experience for repeated queries.

Args:
        user_settings: Custom user settings to save
        user_settings_fields: Field list to save if save_user_settings_fields is True
        save_user_settings_fields: Whether to save the field selection

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| user_settings | dict[str, Any] | None | - | - |
| user_settings_fields | list[str] | None | - | - |
| save_user_settings_fields | bool | - | - |

**Returns**: `None`


##### _handle_virtual_doctype(self, fields: list[str] | tuple[str, ...] | str | None, filters: dict[str, FilterValue] | FilterValue | list[list | FilterValue] | None, or_filters: dict[str, FilterValue] | FilterValue | list[list | FilterValue] | None, start: int | None, offset: int | None, limit_start: int, page_length: int | None, limit: int | None, limit_page_length: int | None, order_by: str, as_list: bool, with_comment_count: bool, save_user_settings: bool, save_user_settings_fields: bool, pluck: str | None, parent_doctype: str | None) → list

Handle virtual doctype queries by delegating to controller.get_list().

Virtual doctypes don't have database tables and use controller methods
to generate data dynamically. Converts filters to Filters objects and
calls the doctype controller's get_list method.

Returns:
        List of results from controller.get_list()

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| fields | list[str] | tuple[str, ...] | str | None | - | - |
| filters | dict[str, FilterValue] | FilterValue | list[list | FilterValue] | None | - | - |
| or_filters | dict[str, FilterValue] | FilterValue | list[list | FilterValue] | None | - | - |
| start | int | None | - | - |
| offset | int | None | - | - |
| limit_start | int | - | - |
| page_length | int | None | - | - |
| limit | int | None | - | - |
| limit_page_length | int | None | - | - |
| order_by | str | - | - |
| as_list | bool | - | - |
| with_comment_count | bool | - | - |
| save_user_settings | bool | - | - |
| save_user_settings_fields | bool | - | - |
| pluck | str | None | - | - |
| parent_doctype | str | None | - | - |

**Returns**: `list`



