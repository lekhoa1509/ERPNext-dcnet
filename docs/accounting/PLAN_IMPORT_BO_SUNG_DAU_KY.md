# Plan import bo sung du lieu dau ky

**Ngay lap:** 25/06/2026  
**Pham vi:** Chi cac du lieu dau ky con thieu/chua tron ven sau khi da co danh muc co ban.  
**Nguon file:** `data import/02_So_Du_Dau_Ky/`  
**Site doi soat:** `flow.local` trong container `devcontainer-frappe-1`

## 1. Tom tat hien trang

| Nhom dau ky | File nguon | Hien trang trong ERP | Ket luan |
|---|---:|---|---|
| Ton kho VTHH | 1.145 dong, gop thanh 646 cap hang+kho | Co `Stock Reconciliation` va 646 `Stock Ledger Entry` | Gan nhu xong; lech 88 dong do lam tron |
| So du tai khoan tong hop | 49 dong | Da co opening `Journal Entry` | Can doi soat lai voi GL mo coi truoc khi chot |
| Cong no khach hang | 102 dong | Opening GL moi co 73 party lines tren TK 131 | Thieu chi tiet/party mapping |
| Cong no nha cung cap | 299 dong | Opening GL moi co 106 party lines tren TK 331 | Thieu chi tiet/party mapping |
| Cong no nhan vien | 2 dong | Opening GL moi co 1 Employee party line tren TK 141 | Thieu chi tiet/party mapping |
| TSCĐ dau ky | 28 dong | Co GL nguyen gia, nhung `Asset = 0` | Thieu ho so tai san va lich khau hao |
| CCDC dau ky | 179 dong | Chua thay du lieu chi tiet tuong ung | Thieu ho so CCDC/lich phan bo |
| Chi phi tra truoc | 207 dong | Co GL TK 242 | Thieu lich phan bo chi tiet |
| Doanh thu nhan truoc | 839 dong | Co GL TK 3387 | Thieu lich phan bo chi tiet |
| So du tai khoan ngan hang | 6 dong | Co GL tien/bank; `Payment Entry = 0` | Du ve so cai, thieu chung tu tien/bank neu can van hanh chi tiet |

## 2. Van de can xu ly truoc khi import tiep

### 2.1. GL opening mo coi

DB dang co `GL Entry` opening cho 2 voucher khong con ton tai trong `Journal Entry`:

| Voucher | Noi dung nghi van | Gia tri |
|---|---|---:|
| `ACC-JV-2026-00003` | TSCĐ / Temporary Opening | 8.834.740.468 |
| `ACC-JV-2026-00005` | TSCĐ / Temporary Opening | 8.834.740.468 |

**Action:**
- Truy vet log/import run tao ra 2 voucher nay.
- Neu la lan import thu nghiem bi xoa JE nhung con GL, can huy/don sach GL mo coi bang cach dung API/patch co kiem soat, khong xoa tay truc tiep khi chua backup.
- Sau khi don, chay lai doi soat Trial Balance ngay `2026-01-01`.

**Dieu kien pass:**
- Khong con `GL Entry` co `voucher_type = "Journal Entry"` nhung voucher khong ton tai trong `tabJournal Entry`.
- Tong debit = tong credit cho tat ca opening entries.

### 2.2. Xac nhan ngay dau ky

Dang thay opening date la `2026-01-01`. Can xac nhan day la ngay chuyen doi so lieu chinh thuc.

**Can clarify voi khach hang:**
- Ngay chot so lieu dau ky la `01/01/2026` hay ngay go-live khac?
- Cac phat sinh tu `01/01/2026` den go-live co import bang hoa don/chung tu rieng khong?

## 3. Ke hoach import bo sung theo thu tu

### Phase 0. Backup va dong bang so lieu

**Muc tieu:** Dam bao co the rollback neu import sai.

**Viec lam:**
- Backup DB truoc khi sua opening GL.
- Export snapshot cac bang lien quan:
  - `GL Entry`
  - `Journal Entry`
  - `Stock Ledger Entry`
  - `Stock Reconciliation`
  - `Asset`
  - cac DocType/custom DocType lien quan CCDC/CPTT/DTNT neu co
