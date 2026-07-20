# API Reference: delivery_trip.py

**Language**: Python

**Source**: `doctype/delivery_trip/delivery_trip.py`

---

## Classes

### DeliveryTrip

**Inherits from**: Document

#### Methods

##### __init__(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_discard(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_update(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_trash(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_submit(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_update_after_submit(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_cancel(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_stop_addresses(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_delivery_note_not_draft(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_status(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_delivery_notes(self, delete = False)

Update all connected Delivery Notes with Delivery Trip details
(Driver, Vehicle, etc.). If `delete` is `True`, then details
are removed.

Args:
        delete (bool, optional): Defaults to `False`. `True` if driver details need to be emptied, else `False`.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| delete | None | False | - |


##### process_route(self, optimize)

Estimate the arrival times for each stop in the Delivery Trip.
If `optimize` is True, the stops will be re-arranged, based
on the optimized order, before estimating the arrival times.

Args:
        optimize (bool): True if route needs to be optimized, else False

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| optimize | None | - | - |


##### form_route_list(self, optimize)

Form a list of address routes based on the delivery stops. If locks
are present, and the routes need to be optimized, then they will be
split into sublists at the specified lock position(s).

Args:
        optimize (bool): `True` if route needs to be optimized, else `False`

Returns:
        (list of list of str): List of address routes split at locks, if optimize is `True`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| optimize | None | - | - |


##### rearrange_stops(self, optimized_order, start)

Re-arrange delivery stops based on order optimized
for vehicle routing problems.

Args:
        optimized_order (list of int): The index-based optimized order of the route
        start (int): The index at which to start the rearrangement

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| optimized_order | None | - | - |
| start | None | - | - |


##### get_directions(self, route, optimize)

Retrieve map directions for a given route and departure time.
If optimize is `True`, Google Maps will return an optimized
order for the intermediate waypoints.

NOTE: Google's API does take an additional `departure_time` key,
but it only works for routes without any waypoints.

Args:
        route (list of str): Route addresses (origin -> waypoint(s), if any -> destination)
        optimize (bool): `True` if route needs to be optimized, else `False`

Returns:
        (dict): Route legs and, if `optimize` is `True`, optimized waypoint order

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| route | None | - | - |
| optimize | None | - | - |




## Functions

### get_contact_and_address(name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| name | None | - | - |

**Returns**: (none)



### get_default_contact(out, name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| out | None | - | - |
| name | None | - | - |

**Returns**: (none)



### get_default_address(out, name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| out | None | - | - |
| name | None | - | - |

**Returns**: (none)



### get_contact_display(contact)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| contact | None | - | - |

**Returns**: (none)



### sanitize_address(address)

Remove HTML breaks in a given address

Args:
        address (str): Address to be sanitized

Returns:
        (str): Sanitized address

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| address | None | - | - |

**Returns**: (none)



### notify_customers(delivery_trip)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| delivery_trip | None | - | - |

**Returns**: (none)



### get_attachments(delivery_stop)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| delivery_stop | None | - | - |

**Returns**: (none)



### get_driver_email(driver)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| driver | None | - | - |

**Returns**: (none)


