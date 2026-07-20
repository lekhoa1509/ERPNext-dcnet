# API Reference: document_naming_settings.py

**Language**: Python

**Source**: `core/doctype/document_naming_settings/document_naming_settings.py`

---

## Classes

### NamingSeriesNotSetError

**Inherits from**: frappe.ValidationError



### DocumentNamingSettings

**Inherits from**: Document

#### Methods

##### get_transactions_and_prefixes(self)

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _get_transactions(self) → list[str]

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `list[str]`


##### _get_prefixes(self, doctypes) → list[str]

Get all prefixes for naming series.

- For all templates prefix is evaluated considering today's date
- All existing prefix in DB are shared as is.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doctypes | None | - | - |

**Returns**: `list[str]`


##### _evaluate_and_clean_templates(self, series_templates: set[str]) → list[str]

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| series_templates | set[str] | - | - |

**Returns**: `list[str]`


##### get_options_list(self, options: str) → list[str]

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| options | str | - | - |

**Returns**: `list[str]`


##### update_series(self)

update series list

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_set_series(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_series_options_in_meta(self, doctype: str, options: str) → None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doctype | str | - | - |
| options | str | - | - |

**Returns**: `None`


##### update_naming_series_property_setter(self, doctype, property, value)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doctype | None | - | - |
| property | None | - | - |
| value | None | - | - |


##### check_duplicate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_series_name(self, series)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| series | None | - | - |


##### get_options(self, doctype = None)

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doctype | None | None | - |


##### get_current(self)

get series current

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_amendment_rule(self)

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_series_start(self)

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### create_version_log_for_change(self, series, old, new)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| series | None | - | - |
| old | None | - | - |
| new | None | - | - |


##### preview_series(self) → str

Preview what the naming series will generate.

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `str`


##### _fetch_last_doc_if_available(self)

Fetch last doc for evaluating naming series with fields.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### stripped_series(s: str) → str

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| s | str | - | - |

**Returns**: `str`


