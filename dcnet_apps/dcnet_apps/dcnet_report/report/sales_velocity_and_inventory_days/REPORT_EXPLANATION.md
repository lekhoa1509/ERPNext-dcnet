# Sales Velocity and Inventory Days Report

## Mục đích

Report này phân tích **tốc độ luân chuyển hàng hoá** bằng cách kết hợp hai thông tin:

1. **Stock Aging (FIFO)** — tuổi hàng tồn kho dựa trên phương pháp FIFO
2. **Sales Velocity** — tốc độ bán hàng trung bình trong khoảng thời gian phân tích

Từ đó tính ra **Inventory Days** — số ngày dự kiến hàng tồn kho sẽ hết dựa trên tốc độ bán hiện tại.

---

## Tại sao báo cáo dùng chuẩn FIFO để tính Tuổi hàng?

Báo cáo này **bắt buộc sử dụng thuật toán FIFO (Nhập trước - Xuất trước)** để đếm số ngày lưu kho, độc lập với trường `Valuation Method` (Moving Average, LIFO...) được chọn trên hệ thống.

**Lý do:**

1. **Dòng luân chuyển vật lý thực tế:** Trong kho bãi, nhân viên luôn ưu tiên xuất lô hàng cũ đi trước (FIFO) để tránh hết hạn. Do đó, việc giả định lượng hàng CÒN TỒN thuộc về những lô nhập MỚI NHẤT là cách chính xác nhất để do "Tuổi hàng" (Age).
2. **Phương pháp Kế toán (Valuation Method) gây sai lệch Tuổi:** Moving Average trộn lẫn đơn giá các lô hàng với nhau (nhưng không thể trộn ngày nhập). LIFO thì giả định lấy hàng mới nhất đi giao khách và giữ lại hàng cũ nhất trong kho (làm Tuổi hàng tồn báo cáo ra bị già cỗi sai lệch với thực tế kho bãi).

Vì vậy, chọn FIFO làm tiêu chuẩn tính Tuổi Hàng mang lại giá trị quản trị kho sát thực tế nhất.

---

## Ví dụ minh họa các chỉ số chính (Formula & Example)

Giả sử bạn đang cài bộ lọc:

- **From Date:** `01-03-2026`
- **To Date:** `30-03-2026`
- **Period:** `Day` (1 ngày)

Sản phẩm A có các biến động giao dịch như sau:

- Trước đó (tháng 2) tồn: 0 cái
- Ngày 10-03: Nhập 100 cái.
- Ngày 15-03: Bán ra 40 cái.
- Ngày 25-03: Bán ra 20 cái.

| Chỉ số | Cách tính & Diễn giải | Ví dụ áp dụng |
| --- | --- | --- |
| **Available Qty** <br>*(Tồn kho lúc này)* | Tính bằng Tổng lượng tồn kho chốt tại cuối ngày **To Date**. Chỉ số này KHÔNG quan tâm đến `From Date`. | Dù `From Date` là ngày nào, tồn kho chốt tại `30-03` vẫn là: <br>`100 (nhập) - 40 (xuất) - 20 (xuất) = 40 cái` |
| **Total Sold Qty** <br>*(Tổng bán)* | Tổng số lượng hàng đã xuất đi trong giai đoạn từ `From Date` → `To Date`. | Tổng suất bán từ `01-03` đến `30-03`: <br>`40 + 20 = 60 cái` |
| **Avg Sales / Period** <br>*(Tốc độ tiêu thụ)* | Bằng `Total Sold Qty ÷ Số Period`. Phản ánh lượng bán trung bình trong một phân đoạn thời gian (Period). | Số lượng ngày phân tích = (30 - 01) + 1 = 30 ngày = 30 Periods.<br>`Tốc độ bán/ngày = 60 cái ÷ 30 ngày = 2 cái/ngày`. |
| **Inventory Days** <br>*(Hạn cạn kho)* | Bằng `Available Qty ÷ Tốc độ bán mỗi ngày`. Dự báo số ngày cạn kho nếu tiếp tục duy trì tốc độ tiêu thụ hiện tại. | Với lượng tồn 40 cái, mỗi ngày đi 2 cái. <br> `Inventory Days = 40 ÷ 2 = 20 ngày` (khoảng 20 ngày nữa sập kho nếu không nhập thêm). |

---

## Bộ lọc (Filters)

| Filter | Mô tả |
| --- | --- |
| **Company** | Công ty cần phân tích (bắt buộc) |
| **From Date** | Ngày bắt đầu khoảng thời gian tính tốc độ bán (mặc định: 30 ngày trước) |
| **To Date** | Ngày kết thúc phân tích — tồn kho tính đến ngày này (bắt buộc) |
| **Period** | Đơn vị thời gian để tính trung bình: Day, Week, Month, Quarter, Year |
| **Warehouse** | Lọc theo kho cụ thể |
| **Item** | Lọc theo mã hàng |
| **Brand** | Lọc theo thương hiệu |
| **Show Warehouse-wise Stock** | Hiển thị chi tiết theo từng kho |

---

## Các cột trong bảng kết quả

### Thông tin sản phẩm

| Cột | Mô tả |
| --- | --- |
| Item Code | Mã sản phẩm |
| Item Name | Tên sản phẩm |
| Description | Mô tả sản phẩm |
| Item Group | Nhóm sản phẩm |
| Brand | Thương hiệu |
| Warehouse | Kho (chỉ hiển thị khi bật "Show Warehouse-wise Stock") |

### Tồn kho & Tuổi hàng

| Cột | Mô tả |
| --- | --- |
| **Available Qty** | Số lượng tồn kho hiện tại (tính đến "To Date") |
| **Age Details** | Diễn giải chi tiết công thức chia lô tính tuổi hàng theo phương pháp FIFO |
| **Average Age** | Tuổi trung bình hàng tồn kho tính theo FIFO (ngày). Công thức: `Σ(Số lượng lô × Số ngày tồn của lô) ÷ Tổng số lượng tồn` |

### Tốc độ bán & Thời gian lưu kho

| Cột | Công thức | Mô tả |
| --- | --- | --- |
| **Total Sold Qty** | `SUM(ABS(actual_qty))` với `actual_qty < 0` | Tổng số lượng xuất kho trong khoảng From Date → To Date |
| **Avg Sales / Period** | `Total Sold Qty ÷ Số period` | Số lượng bán trung bình mỗi period (đơn vị do bạn chọn) |
| **Inventory Days** | `Available Qty ÷ (Total Sold Qty ÷ Số ngày phân tích)` | Số ngày dự kiến hàng sẽ hết nếu duy trì tốc độ bán hiện tại. Giá trị **0** = không có bán hàng |

### Thông tin bổ sung

| Cột | Mô tả |
| --- | --- |
| UOM | Đơn vị tính của sản phẩm |

---

## Chi tiết công thức bổ sung

### Tốc độ bán trung bình tính theo Period khác

```
Số ngày phân tích = (To Date - From Date) + 1
Số period = Số ngày phân tích ÷ Số ngày/period

- Day: 1 ngày
- Week: 7 ngày
- Month: 30 ngày
- Quarter: 90 ngày
- Year: 365 ngày

Total Sold Qty = SUM(|actual_qty|) từ SLE có actual_qty < 0, trong khoảng From Date → To Date
Avg Sales / Period = Total Sold Qty ÷ Số period
```

- Nếu quá trình tính toán tốc độ bán hàng mỗi ngày = 0 → `Inventory Days = 0` (không ước tính được số ngày sập kho do không có tốc độ tiêu thụ).

### Tuổi trung bình (Average Age)

- Dựa trên FIFO queue, mỗi lô hàng có ngày nhận (`posting_date`) riêng
- Tuổi của từng lô = `To Date - posting_date`
- Công thức cuối cùng của Average Age hiển thị trên báo cáo:
  `Σ (Số lượng lô × Tuổi của lô) ÷ Tổng số lượng tồn kho`

---

## Cách đọc và sử dụng

### Phân tích nhanh

| Inventory Days | Ý nghĩa | Hành động |
| --- | --- | --- |
| **0** | Không có bán hàng trong khoảng thời gian | Cân nhắc khuyến mãi hoặc thanh lý |
| **< 30** | Hàng bán rất nhanh | Kiểm tra để kịp thời nhập hàng |
| **30 - 60** | Luân chuyển bình thường | Duy trì tồn kho hiện tại |
| **60 - 90** | Luân chuyển chậm | Giảm lượng nhập hàng |
| **> 90** | Rủi ro tồn kho cao | Cần thanh lý hoặc giảm giá |

### Kết hợp với Average Age

- **Inventory Days cao + Average Age cao** = Hàng tồn lâu, bán chậm → ưu tiên xử lý
- **Inventory Days thấp + Average Age thấp** = Hàng mới, bán nhanh → rất tốt
- **Inventory Days thấp + Average Age cao** = Bán nhanh nhưng hàng tồn cũ → sẽ cải thiện dần
- **Inventory Days cao + Average Age thấp** = Hàng mới nhưng bán chậm → cần theo dõi

---

## Biểu đồ

Report hiển thị biểu đồ cột (bar chart) cho **top 10 sản phẩm** có Inventory Days cao nhất, bao gồm:

- **Avg Sales / Period** — tốc độ bán trung bình theo đơn vị period đã chọn
- **Inventory Days** — số ngày hàng tồn dự kiến còn

---

## Nguồn dữ liệu

- **Stock Ledger Entry** — sử dụng cả entry nhập và xuất kho
- **Item** — thông tin sản phẩm, nhóm, thương hiệu
- **Warehouse** — lọc và phân nhóm theo kho

> **Lưu ý:** Report sử dụng phương pháp FIFO để tính tuổi hàng tồn kho.
> Dữ liệu bán hàng chỉ tính các giao dịch xuất kho (actual_qty < 0) trong Stock Ledger Entry,
> bao gồm tất cả loại xuất kho (bán hàng, chuyển kho, v.v.)
