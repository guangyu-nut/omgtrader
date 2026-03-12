<template>
  <main class="page">
    <header class="page-header">
      <h1>数据中心</h1>
    </header>

    <p v-if="errorMessage" class="error">{{ errorMessage }}</p>

    <section class="grid">
      <DataSourceForm
        v-model:name="dataSourceName"
        v-model:provider-type="providerType"
        @submit="handleCreateDataSource"
      />
      <SyncTaskTable :rows="marketDataStore.syncTasks" />
    </section>

    <section class="panel">
      <h2>覆盖范围</h2>
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
.page {
  display: grid;
  gap: 1rem;
  padding: 2rem;
}

.page-header {
  display: grid;
  gap: 0.75rem;
}

.grid {
  display: grid;
  gap: 1rem;
  grid-template-columns: repeat(auto-fit, minmax(16rem, 1fr));
}

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

.error {
  color: #b42318;
}
</style>
