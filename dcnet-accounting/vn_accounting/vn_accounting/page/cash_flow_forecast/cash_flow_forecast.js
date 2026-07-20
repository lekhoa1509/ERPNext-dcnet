frappe.pages["cash-flow-forecast"].on_page_load = function (wrapper) {
	const page = frappe.ui.make_app_page({
		parent: wrapper,
		title: __("Cash Flow Forecast"),
		single_column: true,
	});
	new CashFlowForecast(page);
};

class CashFlowForecast {
	constructor(page) {
		this.page = page;
		this.entries = [];
		this.errors = [];
		this.opening_balance = 0;
		this.threshold = 500000000;
		this.historical = [];
		this.confidence_levels = ["overdue", "committed", "probable", "possible"];
		this.active_confidence = new Set(this.confidence_levels);
		this.active_sources = new Set();
		this.all_sources = [];

		this._granularity = "monthly";
		this._period = "12";
		this._history = "0";
		this._company = frappe.defaults.get_user_default("Company") || "";

		// Detail table state (D2 server-side paginated)
		this.detail_search = "";
		this.detail_page = 1;
		this.detail_page_size = 20;
		this.selected_period = null;

		this.setup_page();
		this.load_data();
	}

	setup_page() {
		this.page.wrapper.addClass("forecast-page");
		this.filters = {};

		// ── Filter row: Frappe-native page-form fields ────────────
		this.filters.granularity = this.page.add_field({
			fieldname: "granularity",
			label: __("Granularity"),
			fieldtype: "Select",
			options: `${__("By Month")}\n${__("By Week")}`,
			default: __("By Month"),
			change: () => {
				const v = this.filters.granularity.get_value();
				this._granularity = (v === __("By Week")) ? "weekly" : "monthly";
				this._update_period_label();
				this.load_data();
			},
		});

		this.filters.period = this.page.add_field({
			fieldname: "period",
			label: __("Forecast Periods"),
			fieldtype: "Select",
			options: Array.from({ length: 12 }, (_, i) => String(i + 1)).join("\n"),
			default: "12",
			change: () => {
				this._period = this.filters.period.get_value();
				this.load_data();
			},
		});

		this.filters.history = this.page.add_field({
			fieldname: "history",
			label: __("History Periods"),
			fieldtype: "Select",
			options: ["0", ...Array.from({ length: 12 }, (_, i) => String(i + 1))].join("\n"),
			default: "0",
			change: () => {
				this._history = this.filters.history.get_value();
				this.load_data();
			},
		});

		this.filters.company = this.page.add_field({
			fieldname: "company",
			label: __("Company"),
			fieldtype: "Link",
			options: "Company",
			default: this._company,
			change: () => {
				this._company = this.filters.company.get_value();
				this.load_data();
			},
		});

		// Source: Frappe MultiSelectList — checkbox dropdown with persistent state.
		// Items are grouped by direction (Thu / Chi / Cả hai) inside the dropdown.
		this.filters.sources = this.page.add_field({
			fieldname: "sources",
			label: __("Sources"),
			fieldtype: "MultiSelectList",
			get_data: () => this._sorted_sources_for_picker(),
			change: () => {
				const rows = this.filters.sources.get_value() || [];
				this.active_sources = rows.length ? new Set(rows) : new Set(this.all_sources);
				this.render();
				this.detail_page = 1;
				this._reload_detail_table();
			},
		});
		this._patch_sources_dropdown_grouping();

		// Confidence: same checkbox-dropdown pattern. Pre-select all 4 levels so
		// the page loads with no filter applied but the boxes are visibly ticked.
		const conf_labels = {
			overdue: __("Overdue"),
			committed: __("Committed"),
			probable: __("Probable"),
			possible: __("Possible"),
		};
		this.filters.confidence = this.page.add_field({
			fieldname: "confidence",
			label: __("Confidence"),
			fieldtype: "MultiSelectList",
			get_data: () => this.confidence_levels.map((c) => ({
				value: c,
				label: conf_labels[c] || c,
				description: "",
			})),
			change: () => {
				const rows = this.filters.confidence.get_value() || [];
				this.active_confidence = rows.length ? new Set(rows) : new Set(this.confidence_levels);
				this.render();
				this.detail_page = 1;
				this._reload_detail_table();
			},
		});
		// Force re-apply translated labels (same fix as Sources) — without
		// this, _selected_values from set_value([...strings]) renders as
		// raw "overdue" / "committed" instead of "Quá Hạn" / "Cam Kết".
		this._patch_confidence_dropdown_labels(conf_labels);
		// Initial default-select happens once cells are loaded — see
		// _update_source_dropdowns. Setting it here would fire `change` before
		// _cells exists and crash render().

		// Add visible labels above each native page-field (page.add_field omits
		// labels for Select fields so users see only the value).
		this._inject_filter_labels({
			granularity: __("Granularity"),
			period: __("Forecast"),
			history: __("History"),
			company: __("Company"),
			sources: __("Sources"),
			confidence: __("Confidence"),
		});

		// ── Action menu items (Methodology / Settings / Refresh / Export) ──
		this.page.add_menu_item(`ℹ ${__("Methodology")}`, () => this._show_methodology());
		this.page.add_menu_item(`⚙ ${__("Settings")}`, () => this._show_settings_dialog());
		this.page.add_menu_item(`↻ ${__("Refresh (clear cache)")}`, () => this._refresh_force());
		this.page.set_secondary_action(`↓ ${__("Excel")}`, () => this.export_excel());

		// ── Content area ──
		this.content = $(`<div class="forecast-content">
			<div class="error-banner" style="display:none"></div>
			<div class="forecast-timestamp"></div>
			<div class="kpi-row"></div>
			<div class="chart-container"></div>
			<div class="pivot-container"></div>
			<div class="detail-container"></div>
		</div>`).appendTo(this.page.main);
	}

