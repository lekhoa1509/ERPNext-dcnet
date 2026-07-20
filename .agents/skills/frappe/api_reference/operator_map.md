# API Reference: operator_map.py

**Language**: Python

**Source**: `database/operator_map.py`

---

## Functions

### like(key: Field, value: str) → frappe.qb

Wrapper method for `LIKE`

Args:
        key (str): field
        value (str): criterion

Return:
        frappe.qb: `frappe.qb` object with `LIKE`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| key | Field | - | - |
| value | str | - | - |

**Returns**: `frappe.qb`



### ilike(key: Field, value: str) → frappe.qb

Wrapper method for `ILIKE`
Args:
        key (str): field
        value (str): criterion
Return:
        frappe.qb: `frappe.qb` object with `ILIKE`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| key | Field | - | - |
| value | str | - | - |

**Returns**: `frappe.qb`



### func_in(key: Field, value: list | tuple) → frappe.qb

Wrapper method for `IN`.

Args:
        key (str): field
        value (Union[int, str]): criterion

Return:
        frappe.qb: `frappe.qb` object with `IN`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| key | Field | - | - |
| value | list | tuple | - | - |

**Returns**: `frappe.qb`



### not_like(key: Field, value: str) → frappe.qb

Wrapper method for `NOT LIKE`.

Args:
        key (str): field
        value (str): criterion

Return:
        frappe.qb: `frappe.qb` object with `NOT LIKE`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| key | Field | - | - |
| value | str | - | - |

**Returns**: `frappe.qb`



### func_not_in(key: Field, value: list | tuple | str)

Wrapper method for `NOT IN`.

Args:
        key (str): field
        value (Union[int, str]): criterion

Return:
        frappe.qb: `frappe.qb` object with `NOT IN`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| key | Field | - | - |
| value | list | tuple | str | - | - |

**Returns**: (none)



### func_regex(key: Field, value: str) → frappe.qb

Wrapper method for `REGEX`

Args:
        key (str): field
        value (str): criterion

Return:
        frappe.qb: `frappe.qb` object with `REGEX`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| key | Field | - | - |
| value | str | - | - |

**Returns**: `frappe.qb`



### func_between(key: Field, value: list | tuple) → frappe.qb

Wrapper method for `BETWEEN`.

Args:
        key (str): field
        value (Union[int, str]): criterion

Return:
        frappe.qb: `frappe.qb` object with `BETWEEN`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| key | Field | - | - |
| value | list | tuple | - | - |

**Returns**: `frappe.qb`



### func_is(key, value)

Wrapper for IS

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| key | None | - | - |
| value | None | - | - |

**Returns**: (none)



### func_timespan(key: Field, value: str) → frappe.qb

Wrapper method for `TIMESPAN`.

Args:
        key (str): field
        value (str): criterion

Return:
        frappe.qb: `frappe.qb` object with `TIMESPAN`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| key | Field | - | - |
| value | str | - | - |

**Returns**: `frappe.qb`


