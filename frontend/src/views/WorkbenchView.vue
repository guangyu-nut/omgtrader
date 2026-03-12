<template>
  <main class="page">
    <header class="page-header">
      <h1>工作台</h1>
    </header>

    <section class="grid">
      <RecentRunsPanel :jobs="backtestStore.recentJobs" />
      <DataStatusPanel last-updated="尚未同步" />
    </section>
  </main>
</template>

<script setup lang="ts">
import { onMounted } from "vue";

import RecentRunsPanel from "../components/workbench/RecentRunsPanel.vue";
import DataStatusPanel from "../components/workbench/DataStatusPanel.vue";
import { backtestStore } from "../stores/backtests";

onMounted(async () => {
  await backtestStore.loadRecentJobs();
});
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
  grid-template-columns: repeat(auto-fit, minmax(14rem, 1fr));
}
</style>
