# Module Sales Order - Sequence & Activity Diagrams

> **Nguồn:** `/docs/feature/ERP_SPECIFICATION.md` Section 2 - Quản lý Bán hàng
> **Lưu ý:** Diagrams dựa trên đặc tả YÊU CẦU, không dựa trên code hiện tại

---

## 1. Sequence Diagrams - Quy trình Bán buôn

### 1.1. Sequence: Tạo đơn hàng bán (Bước 1-4)

```mermaid
sequenceDiagram
    participant NV as Nhân viên Kinh doanh
    participant SO as Sales Order
    participant PL as Price List
    participant DP as Discount Policy
    participant DB as Database

    Note over NV: Bước 1-3: Chuẩn bị master data
    NV->>PL: Cập nhật bảng giá niêm yết
    PL->>DB: Lưu bảng giá
    NV->>DP: Cập nhật chính sách chiết khấu
    DP->>DB: Lưu chính sách

    Note over NV: Bước 4: Tạo đơn hàng
    NV->>SO: Tạo đơn hàng mới
    SO->>SO: Khởi tạo form
    NV->>SO: Nhập thông tin chung (KH, ngày giao)
    NV->>SO: Thêm sản phẩm

    SO->>PL: Lấy giá bán theo ngày đơn hàng
    PL-->>SO: Trả về giá bán
    SO->>DP: Lấy chiết khấu theo KH và sản phẩm
    DP-->>SO: Trả về % chiết khấu

    SO->>SO: Tính toán:<br/>- Thành tiền trước CK<br/>- Tiền chiết khấu<br/>- Thành tiền sau CK

    NV->>SO: Submit đơn hàng
    SO->>DB: Lưu đơn hàng
    DB-->>SO: OK
    SO-->>NV: Đơn hàng đã tạo (Status: Draft)
```

### 1.2. Sequence: Kiểm tra tồn kho và tạo lệnh xuất (Bước 5-6)

```mermaid
sequenceDiagram
    participant NV as Nhân viên Kinh doanh
    participant SO as Sales Order
    participant Stock as Stock Ledger
    participant DO as Delivery Note
    participant Kho as Nhân viên Kho

    Note over NV: Bước 5: Kiểm tra tồn kho
    NV->>SO: Xem đơn hàng
    NV->>Stock: Kiểm tra tồn kho
    Stock->>Stock: Tính Available Stock:<br/>Actual Stock - Reserved Stock
    Stock-->>NV: Hiển thị tồn kho khả dụng

    alt Đủ hàng
        Note over NV: Bước 6: Tạo lệnh xuất hàng
        NV->>DO: Tạo lệnh xuất từ đơn hàng
        DO->>SO: Kế thừa dữ liệu
        SO-->>DO: Trả về dữ liệu đơn hàng
        DO->>DO: Điền thông tin:<br/>- Kho xuất<br/>- Ngày đề nghị
        NV->>DO: Submit lệnh xuất
        DO->>DO: Status: Pending Credit Check
        DO->>Kho: Gửi thông báo có lệnh xuất mới
        DO-->>NV: Lệnh xuất đã tạo
    else Thiếu hàng
        Stock-->>NV: ⚠️ Không đủ hàng
        NV->>SO: Thông báo KH
        NV->>SO: Lập lại đơn hàng (nếu cần)
    end
```

### 1.3. Sequence: Kiểm tra công nợ (Bước 7-8) - AUTO

```mermaid
sequenceDiagram
    participant DO as Delivery Note
    participant System as Hệ thống
    participant CL as Credit Limit
    participant AR as Accounts Receivable
    participant SI as Sales Invoice
    participant KTT as Kế toán trưởng
    participant NV as Nhân viên Kinh doanh

    Note over DO: Bước 7-8: Kiểm tra công nợ tự động
    DO->>System: Trigger credit check
    System->>CL: Lấy hạn mức công nợ của KH
    CL-->>System: Trả về credit_limit_amount

    System->>AR: Lấy công nợ hiện tại
    AR-->>System: Trả về current_outstanding

    System->>DO: Lấy tổng giá trị lệnh xuất chưa xuất
    DO-->>System: Trả về pending_delivery_amount

    System->>System: Tính công nợ dự kiến:<br/>current + pending + this_order

    System->>SI: Kiểm tra hóa đơn quá hạn
    SI-->>System: Trả về danh sách overdue_invoices

    alt Điều kiện 1: Có HĐ quá hạn
        System->>System: ❌ Credit Check Failed
        System->>KTT: Gửi yêu cầu duyệt ngoại lệ
        System->>NV: Hiển thị cảnh báo:<br/>- Danh sách HĐ quá hạn
        KTT->>System: Xem yêu cầu duyệt ngoại lệ
        KTT->>System: Nhập lý do duyệt
        KTT->>System: Duyệt ngoại lệ
        System->>DO: Status: Exception Approved
        System-->>NV: ✅ Đã duyệt, cho phép xuất hàng
    else Điều kiện 2: Công nợ dự kiến > Hạn mức
        System->>System: ❌ Credit Check Failed
        System->>KTT: Gửi yêu cầu duyệt ngoại lệ
        System->>NV: Hiển thị cảnh báo:<br/>- Công nợ thực tế<br/>- Công nợ dự kiến<br/>- Hạn mức
        KTT->>System: Xem yêu cầu duyệt ngoại lệ
        alt Kế toán trưởng duyệt
            KTT->>System: Duyệt ngoại lệ
            System->>DO: Status: Exception Approved
            System-->>NV: ✅ Đã duyệt, cho phép xuất hàng
        else Kế toán trưởng từ chối
            KTT->>System: Từ chối
            System->>DO: Status: Rejected
            System->>NV: ❌ Không cho xuất hàng
            System-->>NV: Thông báo KH cần thanh toán công nợ
        end
    else Cả 2 điều kiện OK
        System->>System: ✅ Credit Check Passed
        System->>DO: Status: Credit OK
        System-->>NV: ✅ Cho phép xuất hàng
    end
```

