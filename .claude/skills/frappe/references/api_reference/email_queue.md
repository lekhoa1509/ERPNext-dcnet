# API Reference: email_queue.py

**Language**: Python

**Source**: `email/doctype/email_queue/email_queue.py`

---

## Classes

### EmailQueue

**Inherits from**: Document

#### Methods

##### onload(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_recipients(self, recipients)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| recipients | None | - | - |


##### on_trash(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### prevent_email_queue_delete(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_duplicate(self, recipients)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| recipients | None | - | - |


##### new(cls, doc_data, ignore_permissions = False) → EmailQueue

**Decorators**: `@classmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| cls | None | - | - |
| doc_data | None | - | - |
| ignore_permissions | None | False | - |

**Returns**: `EmailQueue`


##### find(cls, name) → EmailQueue

**Decorators**: `@classmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| cls | None | - | - |
| name | None | - | - |

**Returns**: `EmailQueue`


##### find_one_by_filters(cls)

**Decorators**: `@classmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| cls | None | - | - |


##### update_db(self, commit = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| commit | None | False | - |


##### update_status(self, status, commit = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| status | None | - | - |
| commit | None | False | - |


##### cc(self)

**Decorators**: `@property`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### to(self)

**Decorators**: `@property`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### attachments_list(self)

**Decorators**: `@property`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_email_account(self, raise_error = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| raise_error | None | False | - |


##### is_to_be_sent(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### can_send_now(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### send(self, smtp_server_instance: SMTPServer = None, frappe_mail_client: FrappeMail = None, force_send: bool = False)

Send emails to recipients.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| smtp_server_instance | SMTPServer | None | - |
| frappe_mail_client | FrappeMail | None | - |
| force_send | bool | False | - |


##### clear_old_logs(days = 30)

Remove low priority older than 31 days in Outbox or configured in Log Settings.
Note: Used separate query to avoid deadlock

**Decorators**: `@staticmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| days | None | 30 | - |




### SendMailContext

**Inherits from**: (none)

#### Methods

##### __init__(self, queue_doc: Document, smtp_server_instance: SMTPServer = None, frappe_mail_client: FrappeMail = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| queue_doc | Document | - | - |
| smtp_server_instance | SMTPServer | None | - |
| frappe_mail_client | FrappeMail | None | - |


##### fetch_outgoing_server(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### __enter__(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### __exit__(self, exc_type, exc_val, exc_tb)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| exc_type | None | - | - |
| exc_val | None | - | - |
| exc_tb | None | - | - |


##### notify_failed_email(self)

**Decorators**: `@savepoint(catch=Exception)`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_recipient_status_to_sent(self, recipient)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| recipient | None | - | - |


##### get_message_object(self, message)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| message | None | - | - |


##### message_placeholder(self, placeholder_key)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| placeholder_key | None | - | - |


##### build_message(self, recipient_email) → bytes

Build message specific to the recipient.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| recipient_email | None | - | - |

**Returns**: `bytes`


##### get_tracker_str(self, recipient_email) → str

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| recipient_email | None | - | - |

**Returns**: `str`


##### get_unsubscribe_str(self, recipient_email: str) → str

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| recipient_email | str | - | - |

**Returns**: `str`


##### get_receivers_str(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_recipient_str(self, recipient_email)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| recipient_email | None | - | - |


##### include_attachments(self, message)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| message | None | - | - |


##### _store_file(self, file_name, content)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| file_name | None | - | - |
| content | None | - | - |




### QueueBuilder

Builds Email Queue from the given data

**Inherits from**: (none)

#### Methods

##### __init__(self, recipients = None, sender = None, subject = None, message = None, text_content = None, reference_doctype = None, reference_name = None, unsubscribe_method = None, unsubscribe_params = None, unsubscribe_message = None, attachments = None, reply_to = None, cc = None, bcc = None, message_id = None, in_reply_to = None, send_after = None, expose_recipients = None, send_priority = 1, communication = None, read_receipt = None, queue_separately = False, is_notification = False, add_unsubscribe_link = 1, inline_images = None, header = None, print_letterhead = False, with_container = False, email_read_tracker_url = None, x_priority: Literal[1, 3, 5] = 3, email_headers = None, raw_html = False, add_css = True)

Add email to sending queue (Email Queue)

