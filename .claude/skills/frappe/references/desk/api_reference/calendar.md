# API Reference: calendar.py

**Language**: Python

**Source**: `calendar.py`

---

## Functions

### update_event(args, field_map)

Updates Event (called via calendar) based on passed `field_map`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| args | None | - | - |
| field_map | None | - | - |

**Returns**: (none)



### get_event_conditions(doctype, filters = None)

Return SQL conditions with user permissions and filters for event queries.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| filters | None | None | - |

**Returns**: (none)



### get_events(doctype, start, end, field_map, filters = None, fields = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| start | None | - | - |
| end | None | - | - |
| field_map | None | - | - |
| filters | None | None | - |
| fields | None | None | - |

**Returns**: (none)


