<!-- Source: erpnext_setup skill -->

# ERPNext Setup Module

## Description

The ERPNext Setup module is the **foundational configuration layer** of ERPNext, containing all master data DocTypes and system-wide settings required before any business transactions can occur. This module handles company setup, organizational structure (departments, branches, employees), item categorization, global defaults, and the setup wizard operations.

**Source Path:** `erpnext/setup`
**Files Analyzed:** 73
**Languages:** Python (98.6%), JavaScript (1.4%)
**Analysis Depth:** Full codebase analysis with API extraction

## When to Use This Skill

Use this skill when you need to:

### Company & Organization Setup
- Create or configure a **Company** (legal entity, chart of accounts, default warehouses)
- Set up **Departments** with hierarchical structure (NestedSet)
- Configure **Branches** for multi-location organizations
- Manage **Employee** records and organizational hierarchy

### Master Data Configuration
- Configure **Item Groups** (product categorization hierarchy)
- Set up **Customer Groups** for customer segmentation
- Define **Sales Persons** with territory/commission structure
- Manage **Brands** for product branding

### System Configuration
- Configure **Global Defaults** (default company, currency, date format)
- Set up **Holiday Lists** for leave management
- Configure **Currency Exchange** rates
- Define **Authorization Rules** for transaction limits

### Setup Wizard & Installation
- Understand the **setup wizard** flow for new ERPNext installations
- Create **fixtures** (default data, UOM, territories)
- Configure **default settings** (selling/buying defaults)

### HR Foundation
- Manage **Employee** records (linked to User, Department, Designation)
- Set up **Designations** (job titles)
- Configure **Employee Groups** for bulk operations

## Key Concepts

### NestedSet Pattern

Many DocTypes in the Setup module use the **NestedSet** pattern for hierarchical data (tree structures). This includes:

| DocType | Purpose |
|---------|---------|
| Company | Parent-child company relationships |
| Department | Organizational department hierarchy |
| Employee | Reports-to hierarchy |
| Item Group | Product categorization tree |
| Customer Group | Customer segmentation tree |
| Sales Person | Sales territory hierarchy |

NestedSet stores `lft` (left) and `rgt` (right) values for efficient tree traversal:

```python
# Get all children of an Item Group
children = get_child_item_groups("Electronics")

# Get parent hierarchy
ancestors = get_ancestors_of("Item Group", "Mobile Phones")
```

### Company as Multi-Tenancy Foundation

The **Company** DocType is central to ERPNext multi-tenancy:
- All transactions are linked to a Company
- Chart of Accounts is company-specific
- Default warehouses, cost centers are per-company
- Currency settings are company-level

### Employee-User Linkage

Employees can be linked to Frappe Users for:
- **User Permissions**: Automatic data access restrictions
- **Role Assignment**: Employee-based role profiles
- **Leave/Attendance**: Self-service features

## Quick Reference - Core DocTypes

### Company

```python
# Create a new Company
company = frappe.get_doc({
    "doctype": "Company",
    "company_name": "ACME Corp",
    "abbr": "ACME",
    "default_currency": "USD",
    "country": "United States",
    "chart_of_accounts": "Standard"
})
company.insert()

# Company auto-creates:
# - Default Warehouses (Stores, Finished Goods, Work In Progress)
# - Default Cost Center
# - Default Accounts (from Chart of Accounts)
# - Default Departments
```

### Employee

```python
# Create Employee linked to User
employee = frappe.get_doc({
    "doctype": "Employee",
    "first_name": "John",
    "last_name": "Doe",
    "gender": "Male",
    "date_of_birth": "1990-01-15",
    "date_of_joining": "2024-01-01",
    "company": "ACME Corp",
    "department": "Engineering - ACME",
    "designation": "Software Engineer",
    "user_id": "john@example.com"  # Links to Frappe User
})
employee.insert()

# Check if employee has holiday
from erpnext.setup.doctype.employee.employee import is_holiday
is_today_holiday = is_holiday(employee.name, date=today())
```

