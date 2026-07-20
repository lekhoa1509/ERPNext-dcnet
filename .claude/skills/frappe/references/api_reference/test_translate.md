# API Reference: test_translate.py

**Language**: Python

**Source**: `tests/test_translate.py`

---

## Classes

### TestTranslate

**Inherits from**: IntegrationTestCase

#### Methods

##### setUp(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### tearDown(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_clear_cache(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_extract_message_from_file(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_read_language_variant(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_translation_with_context(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_lazy_translations(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_request_language_resolution_with_form_dict(self)

Test for frappe.translate.get_language

Case 1: frappe.form_dict._lang is set

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_request_language_resolution_with_cookie(self)

Test for frappe.translate.get_language

Case 2: frappe.form_dict._lang is not set, but preferred_language cookie is

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_guest_request_language_resolution_with_cookie(self)

Test for frappe.translate.get_language

Case 3: frappe.form_dict._lang is not set, but preferred_language cookie is [Guest User]

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_global_translations(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_guest_request_language_resolution_with_request_header(self)

Test for frappe.translate.get_language

Case 4: frappe.form_dict._lang & preferred_language cookie is not set, but Accept-Language header is [Guest User]

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_request_language_resolution_with_request_header(self)

Test for frappe.translate.get_language

Case 5: frappe.form_dict._lang & preferred_language cookie is not set, but Accept-Language header is

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_load_all_translate_files(self)

Load all CSV files to ensure they have correct format

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_python_extractor(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_js_extractor(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_js_parser_arg_capturing(self)

Get non-flattened args in correct order so 3rd arg if present is always context.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### verify_translation_files(app)

Function to verify translation file syntax in app.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| app | None | - | - |

**Returns**: (none)



### get_args(code)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| code | None | - | - |

**Returns**: (none)


