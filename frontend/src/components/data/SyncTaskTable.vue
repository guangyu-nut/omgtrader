<template>
  <section class="table-surface sync-task-table">
    <div class="surface-header">
      <div class="surface-header__copy">
        <p class="section-label">Task Queue</p>
        <h2>同步任务</h2>
        <p class="subtle-copy">最近的数据拉取和更新会显示在这里，便于快速确认任务状态。</p>
      </div>
      <div class="status-pills">
        <span class="status-pill status-pill--active">{{ rows.length }} Tasks</span>
      </div>
    </div>

    <p v-if="rows.length === 0" class="empty-copy">暂无同步任务</p>
    <table v-else>
      <thead>
        <tr>
          <th>任务 ID</th>
          <th>状态</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="row in rows" :key="row.id">
          <td>{{ row.id }}</td>
          <td>{{ row.status }}</td>
        </tr>
      </tbody>
    </table>
  </section>
</template>

<script setup lang="ts">
import type { SyncTask } from "../../api/marketData";

defineProps<{
  rows: SyncTask[];
}>();
</script>

<style scoped>
.sync-task-table {
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
