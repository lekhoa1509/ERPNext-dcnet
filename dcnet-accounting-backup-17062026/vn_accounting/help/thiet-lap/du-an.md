---
title: Dự án
order: 7
summary: Khai báo dự án/công trình làm chiều phân tích theo hợp đồng — nền tảng cho giá thành công trình xây lắp (chuỗi 627 → 154 → 632).
---

## Mục đích

**Dự án** là chiều phân tích theo từng công trình/hợp đồng. Gắn dự án vào chứng từ giúp tập hợp chi phí, doanh thu và tính giá thành cho từng công trình — đặc biệt quan trọng với doanh nghiệp **xây lắp / thi công** theo TT99/2025 (chuỗi tập hợp chi phí TK 627 → 154 → 632).

Phân hệ đã bổ sung các trường riêng cho công trình xây lắp: *Dự án Xây lắp?*, *Giá trị hợp đồng*, *Giai đoạn thi công* (Chuẩn bị / Thi công / Hoàn thiện / Bàn giao / Bảo hành), *% Khối lượng nghiệm thu lũy kế*.

## Khi nào dùng

- **Khi nhận một công trình/hợp đồng mới:** tạo Dự án để bắt đầu tập hợp chi phí.
- **Trong suốt thi công:** gắn dự án vào hóa đơn mua, phiếu nhập xuất kho, phiếu xuất kho, đề nghị thanh toán để chi phí chảy vào TK 154 của công trình.
- **Khi xuất hóa đơn nghiệm thu từng đợt:** ghi nhận doanh thu + giá vốn (TK 632) theo dự án.
- **Khi đóng công trình:** kiểm tra số dư TK 154 của dự án về 0.

## Cách thực hiện

1. Mở **Dự án** trên menu Thiết lập.
2. Bấm **+ Thêm**:
   - **Tên dự án.**
   - **Dự án Xây lắp?** — bật nếu là công trình xây lắp (kích hoạt chuỗi giá thành 627→154→632).
   - **Giá trị hợp đồng**, **Giai đoạn thi công**, **% Khối lượng nghiệm thu lũy kế** (cập nhật theo tiến độ).
3. Lưu. Khi nhập chứng từ, chọn dự án cho từng dòng. Nếu bật *Hiện chọn giai đoạn ngay trên chứng từ* trong [Cài đặt kế toán](cai-dat-ke-toan.md), có thể gắn cả giai đoạn ngay lúc nhập.

## Định khoản tự động

Danh mục Dự án **không tự sinh bút toán** — nó là chiều phân tích. Tuy nhiên, khi gắn dự án vào chứng từ, các phân hệ giá thành công trình sinh bút toán theo TK cấu hình ở [Cài đặt kế toán](cai-dat-ke-toan.md):

| Nghiệp vụ | TK Nợ | TK Có | Ghi chú |
|---|---|---|---|
| Tập hợp chi phí trực tiếp công trình | 154 (theo dự án) | 152/331/334... | Vật tư, dịch vụ, nhân công |
| Lương kỹ sư on-site (gắn dự án) | 154 (theo dự án) | 622 | Sinh khi phiếu lương gắn dự án ghi sổ |
| Phân bổ chi phí gián tiếp cuối kỳ | 154 (theo dự án) | 627 | Theo tỷ lệ phân bổ |
| Ghi nhận giá vốn khi xuất HĐ đợt | 632 | 154 (theo dự án) | Recognize doanh thu/giá vốn |
| Đóng công trình (write-off chênh) | 642 (hoặc 632) | 154 (theo dự án) | Nếu còn dư sau quyết toán |

> Doanh nghiệp dịch vụ thuần (không thi công) có thể hạch toán chi phí thẳng vào TK 642 mà không qua 154; chỉ bật *Dự án Xây lắp?* cho công trình thực sự cần tập hợp giá thành.

## Tình huống đặc biệt & cảnh báo

- **Số dư TK 154 của dự án phải = 0 khi đóng công trình.** Nếu còn dư sau quyết toán, write-off phần chênh (TK 642 hoặc 632) — xem báo cáo giá thành theo dự án ở phân hệ Giá thành.
- **TK 627 bắt buộc với xây lắp theo TT99/2025** — không hạch toán chi phí gián tiếp công trình thẳng vào 642. Chuỗi đúng: 627 → 154 → 632.
- **Gắn dự án ở dòng chứng từ, không chỉ ở đầu chứng từ.** Khi đặt dự án ở phần đầu (header) sau khi đã có dòng, các dòng cũ có thể không tự cập nhật — kiểm tra lại từng dòng. Báo cáo giá thành ưu tiên dự án ghi ở đầu chứng từ, sau đó mới đến dòng.
- **% nghiệm thu lũy kế** là số liệu quản trị do người dùng cập nhật — không tự tính từ hóa đơn.

## Báo cáo liên quan

- [Trung tâm chi phí](trung-tam-chi-phi.md) — chiều phân tích theo bộ phận.
- [Cài đặt kế toán](cai-dat-ke-toan.md) — nhóm Giá thành công trình (TK 154/627/632/642/622).
- Phân hệ **Giá thành** — báo cáo lãi/lỗ và giá thành theo dự án.

## FAQ

**Q: Tôi không làm xây lắp, có cần tạo Dự án không?**
**A:** Không bắt buộc. Dự án hữu ích khi cần theo dõi chi phí/doanh thu theo công trình hoặc hợp đồng cụ thể. Doanh nghiệp dịch vụ thuần có thể bỏ qua hoặc chỉ dùng cho hợp đồng lớn.

**Q: Bật "Dự án Xây lắp?" thì khác gì?**
**A:** Đánh dấu công trình thuộc diện tập hợp giá thành xây lắp, để các báo cáo và chuỗi định khoản 627→154→632 xử lý đúng. Công trình không bật cờ này được xem như dự án phân tích thông thường.

**Q: Vì sao gắn dự án ở đầu hóa đơn mà chi phí không vào đúng công trình?**
**A:** Khi gắn dự án ở đầu chứng từ sau khi đã nhập dòng, các dòng có thể chưa cập nhật chiều phân tích. Hãy gắn dự án cho từng dòng, hoặc gắn ở đầu trước khi nhập dòng. Báo cáo lấy ưu tiên dự án ở đầu chứng từ.
