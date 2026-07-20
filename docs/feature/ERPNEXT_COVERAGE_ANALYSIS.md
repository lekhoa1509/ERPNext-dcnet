# Phân tích Coverage: Spec khách hàng vs ERPNext v16

> **Mục đích:** Rà soát toàn bộ features từ 3 file spec của khách, phân loại thành 2 nhóm:
> 1. **Có sẵn trong ERPNext** — chỉ cần config/setup, không cần custom code
> 2. **Cần build mới** — không nằm trong bất kỳ module nào của ERPNext
>
> **Nguồn:** FEATURE_SPECIFICATION.md, ERP_SPECIFICATION.md, IMPORT_PROCESS_SPECIFICATION.md
>
> **Ngày phân tích:** 10/03/2026

---

## Tổng kết

| | Số lượng | Tỷ lệ |
|---|:---:|:---:|
| **Có sẵn trong ERPNext** (config/setup) | **~120** | **51%** |
| **Cần build mới** (custom code) | **~117** | **49%** |
| **Tổng cộng** | **~237** | 100% |

### Top custom modules cần build (theo số features)

| Custom Module | Số features | Độ phức tạp |
|---------------|:-----------:|:-----------:|
| Coaching (golf) | 13 | Cao |
| Kho nâng cao (vị trí, tem, mã vạch) | 12 | Cao |
| Fitting (golf) | 10 | Cao |
| Integration (API, Shopee, Zalo, Viettel Post) | 10 | Cao |
| Trade-in | 9 | Trung bình |
| Kế toán nâng cao (HTKK, CCDC, phân bổ) | 8 | Rất cao |
| CSKH | 7 | Trung bình |
| Dashboard | 6 | Thấp |
| Mua hàng nâng cao | 5 | Trung bình |
| Sales Planning | 4 | Trung bình |
| Báo cáo Custom | ~20 | Trung bình |
| Import Process | ~8 | Cao |

---

## Bảng 1: Có sẵn trong ERPNext (~120 features)

> Các features này đã có trong ERPNext standard, chỉ cần config, setup data, hoặc tùy chỉnh giao diện.

### Đăng nhập / Hệ thống

| # | Spec ID | Feature | ERPNext Module |
|---|---------|---------|----------------|
| 1 | 1.1 | Đăng nhập email/password | Frappe Auth |
| 2 | 1.2 | Đăng xuất | Frappe Auth |
| 3 | 1.3 | Quên mật khẩu | Frappe Auth |

### Lead

| # | Spec ID | Feature | ERPNext Module |
|---|---------|---------|----------------|
| 4 | 3.1 | Danh sách Lead (list, filter) | CRM > Lead |
| 5 | 3.2 | Tạo Lead | CRM > Lead |
| 6 | 3.3 | Import Lead (Excel) | Frappe Data Import |
| 7 | 3.4 | Xem chi tiết Lead | CRM > Lead |
| 8 | 3.5 | Cập nhật Lead | CRM > Lead |
| 9 | 3.6 | Xóa Lead | CRM > Lead |
| 10 | 3.8 | Export Lead | Frappe Data Export |

### Khách hàng

| # | Spec ID | Feature | ERPNext Module |
|---|---------|---------|----------------|
| 11 | 4.1 | Danh sách Khách hàng | Selling > Customer |
| 12 | 4.2 | Xem chi tiết KH (info, lịch sử GD) | Customer DocType |
| 13 | 4.4 | Cập nhật KH | Customer DocType |
| 14 | 4.5 | Quản lý Nguồn KH (CRUD) | CRM > Lead Source |
| 15 | 4.6 | Tích điểm (quy tắc, lên hạng) | Loyalty Program |
| 16 | 4.7 | Xóa KH | Customer DocType |
| 17 | 4.8 | Import KH (Excel) | Frappe Data Import |
| 18 | 4.9 | Export KH (Excel) | Frappe Data Export |

### Đơn hàng bán

| # | Spec ID | Feature | ERPNext Module |
|---|---------|---------|----------------|
| 19 | 5.1 | Danh sách Đơn hàng | Selling > Sales Order |
| 20 | 5.2.1 | Tạo đơn vật dụng (bán lẻ/buôn) | Sales Order |
| 21 | 5.2.6 | Kiểm tra tồn kho trước khi tạo đơn | Stock > Projected Qty |
| 22 | 5.3 | Import Đơn hàng (Excel) | Frappe Data Import |
| 23 | 5.4 | Xem chi tiết Đơn hàng | Sales Order |
| 24 | 5.5 | Cập nhật Đơn hàng | Sales Order |
| 25 | 5.6 | Bảo hành (tạo phiếu, trạng thái) | Support > Warranty Claim |
| 26 | 5.7 | Xóa Đơn hàng | Sales Order (Cancel/Amend) |
| 27 | 5.8 | In Đơn hàng | Print Format |
| 28 | 5.10 | Export Đơn hàng | Frappe Data Export |

### Sản phẩm

| # | Spec ID | Feature | ERPNext Module |
|---|---------|---------|----------------|
| 29 | 6.1 | Danh sách Sản phẩm | Stock > Item |
| 30 | 6.2 | Quản lý Danh mục SP | Stock > Item Group |
| 31 | 6.3 | Tạo Sản phẩm | Item DocType |
| 32 | 6.4 | Import SP (Excel) | Frappe Data Import |
| 33 | 6.5 | Export SP (Excel) | Frappe Data Export |
| 34 | 6.6 | Xem chi tiết SP | Item DocType |

### Bán hàng

| # | Spec ID | Feature | ERPNext Module |
|---|---------|---------|----------------|
| 35 | 7.2 | Chính sách Chiết khấu | Selling > Pricing Rule |
| 36 | 7.3 | Quản lý Bán lẻ (POS, hóa đơn, đổi trả) | POS + Sales Invoice |
| 37 | 7.4 | Hàng trả lại (return) | Sales Invoice (Credit Note) |
| 38 | 7.7 | Danh sách Bảng giá | Stock > Price List |
| 39 | 7.8 | Thêm mới Bảng giá | Price List DocType |
| 40 | 7.9 | Xem chi tiết Bảng giá | Item Price / Price List |
| 41 | 7.10 | Cập nhật Bảng giá | Price List / Item Price |
| 42 | 7.11 | Xóa Bảng giá | Price List DocType |

### Kho

| # | Spec ID | Feature | ERPNext Module |
|---|---------|---------|----------------|
| 43 | 8.1 | Danh sách Kho | Stock > Warehouse |
| 44 | 8.2 | Tạo Kho (tên, mã, địa chỉ, NV phụ trách) | Warehouse DocType |
| 45 | 8.3 | Xem chi tiết Kho (tồn kho, định mức) | Stock Balance + Reorder Level |
| 46 | ERP-4.1.1 | Danh sách kho | Stock > Warehouse |
| 47 | ERP-4.1.3 | Danh mục vật tư hàng hóa | Stock > Item |
| 48 | ERP-4.1.4 | Quản lý theo lô (Batch) | Stock > Batch |
| 49 | ERP-4.1.5 | Quản lý theo Serial | Stock > Serial No |
| 50 | ERP-4.1.6 | Nhập kho (NCC, điều chuyển, trả hàng) | Purchase Receipt / Stock Entry |
| 51 | ERP-4.1.7 | Xuất kho (bán, điều chuyển, hao hụt) | Delivery Note / Stock Entry |
| 52 | ERP-4.1.8 | Nhập xuất theo mã số | Stock Ledger Entry |
| 53 | ERP-4.1.9 | Theo dõi tồn kho thực tế | Stock > Bin / Stock Balance |
| 54 | ERP-4.1.15 | Điều chuyển kho | Stock Entry (Material Transfer) |
| 55 | ERP-4.1.16 | Kiểm kê kho | Stock Reconciliation |
| 56 | ERP-4.1.17 | Điều chỉnh kho (thừa/thiếu) | Stock Reconciliation |
| 57 | ERP-4.1.19 | Lịch sử kho | Stock Ledger + Activity Log |

### Chi nhánh

| # | Spec ID | Feature | ERPNext Module |
|---|---------|---------|----------------|
| 58 | 10.1 | Danh sách Chi nhánh | Setup > Branch |
| 59 | 10.2 | Tạo Chi nhánh | Branch DocType |
| 60 | 10.3 | Xem chi tiết Chi nhánh | Branch DocType |
| 61 | 10.4 | Cập nhật Chi nhánh | Branch DocType |
| 62 | 10.5 | Xóa Chi nhánh | Branch DocType |

### Nhân viên

