# API Reference: push_notification.py

**Language**: Python

**Source**: `push_notification.py`

---

## Classes

### PushNotification

**Inherits from**: (none)

#### Methods

##### __init__(self, project_name: str)

:param project_name: (str) The name of the project.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| project_name | str | - | - |


##### add_token(self, user_id: str, token: str) → tuple[bool, str]

Add a token for a user.

:param user_id: (str) The ID of the user. This should be user's unique identifier.
:param token: (str) The token to be added.
:return: tuple[bool, str] First element is the success status, second element is the message.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| user_id | str | - | - |
| token | str | - | - |

**Returns**: `tuple[bool, str]`


##### remove_token(self, user_id: str, token: str) → tuple[bool, str]

Remove a token for a user.

:param user_id: (str) The ID of the user. This should be user's unique identifier.
:param token: (str) The token to be removed.
:return: tuple[bool, str] First element is the success status, second element is the message.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| user_id | str | - | - |
| token | str | - | - |

**Returns**: `tuple[bool, str]`


##### add_topic(self, topic_name: str) → bool

Add a notification topic.

:param topic_name: (str) The name of the topic.
:return: bool True if successful, False otherwise.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| topic_name | str | - | - |

**Returns**: `bool`


##### remove_topic(self, topic_name: str) → bool

Remove a notification topic.

:param topic_name: (str) The name of the topic.
:return: bool True if successful, False otherwise.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| topic_name | str | - | - |

**Returns**: `bool`


##### subscribe_topic(self, user_id: str, topic_name: str) → bool

Subscribe a user to a topic.

:param user_id: (str) The ID of the user. This should be user's unique identifier.
:param topic_name: (str) The name of the topic. This topic should be already created.
:return: bool True if successful, False otherwise.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| user_id | str | - | - |
| topic_name | str | - | - |

**Returns**: `bool`


##### unsubscribe_topic(self, user_id: str, topic_name: str) → bool

Unsubscribe a user from a topic.

:param user_id: (str) The ID of the user. This should be user's unique identifier.
:param topic_name: (str) The name of the topic. This topic should be already created.
:return: bool True if successful, False otherwise.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| user_id | str | - | - |
| topic_name | str | - | - |

**Returns**: `bool`


##### send_notification_to_user(self, user_id: str, title: str, body: str, link: str | None = None, icon: str | None = None, data: dict | None = None, truncate_body: bool = True, strip_html: bool = True) → bool

Send notification to a user.

:param user_id: (str) The ID of the user. This should be user's unique identifier.
:param title: (str) The title of the notification.
:param body: (str) The body of the notification. At max 1000 characters.
:param link: (str) The link to be opened when the notification is clicked.
:param icon: (str) The icon to be shown in the notification.
:param data: (dict) The data to be sent with the notification. This can be used to provide extra information while dealing with in-app notifications.
:param truncate_body: (bool) Whether to truncate the body or not. If True, the body will be truncated to 1000 characters.
:param strip_html: (bool) Whether to strip HTML tags from the body or not.
:return: bool True if the request queued successfully, False otherwise.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| user_id | str | - | - |
| title | str | - | - |
| body | str | - | - |
| link | str | None | None | - |
| icon | str | None | None | - |
| data | dict | None | None | - |
| truncate_body | bool | True | - |
| strip_html | bool | True | - |

**Returns**: `bool`


##### send_notification_to_topic(self, topic_name: str, title: str, body: str, link: str | None = None, icon: str | None = None, data: dict | None = None, truncate_body: bool = True, strip_html: bool = True) → bool

Send notification to a notification topic.

:param topic_name: (str) The name of the topic. This topic should be already created.
:param title: (str) The title of the notification.
:param body: (str) The body of the notification. At max 1000 characters.
:param link: (str) The link to be opened when the notification is clicked.
:param icon: (str) The icon to be shown in the notification.
:param data: (dict) The data to be sent with the notification. This can be used to provide extra information while dealing with in-app notifications.
:param truncate_body: (bool) Whether to truncate the body or not. If True, the body will be truncated to 1000 characters.
:param strip_html: (bool) Whether to strip HTML tags from the body or not.
:return: bool True if the request queued successfully, False otherwise.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| topic_name | str | - | - |
| title | str | - | - |
| body | str | - | - |
| link | str | None | None | - |
| icon | str | None | None | - |
| data | dict | None | None | - |
| truncate_body | bool | True | - |
| strip_html | bool | True | - |

**Returns**: `bool`


##### is_enabled(self) → bool

Check whether the push notification relay is enabled or not.

:return: bool True if enabled, False otherwise.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `bool`


##### _get_credential(self) → tuple[str, str]

Register & Get the API key and secret from the central relay server.
Also store the API key and secret in the database for future use.

NOTE: This method is private and should not be called directly.

:return: tuple[str, str] The API key and secret.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `tuple[str, str]`


##### _send_post_request(self, method: str, params: dict, use_authentication: bool = True)

Send a POST request to the central relay server.

NOTE: This method is private and should not be called directly.

:param method: (str) The method to be called on the central relay server.
:param params: (dict) The parameters to be sent with the request.
:param use_authentication: (bool) Whether to use authentication or not.
:return: (dict) Response data of the request.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| method | str | - | - |
| params | dict | - | - |
| use_authentication | bool | True | - |


##### _site_name(self) → str

**Decorators**: `@property`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `str`


##### _site_protocol(self) → str

**Decorators**: `@property`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `str`


##### _site_port(self) → str

**Decorators**: `@property`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `str`




## Functions

### auth_webhook(secret: str)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| secret | str | - | - |

**Returns**: (none)



### subscribe(fcm_token: str, project_name: str) → dict

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| fcm_token | str | - | - |
| project_name | str | - | - |

**Returns**: `dict`



### unsubscribe(fcm_token: str, project_name: str) → dict

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| fcm_token | str | - | - |
| project_name | str | - | - |

**Returns**: `dict`