### 1.4. Sequence: Xuất hàng và xuất hóa đơn (Bước 6-9) - Phân quyền

```mermaid
sequenceDiagram
    participant NV as Nhân viên Kinh doanh
    participant DO as Delivery Note
    participant Kho as Nhân viên Kho
    participant Stock as Stock Entry
    participant KT as Kế toán
    participant SI as Sales Invoice
    participant PL as Price List
    participant DP as Discount Policy

    Note over NV,Kho: Bước 6: Kho xuất hàng (Phân quyền)
    NV->>DO: Submit lệnh xuất (đã qua credit check)
    DO->>Kho: Gửi thông báo có lệnh xuất mới

    Kho->>DO: Xem lệnh xuất hàng
    DO->>DO: Phân quyền: Ẩn giá, thành tiền
    DO-->>Kho: Hiển thị:<br/>- Khách hàng (readonly)<br/>- Sản phẩm (readonly)<br/>- Số lượng yêu cầu (readonly)<br/>❌ KHÔNG hiển thị giá, thành tiền

    Kho->>Kho: Lấy hàng theo yêu cầu
    Kho->>DO: Cập nhật thông tin thực xuất:<br/>- Số lượng thực tế<br/>- Serial number<br/>- Batch number<br/>- Kho xuất

    Kho->>DO: Xác nhận đã xuất hàng
    DO->>Stock: Tạo Stock Entry
    Stock->>Stock: Trừ tồn kho
    DO->>DO: Status: Delivered
    DO->>KT: Gửi thông báo đã xuất hàng

    Note over KT,SI: Bước 9: Xuất hóa đơn
    KT->>DO: Xem lệnh xuất đã hoàn thành
    KT->>SI: Tạo hóa đơn từ lệnh xuất
    SI->>DO: Kế thừa dữ liệu
    DO-->>SI: Trả về:<br/>- Khách hàng<br/>- Sản phẩm<br/>- Số lượng THỰC XUẤT<br/>- Serial, Batch

    SI->>SI: Lấy ngày hóa đơn hiện tại
    SI->>PL: Lấy bảng giá theo ngày HĐ
    PL-->>SI: Trả về giá bán
    SI->>DP: Lấy chính sách CK theo ngày HĐ
    DP-->>SI: Trả về % chiết khấu

    SI->>SI: So sánh giá lệnh xuất vs HĐ
    alt Giá khác nhau
        SI->>KT: ⚠️ Cảnh báo: Giá lệnh xuất khác giá HĐ
        KT->>SI: Xác nhận và nhập lý do
        SI->>SI: Ghi log sự khác biệt giá
    end

    KT->>SI: Nhập điều khoản thanh toán
    KT->>SI: Submit hóa đơn
    SI->>SI: Tính toán:<br/>- Tổng tiền hàng<br/>- Tổng tiền CK<br/>- Tổng tiền thuế<br/>- Tổng tiền
    SI->>SI: Status: Unpaid
    SI-->>KT: Hóa đơn đã tạo
```

### 1.5. Sequence: Xử lý trả hàng (Bước 10-11)

```mermaid
sequenceDiagram
    participant KH as Khách hàng
    participant NV as Nhân viên Kinh doanh
    participant RR as Return Request
    participant SI as Sales Invoice
    participant Kho as Nhân viên Kho
    participant PR as Purchase Receipt
    participant KT as Kế toán
    participant SR as Sales Return
    participant AR as Accounts Receivable

    Note over KH,NV: Bước 10: Lệnh nhập hàng trả lại
    KH->>NV: Yêu cầu trả hàng
    NV->>RR: Tạo lệnh nhập hàng trả lại
    RR->>SI: Kế thừa từ hóa đơn bán hàng
    SI-->>RR: Trả về thông tin HĐ

    NV->>RR: Chọn sản phẩm cần trả
    NV->>RR: Nhập số lượng trả
    NV->>RR: Nhập Serial/Batch cần trả
    NV->>RR: Chọn kho nhập
    NV->>RR: Nhập lý do trả hàng
    NV->>RR: Submit lệnh nhập

    RR->>Kho: Gửi thông báo có hàng trả lại

    Kho->>RR: Xem lệnh nhập hàng trả lại
    Kho->>Kho: Nhận hàng và kiểm tra
    Kho->>RR: Cập nhật thông tin thực nhập:<br/>- Mã hàng<br/>- Serial<br/>- Batch<br/>- Số lượng<br/>- Kho
    Kho->>RR: Xác nhận đã nhập hàng
    RR->>PR: Tạo Purchase Receipt
    PR->>PR: Cập nhật tồn kho +
    RR->>KT: Gửi thông báo đã nhập hàng trả lại

    Note over KT,SR: Bước 11: Xử lý hàng bán bị trả lại
    KT->>RR: Xem lệnh nhập hàng trả lại đã hoàn thành
    KT->>SR: Tạo phiếu hàng bán trả lại
    SR->>RR: Kế thừa dữ liệu
    RR-->>SR: Trả về thông tin lệnh nhập

    SR->>SI: Kiểm tra Serial có trong HĐ ban đầu?
    alt Serial không tồn tại
        SI-->>SR: ❌ Serial không tìm thấy
        SR->>KT: ⚠️ Cảnh báo: Serial không tồn tại trong HĐ bán
        KT->>SR: Xác nhận và nhập lý do
        SR->>SR: Ghi log ngoại lệ
    else Serial hợp lệ
        SI-->>SR: ✅ Serial hợp lệ
    end

    KT->>SR: Submit phiếu trả hàng
    SR->>AR: Cập nhật công nợ KH (giảm công nợ)
    AR-->>SR: OK

    alt Hoàn tiền
        SR->>SR: Tạo phiếu chi tiền
        SR-->>KH: Hoàn tiền
    else Ghi giảm trừ công nợ
        SR->>AR: Cập nhật sổ cái
        SR-->>KH: Ghi giảm trừ công nợ
    end

    SR-->>KT: Hoàn thành xử lý trả hàng
```

