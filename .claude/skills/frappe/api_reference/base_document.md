# API Reference: base_document.py

**Language**: Python

**Source**: `model/base_document.py`

---

## Classes

### BaseDocument

**Inherits from**: (none)

#### Methods

##### __init__(self, d)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| d | None | - | - |


##### __json__(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### meta(self)

**Decorators**: `@cached_property`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### permitted_fieldnames(self) → set[str]

**Decorators**: `@cached_property`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `set[str]`


##### _weakref(self)

**Decorators**: `@cached_property`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### __getstate__(self)

Return a copy of `__dict__` excluding unpicklable values like `meta`.

Called when pickling.
More info: https://docs.python.org/3/library/pickle.html#handling-stateful-objects

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### remove_unpicklable_values(self, state)

Remove unpicklable values before pickling

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| state | None | - | - |


##### update(self, d)

Update multiple fields of a doctype using a dictionary of key-value pairs.

Example:
        doc.update({
                "user": "admin",
                "balance": 42000
        })

Developer Note: Logic in the set method is re-implemented here for perf

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| d | None | - | - |


##### update_if_missing(self, d)

Set default values for fields without existing values

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| d | None | - | - |


##### get_db_value(self, key)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| key | None | - | - |


##### get(self, key, filters = None, limit = None, default = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| key | None | - | - |
| filters | None | None | - |
| limit | None | None | - |
| default | None | None | - |


##### getone(self, key, filters = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| key | None | - | - |
| filters | None | None | - |


##### set(self, key, value, as_value = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| key | None | - | - |
| value | None | - | - |
| as_value | None | False | - |


##### delete_key(self, key)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| key | None | - | - |


##### append(self, key: str, value: D | dict | None = None, position: int = -1) → D

Append an item to a child table.

Example:
        doc.append("childtable", {
                "child_table_field": "value",
                "child_table_int_field": 0,
                ...
        })

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| key | str | - | - |
| value | D | dict | None | None | - |
| position | int | -1 | - |

**Returns**: `D`


##### parent_doc(self)

**Decorators**: `@property`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### parent_doc(self, value)

**Decorators**: `@parent_doc.setter`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| value | None | - | - |


##### parent_doc(self)

**Decorators**: `@parent_doc.deleter`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### extend(self, key, value)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| key | None | - | - |
| value | None | - | - |


##### remove(self, doc)

Usage: from the parent doc, pass the child table doc to remove that child doc from the
child table, thus removing it from the parent doc

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doc | None | - | - |


##### _init_child(self, value, key)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| value | None | - | - |
| key | None | - | - |


##### _table_fieldnames(self) → dict

**Decorators**: `@cached_property`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `dict`


##### _non_computed_table_fieldnames(self) → dict

**Decorators**: `@cached_property`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `dict`


##### _get_table_fields(self, include_computed = False)

To get table fields during Document init
Meta.get_table_fields goes into recursion for special doctypes

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| include_computed | None | False | - |


##### _evaluate_virtual_field_options(self, options)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| options | None | - | - |


##### get_valid_dict(self, sanitize = True, convert_dates_to_str = False, ignore_nulls = False, ignore_virtual = False) → _dict

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| sanitize | None | True | - |
| convert_dates_to_str | None | False | - |
| ignore_nulls | None | False | - |
| ignore_virtual | None | False | - |

**Returns**: `_dict`


##### init_child_tables(self)

This is needed so that one can loop over child table properties
without worrying about whether or not they have values

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### init_valid_columns(self)

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


##### is_new(self) → bool

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `bool`


##### docstatus(self) → DocStatus

**Decorators**: `@property`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `DocStatus`


##### docstatus(self, value) → None

**Decorators**: `@docstatus.setter`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| value | None | - | - |

**Returns**: `None`


##### as_dict(self, no_nulls = False, no_default_fields = False, convert_dates_to_str = False, no_child_table_fields = False, no_private_properties = False) → dict

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| no_nulls | None | False | - |
| no_default_fields | None | False | - |
| convert_dates_to_str | None | False | - |
| no_child_table_fields | None | False | - |
| no_private_properties | None | False | - |

**Returns**: `dict`


##### as_json(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_table_field_doctype(self, fieldname)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| fieldname | None | - | - |


##### get_parentfield_of_doctype(self, doctype)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doctype | None | - | - |


##### _handle_hash_conflict(self)

Regenerate hash name in case of collisions

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### db_insert(self, ignore_if_duplicate = False)

INSERT the document (with valid columns) in the database.

args:
        ignore_if_duplicate: ignore primary key collision
                                        at database level (postgres)
                                        in python (mariadb)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| ignore_if_duplicate | None | False | - |


##### db_update(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### db_update_all(self)

Raw update parent + children
DOES NOT VALIDATE AND CALL TRIGGERS

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### show_unique_validation_message(self, e)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| e | None | - | - |


##### get_field_name_by_key_name(self, key_name)

MariaDB stores a mapping between `key_name` and `column_name`.
Return the `column_name` associated with the `key_name` passed.

Args:
        key_name (str): The name of the database index.

