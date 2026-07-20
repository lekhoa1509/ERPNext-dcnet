# API Reference: lost_quotations.py

**Language**: Python

**Source**: `report/lost_quotations/lost_quotations.py`

---

## Functions

### execute(filters = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | None | None | - |

**Returns**: (none)



### get_columns(group_by: Literal['Lost Reason', 'Competitor'])

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| group_by | Literal['Lost Reason', 'Competitor'] | - | - |

**Returns**: (none)



### get_data(company: str, from_date: str, to_date: str, group_by: Literal['Lost Reason', 'Competitor'])

Return quotation value grouped by lost reason or competitor

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| company | str | - | - |
| from_date | str | - | - |
| to_date | str | - | - |
| group_by | Literal['Lost Reason', 'Competitor'] | - | - |

**Returns**: (none)


