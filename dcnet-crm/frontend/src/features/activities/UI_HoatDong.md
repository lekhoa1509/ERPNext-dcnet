# UI – Trang Hoạt động (HoatDong.vue)

## Cấu trúc layout tổng thể

```
screen (100vh, flex-col)
├── Topbar                          ← header toàn màn hình (50px)
└── main (flex-row, flex:1)
    ├── Sidebar (190px)             ← nav trái, active = "Hoạt động"
    └── hd-page (flex:1)
        └── hd-body (flex-row)
            ├── hd-list-panel (268px)   ← danh sách hoạt động
            ├── hd-detail (flex:1)      ← chi tiết hoạt động đang chọn
            └── hd-right (284px)        ← thông tin khách hàng liên quan
```

---

## Các pattern tái sử dụng

### Topbar & Sidebar
Được định nghĩa bằng `defineComponent` + `h()` ngay trong `<script setup>`, dùng lại y hệt ở mọi page. Chỉ thay điều kiện active trong Sidebar:
```ts
text === 'Hoạt động' ? 'active' : ''  // đổi thành tên menu của page tương ứng
```

### Label-value row (dùng ở quick fields và tab content)
```html
<div class="hd-qf-row">           <!-- hoặc hd-ct-row -->
  <span class="hd-qf-lbl">Tên trường</span>
  <span class="hd-qf-val">Giá trị</span>   <!-- hoặc hd-qf-link / hd-qf-priority -->
</div>
```
- `hd-qf-*` → quick fields (trên tabs, cột label 152px)
- `hd-ct-*` → tab content (cột label 160px, có border-bottom từng row)

### Status badge
```html
<!-- inline pill (header sub-row) -->
<span class="hd-det-status-pill">
  <span class="hd-det-status-dot"></span>Hoàn thành
</span>

<!-- filled badge (trong tab content) -->
<span class="hd-ct-status-done">Hoàn thành</span>
```

### Activity list badge
```html
<span class="hd-item-badge hd-badge-inprogress">Đang thực hiện</span>
<span class="hd-item-badge hd-badge-done">Hoàn thành</span>
```

### Tab bar pattern (dùng ở cả detail lẫn right panel)
```html
<div class="hd-tabs-bar">
  <button class="hd-tab hd-tab-active">Tab active</button>
  <button class="hd-tab">Tab khác</button>
  <div class="hd-tabs-end"><!-- icon buttons --></div>
</div>
```

---

## File: src/HoatDong.vue

```vue
<template>
  <div class="screen">
    <Topbar />
    <div class="main">
      <Sidebar />
      <div class="hd-page">
        <div class="hd-body">

          <!-- ===== LEFT: Activity list panel ===== -->
          <div class="hd-list-panel">
            <div class="hd-list-search">
              <Search :size="13" class="hd-search-ico" />
              <input class="hd-search-input" placeholder="Tìm kiếm" />
            </div>
            <div class="hd-list-scroll">
              <div
                v-for="(item, i) in activities" :key="i"
                class="hd-item"
                :class="{ 'hd-item-sel': i === selectedIdx }"
                @click="selectedIdx = i"
              >
                <div class="hd-item-row1">
                  <ClipboardList :size="13" class="hd-item-doc-ico" />
                  <span class="hd-item-title">{{ item.title }}</span>
                </div>
                <div class="hd-item-row2">
                  <span class="hd-item-person">{{ item.person }}</span>
                  <span class="hd-item-badge" :class="item.statusCls">{{ item.status }}</span>
                </div>
                <div class="hd-item-date">{{ item.date }}</div>
              </div>
            </div>
          </div>

          <!-- ===== CENTER: Detail panel ===== -->
          <div class="hd-detail">

            <!-- Header row: back + title + actions -->
            <div class="hd-det-head">
              <div class="hd-det-head-l">
                <button class="hd-det-back-btn"><ChevronLeft :size="19" /></button>
                <span class="hd-det-title">{{ currentAct.fullTitle }}</span>
              </div>
              <div class="hd-det-head-r">
                <button class="hd-det-edit-btn"><Pencil :size="13" /> Sửa</button>
                <button class="hd-det-more-btn"><MoreHorizontal :size="16" /></button>
                <button class="hd-det-cust-btn">
                  <span>NGÂN HÀNG THƯƠNG MẠI CỔ PHẦ...</span>
                  <ChevronDown :size="13" />
                </button>
              </div>
            </div>

            <!-- Sub-row: status + tag -->
            <div class="hd-det-sub">
              <span class="hd-det-status-pill">
                <span class="hd-det-status-dot"></span>Hoàn thành
              </span>
              <span class="hd-det-sep">•</span>
              <button class="hd-det-tag-btn"><Tag :size="12" /> Thêm thẻ</button>
            </div>

            <!-- Quick fields -->
            <div class="hd-qf">
              <div class="hd-qf-row">
                <span class="hd-qf-lbl">Mô tả</span>
                <span class="hd-qf-val">{{ currentAct.description }}</span>
              </div>
              <div class="hd-qf-row">
                <span class="hd-qf-lbl">Khách hàng</span>
                <a class="hd-qf-link">{{ currentAct.customer }}</a>
              </div>
              <div class="hd-qf-row">
                <span class="hd-qf-lbl">Hóa đơn</span>
                <a class="hd-qf-link">{{ currentAct.invoice }}</a>
              </div>
              <div class="hd-qf-row">
                <span class="hd-qf-lbl">Mức độ ưu tiên</span>
                <span class="hd-qf-priority">{{ currentAct.priority }}</span>
              </div>
              <div class="hd-qf-row">
                <span class="hd-qf-lbl">Loại nhiệm vụ</span>
                <span class="hd-qf-val hd-task-type">
                  <span class="hd-task-dot"></span>{{ currentAct.taskType }}
                </span>
              </div>
            </div>

            <!-- Tabs bar -->
            <div class="hd-tabs-bar">
              <button
                v-for="tab in tabs" :key="tab.id"
                class="hd-tab"
                :class="{ 'hd-tab-active': activeTab === tab.id }"
                @click="activeTab = tab.id"
              >{{ tab.label }}</button>
              <div class="hd-tabs-end">
                <button class="hd-tab-act-btn"><Plus :size="15" /></button>
                <button class="hd-tab-act-btn"><AlignJustify :size="15" /></button>
              </div>
            </div>

            <!-- Tab content -->
            <div class="hd-tab-body">
              <div v-if="activeTab === 'chitiet'" class="hd-ct-section">
                <h3 class="hd-ct-heading">Thông tin nhiệm vụ</h3>
                <div class="hd-ct-grid">
                  <div class="hd-ct-row">
                    <span class="hd-ct-lbl">Tiêu đề</span>
                    <span class="hd-ct-val">{{ currentAct.fullTitle }}</span>
                  </div>
                  <div class="hd-ct-row hd-ct-row-top">
                    <span class="hd-ct-lbl">Mô tả</span>
                    <span class="hd-ct-val">{{ currentAct.description }}</span>
                  </div>
                  <div class="hd-ct-row">
                    <span class="hd-ct-lbl">Khách hàng</span>
                    <a class="hd-ct-link">{{ currentAct.customer }}</a>
                  </div>
                  <div class="hd-ct-row">
                    <span class="hd-ct-lbl">Hóa đơn</span>
                    <a class="hd-ct-link">{{ currentAct.invoice }}</a>
                  </div>
                  <div class="hd-ct-row">
                    <span class="hd-ct-lbl">Người thực hiện</span>
                    <a class="hd-ct-link">{{ currentAct.assignee }}</a>
                  </div>
                  <div class="hd-ct-row">
                    <span class="hd-ct-lbl">Đơn vị</span>
                    <span class="hd-ct-val">{{ currentAct.department }}</span>
                  </div>
                  <div class="hd-ct-row">
                    <span class="hd-ct-lbl">Hạn hoàn thành</span>
                    <span class="hd-ct-val">{{ currentAct.dueDate }}&nbsp;&nbsp;&nbsp;{{ currentAct.dueTime }}</span>
                  </div>
                  <div class="hd-ct-row">
                    <span class="hd-ct-lbl">Mức độ ưu tiên</span>
                    <span class="hd-qf-priority">{{ currentAct.priority }}</span>
                  </div>
                  <div class="hd-ct-row">
                    <span class="hd-ct-lbl">Trạng thái</span>
                    <span class="hd-ct-status-done">Hoàn thành</span>
                  </div>
                  <div class="hd-ct-row hd-ct-row-top">
                    <span class="hd-ct-lbl">Người liên quan</span>
                    <div class="hd-ct-related">
                      <span v-for="p in currentAct.relatedPersons" :key="p" class="hd-ct-person">{{ p }}</span>
                    </div>
                  </div>
                </div>
              </div>
              <div v-else class="hd-tab-empty">Chưa có dữ liệu</div>
            </div>
          </div>

          <!-- ===== RIGHT: Customer info panel ===== -->
          <div class="hd-right">
            <div class="hd-rp-top">
              <button class="hd-rp-cust-dd">
                <span>NGÂN HÀNG THƯƠNG MẠI CỔ PHẦ...</span>
                <ChevronDown :size="13" />
              </button>
            </div>
            <div class="hd-rp-tabs">
              <button class="hd-rp-tab hd-rp-tab-active">Thông tin</button>
            </div>
            <div class="hd-rp-scroll">
              <a class="hd-rp-custname">{{ customer.name }}</a>
              <span class="hd-rp-custtype">Khách hàng</span>
              <div class="hd-rp-cust-fields">
                <div class="hd-rp-cf-row">
                  <span class="hd-rp-cfl">Mã số thuế</span>
                  <span class="hd-rp-cfv">{{ customer.taxCode }}</span>
                </div>
                <div class="hd-rp-cf-row">
                  <span class="hd-rp-cfl">Điện thoại</span>
                  <span class="hd-rp-cfv hd-rp-phone">
                    <Phone :size="12" />{{ customer.phone }}
                  </span>
                </div>
                <div class="hd-rp-cf-row">
                  <span class="hd-rp-cfl">Ngành nghề</span>
                  <span class="hd-rp-cfv"></span>
                </div>
                <div class="hd-rp-cf-row">
                  <span class="hd-rp-cfl">Doanh thu</span>
                  <span class="hd-rp-cfv"></span>
                </div>
              </div>
              <a class="hd-rp-more">Xem thêm</a>

              <div class="hd-rp-divider"></div>

              <div class="hd-rp-tasks-head">
                <span class="hd-rp-tasks-title">Công việc đang thực hiện</span>
                <button class="hd-rp-add-btn"><Plus :size="12" /> Thêm</button>
              </div>

              <div v-for="task in customer.tasks" :key="task.id" class="hd-rp-task">
                <CheckSquare :size="13" class="hd-rp-task-ico" />
                <div class="hd-rp-task-body">
                  <a class="hd-rp-task-title">{{ task.title }}</a>
                  <span class="hd-rp-task-date">{{ task.date }}</span>
                </div>
              </div>
            </div>
            <button class="hd-rp-edge-btn">›</button>
          </div>

        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, defineComponent, h } from 'vue'
import {
  Grid3X3, Rocket, Search, Settings, Clock3, UserPlus, MessageCircle, Bell,
  HelpCircle, MoreHorizontal, Home, CircleDollarSign, UserRound, Building2,
  Trophy, FileText, Box, Activity, HeartHandshake, Menu, Bot,
  ChevronLeft, ChevronDown, Pencil, Tag, Plus, AlignJustify,
  ClipboardList, Phone, CheckSquare, ChevronsLeft,
} from 'lucide-vue-next'

// ---- Sidebar menu ----
const menuItems: [any, string][] = [
  [Bot, 'Trung tâm AI'],
  [Home, 'Bàn làm việc'],
  [CircleDollarSign, 'Tiềm năng'],
  [UserRound, 'Liên hệ'],
  [Building2, 'Khách hàng'],
  [Trophy, 'Cơ hội'],
  [FileText, 'Báo giá'],
  [Box, 'Đơn hàng'],
  [Activity, 'Hoạt động'],
  [HeartHandshake, 'Thẻ chăm sóc'],
  [Menu, 'Tất cả'],
]

// ---- Shared layout components ----
const Topbar = defineComponent({
  setup: () => () => h('header', { class: 'topbar' }, [
    h('div', { class: 'top-left' }, [
      h(Grid3X3, { size: 20, class: 'muted' }),
      h('div', { class: 'logo' }, [h(Rocket, { size: 18 }), 'CRM']),
    ]),
    h('div', { class: 'search' }, [
      h(Search, { size: 16, class: 'search-icon' }),
      h('span', { style: 'color:#9aa4b8;font-size:13px' }, 'Tìm kiếm tiềm năng, liên hệ, khách hàng'),
    ]),
    h('div', { class: 'topbar-icons' }, [
      ...[Settings, Clock3, UserPlus, MessageCircle].map((I: any) =>
        h('div', { class: 'ico-wrap' }, [h(I, { size: 19, class: 'muted' })]),
      ),
      h('div', { class: 'ico-wrap notif-wrap' }, [
        h(Bell, { size: 19, class: 'muted' }),
        h('span', { class: 'badge' }, '23'),
      ]),
      ...[HelpCircle, MoreHorizontal].map((I: any) =>
        h('div', { class: 'ico-wrap' }, [h(I, { size: 19, class: 'muted' })]),
      ),
      h('div', { class: 'avatar' }, 'K'),
    ]),
  ]),
})

const Sidebar = defineComponent({
  setup: () => () => h('nav', { class: 'sidebar' }, [
    ...menuItems.map(([I, text]: [any, string]) =>
      h('div', { class: ['nav-item', text === 'Hoạt động' ? 'active' : ''] }, [
        h(I, { size: 16 }), h('span', text),
      ]),
    ),
    h('div', { style: 'margin-top:auto;padding-top:10px;border-top:1px solid #e5e9f0' }, [
      h('button', { class: 'nav-item', style: 'width:100%;border:none;background:none;justify-content:center' }, [
        h(ChevronsLeft, { size: 17, class: 'muted' }),
      ]),
    ]),
  ]),
})

// ---- Activity data ----
interface Activity {
  title: string
  person: string
  status: string
  statusCls: string
  date: string
  fullTitle: string
  description: string
  customer: string
  invoice: string
  priority: string
  taskType: string
  assignee: string
  department: string
  dueDate: string
  dueTime: string
  relatedPersons: string[]
}

const activities: Activity[] = [
  {
    title: '20/06/2026 - Đề nghị xuất hóa đơn - 1...',
    person: 'Quách Lệ Vân (01010052)',
    status: 'Đang thực hiện',
    statusCls: 'hd-badge-inprogress',
    date: '21/06/2026',
    fullTitle: '20/06/2026 - Đề nghị xuất hóa đơn - 1 HĐ 060226/HĐDV/DCNET-BIDV',
    description: 'Dear chị Vân, Nhờ chị xuất hóa đơn cho kh như số ĐNXHĐ dưới đây: XUẤT NGÀY 20/06/026 GIÚP EM',
    customer: 'NGÂN HÀNG THƯƠNG MẠI CỔ PHẦN ĐẦU TƯ VÀ PHÁT TRIỂN VIỆT NAM - CHI NHÁNH ĐỒNG NAI',
    invoice: 'ĐNXHĐ0002894',
    priority: 'Cao',
    taskType: 'Đề nghị xuất hóa đơn',
    assignee: 'Quách Lệ Vân (01010052)',
    department: 'Kế Toán',
    dueDate: '21/06/2026',
    dueTime: '13:56',
    relatedPersons: ['Chung Mỹ Quân (01010074)', 'Lê Thị Hồng (01010075)', 'Dương Đại Sơn (01010031)', 'Lâm Thị Liễu (01010005)'],
  },
  {
    title: '18/06/2026 - Đề nghị xuất hóa đơn - PL0...',
    person: 'Quách Lệ Vân (01010052)',
    status: 'Hoàn thành',
    statusCls: 'hd-badge-done',
    date: '20/06/2026',
    fullTitle: '18/06/2026 - Đề nghị xuất hóa đơn - PL01 HĐ 060226/HĐDV/DCNET-BIDV.ĐONGNAI - NGÂN HÀNG THƯƠNG MẠI CỔ PHẦN...',
    description: 'Dear chị Vân, Nhờ chị xuất hóa đơn cho kh như số ĐNXHĐ dưới đây: XUẤT NGÀY 20/06/026 GIÚP EM',
    customer: 'NGÂN HÀNG THƯƠNG MẠI CỔ PHẦN ĐẦU TƯ VÀ PHÁT TRIỂN VIỆT NAM - CHI NHÁNH ĐỒNG NAI',
    invoice: 'ĐNXHĐ0002894',
    priority: 'Cao',
    taskType: 'Đề nghị xuất hóa đơn',
    assignee: 'Quách Lệ Vân (01010052)',
    department: 'Kế Toán',
    dueDate: '20/06/2026',
    dueTime: '13:56',
    relatedPersons: ['Chung Mỹ Quân (01010074)', 'Lê Thị Hồng (01010075)', 'Dương Đại Sơn (01010031)', 'Lâm Thị Liễu (01010005)'],
  },
  {
    title: '30/06/2026 - Nhắc cước đến hạn - CÔ...',
    person: 'Võ Thị Cẩm Xuyên (0101...)',
    status: 'Đang thực hiện',
    statusCls: 'hd-badge-inprogress',
    date: '22/06/2026',
    fullTitle: '30/06/2026 - Nhắc cước đến hạn - CÔNG TY CỔ PHẦN VIỄN THÔNG FPT',
    description: 'Nhắc cước đến hạn',
    customer: 'CÔNG TY CỔ PHẦN VIỄN THÔNG FPT',
    invoice: '',
    priority: 'Bình thường',
    taskType: 'Nhắc cước đến hạn',
    assignee: 'Võ Thị Cẩm Xuyên (01010)',
    department: 'Kinh doanh',
    dueDate: '30/06/2026',
    dueTime: '09:00',
    relatedPersons: [],
  },
  // ... thêm items tương tự item 3
]

const selectedIdx = ref(1)
const currentAct = computed(() => activities[selectedIdx.value])

// ---- Tabs ----
const tabs = [
  { id: 'chitiet', label: 'Thông tin chi tiết' },
  { id: 'tailieu', label: 'Tài liệu đính kèm' },
  { id: 'noidung', label: 'Nội dung trao đổi' },
  { id: 'ghichu', label: 'Ghi chú' },
]
const activeTab = ref('chitiet')

// ---- Customer info ----
const customer = {
  name: 'NGÂN HÀNG THƯƠNG MẠI CỔ PHẦN ĐẦU TƯ VÀ PHÁT TRIỂN VIỆT NAM - CHI NHÁNH ĐỒNG NAI',
  taxCode: '0100150619-043',
  phone: '02513842729',
  tasks: [
    {
      id: 1,
      title: 'Nhân viên Kinh doanh chốt với KH ngày nghiệm thu đơn hàng TKDV.260125/BIDV Đồng Nai/MPLS 30M',
      date: '27/03/2026',
    },
    {
      id: 2,
      title: '30/06/2026 - Nhắc cước đến hạn - NGÂN HÀNG THƯƠNG MẠI CỔ PHẦN ĐẦU TƯ VÀ PHÁT TRIỂN VIỆT NAM - CHI NHÁNH ĐỒNG NAI - ĐNXHĐ0002894',
      date: '22/06/2026',
    },
  ],
}
</script>
```

