# How To: Rollback and Recovery Strategies

**Difficulty**: Advanced
**Estimated Time**: 30 minutes
**Tags**: rollback, recovery, backup, error-handling

## Overview

Learn strategies for rolling back failed imports and recovering from errors. Covers transaction management, backup strategies, and data cleanup.

## Prerequisites

- Understanding of database transactions
- Frappe architecture knowledge
- Access to database administration

## Rollback Strategies

### 1. Transaction-Based Rollback

```python
import frappe

def import_with_transaction(doctype, data):
    """
    Import with full transaction support.
    """
    # Start transaction
    frappe.db.begin()

    try:
        created_docs = []

        for row in data:
            row["doctype"] = doctype
            doc = frappe.get_doc(row)
            doc.insert()
            created_docs.append(doc.name)

        # All succeeded, commit
        frappe.db.commit()

        return {
            "success": True,
            "created": created_docs
        }

    except Exception as e:
        # Rollback everything
        frappe.db.rollback()

        return {
            "success": False,
            "error": str(e),
            "rolled_back": True
        }
```

### 2. Savepoint-Based Partial Rollback

```python
import frappe

def import_with_savepoints(doctype, data, batch_size=100):
    """
    Import with savepoints for partial rollback.
    """
    results = {
        "successful_batches": [],
        "failed_batches": [],
        "created_docs": []
    }

    for i in range(0, len(data), batch_size):
        batch_num = i // batch_size
        batch = data[i:i + batch_size]

        # Create savepoint
        savepoint_name = f"batch_{batch_num}"
        frappe.db.savepoint(savepoint_name)

        try:
            batch_docs = []
            for row in batch:
                row["doctype"] = doctype
                doc = frappe.get_doc(row)
                doc.insert()
                batch_docs.append(doc.name)

            results["successful_batches"].append(batch_num)
            results["created_docs"].extend(batch_docs)

        except Exception as e:
            # Rollback only this batch
            frappe.db.rollback(save_point=savepoint_name)
            results["failed_batches"].append({
                "batch": batch_num,
                "error": str(e)
            })

    # Commit successful batches
    frappe.db.commit()

    return results
```

### 3. Backup Before Import

```python
import frappe
from frappe.utils import now_datetime

def backup_before_import(doctype, backup_name=None):
    """
    Create backup of DocType data before import.
    """
    if not backup_name:
        backup_name = f"{doctype}_{now_datetime().strftime('%Y%m%d_%H%M%S')}"

    # Get all current records
    data = frappe.get_all(
        doctype,
        fields=["*"],
        limit_page_length=0
    )

    # Store as JSON
    backup_doc = frappe.get_doc({
        "doctype": "Data Import Backup",  # Custom DocType
        "backup_name": backup_name,
        "reference_doctype": doctype,
        "record_count": len(data),
        "data": frappe.as_json(data),
        "created_at": now_datetime()
    })
    backup_doc.insert()

    print(f"Backed up {len(data)} records to {backup_name}")
    return backup_name

def restore_from_backup(backup_name):
    """
    Restore data from backup.
    """
    backup = frappe.get_doc("Data Import Backup", backup_name)
    doctype = backup.reference_doctype
    data = frappe.parse_json(backup.data)

    # Clear current data
    frappe.db.sql(f"DELETE FROM `tab{doctype}`")

    # Restore
    for row in data:
        doc = frappe.get_doc(row)
        doc.flags.ignore_permissions = True
        doc.insert()

    frappe.db.commit()
    print(f"Restored {len(data)} records from {backup_name}")
```

### 4. Import Log-Based Recovery

