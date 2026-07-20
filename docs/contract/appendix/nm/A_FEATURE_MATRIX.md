# PHỤ LỤC A - DANH SÁCH TÍNH NĂNG CHI TIẾT
# FEATURE MATRIX

> **Tài liệu:** SRS - DCNET Flow
> **Phiên bản:** 1.0.0
> **Ngày tạo:** 03/02/2026

---

## TỔNG QUAN

| Thông tin | Giá trị |
|-----------|---------|
| **Tổng số Modules** | 46 |
| **Tổng số Features** | 237 |
| **Phase 1 (CRM)** | 23 modules, 135 features |
| **Phase 2 (ERP)** | 23 modules, 102 features |

---

## PHASE 1: CRM (135 Features)

### Đợt 1: Foundation & Core CRM (74 features)

#### 1. Đăng nhập/Đăng xuất (3 features)

| # | Feature ID | Tên tính năng | Mô tả | Độ ưu tiên |
|---|------------|---------------|-------|------------|
| 1 | AUTH-001 | Đăng nhập | Đăng nhập bằng email/password | Critical |
| 2 | AUTH-002 | Đăng xuất | Đăng xuất khỏi hệ thống | Critical |
| 3 | AUTH-003 | Quên mật khẩu | Khôi phục mật khẩu qua email | High |

#### 2. Quản lý Lead (9 features)

| # | Feature ID | Tên tính năng | Mô tả | Độ ưu tiên |
|---|------------|---------------|-------|------------|
| 4 | LEAD-001 | Danh sách Lead | Hiển thị danh sách Lead với filter | Critical |
| 5 | LEAD-002 | Tạo Lead | Tạo Lead mới với thông tin cơ bản | Critical |
| 6 | LEAD-003 | Import Lead | Import Lead từ file Excel | High |
| 7 | LEAD-004 | Export Lead | Export Lead ra file Excel | Medium |
| 8 | LEAD-005 | Xem chi tiết Lead | Xem thông tin Lead 360° | Critical |
| 9 | LEAD-006 | Cập nhật Lead | Sửa thông tin Lead | Critical |
| 10 | LEAD-007 | Xóa Lead | Xóa Lead khỏi hệ thống | Medium |
| 11 | LEAD-008 | Tự động tạo Lead | Nhận Lead từ nguồn bên ngoài | High |
| 12 | LEAD-009 | API tạo Lead | Expose API cho hệ thống khác | High |

#### 3. Quản lý Khách hàng (12 features)

| # | Feature ID | Tên tính năng | Mô tả | Độ ưu tiên |
|---|------------|---------------|-------|------------|
| 13 | CUST-001 | Danh sách KH | Hiển thị danh sách khách hàng | Critical |
| 14 | CUST-002 | Xem chi tiết KH | Hồ sơ khách hàng 360° | Critical |
| 15 | CUST-003 | Cập nhật KH | Sửa thông tin khách hàng | Critical |
| 16 | CUST-004 | Xóa KH | Xóa khách hàng | Medium |
| 17 | CUST-005 | Import KH | Import KH từ Excel | High |
| 18 | CUST-006 | Export KH | Export KH ra Excel | Medium |
| 19 | CUST-007 | Nguồn KH | Quản lý danh sách nguồn | High |
| 20 | CUST-008 | Quy tắc tích điểm | Thiết lập tích điểm | High |
| 21 | CUST-009 | Quy tắc lên hạng | Thiết lập hạng thành viên | High |
| 22 | CUST-010 | Đổi điểm | Đổi điểm lấy ưu đãi | High |
| 23 | CUST-011 | Lịch sử tích điểm | Xem lịch sử điểm | Medium |
| 24 | CUST-012 | Công nợ KH | Xem công nợ theo KH | Critical |

#### 4. Quản lý Đơn hàng (15 features)

| # | Feature ID | Tên tính năng | Mô tả | Độ ưu tiên |
|---|------------|---------------|-------|------------|
| 25 | ORDER-001 | Danh sách đơn hàng | Hiển thị danh sách đơn | Critical |
| 26 | ORDER-002 | Tạo đơn bán lẻ | Tạo đơn cho khách lẻ | Critical |
| 27 | ORDER-003 | Tạo đơn bán buôn | Tạo đơn cho khách sỉ | Critical |
| 28 | ORDER-004 | Tạo đơn Fitting | Đơn từ dịch vụ Fitting | High |
| 29 | ORDER-005 | Tạo đơn Coaching | Đơn từ dịch vụ Coaching | High |
| 30 | ORDER-006 | Tạo đơn Trade-in | Đơn thu cũ đổi mới | High |
| 31 | ORDER-007 | Import đơn hàng | Import đơn từ Excel | Medium |
| 32 | ORDER-008 | Xem chi tiết đơn | Xem chi tiết đơn hàng | Critical |
| 33 | ORDER-009 | Cập nhật đơn | Sửa đơn hàng | Critical |
| 34 | ORDER-010 | Kiểm tra tồn kho | Check tồn trước khi tạo đơn | Critical |
| 35 | ORDER-011 | Áp dụng voucher | Áp mã giảm giá | High |
| 36 | ORDER-012 | Sử dụng điểm | Thanh toán bằng điểm | High |
| 37 | ORDER-013 | Chọn PTTT | Tiền mặt/CK/COD | Critical |
| 38 | ORDER-014 | Tạo KH mới từ đơn | Popup tạo KH | High |
| 39 | ORDER-015 | Ghi chú đơn hàng | Ghi chú nội bộ/khách | Medium |

#### 5. Quản lý Sản phẩm (8 features)

| # | Feature ID | Tên tính năng | Mô tả | Độ ưu tiên |
|---|------------|---------------|-------|------------|
| 40 | PROD-001 | Danh sách SP | Hiển thị danh sách sản phẩm | Critical |
| 41 | PROD-002 | Tạo sản phẩm | Tạo sản phẩm mới | Critical |
| 42 | PROD-003 | Danh mục SP | Quản lý danh mục sản phẩm | Critical |
| 43 | PROD-004 | Import SP | Import SP từ Excel | High |
| 44 | PROD-005 | Export SP | Export SP ra Excel | Medium |
| 45 | PROD-006 | Xem chi tiết SP | Thông tin chi tiết SP | Critical |
| 46 | PROD-007 | Quản lý biến thể | SP có nhiều biến thể | High |
| 47 | PROD-008 | Thông tin bảo hành | Cài đặt bảo hành SP | Medium |

#### 6. Quản lý Chi nhánh (5 features)

| # | Feature ID | Tên tính năng | Mô tả | Độ ưu tiên |
|---|------------|---------------|-------|------------|
| 48 | BRANCH-001 | Danh sách chi nhánh | Hiển thị danh sách | Critical |
| 49 | BRANCH-002 | Tạo chi nhánh | Tạo chi nhánh mới | High |
| 50 | BRANCH-003 | Xem chi tiết | Thông tin chi nhánh | High |
| 51 | BRANCH-004 | Cập nhật | Sửa thông tin | High |
| 52 | BRANCH-005 | Xóa chi nhánh | Xóa chi nhánh | Medium |

#### 7. Quản lý Nhân viên (7 features)

| # | Feature ID | Tên tính năng | Mô tả | Độ ưu tiên |
|---|------------|---------------|-------|------------|
| 53 | EMP-001 | Danh sách NV | Hiển thị danh sách | Critical |
| 54 | EMP-002 | Tạo nhân viên | Tạo NV mới | Critical |
| 55 | EMP-003 | Xem chi tiết NV | Thông tin NV | High |
| 56 | EMP-004 | Cập nhật NV | Sửa thông tin | High |
| 57 | EMP-005 | Xóa NV | Xóa nhân viên | Medium |
| 58 | EMP-006 | Import NV | Import từ Excel | Medium |
| 59 | EMP-007 | Export NV | Export ra Excel | Medium |

#### 8. Cài đặt (5 features)

| # | Feature ID | Tên tính năng | Mô tả | Độ ưu tiên |
|---|------------|---------------|-------|------------|
| 60 | SET-001 | Phân công Lead | Phân công Lead cho NV | High |
| 61 | SET-002 | Tags KH | Quản lý tags khách hàng | High |
| 62 | SET-003 | Trạng thái cơ hội | Quản lý trạng thái | High |
| 63 | SET-004 | Danh sách chức vụ | Quản lý chức vụ | High |
| 64 | SET-005 | Nhóm KH | Quản lý nhóm khách hàng | High |

#### 9. Quản lý Fitting - Core (5 features)

| # | Feature ID | Tên tính năng | Mô tả | Độ ưu tiên |
|---|------------|---------------|-------|------------|
| 65 | FIT-001 | Danh sách Fitting | Danh sách đơn Fitting | Critical |
| 66 | FIT-002 | Tạo đơn Fitting | Tạo đơn Fitting mới | Critical |
| 67 | FIT-003 | Trạng thái Fitting | Workflow trạng thái | Critical |
| 68 | FIT-004 | Nhập thông số KT | Nhập thông số kỹ thuật | Critical |
| 69 | FIT-005 | Phân công NV | Gán NV Fitting | High |

#### 10. Quản lý Coaching - Core (9 features)

| # | Feature ID | Tên tính năng | Mô tả | Độ ưu tiên |
|---|------------|---------------|-------|------------|
| 70 | COACH-001 | Danh sách Coaching | Danh sách đơn | Critical |
| 71 | COACH-002 | Tạo đơn Coaching | Tạo đơn mới | Critical |
| 72 | COACH-003 | Hồ sơ học viên | Thông tin học viên | Critical |
| 73 | COACH-004 | Quản lý gói học | Các gói huấn luyện | Critical |
| 74 | COACH-005 | Quản lý HLV | Hồ sơ HLV | Critical |
| 75 | COACH-006 | Quản lý sân tập | Danh sách sân tập | High |
| 76 | COACH-007 | Bài test đầu vào | Test đánh giá | High |
| 77 | COACH-008 | Lịch học | Lên lịch buổi học | Critical |
| 78 | COACH-009 | Điểm danh | Điểm danh buổi học | Critical |

#### 11. Thu cũ Đổi mới - Core (5 features)

| # | Feature ID | Tên tính năng | Mô tả | Độ ưu tiên |
|---|------------|---------------|-------|------------|
| 79 | TI-001 | Danh sách Trade-in | Danh sách đơn | Critical |
| 80 | TI-002 | Tạo đơn Trade-in | Tạo đơn mới | Critical |
| 81 | TI-003 | Nhập SP cũ | Thông tin SP cũ | Critical |
| 82 | TI-004 | Chọn SP mới | Chọn SP thay thế | Critical |
| 83 | TI-005 | Tính chênh lệch | Tính toán giá trị | Critical |

---

### Đợt 2: Advanced Features & Operations (48 features)

#### 12. Dashboard (6 features)

| # | Feature ID | Tên tính năng | Mô tả | Độ ưu tiên |
|---|------------|---------------|-------|------------|
| 84 | DASH-001 | DS theo ngày/tuần/tháng | Biểu đồ doanh số | High |
| 85 | DASH-002 | DS bán sỉ | Doanh số bán sỉ | High |
| 86 | DASH-003 | DS bán lẻ | Doanh số bán lẻ | High |
| 87 | DASH-004 | DS theo nguồn KH | Breakdown theo nguồn | High |
| 88 | DASH-005 | DS theo nguồn đơn | Breakdown theo kênh | High |
| 89 | DASH-006 | Top 20 SP | Top sản phẩm bán chạy | High |

#### 13. Chăm sóc Khách hàng (7 features)

