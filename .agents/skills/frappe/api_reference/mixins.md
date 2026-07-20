# API Reference: mixins.py

**Language**: Python

**Source**: `core/doctype/communication/mixins.py`

---

## Classes

### CommunicationEmailMixin

Mixin class to handle communication mails.

**Inherits from**: (none)

#### Methods

##### is_email_communication(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_owner(self)

Get owner of the communication docs parent.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_all_email_addresses(self, exclude_displayname = False)

Get all Email addresses mentioned in the doc along with display name.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| exclude_displayname | None | False | - |


##### get_email_with_displayname(self, email_address)

Return email address after adding displayname.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| email_address | None | - | - |


##### mail_recipients(self, is_inbound_mail_communcation = False)

Build to(recipient) list to send an email.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| is_inbound_mail_communcation | None | False | - |


##### get_mail_recipients_with_displayname(self, is_inbound_mail_communcation = False)

Build to(recipient) list to send an email including displayname in email.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| is_inbound_mail_communcation | None | False | - |


##### mail_cc(self, is_inbound_mail_communcation = False, include_sender = False)

Build cc list to send an email.

* if email copy is requested by sender, then add sender to CC.
* If this doc is created through inbound mail, then add doc owner to cc list
* remove all the thread_notify disabled users.
* Remove standard users from email list

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| is_inbound_mail_communcation | None | False | - |
| include_sender | None | False | - |


##### get_mail_cc_with_displayname(self, is_inbound_mail_communcation = False, include_sender = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| is_inbound_mail_communcation | None | False | - |
| include_sender | None | False | - |


##### mail_bcc(self, is_inbound_mail_communcation = False)

* Thread_notify check
* Email unsubscribe list
* remove standard users.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| is_inbound_mail_communcation | None | False | - |


##### get_mail_bcc_with_displayname(self, is_inbound_mail_communcation = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| is_inbound_mail_communcation | None | False | - |


##### mail_sender(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### mail_sender_fullname(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_mail_sender_with_displayname(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_content(self, print_format = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| print_format | None | None | - |


##### get_attach_link(self, print_format)

Return public link for the attachment via `templates/emails/print_link.html`.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| print_format | None | - | - |


##### get_outgoing_email_account(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_incoming_email_account(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### mail_attachments(self, print_format = None, print_html = None, print_language = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| print_format | None | None | - |
| print_html | None | None | - |
| print_language | None | None | - |


##### get_unsubscribe_message(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### exclude_emails_list(self, is_inbound_mail_communcation = False, include_sender = False) → list

List of mail id's excluded while sending mail.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| is_inbound_mail_communcation | None | False | - |
| include_sender | None | False | - |

**Returns**: `list`


##### get_assignees(self)

Get owners of the reference document.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### filter_thread_notification_disbled_users(emails)

Filter users based on notifications for email threads setting is disabled.

**Decorators**: `@staticmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| emails | None | - | - |


##### filter_disabled_users(emails)

**Decorators**: `@staticmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| emails | None | - | - |


##### sendmail_input_dict(self, print_html = None, print_format = None, send_me_a_copy = None, print_letterhead = None, is_inbound_mail_communcation = None, print_language = None, raw_html = False, add_css = True) → dict

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| print_html | None | None | - |
| print_format | None | None | - |
| send_me_a_copy | None | None | - |
| print_letterhead | None | None | - |
| is_inbound_mail_communcation | None | None | - |
| print_language | None | None | - |
| raw_html | None | False | - |
| add_css | None | True | - |

**Returns**: `dict`


##### send_email(self, print_html = None, print_format = None, send_me_a_copy = None, print_letterhead = None, is_inbound_mail_communcation = None, print_language = None, now = False, raw_html = False, add_css = True)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| print_html | None | None | - |
| print_format | None | None | - |
| send_me_a_copy | None | None | - |
| print_letterhead | None | None | - |
| is_inbound_mail_communcation | None | None | - |
| print_language | None | None | - |
| now | None | False | - |
| raw_html | None | False | - |
| add_css | None | True | - |



