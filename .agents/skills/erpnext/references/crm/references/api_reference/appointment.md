# API Reference: appointment.py

**Language**: Python

**Source**: `doctype/appointment/appointment.py`

---

## Classes

### Appointment

**Inherits from**: Document

#### Methods

##### find_lead_by_email(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### find_customer_by_email(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### before_insert(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### after_insert(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### send_confirmation_email(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_change(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_verified(self, email)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| email | None | - | - |


##### create_lead_and_link(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### auto_assign(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_assignee_from_latest_opportunity(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### create_calendar_event(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _get_verify_url(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### assign_agent(self, agent)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| agent | None | - | - |




## Functions

### _get_agents_sorted_by_asc_workload(date)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| date | None | - | - |

**Returns**: (none)



### _get_agent_list_as_strings()

**Returns**: (none)



### _check_agent_availability(agent_email, scheduled_time)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| agent_email | None | - | - |
| scheduled_time | None | - | - |

**Returns**: (none)



### _get_employee_from_user(user)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| user | None | - | - |

**Returns**: (none)


