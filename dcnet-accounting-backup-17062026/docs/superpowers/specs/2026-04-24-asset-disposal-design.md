# Asset Disposal (Thanh lý TSCĐ) — Design Spec

## Overview

Dedicated Asset Disposal DocType for vn_accounting that wraps ERPNext's asset disposal
with Vietnamese accounting compliance (TT99/2025, VAS 03). Handles both Sell and Scrap
with correct dual-account entries (TK 711 + TK 811), editable account fields, and
a print format for Biên bản thanh lý TSCĐ.

## Architecture

**Approach: Hybrid — ERPNet core + VN account mapping (scored 9/10)**

- Delegate complex depreciation logic to ERPNext (`scrap_asset()` for scrap, `depreciate_asset()` for sell)
- Create VN-correct GL entries with separate 711/811 accounts (ERPNet nets to single `disposal_account`)
- Account fields visible and editable on form, auto-filled from Asset Category + VN Accounting Settings

> **Why hybrid, not custom JE:** ERPNext's pro-rata depreciation + schedule reschedule is 200+ lines
> of tested logic. Replicating = high risk of inconsistency. Hybrid reuses this and adds VN layer only.

> **Why not pure ERPNet wrapper:** ERPNet uses single `disposal_account` for gain/loss (netted).
> TT99/2025 requires gross amounts: book value → TK 811, sale proceeds → TK 711. Vietnamese
> auditors expect to see separate lines on the income statement.

## DocType: Asset Disposal

**Module:** VN Accounting
**Not submittable** (regular DocType with status field).
**Naming:** `AD-.YYYY.-.#####`

### Fields

#### Section: Asset Information
| Field | Type | Notes |
|-------|------|-------|
| `asset` | Link → Asset | Mandatory. Filter: docstatus=1, status NOT IN (Sold, Scrapped) |
| `asset_name` | Data | Read only, fetch from asset |
| `asset_category` | Link → Asset Category | Read only, fetch from asset |
| `company` | Link → Company | Read only, fetch from asset |
| `disposal_date` | Date | Mandatory. Default: today |
| `disposal_type` | Select: Sell / Scrap | Mandatory |
| `status` | Select: Draft / Executed / Cancelled | Default: Draft |

#### Section: Asset Values (read only, auto-calculated)
| Field | Type | Notes |
|-------|------|-------|
| `gross_purchase_amount` | Currency | Fetch from asset.gross_purchase_amount |
| `accumulated_depreciation` | Currency | Calculated: gross - book value (after pro-rata) |
| `book_value` | Currency | Fetch from asset.value_after_depreciation |

#### Section: Sale Details (depends on disposal_type = Sell)
| Field | Type | Notes |
|-------|------|-------|
| `selling_amount` | Currency | Mandatory when Sell |
| `buyer` | Link → Customer | Mandatory when Sell |

#### Section: Accounting Entries
| Field | Type | Notes |
|-------|------|-------|
| `fixed_asset_account` | Link → Account | Auto-fetch from Asset Category, editable |
| `accumulated_depreciation_account` | Link → Account | Auto-fetch from Asset Category, editable |
| `disposal_loss_account` | Link → Account | Auto-fetch from VN Accounting Settings (default TK 811), editable |
| `disposal_income_account` | Link → Account | Auto-fetch from VN Accounting Settings (default TK 711), editable. Visible only when Sell |

#### Section: Details
| Field | Type | Notes |
|-------|------|-------|
| `disposal_reason` | Small Text | Reason for disposal (printed on biên bản) |
| `participants` | Small Text | Committee members (printed on biên bản) |

#### Section: References (read only, set after execution)
| Field | Type | Notes |
|-------|------|-------|
| `journal_entry` | Link → Journal Entry | Writeoff JE created on execute |
| `sales_invoice` | Link → Sales Invoice | SI created on execute (Sell only) |

## Execution Flow

### Scrap Flow

User clicks **"Execute"** button (available when status = Draft):

1. **Validate**: asset is submitted, not already disposed, disposal_date valid
2. **Call `depreciate_asset(asset_doc, disposal_date, "Asset scrapped")`** — ERPNet handles pro-rata
3. **Reload asset** to get updated values
4. **Create writeoff JE** (custom, using form account fields):
   ```
   Nợ accumulated_depreciation_account = accumulated_depreciation
   Nợ disposal_loss_account            = book_value (if book_value > 0)
       Có fixed_asset_account           = gross_purchase_amount
   ```
   - posting_date = disposal_date
   - Submit JE immediately
