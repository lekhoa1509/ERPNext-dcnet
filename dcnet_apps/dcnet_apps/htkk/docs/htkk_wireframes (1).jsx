import { useState } from "react";

const COLORS = {
  bg: "#F8F9FA",
  surface: "#FFFFFF",
  primary: "#1B4F72",
  secondary: "#2E86C1",
  accent: "#D4E6F1",
  green: "#27AE60",
  yellow: "#F39C12",
  red: "#E74C3C",
  gray: "#95A5A6",
  grayLight: "#ECF0F1",
  grayDark: "#2C3E50",
  text: "#2C3E50",
  textMuted: "#7F8C8D",
  border: "#DEE2E6",
};

const screens = [
  { id: "declaration-list", label: "Danh sách Tờ khai" },
  { id: "declaration-draft", label: "Workspace (Draft)" },
  { id: "declaration-pending", label: "Workspace (Pending)" },
  { id: "declaration-submitted", label: "Workspace (Submitted)" },
  { id: "auto-detect", label: "Auto-detect Review" },
  { id: "khbs-modal", label: "KHBS Lý do Modal" },
  { id: "drilldown", label: "Drill-down Popup" },
  { id: "template-manager", label: "Template Manager" },
  { id: "mapping-rule", label: "Mapping Rule" },
  { id: "package-import", label: "Package Import" },
];

// ─── Shared Components ───
function StatusBadge({ status }) {
  const map = {
    Draft: { bg: "#EBF5FB", color: COLORS.secondary, text: "Draft" },
    Pending: { bg: "#FEF9E7", color: COLORS.yellow, text: "Chờ duyệt" },
    Submitted: { bg: "#EAFAF1", color: COLORS.green, text: "Đã chốt" },
    Cancelled: { bg: "#FDEDEC", color: COLORS.red, text: "Đã hủy" },
  };
  const s = map[status] || map.Draft;
  return (
    <span style={{ background: s.bg, color: s.color, padding: "2px 10px", borderRadius: 12, fontSize: 11, fontWeight: 600 }}>
      {s.text}
    </span>
  );
}

function Btn({ children, variant = "primary", size = "md", disabled, onClick, icon }) {
  const styles = {
    primary: { bg: COLORS.primary, color: "#fff", border: "none" },
    secondary: { bg: "#fff", color: COLORS.primary, border: `1px solid ${COLORS.primary}` },
    success: { bg: COLORS.green, color: "#fff", border: "none" },
    danger: { bg: COLORS.red, color: "#fff", border: "none" },
    ghost: { bg: "transparent", color: COLORS.textMuted, border: `1px solid ${COLORS.border}` },
  };
  const s = styles[variant];
  const pad = size === "sm" ? "4px 10px" : "7px 16px";
  const fs = size === "sm" ? 11 : 13;
  return (
    <button
      onClick={onClick}
      disabled={disabled}
      style={{
        background: disabled ? COLORS.grayLight : s.bg,
        color: disabled ? COLORS.gray : s.color,
        border: s.border,
        padding: pad,
        borderRadius: 6,
        fontSize: fs,
        fontWeight: 600,
        cursor: disabled ? "not-allowed" : "pointer",
        display: "inline-flex",
        alignItems: "center",
        gap: 5,
        opacity: disabled ? 0.6 : 1,
        fontFamily: "'IBM Plex Sans', sans-serif",
      }}
    >
      {icon && <span style={{ fontSize: fs + 2 }}>{icon}</span>}
      {children}
    </button>
  );
}

function Tag({ children, color = COLORS.secondary }) {
  return (
    <span style={{ background: color + "18", color, padding: "1px 8px", borderRadius: 4, fontSize: 10, fontWeight: 600 }}>
      {children}
    </span>
  );
}

// ─── Fake Spreadsheet Grid ───
function SpreadsheetGrid({ mode = "draft", showCompare = false }) {
  const cellColors = {
    auto: "#EBF5FB",
    manual: "#FEF9E7",
    readonly: "#F4F6F7",
    error: "#FDEDEC",
    compare: "#F5EEF8",
  };

  const rows = [
    { label: "Doanh thu hàng hóa, DV bán ra", code: "[29]", value: "1,250,000,000", type: "auto" },
    { label: "Thuế GTGT của HH, DV bán ra", code: "[30]", value: "125,000,000", type: "auto" },
    { label: "Hàng hóa, DV mua vào", code: "[37]", value: "980,500,000", type: mode === "draft" ? "manual" : "auto" },
    { label: "Thuế GTGT được khấu trừ", code: "[38]", value: "98,050,000", type: "auto" },
    { label: "Thuế GTGT còn phải nộp", code: "[40]", value: "26,950,000", type: "readonly" },
  ];

  return (
    <div style={{ border: `1px solid ${COLORS.border}`, borderRadius: 4, overflow: "hidden", fontSize: 12 }}>
      {/* Column headers */}
      <div style={{ display: "grid", gridTemplateColumns: "35px 60px 280px 160px", background: "#F0F3F5", borderBottom: `1px solid ${COLORS.border}` }}>
        <div style={{ padding: "4px 6px", borderRight: `1px solid ${COLORS.border}`, color: COLORS.textMuted, fontSize: 10 }}></div>
        <div style={{ padding: "4px 8px", borderRight: `1px solid ${COLORS.border}`, color: COLORS.textMuted, fontWeight: 600, fontSize: 10 }}>A</div>
        <div style={{ padding: "4px 8px", borderRight: `1px solid ${COLORS.border}`, color: COLORS.textMuted, fontWeight: 600, fontSize: 10 }}>B</div>
        <div style={{ padding: "4px 8px", color: COLORS.textMuted, fontWeight: 600, fontSize: 10 }}>C</div>
      </div>
      {rows.map((row, i) => {
        const bg = mode === "submitted" ? cellColors.readonly : cellColors[row.type];
        const compareBg = showCompare && row.type === "manual" ? cellColors.compare : bg;
        return (
          <div key={i} style={{ display: "grid", gridTemplateColumns: "35px 60px 280px 160px", borderBottom: `1px solid ${COLORS.border}` }}>
            <div style={{ padding: "6px", borderRight: `1px solid ${COLORS.border}`, color: COLORS.textMuted, fontSize: 10, background: "#F0F3F5", textAlign: "center" }}>{i + 15}</div>
            <div style={{ padding: "6px 8px", borderRight: `1px solid ${COLORS.border}`, fontWeight: 600, color: COLORS.primary, fontSize: 11 }}>{row.code}</div>
            <div style={{ padding: "6px 8px", borderRight: `1px solid ${COLORS.border}`, color: COLORS.text }}>{row.label}</div>
            <div style={{
              padding: "6px 8px",
              background: compareBg,
              textAlign: "right",
              fontWeight: 500,
              color: COLORS.text,
              position: "relative",
            }}>
              {row.value}
              {showCompare && row.type === "manual" && (
                <div style={{ position: "absolute", top: -1, right: 2, fontSize: 8, color: COLORS.red }}>
                  gốc: 950,200,000
                </div>
              )}
            </div>
          </div>
        );
      })}
    </div>
  );
}

