# API Reference: user_doctype_permissions.py

**Language**: Python

**Source**: `core/report/user_doctype_permissions/user_doctype_permissions.py`

---

## Functions

### execute(filters = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | None | None | - |

**Returns**: (none)



### get_columns() → list[dict]

Return a list of columns for this report.

The first two columns are *DocType* and *Is Owner*. The remaining ones each
represent a permission type.

**Returns**: `list[dict]`



### get_data(user: str) → list[list]

Return the data for this report.

This function retrieves the permissions data for a given user. It aggregates
the permission values by doctype and if_owner flag, and returns the data as
a list of lists.

Args:
        user (str): The user for whom to retrieve the permissions.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| user | str | - | - |

**Returns**: `list[list]`


