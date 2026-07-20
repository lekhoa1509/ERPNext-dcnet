# API Reference: test_sales_order_analysis.py

**Language**: Python

**Source**: `report/sales_order_analysis/test_sales_order_analysis.py`

---

## Classes

### TestSalesOrderAnalysis

**Inherits from**: IntegrationTestCase

#### Methods

##### create_sales_order(self, transaction_date, do_not_save = False, do_not_submit = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| transaction_date | None | - | - |
| do_not_save | None | False | - |
| do_not_submit | None | False | - |


##### create_sales_invoice(self, so, do_not_save = False, do_not_submit = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| so | None | - | - |
| do_not_save | None | False | - |
| do_not_submit | None | False | - |


##### create_delivery_note(self, so, do_not_save = False, do_not_submit = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| so | None | - | - |
| do_not_save | None | False | - |
| do_not_submit | None | False | - |


##### test_01_so_to_deliver_and_bill(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_02_so_to_deliver(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_03_so_to_bill(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_04_so_completed(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_05_all_so_status(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_06_so_pending_delivery_with_multiple_delivery_notes(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_07_so_delivered_with_multiple_delivery_notes(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |



