---
section: Tổng quan
title: Tổng quan Kế toán (Dashboard)
summary: Trang điều khiển tổng hợp 5 chỉ số chính và 8 biểu đồ về doanh thu, chi phí, công nợ, dòng tiền.
---

## Mục đích

Trang **Tổng quan Kế toán** là màn hình điều khiển (dashboard) cho lãnh đạo và kế toán trưởng nắm nhanh "sức khỏe" tài chính của công ty trong một khoảng kỳ: doanh thu, chi phí, công nợ phải thu/phải trả, tồn quỹ, cùng xu hướng và cơ cấu qua các biểu đồ. Đây là màn hình **chỉ xem** — không tạo chứng từ, không định khoản; toàn bộ số liệu được tổng hợp trực tiếp từ Sổ Cái (bút toán đã ghi sổ).

## Khi nào dùng

- Đầu ngày/đầu kỳ: liếc nhanh 5 chỉ số để biết tình hình so với kỳ trước.
- Họp giao ban: trình bày xu hướng doanh thu–chi phí, dòng tiền, top khách hàng.
- Khi cần khoanh vùng: thấy công nợ phải thu tăng bất thường → bấm vào báo cáo chi tiết để truy.
- Không dùng để chốt số quyết toán — số liệu pháp lý lấy ở Báo cáo tài chính (B01/B02/B03-DN).

## Cách thực hiện

1. Bấm **Tổng quan** ở đầu menu → trang dashboard mở.
2. Chọn bộ lọc trên đầu trang:
   - **Công ty**: công ty cần xem (mặc định công ty đang làm việc).
   - **Mức thời gian (period)**: **Tháng / Quý / Năm / Tuần** — quyết định cách chia trục thời gian của các biểu đồ xu hướng.
3. Số liệu tự cập nhật theo bộ lọc.

### 5 chỉ số chính (KPI)

| Chỉ số | Nguồn số liệu | Ý nghĩa |
|---|---|---|
| **Tổng Doanh Thu** | Phát sinh Có TK 511 trong kỳ | Doanh thu bán hàng & cung cấp dịch vụ |
| **Tổng Chi Phí** | Phát sinh Nợ nhóm TK 6xx trong kỳ | Tổng chi phí phát sinh |
| **Công Nợ Phải Thu** | Số dư TK 131 tại thời điểm hiện tại | Khách hàng còn nợ |
| **Công Nợ Phải Trả** | Số dư TK 331 | Còn nợ nhà cung cấp |
| **Tồn Quỹ** | Số dư TK 111 + 112 | Tiền mặt + tiền gửi ngân hàng |

Mỗi chỉ số kèm **mũi tên tăng/giảm (%)** so với kỳ trước liền kề (kỳ trước được suy ra tự động từ khoảng ngày đang chọn).

### 8 biểu đồ

| Biểu đồ | Loại | Nội dung |
|---|---|---|
| Doanh thu – Chi phí | Đường/cột theo thời gian | Diễn biến DT vs CP theo mức thời gian đã chọn |
| Dòng tiền | Đường theo thời gian | Thu – chi tiền (TK 111/112) theo kỳ |
| Công nợ phải thu theo KH | Tròn (donut) | Cơ cấu TK 131 theo từng khách hàng |
| Công nợ phải trả theo NCC | Tròn (donut) | Cơ cấu TK 331 theo nhà cung cấp |
| Doanh thu theo nhóm hàng | Cột | DT chia theo nhóm hàng hóa/dịch vụ |
| Chi phí theo loại | Cột/tròn | CP chia theo nhóm TK 6xx |
| Top khách hàng theo DT | Cột | Khách hàng đóng góp doanh thu lớn nhất |
| Tuổi nợ phải thu | Cột | Phân nhóm công nợ phải thu theo số ngày quá hạn |

> **Lưu ý mức thời gian:** Biểu đồ xu hướng (Doanh thu–Chi phí, Dòng tiền) chia trục theo lựa chọn Tháng/Quý/Năm/Tuần. Biểu đồ tròn (công nợ theo KH/NCC) và tuổi nợ lấy số dư **tại thời điểm hiện tại**, không phụ thuộc khoảng ngày.

## Định khoản tự động

Dashboard **không tạo bút toán**. Mọi con số là kết quả tổng hợp đọc từ Sổ Cái (GL) theo prefix tài khoản (511, 6xx, 131, 331, 111, 112). Muốn số liệu đúng, các chứng từ nguồn phải đã được **ghi sổ (docstatus = Đã duyệt)** — chứng từ ở trạng thái nháp không được tính.

## Tình huống đặc biệt & cảnh báo

- **Số liệu lệch với Báo cáo tài chính:** Dashboard tính nhanh theo prefix TK, có thể làm tròn/gộp khác với B01/B02-DN. Số pháp lý lấy ở **Báo cáo tài chính**, dashboard chỉ để theo dõi nhanh.
- **Chỉ số = 0 hoặc trống:** thường do (a) chưa có bút toán ghi sổ trong kỳ, (b) chọn sai công ty, (c) khoảng ngày không có phát sinh. Kiểm tra **Sổ Cái** để đối chiếu.
- **% so với kỳ trước hiển thị 0%:** kỳ trước không có dữ liệu để so sánh (kỳ đầu tiên).
- **Công nợ phải thu/phải trả là số dư tức thời:** không theo khoảng ngày lọc — phản ánh số dư đến hiện tại.
- **Tồn quỹ âm:** dấu hiệu thiếu bút toán thu hoặc sai kỳ — kiểm tra Sổ quỹ tiền mặt / Sổ tài khoản ngân hàng.

## Báo cáo liên quan

- **Sổ Cái (S03b-DN)** và **Sổ chi tiết tài khoản**: truy nguồn từng con số trên dashboard.
- **Công nợ phải thu / phải trả**: chi tiết theo khách hàng / nhà cung cấp.
- **Báo cáo tài chính (B01/B02/B03-DN)**: số liệu chính thức theo TT99/2025.
- **Dự báo dòng tiền**: nối tiếp biểu đồ Dòng tiền sang dự báo tương lai.

## FAQ

**Q: Vì sao Tổng Doanh Thu trên dashboard khác với B02-DN?**
**A:** Dashboard tính nhanh theo phát sinh Có TK 511 trong khoảng ngày; B02-DN áp dụng đầy đủ quy tắc kết chuyển và loại trừ bút toán khóa sổ theo TT99/2025. Khi cần con số chính xác để báo cáo, dùng B02-DN.

**Q: Đổi mức thời gian Tháng/Quý/Năm/Tuần ảnh hưởng gì?**
**A:** Chỉ thay đổi cách chia trục thời gian của 2 biểu đồ xu hướng (Doanh thu–Chi phí, Dòng tiền). Các chỉ số KPI và biểu đồ tròn không đổi theo lựa chọn này.

**Q: Dashboard có tự cập nhật khi có chứng từ mới không?**
**A:** Dashboard tải lại số liệu khi mở hoặc khi đổi bộ lọc. Để theo dõi giao dịch tiền mặt/ngân hàng cập nhật liên tục trong ngày, dùng các báo cáo Phiếu thu/Phiếu chi (có chế độ tự cập nhật).

**Q: Số liệu chỉ gồm chứng từ đã duyệt hay cả nháp?**
**A:** Chỉ gồm chứng từ **đã ghi sổ** (đã duyệt). Chứng từ nháp chưa sinh bút toán nên không xuất hiện trên dashboard.
