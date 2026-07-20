# API Reference: remove_db_aggregation.py

**Language**: Python

**Source**: `patches/v14_0/remove_db_aggregation.py`

---

## Functions

### execute()

Replace temporarily available Database Aggregate APIs on frappe (develop)

APIs changed:
        * frappe.db.max => frappe.qb.max
        * frappe.db.min => frappe.qb.min
        * frappe.db.sum => frappe.qb.sum
        * frappe.db.avg => frappe.qb.avg

**Returns**: (none)