- Dong bang file nguon trong `data import/02_So_Du_Dau_Ky/`; khong sua truc tiep file goc.

**Dieu kien pass:**
- Co file backup DB.
- Co log checksum/timestamp cho tung file Excel nguon.

### Phase 1. Doi soat va sua opening GL hien co

**Muc tieu:** Lam sach nen ke toan truoc khi nap chi tiet.

**Viec lam:**
- Xu ly GL mo coi `ACC-JV-2026-00003`, `ACC-JV-2026-00005`.
- Doi soat `ACC-JV-2026-00009` voi file:
  - `Danh_sach_so_du_tai_khoan.xlsx`
  - `Danh_sach_cong_no_khach_hang.xlsx`
  - `Danh_sach_cong_no_nha_cung_cap.xlsx`
  - `Danh_sach_cong_no_nhan_vien.xlsx`
  - `Danh_sach_nhap_so_du_tai_khoan_ngan_hang.xlsx`
- Tach ro dong nao da co party, dong nao dang nam tong hop khong party.

**Dieu kien pass:**
- Report doi soat theo account/party/source row.
- Khong import them khi tong so du hien tai chua ro nguon.

### Phase 2. Bo sung cong no dau ky theo party

**Nguon:**
- `Danh_sach_cong_no_khach_hang.xlsx`
- `Danh_sach_cong_no_nha_cung_cap.xlsx`
- `Danh_sach_cong_no_nhan_vien.xlsx`

**Hien trang can luu y:**
- File KH co 102 dong, DB opening GL moi co 73 Customer party lines.
- File NCC co 299 dong, DB opening GL moi co 106 Supplier party lines.
- File NV co 2 dong, DB opening GL moi co 1 Employee party line.

**Phuong an import khuyen nghi:**
- Khong tao them tong so du TK 131/331/141 neu tong GL da co.
- Chuyen cac dong tong hop khong party sang GL co party bang Journal Entry adjustment, hoac rebuild opening JE sau khi da backup va xac nhan.
- Moi dong can co:
  - account (`131`, `331`, `141` hoac tai khoan nguon)
  - party_type
  - party
  - debit/credit
  - source_file
  - source_row
  - misa_code

**Dieu kien pass:**
- Tong TK 131 theo party = tong file cong no KH.
- Tong TK 331 theo party = tong file cong no NCC.
- Tong TK 141 theo party = tong file cong no NV.
- Bao cao Accounts Receivable/Payable hien du party va tong khop Trial Balance.

**Rui ro/can clarify:**
- Dong `Tổng` trong cong no nhan vien khong phai nhan vien that; can tach no thanh doi tuong nao.
- Neu party chua co trong master, phai import master truoc, nhung khong tinh la pham vi dau ky.

### Phase 3. Import chi tiet TSCĐ dau ky

**Nguon:** `Danh_sach_tai_san_co_dinh_dau_ky.xlsx`

**So lieu nguon:**
- 28 tai san.
- Nguyen gia: 8.834.740.468.
- Hao mon luy ke: 5.987.415.766.

**Hien trang ERP:**
- `Asset = 0`.
- `Asset Category = 0`.
- Da co GL nguyen gia trong opening JE, nhung chua co ho so Asset.

**Phuong an import khuyen nghi:**
- Tao `Asset Category` theo loai TSCĐ.
- Tao `Asset` voi `is_existing_asset = 1`.
- Map cac field:
  - Ma tai san -> asset code/name hoac custom field `misa_asset_code`
  - Ten tai san -> asset_name
  - Loai tai san -> asset_category
  - Don vi su dung -> location/department/cost center tuy mapping
  - Nguyen gia -> gross purchase amount/total asset cost
  - Hao mon luy ke -> opening accumulated depreciation
  - Ngay ghi tang -> purchase_date/available_for_use_date
  - Ngay tinh KH -> next depreciation basis
  - Thoi gian SD, thoi gian con lai -> depreciation schedule
  - TK nguyen gia, TK khau hao -> finance book/category accounts

