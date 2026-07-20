# VN Accounting Pro Demo

## Overview

Created a standalone prototype for an alternative Vietnamese accounting workspace inspired by the operating patterns of desktop accounting systems such as MISA and BRAVO, without copying their branding or screens.

## Requirements

- Provide a separate demo surface so users can compare the current VN Accounting workspace with a more accounting-focused interface.
- Keep the prototype isolated from production Frappe pages.
- Favor dense accounting workflows, quick actions, reconciliation, VAT, receivables, payables, and period close tasks.

## Implementation

- Added a static HTML prototype at `docs/vn-accounting/accounting-pro-demo/index.html`.
- Revised the prototype into a small single-page demo: each accounting module renders its own KPIs, workflow, data table, task list, and reports so the demo no longer feels like a static one-screen wireframe.
- Built two modes:
  - `Accounting Pro`: proposed workspace with ribbon actions, KPIs, task queue, charts, data table, and period-close checklist.
  - `So sánh 2 UI`: side-by-side comparison between current workspace-style navigation and the proposed accounting workspace.
- Used inline SVG icons, accessible focus states, responsive layout, and reduced-motion support.

## Technical Notes

- This is a prototype only. It does not change the live `vn_accounting` app or the Frappe workspace.
- The next production step would be turning this into a Frappe custom Page or a small Vue/React desk app backed by existing ERPNext/VN Accounting APIs.

## Verification

- Parsed the HTML with Python `html.parser`.
- Validated that the file has no emoji icons.
- Playwright/browser screenshot verification was not available in this environment.

## Future Updates

- Add real data adapters for AR/AP, Bank Transaction, VAT return, and Period Close.
- Add role-specific home screens for Kế toán viên, Kế toán trưởng, and Ban giám đốc.
- Compare user task completion time between current workspace and Accounting Pro prototype.
