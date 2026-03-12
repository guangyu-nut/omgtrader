<template>
  <section class="panel">
    <h2>同步任务</h2>
    <p v-if="rows.length === 0">暂无同步任务</p>
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
