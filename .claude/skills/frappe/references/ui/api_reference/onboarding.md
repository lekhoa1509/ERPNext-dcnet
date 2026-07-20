# API Reference: onboarding.js

**Language**: JavaScript

**Source**: `frappe/Onboarding/onboarding.js`

---

## Functions

### useOnboarding(appName)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| appName | None | - | - |

**Returns**: (none)



### skip(step, callback = null)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| step | None | - | - |
| callback | None | null | - |

**Returns**: (none)



### skipAll(callback = null)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| callback | None | null | - |

**Returns**: (none)



### reset(step, callback = null)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| step | None | - | - |
| callback | None | null | - |

**Returns**: (none)



### resetAll(callback = null)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| callback | None | null | - |

**Returns**: (none)



### updateOnboardingStep(step, value = true, skipped = false, callback = null)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| step | None | - | - |
| value | None | true | - |
| skipped | None | false | - |
| callback | None | null | - |

**Returns**: (none)



### updateAll(value, callback = null)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| value | None | - | - |
| callback | None | null | - |

**Returns**: (none)



### updateUserOnboardingStatus(steps)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| steps | None | - | - |

**Returns**: (none)



### syncStatus()

**Returns**: (none)



### setUp(steps)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| steps | None | - | - |

**Returns**: (none)