	_update_period_label() {
		const lbl = this._granularity === "weekly" ? __("Forecast (weeks)") : __("Forecast (months)");
		this.filters.period.df.label = lbl;
		this.filters.period.refresh_input?.();
		this.filters.period.$wrapper.find("> .forecast-filter-label").text(lbl);
	}

	_inject_filter_labels(map) {
		// Frappe page.add_field renders Select fields without a visible label.
		// Inject a small label span above each field. $wrapper IS the col-md-2
		// container itself in Frappe v16 page-form, so prepending directly puts
		// the label above the input.
		for (const [fieldname, label] of Object.entries(map)) {
			const ctrl = this.filters[fieldname];
			if (!ctrl?.$wrapper) continue;
			if (!ctrl.$wrapper.find("> .forecast-filter-label").length) {
				ctrl.$wrapper.prepend(`<div class="forecast-filter-label">${label}</div>`);
			}
		}
	}

	_show_methodology() {
		frappe.msgprint({
			title: __("Methodology"),
			message: this._get_methodology_html(),
			indicator: "blue",
			wide: true,
		});
	}

	_refresh_force() {
		frappe.xcall("frappe.cache.delete_value", {
			key: `forecast:${this._company}:${this._from_date}:${this._to_date}`,
		}).finally(() => this.load_data());
	}

	_update_source_dropdowns() {
		// Recompute inflow vs outflow source sets from the latest cells data
		// so the dropdown grouping (Thu / Chi / Cả hai) stays correct.
		this._inflow_sources = new Set();
		this._outflow_sources = new Set();
		for (const src_confs of Object.values(this._cells || {})) {
			for (const [src, confs] of Object.entries(src_confs)) {
				for (const amounts of Object.values(confs)) {
					if (amounts.inflow > 0) this._inflow_sources.add(src);
					if (amounts.outflow > 0) this._outflow_sources.add(src);
				}
			}
		}
		// Default-select all on first load so the picker shows every box ticked
		// (matches the active_* Sets the page initializes with). Done here
		// rather than at add_field time because set_value triggers `change` →
		// render(), and render() needs _cells which only exists after load.
		const src = this.filters.sources;
		if (src && (!src.values || !src.values.length) && this.all_sources?.length) {
			src.set_value([...this.all_sources]);
		}
		const conf = this.filters.confidence;
		if (conf && (!conf.values || !conf.values.length)) {
			conf.set_value([...this.confidence_levels]);
		}
	}

	_source_direction(src) {
		const has_in = this._inflow_sources?.has(src);
		const has_out = this._outflow_sources?.has(src);
		if (has_in && !has_out) return "in";
		if (has_out && !has_in) return "out";
		return "both";
	}

	_sorted_sources_for_picker() {
		// Return sources sorted by direction (in → both → out), then by label.
		// Grouping headers are injected by _patch_sources_dropdown_grouping.
		const order = { in: 0, both: 1, out: 2 };
		const items = (this.all_sources || []).map((s) => ({
			value: s,
			label: this._get_source_label ? this._get_source_label(s) : s,
			description: "",
		}));
		items.sort((a, b) => {
			const da = order[this._source_direction(a.value)] ?? 3;
			const db = order[this._source_direction(b.value)] ?? 3;
			return da - db || a.label.localeCompare(b.label);
		});
		return items;
	}

	_patch_confidence_dropdown_labels(label_map) {
		// Override set_selectable_items to re-apply translated labels.
		// MultiSelectList's process_options uses raw values as labels for
		// items coming via set_value([...strings]).
		const ctrl = this.filters.confidence;
		if (!ctrl) return;
		const orig = ctrl.set_selectable_items.bind(ctrl);
		ctrl.set_selectable_items = (options) => {
			options.forEach((opt) => {
				if (label_map[opt.value]) opt.label = label_map[opt.value];
			});
			orig(options);
		};
	}

