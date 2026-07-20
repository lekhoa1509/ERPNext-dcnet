frappe.ui.form.on("Phuong An Kinh Doanh", {
	contract_ref: function (frm) {
		if (!frm.doc.contract_ref) return;
		frappe.call({
			method: "frappe.client.get",
			args: { doctype: "DCNet Contract", name: frm.doc.contract_ref },
			callback: function (r) {
				if (!r.message) return;
				const c = r.message;
				frm.set_value("customer", c.customer);
				frm.set_value("customer_name", c.customer_name);
				frm.set_value("sales_person", c.sales_person);
				frm.set_value("department", c.department);
				frm.set_value("branch", c.branch);
				frm.set_value("company", c.company);
				frm.set_value("service_type", c.service_type);
				frm.set_value("channel", c.channel);
				frm.set_value("project_category", c.project_category);
				frm.set_value("contract_no_external", c.contract_no_external);

				// Map service_type → pakd_type
				if (!frm.doc.pakd_type) {
					// v0.2.0 D4: every recurring service (including FTTH DN per HD)
					// now maps to Recurring Telecom — Monthly FTTH Rollup option removed.
					const map = {
						"FTTH": "Recurring Telecom",
						"Leased Line": "Recurring Telecom",
						"P2P": "Recurring Telecom",
						"Colocation": "Recurring Telecom",
						"VTTB": "One-off Sale/Project",
					};
					const mapped = map[c.service_type];
					if (mapped) frm.set_value("pakd_type", mapped);
				}

				// Items: auto-fill ONLY if PAKD has no items yet (fresh selection on a
				// blank form). If items exist, leave them — user can use the
				// "Update from Contract" button to refresh when needed.
				const has_items = (frm.doc.items || []).some(
					(it) => it.item_label || it.qty || it.unit_price
				);
				if (!has_items) {
					_sync_items_from_contract(frm, c);
					frappe.show_alert(
						{ message: __("Items copied from contract"), indicator: "green" },
						5
					);
				}

				// Re-evaluate drift (badge + button label)
				_check_contract_drift(frm);
			},
		});
	},

	pakd_type: function (frm) {
		_toggle_fields(frm);
	},

	refresh: function (frm) {
		_toggle_fields(frm);

		if (frm.doc.contract_ref) {
			frm.add_custom_button(__("View Contract"), function () {
				frappe.set_route("Form", "DCNet Contract", frm.doc.contract_ref);
			});
			_check_contract_drift(frm);
		}

		// 2026-05-12 UX redesign: at-a-glance summary header card
		if (!frm.is_new()) {
			_render_pakd_summary_card(frm);
		} else {
			_render_pakd_empty_card(frm);
		}

		// 2026-05-13 FB-2026-00587: replace commission_lines child table with pivot
		_render_commission_pivot(frm);

		// v0.2.0 §6.3: render bi-directional SI/PE/Commission status table.
		// Looks up Sales Invoice + Payment Entry per billing period via the
		// linked DCNet Contract + custom field dcnet_contract on SI/PE.
		_render_invoice_payment_table(frm);

		// v0.2.0: external commission → PAKD Beneficiary Line kind=Referral.
		// The pivot cell click on a Referral beneficiary row opens the
		// "Đăng JE ngay" popover via post_beneficiary_now. No separate button.
	},

	before_workflow_action(frm) {
		// Intercept Reject workflow action to capture rejection reason via dialog
		if (frm.selected_workflow_action !== "Reject") return;
		return new Promise((resolve, reject) => {
			frappe.prompt(
				{
					fieldname: "reason",
					fieldtype: "Small Text",
					label: __("Lý do từ chối"),
					reqd: 1,
					description: __("Lý do này sẽ được lưu và hiển thị trong thẻ Tóm tắt PAKD."),
				},
				(values) => {
					frappe.call({
						method: "dcnet_pakd.dcnet_pakd.api.set_rejection_reason",
						args: { pakd: frm.doc.name, reason: values.reason },
						callback: () => {
							frm.reload_doc().then(resolve);
						},
						error: reject,
					});
				},
				__("Từ chối PAKD"),
				__("Xác nhận từ chối")
			);
		});
	},
});

// Live-recompute revenue_contract when user edits qty / unit_price in the
// items grid. Server's validate() is still source of truth on save.
frappe.ui.form.on("PAKD Item", {
	qty: (frm, cdt, cdn) => _recompute_row(frm, cdt, cdn),
	unit_price: (frm, cdt, cdn) => _recompute_row(frm, cdt, cdn),
	items_remove: (frm) => _recompute_pakd_totals(frm),
});

function _recompute_row(frm, cdt, cdn) {
	const row = locals[cdt][cdn];
	row.revenue_contract = _compute_item_revenue_contract(frm, row);
	frm.refresh_field("items");
	_recompute_pakd_totals(frm);
}

function _toggle_fields(frm) {
	const is_oneoff = frm.doc.pakd_type === "One-off Sale/Project";
	// qty is 1 for recurring, variable for one-off
	frm.fields_dict["items"].grid.toggle_reqd("qty", is_oneoff);
}

function _sync_items_from_contract(frm, contract_doc) {
	frm.clear_table("items");
	(contract_doc.items || []).forEach((it) => {
		const row = frm.add_child("items");
		row.item_label = it.item_label;
		row.uom = it.uom;
		row.qty = it.qty;
		row.unit_price = it.unit_price;
		// Pre-compute revenue_contract client-side so the value appears immediately.
		// Server's compute_pakd_line() is the auth source on save.
		row.revenue_contract = _compute_item_revenue_contract(frm, row);
	});
	frm.refresh_field("items");
	_recompute_pakd_totals(frm);
}

// Mirror of compute_pakd_line() revenue_contract branch (utils/engine.py).
function _compute_item_revenue_contract(frm, item) {
	return Number(item.qty || 0) * Number(item.unit_price || 0);
}

function _recompute_pakd_totals(frm) {
	const total = (frm.doc.items || []).reduce(
		(s, it) => s + Number(it.revenue_contract || 0), 0
	);
	if (frm.doc.total_revenue_contract !== total) {
		frm.set_value("total_revenue_contract", total);
	}
}

// Item signature used for drift detection — order-independent, ignores
// PAKD-only fields (revenue_actual, salary_coefficient, etc).
function _item_signature(items) {
	return (items || [])
		.map((it) => [
			(it.item_label || "").trim(),
			it.uom || "",
			Number(it.qty || 0),
			Number(it.unit_price || 0),
		].join("|"))
		.sort()
		.join(";");
}

function _check_contract_drift(frm) {
	if (!frm.doc.contract_ref) return;
	frappe.db
		.get_doc("DCNet Contract", frm.doc.contract_ref)
		.then((contract) => {
			const pakd_sig = _item_signature(frm.doc.items);
			const contract_sig = _item_signature(contract.items);
			const drifted = pakd_sig !== contract_sig;

			// Remove old button if present (refresh can fire multiple times)
			const base_label = __("Update from Contract");
			Object.keys(frm.custom_buttons || {}).forEach((k) => {
				if (k.indexOf(base_label) === 0) frm.remove_custom_button(k);
			});

			// Show button only when PAKD is editable (Draft, docstatus=0).
			// Submitted PAKDs still show the drift indicator below for audit.
			if (frm.doc.docstatus === 0) {
				const label = drifted ? base_label + " ⚠" : base_label;
				frm.add_custom_button(label, function () {
					frappe.confirm(
						__(
							"This will replace PAKD items with the current contract items ({0} item(s)). Continue?",
							[(contract.items || []).length]
						),
						function () {
							_sync_items_from_contract(frm, contract);
							frm.dirty();
							frappe.show_alert(
								{ message: __("Items updated from contract"), indicator: "green" },
								5
							);
							// Re-evaluate drift after sync
							setTimeout(() => _check_contract_drift(frm), 200);
						}
					);
				});
			}

			// Dashboard indicator when drifted
			frm.dashboard.clear_headline();
			if (drifted) {
				frm.dashboard.set_headline_alert(
					__("Contract has updated items — click 'Update from Contract' to sync"),
					"orange"
				);
			}
		});
}

// ─────────────────────────────────────────────────────────────────────────────
// 2026-05-12 UX redesign: at-a-glance summary header card
// ─────────────────────────────────────────────────────────────────────────────
const _STATE_COLORS = {
	"Draft": "gray",
	"Pending Sales Director": "orange",
	"Pending General Dept": "orange",
	"Pending Branch Director": "orange",
	"Pending Board": "orange",
	"Approved": "green",
	"Rejected": "red",
	"Cancelled": "gray",
};

const _MARGIN_COLORS = { green: "#28a745", amber: "#ffc107", red: "#d9534f" };

function _render_pakd_empty_card(frm) {
	const $w = frm.fields_dict.summary_card && frm.fields_dict.summary_card.$wrapper;
	if (!$w) return;
	$w.html(`
		<div class="dcnet-summary-card dcnet-summary-empty" style="padding:12px; border-radius:8px; background:#f8f9fa; border:1px solid #e2e6ea; color:#6c757d;">
			<div style="font-size:13px;">
				${__("PAKD mới — chọn Hợp đồng và điền hạng mục để bắt đầu.")}
			</div>
		</div>
	`);
}

function _render_pakd_summary_card(frm) {
	const $w = frm.fields_dict.summary_card && frm.fields_dict.summary_card.$wrapper;
	if (!$w) return;
	frappe.call({
		method: "dcnet_pakd.dcnet_pakd.api.get_summary_kpis",
		args: { pakd_name: frm.doc.name },
		callback(r) {
			if (!r.message) return;
			const k = r.message;
			const html = _build_summary_html_pakd(k, frm);
			$w.html(html);
			_wire_pakd_summary_button(frm, k.next_action);
			_promote_pakd_summary_above_dashboard(frm, html);
		},
		error() {
			$w.html(`<div class="text-muted" style="padding:8px;">${__("Không tải được tóm tắt")}</div>`);
		},
	});
}

function _promote_pakd_summary_above_dashboard(frm, html) {
	const $layout = $(frm.wrapper).find('.layout-main-section').first();
	if (!$layout.length) return;
	const $existing = $layout.find('.dcnet-summary-promoted').first();
	const $card = $(`<div class="dcnet-summary-promoted" style="margin: 0 0 12px 0;">${html}</div>`);
	if ($existing.length) {
		$existing.replaceWith($card);
	} else {
		$layout.prepend($card);
	}
	frm.fields_dict.summary_card.$wrapper.closest('.form-section').hide();
	const $btn = $card.find('.dcnet-pakd-summary-action-btn');
	$btn.off('click').on('click', () => {
		frm.fields_dict.summary_card.$wrapper.find('.dcnet-pakd-summary-action-btn').trigger('click');
	});
}

function _build_summary_html_pakd(k, frm) {
	const fmt = (n) => (Number(n) || 0).toLocaleString("vi-VN", { minimumFractionDigits: 0 }) + " ₫";
	const margin_color = _MARGIN_COLORS[k.margin_color] || "inherit";

	const kpi_strip = k.is_empty ? "" : `
		<div class="dcnet-summary-kpis" style="display:flex; gap:24px; flex-wrap:wrap; padding:12px 16px; background:#fff;">
			<div><div class="text-muted" style="font-size:11px;">${__("DT Hợp đồng")}</div><div style="font-size:15px; font-weight:600;">${fmt(k.total_revenue_contract)}</div></div>
			<div><div class="text-muted" style="font-size:11px;">${__("Tổng CP")}</div><div style="font-size:15px; font-weight:600;">${fmt(k.total_cost)}</div></div>
			<div><div class="text-muted" style="font-size:11px;">${__("Tổng DT DV")}</div><div style="font-size:15px; font-weight:600;">${fmt(k.total_revenue_service)}</div></div>
			<div><div class="text-muted" style="font-size:11px;">${__("Hoa hồng")}</div><div style="font-size:15px; font-weight:600;">${fmt(k.total_sales_commission)}${k.effective_commission_pct ? ` <span style="font-size:11px; color:#6a737d; font-weight:500;">(${k.effective_commission_pct}%)</span>` : ""}</div></div>
			<div><div class="text-muted" style="font-size:11px;">${__("Biên lãi")}</div><div style="font-size:15px; font-weight:700; color:${margin_color};">${k.margin_pct}%</div></div>
		</div>
	`;

	const drift_line = k.drifted ? `
		<div style="padding:6px 16px 0; font-size:12.5px; color:#d9534f;">
			⚠ ${__("Hạng mục lệch so với hợp đồng")} — ${__("dùng nút 'Cập nhật từ hợp đồng' để đồng bộ")}
		</div>` : "";

	const next_action = _pakd_next_action_line(k.next_action);

	// Skip the card entirely if there's nothing unique to show. Status / customer /
	// NVKD / branch / contract link / pakd_type are all native form fields rendered
	// below — the previous header block duplicated them and was the main source of
	// "thừa thông tin" feedback. KPI strip + drift warning + next action stay
	// because they're NOT in the form.
	if (k.is_empty && !drift_line && !next_action) return "";

	return `
		<div class="dcnet-summary-card" style="border:1px solid #e2e6ea; border-radius:8px; overflow:hidden; margin-bottom:12px;">
			${kpi_strip}
			<div style="padding:8px 16px 10px; background:#fff;${kpi_strip ? ' border-top:1px solid #e2e6ea;' : ''}">
				${drift_line}
				${next_action}
			</div>
		</div>
	`;
}

function _pakd_next_action_line(na) {
	if (!na || !na.text) return "";
	const text = frappe.utils.escape_html(na.text);
	const button = na.button_label
		? `<button class="btn btn-xs btn-primary dcnet-pakd-summary-action-btn" data-action="${na.button_action || ''}" style="margin-left:8px;">${frappe.utils.escape_html(na.button_label)}</button>`
		: "";
	return `
		<div style="margin-top:6px; font-size:13px; color:#212529;">
			<span style="color:#0366d6;">►</span> <strong>${__("Việc cần làm")}:</strong> ${text} ${button}
		</div>`;
}

function _wire_pakd_summary_button(frm, next_action) {
	if (!next_action || !next_action.button_label) return;
	const $btn = frm.fields_dict.summary_card.$wrapper.find(".dcnet-pakd-summary-action-btn");
	$btn.off("click").on("click", () => {
		_execute_pakd_summary_action(frm, next_action);
	});
}

function _execute_pakd_summary_action(frm, na) {
	const action = na.button_action;
	const args = na.button_args || {};
	if (action === "navigate") {
		frappe.set_route("Form", args.doctype, args.name);
	} else if (action === "send_approval_reminder") {
		frappe.call({
			method: "dcnet_pakd.dcnet_pakd.api.send_approval_reminder",
			args: { pakd: args.pakd },
			callback(r) {
				if (r.message) {
					frappe.show_alert(
						{ message: __("Đã gửi nhắc duyệt tới {0} người", [r.message.sent]), indicator: "green" },
						5
					);
				}
			},
		});
	} else if (action === "submit_for_approval") {
		frappe.msgprint(__("Bấm 'Submit' ở góc phải để gửi PAKD đi duyệt theo workflow."));
	} else if (action === "post_commission") {
		frappe.msgprint(__("Đăng hoa hồng — chức năng đang chuẩn bị. Liên hệ kế toán để xử lý thủ công."));
	} else if (action === "revise_and_resubmit") {
		frappe.msgprint(__("Sửa nội dung PAKD rồi bấm 'Submit' để gửi lại workflow."));
	} else {
		console.warn("Unhandled PAKD summary action:", action, args);
	}
}


// ─────────────────────────────────────────────────────────────────────────────
// Commission pivot grid (FB-2026-00587)
// Rows: SC + License (commission_lines) + each Beneficiary Line
// Cols: billing periods from contract's billing_schedule
// Cells: amount + status pill; click → Frappe Dialog popover with actions.
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

function round_vnd(n) {
	return Math.round(Number(n) || 0);
}