### Item Group

```python
# Create hierarchical Item Groups
parent_group = frappe.get_doc({
    "doctype": "Item Group",
    "item_group_name": "Electronics",
    "parent_item_group": "All Item Groups",
    "is_group": 1  # Can have children
})
parent_group.insert()

child_group = frappe.get_doc({
    "doctype": "Item Group",
    "item_group_name": "Mobile Phones",
    "parent_item_group": "Electronics",
    "is_group": 0  # Leaf node
})
child_group.insert()

# Get all child groups (for filtering items)
from erpnext.setup.doctype.item_group.item_group import get_child_item_groups
mobile_groups = get_child_item_groups("Mobile Phones")
```

### Department

```python
# Create Department with hierarchy
dept = frappe.get_doc({
    "doctype": "Department",
    "department_name": "Engineering",
    "company": "ACME Corp",
    "parent_department": "All Departments - ACME"
})
dept.insert()
# Auto-named as "Engineering - ACME" (with company abbr)
```

### Holiday List

```python
# Create Holiday List
holiday_list = frappe.get_doc({
    "doctype": "Holiday List",
    "holiday_list_name": "US Holidays 2024",
    "from_date": "2024-01-01",
    "to_date": "2024-12-31",
    "weekly_off": "Sunday"
})
# Auto-generate weekly offs
holiday_list.get_weekly_off_dates()
# Add local holidays by country
holiday_list.get_local_holidays()
holiday_list.insert()

# Check if date is holiday
from erpnext.setup.doctype.holiday_list.holiday_list import is_holiday
is_holiday("US Holidays 2024", "2024-12-25")  # True for Christmas
```

### Global Defaults

```python
# Get/Set global defaults
global_defaults = frappe.get_single("Global Defaults")
global_defaults.default_company = "ACME Corp"
global_defaults.default_currency = "USD"
global_defaults.hide_currency_symbol = 0
global_defaults.disable_rounded_total = 0
global_defaults.disable_in_words = 0
global_defaults.save()
```

### Sales Person

```python
# Create Sales Person (hierarchical)
sales_person = frappe.get_doc({
    "doctype": "Sales Person",
    "sales_person_name": "John Smith",
    "parent_sales_person": "Sales Team",
    "employee": "EMP-0001",  # Optional link to Employee
    "commission_rate": 5.0
})
sales_person.insert()
```

### Customer Group

```python
# Create Customer Group hierarchy
customer_group = frappe.get_doc({
    "doctype": "Customer Group",
    "customer_group_name": "Enterprise",
    "parent_customer_group": "All Customer Groups",
    "default_price_list": "Enterprise Price List"
})
customer_group.insert()

# Get all parent groups (for pricing rules)
from erpnext.setup.doctype.customer_group.customer_group import get_parent_customer_groups
parent_groups = get_parent_customer_groups("Enterprise")
```

## Setup Wizard Operations

### Installation Flow

```python
# After ERPNext install, setup wizard runs these operations:

# 1. Install base fixtures (UOM, Market Segments, Sales Stages)
from erpnext.setup.setup_wizard.operations.install_fixtures import install
install(country="United States")

# 2. Create Company with Chart of Accounts
from erpnext.setup.setup_wizard.operations.company_setup import create_fiscal_year_and_company
create_fiscal_year_and_company({
    "company_name": "ACME Corp",
    "company_abbr": "ACME",
    "chart_of_accounts": "Standard",
    "country": "United States",
    "currency": "USD",
    "fy_start_date": "2024-01-01",
    "fy_end_date": "2024-12-31"
})

# 3. Set default settings
from erpnext.setup.setup_wizard.operations.defaults_setup import set_default_settings
set_default_settings({
    "company_name": "ACME Corp",
    "currency": "USD"
})
```

### Default Setup Functions