	_patch_sources_dropdown_grouping() {
		// Override set_selectable_items on this instance to (1) re-sort
		// options by direction (in → both → out) since MultiSelectList
		// internally prepends _selected_values, and (2) inject section
		// headers (Thu / Cả hai / Chi) above each direction group.
		const ctrl = this.filters.sources;
		if (!ctrl) return;
		const orig = ctrl.set_selectable_items.bind(ctrl);
		const order = { in: 0, both: 1, out: 2 };
		const headers = {
			in: __("Inflow sources"),
			out: __("Outflow sources"),
			both: __("Both directions"),
		};
		ctrl.set_selectable_items = (options) => {
			// Re-apply labels — MultiSelectList's process_options uses raw
			// values as labels for items coming via set_value([...strings]),
			// so default-selected sources show "Account" instead of "Chi Phí HĐ".
			options.forEach((opt) => {
				if (this._get_source_label) {
					opt.label = this._get_source_label(opt.value);
				}
			});
			options.sort((a, b) => {
				const da = order[this._source_direction(a.value)] ?? 3;
				const db = order[this._source_direction(b.value)] ?? 3;
				return da - db || (a.label || a.value).localeCompare(b.label || b.value);
			});
			orig(options);
			const $items = ctrl.$list_wrapper.find(".selectable-items");
			let prev = null;
			$items.children(".selectable-item").each((_, el) => {
				const $el = $(el);
				const value = decodeURIComponent($el.attr("data-value") || "");
				const cur = this._source_direction(value);
				if (cur !== prev) {
					$el.before(`<li class="dropdown-header forecast-source-group">${headers[cur] || cur}</li>`);
					prev = cur;
				}
			});
		};
	}

	// ── Data loading ────────────────────────────────────────────

	async load_data() {
		if (!this._company) return;
		frappe.dom.freeze(__("Loading forecast..."));
		try {
			const r = await frappe.xcall("vn_accounting.api.forecast.get_forecast_data", {
				company: this._company,
				months: parseInt(this._period),
				history_months: parseInt(this._history),
				granularity: this._granularity,
			});
			this._cells = r.cells || {};
			this.errors = r.errors || [];
			this.opening_balance = r.opening_balance || 0;
			this.threshold = r.minimum_threshold || 500000000;
			this.historical = r.historical || [];
			this.all_sources = r.sources || [];
			this._from_date = r.from_date;
			this._to_date = r.to_date;
			this.active_sources = new Set(this.all_sources);
			this._update_source_dropdowns();
			this.render();
			this.detail_page = 1;
			this._reload_detail_table();
			this.content.find(".forecast-timestamp").html(
				`<small class="text-muted">${__("Data as of")}: ${frappe.datetime.now_datetime()}</small>`
			);
		} catch (e) {
			frappe.msgprint({ title: __("Error"), message: e.message || String(e), indicator: "red" });
		} finally {
			frappe.dom.unfreeze();
		}
	}

	// ── Rendering ───────────────────────────────────────────────

	_sum_cell(period_key) {
		const src_confs = this._cells[period_key] || {};
		let inflow = 0, outflow = 0, count = 0;
		for (const [src, confs] of Object.entries(src_confs)) {
			if (!this.active_sources.has(src)) continue;
			for (const [conf, amounts] of Object.entries(confs)) {
				if (!this.active_confidence.has(conf)) continue;
				inflow += amounts.inflow || 0;
				outflow += amounts.outflow || 0;
				count += amounts.count || 0;
			}
		}
		return { inflow, outflow, count };
	}

	render() {
		this.render_errors();
		const monthly = this.build_monthly();
		this.render_summary(monthly);
		this.render_chart(monthly);
		this.render_table(monthly);
	}

	render_summary(monthly) {
		const $row = this.content.find(".kpi-row").empty();
		const forecast = monthly.filter((m) => !m.is_historical);
		if (!forecast.length) return;

		const total_in = forecast.reduce((s, m) => s + m.inflow, 0);
		const total_out = forecast.reduce((s, m) => s + m.outflow, 0);
		const net = total_in - total_out;
		const last = forecast[forecast.length - 1];
		const last_closing = last.closing;
		const period_count = forecast.length;
		const period_word = this._granularity === "weekly" ? __("weeks") : __("months");
		const last_label = last.label;

		const performance = total_in > 0
			? `${Math.round((net / total_in) * 100)}%`
			: "—";

		const avg_in = total_in / period_count;
		const avg_out = total_out / period_count;

		const card = (label, value, value_class, footer, icon_html) => `
			<div class="col-md-3">
				<div class="widget widget-box forecast-kpi-card">
					<div class="kpi-label">${label}</div>
					<div class="kpi-value ${value_class}">${value} ${icon_html}</div>
					<div class="kpi-footer text-muted">${footer}</div>
				</div>
			</div>`;

		const arrow_up = `<span class="kpi-icon direction-in">▲</span>`;
		const arrow_down = `<span class="kpi-icon direction-out">▼</span>`;
		const wallet = `<span class="kpi-icon">💼</span>`;

		$row.html(`<div class="row">${
			card(
				__("Closing Balance"),
				this.fmt_short(last_closing),
				"color-balance",
				`${__("Opening:")} ${this.fmt_short(this.opening_balance)} · ${last_label}`,
				wallet,
			) +
			card(
				__("Net Cash Flow"),
				this.fmt_short(net),
				net >= 0 ? "direction-in" : "direction-out",
				`${period_count} ${period_word} · ${__("Performance:")} ${performance}`,
				net >= 0 ? arrow_up : arrow_down,
			) +
			card(
				__("Total Inflow"),
				this.fmt_short(total_in),
				"direction-in",
				`${period_count} ${period_word} · ${__("Avg/period:")} ${this.fmt_short(avg_in)}`,
				arrow_up,
			) +
			card(
				__("Total Outflow"),
				this.fmt_short(total_out),
				"direction-out",
				`${period_count} ${period_word} · ${__("Avg/period:")} ${this.fmt_short(avg_out)}`,
				arrow_down,
			)
		}</div>`);
	}

	render_errors() {
		const $b = this.content.find(".error-banner");
		if (!this.errors.length) { $b.hide(); return; }
		$b.show().html(`<div class="alert alert-warning">
			<strong>${__("Some providers failed")}:</strong>
			${this.errors.map((e) => `<br>${e.provider}: ${e.error}`).join("")}
		</div>`);
	}

	build_monthly() {
		const weekly = this._granularity === "weekly";
		const n = parseInt(this._period || "12");
		const forecast = [];
		let bal = this.opening_balance;

		if (weekly) {
			const today = new Date();
			const monday = new Date(today); monday.setDate(today.getDate() - today.getDay() + 1);
			for (let i = 0; i < n; i++) {
				const d = new Date(monday); d.setDate(monday.getDate() + i * 7);
				const key = this._iso_week_key_from_date(d);
				const { inflow, outflow, count } = this._sum_cell(key);
				const net = inflow - outflow;
				forecast.push({ label: this._week_label(d), key, inflow, outflow, net, opening: bal, closing: bal + net, count, is_historical: false });
				bal += net;
			}
		} else {
			const start = new Date(); start.setDate(1);
			for (let i = 0; i < n; i++) {
				const d = new Date(start); d.setMonth(d.getMonth() + i);
				const key = `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}`;
				const { inflow, outflow, count } = this._sum_cell(key);
				const net = inflow - outflow;
				forecast.push({ label: `T${d.getMonth() + 1}/${d.getFullYear()}`, key, inflow, outflow, net, opening: bal, closing: bal + net, count, is_historical: false });
				bal += net;
			}
		}

		// Prepend historical data
		const hist = this.historical.map((h) => {
			if (h.week) {
				const ws = new Date(h.week_start);
				return { label: this._week_label(ws), key: h.week, inflow: h.inflow, outflow: h.outflow, net: h.inflow - h.outflow, opening: h.opening, closing: h.closing, count: 0, is_historical: true };
			}
			const [y, m] = h.month.split("-");
			return { label: `T${parseInt(m)}/${y}`, key: h.month, inflow: h.inflow, outflow: h.outflow, net: h.inflow - h.outflow, opening: h.opening, closing: h.closing, count: 0, is_historical: true };
		});
		return [...hist, ...forecast];
	}

	_iso_week_key(date_str) {
		const d = new Date(date_str + "T00:00:00");
		return this._iso_week_key_from_date(d);
	}

	_iso_week_key_from_date(d) {
		const tmp = new Date(d.valueOf());
		tmp.setDate(tmp.getDate() + 3 - (tmp.getDay() + 6) % 7);
		const jan4 = new Date(tmp.getFullYear(), 0, 4);
		const week = 1 + Math.round(((tmp - jan4) / 86400000 - 3 + (jan4.getDay() + 6) % 7) / 7);
		return `${tmp.getFullYear()}-W${String(week).padStart(2, "0")}`;
	}

	_week_label(d) {
		const dd = d.getDate(), mm = d.getMonth() + 1;
		return `${dd}/${mm}`;
	}

	render_chart(monthly) {
		const $c = this.content.find(".chart-container").empty();
		if (!monthly.length) return;

		const hc = this.historical.length;

		// Actual values include the boundary point (index hc) so the line
		// reaches the vertical "Hiện hành" divider; without it the actual
		// line stops one step BEFORE the divider.
		const actual_values = monthly.map((m, i) => {
			if (m.is_historical) return m.closing;
			if (i === hc) return m.opening; // = last historical closing
			return null;
		});
		// Forecast values: start at index hc (first forecast period). Its
		// `opening` equals the last historical closing, so the forecast line
		// also begins exactly at the divider — actual ends and forecast
		// starts at the same point.
		const forecast_values = monthly.map((m, i) => {
			if (m.is_historical) return null;
			if (i === hc) return m.opening;  // boundary
			return m.closing;
		});

		new frappe.Chart($("<div></div>").appendTo($c)[0], {
			type: "line",
			height: 320,
			colors: ["#0d6efd", "#7ba6f5", "#28a745", "#dc3545"],
			data: {
				labels: monthly.map((m) => m.label),
				datasets: [
					{ name: __("Actual Balance"),  values: actual_values },
					{ name: __("Forecast Balance"), values: forecast_values },
					{ name: __("Cash Inflow"),     values: monthly.map((m) => m.inflow) },
					{ name: __("Cash Outflow"),    values: monthly.map((m) => m.outflow) },
				],
				yMarkers: [{
					label: __("Minimum Threshold (Balance)"),
					value: this.threshold,
					options: { labelPos: "left" },
				}],
			},
			tooltipOptions: { formatTooltipY: (d) => this.fmt_short(d) },
			axisOptions: { yAxisMode: "tick", shortenYAxisNumbers: true },
			lineOptions: { regionFill: 0, hideDots: 0, dotSize: 3 },
			animate: 0,
		});

		if (hc > 0 && hc < monthly.length) {
			this._add_chart_overlay($c, hc, monthly.length);
		}
		this._dash_forecast_line($c, hc, monthly.length);
	}

