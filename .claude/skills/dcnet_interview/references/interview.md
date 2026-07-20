# Interview Reference — Socratic Questioning for DCNET Flow

## Question Templates by Domain

### Khi clarify feature spec (FEATURE_SPECIFICATION / ERP_SPECIFICATION)

```
"Section [X.Y.Z] nói '[quote]' — ý khách là [interpretation A] hay [interpretation B]?"
"Feature [name] tag [EXT] — cần extend ERPNext [DocType] bằng cách nào?"
"Spec mention '[term]' — đây là [ERPNext concept] hay business concept riêng?"
"[Feature] áp dụng cả 2 công ty hay chỉ [TM/NM]?"
```

### Khi clarify kế toán (COA / GL Entry)

```
"TK [number] — [name]: Account Type trong ERPNext nên là gì? (Stock/Expense/Income/...)"
"Flow [transaction] sinh GL Entry: Nợ [TK] / Có [TK] — đúng chưa?"
"Spec nói '[costing method]' — ERPNext hỗ trợ [X/Y]. Khách accept [Y] không?"
"Phiếu [thu/chi] theo mẫu TT200 hay format ERPNext? Cần field gì thêm?"
```

### Khi clarify workflow / business logic

```
"Khi [event] xảy ra, hệ thống nên [action A] hay [action B]?"
"Status flow: [Draft → Submitted → ...] — có status nào khác không?"
"Ai approve [document]? Role nào? Cần multi-level approval không?"
"Nếu [edge case] thì xử lý sao? Spec không mention."
```

### Khi clarify data migration (BRAVO → ERPNext)

```
"BRAVO field [X] map vào ERPNext field nào?"
"Data [type] có bao nhiêu records? Cần migrate history hay chỉ current?"
"Opening balance tính từ ngày nào?"
"Mã khách/NCC trong BRAVO có format gì? Giữ nguyên hay đổi?"
```

## Ambiguity Signals (Khi nào cần interview)

| Signal | Example | Action |
|--------|---------|--------|
| Spec dùng từ mơ hồ | "hệ thống cần linh hoạt" | Hỏi: linh hoạt nghĩa là gì cụ thể? |
| Spec conflict nhau | TT99 vs TT200 | Hỏi: file nào đúng? |
| Thiếu edge case | Trade-in giá cũ > giá mới | Hỏi: hoàn tiền chênh lệch? |
| Không rõ scope | "báo cáo phân tích" | Hỏi: bao nhiêu báo cáo? fields nào? |
| Không rõ company | Feature X | Hỏi: cả 2 hay chỉ TM/NM? |
| Không rõ timeline | Feature Y | Hỏi: tháng mấy? T3-T6? |

## Anti-Patterns (KHÔNG làm)

- KHÔNG hỏi yes/no questions — hỏi open-ended hoặc choice
- KHÔNG hỏi nhiều câu cùng lúc — 1-2 câu/round
- KHÔNG hỏi lại thứ đã có trong spec — cite spec section
- KHÔNG giả định — ghi rõ "⚠️ Cần clarify với khách hàng"
- KHÔNG tự quyết thay khách — document as CLARIFY.md
