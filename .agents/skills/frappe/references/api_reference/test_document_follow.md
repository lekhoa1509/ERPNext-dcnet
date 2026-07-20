# API Reference: test_document_follow.py

**Language**: Python

**Source**: `email/doctype/document_follow/test_document_follow.py`

---

## Classes

### TestDocumentFollow

**Inherits from**: IntegrationTestCase

#### Methods

##### test_document_follow_version(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_document_follow_comment(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_follow_limit(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_follow_on_create(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_do_not_follow_on_create(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_do_not_follow_on_update(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_follow_on_comment(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_do_not_follow_on_comment(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_follow_on_like(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_do_not_follow_on_like(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_follow_on_assign(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_do_not_follow_on_assign(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_follow_on_share(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_do_not_follow_on_share(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### tearDown(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




### DocumentFollowConditions

**Inherits from**: (none)



## Functions

### get_events_followed_by_user(event_name, user_name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| event_name | None | - | - |
| user_name | None | - | - |

**Returns**: (none)



### get_event()

**Returns**: (none)



### get_user(document_follow = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| document_follow | None | None | - |

**Returns**: (none)



### get_emails(event_doc, search_string)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| event_doc | None | - | - |
| search_string | None | - | - |

**Returns**: (none)