| # | Spec ID | Feature | ERPNext Module |
|---|---------|---------|----------------|
| 63 | 11.1 | Danh sách Nhân viên | HR > Employee |
| 64 | 11.2 | Tạo Nhân viên (1 hoặc nhiều) | Employee DocType |
| 65 | 11.3 | Xem chi tiết Nhân viên | Employee DocType |
| 66 | 11.4 | Cập nhật Nhân viên | Employee DocType |
| 67 | 11.5 | Xóa Nhân viên | Employee DocType |
| 68 | 11.6 | Import Nhân viên (Excel) | Frappe Data Import |
| 69 | 11.7 | Export Nhân viên (Excel) | Frappe Data Export |

### Phân quyền

| # | Spec ID | Feature | ERPNext Module |
|---|---------|---------|----------------|
| 70 | 12.1 | Danh sách Role | Setup > Role |
| 71 | 12.2 | Tạo Role | Role DocType |
| 72 | 12.3 | Cập nhật Role | Role DocType |
| 73 | 12.4 | Xóa Role | Role DocType |

### Cài đặt

| # | Spec ID | Feature | ERPNext Module |
|---|---------|---------|----------------|
| 74 | 13.1 | Cài đặt KH (phân công lead, tags, trạng thái) | CRM Lead Assignment |
| 75 | 13.2 | Danh sách Chức vụ | HR > Designation |
| 76 | 13.3 | Nhóm Khách hàng | Customer Group |
| 77 | 13.4 | Trạng thái Đơn hàng | Sales Order Workflow |

### Danh mục & NCC

| # | Spec ID | Feature | ERPNext Module |
|---|---------|---------|----------------|
| 78 | ERP-DM.KH | Danh mục đối tượng (KH, NCC) | Customer + Supplier |
| 79 | ERP-DM.VTHH | Danh mục vật tư (mã, nhóm, lot tracking) | Item (Batch/Serial) |
| 80 | ERP-3.0.1 | Danh mục NCC | Buying > Supplier |
| 81 | ERP-3.0.2 | Bảng giá NCC | Supplier Quotation |

### Mua hàng

| # | Spec ID | Feature | ERPNext Module |
|---|---------|---------|----------------|
| 82 | ERP-3.Feature 3 | Tạo PO | Purchase Order |
| 83 | ERP-3.Feature 4 | Chi tiết PO (model, SKU, SL, giá) | PO Item |
| 84 | ERP-3.Feature 5 | Theo dõi PO (trạng thái) | PO Workflow |
| 85 | ERP-3.Feature 6 | Nhập hàng 1 phần / nhiều lần | Purchase Receipt (partial) |
| 86 | ERP-3.Feature 7 | Theo dõi thực hiện mua (% đã nhận) | PO % received |
| 87 | ERP-3.Feature 8 | Nhập hàng theo lô | Stock > Batch |
| 88 | ERP-3.Feature 9 | Nhập hàng theo serial | Stock > Serial No |
| 89 | ERP-3.Feature 12 | Nguồn tiền (quỹ, TK ngân hàng) | Mode of Payment |
| 90 | ERP-3.Feature 13 | Phương thức thanh toán | Payment Entry |
| 91 | ERP-3.Feature 14 | Theo dõi thanh toán PO | PO payment status |
| 92 | ERP-3.Feature 15 | Đính kèm chứng từ | File Attachment |
| 93 | ERP-3.Feature 17 | Lịch sử mua hàng | Purchase Analytics |
| 94 | ERP-3.Bước 4 | Đề nghị nhập hàng | Material Request |
| 95 | ERP-3.Bước 5 | Phiếu nhập mua/nhập khẩu | Purchase Receipt |
| 96 | ERP-3.Bước 6 | Chi phí mua hàng (Landed Cost) | Landed Cost Voucher |
| 97 | ERP-3.Bước 7-8 | Trả lại NCC | Purchase Return / Debit Note |
| 98 | ERP-3.Bước 9 | Xác nhận công nợ NCC | Supplier Ledger |
| 99 | ERP-3.Bước 10 | Đề nghị thanh toán | Payment Entry |

### Bán hàng (ERP)

| # | Spec ID | Feature | ERPNext Module |
|---|---------|---------|----------------|
| 100 | ERP-2.Bước 2 | Bảng giá niêm yết | Price List |
| 101 | ERP-2.Bước 4 | Đơn đặt hàng bán (SO) | Sales Order |
| 102 | ERP-2.Bước 5 | Kiểm tra tồn kho | Actual/Projected Qty |
| 103 | ERP-2.Bước 6 | Lệnh xuất hàng | Delivery Note |
| 104 | ERP-2.Bước 9 | Hóa đơn bán buôn | Sales Invoice |
| 105 | ERP-2.Bước 10-11 | Hàng bán trả lại | Sales Return / Credit Note |
| 106 | ERP-2.BánLẻ | Bảng giá bán lẻ + POS | Price List + POS Invoice |

