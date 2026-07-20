# How To: Performance Optimization for Large Imports

**Difficulty**: Advanced
**Estimated Time**: 45 minutes
**Tags**: performance, optimization, large-data

## Overview

Learn techniques to optimize import performance for large datasets (10,000+ records). Covers database optimization, memory management, and parallel processing.

## Prerequisites

- Understanding of Frappe architecture
- Database administration basics
- Python performance concepts

## Performance Techniques

### 1. Batch Processing

```python
import frappe

def optimized_batch_import(doctype, data, batch_size=500):
    """
    Import with optimized batch processing.
    """
    total = len(data)
    success = 0
    failed = 0

    for i in range(0, total, batch_size):
        batch = data[i:i + batch_size]

        # Start transaction
        frappe.db.begin()

        try:
            for row in batch:
                row["doctype"] = doctype
                doc = frappe.get_doc(row)
                doc.flags.ignore_permissions = True
                doc.flags.ignore_links = True
                doc.insert()
                success += 1

            # Commit batch
            frappe.db.commit()

            # Clear cache
            frappe.local.doc_cache = {}

        except Exception as e:
            frappe.db.rollback()
            failed += len(batch)
            frappe.log_error(f"Batch {i//batch_size} failed: {e}")

        # Report progress
        print(f"Processed {min(i + batch_size, total)}/{total}")

    return {"success": success, "failed": failed}
```

### 2. Disable Unnecessary Hooks

```python
def fast_import(doctype, data):
    """
    Import with hooks disabled for speed.
    """
    for row in data:
        row["doctype"] = doctype
        doc = frappe.get_doc(row)

        # Disable various checks
        doc.flags.ignore_permissions = True
        doc.flags.ignore_links = True
        doc.flags.ignore_validate = True
        doc.flags.ignore_mandatory = True

        # Skip controller methods
        doc.flags.ignore_before_insert = True

        doc.insert()

    frappe.db.commit()
```

### 3. Bulk Database Insert

```python
import frappe

def bulk_insert_direct(doctype, records, batch_size=1000):
    """
    Direct bulk insert to database (bypasses ORM).

    WARNING: Skips all validations and hooks.
    Use only for trusted data.
    """
    meta = frappe.get_meta(doctype)
    fields = [df.fieldname for df in meta.fields if df.fieldtype not in ["Table", "Table MultiSelect"]]
    fields.extend(["name", "creation", "modified", "owner", "modified_by", "docstatus"])

    now = frappe.utils.now()
    user = frappe.session.user

    for i in range(0, len(records), batch_size):
        batch = records[i:i + batch_size]

        values = []
        for record in batch:
            row = [record.get(f, None) for f in fields[:-6]]
            row.extend([
                record.get("name") or frappe.generate_hash(doctype, 10),
                now, now, user, user, 0
            ])
            values.append(row)

        # Bulk insert
        frappe.db.bulk_insert(doctype, fields, values, ignore_duplicates=True)

    frappe.db.commit()
```

### 4. Memory Optimization

```python
import gc
import frappe

def memory_efficient_import(doctype, file_path, chunk_size=100):
    """
    Import with minimal memory footprint.
    """
    import csv

    with open(file_path, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)

        chunk = []
        for row in reader:
            chunk.append(row)

            if len(chunk) >= chunk_size:
                process_chunk(doctype, chunk)
                chunk = []

                # Clear memory
                frappe.local.doc_cache = {}
                gc.collect()

        # Process remaining
        if chunk:
            process_chunk(doctype, chunk)

def process_chunk(doctype, chunk):
    """Process a chunk of records."""
    for row in chunk:
        row["doctype"] = doctype
        doc = frappe.get_doc(row)
        doc.flags.ignore_permissions = True
        doc.insert()

    frappe.db.commit()
```

### 5. Index Optimization

