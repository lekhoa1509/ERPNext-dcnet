# API Reference: meta.py

**Language**: Python

**Source**: `model/meta.py`

---

## Classes

### Meta

**Inherits from**: Document

#### Methods

##### __init__(self, doctype: 'str | DocType')

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doctype | 'str | DocType' | - | - |


##### load_from_db(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### process(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### as_dict(self, no_nulls = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| no_nulls | None | False | - |


##### get_link_fields(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_data_fields(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_phone_fields(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_dynamic_link_fields(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_masked_fields(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _dynamic_link_fields(self)

**Decorators**: `@cached_property`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_select_fields(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_image_fields(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_code_fields(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_set_only_once_fields(self)

Return fields with `set_only_once` set

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _set_only_once_fields(self)

**Decorators**: `@cached_property`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_table_fields(self, include_computed = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| include_computed | None | False | - |


##### get_global_search_fields(self)

Return list of fields with `in_global_search` set and `name` if set.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_valid_columns(self) → list[str]

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `list[str]`


##### _valid_columns(self)

**Decorators**: `@cached_property`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_valid_fields(self) → list[str]

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `list[str]`


##### _valid_fields(self)

**Decorators**: `@cached_property`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_field(self, fieldname)

Return docfield from meta.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| fieldname | None | - | - |


##### has_field(self, fieldname)

Return True if fieldname exists.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| fieldname | None | - | - |


##### get_label(self, fieldname)

Return label of the given fieldname.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| fieldname | None | - | - |


##### get_options(self, fieldname)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| fieldname | None | - | - |


##### get_link_doctype(self, fieldname)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| fieldname | None | - | - |


##### get_search_fields(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_fields_to_fetch(self, link_fieldname = None)

Return a list of docfield objects for fields whose values
are to be fetched and updated for a particular link field.

These fields are of type Data, Link, Text, Readonly and their
fetch_from property is set as `link_fieldname`.`source_fieldname`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| link_fieldname | None | None | - |


##### get_list_fields(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_custom_fields(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_title_field(self)

Return the title field of this doctype,
explict via `title_field`, or `title` or `name`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_translatable_fields(self)

Return all fields that are translation enabled

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### is_translatable(self, fieldname)

Return true of false given a field

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| fieldname | None | - | - |


##### get_workflow(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_naming_series_options(self) → list[str]

Get list naming series options.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `list[str]`


##### add_custom_fields(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### apply_property_setters(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### add_custom_links_and_actions(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### check_if_large_table(self)

Apply some heuristics to detect large tables.

UI code can use this information to adapt accordingly.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _fields(self)

**Decorators**: `@cached_property`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _table_fields(self)

**Decorators**: `@cached_property`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _non_computed_table_fields(self)

**Decorators**: `@cached_property`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _table_doctypes(self)

**Decorators**: `@cached_property`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _non_computed_table_doctypes(self)

**Decorators**: `@cached_property`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### init_field_caches(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### sort_fields(self)

Sort fields on the basis of following rules (priority descending):
- `field_order` property setter
- `insert_after` computed based on default order for standard fields
- `insert_after` property for custom fields

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _update_fields_based_on_order(self, field_order)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| field_order | None | - | - |


##### set_custom_permissions(self)

Reset `permissions` with Custom DocPerm if exists

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_fieldnames_with_value(self, with_field_meta = False, with_virtual_fields = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| with_field_meta | None | False | - |
| with_virtual_fields | None | False | - |


##### get_fields_to_check_permissions(self, user_permission_doctypes)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| user_permission_doctypes | None | - | - |


##### get_high_permlevel_fields(self)

Build list of fields with high perm level and all the higher perm levels defined.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### high_permlevel_fields(self)

**Decorators**: `@cached_property`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_permitted_fieldnames(self, parenttype = None)

Build list of `fieldname` with read perm level and all the higher perm levels defined.

Note: If permissions are not defined for DocType, return all the fields with value.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| parenttype | None | None | - |


##### get_permlevel_access(self, permission_type = 'read', parenttype = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| permission_type | None | 'read' | - |
| parenttype | None | None | - |


##### get_permissions(self, parenttype = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| parenttype | None | None | - |


##### get_dashboard_data(self)

Return dashboard setup related to this doctype.

This method will return the `data` property in the `[doctype]_dashboard.py`
file in the doctype's folder, along with any overrides or extensions
implemented in other Frappe applications via hooks.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### add_doctype_links(self, data)

add `links` child table in standard link dashboard format

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| data | None | - | - |


##### get_row_template(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_list_template(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_web_template(self, suffix = '')

Return the relative path of the row template for this doctype.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| suffix | None | '' | - |


##### is_nested_set(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




### _Meta

**Inherits from**: Meta, DocType



## Functions

### get_meta(doctype: 'str | DocType', cached: bool = True) → '_Meta'

Get metadata for a doctype.

Args:
    doctype: The doctype as a string object.
    cached: Whether to use cached metadata (default: True).

Returns:
    Meta object for the given doctype.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | 'str | DocType' | - | - |
| cached | bool | True | - |

**Returns**: `'_Meta'`



### clear_meta_cache(doctype: str = '*')

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | str | '*' | - |

**Returns**: (none)



### load_meta(doctype)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |

**Returns**: (none)



### get_table_columns(doctype)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |

**Returns**: (none)



### load_doctype_from_file(doctype)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |

**Returns**: (none)



### get_parent_dt(dt)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| dt | None | - | - |

**Returns**: (none)



### set_fieldname(field_id, fieldname)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| field_id | None | - | - |
| fieldname | None | - | - |

**Returns**: (none)



### get_field_currency(df, doc = None)

get currency based on DocField options and fieldvalue in doc

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| df | None | - | - |
| doc | None | None | - |

**Returns**: (none)



### get_field_precision(df, doc = None, currency = None)

get precision based on DocField options and fieldvalue in doc

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| df | None | - | - |
| doc | None | None | - |
| currency | None | None | - |

**Returns**: (none)



### get_precision_from_currency_format(currency: str) → int

Get precision from currency format string if applicable.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| currency | str | - | - |

**Returns**: `int`



### get_default_df(fieldname)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| fieldname | None | - | - |

**Returns**: (none)



### trim_tables(doctype = None, dry_run = False, quiet = False)

Removes database fields that don't exist in the doctype (json or custom field). This may be needed
as maintenance since removing a field in a DocType doesn't automatically
delete the db field.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | None | - |
| dry_run | None | False | - |
| quiet | None | False | - |

**Returns**: (none)



### trim_table(doctype, dry_run = True)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| dry_run | None | True | - |

**Returns**: (none)



### _update_field_order_based_on_insert_after(field_order, insert_after_map)

Update the field order based on insert_after_map

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| field_order | None | - | - |
| insert_after_map | None | - | - |

**Returns**: (none)



### _serialize(doc, no_nulls = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |
| no_nulls | None | False | - |

**Returns**: (none)



### is_internal(field)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| field | None | - | - |

**Returns**: (none)



### is_value_field(df)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| df | None | - | - |

**Returns**: (none)


