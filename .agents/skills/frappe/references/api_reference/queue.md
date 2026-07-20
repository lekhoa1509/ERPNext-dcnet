# API Reference: queue.py

**Language**: Python

**Source**: `email/queue.py`

---

## Functions

### get_emails_sent_this_month(email_account = None)

Get count of emails sent from a specific email account.

:param email_account: name of the email account used to send mail

if email_account=None, email account filter is not applied while counting

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| email_account | None | None | - |

**Returns**: (none)



### get_emails_sent_today(email_account = None)

Get count of emails sent from a specific email account.

:param email_account: name of the email account used to send mail

if email_account=None, email account filter is not applied while counting

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| email_account | None | None | - |

**Returns**: (none)



### get_unsubscribe_message(unsubscribe_message: str, expose_recipients: str) → 'frappe._dict[str, str]'

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| unsubscribe_message | str | - | - |
| expose_recipients | str | - | - |

**Returns**: `'frappe._dict[str, str]'`



### get_unsubcribed_url(reference_doctype, reference_name, email, unsubscribe_method, unsubscribe_params)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| reference_doctype | None | - | - |
| reference_name | None | - | - |
| email | None | - | - |
| unsubscribe_method | None | - | - |
| unsubscribe_params | None | - | - |

**Returns**: (none)



### unsubscribe(doctype, name, email)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| name | None | - | - |
| email | None | - | - |

**Returns**: (none)



### return_unsubscribed_page(email, doctype, name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| email | None | - | - |
| doctype | None | - | - |
| name | None | - | - |

**Returns**: (none)



### flush()

flush email queue, every time: called from scheduler.

This should not be called outside of background jobs.

**Returns**: (none)



### get_queue()

**Returns**: (none)



### retry_sending_emails()

**Returns**: (none)