	_dash_forecast_line($container, hc, total) {
		// frappe.Chart's draw cycle finalizes paths via rAF + animation. Even
		// with animate:0 it sometimes re-writes path 'd' on the next frame.
		// Use a MutationObserver so our trim+dash re-applies whenever the chart
		// redraws (filter changes, hover labels recalc bounding boxes, etc.).
		const apply = () => {
			const svg = $container.find("svg")[0];
			if (!svg) return false;
			const groups = svg.querySelectorAll(".dataset-units");
			if (groups.length < 2) return false;

			// Both line paths share the same X coordinates — index N corresponds
			// to monthly[N]. We trim Actual to indices [0..hc] and Forecast to
			// indices [hc..total-1] using path 'd' string surgery.
			const trimPath = (path, fromIdx, toIdx) => {
				if (!path) return;
				const d = path.getAttribute("d") || "";
				const segs = d.split(/(?=[LM])/);
				if (!segs.length) return;
				const expectedLen = toIdx - fromIdx + 1;
				if (segs.length === expectedLen) return; // already trimmed — idempotent
				const slice = segs.slice(fromIdx, toIdx + 1);
				if (!slice.length) return;
				slice[0] = "M" + slice[0].slice(1);
				path.setAttribute("d", slice.join(""));
			};

			const actualPath = groups[0].querySelector("path");
			const forecastPath = groups[1].querySelector("path");

			trimPath(actualPath,   0,         hc);
			trimPath(forecastPath, hc,        total - 1);

			// Dotted dots may also exist (one per data point); hide the ones
			// outside the active range so they don't leave dots at zero.
			const trimDots = (group, fromIdx, toIdx) => {
				const dots = group.querySelectorAll("circle, .data-point");
				dots.forEach((d, i) => {
					if (i < fromIdx || i > toIdx) d.style.display = "none";
				});
			};
			trimDots(groups[0], 0, hc);
			trimDots(groups[1], hc, total - 1);

			// Dashed stroke for the forecast line.
			if (forecastPath) {
				forecastPath.setAttribute("stroke-dasharray", "6,4");
			}
			return true;
		};

		// frappe.Chart finishes drawing asynchronously and re-writes path 'd'
		// across multiple animation frames. Poll at 200ms for 6s to catch the
		// final frame; trim is idempotent (skips already-trimmed paths).
		// Cancel any prior poller so successive renders don't pile up.
		if (this._dash_poll_id) {
			clearInterval(this._dash_poll_id);
		}
		let tries = 0;
		this._dash_poll_id = setInterval(() => {
			apply();
			if (++tries >= 30) {
				clearInterval(this._dash_poll_id);
				this._dash_poll_id = null;
			}
		}, 200);
		// Also run once immediately so the first frame doesn't flash.
		requestAnimationFrame(apply);
	}

	_add_chart_overlay($container, hc, total) {
		setTimeout(() => {
			const svg = $container.find("svg")[0];
			if (!svg) return;
			const drawArea = svg.querySelector(".chart-draw-area");
			if (!drawArea) return;

			const bbox = drawArea.getBBox();
			const step = bbox.width / Math.max(total - 1, 1);
			const x = hc * step;
			const ns = "http://www.w3.org/2000/svg";

			// Background: actual period (light blue)
			const bgA = document.createElementNS(ns, "rect");
			Object.entries({ x: 0, y: 0, width: x, height: bbox.height, fill: "rgba(59,130,246,0.06)" })
				.forEach(([k, v]) => bgA.setAttribute(k, v));
			drawArea.insertBefore(bgA, drawArea.firstChild);

			// Background: forecast period (light pink)
			const bgF = document.createElementNS(ns, "rect");
			Object.entries({ x, y: 0, width: bbox.width - x, height: bbox.height, fill: "rgba(239,68,68,0.05)" })
				.forEach(([k, v]) => bgF.setAttribute(k, v));
			drawArea.insertBefore(bgF, bgA.nextSibling);

			// Vertical dashed line
			const line = document.createElementNS(ns, "line");
			Object.entries({
				x1: x, x2: x, y1: 0, y2: bbox.height,
				stroke: "#94a3b8", "stroke-dasharray": "6,4", "stroke-width": "1.5",
			}).forEach(([k, v]) => line.setAttribute(k, v));
			drawArea.appendChild(line);

			// "Current" label
			const txt = document.createElementNS(ns, "text");
			txt.setAttribute("x", x);
			txt.setAttribute("y", bbox.height + 14);
			txt.setAttribute("text-anchor", "middle");
			txt.setAttribute("font-size", "11");
			txt.setAttribute("fill", "#64748b");
			txt.setAttribute("font-weight", "600");
			txt.textContent = __("Current");
			drawArea.appendChild(txt);
		}, 300);
	}

	render_table(monthly) {
		const $c = this.content.find(".pivot-container").empty();
		if (!monthly.length) return;

		const fmt = (v) => this.fmt(v);

		const periodHeaderCells = monthly.map((m) =>
			`<th class="period-col" data-period="${m.key}" data-historical="${m.is_historical ? 1 : 0}">${m.label}</th>`
		).join("");

		const rowCells = (key, valueFn, classFn) => monthly.map((m) => {
			const cls = classFn ? classFn(m) : "";
			return `<td class="${cls}" data-period="${m.key}">${valueFn(m)}</td>`;
		}).join("");

		const closingClass = (m) => {
			if (m.closing < 0) return "warning-red";
			if (m.closing < this.threshold) return "warning-yellow";
			return "";
		};

		$c.html(`
			<h6 class="forecast-section-title">${__("Summary by month/week")}</h6>
			<div class="forecast-pivot-wrap">
			<table class="table table-bordered forecast-pivot-table">
				<thead>
					<tr>
						<th class="sticky-left">${__("Metric")}</th>
						${periodHeaderCells}
					</tr>
				</thead>
				<tbody>
					<tr><th class="sticky-left">${__("Opening")}</th>${rowCells("opening", (m) => fmt(m.opening))}</tr>
					<tr><th class="sticky-left">${__("Inflow")}</th>${rowCells("inflow", (m) => fmt(m.inflow), () => "direction-in")}</tr>
					<tr><th class="sticky-left">${__("Outflow")}</th>${rowCells("outflow", (m) => fmt(m.outflow), () => "direction-out")}</tr>
					<tr><th class="sticky-left">${__("Closing")}</th>${rowCells("closing", (m) => fmt(m.closing), closingClass)}</tr>
				</tbody>
			</table>
			</div>
		`);

		this.$pivot = $c.find(".forecast-pivot-table");
		const self = this;
		this.$pivot.on("click", "th.period-col, td:not(.sticky-left)", function() {
			const $cell = $(this);
			const period = $cell.attr("data-period");
			if (!period) return;
			const $colHeader = self.$pivot.find(`th.period-col[data-period="${period}"]`);
			if ($colHeader.attr("data-historical") === "1") return;

			const newPeriod = self.selected_period === period ? null : period;
			self._select_period(newPeriod);
		});

		if (this.selected_period) {
			this.$pivot.find(`[data-period="${this.selected_period}"]`).addClass("col-selected");
		}
	}

	_select_period(period_key) {
		this.selected_period = period_key;
		this.$pivot.find(".col-selected").removeClass("col-selected");
		if (period_key) {
			this.$pivot.find(`[data-period="${period_key}"]`).addClass("col-selected");
		}
		this.detail_page = 1;
		this._reload_detail_table();
	}

	// ── Detail table (server-side paginated) ────────────────────

	async _reload_detail_table() {
		if (!this._company) return;
		const $c = this.content.find(".detail-container");
		if (!$c.find(".detail-loading").length) {
			$c.html(`<div class="detail-loading text-center text-muted" style="padding:20px">${__("Loading...")}</div>`);
		}
		try {
			const r = await frappe.xcall("vn_accounting.api.forecast.get_forecast_entries", {
				company: this._company,
				from_date: this._from_date,
				to_date: this._to_date,
				granularity: this._granularity,
				period_key: this.selected_period,
				confidences: [...this.active_confidence],
				sources: [...this.active_sources],
				search: this.detail_search || "",
				page: this.detail_page || 1,
				page_size: this.detail_page_size,
			});
			this._render_detail(r);
		} catch (e) {
			$c.html(`<div class="alert alert-danger">${e.message || String(e)}</div>`);
		}
	}