### Kế toán

| # | Spec ID | Feature | ERPNext Module |
|---|---------|---------|----------------|
| 107 | ERP-5.1.1 | Quản lý tiền mặt (sổ quỹ, thu chi) | Journal Entry / Cash Entry |
| 108 | ERP-5.1.2 | Quản lý tiền ngân hàng | Bank Account / Bank Recon |
| 109 | ERP-5.2.1 | Kế toán mua hàng | Purchase Invoice |
| 110 | ERP-5.2.2 | Theo dõi thanh toán mua | Payment Entry |
| 111 | ERP-5.3.1 | Ghi nhận doanh thu | Sales Invoice |
| 112 | ERP-5.4.1 | Công nợ phải thu (hạn TT, tuổi nợ) | Accounts Receivable |
| 113 | ERP-5.4.2 | Công nợ phải trả | Accounts Payable |
| 114 | ERP-5.5.1 | Giá trị tồn kho | Stock Balance (valuation) |
| 115 | ERP-5.5.2 | Giá vốn COGS (FIFO/Moving Avg) | Stock Valuation |
| 116 | ERP-5.7.1 | Quản lý TSCĐ (khấu hao đường thẳng) | Assets > Asset |
| 117 | ERP-5.8.1 | Kế toán thuế (VAT đầu vào/ra) | Tax Templates |
| 118 | ERP-5.9.1 | Báo cáo KQKD | Profit & Loss Statement |
| 119 | ERP-5.9.4 | Audit log | Frappe Activity Log |

### Báo cáo

| # | Spec ID | Feature | ERPNext Module |
|---|---------|---------|----------------|
| 120 | 14.1 | BC Doanh số (thời gian, chi nhánh, SP) | Sales Analytics |
| 121 | 14.2 | BC Đơn hàng (tổng đơn, trạng thái) | Sales Order Analytics |
| 122 | 14.3 | BC Khách hàng (lead, top KH) | CRM Reports |
| 123 | 14.5 | BC Kho (tồn kho, giá trị, định mức) | Stock Balance / Ledger |
| 124 | ERP-4.2.1 | BC nhập xuất tồn | Stock Balance Report |
| 125 | ERP-4.2.2 | BC theo serial | Serial No Report |
| 126 | ERP-6.1.1-2 | BC tổng hợp NXT, tồn theo kho | Stock Balance (group by) |
| 127 | ERP-6.2.1 | BC hàng bán ra | Sales Analytics |
| 128 | ERP-6.4.2 | Kết xuất BC (Excel, PDF) | Built-in Export |

### Giao vận & Hỗ trợ

| # | Spec ID | Feature | ERPNext Module |
|---|---------|---------|----------------|
| 129 | 9.1 | Danh sách đơn giao vận | Stock > Delivery Note |
| 130 | 4.3.3 | Phiếu hỗ trợ - Ticket | Support > Issue |

---

## Bảng 2: Cần build mới (~117 features)

> Các features này KHÔNG có trong bất kỳ module ERPNext standard nào, cần custom DocType hoặc custom app.

### Dashboard (6 features)

| # | Spec ID | Feature | Lý do | Độ phức tạp |
|---|---------|---------|-------|:-----------:|
| 1 | 2.1 | Dashboard DS theo ngày/tuần/tháng | Custom layout theo spec | Thấp |
| 2 | 2.2 | Dashboard DS bán sỉ | Custom Number Card | Thấp |
| 3 | 2.3 | Dashboard DS bán lẻ tổng | Custom Number Card | Thấp |
| 4 | 2.4 | Dashboard DS theo nguồn KH | Custom report/chart | Thấp |
| 5 | 2.5 | Dashboard DS theo nguồn Đơn hàng | Custom report/chart | Thấp |
| 6 | 2.6 | Dashboard DS theo SP Top 20 | Custom report | Thấp |

### Fitting - Golf (10 features)

