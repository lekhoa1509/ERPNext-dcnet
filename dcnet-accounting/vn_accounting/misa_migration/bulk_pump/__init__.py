"""SQL-pump Misa migration backend.

Alternative to the doc-first ORM path in ``misa_migration/importers/``.
Same input (Misa Migration Row + raw_payload), same final DB shape
(tabSales Invoice + Items + Taxes + Payment Schedule + GL Entry +
Customer balance), different write strategy: pre-compute everything
in memory, then bulk INSERT via raw SQL — bypasses ERPNext ORM's
per-doc validate / hooks / commit cycle.

Target speedup: 10-15x vs ORM path. Trade-off: any validate rule we
need to enforce must be replicated here (Misa source is assumed clean).

Suitable for: archival migration of CLOSED historical periods.
NOT suitable for: live carry-forward where ERPNext lifecycle hooks
must fire (e.g. dunning trigger on overdue SI).
"""
