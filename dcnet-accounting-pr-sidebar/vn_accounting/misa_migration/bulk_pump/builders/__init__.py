"""Per-DocType dict builders for bulk_pump.

Each builder takes Misa source rows + Company context, returns dicts ready
for bulk_insert into the matching tab tables. No DB writes — pure data shape.
"""
