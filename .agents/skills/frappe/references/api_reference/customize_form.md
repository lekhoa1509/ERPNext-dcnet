# API Reference: customize_form.py

**Language**: Python

**Source**: `custom/doctype/customize_form/customize_form.py`

---

## Classes

### CustomizeForm

**Inherits from**: Document

#### Methods

##### on_update(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### fetch_to_customize(self)

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_doctype(self, meta)

Check if the doctype is allowed to be customized.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| meta | None | - | - |


##### load_properties(self, meta)

Load the customize object (this) with the metadata properties

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| meta | None | - | - |


##### create_auto_repeat_custom_field_if_required(self, meta)

Create auto repeat custom field if it's not already present

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| meta | None | - | - |


##### get_name_translation(self)

Get translation object if exists of current doctype name in the default language

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_name_translation(self)

Create, update custom translation for this doctype

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### clear_existing_doc(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### save_customization(self)

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_property_setters(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_property_setter_for_field_order(self, meta)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| meta | None | - | - |


##### set_property_setters_for_doctype(self, meta)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| meta | None | - | - |


##### set_property_setters_for_docfield(self, meta, df, meta_df)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| meta | None | - | - |
| df | None | - | - |
| meta_df | None | - | - |


##### allow_property_change(self, prop, meta_df, df)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| prop | None | - | - |
| meta_df | None | - | - |
| df | None | - | - |


##### set_property_setters_for_actions_and_links(self, meta)

Apply property setters or create custom records for DocType Action and DocType Link

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| meta | None | - | - |


##### update_order_property_setter(self, has_custom, fieldname)

We need to maintain the order of the link/actions if the user has shuffled them.
So we create a new property (ex `links_order`) to keep a list of items.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| has_custom | None | - | - |
| fieldname | None | - | - |


##### clear_removed_items(self, doctype, items)

Clear rows that do not appear in `items`. These have been removed by the user.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doctype | None | - | - |
| items | None | - | - |


##### update_custom_fields(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### add_custom_field(self, df, i)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| df | None | - | - |
| i | None | - | - |


##### update_in_custom_field(self, df, i)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| df | None | - | - |
| i | None | - | - |


##### delete_custom_fields(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### make_property_setter(self, prop, value, property_type, fieldname = None, apply_on = None, row_name = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| prop | None | - | - |
| value | None | - | - |
| property_type | None | - | - |
| fieldname | None | None | - |
| apply_on | None | None | - |
| row_name | None | None | - |


##### get_existing_property_value(self, property_name, fieldname = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| property_name | None | - | - |
| fieldname | None | None | - |


##### validate_fieldtype_change(self, df, old_value, new_value)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| df | None | - | - |
| old_value | None | - | - |
| new_value | None | - | - |


##### validate_fieldtype_length(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### reset_to_defaults(self)

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### reset_layout(self)

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### trim_table(self)

Removes database fields that don't exist in the doctype.

This may be needed as maintenance since removing a field in a DocType
doesn't automatically delete the db field.

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### allow_fieldtype_change(self, old_type: str, new_type: str) → bool

allow type change, if both old_type and new_type are in same field group.
field groups are defined in ALLOWED_FIELDTYPE_CHANGE variables.

**Decorators**: `@classmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| old_type | str | - | - |
| new_type | str | - | - |

**Returns**: `bool`




## Functions

### get_orphaned_columns(doctype: str)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | str | - | - |

**Returns**: (none)



### reset_customization(doctype)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |

**Returns**: (none)



### is_standard_or_system_generated_field(df)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| df | None | - | - |

**Returns**: (none)



### get_link_filters_from_doc_without_customisations(doctype, fieldname)

Get the filters of a link field from a doc without customisations
In backend the customisations are not applied.
Customisations are applied in the client side.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| fieldname | None | - | - |

**Returns**: (none)



### in_field_group(group)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| group | None | - | - |

**Returns**: (none)


