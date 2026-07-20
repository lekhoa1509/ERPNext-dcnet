# Đặc tả Use Cases - Module Quản lý Kho

**Dự án:** DCNET Flow - Nhật Minh Sports
**Module:** Warehouse Management
**Phiên bản:** 1.0
**Nguồn:** ERP_SPECIFICATION.md (Section 4)
**Ngày:** 15/01/2026

---

## 📋 Mục lục

1. [Định nghĩa Module Kho](#1-định-nghĩa-module-kho)
2. [Danh sách Actors và Vai trò](#2-danh-sách-actors-và-vai-trò)
3. [Ma trận Phân quyền](#3-ma-trận-phân-quyền)
4. [Chi tiết Use Cases](#4-chi-tiết-use-cases)
5. [Use Case Diagram](#5-use-case-diagram)

---

## 1. Định nghĩa Module Kho

> **Định nghĩa từ khách hàng:**
>
> Quản lý nhập/xuất/tồn kho theo mã số, kho, lô, vị trí, Serial. Theo dõi nhập/xuất/tồn theo mã vạch. Trừ tồn kho khả dụng (giữ theo đơn hàng). Tạo tem và in tem trên hệ thống.

**Đặc điểm:**
- Quản lý kho theo mã vạch, lô, serial
- Kiểm soát tồn kho khả dụng
- Quy trình kiểm kê định kỳ
- Tính giá vốn theo phương pháp trung bình tháng
- Phân quyền: Ẩn giá với nhân viên kho

**Nguồn:** ERP_SPECIFICATION.md Section 4 (lines 455-641)

---

## 2. Danh sách Actors và Vai trò

### 2.1. Warehouse Manager (Trưởng kho)

**Mô tả:** Quản lý kho, phụ trách toàn bộ hoạt động kho

**Quyền hạn:**
- Xem tất cả phiếu nhập/xuất/điều chuyển
- Duyệt phiếu xuất kho (approval workflow)
- Quản lý danh mục kho, vị trí kho
- Lập lệnh kiểm kê
- Xem giá vốn hàng hóa

---

### 2.2. Warehouse User (Thủ kho)

**Mô tả:** Nhân viên kho thực hiện thao tác nhập/xuất/kiểm kê

**Quyền hạn:**
- Tạo phiếu nhập kho
- Tạo phiếu xuất kho (cần duyệt)
- Tạo phiếu điều chuyển kho
- Tạo phiếu điều chuyển vị trí
- Thực hiện kiểm kê
- Quản lý danh mục lô hàng
- In tem mã vạch

**Giới hạn:**
- **KHÔNG xem được đơn giá, thành tiền**
- **KHÔNG sửa thông tin khách hàng, mặt hàng, số lượng yêu cầu trên lệnh xuất**
- Chỉ cập nhật thông tin thực xuất (seri, lô, kho, số lượng)

---

### 2.3. Accountant (Kế toán)

**Mô tả:** Kế toán viên xử lý chứng từ kho, tính giá vốn

**Quyền hạn:**
- Xem tất cả phiếu kho
- Tạo phiếu nhập mua, phiếu nhập khẩu
- Xử lý phiếu chênh lệch kiểm kê
- Tính giá vốn hàng xuất
- Cập nhật tồn kho đầu kỳ
- Xem báo cáo nhập/xuất/tồn

---

### 2.4. Chief Accountant (Kế toán trưởng)

**Mô tả:** Kế toán trưởng, phụ trách duyệt các giao dịch ngoại lệ

**Quyền hạn:**
- Tất cả quyền của Accountant
- **Duyệt phiếu xuất khi khách hàng vi phạm công nợ** (ngoại lệ)
- Duyệt xử lý chênh lệch kiểm kê
- Khóa sổ kho định kỳ

---

### 2.5. Sales Executive (Nhân viên kinh doanh)

**Mô tả:** Nhân viên kinh doanh tạo lệnh xuất kho

**Quyền hạn:**
- Tạo lệnh xuất kho nội bộ
- Xem trạng thái tồn kho (không xem giá)
- Kiểm tra công nợ khách hàng trước khi xuất

**Giới hạn:**
- Không xem giá vốn hàng hóa

---

## 3. Ma trận Phân quyền

| Use Case | Warehouse Manager | Warehouse User | Accountant | Chief Accountant | Sales Executive |
| --- | --- | --- | --- | --- | --- |
| **UC-W01: Cập nhật tồn kho đầu kỳ** | ✓ | - | ✓ | ✓ | - |
| **UC-W02: Nhập hàng vào kho** | ✓ | ✓ | - | - | - |
| **UC-W03: Xuất hàng từ kho** | ✓ (approve) | ✓ (create) | - | ✓ (approve ngoại lệ) | ✓ (create) |
| **UC-W04: Xuất CCDC** | ✓ | ✓ | - | - | - |
| **UC-W05: Điều chuyển giữa các kho** | ✓ | ✓ | - | - | - |
| **UC-W06: Điều chuyển vị trí trong kho** | ✓ | ✓ | - | - | - |
| **UC-W07: Lập lệnh kiểm kê** | ✓ | - | ✓ | ✓ | - |
| **UC-W08: Thực hiện kiểm kê** | ✓ | ✓ | - | - | - |
| **UC-W09: Xử lý chênh lệch kiểm kê** | ✓ | - | ✓ | ✓ | - |
| **UC-W10: Tính giá vốn hàng xuất** | - | - | ✓ | ✓ | - |
| **UC-W11: Quản lý danh mục lô hàng** | ✓ | ✓ | - | - | - |
| **UC-W12: In tem mã vạch** | ✓ | ✓ | - | - | - |
| **UC-W13: Xuất nội bộ giữa cửa hàng** | ✓ | ✓ | - | - | ✓ |
| **UC-W14: Quản lý hàng ký gửi** | ✓ | ✓ | ✓ | ✓ | - |
| **UC-W15: Kiểm tra công nợ trước xuất hàng** | - | - | - | ✓ (approve) | ✓ (check) |

**Chú thích:**
- ✓ = Có quyền thực hiện
- ✓ (create) = Tạo mới (cần duyệt)
- ✓ (approve) = Duyệt phiếu
- ✓ (check) = Chỉ kiểm tra, không duyệt
- ✓ (approve ngoại lệ) = Duyệt khi vi phạm điều kiện công nợ
- - = Không có quyền

**Field-level Permissions:**

| Field | Warehouse Manager | Warehouse User | Accountant | Chief Accountant | Sales Executive |
| --- | --- | --- | --- | --- | --- |
| **Đơn giá** | ✓ | ✗ | ✓ | ✓ | ✗ |
| **Thành tiền** | ✓ | ✗ | ✓ | ✓ | ✗ |
| **Giá vốn** | ✓ | ✗ | ✓ | ✓ | ✗ |
| **Số lượng** | ✓ | ✓ (read-only on order) | ✓ | ✓ | ✓ |
| **Seri/Lô** | ✓ | ✓ | ✓ | ✓ | ✗ |

**Nguồn:** ERP_SPECIFICATION.md Section 2 (lines 126-128)

---

## 4. Chi tiết Use Cases

### UC-W01: Cập nhật tồn kho đầu kỳ

**ID:** UC-W01
**Tên:** Cập nhật tồn kho đầu kỳ
**Actors:** Warehouse Manager, Accountant, Chief Accountant

**Mô tả:**
Cập nhật số lượng, giá trị tồn kho đầu kỳ vào hệ thống khi bắt đầu sử dụng hoặc chuyển năm kế toán.

**Precondition:**
- User đã đăng nhập vào hệ thống
- Có quyền cập nhật tồn kho đầu kỳ
- Chưa có giao dịch phát sinh trong kỳ

**Main Flow:**
1. User chọn "Tồn kho đầu kỳ"
2. Hệ thống hiển thị form nhập liệu
3. User nhập thông tin:
  - Kỳ kế toán
  - Kho
  - Danh sách vật tư
4. User nhập chi tiết cho từng vật tư:
  - Mã vật tư
  - Tên vật tư
  - Số lượng tồn
  - Số lô/seri (nếu có)
  - Giá trị (Accountant)
5. User submit form
6. Hệ thống lưu tồn kho đầu kỳ

**Postcondition:**
- Tồn kho đầu kỳ được ghi nhận
- Báo cáo tồn kho hiển thị đúng số liệu

**Business Rules:**
- Chỉ thực hiện lần đầu sử dụng hệ thống
- Các năm tiếp theo dùng chức năng "Kết chuyển tồn kho"
- Không được sửa sau khi có phát sinh

**Nguồn:** ERP_SPECIFICATION.md Section 4.1 (lines 460-467)

---

### UC-W02: Nhập hàng vào kho

**ID:** UC-W02
**Tên:** Nhập hàng vào kho
**Actors:** Warehouse Manager, Warehouse User

**Mô tả:**
Ghi nhận hàng hóa nhập kho dựa trên nhu cầu vật tư của các bộ phận khác.

**Precondition:**
- User đã đăng nhập vào hệ thống
- Có quyền tạo phiếu nhập kho
- Có lệnh nhập/đơn hàng/yêu cầu nhập kho

**Main Flow:**
1. User chọn "Tạo phiếu nhập kho"
2. Hệ thống hiển thị form nhập liệu
3. User nhập **Thông tin chung:**
  - Ngày nhập
  - Số phiếu (auto)
  - Người lập (auto-fill)
  - Nội dung
  - Nhà cung cấp
  - Tiền tệ
  - Kho nhập
4. User nhập **Thông tin chi tiết:**
  - Mã vật tư
  - Tên vật tư
  - Số lượng
  - Đơn giá (hidden cho Warehouse User)
  - Thành tiền (hidden cho Warehouse User)
  - Số lô
  - Seri
  - Số đơn hàng (nếu có)
5. User submit form
6. Hệ thống tạo phiếu nhập kho
7. Hệ thống cập nhật tồn kho

**Postcondition:**
- Phiếu nhập kho được tạo
- Tồn kho tăng theo số lượng nhập
- Log hoạt động được ghi nhận

**Business Rules:**
- Số phiếu tự động sinh
- Warehouse User không xem được giá
- Có thể kế thừa từ đơn đặt hàng

**Nguồn:** ERP_SPECIFICATION.md Section 4.2 (lines 469-481)

---

### UC-W03: Xuất hàng từ kho

**ID:** UC-W03
**Tên:** Xuất hàng từ kho (với approval workflow)
**Actors:** Warehouse Manager (approve), Warehouse User (create), Chief Accountant (approve ngoại lệ), Sales Executive (create)

**Mô tả:**
Tạo phiếu xuất kho dựa trên lệnh xuất hàng. Có quy trình duyệt với kiểm tra công nợ.

**Precondition:**
- User đã đăng nhập vào hệ thống
- Có quyền tạo/duyệt phiếu xuất kho
- Có lệnh xuất hàng hợp lệ
- Tồn kho đủ để xuất

**Main Flow:**
1. User chọn "Tạo phiếu xuất kho"
2. Hệ thống hiển thị form
3. User chọn lệnh xuất hàng cần xử lý
4. Hệ thống kế thừa thông tin từ lệnh xuất
5. **Hệ thống kiểm tra công nợ khách hàng** (UC-W15)
6. User cập nhật **Thông tin thực xuất:**
  - Kho xuất
  - Số lượng thực xuất
  - Số lô
  - Seri
  - Vị trí kho
7. User submit form
8. Hệ thống tạo phiếu xuất (trạng thái: Draft)
9. **Warehouse Manager duyệt phiếu xuất**
10. Hệ thống cập nhật tồn kho (trạng thái: Submitted)

**Alternative Flow 1 (Vi phạm công nợ):**
- 5a. Hệ thống phát hiện vi phạm công nợ:
  - Có hóa đơn quá hạn
  - Hoặc giá trị công nợ hiện tại + lệnh xuất đã duyệt + lệnh xuất hiện tại > hạn mức
- 5b. Hệ thống hiển thị cảnh báo
- 5c. **Chief Accountant phải xác nhận** để phiếu xuất hợp lệ
- 5d. Continue main flow

**Alternative Flow 2 (Không đủ tồn kho):**
- 6a. Hệ thống phát hiện tồn kho không đủ
- 6b. Hệ thống hiển thị cảnh báo
- 6c. User điều chỉnh số lượng hoặc hủy phiếu

**Postcondition:**
- Phiếu xuất kho được tạo và duyệt
- Tồn kho giảm theo số lượng xuất
- Lệnh xuất hàng được cập nhật trạng thái
- Log hoạt động được ghi nhận

**Business Rules:**
- Warehouse User không được sửa thông tin khách hàng, mặt hàng, số lượng yêu cầu
- Chỉ cập nhật thông tin thực xuất (seri, lô, kho, số lượng)
- Phiếu xuất cần duyệt mới ảnh hưởng tồn kho
- Kiểm tra công nợ trước khi xuất (UC-W15)

**Nguồn:** ERP_SPECIFICATION.md Section 2.7 (lines 126-162), Section 4.3-5 (line 483)

---

### UC-W04: Xuất CCDC

**ID:** UC-W04
**Tên:** Xuất công cụ dụng cụ (CCDC)
**Actors:** Warehouse Manager, Warehouse User

**Mô tả:**
Ghi nhận CCDC xuất kho dựa trên nhu cầu sử dụng của các bộ phận khác, theo dõi và khai báo phân bổ CCDC hàng tháng.

**Precondition:**
- User đã đăng nhập vào hệ thống
- Có quyền xuất CCDC
- Có nhu cầu sử dụng CCDC từ các bộ phận

**Main Flow:**
1. User chọn "Tạo phiếu xuất CCDC"
2. Hệ thống hiển thị form
3. User nhập **Thông tin chung:**
  - Ngày xuất
  - Số phiếu (auto)
  - Người lập (auto-fill)
  - Nội dung
  - Kho xuất
4. User nhập **Thông tin chi tiết:**
  - Mã hàng
  - Tên hàng
  - Số lượng
  - **Số tháng phân bổ**
  - **Tài khoản nợ phân bổ**
  - **Tài khoản có phân bổ**
  - Mã tăng giảm
  - Đơn giá
  - Thành tiền
5. User submit form
6. Hệ thống tạo phiếu xuất CCDC
7. Hệ thống cập nhật tồn kho
8. Hệ thống tạo lịch phân bổ hàng tháng

**Postcondition:**
- Phiếu xuất CCDC được tạo
- Tồn kho CCDC giảm
- Lịch phân bổ được tạo cho kế toán

**Business Rules:**
- CCDC được phân bổ theo tháng
- Tự động tạo bút toán kế toán phân bổ

**Nguồn:** ERP_SPECIFICATION.md Section 4.6 (lines 487-499)

---

### UC-W05: Điều chuyển giữa các kho

**ID:** UC-W05
**Tên:** Điều chuyển hàng giữa các kho
**Actors:** Warehouse Manager, Warehouse User

**Mô tả:**
Ghi nhận điều chuyển hàng hóa giữa các kho dựa trên yêu cầu điều chuyển kho của các bộ phận khác.

**Precondition:**
- User đã đăng nhập vào hệ thống
- Có quyền tạo phiếu điều chuyển
- Tồn kho xuất đủ để điều chuyển

**Main Flow:**
1. User chọn "Tạo phiếu điều chuyển kho"
2. Hệ thống hiển thị form
3. User chọn lệnh xuất kho nội bộ (nếu có)
4. Hệ thống kế thừa dữ liệu từ lệnh
5. User nhập **Thông tin chung:**
  - Ngày điều chuyển
  - Số phiếu (auto)
  - Người lập (auto-fill)
  - Nội dung
  - **Kho xuất**
  - **Kho nhập**
6. User nhập **Thông tin chi tiết:**
  - Mã vật tư
  - Tên vật tư
  - Số lượng
  - Số lô
  - Số seri
7. User submit form
8. Hệ thống tạo phiếu điều chuyển
9. Hệ thống giảm tồn kho xuất
10. Hệ thống tăng tồn kho nhập

**Alternative Flow (Điều chuyển qua kho trung gian):**
- 1a. Đơn vị có nhu cầu nhận hàng tạo lệnh xuất kho nội bộ
- 1b. Đơn vị xuất làm phiếu xuất điều chuyển từ kho đơn vị xuất sang **kho trung gian**
- 1c. Đơn vị nhận làm phiếu xuất điều chuyển từ **kho trung gian** về kho của đơn vị nhận

**Postcondition:**
- Phiếu điều chuyển được tạo
- Tồn kho xuất giảm
- Tồn kho nhập tăng
- Log hoạt động được ghi nhận

**Business Rules:**
- Kế thừa dữ liệu từ đề nghị xuất kho nội bộ
- Đơn vị có nhu cầu nhận hàng chủ động làm lệnh
- Điều chuyển giữa chi nhánh qua kho trung gian

**Nguồn:** ERP_SPECIFICATION.md Section 4.7 (lines 501-520)

---

### UC-W06: Điều chuyển vị trí trong kho

**ID:** UC-W06
**Tên:** Điều chuyển vị trí hàng hóa trong kho
**Actors:** Warehouse Manager, Warehouse User

**Mô tả:**
Ghi nhận điều chuyển vị trí hàng hóa vật tư trong cùng một kho để tối ưu hóa quản lý không gian kho.

**Precondition:**
- User đã đăng nhập vào hệ thống
- Có quyền tạo phiếu điều chuyển vị trí
- Hàng hóa đang tồn tại trong kho

**Main Flow:**
1. User chọn "Tạo phiếu điều chuyển vị trí"
2. Hệ thống hiển thị form
3. User nhập:
  - Ngày điều chuyển
  - Số phiếu (auto)
  - Kho
  - Mã vật tư
  - Số lô/seri
  - **Vị trí hiện tại**
  - **Vị trí mới**
  - Số lượng
4. User submit form
5. Hệ thống cập nhật vị trí hàng hóa

**Postcondition:**
- Phiếu điều chuyển vị trí được tạo
- Vị trí hàng hóa được cập nhật
- Tồn kho không thay đổi (cùng kho)

**Business Rules:**
- Chỉ điều chuyển trong cùng một kho
- Không ảnh hưởng tồn kho
- Theo dõi lịch sử di chuyển hàng hóa

**Nguồn:** ERP_SPECIFICATION.md Section 4.8 (lines 522-530)

---

### UC-W07: Lập lệnh kiểm kê

**ID:** UC-W07
**Tên:** Lập lệnh kiểm kê kho
**Actors:** Warehouse Manager, Accountant, Chief Accountant

**Mô tả:**
Kế toán gửi yêu cầu kiểm kê cho bộ phận kho để chốt số tồn kho và tiến hành kiểm kê thực tế.

**Precondition:**
- User đã đăng nhập vào hệ thống
- Có quyền lập lệnh kiểm kê

**Main Flow:**
1. Accountant chọn "Tạo lệnh kiểm kê"
2. Hệ thống hiển thị form
3. Accountant nhập:
  - Ngày kiểm kê
  - Kho cần kiểm kê
  - Danh mục vật tư (tất cả/theo nhóm)
  - Người thực hiện kiểm kê
  - Ghi chú
4. Accountant submit form
5. Hệ thống tạo lệnh kiểm kê
6. Hệ thống chốt số tồn kho tại thời điểm tạo lệnh
7. Hệ thống gửi thông báo cho Warehouse Manager
8. **Bộ phận kho dừng hoạt động nhập xuất kho**

**Postcondition:**
- Lệnh kiểm kê được tạo
- Số tồn kho được chốt
- Kho tạm dừng nhập/xuất
- Warehouse User nhận được task kiểm kê

**Business Rules:**
- Kho phải dừng hoạt động nhập xuất trong thời gian kiểm kê
- Chốt số tồn kho trên hệ thống làm cơ sở đối chiếu
- Kiểm kê định kỳ hoặc đột xuất

**Nguồn:** ERP_SPECIFICATION.md Section 4.9 (lines 532-540)

---

### UC-W08: Thực hiện kiểm kê

**ID:** UC-W08
**Tên:** Thực hiện kiểm kê thực tế
**Actors:** Warehouse Manager, Warehouse User

**Mô tả:**
Thủ kho thực hiện kiểm kê lại vật tư hàng hóa, thành phẩm tại các kho và cập nhật số liệu thực tế vào phiếu kiểm kê.

**Precondition:**
- User đã đăng nhập vào hệ thống
- Có quyền thực hiện kiểm kê
- Đã có lệnh kiểm kê (UC-W07)
- Kho đã dừng hoạt động nhập xuất

**Main Flow:**
1. Warehouse User chọn "Phiếu kiểm kê"
2. Hệ thống hiển thị lệnh kiểm kê đang chờ
3. Warehouse User chọn lệnh kiểm kê cần thực hiện
4. Hệ thống hiển thị danh sách vật tư với **số tồn trên hệ thống**
5. Warehouse User thực hiện kiểm đếm thực tế
6. Warehouse User nhập **số tồn thực tế** cho từng vật tư:
  - Mã hàng
  - Đơn vị tính
  - Số lượng sổ sách
  - **Số lượng thực tế**
  - Lô/lot
  - Serial
7. Hệ thống tự động tính **chênh lệch** = Thực tế - Sổ sách
8. Warehouse User submit phiếu
9. Hệ thống lưu phiếu kiểm kê
10. Hệ thống gửi phiếu cho Accountant xử lý (UC-W09)

**Postcondition:**
- Phiếu kiểm kê được hoàn thành
- Chênh lệch được tính toán tự động
- Accountant nhận được task xử lý chênh lệch

**Business Rules:**
- Căn cứ vào tồn kho thực tế để nhập liệu
- Kiểm kê từng kho, từng vật tư, từng thuộc tính (lô, serial)
- Hệ thống tự động tính chênh lệch

**Nguồn:** ERP_SPECIFICATION.md Section 4.10 (lines 542-554)

---

### UC-W09: Xử lý chênh lệch kiểm kê

**ID:** UC-W09
**Tên:** Xử lý chênh lệch kiểm kê
**Actors:** Warehouse Manager, Accountant, Chief Accountant

**Mô tả:**
Dựa trên số liệu tồn kho theo kiểm kê thực tế và số liệu tồn kho trên hệ thống, tạo phiếu nhập/xuất xử lý phần chênh lệch.

**Precondition:**
- User đã đăng nhập vào hệ thống
- Có quyền xử lý chênh lệch kiểm kê
- Phiếu kiểm kê đã hoàn thành (UC-W08)
- Có chênh lệch cần xử lý

**Main Flow:**
1. Accountant chọn "Xử lý chênh lệch kiểm kê"
2. Hệ thống hiển thị phiếu kiểm kê có chênh lệch
3. Accountant chọn phiếu kiểm kê
4. Hệ thống hiển thị chi tiết chênh lệch:
  - Chênh lệch dương (thừa) → Cần tạo phiếu nhập
  - Chênh lệch âm (thiếu) → Cần tạo phiếu xuất
5. Accountant click "Tạo phiếu nhập/xuất chênh lệch"
6. Hệ thống tự động tạo phiếu với thông tin:
  - **Phiếu nhập chênh lệch** (nếu thừa):
    - Ngày
    - Số phiếu
    - Người lập
    - Nội dung: "Xử lý chênh lệch kiểm kê"
    - Kho
    - Chi tiết: Mã vật tư, tên, số lượng thừa, đơn giá, thành tiền, số lô, seri
  - **Phiếu xuất chênh lệch** (nếu thiếu):
    - Tương tự phiếu nhập
7. Accountant duyệt phiếu
8. Hệ thống cập nhật tồn kho

**Postcondition:**
- Phiếu nhập/xuất chênh lệch được tạo
- Tồn kho được điều chỉnh khớp với kiểm kê thực tế
- Bút toán kế toán được ghi nhận

**Business Rules:**
- Tự động tạo phiếu từ phiếu kiểm kê
- Chênh lệch dương → Phiếu nhập
- Chênh lệch âm → Phiếu xuất
- Chief Accountant cần duyệt nếu chênh lệch lớn

**Nguồn:** ERP_SPECIFICATION.md Section 4.11 (lines 556-568)

---

### UC-W10: Tính giá vốn hàng xuất

**ID:** UC-W10
**Tên:** Tính giá vốn hàng xuất
**Actors:** Accountant, Chief Accountant

**Mô tả:**
Kế toán thực hiện tính và áp giá vốn vào các phiếu xuất theo phương pháp trung bình tháng.

**Precondition:**
- User đã đăng nhập vào hệ thống
- Có quyền tính giá vốn
- Có phiếu xuất chưa có giá vốn
- Cuối tháng hoặc cuối kỳ kế toán

**Main Flow:**
1. Accountant chọn "Tính giá vốn hàng xuất"
2. Hệ thống hiển thị form
3. Accountant chọn:
  - Kỳ tính giá (tháng/năm)
  - Kho cần tính
  - Phương pháp: **Trung bình tháng** (default)
4. Accountant click "Thực hiện tính giá"
5. Hệ thống thực hiện tính giá vốn:
  - Lấy giá trị tồn đầu kỳ
  - Cộng giá trị nhập trong kỳ
  - Chia cho tổng số lượng tồn + nhập
  - Áp giá vốn trung bình cho các phiếu xuất trong kỳ
6. Hệ thống cập nhật giá vốn vào phiếu xuất
7. Hệ thống tạo báo cáo tính giá vốn
8. Accountant xem xét và xác nhận

**Postcondition:**
- Giá vốn được tính và áp vào phiếu xuất
- Báo cáo giá vốn được tạo
- Có thể khóa sổ kho

**Business Rules:**
- Phương pháp: **Trung bình tháng**
- Tính cuối tháng hoặc cuối kỳ
- Không được sửa sau khi khóa sổ
- Công thức: Giá vốn TB = (Giá trị tồn đầu + Giá trị nhập) / (SL tồn đầu + SL nhập)

**Nguồn:** ERP_SPECIFICATION.md Section 4.12 (lines 570-578)

---

### UC-W11: Quản lý danh mục lô hàng

**ID:** UC-W11
**Tên:** Quản lý danh mục lô hàng hóa
**Actors:** Warehouse Manager, Warehouse User

**Mô tả:**
Thủ kho khai báo thông tin lô hàng hóa trước khi thực hiện lập phiếu nhập để có thể chọn lô khi làm phiếu nhập.

**Precondition:**
- User đã đăng nhập vào hệ thống
- Có quyền quản lý danh mục lô

**Main Flow:**
1. User chọn "Danh mục lô hàng hóa"
2. Hệ thống hiển thị danh sách lô hiện có
3. User click "Tạo lô mới"
4. User nhập **Thông tin chung:**
  - Ngày tạo
  - Mã lô hàng
5. User nhập **Thông tin chi tiết:**
  - Mã vật tư
  - Tên vật tư
6. User submit form
7. Hệ thống lưu thông tin lô

**Postcondition:**
- Lô hàng mới được tạo
- Có thể chọn lô khi tạo phiếu nhập

**Business Rules:**
- Phải tạo lô trước khi lập phiếu nhập
- Mã lô là duy nhất
- Một lô có thể chứa nhiều vật tư

**Nguồn:** ERP_SPECIFICATION.md Section 4 - Danh mục (lines 588-596)

---

### UC-W12: In tem mã vạch

**ID:** UC-W12
**Tên:** In tem mã vạch cho hàng hóa
**Actors:** Warehouse Manager, Warehouse User

**Mô tả:**
Thủ kho thực hiện in tem để dán lên hàng hóa. Hỗ trợ tem tự tạo và tem của nhà cung cấp.

**Precondition:**
- User đã đăng nhập vào hệ thống
- Có quyền in tem
- Có phiếu nhập khẩu hoặc danh sách vật tư cần in tem

**Main Flow:**
1. User chọn "In tem mã vạch"
2. Hệ thống hiển thị form
3. User nhập **Thông tin chung:**
  - Ngày in
  - **Loại tem:** Tem tự tạo / Tem của nhà cung cấp
  - Người lập (auto-fill)
  - Số lô vật tư
  - Nước sản xuất
  - Nhà cung cấp
  - Địa chỉ nhà cung cấp
  - Đơn vị nhập khẩu
  - Địa chỉ đơn vị
  - Điện thoại
4. User chọn phiếu nhập khẩu để kế thừa dữ liệu (optional)
5. User nhập **Thông tin chi tiết:**
  - Mã vật tư
  - Tên vật tư
  - Đơn vị tính
  - Số seri
  - **Mã vạch** (auto-generate theo quy ước)
  - Số lượng tem in
6. Hệ thống tự động tạo mã vạch:
  - **Tem tự in:** Mã vạch = `mã vật tư + ;; + số lô`
  - **Tem NCC:** Mã vạch = `số seri`
7. User chọn template tem
8. User click "In tem"
9. Hệ thống xuất file PDF tem mã vạch
10. User in tem và dán lên hàng hóa

**Postcondition:**
- Tem mã vạch được in ra
- Log in tem được ghi nhận

**Business Rules:**
- Mã vạch tự động theo quy ước:
  - Tem tự in: `mã vật tư + ;; + số lô`
  - Tem NCC: `số seri`
- Kế thừa mặt hàng, seri từ phiếu nhập khẩu
- Hỗ trợ nhiều template tem

**Nguồn:** ERP_SPECIFICATION.md Section 4 - Danh mục (lines 598-612)

---

### UC-W13: Xuất nội bộ giữa cửa hàng

**ID:** UC-W13
**Tên:** Xuất hàng nội bộ giữa các cửa hàng
**Actors:** Warehouse Manager, Warehouse User, Sales Executive

**Mô tả:**
Quy trình xuất hàng nội bộ giữa các cửa hàng với approval workflow từ cả hai bên (cửa hàng xuất và cửa hàng nhận).

**Precondition:**
- User đã đăng nhập vào hệ thống
- Có quyền tạo/duyệt lệnh xuất nội bộ
- Tồn kho cửa hàng xuất đủ

**Main Flow:**
1. **Nhân viên phụ trách điều phối** lập lệnh xuất hàng nội bộ:
  - Cửa hàng xuất
  - Cửa hàng nhận
  - Danh sách hàng hóa
  - Số lượng
2. **Cửa hàng xuất** làm phiếu xuất điều chuyển kho:
  - Kho xuất: Kho ký gửi (cửa hàng xuất)
  - Kho nhập: Kho ký gửi (cửa hàng nhận)
3. **Trưởng cửa hàng xuất** duyệt phiếu xuất để xác nhận lượng xuất
4. **Trưởng cửa hàng nhận** duyệt phiếu xuất để xác nhận lượng nhập
5. Hệ thống cập nhật tồn kho cả hai cửa hàng

**Postcondition:**
- Phiếu xuất nội bộ được tạo
- Được duyệt bởi cả hai bên
- Tồn kho cửa hàng xuất giảm
- Tồn kho cửa hàng nhận tăng

**Business Rules:**
- Cần duyệt từ cả hai bên (xuất và nhận)
- Kho xuất = kho nhập = kho ký gửi
- Điều phối tập trung

**Nguồn:** ERP_SPECIFICATION.md Section 4 - Quy trình đặc biệt (lines 618-623)

---

### UC-W14: Quản lý hàng ký gửi

**ID:** UC-W14
**Tên:** Quản lý hàng ký gửi (Thăng Long TM ↔ Nhật Minh)
**Actors:** Warehouse Manager, Warehouse User, Accountant, Chief Accountant

**Mô tả:**
Quy trình quản lý hàng ký gửi giữa Thăng Long TM (chủ hàng) và Nhật Minh (đơn vị nhận ký gửi).

**Precondition:**
- User đã đăng nhập vào hệ thống
- Có thỏa thuận ký gửi giữa hai bên

**Main Flow (Nhập xuất hàng ký gửi):**
1. **Tại Thăng Long TM:**
  - Làm phiếu xuất điều chuyển kho
  - Kho xuất: Kho tổng
  - Kho nhập: Kho ký gửi
2. **Tại Nhật Minh:**
  - Làm phiếu nhập kho
  - Kho nhập: Kho ký gửi tại cửa hàng

**Main Flow (Mua bán giữa Nhật Minh và Thăng Long TM):**
1. **Nhật Minh** tổng hợp số lượng thực tế bán cho KH
2. Nhật Minh gửi số liệu cho Thăng Long
3. **Thăng Long** xuất hóa đơn:
  - Kho xuất: Kho hàng ký gửi
  - Khách hàng: Nhật Minh
4. **Nhật Minh** lập phiếu nhập mua:
  - Kho nhập: Kho xuất hóa đơn

**Main Flow (Bán hàng tại Nhật Minh):**
1. Bán hàng cho KH từ kho xuất hóa đơn:
  - Ghi nhận tăng doanh thu
  - Ghi nhận công nợ
2. Xuất kho hàng ký gửi:
  - Giảm lượng tồn kho ký gửi
3. Lập phiếu nhập mua vào kho xuất hóa đơn:
  - Cuối tháng tính được giá vốn

**Postcondition:**
- Hàng ký gửi được theo dõi chính xác
- Doanh thu, công nợ được ghi nhận đúng
- Giá vốn được tính chính xác cuối tháng

**Business Rules:**
- Kho ký gửi là kho đặc biệt
- Phân biệt kho ký gửi và kho xuất hóa đơn
- Nhật Minh báo cáo bán hàng thực tế cho Thăng Long
- Tính giá vốn dựa trên phiếu nhập mua

**Nguồn:** ERP_SPECIFICATION.md Section 4 - Quy trình đặc biệt (lines 625-639)

---

### UC-W15: Kiểm tra công nợ trước xuất hàng

**ID:** UC-W15
**Tên:** Kiểm tra công nợ quá hạn trước khi xuất hàng
**Actors:** Sales Executive (check), Chief Accountant (approve ngoại lệ)

**Mô tả:**
Kiểm tra nếu khách hàng có hóa đơn quá hạn hoặc quá hạn mức công nợ trước khi cho phép xuất hàng. Nếu vi phạm, cần Kế toán trưởng xác nhận.

**Precondition:**
- Có lệnh xuất hàng
- Khách hàng đã được thiết lập hạn mức công nợ

**Main Flow:**
1. Sales Executive tạo lệnh xuất hàng (UC-W03 bước 5)
2. Hệ thống tự động kiểm tra **điều kiện xuất hàng hợp lệ:**
  - **Điều kiện 1:** Khách hàng không có hóa đơn quá hạn
  - **Điều kiện 2:** Giá trị công nợ hiện tại + giá trị trên các lệnh xuất đã duyệt chưa xuất + giá trị trên lệnh xuất hàng hiện tại ≤ hạn mức công nợ
3. Nếu thỏa mãn cả 2 điều kiện:
  - Lệnh xuất hợp lệ
  - Tiếp tục flow xuất hàng
4. Hệ thống lưu log kiểm tra công nợ

**Alternative Flow (Vi phạm công nợ - Xử lý ngoại lệ):**
- 2a. Hệ thống phát hiện vi phạm một trong hai điều kiện:
  - Có hóa đơn quá hạn
  - Hoặc vượt hạn mức công nợ
- 2b. Hệ thống hiển thị cảnh báo chi tiết:
  - Số hóa đơn quá hạn (nếu có)
  - Số ngày quá hạn
  - Hạn mức công nợ
  - Công nợ hiện tại
  - Lệnh xuất đã duyệt chưa xuất
  - Giá trị lệnh xuất hiện tại
  - Tổng công nợ dự kiến
- 2c. Hệ thống chặn lệnh xuất (trạng thái: Pending Approval)
- 2d. Hệ thống gửi thông báo đến **Chief Accountant**
- 2e. **Chief Accountant** xem xét:
  - Xem lịch sử công nợ khách hàng
  - Xem lý do cần xuất hàng
  - Liên hệ khách hàng (nếu cần)
- 2f. **Chief Accountant** quyết định:
  - **Xác nhận:** Lệnh xuất hợp lệ → Tiếp tục flow (Main Flow bước 3)
  - **Từ chối:** Lệnh xuất bị hủy → Thông báo Sales Executive
- 2g. Hệ thống ghi log quyết định

**Postcondition (Main Flow):**
- Lệnh xuất hàng hợp lệ
- Log kiểm tra công nợ được ghi nhận

**Postcondition (Alternative Flow - Approved):**
- Lệnh xuất được xác nhận ngoại lệ
- Log xác nhận của Chief Accountant được ghi nhận

**Postcondition (Alternative Flow - Rejected):**
- Lệnh xuất bị hủy
- Sales Executive nhận được thông báo
- Cần liên hệ khách hàng xử lý công nợ

**Business Rules:**
- **Điều kiện 1:** Không có hóa đơn quá hạn
- **Điều kiện 2:** Tổng công nợ dự kiến ≤ Hạn mức
- Công thức kiểm tra:
```
  Công nợ hiện tại
  + Giá trị lệnh xuất đã duyệt chưa xuất
  + Giá trị lệnh xuất hiện tại
  ≤ Hạn mức công nợ
```
- **Xử lý ngoại lệ:** Kế toán trưởng phải xác nhận nếu vi phạm
- Tự động kiểm tra khi lưu lệnh xuất
- Hiển thị cảnh báo rõ ràng

**Nguồn:** ERP_SPECIFICATION.md Section 2.8 (lines 152-162)

---

## 5. Use Case Diagram

### 5.1. Sơ đồ Use Case (Text)

```
┌──────────────────────────────────────────────────────────────────────────────────────┐
│                         «System» Warehouse Management                                 │
├──────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                        │
│  ┌────────────────────────────────┐                                                   │
│  │ UC-W01: Cập nhật tồn kho đầu kỳ │◄─────────┐                                      │
│  └────────────────────────────────┘          │                                      │
│                                               │                                      │
│  ┌────────────────────────────────┐          │                                      │
│  │ UC-W02: Nhập hàng vào kho      │◄─────────┤                                      │
│  └────────────────────────────────┘          │                                      │
│                                               │                                      │
│  ┌────────────────────────────────┐          │                                      │
│  │ UC-W03: Xuất hàng từ kho       │◄─────────┼──────────┐                           │
│  │         (approval workflow)     │          │          │                           │
│  └────────────────────────────────┘          │          │                           │
│              │                                │          │                           │
│              │ «include»                      │          │                           │
│              ▼                                │          │                           │
│  ┌────────────────────────────────┐          │          │                           │
│  │ UC-W15: Kiểm tra công nợ       │◄─────────┼──────────┼───────────────────┐       │
│  │         trước xuất hàng         │          │          │                   │       │
│  └────────────────────────────────┘          │          │                   │       │
│                                               │          │                   │       │
│  ┌────────────────────────────────┐          │          │                   │       │
│  │ UC-W04: Xuất CCDC              │◄─────────┤          │                   │       │
│  └────────────────────────────────┘          │          │                   │       │
│                                               │          │                   │       │
│  ┌────────────────────────────────┐          │          │                   │       │
│  │ UC-W05: Điều chuyển giữa kho   │◄─────────┤          │                   │       │
│  └────────────────────────────────┘          │          │                   │       │
│                                               │          │                   │       │
│  ┌────────────────────────────────┐          │          │                   │       │
│  │ UC-W06: Điều chuyển vị trí     │◄─────────┤          │                   │       │
│  └────────────────────────────────┘          │          │                   │       │
│                                               │          │                   │       │
│  ┌────────────────────────────────┐          │          │                   │       │
│  │ UC-W07: Lập lệnh kiểm kê       │◄─────────┼──────────┘                   │       │
│  └────────────────────────────────┘          │    (Accountant)              │       │
│              │                                │                              │       │
│              │ «precedes»                     │                              │       │
│              ▼                                │                              │       │
│  ┌────────────────────────────────┐          │                              │       │
│  │ UC-W08: Thực hiện kiểm kê      │◄─────────┤                              │       │
│  └────────────────────────────────┘          │                              │       │
│              │                                │                              │       │
│              │ «precedes»                     │                              │       │
│              ▼                                │                              │       │
│  ┌────────────────────────────────┐          │                              │       │
│  │ UC-W09: Xử lý chênh lệch kiểm kê│◄────────┼──────────┘                   │       │
│  └────────────────────────────────┘          │    (Accountant)              │       │
│                                               │                              │       │
│  ┌────────────────────────────────┐          │                              │       │
│  │ UC-W10: Tính giá vốn hàng xuất │◄─────────┼──────────┘                   │       │
│  └────────────────────────────────┘          │    (Accountant)              │       │
│                                               │                              │       │
│  ┌────────────────────────────────┐          │                              │       │
│  │ UC-W11: Quản lý danh mục lô    │◄─────────┤                              │       │
│  └────────────────────────────────┘          │                              │       │
│                                               │                              │       │
│  ┌────────────────────────────────┐          │                              │       │
│  │ UC-W12: In tem mã vạch         │◄─────────┤                              │       │
│  └────────────────────────────────┘          │                              │       │
│                                               │                              │       │
│  ┌────────────────────────────────┐          │                              │       │
│  │ UC-W13: Xuất nội bộ giữa CH    │◄─────────┼──────────────────────────────┤       │
│  └────────────────────────────────┘          │                              │       │
│                                               │                              │       │
│  ┌────────────────────────────────┐          │                              │       │
│  │ UC-W14: Quản lý hàng ký gửi    │◄─────────┼──────────────────────────────┤       │
│  └────────────────────────────────┘          │                              │       │
│                                               │                              │       │
└───────────────────────────────────────────────┼──────────────────────────────┼───────┘
                                                │                              │
                                                │                              │
     ┌─────────────┐         ┌────────────┐    │       ┌──────────────────┐   │
     │ Warehouse   │─────────│ Warehouse  │────┘       │ Sales Executive  │───┘
     │ Manager     │         │ User       │            └──────────────────┘
     └─────────────┘         └────────────┘
            │
            │
     ┌──────┴─────┐
     │            │
┌────────────┐ ┌──────────────────┐
│ Accountant │ │ Chief Accountant │
└────────────┘ └──────────────────┘
```

### 5.2. Mối quan hệ Actors và Use Cases

**Warehouse Manager:**
- UC-W01: Cập nhật tồn kho đầu kỳ
- UC-W02: Nhập hàng vào kho
- UC-W03: Xuất hàng từ kho (approve)
- UC-W04: Xuất CCDC
- UC-W05: Điều chuyển giữa các kho
- UC-W06: Điều chuyển vị trí trong kho
- UC-W07: Lập lệnh kiểm kê
- UC-W08: Thực hiện kiểm kê
- UC-W09: Xử lý chênh lệch kiểm kê
- UC-W11: Quản lý danh mục lô hàng
- UC-W12: In tem mã vạch
- UC-W13: Xuất nội bộ giữa cửa hàng
- UC-W14: Quản lý hàng ký gửi

**Warehouse User:**
- UC-W02: Nhập hàng vào kho
- UC-W03: Xuất hàng từ kho (create)
- UC-W04: Xuất CCDC
- UC-W05: Điều chuyển giữa các kho
- UC-W06: Điều chuyển vị trí trong kho
- UC-W08: Thực hiện kiểm kê
- UC-W11: Quản lý danh mục lô hàng
- UC-W12: In tem mã vạch
- UC-W13: Xuất nội bộ giữa cửa hàng
- UC-W14: Quản lý hàng ký gửi

**Accountant:**
- UC-W01: Cập nhật tồn kho đầu kỳ
- UC-W07: Lập lệnh kiểm kê
- UC-W09: Xử lý chênh lệch kiểm kê
- UC-W10: Tính giá vốn hàng xuất
- UC-W14: Quản lý hàng ký gửi

**Chief Accountant:**
- UC-W01: Cập nhật tồn kho đầu kỳ
- UC-W03: Xuất hàng từ kho (approve ngoại lệ)
- UC-W07: Lập lệnh kiểm kê
- UC-W09: Xử lý chênh lệch kiểm kê
- UC-W10: Tính giá vốn hàng xuất
- UC-W14: Quản lý hàng ký gửi
- UC-W15: Kiểm tra công nợ trước xuất hàng (approve ngoại lệ)

**Sales Executive:**
- UC-W03: Xuất hàng từ kho (create)
- UC-W13: Xuất nội bộ giữa cửa hàng
- UC-W15: Kiểm tra công nợ trước xuất hàng (check)

### 5.3. Mối quan hệ Include và Precedes

**Include:**
- **UC-W03 «include» UC-W15:**
  - Khi xuất hàng từ kho (UC-W03)
  - Hệ thống tự động kiểm tra công nợ (UC-W15)

**Precedes:**
- **UC-W07 «precedes» UC-W08:**
  - Phải lập lệnh kiểm kê (UC-W07) trước
  - Mới thực hiện kiểm kê (UC-W08)

- **UC-W08 «precedes» UC-W09:**
  - Phải thực hiện kiểm kê (UC-W08) trước
  - Mới xử lý chênh lệch (UC-W09)

---

## 📚 Tham khảo

**Tài liệu liên quan:**
- [ERP_SPECIFICATION.md](./../../feature/ERP_SPECIFICATION.md) - Đặc tả ERP gốc (Section 4)
- [WAREHOUSE_WORKFLOW.md](./WAREHOUSE_WORKFLOW.md) - Workflow và ERD
- [WAREHOUSE_DIAGRAMS.md](./WAREHOUSE_DIAGRAMS.md) - State Machine Diagrams

---

## 📝 Ghi chú quan trọng

1. **Phân quyền Field-level:**
  - Warehouse User **KHÔNG** xem được: Đơn giá, Thành tiền, Giá vốn
  - Warehouse User **KHÔNG** được sửa: Thông tin khách hàng, mặt hàng, số lượng yêu cầu
  - Chỉ cập nhật thông tin thực xuất: Seri, lô, kho, số lượng

2. **Approval Workflow:**
  - Phiếu xuất kho cần Warehouse Manager duyệt
  - Vi phạm công nợ cần Chief Accountant xác nhận
  - Xuất nội bộ giữa cửa hàng cần duyệt từ cả hai bên

3. **Kiểm tra công nợ (UC-W15):**
  - **Điều kiện 1:** Không có hóa đơn quá hạn
  - **Điều kiện 2:** Tổng công nợ dự kiến ≤ Hạn mức
  - **Xử lý ngoại lệ:** Chief Accountant phải xác nhận

4. **Quy trình kiểm kê (UC-W07 → UC-W08 → UC-W09):**
  - Kế toán lập lệnh kiểm kê → Chốt số tồn kho
  - Kho dừng nhập/xuất → Thủ kho kiểm đếm thực tế
  - Hệ thống tính chênh lệch → Kế toán xử lý chênh lệch

5. **Tính giá vốn (UC-W10):**
  - Phương pháp: **Trung bình tháng**
  - Thực hiện cuối tháng
  - Công thức: Giá vốn TB = (Giá trị tồn đầu + Giá trị nhập) / (SL tồn đầu + SL nhập)

6. **In tem mã vạch (UC-W12):**
  - **Tem tự in:** Mã vạch = `mã vật tư + ;; + số lô`
  - **Tem NCC:** Mã vạch = `số seri`

7. **Hàng ký gửi (UC-W14):**
  - Kho ký gửi là kho đặc biệt
  - Phân biệt kho ký gửi và kho xuất hóa đơn
  - Quy trình ba bước: Chuyển ký gửi → Mua bán → Bán lẻ

---

**Ngày cập nhật:** 15/01/2026
**Người soạn:** DCNET Development Team
**Nguồn:** ERP_SPECIFICATION.md v1.0 (Section 4: lines 455-641, Section 2: lines 126-162)
