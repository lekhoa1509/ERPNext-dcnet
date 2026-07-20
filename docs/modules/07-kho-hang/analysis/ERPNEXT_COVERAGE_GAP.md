# ERPNext Coverage & Gap Analysis: Module Kho (30 Features)

> **Module:** 07 - Kho hang | DCNET Flow
> **Phien ban:** 1.0 | **Ngay:** 16/02/2026
> **ERPNext version:** v16 (released 12/01/2026)
> **Nguon:** FEATURE_SPECIFICATION.md, ERP_SPECIFICATION.md Section 4, README.md Feature Matrix
> **Cong ty:** Thang Long TM + Nhat Minh Sport (2 site rieng, code chung)

---

## 1. Tong quan

### 1.1. Thong ke coverage

| Loai | So luong | Ty le |
|------|----------|-------|
| ERPNext native (dung duoc ngay) | 10 | 33% |
| ERPNext + config/customize (them custom field, property setter) | 8 | 27% |
| ERPNext + custom script (client/server script, minor code) | 5 | 17% |
| Custom development (DocType moi, module moi) | 7 | 23% |
| **Tong** | **30** | **100%** |

**Phan tich:**
- **60% (18/30)** features co the giai quyet bang ERPNext native hoac customize nhe. Day la phan setup va configuration, khong can viet code phuc tap.
- **17% (5/30)** can custom script (client script hoac server script) de mo rong ERPNext.
- **23% (7/30)** can custom development hoan toan moi: Barcode/Label (3 features), Warehouse Location (1 feature), custom reports (2 features), Web Sync (1 feature).

### 1.2. Effort summary

| Hang muc | Features | Effort | Ghi chu |
|----------|----------|--------|---------|
| Configuration only | 10 | 3-5 ngay | Setup warehouse, stock settings, permissions |
| Minor customization (custom field, property setter) | 8 | 5-7 ngay | Them fields, customize form, workflow |
| Custom script (client/server script) | 5 | 8-10 ngay | Server script, client script, hooks |
| Major custom development | 7 | 40-55 ngay | New DocType, new module, new reports |
| Testing & QA | 30 | 10-15 ngay | Unit test, integration test, UAT |
| **Tong effort uoc tinh** | **30** | **~66-92 ngay (~13-18 tuan)** | 1 developer |

### 1.3. Phan bo theo priority

| Priority | So luong | ERPNext Native | Can Custom | Ghi chu |
|----------|----------|----------------|------------|---------|
| Critical | 10 | 7 | 3 | BC NXT, Web Sync, Consignment-related |
| High | 16 | 9 | 7 | Barcode/Label, Location, Batch/Serial enhancements |
| Medium | 4 | 2 | 2 | BC theo vi tri, dashboard widgets |

---

## 2. Bang Gap Analysis chi tiet (30 features)

### 2.1. Phase 1: CRM Features (3 features)

| # | Feature ID | Ten | Priority | ERPNext Equivalent | Coverage | Gap cu the | Effort |
|---|-----------|------|----------|-------------------|----------|------------|--------|
| 1 | WH-001 | Danh sach kho | Critical | Warehouse List View | Native | Khong gap. Warehouse List View hien thi day du: ten kho, company, parent warehouse, is_group. Chi can config de them custom column neu can. | 0 |
| 2 | WH-002 | Tao kho | High | Warehouse DocType | Native | Khong gap. Warehouse DocType cho phep tao kho voi tat ca thong tin can thiet: ten, company, parent warehouse, allow_negative_stock, warehouse_type. Can setup hierarchy cho 2 company (TM + NM). | 0.5 ngay (setup) |
| 3 | WH-003 | Xem chi tiet kho/ton kho | Critical | Stock Balance + Warehouse Dashboard | Customize | ERPNext co Stock Balance report nhung can them **dashboard widget** tren Warehouse form de hien thi: ton kho real-time, gia tri ton, so luong item, movement 7 ngay. Can tao **Warehouse Dashboard** custom. | 2-3 ngay |

**Chi tiet WH-003:**

ERPNext v16 da co san:
- `Stock Balance` report: Ton kho theo item + warehouse
- Warehouse form co section links den Stock Ledger Entry
- `Bin` DocType luu actual_qty, reserved_qty, ordered_qty, projected_qty

Can custom:
- Dashboard widget hien thi tong hop ton kho ngay tren Warehouse form
- Widget gia tri ton kho (stock value)
- Widget top items theo so luong
- Widget movement summary (nhap/xuat 7 ngay)

**Approach:** Client script + custom HTML trong Warehouse form, query tu Bin va Stock Ledger Entry.

---

### 2.2. Phase 2: ERP-WH Features (20 features)

#### 2.2.1. Nhap kho (4 features)

| # | Feature ID | Ten | Priority | ERPNext Equivalent | Coverage | Gap cu the | Effort |
|---|-----------|------|----------|-------------------|----------|------------|--------|
| 1 | ERP-WH-001 | Ton kho dau ky | Critical | Stock Reconciliation (purpose=Opening Stock) | Native | Khong gap. Stock Reconciliation voi purpose "Opening Stock" cho phep nhap so luong, gia tri cho tung item/warehouse. Ho tro batch va serial. | 0.5 ngay (setup) |
| 2 | ERP-WH-002 | Phieu nhap mua | Critical | Purchase Receipt | Native | Khong gap. Purchase Receipt tu dong tao tu Purchase Order. Auto-create Stock Ledger Entry va GL Entry khi submit. Ho tro batch, serial, multi-UOM. | 0 |
| 3 | ERP-WH-003 | Phieu nhap khau | Critical | Purchase Receipt + Landed Cost Voucher | Native | ERPNext ho tro day du: Purchase Receipt cho nhap hang + Landed Cost Voucher de phan bo chi phi nhap khau (van chuyen, thue NK, bao hiem) vao gia von. Can config Landed Cost accounts. | 1 ngay (config) |
| 4 | ERP-WH-004 | Phieu nhap khac | High | Stock Entry (Material Receipt) | Native | Khong gap. Stock Entry voi purpose "Material Receipt" dung cho moi loai nhap khac: nhap tu san xuat, nhap hoan tra, nhap kiem ke chenh lech. | 0 |

**Chi tiet ERP-WH-003 (Phieu nhap khau):**

ERPNext flow:
```
Purchase Order (Foreign Supplier)
  -> Purchase Receipt (nhap kho, ghi nhan 1561 Hang hoa)
    -> Landed Cost Voucher (phan bo CP: van chuyen, thue, bao hiem)
      -> Cap nhat valuation_rate trong Stock Ledger Entry
        -> GL Entry: No 1561 (gia von moi), Co 331/1331
```

Config can thiet:
- Landed Cost account setup (TK 15611 - Chi phi van chuyen, thue NK...)
- Exchange rate (multi-currency: USD, JPY)
- Supplier default currency

---

#### 2.2.2. Xuat kho (4 features)

| # | Feature ID | Ten | Priority | ERPNext Equivalent | Coverage | Gap cu the | Effort |
|---|-----------|------|----------|-------------------|----------|------------|--------|
| 5 | ERP-WH-005 | Phieu xuat ban | Critical | Delivery Note | Native | Khong gap. Delivery Note tu dong tao tu Sales Order. Auto-create Stock Ledger Entry (tru ton) va GL Entry (No 632, Co 1561). Ho tro Pick List de lay hang. | 0 |
| 6 | ERP-WH-006 | Phieu xuat khac | High | Stock Entry (Material Issue) | Native | Khong gap. Stock Entry voi purpose "Material Issue" dung cho: xuat noi bo, xuat huy, xuat CCDC. Can them custom field cho CCDC (so thang phan bo, TK no/co phan bo). | 1 ngay |
| 7 | ERP-WH-007 | Phieu dieu chuyen | High | Stock Entry (Material Transfer) | Customize | ERPNext co 2-step transfer (source -> target). Khach yeu cau **3-step** transfer (source -> transit -> target) voi dual approval. Can config Transit Warehouse va customize workflow. | 3-5 ngay |
| 8 | ERP-WH-008 | Phieu xuat tra NCC | High | Purchase Return (Purchase Receipt cancel/return) | Native | ERPNext ho tro Purchase Return bang cach tao Purchase Receipt voi is_return=1. Tu dong dao nguoc Stock Ledger va GL Entry. | 0 |

**Chi tiet ERP-WH-006 (Phieu xuat CCDC):**

ERPNext co Stock Entry (Material Issue) nhung **khong co** tinh nang quan ly CCDC (Cong cu dung cu) voi:
- So thang phan bo
- Tai khoan no/co phan bo
- Ma tang giam

**Gap:** Can them custom fields vao Stock Entry Item:
```python
# Custom fields cho Stock Entry Item (CCDC)
custom_fields = {
    "Stock Entry Item": [
        {"fieldname": "is_ccdc", "fieldtype": "Check", "label": "La CCDC"},
        {"fieldname": "amortization_months", "fieldtype": "Int", "label": "So thang phan bo"},
        {"fieldname": "debit_amortization_account", "fieldtype": "Link", "options": "Account", "label": "TK No phan bo"},
        {"fieldname": "credit_amortization_account", "fieldtype": "Link", "options": "Account", "label": "TK Co phan bo"},
        {"fieldname": "increase_decrease_code", "fieldtype": "Data", "label": "Ma tang giam"},
    ]
}
```

**Chi tiet ERP-WH-007 (Phieu dieu chuyen 3 buoc):**

ERPNext v16 ho tro:
- **2-step transfer:** Stock Entry (Material Transfer) tu source -> target (1 phieu)
- **Multi-step transfer:** Can config Transit Warehouse, tao 2 Stock Entry (source->transit, transit->target)

Gap voi yeu cau khach hang:
1. **Dual approval:** Can workflow cho ca kho xuat va kho nhan duyet rieng
2. **Transit tracking:** Can theo doi hang dang o transit warehouse
3. **Variance handling:** Neu so luong nhan khac so luong xuat, can xu ly chenh lech

**Approach:**
- Config `Transit Warehouse` cho moi company
- Tao custom Workflow tren Stock Entry voi states: Draft -> Pending Source Approval -> In Transit -> Pending Target Approval -> Completed
- Server script de validate dual approval
- Client script de hien thi tracking info

---

#### 2.2.3. Quan ly Batch, Serial, Vi tri (3 features)