// ─── Sheet Tabs ───
function SheetTabs({ active = 0 }) {
  const tabs = ["Tờ khai 01/GTGT", "PL 01-1/GTGT", "PL 01-2/GTGT", "PL 01/KHBS"];
  return (
    <div style={{ display: "flex", borderTop: `1px solid ${COLORS.border}`, background: "#F0F3F5" }}>
      {tabs.map((t, i) => (
        <div key={i} style={{
          padding: "5px 14px",
          fontSize: 11,
          fontWeight: i === active ? 600 : 400,
          color: i === active ? COLORS.primary : COLORS.textMuted,
          background: i === active ? "#fff" : "transparent",
          borderRight: `1px solid ${COLORS.border}`,
          borderTop: i === active ? `2px solid ${COLORS.secondary}` : "2px solid transparent",
          cursor: "pointer",
          fontFamily: "'IBM Plex Sans', sans-serif",
        }}>{t}</div>
      ))}
    </div>
  );
}

// ─── Color Legend ───
function ColorLegend() {
  const items = [
    { color: "#EBF5FB", border: "#2E86C1", label: "Dữ liệu tự động" },
    { color: "#FEF9E7", border: "#F39C12", label: "Đã sửa thủ công" },
    { color: "#F4F6F7", border: "#95A5A6", label: "Read-only / Công thức" },
    { color: "#FDEDEC", border: "#E74C3C", label: "Lỗi validation" },
  ];
  return (
    <div style={{ display: "flex", gap: 12, padding: "6px 0" }}>
      {items.map((item, i) => (
        <div key={i} style={{ display: "flex", alignItems: "center", gap: 4, fontSize: 10, color: COLORS.textMuted }}>
          <div style={{ width: 14, height: 14, background: item.color, border: `1.5px solid ${item.border}`, borderRadius: 2 }} />
          {item.label}
        </div>
      ))}
    </div>
  );
}

// ═══════════════════════════════════════
// SCREEN: Declaration List
// ═══════════════════════════════════════
function DeclarationListScreen() {
  const data = [
    { id: "HTKK-2026-001", type: "GTGT 01/GTGT", period: "Tháng 01/2026", status: "Submitted", company: "Công ty ABC" },
    { id: "HTKK-2026-002", type: "GTGT 01/GTGT", period: "Tháng 02/2026", status: "Pending", company: "Công ty ABC" },
    { id: "HTKK-2026-003", type: "GTGT 01/GTGT", period: "Tháng 03/2026", status: "Draft", company: "Công ty ABC" },
    { id: "HTKK-2026-004", type: "TNDN Quý", period: "Quý I/2026", status: "Draft", company: "Công ty ABC" },
  ];
  return (
    <div>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 16 }}>
        <div>
          <h2 style={{ margin: 0, fontSize: 18, color: COLORS.grayDark, fontFamily: "'IBM Plex Sans', sans-serif" }}>HTKK Declaration</h2>
          <p style={{ margin: "2px 0 0", fontSize: 12, color: COLORS.textMuted }}>Quản lý tờ khai thuế</p>
        </div>
        <Btn icon="＋">Tạo tờ khai mới</Btn>
      </div>

      {/* Alert */}
      <div style={{ background: "#FEF9E7", border: `1px solid ${COLORS.yellow}40`, borderRadius: 6, padding: "8px 12px", marginBottom: 12, display: "flex", alignItems: "center", gap: 8 }}>
        <span style={{ fontSize: 16 }}>⚠️</span>
        <span style={{ fontSize: 12, color: COLORS.text }}>
          <strong>Deadline:</strong> Tờ khai GTGT Tháng 03/2026 cần nộp trước <strong>20/04/2026</strong> (còn 7 ngày)
        </span>
      </div>

      {/* Table */}
      <div style={{ border: `1px solid ${COLORS.border}`, borderRadius: 8, overflow: "hidden" }}>
        <div style={{ display: "grid", gridTemplateColumns: "140px 150px 130px 150px 80px 100px", background: "#F8F9FA", padding: "8px 12px", borderBottom: `1px solid ${COLORS.border}`, fontSize: 11, fontWeight: 600, color: COLORS.textMuted }}>
          <div>Mã</div><div>Loại tờ khai</div><div>Kỳ thuế</div><div>Công ty</div><div>Trạng thái</div><div></div>
        </div>
        {data.map((d, i) => (
          <div key={i} style={{ display: "grid", gridTemplateColumns: "140px 150px 130px 150px 80px 100px", padding: "10px 12px", borderBottom: `1px solid ${COLORS.border}`, fontSize: 12, alignItems: "center", background: i % 2 ? "#FAFBFC" : "#fff" }}>
            <div style={{ fontWeight: 600, color: COLORS.secondary }}>{d.id}</div>
            <div>{d.type}</div>
            <div>{d.period}</div>
            <div style={{ color: COLORS.textMuted }}>{d.company}</div>
            <div><StatusBadge status={d.status} /></div>
            <div><Btn variant="ghost" size="sm">Mở →</Btn></div>
          </div>
        ))}
      </div>
    </div>
  );
}

