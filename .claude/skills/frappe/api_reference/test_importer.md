# API Reference: test_importer.py

**Language**: Python

**Source**: `core/doctype/data_import/test_importer.py`

---

## Classes

### TestImporter

**Inherits from**: IntegrationTestCase

#### Methods

##### setUpClass(cls)

**Decorators**: `@classmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| cls | None | - | - |


##### test_data_import_from_file(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_data_validation_semicolon_success(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_data_validation_semicolon_failure(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_data_import_preview(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_data_import_without_mandatory_values(self)

**Decorators**: `@unimplemented_for(db_type_is.POSTGRES, db_type_is.SQLITE)`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_data_import_update(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_data_import_without_label(self)

Test fallback to fieldname when label is not set for a table.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_importer(self, doctype, import_file, update = False, use_sniffer = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doctype | None | - | - |
| import_file | None | - | - |
| update | None | False | - |
| use_sniffer | None | False | - |


##### get_importer_semicolon(self, doctype, import_file, update = False, use_sniffer = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doctype | None | - | - |
| import_file | None | - | - |
| update | None | False | - |
| use_sniffer | None | False | - |




## Functions

### create_doctype_if_not_exists(doctype_name, force = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype_name | None | - | - |
| force | None | False | - |

**Returns**: (none)



### get_import_file(csv_file_name, force = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| csv_file_name | None | - | - |
| force | None | False | - |

**Returns**: (none)



### get_csv_file_path(file_name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| file_name | None | - | - |

**Returns**: (none)


