# API Reference: sqlite_search.py

**Language**: Python

**Source**: `search/sqlite_search.py`

---

## Classes

### WarningType

Warning types for search indexing.

**Inherits from**: Enum



### IndexWarning

Structured warning for search indexing.

**Inherits from**: (none)

#### Methods

##### __str__(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




### SQLiteSearchIndexMissingError

**Inherits from**: Exception



### SQLiteSearch

Abstract base class for SQLite FTS5-based full-text search for Frappe.

Provides full-text search with advanced features:
- Spelling correction using trigram similarity
- Time-based recency boost with categorical scoring
- Custom scoring with title matching and document type boosts
- Ranking tracking (original BM25 vs modified scores)
- Filtering by user-defined criteria
- Permission-aware search results via query-level filtering

**Inherits from**: ABC

#### Methods

##### scoring_function(func)

Decorator to mark methods as scoring functions that should be automatically
included in the scoring pipeline.

Usage:
    @SQLiteSearch.scoring_function
    def custom_boost(self, row, query, query_words):
        return 1.5

**Decorators**: `@staticmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| func | None | - | - |


##### __init__(self, db_name = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| db_name | None | None | - |


##### _parse_doctype_fields(self, doctype, config)

Parse field definitions for a doctype to extract field names and mappings.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doctype | None | - | - |
| config | None | - | - |


##### _build_doc_configs(self)

Build document configurations from class-level INDEXABLE_DOCTYPES.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _get_schema(self)

Get the search index schema with automatic defaults.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_search_filters(self)

Return filters to apply to search results.

Returns:
    dict: Permission filters in format:
        {
            "field_name": value,  # Single value: field = value
            "field_name": [val1, val2]  # List: field IN (val1, val2)
        }

**Decorators**: `@abstractmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### search(self, query, title_only = False, filters = None)

Main search method with advanced filtering support.

Args:
    query (str): Search query text
    title_only (bool): Whether to search only in titles
    filters (dict): Optional filters by field names

Returns:
    dict: Search results with summary statistics

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| query | None | - | - |
| title_only | None | False | - |
| filters | None | None | - |


##### build_index(self)

Build the complete search index from scratch using atomic replacement.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### index_exists(self)

Check if FTS index exists.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### drop_index(self)

Drop the search index by removing the database file.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### is_search_enabled(self)

Override this to enable/disable search

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### raise_if_not_indexed(self)

Raise exception if search index doesn't exist.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_documents(self)

Get all records to be indexed.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _execute_search_query(self, fts_query, title_only, filters)

Execute the FTS search query with optional filters.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| fts_query | None | - | - |
| title_only | None | - | - |
| filters | None | - | - |


##### _process_search_results(self, raw_results, query)

Process search results with scoring.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| raw_results | None | - | - |
| query | None | - | - |


##### get_scoring_pipeline(self)

Return the scoring pipeline, a list of methods to calculate the final score.
Each method in the list should accept either (row, query) or (row, query, query_words)
and return a float. The final score is the product of all values returned by the pipeline methods.
Subclasses can override this to customize the scoring logic.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _calculate_advanced_score(self, row, query, query_words)

Calculate the final score by executing the scoring pipeline.
The final score is the product of all scores returned by the pipeline methods.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| row | None | - | - |
| query | None | - | - |
| query_words | None | - | - |


##### _get_base_score(self, row, query)

Calculate the base score from BM25.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| row | None | - | - |
| query | None | - | - |


##### _get_title_boost(self, row, query, query_words)

Calculate the title matching boost based on percentage of words matched.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| row | None | - | - |
| query | None | - | - |
| query_words | None | - | - |


##### _get_recency_boost(self, row, query)

Calculate the time-based recency boost.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| row | None | - | - |
| query | None | - | - |


##### _get_text_field_column_index(self, field_name)

Get the 1-based column index of a text field in the FTS table.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| field_name | None | - | - |


##### _expand_query_with_corrections(self, query)

Expand query with spelling corrections.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| query | None | - | - |


##### _find_similar_words(self, word, max_suggestions = MAX_SPELLING_SUGGESTIONS, min_similarity = MIN_SIMILARITY_THRESHOLD)

Find similar words using indexed trigram similarity - much faster!

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| word | None | - | - |
| max_suggestions | None | MAX_SPELLING_SUGGESTIONS | - |
| min_similarity | None | MIN_SIMILARITY_THRESHOLD | - |


##### _build_vocabulary(self, documents)

Build vocabulary and trigram index from documents for spelling correction.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| documents | None | - | - |


