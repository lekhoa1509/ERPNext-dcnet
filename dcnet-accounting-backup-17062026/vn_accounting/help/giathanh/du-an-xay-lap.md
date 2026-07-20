---
title: Setup dự án xây lắp để tính giá thành
section: Giá thành
doctype: null
---

# Setup dự án xây lắp để tính giá thành

Doanh nghiệp xây lắp (thi công công trình, lắp đặt thiết bị) cần cấu hình thêm một số thông tin trên mỗi **Dự án** để hệ thống tính đúng giá thành theo Thông tư 99/2025/TT-BTC. Bài này hướng dẫn kế toán trưởng hoặc người lập dự án thực hiện cấu hình ban đầu.

## Trước khi bắt đầu

Cần có:
- Hợp đồng xây lắp đã ký với chủ đầu tư (để lấy giá trị hợp đồng)
- Kế hoạch bàn giao (nghiệm thu từng đợt hoặc toàn bộ)
- Cơ cấu chi phí dự kiến (NVL trực tiếp, NC trực tiếp, chi phí thi công chung)

## Bật chế độ xây lắp cho dự án

1. Vào **Dự án** (từ menu bên trái hoặc tìm kiếm nhanh)
2. Mở hoặc tạo mới dự án tương ứng với công trình
3. Tìm tab hoặc trường **"Dự án Xây lắp?"** → tích chọn ☑

Sau khi tích, các trường bổ sung xuất hiện:

| Trường | Ý nghĩa |
|--------|---------|
| Giá trị hợp đồng | Tổng giá trị hợp đồng xây lắp đã ký (VND) |
| Tỷ lệ % bàn giao lũy kế | % giá trị hợp đồng đã được nghiệm thu và bàn giao cho chủ đầu tư |
| Giai đoạn thi công | Giai đoạn hiện tại của công trình |

## Nhập thông tin hợp đồng

**Giá trị hợp đồng:** Nhập đúng giá trị hợp đồng theo văn bản ký kết, chưa bao gồm VAT (số tiền net). Hệ thống dùng con số này để tính doanh thu ghi nhận theo tiến độ.

**Tỷ lệ % bàn giao lũy kế:** Cập nhật sau mỗi lần nghiệm thu công trình. Ví dụ:
- Sau nghiệm thu đợt 1 (hoàn thành móng): nhập `30`
- Sau nghiệm thu đợt 2 (hoàn thành thô): nhập `65`
- Nghiệm thu hoàn công: nhập `100`

> **Lưu ý:** Đây là tỷ lệ **lũy kế** (cumulative), không phải tỷ lệ từng đợt. Mỗi lần nghiệm thu, nhập tổng % đã hoàn thành từ đầu dự án đến hiện tại.

**Giai đoạn thi công:** Chọn giai đoạn đang thi công để lọc báo cáo theo giai đoạn. Các giai đoạn: Chuẩn bị → Thi công → Hoàn thiện → Bàn giao → Bảo hành.

## Cách hạch toán chi phí vào dự án

Chi phí xây lắp được hạch toán vào **Trung tâm chi phí** tương ứng với từng dự án. Thiết lập này thường được kế toán trưởng cấu hình khi tạo dự án.

**Để hạch toán chi phí vào đúng dự án:**

Khi nhập các bút toán phát sinh (mua vật tư, tính lương thợ, phân bổ khấu hao máy thi công...), luôn chọn **Trung tâm chi phí** là trung tâm chi phí của dự án này.

Ví dụ:
- Mua sắt cho công trình A → Nợ 621 / Có 331, trung tâm chi phí: `CC-CTRINHA-A`
- Tính lương thợ công trình A → Nợ 622 / Có 334, trung tâm chi phí: `CC-CTRINHA-A`
- Phân bổ chi phí máy thi công → Nợ 627 / Có 214, trung tâm chi phí: `CC-CTRINHA-A`

## Tính giá thành cuối kỳ cho dự án xây lắp

Dự án xây lắp thường chọn hình thức **kết chuyển thẳng vào giá vốn (TK 632)** thay vì nhập kho thành phẩm, vì "sản phẩm" là công trình được bàn giao tại chỗ cho chủ đầu tư.

Quy trình:

1. Vào **Giá thành → Wizard tính giá thành SX**
2. Chọn **Loại đối tượng: Dự án**
3. Chọn dự án cụ thể
4. Tại bước chọn hình thức, chọn **"Kết chuyển thẳng vào giá vốn (TK 632)"**
5. Hệ thống tạo bút toán: Nợ 154 / Có 621, 622, 627 → rồi Nợ 632 / Có 154

## Ghi nhận doanh thu theo tiến độ bàn giao

Khi có biên bản nghiệm thu và hóa đơn xuất cho chủ đầu tư:

1. Cập nhật **Tỷ lệ % bàn giao lũy kế** trên dự án theo biên bản nghiệm thu
2. Tạo hóa đơn bán hàng với giá trị = Giá trị hợp đồng × % bàn giao kỳ này
3. Hạch toán: Nợ 131 / Có 511 (doanh thu theo tiến độ)

> **Ví dụ:** Hợp đồng 2 tỷ đồng. Đợt này nghiệm thu 30% (lũy kế từ 0% lên 30%). Hóa đơn xuất: 2.000.000.000 × 30% = 600.000.000 đồng.

## Báo cáo theo dõi dự án xây lắp

Sau khi cấu hình đúng, sử dụng:

- **Giá thành → Tập hợp chi phí SX**: xem tổng chi phí 621/622/627 theo từng dự án trong kỳ
- **Tổng hợp → Sổ cái**: chọn TK 154 để xem SPDD lũy kế của từng dự án
- **Báo cáo tài chính → Kết quả kinh doanh (B02-DN)**: so sánh doanh thu 511 với giá vốn 632 theo từng kỳ

## Câu hỏi thường gặp

**Dự án có nhiều hạng mục riêng biệt (A, B, C) — hạch toán như thế nào?**

Tạo riêng **Trung tâm chi phí** cho từng hạng mục thay vì cho cả dự án. Khi chạy wizard, chọn loại đối tượng là **Trung tâm chi phí** và tính giá thành từng hạng mục riêng. Dự án tổng hợp là nhóm của các trung tâm chi phí con.

**Tỷ lệ % bàn giao cập nhật khi nào?**

Cập nhật ngay khi có **biên bản nghiệm thu** ký với chủ đầu tư — không đợi đến cuối kỳ. Biên bản nghiệm thu là cơ sở pháp lý để ghi nhận doanh thu đúng kỳ.

**Có thể tính giá thành xây lắp theo hạng mục không?**

Có. Thay vì gán tất cả chi phí vào 1 trung tâm chi phí của dự án, chia nhỏ thành các trung tâm chi phí con (ví dụ: `CC-CTRINHA-A-PHAN-MONG`, `CC-CTRINHA-A-PHAN-KHUNG`). Wizard tính giá thành SX tổng hợp và hiển thị riêng từng trung tâm.