| # | Spec ID | Feature | Lý do | Độ phức tạp |
|---|---------|---------|-------|:-----------:|
| 7 | 16.1.1 | Danh sách đơn Fitting | Golf-specific domain | Cao |
| 8 | 16.1.2 | Tạo đơn Fitting (nguồn, lịch hẹn) | Golf-specific domain | Cao |
| 9 | 16.1.3 | Trạng thái đơn Fitting (5 TT) | Golf-specific domain | TB |
| 10 | 16.1.4 | Nhập thông số kỹ thuật Fitting | Golf-specific domain | Cao |
| 11 | 16.1.5 | Dịch vụ phát sinh (grip, shaft) | Golf-specific domain | TB |
| 12 | 16.1.6 | Phân công NV Fitting | Golf-specific domain | TB |
| 13 | 16.2.1 | Tạo SO từ Fitting | Golf-specific domain | TB |
| 14 | 16.2.2 | Tích hợp Website (API đăng ký) | Golf-specific domain | Cao |
| 15 | 16.2.3 | Báo cáo Fitting | Golf-specific domain | TB |
| 16 | 16.2.4 | Dashboard Widgets Fitting | Golf-specific domain | Thấp |

### Coaching - Golf (13 features)

| # | Spec ID | Feature | Lý do | Độ phức tạp |
|---|---------|---------|-------|:-----------:|
| 17 | 17.1.1 | Danh sách đơn Coaching | Golf-specific domain | Cao |
| 18 | 17.1.2 | Tạo đơn Coaching (hồ sơ, gói học) | Golf-specific domain | Cao |
| 19 | 17.1.3 | Trạng thái đơn Coaching (8 TT) | Golf-specific domain | TB |
| 20 | 17.1.4 | Quản lý Gói huấn luyện | Golf-specific domain | Cao |
| 21 | 17.1.5 | Quản lý HLV (chứng chỉ, rating) | Golf-specific domain | Cao |
| 22 | 17.1.6 | Quản lý Sân tập | Golf-specific domain | TB |
| 23 | 17.1.7 | Bài test đầu vào | Golf-specific domain | Cao |
| 24 | 17.1.8 | Lịch học & Điểm danh | Golf-specific domain | Cao |
| 25 | 17.1.9 | Tiến độ học tập (kỹ năng, đánh giá) | Golf-specific domain | Cao |
| 26 | 17.2.1 | Tạo SO từ Coaching | Golf-specific domain | TB |
| 27 | 17.2.2 | Thông báo & Nhắc lịch tự động | Custom notification | Cao |
| 28 | 17.2.3 | Báo cáo Coaching | Golf-specific domain | TB |
| 29 | 17.2.4 | Dashboard Widgets Coaching | Golf-specific domain | Thấp |

### Trade-in (9 features)

| # | Spec ID | Feature | Lý do | Độ phức tạp |
|---|---------|---------|-------|:-----------:|
| 30 | 18.1.1 | Danh sách đơn Thu cũ Đổi mới | Custom module | Cao |
| 31 | 18.1.2 | Tạo đơn Trade-in (SP cũ/mới, chênh lệch) | Custom module | Cao |
| 32 | 18.1.3 | Trạng thái Trade-in (7 TT) | Custom module | TB |
| 33 | 18.1.4-5 | Xem/Cập nhật đơn Trade-in | Custom module | TB |
| 34 | 18.2.1 | Quy trình kiểm tra & định giá SP cũ | Custom module | Cao |
| 35 | 18.2.2 | Tích hợp Kho (nhập cũ, xuất mới) | Custom integration | Cao |
| 36 | 18.2.3 | Báo cáo Trade-in | Custom module | TB |
| 37 | 18.2.4 | Dashboard Widgets Trade-in | Custom module | Thấp |

### CSKH (7 features)

| # | Spec ID | Feature | Lý do | Độ phức tạp |
|---|---------|---------|-------|:-----------:|
| 38 | 4.3.1 | Lịch chăm sóc tự động (nhắc lịch) | Custom DocType | Cao |
| 39 | 4.3.2 | Lịch gửi khuyến mãi tự động | Custom DocType | Cao |
| 40 | 4.3.4 | Phân quyền CSKH theo nhóm | Custom assignment logic | TB |
| 41 | 4.3.5 | Khảo sát mức độ hài lòng | Custom DocType | TB |
| 42 | 4.3.6 | Tích hợp Zalo OA / Messenger | External integration | Rất cao |
| 43 | 4.3.7 | Upsell/Cross-sell (gợi ý SP) | Custom logic | Cao |
| 44 | 5.9 | Resell (thông báo, đề xuất mua lại) | Custom re-marketing | TB |