// ═══════════════════════════════════════
// SCREEN: Declaration Workspace
// ═══════════════════════════════════════
function DeclarationWorkspace({ mode = "draft" }) {
  const [showCompare, setShowCompare] = useState(false);
  const isDraft = mode === "draft";
  const isPending = mode === "pending";
  const isSubmitted = mode === "submitted";

  return (
    <div style={{ display: "flex", flexDirection: "column", height: "100%" }}>
      {/* Header Bar */}
      <div style={{ background: COLORS.surface, borderBottom: `1px solid ${COLORS.border}`, padding: "10px 16px" }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
          <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
            <span style={{ fontSize: 12, color: COLORS.textMuted, cursor: "pointer" }}>← Quay lại</span>
            <div>
              <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
                <span style={{ fontWeight: 700, fontSize: 15, color: COLORS.grayDark, fontFamily: "'IBM Plex Sans', sans-serif" }}>HTKK-2026-003</span>
                <StatusBadge status={mode === "draft" ? "Draft" : mode === "pending" ? "Pending" : "Submitted"} />
              </div>
              <div style={{ fontSize: 11, color: COLORS.textMuted, marginTop: 2 }}>
                GTGT 01/GTGT · Tháng 03/2026 · Công ty ABC · Lần đầu
              </div>
            </div>
          </div>

          {/* Save status */}
          <div style={{ display: "flex", alignItems: "center", gap: 6, fontSize: 11, color: COLORS.green }}>
            <span>●</span> Đã lưu
          </div>
        </div>

        {/* Action toolbar */}
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginTop: 10 }}>
          <div style={{ display: "flex", gap: 6 }}>
            <Btn variant={isDraft ? "primary" : "ghost"} size="sm" icon="📥" disabled={!isDraft}>Lấy dữ liệu</Btn>
            <Btn variant="ghost" size="sm" icon="🔄" disabled={!isDraft}>Lấy lại</Btn>
            <Btn variant="ghost" size="sm" icon="📋" onClick={() => setShowCompare(!showCompare)}>
              {showCompare ? "Tắt so sánh" : "So sánh với DL gốc"}
            </Btn>
            <Btn variant="ghost" size="sm" icon="⏪" disabled={isSubmitted}>Quay lại bản trước</Btn>
          </div>
          <div style={{ display: "flex", gap: 6 }}>
            <Btn variant="ghost" size="sm" icon="✓" disabled={isSubmitted}>Validate</Btn>
            {isDraft && <Btn variant="secondary" size="sm" icon="📤">Gửi duyệt</Btn>}
            {isPending && <Btn variant="success" size="sm" icon="🔒">Phê duyệt & Submit</Btn>}
            <Btn variant={isSubmitted ? "primary" : "ghost"} size="sm" icon="📄" disabled={!isSubmitted}>Xuất XML</Btn>
          </div>
        </div>
      </div>

      {/* Validate sync warning */}
      {isPending && (
        <div style={{ background: "#FDEDEC", borderBottom: `1px solid ${COLORS.red}30`, padding: "8px 16px", display: "flex", alignItems: "center", gap: 8, fontSize: 12 }}>
          <span>⚠️</span>
          <span><strong>validate_sync:</strong> Hóa đơn <strong>INV-2026-0142</strong> đã bị sửa lúc 14:30 hôm nay. </span>
          <Btn variant="danger" size="sm">Quay về Draft</Btn>
          <Btn variant="ghost" size="sm">Vẫn Submit (ghi nhận rủi ro)</Btn>
        </div>
      )}

      {/* Color legend */}
      <div style={{ padding: "6px 16px", borderBottom: `1px solid ${COLORS.border}`, background: "#FAFBFC" }}>
        <ColorLegend />
      </div>

      {/* Spreadsheet */}
      <div style={{ flex: 1, padding: 16, background: COLORS.bg, overflow: "auto" }}>
        <div style={{ background: COLORS.surface, borderRadius: 6, border: `1px solid ${COLORS.border}`, overflow: "hidden" }}>
          {/* Fake Excel title */}
          <div style={{ padding: "8px 12px", background: "#F8F9FA", borderBottom: `1px solid ${COLORS.border}`, fontSize: 12, fontWeight: 600, color: COLORS.primary }}>
            TỜ KHAI THUẾ GIÁ TRỊ GIA TĂNG (Mẫu số 01/GTGT)
          </div>
          <SpreadsheetGrid mode={mode} showCompare={showCompare} />
          <SheetTabs />
        </div>
      </div>

      {/* Progress bar for background job */}
      {isDraft && (
        <div style={{ padding: "6px 16px", borderTop: `1px solid ${COLORS.border}`, background: "#FAFBFC", display: "flex", alignItems: "center", gap: 10 }}>
          <span style={{ fontSize: 11, color: COLORS.textMuted }}>Đang insert phụ lục (2,340/5,000 dòng)...</span>
          <div style={{ flex: 1, height: 4, background: COLORS.grayLight, borderRadius: 2, maxWidth: 200 }}>
            <div style={{ width: "47%", height: "100%", background: COLORS.secondary, borderRadius: 2, transition: "width 0.3s" }} />
          </div>
          <span style={{ fontSize: 10, color: COLORS.textMuted }}>47%</span>
        </div>
      )}
    </div>
  );
}

