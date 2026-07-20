# API Reference: Bulk Operations Utilities

**Language**: Python

**Source**: `frappe/core/doctype/data_import/`

---

## Overview

Bulk operations utilities provide functions for handling large-scale data operations including batch processing, parallel imports, transaction management, and memory optimization.

## Batch Processing

### Batch Import Function

```python
import frappe
from frappe.core.doctype.data_import.importer import Importer

def batch_import(doctype, file_path, batch_size=500, commit_after_batch=True):
    """
    Import large files in batches.

    Args:
        doctype: Target DocType
        file_path: Path to import file
        batch_size: Records per batch
        commit_after_batch: Commit after each batch
    """
    importer = Importer(doctype, file_path=file_path)
    importer.import_file.parse_data_from_template()

    total = len(importer.import_file.data)
    processed = 0
    success = 0
    failed = 0

    for i in range(0, total, batch_size):
        batch = importer.import_file.data[i:i + batch_size]

        for row in batch:
            try:
                doc = row.parse_doc(doctype)
                frappe.get_doc(doc).insert()
                success += 1
            except Exception as e:
                failed += 1
                frappe.log_error(f"Row {row.index}: {e}")

            processed += 1

        if commit_after_batch:
            frappe.db.commit()

        # Progress update
        frappe.publish_realtime(
            "batch_import_progress",
            {"processed": processed, "total": total}
        )

    return {"success": success, "failed": failed, "total": total}
```

### Chunked Generator

```python
def chunked_import_generator(doctype, file_path, chunk_size=100):
    """
    Generator that yields import results in chunks.

    Useful for memory-efficient processing of large files.
    """
    from frappe.core.doctype.data_import.importer import ImportFile

    import_file = ImportFile(doctype, file_path)
    import_file.parse_data_from_template()

    for doc, rows, indexes in import_file.get_payloads_for_import():
        yield {
            "doc": doc,
            "rows": rows,
            "indexes": indexes
        }

# Usage
for chunk in chunked_import_generator("Customer", "/path/to/file.csv"):
    process_document(chunk["doc"])
```

## Bulk Insert

### Direct Database Insert

```python
import frappe

def bulk_insert_customers(customers: list, batch_size=100):
    """
    Bulk insert using direct database operations.

    WARNING: Bypasses validations and hooks.
    Use only for trusted data.
    """
    from frappe.utils import now

    for i in range(0, len(customers), batch_size):
        batch = customers[i:i + batch_size]

        values = []
        for cust in batch:
            values.append({
                "name": frappe.generate_hash("Customer", 10),
                "doctype": "Customer",
                "customer_name": cust.get("customer_name"),
                "customer_type": cust.get("customer_type", "Company"),
                "territory": cust.get("territory", "All Territories"),
                "creation": now(),
                "modified": now(),
                "owner": frappe.session.user,
                "modified_by": frappe.session.user
            })

        # Bulk insert
        frappe.db.bulk_insert("Customer", values, ignore_duplicates=True)

    frappe.db.commit()
```

### Bulk Insert with frappe.db

```python
import frappe

def bulk_insert_items(items: list):
    """
    Use frappe's bulk_insert for efficient insertion.
    """
    fields = ["name", "item_code", "item_name", "item_group", "stock_uom"]
    values = []

    for item in items:
        values.append([
            item.get("item_code"),  # name
            item.get("item_code"),
            item.get("item_name"),
            item.get("item_group", "All Item Groups"),
            item.get("stock_uom", "Nos")
        ])

    # Bulk insert
    frappe.db.bulk_insert(
        "Item",
        fields=fields,
        values=values,
        ignore_duplicates=True,
        chunk_size=500
    )

    frappe.db.commit()
```

## Bulk Update

### Batch Update Records

```python
import frappe

def bulk_update_territory(old_territory, new_territory, batch_size=100):
    """
    Bulk update territory for all customers.
    """
    customers = frappe.get_all(
        "Customer",
        filters={"territory": old_territory},
        pluck="name"
    )

    for i in range(0, len(customers), batch_size):
        batch = customers[i:i + batch_size]

        frappe.db.sql("""
            UPDATE `tabCustomer`
            SET territory = %s, modified = NOW()
            WHERE name IN %s
        """, (new_territory, batch))

        frappe.db.commit()

    return len(customers)
```

### Bulk Update via Data Import

```python
import frappe

def update_via_import(doctype, updates: list):
    """
    Use Data Import for bulk updates.

    Args:
        doctype: Target DocType
        updates: List of dicts with 'name' and fields to update
    """
    import csv
    from io import StringIO

    # Build CSV
    if not updates:
        return

    fields = list(updates[0].keys())
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(fields)

    for update in updates:
        writer.writerow([update.get(f, "") for f in fields])

    # Create temp file
    content = output.getvalue()
    file_doc = frappe.get_doc({
        "doctype": "File",
        "file_name": "bulk_update.csv",
        "content": content,
        "is_private": 1
    }).insert()

    # Create and run import
    data_import = frappe.new_doc("Data Import")
    data_import.reference_doctype = doctype
    data_import.import_type = "Update Existing Records"
    data_import.import_file = file_doc.file_url
    data_import.insert()
    data_import.start_import()

    return data_import.name
```

## Bulk Delete

### Safe Bulk Delete

```python
import frappe

def bulk_delete(doctype, filters, batch_size=100):
    """
    Bulk delete with proper cleanup.
    """
    records = frappe.get_all(doctype, filters=filters, pluck="name")

    deleted = 0
    for i in range(0, len(records), batch_size):
        batch = records[i:i + batch_size]

        for name in batch:
            try:
                frappe.delete_doc(doctype, name, force=True)
                deleted += 1
            except Exception as e:
                frappe.log_error(f"Failed to delete {doctype} {name}: {e}")

        frappe.db.commit()

    return deleted
```

### Fast Bulk Delete (Direct SQL)

```python
import frappe

def fast_bulk_delete(doctype, filters):
    """
    Fast delete using direct SQL.

    WARNING: Bypasses hooks and linked documents.
    """
    # Get record names
    records = frappe.get_all(doctype, filters=filters, pluck="name")

    if not records:
        return 0

    # Delete child tables first
    meta = frappe.get_meta(doctype)
    for df in meta.get_table_fields():
        frappe.db.sql(f"""
            DELETE FROM `tab{df.options}`
            WHERE parent IN %s
        """, [records])

    # Delete main records
    frappe.db.sql(f"""
        DELETE FROM `tab{doctype}`
        WHERE name IN %s
    """, [records])

    # Delete related File attachments
    frappe.db.sql("""
        DELETE FROM `tabFile`
        WHERE attached_to_doctype = %s
        AND attached_to_name IN %s
    """, (doctype, records))

    frappe.db.commit()

    return len(records)
```

## Transaction Management

### Transaction Wrapper

```python
import frappe
from contextlib import contextmanager

@contextmanager
def bulk_transaction(auto_commit=True, savepoint=True):
    """
    Context manager for bulk operations.
    """
    if savepoint:
        frappe.db.savepoint("bulk_op")

    try:
        yield

        if auto_commit:
            frappe.db.commit()
    except Exception:
        if savepoint:
            frappe.db.rollback(save_point="bulk_op")
        raise

# Usage
with bulk_transaction():
    for item in items:
        frappe.get_doc(item).insert()
```

### Savepoint Management

```python
import frappe

def import_with_savepoints(records, batch_size=50):
    """
    Import with savepoints for partial rollback.
    """
    success_batches = []
    failed_batches = []

    for i in range(0, len(records), batch_size):
        batch_num = i // batch_size
        batch = records[i:i + batch_size]

        frappe.db.savepoint(f"batch_{batch_num}")

        try:
            for record in batch:
                frappe.get_doc(record).insert()
            success_batches.append(batch_num)
        except Exception as e:
            frappe.db.rollback(save_point=f"batch_{batch_num}")
            failed_batches.append({"batch": batch_num, "error": str(e)})

    frappe.db.commit()

    return {
        "success_batches": success_batches,
        "failed_batches": failed_batches
    }
```

## Memory Optimization

### Streaming Large Files

```python
def stream_csv_import(doctype, file_path, process_func):
    """
    Stream CSV file for memory-efficient processing.
    """
    import csv

    with open(file_path, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)

        batch = []
        for row in reader:
            batch.append(row)

            if len(batch) >= 100:
                process_func(doctype, batch)
                batch = []
                # Force garbage collection
                import gc
                gc.collect()

        # Process remaining
        if batch:
            process_func(doctype, batch)
```

### Clear Locals After Processing

```python
import frappe

def process_with_cleanup(records):
    """
    Process records with periodic cache cleanup.
    """
    for i, record in enumerate(records):
        frappe.get_doc(record).insert()

        # Clear caches every 100 records
        if i % 100 == 0:
            frappe.local.doc_cache = {}
            frappe.db.commit()
```

## Parallel Processing

### Multi-threaded Import

```python
from concurrent.futures import ThreadPoolExecutor, as_completed
import frappe

def parallel_import(doctype, records, max_workers=4):
    """
    Import records in parallel using thread pool.

    Note: Each thread needs its own database connection.
    """
    def import_record(record):
        # Each thread needs to connect
        frappe.connect()
        try:
            doc = frappe.get_doc(record)
            doc.insert()
            frappe.db.commit()
            return {"success": True, "name": doc.name}
        except Exception as e:
            return {"success": False, "error": str(e)}
        finally:
            frappe.db.close()

    results = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(import_record, r): r for r in records}

        for future in as_completed(futures):
            results.append(future.result())

    return results
```

### Queue-based Parallel Import

```python
import frappe

def queue_parallel_import(doctype, file_path, num_jobs=4):
    """
    Split file into parts and queue parallel jobs.
    """
    import csv

    with open(file_path, "r") as f:
        reader = list(csv.DictReader(f))

    chunk_size = len(reader) // num_jobs
    job_ids = []

    for i in range(num_jobs):
        start = i * chunk_size
        end = start + chunk_size if i < num_jobs - 1 else len(reader)
        chunk = reader[start:end]

        job = frappe.enqueue(
            import_chunk,
            queue="long",
            doctype=doctype,
            records=chunk
        )
        job_ids.append(job.id)

    return job_ids

def import_chunk(doctype, records):
    """Process a chunk of records."""
    for record in records:
        record["doctype"] = doctype
        frappe.get_doc(record).insert()
    frappe.db.commit()
```

## Usage Example

### Complete Bulk Import with All Features

```python
import frappe

def full_bulk_import(doctype, file_path, options=None):
    """
    Complete bulk import with all optimizations.
    """
    options = options or {}
    batch_size = options.get("batch_size", 500)
    parallel = options.get("parallel", False)
    validate = options.get("validate", True)

    results = {
        "success": 0,
        "failed": 0,
        "errors": []
    }

    # Parse file
    from frappe.core.doctype.data_import.importer import ImportFile
    import_file = ImportFile(doctype, file_path)
    import_file.parse_data_from_template()

    # Validate if needed
    if validate:
        for warning in import_file.get_warnings():
            if warning.get("level") == "error":
                results["errors"].append(warning)

        if results["errors"]:
            return results

    # Process in batches
    data = list(import_file.get_payloads_for_import())

    with bulk_transaction(auto_commit=False):
        for i in range(0, len(data), batch_size):
            batch = data[i:i + batch_size]

            for doc, rows, indexes in batch:
                try:
                    frappe.get_doc(doc).insert()
                    results["success"] += 1
                except Exception as e:
                    results["failed"] += 1
                    results["errors"].append({
                        "rows": indexes,
                        "error": str(e)
                    })

            # Commit batch
            frappe.db.commit()

            # Progress
            frappe.publish_realtime(
                "bulk_import_progress",
                {"processed": i + len(batch), "total": len(data)}
            )

    return results
```

## Related References

- [Background Jobs](background_jobs.md) - Async processing
- [Error Handling](error_handling.md) - Error management
- [Importer](importer.md) - Core import class

---

*Source: frappe/core/doctype/data_import/ | Last updated: 2026-02-04*
