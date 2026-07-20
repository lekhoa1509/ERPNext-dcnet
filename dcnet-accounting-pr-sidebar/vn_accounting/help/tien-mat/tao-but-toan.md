---
title: Tạo bút toán (Journal Entry)
order: 9
summary: Tạo phiếu kế toán tổng quát khi Phiếu thu / Phiếu chi / Rút-nộp không phù hợp.
---

## Mục đích

**Phiếu kế toán** là chứng từ kế toán tổng quát — dùng khi 4 cửa vào riêng biệt (Phiếu thu PT-, Phiếu chi PC-, Thu thanh toán, Chi thanh toán) không phù hợp. Phổ biến cho điều chỉnh, kết chuyển cuối kỳ, đánh giá lại tỷ giá, hạch toán nội bộ phức tạp, hoặc bất kỳ bút toán nào không gắn với hóa đơn bán hàng / hóa đơn mua hàng / TSCĐ.

## Khi nào dùng

- Kế toán trưởng làm điều chỉnh cuối kỳ (kết chuyển 511 → 911, chi phí → 911, đánh giá lại tỷ giá).
- Bút toán không có đối tượng / hóa đơn rõ ràng (vd: chia lương phân bổ chi phí, kết chuyển dở dang).
- Bút toán nhiều dòng phức tạp (>2 dòng: 1 Nợ, 1 Có).
- Bút toán đặc thù: hủy ghi nhận doanh thu, xóa nợ khó đòi, tái phân bổ chi phí.
- Khi kế toán viên gõ trực tiếp số hiệu chứng từ `PT-` hoặc `PC-` để dùng hộp thoại chọn loại của Phiếu chi.

## Cách thực hiện

1. Mở **danh sách phiếu kế toán** (qua mục "Bút toán" trong phần "Tổng hợp", hoặc đường dẫn `/app/journal-entry`) → bấm "+ Thêm".
   ![Biểu mẫu phiếu kế toán mới](_images/tao-but-toan-1.png)
2. Chọn **Loại chứng từ**: tùy mục đích —
   - Phiếu kế toán tổng quát (mặc định).
   - Tiền mặt (TK 111). Số hiệu chứng từ PT-/PC- ưu tiên.
   - Ngân hàng (TK 112).
   - Chuyển khoản nội bộ — chuyển TK 111 ↔ 112 (rút/nộp tiền).
3. Chọn **Số hiệu chứng từ**: PT-.YYYY.- (Phiếu thu) / PC-.YYYY.- (Phiếu chi → kích hoạt hộp thoại chọn loại) / ACC-JV-.YYYY.- (Phiếu kế toán chung).
4. Trong bảng định khoản, thêm các dòng:
   - Tài khoản
   - Số tiền Nợ hoặc Có
   - Loại đối tượng và Đối tượng (tùy chọn, bắt buộc cho TK 131/331/141/334)
   - Trung tâm chi phí (tùy chọn)
   - Diễn giải (tùy chọn, theo từng dòng)
5. Kiểm tra: tổng Nợ = tổng Có (khác 0).
6. Lưu và ghi sổ.

## Quy ước số hiệu chứng từ

| Số hiệu | Mục đích | Hành vi đặc biệt |
|---|---|---|
| PT-.YYYY.- | Phiếu thu | Hiện trên báo cáo Phiếu thu |
| PC-.YYYY.- | Phiếu chi | Hiện trên Phiếu chi và tự mở hộp thoại chọn loại |
| ACC-JV-.YYYY.- | Phiếu kế toán tổng quát | Mặc định cho phiếu kế toán tổng quát |
| MAT-JV-.YYYY.- | Bút toán liên quan kho/vật tư | Tự động cho phiếu kế toán liên quan kho |

Hộp thoại chọn loại của PC-: 6 lựa chọn (Trả NCC / Nộp thuế / Đóng BHXH / Trả lương / Tạm ứng nhân viên / Khác) — điền sẵn TK đối ứng. Xem [Phiếu chi](phieu-chi.md) cho chi tiết.

## Định khoản tự động

Phiếu kế toán không tự định khoản — kế toán viên định khoản thủ công. Tổng Nợ = Tổng Có (ràng buộc kiểm tra). Một số ví dụ phổ biến:

| Trường hợp | TK Nợ | TK Có | Ghi chú |
|---|---|---|---|
| Kết chuyển doanh thu 511 → 911 | 511 | 911 | Cuối kỳ |
| Kết chuyển chi phí → 911 | 911 | 627/641/642 | Cuối kỳ |
| Đánh giá lại tỷ giá cuối kỳ | 1122 / 1112 | 413 (lãi) hoặc 413 → 635 (lỗ) | Cuối tháng |
| Xóa nợ khó đòi | 642 (CP dự phòng) | 131 (KH) | Sau quyết định |
| Phân bổ tiền lương | 622/627/641/642 | 334 | Hằng tháng |
| Trích lập dự phòng | 632 / 642 | 159 / 229 | Cuối kỳ |
| Hủy doanh thu | 511 + 3331 | 131 | Khi hủy hóa đơn bán hàng |

## Tình huống đặc biệt & cảnh báo

- **Phiếu ghi lùi ngày:** Khi nhập ngày ghi sổ trước hôm nay, hệ thống có thể tự đổi về hôm nay — cần kiểm tra lại trước khi lưu.
- **Đa tiền tệ:** Bật chế độ đa tiền tệ, mỗi dòng có tỷ giá riêng. Hệ thống tự ghi chênh lệch tỷ giá.
- **Kiểm tra loại đối tượng:** TK 131 yêu cầu loại đối tượng = Khách hàng; TK 331 → Nhà cung cấp; TK 334/141 → Nhân viên. Nếu thiếu/sai, hệ thống báo lỗi.
- **Tham chiếu chứng từ gốc:** dòng định khoản có trường tham chiếu (liên kết tới hóa đơn bán hàng, hóa đơn mua hàng, TSCĐ, v.v.). Hệ thống đã mở rộng cho các chứng từ tùy chỉnh như công cụ dụng cụ và bàn giao tài sản.
- **Hủy phiếu kế toán:** Hủy phiếu sẽ mở lại các tham chiếu liên kết (vd: nếu phiếu phân bổ tới hóa đơn). Cẩn thận khi hủy phiếu đã gắn liên kết.
- **Hộp thoại chọn loại không hiện:** nếu vào qua hóa đơn bán hàng / hóa đơn mua hàng "Tạo > Phiếu thanh toán" rồi đổi số hiệu chứng từ sang PC- → hộp thoại không tự mở (chỉ kích hoạt khi số hiệu chứng từ được chọn từ đầu hoặc đường dẫn tạo phiếu PC-). Cách xử lý: tải lại biểu mẫu sau khi đổi số hiệu.

## Báo cáo liên quan

- **Phiếu thu**: phiếu kế toán PT- hiện trên đây.
- **Phiếu chi**: phiếu kế toán PC- hiện trên đây.
- **Sổ quỹ tiền mặt / Sổ cái kế toán**: tất cả phiếu kế toán liên quan TK 111/112.
- **Bảng cân đối số phát sinh**: tổng phát sinh và số dư các TK trong kỳ.

## FAQ

**Q: Khi nào dùng phiếu kế toán PT-/PC- so với phiếu thanh toán loại Thu/Chi?**
**A:** Phiếu thanh toán khi có hóa đơn cần thanh toán. Phiếu kế toán PT-/PC- cho bút toán không gắn hóa đơn. Cả hai cùng xuất hiện trên báo cáo Phiếu thu / Phiếu chi.

**Q: Hộp thoại chọn loại của PC- không kích hoạt — sao?**
**A:** Hộp thoại kích hoạt qua sự kiện thay đổi của trường số hiệu chứng từ. Nếu số hiệu được đặt sẵn từ đường dẫn tạo phiếu PC-, hộp thoại tự mở khi biểu mẫu sẵn sàng. Nếu kế toán viên bấm "+ Thêm" trong danh sách trống, số hiệu mặc định có thể là `MAT-JV-` → hộp thoại không kích hoạt. Đổi số hiệu thủ công sang PC-, tải lại biểu mẫu, hộp thoại sẽ kích hoạt.

**Q: Có thể có phiếu kế toán 1 dòng (chỉ Nợ hoặc Có riêng) không?**
**A:** Không — hệ thống bắt tổng Nợ = tổng Có; tối thiểu 2 dòng. Bút toán "1 dòng" thường là sai khái niệm (mọi nghiệp vụ kép luôn có cả 2 vế).

**Q: Loại chứng từ "Cash Entry" có khác phiếu kế toán thông thường?**
**A:** Cash Entry là loại con của phiếu kế toán chuyên cho TK 111. Trường loại chứng từ chỉ là siêu dữ liệu — không thay đổi logic định khoản, nhưng giúp lọc báo cáo (báo cáo Phiếu thu / Phiếu chi lọc theo loại chứng từ Cash Entry).
