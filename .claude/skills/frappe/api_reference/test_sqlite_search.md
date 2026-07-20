# API Reference: test_sqlite_search.py

**Language**: Python

**Source**: `tests/test_sqlite_search.py`

---

## Classes

### TestSQLiteSearch

Test implementation of SQLiteSearch for testing purposes.

**Inherits from**: SQLiteSearch

#### Methods

##### get_search_filters(self)

Return permission filters - for testing, allow all documents.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




### TestSQLiteSearchAPI

Test suite for SQLiteSearch public API functionality.

**Inherits from**: IntegrationTestCase

#### Methods

##### setUpClass(cls)

**Decorators**: `@classmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| cls | None | - | - |


##### tearDownClass(cls)

**Decorators**: `@classmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| cls | None | - | - |


##### setUp(self)

Set up test data for each test.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### tearDown(self)

Clean up test data after each test.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_index_lifecycle_and_status_methods(self)

Test index building, existence checking, and status validation.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_basic_search_functionality(self)

Test core search functionality with various query types.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_search_filtering_and_permissions(self)

Test search filtering and permission-based result filtering.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_advanced_scoring_and_ranking(self)

Test scoring pipeline, ranking, and result ordering.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_spelling_correction_and_query_expansion(self)

Test spelling correction and query expansion functionality.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_document_indexing_operations(self)

Test individual document indexing and removal operations.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_search_result_summary_and_metadata(self)

Test search result summary and metadata information.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_configuration_and_schema_validation(self)

Test configuration validation and schema handling.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_content_processing_and_html_handling(self)

Test content processing including HTML tag removal and text normalization.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_search_disabled_state(self)

Test behavior when search is disabled.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_deduplication_on_reindex(self)

Test that re-indexing the same document does not create duplicates.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_background_operations(self, mock_enqueue)

Test background job integration and module-level functions.

**Decorators**: `@patch('frappe.enqueue')`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| mock_enqueue | None | - | - |




### InvalidSearchClass

**Inherits from**: SQLiteSearch

#### Methods

##### get_search_filters(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




### InvalidDoctypeConfig

**Inherits from**: SQLiteSearch

#### Methods

##### get_search_filters(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




### DisabledSearch

**Inherits from**: TestSQLiteSearch

#### Methods

##### is_search_enabled(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |



