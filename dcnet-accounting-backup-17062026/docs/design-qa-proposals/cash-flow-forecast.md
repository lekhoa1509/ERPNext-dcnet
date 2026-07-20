## Session 2026-04-20 17:22

### Structural UX Proposals (not implemented — need human review)

#### P1. Inflow data too small relative to outflow (Data issue, not UI)

**Observation:** Dòng tiền vào chỉ VND 10.500 - 107.027.000 trong khi dòng tiền ra 43M - 129M. Inflow bars trên chart gần như invisible. Nguyên nhân có thể:
- Thiếu sample data cho Quotation, Sales Order (chưa có trong hệ thống)
- dcnet_contract chỉ có 1 contract với billing thấp
- Unpaid Sales Invoices ít

**Proposal:** Bơm thêm sample data phong phú (spec §9) để demo thực tế hơn. Hoặc xem xét thêm scale option cho chart (log scale khi chênh lệch lớn).

**Impact:** Medium — CFO sẽ nghi ngờ tính chính xác nếu forecast thiếu nguồn thu.

#### P2. Dashboard forecast chart X-axis labels bị cắt

**Observation:** Chart trên Dashboard v2 hiện "T..., T..., T..." thay vì "T4/2026, T5/2026...". Frappe.Chart auto-truncates labels khi container hẹp (50% width).

**Options:**
- A) Rút ngắn label format: "T4" thay vì "T4/2026" (chỉ trên dashboard, full page vẫn dài)
- B) Tăng chiều rộng chart container lên full-width
- C) Chấp nhận truncation (hover tooltip vẫn hiện đầy đủ)

**Recommendation:** A — label ngắn cho dashboard chart vì context đã rõ (12 months forward).

#### P3. Table number formatting dài (VND 1.844.468.000)

**Observation:** Số dư 1.8 tỷ hiện đầy đủ "VND 1.844.468.000" — chiếm nhiều chỗ trên bảng. CFO thường đọc số triệu/tỷ.

**Options:**
- A) Dùng abbreviated format trong bảng (1.84B hoặc 1,844M) — mất precision
- B) Giữ nguyên full format (chính xác hơn cho kế toán)
- C) Thêm toggle "Hiển thị đầy đủ / Rút gọn"

**Recommendation:** B — kế toán cần số chính xác. Chart đã abbreviated, bảng giữ full. Phù hợp 2 đối tượng.

## Session 2026-04-20 17:44 — CFO Expert Review

### P4. Summary bar trên đầu bảng (Structural — need human review)

**Observation:** CFO muốn thấy tổng kết nhanh mà không cần đọc từng dòng. Ví dụ:
- "Tổng thu 12 tháng: 320M | Tổng chi: 1.05B | Thặng dư/thâm hụt: -730M"
- Hoặc 3 KPI cards mini giống Dashboard v2

**Impact:** High — first thing CFO looks at. Hiện phải cộng từng dòng bằng mắt.

### P5. Thêm phương pháp dự báo nâng cao (v2 — Structural)

**Observation:** v1 dùng 4 phương pháp (Direct + Schedule + Historical + Aging-adjusted). Các phương pháp nâng cao hơn cho v2:
- **Regression/ARIMA:** dự báo revenue trend (tăng trưởng/suy giảm) thay vì flat projection
- **Scenario analysis:** Best/Worst/Base case — tham số hoá growth rate, churn rate, payment delay
- **Budget-based:** so sánh forecast vs ngân sách đã duyệt → variance analysis
- **Monte Carlo simulation:** phân phối xác suất cho collection date + amount → confidence interval thay vì point estimate

**Recommendation:** v2 nên bắt đầu với Scenario analysis (3 scenarios) — giá trị thực tiễn cao nhất cho CFO.

### P6. Cột % thay đổi so với tháng trước (Structural — need human review)

**Observation:** CFO cần thấy trend: "tháng này thu tăng 15% so với tháng trước" hoặc "chi giảm 20%". Hiện chỉ có số tuyệt đối.

**Options:**
- Thêm cột "Δ%" bên cạnh Inflow/Outflow (nhỏ, màu xám)
- Hoặc thêm sparkline mini trong cell

**Impact:** Medium — nice-to-have cho trend analysis.