### Kế hoạch Bán hàng (4 features)

| # | Spec ID | Feature | Lý do | Độ phức tạp |
|---|---------|---------|-------|:-----------:|
| 45 | 7.1 | Quản lý Kế hoạch Bán hàng | Custom DocType | TB |
| 46 | ERP-2.Bước 1 | KH bán hàng theo năm (target theo KH) | Custom DocType | TB |
| 47 | ERP-DM.KHDSNK | KH doanh số năm (theo KH, % DS) | Custom DocType | TB |
| 48 | ERP-2.Bước 12 | Tính thưởng đạt KH doanh số | Custom calculation | Cao |

### Bán hàng nâng cao (5 features)

| # | Spec ID | Feature | Lý do | Độ phức tạp |
|---|---------|---------|-------|:-----------:|
| 49 | 7.5 | Tính thưởng Doanh số (3 bước) | Custom commission | Cao |
| 50 | 7.6 | Quản lý Voucher (CRUD) | Custom voucher system | TB |
| 51 | ERP-2.Bước 3 | Chính sách CK bán buôn nâng cao | Custom policy doc | TB |
| 52 | ERP-2.BánLẻ.2 | Chính sách CK bán lẻ (công thức đặc biệt) | Custom formula | TB |
| 53 | ERP-2.Bước 7-8 | Hạn mức & cảnh báo công nợ quá hạn | Custom validation + approval | Cao |

### Kho nâng cao (12 features)

| # | Spec ID | Feature | Lý do | Độ phức tạp |
|---|---------|---------|-------|:-----------:|
| 54 | ERP-4.1.2 | Quản lý vị trí kho (khu vực, kệ, ô) | Không có trong ERPNext | Cao |
| 55 | ERP-4.1.10 | Tồn kho khả dụng (thực tế - tồn giữ) | Custom calculation | TB |
| 56 | ERP-4.1.11 | Giữ hàng theo đơn | Custom reserve logic | Cao |
| 57 | ERP-4.1.12 | Quản lý mã vạch (quy ước tem) | Custom barcode workflow | Cao |
| 58 | ERP-4.1.13 | Tạo tem sản phẩm | Custom label generation | Cao |
| 59 | ERP-4.1.14 | In tem (đơn/hàng loạt, tùy chỉnh mẫu) | Custom label printing | Cao |
| 60 | ERP-4.1.18 | Cảnh báo kho (tồn thấp + sắp hết vòng đời) | Custom alert + shelf-life | TB |
| 61 | ERP-4.1.20 | Tính giá vốn trung bình tháng | ERPNext chỉ có FIFO/MA | Rất cao |
| 62 | ERP-3.Feature 10 | Nhập hàng theo mã vạch (scan) | Custom scan workflow | Cao |
| 63 | ERP-3.Feature 11 | Khai báo vòng đời SP | Custom shelf-life | TB |
| 64 | ERP-3.Feature 16 | Trạng thái phiếu nhập (workflow duyệt) | Custom approval workflow | TB |
| 65 | ERP-4.3 | Xuất nội bộ giữa cửa hàng (duyệt 2 bên) | Custom dual-approval | Cao |

### Ký gửi (1 feature)

| # | Spec ID | Feature | Lý do | Độ phức tạp |
|---|---------|---------|-------|:-----------:|
| 66 | ERP-4.3 | Quy trình hàng ký gửi (TLTM ↔ NM, 5 bước) | Completely custom | Rất cao |

### Mua hàng nâng cao (5 features)

| # | Spec ID | Feature | Lý do | Độ phức tạp |
|---|---------|---------|-------|:-----------:|
| 67 | ERP-3.Bước 1 | Kế hoạch mua hàng (12 tháng, golf-specific) | Custom procurement plan | Cao |
| 68 | ERP-3.Bước 3 | Kế hoạch giao hàng (Ship mode, EAN) | Custom DocType | TB |
| 69 | ERP-3.Feature 1 | Ưu đãi NCC (CK, quà tặng) | Custom incentive tracking | TB |
| 70 | ERP-3.Feature 2 | Import hình ảnh SP hàng loạt | Custom bulk image import | TB |
| 71 | ERP-3.Feature 18 | BC mua hàng (giá bình quân, NCC tốt nhất) | Custom purchasing analytics | TB |

### Kế toán nâng cao (8 features)

