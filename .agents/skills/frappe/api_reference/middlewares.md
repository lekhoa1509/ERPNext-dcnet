# API Reference: middlewares.py

**Language**: Python

**Source**: `middlewares.py`

---

## Classes

### StaticDataMiddleware

**Inherits from**: SharedDataMiddleware

#### Methods

##### __call__(self, environ, start_response)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| environ | None | - | - |
| start_response | None | - | - |


##### get_directory_loader(self, directory)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| directory | None | - | - |




## Functions

### patch_start_response(status, headers, exc_info = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| status | None | - | - |
| headers | None | - | - |
| exc_info | None | None | - |

**Returns**: (none)



### loader(path)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| path | None | - | - |

**Returns**: (none)


