# API Reference: dynamic_links.py

**Language**: Python

**Source**: `model/dynamic_links.py`

---

## Functions

### get_dynamic_link_map(for_delete = False)

Build a map of all dynamically linked tables. For example,
        if Note is dynamically linked to ToDo, the function will return
        `{"Note": ["ToDo"], "Sales Invoice": ["Journal Entry Detail"]}`

Note: Will not map single doctypes

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| for_delete | None | False | - |

**Returns**: (none)



### get_dynamic_links()

Return list of dynamic link fields as DocField.
Uses cache if possible

**Returns**: (none)



### _dynamic_link_map_key(doctype, fieldname)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| fieldname | None | - | - |

**Returns**: (none)



### fetch_distinct_link_doctypes(doctype: str, fieldname: str)

Return all unique doctypes a dynamic link is linking against.
Note:
- results are cached and can *possibly be outdated*
- cache gets updated when a document with different document link is discovered
- raw queries adding dynamic link won't update this cache
- cache miss can often be VERY expensive on large table.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | str | - | - |
| fieldname | str | - | - |

**Returns**: (none)



### invalidate_distinct_link_doctypes(doctype: str, fieldname: str, linked_doctype: str)

If new linked doctype is discovered for a dynamic link then cache is evicted.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | str | - | - |
| fieldname | str | - | - |
| linked_doctype | str | - | - |

**Returns**: (none)