| # | Feature ID | Ten | Priority | ERPNext Equivalent | Coverage | Gap cu the | Effort |
|---|-----------|------|----------|-------------------|----------|------------|--------|
| 9 | ERP-WH-009 | Quan ly lo (Batch) | High | Batch DocType | Custom Script | ERPNext co Batch management day du: auto-create, expiry date, manufacturing date. **Gap:** Can them lifecycle alerts (canh bao sap het han, auto-block xuat khi het han), batch status tracking. | 3-4 ngay |
| 10 | ERP-WH-010 | Quan ly serial | High | Serial No DocType | Custom Script | ERPNext Serial No co status: Active/Inactive/Delivered. **Gap:** DCNET can them status: Ton kho / Ky gui / Da ban / Trade-in / Thanh ly. Can override hoac custom field. | 2-3 ngay |
| 11 | ERP-WH-011 | Quan ly vi tri | High | Khong co | Custom Dev | ERPNext **khong co** warehouse location management (Khu/Ke/O). Can tao DocType moi: Warehouse Location voi hierarchy 3 cap. Link vao Stock Entry Item. | 5-7 ngay |

**Chi tiet ERP-WH-009 (Batch lifecycle alerts):**

ERPNext da co:
- Batch DocType: batch_id, item, manufacturing_date, expiry_date, batch_qty
- Auto-create batch khi nhap kho (neu item.has_batch_no = True)
- Filter batch khi xuat kho (chi hien thi batch co ton trong kho do)

Can them:
```python
# Server script: Batch Expiry Alert (chay hang ngay qua Scheduled Job)
def check_batch_expiry():
    """Canh bao lo hang sap het han trong 30 ngay"""
    batches = frappe.get_all("Batch", filters={
        "expiry_date": ["between", [today(), add_days(today(), 30)]],
        "batch_qty": [">", 0]
    }, fields=["name", "item", "expiry_date", "batch_qty"])

    for batch in batches:
        days_left = date_diff(batch.expiry_date, today())
        if days_left <= 7:
            # Canh bao URGENT
            send_notification("Batch Expiry", f"Lo {batch.name} het han trong {days_left} ngay!")
        elif days_left <= 30:
            # Canh bao WARNING
            send_notification("Batch Expiry Warning", f"Lo {batch.name} het han trong {days_left} ngay")

# Server script: Block xuat batch het han
def validate_batch_on_stock_entry(doc, method):
    """Khong cho xuat batch da het han"""
    for item in doc.items:
        if item.batch_no:
            batch = frappe.get_doc("Batch", item.batch_no)
            if batch.expiry_date and batch.expiry_date < today():
                frappe.throw(f"Lo {item.batch_no} da het han ngay {batch.expiry_date}. Khong duoc xuat.")
```

**Chi tiet ERP-WH-010 (Serial status custom):**

ERPNext Serial No status hien tai:
- `Active` - Co trong kho
- `Inactive` - Khong su dung
- `Delivered` - Da giao cho khach
- `Expired` - Het han (neu batch expired)

DCNET can:
- `In Stock` (Ton kho) - Tuong duong Active
- `On Consignment` (Ky gui) - Hang gui tai shop khac (TM -> NM)
- `Sold` (Da ban) - Tuong duong Delivered
- `Trade-in` - Hang cu thu ve
- `Disposed` (Thanh ly) - Hang thanh ly

**Approach:** Them custom field `dcnet_status` (Select) vao Serial No DocType, khong override field `status` goc cua ERPNext de tranh conflict. Server script de tu dong cap nhat dcnet_status theo nghiep vu.

```python
# Custom field
custom_fields = {
    "Serial No": [
        {
            "fieldname": "dcnet_status",
            "fieldtype": "Select",
            "label": "Trang thai DCNET",
            "options": "\nIn Stock\nOn Consignment\nSold\nTrade-in\nDisposed",
            "insert_after": "status"
        }
    ]
}
```

---

#### 2.2.4. Reserve Stock & Barcode (4 features)

| # | Feature ID | Ten | Priority | ERPNext Equivalent | Coverage | Gap cu the | Effort |
|---|-----------|------|----------|-------------------|----------|------------|--------|
| 12 | ERP-WH-012 | Reserve stock | Critical | Stock Reservation Entry | Native | ERPNext v16 co **Stock Reservation Entry** (tinh nang moi). Khi tao Sales Order, co the reserve stock cho SO do. Bin.reserved_qty tang, projected_qty giam. | 1 ngay (enable + test) |
| 13 | ERP-WH-013 | Gan barcode | High | Khong co | Custom Dev | ERPNext cho phep add barcode vao Item (Item Barcode child table) nhung **khong co** giao dien tao barcode tu dong theo quy uoc (ma VT + ;; + so lo). Can tao DocType Barcode Label. | 5-7 ngay |
| 14 | ERP-WH-014 | Tao tem nhan | High | Khong co | Custom Dev | ERPNext **khong co** label designer/generator. Can tao: template tem (Jinja + CSS), preview, print format. Ho tro nhieu kich thuoc tem. | 4-5 ngay |
| 15 | ERP-WH-015 | In tem hang loat | High | Khong co | Custom Dev | ERPNext **khong co** batch printing cho tem. Can tao: chon nhieu item, generate barcode images (python-barcode library), xuat PDF voi nhieu tem tren 1 trang A4. | 3-4 ngay |

**Chi tiet ERP-WH-012 (Stock Reservation):**

ERPNext v16 Stock Reservation Entry:
- Tu dong tao khi Sales Order submit (neu enable Stock Reservation trong Stock Settings)
- Luu: item_code, warehouse, reserved_qty, voucher_type, voucher_no
- Bin.reserved_qty tang tuong ung
- Khi Delivery Note submit, reserved_qty giam

Config can thiet:
```python
# Stock Settings
frappe.db.set_single_value("Stock Settings", "enable_stock_reservation", 1)
frappe.db.set_single_value("Stock Settings", "auto_reserve_stock_on_sales_order", 1)
```

Khong can custom them. Chi can enable va test.

---

#### 2.2.5. Kiem ke (2 features)

| # | Feature ID | Ten | Priority | ERPNext Equivalent | Coverage | Gap cu the | Effort |
|---|-----------|------|----------|-------------------|----------|------------|--------|
| 16 | ERP-WH-016 | Kiem ke | High | Stock Reconciliation | Custom Script | ERPNext co Stock Reconciliation nhung **khong co**: (1) Freeze warehouse trong khi kiem ke, (2) Approval workflow truoc khi submit. Can custom ca 2. | 3-5 ngay |
| 17 | ERP-WH-017 | Xu ly chenh lech | High | Stock Reconciliation + Stock Entry | Custom Script | ERPNext Stock Reconciliation tu dong dieu chinh khi submit. **Gap:** Can tach buoc: detect variance -> ke toan duyet -> tao phieu nhap/xuat chenh lech rieng (khong auto-adjust). | 3-4 ngay |

**Chi tiet ERP-WH-016 (Freeze warehouse khi kiem ke):**

ERPNext da co:
- `Stock Reconciliation` DocType: nhap so luong thuc te, he thong tu tinh chenh lech
- `Stock Freeze Upto` trong Stock Settings: dong bang tat ca kho den 1 ngay cu the
- Warehouse field `disabled`: vo hieu hoa kho (nhung la disabled vinh vien, khong phai freeze tam thoi)

Gap:
- Khong co tính nang **freeze 1 warehouse cu the** trong khi kiem ke (chi co freeze tat ca hoac khong)
- Khong co approval workflow cho Stock Reconciliation

**Approach:**

```python
# 1. Them custom field vao Warehouse
custom_fields = {
    "Warehouse": [
        {"fieldname": "is_frozen_for_reconciliation", "fieldtype": "Check",
         "label": "Dong bang (Dang kiem ke)", "read_only": 1},
        {"fieldname": "frozen_reconciliation", "fieldtype": "Link",
         "options": "Stock Reconciliation", "label": "Phieu kiem ke", "read_only": 1}
    ]
}

# 2. Server script validate Stock Entry
def validate_warehouse_frozen(doc, method):
    """Block nhap/xuat khi kho dang kiem ke"""
    warehouses = set()
    if doc.from_warehouse:
        warehouses.add(doc.from_warehouse)
    if doc.to_warehouse:
        warehouses.add(doc.to_warehouse)
    for item in doc.items:
        if item.s_warehouse:
            warehouses.add(item.s_warehouse)
        if item.t_warehouse:
            warehouses.add(item.t_warehouse)

    for wh in warehouses:
        if frappe.db.get_value("Warehouse", wh, "is_frozen_for_reconciliation"):
            frappe.throw(f"Kho {wh} dang trong qua trinh kiem ke. Khong the nhap/xuat.")

# 3. Workflow cho Stock Reconciliation
workflow = {
    "states": [
        {"state": "Draft", "doc_status": 0},
        {"state": "Pending Approval", "doc_status": 0},
        {"state": "Approved", "doc_status": 0},
        {"state": "Submitted", "doc_status": 1},
        {"state": "Cancelled", "doc_status": 2}
    ],
    "transitions": [
        {"source": "Draft", "target": "Pending Approval", "action": "Submit for Approval"},
        {"source": "Pending Approval", "target": "Approved", "action": "Approve", "allowed": "Accounts Manager"},
        {"source": "Pending Approval", "target": "Draft", "action": "Reject"},
        {"source": "Approved", "target": "Submitted", "action": "Submit"}
    ]
}
```

**Chi tiet ERP-WH-017 (Xu ly chenh lech):**

ERPNext hien tai: Khi submit Stock Reconciliation, tu dong dieu chinh ton kho (tao Stock Ledger Entry). Khong co buoc trung gian de ke toan duyet chenh lech.

DCNET yeu cau:
1. Thu kho nhap so luong thuc te
2. He thong tinh chenh lech (hien thi: current_qty, actual_qty, difference)
3. **Ke toan duyet** chenh lech truoc khi submit
4. Sau khi duyet, he thong tu dong tao phieu nhap/xuat chenh lech

**Approach:** Su dung Workflow (da mo ta o ERP-WH-016) + server hook `on_submit` de tao Stock Entry cho phan chenh lech.

---

#### 2.2.6. Bao cao ton kho (3 features)

| # | Feature ID | Ten | Priority | ERPNext Equivalent | Coverage | Gap cu the | Effort |
|---|-----------|------|----------|-------------------|----------|------------|--------|
| 18 | ERP-WH-018 | BC ton kho | Critical | Stock Balance Report | Native | ERPNext Stock Balance report day du: item, warehouse, actual_qty, reserved_qty, ordered_qty, projected_qty, valuation_rate, stock_value. Filter theo item_group, warehouse, date. | 0 |
| 19 | ERP-WH-019 | BC gia tri ton | High | Stock Ledger Report + Stock Value Report | Native | ERPNext co: Stock Ledger (chi tiet giao dich), Stock Value Report (gia tri ton theo warehouse). Can config de hien thi VND format dung. | 0.5 ngay (config) |
| 20 | ERP-WH-020 | Canh bao ton | High | Reorder Level (Item) | Customize | ERPNext co Reorder Level trong Item: khi ton < reorder_level, tu dong tao Material Request. **Gap:** Can them canh bao real-time (notification, email, dashboard widget) thay vi chi tao Material Request. | 2-3 ngay |

