---
title: Hệ thống tài khoản
order: 1
summary: Cây tài khoản kế toán theo TT99/2025 — cấu trúc TK cấp 1/2/3, tài khoản tổng và tài khoản chi tiết.
---

## Mục đích

**Hệ thống tài khoản** là danh mục gốc của toàn bộ kế toán: mỗi tài khoản (TK) là một "ngăn" để ghi nhận và theo dõi một loại tài sản, nợ phải trả, vốn, doanh thu hay chi phí. Hệ thống được tổ chức theo dạng **cây nhiều cấp** theo Thông tư 99/2025/TT-BTC: tài khoản cấp 1 (3 chữ số, ví dụ 111, 131, 511), tài khoản cấp 2/3 chi tiết hơn (1111, 1311, 5111…).

Mỗi tài khoản có các thuộc tính chính:

- **Số hiệu tài khoản** (Số TK): mã theo VAS, ví dụ 111, 1121, 632.
- **Là tài khoản tổng?** (`Là nhóm`): tài khoản nhóm/cha chỉ để gom số, **không ghi phát sinh trực tiếp**; tài khoản chi tiết (lá) mới được dùng để định khoản.
- **Loại gốc** (Asset / Liability / Income / Expense / Equity): xác định tài khoản nằm ở Bảng cân đối hay Báo cáo kết quả.
- **Loại tài khoản** (`Account Type`): phân loại nghiệp vụ — Tiền mặt (Cash), Ngân hàng (Bank), Phải thu (Receivable), Phải trả (Payable), Kho (Stock), Giá vốn (Cost of Goods Sold), Khấu hao (Depreciation), Thuế (Tax)… Loại này giúp hệ thống lọc đúng tài khoản cho từng chứng từ.
- **Loại tiền tệ**: tài khoản theo dõi bằng VND hoặc ngoại tệ (ví dụ TK 1122, 1112 theo USD).

## Khi nào dùng

- **Thiết lập ban đầu:** dựng toàn bộ hệ thống tài khoản theo TT99/2025 trước khi nhập bất kỳ chứng từ nào.
- **Khi cần chi tiết hơn:** mở thêm tài khoản con dưới một tài khoản cấp 1 (ví dụ mở 1311, 1312 dưới 131 để tách công nợ theo nhóm khách).
- **Khi gắn loại tài khoản:** đặt đúng `Loại tài khoản` cho tài khoản kho, thuế, khấu hao… để các chức năng tự động (kho, tài sản, thuế) nhận diện.
- **Khi tra cứu cấu trúc:** xem cây tài khoản để biết tài khoản nào là tổng, tài khoản nào chi tiết.

## Cách thực hiện

1. Mở **Hệ thống tài khoản** trên menu Danh mục → cây tài khoản hiển thị dạng phân cấp, có thể bung/thu từng nhánh.
2. **Thêm tài khoản chi tiết:** bấm vào tài khoản cha (ví dụ 131) → "Thêm tài khoản con" → nhập Số TK và tên → chọn `Loại tài khoản` phù hợp.
3. **Khai thuộc tính bắt buộc cho tài khoản lá:**
   - Để trống `Là nhóm` (tài khoản chi tiết).
   - Chọn `Loại tài khoản` đúng nghiệp vụ (ví dụ 1111 → Cash; 156x → Stock; 632 → Cost of Goods Sold; 2141 → Accumulated Depreciation).
   - Chọn loại tiền tệ nếu là tài khoản ngoại tệ.
4. **Đổi tên / số hiệu:** chỉ nên đổi khi tài khoản chưa phát sinh; tài khoản đã có bút toán không nên đổi số hiệu.

## Định khoản tự động

Hệ thống tài khoản **không tự định khoản** — đây là danh mục khai báo. Tuy nhiên nó là **đối tượng đích** của mọi bút toán: chứng từ ghi Nợ/Có vào các tài khoản chi tiết trong danh mục này. `Loại tài khoản` còn được dùng để hệ thống tự gợi ý tài khoản (ví dụ chỉ tài khoản loại Cash mới hiện ở phiếu thu/chi tiền mặt).

## Tình huống đặc biệt & cảnh báo

- **Không ghi vào tài khoản tổng:** nếu cố định khoản vào tài khoản nhóm (`Là nhóm` = có), hệ thống sẽ báo lỗi. Luôn dùng tài khoản chi tiết (lá).
- **TK theo TT99/2025:** áp dụng từ 01/01/2026. Một số thay đổi so với TT200: TK 242 đổi tên thành "Chi phí chờ phân bổ" và **bỏ TK 142**; rà soát tên/cấu trúc trước khi áp dụng.
- **Loại tài khoản quyết định chức năng tự động:** kho cần `Stock`, tài sản cần `Fixed Asset` / `Accumulated Depreciation` / `Depreciation`, thuế cần `Tax`. Thiếu loại này, các chức năng tự động (kho, tài sản, thuế) sẽ báo lỗi hoặc không nhận tài khoản.
- **Xóa tài khoản:** không xóa được tài khoản đã có phát sinh trên Sổ Cái (kể cả bút toán đã hủy). Trường hợp này khóa tài khoản (`Đã khóa`) thay vì xóa.
- **Đa công ty:** mỗi công ty có hệ thống tài khoản riêng — kiểm tra đúng công ty trước khi thêm/sửa.

## Báo cáo liên quan

- **Sổ Cái**: toàn bộ phát sinh theo từng tài khoản.
- **Sổ chi tiết tài khoản**: chi tiết phát sinh + số dư của một tài khoản.
- **Bảng cân đối số phát sinh**: số dư đầu kỳ, phát sinh, số dư cuối kỳ của mọi tài khoản.
- **Báo cáo tình hình tài chính (B01-DN)** và **Báo cáo kết quả hoạt động kinh doanh**: lấy số liệu theo loại gốc của tài khoản.

## FAQ

**Q: Tại sao tôi không định khoản được vào TK 131?**
**A:** Nếu 131 đang là tài khoản tổng (`Là nhóm`), bạn phải định khoản vào tài khoản con chi tiết (ví dụ 1311). Tài khoản tổng chỉ để gom số dư các tài khoản con.

**Q: "Hệ thống tài khoản" trong Danh mục và "Cây tài khoản" trong Thiết lập có khác nhau không?**
**A:** Là cùng một hệ thống tài khoản, cùng dữ liệu. Khác nhau chỉ ở lối truy cập (Danh mục để dùng hằng ngày; Thiết lập gom cùng cấu hình ban đầu). Sửa ở một nơi cập nhật cho cả hai.

**Q: Tôi muốn tách công nợ theo từng khách — có cần mở mỗi khách một tài khoản con không?**
**A:** Không cần. Công nợ đã được theo dõi chi tiết theo từng khách hàng (đối tượng) trên cùng TK 131. Chỉ mở tài khoản con khi cần tách theo nhóm lớn (ví dụ 1311 phải thu trong nước, 1312 phải thu nước ngoài).

**Q: Tôi đặt sai loại tài khoản cho một TK kho — sửa thế nào?**
**A:** Mở tài khoản đó, đổi `Loại tài khoản` thành `Stock`, lưu lại. Nếu tài khoản đã gắn vào kho và đã có phát sinh, nên kiểm tra lại các phiếu nhập/xuất sau khi sửa.
