# API Reference: language.py

**Language**: Python

**Source**: `core/doctype/language/language.py`

---

## Classes

### Language

**Inherits from**: Document

#### Methods

##### validate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### before_rename(self, old, new, merge = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| old | None | - | - |
| new | None | - | - |
| merge | None | False | - |


##### on_update(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_user_defaults(self)

Update user defaults for date, time, number format and first day of the week.

When we change any settings of a language, the defaults for all users with that language
should be updated.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### validate_with_regex(name, label)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| name | None | - | - |
| label | None | - | - |

**Returns**: (none)



### sync_languages()

Create Language records from frappe/geo/languages.csv

**Returns**: (none)


