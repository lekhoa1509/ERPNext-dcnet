# API Reference: google_indexing.py

**Language**: Python

**Source**: `website/doctype/website_settings/google_indexing.py`

---

## Functions

### authorize_access(reauthorize = False, code = None)

If no Authorization code get it from Google and then request for Refresh Token.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| reauthorize | None | False | - |
| code | None | None | - |

**Returns**: (none)



### get_google_indexing_object()

Return an object of Google Indexing object.

**Returns**: (none)



### publish_site(url, operation_type = 'URL_UPDATED')

Send an update/remove url request.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| url | None | - | - |
| operation_type | None | 'URL_UPDATED' | - |

**Returns**: (none)