// ═══════════════════════════════════════
// SCREEN: Auto-detect Review
// ═══════════════════════════════════════
function AutoDetectScreen() {
  const indicators = [
    { code: "[21]", cell: "D9", confidence: 0.95, label: "Thuế suất 0%" },
    { code: "[22]", cell: "D10", confidence: 0.92, label: "Thuế suất 5%" },
    { code: "[29]", cell: "D15", confidence: 0.97, label: "Doanh thu bán ra" },
    { code: "[30]", cell: "D16", confidence: 0.88, label: "Thuế GTGT bán ra" },
    { code: "[37]", cell: "D23", confidence: 0.72, label: "HH, DV mua vào" },
    { code: "[38]", cell: "D24", confidence: 0.65, label: "Thuế GTGT khấu trừ" },
    { code: "[40]", cell: "D26", confidence: 0.45, label: "Thuế còn phải nộp" },
  ];

  const getColor = (c) => c >= 0.9 ? COLORS.green : c >= 0.7 ? COLORS.yellow : COLORS.red;
  const getLabel = (c) => c >= 0.9 ? "Chắc chắn" : c >= 0.7 ? "Cần duyệt" : "Có thể sai";

  return (
    <div style={{ display: "flex", height: "100%" }}>
      {/* Main area */}
      <div style={{ flex: 1, display: "flex", flexDirection: "column" }}>
        <div style={{ padding: "12px 16px", borderBottom: `1px solid ${COLORS.border}`, display: "flex", justifyContent: "space-between", alignItems: "center" }}>
          <div>
            <h3 style={{ margin: 0, fontSize: 15, color: COLORS.grayDark, fontFamily: "'IBM Plex Sans', sans-serif" }}>Auto-detect Review</h3>
            <p style={{ margin: "2px 0 0", fontSize: 11, color: COLORS.textMuted }}>Template: GTGT 01/GTGT (TT80/2021) · Quét xong 42 chỉ tiêu</p>
          </div>
          <div style={{ display: "flex", gap: 6 }}>
            <Btn variant="ghost" size="sm">Chạy lại Auto-detect</Btn>
            <Btn variant="success" size="sm" icon="💾">Lưu Template</Btn>
          </div>
        </div>

        {/* Summary bar */}
        <div style={{ padding: "8px 16px", background: "#FAFBFC", borderBottom: `1px solid ${COLORS.border}`, display: "flex", gap: 16, fontSize: 12 }}>
          <span style={{ color: COLORS.green }}>● 35 chắc chắn</span>
          <span style={{ color: COLORS.yellow }}>● 5 cần duyệt</span>
          <span style={{ color: COLORS.red }}>● 2 có thể sai</span>
          <span style={{ color: COLORS.textMuted }}>| XSD yêu cầu: 42 · Đã map: 42 · Thiếu: 0</span>
        </div>

        {/* Spreadsheet preview */}
        <div style={{ flex: 1, padding: 16, background: COLORS.bg }}>
          <div style={{ background: COLORS.surface, borderRadius: 6, border: `1px solid ${COLORS.border}`, padding: 16, textAlign: "center", color: COLORS.textMuted, fontSize: 13 }}>
            <div style={{ fontSize: 32, marginBottom: 8 }}>📊</div>
            Vùng Univer render file .xlsx gốc<br />
            <span style={{ fontSize: 11 }}>Click ô trên Sidebar → Univer nhảy đến ô tương ứng. Click phải → "Re-assign Named Range"</span>
          </div>
        </div>
      </div>

      {/* Sidebar */}
      <div style={{ width: 280, borderLeft: `1px solid ${COLORS.border}`, background: COLORS.surface, display: "flex", flexDirection: "column" }}>
        <div style={{ padding: "10px 12px", borderBottom: `1px solid ${COLORS.border}`, fontWeight: 600, fontSize: 12, color: COLORS.grayDark }}>
          Chỉ tiêu đã nhận diện
          <div style={{ display: "flex", gap: 4, marginTop: 6 }}>
            <Btn variant="ghost" size="sm">Tất cả</Btn>
            <Btn variant="ghost" size="sm" style={{ color: COLORS.yellow }}>⚡ Cần duyệt (7)</Btn>
          </div>
        </div>
        <div style={{ flex: 1, overflow: "auto" }}>
          {indicators.map((ind, i) => (
            <div key={i} style={{
              padding: "8px 12px",
              borderBottom: `1px solid ${COLORS.border}`,
              cursor: "pointer",
              borderLeft: `3px solid ${getColor(ind.confidence)}`,
              background: ind.confidence < 0.7 ? "#FFF5F5" : "transparent",
            }}>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                <span style={{ fontWeight: 700, fontSize: 13, color: COLORS.primary }}>{ind.code}</span>
                <span style={{ fontSize: 10, color: getColor(ind.confidence), fontWeight: 600 }}>
                  {(ind.confidence * 100).toFixed(0)}% · {getLabel(ind.confidence)}
                </span>
              </div>
              <div style={{ fontSize: 11, color: COLORS.textMuted, marginTop: 2 }}>{ind.label}</div>
              <div style={{ fontSize: 10, color: COLORS.text, marginTop: 2 }}>→ Ô <strong>{ind.cell}</strong></div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

// ═══════════════════════════════════════
// SCREEN: KHBS Modal
// ═══════════════════════════════════════
function KHBSModal() {
  const diffs = [
    { code: "[37]", label: "HH, DV mua vào", old: "950,200,000", new_val: "980,500,000", diff: "+30,300,000", reason: "" },
    { code: "[38]", label: "Thuế GTGT khấu trừ", old: "95,020,000", new_val: "98,050,000", diff: "+3,030,000", reason: "" },
    { code: "[40]", label: "Thuế còn phải nộp", old: "29,980,000", new_val: "26,950,000", diff: "-3,030,000", reason: "" },
  ];
  const reasons = ["Sai hóa đơn", "Sót chứng từ", "Điều chỉnh giá", "Sai thuế suất", "Khác (nhập tay)"];

  return (
    <div style={{ padding: 20 }}>
      <div style={{ background: "rgba(0,0,0,0.3)", position: "absolute", inset: 0, borderRadius: 12 }} />
      <div style={{ position: "relative", background: COLORS.surface, borderRadius: 10, border: `1px solid ${COLORS.border}`, maxWidth: 620, margin: "10px auto", boxShadow: "0 8px 30px rgba(0,0,0,0.15)" }}>
        <div style={{ padding: "14px 20px", borderBottom: `1px solid ${COLORS.border}`, display: "flex", justifyContent: "space-between", alignItems: "center" }}>
          <div>
            <h3 style={{ margin: 0, fontSize: 15, color: COLORS.grayDark, fontFamily: "'IBM Plex Sans', sans-serif" }}>Giải trình Khai bổ sung (KHBS)</h3>
            <p style={{ margin: "2px 0 0", fontSize: 11, color: COLORS.textMuted }}>Bổ sung Lần 1 · So sánh với Tờ khai gốc HTKK-2026-001</p>
          </div>
          <span style={{ cursor: "pointer", fontSize: 18, color: COLORS.textMuted }}>✕</span>
        </div>

        <div style={{ padding: "12px 20px", maxHeight: 300, overflow: "auto" }}>
          <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 12 }}>
            <thead>
              <tr style={{ background: "#F8F9FA" }}>
                <th style={{ padding: "6px 8px", textAlign: "left", borderBottom: `1px solid ${COLORS.border}`, color: COLORS.textMuted, fontWeight: 600 }}>Chỉ tiêu</th>
                <th style={{ padding: "6px 8px", textAlign: "right", borderBottom: `1px solid ${COLORS.border}`, color: COLORS.textMuted, fontWeight: 600 }}>Giá trị cũ</th>
                <th style={{ padding: "6px 8px", textAlign: "right", borderBottom: `1px solid ${COLORS.border}`, color: COLORS.textMuted, fontWeight: 600 }}>Giá trị mới</th>
                <th style={{ padding: "6px 8px", textAlign: "right", borderBottom: `1px solid ${COLORS.border}`, color: COLORS.textMuted, fontWeight: 600 }}>Chênh lệch</th>
                <th style={{ padding: "6px 8px", textAlign: "left", borderBottom: `1px solid ${COLORS.border}`, color: COLORS.textMuted, fontWeight: 600 }}>Lý do</th>
              </tr>
            </thead>
            <tbody>
              {diffs.map((d, i) => (
                <tr key={i}>
                  <td style={{ padding: "8px", borderBottom: `1px solid ${COLORS.border}` }}>
                    <strong style={{ color: COLORS.primary }}>{d.code}</strong>
                    <div style={{ fontSize: 10, color: COLORS.textMuted }}>{d.label}</div>
                  </td>
                  <td style={{ padding: "8px", textAlign: "right", borderBottom: `1px solid ${COLORS.border}`, color: COLORS.textMuted }}>{d.old}</td>
                  <td style={{ padding: "8px", textAlign: "right", borderBottom: `1px solid ${COLORS.border}`, fontWeight: 600 }}>{d.new_val}</td>
                  <td style={{ padding: "8px", textAlign: "right", borderBottom: `1px solid ${COLORS.border}`, color: d.diff.startsWith("+") ? COLORS.green : COLORS.red, fontWeight: 600 }}>{d.diff}</td>
                  <td style={{ padding: "8px", borderBottom: `1px solid ${COLORS.border}` }}>
                    <select style={{ fontSize: 11, padding: "3px 6px", borderRadius: 4, border: `1px solid ${COLORS.border}`, width: "100%" }}>
                      <option value="">Chọn lý do...</option>
                      {reasons.map((r, j) => <option key={j}>{r}</option>)}
                    </select>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>

          <div style={{ marginTop: 10, padding: "8px 10px", background: "#FEF9E7", borderRadius: 6, fontSize: 11, color: COLORS.text }}>
            <strong>Tiền chậm nộp dự kiến:</strong> 3,030,000 × 0.03% × 15 ngày = <strong>13,635 VND</strong>
          </div>
        </div>

        <div style={{ padding: "12px 20px", borderTop: `1px solid ${COLORS.border}`, display: "flex", justifyContent: "flex-end", gap: 8 }}>
          <Btn variant="ghost">Hủy</Btn>
          <Btn variant="primary" icon="✓">Xác nhận & Điền vào PL 01/KHBS</Btn>
        </div>
      </div>
    </div>
  );
}

// ═══════════════════════════════════════
// SCREEN: Drill-down
// ═══════════════════════════════════════
function DrilldownPopup() {
  const invoices = [
    { id: "SINV-2026-0089", date: "05/03/2026", partner: "Công ty XYZ", amount: "450,000,000", tax: "45,000,000" },
    { id: "SINV-2026-0112", date: "12/03/2026", partner: "Công ty DEF", amount: "380,000,000", tax: "38,000,000" },
    { id: "SINV-2026-0145", date: "20/03/2026", partner: "Cửa hàng GHI", amount: "420,000,000", tax: "42,000,000" },
  ];
  return (
    <div style={{ padding: 20 }}>
      <div style={{ background: "rgba(0,0,0,0.3)", position: "absolute", inset: 0, borderRadius: 12 }} />
      <div style={{ position: "relative", background: COLORS.surface, borderRadius: 10, border: `1px solid ${COLORS.border}`, maxWidth: 580, margin: "20px auto", boxShadow: "0 8px 30px rgba(0,0,0,0.15)" }}>
        <div style={{ padding: "14px 20px", borderBottom: `1px solid ${COLORS.border}`, display: "flex", justifyContent: "space-between" }}>
          <div>
            <h3 style={{ margin: 0, fontSize: 14, color: COLORS.grayDark, fontFamily: "'IBM Plex Sans', sans-serif" }}>🔍 Chứng từ gốc — Chỉ tiêu [29]</h3>
            <p style={{ margin: "2px 0 0", fontSize: 11, color: COLORS.textMuted }}>Doanh thu hàng hóa, DV bán ra · Tổng: 1,250,000,000</p>
          </div>
          <span style={{ cursor: "pointer", fontSize: 18, color: COLORS.textMuted }}>✕</span>
        </div>
        <div style={{ padding: "0 20px 12px" }}>
          {invoices.map((inv, i) => (
            <div key={i} style={{ display: "flex", justifyContent: "space-between", alignItems: "center", padding: "10px 0", borderBottom: `1px solid ${COLORS.border}`, fontSize: 12 }}>
              <div>
                <span style={{ color: COLORS.secondary, fontWeight: 600, cursor: "pointer", textDecoration: "underline" }}>{inv.id}</span>
                <div style={{ fontSize: 10, color: COLORS.textMuted, marginTop: 2 }}>{inv.date} · {inv.partner}</div>
              </div>
              <div style={{ textAlign: "right" }}>
                <div style={{ fontWeight: 600 }}>{inv.amount}</div>
                <div style={{ fontSize: 10, color: COLORS.textMuted }}>VAT: {inv.tax}</div>
              </div>
            </div>
          ))}
        </div>
        <div style={{ padding: "10px 20px", borderTop: `1px solid ${COLORS.border}`, fontSize: 11, color: COLORS.textMuted }}>
          Tổng: 3 hóa đơn · Click mã hóa đơn để mở trong ERPNext
        </div>
      </div>
    </div>
  );
}

// ═══════════════════════════════════════
// SCREEN: Template Manager
// ═══════════════════════════════════════
function TemplateManagerScreen() {
  return (
    <div>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 16 }}>
        <div>
          <h2 style={{ margin: 0, fontSize: 18, color: COLORS.grayDark, fontFamily: "'IBM Plex Sans', sans-serif" }}>HTKK Template Manager</h2>
          <p style={{ margin: "2px 0 0", fontSize: 12, color: COLORS.textMuted }}>GTGT 01/GTGT · TT80/2021 · Active</p>
        </div>
        <div style={{ display: "flex", gap: 6 }}>
          <Btn variant="ghost" size="sm">Duplicate</Btn>
          <Btn variant="primary" size="sm" icon="💾">Lưu Template</Btn>
        </div>
      </div>

      {/* Tabs */}
      <div style={{ display: "flex", borderBottom: `2px solid ${COLORS.border}`, marginBottom: 16 }}>
        {["Thông tin chung", "Nền tảng", "Nguồn dữ liệu", "Giao diện & Mapping"].map((tab, i) => (
          <div key={i} style={{
            padding: "8px 16px",
            fontSize: 12,
            fontWeight: i === 1 ? 700 : 400,
            color: i === 1 ? COLORS.primary : COLORS.textMuted,
            borderBottom: i === 1 ? `2px solid ${COLORS.secondary}` : "none",
            cursor: "pointer",
            marginBottom: -2,
            fontFamily: "'IBM Plex Sans', sans-serif",
          }}>{tab}</div>
        ))}
      </div>

      {/* Foundation Tab content */}
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: 12, marginBottom: 16 }}>
        {[
          { label: "File XML (mẫu dữ liệu)", file: "01_GTGT_data.xml", icon: "📄" },
          { label: "File XSD (luật kiểm tra)", file: "01_GTGT_schema.xsd", icon: "📋" },
          { label: "File XLSX (layout gốc)", file: "01_GTGT_TT80.xlsx", icon: "📊" },
        ].map((f, i) => (
          <div key={i} style={{ border: `1px solid ${COLORS.border}`, borderRadius: 8, padding: 12 }}>
            <div style={{ fontSize: 11, color: COLORS.textMuted, marginBottom: 6 }}>{f.label}</div>
            <div style={{ display: "flex", alignItems: "center", gap: 6 }}>
              <span style={{ fontSize: 20 }}>{f.icon}</span>
              <span style={{ fontSize: 12, fontWeight: 600, color: COLORS.text }}>{f.file}</span>
              <Tag color={COLORS.green}>Uploaded</Tag>
            </div>
          </div>
        ))}
      </div>

      {/* Action buttons */}
      <div style={{ display: "flex", gap: 8, marginBottom: 16 }}>
        <Btn variant="secondary" icon="🔍">Parse Schema</Btn>
        <Btn variant="primary" icon="🤖">Auto-detect Indicators</Btn>
      </div>

      {/* Parse result */}
      <div style={{ border: `1px solid ${COLORS.border}`, borderRadius: 8, padding: 12 }}>
        <div style={{ fontSize: 12, fontWeight: 600, color: COLORS.grayDark, marginBottom: 8 }}>Kết quả Parse Schema</div>
        <div style={{ display: "flex", gap: 16, fontSize: 12 }}>
          <span>Fixed Nodes: <strong>42</strong></span>
          <span>Repeatable Nodes: <strong>3</strong> (PL01-1, PL01-2, PL01-KHBS)</span>
          <span style={{ color: COLORS.green }}>✓ Cross-check: 42/42 Named Ranges khớp XSD</span>
        </div>
      </div>
    </div>
  );
}

// ═══════════════════════════════════════
// SCREEN: Mapping Rule Manager
// ═══════════════════════════════════════
function MappingRuleScreen() {
  const [activeSource, setActiveSource] = useState("condition");
  const rules = [
    { code: "CHI_TIEU_29", type: "01/GTGT", source: "Condition Builder", ruleType: "Standard", company: "Tất cả", active: true },
    { code: "CHI_TIEU_30", type: "01/GTGT", source: "Condition Builder", ruleType: "Standard", company: "Tất cả", active: true },
    { code: "CHI_TIEU_37", type: "01/GTGT", source: "SQL Builder", ruleType: "Custom", company: "Công ty ABC", active: true },
    { code: "CHI_TIEU_38", type: "01/GTGT", source: "Python Whitelist", ruleType: "Standard", company: "Tất cả", active: true },
    { code: "CHI_TIEU_40", type: "01/GTGT", source: "Condition Builder", ruleType: "Custom", company: "Công ty ABC", active: false },
  ];
  const srcColor = { "Condition Builder": COLORS.green, "SQL Builder": COLORS.yellow, "Python Whitelist": "#8E44AD" };

  return (
    <div>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 12, padding: "12px 16px 0" }}>
        <div>
          <h2 style={{ margin: 0, fontSize: 18, color: COLORS.grayDark, fontFamily: "'IBM Plex Sans', sans-serif" }}>HTKK Mapping Rule</h2>
          <p style={{ margin: "2px 0 0", fontSize: 12, color: COLORS.textMuted }}>Quy tắc ánh xạ dữ liệu cho chỉ tiêu thuế</p>
        </div>
        <div style={{ display: "flex", gap: 6 }}>
          <Btn variant="ghost" size="sm">Nhân bản Standard Rule</Btn>
          <Btn icon="＋">Tạo Rule mới</Btn>
        </div>
      </div>

      {/* Filters */}
      <div style={{ display: "flex", gap: 8, padding: "8px 16px", fontSize: 11 }}>
        {["Loại TK: 01/GTGT", "Source: Tất cả", "Type: Tất cả", "Công ty: Tất cả"].map((f, i) => (
          <span key={i} style={{ background: COLORS.grayLight, padding: "3px 10px", borderRadius: 4, color: COLORS.text, cursor: "pointer" }}>{f} ▾</span>
        ))}
      </div>

      {/* Table */}
      <div style={{ margin: "0 16px", border: `1px solid ${COLORS.border}`, borderRadius: 8, overflow: "hidden" }}>
        <div style={{ display: "grid", gridTemplateColumns: "140px 100px 140px 90px 120px 60px", background: "#F8F9FA", padding: "8px 12px", borderBottom: `1px solid ${COLORS.border}`, fontSize: 11, fontWeight: 600, color: COLORS.textMuted }}>
          <div>Chỉ tiêu đích</div><div>Loại TK</div><div>Source Type</div><div>Rule Type</div><div>Công ty</div><div>Active</div>
        </div>
        {rules.map((r, i) => (
          <div key={i} style={{ display: "grid", gridTemplateColumns: "140px 100px 140px 90px 120px 60px", padding: "10px 12px", borderBottom: `1px solid ${COLORS.border}`, fontSize: 12, alignItems: "center", background: i % 2 ? "#FAFBFC" : "#fff", opacity: r.active ? 1 : 0.5 }}>
            <div style={{ fontWeight: 600, color: COLORS.primary }}>{r.code}</div>
            <div>{r.type}</div>
            <div><span style={{ background: srcColor[r.source] + "18", color: srcColor[r.source], padding: "1px 8px", borderRadius: 4, fontSize: 10, fontWeight: 600 }}>{r.source}</span></div>
            <div><span style={{ background: r.ruleType === "Custom" ? "#FEF9E7" : "#F4F6F7", color: r.ruleType === "Custom" ? COLORS.yellow : COLORS.gray, padding: "1px 8px", borderRadius: 4, fontSize: 10, fontWeight: 600 }}>{r.ruleType}</span></div>
            <div style={{ fontSize: 11, color: COLORS.textMuted }}>{r.company}</div>
            <div>{r.active ? "✓" : "✗"}</div>
          </div>
        ))}
      </div>

      {/* Source Type Preview */}
      <div style={{ margin: "16px", border: `1px solid ${COLORS.border}`, borderRadius: 8, overflow: "hidden" }}>
        <div style={{ padding: "10px 16px", background: "#F8F9FA", borderBottom: `1px solid ${COLORS.border}`, display: "flex", gap: 8 }}>
          {[["condition", "Condition Builder"], ["sql", "SQL Builder"], ["python", "Python Whitelist"]].map(([id, label]) => (
            <button key={id} onClick={() => setActiveSource(id)} style={{
              background: activeSource === id ? COLORS.primary : "transparent",
              color: activeSource === id ? "#fff" : COLORS.textMuted,
              border: `1px solid ${activeSource === id ? COLORS.primary : COLORS.border}`,
              padding: "4px 12px", borderRadius: 4, fontSize: 11, cursor: "pointer", fontFamily: "'IBM Plex Sans', sans-serif", fontWeight: 600
            }}>{label}</button>
          ))}
        </div>
        <div style={{ padding: 16, minHeight: 120 }}>
          {activeSource === "condition" && (
            <div>
              <div style={{ fontSize: 12, fontWeight: 600, marginBottom: 8, color: COLORS.grayDark }}>No-code · Dành cho Kế toán</div>
              <div style={{ display: "flex", gap: 8, alignItems: "center", flexWrap: "wrap" }}>
                <span style={{ fontSize: 11, color: COLORS.textMuted }}>Doctype:</span>
                <select style={{ fontSize: 11, padding: "4px 8px", borderRadius: 4, border: `1px solid ${COLORS.border}` }}><option>Sales Invoice</option></select>
                <span style={{ fontSize: 11, color: COLORS.textMuted }}>| Lọc:</span>
                <select style={{ fontSize: 11, padding: "4px 8px", borderRadius: 4, border: `1px solid ${COLORS.border}` }}><option>tax_rate</option></select>
                <select style={{ fontSize: 11, padding: "4px 8px", borderRadius: 4, border: `1px solid ${COLORS.border}` }}><option>=</option></select>
                <input style={{ fontSize: 11, padding: "4px 8px", borderRadius: 4, border: `1px solid ${COLORS.border}`, width: 60 }} defaultValue="10" />
                <Btn variant="ghost" size="sm">+ Thêm</Btn>
                <span style={{ fontSize: 11, color: COLORS.textMuted }}>| Aggregate:</span>
                <select style={{ fontSize: 11, padding: "4px 8px", borderRadius: 4, border: `1px solid ${COLORS.border}` }}><option>SUM(base_net_total)</option></select>
              </div>
              <div style={{ marginTop: 10, padding: "6px 10px", background: "#EAFAF1", borderRadius: 4, fontSize: 11, color: COLORS.green }}>Preview: 1,250,000,000</div>
            </div>
          )}
          {activeSource === "sql" && (
            <div>
              <div style={{ fontSize: 12, fontWeight: 600, marginBottom: 8, color: COLORS.grayDark }}>Low-code · Dành cho Admin/Implementer</div>
              <div style={{ background: "#2C3E50", borderRadius: 6, padding: 12, fontFamily: "monospace", fontSize: 11, color: "#ECF0F1", lineHeight: 1.6 }}>
                <span style={{ color: "#3498DB" }}>SELECT</span> <span style={{ color: "#E74C3C" }}>SUM</span>(si.base_net_total)<br/>
                <span style={{ color: "#3498DB" }}>FROM</span> `tabSales Invoice` si<br/>
                <span style={{ color: "#3498DB" }}>WHERE</span> si.posting_date <span style={{ color: "#3498DB" }}>BETWEEN</span> %(from)s <span style={{ color: "#3498DB" }}>AND</span> %(to)s<br/>
                <span style={{ color: "#3498DB" }}>AND</span> si.docstatus = 1
              </div>
              <div style={{ marginTop: 6, padding: "4px 8px", background: "#FEF9E7", borderRadius: 4, fontSize: 10, color: COLORS.yellow }}>⚠ Chỉ SELECT · Timeout 10s · Max 10k rows · Whitelist tables</div>
            </div>
          )}
          {activeSource === "python" && (
            <div>
              <div style={{ fontSize: 12, fontWeight: 600, marginBottom: 8, color: COLORS.grayDark }}>Pro-code · Dành cho Developer</div>
              <div style={{ display: "flex", gap: 8, alignItems: "center" }}>
                <span style={{ fontSize: 11, color: COLORS.textMuted }}>Hàm:</span>
                <input style={{ fontSize: 11, padding: "4px 8px", borderRadius: 4, border: `1px solid ${COLORS.border}`, width: 300, fontFamily: "monospace" }} defaultValue="custom_app.htkk.api.get_vat_allocation" />
              </div>
              <div style={{ marginTop: 8, padding: 8, background: "#F4F6F7", borderRadius: 4, fontSize: 11, color: COLORS.textMuted, fontFamily: "monospace" }}>
                """Tính phân bổ thuế GTGT cho HH,DV dùng chung."""<br/>
                Params: company, from_date, to_date, tax_rate
              </div>
            </div>
          )}
        </div>
        <div style={{ padding: "8px 16px", borderTop: `1px solid ${COLORS.border}`, display: "flex", justifyContent: "flex-end", gap: 6 }}>
          <Btn variant="ghost" size="sm" icon="▶">Test Rule</Btn>
          <Btn variant="primary" size="sm" icon="💾">Lưu Rule</Btn>
        </div>
      </div>
    </div>
  );
}

