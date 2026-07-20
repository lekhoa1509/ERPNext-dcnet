/**
 * dcnet_theme — Excel-style selection summary for Frappe DataTable.
 *
 * When the user drag-selects multiple cells (Shift+click or click-drag) in any
 * DataTable (Query Reports, Script Reports, ListView when applicable), shows a
 * floating bar at the bottom-right of the viewport with:
 *   • Count of selected cells
 *   • Count of numeric cells in the selection
 *   • Sum / Average / Min / Max of numeric values
 *
 * Triggered by feedback FB-2026-00465 / 00474 / 00514 — multiple users asked
 * for Excel-like cell-selection statistics across every query report.
 *
 * Pure DOM observer — no patch into the frappe-datatable library, so it keeps
 * working across Frappe version bumps. The library tags selected cells with
 * `.dt-cell--highlight`; we listen for class changes on `.dt-cell` and parse
 * cell text via Frappe's own `flt()` (respects user's number_format).
 */
(function () {
	if (window.__dcnet_dt_selection_summary_loaded) return;
	window.__dcnet_dt_selection_summary_loaded = true;

	const BAR_ID = "dcnet-dt-selection-summary";

	function parseNumeric(text) {
		if (text == null) return null;
		let s = String(text).trim();
		if (!s || !/\d/.test(s)) return null;
		// Strip a leading currency word/symbol followed by whitespace ("VND 1.234.567")
		s = s.replace(/^[A-Za-z₫$€£¥]+\.?\s+/, "");
		// Strip leading single-char currency symbol ("₫1.234.567", "$100")
		s = s.replace(/^[₫$€£¥]/, "");
		// Strip trailing currency/unit ("1.234.567 VND", "25 %")
		s = s.replace(/\s+[A-Za-z%]+$/, "");
		s = s.replace(/%$/, "");
		// Accounting-style negatives in parens: "(1.234)" -> "-1.234"
		const paren = s.match(/^\((-?[\d.,\s]+)\)$/);
		if (paren) s = "-" + paren[1];
		s = s.trim();
		// What remains must be purely numeric (digits + separators + optional sign)
		if (!/^-?[\d.,\s]+$/.test(s)) return null;
		try {
			const v = (typeof flt === "function") ? flt(s) : parseFloat(s.replace(/[.,\s]/g, ""));
			if (typeof v !== "number" || !isFinite(v)) return null;
			return v;
		} catch (e) {
			return null;
		}
	}

	function formatNum(n) {
		if (!isFinite(n)) return String(n);
		try {
			if (typeof format_number === "function") {
				const precision = Number.isInteger(n) ? 0 : 2;
				return format_number(n, null, precision);
			}
		} catch (e) {
			/* fall through */
		}
		return String(n);
	}

	function getCellText(cell) {
		const content = cell.querySelector(".dt-cell__content");
		return ((content || cell).innerText || (content || cell).textContent || "").trim();
	}

	function getOrCreateBar() {
		let bar = document.getElementById(BAR_ID);
		if (bar) return bar;
		bar = document.createElement("div");
		bar.id = BAR_ID;
		Object.assign(bar.style, {
			position: "fixed",
			bottom: "16px",
			right: "20px",
			background: "var(--bg-color, #ffffff)",
			color: "var(--text-color, #1f272e)",
			border: "1px solid var(--border-color, #d1d8dd)",
			borderRadius: "10px",
			padding: "7px 12px",
			fontFamily: "var(--font-stack, sans-serif)",
			boxShadow: "0 4px 14px rgba(0, 0, 0, 0.14)",
			zIndex: "1090",
			display: "none",
			whiteSpace: "nowrap",
			userSelect: "text",
		});
		document.body.appendChild(bar);
		return bar;
	}

	function renderStat(label, value, accent) {
		const labelStyle =
			"font-size:9.5px;font-weight:600;letter-spacing:0.04em;text-transform:uppercase;color:var(--text-muted,#8d99a6);margin-bottom:1px";
		const valueStyle =
			"font-size:13.5px;font-weight:600;line-height:1.2;color:" +
			(accent || "var(--text-color,#1f272e)") +
			";font-variant-numeric:tabular-nums";
		return (
			`<div style="display:inline-flex;flex-direction:column;align-items:flex-end;padding:0 10px">` +
			`<div style="${labelStyle}">${label}</div>` +
			`<div style="${valueStyle}">${value}</div>` +
			`</div>`
		);
	}

	function hideBar() {
		const bar = document.getElementById(BAR_ID);
		if (bar) bar.style.display = "none";
	}

	function updateSummary() {
		// Use the first datatable that has a live selection — query reports
		// only render one datatable at a time, but ListView dialogs could
		// theoretically have more. Prefer the one with highlights.
		// When user shift-clicks a range, the library highlights three groups:
		//   1. The data cells in the range — these are what we want
		//   2. The column header(s) above the range — "Số tiền"-shaped text
		//   3. The row-index cells (col 0) of each selected row — "1, 2, 3..."
		// Groups 2+3 inflate the visible count and would pollute sum/min/max
		// (FB-2026-00514 follow-up: bar reported 4 cells when 3 amounts visible
		// — the 4th was the column header).
		const rawCells = document.querySelectorAll(".datatable .dt-cell--highlight");
		const cells = Array.from(rawCells).filter((c) => {
			if (c.classList.contains("dt-cell--header")) return false;
			if (c.closest(".dt-header")) return false;
			if (c.getAttribute("data-col-index") === "0") return false;
			return true;
		});
		if (cells.length < 2) {
			hideBar();
			return;
		}
		let total = 0,
			numCount = 0,
			sum = 0,
			min = Infinity,
			max = -Infinity;
		cells.forEach((c) => {
			total++;
			const v = parseNumeric(getCellText(c));
			if (v !== null) {
				numCount++;
				sum += v;
				if (v < min) min = v;
				if (v > max) max = v;
			}
		});
		const bar = getOrCreateBar();
		const divider =
			`<div style="width:1px;background:var(--border-color,#e4e8eb);align-self:stretch;margin:2px 0"></div>`;
		const accent = "var(--primary, #2490ef)";
		const parts = [renderStat("Đã chọn", total)];
		if (numCount > 0) {
			if (numCount !== total) parts.push(renderStat("Ô số", numCount));
			parts.push(renderStat("Tổng", formatNum(sum), accent));
			parts.push(renderStat("Trung bình", formatNum(sum / numCount)));
			if (numCount > 1) {
				parts.push(renderStat("Min", formatNum(min)));
				parts.push(renderStat("Max", formatNum(max)));
			}
		}
		bar.innerHTML = `<div style="display:flex;align-items:stretch">${parts.join(divider)}</div>`;
		bar.style.display = "block";
	}

	let raf = null;
	function scheduleUpdate() {
		if (raf) return;
		raf = requestAnimationFrame(() => {
			raf = null;
			updateSummary();
		});
	}

	// Watch the whole document for class changes on .dt-cell descendants.
	// MutationObserver with attributeFilter is cheap; the engine only fires
	// for class mutations, not every DOM change.
	function startObserver() {
		const obs = new MutationObserver((mutations) => {
			for (const m of mutations) {
				if (
					m.type === "attributes" &&
					m.attributeName === "class" &&
					m.target.classList &&
					m.target.classList.contains("dt-cell")
				) {
					scheduleUpdate();
					return;
				}
			}
		});
		obs.observe(document.body, {
			attributes: true,
			attributeFilter: ["class"],
			subtree: true,
		});
	}

	// Hide bar on route change — selection state from the previous page is no
	// longer meaningful. New page's datatable will trigger fresh updates.
	function hookRouteChange() {
		if (window.frappe && frappe.router && frappe.router.on) {
			frappe.router.on("change", () => hideBar());
		}
	}

	function init() {
		startObserver();
		hookRouteChange();
	}

	if (document.readyState === "loading") {
		document.addEventListener("DOMContentLoaded", init);
	} else {
		init();
	}
})();
