# Module Credit Management - Đặc tả theo Nhật Minh

> **Nguồn:** `docs/feature/ERP_SPECIFICATION.md` Section 2.6-2.8
> **Phiên bản:** 1.0.0 | **Giai đoạn:** Phase 2 ERP - Critical Module
> **Lưu ý:** File này chỉ ghi lại ĐÚNG những gì có trong spec gốc

---

## Định nghĩa

> Quản lý hạn mức tín dụng và kiểm tra công nợ quá hạn của khách hàng trước khi cho phép xuất hàng

**Mục đích:** Kiểm soát rủi ro công nợ trong bán hàng chịu (bán buôn cho đại lý)

---

## Hạn mức công nợ

**Nguồn:** ERP_SPECIFICATION.md Section 2, Bước 7 (line 137-150)

### Màn hình: Hạn mức công nợ

**Mục đích:** Bộ phận KD kiểm tra hạn mức công nợ của KH.

**Cách làm:** Bộ phận KD kiểm tra hạn mức công nợ. Trường hợp hết hạn mức, bộ phận KD lập lại đơn hàng, hợp đồng gửi lại KH.

### Thông tin cần có

**Thông tin chung:**
- Ngày áp dụng
- Tài khoản công nợ

**Thông tin chi tiết:**
- Mã khách hàng
- Tên khách hàng
- Giá trị hạn mức

### Tính năng

- Đính kèm file

**Bộ phận:** Kinh doanh
**Tần suất:** Hàng ngày

---

## Kiểm tra công nợ quá hạn

**Nguồn:** ERP_SPECIFICATION.md Section 2, Bước 8 (line 152-162)

### Màn hình: Lệnh xuất hàng (với Credit Check)

**Mục đích:** Bộ phận KD kiểm tra xem nếu có hóa đơn quá hạn hoặc quá hạn mức không để làm cơ sở cho quyết định có xuất hàng cho KH không.

**Cách làm:** Bộ phận KD thực hiện cập nhật các mặt hàng cần xuất. Khi lưu, phần mềm sẽ thực hiện kiểm tra nếu có hóa đơn quá hạn sẽ hiện cảnh báo.

### Điều kiện xuất hàng hợp lệ

**2 điều kiện bắt buộc:**

1. **Khách hàng không có hóa đơn quá hạn**
2. **Giá trị công nợ hiện tại + giá trị trên các lệnh xuất đã duyệt chưa xuất + giá trị trên lệnh xuất hàng hiện tại không lớn hơn hạn mức công nợ**

### Xử lý ngoại lệ

**Nếu không thỏa mãn 2 điều kiện trên:**
- Kế toán trưởng phải xác nhận thì lệnh xuất mới hợp lệ.

---

## Lệnh xuất hàng - Tính năng Credit Check

**Nguồn:** ERP_SPECIFICATION.md Section 2, Bước 6 (line 110-134)

### Màn hình: Lệnh xuất hàng

**Thông tin cần có:**

#### Thông tin chung:
- Ngày đề nghị
- Người đề nghị
- Kho xuất
- Khách hàng

#### Thông tin chi tiết:
- Mã vật tư
- Tên vật tư
- Đvt
- Số lượng
- Đơn giá trước chiết khấu
- Thành tiền
- Số chính sách chiết khấu
- % chiết khấu
- Tiền chiết khấu
- Tiền sau chiết khấu

### Tính năng cần có

#### 1. Kế thừa dữ liệu từ đơn hàng bán

#### 2. Kiểm tra hạn mức và công nợ quá hạn

**Thống nhất chung:**

- **Khi kiểm tra điều kiện xuất hàng thì phải hiển thị:**
  - Số dư công nợ thực tế
  - Công nợ dự kiến (bao gồm cả lệnh xuất hàng chưa xuất)
  - Số hóa đơn quá hạn

### Yêu cầu phân quyền

- Phân quyền bộ phận kho không nhìn thấy đơn giá, thành tiền
- Phân quyền bộ phận kho không được sửa lại thông tin khách hàng, mặt hàng, số lượng yêu cầu

**Thống nhất chung:**
- Bộ phận kho cập nhật thông tin thực xuất (mặt hàng, seri, lô, kho, số lượng) để làm cơ sở cho kế toán kế thừa dữ liệu

**Bộ phận:** Kinh doanh

---

## Danh mục liên quan

### Danh mục đối tượng (Khách hàng)

**Nguồn:** ERP_SPECIFICATION.md Section 2 - Danh mục liên quan (line 273-277)

**Mô tả:** Dùng để khai báo danh mục các đối tượng như: nhà cung cấp, khách hàng, đối tượng nội bộ.

**Thông tin chung:**
- Mã đối tượng
- Tên đối tượng
- Loại đối tượng
- Địa chỉ
- Mã số thuế
- Người đại diện
- Điện thoại
- Email
- Nhóm đối tượng
- Thông tin tài khoản ngân hàng
- **Phương thức thanh toán**
- **Kỳ hạn thanh toán**

---

## Tóm tắt

### Chức năng chính

| # | Chức năng | Mô tả |
|---|-----------|-------|
| 1 | **Cập nhật hạn mức công nợ** | Quản lý credit limit theo từng khách hàng |
| 2 | **Kiểm tra công nợ tự động** | Tự động check khi tạo lệnh xuất hàng |
| 3 | **Hiển thị thông tin công nợ** | Hiện số dư công nợ thực tế, công nợ dự kiến, hóa đơn quá hạn |
| 4 | **Cảnh báo vượt hạn mức** | Warning nếu không đủ điều kiện xuất hàng |
| 5 | **Xử lý ngoại lệ** | Kế toán trưởng có thể override |

### Bộ phận sử dụng

- **Kinh doanh:** Cập nhật hạn mức, kiểm tra công nợ
- **Kế toán trưởng:** Phê duyệt ngoại lệ (override)

### Tần suất sử dụng

- **Hạn mức công nợ:** Khi có thay đổi chính sách tín dụng
- **Kiểm tra công nợ:** Hàng ngày (khi tạo lệnh xuất)

---

**© 2025 DCNET Corporation - Powered by DCNET Cloud**
