# Module Sales Order - Đặc tả Workflow & ERD

> **Nguồn:** `/docs/feature/ERP_SPECIFICATION.md` Section 2 - Quản lý Bán hàng
> **Lưu ý:** Đây là đặc tả YÊU CẦU, code phải làm theo đặc tả này

---

## 1. Định nghĩa

> Quản lý toàn bộ quy trình bán hàng từ kế hoạch, bảng giá, đơn hàng, xuất kho, hóa đơn đến thu tiền và xử lý trả hàng

**Phạm vi:**
- Bán buôn (Wholesale) - 12 bước
- Bán lẻ (Retail) - 3 bước
- Tích hợp kiểm tra công nợ, hạn mức, tồn kho

---

## 2. ERD - Entity Relationship Diagram

### 2.1. Sales Order Core ERD

```mermaid
erDiagram
    SALES_ORDER ||--o{ SALES_ORDER_ITEM : contains
    SALES_ORDER ||--o| DELIVERY_NOTE : generates
    SALES_ORDER ||--o| SALES_INVOICE : generates
    SALES_ORDER }o--|| CUSTOMER : "ordered by"
    SALES_ORDER }o--|| PRICE_LIST : uses
    SALES_ORDER }o--|| DISCOUNT_POLICY : applies
    SALES_ORDER }o--|| CURRENCY : "in currency"
    SALES_ORDER }o--|| SALES_USER : "created by"

    SALES_ORDER {
        string name PK "SO-YYYYMMDD-XXXX"
        date transaction_date
        string customer FK
        string price_list FK
        string discount_policy FK
        string currency
        decimal grand_total
        date delivery_date
        string status "draft/approved/delivered/invoiced/paid/completed"
        string workflow_state
        int docstatus "0=Draft, 1=Submitted, 2=Cancelled"
    }

    SALES_ORDER_ITEM {
        string name PK
        string parent FK "Sales Order"
        string item_code FK
        string item_name
        string uom
        decimal qty
        decimal rate_before_discount
        decimal amount_before_discount
        string price_list FK
        string discount_policy FK
        decimal discount_percentage
        decimal discount_amount
        decimal amount_after_discount
        date expected_delivery_date
    }

    DELIVERY_NOTE ||--o{ DELIVERY_NOTE_ITEM : contains
    DELIVERY_NOTE }o--|| WAREHOUSE : "from warehouse"
    DELIVERY_NOTE }o--|| SALES_USER : "created by"
    DELIVERY_NOTE }o--|| STOCK_USER : "confirmed by"

    DELIVERY_NOTE {
        string name PK "DN-YYYYMMDD-XXXX"
        date posting_date
        string sales_order FK
        string customer FK
        string warehouse FK
        string created_by FK
        string confirmed_by FK
        string status "draft/credit_check/approved/delivered"
    }

    DELIVERY_NOTE_ITEM {
        string name PK
        string parent FK "Delivery Note"
        string item_code FK
        string item_name
        string uom
        decimal requested_qty
        decimal actual_qty
        string warehouse FK
        string batch_no
        string serial_no
        decimal rate
        decimal amount
    }

    SALES_INVOICE ||--o{ SALES_INVOICE_ITEM : contains
    SALES_INVOICE ||--o{ SERIAL_BATCH_BUNDLE : tracks
    SALES_INVOICE }o--|| ACCOUNTS_USER : "created by"

    SALES_INVOICE {
        string name PK "SI-YYYYMMDD-XXXX"
        date posting_date
        string sales_order FK
        string delivery_note FK
        string customer FK
        string payment_terms
        date due_date
        decimal total
        decimal discount_amount
        decimal tax_amount
        decimal grand_total
        decimal outstanding_amount
        string status "unpaid/paid/overdue"
    }

    SALES_INVOICE_ITEM {
        string name PK
        string parent FK "Sales Invoice"
        string item_code FK
        string sales_order FK
        string delivery_note FK
        string warehouse FK
        decimal qty
        string price_list FK
        decimal rate_before_discount
        decimal amount_before_discount
        string discount_policy FK
        decimal discount_percentage
        decimal discount_amount
        decimal amount_after_discount
    }

    SERIAL_BATCH_BUNDLE {
        string name PK
        string parent FK
        string item_code FK
        string batch_no
        string serial_no
        decimal qty
        string warehouse FK
    }

    CUSTOMER ||--o{ CREDIT_LIMIT : has
    CUSTOMER ||--o{ ANNUAL_SALES_TARGET : has

    CUSTOMER {
        string name PK
        string customer_name
        string customer_type "Company/Individual"
        string tax_id
        string address
        string phone
        string email
        string payment_terms
        string default_currency
    }

    CREDIT_LIMIT {
        string name PK
        string customer FK
        date valid_from
        decimal credit_limit_amount
        string account
    }

    ANNUAL_SALES_TARGET {
        string name PK
        string customer FK
        date fiscal_year
        decimal total_target
        string attachment
    }

    PRICE_LIST ||--o{ PRICE_LIST_ITEM : contains

    PRICE_LIST {
        string name PK
        date valid_from
        string created_by
        string description
        string attachment
    }

    PRICE_LIST_ITEM {
        string name PK
        string parent FK "Price List"
        string item_code FK
        string item_name
        decimal price
        string notes
    }

    DISCOUNT_POLICY ||--o{ DISCOUNT_POLICY_ITEM : contains
    DISCOUNT_POLICY }o--|| CUSTOMER : "for customer"

    DISCOUNT_POLICY {
        string name PK
        date valid_from
        string customer FK
        string description
        string attachment
    }

    DISCOUNT_POLICY_ITEM {
        string name PK
        string parent FK "Discount Policy"
        string item_code FK
        string item_name
        decimal discount_percentage
    }

    ITEM ||--o{ ITEM_UOM_CONVERSION : has

    ITEM {
        string name PK
        string item_name
        string stock_uom
        string macro
        string location
        string product_group
        string color
        string category
        string sales_category
        string product_type
        string statis_factor
        string item_group_1
        string item_group_2
        string item_group_3
        string item_group_4
        string item_group_5
        string item_group_6
        int has_batch_no "Track by batch"
        int has_serial_no "Track by serial"
    }

    ITEM_UOM_CONVERSION {
        string name PK
        string parent FK "Item"
        string uom
        decimal conversion_factor
    }
```

### 2.2. Return Process ERD

```mermaid
erDiagram
    SALES_INVOICE ||--o| RETURN_REQUEST : "triggers return"
    RETURN_REQUEST ||--o{ RETURN_REQUEST_ITEM : contains
    RETURN_REQUEST ||--o| PURCHASE_RECEIPT : "generates receipt"
    PURCHASE_RECEIPT ||--o| SALES_RETURN : "processed as"

    RETURN_REQUEST {
        string name PK "RR-YYYYMMDD-XXXX"
        date request_date
        string sales_invoice FK
        string customer FK
        string warehouse FK
        string requested_by FK
        string reason
        string status "draft/approved/received"
    }

    RETURN_REQUEST_ITEM {
        string name PK
        string parent FK "Return Request"
        string item_code FK
        string item_name
        string uom
        decimal qty
        decimal rate
        decimal amount
        string batch_no
        string serial_no
        string warehouse FK
    }

    PURCHASE_RECEIPT {
        string name PK "PR-YYYYMMDD-XXXX"
        date posting_date
        string return_request FK
        string customer FK "supplier in return context"
        string warehouse FK
    }

    SALES_RETURN {
        string name PK "SR-YYYYMMDD-XXXX"
        date posting_date
        string return_request FK
        string sales_invoice FK
        string customer FK
        string reason
        decimal return_amount
        string status "draft/completed"
    }
```

### 2.3. Retail Sales ERD

```mermaid
erDiagram
    RETAIL_PRICE_LIST ||--o{ RETAIL_PRICE_ITEM : contains
    RETAIL_DISCOUNT_POLICY ||--o{ RETAIL_DISCOUNT_ITEM : contains

    RETAIL_INVOICE ||--o{ RETAIL_INVOICE_ITEM : contains
    RETAIL_INVOICE ||--o{ SERIAL_BATCH_BUNDLE : tracks
    RETAIL_INVOICE }o--|| CUSTOMER : "sold to"
    RETAIL_INVOICE }o--|| WAREHOUSE : "from warehouse"
    RETAIL_INVOICE }o--|| RETAIL_USER : "sold by"
    RETAIL_INVOICE }o--|| RETAIL_PRICE_LIST : uses
    RETAIL_INVOICE }o--|| RETAIL_DISCOUNT_POLICY : applies

    RETAIL_INVOICE {
        string name PK "RI-YYYYMMDD-XXXX"
        date posting_date
        string customer_phone
        decimal cumulative_sales "Doanh số lũy kế"
        string sales_person FK
        string warehouse FK
        string customer FK
        string address
        string description
        decimal total_amount
        decimal discount_amount
        decimal grand_total
        decimal paid_amount
        decimal change_amount
        string tax_type
        decimal tax_rate
        decimal tax_amount
        string einvoice_option "no_invoice/later/immediate"
        string payment_method "cash/card/transfer"
    }

    RETAIL_INVOICE_ITEM {
        string name PK
        string parent FK "Retail Invoice"
        string item_code FK
        string item_name
        string uom
        decimal qty
        string price_list FK
        string discount_policy FK
        decimal rate
        decimal amount
        decimal policy_discount_amount
        decimal special_discount_percentage
        decimal special_discount_amount
        string batch_no
        string serial_no
    }

    RETAIL_PRICE_LIST {
        string name PK
        date valid_from
        string description
    }

    RETAIL_PRICE_ITEM {
        string name PK
        string parent FK "Retail Price List"
        string item_code FK
        string item_name
        decimal price
    }

    RETAIL_DISCOUNT_POLICY {
        string name PK
        date valid_from
        string description
        string attachment
    }

    RETAIL_DISCOUNT_ITEM {
        string name PK
        string parent FK "Retail Discount Policy"
        string item_code FK
        string item_name
        decimal discount_percentage
    }
```