// ═══════════════════════════════════════
// SCREEN: Package Import Wizard
// ═══════════════════════════════════════
function PackageImportScreen() {
  const [step, setStep] = useState(2);
  const steps = ["Upload", "Kiểm tra", "Conflict", "Import"];

  return (
    <div style={{ padding: 20, maxWidth: 650, margin: "0 auto" }}>
      <h2 style={{ margin: "0 0 4px", fontSize: 18, color: COLORS.grayDark, fontFamily: "'IBM Plex Sans', sans-serif" }}>Import Template Package</h2>
      <p style={{ margin: "0 0 16px", fontSize: 12, color: COLORS.textMuted }}>Upload file .htkktpl để cài đặt mẫu tờ khai mới</p>

      {/* Steps */}
      <div style={{ display: "flex", gap: 4, marginBottom: 20 }}>
        {steps.map((s, i) => (
          <div key={i} style={{ flex: 1, textAlign: "center" }}>
            <div style={{
              width: 28, height: 28, borderRadius: 14, margin: "0 auto 4px",
              background: i <= step ? COLORS.primary : COLORS.grayLight,
              color: i <= step ? "#fff" : COLORS.gray,
              display: "flex", alignItems: "center", justifyContent: "center", fontSize: 12, fontWeight: 700
            }}>{i + 1}</div>
            <div style={{ fontSize: 10, color: i <= step ? COLORS.primary : COLORS.gray, fontWeight: i === step ? 700 : 400 }}>{s}</div>
          </div>
        ))}
      </div>

      {/* Step content */}
      <div style={{ border: `1px solid ${COLORS.border}`, borderRadius: 8, overflow: "hidden" }}>
        {/* Step 2: Compatibility */}
        <div style={{ padding: 16, borderBottom: `1px solid ${COLORS.border}` }}>
          <div style={{ fontSize: 12, fontWeight: 600, marginBottom: 10, color: COLORS.grayDark }}>📦 Package: GTGT_01_TT80_v2.htkktpl</div>
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 8, fontSize: 12 }}>
            <div style={{ padding: 8, background: "#F8F9FA", borderRadius: 4 }}>
              <div style={{ color: COLORS.textMuted, fontSize: 10 }}>Template</div>
              <div style={{ fontWeight: 600 }}>GTGT 01/GTGT · TT80/2021</div>
            </div>
            <div style={{ padding: 8, background: "#F8F9FA", borderRadius: 4 }}>
              <div style={{ color: COLORS.textMuted, fontSize: 10 }}>Standard Rules</div>
              <div style={{ fontWeight: 600 }}>42 rules</div>
            </div>
            <div style={{ padding: 8, background: "#EAFAF1", borderRadius: 4 }}>
              <div style={{ color: COLORS.textMuted, fontSize: 10 }}>Module version</div>
              <div style={{ fontWeight: 600, color: COLORS.green }}>✓ Tương thích (3.0 ≥ 3.0)</div>
            </div>
            <div style={{ padding: 8, background: "#F8F9FA", borderRadius: 4 }}>
              <div style={{ color: COLORS.textMuted, fontSize: 10 }}>Files đính kèm</div>
              <div style={{ fontWeight: 600 }}>3 files (xlsx, xml, xsd)</div>
            </div>
          </div>
        </div>

        {/* Step 3: Conflict check */}
        <div style={{ padding: 16 }}>
          <div style={{ fontSize: 12, fontWeight: 600, marginBottom: 8, color: COLORS.grayDark }}>Conflict Check</div>
          <div style={{ border: `1px solid ${COLORS.border}`, borderRadius: 6, overflow: "hidden", fontSize: 12 }}>
            <div style={{ display: "grid", gridTemplateColumns: "180px 100px 1fr", background: "#F8F9FA", padding: "6px 10px", borderBottom: `1px solid ${COLORS.border}`, fontSize: 11, fontWeight: 600, color: COLORS.textMuted }}>
              <div>Rule</div><div>Status</div><div>Action</div>
            </div>
            {[
              { name: "CHI_TIEU_29", status: "Mới", color: COLORS.green },
              { name: "CHI_TIEU_30", status: "Cập nhật", color: COLORS.secondary },
              { name: "CHI_TIEU_37", status: "Conflict", color: COLORS.yellow },
            ].map((r, i) => (
              <div key={i} style={{ display: "grid", gridTemplateColumns: "180px 100px 1fr", padding: "8px 10px", borderBottom: `1px solid ${COLORS.border}`, alignItems: "center", background: r.status === "Conflict" ? "#FEF9E7" : "transparent" }}>
                <div style={{ fontWeight: 600 }}>{r.name}</div>
                <div><span style={{ background: r.color + "18", color: r.color, padding: "1px 8px", borderRadius: 4, fontSize: 10, fontWeight: 600 }}>{r.status}</span></div>
                <div>{r.status === "Conflict" ? (
                  <div style={{ display: "flex", gap: 8, fontSize: 11 }}>
                    <label style={{ display: "flex", alignItems: "center", gap: 3, cursor: "pointer" }}>
                      <input type="radio" name={`conflict-${i}`} defaultChecked style={{ accentColor: COLORS.primary }} /> Giữ Custom
                    </label>
                    <label style={{ display: "flex", alignItems: "center", gap: 3, cursor: "pointer" }}>
                      <input type="radio" name={`conflict-${i}`} style={{ accentColor: COLORS.primary }} /> Ghi đè
                    </label>
                  </div>
                ) : (
                  <span style={{ fontSize: 11, color: COLORS.textMuted }}>Tự động</span>
                )}</div>
              </div>
            ))}
          </div>
          <div style={{ marginTop: 6, fontSize: 11, color: COLORS.textMuted }}>39 rules mới · 2 cập nhật · 1 conflict</div>
        </div>
      </div>

      <div style={{ display: "flex", justifyContent: "flex-end", gap: 8, marginTop: 12 }}>
        <Btn variant="ghost" onClick={() => setStep(Math.max(0, step - 1))}>← Quay lại</Btn>
        <Btn variant="primary" onClick={() => setStep(Math.min(3, step + 1))}>{step === 3 ? "Import ngay" : "Tiếp →"}</Btn>
      </div>
    </div>
  );
}

