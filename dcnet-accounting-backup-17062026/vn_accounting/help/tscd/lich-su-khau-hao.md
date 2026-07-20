---
title: Lịch sử khấu hao
order: 8
summary: Chi tiết từng lần ghi khấu hao theo tài sản — số khấu hao kỳ, lũy kế và giá trị còn lại tại thời điểm.
---

## Mục đích

**Lịch sử khấu hao** liệt kê chi tiết từng lần ghi nhận khấu hao của các tài sản trong kỳ: ngày khấu hao, số khấu hao kỳ đó, hao mòn lũy kế đầu kỳ và lũy kế đến thời điểm, giá trị còn lại và số phiếu kế toán ghi khấu hao. Đây là báo cáo tra cứu (sổ chi tiết khấu hao), không nhập liệu.

## Khi nào dùng

- Cuối tháng/kỳ: đối chiếu chi phí khấu hao đã ghi với sổ chi phí (TK 627/641/642/154).
- Kiểm tra một tài sản đã khấu hao bao nhiêu kỳ, mỗi kỳ bao nhiêu, còn lại bao nhiêu.
- Truy ngược phiếu kế toán ghi khấu hao của một kỳ cụ thể.
- Đối chiếu hao mòn lũy kế với số dư TK 2141.

## Cách thực hiện

1. Bấm **Lịch sử khấu hao** trên menu TSCĐ → báo cáo mở.
2. Lọc theo:
   - **Company** (bắt buộc) — mặc định công ty đang dùng.
   - **From Date / To Date** (bắt buộc) — khoảng thời gian ghi khấu hao (mặc định 1 tháng gần nhất).
   - **Asset** (tài sản) — lọc một tài sản cụ thể.
   - **Asset Category** (loại tài sản), **Cost Center** (trung tâm chi phí), **Finance Book** (sổ tài chính) — tùy chọn.
3. Bấm **Refresh**. Bảng hiển thị: Mã TS | Tên | Ngày khấu hao | Nguyên giá | Hao mòn đầu kỳ | Số khấu hao kỳ | Hao mòn lũy kế | Giá trị còn lại | Phiếu kế toán | Loại TS | TT chi phí | Trạng thái | Ngày mua.
4. Bấm số phiếu kế toán để mở chứng từ ghi khấu hao gốc.

## Định khoản tự động

Báo cáo **không tự định khoản** — chỉ tổng hợp các bút toán khấu hao đã ghi từ Sổ Cái. Mỗi dòng tương ứng một bút toán khấu hao:

| Vế | Tài khoản | Ghi chú |
|---|---|---|
| Nợ | 627/641/642/154 (chi phí khấu hao) | Tùy bộ phận sử dụng; cột "Số khấu hao kỳ" |
| Có | 2141 (hao mòn lũy kế) | Cột "Hao mòn lũy kế" cộng dồn |

> Báo cáo lấy các bút toán có tài khoản loại "Khấu hao" (Depreciation) đối ứng với tài sản trong khoảng ngày đã lọc.

## Tình huống đặc biệt & cảnh báo

- **Bắt buộc khoảng thời gian:** phải chọn Từ ngày và Đến ngày. Mặc định chỉ 1 tháng gần nhất — muốn xem cả năm, mở rộng khoảng ngày (ví dụ 01/01 đến 31/12).
- **Khác Sổ S21-DN:** báo cáo này hiển thị **từng lần** khấu hao (sổ chi tiết theo kỳ), còn S21-DN tổng hợp **một dòng/tài sản** (số dư lũy kế hiện tại). Dùng báo cáo này để truy số khấu hao thực tế từng kỳ.
- **Sổ tài chính mặc định:** ô "Include Default FB Assets" (gồm tài sản dùng sổ tài chính mặc định) bật sẵn — giữ nguyên trừ khi cần lọc theo một sổ tài chính riêng.
- **Chỉ tài sản có phát sinh khấu hao mới hiện:** tài sản chưa tới kỳ khấu hao hoặc chưa lập lịch sẽ không xuất hiện trong khoảng ngày đã chọn.
- **Báo cáo của hệ thống (ERP gốc):** đây là báo cáo chuẩn của hệ thống, nhãn cột hiển thị theo bản dịch — nội dung khớp các trường mô tả ở trên.

## Báo cáo liên quan

- **Sổ S21-DN:** tổng hợp một dòng/tài sản với khấu hao lũy kế và giá trị còn lại.
- **Tính khấu hao:** lịch khấu hao gốc sinh ra các bút toán hiển thị ở báo cáo này.
- **Sổ Cái:** chi tiết bút toán khấu hao (qua link phiếu kế toán).
- **Bảng cân đối số phát sinh:** đối chiếu số dư TK 2141.

## FAQ

**Q: Báo cáo trống dù có tài sản?**
**A:** Kiểm tra khoảng ngày — mặc định chỉ 1 tháng. Tài sản chỉ hiện nếu có bút toán khấu hao phát sinh trong khoảng đã chọn. Mở rộng Từ ngày/Đến ngày để bao trùm các kỳ đã khấu hao.

**Q: Số "Hao mòn lũy kế" trên báo cáo có khớp TK 2141 không?**
**A:** Khớp tại thời điểm của dòng cuối cùng mỗi tài sản (lũy kế đến ngày khấu hao gần nhất trong khoảng lọc). Tổng hao mòn lũy kế của toàn bộ tài sản đối ứng số dư Có TK 2141 trên Bảng cân đối số phát sinh.

**Q: Dùng báo cáo này hay Sổ S21-DN để in cho cơ quan thuế?**
**A:** Sổ S21-DN là sổ TSCĐ chính thức theo TT99/2025 (mẫu 01-TSCĐ). Lịch sử khấu hao là sổ chi tiết khấu hao để đối chiếu nội bộ — dùng kèm khi cần giải trình số khấu hao từng kỳ.
