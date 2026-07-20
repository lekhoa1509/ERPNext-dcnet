# Design QA Proposals — Asset Disposal

## Session 2026-04-24

### Auto-fixed (committed)
- None (no cosmetic issues requiring code change)

### Structural UX Proposals (needs human review before implementing)

1. **Cancel Disposal → restore to original status, not always "Partially Depreciated"**
   - Currently: `cancel_disposal()` always restores asset to "Partially Depreciated"
   - Problem: Fully Depreciated assets get demoted to a wrong status after cancel
   - Fix: Store the original `status` field in the Asset Disposal doc before execution, then restore that on cancel
   - Impact: Logic change in controller + add `original_asset_status` field to DocType
   - Priority: Medium (affects data correctness for fully depreciated asset cancellations)

2. **Journal Entry link not visible on form after execution**
   - Currently: `journal_entry` field may not be visible in the form layout at first glance
   - Suggestion: Add `journal_entry` and `sales_invoice` (for Sell) as read-only link fields in the "Accounting Entries" section so accountants can navigate directly
   - Priority: Low (accountants can find it via filters, but direct link is more convenient)

3. **"Asset Values" section label**
   - The "Asset Values" section merges Gross Purchase Amount + Accumulated Depreciation + Book Value with no visual separator from Scrap vs Sell context
   - For Scrap: these 3 fields are the key numbers. For Sell: the key number is Selling Amount
   - Suggestion: Consider showing Selling Amount more prominently for Sell type (e.g. in a larger font or summary box)
   - Priority: Low

4. **Print format: linked values appear as blue hyperlinks**
   - In the printed "Biên bản thanh lý TSCĐ", values like "ACC-ASS-2026-00002" render as blue links
   - For a formal government document, plain text is more appropriate
   - Fix: Add `color: inherit !important; text-decoration: none !important;` to `.ad-print a` in the Print Format CSS
   - Can be auto-fixed — waiting for human approval given it's a print format change
   - Priority: Medium (affects professional appearance of official documents)
