# API Reference: installation_note.py

**Language**: Python

**Source**: `doctype/installation_note/installation_note.py`

---

## Classes

### InstallationNote

**Inherits from**: TransactionBase

#### Methods

##### __init__(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### is_serial_no_added(self, item_code, serial_no)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| item_code | None | - | - |
| serial_no | None | - | - |


##### is_serial_no_exist(self, item_code, serial_no)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| item_code | None | - | - |
| serial_no | None | - | - |


##### get_prevdoc_serial_no(self, prevdoc_detail_docname)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| prevdoc_detail_docname | None | - | - |


##### is_serial_no_match(self, cur_s_no, prevdoc_s_no, prevdoc_docname)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| cur_s_no | None | - | - |
| prevdoc_s_no | None | - | - |
| prevdoc_docname | None | - | - |


##### validate_serial_no(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_installation_date(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### check_item_table(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_update(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_submit(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_cancel(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |



