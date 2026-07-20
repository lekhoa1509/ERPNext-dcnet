# PAKD commission_lines pivot — implementation plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the 48-row vertical `commission_lines` child table on the PAKD form with a horizontal pivot grid + click-to-popover with status-aware actions (FB-2026-00587). All 3 PAKD types supported. Per-line rate override + per-cell skip + per-cell post (in addition to existing period-bundle post).

**Architecture:** HTML field rendered by JS in-form (matches existing `summary_card` pattern in same file). Engine unchanged; per-line override applied as a ratio inside `_sync_commission_lines` after engine returns. 5 new whitelisted API endpoints in `api.py`. Per-cell JE shape = 2 legs (DR component / CR counter) via new `post_journal_entry_single` helper. Period-bundle JE shape unchanged.

**Tech Stack:** Frappe v16.12, Python 3.14, MariaDB. Frappe Dialog for popover, native `position: sticky` CSS for grid, `frappe.call` for API.

**Working location:** `/home/long/long/frappe-bench-dcnet/apps/dcnet_pakd/` on `develop` branch (currently 9 commits ahead of dcnet/develop, NOT pushed).

**Spec reference:** `apps/dcnet_pakd/docs/specs/2026-05-13-pakd-commission-pivot-design.md` (commit `cce0303`).

---

## Task 1: Data model — extend PAKD Commission Line DocType

**Files:**
- Modify: `dcnet_pakd/dcnet_pakd/doctype/pakd_commission_line/pakd_commission_line.json`
- Create: `dcnet_pakd/patches/v0_2_0/add_commission_line_skipped_state.py`
- Modify: `dcnet_pakd/patches.txt`

- [ ] **Step 1.1: Edit `pakd_commission_line.json` — add `Skipped` option + 3 new fields**

Extend the `state` Select options and add `override_rate`, `posted_by_cell`, `skip_reason` to `field_order` + `fields`. Bump `modified` timestamp to today.

Add to `field_order` (after existing entries):
```
"override_rate",
"posted_by_cell",
"skip_reason"
```

Change the `state` field options from `"Pending\nPosted\nCancelled"` to `"Pending\nPosted\nCancelled\nSkipped"`.

Append to `fields` array (before closing `]`):
```json
{
    "fieldname": "override_rate",
    "fieldtype": "Percent",
    "label": "Tỷ lệ override dòng",
    "precision": "2",
    "description": "Để trống = dùng tỷ lệ PAKD-wide hoặc mẫu. Chỉ dùng cho 1 dòng này."
},
{
    "fieldname": "posted_by_cell",
    "fieldtype": "Check",
    "label": "Đăng theo cell",
    "default": "0",
    "description": "1 = JE được tạo bằng nút 'Chỉ đăng dòng này' (2 legs cho 1 component); 0 = JE gộp toàn kỳ."
},
{
    "fieldname": "skip_reason",
    "fieldtype": "Small Text",
    "label": "Lý do bỏ qua",
    "depends_on": "eval:doc.state==\"Skipped\""
}
```

Bump `"modified": "2026-05-13 12:00:00.000000"` to a later timestamp (e.g. `"2026-05-13 15:00:00.000000"`) so Frappe sees the schema change.

- [ ] **Step 1.2: Create the patch**

Path: `dcnet_pakd/patches/v0_2_0/add_commission_line_skipped_state.py`

```python
"""Reload PAKD Commission Line so the new state option + override_rate +
posted_by_cell + skip_reason fields are in meta before any code reads them.
Idempotent — reload_doc is safe to repeat."""

import frappe


def execute():
	frappe.reload_doc("dcnet_pakd", "doctype", "pakd_commission_line", force=True)
```

- [ ] **Step 1.3: Register patch in `patches.txt`**

Append a new line at end of `dcnet_pakd/patches.txt`:
```
dcnet_pakd.patches.v0_2_0.add_commission_line_skipped_state
```

- [ ] **Step 1.4: Run migrate + verify field meta**

```bash
cd /home/long/long/frappe-bench-dcnet
bench --site dcnet.localhost migrate 2>&1 | tail -10
```

Expected: ends with "Queued rebuilding of search index" (no errors).

Verify with:
```bash
env/bin/python -c "
import frappe
frappe.init(site='dcnet.localhost', sites_path='sites')
frappe.connect()
m = frappe.get_meta('PAKD Commission Line')
print('state opts:', m.get_field('state').options.split('\n'))
print('override_rate:', m.get_field('override_rate').fieldtype if m.get_field('override_rate') else 'MISSING')
print('posted_by_cell:', m.get_field('posted_by_cell').fieldtype if m.get_field('posted_by_cell') else 'MISSING')
print('skip_reason:', m.get_field('skip_reason').fieldtype if m.get_field('skip_reason') else 'MISSING')
"
```

Expected output:
```
state opts: ['Pending', 'Posted', 'Cancelled', 'Skipped']
override_rate: Percent
posted_by_cell: Check
skip_reason: Small Text
```

- [ ] **Step 1.5: Commit**

```bash
cd /home/long/long/frappe-bench-dcnet/apps/dcnet_pakd
git add dcnet_pakd/dcnet_pakd/doctype/pakd_commission_line/pakd_commission_line.json \
        dcnet_pakd/patches/v0_2_0/add_commission_line_skipped_state.py \
        dcnet_pakd/patches.txt
git commit -m "$(cat <<'EOF'
feat(pakd): extend PAKD Commission Line — Skipped state + override_rate + skip_reason

Adds per-line override_rate (Percent), posted_by_cell (Check),
skip_reason (Small Text), and extends state Select to include Skipped.
Patch v0_2_0 reload_doc-s the DocType so meta picks up the new fields.

Part of the commission pivot redesign (FB-2026-00587).

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 2: Engine sync — respect Skipped/Cancelled + apply per-line rescale

**Files:**
- Modify: `dcnet_pakd/dcnet_pakd/doctype/phuong_an_kinh_doanh/phuong_an_kinh_doanh.py` (function `_sync_commission_lines` around line 210)
- Modify: `dcnet_pakd/tests/test_engine.py` (extend with new test class)

- [ ] **Step 2.1: Read current `_sync_commission_lines` to confirm structure**

Already known (lines 210-279):
- Builds `needed: dict[(period_idx, comp_name), amount]` from `self.total_*` per period
- Walks `self.commission_lines`: Posted preserved + popped from needed; Pending updated-in-place if key in needed; otherwise dropped; Cancelled preserved
- Appends remaining needed as new Pending rows

Two changes needed:
1. Also preserve Skipped rows AND pop their key from needed (so we don't recreate a Pending alongside Skipped)
2. After the existing append loop, run a per-line rescale step for Pending lines with override_rate

- [ ] **Step 2.2: Edit `_sync_commission_lines`**

Replace the existing `else: # Cancelled or other states` branch and add the rescale step at the end. Replace this block:

```python
		# Walk existing rows: keep Posted unconditionally, update Pending in place,
		# drop Pending rows whose (period, component) is no longer needed.
		keep_rows = []
		for row in list(self.commission_lines or []):
			key = (row.billing_schedule_idx, row.component)
			if row.state == "Posted":
				needed.pop(key, None)
				keep_rows.append(row)
			elif row.state == "Pending":
				if key in needed:
					row.amount = needed.pop(key)
					keep_rows.append(row)
				# else: drop — period/component no longer needed
			else:
				# Cancelled or other states — preserve as-is
				keep_rows.append(row)

		self.commission_lines = []
		for row in keep_rows:
			self.append("commission_lines", row.as_dict())

		# Append remaining needed (new periods or new components)
		for (period_idx, comp_name), amount in needed.items():
			self.append("commission_lines", {
				"billing_schedule_idx": period_idx,
				"component": comp_name,
				"amount": amount,
				"state": "Pending",
			})
```

With:

```python
		# Walk existing rows: keep Posted/Skipped/Cancelled unconditionally and
		# pop their (period, component) key from `needed` so we never recreate
		# a Pending row alongside a user-decided final state. Update Pending in
		# place; drop Pending rows whose key is no longer in `needed`.
		FINAL_STATES = ("Posted", "Skipped", "Cancelled")
		keep_rows = []
		for row in list(self.commission_lines or []):
			key = (row.billing_schedule_idx, row.component)
			if row.state in FINAL_STATES:
				needed.pop(key, None)
				keep_rows.append(row)
			elif row.state == "Pending":
				if key in needed:
					row.amount = needed.pop(key)
					keep_rows.append(row)
				# else: drop — period/component no longer needed
			else:
				# Unknown future state — preserve as-is to be safe
				keep_rows.append(row)

		self.commission_lines = []
		for row in keep_rows:
			self.append("commission_lines", row.as_dict())

		# Append remaining needed (new periods or new components)
		for (period_idx, comp_name), amount in needed.items():
			self.append("commission_lines", {
				"billing_schedule_idx": period_idx,
				"component": comp_name,
				"amount": amount,
				"state": "Pending",
			})

		# Per-line override rescale: walk Pending lines with override_rate set,
		# rescale amount by ratio (line.override_rate / upstream_rate).
		# upstream_rate = pakd_override_map.get(component) or template_rate(component).
		# Engine already applied upstream_rate when computing self.total_*; this
		# rescale is the diff layer for individual-line overrides.
		pakd_override_map = {
			r.component: float(r.override_rate or 0)
			for r in (self.commission_overrides or [])
		}
		rule = self._get_rule()
		template_rate_map = {}
		if rule:
			template_rate_map = {
				c.component_name: float(c.rate or 0)
				for c in rule.get("components", [])
			}

		for row in self.commission_lines or []:
			if row.state != "Pending":
				continue
			line_override = float(row.override_rate or 0)
			if not line_override:
				continue
			upstream_rate = (
				pakd_override_map.get(row.component)
				or template_rate_map.get(row.component)
				or 0
			)
			if not upstream_rate:
				continue
			row.amount = round(float(row.amount or 0) * line_override / upstream_rate)
```

- [ ] **Step 2.3: Add tests to `tests/test_engine.py`**

The current test file uses pure Python (no Frappe). The sync function is on the controller class, which needs Frappe. Add a new file `tests/test_sync_commission_lines.py` for tests that exercise the controller. Steps below.

Wait — actually tests for `_sync_commission_lines` need `frappe.init()` + DB. For speed and isolation, write them as a separate file that uses live DB but creates a transient PAKD. We have `tests/test_chains_b_c.py` as precedent.

- [ ] **Step 2.4: Create `tests/test_sync_commission_lines.py`**

Path: `apps/dcnet_pakd/dcnet_pakd/tests/test_sync_commission_lines.py`

```python
"""Tests for PAKD _sync_commission_lines override rescale + Skipped/Cancelled preservation.

Run from bench root with `env/bin/python -m unittest dcnet_pakd.tests.test_sync_commission_lines -v`.
"""

import unittest

import frappe


class TestSyncCommissionLines(unittest.TestCase):
	"""End-to-end exercising of _sync_commission_lines via a real PAKD doc.

	Uses an existing draft PAKD (PAKD-2026-00006) and rolls back state at end of each test.
	"""

	PAKD = "PAKD-2026-00006"

	@classmethod
	def setUpClass(cls):
		frappe.set_user("Administrator")

	def setUp(self):
		# Snapshot the current commission_lines state so we can restore
		doc = frappe.get_doc("Phuong An Kinh Doanh", self.PAKD)
		self._snapshot = [
			(l.name, l.state, l.amount, l.override_rate, l.skip_reason)
			for l in doc.commission_lines
		]

	def tearDown(self):
		# Restore state of every snapshotted line
		for name, state, amount, override_rate, skip_reason in self._snapshot:
			if not frappe.db.exists("PAKD Commission Line", name):
				continue
			frappe.db.set_value(
				"PAKD Commission Line",
				name,
				{
					"state": state,
					"amount": amount,
					"override_rate": override_rate or 0,
					"skip_reason": skip_reason or "",
				},
				update_modified=False,
			)
		frappe.db.commit()

	def _line_for(self, doc, component):
		for l in doc.commission_lines:
			if l.component == component and l.state == "Pending":
				return l
		raise AssertionError(f"No Pending line found for component={component}")

	def test_per_line_override_rescales_amount(self):
		"""line.amount=1500 at upstream 10% → set line.override_rate=5 → after save, line.amount=750."""
		doc = frappe.get_doc("Phuong An Kinh Doanh", self.PAKD)
		ms = self._line_for(doc, "Manager Services")
		original_amount = ms.amount

		ms.override_rate = 5.0
		doc.save(ignore_permissions=True)

		doc.reload()
		ms_after = next(l for l in doc.commission_lines if l.name == ms.name)
		# Template MS rate is 10%; rescale = original × (5/10) = original / 2
		self.assertEqual(ms_after.amount, round(original_amount * 5 / 10))

	def test_blank_line_override_falls_through(self):
		"""line.override_rate=0 (default) → no rescale."""
		doc = frappe.get_doc("Phuong An Kinh Doanh", self.PAKD)
		ms = self._line_for(doc, "Manager Services")
		ms.override_rate = 0
		doc.save(ignore_permissions=True)

		doc.reload()
		ms_after = next(l for l in doc.commission_lines if l.name == ms.name)
		# Amount should be the canonical engine-derived value
		self.assertEqual(ms_after.amount, doc.total_manager_services or 1500)

	def test_skipped_lines_preserved_on_resync(self):
		"""line in Skipped state stays Skipped + amount preserved; no Pending duplicate appended."""
		doc = frappe.get_doc("Phuong An Kinh Doanh", self.PAKD)
		ms = self._line_for(doc, "Manager Services")
		ms.state = "Skipped"
		ms.skip_reason = "Test: kỳ này bỏ qua"
		original_amount = ms.amount
		doc.save(ignore_permissions=True)

		doc.reload()
		# Same line still Skipped + amount unchanged
		ms_after = next(l for l in doc.commission_lines if l.name == ms.name)
		self.assertEqual(ms_after.state, "Skipped")
		self.assertEqual(ms_after.amount, original_amount)
		# No duplicate Pending for same (period, component)
		dupes = [
			l for l in doc.commission_lines
			if l.component == "Manager Services"
			and l.billing_schedule_idx == ms_after.billing_schedule_idx
			and l.state == "Pending"
		]
		self.assertEqual(dupes, [])


if __name__ == "__main__":
	unittest.main()
```

- [ ] **Step 2.5: Run tests**

```bash
cd /home/long/long/frappe-bench-dcnet
env/bin/python -m unittest dcnet_pakd.tests.test_sync_commission_lines -v 2>&1 | tail -15
```

Expected:
```
test_blank_line_override_falls_through (...) ... ok
test_per_line_override_rescales_amount (...) ... ok
test_skipped_lines_preserved_on_resync (...) ... ok

----------------------------------------------------------------------
Ran 3 tests in <Xs>

OK
```

If a test fails because the test PAKD's contract billing schedule doesn't have a "Manager Services" Pending line, adjust the test to use a component that does (check `PAKD-2026-00006` state first via `bench --site dcnet.localhost console`).

- [ ] **Step 2.6: Commit**

```bash
cd /home/long/long/frappe-bench-dcnet/apps/dcnet_pakd
git add dcnet_pakd/dcnet_pakd/doctype/phuong_an_kinh_doanh/phuong_an_kinh_doanh.py \
        dcnet_pakd/tests/test_sync_commission_lines.py
git commit -m "$(cat <<'EOF'
feat(pakd): engine sync honors Skipped/Cancelled + applies per-line override rescale

_sync_commission_lines now:
- Preserves Skipped + Cancelled rows AND pops their (period, component) key
  from needed so it doesn't recreate a Pending duplicate alongside the
  user's final-state decision.
- After the canonical engine-derived amounts settle, walks Pending lines
  with override_rate set and rescales by the ratio
  (line.override_rate / upstream_rate) where upstream_rate is the
  PAKD-wide override or the rule template rate.

Tests cover per-line rescale (5% on a 10% template halves the amount),
fall-through when blank, and Skipped preservation without duplicate.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 3: Backend — `post_journal_entry_single` helper for cell-mode posting

**Files:**
- Modify: `dcnet_pakd/dcnet_pakd/integrations/accounting.py`

- [ ] **Step 3.1: Add the helper function in `accounting.py`**

Append (after `post_external_commission_je` function at end of file):

```python
def post_journal_entry_single(
	pakd_doc,
	line,
	payroll_month: str,
	include_sales_commission_party: bool = True,
) -> str:
	"""Create a 2-leg draft JE for a single PAKD Commission Line (cell mode).

	Args:
		line: a PAKD Commission Line row (object with .component, .amount, .name)
		payroll_month: 'YYYY-MM'
		include_sales_commission_party: when component=='Sales Commission' and
			this is True (bypass-HRMS mode), the CR row is tagged with
			party_type=Employee + party=pakd_doc.sales_person.

	Returns the JE name.

	Caller is responsible for verifying that line.state == 'Pending', that the
	component is mappable (in _COMPONENT_ACCOUNT_FIELDS_DIRECT), and (in HRMS
	mode) that the component is NOT Sales Commission (which goes to AS, not JE).
	"""
	settings = frappe.get_cached_doc("PAKD Settings", "PAKD Settings")
	field_map = _COMPONENT_ACCOUNT_FIELDS_DIRECT
	fields = field_map.get(line.component)
	if not fields:
		frappe.throw(_("Không có mapping TK cho {0}").format(line.component))

	dr_field, cr_field = fields
	dr_account = settings.get(dr_field)
	cr_account = settings.get(cr_field) if cr_field else None
	if not dr_account:
		frappe.throw(_("PAKD Settings: chưa cấu hình {0} ({1})").format(line.component, dr_field))
	if cr_field and not cr_account:
		frappe.throw(_("PAKD Settings: chưa cấu hình TK đối ứng {0} ({1})").format(line.component, cr_field))

	je = frappe.new_doc("Journal Entry")
	je.posting_date = _last_day_of_month(payroll_month)
	je.voucher_type = "Journal Entry"
	je.company = pakd_doc.company
	je.remark = f"PAKD commission CELL {line.component} {payroll_month} | PAKD {pakd_doc.name} | line {line.name}"
	je.user_remark = je.remark

	je.append("accounts", {
		"account": dr_account,
		"debit_in_account_currency": line.amount,
		"credit_in_account_currency": 0,
		"cost_center": pakd_doc.get("cost_center"),
	})
	cr_row = {
		"account": cr_account,
		"debit_in_account_currency": 0,
		"credit_in_account_currency": line.amount,
	}
	if (
		line.component == "Sales Commission"
		and include_sales_commission_party
		and pakd_doc.get("sales_person")
	):
		cr_row["party_type"] = "Employee"
		cr_row["party"] = pakd_doc.sales_person
	je.append("accounts", cr_row)

	je.insert(ignore_permissions=True)
	return je.name
