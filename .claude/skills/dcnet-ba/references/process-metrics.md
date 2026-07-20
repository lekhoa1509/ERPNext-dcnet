# Process Metrics Reference - ERPNext Processes

> KPI va metrics cho do luong hieu qua quy trinh ERPNext.
> Dung de thiet lap targets va do luong cai thien sau khi trien khai.

---

## 1. Core Process Metrics

### Time Metrics

| Metric | Dinh nghia | Cach do | Don vi |
|--------|-----------|---------|--------|
| Process Time (PT) | Thoi gian thuc su xu ly | Bam gio tung buoc | phut |
| Lead Time (LT) | Tong thoi gian end-to-end | Tu tao -> hoan thanh | gio/ngay |
| Wait Time (WT) | Thoi gian cho = LT - PT | LT minus PT | gio |
| Cycle Time | Thoi gian trung binh 1 item | LT / throughput | gio |
| Takt Time | Nhip san xuat theo nhu cau | Available time / demand | gio |

### Quality Metrics

| Metric | Dinh nghia | Target |
|--------|-----------|--------|
| %C&A (Complete & Accurate) | % hoan thanh dung ngay lan dau | > 95% |
| Error Rate | % giao dich co loi | < 2% |
| Rework Rate | % can sua lai | < 5% |
| First Pass Yield | % qua duoc validation lan dau | > 90% |

### Efficiency Metrics

| Metric | Cong thuc | Y nghia |
|--------|----------|---------|
| Flow Efficiency | PT / LT x 100% | % thoi gian thuc su tao gia tri |
| Automation Rate | Auto steps / Total steps x 100% | % buoc duoc tu dong hoa |
| Throughput | Items completed / Time period | Nang suat |
| WIP (Work in Progress) | Items in process | Khoi luong do dang |

---

## 2. ERPNext-Specific KPIs

### Mua hang (Purchasing)

| KPI | Cach do trong ERPNext | Target |
|-----|----------------------|--------|
| PO Cycle Time | PO creation -> PO submit | < 1 ngay |
| PR Processing Time | Goods received -> PR submit | < 4 gio |
| Invoice Processing | PR submit -> PI submit | < 2 ngay |
| Supplier Lead Time | PO submit -> PR submit | Track per supplier |
| PO -> Payment Cycle | PO submit -> PE submit | < 30 ngay |

### Ban hang (Sales)

| KPI | Cach do trong ERPNext | Target |
|-----|----------------------|--------|
| SO Processing Time | SO creation -> SO submit | < 2 gio |
| Delivery Time | SO submit -> DN submit | < 3 ngay |
| Invoice Time | DN submit -> SI submit | < 1 ngay |
| DSO (Days Sales Outstanding) | Accounts Receivable aging | < 45 ngay |

### Kho (Inventory)

| KPI | Cach do trong ERPNext | Target |
|-----|----------------------|--------|
| Stock Accuracy | Physical count vs system | > 98% |
| Stock Turn | COGS / Average Inventory | Industry benchmark |
| Receiving Time | Goods arrival -> PR submit | < 4 gio |
| Picking Time | SO confirmed -> DN ready | < 2 gio |

### Ke toan (Accounting)

| KPI | Cach do trong ERPNext | Target |
|-----|----------------------|--------|
| Month-end Close | Days to close books | < 5 ngay |
| Reconciliation Time | Bank -> Payment matching | < 2 ngay |
| GL Accuracy | Manual GL adjustments needed | < 1% |
| Auto GL Rate | Auto GL / Total GL entries | > 95% |

---

## 3. Metrics Template cho BA_ANALYSIS.md

Dung template nay khi viet phan Process Metrics trong file BA_ANALYSIS.md:

```markdown
### Process Metrics: {QT Name}

#### Current State (Uoc tinh)
| Metric | Value | Note |
|--------|-------|------|
| Process Time | Xm | {from observation or estimate} |
| Lead Time | Xh | {including wait time} |
| Flow Efficiency | X% | PT/LT |
| %C&A | X% | {first-time right rate} |
| Automation Rate | X% | {auto vs manual steps} |

#### Target (Sau trien khai ERPNext)
| Metric | Current | Target | Improvement |
|--------|---------|--------|-------------|
| Process Time | Xm | Xm | -X% |
| Lead Time | Xh | Xh | -X% |
| Flow Efficiency | X% | X% | +Xx |
| %C&A | X% | X% | +X% |
| Automation Rate | X% | X% | +X% |

#### Improvement Sources
| Cai thien | Nguon | Metric impact |
|-----------|-------|---------------|
| Auto GL Entry | ERPNext Perpetual Inventory | LT -80%, Error -95% |
| Workflow Approval | ERPNext Workflow | WT -60% |
| Auto-populate from PO | ERPNext Get Items | PT -50%, Error -80% |
```

---

## 4. YAML Structured Output

For machine-readable process metrics (dung trong BA_ANALYSIS.md phan cuoi):

