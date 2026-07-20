# API Reference: comment.py

**Language**: Python

**Source**: `core/doctype/comment/comment.py`

---

## Classes

### Comment

**Inherits from**: Document

#### Methods

##### after_insert(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_update(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_trash(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### notify_change(self, action)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| action | None | - | - |


##### remove_comment_from_cache(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### on_doctype_update()

**Returns**: (none)



### update_comment_in_doc(doc)

Updates `_comments` (JSON) property in parent Document.
Creates a column `_comments` if property does not exist.

Only user created Communication or Comment of type Comment are saved.

`_comments` format

        {
                "comment": [String],
                "by": [user],
                "name": [Comment Document name]
        }

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |

**Returns**: (none)



### get_comments_from_parent(doc)

get the list of comments cached in the document record in the column
`_comments`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |

**Returns**: (none)



### update_comments_in_parent(reference_doctype, reference_name, _comments)

Updates `_comments` property in parent Document with given dict.

:param _comments: Dict of comments.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| reference_doctype | None | - | - |
| reference_name | None | - | - |
| _comments | None | - | - |

**Returns**: (none)



### get_truncated(content)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| content | None | - | - |

**Returns**: (none)