:param recipients: List of recipients.
:param sender: Email sender.
:param subject: Email subject.
:param message: Email message.
:param text_content: Text version of email message.
:param reference_doctype: Reference DocType of caller document.
:param reference_name: Reference name of caller document.
:param send_priority: Priority for Email Queue, default 1.
:param unsubscribe_method: URL method for unsubscribe. Default is `/api/method/frappe.email.queue.unsubscribe`.
:param unsubscribe_params: additional params for unsubscribed links. default are name, doctype, email
:param attachments: Attachments to be sent.
:param reply_to: Reply to be captured here (default inbox)
:param in_reply_to: Used to send the Message-Id of a received email back as In-Reply-To.
:param send_after: Send this email after the given datetime. If value is in integer, then `send_after` will be the automatically set to no of days from current date.
:param communication: Communication link to be set in Email Queue record
:param queue_separately: Queue each email separately
:param is_notification: Marks email as notification so will not trigger notifications from system
:param add_unsubscribe_link: Send unsubscribe link in the footer of the Email, default 1.
:param inline_images: List of inline images as {"filename", "filecontent"}. All src properties will be replaced with random Content-Id
:param header: Append header in email (boolean)
:param with_container: Wraps email inside styled container
:param email_read_tracker_url: A URL for tracking whether an email is read by the recipient.
:param x_priority: 1 = HIGHEST, 3 = NORMAL, 5 = LOWEST
:param email_headers: Additional headers to be added in the email, e.g. {"X-Custom-Header": "value"} or {"Custom-Header": "value"}. Automatically prepends "X-" to the header name if not present.
:param raw_html: Whether to treat email template as a complete HTML file
:param add_css: Add default CSS from hooks/email_css to the email template (default True)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| recipients | None | None | - |
| sender | None | None | - |
| subject | None | None | - |
| message | None | None | - |
| text_content | None | None | - |
| reference_doctype | None | None | - |
| reference_name | None | None | - |
| unsubscribe_method | None | None | - |
| unsubscribe_params | None | None | - |
| unsubscribe_message | None | None | - |
| attachments | None | None | - |
| reply_to | None | None | - |
| cc | None | None | - |
| bcc | None | None | - |
| message_id | None | None | - |
| in_reply_to | None | None | - |
| send_after | None | None | - |
| expose_recipients | None | None | - |
| send_priority | None | 1 | - |
| communication | None | None | - |
| read_receipt | None | None | - |
| queue_separately | None | False | - |
| is_notification | None | False | - |
| add_unsubscribe_link | None | 1 | - |
| inline_images | None | None | - |
| header | None | None | - |
| print_letterhead | None | False | - |
| with_container | None | False | - |
| email_read_tracker_url | None | None | - |
| x_priority | Literal[1, 3, 5] | 3 | - |
| email_headers | None | None | - |
| raw_html | None | False | - |
| add_css | None | True | - |


##### unsubscribe_method(self)

**Decorators**: `@property`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _get_emails_list(self, emails = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| emails | None | None | - |


##### recipients(self)

**Decorators**: `@property`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### cc(self)

**Decorators**: `@property`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### bcc(self)

**Decorators**: `@property`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### send_after(self)

**Decorators**: `@property`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### sender(self)

**Decorators**: `@property`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### email_text_content(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### email_html_content(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### should_include_unsubscribe_link(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### unsubscribe_message(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_outgoing_email_account(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_unsubscribed_user_emails(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### final_recipients(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### final_cc(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### final_bcc(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_attachments(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### prepare_email_content(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### process(self, send_now = False) → EmailQueue | None

Build and return the email queues those are created.

Sends email incase if it is requested to send now.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| send_now | None | False | - |

**Returns**: `EmailQueue | None`


##### send_emails(self, queue_data, final_recipients)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| queue_data | None | - | - |
| final_recipients | None | - | - |


##### as_dict(self, include_recipients = True)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| include_recipients | None | True | - |




## Functions

### retry_sending(queues: str | list[str])

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| queues | str | list[str] | - | - |

**Returns**: (none)



### send_now(name, force_send: bool = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| name | None | - | - |
| force_send | bool | False | - |

**Returns**: (none)



### toggle_sending(enable)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| enable | None | - | - |

**Returns**: (none)



### on_doctype_update()

Add index in `tabCommunication` for `(reference_doctype, reference_name)`

**Returns**: (none)



### get_email_retry_limit()

**Returns**: (none)


