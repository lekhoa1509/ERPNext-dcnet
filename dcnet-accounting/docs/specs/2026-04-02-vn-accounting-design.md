# vn_accounting — Vietnamese Accounting for ERPNext v16

**Date:** 2026-04-02
**Status:** Design approved
**App name:** `vn_accounting`
**ERPNext version:** v16.12.0 (Frappe >=16.0.0)

---

## 1. Overview

Custom Frappe app providing Vietnamese accounting localization for ERPNext v16:

- Chart of Accounts templates per TT99/2024 (replacing TT200 + TT133)
- Auto company defaults after COA import
- Workspace dashboard with KPIs and charts
- Sidebar navigation organized by Vietnamese "phan hanh" (accounting sections)
- Compatible with COA Importer and Company creation flow

Target users: Professional Vietnamese accountants at SMEs and large enterprises.

---

## 2. App Structure

```
apps/vn_accounting/
├── vn_accounting/
│   ├── __init__.py
│   ├── hooks.py
│   ├── modules.txt                        # "VN Accounting"
│   ├── install.py                         # after_install + after_migrate
│   │
│   ├── chart_of_accounts/                 # COA templates
│   │   ├── __init__.py
│   │   ├── vn_large_enterprise.json       # DN lon - Company creation flow
│   │   ├── vn_small_enterprise.json       # DN nho - Company creation flow
│   │   ├── vn_large_enterprise.csv        # DN lon - COA Importer
│   │   ├── vn_small_enterprise.csv        # DN nho - COA Importer
│   │   └── coa_registry.py               # Hook dang ky COA vao ERPNext
│   │
│   ├── setup/                             # Auto-setup
│   │   ├── __init__.py
│   │   └── company_defaults.py            # Map TK VN → company defaults
│   │
│   ├── vn_accounting/                     # Module "VN Accounting"
│   │   ├── __init__.py
│   │   ├── workspace/
│   │   │   └── ke_toan_vn/
│   │   │       └── ke_toan_vn.json        # 1 workspace tong quan (dashboard)
│   │   ├── dashboard_chart/               # Dashboard Charts
│   │   │   ├── doanh_thu_chi_phi_thang/
│   │   │   │   └── doanh_thu_chi_phi_thang.json
│   │   │   ├── cong_no_phai_thu/
│   │   │   │   └── cong_no_phai_thu.json
│   │   │   ├── cong_no_phai_tra/
│   │   │   │   └── cong_no_phai_tra.json
│   │   │   └── bien_dong_tien/
│   │   │       └── bien_dong_tien.json
│   │   ├── number_card/                   # Number Cards (KPI)
│   │   │   ├── tong_doanh_thu/
│   │   │   │   └── tong_doanh_thu.json
│   │   │   ├── tong_chi_phi/
│   │   │   │   └── tong_chi_phi.json
│   │   │   ├── cong_no_phai_thu/
│   │   │   │   └── cong_no_phai_thu.json
│   │   │   ├── cong_no_phai_tra/
│   │   │   │   └── cong_no_phai_tra.json
│   │   │   └── ton_quy/
│   │   │       └── ton_quy.json
│   │   └── report/                        # Custom VN reports
│   │       └── (see Section 5)
│   │
│   ├── workspace_sidebar/                 # Sidebar override
│   │   └── ke_toan_vn.json               # 1 sidebar, 13 phan hanh
│   │
│   └── public/                            # Static assets (if needed)
│
├── pyproject.toml
└── README.md
```

---

## 3. COA Templates

### 3.1. Two templates

| Template | Target | Account count | Based on |
|---|---|---|---|
| `vn_large_enterprise` | DN lon (large enterprise) | ~180 accounts | TT99/2024 (replaces TT200) |
| `vn_small_enterprise` | DN nho (small enterprise) | ~100 accounts | TT99/2024 (replaces TT133) |

### 3.2. Dual format

Each template exists in two formats:
- **JSON** — for Company creation flow (native ERPNext dropdown selection)
- **CSV** — for COA Importer (manual import, 8-column format)

### 3.3. COA Registration

