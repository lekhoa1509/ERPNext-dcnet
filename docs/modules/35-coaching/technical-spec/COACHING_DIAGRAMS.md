# Coaching Module - Tổng hợp Diagrams

> **Mục đích:** Tổng hợp tất cả Mermaid diagrams để dễ review
>
> **Preview online:** Paste vào https://mermaid.live hoặc VS Code extension "Mermaid Preview"

---

## 1. Workflow tổng quan

```mermaid
flowchart TD
    A[Học viên đăng ký] --> B{Nguồn}
    B -->|Website| C[API đẩy vào CRM]
    B -->|Tại cửa hàng| D[NV tạo trực tiếp]
    B -->|Điện thoại| D

    C --> E[Tạo Đơn Coaching]
    D --> E

    E --> F[Bài test đầu vào]
    F --> G[Đánh giá trình độ]
    G --> H[Tư vấn gói phù hợp]

    H --> I{Học viên đăng ký?}
    I -->|Không| J[Lưu Lead, follow-up]
    I -->|Có| K[Đăng ký khoá học]

    K --> L["Tạo đơn hàng (Order)<br/>Thanh toán"]
    L --> M[Xếp lịch học]
    M --> N[Bắt đầu khóa học]

    N --> O{Mỗi buổi học}
    O --> P[Điểm danh]
    P --> Q[Ghi nhận tiến trình]
    Q --> O

    O -->|Hết buổi| R[Hoàn thành khóa]
    R --> S[Đánh giá kết quả]
    S --> T{Đăng ký tiếp?}
    T -->|Có| K
    T -->|Không| U[Kết thúc]

    U --> V["Follow-up:<br/>Bán SP/Tư vấn khóa mới"]
```

---

## 2. State Machine - Trạng thái đơn Coaching

```mermaid
stateDiagram-v2
    [*] --> Mới: Đăng ký
    Mới --> Đã_test: Làm test đầu vào
    Mới --> Hủy: Khách hủy

    Đã_test --> Đã_tư_vấn: Tư vấn gói
    Đã_test --> Hủy: Không phù hợp

    Đã_tư_vấn --> Đã_thanh_toán: Đăng ký khoá học & Tạo đơn hàng
    Đã_tư_vấn --> Hủy: Khách hủy

    Đã_thanh_toán --> Đang_học: Bắt đầu buổi đầu
    Đang_học --> Đang_học: Các buổi tiếp theo

    Đang_học --> Tạm_dừng: Học viên xin nghỉ
    Tạm_dừng --> Đang_học: Học tiếp

    Đang_học --> Hoàn_thành: Hết số buổi

    Hoàn_thành --> [*]
    Hủy --> [*]
    Tạm_dừng --> Hủy: Quá hạn không học
```

---

## 3. ERD - Entity Relationship Diagram

```mermaid
erDiagram
    COACHING_ORDER ||--|| CUSTOMER : belongs_to
    COACHING_ORDER ||--|| COACHING_PACKAGE : uses
    COACHING_ORDER ||--|| COACH : assigned_to
    COACHING_ORDER ||--|| GOLF_COURSE : at
    COACHING_ORDER ||--o| COACHING_TEST : has
    COACHING_ORDER ||--o| COACHING_SPECS : has
    COACHING_ORDER ||--o{ COACHING_SESSION : has
    COACHING_ORDER ||--o{ SALES_ORDER : generates
    COACHING_SESSION ||--o| COACH : taught_by

    COACH ||--|| EMPLOYEE : extends

    COACHING_ORDER {
        int id PK
        string code "Auto: COACH-YYYYMMDD-XXX"
        int customer_id FK
        int package_id FK
        int coach_id FK
        int golf_course_id FK
        string status
        date start_date
        date end_date
        decimal total_fee "Tổng học phí"
        decimal discount "Ưu đãi"
        decimal paid_amount "Đã thanh toán"
        int total_sessions "Tổng số buổi"
        int completed_sessions "Đã học"
        text learning_goals "Mục tiêu học"
        timestamps
    }

    COACHING_PACKAGE {
        int id PK
        string name "VD: 8 buổi cơ bản"
        string type "Cá nhân/Nhóm/Thi đấu"
        int sessions_count "Số buổi"
        int duration_minutes "Thời lượng/buổi"
        decimal price
        text description
        bool is_active
        timestamps
    }

    COACH {
        int id PK
        int employee_id FK
        string certification "Chứng chỉ"
        int experience_years "Kinh nghiệm"
        string specialty "Chuyên môn"
        decimal rating "Đánh giá"
        text bio
        timestamps
    }

    GOLF_COURSE {
        int id PK
        string name "Tên sân tập"
        string address
        int lanes_count "Số lane"
        string contact_phone
        bool is_partner "Đối tác hay của NM"
        timestamps
    }

    COACHING_TEST {
        int id PK
        int coaching_order_id FK
        int coach_id FK "Người test"
        datetime test_date
        string skill_level "Kết quả đánh giá"
        json test_results "Chi tiết bài test"
        text notes
        text recommendations "Đề xuất gói"
        timestamps
    }

    COACHING_SESSION {
        int id PK
        int coaching_order_id FK
        int coach_id FK
        int session_number "Buổi thứ mấy"
        datetime scheduled_at
        datetime actual_start
        datetime actual_end
        string status "scheduled/completed/absent/cancelled"
        text lesson_content "Nội dung buổi học"
        text progress_notes "Ghi chú tiến trình"
        text homework "Bài tập về nhà"
        timestamps
    }

    COACHING_SPECS {
        int id PK
        int coaching_order_id FK
        decimal height_cm "Chiều cao"
        decimal weight_kg "Cân nặng"
        string glove_size "Size tay"
        string player_level "Cấp độ"
        decimal club_head_speed "Tốc độ đầu gậy"
        decimal ball_speed "Tốc độ bóng"
        string swing_shape "Hình swing"
        string ball_flight "Đường bóng"
        string ball_height "Đường cao bóng"
        decimal iron_distance "KC gậy sắt"
        decimal driver_distance "KC driver"
        text current_clubs "Gậy hiện tại"
        text customer_needs "Nhu cầu"
        text notes
        timestamps
    }
```

---

## 4. Sequence Diagram - Đăng ký & Test đầu vào

```mermaid
sequenceDiagram
    actor HV as Học viên
    participant NV as NV Tư vấn
    participant HLV as HLV
    participant CRM as CRM

    HV->>NV: Đăng ký học golf
    NV->>CRM: Tạo đơn Coaching (Mới)

    NV->>HLV: Chuyển cho HLV test
    HLV->>HV: Thực hiện bài test đầu vào
    HLV->>CRM: Nhập kết quả test
    CRM->>CRM: Cập nhật: Đã test

    HLV->>NV: Đề xuất gói phù hợp
    NV->>HV: Tư vấn gói & báo giá
```

---

## 5. Sequence Diagram - Đăng ký khóa học

```mermaid
sequenceDiagram
    actor HV as Học viên
    participant NV as NV Tư vấn
    participant CRM as CRM
    participant KT as Kế toán

    HV->>NV: Đăng ký khoá học (chọn gói & HLV)
    NV->>CRM: Cập nhật gói, HLV, sân tập
    NV->>CRM: Tạo Order (Đơn hàng)

    alt Thanh toán trọn gói
        HV->>KT: Thanh toán 100%
        KT->>CRM: Ghi nhận thanh toán vào Order
    else Thanh toán đặt cọc
        HV->>KT: Đặt cọc X%
        KT->>CRM: Ghi nhận đặt cọc vào Order
        Note over CRM: Còn nợ = Tổng - Đã cọc
    end

    CRM->>CRM: Cập nhật: Đã thanh toán
    NV->>HV: Xếp lịch học
    NV->>CRM: Tạo các buổi học (Sessions)
```

---

## 6. Sequence Diagram - Quá trình học

