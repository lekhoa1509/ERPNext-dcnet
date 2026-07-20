# API Reference: test_base_document.py

**Language**: Python

**Source**: `tests/test_base_document.py`

---

## Classes

### TestExtensionA

**Inherits from**: BaseDocument

#### Methods

##### extension_method_a(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




### TestExtensionB

**Inherits from**: BaseDocument

#### Methods

##### extension_method_b(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




### TestToDoExtension

Extension class that overrides ToDo's validate method

**Inherits from**: BaseDocument

#### Methods

##### validate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### extension_method(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




### TestBaseDocument

**Inherits from**: IntegrationTestCase

#### Methods

##### test_docstatus(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_get_extended_class_with_no_extensions(self)

Test that _get_extended_class returns the base class when no extensions are provided.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_get_extended_class_with_extensions(self)

Test that _get_extended_class properly combines extension classes with base class.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_extension_overrides_todo_method(self)

Test that an extension can override methods from the actual ToDo class

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_extension_invalid_path_raises_exception(self)

Test that an invalid extension path raises an appropriate exception

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_extended_class_is_pickleable(self)

Test that extended class instances can be pickled and unpickled correctly

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### clear_todo_controller_cache()

Helper method to clear controller cache for ToDo

**Returns**: (none)


