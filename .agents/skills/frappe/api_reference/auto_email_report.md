# API Reference: auto_email_report.py

**Language**: Python

**Source**: `email/doctype/auto_email_report/auto_email_report.py`

---

## Classes

### AutoEmailReport

**Inherits from**: Document

#### Methods

##### autoname(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### sender_email(self)

**Decorators**: `@property`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_emails(self)

Cleanup list of emails

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_report_count(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_report_format(self)

check if user has select correct report format

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_mandatory_fields(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_report_content(self)

Return file for the report in given format.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_html_table(self, columns = None, data = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| columns | None | None | - |
| data | None | None | - |


##### get_file_name(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### prepare_dynamic_filters(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_date_filters(self, from_date, to_date)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| from_date | None | - | - |
| to_date | None | - | - |


##### send(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### dynamic_date_filters_set(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### download(name)

Download report locally

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| name | None | - | - |

**Returns**: (none)



### send_now(name)

Send Auto Email report now

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| name | None | - | - |

**Returns**: (none)



### send_daily()

Check reports to be sent daily

**Returns**: (none)



### process_auto_email_report(report)

Process and send the Auto Email Report based on frequency

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| report | None | - | - |

**Returns**: (none)



### send_monthly()

Check reports to be sent monthly

**Returns**: (none)



### make_links(columns, data)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| columns | None | - | - |
| data | None | - | - |

**Returns**: (none)



### update_field_types(columns)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| columns | None | - | - |

**Returns**: (none)



### get_half_year_start(as_str = False)

Returns the first day of the current half-year based on the current date.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| as_str | None | False | - |

**Returns**: (none)


