// Copyright (c) 2026, DCNET Cloud and contributors
// For license information, please see license.txt

frappe.listview_settings["Barcode Label"] = {
	add_fields: ["barcode", "barcode_value", "barcode_type", "uom"],
	formatters: {
		barcode(value, df, doc) {
			if (value) {
				let svg_id = `barcode-${doc.name}`;
				let barcode_format = doc.barcode_type || "CODE128";

				// Normalize format for JsBarcode (e.g., "EAN-13" -> "EAN13")
				if (barcode_format === "EAN-13") barcode_format = "EAN13";
				if (barcode_format === "EAN-8") barcode_format = "EAN8";
				if (barcode_format === "UPC-A") barcode_format = "UPC";

				// Render after list view is rendered
				setTimeout(() => {
					try {
						JsBarcode(`#${svg_id}`, value, {
							format: barcode_format,
							lineColor: "#000",
							width: 1,
							height: 25,
							displayValue: false
						});
					} catch (e) {
						// console.error("JsBarcode Error:", e);
					}
				}, 100);

				return `<svg id="${svg_id}" style="max-width: 100px; height: 30px;"></svg>`;
			}
			return value;
		}
	}
};
