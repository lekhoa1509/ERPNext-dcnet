# API Reference: notifications.js

**Language**: JavaScript

**Source**: `public/js/frappe/ui/notifications/notifications.js`

---

## Classes

### Notifications

**Inherits from**: (none)

#### Methods

##### constructor(opts)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| opts | None | - | - |




### BaseNotificationsView

**Inherits from**: (none)

#### Methods

##### constructor(wrapper, parent, settings)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| wrapper | None | - | - |
| parent | None | - | - |
| settings | None | - | - |


##### appendTo(this.wrapper)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| this.wrapper | None | - | - |


##### make()




### NotificationsView

**Inherits from**: BaseNotificationsView

#### Methods

##### make()


##### find(".notifications-icon")

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| ".notifications-icon" | None | - | - |


##### attr("title", __("Notifications")

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| "title" | None | - | - |
| __("Notifications" | None | - | - |




### EventsView

**Inherits from**: BaseNotificationsView

#### Methods

##### make()


##### get_today()




### ChangelogFeedView

**Inherits from**: BaseNotificationsView

#### Methods

##### make()


##### render_changelog_feed_html(frappe.boot.changelog_feed || [])

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| frappe.boot.changelog_feed || [] | None | - | - |




## Functions

### get_headers_html(item)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item | None | - | - |

**Returns**: (none)



### get_event_html(event)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| event | None | - | - |

**Returns**: (none)



### get_changelog_feed_html(changelog_feed_item)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| changelog_feed_item | None | - | - |

**Returns**: (none)