Hook into `get_charts_for_country` via `regional_overrides` in hooks.py:

```python
# hooks.py
regional_overrides = {
    "Vietnam": {
        "erpnext.accounts.doctype.account.chart_of_accounts.chart_of_accounts.get_charts_for_country": 
            "vn_accounting.chart_of_accounts.coa_registry.get_charts_for_country"
    }
}
```

When user selects country = "Vietnam" in Company setup, both templates appear in the dropdown.

### 3.4. Account number system

Standard Vietnamese account numbers per TT99/2024:
- Class 1: Tai san (Assets) — TK 111-171
- Class 2: Tai san (Assets cont.) — TK 211-244
- Class 3: No phai tra (Liabilities) — TK 331-356
- Class 4: Von chu so huu (Equity) — TK 411-421
- Class 5: Doanh thu (Revenue) — TK 511-521
- Class 6: Chi phi (Expenses) — TK 621-642
- Class 7: Thu nhap khac (Other income) — TK 711
- Class 8: Chi phi khac (Other expenses) — TK 811-821
- Class 9: Xac dinh KQKD (P&L determination) — TK 911
- Class 0: Off-balance-sheet — TK 001-008

**Note:** Exact account details will be verified against official TT99/2024 text during implementation.

---

## 4. Auto Company Defaults

After COA import, `company_defaults.py` maps Vietnamese accounts to ERPNext company defaults.

### 4.1. Hook mechanism

Override `set_default_accounts` or hook into company creation via `doc_events`:

```python
# hooks.py
doc_events = {
    "Company": {
        "after_insert": "vn_accounting.setup.company_defaults.set_vn_defaults"
    }
}
```

### 4.2. Default account mapping

| Company Default | DN Lon (TK) | DN Nho (TK) |
|---|---|---|
| `default_cash_account` | 111 - Tien mat | 111 - Tien mat |
| `default_bank_account` | 112 - Tien gui ngan hang | 112 - Tien gui ngan hang |
| `default_receivable_account` | 131 - Phai thu khach hang | 131 - Phai thu KH |
| `default_payable_account` | 331 - Phai tra nguoi ban | 331 - Phai tra NCC |
| `default_income_account` | 511 - Doanh thu ban hang | 511 - Doanh thu |
| `default_expense_account` | 632 - Gia von hang ban | 632 - Gia von hang ban |
| `stock_received_but_not_billed` | 151 - Hang mua dang di duong | *(not available)* |
| `default_inventory_account` | 156 - Hang hoa | 156 - Hang hoa |
| `accumulated_depreciation_account` | 214 - Hao mon TSCD | 214 - Hao mon TSCD |
| `depreciation_expense_account` | 6274 - CP khau hao SXKD | 6424 - CP khau hao |
| `capital_work_in_progress_account` | 241 - XDCB do dang | *(not available)* |

### 4.3. Detection logic

`set_vn_defaults` checks:
1. Company country == "Vietnam"
2. COA uses Vietnamese account numbers (check if TK 111 exists)
3. Detect template type (large vs small) by checking for TK 621 (only in large enterprise)
4. Map defaults accordingly

---

## 5. Workspace & Sidebar

### 5.1. Architecture: 1 sidebar + 1 workspace

- **1 Workspace Sidebar** (`ke_toan_vn.json`) — full navigation for 13 Vietnamese accounting sections
- **1 Workspace** (`ke_toan_vn.json`) — dashboard with KPIs and charts
- Sidebar links directly to DocType/Report/URL — no sub-workspaces

### 5.2. Sidebar structure (13 sections)