5. **Update Asset**: `disposal_date`, `journal_entry_for_scrap = je.name`, status → "Scrapped"
6. **Update** self: `journal_entry = je.name`, `status = "Executed"`

> **Why custom JE instead of scrap_asset():** scrap_asset() reads Company.disposal_account
> which is a shared field. Modifying it temporarily creates race conditions when 2 users
> dispose assets concurrently. Custom JE reads accounts from the form — isolated, no race.
> Trade-off: ~30 more lines of code but eliminates a concurrency bug.

### Sell Flow

User clicks **"Execute"** button:

1. **Validate**: asset is submitted, not already disposed, selling_amount > 0, buyer set
2. **Call `depreciate_asset(asset_doc, disposal_date, "Asset sold")`** — ERPNet handles pro-rata
3. **Reload asset** to get updated accumulated_depreciation
4. **Create writeoff JE** (custom, using form account fields):
   ```
   Nợ accumulated_depreciation_account = accumulated_depreciation
   Nợ disposal_loss_account            = book_value (if book_value > 0)
       Có fixed_asset_account           = gross_purchase_amount
   ```
   - voucher_type = "Journal Entry"
   - posting_date = disposal_date
   - Submit JE immediately
5. **Create SI** for sale proceeds (plain SI, no is_fixed_asset):
   ```
   item: asset.item_code or generic "Asset Disposal Income" item
   rate: selling_amount
   income_account: disposal_income_account (TK 711)
   customer: buyer
   ```
   - SI created as Draft (kế toán review trước khi submit)
6. **Update Asset** manually:
   - `asset.disposal_date = disposal_date`
   - `asset.journal_entry_for_scrap = je.name` (for ERPNet restore compatibility)
   - `asset.status` → "Sold" (via `asset.db_set`)
7. **Update** self: `journal_entry = je.name`, `sales_invoice = si.name`, `status = "Executed"`

> **Why SI without is_fixed_asset:** Setting is_fixed_asset triggers ERPNet's own disposal
> GL entries (net to disposal_account) on SI submit — would double-book with our JE.

> **Why SI as Draft:** Kế toán may want to add VAT template, adjust amount, or review
> before posting revenue. Execute creates it; kế toán submits when ready.

### Cancel Flow

User clicks **"Cancel"** button (available when status = Executed):

**For Scrap:**
1. **Cancel JE** (writeoff)
2. **Restore depreciation**: call `reverse_depreciation_entry_made_on_disposal(asset_doc)` + `reset_depreciation_schedule(asset_doc)`
3. **Clear Asset**: `disposal_date = None`, `journal_entry_for_scrap = None`, restore previous status
4. Update self.status = "Cancelled"

**For Sell:**
1. **Validate**: SI must be cancelled first (if submitted). Show message if SI is still submitted.
2. **Cancel JE** (writeoff)
3. **Restore depreciation**: call `reverse_depreciation_entry_made_on_disposal(asset_doc)` + `reset_depreciation_schedule(asset_doc)`
4. **Clear Asset**: `disposal_date = None`, `journal_entry_for_scrap = None`, restore previous status
5. Update self.status = "Cancelled"

> **Note:** Both flows share the same cancel logic (cancel JE → restore depreciation → clear asset).
> Sell adds one pre-step: validate SI is cancelled first.

## VN Accounting Settings — New Fields

Add to existing VN Accounting Settings DocType:

| Field | Type | Default |
|-------|------|---------|
| `disposal_loss_account` | Link → Account | Account matching "811 -%" |
| `disposal_income_account` | Link → Account | Account matching "711 -%" |

**Section:** "Asset Disposal" (new section break after existing treasury fields).

## Company Setup Hook

In `doc_events.Company.on_update` (existing hook in vn_accounting):
- Auto-set `Company.disposal_account` = VN Accounting Settings.disposal_loss_account
- Only if company.country == "Vietnam" and disposal_account is empty

> **Why auto-set Company.disposal_account:** ERPNet's scrap_asset() reads this field.
> Setting it to 811 ensures TT99 compliance without manual configuration.

## Sidebar Integration

Update workspace sidebar JSON: change "[Pending] Thanh lý" item:
- label: "Thanh lý" (remove [Pending] prefix)
- link_type: "DocType"
- link_to: "Asset Disposal"
- Remove route to "under-development" page

## Print Format: Biên Bản Thanh Lý TSCĐ

Jinja Print Format with `custom_format = 1`.

**Layout:**
```
                    CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
                        Độc lập - Tự do - Hạnh phúc

                     BIÊN BẢN THANH LÝ TÀI SẢN CỐ ĐỊNH
                           Số: {{ doc.name }}

Ngày {{ disposal_date.day }} tháng {{ disposal_date.month }} năm {{ disposal_date.year }}

Căn cứ Quyết định số ......... ngày ......... của {{ company }}
về việc thanh lý tài sản cố định.

I. Thành phần tham gia:
{{ participants }}

II. Thông tin tài sản:
- Tên tài sản: {{ asset_name }}
- Mã tài sản: {{ asset }}
- Nguyên giá: {{ gross_purchase_amount }}
- Giá trị hao mòn lũy kế: {{ accumulated_depreciation }}
- Giá trị còn lại: {{ book_value }}

III. Hình thức thanh lý: {{ disposal_type_label }}
{% if disposal_type == "Sell" %}
- Giá bán: {{ selling_amount }}
- Người mua: {{ buyer_name }}
{% endif %}

IV. Lý do thanh lý:
{{ disposal_reason }}

V. Kết luận:
Hội đồng thanh lý đã tiến hành thanh lý tài sản theo đúng quy định.

  Kế toán trưởng          Hội đồng thanh lý          Giám đốc
  (Ký, họ tên)            (Ký, họ tên)               (Ký, họ tên)
```

## Translations (vi.csv additions)

```csv
Asset Disposal,Thanh lý TSCĐ
Disposal Type,Hình thức thanh lý
Sell,Bán
Scrap,Hủy
Book Value,Giá trị còn lại
Gross Purchase Amount,Nguyên giá
Accumulated Depreciation,Khấu hao lũy kế
Disposal Reason,Lý do thanh lý
Participants,Thành viên hội đồng thanh lý
Selling Amount,Giá bán
Buyer,Người mua
Disposal Loss Account,TK chi phí thanh lý
Disposal Income Account,TK thu nhập thanh lý
Fixed Asset Account,TK tài sản cố định
Accumulated Depreciation Account,TK hao mòn lũy kế
Execute,Thực hiện thanh lý
Asset Disposal Report,Biên bản thanh lý TSCĐ
```

## Edge Cases

### Khi nào khác?

1. **Fully depreciated asset (book_value = 0) — Scrap:**
   JE only has Nợ 214 / Có 211. No 811 entry (nothing remaining). scrap_asset() handles this correctly (profit_amount = 0 → no disposal GL line).

2. **Fully depreciated asset — Sell:**
   JE writeoff: Nợ 214 / Có 211 (no 811 line). SI: Nợ 131 / Có 711 = selling_amount. All proceeds = pure income.

3. **Asset without depreciation schedule (non-depreciable):**
   Skip depreciate_asset() call. book_value = gross_purchase_amount. Entire value goes to 811 on scrap.

4. **Cancel after Payment Entry exists for SI:**
   Validation: cannot cancel Asset Disposal if SI has linked PE that is submitted. User must cancel PE → cancel SI → then cancel Asset Disposal.

5. **Multiple assets in same disposal:**
   Out of scope for v1. Each Asset Disposal handles one asset. Batch disposal is a future feature.

6. **Asset linked to Bank Loan (collateral):**
   No validation for v1 (vn_accounting Bank Loan doesn't track collateral assets yet). Future: add check.

## Permissions

| Role | Read | Write | Create | Delete | Execute |
|------|------|-------|--------|--------|---------|
| Accounts Manager | ✓ | ✓ | ✓ | ✓ | ✓ |
| Accounts User | ✓ | ✓ | ✓ | ✗ | ✓ |

## Out of Scope (v1)

- CCDC (Công cụ dụng cụ) disposal — different accounts (153/142/242)
- Batch disposal (multiple assets in one form)
- Approval workflow (Hội đồng thanh lý approval chain)
- Asset Disposal Report (list report) — use standard list view for now
- VAT handling automation — kế toán adds tax template manually on SI
