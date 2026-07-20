# API Reference: test_doctype.py

**Language**: Python

**Source**: `core/doctype/doctype/test_doctype.py`

---

## Classes

### TestDocType

**Inherits from**: IntegrationTestCase

#### Methods

##### tearDown(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_validate_name(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_making_sequence_on_change(self)

**Decorators**: `@skipIf(frappe.conf.db_type == 'sqlite', 'Not for SQLite for now')`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_doctype_unique_constraint_dropped(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_validate_search_fields(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_depends_on_fields(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_all_depends_on_fields_conditions(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_sync_field_order(self)

**Decorators**: `@unittest.skipUnless(os.access(frappe.get_app_path('frappe'), os.W_OK), 'Only run if frappe app paths is writable')`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_unique_field_name_for_two_fields(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_fieldname_is_not_name(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_illegal_mandatory_validation(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_link_with_wrong_and_no_options(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_hidden_and_mandatory_without_default(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_field_can_not_be_indexed_validation(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_cancel_link_doctype(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_ignore_cancelation_of_linked_doctype_during_cancel(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_links_table_fieldname_validation(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_create_virtual_doctype(self)

Test virtual DocType.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_create_virtual_doctype_as_child_table(self)

Test virtual DocType as Child Table below a normal DocType.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_default_fieldname(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_autoincremented_doctype_transition(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_json_field(self)

Test json field.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_no_delete_doc(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_export_types(self)

Export python types.

**Decorators**: `@unittest.skipUnless(os.access(frappe.get_app_path('frappe'), os.W_OK), 'Only run if frappe app paths is writable')`, `@patch.dict(frappe.conf, {'developer_mode': 1})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_custom_field_deletion(self)

Custom child tables whose doctype doesn't exist should be auto deleted.

**Decorators**: `@unittest.skipUnless(os.access(frappe.get_app_path('frappe'), os.W_OK), 'Only run if frappe app paths is writable')`, `@patch.dict(frappe.conf, {'developer_mode': 1})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_delete_doctype_with_customization(self)

**Decorators**: `@unittest.skipUnless(os.access(frappe.get_app_path('frappe'), os.W_OK), 'Only run if frappe app paths is writable')`, `@patch.dict(frappe.conf, {'developer_mode': 1})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_delete_orphaned_doctypes(self)

**Decorators**: `@unittest.skipUnless(os.access(frappe.get_app_path('frappe'), os.W_OK), 'Only run if frappe app paths is writable')`, `@patch.dict(frappe.conf, {'developer_mode': 1})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_not_in_list_view_for_not_allowed_mandatory_field(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_no_recursive_fetch(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_meta_serialization(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_row_compression(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_decimal_field_configuration(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_decimal_field_precision_exceeds_length(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_delete_doc_clears_cache(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### new_doctype(name: str | None = None, unique: bool = False, depends_on: str = '', fields: list[dict] | None = None, custom: bool = True, default: str | None = None) → 'DocType'

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| name | str | None | None | - |
| unique | bool | False | - |
| depends_on | str | '' | - |
| fields | list[dict] | None | None | - |
| custom | bool | True | - |
| default | str | None | None | - |

**Returns**: `'DocType'`



### validate(code)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| code | None | - | - |

**Returns**: (none)



### get_format(dt)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| dt | None | - | - |

**Returns**: (none)


