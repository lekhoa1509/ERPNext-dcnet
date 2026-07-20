# API Reference: export_file.py

**Language**: Python

**Source**: `modules/export_file.py`

---

## Functions

### export_doc(doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |

**Returns**: (none)



### export_to_files(record_list = None, record_module = None, verbose = 0, create_init = None)

Export record_list to files. record_list is a list of lists ([doctype, docname, folder name],)  ,

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| record_list | None | None | - |
| record_module | None | None | - |
| verbose | None | 0 | - |
| create_init | None | None | - |

**Returns**: (none)



### write_document_file(doc, record_module = None, create_init = True, folder_name = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |
| record_module | None | None | - |
| create_init | None | True | - |
| folder_name | None | None | - |

**Returns**: (none)



### strip_default_fields(doc, doc_export)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |
| doc_export | None | - | - |

**Returns**: (none)



### write_code_files(folder, fname, doc, doc_export)

Export code files and strip from values

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| folder | None | - | - |
| fname | None | - | - |
| doc | None | - | - |
| doc_export | None | - | - |

**Returns**: (none)



### get_module_name(doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |

**Returns**: (none)



### delete_folder(module, dt, dn)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| module | None | - | - |
| dt | None | - | - |
| dn | None | - | - |

**Returns**: (none)



### create_folder(module, dt, dn, create_init, is_custom_module)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| module | None | - | - |
| dt | None | - | - |
| dn | None | - | - |
| create_init | None | - | - |
| is_custom_module | None | - | - |

**Returns**: (none)



### get_custom_module_path(module)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| module | None | - | - |

**Returns**: (none)



### get_package_path(package)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| package | None | - | - |

**Returns**: (none)



### create_init_py(module_path, dt, dn)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| module_path | None | - | - |
| dt | None | - | - |
| dn | None | - | - |

**Returns**: (none)



### create_if_not_exists(path)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| path | None | - | - |

**Returns**: (none)


