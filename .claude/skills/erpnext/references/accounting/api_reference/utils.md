# API Reference: utils.py

**Language**: Python

**Source**: `utils.py`

---

## Classes

### FiscalYearError

**Inherits from**: frappe.ValidationError



### PaymentEntryUnlinkError

**Inherits from**: frappe.ValidationError



### QueryPaymentLedger

Helper Class for Querying Payment Ledger Entry

**Inherits from**: (none)

#### Methods

##### __init__(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### reset(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### query_for_outstanding(self)

Database query to fetch voucher amount and voucher outstanding using Common Table Expression

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_voucher_outstandings(self, vouchers = None, common_filter = None, posting_date = None, min_outstanding = None, max_outstanding = None, get_payments = False, get_invoices = False, accounting_dimensions = None, limit = None, voucher_no = None)

Fetch voucher amount and outstanding amount from Payment Ledger using Database CTE

vouchers - dict of vouchers to get
common_filter - array of criterions
min_outstanding - filter on minimum total outstanding amount
max_outstanding - filter on maximum total  outstanding amount
get_invoices - only fetch vouchers(ledger entries with +ve outstanding)
get_payments - only fetch payments(ledger entries with -ve outstanding)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| vouchers | None | None | - |
| common_filter | None | None | - |
| posting_date | None | None | - |
| min_outstanding | None | None | - |
| max_outstanding | None | None | - |
| get_payments | None | False | - |
| get_invoices | None | False | - |
| accounting_dimensions | None | None | - |
| limit | None | None | - |
| voucher_no | None | None | - |




## Functions

### get_fiscal_year(date = None, fiscal_year = None, label = 'Date', verbose = 1, company = None, as_dict = False, boolean = None, raise_on_missing = True, truncate = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| date | None | None | - |
| fiscal_year | None | None | - |
| label | None | 'Date' | - |
| verbose | None | 1 | - |
| company | None | None | - |
| as_dict | None | False | - |
| boolean | None | None | - |
| raise_on_missing | None | True | - |
| truncate | None | False | - |

**Returns**: (none)



### get_fiscal_years(transaction_date = None, fiscal_year = None, label = 'Date', verbose = 1, company = None, as_dict = False, boolean = None, raise_on_missing = True)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| transaction_date | None | None | - |
| fiscal_year | None | None | - |
| label | None | 'Date' | - |
| verbose | None | 1 | - |
| company | None | None | - |
| as_dict | None | False | - |
| boolean | None | None | - |
| raise_on_missing | None | True | - |

**Returns**: (none)



### _get_fiscal_years(company = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| company | None | None | - |

**Returns**: (none)



### get_fiscal_year_filter_field(company = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| company | None | None | - |

**Returns**: (none)



### validate_fiscal_year(date, fiscal_year, company, label = 'Date', doc = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| date | None | - | - |
| fiscal_year | None | - | - |
| company | None | - | - |
| label | None | 'Date' | - |
| doc | None | None | - |

**Returns**: (none)



### get_balance_on(account = None, date = None, party_type = None, party = None, company = None, in_account_currency = True, cost_center = None, ignore_account_permission = False, account_type = None, start_date = None, finance_book = None, include_default_fb_balances = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| account | None | None | - |
| date | None | None | - |
| party_type | None | None | - |
| party | None | None | - |
| company | None | None | - |
| in_account_currency | None | True | - |
| cost_center | None | None | - |
| ignore_account_permission | None | False | - |
| account_type | None | None | - |
| start_date | None | None | - |
| finance_book | None | None | - |
| include_default_fb_balances | None | False | - |

**Returns**: (none)



### get_count_on(account, fieldname, date)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| account | None | - | - |
| fieldname | None | - | - |
| date | None | - | - |

**Returns**: (none)



### add_ac(args = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| args | None | None | - |

**Returns**: (none)



### add_cc(args = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| args | None | None | - |

**Returns**: (none)



### _build_dimensions_dict_for_exc_gain_loss(entry: dict | object = None, active_dimensions: list | None = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| entry | dict | object | None | - |
| active_dimensions | list | None | None | - |

**Returns**: (none)



### reconcile_against_document(args, skip_ref_details_update_for_pe = False, active_dimensions = None)

Cancel PE or JV, Update against document, split if required and resubmit

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| args | None | - | - |
| skip_ref_details_update_for_pe | None | False | - |
| active_dimensions | None | None | - |

**Returns**: (none)



### check_if_advance_entry_modified(args)

check if there is already a voucher reference
check if amount is same
check if jv is submitted

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| args | None | - | - |

**Returns**: (none)



### validate_allocated_amount(args)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| args | None | - | - |

**Returns**: (none)



### update_reference_in_journal_entry(d, journal_entry, do_not_save = False)

