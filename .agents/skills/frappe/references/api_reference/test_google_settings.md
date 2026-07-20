# API Reference: test_google_settings.py

**Language**: Python

**Source**: `integrations/doctype/google_settings/test_google_settings.py`

---

## Classes

### TestGoogleSettings

**Inherits from**: IntegrationTestCase

#### Methods

##### setUp(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_picker_disabled(self)

Google Drive Picker should be disabled if it is not enabled in Google Settings.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_google_disabled(self)

Google Drive Picker should be disabled if Google integration is not enabled.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_picker_enabled(self)

If picker is enabled, get_file_picker_settings should return the credentials.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |



