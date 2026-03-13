<template>
  <section class="surface-card recent-runs-panel">
    <div class="surface-header">
      <div class="surface-header__copy">
        <p class="section-label">Recent Backtests</p>
        <h2>最近回测</h2>
        <p class="subtle-copy">优先查看最近任务的收益表现和状态，快速决定是否继续迭代。</p>
      </div>
      <div class="status-pills">
        <span class="status-pill status-pill--active">{{ jobs.length }} Runs</span>
      </div>
    </div>

    <p v-if="jobs.length === 0" class="empty-copy">还没有回测记录</p>
    <ul v-else class="job-list">
      <li v-for="job in jobs" :key="job.id">
        <div class="job-list__meta">
          <strong>{{ job.status }}</strong>
          <span class="font-mono">{{ job.id }}</span>
        </div>
        <span class="job-list__value">{{ formatPercent(job.metrics.total_return) }}</span>
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
.recent-runs-panel {
  min-height: 100%;
}

.job-list {
  display: grid;
  gap: 0.75rem;
  margin: 0;
  padding: 0;
}

.job-list li {
  align-items: center;
  background: rgba(18, 32, 51, 0.03);
  border: 1px solid rgba(18, 32, 51, 0.06);
  border-radius: 1rem;
  display: flex;
  justify-content: space-between;
  list-style: none;
  padding: 0.95rem 1rem;
}

.job-list__meta {
  display: grid;
  gap: 0.2rem;
}

.job-list__meta strong {
  color: var(--text-primary);
}

.job-list__meta span {
  color: var(--text-muted);
  font-size: 0.76rem;
}

.job-list__value {
  color: var(--accent-signal-strong);
  font-family: var(--font-mono);
  font-size: 1rem;
  font-weight: 700;
}

.empty-copy {
  color: var(--text-muted);
  margin: 0;
}
</style>
