# API Reference: tag.py

**Language**: Python

**Source**: `desk/doctype/tag/tag.py`

---

## Classes

### Tag

**Inherits from**: Document



### DocTags

Tags for a particular doctype

**Inherits from**: (none)

#### Methods

##### __init__(self, dt)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| dt | None | - | - |


##### get_tag_fields(self)

Return `tag_fields` property.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_tags(self, dn)

Return tag for a particular item.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| dn | None | - | - |


##### add(self, dn, tag)

Add a new user tag.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| dn | None | - | - |
| tag | None | - | - |


##### remove(self, dn, tag)

Remove a user tag.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| dn | None | - | - |
| tag | None | - | - |


##### remove_all(self, dn)

Remove all user tags (call before delete).

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| dn | None | - | - |


##### update(self, dn, tl)

Update the `_user_tag` column in the table.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| dn | None | - | - |
| tl | None | - | - |


##### setup(self)

Add the `_user_tags` column if not exists.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### check_user_tags(dt)

if the user does not have a tags column, then it creates one

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| dt | None | - | - |

**Returns**: (none)



### add_tag(tag, dt, dn, color = None)

adds a new tag to a record, and creates the Tag master

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| tag | None | - | - |
| dt | None | - | - |
| dn | None | - | - |
| color | None | None | - |

**Returns**: (none)



### add_tags(tags, dt, docs, color = None)

adds a new tag to a record, and creates the Tag master

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| tags | None | - | - |
| dt | None | - | - |
| docs | None | - | - |
| color | None | None | - |

**Returns**: (none)



### remove_tag(tag, dt, dn)

removes tag from the record

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| tag | None | - | - |
| dt | None | - | - |
| dn | None | - | - |

**Returns**: (none)



### get_tagged_docs(doctype, tag)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| tag | None | - | - |

**Returns**: (none)



### get_tags(doctype, txt)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| txt | None | - | - |

**Returns**: (none)



### delete_tags_for_document(doc)

Delete the Tag Link entry of a document that has been deleted.

:param doc: Deleted document

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |

**Returns**: (none)



### update_tags(doc, tags)

Add tags for documents.

:param doc: Document to be added to global tags

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |
| tags | None | - | - |

**Returns**: (none)



### get_documents_for_tag(tag)

Search for given text in Tag Link.

:param tag: tag to be searched

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| tag | None | - | - |

**Returns**: (none)



### get_tags_list_for_awesomebar()

**Returns**: (none)


