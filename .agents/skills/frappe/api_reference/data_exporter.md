# API Reference: data_exporter.js

**Language**: JavaScript

**Source**: `public/js/frappe/data_import/data_exporter.js`

---

## Classes

### DataExporter

**Inherits from**: (none)

#### Methods

##### constructor(doctype, exporting_for, filetype = "CSV")

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| exporting_for | None | - | - |
| filetype | None | "CSV" | - |


##### with_doctype(doctype, ()

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| ( | None | - | - |


##### make_dialog(filetype)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filetype | None | - | - |




## Functions

### get_columns_for_picker(doctype)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |

**Returns**: (none)



### is_field_mandatory(df)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| df | None | - | - |

**Returns**: (none)



### exportable_fields(df)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| df | None | - | - |

**Returns**: (none)


