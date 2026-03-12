<template>
  <section class="panel">
    <h2>回测任务</h2>
    <p v-if="jobs.length === 0">暂无任务</p>
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
.panel {
  border: 1px solid #d0d5dd;
  border-radius: 0.75rem;
  display: grid;
  gap: 0.75rem;
  padding: 1rem;
}

table {
  border-collapse: collapse;
  width: 100%;
}

th,
td {
  border-bottom: 1px solid #d0d5dd;
  padding: 0.5rem;
  text-align: left;
}
</style>