---

## 3. Workflow - Quy trình Bán buôn (12 bước)

### 3.1. Sơ đồ tổng quan - End-to-End Workflow

```mermaid
flowchart TD
    Start([Bắt đầu năm]) --> Step1[Bước 1: Kế hoạch bán hàng theo năm]

    Step1 --> Step2[Bước 2: Bảng giá bán niêm yết]
    Step2 --> Step3[Bước 3: Chính sách chiết khấu bán buôn]

    Step3 --> Step4[Bước 4: Đơn đặt hàng bán]

    Step4 --> Step5{Bước 5: Kiểm tra tồn kho}
    Step5 -->|Đủ hàng| Step6[Bước 6: Lệnh xuất hàng]
    Step5 -->|Thiếu hàng| NotifyCustomer[Thông báo KH]
    NotifyCustomer --> Step4

    Step6 --> Step7{Bước 7: Kiểm tra hạn mức công nợ}
    Step7 -->|OK| Step8{Bước 8: Kiểm tra công nợ quá hạn}
    Step7 -->|Hết hạn mức| Exception1[Lập lại đơn hàng]
    Exception1 --> Step4

    Step8 -->|Hợp lệ| DeliverGoods[Kho xuất hàng]
    Step8 -->|Vi phạm| ExceptionApproval{Kế toán trưởng duyệt?}

    ExceptionApproval -->|Duyệt| DeliverGoods
    ExceptionApproval -->|Từ chối| NotifyPayment[Thông báo KH thanh toán công nợ]
    NotifyPayment --> Step6

    DeliverGoods --> Step9[Bước 9: Hóa đơn bán buôn]

    Step9 --> Payment{Khách thanh toán?}
    Payment -->|Đã thanh toán| CheckReturn{Có trả hàng?}
    Payment -->|Chưa thanh toán| WaitPayment[Chờ thanh toán]
    WaitPayment --> Payment

    CheckReturn -->|Không trả| Step12[Bước 12: Tính thưởng đạt KH doanh số]
    CheckReturn -->|Có trả| Step10[Bước 10: Lệnh nhập hàng trả lại]

    Step10 --> Step11[Bước 11: Hàng bán bị trả lại]
    Step11 --> Step12

    Step12 --> End([Kết thúc])

    style Step4 fill:#ffd19a,stroke:#f59e0b,stroke-width:3px
    style Step8 fill:#fee2e2,stroke:#ef4444,stroke-width:2px
    style ExceptionApproval fill:#fef3c7,stroke:#f59e0b,stroke-width:2px
```

### 3.2. Workflow Chi tiết - Bước 4: Tạo đơn hàng bán (CORE)

```mermaid
flowchart TD
    Start([NV Kinh doanh nhận yêu cầu từ KH]) --> SelectPriceList[Kiểm tra bảng giá hiện hành]

    SelectPriceList --> SelectDiscountPolicy[Kiểm tra chính sách chiết khấu]

    SelectDiscountPolicy --> CreateOrder[Tạo đơn đặt hàng bán]

    CreateOrder --> FillGeneral[Điền thông tin chung:<br/>- Khách hàng<br/>- Ngày giao hàng<br/>- Điều khoản thanh toán]

    FillGeneral --> AddItem[Thêm sản phẩm]

    AddItem --> SelectItem[Chọn mã hàng]
    SelectItem --> AutoPrice{Có bảng giá?}

    AutoPrice -->|Có| LoadPrice[Tự động load giá từ bảng giá]
    AutoPrice -->|Không| ManualPrice[Nhập giá thủ công]

    LoadPrice --> AutoDiscount{Có chính sách chiết khấu?}
    ManualPrice --> AutoDiscount

    AutoDiscount -->|Có| LoadDiscount[Tự động load % chiết khấu]
    AutoDiscount -->|Không| ManualDiscount[Nhập tay % chiết khấu]

    LoadDiscount --> Calculate[Tính toán:<br/>- Thành tiền trước CK<br/>- Tiền chiết khấu<br/>- Thành tiền sau CK]
    ManualDiscount --> Calculate

    Calculate --> MoreItem{Thêm sản phẩm?}
    MoreItem -->|Có| AddItem
    MoreItem -->|Không| Review[Xem lại tổng đơn hàng]

    Review --> Submit[Submit đơn hàng]
    Submit --> SaveOrder[(Lưu đơn hàng)]

    SaveOrder --> End([Chuyển sang Bước 5: Kiểm tra tồn kho])

    style CreateOrder fill:#dbeafe,stroke:#3b82f6,stroke-width:2px
    style SaveOrder fill:#a7fab9,stroke:#22c55e,stroke-width:2px
```

### 3.3. Workflow Chi tiết - Bước 6: Lệnh xuất hàng (Phân quyền)

```mermaid
flowchart TD
    Start([Bộ phận Kinh doanh]) --> CreateDO[Tạo lệnh xuất hàng từ đơn hàng]

    CreateDO --> InheritData[Kế thừa dữ liệu từ đơn hàng:<br/>- Khách hàng<br/>- Sản phẩm<br/>- Số lượng<br/>- Giá, chiết khấu]

    InheritData --> FillWarehouse[Chọn kho xuất]
    FillWarehouse --> DisplayPrice[Hiển thị: Giá, Thành tiền, CK]

    DisplayPrice --> CreditCheck{Kiểm tra công nợ tự động}

    CreditCheck -->|OK| SendToWarehouse[Gửi lệnh xuất cho Bộ phận Kho]
    CreditCheck -->|Vi phạm| ExceptionApproval[Chờ Kế toán trưởng duyệt]

    ExceptionApproval -->|Duyệt| SendToWarehouse
    ExceptionApproval -->|Từ chối| Notify[Thông báo KH thanh toán]
    Notify --> End1([Kết thúc - Không xuất])

    SendToWarehouse --> WarehouseView[Bộ phận Kho xem lệnh xuất]

    WarehouseView --> HidePrice{Phân quyền: Ẩn giá}
    HidePrice --> DisplayNoPrice[Chỉ hiển thị:<br/>- Khách hàng readonly<br/>- Sản phẩm readonly<br/>- Số lượng yêu cầu readonly<br/>- KHÔNG hiển thị giá, thành tiền]

    DisplayNoPrice --> PickItems[Kho lấy hàng theo yêu cầu]

    PickItems --> UpdateActual[Kho cập nhật thông tin thực xuất:<br/>- Số lượng thực tế<br/>- Serial number<br/>- Batch number<br/>- Kho xuất]

    UpdateActual --> ConfirmDelivery[Kho xác nhận đã xuất hàng]

    ConfirmDelivery --> UpdateStock[(Trừ tồn kho)]
    UpdateStock --> NotifyAccounts[Thông báo Kế toán]

    NotifyAccounts --> End2([Chuyển sang Bước 9: Xuất hóa đơn])

    style HidePrice fill:#fef3c7,stroke:#f59e0b,stroke-width:2px
    style DisplayNoPrice fill:#fee2e2,stroke:#ef4444,stroke-width:2px
    style ConfirmDelivery fill:#a7fab9,stroke:#22c55e,stroke-width:2px
```

### 3.4. Workflow Chi tiết - Bước 8: Kiểm tra công nợ quá hạn (Auto)

```mermaid
flowchart TD
    Start([Lệnh xuất hàng được tạo]) --> GetCustomer[Lấy thông tin khách hàng]

    GetCustomer --> GetCreditLimit[Lấy hạn mức công nợ]
    GetCreditLimit --> GetOutstanding[Lấy công nợ hiện tại]
    GetOutstanding --> GetPendingDO[Lấy tổng giá trị lệnh xuất chưa xuất]
    GetPendingDO --> GetCurrentDO[Lấy giá trị lệnh xuất hiện tại]
    GetCurrentDO --> GetOverdueInvoices[Lấy danh sách hóa đơn quá hạn]

    GetOverdueInvoices --> Check1{Có HĐ quá hạn?}

    Check1 -->|Có| Condition1[❌ Điều kiện 1: Vi phạm]
    Check1 -->|Không| Check2{Công nợ ≤ Hạn mức?}

    Check2 -->|Không| Condition2[❌ Điều kiện 2: Vi phạm]
    Check2 -->|Có| AllOK[✅ Cả 2 điều kiện OK]

    Condition1 --> ShowWarning[Hiển thị cảnh báo cho NV KD]
    Condition2 --> ShowWarning

    ShowWarning --> DisplayInfo[Hiển thị thông tin:<br/>- Số dư công nợ thực tế<br/>- Công nợ dự kiến<br/>- Danh sách HĐ quá hạn<br/>- Hạn mức công nợ]

    DisplayInfo --> SendApproval[Gửi yêu cầu duyệt ngoại lệ<br/>cho Kế toán trưởng]

    SendApproval --> WaitApproval{Kế toán trưởng duyệt?}

    WaitApproval -->|Duyệt| LogApproval[Ghi log lý do duyệt ngoại lệ]
    WaitApproval -->|Từ chối| LogReject[Ghi log lý do từ chối]

    LogApproval --> Approved[Status: Approved]
    LogReject --> Rejected[Status: Rejected]

    AllOK --> Approved

    Approved --> End1([Cho phép xuất hàng])
    Rejected --> End2([Không cho xuất - Thông báo KH])

    style Check1 fill:#fef3c7,stroke:#f59e0b,stroke-width:2px
    style Check2 fill:#fef3c7,stroke:#f59e0b,stroke-width:2px
    style ShowWarning fill:#fee2e2,stroke:#ef4444,stroke-width:2px
    style Approved fill:#a7fab9,stroke:#22c55e,stroke-width:2px
    style Rejected fill:#fca6a2,stroke:#dc2626,stroke-width:2px
```

