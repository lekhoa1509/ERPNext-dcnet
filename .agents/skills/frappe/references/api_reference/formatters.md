# API Reference: formatters.py

**Language**: Python

**Source**: `utils/formatters.py`

---

## Functions

### format_value(value, df = None, doc = None, currency = None, translated = False, format = None)

Format value based on given fieldtype, document reference, currency reference.
If docfield info (df) is not given, it will try and guess based on the datatype of the value.

:param value: Value to be formatted.
:param df: (Optional) DocField object with properties `fieldtype`, `options` etc.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| value | None | - | - |
| df | None | None | - |
| doc | None | None | - |
| currency | None | None | - |
| translated | None | False | - |
| format | None | None | - |

**Returns**: (none)