```python
def optimize_for_import(doctype):
    """
    Optimize database indexes before large import.
    """
    # Temporarily disable foreign key checks
    frappe.db.sql("SET FOREIGN_KEY_CHECKS = 0")

    # Disable index updates (MySQL)
    frappe.db.sql(f"ALTER TABLE `tab{doctype}` DISABLE KEYS")

    return lambda: restore_after_import(doctype)

def restore_after_import(doctype):
    """Restore indexes after import."""
    frappe.db.sql(f"ALTER TABLE `tab{doctype}` ENABLE KEYS")
    frappe.db.sql("SET FOREIGN_KEY_CHECKS = 1")
    frappe.db.commit()
```

### 6. Parallel Processing

```python
from concurrent.futures import ProcessPoolExecutor
import frappe

def parallel_import(doctype, file_path, num_workers=4):
    """
    Import using multiple processes.
    """
    import csv

    with open(file_path, "r") as f:
        reader = list(csv.DictReader(f))

    chunk_size = len(reader) // num_workers
    chunks = [
        reader[i:i + chunk_size]
        for i in range(0, len(reader), chunk_size)
    ]

    # Process in parallel
    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        results = list(executor.map(
            import_chunk_worker,
            [(doctype, chunk, i) for i, chunk in enumerate(chunks)]
        ))

    return results

def import_chunk_worker(args):
    """Worker function for parallel import."""
    doctype, chunk, chunk_id = args

    # Initialize Frappe in worker
    frappe.init(site="your_site")
    frappe.connect()

    try:
        success = 0
        for row in chunk:
            row["doctype"] = doctype
            doc = frappe.get_doc(row)
            doc.insert()
            success += 1

        frappe.db.commit()
        return {"chunk": chunk_id, "success": success}
    finally:
        frappe.destroy()
```

### 7. Disable Realtime Updates

```python
def import_without_realtime(doctype, data):
    """
    Import without triggering realtime updates.
    """
    # Disable realtime
    frappe.flags.in_import = True

    try:
        for row in data:
            row["doctype"] = doctype
            doc = frappe.get_doc(row)
            doc.insert()

        frappe.db.commit()
    finally:
        frappe.flags.in_import = False
```

### 8. Use Raw SQL for Lookups

```python
def fast_link_validation(doctype, link_field, values):
    """
    Fast validation of link field values using single query.
    """
    if not values:
        return set()

    link_doctype = frappe.get_meta(doctype).get_field(link_field).options

    # Single query for all values
    existing = frappe.db.sql("""
        SELECT name FROM `tab{doctype}`
        WHERE name IN ({placeholders})
    """.format(
        doctype=link_doctype,
        placeholders=", ".join(["%s"] * len(values))
    ), values, as_dict=False)

    return {row[0] for row in existing}
```

## Complete Optimized Importer