### 3.5. Workflow Chi tiết - Bước 9: Xuất hóa đơn (Kế thừa + Validate)

```mermaid
flowchart TD
    Start([Kho đã xuất hàng]) --> AccountsView[Kế toán xem lệnh xuất đã hoàn thành]

    AccountsView --> CreateInvoice[Tạo hóa đơn bán buôn từ lệnh xuất]

    CreateInvoice --> InheritData[Kế thừa dữ liệu từ lệnh xuất:<br/>- Khách hàng<br/>- Sản phẩm<br/>- Số lượng THỰC XUẤT<br/>- Serial, Batch number]

    InheritData --> GetInvoiceDate[Lấy ngày hóa đơn hiện tại]

    GetInvoiceDate --> AutoLoadPrice[Tự động lấy bảng giá theo ngày HĐ]
    AutoLoadPrice --> AutoLoadDiscount[Tự động lấy chính sách chiết khấu theo ngày HĐ]

    AutoLoadDiscount --> CompareDO[So sánh giá trên lệnh xuất vs HĐ]

    CompareDO --> PriceMatch{Giá khớp?}

    PriceMatch -->|Khác nhau| ShowWarning[⚠️ Cảnh báo:<br/>Giá bán trên lệnh xuất khác giá trên HĐ]
    PriceMatch -->|Khớp| FillInvoice[Điền thông tin HĐ]

    ShowWarning --> AskConfirm{Kế toán xác nhận?}
    AskConfirm -->|Xác nhận| LogPriceDiff[Ghi log sự khác biệt giá]
    AskConfirm -->|Hủy| ReviewPrice[Xem lại giá]
    ReviewPrice --> AutoLoadPrice

    LogPriceDiff --> FillInvoice

    FillInvoice --> EnterPaymentTerms[Nhập điều khoản thanh toán, hạn thanh toán]

    EnterPaymentTerms --> Calculate[Tính toán:<br/>- Tổng tiền hàng<br/>- Tổng tiền chiết khấu<br/>- Tổng tiền thuế<br/>- Tổng tiền]

    Calculate --> ReviewInvoice[Xem lại hóa đơn]
    ReviewInvoice --> SubmitInvoice[Submit hóa đơn]

    SubmitInvoice --> SaveInvoice[(Lưu hóa đơn)]
    SaveInvoice --> UpdateAR[(Cập nhật công nợ KH)]

    UpdateAR --> PrintInvoice{In/Gửi HĐ điện tử?}
    PrintInvoice -->|Có| SendEInvoice[Phát hành HĐ điện tử]
    PrintInvoice -->|Không| End1([Kết thúc])
    SendEInvoice --> End1

    style ShowWarning fill:#fef3c7,stroke:#f59e0b,stroke-width:2px
    style LogPriceDiff fill:#fee2e2,stroke:#ef4444,stroke-width:2px
    style SaveInvoice fill:#a7fab9,stroke:#22c55e,stroke-width:2px
```

### 3.6. Workflow Chi tiết - Bước 10-11: Xử lý trả hàng

```mermaid
flowchart TD
    Start([Khách hàng yêu cầu trả hàng]) --> CheckPolicy{Trong thời hạn trả hàng?}

    CheckPolicy -->|Không| Reject[❌ Từ chối trả hàng]
    CheckPolicy -->|Có| CreateReturn[NV KD tạo lệnh nhập hàng trả lại]

    Reject --> End1([Kết thúc])

    CreateReturn --> InheritInvoice[Kế thừa từ hóa đơn bán hàng]

    InheritInvoice --> SelectItems[Chọn sản phẩm cần trả]
    SelectItems --> EnterQty[Nhập số lượng trả]
    EnterQty --> EnterSerial[Nhập Serial/Batch cần trả]

    EnterSerial --> FillWarehouse[Chọn kho nhập]
    FillWarehouse --> EnterReason[Nhập lý do trả hàng]

    EnterReason --> SubmitReturn[Submit lệnh nhập hàng trả lại]

    SubmitReturn --> SendToWarehouse[Gửi lệnh nhập cho Bộ phận Kho]

    SendToWarehouse --> WarehouseReceive[Kho nhận hàng trả lại]
    WarehouseReceive --> InspectGoods[Kho kiểm tra hàng]

    InspectGoods --> UpdateActual[Kho cập nhật thông tin thực nhập:<br/>- Mã hàng<br/>- Serial<br/>- Batch<br/>- Số lượng<br/>- Kho]

    UpdateActual --> ConfirmReceive[Kho xác nhận đã nhập]

    ConfirmReceive --> NotifyAccounts[Thông báo Kế toán]

    NotifyAccounts --> AccountsProcess[Kế toán xử lý hàng bán bị trả lại]

    AccountsProcess --> InheritReturn[Kế thừa từ lệnh nhập hàng trả lại]

    InheritReturn --> ValidateSerial{Kiểm tra Serial có trong HĐ ban đầu?}

    ValidateSerial -->|Không| ShowWarning[⚠️ Cảnh báo:<br/>Serial không tồn tại trong HĐ bán]
    ValidateSerial -->|Có| CreateCreditNote[Tạo phiếu hàng bán trả lại]

    ShowWarning --> AskConfirm{Kế toán xác nhận?}
    AskConfirm -->|Xác nhận| LogException[Ghi log ngoại lệ]
    AskConfirm -->|Hủy| End2([Kết thúc - Không xử lý])

    LogException --> CreateCreditNote

    CreateCreditNote --> SaveReturn[(Lưu phiếu trả hàng)]
    SaveReturn --> UpdateStock[(Cập nhật tồn kho +)]
    UpdateStock --> UpdateAR[(Cập nhật công nợ KH -)]

    UpdateAR --> RefundOrCredit{Hoàn tiền hay ghi giảm trừ?}

    RefundOrCredit -->|Hoàn tiền| CreatePayment[Tạo phiếu chi tiền]
    RefundOrCredit -->|Ghi giảm trừ| UpdateLedger[Cập nhật sổ cái]

    CreatePayment --> End3([Hoàn thành])
    UpdateLedger --> End3

    style ValidateSerial fill:#fef3c7,stroke:#f59e0b,stroke-width:2px
    style ShowWarning fill:#fee2e2,stroke:#ef4444,stroke-width:2px
    style SaveReturn fill:#a7fab9,stroke:#22c55e,stroke-width:2px
```

