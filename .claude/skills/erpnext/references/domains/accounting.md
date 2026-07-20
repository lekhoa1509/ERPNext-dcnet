<!-- Source: erpnext_accounting skill -->

# ERPNext Accounts Module

## Overview

The ERPNext Accounts module is a comprehensive accounting system built on the Frappe framework. It provides full-featured financial management capabilities including chart of accounts, general ledger, accounts receivable/payable, payment processing, bank reconciliation, and financial reporting.

**Source:** ERPNext Codebase Analysis
**Files Analyzed:** 424
**Languages:** Python (94.6%), JavaScript (5.4%)
**Framework:** Frappe

## When to Use This Skill

Use this skill when you need to:

### Core Accounting Operations
- **Chart of Accounts Management**: Create, modify, or query the hierarchical account structure (Asset, Liability, Equity, Income, Expense)
- **General Ledger Operations**: Work with GL entries, account balances, and financial transactions
- **Journal Entries**: Create manual accounting entries, reversals, and adjustments

### Receivables & Payables
- **Accounts Receivable**: Track customer invoices, aging reports, and outstanding balances
- **Accounts Payable**: Manage supplier invoices, payment schedules, and vendor balances
- **Payment Reconciliation**: Match payments to invoices, handle partial payments

### Banking Operations
- **Bank Account Management**: Configure bank accounts, link to GL accounts
- **Bank Reconciliation**: Clear transactions, match bank statements
- **Bank Transaction Processing**: Import and categorize bank transactions
- **Auto-matching**: Leverage automatic party matching by IBAN/account number

### Financial Reporting
- **Balance Sheet**: Generate balance sheet reports with asset/liability/equity breakdown
- **Profit & Loss**: Income statement generation and analysis
- **Trial Balance**: Account balance verification reports
- **Accounts Receivable/Payable Summary**: Aging analysis and party-wise summaries

### Advanced Features
- **Multi-currency Accounting**: Handle transactions in multiple currencies
- **Accounting Dimensions**: Custom dimension filtering (cost center, project, etc.)
- **Payment Ledger**: Track payment movements and reconciliation status
- **Fiscal Year Management**: Handle accounting periods and year-end closings

## Key Concepts

### Account Hierarchy (NestedSet Pattern)

ERPNext uses a tree structure for the Chart of Accounts. The `Account` DocType inherits from `NestedSet` for efficient hierarchical queries:

```python
class Account(NestedSet):
    def validate(self):
        self.validate_parent_child_account_type()
        self.set_root_and_report_type()
        self.validate_root_details()
```

**Account Types:**
- **Asset**: Bank, Cash, Stock, Fixed Asset, Receivable
- **Liability**: Payable, Stock Liabilities
- **Equity**: Capital, Reserves
- **Income**: Direct Income, Indirect Income
- **Expense**: Direct Expense, Indirect Expense

### Payment Ledger Design

The Payment Ledger (`payment_ledger_entry`) tracks all payment-related transactions:

**Key Fields:**
- `voucher_type`, `voucher_no` - Source document reference
- `against_voucher_type`, `against_voucher_no` - Linked invoice/document
- `amount`, `amount_in_account_currency` - Transaction amounts
- `account`, `party_type`, `party` - Account and party details

### Document Workflow

ERPNext documents follow a standard workflow with `docstatus`:
- **0 (Draft)**: Can be modified freely
- **1 (Submitted)**: Creates GL entries, locked for editing
- **2 (Cancelled)**: Reversal entries created, document archived

## Quick Reference

### Creating and Managing Accounts

```python
# Create a new account
account = frappe.get_doc({
    'doctype': 'Account',
    'account_name': 'Operating Expenses',
    'parent_account': 'Expenses - ABC',
    'company': 'ABC Company',
    'account_type': '',  # Leave blank for group accounts
    'is_group': 1,
    'root_type': 'Expense'
})
account.insert()

# Fetch account with children
children = frappe.get_all('Account',
    filters={'parent_account': 'Expenses - ABC'},
    fields=['name', 'account_name', 'balance'])
```

### Payment Entry with Invoice References

