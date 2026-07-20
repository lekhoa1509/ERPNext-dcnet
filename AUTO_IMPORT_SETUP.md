# Data Import Auto-Import Setup

## Overview
Removed the manual "Import" button confirmation step. Now imports start automatically when a file is uploaded to the Data Import form.

## Changes Made

### 1. Backend Method (`data_import_auto.py`)
- **File:** `dcnet_apps/dcnet_apps/utils/data_import_auto.py`
- **Function:** `auto_start_import(data_import_name)`
- **Purpose:** Whitelisted method that directly triggers import without confirmation
- **Called by:** Client script when file is uploaded

### 2. Client Script (`client_script_data_import_auto.json`)
- **File:** `dcnet_apps/dcnet_apps/fixtures/client_script_data_import_auto.json`
- **Trigger:** When `import_file` field changes
- **Behavior:**
  - Detects when file is uploaded and document is saved
  - Waits 500ms for file processing
  - Calls `auto_start_import()` method
  - Shows success/error alert
  - Disables save button during import

### 3. Hooks Configuration (`hooks.py`)
- **Change:** Added "Data Import" to Client Script fixtures filter
- **Line 85:** `"filters": [["dt", "in", ["Lead", "Batch", "Purchase Receipt", "Data Import"]]]`
- **Effect:** Frappe will load the Data Import client script on form load

## How It Works

1. User uploads CSV/XLSX file to Data Import form
2. File is saved to the document
3. Client script detects `import_file` change
4. After 500ms delay, `auto_start_import()` is called
5. Import starts immediately without user clicking "Start Import" button
6. User sees green alert: "Import started automatically"
7. Form is disabled during import (prevents accidental changes)

## Installation

Run migration to load the new client script fixture:

```bash
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local migrate"
```

## Testing

1. Go to Data Import form
2. Upload a CSV/XLSX file
3. Save the form
4. Import should start automatically
5. Check import progress in the form

## Rollback

If you need to revert to manual import:

1. Delete the client script: `Data Import - Auto Import`
2. Remove "Data Import" from hooks.py line 85
3. Run migrate again

## Notes

- The "Start Import" button is still visible but won't be needed
- Users can still manually click it if needed (it will retry if import failed)
- Import validation (row limits, etc.) still applies
- All existing import features work the same way