**Chi tiet ERP-WH-020 (Canh bao ton kho):**

ERPNext da co:
- Item DocType: `reorder_level`, `reorder_qty` (theo warehouse)
- Auto Material Request: khi ton < reorder_level, he thong tu dong tao Material Request (Purchase)
- Stock Projected Qty report

Can them:
```python
# 1. Scheduled Job: Check low stock hang ngay va gui notification
def check_low_stock_alerts():
    """Kiem tra va gui canh bao ton kho thap"""
    low_items = frappe.db.sql("""
        SELECT b.item_code, b.warehouse, b.actual_qty,
               ir.warehouse_reorder_level, ir.warehouse_reorder_qty,
               i.item_name
        FROM tabBin b
        JOIN tabItem i ON i.name = b.item_code
        JOIN `tabItem Reorder` ir ON ir.parent = i.name AND ir.warehouse = b.warehouse
        WHERE b.actual_qty <= ir.warehouse_reorder_level
        AND b.actual_qty > 0
    """, as_dict=True)

    for item in low_items:
        # Gui notification cho Stock Manager
        frappe.publish_realtime("low_stock_alert", {
            "item_code": item.item_code,
            "warehouse": item.warehouse,
            "actual_qty": item.actual_qty,
            "reorder_level": item.warehouse_reorder_level
        })

# 2. Dashboard widget hien thi low stock items (xem Section 3.7)
```

---

### 2.3. Phase 2: Report Features (5 features)

| # | Feature ID | Ten | Priority | ERPNext Equivalent | Coverage | Gap cu the | Effort |
|---|-----------|------|----------|-------------------|----------|------------|--------|
| 1 | ERP-WH-021 | BC nhap xuat ton | Critical | Khong co (format TT200) | Custom Dev | ERPNext co Stock Ledger nhung **khong co** bao cao theo format TT200 Viet Nam (Bao cao nhap xuat ton: ton dau, nhap trong ky, xuat trong ky, ton cuoi). Can tao Script Report moi. | 5-7 ngay |
| 2 | ERP-WH-022 | BC theo lo | High | Batch-Wise Balance History | Customize | ERPNext co Batch-Wise Balance report. **Gap nho:** Can them filter theo warehouse, them cot expiry_date, highlight lo sap het han. Co the customize bang Script Report extension. | 1-2 ngay |
| 3 | ERP-WH-023 | BC theo serial | High | Khong co (Script Report) | Custom Dev | ERPNext co Serial No list nhung **khong co** bao cao tong hop serial theo trang thai, warehouse, item_group. Can tao Script Report moi. | 3-4 ngay |
| 4 | ERP-WH-024 | BC theo vi tri | Medium | Khong co | Custom Dev | Phu thuoc ERP-WH-011 (Warehouse Location). Can tao sau khi co Location DocType. Script Report query ton kho theo Khu/Ke/O. | 2-3 ngay |
| 5 | ERP-WH-025 | BC gia nhap XBQ | High | Khong co (Script Report) | Custom Script | ERPNext co Stock Ledger voi valuation_rate nhung **khong co** bao cao gia nhap xuat binh quan theo thang (format ke toan VN). Can tao Script Report moi. | 3-5 ngay |

**Chi tiet ERP-WH-021 (Bao cao nhap xuat ton theo TT200):**

Day la bao cao quan trong nhat cua module kho theo chuan ke toan Viet Nam. Format:

```
+-----------+------------+--------+-----------+-----------+-----------+-----------+
| Ma hang   | Ten hang   | DVT    | Ton dau   | Nhap      | Xuat      | Ton cuoi  |
|           |            |        | SL | GT   | SL | GT   | SL | GT   | SL | GT   |
+-----------+------------+--------+----+------+----+------+----+------+----+------+
| SP-001    | Golf Club  | Cai    | 10 | 50M  | 20 | 100M | 15 | 75M  | 15 | 75M  |
| SP-002    | Golf Ball  | Hop    | 50 | 25M  | 100| 50M  | 80 | 40M  | 70 | 35M  |
+-----------+------------+--------+----+------+----+------+----+------+----+------+
| TONG      |            |        |    | 75M  |    | 150M |    | 115M |    | 110M |
+-----------+------------+--------+----+------+----+------+----+------+----+------+
```

**Approach:** Script Report trong dcnet_apps:

```python
# dcnet_apps/dcnet_apps/report/bao_cao_nhap_xuat_ton/bao_cao_nhap_xuat_ton.py
def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_data(filters):
    """
    Query Stock Ledger Entry de tinh:
    - Ton dau = SUM(actual_qty) WHERE posting_date < from_date
    - Nhap trong ky = SUM(actual_qty) WHERE actual_qty > 0 AND posting_date BETWEEN from_date AND to_date
    - Xuat trong ky = SUM(ABS(actual_qty)) WHERE actual_qty < 0 AND posting_date BETWEEN from_date AND to_date
    - Ton cuoi = Ton dau + Nhap - Xuat
    """
    # Query logic here
    pass
```

**Filters:** Company, Warehouse, Item Group, From Date, To Date

---

### 2.4. Web Sync Features (2 features)

| # | Feature ID | Ten | Priority | ERPNext Equivalent | Coverage | Gap cu the | Effort |
|---|-----------|------|----------|-------------------|----------|------------|--------|
| 1 | ERP-WEB-003 | Dong bo kho | High | Khong co | Custom Dev | ERPNext **khong co** dong bo kho voi website ben ngoai (WooCommerce, Shopify). Can tao API endpoint + webhook de sync warehouse data. Tuy nhien, giai doan dau co the dung ERPNext E-commerce module (neu website tren ERPNext). | 3-5 ngay |
| 2 | ERP-WEB-005 | Dong bo ton kho real-time | Critical | Khong co | Custom Dev | Can tao mechanism dong bo ton kho real-time: (1) Hook vao Stock Ledger Entry after_insert de publish event, (2) Webhook/API push ton kho ra website, (3) Can xu ly rate limiting va conflict. | 5-7 ngay |

**Chi tiet ERP-WEB-005 (Dong bo ton kho real-time):**

ERPNext co:
- **Webhook** DocType: co the config webhook khi document thay doi
- **Event Streaming:** frappe.publish_realtime() cho internal events
- **REST API:** Full CRUD API cho tat ca DocType

Can custom:
```python
# hooks.py
doc_events = {
    "Stock Ledger Entry": {
        "after_insert": "dcnet_apps.stock.sync.on_stock_update"
    }
}

# dcnet_apps/stock/sync.py
def on_stock_update(doc, method):
    """Dong bo ton kho khi co thay doi"""
    item_code = doc.item_code
    warehouse = doc.warehouse
    qty_after = doc.qty_after_transaction

    # Lay tong ton across all warehouses (cho website)
    total_qty = frappe.db.sql("""
        SELECT SUM(actual_qty) as total
        FROM tabBin
        WHERE item_code = %s
    """, item_code, as_dict=True)[0].total or 0

    # Push to external website
    push_stock_to_website(item_code, total_qty)

def push_stock_to_website(item_code, qty):
    """Push ton kho ra website qua API"""
    # WooCommerce API / Custom API
    # Rate limit: max 1 update per item per 5 seconds
    pass
```

**Risks:**
- Performance: Stock Ledger Entry co the insert hang tram records moi ngay
- Rate limiting: Can batch updates (5-second delay) de tranh overload website API
- Conflict: Neu website cung co the ban hang, can xu ly concurrent stock updates

---

## 3. Chi tiet tung feature can custom development

### 3.1. Barcode / Label Module -- 3-4 tuan

#### Scope

- **ERP-WH-013:** Gan barcode cho san pham (auto-generate theo quy uoc)
- **ERP-WH-014:** Tao tem nhan (template + preview)
- **ERP-WH-015:** In tem hang loat (batch printing, PDF export)

#### Yeu cau chi tiet

**Tu ERP_SPECIFICATION.md Section 4 (lines 598-612):**

1. **Loai tem:**
   - Tem tu tao (barcode_value = `ma_vat_tu + ";;" + so_lo`)
   - Tem nha cung cap (barcode_value = `so_seri`)

2. **Thong tin tren tem:**
   - Ma vach (barcode image)
   - Ma vat tu, ten vat tu
   - Don vi tinh
   - So seri (neu co)
   - So lo (neu co)
   - Nha cung cap
   - Nuoc san xuat
   - Don vi nhap khau

3. **Tinh nang:**
   - Ke thua du lieu tu phieu nhap khau (Purchase Receipt)
   - In hang loat (chon nhieu item, in nhieu tem)
   - Ho tro nhieu kich thuoc tem (30x20mm, 50x25mm, 100x50mm)
   - Export PDF de in

#### Technical approach

**1. DocType moi: Barcode Label**

```python
# Barcode Label DocType
{
    "doctype": "Barcode Label",
    "module": "DCNET Stock",
    "fields": [
        # Header
        {"fieldname": "posting_date", "fieldtype": "Date", "default": "Today"},
        {"fieldname": "label_type", "fieldtype": "Select",
         "options": "Tem tu tao\nTem nha cung cap"},
        {"fieldname": "purchase_receipt", "fieldtype": "Link", "options": "Purchase Receipt"},
        {"fieldname": "supplier", "fieldtype": "Link", "options": "Supplier"},
        {"fieldname": "country_of_origin", "fieldtype": "Data"},
        {"fieldname": "import_company", "fieldtype": "Link", "options": "Company"},

        # Items (child table)
        {"fieldname": "items", "fieldtype": "Table", "options": "Barcode Label Item"},

        # Print settings
        {"fieldname": "label_size", "fieldtype": "Select",
         "options": "30x20mm\n50x25mm\n100x50mm\nCustom"},
        {"fieldname": "label_format", "fieldtype": "Select",
         "options": "Code128\nEAN-13\nQR Code"}
    ]
}

# Barcode Label Item (child DocType)
{
    "doctype": "Barcode Label Item",
    "fields": [
        {"fieldname": "item_code", "fieldtype": "Link", "options": "Item"},
        {"fieldname": "item_name", "fieldtype": "Data", "fetch_from": "item_code.item_name"},
        {"fieldname": "uom", "fieldtype": "Link", "options": "UOM"},
        {"fieldname": "batch_no", "fieldtype": "Link", "options": "Batch"},
        {"fieldname": "serial_no", "fieldtype": "Small Text"},
        {"fieldname": "barcode_value", "fieldtype": "Data"},  # Auto-generate
        {"fieldname": "qty", "fieldtype": "Int", "label": "So luong tem in", "default": 1}
    ]
}
```

