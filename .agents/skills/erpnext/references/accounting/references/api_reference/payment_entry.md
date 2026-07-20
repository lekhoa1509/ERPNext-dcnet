# API Reference: payment_entry.py

**Language**: Python

**Source**: `doctype/payment_entry/payment_entry.py`

---

## Classes

### InvalidPaymentEntry

**Inherits from**: ValidationError



### PaymentEntry

**Inherits from**: AccountsController

#### Methods

##### __init__(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### setup_party_account_field(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### before_save(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_submit(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_for_repost(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_update_after_submit(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_liability_account(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_cancel(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_payment_requests(self, cancel = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| cancel | None | False | - |


##### update_outstanding_amounts(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_duplicate_entry(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_bank_account_data(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_payment_type_with_outstanding(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_allocated_amount(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_allocated_amount_as_per_payment_request(self)

Allocated amount should not be greater than the outstanding amount of the Payment Request.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### term_based_allocation_enabled_for_reference(self, reference_doctype: str, reference_name: str) → bool

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| reference_doctype | str | - | - |
| reference_name | str | - | - |

**Returns**: `bool`


##### validate_allocated_amount_with_latest_data(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### delink_advance_entry_references(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_missing_values(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_missing_ref_details(self, force: bool = False, update_ref_details_only_for: list | None = None, reference_exchange_details: dict | None = None) → None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| force | bool | False | - |
| update_ref_details_only_for | list | None | None | - |
| reference_exchange_details | dict | None | None | - |

**Returns**: `None`


##### validate_payment_type(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_party_details(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_exchange_rate(self, ref_doc = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| ref_doc | None | None | - |


##### set_source_exchange_rate(self, ref_doc = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| ref_doc | None | None | - |


##### set_target_exchange_rate(self, ref_doc = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| ref_doc | None | None | - |


##### validate_mandatory(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_reference_documents(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_valid_reference_doctypes(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_paid_invoices(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_journal_entry(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_payment_schedule(self, cancel = 0)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| cancel | None | 0 | - |


##### get_allocated_amount_in_transaction_currency(self, allocated_amount, reference_doctype, reference_docname)

Payment Entry could be in base currency while reference's payment schedule
is always in transaction currency.
E.g.
* SI with base=INR and currency=USD
* SI with payment schedule in USD
* PE in INR (accounting done in base currency)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| allocated_amount | None | - | - |
| reference_doctype | None | - | - |
| reference_docname | None | - | - |


##### set_status(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_total_in_words(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### apply_taxes(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_amounts(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_amounts(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_received_amount(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_received_amount(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_amounts_after_tax(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_amounts_in_company_currency(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### calculate_base_allocated_amount_for_reference(self, d) → float

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| d | None | - | - |

**Returns**: `float`


##### set_total_allocated_amount(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_unallocated_amount(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_exchange_gain_loss(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_difference_amount(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_included_taxes(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### clear_unallocated_reference_document_rows(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_title(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_transaction_reference(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_remarks(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_transaction_currency_and_rate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### build_gl_map(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### make_gl_entries(self, cancel = 0, adv_adj = 0)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| cancel | None | 0 | - |
| adv_adj | None | 0 | - |


##### add_party_gl_entries(self, gl_entries)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| gl_entries | None | - | - |


##### make_advance_gl_entries(self, entry: object | dict = None, cancel: bool = 0, update_outstanding: str = 'Yes')

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| entry | object | dict | None | - |
| cancel | bool | 0 | - |
| update_outstanding | str | 'Yes' | - |


##### add_advance_gl_entries(self, gl_entries: list, entry: object | dict | None)

If 'entry' is passed, GL entries only for that reference is added.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| gl_entries | list | - | - |
| entry | object | dict | None | - | - |


##### get_dr_and_account_for_advances(self, reference)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| reference | None | - | - |


##### add_advance_gl_for_reference(self, gl_entries, invoice)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| gl_entries | None | - | - |
| invoice | None | - | - |


##### add_bank_gl_entries(self, gl_entries)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| gl_entries | None | - | - |


##### add_tax_gl_entries(self, gl_entries)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| gl_entries | None | - | - |


##### add_deductions_gl_entries(self, gl_entries)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| gl_entries | None | - | - |