```python
# Create payment entry linked to invoices
pe = frappe.get_doc({
    'doctype': 'Payment Entry',
    'payment_type': 'Receive',
    'party_type': 'Customer',
    'party': 'Customer ABC',
    'paid_amount': 1000,
    'received_amount': 1000,
    'paid_from': 'Debtors - ABC',
    'paid_to': 'Cash - ABC'
})

# Link to sales invoice
pe.append('references', {
    'reference_doctype': 'Sales Invoice',
    'reference_name': 'SINV-00001',
    'allocated_amount': 1000
})
pe.save()
pe.submit()
```

### Payment Reconciliation

```python
# Reconcile payments with invoices
pr = frappe.get_doc('Payment Reconciliation')
pr.company = 'ABC Company'
pr.party_type = 'Customer'
pr.party = 'Customer ABC'
pr.receivable_payable_account = 'Debtors - ABC'

# Get unreconciled entries
pr.get_unreconciled_entries()

# Filter and allocate
invoices = [inv.as_dict() for inv in pr.invoices
            if inv.invoice_number == 'SINV-00001']
payments = [pay.as_dict() for pay in pr.payments
            if pay.reference_name == 'PE-00001']

pr.allocate_entries(frappe._dict({
    'invoices': invoices,
    'payments': payments
}))
pr.reconcile()
```

### Unreconcile Payments (Reverse Reconciliation)

```python
# Unreconcile a payment from invoices
unreconcile = frappe.get_doc({
    'doctype': 'Unreconcile Payment',
    'company': 'ABC Company',
    'voucher_type': 'Payment Entry',
    'voucher_no': 'PE-00001'
})

# Load current allocations
unreconcile.add_references()

# Selectively remove allocations
for allocation in unreconcile.allocations:
    if allocation.reference_name != 'SINV-00001':
        unreconcile.remove(allocation)

unreconcile.save()
unreconcile.submit()  # Executes unreconciliation
```

### Journal Entry for Advance Payment

```python
# Create journal entry for supplier advance
je = frappe.get_doc({
    'doctype': 'Journal Entry',
    'company': 'ABC Company',
    'voucher_type': 'Journal Entry',
    'posting_date': today(),
    'multi_currency': True,
    'accounts': [
        {
            'account': 'Creditors - ABC',
            'party_type': 'Supplier',
            'party': 'Supplier XYZ',
            'debit_in_account_currency': 100,
            'is_advance': 'Yes',
            'reference_type': 'Purchase Order',
            'reference_name': 'PO-00001'
        },
        {
            'account': 'Cash - ABC',
            'credit_in_account_currency': 100
        }
    ]
})
je.save()
je.submit()
```

### Bank Transaction Auto-Matching

```python
# Auto-match party by IBAN/Account number
from erpnext.accounts.doctype.bank_transaction.auto_match_party import AutoMatchParty

matcher = AutoMatchParty()
matcher.bank_party_iban = 'DE89370400440532013000'
matcher.bank_party_account_number = '0532013000'
matcher.description = 'Payment from ABC Corp'

result = matcher.match()  # Returns (party_type, party) or None
```

### Accounts Receivable Report

```python
from erpnext.accounts.report.accounts_receivable.accounts_receivable import (
    ReceivablePayableReport, execute
)

# Generate accounts receivable report
filters = frappe._dict({
    'company': 'ABC Company',
    'report_date': today(),
    'ageing_based_on': 'Due Date',
    'range1': 30, 'range2': 60, 'range3': 90, 'range4': 120,
    'customer': 'Customer ABC'  # Optional filter
})

columns, data = execute(filters)
```

### Balance Sheet Report

```python
from erpnext.accounts.report.balance_sheet.balance_sheet import execute

filters = frappe._dict({
    'company': 'ABC Company',
    'fiscal_year': '2024',
    'periodicity': 'Monthly'
})

columns, data, report_summary, chart = execute(filters)
```

### Accounting Dimensions