	_render_detail(r) {
		const $c = this.content.find(".detail-container").empty();
		const cl = {
			overdue: __("Overdue"), committed: __("Committed"),
			probable: __("Probable"), possible: __("Possible"),
		};

		const chip = this.selected_period
			? `<span class="badge badge-period">📅 ${this.selected_period} <a href="#" class="chip-clear" style="margin-left:4px">✕</a></span>`
			: "";
		const search_input = `<input type="text" class="form-control input-sm detail-search-input"
			placeholder="${__("Search transactions...")}" value="${frappe.utils.escape_html(this.detail_search || "")}" style="max-width:280px">`;

		let html = `
			<div class="detail-header">
				<h6 class="forecast-section-title">${__("Forecast Detail Transactions")}</h6>
				<div class="detail-toolbar">${chip}${search_input}</div>
			</div>
		`;

		if (!r.entries.length) {
			const msg = this.selected_period
				? __("No transactions in {0}").replace("{0}", this.selected_period)
				: __("No transactions");
			html += `<div class="detail-empty text-muted text-center" style="padding:20px">${msg}</div>`;
			$c.html(html);
			this._wire_detail_events($c);
			return;
		}

		html += `<table class="table table-bordered detail-table">
			<thead><tr>
				<th>${__("Type")}</th>
				<th>${__("Description")}</th>
				<th>${__("Status")}</th>
				<th>${__("Expected Date")}</th>
				<th>${__("Reference")}</th>
				<th>${__("Party")}</th>
				<th class="text-right">${__("Inflow")}</th>
				<th class="text-right">${__("Outflow")}</th>
				<th class="text-right">${__("Net")}</th>
			</tr></thead><tbody>`;

		let last_conf = null;
		for (const e of r.entries) {
			if (e.confidence !== last_conf) {
				const g = r.group_totals[e.confidence] || { inflow: 0, outflow: 0, count: 0 };
				html += `<tr class="dd-group-header"><td colspan="9">
					<span class="badge badge-${e.confidence}">${cl[e.confidence] || e.confidence}</span>
					<span class="text-muted" style="margin-left:8px">
						${__("Total")}: <span class="direction-in">+${this.fmt_short(g.inflow)}</span>
						/ <span class="direction-out">-${this.fmt_short(g.outflow)}</span>
						(${g.count} ${__("entries")})
					</span>
				</td></tr>`;
				last_conf = e.confidence;
			}
			const inflow = e.direction === "inflow" ? this.fmt(e.amount) : "—";
			const outflow = e.direction === "outflow" ? this.fmt(e.amount) : "—";
			const net = e.direction === "inflow" ? e.amount : -e.amount;
			const net_class = net >= 0 ? "direction-in" : "direction-out";
			html += `<tr>
				<td>${frappe.utils.escape_html(this._get_source_label(e.source_doctype) || e.category || "")}</td>
				<td>${frappe.utils.escape_html(e.description || "")}</td>
				<td><span class="badge badge-${e.confidence}">${cl[e.confidence]}</span></td>
				<td>${e.expected_date}</td>
				<td>${e.source_name ? `<a href="/app/${frappe.router.slug(e.source_doctype)}/${e.source_name}" target="_blank">${e.source_name}</a>` : "—"}</td>
				<td>${frappe.utils.escape_html(e.party || "—")}</td>
				<td class="text-right direction-in">${inflow}</td>
				<td class="text-right direction-out">${outflow}</td>
				<td class="text-right ${net_class}">${this.fmt(net)}</td>
			</tr>`;
		}
		html += `</tbody></table>`;

		const start = (r.page - 1) * r.page_size + 1;
		const end = Math.min(r.page * r.page_size, r.total);
		const total_pages = Math.max(1, Math.ceil(r.total / r.page_size));

		let pager = "";
		if (total_pages > 1) {
			pager += `<button class="btn btn-default btn-sm pager-prev" ${r.page <= 1 ? "disabled" : ""}>‹</button>`;
			// Show max 3 page buttons in a sliding window around current page
			const win_start = Math.max(1, Math.min(r.page - 1, total_pages - 2));
			const win_end = Math.min(total_pages, win_start + 2);
			for (let p = win_start; p <= win_end; p++) {
				pager += `<button class="btn btn-${p === r.page ? "primary" : "default"} btn-sm pager-page" data-page="${p}">${p}</button>`;
			}
			// Jump-to-page select for arbitrary navigation when >3 pages
			if (total_pages > 3) {
				let opts = "";
				for (let p = 1; p <= total_pages; p++) {
					opts += `<option value="${p}" ${p === r.page ? "selected" : ""}>${__("Page")} ${p}</option>`;
				}
				pager += `<select class="form-control input-sm pager-jump" style="display:inline-block;width:auto;margin:0 4px;vertical-align:middle;">${opts}</select>`;
			}
			pager += `<button class="btn btn-default btn-sm pager-next" ${r.page >= total_pages ? "disabled" : ""}>›</button>`;
		}

		html += `<div class="detail-footer">
			<span class="text-muted">${__("Showing {0} - {1} of {2} transactions")
				.replace("{0}", start).replace("{1}", end).replace("{2}", r.total)}</span>
			<div class="detail-pager">${pager}</div>
		</div>`;

		$c.html(html);
		this._wire_detail_events($c);
	}

	_wire_detail_events($c) {
		const self = this;
		$c.find(".detail-search-input").on("input", function() {
			const v = $(this).val();
			clearTimeout(self._search_debounce_t);
			self._search_debounce_t = setTimeout(() => {
				self.detail_search = v;
				self.detail_page = 1;
				self._reload_detail_table();
			}, 300);
		});
		$c.find(".pager-prev").on("click", () => {
			if (self.detail_page > 1) { self.detail_page--; self._reload_detail_table(); }
		});
		$c.find(".pager-next").on("click", () => {
			self.detail_page++;
			self._reload_detail_table();
		});
		$c.find(".pager-page").on("click", function() {
			self.detail_page = parseInt($(this).attr("data-page"));
			self._reload_detail_table();
		});
		$c.find(".pager-jump").on("change", function() {
			self.detail_page = parseInt($(this).val());
			self._reload_detail_table();
		});
		$c.find(".chip-clear").on("click", (e) => {
			e.preventDefault();
			self._select_period(null);
		});
	}