**2. Barcode generation (python-barcode library):**

```python
import barcode
from barcode.writer import ImageWriter
from io import BytesIO

def generate_barcode_image(value, format="code128"):
    """Tao barcode image tu gia tri"""
    barcode_class = barcode.get_barcode_class(format)
    bc = barcode_class(value, writer=ImageWriter())
    buffer = BytesIO()
    bc.write(buffer)
    return buffer.getvalue()

def auto_generate_barcode_value(label_type, item_code, batch_no=None, serial_no=None):
    """Tao gia tri barcode theo quy uoc"""
    if label_type == "Tem tu tao":
        return f"{item_code};;{batch_no or ''}"
    elif label_type == "Tem nha cung cap":
        return serial_no or ""
```

**3. Label template (Jinja + CSS):**

```html
<!-- Print Format: Barcode Label -->
<style>
.label-container { display: flex; flex-wrap: wrap; }
.label {
    width: {{ label_width }}mm;
    height: {{ label_height }}mm;
    border: 1px solid #ccc;
    padding: 2mm;
    margin: 1mm;
    font-size: 8pt;
    page-break-inside: avoid;
}
.barcode-img { text-align: center; }
</style>

<div class="label-container">
{% for item in doc.items %}
{% for i in range(item.qty) %}
<div class="label">
    <div class="barcode-img">
        <img src="{{ get_barcode_image(item.barcode_value) }}" />
    </div>
    <div>{{ item.item_code }} - {{ item.item_name }}</div>
    {% if item.batch_no %}<div>Lo: {{ item.batch_no }}</div>{% endif %}
    {% if item.serial_no %}<div>SN: {{ item.serial_no }}</div>{% endif %}
    <div>{{ doc.supplier_name }} | {{ doc.country_of_origin }}</div>
</div>
{% endfor %}
{% endfor %}
</div>
```

**4. Get Items from Purchase Receipt (Button):**

```javascript
// Client Script: Barcode Label
frappe.ui.form.on("Barcode Label", {
    purchase_receipt: function(frm) {
        if (frm.doc.purchase_receipt) {
            frappe.call({
                method: "dcnet_apps.stock.barcode.get_items_from_purchase_receipt",
                args: { purchase_receipt: frm.doc.purchase_receipt },
                callback: function(r) {
                    frm.clear_table("items");
                    for (let item of r.message) {
                        let row = frm.add_child("items");
                        Object.assign(row, item);
                    }
                    frm.refresh_field("items");
                }
            });
        }
    }
});
```

#### Effort breakdown

| Task | Effort | Chi tiet |
|------|--------|----------|
| DocType design & creation (Barcode Label + child) | 2 ngay | JSON DocType, fixtures, permissions |
| Barcode generation logic (python-barcode) | 2 ngay | Library install, server-side generation, caching |
| Auto-generate barcode value theo quy uoc | 1 ngay | Tem tu tao vs Tem NCC logic |
| Label template design (3 kich thuoc) | 3 ngay | Jinja template, CSS responsive, preview |
| Print format (A4 layout, multiple labels per page) | 2 ngay | Page break, alignment, margin |
| "Get Items from Purchase Receipt" button | 1 ngay | Client script + whitelisted method |
| Batch printing (chon nhieu item, export PDF) | 2 ngay | Bulk select, PDF merge |
| Scanner integration (USB HID barcode scanner) | 2 ngay | Input field auto-focus, scan-to-field |
| Testing & QA | 2 ngay | Unit test, print test voi may in thuc te |
| **Tong** | **~17 ngay (3.5 tuan)** | |

#### Risks

| Risk | Impact | Xac suat | Mitigation |
|------|--------|----------|------------|
| Barcode format khong duoc confirm (EAN-13 / Code128 / QR) | Medium | Cao | Hoi khach hang som, ho tro nhieu format |
| Kich thuoc tem khong phu hop voi may in | Medium | Trung binh | Test voi may in thuc te cua khach |
| python-barcode library khong tuong thich voi Frappe | Low | Thap | Da kiem tra, compatible |
| Scanner model khong ro | Medium | Cao | Phan lon USB HID scanner deu tuong thich (keyboard emulation) |

---

### 3.2. Warehouse Location (Vi tri kho) -- 1.5-2 tuan

#### Scope

- **ERP-WH-011:** Quan ly vi tri trong kho (Khu / Ke / O)
- **ERP-WH-024:** Bao cao ton kho theo vi tri

#### Yeu cau nghiep vu

Tu ERP_SPECIFICATION.md Section 4:
- Theo doi nhap/xuat/ton theo vi tri trong kho
- Hierarchy 3 cap: **Khu** (Zone) -> **Ke** (Rack) -> **O** (Bin/Shelf)
- Dieu chuyen vi tri (Buoc 8: Phieu dieu chuyen vi tri)
- Bao cao ton theo vi tri

#### Technical approach

**1. DocType moi: Warehouse Location**

```python
{
    "doctype": "Warehouse Location",
    "module": "DCNET Stock",
    "is_tree": True,  # Su dung NestedSet de co hierarchy
    "fields": [
        {"fieldname": "location_name", "fieldtype": "Data", "reqd": 1},
        {"fieldname": "location_code", "fieldtype": "Data", "unique": 1},
        {"fieldname": "warehouse", "fieldtype": "Link", "options": "Warehouse", "reqd": 1},
        {"fieldname": "location_type", "fieldtype": "Select",
         "options": "Zone\nRack\nBin", "reqd": 1},
        {"fieldname": "parent_warehouse_location", "fieldtype": "Link",
         "options": "Warehouse Location"},
        {"fieldname": "capacity", "fieldtype": "Int", "label": "Suc chua (so luong)"},
        {"fieldname": "is_group", "fieldtype": "Check"},
        {"fieldname": "disabled", "fieldtype": "Check"}
    ],
    "nsm_parent_field": "parent_warehouse_location"
}
```

**2. Them custom field vao Stock Entry Item:**

```python
custom_fields = {
    "Stock Entry Detail": [
        {
            "fieldname": "warehouse_location",
            "fieldtype": "Link",
            "options": "Warehouse Location",
            "label": "Vi tri kho",
            "insert_after": "t_warehouse"
        }
    ],
    "Stock Reconciliation Item": [
        {
            "fieldname": "warehouse_location",
            "fieldtype": "Link",
            "options": "Warehouse Location",
            "label": "Vi tri kho",
            "insert_after": "warehouse"
        }
    ]
}
```

**3. Custom report: Stock by Location**

```python
# Script Report: Stock by Location
def execute(filters=None):
    columns = [
        {"fieldname": "warehouse", "label": "Kho", "fieldtype": "Link", "options": "Warehouse"},
        {"fieldname": "location", "label": "Vi tri", "fieldtype": "Link", "options": "Warehouse Location"},
        {"fieldname": "location_type", "label": "Loai", "fieldtype": "Data"},
        {"fieldname": "item_code", "label": "Ma hang", "fieldtype": "Link", "options": "Item"},
        {"fieldname": "item_name", "label": "Ten hang", "fieldtype": "Data"},
        {"fieldname": "actual_qty", "label": "Ton thuc te", "fieldtype": "Float"},
        {"fieldname": "stock_value", "label": "Gia tri ton", "fieldtype": "Currency"},
    ]

    data = frappe.db.sql("""
        SELECT
            sle.warehouse,
            sed.warehouse_location as location,
            wl.location_type,
            sle.item_code,
            i.item_name,
            SUM(sle.actual_qty) as actual_qty,
            SUM(sle.stock_value_difference) as stock_value
        FROM `tabStock Ledger Entry` sle
        JOIN `tabStock Entry Detail` sed ON sed.parent = sle.voucher_no
            AND sed.item_code = sle.item_code
        JOIN `tabWarehouse Location` wl ON wl.name = sed.warehouse_location
        JOIN `tabItem` i ON i.name = sle.item_code
        WHERE sle.is_cancelled = 0
        {conditions}
        GROUP BY sle.warehouse, sed.warehouse_location, sle.item_code
        HAVING SUM(sle.actual_qty) != 0
    """, filters, as_dict=True)

    return columns, data
```

#### Effort breakdown

| Task | Effort | Chi tiet |
|------|--------|----------|
| DocType Warehouse Location (Tree structure) | 2 ngay | NestedSet, fixtures, permissions |
| Custom fields tren Stock Entry Item | 1 ngay | Property Setter, dependency filter |
| Location filter (chi hien thi vi tri cua warehouse duoc chon) | 1 ngay | Client script, get_query |
| Phieu dieu chuyen vi tri (Stock Entry subtype) | 1 ngay | Purpose "Location Transfer" |
| Script Report: Stock by Location | 2 ngay | Query, chart, drill-down |
| Testing | 1 ngay | Unit test, data entry test |
| **Tong** | **~8 ngay (1.5 tuan)** | |

#### Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| Khach khong ro cau truc vi tri (bao nhieu khu, ke, o) | Medium | Hoi khach va cho mau template |
| Performance voi so luong vi tri lon | Low | NestedSet cua Frappe da toi uu |
| Conflict voi Bin DocType cua ERPNext | Low | Warehouse Location la DocType rieng, khong can sua Bin |

#### Phuong an thay the (descope)

**Neu khach dong y:** Co the dung Warehouse hierarchy thay vi Location moi:
- Tao warehouse con cho tung vi tri: `Kho HN > Khu A > Ke 1 > O 1`
- Uu diem: Khong can custom, dung native Bin tracking
- Nhuoc diem: Warehouse tree se rat lon, query cham

**Khuyen nghi:** Tao DocType moi (Warehouse Location) de tach biet logic vi tri va logic kho.

---

### 3.3. Stock Reconciliation Custom (Freeze + Approval) -- 1-1.5 tuan

#### Scope

- **ERP-WH-016:** Kiem ke kho voi freeze warehouse va approval workflow
- **ERP-WH-017:** Xu ly chenh lech voi ke toan duyet truoc

#### Gap chi tiet

| Tinh nang | ERPNext native | DCNET yeu cau | Gap |
|-----------|----------------|---------------|-----|
| Nhap so luong thuc te | Co (Stock Reconciliation Item) | Co | Khong gap |
| Tu dong tinh chenh lech | Co (current_qty - qty) | Co | Khong gap |
| Freeze warehouse | **Khong co** (chi co Stock Freeze Upto global) | Freeze 1 warehouse cu the | Can custom |
| Approval workflow | **Khong co** workflow | Ke toan phai duyet truoc khi submit | Can custom |
| Tao phieu nhap/xuat chenh lech rieng | **Khong co** (tu dong adjust) | Tao Stock Entry rieng cho chenh lech | Can custom |
| Lenh kiem ke (buoc 9) | **Khong co** | Ke toan tao lenh kiem ke truoc | Can custom |

#### Technical approach

**1. Custom Workflow cho Stock Reconciliation:**

Da mo ta chi tiet o Section 2.2.5. Tao Workflow voi states:
- Draft -> Counting (bat dau kiem, freeze warehouse)
- Counting -> Counted (nhap xong so lieu)
- Counted -> Pending Approval (gui ke toan duyet chenh lech)
- Pending Approval -> Submitted (ke toan duyet, submit)
- Any -> Cancelled

**2. Freeze/Unfreeze warehouse logic:**

```python
# hooks.py
doc_events = {
    "Stock Reconciliation": {
        "on_update_after_submit": "dcnet_apps.stock.reconciliation.unfreeze_warehouse",
        "on_cancel": "dcnet_apps.stock.reconciliation.unfreeze_warehouse"
    },
    "Stock Entry": {
        "validate": "dcnet_apps.stock.reconciliation.check_frozen_warehouse"
    },
    "Purchase Receipt": {
        "validate": "dcnet_apps.stock.reconciliation.check_frozen_warehouse_pr"
    },
    "Delivery Note": {
        "validate": "dcnet_apps.stock.reconciliation.check_frozen_warehouse_dn"
    }
}
```

**3. Lenh kiem ke (Stock Reconciliation Order):**

Co the implement bang cach them custom fields vao Stock Reconciliation (them field `reconciliation_order_date`, `ordered_by`, `order_remarks`) thay vi tao DocType moi. Lenh kiem ke thuc chat la Stock Reconciliation o trang thai Draft voi workflow state "Ordered".

#### Effort breakdown

| Task | Effort | Chi tiet |
|------|--------|----------|
| Custom fields tren Warehouse + Stock Reconciliation | 1 ngay | is_frozen_for_reconciliation, freeze timestamps |
| Workflow setup (5 states, transitions, permissions) | 1 ngay | Frappe Workflow DocType |
| Freeze/Unfreeze server logic | 1 ngay | Hook vao Stock Entry, Purchase Receipt, Delivery Note validate |
| Tao phieu nhap/xuat chenh lech tu dong | 1 ngay | Server hook on_submit |
| Notification (gui thong bao khi freeze, khi co chenh lech) | 0.5 ngay | Notification DocType |
| Testing | 1.5 ngay | Test freeze block, workflow transitions, concurrent access |
| **Tong** | **~6 ngay (1.2 tuan)** | |

#### Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| Freeze warehouse anh huong cac phieu dang Draft | Medium | Chi block submit/validate, khong block save Draft |
| Concurrent access: 2 user tao Stock Entry cung luc khi kho frozen | Low | Check o validate level, khong can DB lock |
| Performance: check frozen on every Stock Entry validate | Low | Simple DB query (1 field check) |

---

### 3.4. Monthly Average Costing Gap -- 1-2 tuan (neu chon Option B)

#### Van de

- **Khach yeu cau:** Phuong phap gia von **trung binh thang** (Weighted Average Monthly)
  - Cong thuc: `Gia von = (GT ton dau + GT nhap trong thang) / (SL ton dau + SL nhap trong thang)`
  - Ap dung vao **tat ca phieu xuat** trong thang
  - Chay **cuoi thang** (batch job)

- **ERPNext ho tro:** FIFO, Moving Average, LIFO (v16)
  - **Moving Average:** Tinh gia von ngay khi co giao dich nhap moi
  - Cong thuc: `New Rate = (Existing Value + New Value) / (Existing Qty + New Qty)`
  - Ap dung **real-time** (khong phai cuoi thang)

#### So sanh chi tiet

| Tieu chi | Trung binh thang (khach yeu cau) | Moving Average (ERPNext) |
|----------|--------------------------------|-------------------------|
| **Thoi diem tinh** | Cuoi thang (batch) | Real-time (moi giao dich) |
| **Anh huong** | Tat ca xuat trong thang dung 1 gia | Moi xuat co gia khac nhau |
| **Do chinh xac** | Trung binh cho ca thang | Chinh xac hon theo thoi gian |
| **Phuc tap** | Can job cuoi thang recalculate | Tu dong, khong can can thiep |
| **Bao cao** | Don gian (1 gia von/thang) | Phuc tap (nhieu gia von) |
| **Chuan VN** | Dung TT200 (pho bien) | Chap nhan duoc (TT200 cho phep) |

#### Options

**Option A: Dung Moving Average (KHUYEN NGHI) -- 0 effort**

- TT200/2014 cho phep ca Moving Average va Weighted Average
- Khac biet so voi trung binh thang la khong dang ke (< 1-2% gia tri)
- ERPNext da implement Moving Average rat tot, da test ky
- Khong can custom code nao

**Uu diem:**
- 0 effort, 0 risk
- Real-time gia von (khong phai doi cuoi thang)
- Bao cao luc nao cung chinh xac

**Nhuoc diem:**
- Khach co the khong dong y (vi khac BRAVO cu)
- Gia von moi phieu xuat co the khac nhau (khach quen 1 gia von/thang)

**Option B: Custom Monthly Average Recalculation -- 1-2 tuan**

Giu Moving Average lam primary, them job cuoi thang de recalculate:

```python
# dcnet_apps/stock/monthly_average.py

@frappe.whitelist()
def recalculate_monthly_average(company, month, year):
    """
    Tinh lai gia von trung binh thang cho tat ca item

    Logic:
    1. Lay ton dau thang (SL + GT) tu Stock Ledger Entry
    2. Lay tong nhap trong thang (SL + GT)
    3. Tinh gia von TB = (GT ton dau + GT nhap) / (SL ton dau + SL nhap)
    4. Cap nhat valuation_rate cho tat ca phieu xuat trong thang
    5. Recalculate stock_value cho Stock Ledger Entry
    6. Recalculate GL Entry (602, 1561)
    """
    from_date = f"{year}-{month:02d}-01"
    to_date = get_last_day(from_date)

    items = get_all_items_with_movement(company, from_date, to_date)

    for item in items:
        # 1. Ton dau
        opening = get_opening_balance(item.item_code, item.warehouse, from_date)

        # 2. Nhap trong thang
        receipts = get_receipts_in_period(item.item_code, item.warehouse, from_date, to_date)

        # 3. Tinh gia von TB
        total_qty = opening.qty + receipts.qty
        total_value = opening.value + receipts.value
        avg_rate = total_value / total_qty if total_qty > 0 else 0

        # 4. Cap nhat phieu xuat
        update_issue_valuation(item.item_code, item.warehouse, from_date, to_date, avg_rate)

        # 5. Recalculate SLE
        recalculate_sle(item.item_code, item.warehouse, from_date)

    # 6. Repost GL
    repost_gl_entries(company, from_date, to_date)
```

**Effort Option B:**

| Task | Effort |
|------|--------|
| Monthly average calculation logic | 3 ngay |
| Repost Stock Ledger Entry | 2 ngay |
| Repost GL Entry | 2 ngay |
| UI (button trong Stock Settings hoac custom page) | 1 ngay |
| Testing (verify gia von, GL balance) | 2-3 ngay |
| **Tong** | **~10-11 ngay (2 tuan)** |

**Risks Option B:**

| Risk | Impact | Mitigation |
|------|--------|------------|
| Repost SLE co the gay inconsistency | **Cao** | Backup truoc khi chay, rollback neu loi |
| GL Entry bi sai sau repost | **Cao** | Test ky voi du lieu mau, verify balance |
| Performance voi du lieu lon | Medium | Chay background job (enqueue), co progress bar |
| Conflict voi ERPNext updates | Medium | Repost dung ERPNext API (frappe.enqueue_repost_sle) |

**KHUYEN NGHI:** Trinh bay ca 2 option cho khach, de nghi dung **Option A (Moving Average)** vi:
1. TT200 chap nhan ca 2 phuong phap
2. Khac biet gia tri khong dang ke
3. Giam 2 tuan effort + giam risk

---

### 3.5. Serial Status Custom -- 3-5 ngay

#### Gap

| Serial Status | ERPNext | DCNET | Mapping |
|---------------|---------|-------|---------|
| Active | Co | In Stock | 1:1 |
| Inactive | Co | - | Khong dung |
| Delivered | Co | Sold | 1:1 |
| - | Khong co | On Consignment | **Gap** |
| - | Khong co | Trade-in | **Gap** |
| - | Khong co | Disposed | **Gap** |

#### Technical approach

**Approach 1 (Khuyen nghi):** Them custom field `dcnet_status` (Select) vao Serial No DocType.

```python
# fixtures/custom_field.py
custom_fields = {
    "Serial No": [
        {
            "fieldname": "dcnet_status",
            "fieldtype": "Select",
            "label": "Trang thai DCNET",
            "options": "\nIn Stock\nOn Consignment\nSold\nTrade-in\nDisposed",
            "insert_after": "status",
            "in_list_view": 1,
            "in_standard_filter": 1
        },
        {
            "fieldname": "consignment_warehouse",
            "fieldtype": "Link",
            "options": "Warehouse",
            "label": "Kho ky gui",
            "depends_on": "eval:doc.dcnet_status=='On Consignment'",
            "insert_after": "dcnet_status"
        },
        {
            "fieldname": "trade_in_date",
            "fieldtype": "Date",
            "label": "Ngay trade-in",
            "depends_on": "eval:doc.dcnet_status=='Trade-in'",
            "insert_after": "consignment_warehouse"
        }
    ]
}
```

**Tu dong cap nhat status:**

```python
# hooks.py - Tu dong cap nhat dcnet_status
def update_serial_dcnet_status(doc, method):
    """Cap nhat dcnet_status khi Serial No thay doi"""
    if doc.status == "Active" and doc.warehouse:
        # Check neu warehouse la kho ky gui
        wh_type = frappe.db.get_value("Warehouse", doc.warehouse, "warehouse_type")
        if wh_type == "Consignment":
            doc.dcnet_status = "On Consignment"
            doc.consignment_warehouse = doc.warehouse
        else:
            doc.dcnet_status = "In Stock"
    elif doc.status == "Delivered":
        doc.dcnet_status = "Sold"
```

