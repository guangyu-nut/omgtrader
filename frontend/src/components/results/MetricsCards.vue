<template>
  <section class="metrics-grid">
    <article class="metric-card">
      <p class="section-label">Performance</p>
      <h2>累计收益</h2>
      <p>{{ formatPercent(metrics.total_return) }}</p>
    </article>
    <article class="metric-card">
      <p class="section-label">Risk</p>
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
  gap: var(--space-4);
  grid-template-columns: repeat(auto-fit, minmax(10rem, 1fr));
}

.metric-card {
  background:
    linear-gradient(135deg, rgba(255, 255, 255, 0.72) 0%, rgba(233, 239, 247, 0.94) 100%);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-panel);
  box-shadow: var(--shadow-panel);
  padding: var(--space-5);
}

.metric-card h2 {
  font-size: 1rem;
  margin: 0 0 0.35rem;
}

.metric-card p {
  margin: 0;
}

.metric-card > p:last-child {
  color: var(--accent-signal-strong);
  font-family: var(--font-mono);
  font-size: 1.45rem;
  font-weight: 700;
}
</style>
