# API Reference: valuation.py

**Language**: Python

**Source**: `valuation.py`

---

## Classes

### BinWiseValuation

**Inherits from**: ABC

#### Methods

##### add_stock(self, qty: float, rate: float) → None

**Decorators**: `@abstractmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| qty | float | - | - |
| rate | float | - | - |

**Returns**: `None`


##### remove_stock(self, qty: float, outgoing_rate: float = 0.0, rate_generator: Callable[[], float] | None = None, is_return_purchase_entry: bool = False) → list[StockBin]

**Decorators**: `@abstractmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| qty | float | - | - |
| outgoing_rate | float | 0.0 | - |
| rate_generator | Callable[[], float] | None | None | - |
| is_return_purchase_entry | bool | False | - |

**Returns**: `list[StockBin]`


##### state(self) → list[StockBin]

**Decorators**: `@abstractproperty`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `list[StockBin]`


##### get_total_stock_and_value(self) → tuple[float, float]

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `tuple[float, float]`


##### __repr__(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### __iter__(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### __eq__(self, other)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| other | None | - | - |




### FIFOValuation

Valuation method where a queue of all the incoming stock is maintained.

New stock is added at end of the queue.
Qty consumption happens on First In First Out basis.

Queue is implemented using "bins" of [qty, rate].

ref: https://en.wikipedia.org/wiki/FIFO_and_LIFO_accounting

**Inherits from**: BinWiseValuation

#### Methods

##### __init__(self, state: list[StockBin] | None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| state | list[StockBin] | None | - | - |


##### state(self) → list[StockBin]

Get current state of queue.

**Decorators**: `@property`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `list[StockBin]`


##### add_stock(self, qty: float, rate: float) → None

Update fifo queue with new stock.

args:
        qty: new quantity to add
        rate: incoming rate of new quantity

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| qty | float | - | - |
| rate | float | - | - |

**Returns**: `None`


##### remove_stock(self, qty: float, outgoing_rate: float = 0.0, rate_generator: Callable[[], float] | None = None, is_return_purchase_entry: bool = False) → list[StockBin]

Remove stock from the queue and return popped bins.

args:
        qty: quantity to remove
        rate: outgoing rate
        rate_generator: function to be called if queue is not found and rate is required.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| qty | float | - | - |
| outgoing_rate | float | 0.0 | - |
| rate_generator | Callable[[], float] | None | None | - |
| is_return_purchase_entry | bool | False | - |

**Returns**: `list[StockBin]`




### LIFOValuation

Valuation method where a *stack* of all the incoming stock is maintained.

New stock is added at top of the stack.
Qty consumption happens on Last In First Out basis.

Stack is implemented using "bins" of [qty, rate].

ref: https://en.wikipedia.org/wiki/FIFO_and_LIFO_accounting
Implementation detail: appends and pops both at end of list.

**Inherits from**: BinWiseValuation

#### Methods

##### __init__(self, state: list[StockBin] | None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| state | list[StockBin] | None | - | - |


##### state(self) → list[StockBin]

Get current state of stack.

**Decorators**: `@property`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `list[StockBin]`


##### add_stock(self, qty: float, rate: float) → None

Update lifo stack with new stock.

args:
        qty: new quantity to add
        rate: incoming rate of new quantity.

Behaviour of this is same as FIFO valuation.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| qty | float | - | - |
| rate | float | - | - |

**Returns**: `None`


##### remove_stock(self, qty: float, outgoing_rate: float = 0.0, rate_generator: Callable[[], float] | None = None, is_return_purchase_entry: bool = False) → list[StockBin]

Remove stock from the stack and return popped bins.

args:
        qty: quantity to remove
        rate: outgoing rate - ignored. Kept for backwards compatibility.
        rate_generator: function to be called if stack is not found and rate is required.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| qty | float | - | - |
| outgoing_rate | float | 0.0 | - |
| rate_generator | Callable[[], float] | None | None | - |
| is_return_purchase_entry | bool | False | - |

**Returns**: `list[StockBin]`




## Functions

### round_off_if_near_zero(number: float, precision: int = 7) → float

Rounds off the number to zero only if number is close to zero for decimal
specified in precision. Precision defaults to 7.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| number | float | - | - |
| precision | int | 7 | - |

**Returns**: `float`