```python
# Create custom accounting dimension
dimension = frappe.get_doc({
    'doctype': 'Accounting Dimension',
    'document_type': 'Project',
    'label': 'Project',
    'fieldname': 'project',
    'mandatory_for_bs': 0,
    'mandatory_for_pl': 0
})
dimension.insert()

# Filter by dimension in GL queries
gl_entries = frappe.get_all('GL Entry',
    filters={
        'account': 'Sales - ABC',
        'project': 'PROJ-001'
    },
    fields=['posting_date', 'debit', 'credit', 'voucher_no']
)
```

### Bank Clearance

```python
# Get payment entries for bank clearance
from erpnext.accounts.doctype.bank_clearance.bank_clearance import (
    get_payment_entries_for_bank_clearance
)

entries = get_payment_entries_for_bank_clearance(
    from_date='2024-01-01',
    to_date='2024-01-31',
    account='Bank Account - ABC',
    bank_account='ABC Bank',
    include_reconciled_entries=False,
    include_pos_transactions=True
)
```

## Design Patterns Detected

The codebase extensively uses these design patterns (89 high-confidence instances):

### Factory Pattern (59 instances)
Used for document creation and report generation:
```python
# Factory for document creation
frappe.get_doc({'doctype': 'Payment Entry', ...})

# Factory in reports
def execute(filters):
    return get_columns(), get_data(filters)
```

### Observer Pattern (15 instances)
Document lifecycle hooks for cascading updates:
```python
class Account(NestedSet):
    def on_update(self):
        # Notify child accounts, update caches
        pass

    def after_rename(self, old_name, new_name, merge):
        # Update references in other documents
        pass
```

### Builder Pattern (7 instances)
Complex query and report construction:
```python
class ReceivablePayableReport:
    def __init__(self, filters):
        self.filters = filters
        self.data = []

    def run(self, args):
        self.get_data()
        self.build_data()
        return self.get_columns(), self.data
```

### Command Pattern (5 instances)
Encapsulated operations for reconciliation and unreconciliation:
```python
# Reconciliation as a command
pr.reconcile()

# Unreconciliation as a reversible command
unreconcile.save().submit()
```

### Strategy Pattern (2 instances)
Different matching strategies for auto-party detection:
```python
class AutoMatchbyAccountIBAN:
    def match(self): ...

class AutoMatchbyPartyNameDescription:
    def match(self): ...
```

## Core DocTypes Reference

### Account Management
| DocType | Description |
|---------|-------------|
| `Account` | Chart of accounts (NestedSet tree structure) |
| `Account Category` | Account classification system |
| `Accounting Dimension` | Custom dimension configuration |
| `Accounting Dimension Filter` | Dimension filtering rules |
| `Accounting Period` | Period closing management |
| `Accounts Settings` | Module-wide settings |

### Transaction Documents
| DocType | Description |
|---------|-------------|
| `Payment Entry` | Receive/Pay transactions |
| `Journal Entry` | Manual GL entries |
| `Payment Reconciliation` | Match payments to invoices |
| `Unreconcile Payment` | Reverse reconciliation |

### Banking
| DocType | Description |
|---------|-------------|
| `Bank` | Bank master |
| `Bank Account` | Company bank accounts |
| `Bank Clearance` | Bank statement reconciliation |
| `Bank Transaction` | Imported bank transactions |

### Reporting
| Report | Description |
|--------|-------------|
| `Account Balance` | Account-wise balances |
| `Accounts Receivable` | Customer aging report |
| `Accounts Payable` | Supplier aging report |
| `Balance Sheet` | Financial position |
| `Profit and Loss Statement` | Income statement |

## API Reference Highlights

### Account Class (`doctype/account/account.py`)

```python
class Account(NestedSet):
    def validate(self)
    def validate_parent(self)              # Validate parent account
    def set_root_and_report_type(self)     # Set account classification
    def validate_group_or_ledger(self)     # Enforce group/ledger rules
    def on_update(self)                    # Post-save hooks
```

### ReceivablePayableReport (`report/accounts_receivable/`)

```python
class ReceivablePayableReport:
    def run(self, args)
    def get_data(self)                     # Fetch payment ledger entries
    def build_voucher_dict(self, ple)      # Structure voucher data
    def get_invoices(self, ple)            # Get related invoices
```

