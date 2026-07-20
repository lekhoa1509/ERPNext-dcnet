# API Reference: supplier_scorecard.py

**Language**: Python

**Source**: `doctype/supplier_scorecard/supplier_scorecard.py`

---

## Classes

### SupplierScorecard

**Inherits from**: Document

#### Methods

##### validate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_update(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_standings(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_criteria_weights(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### calculate_total_score(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_standing(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### get_timeline_data(doctype, name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| name | None | - | - |

**Returns**: (none)



### daterange(start_date, end_date)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| start_date | None | - | - |
| end_date | None | - | - |

**Returns**: (none)



### refresh_scorecards()

**Returns**: (none)



### make_all_scorecards(docname)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| docname | None | - | - |

**Returns**: (none)



### get_scorecard_date(period, start_date)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| period | None | - | - |
| start_date | None | - | - |

**Returns**: (none)



### make_default_records()

**Returns**: (none)


