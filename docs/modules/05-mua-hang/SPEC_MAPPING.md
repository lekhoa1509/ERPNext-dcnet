# 05 - Mua hàng: Spec -> ERPNext Mapping

> **Nguồn:** ERP_SPECIFICATION.md Section 3.1 + 3.2 + IMPORT_PROCESS_SPECIFICATION.md
> **ERPNext:** v16 — Buying Module (Purchase Order, Purchase Receipt, Purchase Invoice)
> **Cập nhật:** 17/02/2026

## Quy ước Tags

| Tag | Nghĩa | Action |
|-----|--------|--------|
| `USE` | ERPNext có sẵn, dùng ngay | Config + test |
| `CFG` | ERPNext có, cần config/setup | Setup data, settings, permissions |
| `EXT` | ERPNext có, cần mở rộng | Custom field, client/server script |
| `NEW` | ERPNext không có, cần build | Custom DocType, module mới |
| `REF` | Thuộc module khác | Tham chiếu |

---

## 3.1. Features Mua hàng (18 features)

> Nguồn: ERP_SPECIFICATION.md Section 3.1 — bảng 18 features từ PHASE_2_FEATURES.xlsx

### 3.1.1. Ưu đãi NCC

- **Tag:** `CFG`
- **Spec yêu cầu:** Chiết khấu % + Chiết khấu tiền + Quà tặng
- **ERPNext:** Pricing Rule
- **ERPNext đã có:** Pricing Rule hỗ trợ discount % và discount amount theo Supplier, Item, quantity, date range. Supplier Quotation để so sánh giá.
- **Gap:** "Quà tặng" — ERPNext Pricing Rule có "Free Item" rule (mua X tặng Y). Cần verify có đủ cho yêu cầu không.
- **Action:** Config Pricing Rule cho CK%, CK tiền, Free Item. Test với PO.
- **Effort:** 1 ngày
- **Dependency:** 04 - NCC (Supplier + Price List)

### 3.1.2. Import hình ảnh SP

- **Tag:** `EXT`
- **Spec yêu cầu:** Import ảnh theo model + Quy tắc đặt tên ảnh
- **ERPNext:** File Attach trên Item (single image, manual)
- **ERPNext đã có:** Item có field `image` (1 ảnh) và Attach cho nhiều file. Nhưng chỉ import từng cái.
- **Gap:** Spec yêu cầu bulk import — chọn thư mục, hệ thống tự động match tên file với mã hàng hóa để cập nhật ảnh. ERPNext không có tính năng này.
- **Action:** Custom script/tool: đọc thư mục → match filename vs Item code → attach image. Có thể là bench command hoặc custom page.
- **Effort:** 3 ngày
- **Dependency:** 03 - Sản phẩm (Item master)
- **Clarify:** Xem CLARIFY.md #1.1 — Quy tắc đặt tên file ảnh

### 3.1.3. Tạo PO (Purchase Order)

- **Tag:** `EXT`
- **Spec yêu cầu:** PO Number (auto) + NCC + Kho nhận + Ngày đặt
- **ERPNext:** Purchase Order DocType
- **ERPNext đã có:** PO với Naming Series (auto), Supplier link, Set Warehouse, Posting Date. Items child table với Item, Qty, Rate.
- **Gap:** Spec yêu cầu thêm: Ship mode (Sea/Air/Express), Confirm ship date, PO Number theo hãng (không phải auto của ERPNext). SRS thêm: Điều khoản thanh toán, điều khoản giao hàng.
- **Action:** Custom fields trên PO: `custom_ship_mode` (Select), `custom_confirm_ship_date` (Date), `custom_vendor_po_number` (Data). Config Naming Series.
- **Effort:** 1 ngày
- **Dependency:** 04 - NCC

### 3.1.4. Chi tiết PO

