---
section: Hợp đồng & PAKD
title: Tổng quan Hợp đồng & PAKD
summary: Quản lý hợp đồng dịch vụ, phương án kinh doanh (PAKD), hoa hồng NVKD và các khoản phải trả phía khách, cùng 9 báo cáo theo dõi hóa đơn – thu tiền – công nợ – hoa hồng.
---

## Mục đích

Phân hệ **Hợp đồng & PAKD** quản lý vòng đời thương mại của một thỏa thuận dịch vụ: từ **hợp đồng** (cam kết bán hàng + lịch xuất hóa đơn định kỳ), qua **phương án kinh doanh** (PAKD — tính toán hoa hồng cho nhân viên kinh doanh và các khoản phải trả khác), tới các báo cáo theo dõi **hóa đơn chờ ghi sổ**, **công nợ**, **đôn thúc quá hạn**, **thực thu** và **sổ hoa hồng**.

Hai chứng từ gốc:

- **Danh sách hợp đồng** (Hợp đồng dịch vụ DCNET): cam kết với khách hàng. Khi duyệt, hệ thống tự sinh **lịch xuất hóa đơn** (mỗi kỳ một dòng), tự lập đơn bán hàng ngầm cho hàng hóa bán đứt, và đồng bộ thông tin khách hàng về dữ liệu chủ.
- **Phương án kinh doanh** (PAKD): gắn với một hợp đồng, dùng bộ quy tắc hoa hồng để tính ra hoa hồng NVKD, phí giấy phép viễn thông (GPVT) và các khoản phải trả phía khách (hoa hồng giới thiệu / chênh lệch giá / dịch vụ quản lý). PAKD đi qua quy trình duyệt nhiều cấp; sau khi duyệt + khách thanh toán, kế toán ghi sổ hoa hồng.

## Khi nào dùng

- Khi ký hợp đồng mới: lập **hợp đồng**, nhập gói dịch vụ + kỳ hạn + phí khởi tạo → duyệt để sinh lịch hóa đơn.
- Khi cần tính hoa hồng cho NVKD: lập **PAKD** gắn hợp đồng → gửi duyệt theo cấp.
- Hằng ngày — kế toán: mở **Hóa đơn cần ghi sổ** để duyệt hóa đơn nháp do hệ thống tự sinh.
- Theo dõi thu hồi: **Hóa đơn quá hạn cần đôn thúc**, **Kỳ thu tiền quá hạn**, **Công nợ theo hợp đồng**.
- Đối chiếu dòng tiền: **Thu tiền theo hợp đồng**.
- Cuối kỳ lương / sau khi khách thanh toán: **Sổ hoa hồng NVKD** và **Phải trả phía khách** để biết khoản nào cần ghi sổ tiếp.

## Cách thực hiện

Cấu trúc menu **Hợp đồng & PAKD** gồm 9 mục:

| # | Mục | Loại | Mô tả ngắn |
|---|---|---|---|
| 1 | Danh sách hợp đồng | Danh sách | Hợp đồng dịch vụ — cam kết + lịch xuất hóa đơn định kỳ |
| 2 | Phương án kinh doanh | Danh sách | PAKD — tính hoa hồng NVKD + phải trả phía khách |
| 3 | Hóa đơn cần ghi sổ | Báo cáo | Hóa đơn nháp gắn hợp đồng, chờ kế toán duyệt (ghi sổ) |
| 4 | Hóa đơn quá hạn cần đôn thúc | Báo cáo | Hóa đơn đã ghi sổ, quá hạn, còn nợ |
| 5 | Thu tiền theo hợp đồng | Báo cáo | Phiếu thu gắn hợp đồng — dòng tiền thực thu |
| 6 | Sổ hoa hồng NVKD (phải trả) | Báo cáo | Hoa hồng theo từng NVKD, cả qua bút toán và qua lương |
| 7 | Phải trả phía khách (kickback/markup/referral) | Báo cáo | Khoản phải trả người nhận ngoài, chờ ghi sổ |
| 8 | Công nợ theo hợp đồng | Báo cáo | Kỳ chưa thu / đã xuất hóa đơn / quá hạn theo hợp đồng |
| 9 | Kỳ thu tiền quá hạn | Báo cáo | Các kỳ trong lịch hóa đơn đã quá hạn chưa thu đủ |

