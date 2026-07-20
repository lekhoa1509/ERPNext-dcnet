---
title: Kiểm kê tài sản
order: 5
summary: Kiểm kê thực tế tài sản theo địa điểm/bộ phận; mục mất sinh bút toán Nợ TK 1381 / Có TK 211.
---

## Mục đích

**Kiểm kê TSCĐ** lập biên bản kiểm kê thực tế tài sản theo địa điểm/bộ phận, đối chiếu sổ sách với hiện trạng. Mỗi tài sản được ghi nhận tình trạng: còn nguyên, hỏng, hoặc mất. Khi duyệt, tài sản "mất" sinh bút toán ghi nhận thiếu (Nợ TK 1381 / Có TK 211); tài sản "hỏng" được đánh dấu "Hỏng" (ngừng hoạt động).

## Khi nào dùng

- Kiểm kê định kỳ (cuối năm, cuối kỳ) theo quy định.
- Kiểm kê đột xuất khi bàn giao bộ phận, đổi người quản lý.
- Đối chiếu tài sản thực tế tại một địa điểm/phòng ban với danh mục trên sổ.
- Phát hiện và xử lý tài sản mất/hỏng.

## Cách thực hiện

1. Bấm **Kiểm kê TSCĐ** trên menu TSCĐ → danh sách biên bản (phạm vi TSCĐ) mở. Bấm "+ Thêm".
2. **Phạm vi** đã đặt sẵn = TSCĐ. Chọn **Công ty**, **Ngày kiểm kê**; lọc theo **Địa điểm** và/hoặc **Bộ phận** nếu cần thu hẹp.
3. Bấm **Hành động > Tải danh sách** → hệ thống nạp toàn bộ tài sản (đã ghi sổ) thuộc địa điểm/bộ phận đã chọn vào bảng, kèm giá trị sổ sách.
4. Với từng dòng, chọn **Tình trạng thực tế**: **Còn nguyên** / **Hỏng** / **Mất**; ghi chú nếu cần. Dòng tổng kết hiển thị số lượng theo từng tình trạng.
5. Đổi **Trạng thái** biên bản sang **Completed** (hoàn thành kiểm kê).
6. Bấm **Hành động > Duyệt kiểm kê** → hệ thống xử lý: mục "Mất" sinh bút toán ghi nhận thiếu; mục "Hỏng" chuyển trạng thái tài sản sang "Ngừng hoạt động". Biên bản chuyển sang trạng thái "Approved".

## Định khoản tự động

| Tình trạng | TK Nợ | TK Có | Ghi chú |
|---|---|---|---|
| Mất — tài sản cố định | 1381 | 211 | Tài sản thiếu chờ xử lý / nguyên giá |
| Mất — công cụ dụng cụ (phạm vi CCDC) | 1381 | 153 | Áp dụng cho biên bản phạm vi CCDC |
| Hỏng | — | — | Chỉ đổi trạng thái tài sản sang "Ngừng hoạt động", không sinh bút toán |
| Còn nguyên | — | — | Không xử lý |

> Số tiền bút toán "mất" lấy theo giá trị sổ sách của tài sản tại thời điểm tải danh sách. TK 1381 (tài sản thiếu chờ xử lý) được tra theo công ty; nếu không tìm thấy tài khoản 1381 hoặc 211/153, hệ thống ghi nhật ký lỗi và bỏ qua dòng đó.

## Tình huống đặc biệt & cảnh báo

- **Phải đặt trạng thái "Completed" trước khi duyệt:** nút **Duyệt kiểm kê** chỉ hiện khi trạng thái biên bản = "Completed". Hoàn tất ghi nhận tình trạng rồi đổi trạng thái sang Completed mới duyệt được.
- **Tài khoản TK 1381 phải có sẵn:** xử lý "mất" cần TK 1381 (tài sản thiếu chờ xử lý) và TK 211 (TSCĐ) / 153 (CCDC) trong hệ thống tài khoản. Thiếu tài khoản → dòng đó không sinh bút toán, chỉ ghi nhật ký lỗi (không báo lỗi rõ trên màn hình) → cần kiểm tra Sổ Cái sau khi duyệt.
- **TK xử lý thiếu sau kiểm kê:** TK 1381 chỉ là tài khoản chờ xử lý. Sau khi có quyết định của ban giám đốc, cần lập bút toán xử lý tiếp: bồi thường (TK 1388/334), tính vào chi phí (TK 811), hoặc ghi giảm nguồn — không nằm trong nghiệp vụ kiểm kê này.
- **Tải danh sách ghi đè bảng cũ:** mỗi lần "Tải danh sách" sẽ xóa và nạp lại toàn bộ bảng theo bộ lọc hiện tại — nhập tình trạng xong rồi mới tải lại sẽ mất dữ liệu đã nhập.
- **Nếu nút "Duyệt kiểm kê" báo lỗi quyền:** đây là vấn đề kỹ thuật cần kỹ thuật viên xử lý (xem ghi chú phía dưới) — tạm thời có thể nhờ người có quyền quản trị duyệt.

## Báo cáo liên quan

- **Sổ Cái:** kiểm tra bút toán "mất" (Nợ TK 1381 / Có TK 211) sau khi duyệt.
- **Sổ S22-DN:** theo dõi TSCĐ/CCDC.
- **Danh sách tài sản:** trạng thái tài sản "Ngừng hoạt động" sau khi đánh dấu "Hỏng".

## FAQ

**Q: Kiểm kê khác bàn giao thế nào?**
**A:** Kiểm kê là đối chiếu hiện trạng thực tế với sổ sách (phát hiện mất/hỏng), có thể sinh bút toán điều chỉnh. Bàn giao là chuyển người giữ/địa điểm, không đổi giá trị sổ. Hai chứng từ khác mục đích.

**Q: Tài sản "Hỏng" có sinh bút toán không?**
**A:** Không. "Hỏng" chỉ chuyển trạng thái tài sản sang "Ngừng hoạt động" để theo dõi; việc sửa chữa hay thanh lý xử lý qua nghiệp vụ riêng ([Sửa chữa](sua-chua.md) hoặc [Thanh lý](thanh-ly.md)).

**Q: Một biên bản kiểm kê được nhiều địa điểm không?**
**A:** Bộ lọc địa điểm/bộ phận áp dụng khi tải danh sách. Để kiểm kê nhiều địa điểm, hoặc bỏ lọc địa điểm (tải tất cả) hoặc lập nhiều biên bản theo từng địa điểm cho rõ ràng.