```python
import frappe

def get_import_for_rollback(data_import_name):
    """
    Get all documents created by an import for rollback.
    """
    data_import = frappe.get_doc("Data Import", data_import_name)

    created_docs = []
    for log in data_import.import_log:
        if log.success and log.docname:
            created_docs.append({
                "doctype": data_import.reference_doctype,
                "name": log.docname
            })

    return created_docs

def rollback_import(data_import_name, confirm=False):
    """
    Rollback all documents created by an import.
    """
    docs = get_import_for_rollback(data_import_name)

    if not confirm:
        return {
            "message": f"Would delete {len(docs)} documents",
            "documents": docs[:10],  # Show first 10
            "confirm_required": True
        }

    deleted = 0
    errors = []

    for doc_info in docs:
        try:
            frappe.delete_doc(
                doc_info["doctype"],
                doc_info["name"],
                force=True,
                ignore_permissions=True
            )
            deleted += 1
        except Exception as e:
            errors.append({
                "doc": doc_info["name"],
                "error": str(e)
            })

    frappe.db.commit()

    return {
        "deleted": deleted,
        "errors": errors
    }
```

### 5. Soft Delete with Recovery

```python
import frappe
from frappe.utils import now_datetime

def soft_delete_import(doctype, filter_field, filter_value):
    """
    Soft delete by marking records instead of deleting.
    """
    # Add a custom field 'deleted_at' to track soft deletes

    frappe.db.sql(f"""
        UPDATE `tab{doctype}`
        SET deleted_at = %s, deleted_by = %s
        WHERE {filter_field} = %s AND deleted_at IS NULL
    """, (now_datetime(), frappe.session.user, filter_value))

    frappe.db.commit()

def recover_soft_deleted(doctype, deleted_before=None):
    """
    Recover soft-deleted records.
    """
    conditions = ["deleted_at IS NOT NULL"]
    values = []

    if deleted_before:
        conditions.append("deleted_at >= %s")
        values.append(deleted_before)

    frappe.db.sql(f"""
        UPDATE `tab{doctype}`
        SET deleted_at = NULL, deleted_by = NULL
        WHERE {' AND '.join(conditions)}
    """, values)

    frappe.db.commit()

def hard_delete_soft_deleted(doctype, older_than_days=30):
    """
    Permanently delete soft-deleted records older than X days.
    """
    cutoff = frappe.utils.add_days(frappe.utils.now(), -older_than_days)

    frappe.db.sql(f"""
        DELETE FROM `tab{doctype}`
        WHERE deleted_at IS NOT NULL AND deleted_at < %s
    """, (cutoff,))

    frappe.db.commit()
```

### 6. Idempotent Import with Checkpoints

```python
import frappe
import hashlib

def idempotent_import(doctype, data, import_id):
    """
    Import that can be safely re-run.
    Uses checkpoints to track progress.
    """
    # Get or create checkpoint
    checkpoint = get_checkpoint(import_id)

    processed = set(checkpoint.get("processed_rows", []))
    results = {"new": 0, "skipped": 0, "failed": 0}

    for i, row in enumerate(data):
        row_hash = hash_row(row)

        if row_hash in processed:
            results["skipped"] += 1
            continue

        try:
            row["doctype"] = doctype
            doc = frappe.get_doc(row)
            doc.insert()

            processed.add(row_hash)
            results["new"] += 1

            # Save checkpoint every 100 rows
            if len(processed) % 100 == 0:
                save_checkpoint(import_id, list(processed))

        except frappe.DuplicateEntryError:
            processed.add(row_hash)
            results["skipped"] += 1

        except Exception as e:
            results["failed"] += 1
            frappe.log_error(f"Row {i}: {e}")

    # Final checkpoint
    save_checkpoint(import_id, list(processed))
    frappe.db.commit()

    return results

def hash_row(row):
    """Create hash of row for tracking."""
    content = "|".join(str(v) for v in sorted(row.items()))
    return hashlib.md5(content.encode()).hexdigest()

def get_checkpoint(import_id):
    """Get import checkpoint."""
    try:
        return frappe.parse_json(
            frappe.cache().get_value(f"import_checkpoint_{import_id}")
        ) or {}
    except:
        return {}

def save_checkpoint(import_id, processed_rows):
    """Save import checkpoint."""
    frappe.cache().set_value(
        f"import_checkpoint_{import_id}",
        frappe.as_json({"processed_rows": processed_rows})
    )
```

## Complete Recovery Manager

