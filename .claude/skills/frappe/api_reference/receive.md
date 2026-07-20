# API Reference: receive.py

**Language**: Python

**Source**: `email/receive.py`

---

## Classes

### EmailSizeExceededError

**Inherits from**: frappe.ValidationError



### LoginLimitExceeded

**Inherits from**: frappe.ValidationError



### SentEmailInInboxError

**Inherits from**: Exception



### EmailServer

Wrapper for POP server to pull emails.

**Inherits from**: (none)

#### Methods

##### __init__(self, args = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| args | None | None | - |


##### connect(self)

Connect to **Email Account**.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### connect_imap(self)

Connect to IMAP

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### connect_pop(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### select_imap_folder(self, folder)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| folder | None | - | - |


##### logout(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_messages(self, folder = 'INBOX')

Return new email messages.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| folder | None | 'INBOX' | - |


##### get_new_mails(self, folder)

Return list of new mails

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| folder | None | - | - |


##### check_imap_uidvalidity(self, folder)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| folder | None | - | - |


##### parse_imap_response(self, cmd, response)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| cmd | None | - | - |
| response | None | - | - |


##### retrieve_message(self, uid, msg_num, folder)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| uid | None | - | - |
| msg_num | None | - | - |
| folder | None | - | - |


##### get_email_seen_status(self, uid, flag_string)

parse the email FLAGS response

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| uid | None | - | - |
| flag_string | None | - | - |


##### has_login_limit_exceeded(self, e)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| e | None | - | - |


##### _post_retrieve_cleanup(self, uid, msg_num)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| uid | None | - | - |
| msg_num | None | - | - |


##### is_temporary_system_problem(self, e)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| e | None | - | - |


##### make_error_msg(self, uid, msg_num)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| uid | None | - | - |
| msg_num | None | - | - |


##### update_flag(self, folder, uid_list = None)

set all uids mails the flag as seen

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| folder | None | - | - |
| uid_list | None | None | - |




### Email

Wrapper for an email.

**Inherits from**: (none)

#### Methods

##### __init__(self, content)

Parses headers, content, attachments from given raw message.

:param content: Raw message.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| content | None | - | - |


##### in_reply_to(self)

**Decorators**: `@property`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### parse(self)

Walk and process multi-part email.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_subject(self)

Parse and decode `Subject` header.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_from(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### decode_email(email: bytes | str | None) → str | None

**Decorators**: `@staticmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| email | bytes | str | None | - | - |

**Returns**: `str | None`


##### set_content_and_type(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### process_part(self, part)

Parse email `part` and set it to `text_content`, `html_content` or `attachments`.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| part | None | - | - |


##### show_attached_email_headers_in_content(self, part)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| part | None | - | - |


##### get_charset(self, part)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| part | None | - | - |


##### get_payload(self, part)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| part | None | - | - |


##### get_attachment(self, part)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| part | None | - | - |


##### save_attachments_in_doc(self, doc)

Save email attachments in given document.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doc | None | - | - |


##### get_thread_id(self)

Extract thread ID from `[]`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### is_reply(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




### InboundMail

Class representation of incoming mail along with mail handlers.

**Inherits from**: Email

#### Methods

##### __init__(self, content, email_account, uid = None, seen_status = None, append_to = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| content | None | - | - |
| email_account | None | - | - |
| uid | None | None | - |
| seen_status | None | None | - |
| append_to | None | None | - |


##### get_content(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### process(self)

Create communication record from email.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _build_communication_doc(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### replace_inline_images(self, attachments)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| attachments | None | - | - |


##### is_notification(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### is_exist_in_system(self)

Check if this email already exists in the system(as communication document).

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### is_sender_same_as_receiver(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### is_reply_to_system_sent_mail(self)

Is it a reply to already sent mail.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### parent_email_queue(self)

Get parent record from `Email Queue`.

If it is a reply to already sent mail, then there will be a parent record in EMail Queue.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### parent_communication(self)

Find a related communication so that we can prepare a mail thread.

The way it happens is by using in-reply-to header, and we can't make thread if it does not exist.

Here are the cases to handle:
1. If mail is a reply to already sent mail, then we can get parent communicaion from
        Email Queue record or message_id on communication.
2. Sometimes we send communication name in message-ID directly, use that to get parent communication.
3. Sender sent a reply but reply is on top of what (s)he sent before,
        then parent record exists directly in communication.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### reference_document(self)

Reference document is a document to which mail relate to.

We can get reference document from Parent record(EmailQueue | Communication) if exists.
Otherwise we do subject match to find reference document if we know the reference(append_to) doctype.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_reference_name_from_subject(self)

Ex: "Re: Your email (#OPP-2020-2334343)"

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### match_record_by_subject_and_sender(self, doctype)

Find a record in the given doctype that matches with email subject and sender.

Cases:
1. Sometimes record name is part of subject. We can get document by parsing name from subject
2. Find by matching sender and subject
3. Find by matching subject alone (Special case)
        Ex: when a System User is using Outlook and replies to an email from their own client,
        it reaches the Email Account with the threading info lost and the (sender + subject match)
        doesn't work because the sender in the first communication was someone different to whom
        the system user is replying to via the common email account in Frappe. This fix bypasses
        the sender match when the sender is a system user and subject is atleast 10 chars long
        (for additional safety)

NOTE: We consider not to match by subject if match record is very old.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doctype | None | - | - |


##### _create_reference_document(self, doctype)

Create reference document if it does not exist in the system.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doctype | None | - | - |


##### get_doc(doctype, docname, ignore_error = False)

**Decorators**: `@staticmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| docname | None | - | - |
| ignore_error | None | False | - |


##### get_relative_dt(days)

Get relative to current datetime. Only relative days are supported.

**Decorators**: `@staticmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| days | None | - | - |


##### get_users_linked_to_account(email_account)

Get list of users who linked to Email account.

**Decorators**: `@staticmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| email_account | None | - | - |


##### clean_subject(subject)

Remove Prefixes like 'fw', FWD', 're' etc from subject.

**Decorators**: `@staticmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| subject | None | - | - |


##### get_email_fields(doctype)

Return Email related fields of a doctype.

**Decorators**: `@staticmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |


##### get_document(self, doctype, name)

Is same as frappe.get_doc but suppresses the DoesNotExist error.

**Decorators**: `@staticmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doctype | None | - | - |
| name | None | - | - |


##### as_dict(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |



