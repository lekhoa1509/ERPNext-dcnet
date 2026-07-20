---
title: Bảng cân đối số phát sinh
order: 9
summary: Bảng phẳng số dư đầu kỳ, phát sinh trong kỳ và số dư cuối kỳ của mọi tài khoản chi tiết, kèm dòng tổng cộng kiểm tra cân đối.
---

## Mục đích

**Bảng cân đối số phát sinh** liệt kê theo dạng bảng phẳng (theo Số TK tăng dần) số dư đầu kỳ, phát sinh trong kỳ và số dư cuối kỳ của mọi tài khoản chi tiết có hoạt động. Dòng cuối là Tổng cộng dùng để kiểm tra cân đối (tổng Nợ = tổng Có). Đây là báo cáo bắt buộc cuối kỳ tại Việt Nam (dạng cân đối tài khoản). Chỉ TRA CỨU, không tạo chứng từ.

## Khi nào dùng

- **Cuối tháng/quý/năm:** in báo cáo gửi giám đốc, nộp kèm Báo cáo tài chính.
- **Kiểm tra ghi sổ:** tổng phát sinh Nợ phải bằng tổng phát sinh Có → sổ sách cân.
- **Trước khi khoá sổ:** phát hiện tài khoản lệch dấu (tài sản dư Có, nợ phải trả dư Nợ).
- **Đối chiếu kiểm toán:** căn cứ rà soát biến động trong kỳ.

## Cách thực hiện

1. Mở **Tổng hợp → Bảng cân đối số phát sinh**.
2. Nhập bộ lọc: **Công ty** (bắt buộc), **Từ ngày / Đến ngày** (mặc định 1 tháng gần nhất).
3. Bấm **Chạy báo cáo** → bảng hiển thị từng tài khoản chi tiết (sắp theo Số TK), dòng cuối Tổng cộng in đậm.
4. Xuất PDF/Excel qua **Thực đơn → Tải về**.

### Các cột

| Cột | Ý nghĩa |
|---|---|
| Số TK / Tên tài khoản | Số hiệu và tên tài khoản chi tiết |
| Dư Nợ / Dư Có đầu kỳ | Số dư đầu kỳ tách hai phía |
| PS Nợ / PS Có trong kỳ | Tổng phát sinh Nợ / Có trong kỳ |
| Dư Nợ / Dư Có cuối kỳ | Số dư cuối kỳ tách hai phía |

## Định khoản tự động

Không tự định khoản — báo cáo tổng hợp số liệu từ Sổ Cái. Không tạo chứng từ.

## Tình huống đặc biệt & cảnh báo

- **Chỉ liệt kê tài khoản chi tiết có Số TK:** tài khoản nhóm và tài khoản không có account_number bị loại. Tài khoản không có số dư đầu kỳ và không phát sinh trong kỳ cũng bị bỏ qua (bảng gọn).
- **PS Nợ / PS Có là TỔNG mỗi phía trong kỳ**, không phải số dư. Một tài khoản hoạt động (VD 111) có cả PS Nợ và PS Có lớn — bình thường. Chỉ số dư cuối kỳ mới phản ánh trạng thái.
- **Kiểm tra cân:** dòng Tổng cộng — tổng PS Nợ phải bằng tổng PS Có. Lệch là sổ chưa cân (thường do bút toán nháp chưa ghi sổ hoặc bút toán ngoại tệ chưa quy đổi đúng).
- **Tài khoản lệch dấu:** tài sản (loại 1, 2) nên dư cuối Nợ; nguồn vốn/nợ phải trả (loại 3, 4) nên dư cuối Có; doanh thu/chi phí (5,6,7,8) cuối năm phải về 0 sau kết chuyển. Lệch dấu → kiểm tra.
- **Hiển thị "0" tất cả các cột:** thường do kỳ lọc nằm ngoài phạm vi có dữ liệu — đổi khoảng ngày.

> Phân hệ còn có một báo cáo cùng tên ở dạng cây theo hệ thống tài khoản (xem [Bảng cân đối số phát sinh — dạng cây](bang-can-doi-so-phat-sinh.md)). Bản dạng cây cho phép mở/đóng nhóm và lọc theo trung tâm chi phí / dự án; bản phẳng này nhẹ, sắp theo Số TK, tiện xuất Excel nộp kèm BCTC.

## Báo cáo liên quan

- [Bảng cân đối số phát sinh — dạng cây](bang-can-doi-so-phat-sinh.md): bản theo cây tài khoản, lọc theo TTCP/dự án.
- [Sổ cái (S03b-DN)](so-cai.md): chi tiết phát sinh một tài khoản.
- [Sổ nhật ký chung (S03a-DN)](so-nhat-ky-chung.md): mọi nghiệp vụ theo thời gian.
- [Phiếu kết chuyển định kỳ (911 → 4212)](phieu-ket-chuyen-dinh-ky.md): chạy trước khi lập báo cáo cuối kỳ.

## FAQ

**Q: Vì sao tổng PS Nợ khác tổng PS Có?**
**A:** Sổ chưa cân. Phần lớn do bút toán còn ở trạng thái Nháp (chưa ghi sổ), bút toán bị xóa thủ công, hoặc bút toán ngoại tệ chưa quy đổi theo đồng tiền gốc của công ty. Xem [Tài liệu tự động chờ duyệt](tai-lieu-tu-dong.md) để soát các bút toán nháp.

**Q: Tài khoản 511, 632 cuối năm vẫn còn số dư?**
**A:** Chưa kết chuyển. Doanh thu/chi phí cuối năm phải về 0 sau khi chạy [Phiếu kết chuyển định kỳ (911 → 4212)](phieu-ket-chuyen-dinh-ky.md).

**Q: Báo cáo này khác bản dạng cây thế nào?**
**A:** Bản này phẳng, mỗi dòng một tài khoản chi tiết, sắp theo Số TK, nhẹ và tiện xuất Excel. Bản dạng cây hiển thị cả tài khoản nhóm, mở/đóng được và lọc theo trung tâm chi phí/dự án.
