---
name: dcnet-vn-accounting-import
description: |
  Use when fixing or planning Vietnamese accounting imports for DCNET Flow / ERPNext:
  Chart of Accounts, hệ thống tài khoản, cây tài khoản, TT200, TT133, COA,
  Account import, parent_account, tài khoản cha, account_number, Import Auto,
  Smart Import, NEW_DEPENDENCY_STEPS, PATCHES, BRAVO accounting migration,
  or errors where a parent account like 1121 exists later in the same Excel file.
---

# DCNET Vietnamese Accounting Import

Use this skill for Vietnamese accounting data imports, especially ERPNext `Account`
records from a Chart of Accounts file. The goal is to preserve source accounting
data and fix only structural/import-safe fields.

## Core Rule

If a missing `parent_account` value exists anywhere in the same Excel file or
same import plan, it is **not** missing master data.

Handle it by normalising the parent value and ordering the Account tree so the
parent row is inserted before the child row. Do **not** create
`NEW_DEPENDENCY_STEPS` for that Account, because it will duplicate the row that
is already in the file.

Example:

```text
1121.2 -> parent 1121
1121 exists in the same Excel file at another row
Fix: sort/import 1121 before 1121.2
Wrong: create Account 1121 as NEW_DEPENDENCY_STEPS
Wrong: mark unresolved only because 1121 is not in DB yet
```

## Workflow

1. Confirm this is accounting data:
   - Target DocType is `Account`, or filename/header contains `Chart of Accounts`,
     `he_thong_tai_khoan`, `tai_khoan`, `account_number`, `parent_account`.
   - For other accounting master data, still apply the "same-file means not
     missing" rule to links when possible.

2. Read the full source, not only the preview sample:
   - Build an index by `account_number`, raw `account_name`, predicted ERPNext
     Account name, and row number.
   - Use the full index when deciding whether a parent is missing.

3. Preserve source-of-truth fields:
   - Never change `account_number`, `account_name`, opening balances, debit,
     credit, amount, currency, or source row identity.
   - Treat `account_number` as text, never as a number. Values like `1121.20`
     must not become `1121.2`.
   - Only patch safe structural fields: `parent_account`, `is_group`, `root_type`,
     `report_type`, `account_type`, `account_currency`, `company`, `disabled`,
     `balance_must_be`.

4. Resolve parent accounts:
   - If `parent_account` is present in the file, normalise it.
   - If missing, infer from `account_number` only when the inferred parent exists
     in the same file or already exists in ERPNext.
   - If the inferred parent is not in file and not in DB, then it may be a true
     missing dependency or unresolved issue.

5. Sort the tree:
   - Parent must appear before child within the import step.
   - Do a topological sort by `parent_account`.
   - Cycles are data errors; report them with row/account numbers.
   - Do not use fuzzy matching for Account numbers. `1121` is not the same as
     `112`, even if text similarity is high.

6. Use dependencies conservatively:
   - Create dependency steps only for records truly absent from both DB and file.
   - For COA, automatically create only the Vietnamese root Accounts when missing:
     `Tài sản`, `Nợ phải trả`, `Vốn chủ sở hữu`, `Thu nhập`, `Chi phí`.
   - Never propose `NEW_DEPENDENCY_STEPS` for an `Account` whose `account_number`
     or `account_name` appears in the same source file or same plan.

## Parent Inference

Use Vietnamese account numbering before making AI guesses:

| Account number | Parent rule |
|---|---|
| `111`, `112`, `131`, `331`, `511` | Parent is VN root by account class |
| `1111`, `1112`, `1121` | Parent is first 3 digits: `1111 -> 111`, `1121 -> 112` |
| `1121.2`, `1121.20` | Parent is before dot: `1121` |
| `11210`, `11211` | Parent is first 4 digits: `1121` |

If the source file explicitly supplies a valid parent, prefer the source value.
If it supplies an invalid/missing parent, patch only `parent_account`.

## ERPNext Account Name Rules

ERPNext Account links usually use the final Account document name, commonly:

```text
{account_number} - {account_name} - {company_abbr}
```

or, for root Accounts without an account number:

```text
{account_name} - {company_abbr}
```

When a source parent is a bare account number like `1121`, resolve it to the
matching same-file or existing ERPNext Account. Do not leave a child pointing
to a non-existent literal value like `1121 - ABBR` if the final Account name is
`1121 - Tiền gửi ngân hàng VND - ABBR`.

## VN Root Mapping

| Prefix | root_type | report_type | VN root |
|---|---|---|---|
| `1` | Asset | Balance Sheet | Tài sản |
| `2` | Liability | Balance Sheet | Nợ phải trả |
| `3` | Equity | Balance Sheet | Vốn chủ sở hữu |
| `4` | Equity | Balance Sheet | Vốn chủ sở hữu |
| `5` | Income | Profit and Loss | Thu nhập |
| `6` | Expense | Profit and Loss | Chi phí |
| `7` | Income | Profit and Loss | Thu nhập |
| `8` | Expense | Profit and Loss | Chi phí |
| `9` | Expense | Profit and Loss | Chi phí |

## Basic Account Type Hints

Set `account_type` only when obvious; otherwise leave blank.

| Prefix/example | account_type |
|---|---|
| `111` | Cash |
| `112`, `113` | Bank |
| `131`, `136`, `138` | Receivable |
| `331`, `336`, `338` | Payable |
| `133`, `333` | Tax |
| `151`, `152`, `153`, `155`, `156`, `157` | Stock |
| `211`, `212`, `213`, `217` | Fixed Asset |
| `214` | Accumulated Depreciation |
| `511`, `515`, `711` | Income Account |
| `632` | Cost of Goods Sold |
| `635`, `641`, `642`, `811`, `821`, `911` | Expense Account |

## Safe Fix Response Pattern

For a same-file parent error:

```json
{
  "patches": [
    {
      "step": 2,
      "row": 7,
      "field": "parent_account",
      "value": "1121",
      "reason": "TK cha 1121 có trong cùng file; dùng parent này và sort cây trước khi import."
    }
  ],
  "new_dependency_steps": [],
  "unresolved": []
}
```

If the issue is only row order, return no data-changing patches and state that
the backend should topologically sort the Account records.

## Validation Checklist

Before finishing:

- Every non-root Account has a parent that exists in DB, in a preceding step,
  or earlier in the same sorted Account step.
- No `NEW_DEPENDENCY_STEPS` duplicates an Account already present in the file.
- Root Accounts are limited to the five VN roots above.
- `account_number` and `account_name` are unchanged.
- Children like `1121.2` are ordered after parents like `1121`.
- Re-running the import with `ignore_duplicates=true` will not create duplicate
  Accounts.
