# API Reference: transaction_deletion_record.py

**Language**: Python

**Source**: `doctype/transaction_deletion_record/transaction_deletion_record.py`

---

## Classes

### TransactionDeletionRecord

**Inherits from**: Document

#### Methods

##### __init__(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_discard(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_to_delete_list(self)

Validate To Delete list: existence, protection status, child table exclusion, duplicates

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _is_any_doctype_in_deletion_list(self, doctypes_list)

Check if any DocType from the list is in the To Delete list

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doctypes_list | None | - | - |


##### generate_job_name_for_task(self, task = None)

Generate unique job name for a specific task

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| task | None | None | - |


##### generate_job_name_for_next_tasks(self, task = None)

Generate job names for all tasks following the specified task

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| task | None | None | - |


##### generate_job_name_for_all_tasks(self)

Generate job names for all tasks in the deletion workflow

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### before_submit(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### reset_task_flags(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### before_save(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_submit(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_cancel(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _set_deletion_cache(self)

Set Redis cache flags for per-doctype validation

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _clear_deletion_cache(self)

Clear Redis cache flags

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _get_child_tables(self, doctype_name)

Get list of child table DocType names for a given DocType

Args:
        doctype_name: The parent DocType to check

Returns:
        list: List of child table DocType names (Table field options)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doctype_name | None | - | - |


##### _get_to_delete_row_infos(self, doctype_name, company_field = None, company = None)

Get child tables and document count for a To Delete list row

Args:
        doctype_name: The DocType to get information for
        company_field: Optional company field name to filter by
        company: Optional company value (defaults to self.company)

Returns:
        dict: {"child_doctypes": str, "document_count": int}

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doctype_name | None | - | - |
| company_field | None | None | - |
| company | None | None | - |


##### _has_company_field(self, doctype_name)

Check if DocType has a field specifically named 'company' linking to Company

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doctype_name | None | - | - |


##### _get_company_link_fields(self, doctype_name)

Get all Company Link field names for a DocType

Args:
        doctype_name: The DocType to check

Returns:
        list: List of field names that link to Company DocType, ordered by field index

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doctype_name | None | - | - |


##### generate_to_delete_list(self)

Generate To Delete list with one row per company field

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### populate_doctype_details(self, doctype_name, company = None, company_field = None)

Get child DocTypes and document count for specified DocType

Args:
        doctype_name: The DocType to get details for
        company: Optional company value for filtering (defaults to self.company)
        company_field: Optional company field name to use for filtering

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doctype_name | None | - | - |
| company | None | None | - |
| company_field | None | None | - |


##### export_to_delete_template_method(self)

Export To Delete list as CSV template

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### import_to_delete_template_method(self, csv_content)

Import CSV template and regenerate counts

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| csv_content | None | - | - |


##### enqueue_task(self, task: str | None = None)

Enqueue a deletion task for background execution

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| task | str | None | None | - |


##### execute_task(self, task_to_execute: str | None = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| task_to_execute | str | None | None | - |


##### delete_notifications(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### populate_doctypes_to_be_ignored_table(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_running_task_for_doc(self, job_names: list | None = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| job_names | list | None | None | - |


##### validate_doc_status(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### start_deletion_tasks(self)

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### delete_bins(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### delete_lead_addresses(self)

Delete addresses to which leads are linked

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### reset_company_values(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### initialize_doctypes_to_be_deleted_table(self)

Initialize deletion table from To Delete list or fall back to original logic

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### delete_company_transactions(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_doctypes_to_be_ignored_list(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_doctypes_with_company_field(self, doctypes_to_be_ignored_list)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doctypes_to_be_ignored_list | None | - | - |


##### get_all_child_doctypes(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_number_of_docs_linked_with_specified_company(self, doctype, company_fieldname)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doctype | None | - | - |
| company_fieldname | None | - | - |


##### get_company_field(self, doctype_name)

Get company field name for a DocType

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doctype_name | None | - | - |


##### populate_doctypes_table(self, tables, doctype, company_field, no_of_docs)

Add doctype to processing tracker

Args:
        tables: List of child table DocType names (to exclude)
        doctype: DocType name to track
        company_field: Company link field name (or None)
        no_of_docs: Initial count

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| tables | None | - | - |
| doctype | None | - | - |
| company_field | None | - | - |
| no_of_docs | None | - | - |


##### delete_child_tables(self, doctype, reference_doc_names)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doctype | None | - | - |
| reference_doc_names | None | - | - |


##### delete_docs_linked_with_specified_company(self, doctype, reference_doc_names)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doctype | None | - | - |
| reference_doc_names | None | - | - |


##### get_naming_series_prefix(naming_series: str, doctype_name: str) → str

Extract the static prefix from an autoname pattern.

Args:
        naming_series: The autoname pattern (e.g., "PREFIX.####", "format:PRE-{####}")
        doctype_name: DocType name for error logging

Returns:
        The static prefix before the counter placeholders

**Decorators**: `@staticmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| naming_series | str | - | - |
| doctype_name | str | - | - |

**Returns**: `str`


##### update_naming_series(self, naming_series, doctype_name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| naming_series | None | - | - |
| doctype_name | None | - | - |


##### delete_version_log(self, doctype, docnames)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doctype | None | - | - |
| docnames | None | - | - |


##### delete_communications(self, doctype, reference_doc_names)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doctype | None | - | - |
| reference_doc_names | None | - | - |


##### delete_comments(self, doctype, reference_doc_names)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doctype | None | - | - |
| reference_doc_names | None | - | - |


##### unlink_attachments(self, doctype, reference_doc_names)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doctype | None | - | - |
| reference_doc_names | None | - | - |




## Functions

### get_protected_doctypes()

Get list of protected DocTypes that cannot be deleted (whitelisted for frontend)

**Returns**: (none)



### get_company_link_fields(doctype_name)

Get all Company Link field names for a DocType (whitelisted for frontend autocomplete)

Args:
        doctype_name: The DocType to check

Returns:
        list: List of field names that link to Company DocType, ordered by field index

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype_name | None | - | - |

**Returns**: (none)



### _get_protected_doctypes_internal()

Internal method to get protected doctypes

**Returns**: (none)



### get_doctypes_to_be_ignored()

**Returns**: (none)



### export_to_delete_template(name)

Export To Delete list as CSV via URL access

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| name | None | - | - |

**Returns**: (none)



### process_import_template(transaction_deletion_record_name, file_url)

Import CSV template and populate To Delete list

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| transaction_deletion_record_name | None | - | - |
| file_url | None | - | - |

**Returns**: (none)



### is_deletion_doc_running(company: str | None = None, err_msg: str | None = None)

Check if any deletion is running globally

The company parameter is kept for backwards compatibility but is now ignored.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| company | str | None | None | - |
| err_msg | str | None | None | - |

**Returns**: (none)



### check_for_running_deletion_job(doc, method = None)

Hook function called on document validate - checks Redis cache for running deletions

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |
| method | None | None | - |

**Returns**: (none)


