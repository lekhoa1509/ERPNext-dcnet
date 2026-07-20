# API Reference: test_auto_repeat.py

**Language**: Python

**Source**: `automation/doctype/auto_repeat/test_auto_repeat.py`

---

## Classes

### TestAutoRepeat

**Inherits from**: IntegrationTestCase

#### Methods

##### setUpClass(cls)

**Decorators**: `@classmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| cls | None | - | - |


##### test_daily_auto_repeat(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_weekly_auto_repeat(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_fortnightly_auto_repeat(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_weekly_auto_repeat_with_weekdays(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_monthly_auto_repeat(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### monthly_auto_repeat(self, doctype, docname, start_date, end_date = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doctype | None | - | - |
| docname | None | - | - |
| start_date | None | - | - |
| end_date | None | None | - |


##### test_email_notification(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_next_schedule_date(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_submit_on_creation(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_auto_repeat_assignee(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_auto_repeat_assignee_with_separate_documents(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### add_custom_fields() → 'CustomField'

**Returns**: `'CustomField'`



### make_auto_repeat()

**Returns**: (none)



### create_submittable_doctype(doctype, submit_perms = 1)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| submit_perms | None | 1 | - |

**Returns**: (none)



### get_months(start, end)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| start | None | - | - |
| end | None | - | - |

**Returns**: (none)