```

- [ ] **Step 3.2: Smoke test via direct call**

```bash
cd /home/long/long/frappe-bench-dcnet
env/bin/python -c "
import frappe
frappe.init(site='dcnet.localhost', sites_path='sites')
frappe.connect()
frappe.set_user('Administrator')

from dcnet_pakd.dcnet_pakd.integrations.accounting import post_journal_entry_single
pakd = frappe.get_doc('Phuong An Kinh Doanh', 'PAKD-2026-00006')
# Pick the MS pending line
line = next(l for l in pakd.commission_lines if l.component == 'Manager Services' and l.state == 'Pending')
je_name = post_journal_entry_single(pakd, line, '2026-05')
je = frappe.get_doc('Journal Entry', je_name)
total_dr = sum(r.debit_in_account_currency for r in je.accounts)
total_cr = sum(r.credit_in_account_currency for r in je.accounts)
print(f'JE: {je_name}, legs={len(je.accounts)}, DR={total_dr}, CR={total_cr}, balance={total_dr-total_cr}')
for r in je.accounts:
    print(f'  {r.account[:40]:<40} DR={r.debit_in_account_currency:>8.0f}  CR={r.credit_in_account_currency:>8.0f}')
# Cleanup
frappe.delete_doc('Journal Entry', je_name, force=True, ignore_permissions=True)
frappe.db.commit()
print('Cleaned up test JE')
"
```

Expected: JE with 2 legs, DR=CR=1500 (MS amount), balance=0, then "Cleaned up test JE".

- [ ] **Step 3.3: Commit**

```bash
cd /home/long/long/frappe-bench-dcnet/apps/dcnet_pakd
git add dcnet_pakd/dcnet_pakd/integrations/accounting.py
git commit -m "$(cat <<'EOF'
feat(pakd): post_journal_entry_single — 2-leg JE for cell-mode commission post

Helper for the upcoming cell-click "Chỉ đăng dòng này" action. Creates
a draft JE with DR <component expense> / CR <counter>, optionally
tagging party=Employee on the CR when the component is Sales Commission
and we're in bypass-HRMS mode.

Caller (api.post_pakd_commission_line) is responsible for state +
HRMS-mode guards; this helper just builds the JE.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 4: Backend — 5 whitelisted API endpoints

**Files:**
- Modify: `dcnet_pakd/dcnet_pakd/api.py` (append at end)

- [ ] **Step 4.1: Add permission helper at top of api.py**

After the imports and before `_APPROVER_ROLE_BY_STATE`, add:

```python
# ─────────────────────────────────────────────────────────────────────────────
# Permission gates for commission line mutations
# ─────────────────────────────────────────────────────────────────────────────
_POST_ROLES = {"PAKD Accountant", "PAKD Board", "Accounts Manager", "System Manager"}
_SKIP_ROLES = {"PAKD Board", "Accounts Manager", "System Manager"}
_OVERRIDE_ROLES = {"PAKD Board", "Accounts Manager", "System Manager"}
_REOPEN_ROLES = {"Accounts Manager", "System Manager"}


def _require_any_role(allowed: set[str]) -> None:
	user_roles = set(frappe.get_roles(frappe.session.user))
	if not user_roles.intersection(allowed):
		frappe.throw(
			_("Không đủ quyền — cần một trong: {0}").format(", ".join(sorted(allowed))),
			frappe.PermissionError,
		)
```

- [ ] **Step 4.2: Add `post_pakd_commission_period` endpoint**

Append at end of api.py:

```python
# ─────────────────────────────────────────────────────────────────────────────
# Commission line cell-level actions (pivot UI)
# ─────────────────────────────────────────────────────────────────────────────

@frappe.whitelist()
def post_pakd_commission_period(pakd: str, month_index) -> dict:
	"""Post all Pending lines in this PAKD's column (period bundle).

	Used by the pivot popover '[Đăng toàn kỳ]' button.
	"""
	_require_any_role(_POST_ROLES)

	from dcnet_pakd.dcnet_pakd.events import _post_pakd_commission_lines

	month_index = int(month_index)
	pakd_doc = frappe.get_doc("Phuong An Kinh Doanh", pakd)

	# Find the most recent submitted Receive PE for this period's SI (if any)
	contract = frappe.get_cached_doc("DCNET Contract", pakd_doc.contract_ref)
	bs_row = next(
		(r for r in contract.get("billing_schedule", []) if r.month_index == month_index),
		None,
	)
	pe_doc = None
	if bs_row and bs_row.get("sales_invoice"):
		pe_name_rows = frappe.db.sql(
			"""SELECT per.parent FROM `tabPayment Entry Reference` per
			   JOIN `tabPayment Entry` pe ON pe.name = per.parent
			   WHERE per.reference_doctype = 'Sales Invoice'
			     AND per.reference_name = %s
			     AND pe.docstatus = 1
			     AND pe.payment_type = 'Receive'
			   ORDER BY pe.posting_date DESC LIMIT 1""",
			(bs_row.sales_invoice,),
		)
		if pe_name_rows:
			pe_doc = frappe.get_doc("Payment Entry", pe_name_rows[0][0])

	if pe_doc is None:
		# Synthetic PE for posting_date — use today
		from types import SimpleNamespace
		pe_doc = SimpleNamespace(name="", posting_date=today())

	_post_pakd_commission_lines(pakd_doc.name, month_index, pe_doc)

	# Re-query: how many lines flipped to Posted and which JE
	posted = frappe.get_all(
		"PAKD Commission Line",
		filters={
			"parent": pakd_doc.name,
			"billing_schedule_idx": month_index,
			"state": "Posted",
			"posted_by_cell": 0,
		},
		fields=["name", "journal_entry", "additional_salary"],
	)
	je_name = posted[0].journal_entry if posted else None
	as_name = next((p.additional_salary for p in posted if p.additional_salary), None)
	return {"je": je_name, "additional_salary": as_name, "lines_posted": len(posted)}
```

- [ ] **Step 4.3: Add `post_pakd_commission_line` endpoint**

Append:

```python
@frappe.whitelist()
def post_pakd_commission_line(line_name: str) -> dict:
	"""Cell-mode: post a single Pending PAKD Commission Line as a 2-leg JE.

	Refused for Sales Commission when use_hrms_for_commission=1 (AS path doesn't
	support single-row posting).
	"""
	_require_any_role(_POST_ROLES)

	line = frappe.get_doc("PAKD Commission Line", line_name)
	if line.state != "Pending":
		frappe.throw(_("Dòng không ở trạng thái Chờ — không thể đăng."))

	pakd_doc = frappe.get_doc("Phuong An Kinh Doanh", line.parent)

	settings = frappe.get_cached_doc("PAKD Settings", "PAKD Settings")
	use_hrms = bool(settings.use_hrms_for_commission)
	if use_hrms and line.component == "Sales Commission":
		frappe.throw(
			_("Khi 'Dùng HRMS' bật, Hoa hồng NVKD đi qua Lương bổ sung (AS), "
			  "không thể đăng riêng 1 dòng. Dùng 'Đăng toàn kỳ' để gộp.")
		)

	from dcnet_pakd.dcnet_pakd.integrations.accounting import post_journal_entry_single
	from frappe.utils import add_months, get_first_day

	# Determine payroll_month using cutoff_day (today is the posting date)
	payment_date = getdate(today())
	cutoff_day = settings.cutoff_day_of_month or 5
	ref_month = add_months(payment_date, -1) if payment_date.day <= cutoff_day else payment_date
	payroll_month = ref_month.strftime("%Y-%m")

	je_name = post_journal_entry_single(
		pakd_doc, line, payroll_month,
		include_sales_commission_party=(not use_hrms),
	)

	frappe.db.set_value(
		"PAKD Commission Line",
		line.name,
		{
			"state": "Posted",
			"journal_entry": je_name,
			"posted_by_cell": 1,
			"payroll_month": payroll_month,
		},
		update_modified=False,
	)
	frappe.db.commit()
	return {"je": je_name, "amount": line.amount}
```

- [ ] **Step 4.4: Add `skip_pakd_commission_line` endpoint**

Append:

```python
@frappe.whitelist()
def skip_pakd_commission_line(line_name: str, reason: str) -> dict:
	"""Transition a Pending line to Skipped with a reason (≥3 chars)."""
	_require_any_role(_SKIP_ROLES)

	reason = (reason or "").strip()
	if len(reason) < 3:
		frappe.throw(_("Lý do bỏ qua phải có ít nhất 3 ký tự."))

	line = frappe.get_doc("PAKD Commission Line", line_name)
	if line.state != "Pending":
		frappe.throw(_("Chỉ có thể bỏ qua dòng đang ở trạng thái Chờ."))

	frappe.db.set_value(
		"PAKD Commission Line",
		line.name,
		{"state": "Skipped", "skip_reason": reason},
		update_modified=False,
	)
	# Audit on parent PAKD timeline
	parent_doc = frappe.get_doc("Phuong An Kinh Doanh", line.parent)
	parent_doc.add_comment(
		"Comment",
		_("Bỏ qua hoa hồng: {0} kỳ {1} — {2}").format(line.component, line.billing_schedule_idx, reason),
	)
	frappe.db.commit()
	return {"state": "Skipped"}
```

- [ ] **Step 4.5: Add `set_pakd_commission_line_override` endpoint**

Append:

```python
@frappe.whitelist()
def set_pakd_commission_line_override(line_name: str, override_rate=None) -> dict:
	"""Set or clear line.override_rate. Triggers full PAKD save → _sync_commission_lines rescale."""
	_require_any_role(_OVERRIDE_ROLES)

	# Normalize: blank, "0", 0, None, "null" → clear (0.0 stored)
	if override_rate is None or override_rate == "":
		new_rate = 0.0
	else:
		try:
			new_rate = float(override_rate)
		except (TypeError, ValueError):
			frappe.throw(_("Tỷ lệ phải là số."))
		if new_rate < 0 or new_rate > 1000:
			frappe.throw(_("Tỷ lệ phải nằm trong khoảng 0-1000%."))

	line = frappe.get_doc("PAKD Commission Line", line_name)
	if line.state != "Pending":
		frappe.throw(_("Chỉ có thể đặt override cho dòng đang ở trạng thái Chờ."))

	old_amount = float(line.amount or 0)
	frappe.db.set_value(
		"PAKD Commission Line",
		line.name,
		{"override_rate": new_rate},
		update_modified=False,
	)

	# Trigger _sync_commission_lines rescale via parent save
	parent_doc = frappe.get_doc("Phuong An Kinh Doanh", line.parent)
	parent_doc.save(ignore_permissions=False)
	frappe.db.commit()

	new_amount = float(frappe.db.get_value("PAKD Commission Line", line_name, "amount") or 0)
	return {"old_amount": old_amount, "new_amount": new_amount, "effective_rate": new_rate}
```

- [ ] **Step 4.6: Add `reopen_pakd_commission_line` endpoint**

Append:

```python
@frappe.whitelist()
def reopen_pakd_commission_line(line_name: str) -> dict:
	"""Cancelled or Skipped → Pending (state-only). Deletes draft JE if any."""
	_require_any_role(_REOPEN_ROLES)

	line = frappe.get_doc("PAKD Commission Line", line_name)
	if line.state not in ("Cancelled", "Skipped"):
		frappe.throw(_("Chỉ có thể khôi phục dòng đang ở trạng thái Đã huỷ hoặc Bỏ qua."))

	# If a JE is attached and still a draft, delete it. If submitted, refuse.
	if line.journal_entry and frappe.db.exists("Journal Entry", line.journal_entry):
		je_docstatus = frappe.db.get_value("Journal Entry", line.journal_entry, "docstatus")
		if je_docstatus == 1:
			frappe.throw(
				_("JE {0} đã được duyệt — không thể tự động khôi phục. Vui lòng đảo bút toán thủ công.")
				.format(line.journal_entry)
			)
		frappe.delete_doc("Journal Entry", line.journal_entry, ignore_permissions=True, force=1)

	frappe.db.set_value(
		"PAKD Commission Line",
		line.name,
		{
			"state": "Pending",
			"journal_entry": None,
			"additional_salary": None,
			"payment_entry": None,
			"payroll_month": None,
			"posted_by_cell": 0,
			"skip_reason": "",
		},
		update_modified=False,
	)
	parent_doc = frappe.get_doc("Phuong An Kinh Doanh", line.parent)
	parent_doc.add_comment(
		"Comment",
		_("Khôi phục dòng hoa hồng về Chờ: {0} kỳ {1}").format(line.component, line.billing_schedule_idx),
	)
	frappe.db.commit()
	return {"state": "Pending"}
```

- [ ] **Step 4.7: Restart bench so api.py is reloaded**

```bash
cd /home/long/long/frappe-bench-dcnet
pkill -f "honcho start" 2>&1 || true
sleep 2
setsid -f sh -c 'bench start > /tmp/bench-dcnet.log 2>&1'
sleep 8
curl -sS -o /dev/null -w "HTTP %{http_code} in %{time_total}s\n" http://localhost:8001/api/method/ping
```

Expected: `HTTP 200 in <Xs>`.

- [ ] **Step 4.8: Smoke test each endpoint via authenticated session**

```bash
cd /home/long/long/frappe-bench-dcnet
env/bin/python -c "
import frappe, secrets
frappe.init(site='dcnet.localhost', sites_path='sites')
frappe.connect()
sid = secrets.token_hex(20)
frappe.db.sql(\"INSERT INTO tabSessions (user,sid,sessiondata,ipaddress,lastupdate,status) VALUES ('Administrator', %s, %s, '127.0.0.1', NOW(), 'Active')\",
              (sid, frappe.as_json({'user':'Administrator','ipaddress':'127.0.0.1'})))
frappe.db.commit()
print('SID:', sid)
"
```

Capture the SID. Then test each:

```bash
SID=<sid_from_above>

# Test post_pakd_commission_line on a single Pending line
LINE=$(env/bin/python -c "
import frappe
frappe.init(site='dcnet.localhost', sites_path='sites')
frappe.connect()
l = frappe.db.get_value('PAKD Commission Line', {'parent':'PAKD-2026-00006', 'state':'Pending', 'component':'Manager Services'}, 'name')
print(l)
")
echo "Line: $LINE"
curl -sS -b "sid=$SID" "http://localhost:8001/api/method/dcnet_pakd.dcnet_pakd.api.post_pakd_commission_line?line_name=$LINE" | head -3
```

Expected: `{"message": {"je": "PT-2026-000XX", "amount": 1500.0}}`. Verify in DB:

```bash
env/bin/python -c "
import frappe
frappe.init(site='dcnet.localhost', sites_path='sites')
frappe.connect()
l = frappe.db.get_value('PAKD Commission Line', '$LINE', ['state','journal_entry','posted_by_cell'], as_dict=True)
print(l)
"
```

Expected: `{'state': 'Posted', 'journal_entry': 'PT-2026-...', 'posted_by_cell': 1}`.

