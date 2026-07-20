# API Reference: reportview.py

**Language**: Python

**Source**: `reportview.py`

---

## Functions

### get()

**Returns**: (none)



### get_list()

**Returns**: (none)



### get_count() → int | None

**Returns**: `int | None`



### execute(doctype)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |

**Returns**: (none)



### get_form_params()

parse GET request parameters.

**Returns**: (none)



### validate_args(data)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| data | None | - | - |

**Returns**: (none)



### validate_fields(data)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| data | None | - | - |

**Returns**: (none)



### validate_filters(data, filters)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| data | None | - | - |
| filters | None | - | - |

**Returns**: (none)



### setup_group_by(data)

Add columns for aggregated values e.g. count(name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| data | None | - | - |

**Returns**: (none)



### raise_invalid_field(fieldname)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| fieldname | None | - | - |

**Returns**: (none)



### is_standard(fieldname)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| fieldname | None | - | - |

**Returns**: (none)



### extract_fieldnames(field)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| field | None | - | - |

**Returns**: (none)



### get_meta_and_docfield(fieldname, data)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| fieldname | None | - | - |
| data | None | - | - |

**Returns**: (none)



### update_wildcard_field_param(data)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| data | None | - | - |

**Returns**: (none)



### clean_params(data)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| data | None | - | - |

**Returns**: (none)



### parse_json(data)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| data | None | - | - |

**Returns**: (none)



### get_parenttype_and_fieldname(field, data)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| field | None | - | - |
| data | None | - | - |

**Returns**: (none)



### compress(data, args = None)

separate keys and values

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| data | None | - | - |
| args | None | None | - |

**Returns**: (none)



### save_report(name, doctype, report_settings)

Save reports of type Report Builder from Report View

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| name | None | - | - |
| doctype | None | - | - |
| report_settings | None | - | - |

**Returns**: (none)



### delete_report(name)

Delete reports of type Report Builder from Report View

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| name | None | - | - |

**Returns**: (none)



### export_query()

export from report builder

**Returns**: (none)



### run_report_view_export_job(user_email, form_params, csv_params)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| user_email | None | - | - |
| form_params | None | - | - |
| csv_params | None | - | - |

**Returns**: (none)



### _export_query(form_params, csv_params, populate_response = True)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| form_params | None | - | - |
| csv_params | None | - | - |
| populate_response | None | True | - |

**Returns**: (none)



### append_totals_row(data)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| data | None | - | - |

**Returns**: (none)



### get_field_info(fields, doctype)

Get column names, labels, field types, and translatable properties based on column names.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| fields | None | - | - |
| doctype | None | - | - |

**Returns**: (none)



### handle_duration_fieldtype_values(doctype, data, fields)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| data | None | - | - |
| fields | None | - | - |

**Returns**: (none)



### parse_field(field: str) → tuple[str | None, str]

Parse a field into parenttype and fieldname.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| field | str | - | - |

**Returns**: `tuple[str | None, str]`



### delete_items()

delete selected items

**Returns**: (none)



### delete_bulk(doctype, items)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| items | None | - | - |

**Returns**: (none)



### get_sidebar_stats(stats, doctype, filters = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| stats | None | - | - |
| doctype | None | - | - |
| filters | None | None | - |

**Returns**: (none)



### get_stats(stats, doctype, filters = None)

get tag info

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| stats | None | - | - |
| doctype | None | - | - |
| filters | None | None | - |

**Returns**: (none)



### get_filter_dashboard_data(stats, doctype, filters = None)

get tags info

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| stats | None | - | - |
| doctype | None | - | - |
| filters | None | None | - |

**Returns**: (none)



### scrub_user_tags(tagcount)

rebuild tag list for tags

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| tagcount | None | - | - |

**Returns**: (none)



### get_match_cond(doctype, as_condition = True)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| as_condition | None | True | - |

**Returns**: (none)



### build_match_conditions(doctype, user = None, as_condition = True)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| user | None | None | - |
| as_condition | None | True | - |

**Returns**: (none)



### get_filters_cond(doctype, filters, conditions, ignore_permissions = None, with_match_conditions = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| filters | None | - | - |
| conditions | None | - | - |
| ignore_permissions | None | None | - |
| with_match_conditions | None | False | - |

**Returns**: (none)