function _render_commission_pivot(frm) {
	const $w = frm.fields_dict.commission_pivot_html && frm.fields_dict.commission_pivot_html.$wrapper;
	if (!$w || !$w.length) return;

	const lines = frm.doc.commission_lines || [];
	const benef_lines = frm.doc.beneficiary_lines || [];

	if (!lines.length && !benef_lines.length) {
		$w.html(`<div class="text-muted" style="padding:12px;">${__("Chưa có dòng hoa hồng / chi cho phía khách.")}</div>`);
		return;
	}

	// v0.2.0 §4.4: commission_lines holds SC + License only.
	// MS/AC/Referral live in beneficiary_lines (1 row per kind, optional recipient).
	// Pivot rows: SC + License from rule, then one row per beneficiary_line.
	const commission_row_keys = ["Sales Commission", "License Fee"];
	const override_map = {};
	for (const r of (frm.doc.commission_overrides || [])) {
		override_map[r.component] = { override: r.override_rate || 0, template: r.template_rate || 0 };
	}
	const row_labels = {};
	for (const comp of commission_row_keys) {
		const m = override_map[comp] || { override: 0, template: 0 };
		const effective = m.override || m.template;
		const marker = m.override ? ' <span class="text-muted" title="PAKD-wide override">●</span>' : '';
		row_labels[comp] = `${comp} <span class="text-muted">${effective}%</span>${marker}`;
	}

	// Beneficiary line rows — key prefixed "BL:" + line.name so they're unique
	// from commission keys; label shows kind + recipient + rate.
	const beneficiary_row_keys = [];
	const benef_by_key = {};
	for (const bl of benef_lines) {
		const key = `BL:${bl.name}`;
		beneficiary_row_keys.push(key);
		benef_by_key[key] = bl;
		const recipient = bl.recipient_name ? ` · ${frappe.utils.escape_html(bl.recipient_name)}` : "";
		const tncn = (bl.recipient_tax_pct && bl.recipient_name)
			? ` <span class="text-muted">(TNCN ${bl.recipient_tax_pct}%)</span>` : "";
		const recurrence_tag = bl.recurrence === "One-off"
			? ` <span class="dcnet-pakd-tag-oneoff" title="${__("Trả 1 lần")}">1x</span>`
			: "";
		row_labels[key] = `${bl.kind || "?"}${recipient} <span class="text-muted">${bl.rate_pct || 0}%</span>${tncn}${recurrence_tag}`;
	}

	const row_keys = [...commission_row_keys, ...beneficiary_row_keys];

	// Collect period indices from commission_lines + beneficiary_lines billing_schedule_idx
	const col_set = new Set(lines.map(l => l.billing_schedule_idx));
	for (const bl of benef_lines) {
		if (bl.billing_schedule_idx) col_set.add(bl.billing_schedule_idx);
	}
	const col_indices = Array.from(col_set).sort((a, b) => a - b);

	// Look up SI/PE per period via the contract (cached on frm for re-renders).
	// Also resolves period_start_date → revision_idx for the per-period color band.
	const ensure_bs_cache = (cb) => {
		if (frm._dcnet_pivot_bs_cache !== undefined && frm._dcnet_pivot_bs_cache !== null) {
			cb(frm._dcnet_pivot_bs_cache);
			return;
		}
		if (!frm.doc.contract_ref) {
			frm._dcnet_pivot_bs_cache = {};
			cb({});
			return;
		}
		frappe.db.get_doc("DCNet Contract", frm.doc.contract_ref).then(c => {
			const map = {};
			for (const r of (c.billing_schedule || [])) {
				map[r.month_index] = {
					sales_invoice: r.sales_invoice || null,
					state: r.state || null,
					period_start: r.period_start || null,
				};
			}
			frm._dcnet_pivot_bs_cache = map;
			cb(map);
		}).catch(() => {
			frm._dcnet_pivot_bs_cache = {};
			cb({});
		});
	};

	// Map each billing period → revision_idx using PAKD revisions effective_from.
	// Approved revision with latest effective_from ≤ period_start wins. Periods
	// before any Approved revision get revision_idx=null (rendered no color).
	const _resolve_revision_for_period = (period_start) => {
		if (!period_start) return null;
		const revs = (frm.doc.revisions || [])
			.filter(r => r.workflow_state === "Approved" && r.effective_from && r.effective_from <= period_start)
			.sort((a, b) => (a.effective_from < b.effective_from ? 1 : -1));
		return revs.length ? revs[0].revision_idx : null;
	};

	// Stable color palette indexed by revision_idx (cycles after 6). Colors are
	// soft tints so the cell amounts stay readable.
	const _REVISION_BAND_COLORS = [
		"#e6f6ea",  // rev 0 — green
		"#e7f1ff",  // rev 1 — blue
		"#fff5d6",  // rev 2 — yellow
		"#fce8d8",  // rev 3 — orange
		"#f3e8fc",  // rev 4 — purple
		"#fde6ea",  // rev 5 — pink
	];
	const _band_color = (rev_idx) => {
		if (rev_idx === null || rev_idx === undefined) return null;
		return _REVISION_BAND_COLORS[rev_idx % _REVISION_BAND_COLORS.length];
	};

	ensure_bs_cache((bs_map) => {
		// Each cell carries { amount, line, kind }:
		// - commission_line (SC + License): per-(period, component) row from
		//   commission_lines child table. Click → cell popover with post/skip/
		//   override actions (existing v0.1.x behavior).
		// - beneficiary_line (MS/AC/Referral): row from beneficiary_lines.
		//   Per Period: derives amount from rate × period basis for EVERY period.
		//   One-off: shows amount at period_idx==1 only (first paid period).
		//   Cell state = beneficiary_line.state (row-level — see spec deferred
		//   per-period tracking). Click → row-level action via post_beneficiary_now.
		const cell_map = {};
		for (const k of row_keys) cell_map[k] = {};
		for (const l of lines) {
			const k = l.component;
			if (k in cell_map) {
				cell_map[k][l.billing_schedule_idx] = { amount: l.amount || 0, line: l, kind: "commission" };
			}
		}
		for (const k of beneficiary_row_keys) {
			const bl = benef_by_key[k];
			if (!bl) continue;
			const per_period_amount = round_vnd(bl.amount_per_period || 0);
			if (bl.recurrence === "One-off") {
				// Show only at period 1 (first paid period)
				const first_c = col_indices.find(c => c >= 1);
				if (first_c !== undefined) {
					cell_map[k][first_c] = { amount: per_period_amount, line: bl, kind: "beneficiary" };
				}
			} else {
				for (const c of col_indices) {
					if (c < 1) continue;  // skip Setup Fee period
					cell_map[k][c] = { amount: per_period_amount, line: bl, kind: "beneficiary" };
				}
			}
		}

		const col_totals = {}; for (const c of col_indices) col_totals[c] = 0;
		const row_totals = {}; for (const k of row_keys) row_totals[k] = 0;
		let grand = 0;
		const counted_state = new Set(["Pending", "Posted"]);
		for (const k of row_keys) {
			for (const c of col_indices) {
				const cell = cell_map[k][c];
				if (!cell || !counted_state.has(cell.line.state)) continue;
				col_totals[c] = (col_totals[c] || 0) + cell.amount;
				row_totals[k] = (row_totals[k] || 0) + cell.amount;
				grand += cell.amount;
			}
		}

		const css = `
			<style>
				/* Frappe caps .section-head/.section-body at --page-max-width
				   (900px) with higher specificity — the period pivot needs the
				   full form width, so override with !important for the
				   commission + beneficiary sections only. */
				[data-fieldname="section_commission"] .section-head,
				[data-fieldname="section_commission"] .section-body,
				[data-fieldname="section_beneficiary"] .section-head,
				[data-fieldname="section_beneficiary"] .section-body { max-width: none !important; }
				.dcnet-pakd-pivot-wrap { overflow-x: auto; position: relative; }
				.dcnet-pakd-pivot { border-collapse: separate; border-spacing: 0; min-width: 100%; font-size: 13px; }
				.dcnet-pakd-pivot th, .dcnet-pakd-pivot td { border: 1px solid #e9ebef; padding: 6px 10px; vertical-align: middle; }
				.dcnet-pakd-pivot th { background: #fafbfc; font-weight: 600; text-align: left; white-space: nowrap; }
				.dcnet-pakd-pivot th.col-period { text-align: center; min-width: 110px; }
				.dcnet-pakd-pivot td.cell { text-align: right; min-width: 100px; cursor: pointer; transition: background-color 0.1s; }
				.dcnet-pakd-pivot td.cell:hover { background-color: #f6f8fa; outline: 1px solid #c8d1da; outline-offset: -1px; }
				.dcnet-pakd-pivot td.dcnet-pakd-pending  { background: #fafbfc; color: #6a737d; }
				.dcnet-pakd-pivot td.dcnet-pakd-posted   { background: #e6f6ea; color: #1b6b30; }
				.dcnet-pakd-pivot td.dcnet-pakd-cancelled { background: #fceaea; color: #b32424; text-decoration: line-through; }
				.dcnet-pakd-pivot td.dcnet-pakd-skipped  { background: #fff5d6; color: #8a6500; text-decoration: line-through; }
				.dcnet-pakd-pivot tr.totals-row td { background: #f0f3f6; font-weight: 600; text-align: right; }
				.dcnet-pakd-pivot tr.totals-row td:first-child { text-align: left; }
				.dcnet-pakd-pivot tr.totals-row td.grand { background: #e5eaef; }
				.dcnet-pakd-pivot th.sticky-col, .dcnet-pakd-pivot td.sticky-col {
					position: sticky; left: 0; background: #fafbfc; z-index: 2;
				}
				.dcnet-pakd-pivot th.sticky-col-right, .dcnet-pakd-pivot td.sticky-col-right {
					position: sticky; right: 0; background: #f0f3f6; z-index: 2;
				}
				.dcnet-pakd-pivot td.sticky-col-right.grand { z-index: 3; background: #e5eaef; }
				.dcnet-pakd-status-pill { display: inline-block; margin-left: 6px; font-size: 11px; opacity: 0.9; }
				.dcnet-pakd-cell-by-cell { font-size: 9px; vertical-align: super; margin-left: 2px; opacity: 0.7; }
				.dcnet-pakd-col-link { display: block; font-size: 11px; color: #0366d6; font-weight: 400; text-decoration: none; margin-top: 2px; }
				.dcnet-pakd-col-link.muted { color: #6a737d; }
				.dcnet-pakd-rev-tag { display: inline-block; font-size: 10px; color: #6a737d; font-weight: 500; background: rgba(0,0,0,0.04); padding: 1px 5px; border-radius: 8px; margin-right: 4px; }
				.dcnet-pakd-tag-oneoff { font-size: 10px; padding: 1px 5px; background: #f6f8fa; color: #495057; border-radius: 6px; }
				.dcnet-pakd-rev-legend { font-size: 11px; color: #495057; margin: 8px 0 4px; }
				.dcnet-pakd-rev-legend-swatch { display: inline-block; width: 16px; height: 4px; vertical-align: middle; margin: 0 4px; border-radius: 2px; }
			</style>
		`;

		// Resolve revision_idx per period for the color band + collect distinct
		// revisions in this pivot for the legend.
		const period_revision = {};
		const distinct_revs = new Set();
		for (const c of col_indices) {
			const bs = bs_map[c] || {};
			const rev_idx = _resolve_revision_for_period(bs.period_start);
			period_revision[c] = rev_idx;
			if (rev_idx !== null && rev_idx !== undefined) distinct_revs.add(rev_idx);
		}

		let header_cells = `<th class="sticky-col">${__("Thành phần / Mục")}</th>`;
		for (const c of col_indices) {
			const bs = bs_map[c] || {};
			const rev_idx = period_revision[c];
			const band = _band_color(rev_idx);
			const band_style = band ? ` style="border-top: 4px solid ${band};"` : "";
			let link_html = `<span class="dcnet-pakd-col-link muted">(${__("chưa SI")})</span>`;
			if (bs.sales_invoice) {
				link_html = `<a class="dcnet-pakd-col-link" target="_blank" href="/app/sales-invoice/${encodeURIComponent(bs.sales_invoice)}" onclick="event.stopPropagation();">${frappe.utils.escape_html(bs.sales_invoice)} »</a>`;
			}
			const rev_tag = (rev_idx !== null && rev_idx !== undefined)
				? `<span class="dcnet-pakd-rev-tag" title="${__("Phụ lục")} #${rev_idx}">R${rev_idx}</span>`
				: "";
			header_cells += `<th class="col-period"${band_style}>${__("Kỳ")} ${c} ${rev_tag}${link_html}</th>`;
		}
		header_cells += `<th class="sticky-col-right">${__("Tổng / dòng")}</th>`;

		let body = "";
		for (const k of row_keys) {
			let row = `<tr><th class="sticky-col">${row_labels[k] || k}</th>`;
			for (const c of col_indices) {
				const cell = cell_map[k][c];
				if (!cell) {
					row += `<td></td>`;
					continue;
				}
				const l = cell.line;
				const meta = _PAKD_STATUS_META[l.state] || _PAKD_STATUS_META["Pending"];
				const cell_marker = l.posted_by_cell ? `<sup class="dcnet-pakd-cell-by-cell">c</sup>` : "";
				const kind_attr = ` data-kind="${cell.kind}"`;
				row += `<td class="cell ${meta.className}" data-line="${frappe.utils.escape_html(l.name)}" data-row="${frappe.utils.escape_html(k)}" data-col="${c}"${kind_attr} title="${meta.tooltip}">
					${_fmt_vnd(cell.amount)}
					<span class="dcnet-pakd-status-pill">${meta.icon}${cell_marker}</span>
				</td>`;
			}
			row += `<td class="sticky-col-right">${_fmt_vnd(row_totals[k])}</td>`;
			row += `</tr>`;
			body += row;
		}

		let totals_row = `<tr class="totals-row"><td class="sticky-col">${__("Tổng / kỳ")}</td>`;
		for (const c of col_indices) {
			totals_row += `<td>${_fmt_vnd(col_totals[c])}</td>`;
		}
		totals_row += `<td class="sticky-col-right grand">${_fmt_vnd(grand)}</td>`;
		totals_row += `</tr>`;

		// Revision legend — only shown when ≥1 revision is in play (multiple
		// revisions OR a single revision with explicit Approved state).
		let legend_html = "";
		if (distinct_revs.size) {
			const swatches = Array.from(distinct_revs).sort((a, b) => a - b).map(idx => {
				const c = _band_color(idx);
				return `<span class="dcnet-pakd-rev-legend-swatch" style="background:${c}"></span>R${idx}`;
			}).join(" · ");
			legend_html = `<div class="dcnet-pakd-rev-legend">${__("Phụ lục đang áp dụng")}: ${swatches}</div>`;
		}

		const html = `${css}
			${legend_html}
			<div class="dcnet-pakd-pivot-wrap">
				<table class="dcnet-pakd-pivot">
					<thead><tr>${header_cells}</tr></thead>
					<tbody>${body}${totals_row}</tbody>
				</table>
			</div>`;
		$w.html(html);

		$w.find("td.cell").on("click", (e) => {
			const $cell = $(e.currentTarget);
			const line_name = $cell.data("line");
			const cell_kind = $cell.data("kind") || "commission";
			if (cell_kind === "beneficiary") {
				const bl = (frm.doc.beneficiary_lines || []).find(x => x.name === line_name);
				if (!bl) return;
				_open_beneficiary_popover(frm, bl);
				return;
			}
			const line = (frm.doc.commission_lines || []).find(x => x.name === line_name);
			if (!line) return;
			if (e.ctrlKey || e.metaKey) {
				if (line.state === "Pending") {
					_pivot_post_cell(frm, line);
					return;
				}
			}
			_open_pivot_popover(frm, line, {});
		});
	});
}

function _open_beneficiary_popover(frm, bl) {
	// Beneficiary lines are row-level: state applies to the whole row, not
	// per-period (v0.2.0 deferred per-period tracking). The popover surfaces
	// row totals + a single "Đăng ngay" action that calls post_beneficiary_now.
	const meta = _PAKD_STATUS_META[bl.state] || _PAKD_STATUS_META["Pending"];
	const recipient = bl.recipient_name ? frappe.utils.escape_html(bl.recipient_name) : "—";
	const recipient_id = bl.recipient_id ? frappe.utils.escape_html(bl.recipient_id) : "";
	const tncn_html = (bl.recipient_name && bl.recipient_tax_pct)
		? `<div><strong>${__("TNCN")}:</strong> ${bl.recipient_tax_pct}% — ${__("giữ")} ${_fmt_vnd(bl.pit_amount)} ₫ / kỳ</div>` : "";

	const ref_link = (dt, name) =>
		name ? `<a href="/app/${dt}/${encodeURIComponent(name)}" target="_blank">${frappe.utils.escape_html(name)} »</a>` : "—";

	const refs_html = `
		<div style="margin-top:8px;">
			<strong>${__("Refs")}:</strong><br>
			<small>JE: ${ref_link("journal-entry", bl.journal_entry)}</small><br>
			<small>PE: ${ref_link("payment-entry", bl.payment_entry)}</small>
		</div>
	`;

	const body_html = `
		<div>
			<strong>${__("Loại")}:</strong> ${bl.kind || "?"} ·
			<strong>${__("Người nhận")}:</strong> ${recipient}${recipient_id ? ` (${recipient_id})` : ""}
		</div>
		<div style="margin-top:6px;">
			<strong>${__("Số tiền/kỳ")}:</strong> ${_fmt_vnd(bl.amount_per_period)} ₫
			(${__("Net")}: ${_fmt_vnd(bl.net_amount)} ₫)
		</div>
		${tncn_html}
		<div style="margin-top:6px;"><strong>${__("Trạng thái")}:</strong> ${meta.icon} ${meta.tooltip}</div>
		${refs_html}
		<div style="margin-top:10px; padding:6px 10px; background:#f6f8fa; border-left:3px solid #6a737d; font-size:12px;">
			${__("Beneficiary v0.2.0 — chi cho phía khách hoặc người giới thiệu. Trạng thái áp dụng cho toàn bộ row; theo dõi per-kỳ sẽ bổ sung ở v0.3.0.")}
		</div>
	`;

	const dlg = new frappe.ui.Dialog({
		title: `${bl.kind || "?"} · ${recipient}`,
		fields: [
			{ fieldtype: "HTML", fieldname: "body_html" },
			...(bl.state === "Pending" ? [
				{ fieldtype: "Section Break" },
				{
					fieldtype: "Check",
					fieldname: "non_deductible",
					label: __("Không trừ TNDN (không có HĐ hợp pháp)"),
					default: 1,
					description: __("Mặc định BẬT: PAKD beneficiary là khoản chi cho cá nhân không có HĐ → không trừ TNDN. TẮT nếu có HĐ hợp pháp đính kèm (TT78/2014)."),
				},
			] : []),
		],
		primary_action_label: bl.state === "Pending" ? __("Đăng JE ngay") : __("Đóng"),
		primary_action: (values) => {
			if (bl.state !== "Pending") {
				dlg.hide();
				return;
			}
			frappe.call({
				method: "dcnet_pakd.dcnet_pakd.api.post_beneficiary_now",
				args: {
					beneficiary_line: bl.name,
					non_deductible: values && values.non_deductible ? 1 : 0,
				},
				freeze: true, freeze_message: __("Đăng JE..."),
				callback: (r) => {
					if (r.message) {
						frappe.show_alert({ message: __("Đã đăng JE: {0}", [r.message.journal_entry]), indicator: "green" });
						frm._dcnet_pivot_bs_cache = null;
						frm.reload_doc();
					}
					dlg.hide();
				},
			});
		},
	});
	dlg.fields_dict.body_html.$wrapper.html(body_html);
	dlg.show();
}