##### get_party_account_for_taxes(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_value_in_transaction_currency(self, account_currency, gl_dict, field)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| account_currency | None | - | - |
| gl_dict | None | - | - |
| field | None | - | - |


##### on_recurring(self, reference_doc, auto_repeat_doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| reference_doc | None | - | - |
| auto_repeat_doc | None | - | - |


##### calculate_deductions(self, tax_details)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| tax_details | None | - | - |


##### set_gain_or_loss(self, account_details = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| account_details | None | None | - |


##### get_exchange_rate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### initialize_taxes(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### determine_exclusive_rate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### calculate_taxes(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_current_tax_amount(self, tax)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| tax | None | - | - |


##### get_current_tax_fraction(self, tax)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| tax | None | - | - |


##### set_matched_unset_payment_requests_to_response(self)

Find matched Payment Requests for those references which have no Payment Request set.

And set to `frappe.response` to show in the frontend for allocation.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### allocate_amount_to_references(self, paid_amount, paid_amount_change, allocate_payment_amount)

Allocate `Allocated Amount` and `Payment Request` against `Reference` based on `Paid Amount` and `Outstanding Amount`.

:param paid_amount: Paid Amount / Received Amount.
:param paid_amount_change: Flag to check if `Paid Amount` is changed or not.
:param allocate_payment_amount: Flag to allocate amount or not. (Payment Request is also dependent on this flag)

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| paid_amount | None | - | - |
| paid_amount_change | None | - | - |
| allocate_payment_amount | None | - | - |


##### set_matched_payment_requests(self, matched_payment_requests)

Set `Payment Request` against `Reference` based on `matched_payment_requests`.

:param matched_payment_requests: List of tuple of matched Payment Requests.

---
Example: [(reference_doctype, reference_name, allocated_amount, payment_request), ...]

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| matched_payment_requests | None | - | - |




## Functions

### get_matched_payment_request_of_references(references = None)

Get those `Payment Requests` which are matched with `References`.

        - Amount must be same.
        - Only single `Payment Request` available for this amount.

Example: [(reference_doctype, reference_name, allocated_amount, payment_request), ...]

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| references | None | None | - |

**Returns**: (none)



### get_references_outstanding_amount(references = None)

Fetch accurate outstanding amount of `References`.

    - If `Payment Term` is set, then fetch outstanding amount from `Payment Schedule`.
    - If `Payment Term` is not set, then fetch outstanding amount from `References` it self.

Example: {(reference_doctype, reference_name, payment_term): outstanding_amount, ...}

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| references | None | None | - |

**Returns**: (none)



### get_outstanding_of_references_with_payment_term(references = None)

Fetch outstanding amount of `References` which have `Payment Term` set.

Example: {(reference_doctype, reference_name, payment_term): outstanding_amount, ...}

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| references | None | None | - |

**Returns**: (none)



### get_outstanding_of_references_with_no_payment_term(references)

Fetch outstanding amount of `References` which have no `Payment Term` set.

        - Fetch outstanding amount from `References` it self.

Note: `None` is used for allocation of `Payment Request`
Example: {(reference_doctype, reference_name, None): outstanding_amount, ...}

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| references | None | - | - |

**Returns**: (none)



### get_payment_request_outstanding_set_in_references(references = None)

Fetch outstanding amount of `Payment Request` which are set in `References`.

Example: {payment_request: outstanding_amount, ...}

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| references | None | None | - |

**Returns**: (none)



### validate_inclusive_tax(tax, doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| tax | None | - | - |
| doc | None | - | - |

**Returns**: (none)



### get_outstanding_reference_documents(args, validate = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| args | None | - | - |
| validate | None | False | - |

**Returns**: (none)



### split_invoices_based_on_payment_terms(outstanding_invoices, company) → list

Split a list of invoices based on their payment terms.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| outstanding_invoices | None | - | - |
| company | None | - | - |

**Returns**: `list`



### get_currency_data(outstanding_invoices: list, company: str | None = None) → dict

Get currency and conversion data for a list of invoices.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| outstanding_invoices | list | - | - |
| company | str | None | None | - |

**Returns**: `dict`



### get_split_invoice_rows(invoice: dict, payment_term_template: str, exc_rates: dict) → list

Split invoice based on its payment schedule table.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| invoice | dict | - | - |
| payment_term_template | str | - | - |
| exc_rates | dict | - | - |

**Returns**: `list`



### get_orders_to_be_billed(posting_date, party_type, party, company, party_account_currency, company_currency, cost_center = None, filters = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| posting_date | None | - | - |
| party_type | None | - | - |
| party | None | - | - |
| company | None | - | - |
| party_account_currency | None | - | - |
| company_currency | None | - | - |
| cost_center | None | None | - |
| filters | None | None | - |

**Returns**: (none)



### get_negative_outstanding_invoices(party_type, party, party_account, party_account_currency, company_currency, cost_center = None, condition = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| party_type | None | - | - |
| party | None | - | - |
| party_account | None | - | - |
| party_account_currency | None | - | - |
| company_currency | None | - | - |
| cost_center | None | None | - |
| condition | None | None | - |

**Returns**: (none)



### get_party_details(company, party_type, party, date, cost_center = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| company | None | - | - |
| party_type | None | - | - |
| party | None | - | - |
| date | None | - | - |
| cost_center | None | None | - |

**Returns**: (none)



### get_account_details(account, date, cost_center = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| account | None | - | - |
| date | None | - | - |
| cost_center | None | None | - |

**Returns**: (none)



### get_company_defaults(company)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| company | None | - | - |

**Returns**: (none)



### get_outstanding_on_journal_entry(voucher_no, party_type, party)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| voucher_no | None | - | - |
| party_type | None | - | - |
| party | None | - | - |

**Returns**: (none)



### get_reference_details(reference_doctype, reference_name, party_account_currency, party_type = None, party = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| reference_doctype | None | - | - |
| reference_name | None | - | - |
| party_account_currency | None | - | - |
| party_type | None | None | - |
| party | None | None | - |

**Returns**: (none)



### get_payment_entry(dt, dn, party_amount = None, bank_account = None, bank_amount = None, party_type = None, payment_type = None, reference_date = None, created_from_payment_request = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| dt | None | - | - |
| dn | None | - | - |
| party_amount | None | None | - |
| bank_account | None | None | - |
| bank_amount | None | None | - |
| party_type | None | None | - |
| payment_type | None | None | - |
| reference_date | None | None | - |
| created_from_payment_request | None | False | - |

**Returns**: (none)



### get_open_payment_requests_for_references(references = None)

Fetch all unpaid Payment Requests for the references. 

        - Each reference can have multiple Payment Requests. 


Example: {("Sales Invoice", "SINV-00001"): {"PREQ-00001": 1000, "PREQ-00002": 2000}}

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| references | None | None | - |

**Returns**: (none)



### allocate_open_payment_requests_to_references(references = None, precision = None)

Allocate unpaid Payment Requests to the references. 

---
- Allocation based on below factors
    - Reference Allocated Amount
    - Reference Outstanding Amount (With Payment Terms or without Payment Terms)
    - Reference Payment Request's outstanding amount
---
- Allocation based on below scenarios
    - Reference's Allocated Amount == Payment Request's Outstanding Amount
        - Allocate the Payment Request to the reference
        - This PR will not be allocated further
    - Reference's Allocated Amount < Payment Request's Outstanding Amount
        - Allocate the Payment Request to the reference
        - Reduce the PR's outstanding amount by the allocated amount
        - This PR can be allocated further
    - Reference's Allocated Amount > Payment Request's Outstanding Amount
        - Allocate the Payment Request to the reference
        - Reduce Allocated Amount of the reference by the PR's outstanding amount
        - Create a new row for the remaining amount until the Allocated Amount is 0
            - Allocate PR if available
---
- Note:
    - Priority is given to the first Payment Request of respective references.
    - Single Reference can have multiple rows.
        - With Payment Terms or without Payment Terms
        - With Payment Request or without Payment Request

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| references | None | None | - |
| precision | None | None | - |

**Returns**: (none)



### update_accounting_dimensions(pe, doc)

Updates accounting dimensions in Payment Entry based on the accounting dimensions in the reference document

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| pe | None | - | - |
| doc | None | - | - |

**Returns**: (none)



### get_bank_cash_account(doc, bank_account)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |
| bank_account | None | - | - |

**Returns**: (none)



### set_party_type(dt)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| dt | None | - | - |

**Returns**: (none)



### set_party_account(dt, dn, doc, party_type)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| dt | None | - | - |
| dn | None | - | - |
| doc | None | - | - |
| party_type | None | - | - |

**Returns**: (none)



### set_party_account_currency(dt, party_account, doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| dt | None | - | - |
| party_account | None | - | - |
| doc | None | - | - |

**Returns**: (none)



### set_payment_type(dt, doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| dt | None | - | - |
| doc | None | - | - |

**Returns**: (none)



### set_grand_total_and_outstanding_amount(party_amount, dt, party_account_currency, doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| party_amount | None | - | - |
| dt | None | - | - |
| party_account_currency | None | - | - |
| doc | None | - | - |

**Returns**: (none)



### set_paid_amount_and_received_amount(dt, party_account_currency, bank, outstanding_amount, payment_type, bank_amount, doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| dt | None | - | - |
| party_account_currency | None | - | - |
| bank | None | - | - |
| outstanding_amount | None | - | - |
| payment_type | None | - | - |
| bank_amount | None | - | - |
| doc | None | - | - |

**Returns**: (none)



### apply_early_payment_discount(paid_amount, received_amount, doc, party_account_currency, reference_date)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| paid_amount | None | - | - |
| received_amount | None | - | - |
| doc | None | - | - |
| party_account_currency | None | - | - |
| reference_date | None | - | - |

**Returns**: (none)



### set_pending_discount_loss(pe, doc, discount_amount, base_total_discount_loss, party_account_currency)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| pe | None | - | - |
| doc | None | - | - |
| discount_amount | None | - | - |
| base_total_discount_loss | None | - | - |
| party_account_currency | None | - | - |

**Returns**: (none)



### split_early_payment_discount_loss(pe, doc, valid_discounts) → float

Split early payment discount into Income Loss & Tax Loss.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| pe | None | - | - |
| doc | None | - | - |
| valid_discounts | None | - | - |

**Returns**: `float`



### get_total_discount_percent(doc, valid_discounts) → float

Get total percentage and amount discount applied as a percentage.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |
| valid_discounts | None | - | - |

**Returns**: `float`



### add_income_discount_loss(pe, doc, total_discount_percent) → float

Add loss on income discount in base currency.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| pe | None | - | - |
| doc | None | - | - |
| total_discount_percent | None | - | - |

**Returns**: `float`



### add_tax_discount_loss(pe, doc, total_discount_percentage) → float

Add loss on tax discount in base currency.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| pe | None | - | - |
| doc | None | - | - |
| total_discount_percentage | None | - | - |

**Returns**: `float`



### get_reference_as_per_payment_terms(payment_schedule, dt, dn, doc, grand_total, outstanding_amount, party_account_currency)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| payment_schedule | None | - | - |
| dt | None | - | - |
| dn | None | - | - |
| doc | None | - | - |
| grand_total | None | - | - |
| outstanding_amount | None | - | - |
| party_account_currency | None | - | - |

**Returns**: (none)



### get_paid_amount(dt, dn, party_type, party, account, due_date)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| dt | None | - | - |
| dn | None | - | - |
| party_type | None | - | - |
| party | None | - | - |
| account | None | - | - |
| due_date | None | - | - |

**Returns**: (none)



### make_payment_order(source_name, target_doc = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| source_name | None | - | - |
| target_doc | None | None | - |

**Returns**: (none)



### add_regional_gl_entries(gl_entries, doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| gl_entries | None | - | - |
| doc | None | - | - |

**Returns**: (none)



### _on_previous_row_error(row_range)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| row_range | None | - | - |

**Returns**: (none)



### set_missing_values(source, target)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| source | None | - | - |
| target | None | - | - |

**Returns**: (none)



### _allocation_to_unset_pr_row(row, outstanding_amount, allocated_positive_outstanding, allocated_negative_outstanding)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| row | None | - | - |
| outstanding_amount | None | - | - |
| allocated_positive_outstanding | None | - | - |
| allocated_negative_outstanding | None | - | - |

**Returns**: (none)


