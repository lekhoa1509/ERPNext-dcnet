# API Reference: test_module_profile.py

**Language**: Python

**Source**: `core/doctype/module_profile/test_module_profile.py`

---

## Classes

### TestModuleProfile

**Inherits from**: IntegrationTestCase

#### Methods

##### setUp(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_make_new_module_profile(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_multiple_block_modules(self)

Assign multiple blocked modules from profile to user

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_update_module_profile_propagates_to_users(self)

Updating block_modules in profile should update linked users

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_clear_block_modules(self)

Clearing block_modules in profile should also clear them for users

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_multiple_users_same_profile(self)

Updates should propagate to all users linked to the same profile

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_switch_user_module_profile(self)

Switching user to a different profile updates their block_modules

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |



