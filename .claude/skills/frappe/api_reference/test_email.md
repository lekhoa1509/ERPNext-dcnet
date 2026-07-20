# API Reference: test_email.py

**Language**: Python

**Source**: `tests/test_email.py`

---

## Classes

### TestEmail

**Inherits from**: IntegrationTestCase

#### Methods

##### setUp(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_email_queue(self, send_after = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| send_after | None | None | - |


##### test_send_after(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_flush(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_cc_header(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_cc_footer(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_expose(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_sender(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_unsubscribe(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_image_parsing(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




### TestVerifiedRequests

**Inherits from**: IntegrationTestCase

#### Methods

##### test_round_trip(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




### TestEmailIntegrationTest

Sends email to local SMTP server and verifies correctness.

SMTP4Dev runs as a service in unit test CI job.
If you need to run this test locally, you must setup SMTP4dev locally.

WARNING: SMTP4dev doesn't have stable API, it can break anytime.

**Inherits from**: IntegrationTestCase

#### Methods

##### setUp(self) → None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `None`


##### tearDown(self) → None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `None`


##### get_last_sent_emails(cls)

**Decorators**: `@classmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| cls | None | - | - |


##### get_message(cls, message_id)

**Decorators**: `@classmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| cls | None | - | - |
| message_id | None | - | - |


##### test_send_email(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_store_attachments(self)

"attach print" feature just tells email queue which document to attach, this is not
actually stored unless system setting says so.

**Decorators**: `@IntegrationTestCase.change_settings('System Settings', store_attached_pdf_document=1)`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### _patched_assertion(email_account, assertion)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| email_account | None | - | - |
| assertion | None | - | - |

**Returns**: (none)


