/**
 * One row of the Company → Chi nhánh → Phòng ban tree used by the "Đơn vị"
 * picker (Dự kiến chi dialog). Recurses into itself for child nodes; the
 * actual lazy-loading of children happens in the parent composable via the
 * "toggle" event, which mutates `node` in place (kept reactive by the caller).
 */
export const OrgUnitNode = {
  name: "OrgUnitNode",
  props: {
    node: { type: Object, required: true },
    depth: { type: Number, default: 0 },
    selectedValue: { type: String, default: "" },
  },
  emits: ["toggle", "select"],
  template: `
    <div class="org-node">
      <div class="org-node-row" :style="{ paddingLeft: (depth * 18) + 'px' }">
        <button v-if="node.expandable" type="button" class="org-node-toggle" @click="$emit('toggle', node)">{{ node.expanded ? '−' : '+' }}</button>
        <span v-else class="org-node-toggle org-node-toggle-spacer"></span>
        <span
          class="org-node-label"
          :class="{ selectable: node.selectable, selected: node.selectable && node.value === selectedValue }"
          @click="node.selectable && $emit('select', node)"
        >{{ node.title }}</span>
        <span v-if="node.loading" class="org-node-loading">Đang tải...</span>
      </div>
      <div v-if="node.expanded" class="org-node-children">
        <OrgUnitNode
          v-for="child in node.children"
          :key="child.value"
          :node="child"
          :depth="depth + 1"
          :selected-value="selectedValue"
          @toggle="$emit('toggle', $event)"
          @select="$emit('select', $event)"
        />
        <p v-if="node.loaded && !node.children.length" class="org-node-empty" :style="{ paddingLeft: ((depth + 1) * 18 + 20) + 'px' }">Không có đơn vị con</p>
      </div>
    </div>
  `,
};