```python
# Create default price lists (Standard Buying/Selling)
from erpnext.setup.setup_wizard.operations.defaults_setup import create_price_lists
create_price_lists({"currency": "USD"})

# Create default territories
from erpnext.setup.setup_wizard.operations.defaults_setup import create_territories
create_territories()
# Creates: Home country territory + "Rest of the World"

# Create employee for setup user
from erpnext.setup.setup_wizard.operations.defaults_setup import create_employee_for_self
create_employee_for_self({
    "first_name": "Admin",
    "last_name": "User",
    "email": "admin@example.com"
})
```

## Code Examples from Codebase

### Employee Status Validation

*Source: test_employee.py - Validates employee cannot be marked "Left" if others report to them*

```python
employee1 = make_employee('test_employee_1@company.com')
employee2 = make_employee('test_employee_2@company.com')

employee1_doc = frappe.get_doc('Employee', employee1)
employee2_doc = frappe.get_doc('Employee', employee2)

# Set up reporting hierarchy
employee2_doc.reports_to = employee1_doc.name
employee2_doc.save()

# This should raise error - can't mark as Left when others report to you
employee1_doc.status = 'Left'
self.assertRaises(InactiveEmployeeStatusError, employee1_doc.save)
```

### Employee User Permissions

*Source: test_employee.py - Validates user permission filtering*

```python
employee1 = make_employee('employee_1_test@company.com', create_user_permission=1)
employee2 = make_employee('employee_2_test@company.com', create_user_permission=1)

# Set up hierarchy
employee2_doc = frappe.get_doc('Employee', employee2)
employee2_doc.reports_to = employee1_doc.name
employee2_doc.save()

# Switch to employee1's user context
frappe.set_user(employee1_doc.user_id)

# Query should respect user permissions
employee_list = frappe.db.get_list('Employee', pluck='name')
# employee1 can see themselves and their reportees
```

### Item Group Tree Operations

*Source: test_item_group.py - Moving groups in hierarchy*

```python
# Get current position
old_lft, old_rgt = frappe.db.get_value('Item Group', '_Test Item Group C', ['lft', 'rgt'])

# Move Group B under Group C
group_b = frappe.get_doc('Item Group', '_Test Item Group B')
group_b.parent_item_group = '_Test Item Group C'
group_b.save()

# Verify tree integrity (lft/rgt values updated correctly)
new_lft, new_rgt = frappe.db.get_value('Item Group', '_Test Item Group C', ['lft', 'rgt'])
```

### Company Monthly Sales Update

*Source: company.py - Tracks monthly sales for dashboard*

```python
def update_company_current_month_sales(company):
    """Update Company's Total Monthly Sales.

    Uses date range for current month (portable + index-friendly).
    """
    # Calculates from Sales Invoices
    # Updates company.total_monthly_sales
```

## API Reference Summary

### Company Module

| Function | Description |
|----------|-------------|
| `get_name_with_abbr(name, company)` | Returns name with company abbreviation suffix |
| `install_country_fixtures(company, country)` | Installs country-specific data |
| `update_company_current_month_sales(company)` | Updates monthly sales total |
| `get_default_company_address(name)` | Gets primary company address |
| `create_transaction_deletion_request(company)` | Creates request to delete all transactions |

### Employee Module

| Function | Description |
|----------|-------------|
| `is_holiday(employee, date)` | Check if date is holiday for employee |
| `get_holiday_list_for_employee(employee)` | Get employee's holiday list |
| `get_all_employee_emails(company)` | Get all employee emails in company |
| `create_user(employee, user, email)` | Create Frappe User for employee |
| `deactivate_sales_person(status, employee)` | Deactivate linked Sales Person |

### Item Group Module

| Function | Description |
|----------|-------------|
| `get_child_item_groups(item_group_name)` | Get all child groups recursively |
| `get_item_group_defaults(item, company)` | Get defaults for item from group |

### Holiday List Module

