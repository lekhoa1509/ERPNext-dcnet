# API Reference: subscription.py

**Language**: Python

**Source**: `doctype/subscription/subscription.py`

---

## Classes

### InvoiceCancelled

**Inherits from**: frappe.ValidationError



### InvoiceNotCancelled

**Inherits from**: frappe.ValidationError



### Subscription

**Inherits from**: Document

#### Methods

##### before_insert(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_subscription_period(self, date: DateTimeLikeObject | None = None)

Subscription period is the period to be billed. This method updates the
beginning of the billing period and end of the billing period.
The beginning of the billing period is represented in the doctype as
`current_invoice_start` and the end of the billing period is represented
as `current_invoice_end`.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| date | DateTimeLikeObject | None | None | - |


##### _get_subscription_period(self, date: DateTimeLikeObject | None = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| date | DateTimeLikeObject | None | None | - |


##### get_current_invoice_start(self, date: DateTimeLikeObject | None = None) → DateTimeLikeObject

This returns the date of the beginning of the current billing period.
If the `date` parameter is not given , it will be automatically set as today's
date.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| date | DateTimeLikeObject | None | None | - |

**Returns**: `DateTimeLikeObject`


##### get_current_invoice_end(self, date: DateTimeLikeObject | None = None) → DateTimeLikeObject

This returns the date of the end of the current billing period.
If the subscription is in trial period, it will be set as the end of the
trial period.
If is not in a trial period, it will be `x` days from the beginning of the
current billing period where `x` is the billing interval from the
`Subscription Plan` in the `Subscription`.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| date | DateTimeLikeObject | None | None | - |

**Returns**: `DateTimeLikeObject`


##### validate_plans_billing_cycle(billing_cycle_data: list[dict[str, str]]) → None

Makes sure that all `Subscription Plan` in the `Subscription` have the
same billing interval

**Decorators**: `@staticmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| billing_cycle_data | list[dict[str, str]] | - | - |

**Returns**: `None`


##### get_billing_cycle_and_interval(self) → list[dict[str, str]]

Returns a dict representing the billing interval and cycle for this `Subscription`.
You shouldn't need to call this directly. Use `get_billing_cycle` instead.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `list[dict[str, str]]`


##### get_billing_cycle_data(self) → dict[str, int]

Returns dict contain the billing cycle data.
You shouldn't need to call this directly. Use `get_billing_cycle` instead.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `dict[str, int]`


##### set_subscription_status(self, posting_date: DateTimeLikeObject | None = None) → None

Sets the status of the `Subscription`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| posting_date | DateTimeLikeObject | None | None | - |

**Returns**: `None`


##### is_trialling(self) → bool

Returns `True` if the `Subscription` is in trial period.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `bool`


##### period_has_passed(end_date: DateTimeLikeObject, posting_date: DateTimeLikeObject | None = None) → bool

Returns true if the given `end_date` has passed

**Decorators**: `@staticmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| end_date | DateTimeLikeObject | - | - |
| posting_date | DateTimeLikeObject | None | None | - |

**Returns**: `bool`


##### get_status_for_past_grace_period(self) → str

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `str`


##### is_past_grace_period(self, posting_date: DateTimeLikeObject | None = None) → bool

Returns `True` if the grace period for the `Subscription` has passed

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| posting_date | DateTimeLikeObject | None | None | - |

**Returns**: `bool`


##### current_invoice_is_past_due(self, posting_date: DateTimeLikeObject | None = None) → bool

Returns `True` if the current generated invoice is overdue

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| posting_date | DateTimeLikeObject | None | None | - |

**Returns**: `bool`


##### invoice_document_type(self) → str

**Decorators**: `@property`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `str`


##### validate(self) → None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `None`


##### validate_party_billing_currency(self)

Subscription should be of the same currency as the Party's default billing currency or company default.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_trial_period(self) → None

Runs sanity checks on trial period dates for the `Subscription`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `None`


##### validate_end_date(self) → None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `None`


##### validate_to_follow_calendar_months(self) → None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `None`