| # | Feature ID | Tên tính năng | Mô tả | Độ ưu tiên |
|---|------------|---------------|-------|------------|
| 90 | CSKH-001 | Lịch chăm sóc tự động | Thiết lập lịch CSKH | High |
| 91 | CSKH-002 | Gửi KM tự động | Lọc KH gửi KM | High |
| 92 | CSKH-003 | Phiếu hỗ trợ | Ticket system | High |
| 93 | CSKH-004 | Phân quyền CSKH | Gán nhóm KH cho NV | Medium |
| 94 | CSKH-005 | Khảo sát hài lòng | Form khảo sát | Medium |
| 95 | CSKH-006 | Tích hợp Zalo/Mess | Giao tiếp đa kênh | High |
| 96 | CSKH-007 | Upsell/Cross-sell | Gợi ý SP | Medium |

#### 14. Đơn hàng nâng cao (8 features)

| # | Feature ID | Tên tính năng | Mô tả | Độ ưu tiên |
|---|------------|---------------|-------|------------|
| 97 | ORDER-016 | Bảo hành | Tạo phiếu bảo hành | High |
| 98 | ORDER-017 | Xóa đơn hàng | Xóa/Hủy đơn | Medium |
| 99 | ORDER-018 | In đơn hàng | In phiếu đơn | High |
| 100 | ORDER-019 | Resell | Đề xuất mua lại | Medium |
| 101 | ORDER-020 | Export đơn | Export ra Excel | Medium |
| 102 | ORDER-021 | API tạo đơn | Expose API đơn hàng | High |
| 103 | ORDER-022 | Đồng bộ Shopee | Nhận đơn từ Shopee | High |
| 104 | ORDER-023 | Đồng bộ TikTok | Nhận đơn từ TikTok | High |

#### 15. Quản lý Bán hàng (11 features)

| # | Feature ID | Tên tính năng | Mô tả | Độ ưu tiên |
|---|------------|---------------|-------|------------|
| 105 | SALE-001 | KH bán hàng | Lập kế hoạch năm | High |
| 106 | SALE-002 | Chính sách CK | Quản lý chiết khấu | Critical |
| 107 | SALE-003 | Quản lý hàng trả | Xử lý hàng trả lại | High |
| 108 | SALE-004 | Tính thưởng DS | Tính thưởng NV | High |
| 109 | SALE-005 | Quản lý Voucher | Tạo/quản lý voucher | High |
| 110 | SALE-006 | Danh sách bảng giá | Quản lý bảng giá | Critical |
| 111 | SALE-007 | Thêm bảng giá | Tạo bảng giá mới | Critical |
| 112 | SALE-008 | Xem bảng giá | Chi tiết bảng giá | High |
| 113 | SALE-009 | Cập nhật bảng giá | Sửa bảng giá | High |
| 114 | SALE-010 | Xóa bảng giá | Xóa bảng giá | Medium |
| 115 | SALE-011 | Hạn mức công nợ | Thiết lập hạn mức | Critical |

#### 16. Quản lý Kho (3 features)

| # | Feature ID | Tên tính năng | Mô tả | Độ ưu tiên |
|---|------------|---------------|-------|------------|
| 116 | WH-001 | Danh sách kho | Hiển thị danh sách kho | Critical |
| 117 | WH-002 | Tạo kho | Tạo kho mới | High |
| 118 | WH-003 | Xem chi tiết kho | Tồn kho trong kho | Critical |

#### 17. Quản lý Giao vận (2 features)

| # | Feature ID | Tên tính năng | Mô tả | Độ ưu tiên |
|---|------------|---------------|-------|------------|
| 119 | SHIP-001 | Danh sách giao vận | Danh sách đơn ship | High |
| 120 | SHIP-002 | Liên kết Viettel Post | Tạo đơn, tracking | Critical |

#### 18. Fitting - Tích hợp (4 features)

| # | Feature ID | Tên tính năng | Mô tả | Độ ưu tiên |
|---|------------|---------------|-------|------------|
| 121 | FIT-006 | Tạo SO từ Fitting | Tạo đơn từ Fitting | High |
| 122 | FIT-007 | Tích hợp Website | API nhận đăng ký | High |
| 123 | FIT-008 | Báo cáo Fitting | Các báo cáo Fitting | High |
| 124 | FIT-009 | Dashboard Fitting | Widget Fitting | Medium |

