# API Reference: webhook.py

**Language**: Python

**Source**: `integrations/doctype/webhook/webhook.py`

---

## Classes

### Webhook

**Inherits from**: Document

#### Methods

##### validate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_update(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### execute_for_doc(self, doc: Document)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doc | Document | - | - |


##### validate_docevent(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_condition(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_request_url(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_request_body(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_repeating_fields(self)

Error when Same Field is entered multiple times in webhook_data

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_secret(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### preview_meets_condition(self, preview_document)

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| preview_document | None | - | - |


##### preview_request_body(self, preview_document)

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| preview_document | None | - | - |




## Functions

### get_context(doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |

**Returns**: (none)



### enqueue_webhook(doc, webhook) → None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |
| webhook | None | - | - |

**Returns**: `None`



### log_request(webhook: str, doctype: str, docname: str, url: str, headers: dict, data: dict, res: requests.Response | None = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| webhook | str | - | - |
| doctype | str | - | - |
| docname | str | - | - |
| url | str | - | - |
| headers | dict | - | - |
| data | dict | - | - |
| res | requests.Response | None | None | - |

**Returns**: (none)



### get_webhook_headers(doc, webhook)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |
| webhook | None | - | - |

**Returns**: (none)



### get_webhook_data(doc, webhook)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |
| webhook | None | - | - |

**Returns**: (none)



### get_all_queues()

Fetches all workers and returns a list of available queue names.

**Returns**: (none)