##### generate_invoice(self, from_date: DateTimeLikeObject | None = None, to_date: DateTimeLikeObject | None = None, posting_date: DateTimeLikeObject | None = None) → Document

Creates a `Invoice` for the `Subscription`, updates `self.invoices` and
saves the `Subscription`.
Backwards compatibility

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| from_date | DateTimeLikeObject | None | None | - |
| to_date | DateTimeLikeObject | None | None | - |
| posting_date | DateTimeLikeObject | None | None | - |

**Returns**: `Document`


##### create_invoice(self, from_date: DateTimeLikeObject | None = None, to_date: DateTimeLikeObject | None = None, posting_date: DateTimeLikeObject | None = None) → Document

Creates a `Invoice`, submits it and returns it

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| from_date | DateTimeLikeObject | None | None | - |
| to_date | DateTimeLikeObject | None | None | - |
| posting_date | DateTimeLikeObject | None | None | - |

**Returns**: `Document`


##### get_items_from_plans(self, plans: list[dict[str, str]], prorate: int = 0) → list[dict]

Returns the `Item`s linked to `Subscription Plan`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| plans | list[dict[str, str]] | - | - |
| prorate | int | 0 | - |

**Returns**: `list[dict]`


##### process(self, posting_date: DateTimeLikeObject | None = None) → bool

To be called by task periodically. It checks the subscription and takes appropriate action
as need be. It calls either of these methods depending the `Subscription` status:
1. `process_for_active`
2. `process_for_past_due`

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| posting_date | DateTimeLikeObject | None | None | - |

**Returns**: `bool`


##### can_generate_new_invoice(self, posting_date: DateTimeLikeObject | None = None) → bool

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| posting_date | DateTimeLikeObject | None | None | - |

**Returns**: `bool`


##### is_current_invoice_generated(self, _current_start_date: DateTimeLikeObject | None = None, _current_end_date: DateTimeLikeObject | None = None) → bool

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| _current_start_date | DateTimeLikeObject | None | None | - |
| _current_end_date | DateTimeLikeObject | None | None | - |

**Returns**: `bool`


##### current_invoice(self) → Document | None

Adds property for accessing the current_invoice

**Decorators**: `@property`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `Document | None`


##### get_current_invoice(self) → Document | None

Returns the most recent generated invoice.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `Document | None`


##### cancel_subscription_at_period_end(self) → None

Called when `Subscription.cancel_at_period_end` is truthy

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `None`


##### invoices(self) → list[dict]

**Decorators**: `@property`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `list[dict]`


##### is_paid(invoice: Document) → bool

Return `True` if the given invoice is paid

**Decorators**: `@staticmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| invoice | Document | - | - |

**Returns**: `bool`


##### has_outstanding_invoice(self) → int

Returns `True` if the most recent invoice for the `Subscription` is not paid

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `int`


##### cancel_subscription(self) → None

This sets the subscription as cancelled. It will stop invoices from being generated
but it will not affect already created invoices.

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `None`


##### restart_subscription(self, posting_date: DateTimeLikeObject | None = None) → None

This sets the subscription as active. The subscription will be made to be like a new
subscription and the `Subscription` will lose all the history of generated invoices
it has.

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| posting_date | DateTimeLikeObject | None | None | - |

**Returns**: `None`


##### force_fetch_subscription_updates(self)

Process Subscription and create Invoices even if current date doesn't lie between current_invoice_start and currenct_invoice_end
It makes use of 'Proces Subscription' to force processing in a specific 'posting_date'

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### is_prorate() → int

**Returns**: `int`



### get_prorata_factor(period_end: DateTimeLikeObject, period_start: DateTimeLikeObject, is_prepaid: int | None = None) → int | float

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| period_end | DateTimeLikeObject | - | - |
| period_start | DateTimeLikeObject | - | - |
| is_prepaid | int | None | None | - |

**Returns**: `int | float`



### process_all(subscription: list, posting_date: DateTimeLikeObject | None = None) → None

Task to updates the status of all `Subscription` apart from those that are cancelled

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| subscription | list | - | - |
| posting_date | DateTimeLikeObject | None | None | - |

**Returns**: `None`