### 1.6. Sequence: Tính thưởng đạt kế hoạch doanh số (Bước 12)

```mermaid
sequenceDiagram
    participant KT as Kế toán
    participant System as Hệ thống
    participant AST as Annual Sales Target
    participant SI as Sales Invoice
    participant Bonus as Bonus Calculation
    participant AR as Accounts Receivable
    participant GL as General Ledger

    Note over KT: Bước 12: Tính thưởng đạt KH doanh số
    KT->>System: Chọn "Tính thưởng đạt kế hoạch doanh số"
    System->>AST: Lấy danh sách KH có kế hoạch doanh số
    AST-->>System: Trả về danh sách KH

    System-->>KT: Hiển thị danh sách KH

    KT->>System: Chọn khách hàng cần tính thưởng
    System->>AST: Lấy kế hoạch doanh số của KH
    AST-->>System: Trả về target_amount

    System->>SI: Lấy doanh số thực tế của KH (theo năm/kỳ)
    SI->>SI: Tính tổng doanh số:<br/>SUM(grand_total) WHERE customer = X
    SI-->>System: Trả về actual_sales

    System->>Bonus: Tính toán thưởng
    Bonus->>Bonus: Tính % đạt kế hoạch:<br/>achievement_percentage = (actual_sales / target_amount) × 100

    Bonus->>Bonus: Tính tiền thưởng theo quy định:<br/>- Đạt 80-100%: Thưởng X%<br/>- Đạt 100-120%: Thưởng Y%<br/>- Đạt >120%: Thưởng Z%

    Bonus-->>System: Trả về bonus_amount

    System-->>KT: Hiển thị:<br/>- Doanh số kế hoạch<br/>- Doanh số thực tế<br/>- % đạt kế hoạch<br/>- Tiền thưởng/CKKM

    KT->>System: Xác nhận
    System->>AR: Ghi nhận giảm trừ công nợ
    AR->>GL: Tạo bút toán:<br/>- Debit: Chi phí bán hàng<br/>- Credit: Công nợ phải thu
    GL-->>System: OK

    System->>System: Tạo phiếu thu tiền mặt (nếu thanh toán ngay)
    System-->>KT: Hoàn thành tính thưởng
```

---

## 2. Sequence Diagrams - Quy trình Bán lẻ

### 2.1. Sequence: Lập hóa đơn bán lẻ (POS) - Bước 1-3

```mermaid
sequenceDiagram
    participant KH as Khách hàng
    participant NV as Nhân viên Cửa hàng
    participant POS as POS System
    participant RPL as Retail Price List
    participant RDP as Retail Discount Policy
    participant Stock as Stock Ledger
    participant RI as Retail Invoice
    participant Payment as Payment Gateway

    Note over KH,NV: Bước 1-2: Chuẩn bị bảng giá và chính sách CK
    Note over KH,NV: Bước 3: Lập hóa đơn bán lẻ

    KH->>NV: Đến cửa hàng
    NV->>POS: Mở POS

    alt Khách hàng có SĐT
        NV->>POS: Nhập SĐT khách hàng
        POS->>POS: Tìm kiếm khách hàng
        POS-->>NV: Hiển thị:<br/>- Tên<br/>- Địa chỉ<br/>- Doanh số lũy kế
    else Khách vãng lai
        NV->>POS: Bỏ qua nhập SĐT
    end

    KH->>NV: Đưa sản phẩm
    NV->>POS: Quét mã sản phẩm hoặc chọn thủ công

    POS->>RPL: Lấy giá bán lẻ
    RPL-->>POS: Trả về retail_price

    POS->>RDP: Lấy chiết khấu theo chính sách
    RDP-->>POS: Trả về policy_discount_percentage

    alt Áp dụng chiết khấu đặc biệt
        NV->>POS: Nhập % chiết khấu đặc biệt
        POS->>POS: Tính tiền CK đặc biệt:<br/>tiền hàng - CK chính sách × % CK đặc biệt
    end

    NV->>POS: Nhập số lượng

    POS->>Stock: Kiểm tra tồn kho
    Stock-->>POS: Trả về available_qty

    alt Đủ hàng
        POS->>POS: Thêm vào giỏ hàng
        POS-->>NV: Hiển thị giỏ hàng
    else Hết hàng
        POS-->>NV: ⚠️ Hết hàng
    end

    loop Thêm sản phẩm khác
        KH->>NV: Đưa sản phẩm tiếp theo
        NV->>POS: Quét mã sản phẩm
        Note over POS: Lặp lại quy trình trên
    end

    NV->>POS: Chọn loại thuế, thuế suất
    POS->>POS: Tính tổng:<br/>- Tiền hàng<br/>- Tiền CK<br/>- Tiền thuế<br/>- Tổng tiền

    POS-->>NV: Hiển thị tổng tiền
    NV->>KH: Thông báo tổng tiền

    alt Thanh toán tiền mặt
        KH->>NV: Đưa tiền mặt
        NV->>POS: Nhập tiền khách đưa
        POS->>POS: Tính tiền thừa:<br/>Trả lại = Tiền đưa - Tổng tiền
        POS-->>NV: Hiển thị tiền thừa
        NV->>KH: Trả lại tiền thừa
    else Thanh toán thẻ
        NV->>POS: Chọn thanh toán thẻ
        POS->>Payment: Gửi yêu cầu thanh toán
        Payment-->>POS: Xác nhận thanh toán thành công
    else Thanh toán chuyển khoản
        NV->>POS: Chọn chuyển khoản
        POS-->>NV: Hiển thị thông tin TK
        KH->>KH: Chuyển khoản
        NV->>POS: Xác nhận đã nhận tiền
    else Công nợ
        NV->>POS: Chọn công nợ
        POS->>POS: Ghi nhận công nợ
    end

    NV->>POS: Nhập Serial/Batch cho từng sản phẩm

    NV->>POS: Chọn xuất hóa đơn điện tử
    alt Không lấy hóa đơn
        NV->>POS: Chọn "Không lấy hóa đơn"
    else Phát hành sau
        NV->>POS: Chọn "Phát hành sau"
        POS->>POS: Đưa vào queue
    else Phát hành ngay
        NV->>POS: Chọn "Phát hành ngay"
        POS->>POS: Phát hành hóa đơn điện tử ngay
    end

    NV->>POS: Submit hóa đơn
    POS->>RI: Tạo hóa đơn bán lẻ
    RI->>Stock: Trừ tồn kho
    Stock-->>RI: OK
    RI->>RI: Cập nhật doanh số lũy kế
    RI-->>POS: OK

    POS->>POS: In hóa đơn
    POS-->>NV: Hóa đơn đã in
    NV->>KH: Giao hóa đơn và hàng
```

---

## 3. Activity Diagrams

### 3.1. Activity: Tạo đơn hàng bán (End-to-End)

```mermaid
flowchart TD
    Start([Bắt đầu]) --> CheckMasterData{Đã có master data?}

    CheckMasterData -->|Chưa| CreatePriceList[Tạo bảng giá niêm yết]
    CheckMasterData -->|Có| CreateOrder

    CreatePriceList --> CreateDiscountPolicy[Tạo chính sách chiết khấu]
    CreateDiscountPolicy --> CreateOrder

    CreateOrder[Tạo đơn hàng bán]
    CreateOrder --> FillCustomer[Điền thông tin khách hàng]
    FillCustomer --> AddItem[Thêm sản phẩm]

    AddItem --> LoadPrice[Load giá từ bảng giá]
    LoadPrice --> LoadDiscount[Load chiết khấu từ chính sách]
    LoadDiscount --> Calculate[Tính toán thành tiền]

    Calculate --> MoreItem{Thêm sản phẩm?}
    MoreItem -->|Có| AddItem
    MoreItem -->|Không| Submit[Submit đơn hàng]

    Submit --> SaveOrder[(Lưu đơn hàng)]
    SaveOrder --> CheckStock[Kiểm tra tồn kho]

    CheckStock --> StockStatus{Đủ hàng?}
    StockStatus -->|Không| NotifyCustomer[Thông báo KH]
    NotifyCustomer --> End1([Kết thúc - Chờ hàng về])

    StockStatus -->|Có| CreateDeliveryNote[Tạo lệnh xuất hàng]

    CreateDeliveryNote --> CreditCheck[Kiểm tra công nợ tự động]

    CreditCheck --> CreditStatus{Hợp lệ?}
    CreditStatus -->|Vi phạm| ExceptionApproval{Kế toán trưởng duyệt?}
    CreditStatus -->|OK| DeliverGoods

    ExceptionApproval -->|Duyệt| DeliverGoods[Kho xuất hàng]
    ExceptionApproval -->|Từ chối| NotifyPayment[Thông báo KH thanh toán công nợ]
    NotifyPayment --> End2([Kết thúc - Chờ KH thanh toán])

    DeliverGoods --> CreateInvoice[Kế toán xuất hóa đơn]
    CreateInvoice --> WaitPayment[Chờ KH thanh toán]

    WaitPayment --> PaymentStatus{Đã thanh toán?}
    PaymentStatus -->|Chưa| WaitPayment
    PaymentStatus -->|Có| CheckReturn{Có trả hàng?}

    CheckReturn -->|Không| CalculateBonus[Tính thưởng đạt KH doanh số]
    CheckReturn -->|Có| ProcessReturn[Xử lý trả hàng]
    ProcessReturn --> CalculateBonus

    CalculateBonus --> End3([Hoàn thành])

    style CreateOrder fill:#dbeafe,stroke:#3b82f6,stroke-width:2px
    style CreditCheck fill:#fef3c7,stroke:#f59e0b,stroke-width:2px
    style ExceptionApproval fill:#fee2e2,stroke:#ef4444,stroke-width:2px
    style DeliverGoods fill:#a7fab9,stroke:#22c55e,stroke-width:2px
```

### 3.2. Activity: Kiểm tra công nợ và duyệt ngoại lệ

```mermaid
flowchart TD
    Start([Lệnh xuất hàng được tạo]) --> GetData[Lấy dữ liệu KH]

    GetData --> GetCreditLimit[Lấy hạn mức công nợ]
    GetCreditLimit --> GetOutstanding[Lấy công nợ hiện tại]
    GetOutstanding --> GetPendingDO[Lấy tổng lệnh xuất chưa xuất]
    GetPendingDO --> GetCurrentDO[Lấy giá trị lệnh xuất hiện tại]
    GetCurrentDO --> GetOverdue[Lấy danh sách HĐ quá hạn]

    GetOverdue --> CalculateTotal[Tính công nợ dự kiến:<br/>current + pending + current_do]

    CalculateTotal --> Check1{Có HĐ quá hạn?}

    Check1 -->|Có| Violation1[Vi phạm điều kiện 1]
    Check1 -->|Không| Check2{Công nợ dự kiến ≤ Hạn mức?}

    Check2 -->|Không| Violation2[Vi phạm điều kiện 2]
    Check2 -->|Có| AllOK[Cả 2 điều kiện OK]

    Violation1 --> ShowWarning[Hiển thị cảnh báo:<br/>- Số dư công nợ<br/>- Công nợ dự kiến<br/>- HĐ quá hạn<br/>- Hạn mức]
    Violation2 --> ShowWarning

    ShowWarning --> SendNotification[Gửi thông báo cho:<br/>- NV Kinh doanh<br/>- Kế toán trưởng]

    SendNotification --> WaitApproval[Chờ Kế toán trưởng duyệt]

    WaitApproval --> KTTReview{Kế toán trưởng xem xét}

    KTTReview -->|Duyệt| EnterReason[Nhập lý do duyệt ngoại lệ]
    KTTReview -->|Từ chối| EnterRejectReason[Nhập lý do từ chối]

    EnterReason --> LogApproval[Ghi log phê duyệt]
    EnterRejectReason --> LogReject[Ghi log từ chối]

    LogApproval --> UpdateStatus1[Status: Exception Approved]
    LogReject --> UpdateStatus2[Status: Rejected]
    AllOK --> UpdateStatus3[Status: Credit OK]

    UpdateStatus1 --> Approved[Cho phép xuất hàng]
    UpdateStatus3 --> Approved

    UpdateStatus2 --> Rejected[Không cho xuất hàng]
    Rejected --> NotifyCustomer[Thông báo KH thanh toán công nợ]

    Approved --> End1([Chuyển sang xuất hàng])
    NotifyCustomer --> End2([Kết thúc - Chờ thanh toán])

    style ShowWarning fill:#fee2e2,stroke:#ef4444,stroke-width:2px
    style WaitApproval fill:#fef3c7,stroke:#f59e0b,stroke-width:2px
    style Approved fill:#a7fab9,stroke:#22c55e,stroke-width:2px
    style Rejected fill:#fca6a2,stroke:#dc2626,stroke-width:2px
```

### 3.3. Activity: Xuất hàng với phân quyền

```mermaid
flowchart TD
    Start([Lệnh xuất đã qua credit check]) --> SendToWarehouse[Gửi lệnh xuất cho Kho]

    SendToWarehouse --> WarehouseLogin[Kho đăng nhập hệ thống]
    WarehouseLogin --> ViewDO[Kho xem lệnh xuất]

    ViewDO --> CheckPermission{Kiểm tra phân quyền}

    CheckPermission --> HidePrice[Ẩn:<br/>- Đơn giá<br/>- Thành tiền<br/>- Tiền chiết khấu<br/>- Tiền sau chiết khấu]

    HidePrice --> ShowReadonly[Hiển thị READONLY:<br/>- Khách hàng<br/>- Sản phẩm<br/>- Số lượng yêu cầu]

    ShowReadonly --> DisableEdit[Không cho phép sửa:<br/>- Thông tin KH<br/>- Mặt hàng<br/>- Số lượng yêu cầu]

    DisableEdit --> WarehousePick[Kho lấy hàng theo yêu cầu]

    WarehousePick --> UpdateActual[Kho cập nhật thông tin thực xuất]

    UpdateActual --> EnterSerial[Nhập Serial number]
    EnterSerial --> EnterBatch[Nhập Batch number]
    EnterBatch --> EnterActualQty[Nhập số lượng thực tế]
    EnterActualQty --> SelectWarehouse[Chọn kho xuất]

    SelectWarehouse --> ValidateData{Validate dữ liệu}

    ValidateData -->|Lỗi| ShowError[Hiển thị lỗi]
    ShowError --> UpdateActual

    ValidateData -->|OK| Confirm[Kho xác nhận đã xuất hàng]

    Confirm --> CreateStockEntry[Tạo Stock Entry]
    CreateStockEntry --> UpdateStock[(Trừ tồn kho)]

    UpdateStock --> UpdateDOStatus[Cập nhật Status: Delivered]
    UpdateDOStatus --> NotifyAccounts[Gửi thông báo cho Kế toán]

    NotifyAccounts --> End([Hoàn thành xuất hàng])

    style HidePrice fill:#fee2e2,stroke:#ef4444,stroke-width:2px
    style DisableEdit fill:#fef3c7,stroke:#f59e0b,stroke-width:2px
    style Confirm fill:#a7fab9,stroke:#22c55e,stroke-width:2px
```

### 3.4. Activity: Xuất hóa đơn với validate giá

