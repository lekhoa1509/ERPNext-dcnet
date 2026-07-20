# API Reference: mapper.py

**Language**: Python

**Source**: `model/mapper.py`

---

## Functions

### make_mapped_doc(method, source_name, selected_children = None, args = None)

Return the mapped document calling the given mapper method.
Set `selected_children` as flags for the `get_mapped_doc` method.

Called from `open_mapped_doc` from create_new.js

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| method | None | - | - |
| source_name | None | - | - |
| selected_children | None | None | - |
| args | None | None | - |

**Returns**: (none)



### map_docs(method, source_names, target_doc, args = None)

Return the mapped document calling the given mapper method with each of the given source docs on the target doc.

:param args: Args as string to pass to the mapper method

e.g. args: "{ 'supplier': 'XYZ' }"

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| method | None | - | - |
| source_names | None | - | - |
| target_doc | None | - | - |
| args | None | None | - |

**Returns**: (none)



### get_mapped_doc(from_doctype, from_docname, table_maps, target_doc = None, postprocess = None, ignore_permissions = False, ignore_child_tables = False, cached = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| from_doctype | None | - | - |
| from_docname | None | - | - |
| table_maps | None | - | - |
| target_doc | None | None | - |
| postprocess | None | None | - |
| ignore_permissions | None | False | - |
| ignore_child_tables | None | False | - |
| cached | None | False | - |

**Returns**: (none)



### map_doc(source_doc, target_doc, table_map, source_parent = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| source_doc | None | - | - |
| target_doc | None | - | - |
| table_map | None | - | - |
| source_parent | None | None | - |

**Returns**: (none)



### map_fields(source_doc, target_doc, table_map, source_parent)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| source_doc | None | - | - |
| target_doc | None | - | - |
| table_map | None | - | - |
| source_parent | None | - | - |

**Returns**: (none)



### map_fetch_fields(target_doc, df, no_copy_fields)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| target_doc | None | - | - |
| df | None | - | - |
| no_copy_fields | None | - | - |

**Returns**: (none)



### map_child_doc(source_d, target_parent, table_map, source_parent = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| source_d | None | - | - |
| target_parent | None | - | - |
| table_map | None | - | - |
| source_parent | None | None | - |

**Returns**: (none)