---

## 4. Workflow - Quy trình Bán lẻ (3 bước)

### 4.1. Sơ đồ tổng quan - Retail Workflow

```mermaid
flowchart TD
    Start([Khách hàng đến cửa hàng]) --> Step1[Bước 1: Bảng giá bán lẻ]
    Step1 --> Step2[Bước 2: Chính sách chiết khấu bán lẻ]

    Step2 --> Step3[Bước 3: Nhân viên lập hóa đơn bán lẻ]

    Step3 --> SelectItems[Chọn sản phẩm]
    SelectItems --> AutoPrice[Tự động load giá từ bảng giá bán lẻ]
    AutoPrice --> AutoDiscount[Tự động load chiết khấu theo chính sách]

    AutoDiscount --> SpecialDiscount{Áp dụng chiết khấu đặc biệt?}
    SpecialDiscount -->|Có| EnterSpecialDiscount[Nhập % chiết khấu đặc biệt]
    SpecialDiscount -->|Không| Calculate

    EnterSpecialDiscount --> Calculate[Tính toán:<br/>Tiền CK đặc biệt = <br/>tiền hàng trước CK - CK chính sách × % CK đặc biệt]

    Calculate --> EnterSerial[Nhập Serial/Batch]
    EnterSerial --> SelectPayment{Phương thức thanh toán?}

    SelectPayment -->|Tiền mặt| Cash[Nhập tiền khách đưa]
    SelectPayment -->|Thẻ| Card[Quẹt thẻ]
    SelectPayment -->|Chuyển khoản| Transfer[Chuyển khoản]
    SelectPayment -->|Công nợ| Credit[Ghi công nợ]

    Cash --> CalculateChange[Tính tiền thừa trả khách]
    Card --> PrintReceipt
    Transfer --> PrintReceipt
    Credit --> PrintReceipt
    CalculateChange --> PrintReceipt[In hóa đơn]

    PrintReceipt --> EInvoice{Xuất hóa đơn điện tử?}
    EInvoice -->|Không lấy| End1([Hoàn thành])
    EInvoice -->|Phát hành sau| QueueEInvoice[Đưa vào queue phát hành sau]
    EInvoice -->|Phát hành ngay| SendEInvoice[Phát hành HĐ điện tử ngay]

    QueueEInvoice --> End2([Hoàn thành])
    SendEInvoice --> End2

    style Step3 fill:#dbeafe,stroke:#3b82f6,stroke-width:2px
    style Calculate fill:#fef3c7,stroke:#f59e0b,stroke-width:2px
    style PrintReceipt fill:#a7fab9,stroke:#22c55e,stroke-width:2px
```

### 4.2. Workflow Chi tiết - Bước 3: Lập hóa đơn bán lẻ (POS)

```mermaid
flowchart TD
    Start([NV Cửa hàng mở POS]) --> CustomerPhone{Nhập SĐT khách hàng?}

    CustomerPhone -->|Có| SearchCustomer[Tìm khách hàng]
    CustomerPhone -->|Không| WalkIn[Khách vãng lai]

    SearchCustomer --> LoadCustomerData[Load thông tin:<br/>- Tên<br/>- Địa chỉ<br/>- Doanh số lũy kế]
    WalkIn --> AddItem
    LoadCustomerData --> AddItem

    AddItem[Quét mã sản phẩm hoặc chọn thủ công]

    AddItem --> GetPrice[Lấy giá từ bảng giá bán lẻ]
    GetPrice --> GetDiscount{Có chính sách chiết khấu?}

    GetDiscount -->|Có| ApplyPolicyDiscount[Áp dụng chiết khấu theo chính sách]
    GetDiscount -->|Không| EnterQty

    ApplyPolicyDiscount --> SpecialDiscount{Áp dụng chiết khấu đặc biệt?}
    SpecialDiscount -->|Có| EnterSpecialPercent[Nhập % chiết khấu đặc biệt]
    SpecialDiscount -->|Không| EnterQty

    EnterSpecialPercent --> CalculateSpecial[Tính tiền CK đặc biệt:<br/>tiền hàng - CK chính sách × % CK đặc biệt]
    CalculateSpecial --> EnterQty

    EnterQty[Nhập số lượng]
    EnterQty --> CheckStock{Kiểm tra tồn kho}
    CheckStock -->|Đủ hàng| AddToCart[Thêm vào giỏ hàng]
    CheckStock -->|Hết hàng| OutOfStock[⚠️ Hết hàng]
    OutOfStock --> End1([Kết thúc])

    AddToCart --> MoreItem{Thêm sản phẩm?}
    MoreItem -->|Có| AddItem
    MoreItem -->|Không| SelectTax[Chọn loại thuế, thuế suất]

    SelectTax --> CalculateTotal[Tính tổng:<br/>- Tiền hàng<br/>- Tiền chiết khấu<br/>- Tiền thuế<br/>- Tổng tiền]

    CalculateTotal --> SelectPaymentMethod[Chọn phương thức thanh toán]

    SelectPaymentMethod --> PaymentType{Loại thanh toán?}

    PaymentType -->|Tiền mặt| EnterPaidAmount[Nhập tiền khách đưa]
    PaymentType -->|Thẻ| CardPayment[Thông tin thẻ thanh toán]
    PaymentType -->|Chuyển khoản| BankTransfer[Thông tin chuyển khoản]
    PaymentType -->|Công nợ| CreditPayment[Ghi công nợ]

    EnterPaidAmount --> CalculateChange[Tính tiền thừa trả khách:<br/>Trả lại khách = Tiền đưa - Tổng tiền]
    CardPayment --> ProcessPayment
    BankTransfer --> ProcessPayment
    CreditPayment --> ProcessPayment
    CalculateChange --> ProcessPayment

    ProcessPayment[Xử lý thanh toán]

    ProcessPayment --> EnterSerial[Nhập Serial/Batch cho từng sản phẩm]

    EnterSerial --> SelectEInvoice[Chọn xuất hóa đơn điện tử]

    SelectEInvoice --> EInvoiceOption{Tùy chọn HĐ điện tử?}

    EInvoiceOption -->|Không lấy HĐ| Submit1[Submit hóa đơn]
    EInvoiceOption -->|Phát hành sau| Submit2[Submit + Queue]
    EInvoiceOption -->|Phát hành ngay| Submit3[Submit + Phát hành]

    Submit1 --> SaveInvoice[(Lưu hóa đơn)]
    Submit2 --> SaveInvoice
    Submit3 --> SaveInvoice

    SaveInvoice --> UpdateStock[(Trừ tồn kho)]
    UpdateStock --> UpdateSales[(Cập nhật doanh số lũy kế)]

    UpdateSales --> PrintInvoice[In hóa đơn]

    PrintInvoice --> End2([Hoàn thành - Giao hàng cho KH])

    style AddItem fill:#dbeafe,stroke:#3b82f6,stroke-width:2px
    style CalculateSpecial fill:#fef3c7,stroke:#f59e0b,stroke-width:2px
    style SaveInvoice fill:#a7fab9,stroke:#22c55e,stroke-width:2px
```

---

## 5. State Machine - Sales Order Status

```mermaid
stateDiagram-v2
    [*] --> draft: NV tạo đơn

    draft --> submitted: Submit đơn hàng
    draft --> cancelled: Hủy đơn

    submitted --> to_deliver: Đợi giao hàng

    to_deliver --> checking_stock: Kiểm tra tồn kho

    checking_stock --> stock_ok: Đủ hàng
    checking_stock --> stock_insufficient: Thiếu hàng

    stock_insufficient --> draft: Thông báo KH, lập lại đơn

    stock_ok --> delivery_note_created: Tạo lệnh xuất hàng

    delivery_note_created --> credit_check: Kiểm tra công nợ tự động

    credit_check --> credit_ok: Hợp lệ
    credit_check --> credit_violation: Vi phạm công nợ

    credit_violation --> exception_pending: Chờ Kế toán trưởng duyệt

    exception_pending --> credit_ok: Kế toán trưởng duyệt
    exception_pending --> to_deliver: Từ chối - Chờ KH thanh toán

    credit_ok --> to_deliver_and_bill: Kho xuất hàng

    to_deliver_and_bill --> to_bill: Hàng đã giao, chờ xuất HĐ

    to_bill --> completed: Xuất HĐ xong

    completed --> return_requested: Khách yêu cầu trả hàng

    return_requested --> return_processing: Xử lý trả hàng

    return_processing --> completed: Hoàn tất trả hàng

    completed --> [*]
    cancelled --> [*]

    note right of credit_check
        Điều kiện hợp lệ:
        1. Không có HĐ quá hạn
        2. Công nợ ≤ Hạn mức
    end note

    note right of exception_pending
        Xử lý ngoại lệ:
        Kế toán trưởng xác nhận
        cho phép xuất hàng
    end note

    note right of completed
        Terminal State
        Đơn hàng hoàn thành
    end note
```

