# API Reference: full_text_search.py

**Language**: Python

**Source**: `search/full_text_search.py`

---

## Classes

### FullTextSearch

Frappe Wrapper for Whoosh

**Inherits from**: (none)

#### Methods

##### __init__(self, index_name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| index_name | None | - | - |


##### get_schema(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_fields_to_search(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_id(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_items_to_index(self)

Get all documents to be indexed conforming to the schema

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_document_to_index(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### build(self)

Build search index for all documents

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_index_by_name(self, doc_name)

Wraps `update_index` method, gets the document from name
and updates the index. This function changes the current user
and should only be run as administrator or in a background job.

Args:
        self (object): FullTextSearch Instance
        doc_name (str): name of the document to be updated

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doc_name | None | - | - |


##### remove_document_from_index(self, doc_name)

Remove document from search index

Args:
        self (object): FullTextSearch Instance
        doc_name (str): name of the document to be removed

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doc_name | None | - | - |


##### update_index(self, document)

Update search index for a document

Args:
        self (object): FullTextSearch Instance
        document (_dict): A dictionary with title, path and content

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| document | None | - | - |


##### get_index(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### create_index(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### build_index(self)

Build index for all parsed documents

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### search(self, text: str, scope: str | None = None, limit: int = 20) → list[frappe._dict]

Search from the current index.

Args:
        text: String to search for
        scope: Scope to limit the search. Defaults to None.
        limit: Limit number of search results. Defaults to 20.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| text | str | - | - |
| scope | str | None | None | - |
| limit | int | 20 | - |

**Returns**: `list[frappe._dict]`




### FuzzyTermExtended

**Inherits from**: FuzzyTerm

#### Methods

##### __init__(self, fieldname, text, boost = 1.0, maxdist = 2, prefixlength = 1, constantscore = True)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| fieldname | None | - | - |
| text | None | - | - |
| boost | None | 1.0 | - |
| maxdist | None | 2 | - |
| prefixlength | None | 1 | - |
| constantscore | None | True | - |




## Functions

### get_index_path(index_name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| index_name | None | - | - |

**Returns**: (none)