```
Trang chu (→ Workspace: ke_toan_vn)

[Section] Quy tien mat
  - Thu tien mat (→ Payment Entry: Cash + Receive)
  - Chi tien mat (→ Payment Entry: Cash + Pay)
  - So quy tien mat (→ Report)
  - Bao cao ton quy (→ Report)

[Section] Ngan hang
  - Thu tien ngan hang (→ Payment Entry: Bank + Receive)
  - Chi tien ngan hang (→ Payment Entry: Bank + Pay)
  - So tien gui ngan hang (→ Report)
  - Doi chieu ngan hang (→ Bank Reconciliation Tool)
  - Chuyen tien noi bo (→ Journal Entry)

[Section] Mua hang
  - Don mua hang (→ Purchase Order)
  - Hoa don mua hang (→ Purchase Invoice)
  - Mua hang nhap kho (→ Purchase Receipt)
  - Hang mua tra lai (→ Purchase Invoice Return)
  - Cong no phai tra (→ Report: So chi tiet TK 331)
  - Bang tong hop cong no NCC (→ Report: AP Aging VN)
  - Bao cao mua hang (→ Report)

[Section] Ban hang
  - Bao gia (→ Quotation)
  - Don ban hang (→ Sales Order)
  - Hoa don ban hang (→ Sales Invoice)
  - Hang ban tra lai (→ Sales Invoice Return)
  - Cong no phai thu (→ Report: So chi tiet TK 131)
  - Bang tong hop cong no KH (→ Report: AR Aging VN)
  - Bao cao ban hang (→ Report)

[Section] Kho
  - Nhap kho (→ Stock Entry: Material Receipt)
  - Xuat kho (→ Stock Entry: Material Issue)
  - Chuyen kho (→ Stock Entry: Material Transfer)
  - Kiem ke kho (→ Stock Reconciliation)
  - The kho (→ Report: Stock Ledger VN)
  - Bao cao nhap xuat ton (→ Report)

[Section] Tai san co dinh
  - Ghi tang TSCD (→ Asset)
  - Tinh khau hao (→ Asset Depreciation)
  - Thanh ly TSCD (→ Asset)
  - So TSCD (→ Report)
  - Bang tinh khau hao (→ Report)

[Section] Cong cu dung cu (collapsible, default closed)
  - Ghi tang CCDC (→ Asset Low Value)
  - Phan bo CCDC (→ Report)
  - Bao cao CCDC (→ Report)

[Section] Tien luong
  - Bang cham cong (→ Attendance)
  - Bang luong (→ Payroll Entry)
  - Phieu luong (→ Salary Slip)
  - BHXH, BHYT, BHTN (→ Report)
  - Thue TNCN (→ Report)

[Section] Gia thanh (collapsible, default closed)
  - Tap hop chi phi SX (→ BOM / Work Order)
  - Tinh gia thanh (→ Report)
  - Bao cao gia thanh (→ Report)

[Section] Thue
  - Bang ke HD GTGT dau vao (→ Report)
  - Bang ke HD GTGT dau ra (→ Report)
  - To khai thue GTGT (→ Report)
  - Thue TNDN (→ Report)
  - Tinh hinh su dung hoa don (→ Report)

[Section] Tong hop
  - Phieu ke toan (→ Journal Entry)
  - Ket chuyen cuoi ky (→ Period Closing Voucher)
  - Khoa so ke toan (→ Accounting Period)
  - So nhat ky chung (→ Report)
  - So cai (→ Report)
  - So chi tiet tai khoan (→ Report)
  - Bang can doi so phat sinh (→ Report: Trial Balance VN)

[Section] Bao cao tai chinh
  - Bang CDKT — B01-DN (→ Report)
  - BC Ket qua HDKD — B02-DN (→ Report)
  - BC Luu chuyen tien te — B03-DN (→ Report)
  - Thuyet minh BCTC — B09-DN (→ Report)

[Section] Danh muc
  - He thong tai khoan (→ Chart of Accounts)
  - Khach hang (→ Customer)
  - Nha cung cap (→ Supplier)
  - Hang hoa, vat tu (→ Item)
  - Kho (→ Warehouse)
  - Nhan vien (→ Employee)

[Section] Thiet lap
  - Cai dat ke toan (→ Accounts Settings)
  - Import cay tai khoan (→ COA Importer)
  - Nam tai chinh (→ Fiscal Year)
  - Ky ke toan (→ Accounting Period)
```

### 5.3. Workspace dashboard layout