**Approach 2 (Phuc tap hon):** Override `status` field cua Serial No. **Khong khuyen nghi** vi se conflict voi ERPNext internal logic (nhieu controller check `status` field).

#### Effort breakdown

| Task | Effort |
|------|--------|
| Custom fields (dcnet_status, consignment_warehouse, trade_in_date) | 0.5 ngay |
| Auto-update server script | 1 ngay |
| List view filter va indicator | 0.5 ngay |
| Report: Serial No by Status | 1 ngay |
| Testing | 1 ngay |
| **Tong** | **~4 ngay** |

---

### 3.6. Dashboard Widgets -- 1-1.5 tuan

#### Custom widgets can tao

| # | Widget | Mo ta | Data source | Priority |
|---|--------|-------|-------------|----------|
| 1 | Low Stock Items | Danh sach item co ton < reorder_level | Bin + Item Reorder | High |
| 2 | Expiring Batches | Danh sach lo hang sap het han (30 ngay) | Batch | High |
| 3 | Stock Movement Summary | Tong nhap/xuat/dieu chuyen 7 ngay | Stock Ledger Entry | Medium |
| 4 | Stock Value by Category | Gia tri ton kho theo nhom hang (pie chart) | Bin + Item | Medium |
| 5 | Warehouse Utilization | % su dung kho (neu co capacity) | Bin + Warehouse | Low |

#### Technical approach

**Workspace custom page** trong dcnet_apps:

```python
# dcnet_apps/stock/page/stock_dashboard/stock_dashboard.py

@frappe.whitelist()
def get_dashboard_data():
    """API endpoint cho Stock Dashboard"""
    return {
        "low_stock": get_low_stock_items(),
        "expiring_batches": get_expiring_batches(),
        "movement_summary": get_movement_summary(),
        "value_by_category": get_value_by_category(),
        "warehouse_utilization": get_warehouse_utilization()
    }

def get_low_stock_items(limit=20):
    return frappe.db.sql("""
        SELECT b.item_code, i.item_name, b.warehouse,
               b.actual_qty, ir.warehouse_reorder_level,
               ROUND(b.actual_qty / ir.warehouse_reorder_level * 100, 1) as stock_pct
        FROM tabBin b
        JOIN tabItem i ON i.name = b.item_code
        JOIN `tabItem Reorder` ir ON ir.parent = i.name AND ir.warehouse = b.warehouse
        WHERE b.actual_qty <= ir.warehouse_reorder_level
        AND b.actual_qty > 0
        ORDER BY stock_pct ASC
        LIMIT %s
    """, limit, as_dict=True)

def get_expiring_batches(days=30):
    return frappe.db.sql("""
        SELECT b.name, b.item, i.item_name, b.expiry_date, b.batch_qty,
               DATEDIFF(b.expiry_date, CURDATE()) as days_left
        FROM tabBatch b
        JOIN tabItem i ON i.name = b.item
        WHERE b.expiry_date BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL %s DAY)
        AND b.batch_qty > 0
        ORDER BY b.expiry_date ASC
    """, days, as_dict=True)

def get_movement_summary(days=7):
    from_date = add_days(today(), -days)
    return frappe.db.sql("""
        SELECT
            SUM(CASE WHEN actual_qty > 0 THEN actual_qty ELSE 0 END) as total_in,
            SUM(CASE WHEN actual_qty < 0 THEN ABS(actual_qty) ELSE 0 END) as total_out,
            COUNT(DISTINCT voucher_no) as total_vouchers,
            SUM(CASE WHEN actual_qty > 0 THEN stock_value_difference ELSE 0 END) as value_in,
            SUM(CASE WHEN actual_qty < 0 THEN ABS(stock_value_difference) ELSE 0 END) as value_out
        FROM `tabStock Ledger Entry`
        WHERE posting_date >= %s AND is_cancelled = 0
    """, from_date, as_dict=True)[0]
```

#### Effort breakdown

| Task | Effort |
|------|--------|
| Dashboard page setup (HTML + JS) | 1 ngay |
| Low Stock widget (query + card) | 1 ngay |
| Expiring Batches widget (query + card) | 1 ngay |
| Movement Summary widget (query + chart) | 1 ngay |
| Stock Value by Category (query + pie chart) | 1 ngay |
| Scheduled Job cho alerts (email + notification) | 1 ngay |
| Testing | 1 ngay |
| **Tong** | **~7 ngay (1.5 tuan)** |

---

### 3.7. CCDC Amortization Tracking -- 1 tuan

#### Gap

- **ERPNext:** Co Asset DocType nhung cho tai san co dinh (Fixed Assets), khong phai CCDC (Cong cu dung cu)
- **DCNET yeu cau:** Khi xuat CCDC, can theo doi phan bo gia tri theo thang (VD: xuat CCDC 12 trieu, phan bo 12 thang, moi thang 1 trieu)

#### Technical approach

**Option A (Khuyen nghi): Dung Asset DocType cua ERPNext**

ERPNext Asset ho tro:
- Depreciation Method: Straight Line (Duong thang) -- phu hop voi phan bo CCDC
- Depreciation Schedule: Tu dong tinh theo thang
- GL Entry: Tu dong tao but toan phan bo hang thang
- Asset Category: Co the tao category "CCDC" rieng

**Config:**
```
Asset Category: CCDC
  - Depreciation Method: Straight Line
  - Total Number of Depreciations: (so thang phan bo)
  - Frequency of Depreciation (Months): 1
  - Fixed Asset Account: TK 242 (Chi phi tra truoc)
  - Depreciation Expense Account: TK 642 (Chi phi quan ly)
  - Accumulated Depreciation Account: TK 2141 (Hao mon TSCD)
```

**Gap nho:** CCDC dung TK 242 (Chi phi tra truoc), khong dung TK 211 (TSCD). Can config Account mapping cho dung.

**Option B: Custom DocType CCDC**

Neu khach khong muon dung Asset DocType (vi CCDC khong phai TSCD theo ke toan VN):

```python
{
    "doctype": "CCDC",
    "module": "DCNET Stock",
    "fields": [
        {"fieldname": "item_code", "fieldtype": "Link", "options": "Item"},
        {"fieldname": "warehouse", "fieldtype": "Link", "options": "Warehouse"},
        {"fieldname": "stock_entry", "fieldtype": "Link", "options": "Stock Entry"},
        {"fieldname": "total_value", "fieldtype": "Currency"},
        {"fieldname": "amortization_months", "fieldtype": "Int"},
        {"fieldname": "monthly_amount", "fieldtype": "Currency"},  # total_value / amortization_months
        {"fieldname": "start_date", "fieldtype": "Date"},
        {"fieldname": "debit_account", "fieldtype": "Link", "options": "Account"},  # TK No phan bo
        {"fieldname": "credit_account", "fieldtype": "Link", "options": "Account"},  # TK Co phan bo
        {"fieldname": "amortization_schedule", "fieldtype": "Table", "options": "CCDC Schedule"}
    ]
}
```

#### Effort breakdown

| Task | Effort (Option A) | Effort (Option B) |
|------|-------------------|-------------------|
| Config Asset Category + Accounts | 1 ngay | N/A |
| DocType design | N/A | 2 ngay |
| Amortization schedule logic | 0 (ERPNext co) | 2 ngay |
| Monthly GL Entry auto-post | 0 (ERPNext co) | 2 ngay |
| Bao cao CCDC | 1 ngay | 1 ngay |
| Testing | 1 ngay | 2 ngay |
| **Tong** | **~3 ngay** | **~9 ngay (2 tuan)** |

**Khuyen nghi:** Dung **Option A** (ERPNext Asset) voi config CCDC category. Chi can 3 ngay.

---

### 3.8. Custom Reports -- 2-3 tuan

#### Reports can build

| # | Feature ID | Ten | Loai | Effort |
|---|-----------|------|------|--------|
| 1 | ERP-WH-021 | BC nhap xuat ton (TT200) | Script Report | 5-7 ngay |
| 2 | ERP-WH-023 | BC theo serial | Script Report | 3-4 ngay |
| 3 | ERP-WH-024 | BC theo vi tri | Script Report | 2-3 ngay |
| 4 | ERP-WH-025 | BC gia nhap xuat binh quan | Script Report | 3-5 ngay |

#### Chi tiet ERP-WH-021: BC nhap xuat ton (TT200 format)

Da mo ta chi tiet o Section 2.3. Day la report quan trong nhat.

**Columns:**
- Ma hang, Ten hang, DVT
- Ton dau ky: SL, GT
- Nhap trong ky: SL, GT (tach theo loai: nhap mua, nhap khac, nhap dieu chuyen)
- Xuat trong ky: SL, GT (tach theo loai: xuat ban, xuat khac, xuat dieu chuyen)
- Ton cuoi ky: SL, GT

**Filters:**
- Company (bat buoc)
- Warehouse (da chon hoac tat ca)
- Item Group
- From Date, To Date (bat buoc)

**Data source:** Stock Ledger Entry, gom nhom theo item_code + warehouse

**Output:** Table + Export Excel/PDF

#### Chi tiet ERP-WH-023: BC theo serial

**Columns:**
- Serial No, Item Code, Item Name
- Status (ERPNext), DCNET Status
- Current Warehouse
- Purchase Date, Purchase Rate
- Delivery Date, Customer (neu da ban)
- Age (so ngay tu khi nhap)

**Filters:**
- Company, Warehouse, Item Group
- DCNET Status
- Date Range

#### Chi tiet ERP-WH-025: BC gia nhap xuat binh quan

**Columns:**
- Ma hang, Ten hang, DVT
- Gia nhap binh quan ky (SUM(nhap_value) / SUM(nhap_qty))
- Gia xuat binh quan ky (SUM(xuat_value) / SUM(xuat_qty))
- So sanh: gia nhap vs gia xuat vs gia von hien tai

**Data source:** Stock Ledger Entry

#### Effort breakdown tong

| Task | Effort |
|------|--------|
| BC nhap xuat ton (TT200) | 5-7 ngay |
| BC theo serial | 3-4 ngay |
| BC theo vi tri | 2-3 ngay |
| BC gia nhap xuat BQ | 3-5 ngay |
| **Tong** | **~13-19 ngay (2.5-4 tuan)** |

**Ghi chu:** BC theo vi tri (ERP-WH-024) phu thuoc vao ERP-WH-011 (Warehouse Location DocType). Can lam ERP-WH-011 truoc.

