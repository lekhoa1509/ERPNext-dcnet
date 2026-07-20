---
title: Dự án — Giá thành công trình
order: 5
summary: Hồ sơ tính giá thành cho doanh nghiệp xây lắp — gom chi phí theo giai đoạn, tính giá xuất, xuất hóa đơn từng đợt, sinh bút toán 627 → 154 → 632.
---

## Mục đích

**Dự án — Giá thành** (Công trình & Giá thành) là hồ sơ trung tâm để doanh nghiệp xây lắp / thi công công trình:

1. **Gom chi phí thực tế** theo nhiều giai đoạn cho mỗi công trình.
2. **Tính giá xuất hóa đơn linh hoạt** theo 6 phương pháp markup.
3. **Xuất hóa đơn theo từng đợt nghiệm thu** (một công trình có thể nhiều hóa đơn).
4. **Báo cáo lãi/lỗ chi tiết** theo công trình + giai đoạn, phân biệt chi phí trực tiếp và phân bổ.
5. **Sinh bút toán đúng TT99/2025** — chuỗi 627 → 154 → 632 cho doanh nghiệp thi công.

Mỗi công trình có một hồ sơ giá thành (gắn 1:1 với Dự án). Dùng cho kế toán trưởng và quản lý dự án.

## Khi nào dùng

- Khi nhận một công trình mới: tạo hồ sơ giá thành và khai các giai đoạn dự kiến.
- Khi phát sinh chi phí công trình (mua vật tư, lương thợ, khấu hao): tag công trình.
- Cuối tháng: pin chi phí "kho chung" vào giai đoạn (qua Pivot Tool), kết chuyển chi phí gián tiếp.
- Khi nghiệm thu một đợt: tạo hóa đơn bán hàng từ giai đoạn tương ứng.
- Khi hoàn tất: đóng công trình, chốt lãi/lỗ, đưa TK 154 về 0.

## Cách thực hiện

1. Vào **Giá thành → Dự án — Giá thành** → **+ Thêm** → chọn **Dự án** (Project). Hệ thống tự lấy tên, khách hàng, công ty.
2. Tab **Stages & Pin chi phí**: khai các **giai đoạn** (tạm ứng / thi công / nghiệm thu...), mỗi giai đoạn có một phương pháp markup và một ngày dự kiến xuất hóa đơn. Xem [6 phương pháp markup cho giai đoạn](project-costing-stage-markup.md).
3. Nhập chi phí hằng ngày qua phiếu mua hàng / phiếu xuất kho / hoàn ứng, **tag công trình** (giai đoạn để trống cũng được — vào "kho chung").
4. Cuối tháng: mở **Pivot Tool** (tab Stages) → pin chi phí từ kho chung vào giai đoạn → bấm **Tính lại** để cập nhật giá đề xuất. Xem [Pivot Tool](project-costing-pivot-tool.md).
5. Khi nghiệm thu: trên thẻ giai đoạn bấm **Tạo HĐ** → hệ thống sinh hóa đơn bán hàng nháp → kế toán review và ghi sổ.
6. Khi hoàn tất: bấm **Đóng công trình** → chốt số dư 154. Xem [Đóng công trình](project-costing-close.md).

## Định khoản tự động

| Trường hợp | TK Nợ | TK Có | Ghi chú |
|---|---|---|---|
| Kết chuyển chi phí gián tiếp vào công trình | 154 (gắn công trình) | 627 / 622 / 6424 | Qua [Kết chuyển CP SXC](project-costing-allocation-run.md) |
| Bù tài khoản dở dang khi override TK 154 trên chứng từ chi phí | 154 | TK chi phí gốc | Tự sinh khi kế toán đổi TK trên chứng từ |
| Giá vốn theo giai đoạn khi hóa đơn ghi sổ | **632** | **154** (gắn công trình) | Sinh khi hóa đơn của giai đoạn được ghi sổ |
| Write-off khi đóng công trình còn dư | 642 (hoặc 632) | 154 | Khi đóng có chi phí dư |

Doanh thu theo tiến độ ghi nhận trên hóa đơn bán hàng (Nợ 131 / Có 511). Mở hồ sơ công trình → kéo xuống mục **Bút toán liên quan** để xem tất cả bút toán hệ thống đã sinh, mỗi dòng có liên kết tới bút toán.

## Tình huống đặc biệt & cảnh báo

- **Mọi chi phí liên quan công trình phải tag công trình** — bỏ trống thì không vào báo cáo công trình.
- **Phiếu mua hàng vào kho chung** (dùng dần nhiều công trình): KHÔNG tag công trình; khi dùng thì tạo phiếu xuất kho theo số lượng thực tế và tag công trình trên phiếu xuất.
- **Bảng chấm công KHÔNG phải nguồn chi phí** — không phát sinh bút toán; lương hạch toán qua bảng lương rồi kết chuyển. Xem [Phân bổ lương + khấu hao](project-costing-luong-khau-hao.md).
- **TK 627 và 642 cần kế toán trưởng cấu hình** nếu hệ thống tài khoản chưa có sẵn (154 và 632 được điền tự động khi cài đặt).
- **Phân quyền:** kế toán viên chỉ xem; pin chi phí / tạo hóa đơn nháp dành cho quản lý dự án và kế toán trưởng; ghi sổ hóa đơn và đóng công trình dành cho kế toán trưởng.

## Báo cáo liên quan

- [6 phương pháp markup cho giai đoạn](project-costing-stage-markup.md).
- [Pivot Tool — gán chi phí vào giai đoạn](project-costing-pivot-tool.md).
- [Kết chuyển CP SXC (627 → 154)](project-costing-allocation-run.md).
- [Phân bổ lương + khấu hao thiết bị vào công trình](project-costing-luong-khau-hao.md).
- [Đóng công trình và xử lý chi phí dư](project-costing-close.md).
- [Tiến độ xuất hóa đơn công trình](project-invoicing-progress.md).
- [Setup dự án xây lắp](du-an-xay-lap.md).

## FAQ

**Q: Một công trình bắt buộc một hóa đơn?**
**A:** Không. Mỗi giai đoạn xuất một hóa đơn riêng theo đợt nghiệm thu — phù hợp thực tế xây lắp thanh toán theo tiến độ.

**Q: Cấu hình TK mặc định ở đâu?**
**A:** Mở **Cài đặt kế toán → Giá thành công trình**: TK dở dang (154), TK gom chi phí gián tiếp (627), TK giá vốn (632), TK write-off khi đóng (642).

**Q: Đóng công trình mà TK 154 còn dư thì sao?**
**A:** Hệ thống hỏi cách xử lý phần dư (write-off 642 hoặc 632). Xem [Đóng công trình](project-costing-close.md).
