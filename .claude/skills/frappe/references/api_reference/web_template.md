# API Reference: web_template.py

**Language**: Python

**Source**: `website/doctype/web_template/web_template.py`

---

## Classes

### WebTemplate

**Inherits from**: Document

#### Methods

##### validate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### before_save(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_update(self)

Clear cache for all Web Pages in which this template is used

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_trash(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### export_to_files(self)

Export Web Template to a new folder.

Doc is exported as JSON. The content of the `template` field gets
written into a separate HTML file. The template should not be contained
in the JSON.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### import_from_files(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### create_template_file(self, html = None)

Touch a HTML file for the Web Template and add existing content, if any.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| html | None | None | - |


##### get_template_folder(self)

Return the absolute path to the template's folder.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_template_path(self)

Return the absolute path to the template's HTML file.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_template(self, standard = False)

Get the jinja template string.

Params:
standard - if True, look on the disk instead of in the database.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| standard | None | False | - |


##### render(self, values = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| values | None | None | - |