- **Tag:** `USE`
- **Spec yêu cầu:** Model + SKU + Số lượng + Giá mua
- **ERPNext:** Purchase Order Item (child table)
- **ERPNext đã có:** Item Code, Item Name, Qty, Rate, Amount. UOM, Warehouse per item.
- **Gap:** Không có gap. Item code = SKU, Item Name có thể chứa Model.
- **Action:** Đảm bảo Item master (module 03) có trường Model/SKU mapping đúng.
- **Effort:** 0.5 ngày
- **Dependency:** 03 - Sản phẩm

### 3.1.5. Theo dõi PO theo số PO

- **Tag:** `EXT`
- **Spec yêu cầu:** Trạng thái: Nháp → Đã gửi NCC → Đang giao → Hoàn thành
- **ERPNext:** PO Status tracking (Draft → Submitted → To Receive → Completed)
- **ERPNext đã có:** PO có status tự động: Draft, To Receive and Bill, To Receive, To Bill, Completed, Cancelled, On Hold, Closed.
- **Gap:** Spec yêu cầu trạng thái "Đã gửi NCC" và "Đang giao" — ERPNext không có. ERPNext chỉ có Draft → Submitted (= To Receive). Cần thêm trạng thái trung gian.
- **Action:** Workflow trên Purchase Order thêm states: "Đã gửi NCC", "Đang giao". Hoặc dùng custom field `custom_supplier_status` (Select).
- **Effort:** 2 ngày
- **Clarify:** Xem CLARIFY.md #2.1 — Workflow PO hay custom field?

### 3.1.6. Cập nhật lệnh nhập hàng

- **Tag:** `USE`
- **Spec yêu cầu:** Sinh lệnh nhập từ PO + Nhập một phần / nhiều lần
- **ERPNext:** Purchase Receipt from PO
- **ERPNext đã có:** Tạo Purchase Receipt từ PO (Get Items From → Purchase Order). Hỗ trợ partial receipt (nhập 1 phần, nhiều lần).
- **Gap:** Không có gap lớn. ERPNext hỗ trợ đầy đủ.
- **Action:** Config và test luồng PO → Purchase Receipt (partial). Xem thêm 3.2.4 (Đề nghị nhập hàng) nếu cần bước trung gian.
- **Effort:** 0.5 ngày

### 3.1.7. Theo dõi thực hiện mua hàng

- **Tag:** `USE`
- **Spec yêu cầu:** Đã đặt + Đã nhận một phần (%) + Đã nhận đủ
- **ERPNext:** PO % Received / Status indicators
- **ERPNext đã có:** PO Dashboard hiển thị % Received, % Billed. Status tự động chuyển khi nhận hàng (To Receive → Completed).
- **Gap:** Không có gap.
- **Action:** Test và verify PO dashboard hiển thị đúng.
- **Effort:** 0.5 ngày

### 3.1.8. Nhập hàng theo lô

- **Tag:** `CFG`
- **Spec yêu cầu:** Mã lô + Ngày nhập + Gắn với PO
- **ERPNext:** Batch No trong Purchase Receipt
- **ERPNext đã có:** Item có `has_batch_no = 1` → Purchase Receipt yêu cầu nhập Batch No. Batch có manufacturing_date, expiry_date.
- **Gap:** Không có gap lớn. Cần đảm bảo Item master bật Batch.
- **Action:** Enable Batch tracking cho các Item cần thiết (module 03). Config Batch naming.
- **Effort:** 0.5 ngày
- **Dependency:** 03 - Sản phẩm (Item has_batch_no)

### 3.1.9. Nhập hàng theo serial

- **Tag:** `CFG`
- **Spec yêu cầu:** Serial duy nhất + Scan serial khi nhập
- **ERPNext:** Serial No trong Purchase Receipt
- **ERPNext đã có:** Item có `has_serial_no = 1` → Purchase Receipt yêu cầu nhập Serial No (1 per unit). Serial No tự động tạo hoặc nhập manual.
- **Gap:** "Scan serial" — cần barcode scanner integration (xem 3.1.10).
- **Action:** Enable Serial No cho các Item cần thiết. Config serial naming pattern.
- **Effort:** 0.5 ngày
- **Dependency:** 03 - Sản phẩm (Item has_serial_no)

