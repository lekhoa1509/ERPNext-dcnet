# API Reference: exceptions.py

**Language**: Python

**Source**: `exceptions.py`

---

## Classes

### SiteNotSpecifiedError

**Inherits from**: Exception

#### Methods

##### __init__(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




### DatabaseModificationError

Error raised when attempting to modify the database in a read-only document context.

**Inherits from**: Exception



### UrlSchemeNotSupported

**Inherits from**: Exception



### ValidationError

**Inherits from**: Exception



### FrappeTypeError

**Inherits from**: TypeError



### AuthenticationError

**Inherits from**: Exception



### SessionExpired

**Inherits from**: Exception



### PermissionError

**Inherits from**: Exception



### DoesNotExistError

**Inherits from**: ValidationError

#### Methods

##### __init__(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




### PageDoesNotExistError

**Inherits from**: ValidationError



### NameError

**Inherits from**: Exception



### OutgoingEmailError

**Inherits from**: Exception



### SessionStopped

**Inherits from**: Exception



### UnsupportedMediaType

**Inherits from**: Exception



### RequestToken

**Inherits from**: Exception



### Redirect

**Inherits from**: Exception

#### Methods

##### __init__(self, http_status_code: int = 301)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| http_status_code | int | 301 | - |




### CSRFTokenError

**Inherits from**: Exception



### TooManyRequestsError

**Inherits from**: Exception



### ImproperDBConfigurationError

Used when frappe detects that database or tables are not properly
configured

**Inherits from**: Exception

#### Methods

##### __init__(self, reason, msg = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| reason | None | - | - |
| msg | None | None | - |




### DuplicateEntryError

**Inherits from**: NameError



### DataError

**Inherits from**: ValidationError



### UnknownDomainError

**Inherits from**: Exception



### MappingMismatchError

**Inherits from**: ValidationError



### InvalidStatusError

**Inherits from**: ValidationError



### MandatoryError

**Inherits from**: ValidationError



### NonNegativeError

**Inherits from**: ValidationError



### InvalidSignatureError

**Inherits from**: ValidationError



### RateLimitExceededError

**Inherits from**: ValidationError



### CannotChangeConstantError

**Inherits from**: ValidationError



### CharacterLengthExceededError

**Inherits from**: ValidationError



### UpdateAfterSubmitError

**Inherits from**: ValidationError



### LinkValidationError

**Inherits from**: ValidationError



### CancelledLinkError

**Inherits from**: LinkValidationError



### DocstatusTransitionError

**Inherits from**: ValidationError



### TimestampMismatchError

**Inherits from**: ValidationError



### EmptyTableError

**Inherits from**: ValidationError



### LinkExistsError

**Inherits from**: ValidationError



### InvalidEmailAddressError

**Inherits from**: ValidationError



### InvalidNameError

**Inherits from**: ValidationError



### InvalidPhoneNumberError

**Inherits from**: ValidationError



### TemplateNotFoundError

**Inherits from**: ValidationError



### UniqueValidationError

**Inherits from**: ValidationError



### AppNotInstalledError

**Inherits from**: ValidationError



### IncorrectSitePath

**Inherits from**: NotFound



### ImplicitCommitError

**Inherits from**: ValidationError



### RetryBackgroundJobError

**Inherits from**: Exception



### DocumentLockedError

**Inherits from**: ValidationError



### CircularLinkingError

**Inherits from**: ValidationError



### SecurityException

**Inherits from**: Exception



### InvalidColumnName

**Inherits from**: ValidationError



### IncompatibleApp

**Inherits from**: ValidationError



### InvalidDates

**Inherits from**: ValidationError



### DataTooLongException

**Inherits from**: ValidationError



### FileAlreadyAttachedException

**Inherits from**: Exception



### DocumentAlreadyRestored

**Inherits from**: ValidationError



### AttachmentLimitReached

**Inherits from**: ValidationError



### QueryTimeoutError

**Inherits from**: Exception



### QueryDeadlockError

**Inherits from**: Exception



### InReadOnlyMode

**Inherits from**: ValidationError



### SessionBootFailed

**Inherits from**: ValidationError



### QueueOverloaded

**Inherits from**: ValidationError



### PrintFormatError

**Inherits from**: ValidationError



### TooManyWritesError

**Inherits from**: Exception



### InvalidAuthorizationHeader

**Inherits from**: CSRFTokenError



### InvalidAuthorizationPrefix

**Inherits from**: CSRFTokenError



### InvalidAuthorizationToken

**Inherits from**: CSRFTokenError



### InvalidDatabaseFile

**Inherits from**: ValidationError



### ExecutableNotFound

**Inherits from**: FileNotFoundError



### InvalidRoundingMethod

**Inherits from**: FileNotFoundError



### InvalidRemoteException

**Inherits from**: Exception



### LinkExpired

**Inherits from**: ValidationError



### CommandFailedError

**Inherits from**: Exception

#### Methods

##### __init__(self, message: str, out: str, err: str)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| message | str | - | - |
| out | str | - | - |
| err | str | - | - |