##### _get_connection(self, read_only = False)

Get SQLite connection with FTS5 support and performance optimizations.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| read_only | None | False | - |


##### _set_pragmas(self, cursor, is_read = False)

Set SQLite performance pragmas.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| cursor | None | - | - |
| is_read | None | False | - |


##### _ensure_fts_table(self)

Create FTS table and related tables if they don't exist.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _index_documents(self, documents)

Bulk index documents into SQLite FTS.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| documents | None | - | - |


##### index_doc(self, doctype, docname)

Index a single document.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doctype | None | - | - |
| docname | None | - | - |


##### remove_doc(self, doctype, docname)

Remove a single document from the index.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doctype | None | - | - |
| docname | None | - | - |


##### _update_progress(self, message, progress, total = 100, absolute = True)

Update progress bar only if not running in a web request context or tests.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| message | None | - | - |
| progress | None | - | - |
| total | None | 100 | - |
| absolute | None | True | - |


##### _validate_config(self)

Validate document configuration at startup.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _empty_search_result(self, title_only = False, filters = None)

Return empty search result structure.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| title_only | None | False | - |
| filters | None | None | - |


##### _get_db_path(self, is_temp = False)

Get the path for the SQLite FTS database.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| is_temp | None | False | - |


##### _prepare_fts_query(self, query)

Prepare query for FTS5 with proper escaping and operators.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| query | None | - | - |


##### sql(self, query, params = None, read_only = False, commit = False)

Execute a SQL query on the search database.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| query | None | - | - |
| params | None | None | - |
| read_only | None | False | - |
| commit | None | False | - |


##### prepare_document(self, doc)

Prepare a document for indexing by validating and transforming it.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doc | None | - | - |


##### _validate_document_for_indexing(self, doc)

Run all validation checks for a document before indexing.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doc | None | - | - |


##### _add_text_fields_to_document(self, document, doc, config)

Populate text fields in the document for indexing.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| document | None | - | - |
| doc | None | - | - |
| config | None | - | - |


##### _add_metadata_fields_to_document(self, document, doc, config)

Populate metadata fields in the document for indexing.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| document | None | - | - |
| doc | None | - | - |
| config | None | - | - |


##### _process_content(self, content)

Process content to remove HTML tags, links, and images for better indexing quality.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| content | None | - | - |


##### _generate_trigrams(self, word)

Generate trigrams for a word for fuzzy matching.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| word | None | - | - |


##### _print_warning_summary(self)

Print a summary of warnings collected during indexing.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _add_warning(self, warning_type: WarningType, message: str)

Add a structured warning to the warnings list.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| warning_type | WarningType | - | - |
| message | str | - | - |


##### _warn_invalid_document(self, doc: dict, reason: str)

Add warning for invalid document.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doc | dict | - | - |
| reason | str | - | - |


##### _warn_missing_text_fields(self, doctype: str, docname: str, missing_fields: list)

Add warning for missing text fields.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doctype | str | - | - |
| docname | str | - | - |
| missing_fields | list | - | - |


##### _warn_missing_content_field(self, doctype: str, docname: str, field: str)

Add warning for missing content field.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doctype | str | - | - |
| docname | str | - | - |
| field | str | - | - |


##### _warn_missing_title_field(self, doctype: str, docname: str, field: str)

Add warning for missing title field.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doctype | str | - | - |
| docname | str | - | - |
| field | str | - | - |


##### _warn_missing_doctype(self, doc: Any)

Add warning for missing doctype.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doc | Any | - | - |


##### _warn_missing_name(self, doctype: str)

Add warning for missing name.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doctype | str | - | - |


##### get_warning_statistics(self) → dict[str, Any]

Get warning statistics for programmatic use.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `dict[str, Any]`




## Functions

### build_index_if_not_exists()

Build index if it doesn't exist.

**Returns**: (none)



### build_index(SearchClass: type[SQLiteSearch] | None = None, search_class_path: str | None = None, force: bool = False)

Build search index for SearchClass

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| SearchClass | type[SQLiteSearch] | None | None | - |
| search_class_path | str | None | None | - |
| force | bool | False | - |

**Returns**: (none)



### build_index_in_background()

Enqueue index building in background.

**Returns**: (none)



### update_doc_index(doc: Document, method = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | Document | - | - |
| method | None | None | - |

**Returns**: (none)



### delete_doc_index(doc: Document, method = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | Document | - | - |
| method | None | None | - |

**Returns**: (none)



### get_search_classes() → list[type[SQLiteSearch]]

**Returns**: `list[type[SQLiteSearch]]`