```mermaid
flowchart TD
    Start([Kho đã xuất hàng]) --> AccountsView[Kế toán xem lệnh xuất hoàn thành]

    AccountsView --> CreateInvoice[Tạo hóa đơn từ lệnh xuất]

    CreateInvoice --> InheritData[Kế thừa dữ liệu:<br/>- Khách hàng<br/>- Sản phẩm<br/>- Số lượng THỰC XUẤT<br/>- Serial, Batch]

    InheritData --> GetInvoiceDate[Lấy ngày hóa đơn]

    GetInvoiceDate --> AutoLoadPrice[Tự động lấy bảng giá theo ngày HĐ]
    AutoLoadPrice --> AutoLoadDiscount[Tự động lấy chính sách CK theo ngày HĐ]

    AutoLoadDiscount --> GetDOPrice[Lấy giá từ lệnh xuất]
    GetDOPrice --> GetInvoicePrice[Lấy giá từ HĐ hiện tại]

    GetInvoicePrice --> ComparePrice{Giá lệnh xuất<br/>= Giá HĐ?}

    ComparePrice -->|Khác| ShowWarning[⚠️ Cảnh báo:<br/>Giá bán trên lệnh xuất<br/>khác giá bán trên HĐ]
    ComparePrice -->|Khớp| FillInvoice

    ShowWarning --> DisplayPriceDiff[Hiển thị:<br/>- Giá lệnh xuất<br/>- Giá HĐ hiện tại<br/>- Chênh lệch]

    DisplayPriceDiff --> AskConfirm{Kế toán xác nhận?}

    AskConfirm -->|Xác nhận| EnterReason[Nhập lý do chênh lệch giá]
    AskConfirm -->|Không| ReviewPrice[Xem lại giá]
    ReviewPrice --> ManualAdjust[Điều chỉnh giá thủ công]
    ManualAdjust --> FillInvoice

    EnterReason --> LogPriceDiff[Ghi log sự khác biệt giá]
    LogPriceDiff --> FillInvoice

    FillInvoice[Điền thông tin HĐ]
    FillInvoice --> EnterPaymentTerms[Nhập điều khoản thanh toán]
    EnterPaymentTerms --> EnterDueDate[Nhập hạn thanh toán]

    EnterDueDate --> Calculate[Tính toán:<br/>- Tổng tiền hàng<br/>- Tổng tiền CK<br/>- Tổng tiền thuế<br/>- Tổng tiền]

    Calculate --> ReviewInvoice[Xem lại hóa đơn]
    ReviewInvoice --> SubmitInvoice[Submit hóa đơn]

    SubmitInvoice --> SaveInvoice[(Lưu hóa đơn)]
    SaveInvoice --> UpdateAR[(Cập nhật công nợ KH)]

    UpdateAR --> EInvoiceOption{Xuất HĐ điện tử?}

    EInvoiceOption -->|Có| SendEInvoice[Phát hành HĐ điện tử]
    EInvoiceOption -->|Không| PrintInvoice[In hóa đơn giấy]

    SendEInvoice --> End1([Hoàn thành])
    PrintInvoice --> End1

    style ShowWarning fill:#fef3c7,stroke:#f59e0b,stroke-width:2px
    style LogPriceDiff fill:#fee2e2,stroke:#ef4444,stroke-width:2px
    style SaveInvoice fill:#a7fab9,stroke:#22c55e,stroke-width:2px
```

### 3.5. Activity: Xử lý trả hàng với validate Serial

```mermaid
flowchart TD
    Start([Khách hàng yêu cầu trả hàng]) --> CheckPolicy{Trong thời hạn?}

    CheckPolicy -->|Không| RejectReturn[❌ Từ chối trả hàng]
    CheckPolicy -->|Có| CreateReturn[NV KD tạo lệnh nhập hàng trả lại]

    RejectReturn --> End1([Kết thúc])

    CreateReturn --> SelectInvoice[Chọn hóa đơn bán hàng]
    SelectInvoice --> InheritData[Kế thừa dữ liệu từ HĐ]

    InheritData --> SelectItems[Chọn sản phẩm cần trả]
    SelectItems --> EnterQty[Nhập số lượng trả]
    EnterQty --> EnterSerial[Nhập Serial/Batch cần trả]

    EnterSerial --> SelectWarehouse[Chọn kho nhập]
    SelectWarehouse --> EnterReason[Nhập lý do trả hàng]

    EnterReason --> SubmitReturn[Submit lệnh nhập]
    SubmitReturn --> SendToWarehouse[Gửi lệnh nhập cho Kho]

    SendToWarehouse --> WarehouseReceive[Kho nhận hàng trả lại]
    WarehouseReceive --> InspectGoods[Kho kiểm tra hàng]

    InspectGoods --> GoodsStatus{Hàng hợp lệ?}
    GoodsStatus -->|Không| RejectGoods[Từ chối nhận hàng]
    GoodsStatus -->|Có| UpdateActual[Kho cập nhật thông tin thực nhập]

    RejectGoods --> NotifyReject[Thông báo NV KD]
    NotifyReject --> End2([Kết thúc - Không nhận])

    UpdateActual --> EnterActualSerial[Nhập Serial/Batch thực nhập]
    EnterActualSerial --> EnterActualQty[Nhập số lượng thực tế]
    EnterActualQty --> ConfirmReceive[Kho xác nhận đã nhập]

    ConfirmReceive --> CreatePR[Tạo Purchase Receipt]
    CreatePR --> UpdateStockPlus[(Cập nhật tồn kho +)]
    UpdateStockPlus --> NotifyAccounts[Thông báo Kế toán]

    NotifyAccounts --> AccountsProcess[Kế toán xử lý hàng bán trả lại]

    AccountsProcess --> InheritReturn[Kế thừa từ lệnh nhập]
    InheritReturn --> GetInvoice[Lấy hóa đơn bán ban đầu]

    GetInvoice --> ValidateSerial{Kiểm tra Serial<br/>có trong HĐ?}

    ValidateSerial -->|Không| ShowSerialWarning[⚠️ Cảnh báo:<br/>Serial không tồn tại<br/>trong HĐ bán hàng]
    ValidateSerial -->|Có| CreateCreditNote

    ShowSerialWarning --> DisplaySerialInfo[Hiển thị:<br/>- Serial nhập<br/>- Serial trong HĐ<br/>- Danh sách Serial hợp lệ]

    DisplaySerialInfo --> AskAccountsConfirm{Kế toán xác nhận?}

    AskAccountsConfirm -->|Xác nhận| EnterExceptionReason[Nhập lý do ngoại lệ]
    AskAccountsConfirm -->|Không| RejectProcessing[Từ chối xử lý]

    RejectProcessing --> End3([Kết thúc - Không xử lý])

    EnterExceptionReason --> LogSerialException[Ghi log ngoại lệ Serial]
    LogSerialException --> CreateCreditNote

    CreateCreditNote[Tạo phiếu hàng bán trả lại]
    CreateCreditNote --> SaveReturn[(Lưu phiếu trả hàng)]

    SaveReturn --> UpdateARMinus[(Cập nhật công nợ KH -)]

    UpdateARMinus --> RefundOption{Hoàn tiền<br/>hay ghi giảm trừ?}

    RefundOption -->|Hoàn tiền| CreatePaymentVoucher[Tạo phiếu chi tiền]
    RefundOption -->|Ghi giảm trừ| UpdateLedger[Cập nhật sổ cái]

    CreatePaymentVoucher --> ProcessRefund[Xử lý hoàn tiền]
    ProcessRefund --> NotifyCustomer1[Thông báo KH nhận tiền]

    UpdateLedger --> NotifyCustomer2[Thông báo KH ghi giảm trừ]

    NotifyCustomer1 --> End4([Hoàn thành])
    NotifyCustomer2 --> End4

    style ShowSerialWarning fill:#fef3c7,stroke:#f59e0b,stroke-width:2px
    style LogSerialException fill:#fee2e2,stroke:#ef4444,stroke-width:2px
    style SaveReturn fill:#a7fab9,stroke:#22c55e,stroke-width:2px
```