### 3.1.10. Nhập hàng theo mã vạch

- **Tag:** `EXT`
- **Spec yêu cầu:** Gán barcode cho SP/serial + Nhập kho bằng quét
- **ERPNext:** Item Barcode (child table) + Scan Barcode button
- **ERPNext đã có:** Item có child table `barcodes` (EAN, UPC, etc.). Purchase Receipt có nút "Scan Barcode" để add item bằng quét. Stock Settings có `enable_barcode_scanning`.
- **Gap:** Basic scan có sẵn. Nhưng scan serial khi nhập hàng (quét từng serial) cần verify — ERPNext standard chỉ scan để add item row, không phải scan serial no.
- **Action:** Enable barcode scanning. Test scan workflow. Nếu cần scan serial → Client Script extend.
- **Effort:** 2 ngày
- **Clarify:** Xem CLARIFY.md #1.2 — Barcode quét serial hay quét item?

### 3.1.11. Khai báo vòng đời SP

- **Tag:** `EXT`
- **Spec yêu cầu:** 6 tháng / 1 năm / 2 năm + Tính từ ngày nhập
- **ERPNext:** Item `shelf_life_in_days` + Batch `expiry_date`
- **ERPNext đã có:** Item có `shelf_life_in_days`. Khi tạo Batch trong Purchase Receipt, `expiry_date` tự động tính = ngày nhập + shelf_life. Batch-wise Expiry report có sẵn.
- **Gap:** Spec nói "vòng đời" — cần verify là shelf life (hết hạn) hay product lifecycle (ngừng kinh doanh). ERPNext có `end_of_life` trên Item (ngừng bán) và `shelf_life_in_days` trên Batch (hết hạn).
- **Action:** Config shelf_life_in_days cho các Item. Nếu là "vòng đời kinh doanh" → dùng `end_of_life` + custom alert.
- **Effort:** 1 ngày
- **Clarify:** Xem CLARIFY.md #1.3 — Vòng đời = shelf life hay product lifecycle?

### 3.1.12. Thông tin nguồn tiền

- **Tag:** `CFG`
- **Spec yêu cầu:** Quỹ tiền mặt / TK ngân hàng
- **ERPNext:** Mode of Payment + Payment Entry
- **ERPNext đã có:** Mode of Payment (Cash, Bank Transfer, etc.) liên kết với Account. Payment Entry chọn Mode of Payment.
- **Gap:** Không có gap.
- **Action:** Setup Mode of Payment: Tiền mặt (1111), Ngân hàng (1121). Link với Account trong COA.
- **Effort:** 0.5 ngày
- **Dependency:** COA setup (kế toán)

### 3.1.13. Phương thức thanh toán

- **Tag:** `CFG`
- **Spec yêu cầu:** Tiền mặt + Chuyển khoản + Công nợ
- **ERPNext:** Payment Terms Template
- **ERPNext đã có:** Payment Terms Template (VD: 100% khi giao, 50/50, Net 30). Payment Schedule trên PO/Invoice.
- **Gap:** Không có gap.
- **Action:** Tạo Payment Terms Template: COD, Net 30, Net 60, 50/50. Gán vào Supplier.
- **Effort:** 0.5 ngày
- **Dependency:** 04 - NCC (Payment Terms)

### 3.1.14. Theo dõi thanh toán PO

- **Tag:** `USE`
- **Spec yêu cầu:** Đã thanh toán + Thanh toán 1 phần + Còn nợ
- **ERPNext:** Payment Entry + PO Advance
- **ERPNext đã có:** Payment Entry link với PO. PO Dashboard hiển thị % Paid. Purchase Invoice tracking Paid/Unpaid/Overdue.
- **Gap:** Không có gap.
- **Action:** Test luồng Payment Entry → PO → Invoice. Verify dashboard hiển thị đúng.
- **Effort:** 0.5 ngày

### 3.1.15. Đính kèm chứng từ

