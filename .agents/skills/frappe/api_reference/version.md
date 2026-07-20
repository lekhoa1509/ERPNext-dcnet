# API Reference: version.py

**Language**: Python

**Source**: `core/doctype/version/version.py`

---

## Classes

### Version

**Inherits from**: Document

#### Methods

##### update_version_info(self, old: Document | None, new: Document) → bool

Update changed info and return true if change contains useful data.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| old | Document | None | - | - |
| new | Document | - | - |

**Returns**: `bool`


##### set_impersonator(data)

**Decorators**: `@staticmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| data | None | - | - |


##### set_diff(self, old: Document, new: Document) → bool

Set the data property with the diff of the docs if present

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| old | Document | - | - |
| new | Document | - | - |

**Returns**: `bool`


##### for_insert(self, doc: Document) → bool

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doc | Document | - | - |

**Returns**: `bool`


##### get_data(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### get_diff(old, new, for_child = False, compare_cancelled = False)

Get diff between 2 document objects

If there is a change, then returns a dict like:

        {
                "changed"    : [[fieldname1, old, new], [fieldname2, old, new]],
                "added"      : [[table_fieldname1, {dict}], ],
                "removed"    : [[table_fieldname1, {dict}], ],
                "row_changed": [[table_fieldname1, row_name1, row_index,
                        [[child_fieldname1, old, new],
                        [child_fieldname2, old, new]], ]
                ],

        }

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| old | None | - | - |
| new | None | - | - |
| for_child | None | False | - |
| compare_cancelled | None | False | - |

**Returns**: (none)



### on_doctype_update()

**Returns**: (none)


