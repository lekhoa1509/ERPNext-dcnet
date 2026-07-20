---
section: Danh mục
title: Tổng quan Danh mục
summary: Khai báo dữ liệu nền — hệ thống tài khoản, khách hàng, nhà cung cấp, hàng hóa, kho, nhân viên và định mức vật tư — làm cơ sở cho mọi nghiệp vụ và định khoản.
---

## Mục đích

Phân hệ **Danh mục** là nơi khai báo **dữ liệu nền** (master data) cho toàn bộ hệ thống kế toán: hệ thống tài khoản, đối tượng công nợ (khách hàng, nhà cung cấp), hàng hóa – vật tư, kho, nhân viên và định mức vật tư. Đây là "từ điển" mà mọi chứng từ và báo cáo tham chiếu tới.

Bản thân danh mục **không tự sinh bút toán** — khai báo một khách hàng hay một mặt hàng không tạo ra phát sinh trên Sổ Cái. Tuy nhiên dữ liệu nền **quyết định cách định khoản** của các chứng từ sau này: tài khoản doanh thu / giá vốn mặc định của mặt hàng, tài khoản công nợ của khách / nhà cung cấp, tài khoản kho của từng kho… Khai báo đúng ngay từ đầu giúp chứng từ tự điền đúng tài khoản, hạn chế sai sót lặp lại.

## Khi nào dùng

- **Khi thiết lập ban đầu:** dựng hệ thống tài khoản theo Thông tư 99/2025/TT-BTC, khai báo danh sách khách hàng / nhà cung cấp / mặt hàng / kho hiện có.
- **Khi phát sinh đối tượng mới:** thêm khách hàng mới ký hợp đồng, nhà cung cấp mới, mặt hàng mới nhập về, mở thêm kho/chi nhánh, tuyển nhân viên mới.
- **Khi cần chuẩn hóa định khoản:** gán tài khoản doanh thu / giá vốn mặc định cho nhóm hàng, tài khoản công nợ riêng cho khách đặc thù, tài khoản kho cho từng kho.
- **Trước khi nhập liệu hàng loạt / lên báo cáo:** đảm bảo danh mục đầy đủ để chứng từ và báo cáo tham chiếu chính xác.

## Cách thực hiện

Phân hệ **Danh mục** gồm 7 mục:

| # | Mục | Loại | Mô tả ngắn |
|---|---|---|---|
| 1 | Hệ thống tài khoản | Cây dữ liệu | Cây tài khoản kế toán theo TT99/2025 (TK cấp 1/2/3) |
| 2 | Khách hàng | Danh mục | Đối tượng phải thu (TK 131), gồm mã, MST, nhóm |
| 3 | Nhà cung cấp | Danh mục | Đối tượng phải trả (TK 331), gồm mã, MST, nhóm |
| 4 | Hàng hóa, vật tư | Danh mục | Mặt hàng kinh doanh / vật tư, đơn vị tính, TK mặc định |
| 5 | Kho | Danh mục | Kho vật lý gắn với tài khoản hàng tồn kho (152/153/155/156) |
| 6 | Nhân viên | Danh mục | Hồ sơ nhân sự dùng cho tạm ứng (141) và tiền lương (334) |
| 7 | Định mức vật tư | Danh mục | Định mức nguyên vật liệu cho 1 đơn vị thành phẩm (dùng cho giá thành) |

### Quy trình điển hình

1. **Dựng hệ thống tài khoản** theo TT99/2025 trước tiên — đây là gốc của mọi định khoản. Xem [Hệ thống tài khoản](he-thong-tai-khoan.md).
2. **Khai báo kho** và gán tài khoản kho (152/153/155/156) cho từng kho. Xem [Kho](kho.md).
3. **Khai báo mặt hàng**, gán nhóm hàng, đơn vị tính, kho mặc định, và **tài khoản doanh thu / giá vốn mặc định** qua mục "Giá trị mặc định". Xem [Hàng hóa, vật tư](hang-hoa-vat-tu.md).
4. **Khai báo khách hàng / nhà cung cấp**, nhập MST, nhóm, và tài khoản công nợ mặc định nếu khác chuẩn. Xem [Khách hàng](khach-hang.md), [Nhà cung cấp](nha-cung-cap.md).
5. **Khai báo nhân viên** phục vụ tạm ứng và tính lương. Xem [Nhân viên](nhan-vien.md).
6. **Khai báo định mức vật tư** cho doanh nghiệp sản xuất, làm cơ sở tính giá thành. Xem [Định mức vật tư](dinh-muc-vat-tu.md).

### Liên kết tới các bài hướng dẫn chi tiết

