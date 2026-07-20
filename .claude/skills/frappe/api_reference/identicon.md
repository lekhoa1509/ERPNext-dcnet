# API Reference: identicon.py

**Language**: Python

**Source**: `utils/identicon.py`

---

## Classes

### Identicon

**Inherits from**: (none)

#### Methods

##### __init__(self, str_, background = '#fafbfc')

`str_` is the string used to generate the identicon.
`background` is the background of the identicon.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| str_ | None | - | - |
| background | None | '#fafbfc' | - |


##### digest(self, str_)

Return an MD5 numeric hash.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| str_ | None | - | - |


##### calculate(self)

Creates the identicon.
First three bytes are used to generate the color,
remaining bytes are used to create the drawing

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### generate(self)

Save and show calculated identicon

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### base64(self, format = 'PNG')

Return the identicon's base64

Created by: liuzheng712
Bug report: https://github.com/liuzheng712/identicons/issues

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| format | None | 'PNG' | - |