#### 19. Coaching - Tích hợp (4 features)

| # | Feature ID | Tên tính năng | Mô tả | Độ ưu tiên |
|---|------------|---------------|-------|------------|
| 125 | COACH-010 | Tạo SO từ Coaching | Tạo đơn thanh toán | High |
| 126 | COACH-011 | Thông báo tự động | Nhắc lịch học | High |
| 127 | COACH-012 | Báo cáo Coaching | Các báo cáo | High |
| 128 | COACH-013 | Dashboard Coaching | Widget Coaching | Medium |

#### 20. Trade-in - Tích hợp (3 features)

| # | Feature ID | Tên tính năng | Mô tả | Độ ưu tiên |
|---|------------|---------------|-------|------------|
| 129 | TI-006 | Quy trình định giá | Kiểm tra & định giá | High |
| 130 | TI-007 | Tích hợp kho | Nhập/Xuất kho tự động | High |
| 131 | TI-008 | Báo cáo Trade-in | Các báo cáo | High |

---

### Đợt 3: Reports & Security (13 features)

#### 21. Role & Permission (4 features)

| # | Feature ID | Tên tính năng | Mô tả | Độ ưu tiên |
|---|------------|---------------|-------|------------|
| 132 | ROLE-001 | Danh sách Role | Hiển thị danh sách | Critical |
| 133 | ROLE-002 | Tạo Role | Tạo role mới | Critical |
| 134 | ROLE-003 | Cập nhật Role | Sửa quyền role | Critical |
| 135 | ROLE-004 | Xóa Role | Xóa role | Medium |

#### 22. Báo cáo (5 features)

| # | Feature ID | Tên tính năng | Mô tả | Độ ưu tiên |
|---|------------|---------------|-------|------------|
| 136 | RPT-001 | BC Doanh số | Báo cáo doanh số | Critical |
| 137 | RPT-002 | BC Đơn hàng | Báo cáo đơn hàng | Critical |
| 138 | RPT-003 | BC Khách hàng | Báo cáo khách hàng | High |
| 139 | RPT-004 | BC Nhân viên | Báo cáo nhân viên | High |
| 140 | RPT-005 | BC Kho | Báo cáo kho | High |

#### 23. Web Analytics (4 features)

| # | Feature ID | Tên tính năng | Mô tả | Độ ưu tiên |
|---|------------|---------------|-------|------------|
| 141 | WEB-001 | Lượt truy cập | Tracking lượt truy cập | Medium |
| 142 | WEB-002 | Heatmap | Bản đồ nhiệt | Medium |
| 143 | WEB-003 | Phân tích Data | PageView, Event | Medium |
| 144 | WEB-004 | Tối ưu | Recording không ảnh hưởng | Medium |

---

## PHASE 2: ERP (102 Features)

### Đợt 1: Quản lý Bán hàng + Mua hàng (38 features)

#### 24. Bán hàng - Bán buôn (12 features)

| # | Feature ID | Tên tính năng | Mô tả | Độ ưu tiên |
|---|------------|---------------|-------|------------|
| 145 | ERP-SALE-001 | Kế hoạch bán hàng | Lập KH theo năm | High |
| 146 | ERP-SALE-002 | Bảng giá niêm yết | Cập nhật giá | Critical |
| 147 | ERP-SALE-003 | CS chiết khấu sỉ | Chiết khấu theo KH | Critical |
| 148 | ERP-SALE-004 | Đơn đặt hàng bán | Tạo đơn hàng bán | Critical |
| 149 | ERP-SALE-005 | Kiểm tra tồn kho | Check trước khi bán | Critical |
| 150 | ERP-SALE-006 | Lệnh xuất hàng | Chuyển cho kho | Critical |
| 151 | ERP-SALE-007 | Kiểm tra hạn mức | Check hạn mức CN | Critical |
| 152 | ERP-SALE-008 | KT công nợ quá hạn | Check HĐ quá hạn | Critical |
| 153 | ERP-SALE-009 | Hóa đơn bán buôn | Xuất hóa đơn | Critical |
| 154 | ERP-SALE-010 | Lệnh nhập trả | Xử lý hàng trả | High |
| 155 | ERP-SALE-011 | Hàng bán trả lại | Ghi nhận trả lại | High |
| 156 | ERP-SALE-012 | Tính thưởng DS | Tính khi đạt KH | High |

