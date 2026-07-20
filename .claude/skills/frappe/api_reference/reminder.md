# API Reference: reminder.py

**Language**: Python

**Source**: `automation/doctype/reminder/reminder.py`

---

## Classes

### Reminder

**Inherits from**: Document

#### Methods

##### clear_old_logs(days = 30)

**Decorators**: `@staticmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| days | None | 30 | - |


##### validate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### send_reminder(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### create_new_reminder(remind_at: str, description: str, reminder_doctype: str | None = None, reminder_docname: str | None = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| remind_at | str | - | - |
| description | str | - | - |
| reminder_doctype | str | None | None | - |
| reminder_docname | str | None | None | - |

**Returns**: (none)



### send_reminders()

**Returns**: (none)


