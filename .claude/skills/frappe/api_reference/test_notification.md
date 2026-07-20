# API Reference: test_notification.py

**Language**: Python

**Source**: `email/doctype/notification/test_notification.py`

---

## Classes

### TestNotification

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


##### test_new_and_save(self)

Check creating a new communication triggers a notification.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_condition(self)

Check notification is triggered based on a condition.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_invalid_condition(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_value_changed(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_minutes_positive_offset(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_minutes_negative_offset(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_minutes_offset_validation(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_alert_disabled_on_wrong_field(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_date_changed(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_cc_jinja(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_notification_to_assignee(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_notification_by_child_table_field(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_notification_value_change_casted_types(self)

Make sure value change event dont fire because of incorrect type comparisons.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_attach_files_from_field(self)

Test notification with 'From Field' attachment option.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_attach_files_all(self)

Test notification with 'All' attachment option.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_attach_files_empty_option(self)

Test notification with empty attachment option (no attachments).

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### tearDownClass(cls)

**Decorators**: `@classmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| cls | None | - | - |


##### test_notification_with_jinja_template(self)

Test Notification with Jinja Template

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_filters_condition(self)

Test Notification with Condition Type 'Filters'.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### get_test_notification(config)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| config | None | - | - |

**Returns**: (none)



### get_test_doctype_with_attach_field(doctype_name = 'Test Attach Doctype')

Create a temporary doctype with an attach field for testing.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype_name | None | 'Test Attach Doctype' | - |

**Returns**: (none)



### create_test_file(file_name = 'test_attachment.txt', content = 'Test file content')

Create a test file and return its File document.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| file_name | None | 'test_attachment.txt' | - |
| content | None | 'Test file content' | - |

**Returns**: (none)