- [Hệ thống tài khoản](he-thong-tai-khoan.md)
- [Khách hàng](khach-hang.md) · [Nhà cung cấp](nha-cung-cap.md)
- [Hàng hóa, vật tư](hang-hoa-vat-tu.md) · [Kho](kho.md)
- [Nhân viên](nhan-vien.md) · [Định mức vật tư](dinh-muc-vat-tu.md)

## Định khoản tự động

Danh mục **không trực tiếp sinh bút toán**. Vai trò của danh mục là **cung cấp tài khoản mặc định** cho chứng từ:

| Dữ liệu nền | Trường mặc định | Ảnh hưởng tới định khoản |
|---|---|---|
| Hàng hóa, vật tư | TK doanh thu / TK giá vốn (Giá trị mặc định) | Hóa đơn bán hàng lấy TK 511; xuất kho/giá vốn lấy TK 632 |
| Kho | Tài khoản kho | Nhập/xuất kho ghi Nợ/Có đúng TK 152/153/155/156 |
| Khách hàng | Tài khoản phải thu | Hóa đơn bán hàng ghi Nợ TK 131 đúng đối tượng |
| Nhà cung cấp | Tài khoản phải trả | Hóa đơn mua hàng ghi Có TK 331 đúng đối tượng |
| Nhân viên | (gắn với người nhận) | Tạm ứng ghi TK 141; lương ghi TK 334 theo từng người |

Tài khoản mặc định chỉ là **gợi ý điền sẵn** — kế toán viên vẫn có thể chỉnh trên chứng từ khi cần.

## Tình huống đặc biệt & cảnh báo

- **Tài khoản tổng (nhóm) không định khoản trực tiếp:** chỉ tài khoản chi tiết (lá, không phải nhóm) mới được dùng để ghi phát sinh. Xem [Hệ thống tài khoản](he-thong-tai-khoan.md).
- **Tài khoản theo TT99/2025:** áp dụng từ 01/01/2026, thay Thông tư 200/2014. Lưu ý các thay đổi như TK 242 "Chi phí chờ phân bổ" (bỏ TK 142).
- **MST sai/trùng:** khai báo sai mã số thuế khách / nhà cung cấp gây sai hóa đơn điện tử và tờ khai thuế — kiểm tra kỹ trước khi lập chứng từ.
- **Mặt hàng thiếu tài khoản mặc định:** nếu mặt hàng không khai TK doanh thu / giá vốn, chứng từ sẽ rơi về tài khoản mặc định của công ty — dễ sai. Nên gán đầy đủ theo nhóm hàng.
- **Đa công ty:** tài khoản, kho, và Giá trị mặc định của mặt hàng đều khai theo **từng công ty** — kiểm tra đúng công ty đang làm việc.

## Báo cáo liên quan

- **Sổ Cái / Sổ chi tiết tài khoản**: tra cứu phát sinh theo từng tài khoản đã khai báo.
- **Bảng cân đối số phát sinh**: kiểm tra số dư các tài khoản trong hệ thống tài khoản.
- **Báo cáo công nợ phải thu / phải trả**: tổng hợp theo khách hàng / nhà cung cấp.
- **Báo cáo nhập – xuất – tồn**: theo dõi số lượng và giá trị theo mặt hàng và kho.

## FAQ

**Q: Khai báo một mặt hàng/khách hàng mới có tạo ra bút toán không?**
**A:** Không. Danh mục chỉ là dữ liệu nền. Bút toán chỉ phát sinh khi lập chứng từ thực tế (hóa đơn, phiếu thu/chi, phiếu nhập/xuất kho…). Nhưng danh mục quyết định chứng từ điền tài khoản nào.

**Q: Tôi sửa tài khoản doanh thu mặc định của mặt hàng — các hóa đơn cũ có đổi theo không?**
**A:** Không. Tài khoản mặc định chỉ áp dụng cho **chứng từ lập mới** sau khi sửa. Chứng từ đã ghi sổ giữ nguyên định khoản cũ.

**Q: "Hệ thống tài khoản" ở đây có giống "Cây tài khoản" trong phần Thiết lập không?**
**A:** Cùng một hệ thống tài khoản (cùng dữ liệu). Trong Danh mục là lối truy cập nhanh để xem/khai báo tài khoản dùng hằng ngày; trong Thiết lập đặt cùng nhóm cấu hình ban đầu. Sửa ở đâu cũng cập nhật chung.

**Q: Nhân viên ở Danh mục có phải khai lại trong phân hệ Tiền lương không?**
**A:** Không. Đây là **cùng một hồ sơ nhân viên** — khai một lần dùng chung cho tạm ứng (TK 141) và tính lương (TK 334).
