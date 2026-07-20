# API Reference: purchase_receipt.py

**Language**: Python

**Source**: `doctype/purchase_receipt/purchase_receipt.py`

---

## Classes

### PurchaseReceipt

**Inherits from**: BuyingController

#### Methods

##### __init__(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### before_validate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_uom_is_integer(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_cwip_accounts(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_provisional_expense_account(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_with_previous_doc(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### po_required(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_items_quality_inspection(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_already_received_qty(self, po, po_detail)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| po | None | - | - |
| po_detail | None | - | - |


##### get_po_qty_and_warehouse(self, po_detail)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| po_detail | None | - | - |


##### check_on_hold_or_closed_status(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_submit(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_received_qty_if_from_pp(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### check_next_docstatus(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_cancel(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### before_cancel(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### remove_amount_difference_with_purchase_invoice(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_gl_entries(self, inventory_account_map = None, via_landed_cost_voucher = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| inventory_account_map | None | None | - |
| via_landed_cost_voucher | None | False | - |


##### make_item_gl_entries(self, gl_entries, inventory_account_map = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| gl_entries | None | - | - |
| inventory_account_map | None | None | - |


##### add_provisional_gl_entry(self, item, gl_entries, posting_date, provisional_account, reverse = 0, item_amount = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| item | None | - | - |
| gl_entries | None | - | - |
| posting_date | None | - | - |
| provisional_account | None | - | - |
| reverse | None | 0 | - |
| item_amount | None | None | - |


##### is_landed_cost_booked_for_any_item(self) → bool

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `bool`


##### make_tax_gl_entries(self, gl_entries, via_landed_cost_voucher = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| gl_entries | None | - | - |
| via_landed_cost_voucher | None | False | - |


##### update_assets(self, item, valuation_rate)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| item | None | - | - |
| valuation_rate | None | - | - |


##### update_status(self, status)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| status | None | - | - |


##### update_billing_status(self, update_modified = True)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| update_modified | None | True | - |


##### reserve_stock(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### reserve_stock_for_sales_order(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### reserve_stock_for_production_plan(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_production_plan_references(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### enable_recalculate_rate_in_sles(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### get_stock_value_difference(voucher_no, voucher_detail_no, warehouse)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| voucher_no | None | - | - |
| voucher_detail_no | None | - | - |
| warehouse | None | - | - |

**Returns**: (none)



### update_billed_amount_based_on_po(po_details, update_modified = True, pr_doc = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| po_details | None | - | - |
| update_modified | None | True | - |
| pr_doc | None | None | - |

**Returns**: (none)



### get_purchase_receipts_against_po_details(po_details)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| po_details | None | - | - |

**Returns**: (none)



### get_billed_amount_against_pr(pr_items)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| pr_items | None | - | - |

**Returns**: (none)



### get_billed_amount_against_po(po_items)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| po_items | None | - | - |

**Returns**: (none)



### update_billing_percentage(pr_doc, update_modified = True, adjust_incoming_rate = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| pr_doc | None | - | - |
| update_modified | None | True | - |
| adjust_incoming_rate | None | False | - |

**Returns**: (none)



### get_billed_qty_against_purchase_receipt(pr_doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| pr_doc | None | - | - |

**Returns**: (none)



### get_billed_qty_against_purchase_order(pr_doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| pr_doc | None | - | - |

**Returns**: (none)



### adjust_incoming_rate_for_pr(doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |

**Returns**: (none)



### get_item_wise_returned_qty(pr_doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| pr_doc | None | - | - |

**Returns**: (none)



### make_purchase_invoice(source_name, target_doc = None, args = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| source_name | None | - | - |
| target_doc | None | None | - |
| args | None | None | - |

**Returns**: (none)



### get_invoiced_qty_map(purchase_receipt)

returns a map: {pr_detail: invoiced_qty}

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| purchase_receipt | None | - | - |

**Returns**: (none)



### get_returned_qty_map(purchase_receipt)

returns a map: {pr_detail: returned_qty}

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| purchase_receipt | None | - | - |

**Returns**: (none)



### make_purchase_return_against_rejected_warehouse(source_name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| source_name | None | - | - |

**Returns**: (none)



### make_purchase_return(source_name, target_doc = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| source_name | None | - | - |
| target_doc | None | None | - |

**Returns**: (none)



### update_purchase_receipt_status(docname, status)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| docname | None | - | - |
| status | None | - | - |

**Returns**: (none)



### make_stock_entry(source_name, target_doc = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| source_name | None | - | - |
| target_doc | None | None | - |

**Returns**: (none)



### make_inter_company_delivery_note(source_name, target_doc = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| source_name | None | - | - |
| target_doc | None | None | - |

**Returns**: (none)



### update_regional_gl_entries(gl_list, doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| gl_list | None | - | - |
| doc | None | - | - |

**Returns**: (none)



### make_lcv(doctype, docname)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| docname | None | - | - |

**Returns**: (none)



### set_missing_values(source, target)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| source | None | - | - |
| target | None | - | - |

**Returns**: (none)



### update_item(source_doc, target_doc, source_parent)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| source_doc | None | - | - |
| target_doc | None | - | - |
| source_parent | None | - | - |

**Returns**: (none)



### get_pending_qty(item_row)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item_row | None | - | - |

**Returns**: (none)



### select_item(d)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| d | None | - | - |

**Returns**: (none)



### set_missing_values(source, target)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| source | None | - | - |
| target | None | - | - |

**Returns**: (none)



### update_item(source_doc, target_doc, source_parent)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| source_doc | None | - | - |
| target_doc | None | - | - |
| source_parent | None | - | - |

**Returns**: (none)



### validate_account(account_type)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| account_type | None | - | - |

**Returns**: (none)



### make_item_asset_inward_gl_entry(item, stock_value_diff, stock_asset_account_name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item | None | - | - |
| stock_value_diff | None | - | - |
| stock_asset_account_name | None | - | - |

**Returns**: (none)



### make_stock_received_but_not_billed_entry(item)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item | None | - | - |

**Returns**: (none)



### make_landed_cost_gl_entries(item)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item | None | - | - |

**Returns**: (none)



### make_amount_difference_entry(item)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item | None | - | - |

**Returns**: (none)



### make_sub_contracting_gl_entries(item)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item | None | - | - |

**Returns**: (none)



### make_divisional_loss_gl_entry(item, outgoing_amount)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item | None | - | - |
| outgoing_amount | None | - | - |

**Returns**: (none)


