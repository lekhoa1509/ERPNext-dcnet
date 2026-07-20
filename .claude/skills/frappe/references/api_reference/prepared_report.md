# API Reference: prepared_report.py

**Language**: Python

**Source**: `core/doctype/prepared_report/prepared_report.py`

---

## Classes

### PreparedReport

**Inherits from**: Document

#### Methods

##### queued_by(self)

**Decorators**: `@property`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### queued_at(self)

**Decorators**: `@property`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### clear_old_logs(days = 30)

**Decorators**: `@staticmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| days | None | 30 | - |


##### before_insert(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_trash(self)

Remove pending job from queue, if already running then kill the job.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### after_insert(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_prepared_data(self, with_file_name = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| with_file_name | None | False | - |




## Functions

### generate_report(prepared_report)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| prepared_report | None | - | - |

**Returns**: (none)



### _save_error(instance, error)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| instance | None | - | - |
| error | None | - | - |

**Returns**: (none)



### update_job_id(prepared_report)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| prepared_report | None | - | - |

**Returns**: (none)



### make_prepared_report(report_name, filters = None)

run reports in background

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| report_name | None | - | - |
| filters | None | None | - |

**Returns**: (none)



### stop_prepared_report(report_name: str)

Stop a running Prepared Report job.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| report_name | str | - | - |

**Returns**: (none)



### process_filters_for_prepared_report(filters: dict[str, Any] | str) → str

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | dict[str, Any] | str | - | - |

**Returns**: `str`



### get_reports_in_queued_state(report_name, filters)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| report_name | None | - | - |
| filters | None | - | - |

**Returns**: (none)



### get_completed_prepared_report(filters, user, report_name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | None | - | - |
| user | None | - | - |
| report_name | None | - | - |

**Returns**: (none)



### expire_stalled_report()

**Returns**: (none)



### delete_prepared_reports(reports)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| reports | None | - | - |

**Returns**: (none)



### create_json_gz_file(data, dt, dn, report_name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| data | None | - | - |
| dt | None | - | - |
| dn | None | - | - |
| report_name | None | - | - |

**Returns**: (none)



### download_attachment(dn)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| dn | None | - | - |

**Returns**: (none)



### get_permission_query_condition(user)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| user | None | - | - |

**Returns**: (none)



### has_permission(doc, user)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |
| user | None | - | - |

**Returns**: (none)



### enqueue_json_to_csv_conversion(prepared_report_name)

Call this to enqueue the conversion in background.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| prepared_report_name | None | - | - |

**Returns**: (none)



### convert_json_to_csv(prepared_report_name)

Background job: Fetch JSON file, convert to CSV, attach CSV to Prepared Report.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| prepared_report_name | None | - | - |

**Returns**: (none)