- **Tag:** `USE`
- **Spec yêu cầu:** Hóa đơn NCC + Phiếu giao hàng + Hợp đồng
- **ERPNext:** File Attach (built-in trên mọi DocType)
- **ERPNext đã có:** Mọi DocType có sidebar Attach File (PDF, image, etc.). Unlimited attachments.
- **Gap:** Không có gap.
- **Action:** Hướng dẫn user attach chứng từ. Có thể add custom field `custom_attachment_type` (Select) nếu cần phân loại.
- **Effort:** 0.5 ngày

### 3.1.16. Trạng thái phiếu nhập

- **Tag:** `EXT`
- **Spec yêu cầu:** Nháp + Chờ duyệt + Đã nhập kho
- **ERPNext:** Purchase Receipt (Draft → Submitted)
- **ERPNext đã có:** Purchase Receipt chỉ có 2 state: Draft (nháp) và Submitted (đã nhập kho). Không có "Chờ duyệt" sẵn.
- **Gap:** Cần thêm bước "Chờ duyệt" trước khi Submit. ERPNext Workflow có thể thêm state.
- **Action:** Tạo Workflow cho Purchase Receipt: Draft → Chờ duyệt (role Kho) → Đã nhập kho (role KT). Hoặc dùng Authorization Rule để yêu cầu approve.
- **Effort:** 2 ngày
- **Clarify:** Xem CLARIFY.md #2.2 — Ai duyệt phiếu nhập? Theo giá trị hay tất cả?

### 3.1.17. Lịch sử mua hàng

- **Tag:** `USE`
- **Spec yêu cầu:** Theo NCC + Theo PO + Theo SP
- **ERPNext:** Reports + Supplier Dashboard
- **ERPNext đã có:** Supplier Dashboard (linked POs, PRs, PIs). Built-in reports: Purchase Order Analysis, Purchase Invoice Trends. Purchase Register.
- **Gap:** Không có gap lớn. Reports có sẵn, có thể cần tùy chỉnh view.
- **Action:** Verify built-in reports đủ yêu cầu. Nếu thiếu → Script Report.
- **Effort:** 0.5 ngày

### 3.1.18. Báo cáo mua hàng

- **Tag:** `EXT`
- **Spec yêu cầu:** Giá mua bình quân + NCC tốt nhất + Chi phí mua
- **ERPNext:** Built-in reports + Custom Script Report
- **ERPNext đã có:** Purchase Analytics, Item-wise Purchase History, Supplier-wise Sales Analytics.
- **Gap:** "Giá mua bình quân" — ERPNext có Valuation Rate nhưng không có report riêng. "NCC tốt nhất" — không có sẵn. "Chi phí mua tổng hợp" — Landed Cost chưa có report.
- **Action:** Tạo 2-3 Script Reports: BC Giá mua bình quân, BC NCC tốt nhất, BC Chi phí mua. Có thể thuộc module 06 (BC Phân tích).
- **Effort:** 3 ngày
- **Dependency:** Data từ PO, PI, LCV

---

## 3.2. Quy trình Mua hàng chi tiết (10 bước)

> Nguồn: ERP_SPECIFICATION.md Section 3.2 — mô tả màn hình và luồng nghiệp vụ
> Overlap với 3.1 được ghi chú. Các bước NEW là màn hình/DocType chưa có trong 3.1.

### 3.2.1. Kế hoạch mua hàng

- **Tag:** `NEW`
- **Spec yêu cầu:** Màn hình Kế hoạch mua hàng — thông tin chung (ngày, số KH, NCC, nội dung) + chi tiết (mã VT, tên VT, ĐVT, loại mua Demo/Purchase, đơn giá, Family, Year, Category, Sub Category, Shaft, Price, số lượng tháng 1-12)
- **ERPNext:** Material Request (gần nhất)
- **ERPNext đã có:** Material Request (MR) cho yêu cầu mua hàng, nhưng format hoàn toàn khác — MR là 1 danh sách items đơn giản, không có cột tháng 1-12, không có Family/Category/Shaft.
- **Gap:** Format spec rất đặc thù cho ngành golf (monthly planning, product attributes). ERPNext MR không phù hợp. Cần custom DocType.
- **Action:** Tạo custom DocType "Purchase Plan" (hoặc "Kế Hoạch Mua Hàng") với child table chứa các trường đặc thù. Link tới Supplier, kế thừa sang PO.
- **Effort:** 5 ngày
- **Clarify:** Xem CLARIFY.md #3.1 — Cần confirm format màn hình với khách
- **Legacy ref:** `import-management/IMPORT_MANAGEMENT_STATUS.md` Section 6.1 (Import Schedule)

