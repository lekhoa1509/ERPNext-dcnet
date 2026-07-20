---
title: Cài đặt kế toán
order: 1
summary: Trung tâm cấu hình TK mặc định và ngưỡng nghiệp vụ cho toàn phân hệ Kế toán Việt Nam — quyết định TK các phân hệ khác dùng khi sinh bút toán.
---

## Mục đích

**Cài đặt kế toán** là bản cấu hình trung tâm (một bản duy nhất cho công ty) khai báo **tài khoản mặc định** và **ngưỡng nghiệp vụ** mà mọi phân hệ khác (Tiền mặt, Tiền gửi/Vay, Giá thành công trình, Kết chuyển cuối kỳ, TSCĐ/CCDC, Doanh thu/Chi phí hoãn lại...) dùng làm điểm xuất phát khi sinh bút toán tự động.

Bản thân màn hình này **không tạo bút toán** — nó chỉ **quyết định** các TK Nợ/Có mà những chức năng khác sẽ dùng. Đặt sai TK ở đây sẽ kéo theo bút toán sai ở mọi phân hệ liên quan, nên đây là màn hình kế toán trưởng cần kiểm tra đầu tiên khi triển khai.

Dành cho: kế toán trưởng / quản trị kế toán (vai trò Accounts Manager hoặc System Manager có quyền sửa; Accounts User chỉ xem).

## Khi nào dùng

- **Khi mới triển khai hệ thống:** rà soát toàn bộ TK mặc định theo hệ thống tài khoản (TT99/2025) của công ty trước khi cho kế toán viên nhập liệu.
- **Khi đổi hệ thống tài khoản / tách TK chi tiết:** ví dụ tách 632 thành 632a/632b — cập nhật lại các ô tương ứng.
- **Khi cấu hình kết chuyển cuối kỳ (TK 911):** khai TK 911/4212/4211/821 và danh sách TK doanh thu/chi phí cần kết chuyển trước khi chạy trợ lý kết chuyển.
- **Khi đặt ngưỡng nghiệp vụ:** ngưỡng ghi nhận TSCĐ (30 triệu), ngưỡng cần duyệt khi thanh lý/bàn giao tài sản, ngưỡng cảnh báo tồn quỹ tối thiểu, số ngày nhắc đáo hạn tiền gửi/khoản vay.
- **Khi phân quyền truy cập phân hệ:** bật/tắt giới hạn vai trò được vào phân hệ Kế toán Việt Nam.

## Cách thực hiện

1. Mở mục **Cài đặt kế toán** trên menu Thiết lập. Màn hình chia thành nhiều nhóm (section); mỗi nhóm ứng với một phân hệ.
2. Điền/chọn TK ở từng ô (mỗi ô là một liên kết tới một tài khoản trong cây tài khoản). Phần mô tả dưới mỗi ô đã ghi sẵn **số hiệu TK gợi ý** theo TT99/2025.
3. Bấm **Lưu** (Ctrl+S). Hệ thống áp dụng ngay cho lần sinh bút toán kế tiếp của các phân hệ.

### Các nhóm cấu hình và TK liên quan

**1. Phân quyền truy cập phân hệ**
- *Bật giới hạn truy cập theo vai trò* (mặc định bật): chỉ người có ít nhất 1 vai trò trong "Vai trò được phép" mới vào được phân hệ. Mặc định: Accounts User, Accounts Manager, Auditor.

**2. Tiền gửi & Khoản vay (Term Deposits & Bank Loans)**

| Ô cấu hình | TK gợi ý | Dùng cho |
|---|---|---|
| TK tiền gửi có kỳ hạn | 1281 | Gốc tiền gửi |
| TK doanh thu lãi tiền gửi | 515 | Lãi tiền gửi |
| TK khoản vay phải trả | 3411 | Gốc khoản vay |
| TK chi phí lãi vay | 635 | Lãi vay |

**3. TK trích trước (Accrual)**

| Ô cấu hình | TK gợi ý | Dùng cho |
|---|---|---|
| TK lãi tiền gửi phải thu (dồn tích) | 1388 | Lãi tiền gửi chưa thu |
| TK lãi vay phải trả (dồn tích) | 335 | Lãi vay chưa trả |

**4. Cảnh báo đáo hạn:** số ngày trước đáo hạn để nhắc tiền gửi (mặc định 7) và khoản vay (mặc định 7).

**5. Kiểm kê quỹ (Cash Count)**

| Ô cấu hình | TK gợi ý | Dùng cho |
|---|---|---|
| TK thừa quỹ | 3381 | Tiền thừa chờ xử lý |
| TK thiếu quỹ | 1381 | Tiền thiếu chờ xử lý |
| TK phải thu nhân viên | 1388 | Quy thiếu cho thủ quỹ |
| TK chi phí quản lý | 6425 | Xử lý thiếu vào chi phí |
| TK thu nhập khác | 711 | Xử lý thừa vào thu nhập |

**6. Thanh lý tài sản (Asset Disposal)**

| Ô cấu hình | TK gợi ý | Dùng cho |
|---|---|---|
| TK lỗ thanh lý | 811 | Chi phí khác (lỗ thanh lý) |
| TK thu nhập thanh lý | 711 | Thu nhập khác (lãi thanh lý) |

**7. Dự báo dòng tiền:** *Ngưỡng tồn quỹ tối thiểu* (mặc định 500 triệu) — mức cảnh báo trên trang Dự báo dòng tiền.

**8. Phân quyền TSCĐ & CCDC + Ngưỡng giá trị**
- *Ngưỡng ghi nhận TSCĐ* (mặc định **30 triệu** theo TT99/2025): tài sản dưới ngưỡng coi là công cụ dụng cụ.
- *Ngưỡng thanh lý cần duyệt* (mặc định 50 triệu); *Ngưỡng bàn giao cần đồng ký* (mặc định 100 triệu).
- *Ma trận phân quyền*: bảng quyền theo loại chứng từ và vai trò; bấm **Khôi phục mặc định** để nạp lại bộ quyền chuẩn.

**9. Doanh thu / Chi phí hoãn lại**

| Ô cấu hình | TK gợi ý | Dùng cho |
|---|---|---|
| TK doanh thu chưa thực hiện | 3387 | Lịch phân bổ doanh thu hoãn lại |
| TK chi phí chờ phân bổ | 242 | Lịch phân bổ chi phí hoãn lại |

> TT99/2025 đổi tên TK 242 thành **"Chi phí chờ phân bổ"** và bỏ TK 142.

**10. Kết chuyển cuối kỳ (TK 911)** — quan trọng nhất cho khóa sổ

| Ô cấu hình | TK gợi ý | Vai trò |
|---|---|---|
| TK xác định kết quả kinh doanh | 911 | Trung gian tập hợp doanh thu/chi phí |
| TK lợi nhuận chưa phân phối kỳ này | 4212 | Nhận lãi/lỗ sau kết chuyển |
| TK lợi nhuận chưa phân phối năm trước | 4211 | Lũy kế năm trước (mã 421 trên B01-DN) |
| TK chi phí thuế TNDN | 821 | Chỉ kết chuyển ở kỳ cuối năm |
| Danh sách TK doanh thu kết chuyển | 511, 512, 515, 711 | Nợ các TK này / Có 911 |
| Danh sách TK chi phí kết chuyển hàng kỳ | 632, 635, 641, 642, 811 | Nợ 911 / Có các TK này |
| Sai số cho phép khi cân đối | 1 VNĐ | Dung sai làm tròn khi kết chuyển |

**11. Giá thành công trình (xây lắp)** — chuỗi 627 → 154 → 632

| Ô cấu hình | TK gợi ý | Vai trò |
|---|---|---|
| TK tập hợp chi phí công trình (WIP) | 154 | Gom chi phí trực tiếp công trình |
| TK gom chi phí gián tiếp (Overhead) | 627 | Chi phí sản xuất chung chờ phân bổ |
| TK giá vốn công trình (COGS) | 632 | Ghi nhận khi xuất hóa đơn đợt |
| TK write-off khi đóng công trình | 642 | Chi phí không phân bổ (có thể chọn 632) |
| TK lương trực tiếp | 622 | Lương kỹ sư on-site (Nợ 154 / Có 622) |

- *Hiện chọn giai đoạn ngay trên chứng từ* (mặc định bật): cho phép gắn giai đoạn công trình ngay khi nhập hóa đơn mua / phiếu nhập xuất kho / phiếu xuất kho / đề nghị thanh toán.

## Định khoản tự động

Màn hình này **không tự sinh bút toán**. Vai trò của nó là **quyết định TK mặc định** mà các phân hệ khác dùng khi sinh bút toán. Ví dụ:

| Phân hệ sinh bút toán | TK lấy từ Cài đặt kế toán |
|---|---|
| Kiểm kê quỹ (xử lý thừa/thiếu) | 3381 / 1381 / 1388 / 6425 / 711 |
| Thanh lý TSCĐ | 811 (lỗ) / 711 (lãi) |
| Lịch phân bổ doanh thu/chi phí hoãn lại | 3387 / 242 |
| Trợ lý kết chuyển cuối kỳ | 911 / 4212 / 4211 / 821 + danh sách 5xx/6xx |
| Giá thành công trình | 154 / 627 / 632 / 642 / 622 |
| Tiền gửi/Khoản vay (lãi dồn tích) | 1281 / 515 / 3411 / 635 / 1388 / 335 |

## Tình huống đặc biệt & cảnh báo

- **Sửa TK ở đây KHÔNG sửa lùi các bút toán đã ghi sổ.** Chỉ áp dụng cho lần sinh bút toán kế tiếp. Muốn sửa bút toán cũ phải điều chỉnh thủ công.
- **Các ô bắt buộc cho kết chuyển:** TK 911, 4212, 4211, 821, danh sách TK doanh thu và TK chi phí là bắt buộc — nếu trống, trợ lý kết chuyển cuối kỳ sẽ không chạy được.
- **Đừng thêm 821 vào danh sách chi phí kết chuyển hàng kỳ.** TK 821 được hệ thống xử lý riêng: chỉ kết chuyển ở kỳ cuối năm tài chính (tự phát hiện), kỳ thường để tích lũy cả năm.
- **Ngưỡng TSCĐ 30 triệu theo TT99/2025:** tài sản dưới ngưỡng phải hạch toán là CCDC (công cụ dụng cụ) qua TK 153/242, không vào TK 211.
- **Chỉ Accounts Manager / System Manager sửa được.** Accounts User chỉ xem để tra TK mặc định.
- **TK chọn phải tồn tại trong cây tài khoản của đúng công ty.** Nếu cây tài khoản chưa có TK con (ví dụ 1281, 3411) thì phải tạo trong Cây tài khoản trước.

## Báo cáo liên quan

- [Cây tài khoản](cay-tai-khoan.md) — nơi tạo/sửa các TK được chọn ở đây.
- [Cài đặt PAKD](cai-dat-pakd.md) — cấu hình TK hoa hồng (PAKD) riêng, độc lập với màn hình này.
- [Cài đặt Hợp đồng](cai-dat-hop-dong.md) — cấu hình TK doanh thu mặc định cho hóa đơn hợp đồng.
- [Trung tâm chi phí](trung-tam-chi-phi.md), [Dự án](du-an.md) — chiều phân tích dùng cùng chuỗi 627→154.

## FAQ

**Q: Tại sao có nhiều ô TK trùng số hiệu (711 ở cả Kiểm kê quỹ và Thanh lý)?**
**A:** Mỗi ô là TK mặc định cho một nghiệp vụ cụ thể. Trùng số hiệu là bình thường vì cùng một TK (711 - Thu nhập khác) phục vụ nhiều nghiệp vụ. Đặt riêng từng ô để sau này nếu công ty tách TK chi tiết thì cấu hình được độc lập.

**Q: Tôi đổi TK giá vốn công trình từ 632 sang 632b, các bút toán cũ có đổi theo không?**
**A:** Không. Các bút toán đã ghi sổ giữ nguyên TK cũ; chỉ bút toán sinh sau khi lưu mới dùng TK mới. Nếu cần đồng bộ, phải điều chỉnh thủ công các bút toán cũ.

**Q: Phân hệ hoa hồng (PAKD) lấy TK từ màn hình này phải không?**
**A:** Không. Hoa hồng có màn hình cấu hình riêng — xem [Cài đặt PAKD](cai-dat-pakd.md). Màn hình Cài đặt kế toán không quản TK hoa hồng.

**Q: Vì sao bật/tắt "giới hạn truy cập theo vai trò" cần đăng nhập lại mới thấy?**
**A:** Danh sách phân hệ được nạp một lần khi đăng nhập. Sau khi đổi cấu hình vai trò, người dùng cần đăng xuất rồi đăng nhập lại để áp dụng.
