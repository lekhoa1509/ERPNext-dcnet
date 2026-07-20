# API Reference: email.py

**Language**: Python

**Source**: `core/doctype/communication/email.py`

---

## Functions

### make(doctype = None, name = None, content = None, subject = None, sent_or_received = 'Sent', sender = None, sender_full_name = None, recipients = None, communication_medium = 'Email', send_email = False, print_html = None, print_format = None, attachments = None, send_me_a_copy = False, cc = None, bcc = None, read_receipt = None, print_letterhead = True, email_template = None, communication_type = None, send_after = None, print_language = None, now = False, raw_html = False, add_css = True) → dict[str, str]

Make a new communication. Checks for email permissions for specified Document.

:param doctype: Reference DocType.
:param name: Reference Document name.
:param content: Communication body.
:param subject: Communication subject.
:param sent_or_received: Sent or Received (default **Sent**).
:param sender: Communcation sender (default current user).
:param recipients: Communication recipients as list.
:param communication_medium: Medium of communication (default **Email**).
:param send_email: Send via email (default **False**).
:param print_html: HTML Print format to be sent as attachment.
:param print_format: Print Format name of parent document to be sent as attachment.
:param attachments: List of File names or dicts with keys "fname" and "fcontent"
:param send_me_a_copy: Send a copy to the sender (default **False**).
:param email_template: Template which is used to compose mail .
:param send_after: Send after the given datetime.
:param raw_html: Whether to use html version of email template
:param add_css: Add default CSS from hooks/email_css to the email template (default **True**)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | None | - |
| name | None | None | - |
| content | None | None | - |
| subject | None | None | - |
| sent_or_received | None | 'Sent' | - |
| sender | None | None | - |
| sender_full_name | None | None | - |
| recipients | None | None | - |
| communication_medium | None | 'Email' | - |
| send_email | None | False | - |
| print_html | None | None | - |
| print_format | None | None | - |
| attachments | None | None | - |
| send_me_a_copy | None | False | - |
| cc | None | None | - |
| bcc | None | None | - |
| read_receipt | None | None | - |
| print_letterhead | None | True | - |
| email_template | None | None | - |
| communication_type | None | None | - |
| send_after | None | None | - |
| print_language | None | None | - |
| now | None | False | - |
| raw_html | None | False | - |
| add_css | None | True | - |

**Returns**: `dict[str, str]`



### _make(doctype = None, name = None, content = None, subject = None, sent_or_received = 'Sent', sender = None, sender_full_name = None, recipients = None, communication_medium = 'Email', send_email = False, print_html = None, print_format = None, attachments = None, send_me_a_copy = False, cc = None, bcc = None, read_receipt = None, print_letterhead = True, email_template = None, communication_type = None, add_signature = True, send_after = None, print_language = None, now = False, raw_html = False, add_css = True) → dict[str, str]

Internal method to make a new communication that ignores Permission checks.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | None | - |
| name | None | None | - |
| content | None | None | - |
| subject | None | None | - |
| sent_or_received | None | 'Sent' | - |
| sender | None | None | - |
| sender_full_name | None | None | - |
| recipients | None | None | - |
| communication_medium | None | 'Email' | - |
| send_email | None | False | - |
| print_html | None | None | - |
| print_format | None | None | - |
| attachments | None | None | - |
| send_me_a_copy | None | False | - |
| cc | None | None | - |
| bcc | None | None | - |
| read_receipt | None | None | - |
| print_letterhead | None | True | - |
| email_template | None | None | - |
| communication_type | None | None | - |
| add_signature | None | True | - |
| send_after | None | None | - |
| print_language | None | None | - |
| now | None | False | - |
| raw_html | None | False | - |
| add_css | None | True | - |

**Returns**: `dict[str, str]`



### validate_email(doc: 'Communication') → None

Validate Email Addresses of Recipients and CC

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | 'Communication' | - | - |

**Returns**: `None`



### set_incoming_outgoing_accounts(doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |

**Returns**: (none)



### add_attachments(name: str, attachments: Iterable[str | dict]) → None

Add attachments to the given Communication

:param name: Communication name
:param attachments: File names or dicts with keys "fname" and "fcontent"

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| name | str | - | - |
| attachments | Iterable[str | dict] | - | - |

**Returns**: `None`



### mark_email_as_seen(name: str | None = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| name | str | None | None | - |

**Returns**: (none)



### _mark_email_as_seen(name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| name | None | - | - |

**Returns**: (none)



### update_communication_as_read(name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| name | None | - | - |

**Returns**: (none)


