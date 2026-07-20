# VN Accounting Tax Settings Sidebar

## Overview

Added missing tax setup links to the VN Accounting tax sidebar so accounting users can access tax categories, tax rules, and withholding tax categories from the same tax menu as VAT reports and tax templates.

## Requirements

- Surface tax setup entries needed by accounting users.
- Keep the items inside `VN Accounting > Thuế`.
- Use standard ERPNext DocTypes where available.

## Implementation

- Added `Danh mục thuế` linking to `Tax Category`.
- Added `Quy tắc thuế` linking to `Tax Rule`.
- Added `Danh mục thuế khấu trừ` linking to `Tax Withholding Category`.
- Updated tax help index and added short user guides for the new entries.

## Files Changed

- `dcnet-accounting/vn_accounting/workspace_sidebar/vn_accounting.json`
- `dcnet-accounting/vn_accounting/help/thue/index.md`
- `dcnet-accounting/vn_accounting/help/thue/danh-muc-thue.md`
- `dcnet-accounting/vn_accounting/help/thue/quy-tac-thue.md`
- `dcnet-accounting/vn_accounting/help/thue/danh-muc-thue-khau-tru.md`

## Deployment

Run sidebar sync and clear cache:

```bash
bench --site flow.local execute vn_accounting.install._sync_workspace_sidebar
bench --site flow.local clear-cache
```

## Verification Checklist

- `Danh mục thuế` appears under `VN Accounting > Thuế`.
- `Quy tắc thuế` appears under `VN Accounting > Thuế`.
- `Danh mục thuế khấu trừ` appears under `VN Accounting > Thuế`.
- Each item opens the expected ERPNext DocType list.