### Quy trình điển hình

1. **Ký hợp đồng:** mở **Danh sách hợp đồng** → "+ Thêm" → nhập khách hàng, gói dịch vụ, kỳ hạn, phí khởi tạo, ngày nghiệm thu → "Ghi sổ" (duyệt). Hệ thống tự sinh lịch xuất hóa đơn cho từng kỳ.
2. **Lập PAKD:** mở **Phương án kinh doanh** → "+ Thêm" → chọn hợp đồng + NVKD → hệ thống tự tính hoa hồng theo bộ quy tắc. Gửi duyệt theo cấp (GĐ Kinh doanh → Phòng Tổng hợp → GĐ Chi nhánh → Ban Lãnh đạo, tùy loại).
3. **Xuất + ghi sổ hóa đơn:** đến kỳ, hệ thống sinh hóa đơn nháp. Kế toán mở **Hóa đơn cần ghi sổ** → ghi sổ (duyệt) → xuất hóa đơn VAT chính thức.
4. **Thu tiền:** khi khách trả, lập phiếu thu gắn hợp đồng. Xem trên **Thu tiền theo hợp đồng**.
5. **Ghi sổ hoa hồng:** sau khi PAKD đã duyệt và kỳ đã thu tiền, kế toán mở **Sổ hoa hồng NVKD** + **Phải trả phía khách**, ghi sổ các khoản hoa hồng tương ứng (theo tỷ lệ thực thu).
6. **Theo dõi công nợ:** định kỳ rà **Công nợ theo hợp đồng**, **Kỳ thu tiền quá hạn**, **Hóa đơn quá hạn cần đôn thúc** để đôn thúc khách.

### Liên kết tới các bài hướng dẫn chi tiết

- **Chứng từ gốc:** [Danh sách hợp đồng](danh-sach-hop-dong.md), [Phương án kinh doanh](phuong-an-kinh-doanh.md).
- **Hóa đơn:** [Hóa đơn cần ghi sổ](hoa-don-can-ghi-so.md), [Hóa đơn quá hạn cần đôn thúc](hoa-don-qua-han-don-thuc.md).
- **Thu tiền & công nợ:** [Thu tiền theo hợp đồng](thu-tien-theo-hop-dong.md), [Công nợ theo hợp đồng](cong-no-theo-hop-dong.md), [Kỳ thu tiền quá hạn](ky-thu-tien-qua-han.md).
- **Hoa hồng & phải trả:** [Sổ hoa hồng NVKD](so-hoa-hong-nvkd.md), [Phải trả phía khách](phai-tra-phia-khach.md).

## Định khoản tự động (tổng quát)

- **Hợp đồng** không tự định khoản khi lập. Khi hủy hợp đồng giữa kỳ, các kỳ đã xuất hóa đơn được hệ thống tự lập **hóa đơn trả lại** (giảm trừ doanh thu); kỳ đã thu tiền chỉ cảnh báo, không tự hoàn tiền.
- **PAKD** tự sinh **bút toán** ghi nhận chi phí hoa hồng khi kế toán bấm đăng (hoặc tự đăng theo tỷ lệ thực thu khi khách thanh toán). Tài khoản dùng để định khoản **không cố định trong mã** — kế toán cấu hình trong **Thiết lập PAKD**. Hình mẫu định khoản:

