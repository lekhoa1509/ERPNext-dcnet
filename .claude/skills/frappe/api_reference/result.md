# API Reference: result.py

**Language**: Python

**Source**: `testing/result.py`

---

## Classes

### TestResult

**Inherits from**: unittest.TextTestResult

#### Methods

##### __init__(self, stream, descriptions, verbosity)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| stream | None | - | - |
| descriptions | None | - | - |
| verbosity | None | - | - |


##### _setupStdout(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _restoreStdout(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### startTestRun(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### stopTestRun(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### startTest(self, test)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| test | None | - | - |


##### stopTest(self, test)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| test | None | - | - |


##### getTestMethodName(self, test)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| test | None | - | - |


##### addSuccess(self, test)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| test | None | - | - |


##### addError(self, test, err)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| test | None | - | - |
| err | None | - | - |


##### addFailure(self, test, err)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| test | None | - | - |
| err | None | - | - |


##### addSkip(self, test, reason)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| test | None | - | - |
| reason | None | - | - |


##### addExpectedFailure(self, test, err)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| test | None | - | - |
| err | None | - | - |


##### addUnexpectedSuccess(self, test)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| test | None | - | - |


##### printErrors(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### printErrorList(self, flavour, errors, color)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| flavour | None | - | - |
| errors | None | - | - |
| color | None | - | - |


##### __str__(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _write_result(self, test, status, color, suffix = '')

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| test | None | - | - |
| status | None | - | - |
| color | None | - | - |
| suffix | None | '' | - |




### FrappeTestResult

**Inherits from**: unittest.TextTestResult

#### Methods

##### __init__(self, stream, descriptions, verbosity)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| stream | None | - | - |
| descriptions | None | - | - |
| verbosity | None | - | - |


##### startTest(self, test)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| test | None | - | - |


##### getTestMethodName(self, test)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| test | None | - | - |


##### addSuccess(self, test)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| test | None | - | - |


##### addError(self, test, err)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| test | None | - | - |
| err | None | - | - |


##### addFailure(self, test, err)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| test | None | - | - |
| err | None | - | - |


##### addSkip(self, test, reason)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| test | None | - | - |
| reason | None | - | - |


##### addExpectedFailure(self, test, err)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| test | None | - | - |
| err | None | - | - |


##### addUnexpectedSuccess(self, test)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| test | None | - | - |