---

### 3.9. Consignment Workflow Integration -- 4-5 tuan

#### Scope

Day la phan **phuc tap nhat** cua module Kho. Lien quan den quy trinh hang ky gui giua Thang Long TM va Nhat Minh Sport.

**Nguon:** ERP_SPECIFICATION.md Section 4 (lines 625-640)

#### Workflow 5 buoc

```
Buoc 1: TL lam phieu xuat dieu chuyen tu Kho Tong -> Kho Ky Gui TL
Buoc 2: Van chuyen thuc te den NM
Buoc 3: NM lam phieu nhap vao Kho Ky Gui NM
Buoc 4: Cuoi thang: NM tong hop SL ban, TL xuat hoa don tu Kho Ky Gui
Buoc 5: NM lam phieu nhap mua vao Kho Xuat Hoa Don
```

#### Cau truc kho

**Thang Long TM:**
- Kho Tong TL (main warehouse)
- Kho Ky Gui TL (consignment out)

**Nhat Minh Sport:**
- Kho Ky Gui NM (consignment in)
- Kho Xuat Hoa Don NM (invoice warehouse)

#### ERPNext coverage

| Buoc | ERPNext | Coverage | Gap |
|------|---------|----------|-----|
| 1 (TL xuat dieu chuyen) | Stock Entry (Material Transfer) | Native | Khong gap |
| 2 (Van chuyen) | Transit Warehouse | Customize | Can config Transit |
| 3 (NM nhap ky gui) | Stock Entry (Material Receipt) | Customize | Can cross-company logic |
| 4 (TL xuat hoa don) | Sales Invoice (inter-company) | Customize | Can config Inter Company Transaction |
| 5 (NM nhap mua) | Purchase Invoice + Purchase Receipt | Customize | Auto-create tu SI |

#### Technical approach

**1. Warehouse setup:**
```python
# Company: Thang Long TM
warehouses_tl = [
    {"name": "Kho Tong - TL", "warehouse_type": ""},
    {"name": "Kho Ky Gui - TL", "warehouse_type": "Consignment"},
    {"name": "Kho Transit - TL", "warehouse_type": "Transit"}
]

# Company: Nhat Minh Sport
warehouses_nm = [
    {"name": "Kho Ky Gui - NM", "warehouse_type": "Consignment"},
    {"name": "Kho Xuat Hoa Don - NM", "warehouse_type": ""},
]
```

**2. Inter Company Transaction:**

ERPNext v16 ho tro Inter Company Transaction:
- Sales Invoice (TL) tu dong tao Purchase Invoice (NM)
- Config trong `Company` DocType: `inter_company_order_reference`

```python
# Company settings
frappe.db.set_value("Company", "Thang Long TM", {
    "allow_inter_company_transaction": 1
})
frappe.db.set_value("Company", "Nhat Minh Sport", {
    "allow_inter_company_transaction": 1
})

# Internal Customer/Supplier
# TL co Internal Customer "Nhat Minh Sport"
# NM co Internal Supplier "Thang Long TM"
```

**3. Monthly reconciliation (Buoc 4):**

Can tao **Custom DocType: Consignment Reconciliation** de tong hop SL ban hang tu kho ky gui hang thang:

```python
{
    "doctype": "Consignment Reconciliation",
    "module": "DCNET Stock",
    "fields": [
        {"fieldname": "company", "fieldtype": "Link", "options": "Company"},
        {"fieldname": "consignment_warehouse", "fieldtype": "Link", "options": "Warehouse"},
        {"fieldname": "month", "fieldtype": "Date"},
        {"fieldname": "items", "fieldtype": "Table", "options": "Consignment Reconciliation Item"},
        {"fieldname": "total_qty", "fieldtype": "Float"},
        {"fieldname": "total_value", "fieldtype": "Currency"},
        {"fieldname": "sales_invoice", "fieldtype": "Link", "options": "Sales Invoice"}
    ]
}

# Child Table
{
    "doctype": "Consignment Reconciliation Item",
    "fields": [
        {"fieldname": "item_code", "fieldtype": "Link", "options": "Item"},
        {"fieldname": "qty_sold", "fieldtype": "Float"},
        {"fieldname": "rate", "fieldtype": "Currency"},
        {"fieldname": "amount", "fieldtype": "Currency"}
    ]
}
```

**4. Auto-create Sales Invoice tu Consignment Reconciliation:**

```python
@frappe.whitelist()
def create_sales_invoice_from_reconciliation(reconciliation_name):
    """Tao Sales Invoice tu TL cho NM dua tren reconciliation"""
    recon = frappe.get_doc("Consignment Reconciliation", reconciliation_name)

    si = frappe.new_doc("Sales Invoice")
    si.company = "Thang Long TM"
    si.customer = "Nhat Minh Sport"  # Internal Customer
    si.set_warehouse = recon.consignment_warehouse
    si.inter_company_invoice_reference = ""  # Se auto-link

    for item in recon.items:
        si.append("items", {
            "item_code": item.item_code,
            "qty": item.qty_sold,
            "rate": item.rate,
            "warehouse": recon.consignment_warehouse
        })

    si.insert()
    si.submit()

    # Auto-create Purchase Invoice tai NM (ERPNext Inter Company feature)
    # ERPNext tu dong tao neu da config Inter Company Transaction

    recon.sales_invoice = si.name
    recon.save()

    return si.name
```

#### Effort breakdown

| Task | Effort | Chi tiet |
|------|--------|----------|
| Warehouse setup (4 kho, hierarchy, types) | 1 ngay | Config, fixtures |
| Inter Company Transaction config | 2 ngay | Internal Customer/Supplier, account mapping |
| Consignment Reconciliation DocType | 3 ngay | DocType, child table, permissions |
| Auto-populate items (query SLE tu kho ky gui) | 2 ngay | Server logic, date range filter |
| Auto-create Sales Invoice | 2 ngay | Whitelisted method, Inter Company link |
| Consignment Dashboard (hang ton ky gui, aging) | 2 ngay | Custom page hoac Report Builder |
| Consignment Reports (2-3 reports) | 3 ngay | Tong hop ky gui, doi chieu, aging |
| Workflow (approval cho reconciliation) | 1 ngay | Frappe Workflow |
| Accounting integration (GL Entry verification) | 2 ngay | Verify bUT toan No/Co dung |
| Testing & QA | 3 ngay | End-to-end test 2 company |
| **Tong** | **~21 ngay (4-5 tuan)** | |

#### Risks

| Risk | Impact | Xac suat | Mitigation |
|------|--------|----------|------------|
| Inter Company Transaction phuc tap | **Cao** | Cao | Test ky voi 2 company setup som |
| Cross-company stock tracking | **Cao** | Trung binh | Dung warehouse_type "Consignment" de phan biet |
| Accounting entries sai (cross-company) | **Cao** | Trung binh | Verify GL Entry sau moi buoc |
| Scope creep (khach muon them tinh nang) | **Cao** | Cao | Define scope ro rang trong SRS, sign-off truoc khi code |
| Performance voi du lieu lon (nhieu item ky gui) | Medium | Thap | Index, pagination, background job |

---

## 4. Tong effort estimate

### 4.1. Summary by category

| Category | Features | Effort | Developer | Phase |
|----------|----------|--------|-----------|-------|
| Configuration only | 10 | 3-5 ngay | DevOps/Setup | T3-T4 |
| Minor customization (fields, properties) | 8 | 5-7 ngay | 1 dev | T4 |
| Custom scripts (client/server) | 5 | 8-10 ngay | 1 dev | T4 |
| Barcode/Label module | 3 | 17 ngay | 1 dev | T4 |
| Warehouse Location module | 2 | 8 ngay | 1 dev | T4-T5 |
| Stock Reconciliation custom | 2 | 6 ngay | 1 dev | T4 |
| Monthly Average (neu chon Option B) | 1 | 10-11 ngay | 1 dev | T5 |
| Serial Status custom | 1 | 4 ngay | 1 dev | T4 |
| Dashboard widgets | 5 | 7 ngay | 1 dev | T4-T5 |
| CCDC tracking | 1 | 3 ngay | 1 dev | T5 |
| Custom reports | 4 | 13-19 ngay | 1 dev | T4-T5 |
| Consignment workflow | N/A | 21 ngay | 1 dev | T4-T5 |
| Web Sync | 2 | 8-12 ngay | 1 dev | T5-T6 |
| Testing & QA tong | ALL | 10-15 ngay | 1 dev + QA | T4-T5 |
| **TONG (khong tinh Monthly Avg Option B)** | **30** | **~113-134 ngay** | | |
| **TONG (co Monthly Avg Option B)** | **30** | **~123-145 ngay** | | |

**Quy doi:** ~113-134 ngay = **~23-27 tuan** cho 1 developer, hoac **~12-14 tuan** cho 2 developers lam song song.

### 4.2. Timeline de xuat

**Gia dinh:** 1 developer chinh (Cuong hoac Dat), co ho tro tu developer khac khi can.

| Tuan | Noi dung | Output | Developer |
|------|----------|--------|-----------|
| **T4 - Tuan 1-2** | Core setup + Configuration | 10 features config xong. Warehouse hierarchy, Stock Settings, permissions, Item reorder level. | 1 dev |
| **T4 - Tuan 3-4** | Minor customization + Custom scripts | 13 features (8 customize + 5 script). Custom fields, workflows, batch alerts, serial status. | 1 dev |
| **T4 - Tuan 5-6** | Stock Reconciliation custom + Dashboard | ERP-WH-016, 017 xong. Dashboard widgets deploy. | 1 dev |
| **T4 - Tuan 7-8** | Barcode/Label module | ERP-WH-013, 014, 015 xong. Barcode Label DocType, print format, batch printing. | 1 dev |
| **T5 - Tuan 1-2** | Warehouse Location + Custom Reports (1) | ERP-WH-011, 024 xong. BC nhap xuat ton (ERP-WH-021). | 1 dev |
| **T5 - Tuan 3-4** | Consignment workflow (1) | Warehouse setup, Inter Company config, Consignment Reconciliation DocType. | 1 dev |
| **T5 - Tuan 5-6** | Consignment workflow (2) + Reports | Auto SI, dashboard, consignment reports. BC serial, BC gia XBQ. | 1 dev |
| **T5 - Tuan 7-8** | CCDC + Monthly Average (neu co) + Web Sync | ERP-WH-006 CCDC, Web Sync API endpoints. | 1 dev |
| **T6 - Tuan 1-2** | Testing & QA + Bug fix | Tat ca 30 features tested end-to-end. UAT voi khach. | 1 dev + QA |

