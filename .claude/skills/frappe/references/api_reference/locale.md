# API Reference: locale.py

**Language**: Python

**Source**: `locale.py`

---

## Functions

### get_number_format(language: str | None = None) → NumberFormat

Return the number format for the given language.

:param language: The language code to get the value for. Defaults to the current user's language.
:return: The number format. Defaults to "#,###.##" if not found.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| language | str | None | None | - |

**Returns**: `NumberFormat`



### get_date_format(language: str | None = None) → str

Return the date format for the given language.

:param language: The language code to get the value for. Defaults to the current user's language.
:return: The date format string. Defaults to "yyyy-mm-dd" if not found.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| language | str | None | None | - |

**Returns**: `str`



### get_time_format(language: str | None = None) → str

Return the time format for the given language.

:param language: The language code to get the value for. Defaults to the current user's language.
:return: The time format string. Defaults to "HH:mm:ss" if not found.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| language | str | None | None | - |

**Returns**: `str`



### get_first_day_of_the_week(language: str | None = None) → str

Return the first day of the week for the given language.

:param language: The language code to get the value for. Defaults to the current user's language.
:return: The first day of the week. Defaults to "Sunday" if not found.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| language | str | None | None | - |

**Returns**: `str`



### get_locale_value(key: str, language: str | None = None) → str | None

Return the value of the key from the Language record or System Settings.

:param key: The settings key to get the value for.
:param language: The language code to get the value for. Defaults to the current user's language.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| key | str | - | - |
| language | str | None | None | - |

**Returns**: `str | None`


