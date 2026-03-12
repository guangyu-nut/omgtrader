<template>
  <section class="rebalance-table">
    <h2>调仓记录</h2>
    <p v-if="rows.length === 0">暂无调仓记录</p>
    <table v-else>
      <thead>
        <tr>
          <th>股票</th>
          <th>动作</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="row in rows" :key="`${row.symbol}-${row.action}`">
          <td>{{ row.symbol }}</td>
          <td>{{ row.action }}</td>
        </tr>
      </tbody>
    </table>
  </section>
</template>

<script setup lang="ts">
import type { RebalanceRow } from "../../api/results";

defineProps<{
  rows: RebalanceRow[];
}>();
</script>

<style scoped>
.rebalance-table {
  display: grid;
  gap: 0.75rem;
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