Updates against document, if partial amount splits into rows

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| d | None | - | - |
| journal_entry | None | - | - |
| do_not_save | None | False | - |

**Returns**: (none)



### update_reference_in_payment_entry(d, payment_entry, do_not_save = False, skip_ref_details_update_for_pe = False, dimensions_dict = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| d | None | - | - |
| payment_entry | None | - | - |
| do_not_save | None | False | - |
| skip_ref_details_update_for_pe | None | False | - |
| dimensions_dict | None | None | - |

**Returns**: (none)



### get_reconciliation_effect_date(against_voucher_type, against_voucher, company, posting_date)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| against_voucher_type | None | - | - |
| against_voucher | None | - | - |
| company | None | - | - |
| posting_date | None | - | - |

**Returns**: (none)



### cancel_exchange_gain_loss_journal(parent_doc: dict | object, referenced_dt: str | None = None, referenced_dn: str | None = None) → None

Cancel Exchange Gain/Loss for Sales/Purchase Invoice, if they have any.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| parent_doc | dict | object | - | - |
| referenced_dt | str | None | None | - |
| referenced_dn | str | None | None | - |

**Returns**: `None`



### delete_exchange_gain_loss_journal(parent_doc: dict | object, referenced_dt: str | None = None, referenced_dn: str | None = None) → None

Delete Exchange Gain/Loss for Sales/Purchase Invoice, if they have any.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| parent_doc | dict | object | - | - |
| referenced_dt | str | None | None | - |
| referenced_dn | str | None | None | - |

**Returns**: `None`



### get_linked_exchange_gain_loss_journal(referenced_dt: str, referenced_dn: str, je_docstatus: int) → list

Get all the linked exchange gain/loss journal entries for a given document.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| referenced_dt | str | - | - |
| referenced_dn | str | - | - |
| je_docstatus | int | - | - |

**Returns**: `list`



### cancel_common_party_journal(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: (none)



### update_accounting_ledgers_after_reference_removal(ref_type: str | None = None, ref_no: str | None = None, payment_name: str | None = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| ref_type | str | None | None | - |
| ref_no | str | None | None | - |
| payment_name | str | None | None | - |

**Returns**: (none)



### remove_ref_from_advance_section(ref_doc: object = None, payment_name: str | None = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| ref_doc | object | None | - |
| payment_name | str | None | None | - |

**Returns**: (none)



### unlink_ref_doc_from_payment_entries(ref_doc: object = None, payment_name: str | None = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| ref_doc | object | None | - |
| payment_name | str | None | None | - |

**Returns**: (none)



### remove_ref_doc_link_from_jv(ref_type: str | None = None, ref_no: str | None = None, payment_name: str | None = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| ref_type | str | None | None | - |
| ref_no | str | None | None | - |
| payment_name | str | None | None | - |

**Returns**: (none)



### convert_to_list(result)

Convert tuple to list

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| result | None | - | - |

**Returns**: (none)



### remove_ref_doc_link_from_pe(ref_type: str | None = None, ref_no: str | None = None, payment_name: str | None = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| ref_type | str | None | None | - |
| ref_no | str | None | None | - |
| payment_name | str | None | None | - |

**Returns**: (none)



### get_company_default(company, fieldname, ignore_validation = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| company | None | - | - |
| fieldname | None | - | - |
| ignore_validation | None | False | - |

**Returns**: (none)



### fix_total_debit_credit()

**Returns**: (none)



### get_currency_precision()

**Returns**: (none)



### get_fraction_units(currency: str) → int

Returns the number of fraction units for a currency.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| currency | str | - | - |

**Returns**: `int`



### get_zero_cutoff(currency: str) → float

Returns the zero cutoff for a currency.

For example, if the Fraction Units for a currency are set to 100, then the zero cutoff is 0.005.
We don't want to display values less than the zero cutoff.
This value was chosen for compatibility with the previous hard-coded value of 0.005.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| currency | str | - | - |

**Returns**: `float`



### get_held_invoices(party_type, party)

Returns a list of names Purchase Invoices for the given party that are on hold

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| party_type | None | - | - |
| party | None | - | - |

**Returns**: (none)



### get_outstanding_invoices(party_type, party, account, common_filter = None, posting_date = None, min_outstanding = None, max_outstanding = None, accounting_dimensions = None, vouchers = None, limit = None, voucher_no = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| party_type | None | - | - |
| party | None | - | - |
| account | None | - | - |
| common_filter | None | None | - |
| posting_date | None | None | - |
| min_outstanding | None | None | - |
| max_outstanding | None | None | - |
| accounting_dimensions | None | None | - |
| vouchers | None | None | - |
| limit | None | None | - |
| voucher_no | None | None | - |

**Returns**: (none)



