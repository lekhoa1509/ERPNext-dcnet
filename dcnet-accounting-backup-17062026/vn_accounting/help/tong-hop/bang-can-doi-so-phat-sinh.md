---
title: Bảng cân đối số phát sinh (dạng cây)
order: 13
summary: Bảng cân đối số phát sinh theo cây hệ thống tài khoản TT99/2025, mở/đóng từng nhóm, lọc theo trung tâm chi phí / dự án.
---

## Mục đích

**Bảng cân đối số phát sinh (dạng cây)** tổng hợp số dư đầu kỳ, phát sinh trong kỳ và số dư cuối kỳ của mọi tài khoản theo cấu trúc cây hệ thống tài khoản TT99/2025 — tài khoản tổng hợp (1, 11, 111...) ở trên, tài khoản chi tiết bên dưới, mở/đóng từng nhóm. Cho phép lọc theo trung tâm chi phí và dự án. Đây là báo cáo bắt buộc cuối kỳ tại Việt Nam. Chỉ TRA CỨU, không tạo chứng từ.

## Khi nào dùng

- **Cuối tháng/quý/năm:** in báo cáo gửi giám đốc + nộp kèm Báo cáo tài chính.
- **Kiểm tra ghi sổ:** tổng Nợ phải bằng tổng Có ở dòng cuối → sổ sách cân.
- **Giám sát theo bộ phận/dự án:** lọc theo trung tâm chi phí hoặc dự án.
- **Trước khi khoá sổ:** phát hiện tài khoản lệch dấu (tài sản dư Có, nợ phải trả dư Nợ).

## Cách thực hiện

1. Mở **Tổng hợp → Bảng cân đối số phát sinh** (bản dạng cây).
2. Nhập bộ lọc:
   - **Năm tài chính** + **Từ ngày / Đến ngày** (mặc định = năm tài chính hiện tại).
   - **Trung tâm chi phí** / **Dự án** (tùy chọn).
   - **Hiển thị tài khoản nhóm** — bật để thấy cả tài khoản tổng hợp (1, 11, 111).
   - **Hiển thị giá trị bằng không** — bật khi muốn rà cả tài khoản không phát sinh.
3. Bấm **Chạy báo cáo** → mở/đóng từng nhóm tài khoản trong cây.
4. Xuất PDF/Excel qua **Thực đơn → Tải về**.

### Sáu cột chính

| Cột | Ý nghĩa |
|---|---|
| Dư đầu kỳ Nợ / Có | Số dư đầu kỳ phía Nợ và phía Có |
| Phát sinh Nợ / Có | TỔNG các bút toán Nợ / Có trong kỳ (không phải số dư) |
| Dư cuối kỳ Nợ / Có | Số dư cuối kỳ phía Nợ và phía Có |

> **Lưu ý:** "Phát sinh Nợ / Có" là TỔNG MỖI PHÍA TRONG KỲ. Một tài khoản hoạt động (VD 111) có cả Phát sinh Nợ và Có cùng lớn — bình thường. Chỉ số dư cuối kỳ mới phản ánh trạng thái tại thời điểm in.

## Định khoản tự động

Không tự định khoản — báo cáo tổng hợp số liệu từ Sổ Cái. Không tạo chứng từ.

## Tình huống đặc biệt & cảnh báo

- **Cân bằng tổng:** dòng Tổng cộng — tổng Phát sinh Nợ phải bằng tổng Phát sinh Có. Lệch là sổ chưa cân (đa số do bút toán nháp chưa ghi sổ hoặc một chiều mất leg).
- **Tài khoản lệch dấu:** tài sản (loại 1) nên dư cuối Nợ; nguồn vốn + nợ phải trả (loại 3, 4) nên dư cuối Có; doanh thu (5, 7) và chi phí (6, 8) cuối năm phải về 0 sau kết chuyển.
- **Kế toán đầu năm:** Dư đầu kỳ Nợ tổng phải bằng Dư đầu kỳ Có tổng. Lệch là số dư đầu kỳ chưa cân — kiểm tra Opening Balance.
- **Hiển thị "0" hết:** thường do kỳ lọc nằm ngoài phạm vi có dữ liệu — đổi Năm tài chính / khoảng ngày.
- **Đổi tên cột so với bản gốc hệ thống:** "Ghi nợ/Ghi có" của bản dịch gốc dễ hiểu nhầm là số dư phía Nợ/Có; bản này đổi thành "Phát sinh" cho đúng ngữ kế toán Việt Nam (tổng bút toán xảy ra trong kỳ).

## Báo cáo liên quan

- [Bảng cân đối số phát sinh (phẳng)](trial-balance.md): bản phẳng theo Số TK, nhẹ, tiện xuất Excel.
- [Sổ cái (S03b-DN)](so-cai.md): chi tiết phát sinh một tài khoản.
- [Tài liệu tự động chờ duyệt](tai-lieu-tu-dong.md): soát bút toán nháp khi tổng lệch.
- [Phiếu kết chuyển định kỳ (911 → 4212)](phieu-ket-chuyen-dinh-ky.md): kết chuyển trước khi lập báo cáo cuối kỳ.

## FAQ

**Q: Vì sao nhiều tài khoản có cả Phát sinh Nợ và Phát sinh Có?**
**A:** Vì đó là TỔNG phát sinh mỗi phía trong kỳ. Tài khoản hoạt động (tiền, công nợ) tự nhiên có cả hai chiều. Không phải lỗi.

**Q: Tổng Phát sinh Nợ ≠ Phát sinh Có?**
**A:** Sổ chưa cân. Phần lớn do bút toán còn Nháp, bút toán bị xóa thủ công, hoặc bút toán ngoại tệ chưa quy đổi theo đồng tiền gốc. Xem [Tài liệu tự động chờ duyệt](tai-lieu-tu-dong.md).

**Q: Bản dạng cây khác bản phẳng thế nào?**
**A:** Bản dạng cây hiển thị cả tài khoản nhóm, mở/đóng được, lọc theo trung tâm chi phí/dự án. Bản phẳng chỉ liệt kê tài khoản chi tiết theo Số TK, gọn, tiện xuất Excel nộp kèm BCTC.