**Dieu kien pass:**
- Co 28 Asset.
- Tong nguyen gia Asset = 8.834.740.468.
- Tong hao mon luy ke = 5.987.415.766.
- Lich khau hao tu ky tiep theo khong tao trung GL opening.

**Rui ro/can clarify:**
- ERPNext Asset import co the tu dong tao GL neu khong cau hinh dung. Can dam bao khong ghi trung nguyen gia/hao mon da co trong opening GL.

### Phase 4. Import CCDC dau ky

**Nguon:** `Danh_sach_cong_cu_dung_cu_dau_ky.xlsx`

**So lieu nguon:**
- 179 dong.
- So luong: 770.
- Gia tri CCDC: 3.146.244.052.
- Gia tri con lai: 140.868.814.

**Hien trang ERP:**
- Chua thay du lieu chi tiet CCDC tuong ung.

**Phuong an can chon:**
- Option A: Dung `Asset` cho CCDC gia tri thap, them flag/custom field `is_low_value_asset`.
- Option B: Tao custom DocType `Prepaid/Allocated Tool` de quan ly CCDC va lich phan bo.
- Option C: Chi giu GL neu khach khong can quan ly CCDC chi tiet trong ERP.

**Khuyen nghi:** Option B neu can theo doi phan bo CCDC hang ky; Option A neu muon tan dung Asset module.

**Dieu kien pass:**
- Moi CCDC co ma, ten, ngay ghi tang, so luong, nguyen gia/gia tri con lai, so ky phan bo, so ky con lai, TK cho phan bo.
- Tong gia tri con lai khop file.
- Chay thu ky phan bo tiep theo va doi soat GL.

**Can clarify voi khach hang:**
- Co can quan ly CCDC theo tung ma hay chi can so du TK?
- CCDC da ngung phan bo co can import de tra cuu lich su khong?

### Phase 5. Import chi tiet chi phi tra truoc

**Nguon:** `Danh_sach_chi_phi_tra_truoc_dau_ky.xlsx`

**So lieu nguon:**
- 207 dong.
- So tien: 5.092.218.792.
- So tien con lai: 2.684.734.980.

**Hien trang ERP:**
- Da co opening GL vao TK 242.
- Chua co lich phan bo chi tiet theo tung khoan.

**Phuong an import khuyen nghi:**
- Tao custom DocType hoac dung co che deferred expense neu ERPNext dap ung du.
- Moi dong can co:
  - Ma CP tra truoc
  - Ten CP tra truoc
  - Ngay bat dau phan bo
  - So tien ban dau
  - So tien con lai
  - So ky phan bo
  - So ky con lai
  - So tien phan bo hang ky
  - Tai khoan cho phan bo

**Dieu kien pass:**
- Tong so tien con lai theo chi tiet = so du TK 242 can theo doi.
- Lich phan bo ky tiep theo sinh but toan dung TK chi phi va TK 242.
- Khong tao lai GL opening da co.

### Phase 6. Import chi tiet doanh thu nhan truoc

**Nguon:** `Danh_sach_doanh_thu_nhan_truoc_dau_ky.xlsx`

**So lieu nguon:**
- 839 dong.
- Doanh thu chua phan bo: 11.693.520.400.

**Hien trang ERP:**
- Da co opening GL vao TK 3387.
- Chua co lich phan bo chi tiet theo hang/doi tuong/don hang.

**Phuong an import khuyen nghi:**
- Dung deferred revenue neu item/sales invoice mapping du tot; neu khong, tao custom DocType quan ly lich phan bo DTNT.
- Moi dong can giu source identity:
  - So chung tu
  - Ngay hach toan
  - Ma hang / ten hang
  - TK doanh thu chua thuc hien
  - TK doanh thu phan bo
  - Ngay bat dau/ket thuc phan bo
  - So ky, so ky da phan bo, so ky con lai
  - Doanh thu phan bo/ky
  - Doanh thu da phan bo luy ke
  - Doanh thu chua phan bo
  - Doi tuong, don vi, don dat hang

**Dieu kien pass:**
- Tong doanh thu chua phan bo chi tiet = so du TK 3387 lien quan.
- Lich phan bo ky tiep theo sinh GL dung TK doanh thu va TK 3387.
- Co the truy vet tu dong chi tiet ve source row.