| # | Spec ID | Feature | Lý do | Độ phức tạp |
|---|---------|---------|-------|:-----------:|
| 72 | ERP-5.1.2 | Theo dõi khế ước ngân hàng | Custom DocType | TB |
| 73 | ERP-5.4.3 | Tạm ứng - Hoàn ứng (NV/NCC) | Custom advance workflow | Cao |
| 74 | ERP-5.6.1 | Chi phí hỗ trợ hàng (Marketing, Demo) | Custom cost tracking | TB |
| 75 | ERP-5.6.2 | Phân bổ chi phí (theo SP, chiến dịch) | Custom cost allocation | Cao |
| 76 | ERP-5.7.2 | Công cụ dụng cụ (phân bổ nhiều kỳ) | Custom CCDC tracking | Cao |
| 77 | ERP-5.8.2 | Kết xuất dữ liệu thuế HTKK | Custom Vietnam tax export | Rất cao |
| 78 | ERP-5.9.4 | Bút toán tự động (tỷ giá, kết chuyển) | Custom recurring entries | Cao |
| 79 | ERP-5.9.2 | BC chi phí (Marketing, Demo, sự kiện) | Custom event cost report | TB |

### Tích hợp (10 features)

| # | Spec ID | Feature | Lý do | Độ phức tạp |
|---|---------|---------|-------|:-----------:|
| 80 | 3.7 | Tự động tạo Lead từ nhanh.vn | Integration nhanh.vn | Cao |
| 81 | 3.9 | API tạo Khách hàng (từ hệ thống khác) | Custom API endpoint | TB |
| 82 | 5.11 | API tạo Đơn hàng | Custom API endpoint | TB |
| 83 | 5.12 | Kết nối Shopee/TikTok/Lazada/Website | E-commerce integration | Rất cao |
| 84 | 9.2 | Liên kết Viettel Post (tạo đơn, tracking) | Custom integration | Cao |
| 85 | ERP-7.1.1 | Đồng bộ dữ liệu cho hãng | Custom data sync | Cao |
| 86 | ERP-7.2.1 | Đồng bộ KH (Web ↔ CRM, 2 chiều) | Custom API | Cao |
| 87 | ERP-7.2.2-3 | Đồng bộ hàng hóa + kho → Web | Custom API | Cao |
| 88 | ERP-7.2.4 | Đồng bộ đơn hàng Web → CRM | Custom API | Cao |
| 89 | ERP-7.2.5 | Đồng bộ tồn kho realtime → Web | Custom API | Rất cao |

### Web Analytics (4 features)

| # | Spec ID | Feature | Lý do | Độ phức tạp |
|---|---------|---------|-------|:-----------:|
| 90 | 15.1 | Ghi nhận lượt truy cập web | Website analytics | Cao |
| 91 | 15.2 | Bản đồ nhiệt (Heatmap) | Website heatmap | Rất cao |
| 92 | 15.3 | Phân tích Data (PageView, Session...) | Website analytics | Rất cao |
| 93 | 15.4 | Tối ưu (ghi phiên không ảnh hưởng tốc độ) | Website performance | Cao |

### Báo cáo Custom (~20 features)

| # | Spec ID | Feature | Lý do | Độ phức tạp |
|---|---------|---------|-------|:-----------:|
| 94 | 14.4 | BC Nhân viên (tỉ lệ chốt, hiệu suất) | Custom KPI report | TB |
| 95 | 14.2 | BC Fitting (doanh thu, số buổi) | Custom report | TB |
| 96 | 14.2 | BC Coaching (doanh thu, HLV) | Custom report | TB |
| 97 | 14.2 | BC Cửa hàng/Đại lý | Custom report | TB |
| 98 | ERP-3.BC | BC so sánh KH mua vs đơn hàng | Custom comparison report | TB |
| 99 | ERP-4.2.3 | BC tồn khả dụng (thực tế vs tồn giữ) | Custom report | Thấp |
| 100 | ERP-4.2.4 | BC vòng đời SP (còn 60/45 ngày) | Custom report | Thấp |
| 101 | ERP-4.2.5 | Phân tích kho (bán nhanh/chậm) | Custom report | TB |
| 102 | ERP-5.9.3 | BC quản trị (chi nhánh, đại lý) | Custom report | TB |
| 103 | ERP-6.1.3 | BC tồn kho theo model/SKU (tỷ trọng) | Custom report | Thấp |
| 104 | ERP-6.1.4 | BC tồn kho theo lô | Custom report | Thấp |
| 105 | ERP-6.1.5 | BC tồn theo vòng đời (mới/chậm/sắp hết) | Custom report | TB |
| 106 | ERP-6.2.2 | BC hàng bán theo đại lý | Custom report | Thấp |
| 107 | ERP-6.2.3 | BC luân chuyển hàng hóa | Custom report | TB |
| 108 | ERP-6.3.1 | BC hàng tồn chậm (đề xuất sale/điều chuyển) | Custom report | TB |
| 109 | ERP-6.3.2 | BC hàng sắp hết vòng đời (60/45 ngày) | Custom report | Thấp |
| 110 | ERP-6.3.3 | BC hàng điều chuyển (giữa kho, cho đại lý) | Custom report | Thấp |
| 111 | ERP-6.3.4 | BC hàng thanh lý / sale | Custom report | Thấp |
| 112 | ERP-6.4.1 | BC quản trị theo yêu cầu | Custom flexible report | Cao |

