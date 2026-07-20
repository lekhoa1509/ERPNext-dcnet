# API Reference: query_report.py

**Language**: Python

**Source**: `query_report.py`

---

## Functions

### get_report_doc(report_name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| report_name | None | - | - |

**Returns**: (none)



### get_report_result(report, filters)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| report | None | - | - |
| filters | None | - | - |

**Returns**: (none)



### generate_report_result(report, filters = None, user = None, custom_columns = None, is_tree = False, parent_field = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| report | None | - | - |
| filters | None | None | - |
| user | None | None | - |
| custom_columns | None | None | - |
| is_tree | None | False | - |
| parent_field | None | None | - |

**Returns**: (none)



### normalize_result(result, columns)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| result | None | - | - |
| columns | None | - | - |

**Returns**: (none)



### get_script(report_name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| report_name | None | - | - |

**Returns**: (none)



### get_reference_report(report)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| report | None | - | - |

**Returns**: (none)



### run(report_name, filters = None, user = None, ignore_prepared_report = False, custom_columns = None, is_tree = False, parent_field = None, are_default_filters = True, js_filters = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| report_name | None | - | - |
| filters | None | None | - |
| user | None | None | - |
| ignore_prepared_report | None | False | - |
| custom_columns | None | None | - |
| is_tree | None | False | - |
| parent_field | None | None | - |
| are_default_filters | None | True | - |
| js_filters | None | None | - |

**Returns**: (none)



### add_custom_column_data(custom_columns, result)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| custom_columns | None | - | - |
| result | None | - | - |

**Returns**: (none)



### get_prepared_report_result(report, filters, dn = '', user = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| report | None | - | - |
| filters | None | - | - |
| dn | None | '' | - |
| user | None | None | - |

**Returns**: (none)



### export_query()

export from query reports

**Returns**: (none)



### run_export_query_job(user_email: str, form_params, csv_params)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| user_email | str | - | - |
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



### valid_report_name(report_name, suffix)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| report_name | None | - | - |
| suffix | None | - | - |

**Returns**: (none)



### format_fields(data: frappe._dict) → None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| data | frappe._dict | - | - |

**Returns**: `None`



### build_xlsx_data(data: frappe._dict, visible_idx: list[int], include_indentation: bool, include_filters: bool = False, ignore_visible_idx: bool = False, include_hidden_columns: bool = False) → tuple[list[list[Any]], list[int], int]

Build Excel data structure from report data with proper formatting.

Args:
        data: Report data containing columns, result, and filters
        visible_idx: List of row indices that are visible in the report
        include_indentation: Whether to include indentation for tree-like data
        include_filters: Whether to include filter rows at the top of the Excel sheet
        ignore_visible_idx: Whether to ignore the visible_idx parameter
        include_hidden_columns: Whether to include columns marked as hidden

Returns:
        tuple: A tuple containing:
                - result: List of rows for the Excel sheet
                - column_widths: List of column widths for the Excel sheet
                - header_index: Index of the header row in the result

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| data | frappe._dict | - | - |
| visible_idx | list[int] | - | - |
| include_indentation | bool | - | - |
| include_filters | bool | False | - |
| ignore_visible_idx | bool | False | - |
| include_hidden_columns | bool | False | - |

**Returns**: `tuple[list[list[Any]], list[int], int]`



### add_total_row(result, columns, meta = None, is_tree = False, parent_field = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| result | None | - | - |
| columns | None | - | - |
| meta | None | None | - |
| is_tree | None | False | - |
| parent_field | None | None | - |

**Returns**: (none)



### get_data_for_custom_field(doctype, field, names = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| field | None | - | - |
| names | None | None | - |

**Returns**: (none)



### get_data_for_custom_report(columns, result)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| columns | None | - | - |
| result | None | - | - |

**Returns**: (none)



### save_report(reference_report, report_name, columns, filters)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| reference_report | None | - | - |
| report_name | None | - | - |
| columns | None | - | - |
| filters | None | - | - |

**Returns**: (none)



### get_filtered_data(ref_doctype, columns, data, user)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| ref_doctype | None | - | - |
| columns | None | - | - |
| data | None | - | - |
| user | None | - | - |

**Returns**: (none)



### has_match(row, linked_doctypes, doctype_match_filters, ref_doctype, if_owner, columns_dict, user)

Return True if after evaluating permissions for each linked doctype:
        - There is an owner match for the ref_doctype
        - `and` There is a user permission match for all linked doctypes

Return True if the row is empty.

Note:
Each doctype could have multiple conflicting user permission doctypes.
Hence even if one of the sets allows a match, it is true.
This behavior is equivalent to the trickling of user permissions of linked doctypes to the ref doctype.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| row | None | - | - |
| linked_doctypes | None | - | - |
| doctype_match_filters | None | - | - |
| ref_doctype | None | - | - |
| if_owner | None | - | - |
| columns_dict | None | - | - |
| user | None | - | - |

**Returns**: (none)



### has_unrestricted_read_access(doctype, user)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| user | None | - | - |

**Returns**: (none)



### get_linked_doctypes(columns, data)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| columns | None | - | - |
| data | None | - | - |

**Returns**: (none)



### get_columns_dict(columns)

Return a dict with column docfield values as dict.

The keys for the dict are both idx and fieldname,
so either index or fieldname can be used to search for a column's docfield properties.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| columns | None | - | - |

**Returns**: (none)



### get_column_as_dict(col)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| col | None | - | - |

**Returns**: (none)



### get_user_match_filters(doctypes, user)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctypes | None | - | - |
| user | None | - | - |

**Returns**: (none)



### validate_filters_permissions(report_name, filters = None, user = None, js_filters = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| report_name | None | - | - |
| filters | None | None | - |
| user | None | None | - |
| js_filters | None | None | - |

**Returns**: (none)



### translate_report_data(data, total_row)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| data | None | - | - |
| total_row | None | - | - |

**Returns**: (none)



### get_report_data(doc, data)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |
| data | None | - | - |

**Returns**: (none)


