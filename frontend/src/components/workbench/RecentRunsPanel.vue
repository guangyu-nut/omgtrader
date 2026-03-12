<template>
  <section class="panel">
    <h2>最近回测</h2>
    <p v-if="jobs.length === 0">还没有回测记录</p>
    <ul v-else class="job-list">
      <li v-for="job in jobs" :key="job.id">
        <strong>{{ job.status }}</strong>
        <span>{{ formatPercent(job.metrics.total_return) }}</span>
      </li>
    </ul>
  </section>
</template>

<script setup lang="ts">
import type { BacktestJobSummary } from "../../api/backtests";

defineProps<{
  jobs: BacktestJobSummary[];
}>();

function formatPercent(value: number | null) {
  if (value === null) {
    return "--";
  }

  return `${(value * 100).toFixed(2)}%`;
}
</script>

<style scoped>
.panel {
  border: 1px solid #d0d5dd;
  border-radius: 0.75rem;
  display: grid;
  gap: 0.75rem;
  padding: 1rem;
}

.job-list {
  display: grid;
  gap: 0.5rem;
  margin: 0;
  padding: 0;
}

.job-list li {
  display: flex;
  justify-content: space-between;
  list-style: none;
}
</style>