| Trường hợp | TK Nợ (chi phí) | TK Có (phải trả) | Ghi chú |
|---|---|---|---|
| Hoa hồng NVKD (qua bút toán, không qua lương) | TK chi phí hoa hồng NVKD (vd 6421/6418) | TK phải trả NVKD (3341, gắn người lao động) | Khi tắt "Dùng HRMS" |
| Hoa hồng NVKD (qua lương) | — | — | Khi bật "Dùng HRMS": đẩy qua **Lương bổ sung**, không sinh bút toán riêng |
| Phí giấy phép viễn thông (GPVT) | TK phí GPVT (vd 6425) | TK phí, lệ phí phải nộp (3338 / 33382) | Phí nhà nước |
| Dịch vụ quản lý / Chi phí ngoài (phải trả người nhận) | TK chi phí tương ứng | TK phải trả (3388) | 2 vế |
| Phải trả phía khách có khấu trừ TNCN (giới thiệu/đích danh) | TK chi phí | TK phải trả người ngoài (3388) + TK thuế TNCN tạm giữ (3335) | 3 vế: net cho người nhận + TNCN giữ lại |

> Số hiệu TK ở trên là ví dụ — số thực do kế toán cấu hình trong **Thiết lập PAKD**, theo hệ thống tài khoản TT99/2025 của công ty.

## Tình huống đặc biệt & cảnh báo

- **Hóa đơn tự sinh ở trạng thái nháp:** hệ thống chỉ tạo hóa đơn nháp khi đến kỳ; kế toán phải tự ghi sổ. Hóa đơn nháp gắn hợp đồng nằm ở **Hóa đơn cần ghi sổ**, không lẫn với hóa đơn lẻ ngoài hợp đồng.
- **Hoa hồng ghi sổ theo cơ sở tiền (cash-basis):** chỉ ghi sổ hoa hồng cho kỳ đã thu được tiền của khách. Khi bấm "Đăng theo tỷ lệ", hệ thống tính phần hoa hồng tương ứng số tiền thực thu/tổng doanh thu hợp đồng.
- **Một hợp đồng chỉ có một PAKD đang hiệu lực:** không thể lập PAKD thứ hai cho cùng hợp đồng (trừ PAKD đã hủy).
- **Khoản phải trả phía khách thường KHÔNG được trừ thuế TNDN:** khoản chi cho cá nhân ngoài lương không có hóa đơn hợp pháp bị đánh dấu "không trừ TNDN" mặc định (theo nguyên tắc thuế TNDN). Việc khấu trừ TNCN và việc được trừ TNDN là hai sắc thuế khác nhau — kế toán xác nhận trên hộp thoại khi đăng.
- **Trung lập về nghiệp vụ:** các khoản "phải trả phía khách" (giới thiệu / chênh lệch giá / dịch vụ quản lý) được hệ thống ghi nhận theo cấu hình; tài liệu này chỉ mô tả cơ chế ghi sổ, không đánh giá bản chất nghiệp vụ.

## Báo cáo liên quan

- Phân hệ **Tổng hợp** (Sổ Cái, phiếu kế toán) để xem các bút toán hoa hồng đã ghi sổ.
- Phân hệ **Bán hàng** (hóa đơn bán hàng) và **Ngân hàng** (đối soát phiếu thu) để theo dõi hóa đơn + dòng tiền của hợp đồng.

## FAQ

**Q: Hợp đồng và PAKD khác nhau thế nào?**
**A:** Hợp đồng là cam kết với khách (giá, gói dịch vụ, kỳ hạn, lịch xuất hóa đơn). PAKD gắn vào một hợp đồng và tính phần "chi" nội bộ phát sinh từ hợp đồng đó — hoa hồng NVKD, phí giấy phép, khoản phải trả phía khách. Một hợp đồng có tối đa một PAKD hiệu lực.

**Q: Vì sao hoa hồng chưa ghi sổ dù PAKD đã duyệt?**
**A:** Hoa hồng ghi sổ theo cơ sở tiền — chỉ ghi cho kỳ khách đã thanh toán. Mở **Sổ hoa hồng NVKD** và **Phải trả phía khách** để xem khoản nào đủ điều kiện ghi sổ (kỳ đã thu tiền) rồi đăng.

**Q: Hoa hồng NVKD ghi vào sổ lương hay sổ kế toán?**
**A:** Tùy thiết lập "Dùng HRMS". Bật → hoa hồng NVKD đi qua **Lương bổ sung** (vào kỳ lương). Tắt → sinh **bút toán** riêng, ghi Có vào TK phải trả người lao động gắn đích danh NVKD.
