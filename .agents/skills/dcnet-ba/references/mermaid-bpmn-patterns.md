# Mermaid BPMN Rendering Patterns

> Cách vẽ BPMN bằng Mermaid syntax cho BA_ANALYSIS.md
> Mermaid không hỗ trợ native BPMN — dùng flowchart + subgraph mô phỏng.

---

## 1. Swimlane Pattern (Core)

Dùng `flowchart LR` (left-to-right) + `subgraph` cho swimlanes:

```mermaid
flowchart LR
    subgraph "BP Mua hàng"
        A["Tạo Purchase Order"] --> B["Gửi PO cho NCC"]
    end
    subgraph "NCC"
        B --> C["Xác nhận PO"]
        C --> D["Giao hàng"]
    end
    subgraph "NV Kho"
        D --> E["Nhận hàng + QC"]
        E --> F["Tạo Purchase Receipt"]
    end
    subgraph "Kế toán"
        F --> G["Tạo Purchase Invoice"]
        G --> H["GL Entry auto"]
    end
```

**Rules:**
- `flowchart LR` cho luồng trái → phải (swimlane ngang)
- `flowchart TB` cho luồng trên → dưới (swimlane dọc)
- Mỗi `subgraph` = 1 lane/role
- Quote tên subgraph: `subgraph "Tên Role"`
- Quote node labels có ký tự đặc biệt: `A["Label có dấu"]`

---

## 2. Gateway Patterns

### Exclusive Gateway (XOR) — Chỉ 1 đường

```mermaid
flowchart TB
    A["Review phiếu nhập"] --> B{"Duyệt?"}
    B -->|"Đồng ý"| C["Submit Purchase Receipt"]
    B -->|"Từ chối"| D["Trả lại Draft + ghi chú"]
    D --> A
```

### Parallel Gateway (AND) — Tất cả cùng lúc

```mermaid
flowchart TB
    A["PO Submit"] --> B["Gửi email NCC"]
    A --> C["Cập nhật Dashboard"]
    A --> D["Ghi Activity Log"]
    B --> E["Chờ tất cả hoàn thành"]
    C --> E
    D --> E
```

### Inclusive Gateway (OR) — 1 hoặc nhiều

```mermaid
flowchart TB
    A["Nhận hàng"] --> B{"Kiểm tra gì?"}
    B -->|"Số lượng"| C["Đếm SL"]
    B -->|"Chất lượng"| D["QC Check"]
    B -->|"Serial"| E["Scan Serial"]
    C --> F["Hoàn thành kiểm tra"]
    D --> F
    E --> F
```

> **Lưu ý:** Mermaid không phân biệt XOR/AND/OR visually.
> Dùng label và ghi chú để phân biệt:
> - XOR: chỉ 1 edge có điều kiện true
> - AND: ghi "(song song)"
> - OR: ghi "(1 hoặc nhiều)"

---

## 3. Start/End Events

```mermaid
flowchart LR
    START(("Bắt đầu")) --> A["Bước 1"]
    A --> B["Bước 2"]
    B --> END(("Kết thúc"))
```

**Shapes:**
- Start/End: `(("Label"))` — hình tròn kép
- Task: `["Label"]` — hình chữ nhật
- Decision: `{"Label?"}` — hình thoi
- Sub-process: `[["Label"]]` — hình chữ nhật kép

---

## 4. Exception Handling Pattern

```mermaid
flowchart TB
    A["Tạo Payment Entry"] --> B{"Thành công?"}
    B -->|"OK"| C["PE Submit → GL Entry"]
    B -->|"Lỗi số dư"| D["Thông báo Insufficient Balance"]
    B -->|"Lỗi rate"| E["Thông báo Exchange Rate Missing"]
    D --> F{"Sửa được?"}
    E --> F
    F -->|"Có"| A
    F -->|"Không"| G["Escalate → Kế toán trưởng"]
```

---

## 5. Approval Workflow Pattern (ERPNext)

```mermaid
flowchart LR
    subgraph "Người tạo"
        A["Tạo Draft"] --> B["Submit Request"]
    end
    subgraph "Người duyệt"
        B --> C{"Duyệt?"}
        C -->|"Approve"| D["Document Submit"]
        C -->|"Reject"| E["Return + Comment"]
    end
    subgraph "Hệ thống"
        D --> F["Auto: Stock Ledger"]
        D --> G["Auto: GL Entry"]
    end
    E --> A
```

---

## 6. Multi-step Process with Partial Receipt

```mermaid
flowchart TB
    PO["PO Submit<br/>100 units"] --> PR1["PR #1: 40 units"]
    PO --> PR2["PR #2: 35 units"]
    PO --> PR3["PR #3: 25 units"]
    PR1 --> SLE1["Stock +40"]
    PR2 --> SLE2["Stock +35"]
    PR3 --> SLE3["Stock +25"]
    SLE1 --> CHECK{"PO Complete?<br/>Received: 100/100"}
    SLE2 --> CHECK
    SLE3 --> CHECK
    CHECK -->|"Yes"| DONE["PO Status: Completed"]
    CHECK -->|"No"| WAIT["PO Status: To Receive"]
```

---

## 7. End-to-End Process (Full Module)

Pattern cho vẽ toàn bộ quy trình module:

```mermaid
flowchart TB
    subgraph "Phase 1: Planning"
        P1["Tạo Kế hoạch MH"] --> P2["Duyệt KH"]
    end
    subgraph "Phase 2: Ordering"
        P2 --> O1["Tạo PO từ KH"]
        O1 --> O2["Gửi PO cho NCC"]
        O2 --> O3["NCC xác nhận"]
    end
    subgraph "Phase 3: Receiving"
        O3 --> R1["Nhận hàng"]
        R1 --> R2{"QC Pass?"}
        R2 -->|"Pass"| R3["Submit PR"]
        R2 -->|"Fail"| R4["Return NCC"]
    end
    subgraph "Phase 4: Accounting"
        R3 --> A1["Tạo Purchase Invoice"]
        A1 --> A2["Payment Entry"]
    end
```

---

## 8. Process Status Colors (Optional)

Dùng `style` để tô màu theo loại:

```
%% Automated step (Green)
style F fill:#e8f5e9,stroke:#4caf50

%% Manual step (Orange)
style B fill:#fff3e0,stroke:#ff9800

%% Exception/Error (Red)
style D fill:#fce4ec,stroke:#f44336

%% Decision point (Yellow)
style C fill:#fff9c4,stroke:#f9a825

%% External party (Blue)
style E fill:#e3f2fd,stroke:#1976d2
```

**Color convention cho DCNET:**

| Loại | Fill | Stroke | Dùng cho |
|------|------|--------|----------|
| Auto (hệ thống) | `#e8f5e9` | `#4caf50` | Service task, auto GL, auto stock |
| Manual (người) | `#fff3e0` | `#ff9800` | User task, form fill |
| Error/Exception | `#fce4ec` | `#f44336` | Lỗi, reject, return |
| Decision | `#fff9c4` | `#f9a825` | Gateway, approval |
| External | `#e3f2fd` | `#1976d2` | NCC, khách hàng, bên ngoài |
| Milestone | `#f3e5f5` | `#7b1fa2` | Phase end, checkpoint |

---

## 9. Sequence Diagram (cho API/Integration flows)

Khi cần mô tả interaction giữa các hệ thống:

```mermaid
sequenceDiagram
    actor User as BP Mua hàng
    participant PO as Purchase Order
    participant PR as Purchase Receipt
    participant SLE as Stock Ledger
    participant GL as GL Entry

    User->>PO: Tạo PO (Draft)
    User->>PO: Submit PO
    PO-->>User: PO Submitted

    User->>PR: Tạo PR từ PO
    User->>PR: Submit PR
    PR->>SLE: Auto: Stock Ledger Entry
    PR-->>User: PR Submitted + Stock updated

    User->>GL: Tạo Purchase Invoice
    GL-->>User: Auto GL Entry created
```

---

## 10. State Diagram (cho DocType lifecycle)

```mermaid
stateDiagram-v2
    [*] --> DRAFT
    DRAFT --> PENDING: Submit request
    PENDING --> APPROVED: Manager approve
    PENDING --> REJECTED: Manager reject
    REJECTED --> DRAFT: Revise
    APPROVED --> SUBMITTED: Auto submit
    SUBMITTED --> CANCELLED: Cancel
    SUBMITTED --> AMENDED: Amend
    SUBMITTED --> [*]: Completed

    DRAFT: Nháp
    PENDING: Chờ duyệt
    APPROVED: Đã duyệt
    REJECTED: Từ chối
    SUBMITTED: Đã ghi sổ
    CANCELLED: Đã hủy
    AMENDED: Đã sửa
```

> **IMPORTANT:** State IDs phải là ASCII (không dùng tiếng Việt trong ID).
> Dùng label bên dưới để hiển thị tiếng Việt.

---

## 11. Mermaid Syntax Quick Reference

| Element | Syntax | Example |
|---------|--------|---------|
| Rectangle | `A["Label"]` | `A["Tạo PO"]` |
| Rounded rect | `A("Label")` | `A("Start")` |
| Circle | `A(("Label"))` | `A(("End"))` |
| Diamond | `A{"Label?"}` | `A{"Duyệt?"}` |
| Double rect | `A[["Label"]]` | `A[["Sub-process"]]` |
| Arrow | `-->` | `A --> B` |
| Arrow + label | `-->\|"label"\|` | `A -->\|"Yes"\| B` |
| Dotted arrow | `-.->` | `A -.-> B` |
| Thick arrow | `==>` | `A ==> B` |
| Subgraph | `subgraph "Name"` | `subgraph "Kho"` |

---

## 12. Common Mistakes & Fixes

| Mistake | Fix |
|---------|-----|
| Vietnamese in state IDs | Dùng ASCII IDs + label definitions |
| Unquoted special chars | Quote: `A["text: value"]` |
| Missing subgraph `end` | Mỗi `subgraph` phải có `end` |
| Crossing connections | Rearrange nodes, dùng hidden nodes |
| Too many nodes (>25) | Tách thành multiple diagrams |
| Label quá dài | Max ~40 chars, dùng `<br/>` xuống dòng |
| Duplicate node IDs | Mỗi node ID unique trong 1 diagram |

---

## 13. Reuse Rules from dcnet-module

Follow [mermaid-validation.md](../../dcnet-module/references/mermaid-validation.md):
1. State diagrams: ASCII IDs only
2. Flowcharts: Quote special characters
3. ERD: No Unicode in descriptions
4. Line endings: Unix (LF)
5. Code fences: Must be balanced
