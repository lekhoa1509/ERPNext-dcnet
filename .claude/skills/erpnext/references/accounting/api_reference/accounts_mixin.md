# API Reference: accounts_mixin.py

**Language**: Python

**Source**: `test/accounts_mixin.py`

---

## Classes

### AccountsTestMixin

**Inherits from**: (none)

#### Methods

##### create_customer(self, customer_name = '_Test Customer', currency = None, default_account = None, company = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| customer_name | None | '_Test Customer' | - |
| currency | None | None | - |
| default_account | None | None | - |
| company | None | None | - |


##### create_supplier(self, supplier_name = '_Test Supplier', currency = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| supplier_name | None | '_Test Supplier' | - |
| currency | None | None | - |


##### create_item(self, item_name = '_Test Item', is_stock = 0, warehouse = None, company = None, valuation_rate = 0)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| item_name | None | '_Test Item' | - |
| is_stock | None | 0 | - |
| warehouse | None | None | - |
| company | None | None | - |
| valuation_rate | None | 0 | - |


##### create_company(self, company_name = '_Test Company', abbr = '_TC')

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| company_name | None | '_Test Company' | - |
| abbr | None | '_TC' | - |


##### enable_advance_as_liability(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### disable_advance_as_liability(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### identify_default_warehouses(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### create_usd_receivable_account(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### create_usd_payable_account(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### clear_old_entries(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### create_price_list(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |



