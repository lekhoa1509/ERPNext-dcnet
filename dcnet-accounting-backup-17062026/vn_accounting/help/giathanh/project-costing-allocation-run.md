---
title: Kết chuyển CP SXC (627 → 154)
order: 9
summary: Cuối kỳ phân bổ chi phí sản xuất chung / gián tiếp ra nhiều công trình, kết chuyển TK 627 sang TK 154 theo TT99/2025.
---

## Mục đích

Chi phí gián tiếp (chi phí sản xuất chung) là chi phí phát sinh cho nhiều công trình, không gắn trực tiếp một công trình duy nhất:

- Lương quản lý dự án (PM).
- Văn phòng phẩm chung.
- Chi phí xe công ty.
- Khấu hao thiết bị thi công dùng chung.

Theo TT99/2025, doanh nghiệp xây lắp / thi công bắt buộc gom các chi phí này vào **TK 627 — Chi phí sản xuất chung** và cuối kỳ **kết chuyển 627 sang 154** (chi phí sản xuất kinh doanh dở dang) cho từng công trình. **Đợt kết chuyển chi phí** (Cost Allocation Run) thực hiện việc này theo tỷ lệ phân bổ.

Dùng cho kế toán trưởng, chạy cuối tháng.

## Khi nào dùng

- Cuối tháng, sau khi đã gom đủ chi phí gián tiếp vào TK 627 (hoặc 622/6424 tùy nguồn).
- Khi cần chia lương PM, khấu hao thiết bị, chi phí chung ra các công trình đang thi công.
- Xem chi tiết các nguồn chi phí điển hình ở bài [Phân bổ lương + khấu hao thiết bị vào công trình](project-costing-luong-khau-hao.md).

## Cách thực hiện

1. Vào **Giá thành → Kết chuyển CP SXC (627→154)** → **+ Thêm**.
2. Điền **Kỳ bắt đầu / Kỳ kết thúc**, **Công ty**, **Ngày hạch toán** (mặc định cuối kỳ), **Phương pháp** (Đều / Thủ công).
3. (Tùy chọn) **TK ghi Có (override)**: chọn 627 mặc định, hoặc 622 (phân bổ lương trực tiếp), 6424 (khấu hao) tùy nguồn chi phí.
4. Bảng **Nguồn chi phí cần phân bổ**: thêm các chứng từ + số tiền (ví dụ hóa đơn văn phòng phẩm, bảng lương PM, bút toán khấu hao).
5. Bảng **Phân bổ ra công trình**: thêm các công trình đích.
   - **Đều**: hệ thống chia đều, dòng cuối nhận phần dư để tổng khớp.
   - **Thủ công**: nhập % từng công trình, tổng phải = 100%.
   - Có thể gắn **giai đoạn** cho từng dòng — để trống thì chi phí vào "kho chung" của công trình (chờ pin sau qua Pivot Tool).
6. **Lưu** → hệ thống tính lại số tiền từng dòng. **Ghi sổ** → sinh bút toán.

## Định khoản tự động

| Trường hợp | TK Nợ | TK Có | Ghi chú |
|---|---|---|---|
| Kết chuyển chi phí gián tiếp ra công trình | **154** (gắn từng công trình + giai đoạn) | **627** (hoặc TK ghi Có override: 622 / 6424) | Mỗi công trình một dòng Nợ, một dòng Có gộp |

Ví dụ tổng 36.000.000 chia đều 4 công trình:

```
Nợ 154 (công trình A)    9.000.000
Nợ 154 (công trình B)    9.000.000
Nợ 154 (công trình C)    9.000.000
Nợ 154 (công trình D)    9.000.000
       Có 627                        36.000.000
```

Mỗi dòng gắn tham chiếu về đợt kết chuyển để truy vết. Hủy đợt → bút toán tự đảo dấu (đánh dấu là đã hủy trên Sổ Cái).

## Tình huống đặc biệt & cảnh báo

- **Phương pháp Thủ công: tổng % phải bằng 100%** — nếu không, hệ thống chặn ghi sổ.
- **Không kết chuyển vào kỳ đã đóng sổ** — nếu kỳ trùng kỳ đã có chứng từ khóa sổ, hệ thống chặn; lùi sang kỳ sau hoặc mở lại kỳ.
- **Không kết chuyển vào giai đoạn đã xuất hóa đơn** — giai đoạn đã có bút toán giá vốn bị khóa.
- **Cảnh báo VAS — TK 627 còn số dư:** sau ghi sổ, nếu TK 627 vẫn còn số dư, hệ thống nhắc: theo TT99/2025 cuối kỳ TK 627 phải kết chuyển hết sang 154 (hoặc 632 nếu vượt công suất bình thường).
- **Cảnh báo VAS — công trình đã hoàn thành còn dư 154:** nếu công trình đích đã hoàn thành mà TK 154 còn số dư, hệ thống nhắc cần kết chuyển 154 → 632 hoặc write-off 154 → 642.
- **Phần vượt công suất bình thường** (chi phí SXC cố định vượt công suất) theo TT99 phải ghi thẳng Dr 632 — hiện kế toán tự tách thủ công nếu cần.

## Báo cáo liên quan

- [Phân bổ lương + khấu hao thiết bị vào công trình](project-costing-luong-khau-hao.md): các tình huống nguồn chi phí cụ thể.
- [Dự án — Giá thành](project-costing-tinh-gia-thanh.md): tổng quan công cụ tính giá thành công trình.
- [Pivot Tool — gán chi phí vào giai đoạn](project-costing-pivot-tool.md): pin chi phí "kho chung" vào giai đoạn.
- [Đóng công trình và xử lý chi phí dư](project-costing-close.md): kết chuyển 154 còn dư khi đóng.

## FAQ

**Q: Muốn phân bổ theo % giá trị hợp đồng hoặc % chi phí trực tiếp thì sao?**
**A:** Tự tính tỷ lệ rồi nhập % thủ công. Hệ thống chỉ hỗ trợ sẵn 2 phương pháp Đều và Thủ công để tránh sai công thức.

**Q: Đã ghi sổ rồi muốn sửa?**
**A:** Hủy đợt (nếu chưa có công trình đích xuất hóa đơn trong kỳ) — bút toán tự đảo dấu — rồi tạo lại. Nếu đã xuất hóa đơn, lập một đợt kết chuyển đảo dấu để điều chỉnh.
