# Excel Print Preview

## Overview

The Excel Print Template Builder now renders preview as a print-like page instead of an editable spreadsheet grid.

## Requirements

- Hide Excel row/column headers in preview.
- Hide default gridlines.
- Preserve workbook layout details: merged cells, column widths, row heights, borders, fills, fonts, alignment, and wrapped text.
- Show a trimmed print area based on actual content/style instead of the full builder canvas.
- Resolve common Excel formulas used in print templates, including arithmetic cell references and `SUM(...)`.

## Implementation

> Restored on 14/07/2026 from this specification after the original builder source was no longer present in `dcnet-accounting`.

- Added DocType `Excel Print Template`, route `/app/excel-print-template-builder`, workbook serialization/rendering engine, secured whitelisted APIs, and document-form integration for the 25 supported voucher DocTypes.
- Changed the document-form `In Excel` action to open a template-management dialog like the Contract print flow. The dialog remains usable when no template exists and provides create, edit, delete, preview, download, and print actions according to the user's permissions.
- The canonical implementation lives under `vn_accounting/excel_printing/`, `vn_accounting/vn_accounting/doctype/excel_print_template/`, and `vn_accounting/vn_accounting/page/excel_print_template_builder/`.

- Added a print-preview renderer to `vn_accounting/vn_accounting/page/excel_print_template_builder/excel_print_template_builder.js`.
- Updated the document form Excel-template dialog in `vn_accounting/public/js/form_utils.bundle.js` to use the same print-like renderer.
- The renderer builds an HTML table from the filled workbook grid returned by `preview_excel_template_grid`.
- Preserved detailed Excel cell styling in the preview payload, including per-side borders, inherited row/column styles, merged-cell border edges, row heights, and copied item-row merge/style details.
- Fixed inline preview CSS generation so Excel font names with spaces do not break the cell `style` attribute.
- Preserved and shifted merged ranges when expanding item rows, preventing duplicated or overlaid totals/signature blocks.
- Treat the builder workbook JSON as the canonical template source during preview/export, so stale rows from the originally uploaded Excel file cannot reappear after the user edits the grid.
- Made the preview dialog wide, vertically roomy, resizable by dragging, and added an expand/collapse icon in the modal header.
- Protected `{{...}}` placeholders as token-like fields while editing: Backspace/Delete removes the whole placeholder instead of corrupting it character by character.
- Added number-format examples to the format dropdown and cell tooltip metadata.
- Added explicit VND/`đ` number-format choices and preview-side rendering for Vietnamese currency formats.
- Skipped invalid merge ranges that contain multiple non-empty cells so labels such as `Tổng cộng` are not hidden in preview.
- Curated the builder sidebar field list to common invoice/document fields instead of exposing every ERP DocType field.
- Added two import modes when loading an Excel template: manual mapping or AI-assisted auto mapping. AI uses the existing OpenAI-compatible settings when enabled, validates returned field keys/cells, and falls back to a basic label/header mapper if AI is unavailable.
- Cleaned AI-mapped templates after analysis by replacing/removing dotted fill-in lines, including dots inside the same cell as mapped placeholders, and deleting repeated sample item rows/formulas below the single item template row.
- Added a basic party address field so invoice address lines can be auto-mapped without exposing the full DocType field list.
- Expanded Excel print templates from the initial sales/purchase/stock set to 25 common voucher DocTypes across selling, buying, accounting, stock, subcontracting, manufacturing, and HR advances/claims. The form button list and backend supported DocType list are kept in sync.
- Added table-specific field groups for accounting rows, payment references, expense claim lines, and manufacturing material rows so non-invoice vouchers do not show only item-code/qty/rate fields.

## Technical Notes

- The builder editor still uses the spreadsheet grid.
- Preview uses separate `.xpt-print-*` and `.xpd-print-*` CSS classes so editor behavior is unaffected.
- Formula evaluation is intentionally small and browser-side: arithmetic references and `SUM` ranges cover the generated template formulas without changing exported `.xlsx` files.

## Deployment

Run the normal asset build/deploy flow for Frappe assets, then clear browser cache if the old dialog remains visible.

## Future Updates

- Add support for more Excel functions if templates begin using them.
- Consider server-side LibreOffice calculation if exact Excel formula parity becomes required.

## Troubleshooting

- If formulas appear as raw `=...`, check whether the formula uses an unsupported function.
- If preview shows too much blank area, inspect blank cells with border/fill styles in the source workbook.

## Verification Checklist

- Open Excel Print Template Builder.
- Click `Xem trước`.
- Confirm preview appears as a print page without Excel row/column headers.
- Confirm merged cells, borders, and filled document values still render.
- Confirm inserted item rows do not duplicate totals/signatures and the preview dialog can be resized.
- Confirm deleting inside `{{item.rate}}` removes the whole placeholder and hovering number format shows examples.
- Confirm `Tổng cộng` still appears after item rows expand and VND formats render with `đ/₫`.
- Confirm the left field sidebar shows only common document, item, total/tax, and company fields.
- Confirm `Load Excel mẫu` offers manual and AI auto-fill modes, and AI mode inserts placeholders into likely invoice fields without changing cell styles.
- Confirm AI mode leaves only one item template row and removes dotted fill-in text around mapped placeholders.