// ═══════════════════════════════════════
// MAIN APP
// ═══════════════════════════════════════
export default function HTKKWireframes() {
  const [activeScreen, setActiveScreen] = useState("declaration-draft");

  const renderScreen = () => {
    switch (activeScreen) {
      case "declaration-list": return <DeclarationListScreen />;
      case "declaration-draft": return <DeclarationWorkspace mode="draft" />;
      case "declaration-pending": return <DeclarationWorkspace mode="pending" />;
      case "declaration-submitted": return <DeclarationWorkspace mode="submitted" />;
      case "auto-detect": return <AutoDetectScreen />;
      case "khbs-modal": return <KHBSModal />;
      case "drilldown": return <DrilldownPopup />;
      case "template-manager": return <TemplateManagerScreen />;
      case "mapping-rule": return <MappingRuleScreen />;
      case "package-import": return <PackageImportScreen />;
      default: return <DeclarationWorkspace mode="draft" />;
    }
  };

  return (
    <div style={{ fontFamily: "'IBM Plex Sans', -apple-system, sans-serif", background: "#E8ECEF", height: "100vh", display: "flex", flexDirection: "column" }}>
      <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600;700&display=swap" rel="stylesheet" />

      {/* Screen selector */}
      <div style={{ background: COLORS.primary, padding: "8px 16px", display: "flex", alignItems: "center", gap: 8, overflowX: "auto" }}>
        <span style={{ color: "#ffffff90", fontSize: 11, fontWeight: 600, whiteSpace: "nowrap", marginRight: 4 }}>WIREFRAME:</span>
        {screens.map(s => (
          <button
            key={s.id}
            onClick={() => setActiveScreen(s.id)}
            style={{
              background: activeScreen === s.id ? "rgba(255,255,255,0.2)" : "transparent",
              color: activeScreen === s.id ? "#fff" : "#ffffff80",
              border: `1px solid ${activeScreen === s.id ? "rgba(255,255,255,0.3)" : "transparent"}`,
              padding: "4px 10px",
              borderRadius: 4,
              fontSize: 11,
              cursor: "pointer",
              whiteSpace: "nowrap",
              fontFamily: "'IBM Plex Sans', sans-serif",
              fontWeight: activeScreen === s.id ? 600 : 400,
            }}
          >{s.label}</button>
        ))}
      </div>

      {/* Screen content */}
      <div style={{ flex: 1, overflow: "auto", position: "relative" }}>
        <div style={{ background: COLORS.surface, margin: 12, borderRadius: 12, border: `1px solid ${COLORS.border}`, height: "calc(100% - 24px)", overflow: "auto", position: "relative" }}>
          {renderScreen()}
        </div>
      </div>
    </div>
  );
}
