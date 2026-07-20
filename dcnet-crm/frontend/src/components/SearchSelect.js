/**
 * Searchable dropdown component for CRM forms.
 * Replaces <select> with a filterable list panel.
 *
 * The panel is teleported to <body> and positioned with `position: fixed`
 * so it never gets clipped by overflow containers (e.g. scrollable tables).
 *
 * Props:
 *   modelValue   - v-model binding (string)
 *   options      - array of objects (each must have at least the key matching valueKey)
 *   valueKey     - key used as the stored value       (default: 'name')
 *   labelKey     - key used as the display label      (default: 'name')
 *   subKey       - key for secondary line (optional)  (default: '')
 *   metaKeys     - array of keys joined by " · " on line 2 (optional, default: [])
 *   descKey      - key for a third muted line (optional, default: '')
 *   addLabel     - if set, shows a "+ {addLabel}" footer that emits 'add'
 *   placeholder  - shown when nothing selected        (default: '- Không chọn -')
 */
const MAX_RENDER = 80;

export const SearchSelect = {
  template: `
    <div class="ss-wrap" ref="wrap">
      <button type="button" class="ss-trigger" @click.stop="toggle" :class="{open: open, empty: !modelValue}">
        <span class="ss-val">{{ displayLabel }}</span>
        <svg class="ss-caret" width="12" height="7" viewBox="0 0 12 7" fill="none">
          <path d="M1 1l5 5 5-5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </button>
      <teleport to="body">
        <div v-if="open" class="ss-panel" :class="{ 'ss-panel-rich': rich }" :style="panelStyle" ref="panel">
          <div class="ss-search-row">
            <input ref="inp" v-model="q" class="ss-inp" placeholder="Tìm kiếm..." @keydown.esc.prevent="close" @keydown.enter.prevent="pickFirst" @click.stop>
            <svg class="ss-search-ico" width="15" height="15" viewBox="0 0 24 24" fill="none"><circle cx="11" cy="11" r="7" stroke="currentColor" stroke-width="1.8"/><path d="m20 20-3.5-3.5" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>
          </div>
          <ul class="ss-list" @click.stop>
            <li class="ss-opt ss-opt-none" @mousedown.prevent="pick('')">{{ placeholder }}</li>
            <li
              v-for="opt in shown"
              :key="getVal(opt)"
              class="ss-opt"
              :class="{ active: getVal(opt) === modelValue }"
              @mousedown.prevent="pick(getVal(opt))"
            >
              <span class="ss-opt-label">{{ getLabel(opt) }}</span>
              <span v-if="metaLine(opt)" class="ss-opt-meta">{{ metaLine(opt) }}</span>
              <span v-else-if="subKey && opt[subKey]" class="ss-opt-sub">{{ opt[subKey] }}</span>
              <span v-if="descKey && opt[descKey]" class="ss-opt-desc">{{ opt[descKey] }}</span>
            </li>
            <li v-if="!filtered.length" class="ss-opt ss-opt-empty">Không tìm thấy</li>
            <li v-else-if="filtered.length > shown.length" class="ss-opt ss-opt-more">Còn {{ filtered.length - shown.length }} kết quả — gõ để lọc thêm…</li>
          </ul>
          <button v-if="addLabel" type="button" class="ss-add" @mousedown.prevent="onAdd">
            <span class="ss-add-plus">＋</span> {{ addLabel }}
          </button>
        </div>
      </teleport>
    </div>
  `,
  props: {
    modelValue: { type: String, default: "" },
    options: { type: Array, default: () => [] },
    valueKey: { type: String, default: "name" },
    labelKey: { type: String, default: "name" },
    subKey: { type: String, default: "" },
    metaKeys: { type: Array, default: () => [] },
    descKey: { type: String, default: "" },
    addLabel: { type: String, default: "" },
    placeholder: { type: String, default: "- Không chọn -" },
  },
  emits: ["update:modelValue", "add"],
  data() {
    return { open: false, q: "", panelStyle: {} };
  },
  computed: {
    rich() {
      return (this.metaKeys && this.metaKeys.length) || !!this.descKey;
    },
    displayLabel() {
      if (!this.modelValue) return this.placeholder;
      const opt = (this.options || []).find((o) => this.getVal(o) === this.modelValue);
      return opt ? this.getLabel(opt) : this.modelValue;
    },
    filtered() {
      const q = (this.q || "").toLowerCase().trim();
      if (!q) return this.options || [];
      return (this.options || []).filter((o) => {
        const hay = [
          this.getLabel(o),
          this.getVal(o),
          this.subKey ? o[this.subKey] : "",
          this.descKey ? o[this.descKey] : "",
          ...(this.metaKeys || []).map((k) => o[k]),
        ]
          .filter(Boolean)
          .join(" ")
          .toLowerCase();
        return hay.includes(q);
      });
    },
    shown() {
      return this.filtered.slice(0, MAX_RENDER);
    },
  },
  methods: {
    getVal(opt) {
      return typeof opt === "string" ? opt : (opt[this.valueKey] || "");
    },
    getLabel(opt) {
      return typeof opt === "string" ? opt : (opt[this.labelKey] || opt[this.valueKey] || "");
    },
    metaLine(opt) {
      if (typeof opt === "string" || !this.metaKeys || !this.metaKeys.length) return "";
      return this.metaKeys.map((k) => opt[k]).filter(Boolean).join(" · ");
    },
    onAdd() {
      this.close();
      this.$emit("add");
    },
    toggle() {
      this.open = !this.open;
      if (this.open) {
        this.$nextTick(() => {
          this.updatePosition();
          this.$refs.inp?.focus();
          this.q = "";
        });
        window.addEventListener("scroll", this.updatePosition, true);
        window.addEventListener("resize", this.updatePosition);
      } else {
        this.detachReposition();
      }
    },
    close() {
      this.open = false;
      this.detachReposition();
    },
    detachReposition() {
      window.removeEventListener("scroll", this.updatePosition, true);
      window.removeEventListener("resize", this.updatePosition);
    },
    updatePosition() {
      const wrap = this.$refs.wrap;
      if (!wrap) return;
      const r = wrap.getBoundingClientRect();
      const vw = window.innerWidth;
      const vh = window.innerHeight;
      const width = Math.max(r.width, this.rich ? 420 : r.width);
      let left = r.left;
      if (left + width > vw - 8) left = Math.max(8, vw - width - 8);
      const panelH = this.$refs.panel ? this.$refs.panel.offsetHeight : 320;
      const spaceBelow = vh - r.bottom;
      const openUp = spaceBelow < panelH + 12 && r.top > spaceBelow;
      const top = openUp ? Math.max(8, r.top - panelH - 4) : r.bottom + 4;
      this.panelStyle = {
        position: "fixed",
        top: top + "px",
        left: left + "px",
        width: width + "px",
        right: "auto",
      };
    },
    pick(val) {
      this.$emit("update:modelValue", val);
      this.close();
      this.q = "";
    },
    pickFirst() {
      if (this.shown.length) this.pick(this.getVal(this.shown[0]));
    },
    onOutside(e) {
      const inWrap = this.$refs.wrap && this.$refs.wrap.contains(e.target);
      const inPanel = this.$refs.panel && this.$refs.panel.contains(e.target);
      if (!inWrap && !inPanel) this.close();
    },
  },
  mounted() {
    document.addEventListener("mousedown", this.onOutside);
  },
  beforeUnmount() {
    document.removeEventListener("mousedown", this.onOutside);
    this.detachReposition();
  },
};
