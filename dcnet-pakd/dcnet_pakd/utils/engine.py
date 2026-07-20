"""Pure rule engine for PAKD commission + beneficiary calculation.

v0.2.0 — split output:
- ``commission_line``: Sales Commission + License Fee (rule-template-driven)
- ``beneficiary_lines``: Manager Services + Add Costs + Referral (PAKD-row-driven)

Backward compatibility: legacy callers that pass MS/AC inside ``rule_components``
still work — they are mapped to the legacy result keys ``manager_services`` /
``add_costs``. New callers pass ``beneficiary_specs`` and read ``beneficiaries``.
NO frappe imports — pure Python for testability.
"""

from typing import Any


# ---------------------------------------------------------------------------
# Rule template resolution (unchanged from v0.1.x)
# ---------------------------------------------------------------------------


def resolve_rule(
	pakd_type: str,
	service_type: str,
	branch: str,
	rules_list: list[dict],
	channel: str = "",
) -> dict | None:
	"""Find the most specific rule template matching the given scope."""
	best = None
	best_score = -1

	for rule in rules_list:
		if rule.get("scope_pakd_type") != pakd_type:
			continue

		rule_service = rule.get("scope_service_type") or ""
		rule_branch = rule.get("scope_branch") or ""
		rule_channel = rule.get("scope_channel") or ""

		if rule_service and rule_service != service_type:
			continue
		if rule_branch and rule_branch != branch:
			continue
		if rule_channel and rule_channel != channel:
			continue

		score = 1
		if rule_service:
			score += 2
		if rule_channel:
			score += 3
		if rule_branch:
			score += 4

		if score > best_score:
			best_score = score
			best = rule

	return best


# ---------------------------------------------------------------------------
# Revision lookup — pick the Approved revision active at a given period
# ---------------------------------------------------------------------------


def resolve_active_revision(revisions: list[dict], period_start_date) -> dict | None:
	"""Pick the most recent Approved revision whose effective_from ≤ period.

	Args:
		revisions: list of PAKD Revision dicts with ``effective_from``,
			``workflow_state``, ``revision_idx``.
		period_start_date: a ``datetime.date`` (caller normalizes from Frappe Date).

	Returns the active revision dict, or ``None`` if no Approved revision exists
	yet at the given period (commission deferred until first approval).
	"""
	approved = [
		r for r in (revisions or [])
		if r.get("workflow_state") == "Approved"
		and r.get("effective_from")
		and r["effective_from"] <= period_start_date
	]
	if not approved:
		return None
	return max(approved, key=lambda r: r["effective_from"])


# ---------------------------------------------------------------------------
# Base computation — supports both v0.1.x legacy names and v0.2.0 explicit names
# ---------------------------------------------------------------------------


# Map every accepted rate_base / base_formula token onto a canonical name so the
# engine can ship clear identifiers (contract_minus_ac_unit / _total) while
# existing rule template rows + tests keep working.
_BASE_FORMULA_ALIASES = {
	# v0.2.0 canonical names
	"contract_revenue": "contract_revenue",
	"contract_minus_ac_unit": "contract_minus_ac_unit",
	"contract_minus_ac_total": "contract_minus_ac_total",
	"ac_only": "ac_only",
	# legacy aliases (engine v0.1.x — keep so existing rule template rows resolve)
	"unit_price": "contract_revenue",
	"unit_price_minus_add_costs": "contract_minus_ac_unit",
	"add_costs_gross": "ac_only",
}


def _canonical_base(formula: str) -> str:
	return _BASE_FORMULA_ALIASES.get(formula or "", formula or "")


def _compute_base(formula: str, line: dict, ctx: dict | None = None) -> float:
	"""Compute the base amount for a component based on rate_base/base_formula.

	Args:
		formula: rate_base name (canonical or legacy alias).
		line: PAKD Item dict — needs qty, unit_price, add_costs_unit_price,
			optional revenue_actual.
		ctx: optional pass-through context. Currently used for
			``ac_total`` (precomputed Add Costs total), which lets
			``contract_minus_ac_total`` subtract the AC total rather than the
			AC unit price. ``None`` falls back to 0 (which then matches the
			revenue value — caller must ensure AC has been computed when this
			formula is used).
	"""
	qty = float(line.get("qty", 1))
	unit_price = float(line.get("unit_price", 0))
	ac_unit_price = float(line.get("add_costs_unit_price", 0))
	ac_total = float((ctx or {}).get("ac_total", 0))

	canonical = _canonical_base(formula)
	if canonical == "contract_revenue":
		return unit_price * qty
	if canonical == "contract_minus_ac_unit":
		return (unit_price - ac_unit_price) * qty
	if canonical == "contract_minus_ac_total":
		# Mẫu 03 MS: F19 = D19 × (F16 − F20)
		# = MS_rate × (revenue_total − AC_total)
		# AC_total comes from prior pass over beneficiary_lines.
		return unit_price * qty - ac_total
	if canonical == "ac_only":
		return ac_unit_price * qty
	return 0.0


# ---------------------------------------------------------------------------
# Commission + beneficiary computation
# ---------------------------------------------------------------------------


def _round_money(value: float) -> float:
	"""Round to nearest VND (no fractions). Frappe Currency stores 2 decimals
	but VN accounting rounds to đồng for invoices; keep 0 decimal here so the
	UI display matches manual Excel calc."""
	return round(value, 2)


