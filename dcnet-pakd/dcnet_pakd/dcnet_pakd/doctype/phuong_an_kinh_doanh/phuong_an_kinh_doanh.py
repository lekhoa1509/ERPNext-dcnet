import frappe
from frappe import _
from frappe.model.document import Document

from dcnet_pakd.utils.engine import compute_pakd_line, resolve_rule


class PhuongAnKinhDoanh(Document):
	def validate(self):
		self._validate_contract_not_cancelled()
		self._validate_unique_pakd_per_contract()
		self._sync_commission_overrides()
		self._compute_items()
		self._compute_totals()
		self._sync_commission_lines()
		self._sync_sidebar_flags()

	def _sync_sidebar_flags(self):
		"""Maintain has_pending_revision + has_referral_pending so the
		vn_accounting sidebar filters land on the right rows."""
		pending_states = {"Draft", "Pending Sales Director", "Pending General Dept",
		                   "Pending Branch Director", "Pending Board"}
		self.has_pending_revision = 1 if any(
			(r.workflow_state or "") in pending_states for r in (self.revisions or [])
		) else 0
		self.has_referral_pending = 1 if any(
			(bl.kind == "Referral" and (bl.state or "Pending") == "Pending")
			for bl in (self.beneficiary_lines or [])
		) else 0

	def _validate_contract_not_cancelled(self):
		if self.contract_ref:
			status = frappe.db.get_value("DCNet Contract", self.contract_ref, "status")
			if status == "Cancelled":
				frappe.throw(_("Contract has been cancelled, cannot create/edit PAKD"))

	def _validate_unique_pakd_per_contract(self):
		if not self.contract_ref:
			return
		existing = frappe.db.exists(
			"Phuong An Kinh Doanh",
			{
				"contract_ref": self.contract_ref,
				"workflow_state": ["!=", "Cancelled"],
				"name": ["!=", self.name],
			},
		)
		if existing:
			frappe.throw(_("PAKD already exists for contract {0}").format(self.contract_ref))

	def _compute_items(self):
		"""Use rule engine to compute cost fields on each PAKD Item + write back
		beneficiary line totals at the PAKD parent level."""
		rule = self._get_rule()
		components = []
		if rule:
			components = [
				{
					"component_name": c.component_name,
					"rate": c.rate,
					"base_formula": c.base_formula,
				}
				for c in rule.get("components", [])
			]

		# Build per-component override map from the PAKD's commission_overrides
		# table. Blank Frappe Percent round-trips through DB as 0 → treated as
		# "use template rate" (UI label: "Để trống = dùng mẫu").
		overrides = {
			row.component: row.override_rate
			for row in (self.commission_overrides or [])
			if row.override_rate
		}

		# v0.2.0: beneficiary_lines at PAKD parent (MS/AC/Referral). Pass
		# through to engine so MS rate_base + recipient TNCN are respected.
		beneficiary_specs = [
			{
				"row_name": bl.name,
				"kind": bl.kind,
				"rate_pct": bl.rate_pct or 0,
				"rate_base": bl.rate_base or "contract_revenue",
				"recipient_name": bl.recipient_name,
				"recipient_tax_pct": bl.recipient_tax_pct or 0,
			}
			for bl in (self.beneficiary_lines or [])
		]

		header_data = {"pakd_type": self.pakd_type}

		# Track beneficiary amounts per row_name across items (typically 1 item)
		benef_totals: dict[str, dict[str, float]] = {}

		for item in self.items:
			line_data = {
				"qty": item.qty or 1,
				"unit_price": item.unit_price or 0,
				"add_costs_unit_price": item.add_costs_unit_price or 0,
			}
			result = compute_pakd_line(
				line_data, header_data, components,
				beneficiary_specs=beneficiary_specs,
				overrides=overrides,
			)
			item.revenue_contract = result["revenue_contract"]
			item.add_costs = result["add_costs"]
			item.manager_services = result["manager_services"]
			item.license_fee = result["license_fee"]
			item.sales_commission = result["sales_commission"]
			item.total_cost = result["total_cost"]
			item.revenue_service = result["revenue_service"]

			# Accumulate beneficiary amounts back to each PAKD Beneficiary Line
			for b in result["beneficiaries"]:
				key = b.get("row_name") or ""
				if not key:
					continue
				agg = benef_totals.setdefault(key, {"amount": 0.0, "pit_amount": 0.0, "net_amount": 0.0})
				agg["amount"] += b["amount"]
				agg["pit_amount"] += b["pit_amount"]
				agg["net_amount"] += b["net_amount"]

		# Write back to each beneficiary_line row so the form shows amounts
		for bl in (self.beneficiary_lines or []):
			agg = benef_totals.get(bl.name, {"amount": 0.0, "pit_amount": 0.0, "net_amount": 0.0})
			bl.amount_per_period = round(agg["amount"], 2)
			bl.pit_amount = round(agg["pit_amount"], 2)
			bl.net_amount = round(agg["net_amount"], 2)

	def _compute_totals(self):
		"""Sum item-level computed fields into header totals + compute margin."""
		self.total_revenue_contract = sum(i.revenue_contract or 0 for i in self.items)
		self.total_add_costs = sum(i.add_costs or 0 for i in self.items)
		self.total_manager_services = sum(i.manager_services or 0 for i in self.items)
		self.total_license_fee = sum(i.license_fee or 0 for i in self.items)
		self.total_sales_commission = sum(i.sales_commission or 0 for i in self.items)
		self.total_cost = sum(i.total_cost or 0 for i in self.items)
		self.total_revenue_service = sum(i.revenue_service or 0 for i in self.items)

		# Margin % displayed in Tổng tính toán & biên lãi section + summary card
		tr_service = float(self.total_revenue_service or 0)
		total_cost = float(self.total_cost or 0)
		self.margin_pct = round((tr_service - total_cost) / tr_service * 100, 1) if tr_service else 0

		# Effective commission % = how much of contract revenue NVKD actually receives
		tr_contract = float(self.total_revenue_contract or 0)
		total_commission = float(self.total_sales_commission or 0)
		self.effective_commission_pct = round(total_commission / tr_contract * 100, 2) if tr_contract else 0

		# external_commission_* flat block removed in v0.2.0 (replaced by
		# PAKD Beneficiary Line kind=Referral). _compute_external_commission()
		# no longer exists.

	def _sync_commission_overrides(self):
		"""Keep ``commission_overrides`` in sync with the current rule template.

		Ensures one row per component defined on the matched rule template,
		refreshing ``template_rate`` to the current value. User-entered
		``override_rate`` values are preserved. Rows for components no longer
		in the template are dropped.
		"""
		rule = self._get_rule()
		if not rule:
			# No matching rule yet (scope not resolved) — leave any existing rows
			# untouched so user-entered overrides aren't lost while config is in flux.
			return

		template_rates = {c.component_name: float(c.rate or 0) for c in rule.get("components", [])}
		existing = {row.component: row for row in (self.commission_overrides or [])}

		# Update template_rate on existing rows; collect components missing rows
		missing = []
		for comp_name, tpl_rate in template_rates.items():
			row = existing.get(comp_name)
			if row is not None:
				row.template_rate = tpl_rate
			else:
				missing.append((comp_name, tpl_rate))

		# Drop rows whose component is no longer in the template
		self.commission_overrides = [
			r for r in (self.commission_overrides or []) if r.component in template_rates
		]

		# Append rows for newly-introduced components
		for comp_name, tpl_rate in missing:
			self.append("commission_overrides", {
				"component": comp_name,
				"template_rate": tpl_rate,
				"override_rate": None,
			})

	def _get_rule(self):
		"""Find the best matching commission rule template."""
		templates = frappe.get_all(
			"PAKD Commission Rule Template",
			fields=[
				"name",
				"scope_pakd_type",
				"scope_service_type",
				"scope_branch",
				"scope_channel",
			],
		)
		rules_list = []
		for t in templates:
			rules_list.append({
				"template_name": t.name,
				"scope_pakd_type": t.scope_pakd_type,
				"scope_service_type": t.scope_service_type or "",
				"scope_branch": t.scope_branch or "",
				"scope_channel": t.scope_channel or "",
			})

		matched = resolve_rule(
			self.pakd_type,
			self.service_type or "",
			self.branch or "",
			rules_list,
			channel=self.channel or "",
		)
		if not matched:
			return None

		# Load full template with components
		doc = frappe.get_cached_doc("PAKD Commission Rule Template", matched["template_name"])
		return doc

	def _sync_commission_lines(self):
		"""Keep `commission_lines` in sync with Contract billing_schedule + totals.

		Runs on every save (validate hook) so Pending rows are visible as a preview
		on Draft — sales rep can sanity-check commission split before sending for
		approval. Posted rows are preserved untouched; Pending rows are updated in
		place or dropped when no longer needed.

		1 line per (billing_period × cost_component), skip month_index=0 (setup fee).
		"""
		if not self.contract_ref:
			return

		try:
			contract = frappe.get_cached_doc("DCNet Contract", self.contract_ref)
		except frappe.DoesNotExistError:
			return
		billing_schedule = contract.get("billing_schedule", []) or []
		if not billing_schedule:
			return

		# v0.2.0 §4.4: commission_lines only holds Sales Commission + License Fee.
		# Manager Services / Add Costs / Referral live in beneficiary_lines (synced
		# separately via _sync_beneficiary_state). Legacy total_manager_services /
		# total_add_costs values are kept on the parent for header KPI display.
		component_amounts = {}
		if self.total_license_fee:
			component_amounts["License Fee"] = self.total_license_fee
		if self.total_sales_commission:
			component_amounts["Sales Commission"] = self.total_sales_commission

		needed: dict[tuple, float] = {}
		for period in billing_schedule:
			# v0.2.0: skip Setup Fee rows (no commission). Both One-off Goods + Service rows
			# generate commission. Backward compat: legacy bs rows without item_type fall
			# back to the month_index==0 setup-fee rule.
			if (period.get("item_type") or "") == "Setup Fee":
				continue
			if not period.get("item_type") and period.month_index == 0:
				continue
			for comp_name, amount in component_amounts.items():
				if not amount:
					continue
				needed[(period.month_index, comp_name)] = amount

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
		# The engine already applied upstream_rate when computing self.total_*;
		# this rescale is the diff layer for individual-line overrides.
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
