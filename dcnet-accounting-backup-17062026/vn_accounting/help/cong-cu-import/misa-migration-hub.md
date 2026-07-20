---
title: Trung tâm chuyển dữ liệu Misa
order: 1
summary: Màn hình thực hiện quy trình 4 bước đưa dữ liệu kế toán từ Misa cũ vào hệ thống, kèm kiểm tra cân đối sau import.
---

## Mục đích

**Trung tâm chuyển dữ liệu Misa** là màn hình công cụ giúp đưa toàn bộ dữ liệu kế toán từ phần mềm **Misa** (Misa SME) vào hệ thống mới khi doanh nghiệp chuyển đổi phần mềm. Màn hình dẫn dắt kế toán qua **4 bước**: Tải lên file → Phân tích → Duyệt → Tạo vào hệ thống. Đối tượng dùng là kế toán tổng hợp / kế toán trưởng phụ trách việc khởi tạo hệ thống.

Đây là **công cụ một lần** dùng lúc go-live. Quy trình tóm lại: đọc file Misa → ánh xạ tài khoản → bơm chứng từ (dựng lại bút toán lịch sử) → kiểm tra → đối chiếu.

## Khi nào dùng

- Lần đầu đưa hệ thống vào hoạt động, cần mang số dư đầu kỳ + toàn bộ phát sinh từ Misa sang.
- Sau khi đã kết xuất đầy đủ các file Excel cần thiết từ Misa.
- Khi muốn import thử trên một công ty, đối chiếu cân đối, rồi mới chính thức sử dụng.

## Cách thực hiện

Mở màn hình từ menu **Công cụ Import → Trung tâm chuyển dữ liệu Misa**. Nút **"Lịch sử"** ở góc trên mở danh sách các đợt đã chạy.

**Bước 1 — Tải lên file**
1. Tạo một **đợt chuyển dữ liệu** mới: chọn **Công ty** (đích nhận dữ liệu), đặt **tiêu đề đợt** (ví dụ "Import Misa T1/2026"), và nhập **Ngày OB (đầu kỳ)**.
   - Lưu ý ngày OB: file "đầu kỳ" của Misa không kèm ngày, nên bắt buộc nhập. Ví dụ đầu kỳ 2026 → chọn 31/12/2025.
2. Kéo–thả hoặc chọn các file Excel (.xlsx/.xls). Với mỗi file, chọn đúng **Loại** (Nhật ký chung, Bảng kê bán ra, Bảng kê mua vào, Hệ thống tài khoản, Khách hàng, Nhà cung cấp, Hàng hóa, Kho, Phòng ban, Trung tâm chi phí, Công trình, Phân loại tài sản cố định, Phân loại công cụ dụng cụ…).
3. Trên màn hình có sẵn hướng dẫn **"Thứ tự migration khuyến nghị"** — nên tuân theo để tránh thiếu dữ liệu.

**Bước 2 — Phân tích**
4. Bấm **"Bắt đầu phân tích"**. Hệ thống đọc nội dung từng file, tìm dòng tiêu đề, tách dòng, tự phân loại. Bước này chỉ "đọc hiểu" — chưa ghi gì vào sổ, có thể chạy lại an toàn. File lớn (Nhật ký chung cả năm ~90.000 dòng) có thể mất vài phút; thanh tiến độ hiển thị số dòng đã đọc.

**Bước 3 — Duyệt**
5. Xem từng nhóm dữ liệu theo các tab giai đoạn. Xử lý các dòng **Trùng / Không hợp lệ** (thường là dòng "Tổng", dòng phụ đề do Misa xuất kèm — có thể bỏ qua hàng loạt).
6. Nếu hệ thống đang có **dữ liệu mẫu**, màn hình hiện cảnh báo và đề nghị xử lý trước khi import.
7. Bấm **"Đánh dấu đã duyệt"**.

**Bước 4 — Tạo vào hệ thống**
8. (Nếu cần) bấm **"Cài đặt CoA Misa"** để bổ sung tài khoản chi tiết của Misa, và **"Trích xuất master từ batch"** để tự dựng danh mục (tài khoản, kho, hàng hóa, khách, nhà cung cấp) từ nội dung chứng từ — vì Misa thường không xuất file danh mục riêng.
9. Xem **kiểm tra pre-flight**: hệ thống kiểm tra các điều kiện (bút toán cân Nợ = Có, kỳ chưa khóa, đã có khách/nhà cung cấp, tiền tệ công ty là VND, không trùng chứng từ…). Lỗi mức **chặn** sẽ không cho tạo cho tới khi sửa; mức **cảnh báo** chỉ nhắc.
10. Bấm **"Tạo vào hệ thống"**. Hệ thống chạy nền theo thứ tự: danh mục tham chiếu → hệ thống tài khoản → khách/nhà cung cấp/hàng hóa → số dư đầu kỳ → chứng từ phát sinh (chèn rồi đẩy lên sổ). Bạn có thể đóng tab, tiến trình vẫn tiếp tục; màn hình hiển thị tiến độ theo từng giai đoạn.
   - Có thêm nút **"Tạo chế độ nhanh (SQL)"** — nhanh hơn nhiều lần nhưng bỏ qua kiểm tra của hệ thống, chỉ dùng cho dữ liệu lịch sử nguồn đã chắc chắn sạch.

**Sau khi tạo xong**
11. Chạy **"Kiểm tra cân đối sau import"** để phát hiện tài khoản lệch dấu, thiếu số dư đầu kỳ, lệch công nợ.
12. Nếu có dòng lỗi, bấm **"Xem & Retry"** để xem lý do từng nhóm lỗi + gợi ý sửa, khắc phục nguồn rồi chạy lại.
13. Nếu phát hiện sai sót lớn, bấm **"Hoàn tác (Undo)"** để hủy + xóa toàn bộ chứng từ do đợt này tạo và làm lại.