### AutoMatchParty (`doctype/bank_transaction/auto_match_party.py`)

```python
class AutoMatchParty:
    def match(self) -> tuple | None        # Returns (party_type, party)

class AutoMatchbyAccountIBAN:
    def match_account_in_party(self)       # Match by IBAN/account

class AutoMatchbyPartyNameDescription:
    def match(self)                        # Match by name/description
```

## Working with This Skill

### For Beginners

1. **Start with Account Structure**: Understand the Chart of Accounts hierarchy before diving into transactions
2. **Use Test Fixtures**: The `AccountsTestMixin` class provides helpers for test setup:
   ```python
   class AccountsTestMixin:
       def create_customer(self, customer_name, currency=None)
       def create_supplier(self, supplier_name, currency=None)
       def create_company(self, company_name, abbr)
   ```
3. **Follow Document Workflow**: Draft -> Submit -> Cancel follows the standard pattern

### For Intermediate Users

1. **Leverage Reconciliation Tools**: Use `Payment Reconciliation` for bulk matching
2. **Custom Dimensions**: Add project/department tracking via `Accounting Dimension`
3. **Report Customization**: Extend `ReceivablePayableReport` for custom reports

### For Advanced Users

1. **Payment Ledger Integration**: Direct queries against `Payment Ledger Entry` for performance
2. **Custom Matching Logic**: Extend `AutoMatchParty` for custom matching strategies
3. **Period Closing**: Use `Account Closing Balance` for efficient period-end processing

## Reference Documentation

### API Reference (`references/api_reference/`)
Complete Python/JavaScript API documentation extracted from source code:
- **31 API reference files** covering all major modules
- Method signatures, parameters, return types
- Inheritance relationships

### Design Patterns (`references/patterns/`)
Detailed pattern analysis with code locations:
- Factory pattern implementations
- Observer hooks and callbacks
- Builder pattern for complex objects

### Test Examples (`references/test_examples/`)
Real-world usage patterns from test suite:
- Payment reconciliation workflows
- Unreconciliation scenarios
- Multi-invoice payment handling
- Advance payment tracking

### Configuration (`references/config_patterns/`)
Configuration file analysis:
- 100 configuration files analyzed
- 1996 total settings identified
- JSON schema patterns

### Project Documentation (`references/documentation/`)
20 markdown documentation files:
- Payment Ledger design documentation
- Account DocType specifications
- Module-specific READMEs

## Exception Classes

The module defines specific exception types for validation:

```python
from erpnext.accounts.doctype.account.account import (
    RootNotEditable,           # Cannot edit root accounts
    BalanceMismatchError,      # Balance validation failure
    InvalidAccountMergeError   # Invalid merge operation
)

from erpnext.accounts.doctype.accounting_period.accounting_period import (
    OverlapError,              # Period date overlap
    ClosedAccountingPeriod     # Transaction in closed period
)
```

## Common Validation Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `RootNotEditable` | Attempting to modify root account | Create child accounts instead |
| `BalanceMismatchError` | Debit/credit imbalance | Verify journal entry totals |
| `OverlapError` | Accounting periods overlap | Adjust period dates |
| `ClosedAccountingPeriod` | Transaction in closed period | Reopen period or adjust date |

## Best Practices

### Account Management
- Always use hierarchical structure (groups contain ledgers)
- Set `root_type` correctly (Asset, Liability, Equity, Income, Expense)
- Use `account_type` for special accounts (Bank, Cash, Receivable, Payable)

### Payment Processing
- Link payments to invoices using `references` table
- Use `allocated_amount` for partial payments
- Leverage auto-reconciliation for high-volume processing

### Reporting
- Use filters to limit data scope
- Implement pagination for large datasets
- Cache frequently-accessed reports

### Multi-Currency
- Set `multi_currency: True` on journal entries
- Use `*_in_account_currency` fields for local amounts
- Track exchange rates at transaction time

---

**Generated by Skill Seekers** | ERPNext Accounts Module Analysis

*Source: Codebase analysis with C3.x features (API Reference, Design Patterns, Test Examples, Configuration, Documentation)*
