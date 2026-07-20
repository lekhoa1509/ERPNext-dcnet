# API Reference: test_email_account.py

**Language**: Python

**Source**: `email/doctype/email_account/test_email_account.py`

---

## Classes

### TestEmailAccount

**Inherits from**: IntegrationTestCase

#### Methods

##### setUpClass(cls)

**Decorators**: `@classmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| cls | None | - | - |


##### tearDownClass(cls)

**Decorators**: `@classmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| cls | None | - | - |


##### setUp(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_test_mail(self, fname)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| fname | None | - | - |


##### test_incoming(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_unread_notification(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_incoming_with_attach(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_incoming_attached_email_from_outlook_plain_text_only(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_incoming_attached_email_from_outlook_layers(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_outgoing(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_sendmail(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_print_format(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_threading(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_threading_by_subject(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_threading_by_message_id(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_auto_reply(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_handle_bad_emails(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_handle_bad_encoding(self)

If the email has invalid encoding, it should still be saved as an Unhandled Email.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_imap_folder(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_imap_folder_missing(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_append_to(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_append_to_with_imap_folders(self)

**Decorators**: `@unittest.skip('poorly written and flaky')`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### mocked_get_inbound_mails(email_account, messages = None, mocked_logout = None, mocked_select_imap_folder = None)

**Decorators**: `@patch('frappe.email.receive.EmailServer.select_imap_folder', return_value=True)`, `@patch('frappe.email.receive.EmailServer.logout', side_effect=lambda: None)`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| email_account | None | - | - |
| messages | None | None | - |
| mocked_logout | None | None | - |
| mocked_select_imap_folder | None | None | - |


##### mocked_email_receive(email_account, messages = None, mocked_logout = None, mocked_select_imap_folder = None)

**Decorators**: `@patch('frappe.email.receive.EmailServer.select_imap_folder', return_value=True)`, `@patch('frappe.email.receive.EmailServer.logout', side_effect=lambda: None)`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| email_account | None | - | - |
| messages | None | None | - |
| mocked_logout | None | None | - |
| mocked_select_imap_folder | None | None | - |




### TestInboundMail

**Inherits from**: IntegrationTestCase

#### Methods

##### setUpClass(cls)

**Decorators**: `@classmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| cls | None | - | - |


##### tearDownClass(cls)

**Decorators**: `@classmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| cls | None | - | - |


##### setUp(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_test_mail(self, fname)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| fname | None | - | - |


##### new_doc(self, doctype)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doctype | None | - | - |


##### new_communication(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### new_email_queue(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### new_todo(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_self_sent_mail(self)

Check that we raise SentEmailInInboxError if the inbound mail is self sent mail.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_mail_exist_validation(self)

Do not create communication record if the mail is already downloaded into the system.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_find_parent_email_queue(self)

If the mail is reply to the already sent mail, there will be a email queue record.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_find_parent_communication_through_queue(self)

Find parent communication of an inbound mail.
Cases where parent communication does exist:
1. No parent communication is the mail is not a reply.

Cases where parent communication does not exist:
2. If mail is not a reply to system sent mail, then there can exist co

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_find_parent_communication_for_self_reply(self)

If the inbound email is a reply but not reply to system sent mail.

Ex: User replied to his/her mail.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_find_parent_communication_from_header(self)

Incase of header contains parent communication name

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_reference_document(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_reference_document_by_record_name_in_subject(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_reference_document_by_subject_match(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_reference_document_by_subject_match_with_accents(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_create_communication_from_mail(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### cleanup(sender = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| sender | None | None | - |

**Returns**: (none)



### get_mocked_messages()

**Returns**: (none)



### get_mocked_messages()

**Returns**: (none)


