# BPMN Notation Reference

> Business Process Model and Notation — chuẩn quốc tế mô hình hóa quy trình nghiệp vụ.
> Dùng khi vẽ process diagrams trong BA_ANALYSIS.md

---

## BPMN Core Elements

### 1. Activities (Hình chữ nhật)

| Type | Symbol | Description | Khi dùng |
|------|--------|-------------|----------|
| **Task** | Rectangle | Đơn vị công việc nguyên tử | Bước đơn lẻ: "Tạo PO", "Duyệt phiếu" |
| **Sub-Process** | Rectangle + marker | Chứa process con | Nhóm nhiều bước: "Nhập kho" |
| **Call Activity** | Rectangle thick border | Gọi process tái sử dụng | Quy trình dùng lại: "Kiểm tra tồn kho" |

**Task Types (BPMN 2.0):**

| Type | Description | ERPNext mapping |
|------|-------------|-----------------|
| User Task | Cần người thao tác | Form fill, button click trên Desk |
| Service Task | Hệ thống tự động | Server script, hooks, API call |
| Script Task | Chạy code/script | Client script, scheduled job |
| Business Rule Task | Đánh giá luật nghiệp vụ | Pricing Rule, Workflow State |
| Send Task | Gửi thông điệp | Email notification, webhook |
| Receive Task | Nhận thông điệp | Webhook receiver, API endpoint |
| Manual Task | Công việc vật lý, không cần hệ thống | Kiểm đếm hàng, ký giấy |

### 2. Events (Hình tròn)

| Position | Symbol | Description |
|----------|--------|-------------|
| **Start** | Thin circle | Khởi đầu quy trình (trigger) |
| **Intermediate** | Double circle | Sự kiện giữa quy trình |
| **End** | Thick circle | Kết thúc quy trình |

**Event Types:**

| Type | Trigger | ERPNext example |
|------|---------|-----------------|
| None | Không xác định | Bắt đầu manual |
| Message | Nhận/gửi message | Email notification |
| Timer | Thời gian | Scheduled task, cron |
| Error | Lỗi xảy ra | Validation error, stock không đủ |
| Signal | Broadcast | Event hook across modules |
| Terminate | Kết thúc toàn bộ | Cancel document |

### 3. Gateways (Hình thoi)

| Type | Symbol | Description | Khi dùng |
|------|--------|-------------|----------|
| **Exclusive (XOR)** | Diamond + X | CHỈ 1 đường đi | "Duyệt hay Từ chối?" |
| **Parallel (AND)** | Diamond + + | TẤT CẢ đường đi cùng lúc | "Gửi email + Cập nhật kho + Ghi sổ" |
| **Inclusive (OR)** | Diamond + O | 1 HOẶC NHIỀU đường đi | "Cần kiểm hàng VÀ/HOẶC kiểm giá" |
| **Event-Based** | Diamond + circle | Chờ sự kiện xảy ra | "Chờ NCC confirm HOẶC timeout 7 ngày" |

**Gateway Rules:**
- Mỗi split gateway PHẢI có join gateway tương ứng
- XOR split → XOR join
- AND split → AND join
- Label rõ điều kiện trên mỗi nhánh

### 4. Connectors

| Type | Symbol | Description |
|------|--------|-------------|
| **Sequence Flow** | Solid arrow → | Thứ tự thực hiện |
| **Message Flow** | Dashed arrow ⇢ | Giao tiếp giữa pools |
| **Association** | Dotted line ··· | Gắn artifacts vào elements |

### 5. Swimlanes

| Type | Description | Khi dùng |
|------|-------------|----------|
| **Pool** | Đại diện tổ chức/hệ thống | "Công ty TLTM", "NCC Titleist" |
| **Lane** | Phân chia trong pool theo role | "BP Mua hàng", "NV Kho", "Kế toán" |

---

## Common Process Patterns

### Pattern 1: Sequential (Tuần tự)

Từng bước nối tiếp nhau.

```
A → B → C → D
```

**Dùng khi:** Luồng đơn giản, ít nhánh.

### Pattern 2: Parallel Split & Join

Nhiều việc làm cùng lúc, chờ tất cả xong mới tiếp.

```
      ┌→ B ─┐
A → ╋ → C ─╋ → E
      └→ D ─┘
```

**ERPNext example:** Submit PO → (Gửi email NCC + Cập nhật Dashboard + Log activity) → Done

### Pattern 3: Exclusive Decision

Chỉ đi 1 đường dựa trên điều kiện.

```
      ┌─Yes→ B
A → ◇
      └─No─→ C
```

**ERPNext example:** PR Draft → Duyệt? → (Yes: Submit PR) / (No: Return for revision)

### Pattern 4: Loop / Iteration

Lặp cho đến khi thỏa điều kiện.

```
A → B → ◇─No→ B (lặp lại)
         └─Yes→ C
```

**ERPNext example:** QC Check → Pass? → (No: Re-inspect) / (Yes: Accept)

### Pattern 5: Exception Handling

Xử lý lỗi và ngoại lệ.

```
A → ◇─Success→ B
     └─Error→ C → ◇─Recoverable?─Yes→ A (retry)
                    └─No→ D (escalate)
```

**ERPNext example:** Payment → Success? → (Error: Payment failed) → Retry or Escalate

### Pattern 6: Approval Workflow

Mẫu phê duyệt thường gặp trong ERPNext.

```
Draft → Submit Request → ◇ Reviewer
                          ├─Approve→ Submit → Auto GL/Stock
                          └─Reject→ Return to Draft (with comments)
```

**ERPNext Workflow DocType:** Draft → Pending Approval → Approved → Submitted

---

## BPMN for ERPNext — Mapping Conventions

| BPMN Concept | ERPNext Equivalent |
|-------------|-------------------|
| Pool | Company / External Party (Supplier, Customer) |
| Lane | Role (Purchase User, Stock User, Accounts User) |
| User Task | Form action (fill, submit, amend) |
| Service Task | Server script, on_submit hook, auto GL |
| Start Event (Message) | Incoming email, webhook, API call |
| Start Event (Timer) | Scheduled task (bench execute) |
| Exclusive Gateway | Workflow transition conditions |
| Error End Event | ValidationError, frappe.throw() |
| Terminate End Event | Cancel document (is_cancelled=1) |

---

## Validation Checklist

| Check | Question |
|-------|----------|
| All paths connected | Tất cả activities có incoming + outgoing flows? |
| No dead ends | Tất cả paths đến được end event? |
| Gateways balanced | Split gateway có join gateway tương ứng? |
| Roles assigned | Mỗi activity nằm trong 1 lane? |
| Triggers defined | Mỗi start event có trigger rõ ràng? |
| Labels clear | Gateways có label dạng câu hỏi? |
| Exceptions handled | Có xử lý lỗi cho bước quan trọng? |