Raises:
        IndexError: If the key is not found in the table.

Return:
        str: The column name associated with the key.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| key_name | None | - | - |


##### get_label_from_fieldname(self, fieldname)

Return the associated label for fieldname.

Args:
        fieldname (str): The fieldname in the DocType to use to pull the label.

Return:
        str: The label associated with the fieldname, if found, otherwise `None`.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| fieldname | None | - | - |


##### update_modified(self)

Update modified timestamp

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _fix_numeric_types(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _get_missing_mandatory_fields(self)

Get mandatory fields that do not have any values

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_invalid_links(self, is_submittable = False)

Return list of invalid links and also update fetch values if not set.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| is_submittable | None | False | - |


##### set_fetch_from_value(self, doctype, df, values)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doctype | None | - | - |
| df | None | - | - |
| values | None | - | - |


##### _validate_selects(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _validate_data_fields(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _validate_constants(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _validate_length(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _validate_code_fields(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _sync_autoname_field(self)

Keep autoname field in sync with `name`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### throw_length_exceeded_error(self, df, max_length, value)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| df | None | - | - |
| max_length | None | - | - |
| value | None | - | - |


##### _validate_update_after_submit(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _sanitize_content(self)

Sanitize HTML and Email in field values. Used to prevent XSS.

- Ignore if 'Ignore XSS Filter' is checked or fieldtype is 'Code'

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _save_passwords(self)

Save password field values in __Auth table

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_password(self, fieldname = 'password', raise_exception = True)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| fieldname | None | 'password' | - |
| raise_exception | None | True | - |


##### is_dummy_password(self, pwd)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| pwd | None | - | - |


##### precision(self, fieldname, parentfield = None) → int | None

Return float precision for a particular field (or get global default).

:param fieldname: Fieldname for which precision is required.
:param parentfield: If fieldname is in child table.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| fieldname | None | - | - |
| parentfield | None | None | - |

**Returns**: `int | None`


##### get_formatted(self, fieldname, doc = None, currency = None, absolute_value = False, translated = False, format = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| fieldname | None | - | - |
| doc | None | None | - |
| currency | None | None | - |
| absolute_value | None | False | - |
| translated | None | False | - |
| format | None | None | - |


##### is_print_hide(self, fieldname, df = None, for_print = True)

Return True if fieldname is to be hidden for print.

Print Hide can be set via the Print Format Builder or in the controller as a list
of hidden fields. Example

        class MyDoc(Document):
                def __setup__(self):
                        self.print_hide = ["field1", "field2"]

:param fieldname: Fieldname to be checked if hidden.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| fieldname | None | - | - |
| df | None | None | - |
| for_print | None | True | - |


##### in_format_data(self, fieldname)

Return True if shown via Print Format::`format_data` property.

Called from within standard print format.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| fieldname | None | - | - |


##### reset_values_if_no_permlevel_access(self, has_access_to, high_permlevel_fields, mask_fields = None)

If the user does not have permissions at permlevel > 0, then reset the values to original / default

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| has_access_to | None | - | - |
| high_permlevel_fields | None | - | - |
| mask_fields | None | None | - |


##### get_value(self, fieldname)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| fieldname | None | - | - |


##### cast(self, value, df)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| value | None | - | - |
| df | None | - | - |


##### _extract_images_from_text_editor(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### _reduce_extended_instance(doc)

Make extended class instances pickle-able.

When unpickling, this will use get_controller() to recreate the extended class.
Respects the __getstate__ method for proper state handling.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |

**Returns**: (none)



### _reconstruct_extended_instance(doctype)

Helper function to reconstruct an extended class instance during unpickling.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |

**Returns**: (none)



### get_controller(doctype)

Return the locally cached **class** object of the given DocType.

For `custom` type, return `frappe.model.document.Document`.

:param doctype: DocType name as string.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |

**Returns**: (none)



### import_controller(doctype)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |

**Returns**: (none)



### _update_computed_ct_props(class_, doctype)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| class_ | None | - | - |
| doctype | None | - | - |

**Returns**: (none)



### _update_computed_ct_prop(class_, df)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| class_ | None | - | - |
| df | None | - | - |

**Returns**: (none)



### _get_extended_class(base_class, doctype)

Create an extended class by mixing extension classes with the base class.

Args:
        base_class: The base document class
        doctype: The doctype name

Returns:
        Extended class that combines all extension classes with the base class

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| base_class | None | - | - |
| doctype | None | - | - |

**Returns**: (none)



### _filter(data, filters, limit = None)

pass filters as:
{"key": "val", "key": ["!=", "val"],
"key": ["in", "val"], "key": ["not in", "val"], "key": "^val",
"key" : True (exists), "key": False (does not exist) }

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| data | None | - | - |
| filters | None | - | - |
| limit | None | None | - |

**Returns**: (none)



### computed_ct_prop(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: (none)



### get_msg(df)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| df | None | - | - |

**Returns**: (none)



### has_content(df)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| df | None | - | - |

**Returns**: (none)



### get_msg(df, docname)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| df | None | - | - |
| docname | None | - | - |

**Returns**: (none)


