# API Reference: utils.py

**Language**: Python

**Source**: `utils.py`

---

## Functions

### before_tests()

**Returns**: (none)



### get_pegged_currencies()

**Returns**: (none)



### get_pegged_rate(pegged_map, from_currency, to_currency, transaction_date = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| pegged_map | None | - | - |
| from_currency | None | - | - |
| to_currency | None | - | - |
| transaction_date | None | None | - |

**Returns**: (none)



### get_exchange_rate(from_currency, to_currency, transaction_date = None, args = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| from_currency | None | - | - |
| to_currency | None | - | - |
| transaction_date | None | None | - |
| args | None | None | - |

**Returns**: (none)



### format_ces_api(data, param)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| data | None | - | - |
| param | None | - | - |

**Returns**: (none)



### enable_all_roles_and_domains()

enable all roles and domain for testing

**Returns**: (none)



### _enable_all_roles_for_admin()

**Returns**: (none)



### set_defaults_for_tests()

**Returns**: (none)



### insert_record(records)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| records | None | - | - |

**Returns**: (none)



### welcome_email()

**Returns**: (none)



### identity(x)

Used for redefining the translation function to return the string as is.

We want to create english records but still mark the strings as translatable.
E.g. when the respective DocTypes have 'Translate Link Fields' enabled or
we're creating custom fields.

Use like this: `from erpnext.setup.utils import identity as _`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| x | None | - | - |

**Returns**: (none)