### get_account_name(account_type = None, root_type = None, is_group = None, account_currency = None, company = None)

return account based on matching conditions

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| account_type | None | None | - |
| root_type | None | None | - |
| is_group | None | None | - |
| account_currency | None | None | - |
| company | None | None | - |

**Returns**: (none)



### get_companies()

get a list of companies based on permission

**Returns**: (none)



### get_children(doctype, parent, company, is_root = False, include_disabled = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| parent | None | - | - |
| company | None | - | - |
| is_root | None | False | - |
| include_disabled | None | False | - |

**Returns**: (none)



### get_account_balances(accounts, company, finance_book = None, include_default_fb_balances = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| accounts | None | - | - |
| company | None | - | - |
| finance_book | None | None | - |
| include_default_fb_balances | None | False | - |

**Returns**: (none)



### create_payment_gateway_account(gateway, payment_channel = 'Email', company = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| gateway | None | - | - |
| payment_channel | None | 'Email' | - |
| company | None | None | - |

**Returns**: (none)



### update_cost_center(docname, cost_center_name, cost_center_number, company, merge)

Renames the document by adding the number as a prefix to the current name and updates
all transaction where it was present.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| docname | None | - | - |
| cost_center_name | None | - | - |
| cost_center_number | None | - | - |
| company | None | - | - |
| merge | None | - | - |

**Returns**: (none)



### validate_field_number(doctype_name, docname, number_value, company, field_name)

Validate if the number entered isn't already assigned to some other document.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype_name | None | - | - |
| docname | None | - | - |
| number_value | None | - | - |
| company | None | - | - |
| field_name | None | - | - |

**Returns**: (none)



### get_autoname_with_number(number_value, doc_title, company)

append title with prefix as number and suffix as company's abbreviation separated by '-'

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| number_value | None | - | - |
| doc_title | None | - | - |
| company | None | - | - |

**Returns**: (none)



### parse_naming_series_variable(doc, variable)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |
| variable | None | - | - |

**Returns**: (none)



### get_coa(doctype, parent, is_root = None, chart = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| parent | None | - | - |
| is_root | None | None | - |
| chart | None | None | - |

**Returns**: (none)



### update_gl_entries_after(posting_date, posting_time, for_warehouses = None, for_items = None, warehouse_account = None, company = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| posting_date | None | - | - |
| posting_time | None | - | - |
| for_warehouses | None | None | - |
| for_items | None | None | - |
| warehouse_account | None | None | - |
| company | None | None | - |

**Returns**: (none)



### repost_gle_for_stock_vouchers(stock_vouchers: list[tuple[str, str]], posting_date: str, company: str | None = None, warehouse_account = None, repost_doc: Optional['RepostItemValuation'] = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| stock_vouchers | list[tuple[str, str]] | - | - |
| posting_date | str | - | - |
| company | str | None | None | - |
| warehouse_account | None | None | - |
| repost_doc | Optional['RepostItemValuation'] | None | - |

**Returns**: (none)



### _delete_pl_entries(voucher_type, voucher_no)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| voucher_type | None | - | - |
| voucher_no | None | - | - |

**Returns**: (none)



### _delete_adv_pl_entries(voucher_type, voucher_no)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| voucher_type | None | - | - |
| voucher_no | None | - | - |

**Returns**: (none)



### _delete_gl_entries(voucher_type, voucher_no)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| voucher_type | None | - | - |
| voucher_no | None | - | - |

**Returns**: (none)



### _delete_accounting_ledger_entries(voucher_type, voucher_no)

Remove entries from both General and Payment Ledger for specified Voucher

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| voucher_type | None | - | - |
| voucher_no | None | - | - |

**Returns**: (none)



### sort_stock_vouchers_by_posting_date(stock_vouchers: list[tuple[str, str]], company = None) → list[tuple[str, str]]

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| stock_vouchers | list[tuple[str, str]] | - | - |
| company | None | None | - |

**Returns**: `list[tuple[str, str]]`



### get_future_stock_vouchers(posting_date, posting_time, for_warehouses = None, for_items = None, company = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| posting_date | None | - | - |
| posting_time | None | - | - |
| for_warehouses | None | None | - |
| for_items | None | None | - |
| company | None | None | - |

**Returns**: (none)



### get_voucherwise_gl_entries(future_stock_vouchers, posting_date)

Get voucherwise list of GL entries.

Only fetches GLE fields required for comparing with new GLE.
Check compare_existing_and_expected_gle function below.

returns:
        Dict[Tuple[voucher_type, voucher_no], List[GL Entries]]

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| future_stock_vouchers | None | - | - |
| posting_date | None | - | - |

**Returns**: (none)



### compare_existing_and_expected_gle(existing_gle, expected_gle, precision)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| existing_gle | None | - | - |
| expected_gle | None | - | - |
| precision | None | - | - |

