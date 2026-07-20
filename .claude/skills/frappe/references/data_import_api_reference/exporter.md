# API Reference: exporter.py

**Language**: Python

**Source**: `exporter.py`

---

## Classes

### Exporter

**Inherits from**: (none)

#### Methods

##### __init__(self, doctype, export_fields = None, export_data = False, export_filters = None, export_page_length = None, file_type = 'CSV')

Exports records of a DocType for use with Importer
        :param doctype: Document Type to export
        :param export_fields=None: One of 'All', 'Mandatory' or {'DocType': ['field1', 'field2'], 'Child DocType': ['childfield1']}
        :param export_data=False: Whether to export data as well
        :param export_filters=None: The filters (dict or list) which is used to query the records
        :param file_type: One of 'Excel' or 'CSV'

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doctype | None | - | - |
| export_fields | None | None | - |
| export_data | None | False | - |
| export_filters | None | None | - |
| export_page_length | None | None | - |
| file_type | None | 'CSV' | - |


##### get_all_exportable_fields(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### serialize_exportable_fields(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_exportable_fields(self, doctype, fieldnames)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doctype | None | - | - |
| fieldnames | None | - | - |


##### get_data_to_export(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### add_data_row(self, doctype, parentfield, doc, rows, row_idx)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doctype | None | - | - |
| parentfield | None | - | - |
| doc | None | - | - |
| rows | None | - | - |
| row_idx | None | - | - |


##### get_data_as_docs(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### add_header(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### add_data(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_csv_array(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_csv_array_for_export(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### build_response(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### group_children_data_by_parent(self, children_data: dict[str, list])

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| children_data | dict[str, list] | - | - |




## Functions

### is_exportable(df)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| df | None | - | - |

**Returns**: (none)



### format_column_name(df)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| df | None | - | - |

**Returns**: (none)


