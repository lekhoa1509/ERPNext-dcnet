# API Reference: test_communication.py

**Language**: Python

**Source**: `core/doctype/communication/test_communication.py`

---

## Classes

### TestCommunication

**Inherits from**: IntegrationTestCase

#### Methods

##### test_email(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_name(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_circular_linking(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_deduplication_timeline_links(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_contacts_attached(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_get_communication_data(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_parse_email(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_get_emails(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_signature_in_email_content(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_mark_as_spam(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




### TestCommunicationEmailMixin

**Inherits from**: IntegrationTestCase

#### Methods

##### new_communication(self, recipients = None, cc = None, bcc = None) → Communication

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| recipients | None | None | - |
| cc | None | None | - |
| bcc | None | None | - |

**Returns**: `Communication`


##### new_user(self, email)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| email | None | - | - |


##### test_recipients(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_cc(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_bcc(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_sendmail(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_add_attachments_by_filename(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_add_attachments_by_file_content(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### create_email_account() → 'EmailAccount'

**Returns**: `'EmailAccount'`



### test(assertion, cc_list = None, set_user_as = None, include_sender = False, thread_notify = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| assertion | None | - | - |
| cc_list | None | None | - |
| set_user_as | None | None | - |
| include_sender | None | False | - |
| thread_notify | None | False | - |

**Returns**: (none)


