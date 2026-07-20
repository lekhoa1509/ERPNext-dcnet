# API Reference: permission_log.py

**Language**: Python

**Source**: `core/doctype/permission_log/permission_log.py`

---

## Classes

### PermissionLog

**Inherits from**: Document

#### Methods

##### changed_at(self)

**Decorators**: `@property`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### make_perm_log(doc, method = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |
| method | None | None | - |

**Returns**: (none)



### insert_perm_log(doc: Document, doc_before_save: Document = None, for_doctype: str | None = None, for_document: str | None = None, fields: list | tuple | None = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | Document | - | - |
| doc_before_save | Document | None | - |
| for_doctype | str | None | None | - |
| for_document | str | None | None | - |
| fields | list | tuple | None | None | - |

**Returns**: (none)



### get_changes(doc: Document, doc_before_save = None, fields = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | Document | - | - |
| doc_before_save | None | None | - |
| fields | None | None | - |

**Returns**: (none)



### get_changes_diff(current_changes, previous_changes)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| current_changes | None | - | - |
| previous_changes | None | - | - |

**Returns**: (none)



### get_filtered_changes(changes, filters = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| changes | None | - | - |
| filters | None | None | - |

**Returns**: (none)



### filter_child_docs(child_docs, filter_keys)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| child_docs | None | - | - |
| filter_keys | None | - | - |

**Returns**: (none)


