# API Reference: email_template.py

**Language**: Python

**Source**: `email/doctype/email_template/email_template.py`

---

## Classes

### EmailTemplate

**Inherits from**: Document

#### Methods

##### response_(self)

**Decorators**: `@property`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_formatted_subject(self, doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doc | None | - | - |


##### get_formatted_response(self, doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doc | None | - | - |


##### get_formatted_email(self, doc, sender = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doc | None | - | - |
| sender | None | None | - |


##### inject_email_account(self, doc, sender = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doc | None | - | - |
| sender | None | None | - |




## Functions

### get_email_template(template_name, doc, sender = None)

Return the processed HTML of a email template with the given doc

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| template_name | None | - | - |
| doc | None | - | - |
| sender | None | None | - |

**Returns**: (none)


