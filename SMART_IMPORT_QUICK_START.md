# Smart Import - Quick Start Guide

## What is Smart Import?

Smart Import replaces the manual import process with an intelligent system that:
- Automatically analyzes CSV/XLSX files
- Maps columns to database fields using AI
- Validates and transforms data
- Inserts records directly (no confirmation button needed)

## Installation (2 minutes)

```bash
# 1. Run migration to load client script
docker exec devcontainer-frappe-1 bash -c \
  "cd /workspace/development/frappe-bench && \
   bench --site flow.local migrate"

# 2. Clear cache
docker exec devcontainer-frappe-1 bash -c \
  "cd /workspace/development/frappe-bench && \
   bench --site flow.local clear-cache"

# 3. Done! Refresh browser
```

## Usage (3 steps)

### Step 1: Prepare File
Create CSV or XLSX with headers matching DocType field names or labels:

```csv
Customer Name,Email,Phone,City
ABC Company,abc@example.com,0123456789,Hanoi
XYZ Corp,xyz@example.com,0987654321,HCMC
```

### Step 2: Upload
1. Go to **Data Import** form
2. Select target DocType (e.g., Customer)
3. Upload your file
4. Click **Save**

### Step 3: Confirm
- Dialog appears: "Use Smart Import?"
- Click **Yes** → Import starts automatically
- Results show: "X records created, Y failed"

## Column Mapping Examples

### Customer Import
| File Column | Maps To | Notes |
|-------------|---------|-------|
| Customer Name | customer_name | Exact match |
| Email | email_id | Label match |
| Phone | phone_1 | Fuzzy match |
| City | city | Exact match |

### Item Import
| File Column | Maps To | Notes |
|-------------|---------|-------|
| Item Code | item_code | Exact match |
| Item Name | item_name | Exact match |
| Price | standard_rate | Label match |
| Stock | stock_qty | Fuzzy match |

## Data Type Conversion

Smart Import automatically converts data:

| Field Type | Input | Output |
|-----------|-------|--------|
| Int | "123.45" | 123 |
| Float | "123.45" | 123.45 |
| Currency | "$1,234.56" | 1234.56 |
| Date | "2026-05-21" | 2026-05-21 |
| Checkbox | "yes" / "no" | 1 / 0 |
| Link | "Customer-001" | Validates exists |

## Error Handling

### If import fails:
1. Check error log: Menu → Tools → Error Log
2. Search for "Smart Import"
3. Fix data issues
4. Try again

### Common issues:
- **"File is empty"** → Add data rows
- **"Could not map columns"** → Check header names
- **"Link validation failed"** → Ensure linked records exist

## Advantages

✅ **No manual mapping** - AI does it automatically
✅ **Faster** - Direct insertion, no confirmation needed
✅ **Smarter** - Handles data type conversion
✅ **Safer** - Validates all data before insertion
✅ **Easier** - Simple 3-step process

## Fallback to Standard Import

If Smart Import doesn't work:
1. Click **No** in the dialog
2. Use standard import with manual mapping
3. Click **Start Import** button

## Configuration

### Adjust confidence threshold (smart_import.py line 127):
```python
if best_match and best_score > 0.5:  # Lower = more lenient
```

### Adjust max rows (data_import_validation.py):
```python
DEFAULT_MAX_IMPORT_ROWS = 5000  # Increase for larger files
```

Can also be overridden with `dcnet_max_import_rows` in `site_config.json`
or the `DCNET_MAX_IMPORT_ROWS` environment variable.

## Support

- 📖 Full docs: `SMART_IMPORT_SETUP.md`
- 🐛 Errors: Menu → Tools → Error Log
- 💬 Questions: Contact dev team

---

**Ready to use!** Go to Data Import and try it now.