#### 25. Bán hàng - Bán lẻ (3 features)

| # | Feature ID | Tên tính năng | Mô tả | Độ ưu tiên |
|---|------------|---------------|-------|------------|
| 157 | ERP-SALE-013 | Bảng giá lẻ | Giá bán lẻ | Critical |
| 158 | ERP-SALE-014 | CS chiết khấu lẻ | Chiết khấu lẻ | High |
| 159 | ERP-SALE-015 | Hóa đơn bán lẻ | POS bán hàng | Critical |

#### 26. Danh mục Bán hàng (3 features)

| # | Feature ID | Tên tính năng | Mô tả | Độ ưu tiên |
|---|------------|---------------|-------|------------|
| 160 | ERP-SALE-016 | Danh mục KH | Quản lý khách hàng | Critical |
| 161 | ERP-SALE-017 | Danh mục VTHH | Quản lý sản phẩm | Critical |
| 162 | ERP-SALE-018 | KH doanh số năm | Kế hoạch DS | High |

#### 27. Quản lý Mua hàng (20 features)

| # | Feature ID | Tên tính năng | Mô tả | Độ ưu tiên |
|---|------------|---------------|-------|------------|
| 163 | ERP-PURCH-001 | Danh mục NCC | Quản lý NCC | Critical |
| 164 | ERP-PURCH-002 | Bảng giá NCC | Giá mua từ NCC | High |
| 165 | ERP-PURCH-003 | Ưu đãi NCC | CK%, tiền, quà | High |
| 166 | ERP-PURCH-004 | Import hình ảnh | Import ảnh SP | High |
| 167 | ERP-PURCH-005 | Tạo PO | Tạo Purchase Order | Critical |
| 168 | ERP-PURCH-006 | Chi tiết PO | Model, SKU, SL | Critical |
| 169 | ERP-PURCH-007 | Theo dõi PO | Trạng thái PO | Critical |
| 170 | ERP-PURCH-008 | Lệnh nhập hàng | Sinh từ PO | Critical |
| 171 | ERP-PURCH-009 | Theo dõi mua hàng | % đã nhận | High |
| 172 | ERP-PURCH-010 | Nhập theo lô | Mã lô | High |
| 173 | ERP-PURCH-011 | Nhập theo serial | Serial duy nhất | High |
| 174 | ERP-PURCH-012 | Nhập theo barcode | Quét mã vạch | High |
| 175 | ERP-PURCH-013 | Vòng đời SP | 6 tháng/1 năm | Medium |
| 176 | ERP-PURCH-014 | Nguồn tiền | Quỹ TM/TK bank | High |
| 177 | ERP-PURCH-015 | PT thanh toán | TM/CK/Công nợ | Critical |
| 178 | ERP-PURCH-016 | Theo dõi TT PO | Đã TT / Còn nợ | Critical |
| 179 | ERP-PURCH-017 | Đính kèm CT | HĐ, phiếu GH | High |
| 180 | ERP-PURCH-018 | Trạng thái nhập | Nháp/Duyệt/Nhập | Critical |
| 181 | ERP-PURCH-019 | Lịch sử mua | Theo NCC/PO/SP | High |
| 182 | ERP-PURCH-020 | BC mua hàng | Giá BQ, NCC tốt | High |

---

### Đợt 2: Quản lý Kho + Kế toán (44 features)

#### 28. Quản lý Kho (20 features)

| # | Feature ID | Tên tính năng | Mô tả | Độ ưu tiên |
|---|------------|---------------|-------|------------|
| 183 | ERP-WH-001 | Tồn kho đầu kỳ | Nhập tồn ban đầu | Critical |
| 184 | ERP-WH-002 | Phiếu nhập mua | Nhập từ NCC | Critical |
| 185 | ERP-WH-003 | Phiếu nhập khẩu | Nhập khẩu | Critical |
| 186 | ERP-WH-004 | Phiếu nhập khác | Nhập điều chỉnh | High |
| 187 | ERP-WH-005 | Phiếu xuất bán | Xuất cho KH | Critical |
| 188 | ERP-WH-006 | Phiếu xuất khác | Xuất điều chỉnh | High |
| 189 | ERP-WH-007 | Phiếu điều chuyển | Chuyển kho | High |
| 190 | ERP-WH-008 | Phiếu xuất trả NCC | Trả hàng NCC | High |
| 191 | ERP-WH-009 | Quản lý lô | Theo dõi theo lô | High |
| 192 | ERP-WH-010 | Quản lý serial | Theo dõi serial | High |
| 193 | ERP-WH-011 | Quản lý vị trí | Vị trí trong kho | High |
| 194 | ERP-WH-012 | Reserve stock | Giữ hàng theo đơn | Critical |
| 195 | ERP-WH-013 | Gán barcode | Gán mã vạch SP | High |
| 196 | ERP-WH-014 | Tạo tem nhãn | Template tem | High |
| 197 | ERP-WH-015 | In tem hàng loạt | In batch | High |
| 198 | ERP-WH-016 | Kiểm kê | Tạo phiếu kiểm kê | High |
| 199 | ERP-WH-017 | Xử lý chênh lệch | Điều chỉnh kho | High |
| 200 | ERP-WH-018 | BC tồn kho | Báo cáo tồn | Critical |
| 201 | ERP-WH-019 | BC giá trị tồn | Giá trị tồn kho | High |
| 202 | ERP-WH-020 | Cảnh báo tồn | Dưới định mức | High |

#### 29. Quản lý Kế toán (20 features)

| # | Feature ID | Tên tính năng | Mô tả | Độ ưu tiên |
|---|------------|---------------|-------|------------|
| 203 | ERP-ACC-001 | Phiếu thu | Thu tiền từ KH | Critical |
| 204 | ERP-ACC-002 | Phiếu chi | Chi tiền cho NCC | Critical |
| 205 | ERP-ACC-003 | Báo có | NH báo có | High |
| 206 | ERP-ACC-004 | Báo nợ | NH báo nợ | High |
| 207 | ERP-ACC-005 | Công nợ phải thu | AR aging | Critical |
| 208 | ERP-ACC-006 | Công nợ phải trả | AP aging | Critical |
| 209 | ERP-ACC-007 | Đối chiếu CN | Đối chiếu với KH/NCC | High |
| 210 | ERP-ACC-008 | Hóa đơn bán | Xuất hóa đơn | Critical |
| 211 | ERP-ACC-009 | Hóa đơn mua | Nhận hóa đơn | Critical |
| 212 | ERP-ACC-010 | Sổ cái | General Ledger | Critical |
| 213 | ERP-ACC-011 | Sổ nhật ký | Journal Entry | Critical |
| 214 | ERP-ACC-012 | Bút toán điều chỉnh | Adjustment | High |
| 215 | ERP-ACC-013 | Kế toán TSCĐ | Fixed Assets | High |
| 216 | ERP-ACC-014 | Khấu hao TSCĐ | Depreciation | High |
| 217 | ERP-ACC-015 | Kế toán thuế | VAT, CIT | Critical |
| 218 | ERP-ACC-016 | Chi phí hỗ trợ hãng | Brand support | High |
| 219 | ERP-ACC-017 | Chi phí sự kiện | Event costing | High |
| 220 | ERP-ACC-018 | BC tài chính | P&L, BS | Critical |
| 221 | ERP-ACC-019 | BC dòng tiền | Cash flow | High |
| 222 | ERP-ACC-020 | Đề nghị thanh toán | Payment request | High |

#### 30. Báo cáo Kho (5 features)