### 3.2.2. Đơn hàng mua / Hợp đồng mua

- **Tag:** `CFG`
- **Spec yêu cầu:** Màn hình Đơn hàng mua — kế thừa từ KHMH. Thông tin: ngày, số ĐH, người lập, NCC, điều khoản TT, điều khoản GH + chi tiết: mã VT, tên VT, ĐVT, SL, ghi chú, số KHMH.
- **ERPNext:** Purchase Order
- **ERPNext đã có:** PO có đầy đủ các trường yêu cầu. "Get Items From" có thể link từ Material Request.
- **Gap:** Cần link từ custom "Purchase Plan" (3.2.1) thay vì MR. Trường "số kế hoạch mua hàng" cần custom field.
- **Action:** Config PO. Custom field `custom_purchase_plan` (Link). Setup "Get Items From Purchase Plan" nếu có custom DocType.
- **Effort:** 1 ngày
- **Overlap:** 3.1.3, 3.1.4

### 3.2.3. Kế hoạch giao hàng

- **Tag:** `NEW`
- **Spec yêu cầu:** Màn hình Kế hoạch giao hàng — rất nhiều trường đặc thù: PO Number, PO Create Date, Buyer name, Type, Product Group, Category, Location, Model, Stastic factor, Total Unit, Ship to, Month, Confirm ship date, Ship mode, EAN, UPC, PO comment, Remark, số KHMH, số ĐH. Kế thừa từ ĐH mua. Cảnh báo nếu tên VT chính thức khác tên trên danh mục.
- **ERPNext:** Không có tương đương
- **ERPNext đã có:** PO có thể track delivery dates nhưng không có DocType riêng cho "Kế hoạch giao hàng" với format này.
- **Gap:** Rất nhiều trường đặc thù không có trong ERPNext. Đây là format import từ hãng (Titleist/FootJoy) → cần DocType riêng.
- **Action:** Tạo custom DocType "Delivery Schedule" (hoặc "Kế Hoạch Giao Hàng"). Link tới PO. Import từ Excel của hãng. Client script cảnh báo tên VT.
- **Effort:** 5 ngày
- **Legacy ref:** `import-management/IMPORT_MANAGEMENT_STATUS.md` Section 2.4 (Delivery Schedule Status)

### 3.2.4. Đề nghị nhập hàng / Lệnh nhập hàng

- **Tag:** `EXT`
- **Spec yêu cầu:** Màn hình Lệnh nhập hàng — thông tin: ngày, số lệnh, người lập, NCC, kho, tình trạng thông quan, ngày dự kiến/thực tế thông quan. Chi tiết: mã VT, tên VT, SL, khách hàng, số KHMH, số ĐH, số KHGH. Chi tiết lô: số lot, serial number, SL.
- **ERPNext:** Purchase Receipt (Draft) hoặc Material Request
- **ERPNext đã có:** Purchase Receipt từ PO có thể làm draft trước khi submit. Nhưng không có trường thông quan, và không phải "lệnh" riêng trước khi nhập.
- **Gap:** Spec mô tả đây là 1 document riêng TRƯỚC Purchase Receipt — BP mua hàng tạo "lệnh", sau đó KT mới tạo phiếu nhập. Cần thêm trường thông quan. Có thể extend Purchase Receipt hoặc tạo DocType riêng.
- **Action:** Option A: Custom fields trên Purchase Receipt Draft (custom_customs_status, custom_clearance_date, etc.) + Workflow. Option B: Custom DocType "Lệnh Nhập Hàng" → link sang Purchase Receipt. Recommend Option A (đơn giản hơn).
- **Effort:** 3 ngày
- **Clarify:** Xem CLARIFY.md #3.2 — Custom DocType hay extend Purchase Receipt?