### 4.3. Dependencies & risks tong

| Risk | Impact | Xac suat | Mitigation |
|------|--------|----------|------------|
| **Scope creep** tu consignment | Cao | Cao | Define scope ro rang, sign-off truoc khi code |
| **Phuong phap gia von** khong duoc quyet dinh | Cao | Cao | Trinh bay 2 option cho khach truoc khi bat dau, deadline quyet dinh: truoc T5 |
| **Barcode hardware** khong tuong thich | Medium | Trung binh | Yeu cau khach cung cap model may scan som (truoc T4 tuan 7) |
| **Cross-company transactions** phuc tap | Cao | Trung binh | Test 2-company setup som (T4 tuan 1-2), verify accounting entries |
| **Monthly Average repost** gay data corruption | Cao | Thap (neu chon Option A) | Khuyen nghi khach dung Moving Average (Option A) |
| **Web Sync** conflict | Medium | Trung binh | Rate limiting, idempotent API design |
| **Performance** voi du lieu lon | Medium | Thap | Index, pagination, background job, test voi 100K records |
| **ERPNext v16 bugs** | Medium | Trung binh | Follow ERPNext GitHub issues, co fallback plan |

### 4.4. Phu thuoc giua cac features

```
ERP-WH-011 (Location) ──────────────────> ERP-WH-024 (BC theo vi tri)

ERP-WH-013 (Barcode) ───> ERP-WH-014 (Tem) ───> ERP-WH-015 (In hang loat)

ERP-WH-016 (Kiem ke) ───> ERP-WH-017 (Chenh lech)

Consignment setup ───> ERP-WH-010 (Serial custom) ───> ERP-WH-023 (BC serial)
      |
      └──> ERP-WEB-003/005 (Web Sync)

ERP-WH-001 (Ton dau ky) ───> ERP-WH-018 (BC ton kho)
                              ERP-WH-019 (BC gia tri ton)
                              ERP-WH-021 (BC NXT)
```

---

## 5. Recommendation

### 5.1. Approach strategy

**Giai doan 1 (Tuan 1-4): Setup & Configure ERPNext native**
1. Setup Warehouse hierarchy cho 2 company
2. Enable Stock Reservation, Perpetual Inventory
3. Config Stock Settings (valuation method, negative stock, reorder)
4. Setup roles & permissions
5. Test cac flow chinh: nhap mua, xuat ban, dieu chuyen, kiem ke

**Giai doan 2 (Tuan 5-8): Minor customization**
1. Custom fields (Serial status, CCDC fields, Location link)
2. Workflow (Stock Reconciliation approval)
3. Server scripts (batch alerts, freeze warehouse)
4. Dashboard widgets

**Giai doan 3 (Tuan 9-14): Major custom development**
1. Barcode/Label module (3 tuan)
2. Warehouse Location module (1.5 tuan)
3. Custom reports (2-3 tuan, song song)

**Giai doan 4 (Tuan 15-20): Consignment + Integration**
1. Consignment workflow (4-5 tuan)
2. Web Sync API (1-2 tuan, song song)
3. CCDC tracking (0.5 tuan)

**Giai doan 5 (Tuan 21-22): Testing & QA**
1. End-to-end testing tat ca 30 features
2. UAT voi khach hang
3. Bug fix va fine-tuning

### 5.2. Quick wins (deploy truoc, thay gia tri ngay)

| # | Feature | Effort | Gia tri | Khi nao |
|---|---------|--------|---------|---------|
| 1 | Warehouse setup | 0.5 ngay | Cao | Tuan 1 |
| 2 | Stock Entry (Receipt, Issue, Transfer) | 0 (native) | Cao | Tuan 1 |
| 3 | Purchase Receipt + Delivery Note | 0 (native) | Cao | Tuan 1 |
| 4 | Stock Reservation | 1 ngay (enable) | Cao | Tuan 1 |
| 5 | Stock Balance + Stock Ledger reports | 0 (native) | Cao | Tuan 1 |
| 6 | Ton kho dau ky (Stock Reconciliation) | 0.5 ngay | Cao | Tuan 1-2 |
| 7 | Batch management | 0 (native) | Trung binh | Tuan 2 |
| 8 | Serial No management | 0 (native) | Trung binh | Tuan 2 |

**Ket luan:** 8 features (27%) co the deploy trong 1-2 tuan dau tien voi effort gan nhu 0.

### 5.3. Defer / descope candidates

Cac features co the hoan lai hoac bo neu can giam scope:

| # | Feature | Ly do co the hoan | Impact neu hoan |
|---|---------|-------------------|-----------------|
| 1 | ERP-WH-011: Warehouse Location | Dung warehouse hierarchy thay the (kho con) | Thap - co workaround |
| 2 | ERP-WH-024: BC theo vi tri | Phu thuoc Location, co the dung Stock Balance filter by warehouse | Thap |
| 3 | Monthly Average Costing (Option B) | Dung Moving Average thay the (TT200 chap nhan) | Thap - khac biet < 2% |
| 4 | ERP-WH-015: In tem hang loat | Co the in tung tem truoc, batch printing la nice-to-have | Thap |
| 5 | Dashboard widgets (3-5) | Nice-to-have, dung Stock Balance report thay the | Thap |
| 6 | ERP-WEB-003: Dong bo kho | Hoan den khi co website (co the T6-T7) | Trung binh |

**Neu descope 6 features nay:** Giam ~25 ngay (~5 tuan), tong effort con ~88-109 ngay (~18-22 tuan cho 1 dev).

### 5.4. Cac quyet dinh can khach hang xac nhan truoc khi bat dau

| # | Quyet dinh | Deadline | Anh huong |
|---|-----------|----------|-----------|
| 1 | Phuong phap gia von: Moving Average hay Trung binh thang? | Truoc T4 tuan 1 | +-2 tuan effort |
| 2 | Barcode format: EAN-13 / Code128 / QR? | Truoc T4 tuan 5 | Khong lon |
| 3 | Kich thuoc tem nhan (mm)? | Truoc T4 tuan 5 | Khong lon |
| 4 | Model may scan barcode? | Truoc T4 tuan 7 | Test hardware |
| 5 | Cau truc vi tri kho (bao nhieu khu, ke, o)? | Truoc T5 tuan 1 | Design DocType |
| 6 | Website platform (ERPNext / WooCommerce / khac)? | Truoc T5 tuan 7 | Web Sync approach |
| 7 | Cac kho cu the cua TM va NM? Ten? Allow negative? | Truoc T4 tuan 1 | Setup |
| 8 | CCDC: dung Asset DocType hay custom? | Truoc T5 tuan 7 | +-1 tuan effort |

---

## 6. Ma tran feature vs ERPNext DocType

| ERPNext DocType | Features su dung | Coverage |
|----------------|-----------------|----------|
| **Warehouse** | WH-001, WH-002, WH-003 | 3 features |
| **Stock Entry** | ERP-WH-004, 006, 007 | 3 features |
| **Purchase Receipt** | ERP-WH-002, 003, 008 | 3 features |
| **Delivery Note** | ERP-WH-005 | 1 feature |
| **Stock Reconciliation** | ERP-WH-001, 016, 017 | 3 features |
| **Batch** | ERP-WH-009, 022 | 2 features |
| **Serial No** | ERP-WH-010, 023 | 2 features |
| **Bin** | ERP-WH-012, 018, 020 | 3 features (data source) |
| **Stock Ledger Entry** | ERP-WH-019, 021, 025 | 3 features (data source) |
| **Landed Cost Voucher** | ERP-WH-003 | 1 feature |
| **Stock Reservation Entry** | ERP-WH-012 | 1 feature |
| **Item** | ERP-WH-013 (barcode field) | 1 feature (partial) |
| **Custom: Barcode Label** | ERP-WH-013, 014, 015 | 3 features |
| **Custom: Warehouse Location** | ERP-WH-011, 024 | 2 features |
| **Custom: Consignment Reconciliation** | Consignment workflow | Related |

---

## Tham khao

### Tai lieu noi bo
- `docs/modules/07-kho-hang/README.md` -- Feature matrix (30 features)
- `docs/modules/07-kho-hang/analysis/WAREHOUSE_WORKFLOW.md` -- Workflow & phan tich nghiep vu
- `docs/modules/07-kho-hang/analysis/WAREHOUSE_STATUS.md` -- Status workflow & state machine
- `docs/modules/07-kho-hang/technical-spec/WAREHOUSE_SPEC.md` -- Spec Summary 12 buoc
- `docs/feature/ERP_SPECIFICATION.md` -- Dac ta chuc nang Section 4
- `docs/erpnext-flows/MODULE_GAP_ANALYSIS.md` -- Module Gap Analysis tong the
- `docs/accounting/COA_ANALYSIS.md` -- Chart of Accounts (TK 1561, 632, 331...)

### ERPNext Documentation
- [Stock Module](https://docs.erpnext.com/docs/user/manual/en/stock)
- [Stock Entry](https://docs.erpnext.com/docs/user/manual/en/stock/stock-entry)
- [Stock Reconciliation](https://docs.erpnext.com/docs/user/manual/en/stock/stock-reconciliation)
- [Batch](https://docs.erpnext.com/docs/user/manual/en/stock/batch)
- [Serial No](https://docs.erpnext.com/docs/user/manual/en/stock/serial-no)
- [Landed Cost Voucher](https://docs.erpnext.com/docs/user/manual/en/stock/landed-cost-voucher)
- [Stock Reservation](https://docs.erpnext.com/docs/user/manual/en/stock/stock-reservation)
- [Inter Company Transactions](https://docs.erpnext.com/docs/user/manual/en/accounts/inter-company-journal-entry)

### Cong cu / Library
- [python-barcode](https://pypi.org/project/python-barcode/) -- Barcode generation library
- [Jinja2](https://jinja.palletsprojects.com/) -- Label template engine (built-in Frappe)
- [WeasyPrint / wkhtmltopdf](https://docs.erpnext.com/docs/user/manual/en/setting-up/print/print-format) -- PDF generation (built-in Frappe)

---

**Lich su thay doi:**
- 16/02/2026: v1.0 - Tao file, 30 features analysis, effort estimate, timeline
  - Nguon: ERP_SPECIFICATION.md Section 4, README.md Feature Matrix
  - Phan tich chi tiet: Barcode (3.1), Location (3.2), Reconciliation (3.3), Monthly Average (3.4), Serial Status (3.5), Dashboard (3.6), CCDC (3.7), Reports (3.8), Consignment (3.9)

---

**Last Updated:** 16/02/2026