### 3.6. Activity: Lập hóa đơn bán lẻ (POS Flow)

```mermaid
flowchart TD
    Start([Khách hàng đến cửa hàng]) --> OpenPOS[NV mở POS]

    OpenPOS --> CustomerType{Loại khách hàng?}

    CustomerType -->|Có SĐT| EnterPhone[Nhập SĐT]
    CustomerType -->|Vãng lai| ScanItem

    EnterPhone --> SearchCustomer[Tìm kiếm khách hàng]
    SearchCustomer --> CustomerFound{Tìm thấy?}

    CustomerFound -->|Có| LoadCustomerData[Load thông tin:<br/>- Tên<br/>- Địa chỉ<br/>- Doanh số lũy kế]
    CustomerFound -->|Không| CreateNewCustomer[Tạo KH mới]

    LoadCustomerData --> ScanItem
    CreateNewCustomer --> ScanItem

    ScanItem[Quét mã sản phẩm hoặc chọn thủ công]

    ScanItem --> GetRetailPrice[Lấy giá bán lẻ]
    GetRetailPrice --> GetRetailDiscount[Lấy chiết khấu theo chính sách]

    GetRetailDiscount --> SpecialDiscount{Áp dụng CK đặc biệt?}

    SpecialDiscount -->|Có| EnterSpecialPercent[Nhập % CK đặc biệt]
    SpecialDiscount -->|Không| EnterQty

    EnterSpecialPercent --> CalculateSpecial[Tính tiền CK đặc biệt:<br/>tiền hàng - CK chính sách × % CK đặc biệt]
    CalculateSpecial --> EnterQty

    EnterQty[Nhập số lượng]
    EnterQty --> CheckStock{Kiểm tra tồn kho}

    CheckStock -->|Đủ hàng| AddToCart[Thêm vào giỏ hàng]
    CheckStock -->|Hết hàng| OutOfStock[⚠️ Hết hàng]

    OutOfStock --> ScanItem

    AddToCart --> UpdateCart[Cập nhật giỏ hàng]
    UpdateCart --> MoreItem{Thêm sản phẩm?}

    MoreItem -->|Có| ScanItem
    MoreItem -->|Không| SelectTax[Chọn loại thuế, thuế suất]

    SelectTax --> CalculateTotal[Tính tổng:<br/>- Tiền hàng<br/>- Tiền CK<br/>- Tiền thuế<br/>- Tổng tiền]

    CalculateTotal --> DisplayTotal[Hiển thị tổng tiền]
    DisplayTotal --> SelectPayment{Phương thức thanh toán?}

    SelectPayment -->|Tiền mặt| EnterCash[Nhập tiền khách đưa]
    SelectPayment -->|Thẻ| ProcessCard[Quẹt thẻ]
    SelectPayment -->|Chuyển khoản| ProcessTransfer[Xử lý chuyển khoản]
    SelectPayment -->|Công nợ| ProcessCredit[Ghi công nợ]

    EnterCash --> CalculateChange[Tính tiền thừa:<br/>Trả lại = Tiền đưa - Tổng tiền]
    CalculateChange --> ProcessPayment
    ProcessCard --> ProcessPayment
    ProcessTransfer --> ProcessPayment
    ProcessCredit --> ProcessPayment

    ProcessPayment[Xử lý thanh toán]
    ProcessPayment --> PaymentSuccess{Thanh toán thành công?}

    PaymentSuccess -->|Không| ShowPaymentError[Hiển thị lỗi thanh toán]
    ShowPaymentError --> SelectPayment

    PaymentSuccess -->|Có| EnterSerial[Nhập Serial/Batch cho từng sản phẩm]

    EnterSerial --> SelectEInvoice{Xuất HĐ điện tử?}

    SelectEInvoice -->|Không lấy| SubmitInvoice1[Submit HĐ]
    SelectEInvoice -->|Phát hành sau| SubmitInvoice2[Submit + Queue]
    SelectEInvoice -->|Phát hành ngay| SubmitInvoice3[Submit + Phát hành]

    SubmitInvoice1 --> SaveInvoice[(Lưu hóa đơn)]
    SubmitInvoice2 --> SaveInvoice
    SubmitInvoice3 --> SaveInvoice

    SaveInvoice --> UpdateStock[(Trừ tồn kho)]
    UpdateStock --> UpdateCumulative[(Cập nhật doanh số lũy kế)]

    UpdateCumulative --> UpdatePayment{Loại thanh toán?}

    UpdatePayment -->|Tiền mặt/Thẻ/TK| PrintInvoice[In hóa đơn]
    UpdatePayment -->|Công nợ| UpdateAR[(Cập nhật công nợ)]

    UpdateAR --> PrintInvoice

    PrintInvoice --> GiveChange{Có tiền thừa?}
    GiveChange -->|Có| ReturnChange[Trả tiền thừa cho KH]
    GiveChange -->|Không| GiveGoods

    ReturnChange --> GiveGoods[Giao hàng cho KH]
    GiveGoods --> End([Hoàn thành])

    style ScanItem fill:#dbeafe,stroke:#3b82f6,stroke-width:2px
    style CalculateSpecial fill:#fef3c7,stroke:#f59e0b,stroke-width:2px
    style SaveInvoice fill:#a7fab9,stroke:#22c55e,stroke-width:2px
```

