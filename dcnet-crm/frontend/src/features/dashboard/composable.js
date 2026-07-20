import { computed, ref } from "vue/dist/vue.esm-bundler.js";
import { call } from "../../utils.js";

export function useDashboard(ctx) {
  const dashboard = ref({
    kpis: { leads: 0, opportunities: 0, customers: 0, orders: 0, order_value: 0 },
    funnel: [],
  });

  const funnelTotal = computed(() => dashboard.value.funnel.reduce(
    (total, stage) => total + Number(stage.count || 0),
    0,
  ));
  const funnelValue = computed(() => dashboard.value.funnel.reduce(
    (total, stage) => total + Number(stage.amount || 0),
    0,
  ));
  const funnelMax = computed(() => Math.max(
    ...dashboard.value.funnel.map((stage) => Number(stage.count || 0)),
    1,
  ));
  const funnelColors = ["#79a7e8", "#b5df66", "#f4c976", "#76cdb8", "#a994db", "#ef9b8f"];
  const funnelDonutStyle = computed(() => {
    if (!funnelTotal.value) return { background: "#edf0f2" };
    let cursor = 0;
    const segments = dashboard.value.funnel.slice(0, 6).map((stage, index) => {
      const start = cursor;
      cursor += (Number(stage.count || 0) / funnelTotal.value) * 100;
      return `${funnelColors[index]} ${start}% ${cursor}%`;
    });
    if (cursor < 100) segments.push(`#edf0f2 ${cursor}% 100%`);
    return { background: `conic-gradient(from -90deg, ${segments.join(", ")})` };
  });

  function funnelWidth(count) {
    return `${Math.max((Number(count || 0) / funnelMax.value) * 100, 4)}%`;
  }

  function funnelColor(index) {
    return funnelColors[index % funnelColors.length];
  }

  async function loadDashboard() {
    ctx.loading.value = true;
    try {
      const data = await call("get_dashboard");
      dashboard.value = {
        kpis: { ...dashboard.value.kpis, ...(data?.kpis || {}) },
        funnel: Array.isArray(data?.funnel) ? data.funnel : [],
      };
    }
    finally { ctx.loading.value = false; }
  }

  return { dashboard, funnelTotal, funnelValue, funnelDonutStyle, funnelWidth, funnelColor, loadDashboard };
}
