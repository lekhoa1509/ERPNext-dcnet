# API Reference: translations.py

**Language**: Python

**Source**: `utils/translations.py`

---

## Functions

### _(msg: str, lang: str | None = None, context: str | None = None) → str

Return translated string in current lang, if exists.
Usage:
        _('Change')
        _('Change', context='Coins')

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| msg | str | - | - |
| lang | str | None | None | - |
| context | str | None | None | - |

**Returns**: `str`



### _lt(msg: str, lang: str | None = None, context: str | None = None)

Lazily translate a string.


This function returns a "lazy string" which when casted to string via some operation applies
translation first before casting.

This is only useful for translating strings in global scope or anything that potentially runs
before `frappe.init()`

Note: Result is not guaranteed to equivalent to pure strings for all operations.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| msg | str | - | - |
| lang | str | None | None | - |
| context | str | None | None | - |

**Returns**: (none)



### set_user_lang(user: str, user_language: str | None = None) → None

Guess and set user language for the session. `frappe.local.lang`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| user | str | - | - |
| user_language | str | None | None | - |

**Returns**: `None`


