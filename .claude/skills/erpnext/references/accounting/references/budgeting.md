# Erpnext_Accounting - Budgeting

**Pages:** 2

---

## Budget Revision

**URL:** https://docs.frappe.io/erpnext/erpnext/accounting/erpnext/erpnext/accounting/budgeting/budget-revision

**Contents:**
- Budget Revision
- 1. How can you revise an existing budget
- 2. When to Use a Budget Revision

A Budget Revision allows you to update an existing budget when plans change during the fiscal year.

Instead of editing a submitted Budget, revisions help maintain:

The previous Budget is cancelled, The revised Budget becomes active.

Use a Budget Revision when:

---

## Budget

**URL:** https://docs.frappe.io/erpnext/erpnext/accounting/erpnext/erpnext/accounting/budgeting/budget

**Contents:**
- Budget
- 1. Prerequisites
- 2. How to Create a new Budget
- 3. Budget Distribution
    - Distribution Frequency
    - Distribute Equally
- 4. Control Actions (Alerts)
- 5. Exception Budget Approver Role

Budgeting is a financial plan that helps controlling company expenses.

Budgeting helps control company expenses by defining how much can be spent, where it can be spent, and within which fiscal years.

In ERPNext, budgets are created against a single dimension (Cost Center, Project, or Accounting Dimension) and are used to plan expenses and prevent overspending.

To access the Budget list, go to:

Home > Accounting > Cost Center and Budgeting > Budget

Before creating and using Budgets, ensure the following are set up:

A single Budget applies to one account and one dimension, and can span multiple fiscal years.

Budget Distribution controls how the total budget amount is allocated across time within the selected fiscal years. Each row of budget distribution child table contains - Start Date, End Date, Amount, Percentage.

Distribution Frequency defines the time interval used for budget allocation:

On budget there is a checkbox Distribute Equally, when this checkbox is enabled, the total budget amount is split evenly across all periods. Budget Distribution rows are generated automatically.

When Distribute Equally is disabled, budget distribution rows are still generated automatically based on the selected distribution frequency but Start Date and End Date are not editable and you can manually adjust: Amount or Percentage.

Control actions can be triggered when:

You can set a control action in the Budget based on Material Requests, Purchase Orders, or on actual expenses. Further, you can set a control action for annual or monthly budgets.

There are three types of control actions.

You can set separate actions for monthly and annual budgets. If you exceed the budget, a warning will be shown:

Note that a similar warning will be triggered for any type of transactions set in the budget for the particular Account heads.

This setting allows selected users to bypass budget restrictions even when the budget is exceeded.

Here is a video demonstration:

---
