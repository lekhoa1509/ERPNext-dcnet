/**
 * VN Accounting — Dashboard chart enhancements.
 * - Translate "Rest" → "Khác" in donut/pie legends (frappe-charts hardcodes it)
 * - Re-layout donut/pie legends into 2-column vertical grid (horizontal overlaps long names)
 */
(function () {
	if (typeof MutationObserver === "undefined") return;

	const LEGEND_ROW_H = 22;

	function fixChartLegends() {
		// Translate "Rest" → "Khác"
		document.querySelectorAll("text.legend-dataset-label").forEach((el) => {
			if (el.textContent === "Rest") el.textContent = "Khác";
		});

		// Re-layout donut/pie chart legends vertically
		document.querySelectorAll(".frappe-chart").forEach((chart) => {
			// Only donut/pie charts have <path> slices, not <rect> bars
			const hasPieSlices = chart.querySelector("path.donut-path, path.pie-path");
			if (!hasPieSlices) return;

			const legendArea = chart.querySelector(".chart-legend");
			if (!legendArea) return;
			const items = legendArea.querySelectorAll(":scope > g");
			if (items.length === 0) return;

			// Check if already re-laid out (avoid re-processing)
			if (legendArea.dataset.vnFixed === "1") return;
			legendArea.dataset.vnFixed = "1";

			// Stack vertically — 2 columns
			const colWidth = 200;
			items.forEach((g, i) => {
				const col = i % 2;
				const row = Math.floor(i / 2);
				g.setAttribute("transform", `translate(${col * colWidth}, ${row * LEGEND_ROW_H})`);
			});

			// Increase container min-height so vertical legends are not clipped
			const rows = Math.ceil(items.length / 2);
			const extraH = Math.max(0, rows * LEGEND_ROW_H - 30);
			const container = chart.closest(".frappe-chart");
			if (container && extraH > 0) {
				const curH = container.getBoundingClientRect().height;
				container.style.minHeight = (curH + extraH) + "px";
			}
		});
	}

	const obs = new MutationObserver(fixChartLegends);
	document.addEventListener("DOMContentLoaded", () => {
		obs.observe(document.body, { childList: true, subtree: true });
	});
	if (frappe.router && frappe.router.on) {
		frappe.router.on("change", () => setTimeout(fixChartLegends, 2000));
	}
})();
