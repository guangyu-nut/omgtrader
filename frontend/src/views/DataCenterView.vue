<template>
  <main class="page-shell data-center-view">
    <header class="page-header">
      <p class="eyebrow">Data Operations</p>
      <h1>数据运行面板</h1>
      <p class="page-intro">
        管理本地数据源、同步任务与行情覆盖范围，确认回测前的数据是否已经就绪。
      </p>
    </header>

    <p v-if="errorMessage" class="error">{{ errorMessage }}</p>

    <section class="panel-grid panel-grid--three">
      <article class="surface-card surface-card--muted data-summary-card">
        <p class="section-label">Sources</p>
        <strong>{{ marketDataStore.dataSources.length }} 个数据源</strong>
        <span>支持免费源与 Token 源双层接入，当前优先服务本地研究场景。</span>
      </article>
      <article class="surface-card data-summary-card">
        <p class="section-label">Tasks</p>
        <strong>{{ marketDataStore.syncTasks.length }} 条同步任务</strong>
        <span>同步队列用于追踪最近更新状态和失败信息，帮助定位数据缺口。</span>
      </article>
      <article class="surface-card data-summary-card">
        <p class="section-label">Coverage</p>
        <strong>{{ marketDataStore.coverages.length }} 个覆盖标的</strong>
        <span>覆盖范围区会显示最近更新时间，帮助你判断数据是否适合发起回测。</span>
      </article>
    </section>

    <section class="panel-grid panel-grid--two">
      <DataSourceForm
        v-model:name="dataSourceName"
        v-model:provider-type="providerType"
        @submit="handleCreateDataSource"
      />
      <SyncTaskTable :rows="marketDataStore.syncTasks" />
    </section>

    <section class="table-surface coverage-panel">
      <div class="surface-header coverage-panel__header">
        <div class="surface-header__copy">
          <p class="section-label">Coverage</p>
          <h2>覆盖范围</h2>
          <p class="subtle-copy">重点确认日线与分钟线的最近更新时间，避免研究基线漂移。</p>
        </div>
        <div class="status-pills">
          <span class="status-pill status-pill--active">A 股</span>
          <span class="status-pill">Minute Aware</span>
        </div>
      </div>

      <table>
        <thead>
          <tr>
            <th>标的</th>
            <th>最近更新时间</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="marketDataStore.coverages.length === 0">
            <td colspan="2">暂无覆盖数据</td>
          </tr>
          <tr v-for="row in marketDataStore.coverages" :key="row.symbol_code">
            <td>{{ row.symbol_code }}</td>
            <td>{{ row.minute_end ?? row.daily_end ?? "--" }}</td>
          </tr>
        </tbody>
      </table>
    </section>
  </main>
</template>

<script setup lang="ts">
import { onMounted, ref } from "vue";

import DataSourceForm from "../components/data/DataSourceForm.vue";
import SyncTaskTable from "../components/data/SyncTaskTable.vue";
import { marketDataStore } from "../stores/marketData";

const dataSourceName = ref("free-default");
const providerType = ref("free");
const errorMessage = ref("");

onMounted(async () => {
  try {
    await marketDataStore.loadCoverage();
    await marketDataStore.loadSyncTasks();
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : "加载数据中心失败";
  }
});

async function handleCreateDataSource() {
  errorMessage.value = "";

  try {
    await marketDataStore.createDataSource({
      enabled: true,
      name: dataSourceName.value,
      provider_type: providerType.value,
    });
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : "创建数据源失败";
  }
}
</script>

<style scoped>
.data-center-view {
  padding: var(--space-3) 0 var(--space-7);
}

.data-summary-card {
  min-height: 10.5rem;
}

.data-summary-card strong {
  font-size: 1.15rem;
}

.data-summary-card span {
  color: var(--text-muted);
  font-size: var(--text-sm);
}

.coverage-panel {
  display: grid;
  gap: var(--space-4);
  overflow: hidden;
  padding: var(--space-6);
}

.error {
  color: #b45309;
  margin: 0;
}
</style>
