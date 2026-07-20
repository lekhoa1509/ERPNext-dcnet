# API Reference: importer.py

**Language**: Python

**Source**: `importer.py`

---

## Classes

### Importer

**Inherits from**: (none)

#### Methods

##### __init__(self, doctype, data_import = None, file_path = None, import_type = None, console = False, use_sniffer = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doctype | None | - | - |
| data_import | None | None | - |
| file_path | None | None | - |
| import_type | None | None | - |
| console | None | False | - |
| use_sniffer | None | False | - |


##### get_data_for_import_preview(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### before_import(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### import_data(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### after_import(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### process_doc(self, doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doc | None | - | - |


##### insert_record(self, doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doc | None | - | - |


##### update_record(self, doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doc | None | - | - |


##### get_eta(self, current, total, processing_time)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| current | None | - | - |
| total | None | - | - |
| processing_time | None | - | - |


##### export_errored_rows(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### export_import_log(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### print_import_log(self, import_log)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| import_log | None | - | - |


##### print_grouped_warnings(self, warnings)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| warnings | None | - | - |




### ImportFile

**Inherits from**: (none)

#### Methods

##### __init__(self, doctype, file, template_options = None, import_type = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doctype | None | - | - |
| file | None | - | - |
| template_options | None | None | - |
| import_type | None | None | - |


##### get_data_from_template_file(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### parse_data_from_template(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_data_for_import_preview(self)

Adds a serial number column as the first column

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_payloads_for_import(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### parse_next_row_for_import(self, data)

Parse rows that make up a doc. A doc maybe built from a single row or multiple rows.
Return the doc, rows, and data without the rows.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| data | None | - | - |


##### get_warnings(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### read_file(self, file_path: str)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| file_path | str | - | - |


##### read_content(self, content, extension)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| content | None | - | - |
| extension | None | - | - |




### Row

**Inherits from**: (none)

#### Methods

##### __init__(self, index, row, doctype, header, import_type)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| index | None | - | - |
| row | None | - | - |
| doctype | None | - | - |
| header | None | - | - |
| import_type | None | - | - |


##### parse_doc(self, doctype, parent_doc = None, table_df = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doctype | None | - | - |
| parent_doc | None | None | - |
| table_df | None | None | - |


##### _parse_doc(self, doctype, columns, values, parent_doc = None, table_df = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doctype | None | - | - |
| columns | None | - | - |
| values | None | - | - |
| parent_doc | None | None | - |
| table_df | None | None | - |


##### validate_value(self, value, col)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| value | None | - | - |
| col | None | - | - |


##### link_exists(self, value, df)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| value | None | - | - |
| df | None | - | - |


##### parse_value(self, value, col)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| value | None | - | - |
| col | None | - | - |


##### get_date(self, value, column) → date

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| value | None | - | - |
| column | None | - | - |

**Returns**: `date`


##### get_datetime(self, value, column) → datetime

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| value | None | - | - |
| column | None | - | - |

**Returns**: `datetime`


##### get_values(self, indexes)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| indexes | None | - | - |


##### get(self, index)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| index | None | - | - |


##### as_list(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




### Header

**Inherits from**: Row

#### Methods

##### __init__(self, index, row, doctype, raw_data, column_to_field_map = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| index | None | - | - |
| row | None | - | - |
| doctype | None | - | - |
| raw_data | None | - | - |
| column_to_field_map | None | None | - |


##### get_column_indexes(self, doctype, tablefield = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doctype | None | - | - |
| tablefield | None | None | - |


##### get_columns(self, indexes)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| indexes | None | - | - |




### Column

**Inherits from**: (none)

#### Methods

##### __init__(self, index, header, doctype, column_values, map_to_field = None, seen = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| index | None | - | - |
| header | None | - | - |
| doctype | None | - | - |
| column_values | None | - | - |
| map_to_field | None | None | - |
| seen | None | None | - |


##### parse(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### guess_date_format_for_column(self)

Guesses date format for a column by parsing all the values in the column,
getting the date format and then returning the one which has the maximum frequency

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_values(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### as_dict(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### build_fields_dict_for_column_matching(parent_doctype)

Build a dict with various keys to match with column headers and value as docfield
The keys can be label or fieldname
{
        'Customer': df1,
        'customer': df1,
        'Due Date': df2,
        'due_date': df2,
        'Item Code (Sales Invoice Item)': df3,
        'Sales Invoice Item:item_code': df3,
}

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| parent_doctype | None | - | - |

**Returns**: (none)



### get_df_for_column_header(doctype, header)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| header | None | - | - |

**Returns**: (none)



### get_id_field(doctype)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |

**Returns**: (none)



### get_autoname_field(doctype)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |

**Returns**: (none)



### get_item_at_index(_list, i, default = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| _list | None | - | - |
| i | None | - | - |
| default | None | None | - |

**Returns**: (none)



### get_user_format(date_format)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| date_format | None | - | - |

**Returns**: (none)



### df_as_json(df)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| df | None | - | - |

**Returns**: (none)



### get_select_options(df)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| df | None | - | - |

**Returns**: (none)



### create_import_log(data_import, log_index, log_details)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| data_import | None | - | - |
| log_index | None | - | - |
| log_details | None | - | - |

**Returns**: (none)



### get_standard_fields(doctype)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |

**Returns**: (none)



### build_fields_dict_for_doctype()

**Returns**: (none)



### is_table_field(df)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| df | None | - | - |

**Returns**: (none)



### guess_date_format(d)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| d | None | - | - |

**Returns**: (none)