**Clean up the test JE + reset line:**
```bash
env/bin/python -c "
import frappe
frappe.init(site='dcnet.localhost', sites_path='sites')
frappe.connect()
je = frappe.db.get_value('PAKD Commission Line', '$LINE', 'journal_entry')
if je and frappe.db.exists('Journal Entry', je):
    frappe.delete_doc('Journal Entry', je, force=True, ignore_permissions=True)
frappe.db.set_value('PAKD Commission Line', '$LINE', {'state':'Pending','journal_entry':None,'posted_by_cell':0,'payroll_month':None}, update_modified=False)
frappe.db.commit()
print('Reset')
"
```

- [ ] **Step 4.9: Commit**

```bash
cd /home/long/long/frappe-bench-dcnet/apps/dcnet_pakd
git add dcnet_pakd/dcnet_pakd/api.py
git commit -m "$(cat <<'EOF'
feat(pakd): 5 commission line API endpoints for pivot cell actions

Adds whitelisted endpoints used by the pivot popover:
- post_pakd_commission_period(pakd, month_index) — wrap _post_pakd_commission_lines
- post_pakd_commission_line(line_name) — 2-leg JE for one cell
- skip_pakd_commission_line(line_name, reason) — Pending → Skipped
- set_pakd_commission_line_override(line_name, override_rate) — triggers re-sync rescale
- reopen_pakd_commission_line(line_name) — Cancelled/Skipped → Pending

Each endpoint gates on role: post needs Accountant/Board/AcctsMgr;
skip + override need Board/AcctsMgr; reopen needs AcctsMgr.

Cell-mode post is refused on Sales Commission when use_hrms=1 (the AS
path doesn't support single-row posting).

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 5: Form JSON — hide commission_lines, add commission_pivot_html

**Files:**
- Modify: `dcnet_pakd/dcnet_pakd/doctype/phuong_an_kinh_doanh/phuong_an_kinh_doanh.json`

- [ ] **Step 5.1: Locate the `section_commission` block and add the HTML field**

Grep for the section anchor:
```bash
grep -n "section_commission\|commission_lines" /home/long/long/frappe-bench-dcnet/apps/dcnet_pakd/dcnet_pakd/dcnet_pakd/doctype/phuong_an_kinh_doanh/phuong_an_kinh_doanh.json | head
```

In `field_order` array, locate `"commission_lines"` and insert `"commission_pivot_html"` BEFORE it. Result should look like:

```
...
"section_commission",
"commission_pivot_html",
"commission_lines",
...
```

In `fields` array, find the `commission_lines` field definition and:
1. Add `"hidden": 1` to it (so the old grid is no longer visible)
2. Insert a new field block BEFORE it:

```json
{
    "fieldname": "commission_pivot_html",
    "fieldtype": "HTML",
    "label": "Bảng hoa hồng theo kỳ"
},
```

Bump the doctype's `modified` timestamp to a later value.

- [ ] **Step 5.2: Run migrate**

```bash
cd /home/long/long/frappe-bench-dcnet
bench --site dcnet.localhost migrate 2>&1 | tail -5
bench --site dcnet.localhost clear-cache 2>&1 | tail -3
```

- [ ] **Step 5.3: Verify field meta**

```bash
env/bin/python -c "
import frappe
frappe.init(site='dcnet.localhost', sites_path='sites')
frappe.connect()
m = frappe.get_meta('Phuong An Kinh Doanh')
f1 = m.get_field('commission_pivot_html')
f2 = m.get_field('commission_lines')
print('commission_pivot_html:', f1.fieldtype if f1 else 'MISSING', '|', f1.label if f1 else '')
print('commission_lines hidden:', f2.hidden if f2 else 'MISSING')
"
```

Expected:
```
commission_pivot_html: HTML | Bảng hoa hồng theo kỳ
commission_lines hidden: 1
```

- [ ] **Step 5.4: Commit**

```bash
cd /home/long/long/frappe-bench-dcnet/apps/dcnet_pakd
git add dcnet_pakd/dcnet_pakd/doctype/phuong_an_kinh_doanh/phuong_an_kinh_doanh.json
git commit -m "$(cat <<'EOF'
feat(pakd): hide commission_lines table, add commission_pivot_html field

Replaces the vertical 48-row child table with an HTML field for the
pivot grid. The pivot is rendered by JS in phuong_an_kinh_doanh.js
(next commit).

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 6: JS — render the pivot grid + popover dialog

**Files:**
- Modify: `dcnet_pakd/dcnet_pakd/doctype/phuong_an_kinh_doanh/phuong_an_kinh_doanh.js`

- [ ] **Step 6.1: Hook the pivot render into the form refresh**

Find the existing `refresh` function (around line 65-75 of phuong_an_kinh_doanh.js) and add a call to a new `_render_commission_pivot(frm)` function — same placement as `_render_pakd_summary_card(frm)`. Right after that call, add:

```js
_render_commission_pivot(frm);
```

- [ ] **Step 6.2: Add the pivot renderer**

Append at the end of phuong_an_kinh_doanh.js (before the final closing brace/EOF):