---

## 4. Tổng kết Diagrams

### 4.1. Thống kê

| Loại Diagram | Số lượng | Mục đích |
|--------------|----------|----------|
| **Sequence Diagrams** | 7 | Mô tả tương tác giữa các actors và systems |
| **Activity Diagrams** | 6 | Mô tả luồng xử lý chi tiết với logic |
| **Tổng cộng** | 13 | 100% coverage các use cases |

### 4.2. Phân bố theo quy trình

| Quy trình | Sequence Diagrams | Activity Diagrams |
|-----------|-------------------|-------------------|
| **Bán buôn** | 6 | 5 |
| **Bán lẻ** | 1 | 1 |

### 4.3. Phân bố theo bước

| Bước | Diagrams | Loại |
|------|----------|------|
| Bước 1-4: Tạo đơn hàng | 2 | Sequence + Activity |
| Bước 5-6: Kiểm tra tồn kho và tạo lệnh xuất | 2 | Sequence + Activity |
| Bước 7-8: Kiểm tra công nợ | 2 | Sequence + Activity |
| Bước 6,9: Xuất hàng và xuất hóa đơn | 2 | Sequence + Activity |
| Bước 10-11: Xử lý trả hàng | 2 | Sequence + Activity |
| Bước 12: Tính thưởng doanh số | 1 | Sequence |
| Bán lẻ: Lập hóa đơn | 2 | Sequence + Activity |

---

## 5. Key Features trong Diagrams

### 5.1. Phân quyền (Access Control)

**Được thể hiện trong:**
- Sequence: Xuất hàng và xuất hóa đơn (Bước 6-9)
- Activity: Xuất hàng với phân quyền

**Điểm nổi bật:**
- Kho không thấy giá, thành tiền
- Kho không được sửa thông tin khách hàng, số lượng

### 5.2. Kiểm tra công nợ tự động (Credit Check)

**Được thể hiện trong:**
- Sequence: Kiểm tra công nợ (Bước 7-8)
- Activity: Kiểm tra công nợ và duyệt ngoại lệ

**Điểm nổi bật:**
- 2 điều kiện: Không có HĐ quá hạn + Công nợ ≤ Hạn mức
- Xử lý ngoại lệ: Kế toán trưởng duyệt

### 5.3. Validate giá và Serial (Data Validation)

**Được thể hiện trong:**
- Sequence: Xuất hóa đơn (Bước 9)
- Sequence: Xử lý trả hàng (Bước 10-11)
- Activity: Xuất hóa đơn với validate giá
- Activity: Xử lý trả hàng với validate Serial

**Điểm nổi bật:**
- Cảnh báo khi giá lệnh xuất ≠ giá HĐ
- Cảnh báo khi Serial trả hàng không tồn tại trong HĐ bán

### 5.4. Kế thừa dữ liệu (Data Inheritance)

**Được thể hiện trong:**
- Tất cả sequence diagrams

**Luồng kế thừa:**
1. Đơn hàng → Lệnh xuất hàng
2. Lệnh xuất hàng → Hóa đơn bán buôn
3. Hóa đơn bán hàng → Lệnh nhập hàng trả lại
4. Lệnh nhập hàng trả lại → Phiếu hàng bán trả lại

### 5.5. Chiết khấu đặc biệt (Retail Discount)

**Được thể hiện trong:**
- Sequence: Lập hóa đơn bán lẻ (POS)
- Activity: Lập hóa đơn bán lẻ

**Công thức:**
```
Tiền chiết khấu đặc biệt = (tiền hàng trước CK - tiền CK theo chính sách) × % CK đặc biệt
```

---

**Nguồn:** ERP_SPECIFICATION.md Section 2 (lines 46-298)
**Coverage:** 18/18 sections (100%)
**Tổng số diagrams:** 13 (7 Sequence + 6 Activity)
