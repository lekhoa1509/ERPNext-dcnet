# API Reference: inbox.py

**Language**: Python

**Source**: `email/inbox.py`

---

## Functions

### get_email_accounts(user = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| user | None | None | - |

**Returns**: (none)



### create_email_flag_queue(names, action)

create email flag queue to mark email either as read or unread

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| names | None | - | - |
| action | None | - | - |

**Returns**: (none)



### mark_as_closed_open(communication: str, status: str)

Set status to open or close

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| communication | str | - | - |
| status | str | - | - |

**Returns**: (none)



### move_email(communication: str, email_account: str)

Move email to another email account.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| communication | str | - | - |
| email_account | str | - | - |

**Returns**: (none)



### mark_as_trash(communication: str)

Set email status to trash.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| communication | str | - | - |

**Returns**: (none)



### mark_as_spam(communication: str, sender: str)

Set email status to spam.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| communication | str | - | - |
| sender | str | - | - |

**Returns**: (none)



### link_communication_to_document(doc, reference_doctype, reference_name, ignore_communication_links)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |
| reference_doctype | None | - | - |
| reference_name | None | - | - |
| ignore_communication_links | None | - | - |

**Returns**: (none)



### mark_as_seen_unseen(name, action)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| name | None | - | - |
| action | None | - | - |

**Returns**: (none)


