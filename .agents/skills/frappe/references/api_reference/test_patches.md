# API Reference: test_patches.py

**Language**: Python

**Source**: `tests/test_patches.py`

---

## Classes

### TestPatches

**Inherits from**: IntegrationTestCase

#### Methods

##### test_patch_module_names(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_get_patch_list(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_all_patches_are_marked_completed(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




### TestPatchReader

**Inherits from**: IntegrationTestCase

#### Methods

##### get_patches(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_empty_file(self, _file)

**Decorators**: `@patch('builtins.open', new_callable=mock_open, read_data=EMTPY_FILE)`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| _file | None | - | - |


##### test_empty_sections(self, _file)

**Decorators**: `@patch('builtins.open', new_callable=mock_open, read_data=EMTPY_SECTION)`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| _file | None | - | - |


##### test_new_style(self, _file)

**Decorators**: `@patch('builtins.open', new_callable=mock_open, read_data=FILLED_SECTIONS)`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| _file | None | - | - |


##### test_old_style(self, _file)

**Decorators**: `@patch('builtins.open', new_callable=mock_open, read_data=OLD_STYLE_PATCH_TXT)`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| _file | None | - | - |


##### test_new_style_edge_cases(self, _file)

**Decorators**: `@patch('builtins.open', new_callable=mock_open, read_data=EDGE_CASES)`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| _file | None | - | - |


##### test_ignore_comments(self, _file)

**Decorators**: `@patch('builtins.open', new_callable=mock_open, read_data=COMMENTED_OUT)`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| _file | None | - | - |


##### test_verify_patch_txt(self)

Make sure all patches/**.py files are part of patches.txt

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### check_patch_files(app)

Make sure all patches/**.py files are part of patches.txt

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| app | None | - | - |

**Returns**: (none)



### _get_dotted_path(file: Path, app) → str

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| file | Path | - | - |
| app | None | - | - |

**Returns**: `str`