	// ── Formatting ──────────────────────────────────────────────

	fmt(v) { return frappe.format(v, { fieldtype: "Currency" }); }

	fmt_short(v) {
		const a = Math.abs(v), s = v < 0 ? "-" : "";
		const vnd = (frappe.boot.sysdefaults.currency || "VND") === "VND";
		if (a >= 1e9) return s + (a / 1e9).toFixed(1) + (vnd ? " tỷ" : "B");
		if (a >= 1e6) return s + (a / 1e6).toFixed(1) + (vnd ? " tr" : "M");
		if (a >= 1e3) return s + (a / 1e3).toFixed(0) + (vnd ? " ng" : "K");
		return frappe.format(v, { fieldtype: "Currency" });
	}

	// ── Methodology ─────────────────────────────────────────────

	_get_methodology_html() {
		return `
		<div class="methodology-section">
			<div class="methodology-title">${__("Opening Balance")} — Số dư đầu kỳ</div>
			<div class="methodology-desc">${__("GL balance of cash (TK 111) + bank (TK 112) + in-transit (TK 113) as of today")}</div>
		</div>
		<div class="methodology-section">
			<div class="methodology-title">${__("Forecast methods")} — Phương pháp dự báo</div>
			<table class="methodology-table"><tr>
				<th>${__("Method")}</th><th>${__("Sources")}</th><th>${__("How")}</th>
			</tr><tr>
				<td><strong>${__("Direct")}</strong></td>
				<td>SI, PI, SO, PO, Quotation, Term Deposit, Bank Loan, Contract, PAKD</td>
				<td>${__("Outstanding amount + due date from documents")}</td>
			</tr><tr>
				<td><strong>${__("Historical")}</strong></td>
				<td>Revenue (511/512), OpEx (6xx), Payroll, Insurance, VAT, CIT, PIT</td>
				<td>${__("Median of past 6-12 months GL, projected forward")}</td>
			</tr><tr>
				<td><strong>${__("Aging")}</strong></td>
				<td>Sales Invoice (inflow)</td>
				<td>${__("Adjusted by customer's median payment delay")}</td>
			</tr></table>
		</div>`;
	}

	// ── Source labels ────────────────────────────────────────────

	_get_source_label(s) {
		return ({
			"Account": __("OpEx"), "Revenue Projection": __("Revenue"),
			"Company": __("Payroll/Ins"), "Term Deposit": __("Term Deposit"),
			"Bank Loan": __("Bank Loan"), "DCNet Contract": __("Contract"),
			"Phuong An Kinh Doanh": __("PAKD"), "Sales Invoice": __("Sales Inv"),
			"Purchase Invoice": __("Purchase Inv"), "Sales Order": __("Sales Order"),
			"Purchase Order": __("Purchase Order"), "Quotation": __("Quotation"),
		})[s] || __(s);
	}

	_get_source_tooltip(s) {
		return ({
			"Account": __("Recurring expenses (TK 6xx) from GL history"),
			"Revenue Projection": __("Revenue (TK 511/512) from GL history"),
			"Company": __("Payroll (TK 334) + Insurance (TK 3383-3386)"),
			"Term Deposit": __("Principal + interest on maturity"),
			"Bank Loan": __("Scheduled repayments"),
			"Sales Invoice": __("Outstanding, adjusted by payment history"),
			"Purchase Invoice": __("Outstanding supplier invoices"),
			"Sales Order": __("Unbilled portion of confirmed orders"),
			"Purchase Order": __("Unbilled portion of purchase orders"),
			"Quotation": __("Open quotations"),
		})[s] || "";
	}

	// ── Settings + Export ────────────────────────────────────────

	_show_settings_dialog() {
		const d = new frappe.ui.Dialog({
			title: __("Cash Flow Forecast Settings"),
			fields: [
				{
					fieldname: "minimum_cash_threshold",
					label: __("Minimum Cash Threshold"),
					fieldtype: "Currency",
					default: this.threshold,
					description: __("Closing balance below this value will be highlighted in yellow. Set 0 to disable."),
				},
			],
			primary_action_label: __("Save"),
			primary_action: (values) => {
				frappe.xcall("frappe.client.set_value", {
					doctype: "VN Accounting Settings",
					name: "VN Accounting Settings",
					fieldname: "minimum_cash_threshold",
					value: values.minimum_cash_threshold,
				}).then(() => {
					this.threshold = values.minimum_cash_threshold || 0;
					d.hide();
					frappe.show_alert({ message: __("Saved"), indicator: "green" });
					this.render();
				});
			},
		});
		d.show();
	}

	export_excel() {
		if (!this._company) return;
		window.open(`/api/method/vn_accounting.api.forecast.export_forecast_excel?company=${encodeURIComponent(this._company)}&months=${this._period}&history_months=${this._history}`);
	}
}