### Import Process (8 features)

| # | Spec ID | Feature | Lý do | Độ phức tạp |
|---|---------|---------|-------|:-----------:|
| 113 | Đại lý B1 | BC bán hàng / thị trường (họp đề xuất) | Custom dealer report | TB |
| 114 | Đại lý B4 | Pre-order + MOQ tracking | Custom DocType | Cao |
| 115 | Đại lý B4 | Lịch trình đặt hàng 7 loại SP | Domain-specific calendar | Cao |
| 116 | Đại lý B6 | Deadline tracking 01 ngày kiểm tra | Custom SLA | TB |
| 117 | TLTM B1 | Lịch trình đặt hàng cố định + đặc biệt | Custom procurement calendar | Cao |
| 118 | TLTM B2 | Workflow họp 6 bộ phận đánh giá SP | Multi-dept approval | Cao |
| 119 | TLTM B3 | Workflow 3 cấp approval | Custom multi-level | TB |
| 120 | TLTM B5-9 | Timeline tracking + Hải quan + Kiểm tra hàng | Custom import workflow | Rất cao |

### Khác (2 features)

| # | Spec ID | Feature | Lý do | Độ phức tạp |
|---|---------|---------|-------|:-----------:|
| 121 | 3.4 | Lịch sử tư vấn (SP, NV, nội dung) | Custom child table in Lead | Thấp |
| 122 | 13.5 | Danh sách Hành động NV (gọi, nhắn, email) | Custom activity type | Thấp |

---

## Ghi chú

### Lưu ý quan trọng

1. **"Có sẵn" không có nghĩa là "không cần làm gì"** — vẫn cần config, setup data, tùy chỉnh Print Format, Permission, Workflow cho phù hợp.

2. **Gap Analysis cũ** (`*_GAP_ANALYSIS.md`) tham chiếu nền tảng CŨ (flow_crm / Aureus / Laravel). Không áp dụng cho ERPNext v16.

3. **Một số features "có sẵn" nhưng cần mở rộng nhẹ** (custom field, client script) — không liệt kê ở Bảng 2 vì effort thấp, vẫn dùng DocType gốc.

4. **Web Analytics (15.x)** — nên cân nhắc dùng 3rd party (Google Analytics, Hotjar) thay vì tự build.

5. **Giá vốn trung bình tháng (ERP-4.1.20)** — ERPNext chỉ hỗ trợ FIFO và Moving Average. Cần clarify với khách.

### Vấn đề cần clarify với khách hàng

| # | Vấn đề | Ảnh hưởng |
|---|--------|-----------|
| 1 | TT99 vs TT200 (hệ thống tài khoản) | Toàn bộ kế toán |
| 2 | Giá vốn "trung bình tháng" vs Moving Average | Kho + Kế toán |
| 3 | Trade-in: Giá cũ > giá mới → hoàn tiền? | Trade-in module |
| 4 | HĐĐT: Tích hợp nhà cung cấp nào? | Kế toán thuế |
| 5 | Web Analytics: Tự build hay dùng 3rd party? | Scope & effort |
| 6 | Shopee/TikTok/Lazada: Cần tích hợp ngay hay sau? | Timeline |

---

**Nguồn:** FEATURE_SPECIFICATION.md, ERP_SPECIFICATION.md, IMPORT_PROCESS_SPECIFICATION.md
**Ngày phân tích:** 10/03/2026
**Cập nhật lần cuối:** 10/03/2026
