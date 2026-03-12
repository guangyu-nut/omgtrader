<template>
  <main class="results-view">
    <header class="results-header">
      <h1>回测结果</h1>
      <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
    </header>

    <MetricsCards v-if="result" :metrics="result.metrics" />

    <section v-if="result" class="curve-card">
      <h2>收益曲线</h2>
      <p>{{ curveSummary }}</p>
      <pre class="curve-preview">{{ JSON.stringify(curveOptions, null, 2) }}</pre>
    </section>

    <RebalanceTable v-if="result" :rows="result.rebalances" />
    <AiInsightPanel v-if="result" :job-id="String(route.params.jobId)" />
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
  gap: 1rem;
  padding: 2rem;
}

.results-header {
  display: grid;
  gap: 0.5rem;
}

.curve-card {
  border: 1px solid #d0d5dd;
  border-radius: 0.75rem;
  display: grid;
  gap: 0.75rem;
  padding: 1rem;
}

.curve-preview {
  background: #f8fafc;
  border-radius: 0.5rem;
  margin: 0;
  overflow: auto;
  padding: 0.75rem;
}

.error {
  color: #b42318;
}
</style>
