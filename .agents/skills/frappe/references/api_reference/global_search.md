# API Reference: global_search.py

**Language**: Python

**Source**: `utils/global_search.py`

---

## Functions

### setup_global_search_table()

Creates __global_search table
:return:

**Returns**: (none)



### reset()

Deletes all data in __global_search
:return:

**Returns**: (none)



### get_doctypes_with_global_search(with_child_tables = True)

Return doctypes with global search fields
:param with_child_tables:
:return:

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| with_child_tables | None | True | - |

**Returns**: (none)



### rebuild_for_doctype(doctype)

Rebuild entries of doctype's documents in __global_search on change of
searchable fields
:param doctype: Doctype

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |

**Returns**: (none)



### delete_global_search_records_for_doctype(doctype)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |

**Returns**: (none)



### get_selected_fields(meta, global_search_fields)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| meta | None | - | - |
| global_search_fields | None | - | - |

**Returns**: (none)



### get_children_data(doctype, meta)

Get all records from all the child tables of a doctype

all_children = {
        "parent1": {
                "child_doctype1": [
                        {
                                "field1": val1,
                                "field2": val2
                        }
                ]
        }
}

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| meta | None | - | - |

**Returns**: (none)



### insert_values_for_multiple_docs(all_contents)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| all_contents | None | - | - |

**Returns**: (none)



### update_global_search(doc)

Add values marked with `in_global_search` to
`global_search_queue` from given doc
:param doc: Document to be added to global search

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |

**Returns**: (none)



### update_global_search_for_all_web_pages()

**Returns**: (none)



### get_routes_to_index()

**Returns**: (none)



### add_route_to_global_search(route)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| route | None | - | - |

**Returns**: (none)



### get_formatted_value(value, field)

Prepare field from raw data
:param value:
:param field:
:return:

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| value | None | - | - |
| field | None | - | - |

**Returns**: (none)



### sync_global_search()

Inserts / updates values from `global_search_queue` to __global_search.
This is called via job scheduler
:param flags:
:return:

**Returns**: (none)



### _get_deduped_search_item_values(items)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| items | None | - | - |

**Returns**: (none)



### sync_values(values: list)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| values | list | - | - |

**Returns**: (none)



### sync_value_in_queue(value)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| value | None | - | - |

**Returns**: (none)



### sync_value(value: dict)

Sync a given document to global search
:param value: dict of { doctype, name, content, published, title, route }

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| value | dict | - | - |

**Returns**: (none)



### delete_for_document(doc)

Delete the __global_search entry of a document that has
been deleted
:param doc: Deleted document

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |

**Returns**: (none)



### search(text, start = 0, limit = 20, doctype = '')

Search for given text in __global_search
:param text: phrase to be searched
:param start: start results at, default 0
:param limit: number of results to return, default 20
:return: Array of result objects

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| text | None | - | - |
| start | None | 0 | - |
| limit | None | 20 | - |
| doctype | None | '' | - |

**Returns**: (none)



### web_search(text: str, scope: str | None = None, start: int = 0, limit: int = 20)

Search for given text in __global_search where published = 1
:param text: phrase to be searched
:param scope: search only in this route, for e.g /docs
:param start: start results at, default 0
:param limit: number of results to return, default 20
:return: Array of result objects

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| text | str | - | - |
| scope | str | None | None | - |
| start | int | 0 | - |
| limit | int | 20 | - |

**Returns**: (none)



### get_distinct_words(text)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| text | None | - | - |

**Returns**: (none)



### _get()

**Returns**: (none)



### _get_filters()

**Returns**: (none)



### get_search_queue_item_generator()

**Returns**: (none)


