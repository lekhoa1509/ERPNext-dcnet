# API Reference: email_queue_recipient.py

**Language**: Python

**Source**: `email/doctype/email_queue_recipient/email_queue_recipient.py`

---

## Classes

### EmailQueueRecipient

**Inherits from**: Document

#### Methods

##### is_mail_to_be_sent(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### is_mail_sent(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_db(self, commit = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| commit | None | False | - |




## Functions

### on_doctype_update()

Index required for log clearing, modified is not indexed on child table by default

**Returns**: (none)