```python
import frappe
from frappe.utils import now_datetime

class ImportRecoveryManager:
    """
    Manage import rollback and recovery.
    """

    def __init__(self, doctype):
        self.doctype = doctype
        self.backup_name = None

    def pre_import_backup(self):
        """Create backup before import."""
        self.backup_name = f"{self.doctype}_{now_datetime().strftime('%Y%m%d_%H%M%S')}"

        # Export current data
        data = frappe.get_all(self.doctype, fields=["*"])

        # Save to file
        import json
        backup_path = f"/tmp/{self.backup_name}.json"

        with open(backup_path, "w") as f:
            json.dump(data, f, default=str)

        print(f"Backup created: {backup_path}")
        return backup_path

    def import_with_recovery(self, data, batch_size=100):
        """
        Import with full recovery support.
        """
        # Pre-backup
        backup_path = self.pre_import_backup()

        results = {
            "success": 0,
            "failed": 0,
            "created_docs": [],
            "errors": [],
            "backup": backup_path
        }

        for i in range(0, len(data), batch_size):
            batch = data[i:i + batch_size]

            # Savepoint for batch
            frappe.db.savepoint(f"batch_{i}")

            batch_success = True
            batch_docs = []

            for row in batch:
                try:
                    row["doctype"] = self.doctype
                    doc = frappe.get_doc(row)
                    doc.insert()
                    batch_docs.append(doc.name)
                    results["success"] += 1
                except Exception as e:
                    results["failed"] += 1
                    results["errors"].append({
                        "row": row,
                        "error": str(e)
                    })
                    batch_success = False

            if batch_success:
                results["created_docs"].extend(batch_docs)
            else:
                # Rollback batch on any error
                frappe.db.rollback(save_point=f"batch_{i}")
                results["success"] -= len(batch_docs)
                results["failed"] += len(batch_docs)

        frappe.db.commit()
        return results

    def rollback_created(self, doc_names):
        """
        Rollback specific created documents.
        """
        deleted = 0
        errors = []

        for name in doc_names:
            try:
                frappe.delete_doc(
                    self.doctype,
                    name,
                    force=True
                )
                deleted += 1
            except Exception as e:
                errors.append({"name": name, "error": str(e)})

        frappe.db.commit()
        return {"deleted": deleted, "errors": errors}

    def restore_from_backup(self, backup_path):
        """
        Full restore from backup.
        """
        import json

        with open(backup_path, "r") as f:
            data = json.load(f)

        # Clear current data
        current_count = frappe.db.count(self.doctype)
        frappe.db.sql(f"DELETE FROM `tab{self.doctype}`")

        # Restore
        restored = 0
        for row in data:
            try:
                # Clean metadata
                for key in ["creation", "modified", "owner", "modified_by"]:
                    row.pop(key, None)

                doc = frappe.get_doc(row)
                doc.flags.ignore_permissions = True
                doc.insert()
                restored += 1
            except Exception as e:
                frappe.log_error(f"Restore error: {e}")

        frappe.db.commit()

        return {
            "cleared": current_count,
            "restored": restored
        }


# Usage
manager = ImportRecoveryManager("Customer")

# Import with recovery
import csv
with open("/path/to/customers.csv", "r") as f:
    data = list(csv.DictReader(f))

results = manager.import_with_recovery(data)

print(f"Success: {results['success']}, Failed: {results['failed']}")

# If something went wrong, rollback
if results["failed"] > 0:
    print("Rolling back created documents...")
    manager.rollback_created(results["created_docs"])

# Or full restore
# manager.restore_from_backup(results["backup"])
```

## Best Practices

1. **Always backup before large imports**
2. **Use transactions for atomic operations**
3. **Implement checkpoints for resumable imports**
4. **Log all operations for audit trail**
5. **Test rollback procedures before production use**

## Next Steps

- [Performance Optimization](../performance-optimization/performance-optimization.md)
- [Import Validation and Error Handling](../import-validation-error-handling/import-validation-error-handling.md)

---

*Last updated: 2026-02-04*
