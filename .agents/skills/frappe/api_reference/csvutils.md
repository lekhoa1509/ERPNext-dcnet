# API Reference: csvutils.py

**Language**: Python

**Source**: `utils/csvutils.py`

---

## Classes

### UnicodeWriter

**Inherits from**: (none)

#### Methods

##### __init__(self, encoding = 'utf-8', quoting = csv.QUOTE_NONNUMERIC)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| encoding | None | 'utf-8' | - |
| quoting | None | csv.QUOTE_NONNUMERIC | - |


##### writerow(self, row)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| row | None | - | - |


##### getvalue(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### read_csv_content_from_attached_file(doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |

**Returns**: (none)



### read_csv_content(fcontent, use_sniffer: bool = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| fcontent | None | - | - |
| use_sniffer | bool | False | - |

**Returns**: (none)



### send_csv_to_client(args)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| args | None | - | - |

**Returns**: (none)



### to_csv(data)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| data | None | - | - |

**Returns**: (none)



### build_csv_response(data, filename)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| data | None | - | - |
| filename | None | - | - |

**Returns**: (none)



### check_record(d)

check for mandatory, select options, dates. these should ideally be in doclist

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| d | None | - | - |

**Returns**: (none)



### import_doc(d, doctype, overwrite, row_idx, submit = False, ignore_links = False)

import main (non child) document

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| d | None | - | - |
| doctype | None | - | - |
| overwrite | None | - | - |
| row_idx | None | - | - |
| submit | None | False | - |
| ignore_links | None | False | - |

**Returns**: (none)



### getlink(doctype, name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| name | None | - | - |

**Returns**: (none)



### get_csv_content_from_google_sheets(url)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| url | None | - | - |

**Returns**: (none)



### validate_google_sheets_url(url)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| url | None | - | - |

**Returns**: (none)


