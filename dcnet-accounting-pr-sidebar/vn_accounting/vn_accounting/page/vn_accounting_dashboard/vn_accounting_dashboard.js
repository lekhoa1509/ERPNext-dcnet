frappe.pages["vn-accounting-dashboard"].on_page_load = function (wrapper) {
	const page = frappe.ui.make_app_page({
		parent: wrapper,
		title: __("Tổng Quan Kế Toán"),
		single_column: true,
	});

	wrapper.dashboard = new VNADashboard(page);
};

// Granularity config: filter value → API param + date range builder
const GRANULARITY_MAP = {
	"Tuần": {
		granularity: "week",
		get_range: () => {
			const today = frappe.datetime.get_today();
			const d = new Date(today);
			const day = d.getDay() || 7; // Mon=1, Sun=7
			d.setDate(d.getDate() - day + 1); // Monday
			const from_date = d.toISOString().slice(0, 10);
			d.setDate(d.getDate() + 6); // Sunday
			const to_date = d.toISOString().slice(0, 10);
			return { from_date, to_date };
		},
	},
	"Tháng": {
		granularity: "month",
		get_range: () => ({
			from_date: frappe.datetime.month_start(),
			to_date: frappe.datetime.month_end(),
		}),
	},
	"Quý": {
		granularity: "quarter",
		get_range: () => ({
			from_date: frappe.datetime.quarter_start(),
			to_date: frappe.datetime.quarter_end(),
		}),
	},
	"Năm": {
		granularity: "year",
		get_range: () => ({
			from_date: frappe.datetime.year_start(),
			to_date: frappe.datetime.year_end(),
		}),
	},
};

class VNADashboard {
	constructor(page) {
		this.page = page;
		this.charts = {};
		this.setup_filters();
		this.render_layout();
		this.setup_resize_observer();
		this.load_data();
	}

	setup_resize_observer() {
		// frappe.Chart doesn't auto-redraw on container resize (sidebar collapse,
		// window resize, browser zoom). Re-render every chart with the same
		// data on a debounced resize.
		if (typeof ResizeObserver === "undefined") return;
		let timer = null;
		const rerender = () => {
			for (const id in this.charts) {
				const c = this.charts[id];
				if (!c) continue;
				try { c.draw(true); } catch (_e) {}
			}
		};
		const obs = new ResizeObserver(() => {
			clearTimeout(timer);
			timer = setTimeout(rerender, 120);
		});
		// page.body is a jQuery object; ResizeObserver needs a raw Element.
		const target = this.page.body instanceof Element ? this.page.body : this.page.body[0];
		if (target) obs.observe(target);
	}

	setup_filters() {
		this.period_field = this.page.add_field({
			fieldname: "period",
			label: __("Kỳ"),
			fieldtype: "Select",
			options: "Tháng\nQuý\nNăm\nTuần",
			default: "Tháng",
			change: () => this.load_data(),
		});

		this.company_field = this.page.add_field({
			fieldname: "company",
			label: __("Công ty"),
			fieldtype: "Link",
			options: "Company",
			default: frappe.defaults.get_user_default("Company"),
			change: () => this.load_data(),
		});

		// Hide company if only one
		frappe.xcall("frappe.client.get_count", { doctype: "Company" }).then((count) => {
			if (count <= 1) {
				this.company_field.$wrapper.hide();
			}
		});
	}

	get_params() {
		const period = this.period_field.get_value();
		const config = GRANULARITY_MAP[period] || GRANULARITY_MAP["Tháng"];
		const { from_date, to_date } = config.get_range();
		return { from_date, to_date, granularity: config.granularity };
	}

	render_layout() {
		this.$container = $(`
			<div class="vna-dashboard">
				<div class="vna-kpi-row"></div>
				<div class="vna-chart-grid">
					<div class="widget widget-box vna-chart-card">
						<div class="vna-chart-title">${__("Doanh Thu & Chi Phí")}</div>
						<div class="vna-chart-subtitle vna-subtitle-period"></div>
						<div id="vna-revenue-expense"></div>
					</div>
					<div class="widget widget-box vna-chart-card">
						<div class="vna-chart-title">${__("Dòng Tiền")}</div>
						<div class="vna-chart-subtitle">${__("Số dư cuối kỳ (tiền mặt + ngân hàng)")}</div>
						<div id="vna-cash-timeline"></div>
					</div>
					<div class="widget widget-box vna-chart-card" style="cursor:pointer" onclick="frappe.set_route('/desk/cash-flow-forecast')">
						<div class="vna-chart-title">${__("Dự Báo Dòng Tiền")} →</div>
						<div class="vna-chart-subtitle">${__("Committed only")}, 12 ${__("Months").toLowerCase()}</div>
						<div id="vna-forecast-chart"></div>
					</div>
					<div class="widget widget-box vna-chart-card">
						<div class="vna-chart-title">${__("Công Nợ Phải Thu")}</div>
						<div class="vna-chart-subtitle">${__("Top khách hàng theo dư nợ")}</div>
						<div id="vna-ar-donut"></div>
					</div>
					<div class="widget widget-box vna-chart-card">
						<div class="vna-chart-title">${__("Công Nợ Phải Trả")}</div>
						<div class="vna-chart-subtitle">${__("Top nhà cung cấp theo dư nợ")}</div>
						<div id="vna-ap-donut"></div>
					</div>
					<div class="widget widget-box vna-chart-card">
						<div class="vna-chart-title">${__("Doanh Thu Theo Nhóm Hàng")}</div>
						<div class="vna-chart-subtitle">${__("Phân bổ theo nhóm sản phẩm/dịch vụ")}</div>
						<div id="vna-revenue-item-group"></div>
					</div>
					<div class="widget widget-box vna-chart-card">
						<div class="vna-chart-title">${__("Chi Phí Theo Loại")}</div>
						<div class="vna-chart-subtitle">${__("Giá vốn, bán hàng, quản lý")}</div>
						<div id="vna-expense-type"></div>
					</div>
					<div class="widget widget-box vna-chart-card">
						<div class="vna-chart-title">${__("Top 5 Khách Hàng")}</div>
						<div class="vna-chart-subtitle">${__("Theo doanh thu trong kỳ")}</div>
						<div id="vna-top-customers"></div>
					</div>
					<div class="widget widget-box vna-chart-card">
						<div class="vna-chart-title">${__("Tuổi Nợ Phải Thu")}</div>
						<div class="vna-chart-subtitle">${__("Phân tích theo thời gian quá hạn")}</div>
						<div id="vna-ar-aging"></div>
					</div>
				</div>
			</div>
		`).appendTo(this.page.body);
	}

	load_data() {
		const { from_date, to_date, granularity } = this.get_params();
		const company = this.company_field.get_value();
		if (!company) return;

		// Update subtitle to reflect granularity
		const subtitle_map = {
			week: "12 tuần gần nhất",
			month: "12 tháng gần nhất",
			quarter: "8 quý gần nhất",
			year: "5 năm gần nhất",
		};
		this.page.body.find(".vna-subtitle-period").text(subtitle_map[granularity] || "");

		this.page.body.find(".vna-kpi-row").html(
			'<div class="text-muted" style="padding:16px">' + __("Đang tải...") + "</div>"
		);

		frappe.xcall("vn_accounting.api.dashboard.get_dashboard", {
			from_date,
			to_date,
			company,
			granularity,
		}).then((data) => {
			this.render_kpis(data.kpis);
			this.render_charts(data.charts);
		});
	}

	render_kpis(kpis) {
		const $row = this.page.body.find(".vna-kpi-row");
		$row.empty();

		for (const kpi of kpis) {
			let delta_class = "neutral";
			let delta_text = "\u2014";

			if (kpi.delta !== null && kpi.delta !== undefined) {
				delta_class = kpi.delta >= 0 ? "up" : "down";
				const arrow = kpi.delta >= 0 ? "\u2191" : "\u2193";
				delta_text = `${arrow} ${Math.abs(kpi.delta)}%`;
			}

			const display_val = format_currency(Math.abs(kpi.value), "VND", 0);

			$row.append(`
				<div class="widget widget-box vna-kpi-card">
					<div class="vna-kpi-title" style="color:${kpi.color}">${kpi.title}</div>
					<div class="vna-kpi-value">${display_val}</div>
					<div class="vna-kpi-delta ${delta_class}">${delta_text}</div>
				</div>
			`);
		}
	}

	render_charts(charts) {
		const currency_tooltip = { formatTooltipY: (d) => format_currency(d, "VND", 0) };
		const vn_axis = { xAxisMode: "tick", shortenYAxisNumbers: 1 };

		// Row 1
		this._render_chart("vna-revenue-expense", "bar", charts.revenue_expense, {
			barOptions: { stacked: true },
			colors: ["#2e7d32", "#e65100", "#1565c0"],
			height: 280,
			tooltipOptions: currency_tooltip,
			axisOptions: vn_axis,
		});

		this._render_chart("vna-cash-timeline", "line", charts.cash_timeline, {
			colors: ["#00695c", "#1565c0"],
			height: 280,
			tooltipOptions: currency_tooltip,
			axisOptions: vn_axis,
		});

		// Forecast chart — load async from separate API
		this._load_forecast_chart(currency_tooltip, vn_axis);

		// Row 2
		this._render_chart("vna-ar-donut", "donut", charts.ar_by_customer, {
			colors: ["#1565c0", "#42a5f5", "#90caf9", "#bbdefb", "#e0e0e0"],
			height: 280,
		});

		this._render_chart("vna-ap-donut", "donut", charts.ap_by_supplier, {
			colors: ["#c62828", "#ef5350", "#ef9a9a", "#ffcdd2", "#e0e0e0"],
			height: 280,
		});

		// Row 3
		this._render_chart("vna-revenue-item-group", "donut", charts.revenue_by_item_group, {
			colors: ["#7c4dff", "#b388ff", "#d1c4e9", "#ede7f6", "#e0e0e0"],
			height: 280,
		});

		this._render_chart("vna-expense-type", "donut", charts.expense_by_type, {
			colors: ["#ff6f00", "#ffa726", "#ffcc80", "#fff3e0", "#e0e0e0"],
			height: 280,
		});

		// Row 4
		this._render_chart("vna-top-customers", "bar", charts.top_customers_revenue, {
			colors: ["#1565c0"],
			height: 280,
			tooltipOptions: currency_tooltip,
			axisOptions: vn_axis,
		});

		this._render_chart("vna-ar-aging", "bar", charts.ar_aging, {
			barOptions: { stacked: false },
			colors: ["#4caf50", "#ff9800", "#f44336", "#b71c1c"],
			height: 280,
			tooltipOptions: currency_tooltip,
			axisOptions: vn_axis,
		});

		// Wire donut clicks
		this._wire_donut_click("vna-ar-donut", "Sales Invoice", "customer");
		this._wire_donut_click("vna-ap-donut", "Purchase Invoice", "supplier");
	}

	_wire_donut_click(container_id, doctype, field) {
		const el = document.getElementById(container_id);
		if (el) {
			el.addEventListener("data-select", (e) => {
				if (e.detail && e.detail.label && e.detail.label !== "Khác") {
					frappe.set_route("List", doctype, { [field]: e.detail.label, docstatus: 1 });
				}
			});
		}
	}

	_render_chart(container_id, type, data, options) {
		const el = document.getElementById(container_id);
		if (!el) return;

		if (this.charts[container_id]) {
			this.charts[container_id].destroy();
		}

		if (!data || !data.labels || !data.labels.length) {
			el.innerHTML = '<div class="text-muted text-center" style="padding:40px">' + __("Không có dữ liệu") + "</div>";
			return;
		}

		this.charts[container_id] = new frappe.Chart(el, {
			type: type,
			data: data,
			truncateLegends: 1,
			...options,
		});
	}

	async _load_forecast_chart(currency_tooltip, vn_axis) {
		try {
			const r = await frappe.xcall(
				"vn_accounting.api.forecast.get_forecast_chart",
				{ company: this.company, months: 12 }
			);
			if (!r || !r.labels || !r.labels.length) return;
			this._render_chart("vna-forecast-chart", "axis-mixed", {
				labels: r.labels,
				datasets: [
					{ name: __("Inflow"), type: "bar", values: r.datasets.inflow },
					{ name: __("Outflow"), type: "bar", values: r.datasets.outflow.map((v) => -v) },
					{ name: __("Closing Balance"), type: "line", values: r.datasets.balance },
				],
			}, {
				colors: ["#28a745", "#dc3545", "#0056b3"],
				height: 280,
				tooltipOptions: currency_tooltip,
				axisOptions: vn_axis,
			});
		} catch (e) {
			console.warn("Forecast chart failed:", e);
		}
	}
}