def compute_pakd_line(
	line_data: dict,
	header_data: dict,
	rule_components: list[dict],
	beneficiary_specs: list[dict] | None = None,
	overrides: dict[str, float] | None = None,
) -> dict:
	"""Compute commission + beneficiary fields for a single PAKD Item line.

	Args:
		line_data: PAKD Item dict — qty, unit_price, add_costs_unit_price.
		header_data: PAKD header dict — pakd_type (informational only in v0.2.0).
		rule_components: rule template components. Engine v0.2.0 only acts on
			``Sales Commission`` + ``License Fee`` entries here; legacy
			``Manager Services`` / ``Add Costs`` entries are honored as fallback
			when ``beneficiary_specs`` is empty (legacy compat).
		beneficiary_specs: PAKD Beneficiary Line dicts — kind / rate_pct /
			rate_base / recipient_name / recipient_tax_pct / row_name. When
			non-empty, takes precedence over MS/AC entries in rule_components.
		overrides: optional ``{component_name: override_rate}`` for the
			rule-template-driven components. Blank/0 falls through to template.

	Returns:
		{
		  "revenue_contract": float,
		  "sales_commission": float,     # SC component amount (per-period or total)
		  "license_fee": float,          # License Fee amount
		  "beneficiaries": [
		    {"kind": ..., "row_name": ..., "amount": ..., "pit_amount": ...,
		     "net_amount": ...},
		    ...
		  ],
		  "manager_services": float,     # legacy convenience (sum of Manager Services beneficiaries)
		  "add_costs": float,            # legacy convenience (sum of Add Costs beneficiaries)
		  "total_cost": float,
		  "revenue_service": float,
		}
	"""
	qty = float(line_data.get("qty", 1))
	unit_price = float(line_data.get("unit_price", 0))

	revenue_contract = unit_price * qty
	overrides = overrides or {}
	beneficiary_specs = beneficiary_specs or []

	result: dict[str, Any] = {
		"revenue_contract": revenue_contract,
		"sales_commission": 0.0,
		"license_fee": 0.0,
		"beneficiaries": [],
		"manager_services": 0.0,
		"add_costs": 0.0,
	}

	# ── Pass 1: compute AC first (its base is independent of other totals)
	# AC populates ctx['ac_total'] so subsequent beneficiaries that use
	# contract_minus_ac_total subtract the correct AC total. If
	# beneficiary_specs has no Add Costs row, fall back to legacy rule_components
	# Add Costs entry (so older PAKD docs that never moved to beneficiary_lines
	# still produce a number).
	ctx: dict[str, Any] = {"ac_total": 0.0}
	ac_total = 0.0
	ac_spec_seen = False
	for spec in beneficiary_specs:
		if spec.get("kind") == "Add Costs":
			ac_spec_seen = True
			rate_pct = float(spec.get("rate_pct") or 0)
			base = _compute_base(spec.get("rate_base", "ac_only"), line_data, ctx)
			ac_total = _round_money(base * rate_pct / 100.0)
			break
	if not ac_spec_seen:
		for comp in rule_components:
			if comp.get("component_name") == "Add Costs":
				rate_pct = float(comp.get("rate") or 0)
				base = _compute_base(comp.get("base_formula", "ac_only"), line_data, ctx)
				ac_total = _round_money(base * rate_pct / 100.0)
				break
	ctx["ac_total"] = ac_total

	# ── Pass 2: walk beneficiary_specs to produce the beneficiaries list. AC
	# row is included in this pass so its row + recipient fields land in output.
	if beneficiary_specs:
		for spec in beneficiary_specs:
			kind = spec.get("kind") or ""
			rate_pct = float(spec.get("rate_pct") or 0)
			rate_base = spec.get("rate_base") or "contract_revenue"
			if kind == "Add Costs":
				amount = ac_total
			else:
				base = _compute_base(rate_base, line_data, ctx)
				amount = _round_money(base * rate_pct / 100.0)

			tax_pct = float(spec.get("recipient_tax_pct") or 0)
			has_recipient = bool(spec.get("recipient_name"))
			pit_amount = _round_money(amount * tax_pct / 100.0) if has_recipient else 0.0
			net_amount = amount - pit_amount

			result["beneficiaries"].append({
				"kind": kind,
				"row_name": spec.get("row_name") or spec.get("name") or "",
				"rate_base": rate_base,
				"rate_pct": rate_pct,
				"amount": amount,
				"pit_amount": pit_amount,
				"net_amount": net_amount,
			})
			if kind == "Manager Services":
				result["manager_services"] += amount
			elif kind == "Add Costs":
				result["add_costs"] += amount

	# ── Pass 3: walk rule_components for SC + License (and legacy MS/AC when
	# no beneficiary_spec for them exists). Apply per-PAKD overrides on rate.
	seen_kinds = {b["kind"] for b in result["beneficiaries"]}
	for comp in rule_components:
		name = comp.get("component_name", "")
		template_rate = float(comp.get("rate") or 0)
		override_rate = overrides.get(name)
		rate_pct = override_rate if override_rate else template_rate
		formula = comp.get("base_formula", "")
		base = _compute_base(formula, line_data, ctx)
		amount = _round_money(base * rate_pct / 100.0)

		if name == "Sales Commission":
			result["sales_commission"] = amount
		elif name == "License Fee":
			result["license_fee"] = amount
		elif name == "Manager Services" and "Manager Services" not in seen_kinds:
			# Legacy path: no beneficiary_spec for MS, but rule template has one.
			# Mirror to both the result["manager_services"] convenience key and
			# the beneficiaries list so downstream sums see one source of truth.
			result["manager_services"] = amount
			result["beneficiaries"].append({
				"kind": "Manager Services",
				"row_name": "",
				"rate_base": _canonical_base(formula),
				"rate_pct": rate_pct,
				"amount": amount,
				"pit_amount": 0.0,
				"net_amount": amount,
			})
		elif name == "Add Costs" and "Add Costs" not in seen_kinds:
			result["add_costs"] = amount
			# AC already added to ac_total in Pass 1 (legacy path); make sure
			# the beneficiary list reflects it so the output shape is consistent.
			result["beneficiaries"].append({
				"kind": "Add Costs",
				"row_name": "",
				"rate_base": _canonical_base(formula),
				"rate_pct": rate_pct,
				"amount": amount,
				"pit_amount": 0.0,
				"net_amount": amount,
			})

	# ── Totals
	benef_total = sum(b["amount"] for b in result["beneficiaries"])
	result["total_cost"] = _round_money(
		result["sales_commission"] + result["license_fee"] + benef_total
	)
	result["revenue_service"] = _round_money(revenue_contract - result["total_cost"])

	return result
