# 03 - Quản lý Sản phẩm: Vấn đề cần Clarify

> **Ngày tạo:** 16/02/2026
> **Trạng thái:** Chờ khách hàng xác nhận

---

## Quy ước

| Icon | Ý nghĩa |
|------|---------|
| :red_circle: | **Critical** — Block triển khai, cần trả lời trước khi code |
| :orange_circle: | **High** — Ảnh hưởng thiết kế, cần trả lời trước Sprint |
| :yellow_circle: | **Medium** — Có thể dùng giá trị mặc định, confirm sau |
| :green_circle: | **Resolved** — Đã có câu trả lời |

---

## 1. Mã sản phẩm & SKU

| # | Câu hỏi | Priority | Ảnh hưởng | Trả lời | Nguồn |
|---|---------|----------|-----------|---------|-------|
| 1.1 | Spec ghi cả "Mã sản phẩm" và "SKU" — đây là 2 field riêng hay cùng 1? ERPNext dùng `item_code` làm mã chính. Nếu cần SKU riêng (VD: mã nhà sản xuất) → thêm custom field. | :yellow_circle: Medium | List view 6.1, Import 6.4 | Recommend: dùng `item_code` = mã SP, `manufacturer_part_no` = SKU nhà SX. Nếu không đủ → thêm `custom_sku` | 6.1 |

---

## 2. Tích điểm sản phẩm

| # | Câu hỏi | Priority | Ảnh hưởng | Trả lời | Nguồn |
|---|---------|----------|-----------|---------|-------|
| 2.1 | "Tích điểm" trong Import SP — mỗi SP có số điểm riêng (VD: gậy driver = 100 điểm) hay tính điểm theo % giá trị đơn hàng? ERPNext Loyalty Program tính theo amount (VD: 1 điểm/100.000đ). Nếu per item → cần custom field. | :orange_circle: High | Import 6.4, liên quan module 38-tich-diem | Recommend: dùng Loyalty Program (theo amount), bỏ field tích điểm per item. Nếu cần per item → thêm `custom_loyalty_points` | 6.4 |

---

## 3. Thuộc tính vật lý

| # | Câu hỏi | Priority | Ảnh hưởng | Trả lời | Nguồn |
|---|---------|----------|-----------|---------|-------|
| 3.1 | "Thuộc tính thêm (chiều cao, dài, rộng, chất liệu)" — áp dụng cho tất cả SP hay chỉ một số nhóm SP nhất định (VD: gậy golf cần chiều dài, quần áo cần chất liệu)? | :yellow_circle: Medium | Item form 6.3, Import 6.4 | Recommend: thêm tất cả fields nhưng không bắt buộc nhập, ẩn/hiện theo Item Group nếu cần | 6.4 |

---

## 4. Bảo hành

| # | Câu hỏi | Priority | Ảnh hưởng | Trả lời | Nguồn |
|---|---------|----------|-----------|---------|-------|
| 4.1 | Spec ghi "bảo hành 1 năm với tất cả SP (gậy golf, shaft)" — chỉ gậy golf và shaft được bảo hành hay thực sự tất cả SP (kể cả bóng, mũ, găng tay)? | :yellow_circle: Medium | Chi tiết SP 6.6 | Recommend: default 12 tháng cho tất cả, cho phép sửa per item (VD: bóng golf = 0 tháng) | 6.6 |

---

## Thống kê

| Priority | Số lượng |
|----------|----------|
| :red_circle: Critical | 0 |
| :orange_circle: High | 1 |
| :yellow_circle: Medium | 3 |
| **Tổng** | **4** |
