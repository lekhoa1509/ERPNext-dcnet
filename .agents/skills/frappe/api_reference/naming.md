# API Reference: naming.py

**Language**: Python

**Source**: `model/naming.py`

---

## Classes

### InvalidNamingSeriesError

**Inherits from**: frappe.ValidationError



### InvalidUUIDValue

**Inherits from**: frappe.ValidationError



### NamingSeries

**Inherits from**: (none)

#### Methods

##### __init__(self, series: str)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| series | str | - | - |


##### validate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### generate_next_name(self, doc: 'Document') → str

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doc | 'Document' | - | - |

**Returns**: `str`


##### get_prefix(self) → str

Naming series stores prefix to maintain a counter in DB. This prefix can be used to update counter or validations.

e.g. `SINV-.YY.-.####` has prefix of `SINV-22-` in database for year 2022.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `str`


##### get_preview(self, doc = None) → list[str]

Generate preview of naming series without using DB counters

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doc | None | None | - |

**Returns**: `list[str]`


##### update_counter(self, new_count: int) → None

Warning: Incorrectly updating series can result in unusable transactions

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| new_count | int | - | - |

**Returns**: `None`


##### get_current_value(self) → int

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `int`




## Functions

### set_new_name(doc)

Sets the `name` property for the document based on various rules.

1. If amended doc, set suffix.
2. If `autoname` method is declared, then call it.
3. If `autoname` property is set in the DocType (`meta`), then build it using the `autoname` property.
4. If no rule defined, use hash.

:param doc: Document to be named.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |

**Returns**: (none)



### is_autoincremented(doctype: str, meta: 'Meta' | None = None) → bool

Checks if the doctype has autoincrement autoname set

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | str | - | - |
| meta | 'Meta' | None | None | - |

**Returns**: `bool`



### set_name_from_naming_options(autoname, doc)

Get a name based on the autoname field option

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| autoname | None | - | - |
| doc | None | - | - |

**Returns**: (none)



### set_naming_from_document_naming_rule(doc)

Evaluate rules based on "Document Naming Series" doctype

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |

**Returns**: (none)



### set_name_by_naming_series(doc)

Sets name by the `naming_series` property

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |

**Returns**: (none)



### make_autoname(key = '', doctype = '', doc = '')

     Creates an autoname from the given key:

     **Autoname rules:**

              * The key is separated by '.'
              * '####' represents a series. The string before this part becomes the prefix:
                     Example: ABC.#### creates a series ABC0001, ABC0002 etc
              * 'MM' represents the current month
              * 'YY' and 'YYYY' represent the current year


*Example:*

              * DE./.YY./.MM./.##### will create a series like
                DE/09/01/00001 where 09 is the year, 01 is the month and 00001 is the series

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| key | None | '' | - |
| doctype | None | '' | - |
| doc | None | '' | - |

**Returns**: (none)



### _get_timestamp_prefix()

**Returns**: (none)



### _generate_random_string(length = 10)

Better version of frappe.generate_hash for naming.

This uses entire base32 instead of base16 used by generate_hash. So it has twice as many
characters and hence more likely to have shorter common prefixes. i.e. slighly faster comparisons and less conflicts.

Why not base36?
It's not in standard library else using all characters is probably better approach.
Why not base64?
MySQL is case-insensitive, we can't use both upper and lower case characters.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| length | None | 10 | - |

**Returns**: (none)



### parse_naming_series(parts: list[str] | str, doctype = None, doc: 'Document' | None = None, number_generator: Callable[[str, int], str] | None = None) → str

Parse the naming series and get next name.

args:
        parts: naming series parts (split by `.`)
        doc: document to use for series that have parts using fieldnames
        number_generator: Use different counter backend other than `tabSeries`. Primarily used for testing.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| parts | list[str] | str | - | - |
| doctype | None | None | - |
| doc | 'Document' | None | None | - |
| number_generator | Callable[[str, int], str] | None | None | - |

**Returns**: `str`



### has_custom_parser(e)

Return True if the naming series part has a custom parser.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| e | None | - | - |

**Returns**: (none)



### determine_consecutive_week_number(datetime)

Determines the consecutive calendar week

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| datetime | None | - | - |

**Returns**: (none)



### getseries(key, digits)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| key | None | - | - |
| digits | None | - | - |

**Returns**: (none)



### revert_series_if_last(key, name, doc = None)

Reverts the series for particular naming series:
* key is naming series          - SINV-.YYYY-.####
* name is actual name           - SINV-2021-0001

1. This function split the key into two parts prefix (SINV-YYYY) & hashes (####).
2. Use prefix to get the current index of that naming series from Series table
3. Then revert the current index.

*For custom naming series:*
1. hash can exist anywhere, if it exist in hashes then it take normal flow.
2. If hash doesn't exit in hashes, we get the hash from prefix, then update name and prefix accordingly.

*Example:*
        1. key = SINV-.YYYY.-
                * If key doesn't have hash it will add hash at the end
                * prefix will be SINV-YYYY based on this will get current index from Series table.
        2. key = SINV-.####.-2021
                * now prefix = SINV-#### and hashes = 2021 (hash doesn't exist)
                * will search hash in key then accordingly get prefix = SINV-
        3. key = ####.-2021
                * prefix = #### and hashes = 2021 (hash doesn't exist)
                * will search hash in key then accordingly get prefix = ""

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| key | None | - | - |
| name | None | - | - |
| doc | None | None | - |

**Returns**: (none)



### get_default_naming_series(doctype: str) → str | None

get default value for `naming_series` property

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | str | - | - |

**Returns**: `str | None`



### validate_name(doctype: str, name: int | str)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | str | - | - |
| name | int | str | - | - |

**Returns**: (none)



### append_number_if_name_exists(doctype, value, fieldname = 'name', separator = '-', filters = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| value | None | - | - |
| fieldname | None | 'name' | - |
| separator | None | '-' | - |
| filters | None | None | - |

**Returns**: (none)



### _set_amended_name(doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |

**Returns**: (none)



### _field_autoname(autoname, doc, skip_slicing = None)

Generate a name using `DocType` field. This is called when the doctype's
`autoname` field starts with 'field:'

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| autoname | None | - | - |
| doc | None | - | - |
| skip_slicing | None | None | - |

**Returns**: (none)



### _prompt_autoname(autoname, doc)

Generate a name using Prompt option. This simply means the user will have to set the name manually.
This is called when the doctype's `autoname` field starts with 'prompt'.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| autoname | None | - | - |
| doc | None | - | - |

**Returns**: (none)



### _format_autoname(autoname: str, doc)

Generate autoname by replacing all instances of braced params (fields, date params ('DD', 'MM', 'YY'), series)
Independent of remaining string or separators.

Example pattern: 'format:LOG-{MM}-{fieldname1}-{fieldname2}-{#####}'

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| autoname | str | - | - |
| doc | None | - | - |

**Returns**: (none)



### get_param_value_for_match(match)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| match | None | - | - |

**Returns**: (none)



### fake_counter_backend(partial_series, digits)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| partial_series | None | - | - |
| digits | None | - | - |

**Returns**: (none)



### fake_counter(_prefix, digits)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| _prefix | None | - | - |
| digits | None | - | - |

**Returns**: (none)