function _open_pivot_popover(frm, line, options) {
	options = options || {};
	const meta = _PAKD_STATUS_META[line.state] || _PAKD_STATUS_META["Pending"];
	const title = `${line.component} · ${__("Kỳ")} ${line.billing_schedule_idx}`;

	let rate_source = __("(mặc định mẫu)");
	let effective_rate = null;
	let display_amount = line.amount;
	if (line.override_rate) {
		effective_rate = line.override_rate;
		rate_source = __("(override dòng)");
	} else {
		const ov = (frm.doc.commission_overrides || []).find(r => r.component === line.component);
		if (ov && ov.override_rate) {
			effective_rate = ov.override_rate;
			rate_source = __("(override PAKD-wide)");
		} else if (ov && ov.template_rate) {
			effective_rate = ov.template_rate;
		}
	}

	const ref_link = (dt, name) =>
		name ? `<a href="/app/${dt}/${encodeURIComponent(name)}" target="_blank">${frappe.utils.escape_html(name)} »</a>` : "—";

	const refs_html = `
		<div style="margin-top:8px;">
			<strong>${__("Refs")}:</strong><br>
			<small>JE: ${ref_link("journal-entry", line.journal_entry)}</small><br>
			<small>AS: ${ref_link("additional-salary", line.additional_salary)}</small><br>
			<small>PE: ${ref_link("payment-entry", line.payment_entry)}</small>
		</div>
	`;
	const skip_html = line.state === "Skipped" && line.skip_reason
		? `<div style="margin-top:8px;"><strong>${__("Lý do bỏ qua")}:</strong> ${frappe.utils.escape_html(line.skip_reason)}</div>`
		: "";

	const summary_html = `
		<div>
			<strong>${__("Số tiền")}:</strong> ${_fmt_vnd(display_amount)} ₫ · <strong>${__("Trạng thái")}:</strong> ${meta.icon} ${meta.tooltip}
		</div>
		<div style="margin-top:6px;">
			<strong>${__("Tỷ lệ áp dụng")}:</strong> ${effective_rate || "—"}% ${rate_source}
		</div>
		${refs_html}
		${skip_html}
	`;

	const fields = [{ fieldtype: "HTML", fieldname: "summary", options: summary_html }];
	if (line.state === "Pending") {
		fields.push({
			fieldtype: "Float", fieldname: "override_input",
			label: __("Tuỳ chỉnh tỷ lệ (% — 0 = dùng mặc định)"),
			default: line.override_rate || 0, precision: 2,
		});
	}

	const d = new frappe.ui.Dialog({
		title,
		fields,
		primary_action_label: _primary_action_label(line, frm, options),
		primary_action: () => _primary_action(d, frm, line),
	});

	d.$wrapper.on("shown.bs.modal", () => {
		const $footer = d.$wrapper.find(".modal-footer");
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

function _primary_action_label(line, frm, options) {
	if (line.state === "Pending") {
		const same_col = (frm.doc.commission_lines || [])
			.filter(l => l.billing_schedule_idx === line.billing_schedule_idx && l.state === "Pending");
		return __("Đăng toàn kỳ ({0} dòng)", [same_col.length]);
	}
	if (line.state === "Posted") return __("Mở JE »");
	if (line.state === "Cancelled" || line.state === "Skipped") return __("Khôi phục về Chờ");
	return __("Đóng");
}

function _primary_action(dialog, frm, line) {
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
		const settings_use_hrms = (frappe.boot && frappe.boot.dcnet_pakd_use_hrms) || 0;
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
	if (line.state === "Posted" && line.journal_entry) {
		buttons.push({
			label: __("Đảo bút toán"),
			handler: () => {
				frappe.confirm(
					__("Xoá JE nháp {0}? Nếu JE đã được duyệt sẽ không cho xoá tự động.", [line.journal_entry]),
					() => {
						frappe.db.get_value("Journal Entry", line.journal_entry, "docstatus").then(r => {
							const ds = r.message && r.message.docstatus;
							if (ds === 0) {
								frappe.call({
									method: "frappe.client.delete",
									args: { doctype: "Journal Entry", name: line.journal_entry },
									callback: () => {
										frappe.show_alert({ message: __("Đã xoá JE nháp"), indicator: "green" });
										frm.reload_doc();
									},
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

function _pivot_post_cell(frm, line) {
	frappe.call({
		method: "dcnet_pakd.dcnet_pakd.api.post_pakd_commission_line",
		args: { line_name: line.name },
		freeze: true, freeze_message: __("Đang đăng dòng..."),
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
		freeze: true, freeze_message: __("Đang đăng toàn kỳ..."),
		callback: (r) => {
			if (r.message) {
				const je = r.message.je || "—";
				frappe.show_alert({
					message: __("Đã đăng {0} dòng (JE {1})", [r.message.lines_posted, je]),
					indicator: "green",
				});
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
		__("Bỏ qua dòng này"), __("Lưu")
	);
}

function _pivot_set_override(frm, line, override_rate) {
	frappe.call({
		method: "dcnet_pakd.dcnet_pakd.api.set_pakd_commission_line_override",
		args: { line_name: line.name, override_rate: override_rate },
		freeze: true, freeze_message: __("Đang cập nhật tỷ lệ..."),
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

// ─────────────────────────────────────────────────────────────────────────────
// v0.2.0 §6.3 — Bi-directional SI / PE / Commission status table
// Looks up Sales Invoice + Payment Entry per billing period via the linked
// DCNet Contract + custom fields dcnet_contract / billing_period_idx on SI/PE.
// Same renderer is shared with dcnet_contract.js so the table looks identical
// on both forms; the only difference is the data source for billing_schedule:
//   - PAKD form: fetch the linked DCNet Contract's billing_schedule.
//   - Contract form: read frm.doc.billing_schedule directly.
// ─────────────────────────────────────────────────────────────────────────────

function _render_invoice_payment_table(frm) {
	const $w = frm.fields_dict.invoice_payment_html && frm.fields_dict.invoice_payment_html.$wrapper;
	if (!$w || !$w.length) return;

	if (!frm.doc.contract_ref) {
		$w.html(`<div class="text-muted" style="padding:12px;">${__("Chưa liên kết Hợp đồng.")}</div>`);
		return;
	}

	frappe.db.get_doc("DCNet Contract", frm.doc.contract_ref).then(contract => {
		const bs = contract.billing_schedule || [];
		dcnet_render_invoice_payment_table($w, bs, contract.name, { source: "pakd" });
	}).catch(() => {
		$w.html(`<div class="text-danger" style="padding:12px;">${__("Không tải được lịch billing.")}</div>`);
	});
}

// Module-scope so dcnet_contract.js can reuse via window namespace
window.dcnet_render_invoice_payment_table = function ($w, billing_schedule, contract_name, opts) {
	opts = opts || {};
	if (!Array.isArray(billing_schedule) || !billing_schedule.length) {
		$w.html(`<div class="text-muted" style="padding:12px;">${__("Chưa sinh lịch billing.")}</div>`);
		return;
	}

	// Lazy-load gate: if > 50 SI, render header + collapsed body that loads on demand.
	const total_rows = billing_schedule.length;
	const lazy = total_rows > 50;

	const css = `
		<style>
			.dcnet-ipt-wrap { overflow-x: auto; }
			.dcnet-ipt { border-collapse: separate; border-spacing: 0; width: 100%; font-size: 13px; }
			.dcnet-ipt th, .dcnet-ipt td { border-bottom: 1px solid #e9ebef; padding: 6px 10px; vertical-align: middle; }
			.dcnet-ipt th { background: #fafbfc; font-weight: 600; text-align: left; }
			.dcnet-ipt td.col-amount { text-align: right; min-width: 110px; }
			.dcnet-ipt td.col-status { text-align: center; min-width: 90px; }
			.dcnet-ipt-pill { display: inline-block; padding: 2px 8px; border-radius: 999px; font-size: 11px; font-weight: 500; }
			.dcnet-ipt-pill.paid { background: #e6f6ea; color: #1b6b30; }
			.dcnet-ipt-pill.invoiced { background: #e7f1ff; color: #0a558c; }
			.dcnet-ipt-pill.overdue { background: #fceaea; color: #b32424; }
			.dcnet-ipt-pill.projected { background: #f6f8fa; color: #6a737d; }
			.dcnet-ipt a { color: #0366d6; text-decoration: none; }
			.dcnet-ipt a:hover { text-decoration: underline; }
		</style>
	`;

	const _fmt = (n) => Math.round(Number(n) || 0).toLocaleString("vi-VN");
	const _link = (dt, name) => name
		? `<a href="/app/${dt}/${encodeURIComponent(name)}" target="_blank">${frappe.utils.escape_html(name)} »</a>`
		: '<span class="text-muted">—</span>';

	const _state_pill = (bs) => {
		if (bs.state === "Paid") return `<span class="dcnet-ipt-pill paid">${__("Đã thu")}</span>`;
		if (bs.state === "Invoiced") {
			// Check overdue: due_date < today + state != Paid
			const today = frappe.datetime.now_date();
			if (bs.due_date && bs.due_date < today) {
				return `<span class="dcnet-ipt-pill overdue">${__("Quá hạn")}</span>`;
			}
			return `<span class="dcnet-ipt-pill invoiced">${__("Đã xuất HĐ")}</span>`;
		}
		return `<span class="dcnet-ipt-pill projected">${__("Dự kiến")}</span>`;
	};

	const _render_rows = (peByInvoice, commission_status_by_period) => {
		let body = "";
		for (const row of billing_schedule) {
			const idx = row.month_index;
			const si_name = row.sales_invoice || null;
			const pe_name = si_name && peByInvoice ? (peByInvoice[si_name] || null) : null;
			const commission_state = commission_status_by_period ? (commission_status_by_period[idx] || "") : "";
			body += `<tr>
				<td>${idx}</td>
				<td>${frappe.utils.escape_html(row.item_type || "")}</td>
				<td>${row.due_date ? frappe.datetime.str_to_user(row.due_date) : ""}</td>
				<td class="col-amount">${_fmt(row.amount)}</td>
				<td>${_link("sales-invoice", si_name)}</td>
				<td class="col-status">${_state_pill(row)}</td>
				<td>${_link("payment-entry", pe_name)}</td>
				<td>${commission_state ? frappe.utils.escape_html(commission_state) : '<span class="text-muted">—</span>'}</td>
			</tr>`;
		}
		return `${css}
			<div class="dcnet-ipt-wrap">
				<table class="dcnet-ipt">
					<thead><tr>
						<th>${__("Kỳ")}</th>
						<th>${__("Loại")}</th>
						<th>${__("Hạn thu")}</th>
						<th class="col-amount">${__("Số tiền")}</th>
						<th>${__("Hóa đơn")}</th>
						<th class="col-status">${__("Trạng thái")}</th>
						<th>${__("Thu tiền")}</th>
						<th>${__("Hoa hồng")}</th>
					</tr></thead>
					<tbody>${body}</tbody>
				</table>
			</div>`;
	};

	// Resolve PE per SI in batches (avoid N+1 calls).
	const si_names = billing_schedule.map(r => r.sales_invoice).filter(Boolean);

	const _lookup_pes = () => new Promise((resolve) => {
		if (!si_names.length) return resolve({});
		frappe.db.get_list("Payment Entry", {
			filters: [
				["docstatus", "=", 1],
				["payment_type", "=", "Receive"],
				["dcnet_contract", "=", contract_name],
			],
			fields: ["name", "billing_period_idx"],
			limit: 500,
		}).then(pes => {
			// Build map: billing_period_idx → PE name (use latest PE for each idx)
			const byIdx = {};
			for (const p of pes) {
				if (p.billing_period_idx != null) byIdx[p.billing_period_idx] = p.name;
			}
			// Cross-walk: row.month_index → SI → PE (via byIdx fallback)
			const byInvoice = {};
			for (const r of billing_schedule) {
				if (!r.sales_invoice) continue;
				byInvoice[r.sales_invoice] = byIdx[r.month_index] || null;
			}
			resolve(byInvoice);
		}).catch(() => resolve({}));
	});

	const _lookup_commission_status = () => new Promise((resolve) => {
		// PAKD Commission Line is a child DocType (istable=1) with empty
		// permissions — a direct frappe.db.get_list() 403s even for Admin.
		// Reuse dcnet_contract's whitelisted parent-level endpoint.
		frappe.call({
			method: "dcnet_contract.dcnet_contract.api.get_contract_commission_states",
			args: { contract: contract_name },
			callback: (r) => resolve(r.message || {}),
			error: () => resolve({}),
		});
	});

	if (lazy) {
		$w.html(`<div class="text-muted" style="padding:12px;">
			${__("Hợp đồng có {0} kỳ — bấm để tải bảng đầy đủ.", [total_rows])}
			<button class="btn btn-xs btn-default" style="margin-left:8px;">${__("Tải bảng")}</button>
		</div>`);
		$w.find("button").on("click", () => {
			Promise.all([_lookup_pes(), _lookup_commission_status()]).then(([pes, commission]) => {
				$w.html(_render_rows(pes, commission));
			});
		});
		return;
	}

	Promise.all([_lookup_pes(), _lookup_commission_status()]).then(([pes, commission]) => {
		$w.html(_render_rows(pes, commission));
	});
};