```python
import frappe
import gc
from contextlib import contextmanager

class OptimizedImporter:
    """
    High-performance data importer.
    """

    def __init__(self, doctype):
        self.doctype = doctype
        self.batch_size = 500
        self.results = {"success": 0, "failed": 0, "errors": []}

    @contextmanager
    def optimization_context(self):
        """Context manager for import optimizations."""
        # Store original values
        original_in_import = frappe.flags.get("in_import")

        # Apply optimizations
        frappe.flags.in_import = True

        try:
            yield
        finally:
            # Restore
            frappe.flags.in_import = original_in_import
            frappe.local.doc_cache = {}
            gc.collect()

    def preload_link_values(self, data, link_fields):
        """
        Pre-validate all link field values.
        """
        self.valid_links = {}

        for field, link_doctype in link_fields.items():
            # Collect all unique values
            values = list(set(
                row.get(field) for row in data
                if row.get(field)
            ))

            if values:
                # Single query
                existing = frappe.db.sql("""
                    SELECT name FROM `tab{doctype}`
                    WHERE name IN ({placeholders})
                """.format(
                    doctype=link_doctype,
                    placeholders=", ".join(["%s"] * len(values))
                ), values, pluck="name")

                self.valid_links[field] = set(existing)

    def validate_row(self, row):
        """Fast row validation."""
        for field, valid_values in self.valid_links.items():
            value = row.get(field)
            if value and value not in valid_values:
                return False, f"Invalid {field}: {value}"
        return True, None

    def import_data(self, data, skip_validation=False):
        """
        Run optimized import.
        """
        with self.optimization_context():
            # Pre-validate links
            meta = frappe.get_meta(self.doctype)
            link_fields = {
                df.fieldname: df.options
                for df in meta.fields
                if df.fieldtype == "Link"
            }

            if not skip_validation:
                self.preload_link_values(data, link_fields)

            # Process in batches
            for i in range(0, len(data), self.batch_size):
                batch = data[i:i + self.batch_size]
                self.process_batch(batch, skip_validation)

                # Progress
                progress = min(i + self.batch_size, len(data))
                print(f"Processed {progress}/{len(data)}")

        return self.results

    def process_batch(self, batch, skip_validation):
        """Process a single batch."""
        frappe.db.begin()

        try:
            for row in batch:
                # Quick validation
                if not skip_validation:
                    valid, error = self.validate_row(row)
                    if not valid:
                        self.results["failed"] += 1
                        self.results["errors"].append(error)
                        continue

                # Create document
                row["doctype"] = self.doctype
                doc = frappe.get_doc(row)

                # Set flags for speed
                doc.flags.ignore_permissions = True
                doc.flags.ignore_links = True

                doc.insert()
                self.results["success"] += 1

            frappe.db.commit()

        except Exception as e:
            frappe.db.rollback()
            self.results["failed"] += len(batch)
            self.results["errors"].append(str(e))

        # Clear cache after batch
        frappe.local.doc_cache = {}


# Usage
importer = OptimizedImporter("Customer")
importer.batch_size = 1000

import csv
with open("/path/to/customers.csv", "r") as f:
    data = list(csv.DictReader(f))

results = importer.import_data(data)
print(f"Success: {results['success']}, Failed: {results['failed']}")
```

## Benchmarking

```python
import time
import frappe

def benchmark_import(doctype, data, method_name, import_func):
    """
    Benchmark import performance.
    """
    start = time.time()
    result = import_func(doctype, data)
    elapsed = time.time() - start

    records_per_second = len(data) / elapsed if elapsed > 0 else 0

    print(f"\n{method_name}:")
    print(f"  Total records: {len(data)}")
    print(f"  Time: {elapsed:.2f}s")
    print(f"  Speed: {records_per_second:.1f} records/sec")

    return {
        "method": method_name,
        "records": len(data),
        "time": elapsed,
        "speed": records_per_second
    }

# Compare methods
methods = [
    ("Standard Import", standard_import),
    ("Batch Import", optimized_batch_import),
    ("Bulk Insert", bulk_insert_direct),
]

results = []
for name, func in methods:
    # Reset between tests
    frappe.db.sql(f"DELETE FROM `tabTest DocType`")
    frappe.db.commit()

    result = benchmark_import("Test DocType", test_data, name, func)
    results.append(result)

# Print comparison
print("\n" + "="*50)
print("Performance Comparison")
print("="*50)
for r in results:
    print(f"{r['method']}: {r['speed']:.1f} rec/s")
```

## Performance Tips Summary

| Technique | Speedup | Use Case |
|-----------|---------|----------|
| Batch processing | 2-3x | All imports |
| Disable hooks | 3-5x | Trusted data |
| Bulk insert | 10-20x | Simple DocTypes |
| Parallel processing | 2-4x | Large files |
| Pre-validate links | 2-3x | Many Link fields |
| Memory cleanup | N/A | Very large files |

## Next Steps

- [Rollback and Recovery](../rollback-recovery/rollback-recovery.md)
- [Import Validation and Error Handling](../import-validation-error-handling/import-validation-error-handling.md)

---

*Last updated: 2026-02-04*
