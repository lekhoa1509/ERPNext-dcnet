# API Reference: personal_data_download_request.py

**Language**: Python

**Source**: `website/doctype/personal_data_download_request/personal_data_download_request.py`

---

## Classes

### PersonalDataDownloadRequest

**Inherits from**: Document

#### Methods

##### after_insert(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### generate_file_and_send_mail(self, personal_data)

generate the file link for download

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| personal_data | None | - | - |




## Functions

### get_user_data(user)

Return user data not linked to `User` doctype.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| user | None | - | - |

**Returns**: (none)


