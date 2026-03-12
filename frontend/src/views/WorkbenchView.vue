<template>
  <main class="page">
    <header class="page-header">
      <h1>工作台</h1>
      <nav class="nav">
        <button type="button" @click="goTo('/backtests')">回测中心</button>
        <button type="button" @click="goTo('/results/demo')">结果页</button>
      </nav>
    </header>

    <section class="grid">
      <RecentRunsPanel :jobs="backtestStore.recentJobs" />
      <DataStatusPanel last-updated="尚未同步" />
    </section>
  </main>
</template>

<script setup lang="ts">
import { onMounted } from "vue";

import { router } from "../router";
import RecentRunsPanel from "../components/workbench/RecentRunsPanel.vue";
import DataStatusPanel from "../components/workbench/DataStatusPanel.vue";
import { backtestStore } from "../stores/backtests";

onMounted(async () => {
  await backtestStore.loadRecentJobs();
});

async function goTo(path: string) {
  await router.push(path);
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

.nav {
  display: flex;
  gap: 1rem;
}

.nav button {
  background: none;
  border: none;
  color: #0f62fe;
  cursor: pointer;
  padding: 0;
}

.grid {
  display: grid;
  gap: 1rem;
  grid-template-columns: repeat(auto-fit, minmax(14rem, 1fr));
}
</style>