```
[header] Tong quan ke toan
[nc] Doanh thu thang  [nc] Chi phi thang  [nc] CN Phai thu  [nc] CN Phai tra  [nc] Ton quy
      col=2                 col=2              col=3             col=3           col=2
[chart] DT/CP theo thang (col=6)    [chart] Bien dong tien mat + NH (col=6)
[chart] Cong no PT aging (col=6)    [chart] Cong no PP aging (col=6)
[header] Phan hanh ke toan
[card] Quy   [card] NH    [card] Mua   [card] Ban   [card] Kho
       col=2       col=2       col=3       col=3       col=2
[card] TSCD  [card] CCDC  [card] Luong [card] Thue  [card] Tong hop
       col=2       col=2       col=3       col=3       col=2
[header] Bao cao tai chinh
[card] B01-DN  [card] B02-DN  [card] B03-DN  [card] B09-DN
        col=3         col=3         col=3         col=3
```

---

## 6. Reports Scope

### 6.1. Reports included in v1.0 (priority)

| Report | Type | Description |
|---|---|---|
| So quy tien mat | Script Report | Cash book per mau S07-DN |
| So tien gui ngan hang | Script Report | Bank book per mau S08-DN |
| So chi tiet tai khoan | Script Report | Sub-ledger with doi ung (corresponding account) |
| Bang can doi so phat sinh | Script Report | Trial Balance VN format |

### 6.2. Reports linked from ERPNext (existing)

| Sidebar Label | ERPNext Report |
|---|---|
| Cong no phai thu | Accounts Receivable |
| Cong no phai tra | Accounts Payable |
| Bang tong hop CN KH | Accounts Receivable Summary |
| Bang tong hop CN NCC | Accounts Payable Summary |
| The kho | Stock Ledger |
| Bao cao nhap xuat ton | Stock Balance |
| Bang tinh khau hao | Asset Depreciation Ledger |
| So TSCD | Asset Register |
| Bao cao ban hang | Sales Analytics |
| Bao cao mua hang | Purchase Analytics |

### 6.3. Reports deferred (future phases)

- BCTC: B01-DN (Balance Sheet VN), B02-DN (P&L VN), B03-DN (Cash Flow VN), B09-DN (Notes)
- Tax: Bang ke GTGT dau vao/ra, To khai thue GTGT
- So nhat ky chung (General Journal VN format)
- So cai (General Ledger VN format)
- Reports for Luong, Gia thanh, CCDC

---

## 7. Hooks Summary

```python
# hooks.py key entries

app_name = "vn_accounting"
app_title = "VN Accounting"
app_publisher = "DCNET"

# COA registration
regional_overrides = {
    "Vietnam": {
        "erpnext.accounts.doctype.account.chart_of_accounts.chart_of_accounts.get_charts_for_country":
            "vn_accounting.chart_of_accounts.coa_registry.get_charts_for_country"
    }
}

# Auto company defaults
doc_events = {
    "Company": {
        "after_insert": "vn_accounting.setup.company_defaults.set_vn_defaults"
    }
}

# After migrate - ensure COA templates registered
after_migrate = ["vn_accounting.install.after_migrate"]
```

---

## 8. Dependencies

- **Required:** ERPNext >= 16.0.0, Frappe >= 16.0.0
- **Optional:** HRMS (for Payroll section), ERPNext Manufacturing (for Gia thanh section)
- **No dependency on:** dcnet_apps, flow_next, or any other custom app

---

## 9. Out of Scope (v1.0)

- Vietnamese print formats (Phieu thu/chi mau C30-BB, etc.)
- E-invoice integration (handled by existing einvoice module in dcnet_apps)
- HTKK XML export (handled by existing htkk module in dcnet_apps)
- Production costing VN style (gia thanh san pham)
- Custom DocTypes (all features use existing ERPNext DocTypes)

---

## 10. Success Criteria

1. User creates Company with country=Vietnam → sees 2 COA options in dropdown
2. After COA import → company defaults auto-populated correctly
3. Sidebar "Ke toan VN" appears with all 13 sections, links work
4. Dashboard workspace shows KPIs and charts with real data
5. 4 priority reports render correctly with Vietnamese format