```yaml
process_metrics:
  module: "{STT}-{slug}"
  date: "{ISO date}"

  processes:
    - id: "QT1"
      name: "{Process name}"

      current_state:
        process_time_minutes: X
        lead_time_hours: X
        flow_efficiency_percent: X
        complete_accurate_percent: X
        automation_rate_percent: X
        wip_count: X

      target_state:
        process_time_minutes: X
        lead_time_hours: X
        flow_efficiency_percent: X
        complete_accurate_percent: X
        automation_rate_percent: X
        wip_count: X

      improvements:
        - name: "{Improvement}"
          source: "{ERPNext feature}"
          metric: "{Which metric}"
          impact: "{Quantified improvement}"

      bottlenecks:
        - step: "{Step name}"
          cause: "{Root cause}"
          solution: "{ERPNext solution}"

  summary:
    total_lt_reduction_percent: X
    total_fe_improvement: "X% -> X%"
    automation_increase: "X% -> X%"
    key_risk: "{Main risk}"
```

---

## 5. Benchmark Data (DCNET Reference)

### Industry Benchmarks - Retail/Distribution

| Process | Typical LT | Best Practice LT | ERPNext Target |
|---------|-----------|------------------|----------------|
| Order-to-Cash | 15-30 days | 3-7 days | 5-10 days |
| Procure-to-Pay | 30-60 days | 10-20 days | 15-25 days |
| Month-end Close | 10-15 days | 3-5 days | 5-7 days |
| Inventory Count | Monthly manual | Real-time | Perpetual + quarterly count |

### Automation Rate by Module

| Module | Before ERP | After ERPNext | Key automations |
|--------|-----------|---------------|-----------------|
| Purchasing | 20-30% | 70-80% | Auto GL, workflow, PO->PR->PI flow |
| Sales | 30-40% | 75-85% | Auto pricing, SO->DN->SI flow |
| Inventory | 10-20% | 60-70% | Perpetual inventory, barcode |
| Accounting | 40-50% | 85-95% | Auto GL, bank recon, tax calc |

---

## 6. When to Include Process Metrics

| Module Type | Include Metrics? | Level |
|-------------|-----------------|-------|
| Simple (all USE/CFG) | Basic only | Current/Target LT table |
| Medium (some EXT) | Standard | Full metrics template |
| Complex (EXT/NEW) | Comprehensive | Full template + YAML + benchmarks |
| Accounting | Always comprehensive | Full + compliance metrics |

---

## 7. Metrics Collection Guidelines

### Before Go-Live (Estimate)

- Use industry benchmarks as baseline
- Interview users for current process times
- Mark all estimates clearly: "Warning: Uoc tinh, can do thuc te"
- Compare with BRAVO current state where possible

### After Go-Live (Measure)

- ERPNext has built-in creation/modification timestamps on every DocType
- Use `creation` and `modified` fields to calculate actual LT, PT
- Custom Report to aggregate metrics by period
- Dashboard for real-time KPIs (Number Cards + Dashboard Charts)

### ERPNext Fields for Measurement

```
Every DocType has:
  creation    — timestamp when doc was created
  modified    — timestamp of last modification
  owner       — user who created
  modified_by — user who last modified

Workflow Action Log:
  workflow_state changes with timestamps → calculate wait time per step

Amendment Log:
  amended_from → track rework rate

Status transitions:
  Draft → Submitted → Cancelled → Amended
  Each transition = measurable event
```

### Calculating Metrics from ERPNext Data

```python
# Lead Time: PO submit -> PI submit
lead_time = frappe.db.sql("""
    SELECT
        pi.name,
        TIMESTAMPDIFF(HOUR, po.modified, pi.modified) as lead_time_hours
    FROM `tabPurchase Invoice` pi
    JOIN `tabPurchase Order` po ON pi.purchase_order = po.name
    WHERE pi.docstatus = 1
""")

# Automation Rate: count auto vs manual GL entries
auto_gl = frappe.db.count("GL Entry", {"is_cancelled": 0, "voucher_type": ["!=", "Journal Entry"]})
manual_gl = frappe.db.count("GL Entry", {"is_cancelled": 0, "voucher_type": "Journal Entry"})
automation_rate = auto_gl / (auto_gl + manual_gl) * 100
```

---

## 8. DCNET-Specific Considerations

### Migration from BRAVO

Khi do luong improvement, can compare:

| Aspect | BRAVO (Current) | ERPNext (Target) | How to measure |
|--------|-----------------|-------------------|----------------|
| Data entry | Manual, tung truong | Auto-populate from linked docs | PT reduction |
| Approval | Giay / email | ERPNext Workflow | WT reduction |
| GL posting | Manual journal entry | Auto GL from transactions | Automation Rate |
| Reporting | Export Excel -> xu ly | Real-time Dashboard | Report generation time |
| Inventory | Periodic count | Perpetual + Stock Ledger | Stock Accuracy |

### Two-Company Setup (Thang Long TM + Nhat Minh Sport)

- Metrics targets may differ between 2 companies
- Track separately: `company` filter in all queries
- Benchmark against each other after go-live
- Same code, different data volumes -> different performance profiles
