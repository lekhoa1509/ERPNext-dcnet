"""Backfill workflow_state on docs that have an active Workflow but empty state.

Symptom: every time accountant opens a Sales Invoice / Phuong An Kinh Doanh
form, Frappe's `frappe.model.workflow.get_transitions` API call throws
HTTP 417 "WorkflowStateError: Workflow State not set" — because the doc's
`workflow_state` field is NULL/empty.

Root cause: bulk-INSERT migration paths (bulk_pump, sample seeds) submit docs
without setting `workflow_state`. Stock Frappe submit handler would set it from
workflow transitions; raw SQL INSERT bypasses that path.

Fix: per active Workflow, find the state where `doc_status='1'` (submitted)
and backfill `workflow_state` on every docstatus=1 row that's currently empty.
For docstatus=0 / docstatus=2, leave alone (those are draft / cancelled and
their state should match user intent).

Idempotent — second run finds 0 empty rows + no-op.
"""
from __future__ import annotations

import frappe


def execute():
	active_workflows = frappe.db.sql(
		"""SELECT name, document_type, workflow_state_field
		   FROM `tabWorkflow` WHERE is_active = 1""",
		as_dict=True,
	)
	total_backfilled = 0

	for wf in active_workflows:
		dt = wf.document_type
		state_field = wf.workflow_state_field or "workflow_state"

		if not frappe.db.has_column(dt, state_field):
			continue

		# Find the workflow state matching docstatus=1 ("submitted")
		submitted_state = frappe.db.get_value(
			"Workflow Document State",
			{"parent": wf.name, "doc_status": "1"},
			"state",
			order_by="idx ASC",  # prefer first defined submitted state
		)
		if not submitted_state:
			frappe.log_error(
				title=f"[backfill_workflow_state] No submitted state",
				message=f"Workflow {wf.name} ({dt}) has no state with doc_status=1; skipping.",
			)
			continue

		# Backfill submitted rows with empty state
		updated = frappe.db.sql(
			f"""UPDATE `tab{dt}` SET {state_field} = %s
			    WHERE docstatus = 1 AND ({state_field} IS NULL OR {state_field} = '')""",
			(submitted_state,),
		)
		# `cursor.rowcount` not exposed via frappe.db.sql; count affected rows separately
		count = frappe.db.sql(
			f"""SELECT COUNT(*) FROM `tab{dt}`
			    WHERE docstatus = 1 AND {state_field} = %s""",
			(submitted_state,),
			as_list=True,
		)[0][0]
		# We can't tell exactly how many WE updated vs were already set; report
		# the count of docstatus=1 rows now in the submitted state — useful for
		# eyeballing the patch effect in bench logs.
		print(f"[backfill_workflow_state] {dt}: {count} docstatus=1 rows now in state '{submitted_state}'")
		total_backfilled += count

	print(f"[backfill_workflow_state] DONE — total docstatus=1 rows synced: {total_backfilled}")
	frappe.db.commit()