---

## 6. Integration Points

### 6.1. Tích hợp Quản lý Kho

```mermaid
flowchart LR
    SalesOrder[Sales Order] -->|1. Kiểm tra tồn| StockLedger[Stock Ledger]
    SalesOrder -->|2. Tạo lệnh xuất| DeliveryNote[Delivery Note]
    DeliveryNote -->|3. Cập nhật thực xuất| StockEntry[Stock Entry]
    StockEntry -->|4. Trừ tồn kho| StockLedger
    StockLedger -->|5. Thông báo| SalesOrder
```

### 6.2. Tích hợp Quản lý Công nợ

```mermaid
flowchart LR
    SalesOrder[Sales Order] -->|1. Kiểm tra hạn mức| CreditLimit[Credit Limit]
    SalesOrder -->|2. Kiểm tra quá hạn| SalesInvoice[Sales Invoice - Overdue]
    CreditLimit -->|3. Hạn mức OK?| ValidationResult{Hợp lệ?}
    SalesInvoice -->|4. Có HĐ quá hạn?| ValidationResult
    ValidationResult -->|Vi phạm| ExceptionApproval[Exception Approval]
    ValidationResult -->|OK| DeliveryNote[Delivery Note]
    ExceptionApproval -->|Duyệt| DeliveryNote
```

### 6.3. Tích hợp Kế toán

```mermaid
flowchart LR
    DeliveryNote[Delivery Note] -->|1. Kế thừa dữ liệu| SalesInvoice[Sales Invoice]
    SalesInvoice -->|2. Cập nhật công nợ| AccountsReceivable[Accounts Receivable]
    AccountsReceivable -->|3. Tạo bút toán| GLEntry[General Ledger Entry]
    PaymentEntry[Payment Entry] -->|4. Ghi nhận thanh toán| AccountsReceivable
    AccountsReceivable -->|5. Đối trừ| SalesInvoice
```

---

## 7. Business Rules Summary

### 7.1. Quy tắc giá và chiết khấu

| Quy tắc | Mô tả |
|---------|-------|
| **Kế thừa giá** | Đơn hàng → Lệnh xuất → Hóa đơn |
| **Ưu tiên bảng giá** | Bảng giá > Giá thủ công |
| **Ưu tiên chiết khấu** | Chính sách CK > CK thủ công |
| **CK bán lẻ** | CK theo chính sách + CK đặc biệt |
| **Cảnh báo giá khác** | Giá lệnh xuất ≠ Giá HĐ → Cảnh báo |

### 7.2. Quy tắc công nợ

| Quy tắc | Mô tả |
|---------|-------|
| **Điều kiện xuất hàng** | Không có HĐ quá hạn + Công nợ ≤ Hạn mức |
| **Công nợ dự kiến** | Công nợ hiện tại + Lệnh xuất chưa xuất + Lệnh xuất hiện tại |
| **Xử lý ngoại lệ** | Kế toán trưởng phải duyệt thì mới xuất hàng |
| **HĐ quá hạn** | HĐ quá 30 ngày (hoặc theo kỳ hạn thanh toán) |

### 7.3. Quy tắc phân quyền

| Bộ phận | Quyền hạn | Giới hạn |
|---------|-----------|----------|
| **Kinh doanh** | Tạo đơn, tạo lệnh xuất, kiểm tra tồn kho | Không duyệt ngoại lệ |
| **Kho** | Xem lệnh xuất, cập nhật thực xuất | Không thấy giá, không sửa khách hàng/số lượng |
| **Kế toán** | Xuất HĐ, xử lý trả hàng | Không duyệt ngoại lệ |
| **Kế toán trưởng** | Duyệt ngoại lệ công nợ | Toàn quyền |
| **Cửa hàng** | Lập HĐ bán lẻ | Chỉ bán lẻ |

### 7.4. Quy tắc theo dõi lô, seri

| Quy tắc | Mô tả |
|---------|-------|
| **Bắt buộc nhập** | Trên tất cả màn hình nhập xuất |
| **Kiểm tra trả hàng** | Serial trả hàng phải tồn tại trong HĐ bán ban đầu |
| **Cảnh báo** | Nếu serial không tồn tại → Cảnh báo |

---

**Nguồn:** ERP_SPECIFICATION.md Section 2 (lines 46-298)
**Coverage:** 18/18 sections (100%)
**Tổng số diagrams:** 12 workflows + 3 ERDs + 1 state machine = 16 diagrams
