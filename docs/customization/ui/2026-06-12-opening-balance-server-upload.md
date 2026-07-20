# Opening Balance Server Upload

## Overview

`Opening Balance Import` now accepts Excel files from the user's computer and
stores them in the site's private server files before analysis.

## Requirement

- Source: user request on 2026-06-12.
- Add the same file and folder upload workflow already available in `Import Auto`.
- Keep the existing server path input available for migration operators.

## Implementation

- Added `Upload Files` and `Upload Folder` actions to the form and dashboard.
- Uploaded `.xlsx` and `.xls` files preserve their relative folder paths.
- Files are saved under `private/files/import_auto_uploads/` in a folder scoped
  to the `Opening Balance Import` document.
- The document's `folder_path` is updated automatically.
- Upload completion starts `AI Analyze Files` immediately.
- Existing server-side filename, extension, path traversal, CSRF, and document
  permission checks are reused from `Import Auto`.
- The `dcnet_migrate` install/migrate hook and project setup scripts enforce a
  minimum 100 MB request limit per uploaded file without reducing a higher
  administrator-defined limit.
- The UI validates the active Frappe upload limit before sending the request.

## Files

- `dcnet-migrate/dcnet_migrate/import_auto/doctype/import_auto/import_auto.py`
- `dcnet-migrate/dcnet_migrate/import_auto/doctype/opening_balance_import/opening_balance_import.py`
- `dcnet-migrate/dcnet_migrate/import_auto/doctype/opening_balance_import/opening_balance_import.js`

## Deployment

```bash
bench --site flow.local migrate
bench --site flow.local clear-cache
```

## Verification

- Python syntax check.
- JavaScript syntax check.
- Manual upload of multiple files and a nested folder.
