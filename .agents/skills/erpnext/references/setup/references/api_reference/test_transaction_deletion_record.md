# API Reference: test_transaction_deletion_record.py

**Language**: Python

**Source**: `doctype/transaction_deletion_record/test_transaction_deletion_record.py`

---

## Classes

### TestTransactionDeletionRecord

**Inherits from**: IntegrationTestCase

#### Methods

##### setUp(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### tearDown(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _clear_all_deletion_cache_flags(self)

Clear all deletion_running_doctype:* cache keys

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_doctypes_contain_company_field(self)

Test that all DocTypes in To Delete list have a valid company link field

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_no_of_docs_is_correct(self)

Test that document counts are calculated correctly in To Delete list

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_deletion_is_successful(self)

Test that deletion actually removes documents

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_company_transaction_deletion_request(self)

Test creation via company deletion request method

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_generate_to_delete_list(self)

Test automatic generation of To Delete list

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_validation_prevents_child_tables(self)

Test that child tables cannot be added to To Delete list

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_validation_prevents_protected_doctypes(self)

Test that protected DocTypes cannot be added to To Delete list

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_csv_export_import(self)

Test CSV export and import functionality with company_field column

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_progress_tracking(self)

Test that deleted checkbox is marked when DocType deletion completes

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_composite_key_validation(self)

Test that duplicate (doctype_name + company_field) combinations are prevented

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_same_doctype_different_company_field_allowed(self)

Test that same DocType can be added with different company_field values

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_company_field_validation(self)

Test that invalid company_field values are rejected

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_get_naming_series_prefix_with_dot(self)

Test prefix extraction for standard dot-separated naming series

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_get_naming_series_prefix_with_brace(self)

Test prefix extraction for format patterns with brace separators

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_get_naming_series_prefix_fallback(self)

Test prefix extraction fallback for patterns without standard separators

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_cache_flag_management(self)

Test that cache flags can be set and cleared correctly

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_check_for_running_deletion_blocks_save(self)

Test that check_for_running_deletion_job blocks saves when cache flag exists

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_check_for_running_deletion_allows_save_when_no_flag(self)

Test that documents can be saved when no deletion is running

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_only_one_deletion_allowed_globally(self)

Test that only one deletion can be submitted at a time (global enforcement)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### create_company(company_name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| company_name | None | - | - |

**Returns**: (none)



### create_and_submit_transaction_deletion_doc(company)

Create and execute a transaction deletion record

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| company | None | - | - |

**Returns**: (none)



### create_task(company)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| company | None | - | - |

**Returns**: (none)