## Định khoản tự động

Công cụ **không tự sinh bút toán mới** — nó **dựng lại đúng bút toán lịch sử theo nguồn Misa**:

| Trường hợp | Nguồn / Cách dựng | Ghi chú |
|---|---|---|
| Chứng từ phát sinh trong kỳ | File Nhật ký chung đã chứa sẵn cặp Nợ/Có | Mỗi chứng từ Misa → hóa đơn bán hàng / hóa đơn mua hàng / phiếu thanh toán / phiếu nhập xuất kho / phiếu kế toán tương ứng, rồi ghi sổ |
| Số dư đầu kỳ tài khoản | File số dư tài khoản đầu kỳ | Dựng thành bút toán đầu kỳ tại ngày OB |
| Công nợ phải thu / phải trả đầu kỳ | File OB công nợ | Dr/Cr 131 (phải thu) hoặc 331 (phải trả) theo từng đối tượng |
| Tồn kho đầu kỳ | File OB tồn kho | Tạo phiếu nhập kho đầu kỳ |
| Tài sản cố định đầu kỳ | File OB tài sản | Theo nguyên giá 211 và hao mòn lũy kế 2141 |
| Công cụ dụng cụ / chi phí trả trước đầu kỳ | File OB tương ứng | Chi phí chờ phân bổ 242 (theo TT99/2025) |

Vì là dữ liệu lịch sử đã chốt, công cụ tin tưởng số liệu nguồn. **Kế toán chịu trách nhiệm đối chiếu lại** số dư sau khi import.

## Tình huống đặc biệt & cảnh báo

- **Bắt buộc đối chiếu cân đối sau import**: luôn chạy "Kiểm tra cân đối sau import" và so Bảng cân đối số phát sinh của hệ thống với của Misa. Chỉ khi khớp mới coi là đạt.
- **Tài khoản thụ động dễ thiếu**: file số dư đầu kỳ Misa thường bỏ sót một số tài khoản thụ động (ví dụ 3387, 1331, 1551…), khiến tài khoản đó kết thúc với **số dư âm**. Khắc phục: kết xuất lại file số dư đầy đủ, hoặc bổ sung bằng một phiếu kế toán điều chỉnh đầu kỳ.
- **Đúng thứ tự nhập**: phải có danh mục + hệ thống tài khoản + khách/nhà cung cấp/hàng hóa **trước** số dư đầu kỳ và chứng từ. Thiếu → bước sau có thể bỏ qua dữ liệu hoặc lỗi. Pre-flight giúp phát hiện trước khi bấm Tạo.
- **Kỳ kế toán đã khóa**: nếu kỳ đã chốt sổ, không tạo được chứng từ vào kỳ đó — phải mở khóa kỳ trước.
- **Một công ty một đợt đang chạy**: mỗi công ty chỉ chạy một đợt tại một thời điểm.
- **Tiền tệ công ty phải là VND**: pre-flight sẽ chặn nếu công ty đặt tiền tệ khác.
- **Dòng lỗi sau khi tạo**: phải **sửa đúng nguyên nhân gốc** (ánh xạ tài khoản còn thiếu, chưa có khách/nhà cung cấp…) trước khi bấm Retry, nếu không sẽ lỗi y hệt.
- **Chế độ nhanh (SQL)**: bỏ qua kiểm tra và lịch sử chi tiết từng chứng từ — chỉ dùng cho dữ liệu nguồn đã sạch, nên chạy thử trên đợt nhỏ trước.

## Báo cáo liên quan

- [Lịch sử chuyển dữ liệu](lich-su-migration.md) — tra cứu các đợt đã chạy, trạng thái và số dòng.
- Sau import, dùng **Sổ Cái** và **Bảng cân đối số phát sinh** ở phân hệ **Tổng hợp** để đối chiếu với Misa.

## FAQ

**Q: Đang import mà đóng tab có sao không?**
**A:** Không sao. Tiến trình chạy nền; mở lại màn hình sẽ tự tiếp tục theo dõi và hiển thị tiến độ.

**Q: Vì sao một số nhóm hiển thị "đã có" mà không tạo doc mới?**
**A:** Đó là các bản ghi danh mục đã tồn tại sẵn trong hệ thống (ví dụ tài khoản, đơn vị tính) — hệ thống bỏ qua việc tạo trùng, vẫn tính là đã xử lý.

**Q: "Bảng kê bán ra / mua vào" sao không thấy tạo chứng từ riêng?**
**A:** Hai file này là **dữ liệu tham chiếu** cung cấp chi tiết dòng hàng cho các chứng từ ở Nhật ký chung, không tạo doc riêng. Hệ thống hiển thị số dòng đã đọc thay vì số doc đã tạo.

**Q: Import rất chậm có bình thường không?**
**A:** Với dữ liệu lớn (cả năm + đầu kỳ ~hơn 100.000 dòng), toàn bộ quá trình có thể mất vài chục phút trên máy chủ phát triển; trên máy chủ thật thường nhanh hơn. Màn hình luôn hiển thị tiến độ theo từng giai đoạn.

**Q: Khác gì giữa "Hoàn tác" và "Khôi phục pipeline (nâng cao)"?**
**A:** "Hoàn tác (Undo)" hủy + xóa toàn bộ chứng từ của cả đợt (mức đợt). Mục "Khôi phục pipeline" là công cụ nâng cao chạy ở mức chi tiết hơn (hủy/xóa riêng các chứng từ phát sinh Phase 4), dành cho người vận hành xử lý sự cố.
