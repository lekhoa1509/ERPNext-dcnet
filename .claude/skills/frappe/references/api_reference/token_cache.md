# API Reference: token_cache.py

**Language**: Python

**Source**: `integrations/doctype/token_cache/token_cache.py`

---

## Classes

### TokenCache

**Inherits from**: Document

#### Methods

##### get_auth_header(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_data(self, data)

Store data returned by authorization flow.

Params:
data - Dict with access_token, refresh_token, expires_in and scope.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| data | None | - | - |


##### get_expires_in(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### is_expired(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_json(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |



