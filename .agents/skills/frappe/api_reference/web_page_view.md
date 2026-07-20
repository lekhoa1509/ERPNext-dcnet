# API Reference: web_page_view.py

**Language**: Python

**Source**: `website/doctype/web_page_view/web_page_view.py`

---

## Classes

### WebPageView

**Inherits from**: Document

#### Methods

##### clear_old_logs(days = 180)

**Decorators**: `@staticmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| days | None | 180 | - |




## Functions

### make_view_log(referrer = None, browser = None, version = None, user_tz = None, source = None, campaign = None, medium = None, content = None, visitor_id = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| referrer | None | None | - |
| browser | None | None | - |
| version | None | None | - |
| user_tz | None | None | - |
| source | None | None | - |
| campaign | None | None | - |
| medium | None | None | - |
| content | None | None | - |
| visitor_id | None | None | - |

**Returns**: (none)



### get_page_view_count(path)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| path | None | - | - |

**Returns**: (none)



### is_tracking_enabled()

**Returns**: (none)


