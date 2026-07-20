---
section: Thiết lập
title: Tổng quan Thiết lập
summary: Phân hệ Thiết lập — khai báo TK mặc định, ngưỡng nghiệp vụ, chiều phân tích, năm/kỳ kế toán, mẫu hợp đồng và quy tắc hoa hồng cho toàn hệ thống kế toán.
---

## Mục đích

Phân hệ **Thiết lập** là nơi khai báo nền tảng cho toàn bộ hệ thống Kế toán Việt Nam: hệ thống tài khoản (cây TK theo TT99/2025), tài khoản mặc định và ngưỡng nghiệp vụ, chiều phân tích quản trị (trung tâm chi phí, dự án), khung thời gian (năm tài chính, kỳ kế toán), quy tắc kho, cùng cấu hình cho hai phân hệ đặc thù của DCNET là **Hợp đồng** và **PAKD (phương án kinh doanh)**.

Đặc điểm chung của phân hệ này: **hầu hết các mục không tự sinh bút toán** — chúng **quyết định TK và quy tắc** mà các phân hệ nghiệp vụ khác (Tiền mặt, Kho, Giá thành, Hợp đồng, PAKD, Kết chuyển cuối kỳ...) dùng khi ghi sổ. Vì vậy đây là phân hệ kế toán trưởng cần thiết lập đúng **trước tiên** khi triển khai.

## Khi nào dùng

- **Khi mới triển khai:** khởi tạo cây tài khoản, năm tài chính, các TK mặc định và ngưỡng nghiệp vụ.
- **Khi chính sách thay đổi:** đổi TK doanh thu hợp đồng, tỷ lệ khấu trừ TNCN hoa hồng, ngưỡng TSCĐ, mẫu thuế...
- **Đầu kỳ/cuối kỳ:** tạo năm tài chính mới, chốt kỳ kế toán.
- **Khi cần kiểm soát:** lập ngân sách, phân quyền truy cập phân hệ.

## Cách thực hiện

Cấu trúc menu **Thiết lập** gồm các mục:

| # | Mục | Loại | Mô tả ngắn |
|---|---|---|---|
| 1 | Mẫu hợp đồng | Danh mục | Mẫu hợp đồng/phụ lục (.docx → biến điền → duyệt phiên bản) |
| 2 | Cây tài khoản | Danh mục | Hệ thống tài khoản TT99/2025 (khởi tạo, cấp cha-con, loại TK) |
| 3 | Cài đặt Hợp đồng | Cấu hình | TK doanh thu, mẫu thuế VAT, lịch thu, ánh xạ chi nhánh-TTCP |
| 4 | Import cây tài khoản | Công cụ | Nạp cả cây TK từ file 8 cột |
| 5 | Mẫu quy tắc hoa hồng | Danh mục | Thành phần + tỷ lệ hoa hồng PAKD theo phạm vi |
| 6 | Năm tài chính | Danh mục | Khung năm kế toán (01/01–31/12) |
| 7 | Cài đặt PAKD | Cấu hình | TK hoa hồng nội bộ/ngoài, khấu trừ TNCN, ngày chốt, nhắc duyệt |
| 8 | Kỳ kế toán | Danh mục | Khóa sổ theo tháng/quý |
| 9 | Lịch sử nhắc duyệt PAKD | Nhật ký | Vết các lần nhắc duyệt PAKD |
| 10 | Trung tâm chi phí | Danh mục | Chiều phân tích theo bộ phận/chi nhánh |
| 11 | Dự án | Danh mục | Chiều phân tích theo công trình (xây lắp 627→154→632) |
| 12 | Ngân sách | Danh mục | Dự toán + so sánh ngân sách-thực tế |
| 13 | Cài đặt kho | Cấu hình | Phương pháp tính giá xuất, tồn âm, TK kho |
| 14 | Cài đặt ngân hàng | Cấu hình | Thiết lập import sao kê, đối soát và xử lý giao dịch ngân hàng |
| 15 | Cài đặt kế toán | Cấu hình | TK mặc định + ngưỡng cho toàn phân hệ (quan trọng nhất) |

> Một số mục dùng chung với phân hệ khác: **Cây tài khoản** (cũng ở Danh mục), **Kỳ kế toán** (cũng ở Tổng hợp), **Cài đặt PAKD** và **Lịch sử nhắc duyệt PAKD** (cũng ở Kho). Cùng một danh mục/cấu hình — chỉ khác góc nhìn theo phân hệ.

### Quy trình điển hình (triển khai mới)

1. **Khởi tạo cây tài khoản:** [Import cây tài khoản](import-cay-tai-khoan.md) từ file TT99/2025, rồi tinh chỉnh trong [Cây tài khoản](cay-tai-khoan.md) (tách TK ngân hàng, nhóm dịch vụ; đặt "Loại TK" cho TK lá).
2. **Tạo khung thời gian:** [Năm tài chính](nam-tai-chinh.md) (và năm trước nếu nhập số dư đầu kỳ).
3. **Cấu hình TK mặc định:** [Cài đặt kế toán](cai-dat-ke-toan.md) — TK kết chuyển 911/4212/4211/821, giá thành 154/627/632, kiểm kê quỹ, thanh lý, hoãn lại; ngưỡng TSCĐ 30 triệu.
4. **Cấu hình kho và ngân hàng:** [Cài đặt kho](cai-dat-kho.md) — phương pháp tính giá xuất, tồn âm; [Cài đặt ngân hàng](cai-dat-ngan-hang.md) — import sao kê và đối soát.
5. **Dựng chiều phân tích:** [Trung tâm chi phí](trung-tam-chi-phi.md), [Dự án](du-an.md) theo cơ cấu tổ chức/công trình.
6. **Cấu hình phân hệ đặc thù:** [Cài đặt Hợp đồng](cai-dat-hop-dong.md) + [Mẫu hợp đồng](mau-hop-dong.md); [Cài đặt PAKD](cai-dat-pakd.md) + [Mẫu quy tắc hoa hồng](mau-quy-tac-hoa-hong.md).
7. **Lập ngân sách** (nếu cần kiểm soát chi): [Ngân sách](ngan-sach.md).
8. **Vận hành định kỳ:** kết chuyển cuối kỳ → đối chiếu → khóa [Kỳ kế toán](ky-ke-toan.md).

### Liên kết tới các bài hướng dẫn chi tiết

- **TK mặc định & ngưỡng:** [Cài đặt kế toán](cai-dat-ke-toan.md).
- **Hệ thống tài khoản:** [Cây tài khoản](cay-tai-khoan.md), [Import cây tài khoản](import-cay-tai-khoan.md).
- **Khung thời gian:** [Năm tài chính](nam-tai-chinh.md), [Kỳ kế toán](ky-ke-toan.md).
- **Chiều phân tích & ngân sách:** [Trung tâm chi phí](trung-tam-chi-phi.md), [Dự án](du-an.md), [Ngân sách](ngan-sach.md).
- **Kho & ngân hàng:** [Cài đặt kho](cai-dat-kho.md), [Cài đặt ngân hàng](cai-dat-ngan-hang.md).
- **Hợp đồng:** [Cài đặt Hợp đồng](cai-dat-hop-dong.md), [Mẫu hợp đồng](mau-hop-dong.md).
- **PAKD:** [Cài đặt PAKD](cai-dat-pakd.md), [Mẫu quy tắc hoa hồng](mau-quy-tac-hoa-hong.md), [Lịch sử nhắc duyệt PAKD](lich-su-nhac-duyet-pakd.md).

## Định khoản tự động

Phân hệ Thiết lập **không trực tiếp tạo bút toán**. Vai trò của nó là **khai báo TK mặc định và quy tắc** để các phân hệ khác sinh bút toán đúng:

| Cấu hình | Phân hệ tiêu thụ | TK quyết định |
|---|---|---|
| Cài đặt kế toán | Tiền mặt, TSCĐ, Giá thành, Kết chuyển, Hoãn lại | 911/4212/4211/821, 154/627/632, 811/711, 3387/242... |
| Cài đặt Hợp đồng | Hợp đồng | Doanh thu 511x, thuế 3331 |
| Cài đặt PAKD | PAKD | Hoa hồng 6427/334/3388/3335/3338 |
| Cài đặt kho | Kho | Giá vốn 632, tồn 15x |
| Cài đặt ngân hàng | Ngân hàng | Tolerance đối soát, TK phí/chênh lệch ngân hàng |
| Cây tài khoản | Toàn hệ thống | Tất cả TK |

## Tình huống đặc biệt & cảnh báo

- **Đặt sai TK ở Thiết lập kéo theo bút toán sai ở mọi phân hệ.** Rà soát kỹ TK mặc định trước khi cho nhập liệu.
- **Sửa TK mặc định KHÔNG sửa lùi bút toán đã ghi sổ** — chỉ áp dụng cho lần sinh kế tiếp.
- **Theo TT99/2025** (hiệu lực 2026-01-01): TK 242 "Chi phí chờ phân bổ", bỏ TK 142, ngưỡng TSCĐ 30 triệu, xây lắp bắt buộc TK 627. Khởi tạo mới theo TT99/2025, không mặc định TT200.
- **Ngân sách phải ghi sổ (duyệt) + bật phân bổ đều** mới chạy báo cáo so sánh.
- **Khóa kỳ kế toán** chỉ chặn ghi sổ — không thay cho kết chuyển TK 911 (kết chuyển trước, khóa sau).
- **Mục dùng chung** (Cây tài khoản, Kỳ kế toán, Cài đặt PAKD, Lịch sử nhắc duyệt) chỉ có một bản dữ liệu — sửa ở phân hệ nào cũng là sửa cùng một nơi.

## Báo cáo liên quan

- Phân hệ **Danh mục** — tra cứu khách hàng/nhà cung cấp/mặt hàng và cây TK hằng ngày.
- Phân hệ **Tổng hợp** — kết chuyển cuối kỳ, chốt sổ, số dư đầu kỳ.
- Phân hệ **Báo cáo tài chính** — B01/B02/B03-DN theo TT99/2025.
- Phân hệ **Hợp đồng & PAKD**, **Kho**, **Giá thành** — nơi các cấu hình ở đây phát huy tác dụng.

## FAQ

**Q: Tôi nên thiết lập gì đầu tiên khi triển khai?**
**A:** Theo thứ tự: (1) Cây tài khoản (import + tinh chỉnh), (2) Năm tài chính, (3) Cài đặt kế toán (TK mặc định + ngưỡng), (4) Cài đặt kho và ngân hàng, (5) Trung tâm chi phí/Dự án, (6) Cài đặt Hợp đồng/PAKD. Đặt đúng nền tảng trước khi nhập chứng từ.

**Q: Vì sao nhiều mục "Cài đặt" mà không thấy nó tạo bút toán nào?**
**A:** Các mục Thiết lập chỉ **quyết định TK và quy tắc**. Bút toán phát sinh ở phân hệ nghiệp vụ (Tiền mặt, Kho, Hợp đồng, PAKD...) dựa trên cấu hình tại đây.

**Q: Cài đặt kế toán và Cài đặt PAKD khác nhau thế nào?**
**A:** Cài đặt kế toán quản TK mặc định cho phần lớn phân hệ (kết chuyển, giá thành, kiểm kê, thanh lý, hoãn lại). Cài đặt PAKD quản riêng TK hoa hồng và quy tắc PAKD — hai nơi độc lập, không thay thế nhau.

**Q: Đổi hệ thống tài khoản từ TT200 sang TT99/2025 thì làm gì?**
**A:** Cập nhật cây tài khoản (đổi tên TK 242, bỏ 142, cấu trúc TK con) và rà lại các TK mặc định trong Cài đặt kế toán/Hợp đồng/PAKD. Lưu ý số dư cũ vẫn theo bút toán đã ghi.
