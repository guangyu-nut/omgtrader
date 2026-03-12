<template>
  <section class="metrics-grid">
    <article class="metric-card">
      <h2>累计收益</h2>
      <p>{{ formatPercent(metrics.total_return) }}</p>
    </article>
    <article class="metric-card">
      <h2>最大回撤</h2>
      <p>{{ formatPercent(metrics.max_drawdown) }}</p>
    </article>
  </section>
</template>

<script setup lang="ts">
const props = defineProps<{
  metrics: {
    total_return: number | null;
    max_drawdown: number | null;
  };
}>();

function formatPercent(value: number | null) {
  if (value === null) {
    return "--";
  }

  return `${(value * 100).toFixed(2)}%`;
}
</script>

<style scoped>
.metrics-grid {
  display: grid;
  gap: 1rem;
  grid-template-columns: repeat(auto-fit, minmax(10rem, 1fr));
}

.metric-card {
  border: 1px solid #d0d5dd;
  border-radius: 0.75rem;
  padding: 1rem;
}

.metric-card h2 {
  font-size: 1rem;
  margin: 0 0 0.5rem;
}

.metric-card p {
  font-size: 1.1rem;
  margin: 0;
}
</style>