### Phase 7. So du ngan hang/tien mat chi tiet

**Nguon:** `Danh_sach_nhap_so_du_tai_khoan_ngan_hang.xlsx`

**So lieu nguon:**
- 6 dong.
- Du No: 2.530.522.948.

**Hien trang ERP:**
- Da co GL tien/bank.
- `Payment Entry = 0`.

**Phuong an:**
- Neu chi can Trial Balance: giu JE opening.
- Neu can doi soat ngan hang theo Bank Account: tao opening reference theo Bank Account, dam bao khong ghi trung GL.

**Dieu kien pass:**
- Bank Account Balance report khop GL.
- Khong phat sinh duplicate debit tren TK 112.

## 4. Thu tu uu tien de lam

1. Backup DB va xu ly GL mo coi.
2. Doi soat lai opening JE tong hop `ACC-JV-2026-00009`.
3. Hoan thien cong no KH/NCC/NV theo party vi anh huong AR/AP reports.
4. Import chi tiet TSCĐ va lich khau hao.
5. Chon phuong an CCDC va import chi tiet.
6. Import chi tiet CPTT va DTNT de chay phan bo ky sau.
7. Doi soat bank/cash detail neu khach can van hanh ngan hang trong ERP.
8. Chay final reconciliation report.

## 5. Checklist doi soat cuoi

- [ ] Khong con GL opening mo coi.
- [ ] Tong debit opening = tong credit opening.
- [ ] Trial Balance tai `2026-01-01` khop file nguon sau khi loai tru cac dong da import bang module rieng.
- [ ] AR theo Customer khop file cong no KH.
- [ ] AP theo Supplier khop file cong no NCC.
- [ ] Employee advance/payable khop file cong no NV.
- [ ] Stock Balance khop 646 cap hang+kho va tong gia tri lech trong nguong lam tron.
- [ ] Asset Register co 28 TSCĐ va khop nguyen gia/hao mon luy ke.
- [ ] Lich phan bo CCDC/CPTT/DTNT chay duoc ky tiep theo.
- [ ] Moi dong import co source trace: file, sheet, row, ma MISA/chung tu.

## 6. Cau hoi can clarify

1. Ngay chot dau ky chinh thuc la `01/01/2026` hay ngay go-live?
2. Cong no nhan vien co dong `Tổng`: day la dong tong cong hay doi tuong that?
3. Khach co can quan ly chi tiet CCDC trong ERP hay chi can so du tai khoan?
4. CPTT va DTNT co can ERP tu dong sinh but toan phan bo hang thang khong?
5. TSCĐ da co hao mon luy ke: khi import Asset, co chap nhan chi tao Asset record khong tao lai GL opening?
6. Bank opening co can doi soat theo Bank Account report hay chi can Trial Balance?

## 7. Lenh kiem tra nhanh

```bash
docker exec devcontainer-frappe-1 bash -lc 'cd /workspace/development/frappe-bench && bench --site flow.local mariadb -e "select gle.voucher_no, count(*) from \`tabGL Entry\` gle left join \`tabJournal Entry\` je on je.name=gle.voucher_no where gle.voucher_type=\"Journal Entry\" and gle.is_opening=\"Yes\" and je.name is null group by gle.voucher_no;"'
```

```bash
docker exec devcontainer-frappe-1 bash -lc 'cd /workspace/development/frappe-bench && bench --site flow.local mariadb -e "select voucher_no, party_type, count(distinct party) parties, count(*) line_count, round(sum(debit),0) debit, round(sum(credit),0) credit from \`tabGL Entry\` where is_opening=\"Yes\" and ifnull(party_type,\"\")<>\"\" group by voucher_no, party_type;"'
```

```bash
docker exec devcontainer-frappe-1 bash -lc 'cd /workspace/development/frappe-bench && bench --site flow.local mariadb -e "select \"Asset\" dt, count(*) cnt from tabAsset union all select \"Stock Ledger Entry\", count(*) from \`tabStock Ledger Entry\` union all select \"Payment Entry\", count(*) from \`tabPayment Entry\`;"'
```