---

## CSS (phần `/* ===== HOAT DONG PAGE ===== */` trong style.css)

```css
/* ===== HOAT DONG PAGE ===== */
.hd-page { flex: 1; min-width: 0; display: flex; flex-direction: column; overflow: hidden; background: #fff; }
.hd-body { flex: 1; display: flex; overflow: hidden; }

/* ---- Activity list panel ---- */
.hd-list-panel {
  width: 268px; min-width: 268px;
  border-right: 1px solid #e5e9f0;
  display: flex; flex-direction: column;
  overflow: hidden;
}
.hd-list-search {
  height: 44px; min-height: 44px;
  display: flex; align-items: center; gap: 7px;
  padding: 0 12px;
  border-bottom: 1px solid #e5e9f0;
  flex-shrink: 0;
}
.hd-search-ico { color: #9aa4b8; flex-shrink: 0; }
.hd-search-input {
  flex: 1; border: none; outline: none;
  font-size: 13px; color: #374151; font-family: inherit;
  background: transparent;
}
.hd-search-input::placeholder { color: #9aa4b8; }
.hd-list-scroll { flex: 1; overflow-y: auto; }
.hd-item {
  padding: 10px 12px;
  border-bottom: 1px solid #f0f3f8;
  cursor: pointer;
  border-left: 3px solid transparent;
}
.hd-item:hover { background: #fafbfc; }
.hd-item-sel { background: #fff5f0 !important; border-left-color: #f97316; }
.hd-item-row1 {
  display: flex; align-items: flex-start; gap: 6px;
  margin-bottom: 5px;
}
.hd-item-doc-ico { color: #6b7280; flex-shrink: 0; margin-top: 1px; }
.hd-item-title {
  font-size: 12.5px; font-weight: 600; color: #111827;
  overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
  flex: 1; min-width: 0;
}
.hd-item-row2 {
  display: flex; align-items: center; gap: 6px; margin-bottom: 4px;
  flex-wrap: wrap;
}
.hd-item-person { font-size: 12px; color: #6b7280; }
.hd-item-badge {
  font-size: 11px; font-weight: 600;
  border-radius: 4px; padding: 1px 6px;
}
.hd-badge-inprogress { color: #2563eb; background: #eff6ff; }
.hd-badge-done { color: #16a34a; background: #f0fdf4; }
.hd-item-date { font-size: 12px; color: #9ca3af; }

/* ---- Detail panel ---- */
.hd-detail {
  flex: 1; min-width: 0;
  display: flex; flex-direction: column;
  border-right: 1px solid #e5e9f0;
  overflow: hidden;
}

/* Header row */
.hd-det-head {
  display: flex; align-items: center; justify-content: space-between;
  padding: 12px 16px 0;
  gap: 8px;
  flex-shrink: 0;
}
.hd-det-head-l { display: flex; align-items: center; gap: 8px; flex: 1; min-width: 0; }
.hd-det-back-btn {
  width: 28px; height: 28px; border: none; background: transparent;
  display: grid; place-items: center; color: #374151;
  border-radius: 6px; flex-shrink: 0; cursor: pointer;
}
.hd-det-back-btn:hover { background: #f3f4f6; }
.hd-det-title {
  font-size: 13.5px; font-weight: 700; color: #0f172a;
  overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
  flex: 1; min-width: 0;
}
.hd-det-head-r { display: flex; align-items: center; gap: 6px; flex-shrink: 0; }
.hd-det-edit-btn {
  height: 30px; padding: 0 10px;
  border: 1px solid #dde3ef; background: #fff;
  border-radius: 6px; font-size: 12.5px; font-weight: 600; color: #374151;
  display: flex; align-items: center; gap: 5px; cursor: pointer;
}
.hd-det-edit-btn:hover { background: #f7f8fc; }
.hd-det-more-btn {
  width: 30px; height: 30px;
  border: 1px solid #dde3ef; background: #fff;
  border-radius: 6px; display: grid; place-items: center;
  color: #374151; cursor: pointer;
}
.hd-det-more-btn:hover { background: #f7f8fc; }
.hd-det-cust-btn {
  height: 30px; padding: 0 10px;
  border: 1px solid #dde3ef; background: #fff;
  border-radius: 6px; font-size: 12px; font-weight: 600; color: #374151;
  display: flex; align-items: center; gap: 5px; cursor: pointer;
  max-width: 230px;
}
.hd-det-cust-btn span { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.hd-det-cust-btn:hover { background: #f7f8fc; }

/* Status sub-row */
.hd-det-sub {
  display: flex; align-items: center; gap: 8px;
  padding: 7px 16px 10px;
  flex-shrink: 0;
}
.hd-det-status-pill {
  display: inline-flex; align-items: center; gap: 5px;
  font-size: 12.5px; font-weight: 600; color: #16a34a;
}
.hd-det-status-dot {
  width: 8px; height: 8px; border-radius: 50%; background: #16a34a; flex-shrink: 0;
}
.hd-det-sep { color: #d1d5db; font-size: 16px; }
.hd-det-tag-btn {
  display: inline-flex; align-items: center; gap: 4px;
  border: none; background: transparent;
  font-size: 12.5px; font-weight: 600; color: #3b5bdb;
  cursor: pointer; padding: 0; font-family: inherit;
}
.hd-det-tag-btn:hover { text-decoration: underline; }

/* Quick fields */
.hd-qf {
  padding: 4px 16px 12px;
  flex-shrink: 0;
  border-bottom: 1px solid #e8edf4;
}
.hd-qf-row {
  display: grid; grid-template-columns: 152px 1fr;
  min-height: 30px; align-items: center;
  gap: 8px;
}
.hd-qf-lbl { font-size: 13px; color: #6b7280; }
.hd-qf-val { font-size: 13px; color: #111827; font-weight: 500; }
.hd-qf-link {
  font-size: 13px; color: #2563eb; font-weight: 500; cursor: pointer;
  overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
}
.hd-qf-link:hover { text-decoration: underline; }
.hd-qf-priority { font-size: 13px; color: #dc2626; font-weight: 600; }
.hd-task-type { display: flex; align-items: center; gap: 5px; }
.hd-task-dot {
  display: inline-block; width: 7px; height: 7px;
  border-radius: 50%; background: #374151; flex-shrink: 0;
}

/* Tabs bar */
.hd-tabs-bar {
  display: flex; align-items: flex-end;
  height: 44px; min-height: 44px;
  padding: 0 16px;
  border-bottom: 1px solid #e5e9f0;
  flex-shrink: 0;
  overflow-x: auto;
}
.hd-tabs-bar::-webkit-scrollbar { display: none; }
.hd-tab {
  height: 44px; padding: 0 14px 10px;
  border: none; background: transparent;
  font-size: 13px; font-weight: 600; color: #6b7280;
  white-space: nowrap; cursor: pointer; position: relative;
  font-family: inherit;
}
.hd-tab:hover { color: #374151; }
.hd-tab-active { color: #3b5bdb; }
.hd-tab-active::after {
  content: ''; position: absolute; bottom: 0; left: 10px; right: 10px;
  height: 2.5px; background: #3b5bdb; border-radius: 2px;
}
.hd-tabs-end {
  margin-left: auto; display: flex; align-items: center; gap: 2px; padding-bottom: 8px;
}
.hd-tab-act-btn {
  width: 28px; height: 28px;
  border: none; background: transparent;
  display: grid; place-items: center;
  color: #6b7280; border-radius: 5px; cursor: pointer;
}
.hd-tab-act-btn:hover { background: #f3f4f6; color: #374151; }

/* Tab content */
.hd-tab-body { flex: 1; overflow-y: auto; padding: 16px; }
.hd-ct-heading { font-size: 14px; font-weight: 700; color: #111827; margin-bottom: 12px; }
.hd-ct-grid { display: flex; flex-direction: column; }
.hd-ct-row {
  display: grid; grid-template-columns: 160px 1fr;
  min-height: 36px; align-items: center;
  border-bottom: 1px solid #f0f3f8;
  gap: 8px; padding: 4px 0;
}
.hd-ct-row:last-child { border-bottom: none; }
.hd-ct-row-top { align-items: start; padding-top: 8px; }
.hd-ct-lbl { font-size: 13px; color: #6b7280; }
.hd-ct-val { font-size: 13px; color: #111827; font-weight: 500; line-height: 1.5; }
.hd-ct-link { font-size: 13px; color: #2563eb; font-weight: 500; cursor: pointer; }
.hd-ct-link:hover { text-decoration: underline; }
.hd-ct-status-done {
  display: inline-flex; align-items: center;
  background: #dcfce7; color: #16a34a;
  border-radius: 6px; padding: 3px 12px;
  font-size: 12.5px; font-weight: 700;
}
.hd-ct-related {
  display: grid; grid-template-columns: 1fr 1fr;
  gap: 4px 12px; padding: 4px 0;
}
.hd-ct-person { font-size: 13px; color: #374151; }
.hd-tab-empty {
  display: flex; align-items: center; justify-content: center;
  height: 120px; color: #9ca3af; font-size: 13px;
}

/* ---- Right customer panel ---- */
.hd-right {
  width: 284px; min-width: 284px;
  display: flex; flex-direction: column;
  overflow: hidden;
  position: relative;
}
.hd-rp-top { padding: 10px 12px 0; flex-shrink: 0; }
.hd-rp-cust-dd {
  width: 100%; height: 32px;
  border: 1px solid #dde3ef; background: #fff;
  border-radius: 6px; padding: 0 10px;
  display: flex; align-items: center; justify-content: space-between;
  font-size: 12px; font-weight: 600; color: #374151;
  cursor: pointer; gap: 6px; font-family: inherit;
}
.hd-rp-cust-dd span { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; flex: 1; }
.hd-rp-cust-dd:hover { background: #f7f8fc; }
.hd-rp-tabs {
  display: flex; padding: 6px 12px 0;
  border-bottom: 1px solid #e5e9f0;
  flex-shrink: 0;
}
.hd-rp-tab {
  height: 34px; padding: 0 10px 10px;
  border: none; background: transparent;
  font-size: 13px; font-weight: 600; color: #6b7280;
  cursor: pointer; position: relative; font-family: inherit;
}
.hd-rp-tab-active { color: #3b5bdb; }
.hd-rp-tab-active::after {
  content: ''; position: absolute; bottom: 0; left: 6px; right: 6px;
  height: 2.5px; background: #3b5bdb; border-radius: 2px;
}
.hd-rp-scroll {
  flex: 1; overflow-y: auto;
  padding: 12px 14px;
  display: flex; flex-direction: column;
}
.hd-rp-custname {
  font-size: 13px; font-weight: 700; color: #2563eb;
  cursor: pointer; line-height: 1.5; margin-bottom: 2px; display: block;
}
.hd-rp-custname:hover { text-decoration: underline; }
.hd-rp-custtype { font-size: 12px; color: #6b7280; margin-bottom: 12px; display: block; }
.hd-rp-cust-fields { display: flex; flex-direction: column; margin-bottom: 8px; }
.hd-rp-cf-row {
  display: grid; grid-template-columns: 92px 1fr;
  min-height: 28px; align-items: center;
  font-size: 12.5px;
  border-bottom: 1px solid #f7f8fc;
}
.hd-rp-cf-row:last-child { border-bottom: none; }
.hd-rp-cfl { color: #6b7280; }
.hd-rp-cfv { color: #111827; font-weight: 500; }
.hd-rp-phone { display: flex; align-items: center; gap: 4px; color: #2563eb; }
.hd-rp-more {
  font-size: 12.5px; color: #2563eb; font-weight: 600;
  cursor: pointer; margin-bottom: 12px;
}
.hd-rp-more:hover { text-decoration: underline; }
.hd-rp-divider { height: 1px; background: #e5e9f0; margin: 0 -14px 12px; }
.hd-rp-tasks-head {
  display: flex; align-items: center; justify-content: space-between;
  margin-bottom: 10px;
}
.hd-rp-tasks-title { font-size: 13px; font-weight: 700; color: #111827; }
.hd-rp-add-btn {
  height: 26px; padding: 0 8px;
  border: 1px solid #dde3ef; background: #fff;
  border-radius: 5px; font-size: 12px; font-weight: 600; color: #374151;
  display: flex; align-items: center; gap: 3px; cursor: pointer; font-family: inherit;
}
.hd-rp-add-btn:hover { background: #f7f8fc; }
.hd-rp-task {
  display: flex; gap: 8px; align-items: flex-start;
  margin-bottom: 12px;
}
.hd-rp-task-ico { color: #3b5bdb; flex-shrink: 0; margin-top: 2px; }
.hd-rp-task-body { flex: 1; min-width: 0; }
.hd-rp-task-title {
  font-size: 12.5px; color: #2563eb; font-weight: 500;
  cursor: pointer; display: block; margin-bottom: 3px; line-height: 1.4;
}
.hd-rp-task-title:hover { text-decoration: underline; }
.hd-rp-task-date { font-size: 12px; color: #9ca3af; }
.hd-rp-edge-btn {
  position: absolute; right: 0; top: 50%; transform: translateY(-50%);
  width: 14px; height: 36px;
  border: none; background: #1d6cf6; color: #fff;
  border-radius: 6px 0 0 6px;
  display: grid; place-items: center;
  font-size: 14px; cursor: pointer; z-index: 5;
}
```
