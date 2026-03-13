<template>
  <section class="table-surface rebalance-table">
    <div class="surface-header">
      <div class="surface-header__copy">
        <p class="section-label">Execution Log</p>
        <h2>调仓记录</h2>
        <p class="subtle-copy">用于复盘组合在各轮调仓中的动作变化，后续可继续扩展到成交与持仓明细。</p>
      </div>
      <div class="status-pills">
        <span class="status-pill">{{ rows.length }} Rows</span>
      </div>
    </div>

    <p v-if="rows.length === 0" class="empty-copy">暂无调仓记录</p>
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
  gap: var(--space-4);
  overflow: hidden;
  padding: var(--space-6);
}

.empty-copy {
  color: var(--text-muted);
  margin: 0;
}
</style>
