<template>
  <main class="page-shell results-view">
    <header class="page-header results-header">
      <p class="eyebrow">Analysis Overview</p>
      <h1>分析总览</h1>
      <p class="page-intro">围绕单次回测任务快速查看收益、风险、曲线摘要和 AI 辅助结论。</p>
      <div class="status-pills">
        <span class="status-pill status-pill--active">Job {{ route.params.jobId }}</span>
        <span v-if="result" class="status-pill">{{ curveSummary }}</span>
      </div>
      <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
    </header>

    <MetricsCards v-if="result" :metrics="result.metrics" />

    <section v-if="result" class="results-main-grid">
      <section class="terminal-surface curve-card">
        <div class="surface-header">
          <div class="surface-header__copy">
            <p class="section-label curve-card__eyebrow">Equity Curve</p>
            <h2>收益曲线</h2>
            <p class="subtle-copy curve-card__intro">当前版本先展示曲线摘要和配置预览，后续可平滑替换为完整图表画布。</p>
          </div>
          <div class="status-pills">
            <span class="status-pill status-pill--signal">Curve</span>
          </div>
        </div>
        <pre class="curve-preview">{{ JSON.stringify(curveOptions, null, 2) }}</pre>
      </section>

      <AiInsightPanel :job-id="String(route.params.jobId)" />
    </section>

    <RebalanceTable v-if="result" :rows="result.rebalances" />
  </main>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from "vue";
import { useRoute } from "vue-router";

import { buildEquityCurveOptions } from "../charts/equityCurveOptions";
import { getBacktestResult, type BacktestResult } from "../api/results";
import AiInsightPanel from "../components/results/AiInsightPanel.vue";
import MetricsCards from "../components/results/MetricsCards.vue";
import RebalanceTable from "../components/results/RebalanceTable.vue";

const route = useRoute();
const errorMessage = ref("");
const result = ref<BacktestResult | null>(null);
const curveOptions = computed(() => buildEquityCurveOptions(result.value?.equity_curve ?? []));
const curveSummary = computed(() => `曲线点数：${curveOptions.value.series[0].data.length}`);

onMounted(async () => {
  errorMessage.value = "";

  try {
    result.value = await getBacktestResult(String(route.params.jobId));
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : "加载回测结果失败";
  }
});
</script>

<style scoped>
.results-view {
  display: grid;
  gap: var(--space-5);
  padding: var(--space-3) 0 var(--space-7);
}

.results-header {
  align-items: start;
}

.curve-card {
  display: grid;
  gap: var(--space-4);
}

.curve-preview {
  background: rgba(7, 13, 22, 0.72);
  border: 1px solid rgba(123, 176, 255, 0.14);
  border-radius: 1rem;
  color: var(--text-on-dark);
  font-family: var(--font-mono);
  margin: 0;
  overflow: auto;
  padding: 1rem;
}

.curve-card__eyebrow,
.curve-card__intro {
  color: var(--text-on-dark-muted);
}

.results-main-grid {
  display: grid;
  gap: var(--space-5);
  grid-template-columns: minmax(0, 1.45fr) minmax(18rem, 0.85fr);
}

.error {
  color: #b45309;
  margin: 0;
}

@media (max-width: 1100px) {
  .results-main-grid {
    grid-template-columns: 1fr;
  }
}
</style>
