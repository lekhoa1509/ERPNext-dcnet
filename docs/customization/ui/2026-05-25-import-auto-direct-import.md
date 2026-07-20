# Import Auto Direct Import

## Overview

Import Auto now creates a cached Python import script plan during analysis, then lets users click **Import** directly from each ready file row.

## Requirements

- Source: user request on 2026-05-25.
- Khi phân tích file, hệ thống dùng khoảng 10 dòng ngẫu nhiên để tạo mapping/script luôn.
- Nút từng dòng đổi từ "Tạo mapping/script" sang "Import" vì script đã có sẵn.
- Python executor vẫn đọc lại toàn bộ Excel khi import; AI không import trực tiếp toàn bộ dữ liệu.

## Implementation

- Added hidden script-cache fields to `Import Auto File`:
  - `smart_plan_status`
  - `smart_plan_generated_on`
  - `smart_plan_json`
  - `smart_plan_error`
- `analyze_files` and `reanalyze_file` now build `smart_plan_json` from saved `analysis_json` mappings.
- Existing Smart Plan background job also stores its result back to the row.
- Row action button now runs the cached plan directly; older rows without a cached plan fall back to creating a plan, then importing.

## Technical Notes

- Cached plans use the same smart-plan schema consumed by `smart_executor.execute_plan`.
- Plan records are preview-only; `row_template` is expanded to all Excel rows during execution.
- If script generation fails, the row is marked `Error` with `smart_plan_error`.
- Smart Import no longer wraps the whole plan in one rollback savepoint. Each row gets its own savepoint, so a failed row is rolled back by itself while the executor continues with later rows.
- When rows fail, the final popup shows the skipped/error rows. Users can choose AI repair for the first error row or fix the Excel file manually and rerun.
- Item master imports now have safe fallback defaults for required master fields such as `stock_uom` and `item_group`; AI Smart Fix may also fill these fields when they are blank.
- Smart Import now stores an execution report in `error_detail` when any row is skipped or fails. The list UI parses this report and shows a separate icon button beside the existing action icons so users can inspect skipped/error rows per file.
- Rows whose analysis failed now show a separate AI action. It forces Smart Plan generation from the Excel file and presents the plan before import.
- The Smart Import success handler now separates server failures from UI rendering failures, so a successful import will not show the misleading "Import chưa hoàn tất" dialog if only the report dialog fails to render.
- The skipped/error report dialog now reads skipped details from `skipped_rows` and normalises report arrays before rendering, preventing the yellow fallback toast when an import completed with skipped rows.
- Supplier/Customer duplicate matching during import is exact-only (`name`, label, or `tax_id`). Branch names that contain the parent company name are no longer skipped as fuzzy duplicates.
- Item duplicate matching during import is exact-only by `item_code`/document `name`. `item_name` is not treated as unique because many product/service variants can share the same display name.
- The skipped/error popup now offers **AI fix & import lại** for both failed rows and skipped rows when a cached Smart Plan is available.
- Rows that AI could not classify now show an **AI xử lý** action. It force-generates a Smart Plan from the file, shows the proposed handling steps for user approval, and only imports after the user accepts the plan.
- When a forced Smart Plan succeeds, the file row cache is updated with the inferred target DocType and downgraded from `Error` to `Warning` so the approved plan can be rerun from the row.

## Deployment

Run:

```bash
bench --site flow.local migrate
```

## Future Updates

- Add a small "Preview script" action if users need to inspect the cached plan before import.

## Troubleshooting

- If a row shows `Lỗi script`, open the row error detail or run "Phân tích lại" with feedback.
- If an old analyzed row has no cached plan, click `Import`; the UI will create a plan first, then continue import.
- If the screen turns gray after a successful import, the import dialog cleanup removes stale Bootstrap modal backdrops when no modal is still visible.
- If one row fails, that row is skipped and later rows continue importing. At the end, open the row list popup and choose AI repair or manual Excel correction.
- If the created-record count is lower than the Excel row count, open **Xem danh sách dòng** on that file row. Duplicate rows, total rows, missing mandatory fields, and hard errors are grouped separately in the report.
- If the UI says the import finished but cannot open the report, hard refresh the browser once; the fixed client script needs the latest Desk asset/cache.
- If Supplier/Customer branches were previously skipped as duplicates, clear the old partial import data or reset the site, then import again so the stricter duplicate matcher can create them correctly.
- If Item rows were previously skipped because they shared the same `item_name`, rerun the partial file. Existing exact `item_code` rows will be skipped and missing distinct `item_code` rows will be inserted.
- For files like `Bang_ke_hoa_don_chung_tu_hang_hoa_dich_vu_ban_ra_mau_quan_tri 01-2026.xlsx` where normal analysis cannot classify the category, use **AI xử lý** to review the AI handling proposal before importing.

## Verification Checklist

- [x] Python syntax check passed.
- [x] JavaScript syntax check passed.
- [x] `bench --site flow.local migrate` completed.
- [x] `Import Auto File` DocField cache fields exist on `flow.local`.
- [x] Stale modal backdrop cleanup added after closing the import progress dialog.
