<template>
  <section class="table-surface backtest-job-table">
    <div class="surface-header">
      <div class="surface-header__copy">
        <p class="section-label">Task Queue</p>
        <h2>回测任务</h2>
        <p class="subtle-copy">所有已发起的回测任务会在这里排队展示，方便你回到结果页继续分析。</p>
      </div>
      <div class="status-pills">
        <span class="status-pill status-pill--active">{{ jobs.length }} Jobs</span>
      </div>
    </div>

    <p v-if="jobs.length === 0" class="empty-copy">暂无任务</p>
    <table v-else>
      <thead>
        <tr>
          <th>任务 ID</th>
          <th>状态</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="job in jobs" :key="job.id">
          <td>{{ job.id }}</td>
          <td>{{ job.status }}</td>
        </tr>
      </tbody>
    </table>
  </section>
</template>

<script setup lang="ts">
import type { BacktestJobSummary } from "../../api/backtests";

defineProps<{
  jobs: BacktestJobSummary[];
}>();
</script>

<style scoped>
.backtest-job-table {
  display: grid;
  gap: var(--space-4);
  overflow: hidden;
  padding: var(--space-6);
}

.empty-copy {
  color: var(--text-muted);
  margin: 0;
}
</style>
