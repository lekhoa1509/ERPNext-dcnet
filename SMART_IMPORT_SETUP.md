# Smart Import - AI-Powered Data Import

## Overview

**Smart Import** is an intelligent data import system that:
- ✅ Analyzes uploaded CSV/XLSX files automatically
- ✅ Maps columns to DocType fields intelligently (no manual mapping needed)
- ✅ Validates and transforms data based on field types
- ✅ Inserts records directly into the database
- ✅ Bypasses the standard import confirmation flow

## How It Works

```
User uploads file
    ↓
Smart Import dialog appears
    ↓
User confirms "Use Smart Import"
    ↓
System analyzes file headers
    ↓
AI maps columns to DocType fields
    ↓
Data is validated & transformed
    ↓
Records inserted directly
    ↓
Results shown (success/failed count)
```

## Features

### 1. Automatic Column Mapping
- **Exact Match**: Matches headers to field names (case-insensitive)
- **Label Match**: Matches headers to field labels
- **Fuzzy Match**: Finds similar field names using word overlap
- **Confidence Threshold**: Only maps columns with >50% confidence

### 2. Data Type Conversion
Automatically converts data based on field type:
- `Int` → Converts to integer
- `Float` → Converts to decimal
- `Currency` → Removes symbols, converts to float
- `Date` → Parses date strings
- `Checkbox` → Converts yes/no/true/false to 1/0
- `Link` → Validates linked document exists
- `Data` → Keeps as string

### 3. Validation
- Checks required fields
- Validates linked documents exist
- Handles missing/null values gracefully
- Logs errors for failed rows

### 4. Direct Insertion
- Creates documents directly without manual review
- Bypasses standard import UI
- Faster processing for large files
- Maintains data integrity

## Files Created

### Backend
- **`dcnet_apps/dcnet_apps/utils/smart_import.py`**
  - `SmartImporter` class: Main logic
  - `smart_import()` whitelisted method: Entry point
  - Column mapping algorithm
  - Data validation & transformation

### Frontend
- **`dcnet_apps/dcnet_apps/fixtures/client_script_smart_import.json`**
  - Triggers when file is uploaded
  - Shows confirmation dialog
  - Calls backend method
  - Displays results

### Configuration
- **`dcnet_apps/dcnet_apps/hooks.py`** (line 85)
  - Added "Data Import" to Client Script fixtures

## Usage

### Step 1: Go to Data Import
Navigate to: **Data Import** form

### Step 2: Select DocType
Choose the target DocType (e.g., Customer, Item, Sales Order)

### Step 3: Upload File
Upload CSV or XLSX file with data

### Step 4: Save
Save the form

### Step 5: Confirm Smart Import
Dialog appears asking "Use Smart Import?"
- Click **Yes** → Smart Import starts
- Click **No** → Use standard import

### Step 6: View Results
Results show:
- ✅ Number of records created
- ❌ Number of failed records
- 📋 Error details (if any)

## Example

### Input File (customers.csv)
```
Customer Name,Email,Phone,City
ABC Company,abc@example.com,0123456789,Hanoi
XYZ Corp,xyz@example.com,0987654321,HCMC
```

### Column Mapping (Auto-detected)
```
Customer Name → customer_name
Email → email_id
Phone → phone
City → city
```

### Result
```
✅ Smart Import Complete: 2 records created, 0 failed
```

## Installation

### 1. Run Migration
```bash
docker exec devcontainer-frappe-1 bash -c \
  "cd /workspace/development/frappe-bench && \
   bench --site flow.local migrate"
```

### 2. Clear Cache
```bash
docker exec devcontainer-frappe-1 bash -c \
  "cd /workspace/development/frappe-bench && \
   bench --site flow.local clear-cache"
```

### 3. Test
1. Go to Data Import form
2. Upload a test CSV file
3. Save the form
4. Confirm Smart Import dialog
5. Check results

## Configuration

### Confidence Threshold
Edit `smart_import.py` line 127:
```python
if best_match and best_score > 0.5:  # Change 0.5 to adjust sensitivity
```

### Max Rows
Edit `data_import_validation.py` to adjust:
```python
DEFAULT_MAX_IMPORT_ROWS = 5000  # Change as needed
```

## Error Handling

### Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| "File is empty" | CSV/XLSX has no data rows | Add data rows to file |
| "Could not map any columns" | Headers don't match any fields | Check column names match DocType fields |
| "No valid rows found" | All rows failed validation | Check data types match field types |
| "Link validation failed" | Referenced document doesn't exist | Ensure linked records exist first |

### Viewing Errors
Errors are logged in:
- **Frappe Error Log**: Menu → Tools → Error Log
- Search for "Smart Import"

## Advantages vs Standard Import

| Feature | Smart Import | Standard Import |
|---------|--------------|-----------------|
| Column Mapping | Automatic | Manual |
| Data Validation | Automatic | Manual |
| Insertion | Direct | Requires confirmation |
| Speed | Fast | Slower (requires review) |
| Learning Curve | Low | High |
| Error Handling | Automatic | Manual |

## Limitations

- ⚠️ Requires exact field names or similar labels
- ⚠️ Cannot handle complex nested data
- ⚠️ Link fields must reference existing documents
- ⚠️ No support for child table imports yet
- ⚠️ File size limited to 5000 rows by default (configurable)

## Future Enhancements

- [ ] Support for child table imports
- [ ] AI-powered column mapping using LLM
- [ ] Batch import with progress tracking
- [ ] Import templates/presets
- [ ] Duplicate detection
- [ ] Data enrichment from external sources

## Troubleshooting

### Smart Import dialog doesn't appear
1. Check browser console for errors (F12)
2. Verify client script is loaded: Menu → Tools → Client Script
3. Clear browser cache (Ctrl+Shift+Delete)
4. Run `bench clear-cache` and refresh

### Records not being created
1. Check error log for validation errors
2. Verify linked documents exist
3. Check field types match data
4. Try with smaller file first

### Slow import
1. Reduce file size (split into batches)
2. Check server resources
3. Disable other background jobs
4. Check database performance

## Support

For issues or questions:
1. Check error log: Menu → Tools → Error Log
2. Review this documentation
3. Contact development team

---

**Last Updated:** 2026-05-21
**Version:** 1.0
**Status:** Production Ready