```js
// ─────────────────────────────────────────────────────────────────────────────
// Commission pivot grid (replaces the read-only child table)
// ─────────────────────────────────────────────────────────────────────────────

const _PAKD_STATUS_META = {
	"Pending":   { icon: "○", className: "dcnet-pakd-pending",   tooltip: __("Chờ đăng") },
	"Posted":    { icon: "✓", className: "dcnet-pakd-posted",    tooltip: __("Đã đăng") },
	"Cancelled": { icon: "⨯", className: "dcnet-pakd-cancelled", tooltip: __("Đã huỷ") },
	"Skipped":   { icon: "↷", className: "dcnet-pakd-skipped",   tooltip: __("Bỏ qua") },
};

function _fmt_vnd(n) {
	if (!n) return "0";
	return Math.round(Number(n)).toLocaleString("vi-VN");
}

function _render_commission_pivot(frm) {
	const $w = frm.fields_dict.commission_pivot_html && frm.fields_dict.commission_pivot_html.$wrapper;
	if (!$w || !$w.length) return;

	const lines = frm.doc.commission_lines || [];
	if (!lines.length) {
		$w.html(`<div class="text-muted" style="padding:12px;">${__("Chưa có dòng hoa hồng.")}</div>`);
		return;
	}

	// Build row + column axes
	const is_ftth = frm.doc.pakd_type === "Monthly FTTH Rollup";
	let row_keys, row_labels;
	if (is_ftth) {
		// rows = PAKD Items by item_code (deduped, in order encountered)
		const seen = new Set();
		row_keys = [];
		row_labels = {};
		for (const item of (frm.doc.items || [])) {
			const key = item.item_code || item.name;
			if (seen.has(key)) continue;
			seen.add(key);
			row_keys.push(key);
			const coef = item.salary_coefficient ? ` · ${item.salary_coefficient}%` : "";
			row_labels[key] = `${frappe.utils.escape_html(item.item_code || "")}${coef}`;
		}
	} else {
		row_keys = ["Manager Services", "Add Costs", "License Fee", "Sales Commission"];
		// effective rate per component (uses commission_overrides + template)
		const override_map = {};
		for (const r of (frm.doc.commission_overrides || [])) {
			override_map[r.component] = { override: r.override_rate || 0, template: r.template_rate || 0 };
		}
		row_labels = {};
		for (const comp of row_keys) {
			const m = override_map[comp] || { override: 0, template: 0 };
			const effective = m.override || m.template;
			const marker = m.override ? ' <span class="text-muted">●</span>' : '';
			row_labels[comp] = `${comp} <span class="text-muted">${effective}%</span>${marker}`;
		}
	}

	const col_indices = Array.from(new Set(lines.map(l => l.billing_schedule_idx))).sort((a, b) => a - b);
	// Column headers via contract billing schedule (if accessible)
	const col_si = {};
	for (const l of lines) {
		if (!col_si[l.billing_schedule_idx]) {
			col_si[l.billing_schedule_idx] = {};
		}
	}

	// Look up SI/PE per period via separate frappe.call (cached in closure)
	if (!frm._dcnet_pivot_bs_cache) {
		frm._dcnet_pivot_bs_cache = null;
	}
	const ensure_bs_cache = (cb) => {
		if (frm._dcnet_pivot_bs_cache !== null) {
			cb(frm._dcnet_pivot_bs_cache);
			return;
		}
		if (!frm.doc.contract_ref) {
			frm._dcnet_pivot_bs_cache = {};
			cb({});
			return;
		}
		frappe.db.get_doc("DCNET Contract", frm.doc.contract_ref).then(c => {
			const map = {};
			for (const r of (c.billing_schedule || [])) {
				map[r.month_index] = {
					sales_invoice: r.sales_invoice || null,
					state: r.state || null,
				};
			}
			frm._dcnet_pivot_bs_cache = map;
			cb(map);
		}).catch(() => {
			frm._dcnet_pivot_bs_cache = {};
			cb({});
		});
	};

	ensure_bs_cache((bs_map) => {
		// Build cell map: cell_map[row_key][col_idx] = line
		const cell_map = {};
		for (const k of row_keys) cell_map[k] = {};
		for (const l of lines) {
			const k = is_ftth ? (l.item_code || l.component || row_keys[0]) : l.component;
			if (k in cell_map) {
				cell_map[k][l.billing_schedule_idx] = l;
			}
		}

		// Totals
		const col_totals = {}; for (const c of col_indices) col_totals[c] = 0;
		const row_totals = {}; for (const k of row_keys) row_totals[k] = 0;
		let grand = 0;
		const counted_state = new Set(["Pending", "Posted"]);
		for (const l of lines) {
			const k = is_ftth ? (l.item_code || l.component || row_keys[0]) : l.component;
			if (!(k in cell_map)) continue;
			if (!counted_state.has(l.state)) continue;
			col_totals[l.billing_schedule_idx] = (col_totals[l.billing_schedule_idx] || 0) + (l.amount || 0);
			row_totals[k] = (row_totals[k] || 0) + (l.amount || 0);
			grand += l.amount || 0;
		}

		// Render
		const css = `
			<style>
				.dcnet-pakd-pivot-wrap { overflow-x: auto; position: relative; }
				.dcnet-pakd-pivot { border-collapse: separate; border-spacing: 0; min-width: 100%; font-size: 13px; }
				.dcnet-pakd-pivot th, .dcnet-pakd-pivot td { border: 1px solid #e9ebef; padding: 6px 10px; vertical-align: middle; }
				.dcnet-pakd-pivot th { background: #fafbfc; font-weight: 600; text-align: left; white-space: nowrap; }
				.dcnet-pakd-pivot th.col-period { text-align: center; min-width: 100px; }
				.dcnet-pakd-pivot td.cell { text-align: right; min-width: 100px; cursor: pointer; transition: background-color 0.1s; }
				.dcnet-pakd-pivot td.cell:hover { background-color: #f6f8fa; outline: 1px solid #c8d1da; outline-offset: -1px; }
				.dcnet-pakd-pivot td.dcnet-pakd-pending  { background: #fafbfc; color: #6a737d; }
				.dcnet-pakd-pivot td.dcnet-pakd-posted   { background: #e6f6ea; color: #1b6b30; }
				.dcnet-pakd-pivot td.dcnet-pakd-cancelled { background: #fceaea; color: #b32424; text-decoration: line-through; }
				.dcnet-pakd-pivot td.dcnet-pakd-skipped  { background: #fff5d6; color: #8a6500; text-decoration: line-through; }
				.dcnet-pakd-pivot tr.totals-row td { background: #f0f3f6; font-weight: 600; }
				.dcnet-pakd-pivot tr.totals-row td.grand { background: #e5eaef; }
				.dcnet-pakd-pivot th.sticky-col, .dcnet-pakd-pivot td.sticky-col {
					position: sticky; left: 0; background: #fafbfc; z-index: 2;
				}
				.dcnet-pakd-pivot th.sticky-col-right, .dcnet-pakd-pivot td.sticky-col-right {
					position: sticky; right: 0; background: #f0f3f6; z-index: 2;
				}
				.dcnet-pakd-pivot th.sticky-col-right.grand, .dcnet-pakd-pivot td.sticky-col-right.grand { z-index: 3; background: #e5eaef; }
				.dcnet-pakd-status-pill { display: inline-block; margin-left: 6px; font-size: 11px; opacity: 0.9; }
				.dcnet-pakd-cell-by-cell { font-size: 9px; vertical-align: super; margin-left: 2px; opacity: 0.7; }
				.dcnet-pakd-col-link { display: block; font-size: 11px; color: #0366d6; font-weight: 400; text-decoration: none; margin-top: 2px; }
				.dcnet-pakd-col-link.muted { color: #6a737d; }
			</style>
		`;

		// Header cells
		let header_cells = `<th class="sticky-col">${__("Thành phần / Mục")}</th>`;
		for (const c of col_indices) {
			const bs = bs_map[c] || {};
			let link_html = `<span class="dcnet-pakd-col-link muted">(${__("chưa SI")})</span>`;
			if (bs.sales_invoice) {
				link_html = `<a class="dcnet-pakd-col-link" target="_blank" href="/app/sales-invoice/${encodeURIComponent(bs.sales_invoice)}">${frappe.utils.escape_html(bs.sales_invoice)} »</a>`;
			}
			header_cells += `<th class="col-period">${__("Kỳ")} ${c}${link_html}</th>`;
		}
		header_cells += `<th class="sticky-col-right">${__("Tổng / dòng")}</th>`;

		// Body rows
		let body = "";
		for (const k of row_keys) {
			let row = `<tr><th class="sticky-col">${row_labels[k] || k}</th>`;
			for (const c of col_indices) {
				const l = cell_map[k][c];
				if (!l) {
					row += `<td></td>`;
					continue;
				}
				const meta = _PAKD_STATUS_META[l.state] || _PAKD_STATUS_META["Pending"];
				const cell_marker = l.posted_by_cell ? `<sup class="dcnet-pakd-cell-by-cell">c</sup>` : "";
				row += `<td class="cell ${meta.className}" data-line="${frappe.utils.escape_html(l.name)}" data-row="${k}" data-col="${c}" title="${meta.tooltip}">
					${_fmt_vnd(l.amount)}
					<span class="dcnet-pakd-status-pill">${meta.icon}${cell_marker}</span>
				</td>`;
			}
			row += `<td class="sticky-col-right">${_fmt_vnd(row_totals[k])}</td>`;
			row += `</tr>`;
			body += row;
		}

		// Totals row
		let totals_row = `<tr class="totals-row"><td class="sticky-col">${__("Tổng / kỳ")}</td>`;
		for (const c of col_indices) {
			totals_row += `<td>${_fmt_vnd(col_totals[c])}</td>`;
		}
		totals_row += `<td class="sticky-col-right grand">${_fmt_vnd(grand)}</td>`;
		totals_row += `</tr>`;

		const html = `${css}
			<div class="dcnet-pakd-pivot-wrap">
				<table class="dcnet-pakd-pivot">
					<thead><tr>${header_cells}</tr></thead>
					<tbody>${body}${totals_row}</tbody>
				</table>
			</div>`;
		$w.html(html);

		// Wire cell click → popover
		$w.find("td.cell").on("click", (e) => {
			const $cell = $(e.currentTarget);
			const line_name = $cell.data("line");
			const line = (frm.doc.commission_lines || []).find(x => x.name === line_name);
			if (!line) return;
			if (e.ctrlKey || e.metaKey) {
				if (line.state === "Pending") {
					_pivot_post_cell(frm, line);
					return;
				}
			}
			_open_pivot_popover(frm, line, { col_period: $cell.data("col") });
		});
	});
}
```

- [ ] **Step 6.3: Add the popover dialog**

Append:

```js
function _open_pivot_popover(frm, line, options) {
	const meta = _PAKD_STATUS_META[line.state] || _PAKD_STATUS_META["Pending"];
	const title = `${line.component} · ${__("Kỳ")} ${line.billing_schedule_idx}`;

	// Effective rate display
	let rate_source = __("(mặc định mẫu)");
	let effective_rate = null;
	if (line.override_rate) {
		effective_rate = line.override_rate;
		rate_source = __("(override dòng)");
	} else {
		const overrides = frm.doc.commission_overrides || [];
		const ov = overrides.find(r => r.component === line.component);
		if (ov && ov.override_rate) {
			effective_rate = ov.override_rate;
			rate_source = __("(override PAKD-wide)");
		} else if (ov && ov.template_rate) {
			effective_rate = ov.template_rate;
		}
	}

	const refs_html = `
		<div style="margin-top:8px;">
			<strong>${__("Refs")}:</strong><br>
			<small>SI: ${line.payment_entry ? __("(qua PE)") : (line.journal_entry ? "" : "—")}</small><br>
			<small>JE: ${line.journal_entry ? `<a href="/app/journal-entry/${line.journal_entry}" target="_blank">${line.journal_entry} »</a>` : "—"}</small><br>
			<small>AS: ${line.additional_salary ? `<a href="/app/additional-salary/${line.additional_salary}" target="_blank">${line.additional_salary} »</a>` : "—"}</small><br>
			<small>PE: ${line.payment_entry ? `<a href="/app/payment-entry/${line.payment_entry}" target="_blank">${line.payment_entry} »</a>` : "—"}</small>
		</div>
	`;

	const skip_html = line.state === "Skipped" && line.skip_reason
		? `<div style="margin-top:8px;"><strong>${__("Lý do bỏ qua")}:</strong> ${frappe.utils.escape_html(line.skip_reason)}</div>`
		: "";

	const summary_html = `
		<div>
			<strong>${__("Số tiền")}:</strong> ${_fmt_vnd(line.amount)} ₫ · <strong>${__("Trạng thái")}:</strong> ${meta.icon} ${meta.tooltip}
		</div>
		<div style="margin-top:6px;">
			<strong>${__("Tỷ lệ áp dụng")}:</strong> ${effective_rate || "—"}% ${rate_source}
		</div>
		${refs_html}
		${skip_html}
	`;

	// Action buttons differ by state
	const fields = [];
	fields.push({ fieldtype: "HTML", fieldname: "summary", options: summary_html });

	if (line.state === "Pending") {
		fields.push({
			fieldtype: "Float", fieldname: "override_input",
			label: __("Tuỳ chỉnh tỷ lệ (% - để 0 dùng mặc định)"),
			default: line.override_rate || 0, precision: 2,
		});
	}

	const d = new frappe.ui.Dialog({
		title,
		fields,
		primary_action_label: _primary_action_label(line, frm),
		primary_action: () => _primary_action(d, frm, line, options),
	});

	// Secondary actions: render after dialog opens
	d.$wrapper.on("shown.bs.modal", () => {
		const $footer = d.$wrapper.find(".modal-footer");
		// Clear our previous extras so re-opens don't duplicate
		$footer.find(".dcnet-pakd-secondary").remove();
		const secondary = _secondary_actions(d, frm, line, options);
		for (const btn of secondary) {
			const $b = $(`<button class="btn btn-default btn-sm dcnet-pakd-secondary" style="margin-right:4px;">${btn.label}</button>`);
			$b.on("click", btn.handler);
			$footer.prepend($b);
		}
	});

	d.show();
}

function _primary_action_label(line, frm) {
	if (line.state === "Pending") {
		const same_col = (frm.doc.commission_lines || [])
			.filter(l => l.billing_schedule_idx === line.billing_schedule_idx && l.state === "Pending");
		return __("Đăng toàn kỳ ({0} dòng)", [same_col.length]);
	}
	if (line.state === "Posted") return __("Mở JE »");
	if (line.state === "Cancelled" || line.state === "Skipped") return __("Khôi phục về Chờ");
	return __("Đóng");
}

function _primary_action(dialog, frm, line, options) {
	if (line.state === "Pending") {
		_pivot_post_period(frm, line);
		dialog.hide();
		return;
	}
	if (line.state === "Posted") {
		if (line.journal_entry) {
			frappe.set_route("Form", "Journal Entry", line.journal_entry);
		}
		dialog.hide();
		return;
	}
	if (line.state === "Cancelled" || line.state === "Skipped") {
		_pivot_reopen_line(frm, line);
		dialog.hide();
		return;
	}
	dialog.hide();
}

function _secondary_actions(dialog, frm, line, options) {
	const buttons = [];
	if (line.state === "Pending") {
		const settings_use_hrms = (frappe.boot.dcnet_pakd_use_hrms || 0); // safe fallback
		const hide_cell_post = settings_use_hrms && line.component === "Sales Commission";
		if (!hide_cell_post) {
			buttons.push({
				label: __("Chỉ đăng dòng này"),
				handler: () => { _pivot_post_cell(frm, line); dialog.hide(); },
			});
		}
		buttons.push({
			label: __("Bỏ qua dòng này"),
			handler: () => { _pivot_skip_line(frm, line); dialog.hide(); },
		});
		buttons.push({
			label: __("Áp dụng tỷ lệ override"),
			handler: () => {
				const new_rate = dialog.get_value("override_input") || 0;
				_pivot_set_override(frm, line, new_rate);
				dialog.hide();
			},
		});
	}
	if (line.state === "Posted") {
		buttons.push({
			label: __("Đảo bút toán"),
			handler: () => {
				if (!line.journal_entry) return;
				frappe.confirm(
					__("Đảo (xoá) bút toán {0}? Chỉ áp dụng cho JE còn ở trạng thái Nháp.", [line.journal_entry]),
					() => {
						frappe.db.get_value("Journal Entry", line.journal_entry, "docstatus").then(r => {
							if (r.message && r.message.docstatus === 0) {
								frappe.db.delete_doc("Journal Entry", line.journal_entry).then(() => {
									frappe.show_alert({ message: __("Đã xoá JE nháp"), indicator: "green" });
									frm.reload_doc();
								});
							} else {
								frappe.msgprint(__("JE đã được duyệt — vui lòng đảo bút toán thủ công."));
							}
						});
						dialog.hide();
					}
				);
			},
		});
	}
	return buttons;
}
```

- [ ] **Step 6.4: Add the action dispatchers**

Append:

```js
function _pivot_post_cell(frm, line) {
	frappe.call({
		method: "dcnet_pakd.dcnet_pakd.api.post_pakd_commission_line",
		args: { line_name: line.name },
		freeze: true,
		freeze_message: __("Đang đăng dòng..."),
		callback: (r) => {
			if (r.message && r.message.je) {
				frappe.show_alert({ message: __("Đã đăng JE {0}", [r.message.je]), indicator: "green" });
				frm.reload_doc();
			}
		},
	});
}

function _pivot_post_period(frm, line) {
	frappe.call({
		method: "dcnet_pakd.dcnet_pakd.api.post_pakd_commission_period",
		args: { pakd: frm.docname, month_index: line.billing_schedule_idx },
		freeze: true,
		freeze_message: __("Đang đăng toàn kỳ..."),
		callback: (r) => {
			if (r.message) {
				const je = r.message.je || "—";
				frappe.show_alert({ message: __("Đã đăng {0} dòng (JE {1})", [r.message.lines_posted, je]), indicator: "green" });
				frm.reload_doc();
			}
		},
	});
}

function _pivot_skip_line(frm, line) {
	frappe.prompt(
		[{ fieldname: "reason", fieldtype: "Small Text", label: __("Lý do bỏ qua"), reqd: 1 }],
		(values) => {
			frappe.call({
				method: "dcnet_pakd.dcnet_pakd.api.skip_pakd_commission_line",
				args: { line_name: line.name, reason: values.reason },
				freeze: true,
				callback: () => {
					frappe.show_alert({ message: __("Đã đánh dấu bỏ qua"), indicator: "blue" });
					frm.reload_doc();
				},
			});
		},
		__("Bỏ qua dòng này"),
		__("Lưu")
	);
}

function _pivot_set_override(frm, line, override_rate) {
	frappe.call({
		method: "dcnet_pakd.dcnet_pakd.api.set_pakd_commission_line_override",
		args: { line_name: line.name, override_rate: override_rate },
		freeze: true,
		freeze_message: __("Đang cập nhật tỷ lệ..."),
		callback: (r) => {
			if (r.message) {
				frappe.show_alert({
					message: __("Số tiền: {0} → {1}", [_fmt_vnd(r.message.old_amount), _fmt_vnd(r.message.new_amount)]),
					indicator: "blue",
				});
				frm.reload_doc();
			}
		},
	});
}

function _pivot_reopen_line(frm, line) {
	frappe.call({
		method: "dcnet_pakd.dcnet_pakd.api.reopen_pakd_commission_line",
		args: { line_name: line.name },
		freeze: true,
		callback: () => {
			frappe.show_alert({ message: __("Đã khôi phục về Chờ"), indicator: "green" });
			frm.reload_doc();
		},
	});
}
```

- [ ] **Step 6.5: Boot data — surface `use_hrms_for_commission` to JS**

The popover decides whether to hide "Chỉ đăng dòng này" on SC cells based on `frappe.boot.dcnet_pakd_use_hrms`. To make that available, add a boot hook.

Check if `dcnet_pakd/hooks.py` has a `boot_session` entry. If not, add one. Otherwise extend the existing function.

```bash
grep -n "boot_session\|extend_bootinfo" /home/long/long/frappe-bench-dcnet/apps/dcnet_pakd/dcnet_pakd/hooks.py
```

If nothing, add to hooks.py:
```python
extend_bootinfo = "dcnet_pakd.dcnet_pakd.boot.boot_session"
```

Create `dcnet_pakd/dcnet_pakd/boot.py`:
```python
"""Boot session extensions for the PAKD app — surfaces PAKD Settings flags to JS."""

import frappe


def boot_session(bootinfo):
	try:
		use_hrms = frappe.db.get_single_value("PAKD Settings", "use_hrms_for_commission")
		bootinfo["dcnet_pakd_use_hrms"] = int(use_hrms or 0)
	except Exception:
		bootinfo["dcnet_pakd_use_hrms"] = 0
```

- [ ] **Step 6.6: Build assets + clear cache + restart bench**

```bash
cd /home/long/long/frappe-bench-dcnet
bench build --app dcnet_pakd 2>&1 | tail -5
bench --site dcnet.localhost clear-cache 2>&1 | tail -3
pkill -f "honcho start" 2>&1 || true
sleep 2
setsid -f sh -c 'bench start > /tmp/bench-dcnet.log 2>&1'
sleep 8
curl -sS -o /dev/null -w "HTTP %{http_code} in %{time_total}s\n" http://localhost:8001/api/method/ping
```

Expected: `HTTP 200`.

- [ ] **Step 6.7: Commit**

```bash
cd /home/long/long/frappe-bench-dcnet/apps/dcnet_pakd
git add dcnet_pakd/dcnet_pakd/doctype/phuong_an_kinh_doanh/phuong_an_kinh_doanh.js \
        dcnet_pakd/dcnet_pakd/boot.py \
        dcnet_pakd/hooks.py
git commit -m "$(cat <<'EOF'
feat(pakd): pivot grid + cell popover dialog (FB-2026-00587)

Replaces the read-only commission_lines child table with a JS-rendered
horizontal pivot:
- Rows: components (Recurring/One-off) or PAKD Items (FTTH Rollup)
- Cols: billing periods from contract billing_schedule
- Sticky first + last column; status-tinted cells; period totals + grand total

Click any cell to open the Frappe Dialog popover with status-aware
actions:
- Pending: [Đăng toàn kỳ] · [Chỉ đăng dòng này] · [Bỏ qua] · [Override %]
- Posted:  [Mở JE »] · [Đảo bút toán]
- Skipped/Cancelled: [Khôi phục về Chờ]

Ctrl/Cmd+click on a Pending cell fires "Chỉ đăng dòng này" directly
(bypass popover).

Boot session exposes use_hrms_for_commission so the popover can hide
single-cell post on Sales Commission in HRMS mode (where SC goes through
Additional Salary, not JE).

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 7: Live dogfood via Playwright MCP

**Goal:** Verify every UI flow listed in §10 of the spec passes against the running bench at `dcnet.localhost:8001`. No code changes here unless a flow fails.

- [ ] **Step 7.1: Navigate to PAKD-2026-00006 (Draft, 3 Pending lines)**

Use Playwright MCP `browser_navigate http://localhost:8001/app/phuong-an-kinh-doanh/PAKD-2026-00006`, wait 3s, snapshot.

- [ ] **Step 7.2: Verify pivot renders 4 rows × 3 cols (label + 1 period + total)**

Use `browser_evaluate`:
```js
() => {
  const t = document.querySelector('.dcnet-pakd-pivot');
  if (!t) return { error: 'pivot not rendered' };
  const headers = Array.from(t.querySelectorAll('thead th')).map(h => h.textContent.trim().substring(0, 30));
  const rows = Array.from(t.querySelectorAll('tbody tr')).map(r => Array.from(r.children).map(c => c.textContent.trim().substring(0, 25)));
  return { headers, rows };
}
```

Expected: headers ~ `["Thành phần / Mục", "Kỳ 1...", "Tổng / dòng"]`; first body row label like `"Manager Services 10%"`; totals row at bottom.

- [ ] **Step 7.3: Test override flow (5% on MS row → halves to 750)**

Click the MS cell at Kỳ 1, fill `override_input=5`, click "Áp dụng tỷ lệ override". Wait 2s. Verify the MS cell value updates from 1500 → 750.

Cleanup: re-click cell, set override to 0, apply. Verify back to 1500.

- [ ] **Step 7.4: Test skip flow**

Click MS cell, click "Bỏ qua dòng này", fill reason "Test bỏ qua tự động". Wait 2s. Verify cell shows amber `↷` icon and is strikethrough. Verify column total no longer includes this line.

Cleanup: click cell again, click "Khôi phục về Chờ". Wait 2s. Verify cell back to Pending state.

- [ ] **Step 7.5: Test per-cell post (Ctrl+click)**

Hold Ctrl + click the AC cell at Kỳ 1. Wait 3s. Verify cell flips to Posted (green ✓ with `c` superscript). Open the JE link from the popover (re-click cell) and verify it's a 2-leg JE (DR 6418 / CR 3388, both 500).

Cleanup: re-click the cell, click "Đảo bút toán" to delete the draft JE. Verify cell flips back to Pending.

- [ ] **Step 7.6: Test mobile @ 390×844**

Resize the browser to 390×844 via `browser_resize`. Verify horizontal scroll is enabled, sticky-label column stays visible while scrolling right, and `document.documentElement.scrollWidth > window.innerWidth === false`.

- [ ] **Step 7.7: Verify console error count = 0**

Use `browser_console_messages level=error all=true`. Should be empty.

- [ ] **Step 7.8: If any flow fails — fix + commit fix + re-test that step**

Any failure here is a bug in Task 6's JS. Fix in `phuong_an_kinh_doanh.js`, re-run `bench build --app dcnet_pakd` (no need to restart bench for JS-only changes, but if the change is also touching `boot.py` or hooks then restart), hard-refresh browser (Ctrl+Shift+R), re-run the failing step.

Commit any fixes as `fix(pakd): pivot dogfood — <what>`.

- [ ] **Step 7.9: Final commit (if no fixes needed)**

If all flows passed cleanly, no commit needed. If any fix was made, ensure it's committed before moving on.

---

## Task 8: Resolve feedback + write session-last

**Files:**
- (no code changes)

- [ ] **Step 8.1: Mark FB-2026-00587 as in-progress in feedback inbox**

```bash
python3 ~/.claude/skills/feedback-inbox/inbox.py inprogress FB-2026-00587 --reason "Pivot implementation shipped on develop (commits Task1-7). Awaiting PR to dcnet/develop."
```

- [ ] **Step 8.2: Verify final state of dcnet_pakd**

```bash
cd /home/long/long/frappe-bench-dcnet/apps/dcnet_pakd
git log --oneline -10
git status -s
```

Expected: clean working tree, ~7 new commits from this plan on top of `cce0303`.

- [ ] **Step 8.3: Update session-last**

Append to `/home/long/long/frappe-bench-dcnet/.multi-session/session-last-dcnet-pakd-phase7-bc.md` (or a new file `session-last-dcnet-pakd-pivot.md`):

A short summary of what was implemented + which commits + status of FB-2026-00587. Include the count of total commits ahead of dcnet/develop now (was 9, should be ~16 after this work).

- [ ] **Step 8.4: Hand back to operator**

Tell the user:
- All tasks complete
- N commits added (list SHAs + one-line summaries)
- FB-2026-00587 marked in-progress
- Total commits ahead of dcnet/develop is now X
- Ready to either continue with another feedback batch or open a PR

---

## Self-review notes

**Spec coverage:**
- §2 Data model → Task 1 ✓
- §2 Override precedence → Task 2 ✓
- §3 UI / pivot grid layout → Task 6 ✓
- §4 Cell popover → Task 6 ✓
- §5 Backend API (5 endpoints) → Task 4 ✓
- §6 JE shape (both modes) → Tasks 3 + 4 ✓
- §7 Permissions → Task 4 (per-endpoint `_require_any_role`) ✓
- §8 Engine integration → Task 2 ✓
- §9 File changes → Tasks 1, 2, 3, 4, 5, 6 cover the listed files ✓
- §10 Test plan → engine tests in Task 2; API smoke test in Task 4; UI dogfood in Task 7 ✓
- §11 Migration & rollback → Task 1 patch is reload-only + new fields default-blank; rollback = `hidden=0` on commission_lines and remove pivot field ✓
- §12 Open questions → resolved inline (sticky CSS via plain `position:sticky`; ctrl+click bound in cell handler; history is `add_comment` on parent; "Open Line" link not added — defer to user feedback)

**Placeholders:** None.

**Type consistency:** `line` object passed across Tasks 3-6 always has `.name, .component, .amount, .state, .billing_schedule_idx, .override_rate, .posted_by_cell, .skip_reason`. `pakd_doc` always has `.name, .company, .commission_lines, .commission_overrides, .contract_ref, .sales_person`. API endpoint return shapes consistent with §5 of the spec.

**Scope check:** Single feature, single plan. ~7 commits. Inline-executable in one main session.