### 3.2.5. Phiếu nhập mua / Nhập khẩu

- **Tag:** `EXT`
- **Spec yêu cầu:** Màn hình Phiếu nhập mua/Nhập khẩu — kế thừa từ Lệnh nhập. Thêm: tiền tệ, số tờ khai, đơn giá KH, đơn giá ĐH (để so sánh). Cảnh báo nếu giá nhập khác giá ĐH.
- **ERPNext:** Purchase Receipt + Purchase Invoice
- **ERPNext đã có:** Purchase Receipt (nhập kho) và Purchase Invoice (ghi nhận công nợ). Hỗ trợ multi-currency. "Get Items From PO" tự động lấy giá từ PO.
- **Gap:** Trường "số tờ khai" cần custom field. Cảnh báo giá nhập vs giá PO — cần client script so sánh Rate vs PO Rate.
- **Action:** Custom fields: `custom_declaration_no` (Data), `custom_po_rate` (Currency, fetch từ PO). Client script cảnh báo khi Rate != PO Rate.
- **Effort:** 2 ngày
- **Overlap:** 3.1.6, 3.1.8, 3.1.9

### 3.2.6. Chi phí mua hàng

- **Tag:** `USE`
- **Spec yêu cầu:** Màn hình Chi phí mua hàng — vận chuyển, bốc dỡ...
- **ERPNext:** Landed Cost Voucher (LCV)
- **ERPNext đã có:** LCV link với Purchase Receipt, phân bổ chi phí (vận chuyển, thuế, bảo hiểm) vào giá nhập kho. Hỗ trợ nhiều loại chi phí.
- **Gap:** Không có gap lớn. LCV là chính xác những gì spec mô tả.
- **Action:** Config và test LCV workflow: Purchase Receipt → LCV (thêm chi phí) → Giá nhập được điều chỉnh.
- **Effort:** 1 ngày

### 3.2.7. Lệnh xuất trả lại NCC

- **Tag:** `EXT`
- **Spec yêu cầu:** BP mua hàng thống kê SP lỗi, hỏng, không đạt chất lượng gửi trả NCC. Màn hình Lệnh xuất hàng.
- **ERPNext:** Purchase Return (Debit Note) hoặc Stock Entry (Material Issue)
- **ERPNext đã có:** Purchase Receipt có nút "Make Return" → tạo return entry (số lượng âm). Debit Note tự động ghi nhận giảm công nợ.
- **Gap:** Spec mô tả 2 bước: (1) Lệnh xuất trả = quyết định trả, (2) Phiếu xuất trả = thực hiện trả kho. ERPNext gộp thành 1 bước (Return). Cần verify có cần tách 2 bước (approval trước khi xuất kho) hay không.
- **Action:** Nếu cần 2 bước: Workflow trên Purchase Receipt Return (Draft = Lệnh → Approved → Submitted = Phiếu xuất). Nếu 1 bước đủ: dùng Return trực tiếp.
- **Effort:** 2 ngày
- **Clarify:** Xem CLARIFY.md #3.3 — Cần tách 2 bước (lệnh + phiếu) hay 1 bước?

### 3.2.8. Trả lại NCC

- **Tag:** `USE`
- **Spec yêu cầu:** BP kho trả lại hàng không đạt chất lượng. Kế thừa từ Lệnh xuất trả. Màn hình Phiếu xuất trả lại.
- **ERPNext:** Purchase Receipt Return (Is Return = 1)
- **ERPNext đã có:** Purchase Receipt Return tự động giảm stock và giảm công nợ (Debit Note).
- **Gap:** Overlap với 3.2.7. Nếu 3.2.7 dùng Workflow thì 3.2.8 là bước Submit của Return.
- **Action:** Xem 3.2.7.
- **Effort:** (đã tính trong 3.2.7)
- **Overlap:** 3.2.7