```mermaid
sequenceDiagram
    actor HV as Học viên
    participant HLV as HLV
    participant CRM as CRM

    loop Mỗi buổi học
        HV->>HLV: Đến học theo lịch

        alt Có mặt
            HLV->>CRM: Điểm danh: Có mặt
            HLV->>HV: Thực hiện buổi học
            HLV->>CRM: Ghi nhận nội dung & tiến trình
            CRM->>CRM: completed_sessions += 1
        else Vắng mặt
            HLV->>CRM: Điểm danh: Vắng
            Note over CRM: Xử lý theo chính sách?
        end
    end

    CRM->>CRM: Kiểm tra completed == total
    CRM->>CRM: Cập nhật: Hoàn thành
```

---

## 7. Flowchart - Điểm danh & Xử lý vắng

```mermaid
flowchart TD
    A[Buổi học theo lịch] --> B{Học viên có mặt?}

    B -->|Có| C[Điểm danh: Completed]
    B -->|Không| D{Báo trước?}

    D -->|Có| E[Điểm danh: Cancelled]
    D -->|Không| F[Điểm danh: Absent]

    E --> G{Chính sách học bù?}
    F --> G

    G -->|Được bù| H[Tạo buổi bù]
    G -->|Mất buổi| I[Trừ vào gói]

    C --> J[Cập nhật tiến trình]
    H --> J
    I --> J
```

---

## 8. Flowchart - Thanh toán

```mermaid
flowchart TD
    A[Đơn Coaching] --> B{Hình thức thanh toán?}

    B -->|Trọn gói| C[Thu 100%]
    B -->|Đặt cọc| D[Thu X%]
    B -->|Theo buổi| E[Thu từng buổi]

    C --> F[paid_amount = total_fee]
    D --> G[paid_amount = deposit]
    E --> H[paid_amount += per_session]

    F --> I{Còn nợ?}
    G --> I
    H --> I

    I -->|Có| J[Theo dõi công nợ]
    I -->|Không| K[Hoàn tất]

    J --> L{Nhắc nợ?}
    L -->|Có| M[Gửi thông báo]
```

---

## 9. Integration Diagram

```mermaid
flowchart TD
    subgraph COACHING["dcnet/coaching"]
        C1[Đơn Coaching]
        C2[Gói huấn luyện]
        C3[Buổi học]
        C4[Bài test]
        C5[HLV]
        C6[Sân tập]
        C7[Thông số KT]
    end

    subgraph PARTNERS["Partners"]
        P1[Customer]
    end

    subgraph EMPLOYEES["Employees"]
        E1[Employee]
    end

    subgraph SALES["Sales"]
        S1[Sales Order]
    end

    subgraph ACCOUNTS["Accounting"]
        A1[Payment]
        A2[Invoice]
    end

    subgraph CALENDAR["Calendar"]
        CAL1[Event]
    end

    P1 --> C1
    E1 --> C5
    C1 --> S1
    C1 --> A1
    C1 --> A2
    C3 --> CAL1
```

---

## 10. Tracking doanh thu phát sinh

```mermaid
flowchart LR
    A[Học viên hoàn thành khóa] --> B[Theo dõi đơn hàng]
    B --> C{Có mua SP?}

    C -->|Có| D[Link đơn SP với đơn Coaching]
    C -->|Không| E[Follow-up]

    D --> F[Tính doanh thu phát sinh]

    subgraph Report["Báo cáo Coaching"]
        G[Doanh thu đào tạo]
        H[Doanh thu SP phát sinh]
    end

    F --> H
```

---

## Quick Preview Commands

```bash
# VS Code với extension "Markdown Preview Mermaid Support"
# Hoặc paste từng block vào https://mermaid.live

# Export SVG/PNG từ CLI (cần cài mermaid-cli)
npx @mermaid-js/mermaid-cli mmdc -i COACHING_DIAGRAMS.md -o coaching-diagrams.svg
```

---

*Cập nhật: 2025-12-09*