| # | Feature ID | Tên tính năng | Mô tả | Độ ưu tiên |
|---|------------|---------------|-------|------------|
| 223 | ERP-WH-021 | BC nhập xuất tồn | Inventory movement | Critical |
| 224 | ERP-WH-022 | BC theo lô | Batch report | High |
| 225 | ERP-WH-023 | BC theo serial | Serial report | High |
| 226 | ERP-WH-024 | BC theo vị trí | Location report | Medium |
| 227 | ERP-WH-025 | BC giá nhập XBQ | Average cost | High |

---

### Đợt 3: Báo cáo + Kết nối Web (20 features)

#### 31. Báo cáo Tổng hợp (10 features)

| # | Feature ID | Tên tính năng | Mô tả | Độ ưu tiên |
|---|------------|---------------|-------|------------|
| 228 | ERP-RPT-001 | BC bán hàng | Sales report | Critical |
| 229 | ERP-RPT-002 | BC mua hàng | Purchase report | Critical |
| 230 | ERP-RPT-003 | BC công nợ | AR/AP report | Critical |
| 231 | ERP-RPT-004 | BC lãi gộp | Gross profit | High |
| 232 | ERP-RPT-005 | BC theo NV | Staff report | High |
| 233 | ERP-RPT-006 | BC theo KH | Customer report | High |
| 234 | ERP-RPT-007 | BC theo NCC | Supplier report | High |
| 235 | ERP-RPT-008 | BC so sánh | Comparison report | High |
| 236 | ERP-RPT-009 | BC chi phí | Cost report | High |
| 237 | ERP-RPT-010 | BC tổng hợp | Consolidated report | High |

#### 32. Kết nối Web (5 features)

| # | Feature ID | Tên tính năng | Mô tả | Độ ưu tiên |
|---|------------|---------------|-------|------------|
| 238 | ERP-WEB-001 | Đồng bộ DM KH | Sync customers | High |
| 239 | ERP-WEB-002 | Đồng bộ DM SP | Sync products | High |
| 240 | ERP-WEB-003 | Đồng bộ kho | Sync warehouse | High |
| 241 | ERP-WEB-004 | Đồng bộ đơn hàng | Sync orders | Critical |
| 242 | ERP-WEB-005 | Đồng bộ tồn kho | Sync stock | Critical |

#### 33. Quy trình Nhập khẩu (5 features)

| # | Feature ID | Tên tính năng | Mô tả | Độ ưu tiên |
|---|------------|---------------|-------|------------|
| 243 | ERP-IMP-001 | Lịch đặt hàng | 7 loại SP | High |
| 244 | ERP-IMP-002 | Pre-order | Đơn đặt trước | High |
| 245 | ERP-IMP-003 | KH giao hàng | Delivery schedule | High |
| 246 | ERP-IMP-004 | Thủ tục hải quan | Customs | High |
| 247 | ERP-IMP-005 | BC so sánh KH-TH | Plan vs Actual | High |

---

## TỔNG HỢP THEO PHASE

### Phase 1: CRM

| Đợt | Thời gian | Modules | Features |
|-----|-----------|---------|----------|
| Đợt 1 | 50 ngày | 11 | 74 |
| Đợt 2 | 30 ngày | 9 | 48 |
| Đợt 3 | 10 ngày | 3 | 13 |
| **Tổng** | **90 ngày** | **23** | **135** |

### Phase 2: ERP

| Đợt | Thời gian | Modules | Features |
|-----|-----------|---------|----------|
| Đợt 1 | 30 ngày | 5 | 38 |
| Đợt 2 | 45 ngày | 12 | 44 |
| Đợt 3 | 15 ngày | 6 | 20 |
| **Tổng** | **90 ngày** | **23** | **102** |

### Grand Total

| Phase | Duration | Modules | Features |
|-------|----------|---------|----------|
| Phase 1 (CRM) | 90 ngày | 23 | 135 |
| Phase 2 (ERP) | 90 ngày | 23 | 102 |
| **TỔNG CỘNG** | **180 ngày** | **46** | **237** |

---

**© 2026 DCNET Corporation**