### 3.2.9. Xác nhận công nợ

- **Tag:** `REF`
- **Spec yêu cầu:** BP mua hàng xác nhận công nợ và lập đề nghị thanh toán cho NCC.
- **ERPNext:** Accounts Payable report + Statement of Accounts
- **Gap:** Thuộc module 26 - KT Công nợ. Không thuộc scope module 05.
- **Action:** Ref → Module 26

### 3.2.10. Đề nghị thanh toán

- **Tag:** `EXT`
- **Spec yêu cầu:** Màn hình Đề nghị thanh toán — Ngày đề nghị, số đề nghị, nội dung, NCC, ĐH mua/HĐ mua, giá trị ĐH, đã tạm ứng, giá trị thanh toán, người lập, hình thức TT. Kế thừa từ ĐH mua.
- **ERPNext:** Payment Request hoặc Payment Entry
- **ERPNext đã có:** Payment Request (yêu cầu thanh toán, gửi email). Payment Entry (thực hiện thanh toán). Nhưng không có "Đề nghị thanh toán" như 1 approval document riêng.
- **Gap:** Spec mô tả "Đề nghị" = document cần phê duyệt TRƯỚC khi thanh toán. ERPNext Payment Request không có approval workflow sẵn.
- **Action:** Option A: Workflow trên Payment Entry (Draft → Đề nghị → Approved → Paid). Option B: Custom DocType "Đề Nghị Thanh Toán" → link sang Payment Entry. Recommend Option A.
- **Effort:** 2 ngày
- **Clarify:** Xem CLARIFY.md #3.4 — Workflow Payment Entry hay DocType riêng?

---

## Phần bổ sung

> Cuối Section 3 của ERP spec, có thêm 2 items:

### Import ảnh chi tiết

- **Tag:** `REF`
- **Spec yêu cầu:** Mô tả chi tiết cách import ảnh: chọn thư mục, đọc filename → match mã hàng → upload lên server.
- **Gap:** Đã cover trong 3.1.2. Đây là mô tả chi tiết của 3.1.2.
- **Action:** Ref → 3.1.2

### Báo cáo so sánh KHMH và ĐH

- **Tag:** `REF`
- **Spec yêu cầu:** Báo cáo so sánh Kế hoạch mua hàng vs Đơn đặt hàng
- **Gap:** Thuộc module 06 (BC Phân tích).
- **Action:** Ref → Module 06

---

## Tổng hợp

| Tag | Số feature | Effort |
|-----|-----------|--------|
| `USE` | 7 | 3.5 ngày |
| `CFG` | 4 | 3 ngày |
| `EXT` | 9 | 18 ngày |
| `NEW` | 2 | 10 ngày |
| `REF` | 3 | 0 |
| **Tổng** | **25** (ko tính 3 REF) | **~34.5 ngày** |

> **Lưu ý:** 34.5 ngày là effort tương đối, nhiều features làm song song.
> Thực tế ~20-25 ngày làm việc (1 người).

### Phân bổ effort theo nhóm

| Nhóm | Features | Effort |
|------|----------|--------|
| PO & Tracking (3.1.3-7, 3.2.2) | 6 | 5 ngày |
| Nhập hàng (3.1.6, 3.1.8-10, 3.1.16, 3.2.4-5) | 7 | 8.5 ngày |
| Thanh toán (3.1.12-14, 3.2.9-10) | 5 | 3.5 ngày |
| Kế hoạch (3.2.1, 3.2.3) — NEW DocTypes | 2 | 10 ngày |
| Ưu đãi + Import ảnh (3.1.1-2) | 2 | 4 ngày |
| Vòng đời + Trả hàng (3.1.11, 3.2.7-8) | 3 | 3 ngày |
| Báo cáo (3.1.17-18) | 2 | 3.5 ngày |
| Testing & QA | - | 3 ngày |