| Function | Description |
|----------|-------------|
| `is_holiday(holiday_list, date)` | Check if date is in holiday list |
| `is_half_holiday(holiday_list, date)` | Check if date is half-day holiday |
| `get_events(start, end, filters)` | Get holidays for calendar view |

### Department Module

| Function | Description |
|----------|-------------|
| `get_abbreviated_name(name, company)` | Returns "Name - ABBR" format |
| `get_children(doctype, parent, company)` | Get child departments |

## Design Patterns Detected

| Pattern | Count | Usage |
|---------|-------|-------|
| **Factory** | 7 instances | Company setup creates warehouses, accounts, departments |
| **Observer** | 2 instances | Employee on_update triggers user permission updates |

## Available Reference Files

### API Reference (`references/api_reference/`)

| File | Description |
|------|-------------|
| `company.md` | Company DocType - all methods and functions |
| `employee.md` | Employee DocType - validation, user linkage |
| `item_group.md` | Item Group hierarchy management |
| `department.md` | Department NestedSet operations |
| `holiday_list.md` | Holiday management functions |
| `global_defaults.md` | System-wide default settings |
| `sales_person.md` | Sales person hierarchy and commission |
| `customer_group.md` | Customer segmentation tree |
| `currency_exchange.md` | Currency exchange rate management |
| `authorization_rule.md` | Transaction authorization limits |
| `install.md` | Post-install setup functions |
| `install_fixtures.md` | Fixture installation operations |
| `defaults_setup.md` | Default settings setup |

### Documentation (`references/documentation/`)

| Category | Content |
|----------|---------|
| Architecture | Employee, Designation DocType structures |
| Other | Authorization Rules, Branch, Brand, Company setup guides |

## Working with This Skill

### For Beginners

1. **Start with Company**: Every ERPNext instance needs at least one Company
2. **Understand the hierarchy**: Company → Department → Employee
3. **Use setup wizard**: For new installations, let the wizard handle initial setup
4. **Check Global Defaults**: Many issues come from incorrect global settings

### For Intermediate Users

1. **Multi-company setup**: Use parent-child Company relationships
2. **User Permissions**: Link Employees to Users for automatic data filtering
3. **Holiday Lists**: Essential for HR module (Leave, Attendance)
4. **Item Groups**: Build proper hierarchy for pricing rules and reports

### For Advanced Users

1. **NestedSet operations**: Understand lft/rgt for custom queries
2. **Setup fixtures**: Customize `install_fixtures.py` for custom data
3. **Authorization Rules**: Set up approval workflows based on amounts
4. **Currency Exchange**: Automatic rate fetching and validation

### Common Integration Points

```
Company ─┬─► Chart of Accounts (Accounting)
         ├─► Default Warehouse (Stock)
         ├─► Cost Center (Accounting)
         └─► Departments ─► Employees

Employee ─┬─► User (Frappe)
          ├─► User Permissions
          ├─► Sales Person (Selling)
          └─► Holiday List (HR)

Item Group ─► Item Defaults (Stock)
           ─► Pricing Rules (Selling/Buying)

Customer Group ─► Customer Defaults (Selling)
               ─► Pricing Rules
```

## Common Issues & Solutions

### Issue: Department names conflict across companies

**Solution**: Departments auto-append company abbreviation:
```python
# "Engineering" in company "ACME" becomes "Engineering - ACME"
```

### Issue: Employee can't login

**Solution**: Check `user_id` field is linked to an enabled User:
```python
employee = frappe.get_doc("Employee", employee_name)
user = frappe.get_doc("User", employee.user_id)
if not user.enabled:
    user.enabled = 1
    user.save()
```

### Issue: Holiday list not working

**Solution**: Verify holiday list is assigned to Employee or Company:
```python
# Check Employee → Holiday List field
# Or Company → Default Holiday List in HR Settings
```

---

**Module Statistics:**
- 73 files analyzed
- 37 API reference documents generated
- 25 documentation files extracted
- 9 design patterns detected

**Generated from ERPNext v16 codebase analysis**