**Returns**: (none)



### get_stock_accounts(company, voucher_type = None, voucher_no = None, accounts = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| company | None | - | - |
| voucher_type | None | None | - |
| voucher_no | None | None | - |
| accounts | None | None | - |

**Returns**: (none)



### get_stock_and_account_balance(account = None, posting_date = None, company = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| account | None | None | - |
| posting_date | None | None | - |
| company | None | None | - |

**Returns**: (none)



### get_journal_entry(account, stock_adjustment_account, amount)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| account | None | - | - |
| stock_adjustment_account | None | - | - |
| amount | None | - | - |

**Returns**: (none)



### check_and_delete_linked_reports(report)

Check if reports are referenced in Desktop Icon

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| report | None | - | - |

**Returns**: (none)



### create_err_and_its_journals(company: dict) → None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| company | dict | - | - |

**Returns**: `None`



### _auto_create_exchange_rate_revaluation_for(frequency: str) → None

Internal helper to avoid code duplication and typos.
Fetches companies by frequency and triggers ERR.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| frequency | str | - | - |

**Returns**: `None`



### auto_create_exchange_rate_revaluation_daily() → None

Executed by background job

**Returns**: `None`



### auto_create_exchange_rate_revaluation_weekly() → None

Executed by background job

**Returns**: `None`



### auto_create_exchange_rate_revaluation_monthly() → None

Executed by background job

**Returns**: `None`



### get_payment_ledger_entries(gl_entries, cancel = 0)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| gl_entries | None | - | - |
| cancel | None | 0 | - |

**Returns**: (none)



### get_advance_ledger_entry(gle, against_voucher_type, against_voucher_no, amount, cancel, base_amount = None, exchange_rate = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| gle | None | - | - |
| against_voucher_type | None | - | - |
| against_voucher_no | None | - | - |
| amount | None | - | - |
| cancel | None | - | - |
| base_amount | None | None | - |
| exchange_rate | None | None | - |

**Returns**: (none)



### create_payment_ledger_entry(gl_entries, cancel = 0, adv_adj = 0, update_outstanding = 'Yes', from_repost = 0, partial_cancel = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| gl_entries | None | - | - |
| cancel | None | 0 | - |
| adv_adj | None | 0 | - |
| update_outstanding | None | 'Yes' | - |
| from_repost | None | 0 | - |
| partial_cancel | None | False | - |

**Returns**: (none)



### update_voucher_outstanding(voucher_type, voucher_no, account, party_type, party)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| voucher_type | None | - | - |
| voucher_no | None | - | - |
| account | None | - | - |
| party_type | None | - | - |
| party | None | - | - |

**Returns**: (none)



### delink_original_entry(pl_entry, partial_cancel = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| pl_entry | None | - | - |
| partial_cancel | None | False | - |

**Returns**: (none)



### create_gain_loss_journal(company, posting_date, party_type, party, party_account, gain_loss_account, exc_gain_loss, dr_or_cr, reverse_dr_or_cr, ref1_dt, ref1_dn, ref1_detail_no, ref2_dt, ref2_dn, ref2_detail_no, cost_center, dimensions) → str

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| company | None | - | - |
| posting_date | None | - | - |
| party_type | None | - | - |
| party | None | - | - |
| party_account | None | - | - |
| gain_loss_account | None | - | - |
| exc_gain_loss | None | - | - |
| dr_or_cr | None | - | - |
| reverse_dr_or_cr | None | - | - |
| ref1_dt | None | - | - |
| ref1_dn | None | - | - |
| ref1_detail_no | None | - | - |
| ref2_dt | None | - | - |
| ref2_dn | None | - | - |
| ref2_detail_no | None | - | - |
| cost_center | None | - | - |
| dimensions | None | - | - |

**Returns**: `str`



### get_party_types_from_account_type(account_type)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| account_type | None | - | - |

**Returns**: (none)



### get_advance_payment_doctypes(payment_type = None)

Get list of advance payment doctypes based on type.
:param type: Optional, can be "receivable" or "payable". If not provided, returns both.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| payment_type | None | None | - |

**Returns**: (none)



### run_ledger_health_checks()

**Returns**: (none)



### sync_auto_reconcile_config(auto_reconciliation_job_trigger: int = 15)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| auto_reconciliation_job_trigger | int | 15 | - |

**Returns**: (none)



### get_link_fields_grouped_by_option(doctype)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |

**Returns**: (none)



### build_qb_match_conditions(doctype, user = None) → list

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| user | None | None | - |

**Returns**: `list`



### is_immutable_ledger_enabled()

**Returns**: (none)



### get_account_type(account)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| account | None | - | - |

**Returns**: (none)


