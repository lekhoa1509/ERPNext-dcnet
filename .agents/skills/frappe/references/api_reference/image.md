# API Reference: image.py

**Language**: Python

**Source**: `utils/image.py`

---

## Functions

### resize_images(path, maxdim = 700)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| path | None | - | - |
| maxdim | None | 700 | - |

**Returns**: (none)



### strip_exif_data(content, content_type) → bytes

Strip EXIF from image files which support it.

Works by creating a new Image object which ignores exif by
default and then extracts the binary data back into content.

Return Stripped image content.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| content | None | - | - |
| content_type | None | - | - |

**Returns**: `bytes`



### optimize_image(content, content_type, max_width = 1024, max_height = 768, optimize = True, quality = 85)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| content | None | - | - |
| content_type | None | - | - |
| max_width | None | 1024 | - |
| max_height | None | 768 | - |
| optimize | None | True | - |
| quality | None | 85 | - |

**Returns**: (none)


