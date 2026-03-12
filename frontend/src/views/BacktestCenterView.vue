<template>
  <main class="page">
    <header class="page-header">
      <h1>回测中心</h1>
      <nav class="nav">
        <button type="button" @click="goTo('/workbench')">工作台</button>
        <button type="button" @click="goTo('/results/demo')">结果页</button>
      </nav>
    </header>

    <p v-if="errorMessage" class="error">{{ errorMessage }}</p>

    <section class="grid">
      <BacktestLaunchCard v-model:strategy-instance-id="strategyInstanceId" @launch="handleLaunch" />
      <BacktestJobTable :jobs="backtestStore.recentJobs" />
    </section>
  </main>
</template>

<script setup lang="ts">
import { onMounted, ref } from "vue";

import { router } from "../router";
import BacktestJobTable from "../components/backtests/BacktestJobTable.vue";
import BacktestLaunchCard from "../components/backtests/BacktestLaunchCard.vue";
import { backtestStore } from "../stores/backtests";

const errorMessage = ref("");
const strategyInstanceId = ref("");

onMounted(async () => {
  await backtestStore.loadRecentJobs();
});

async function goTo(path: string) {
  await router.push(path);
}

async function handleLaunch() {
  errorMessage.value = "";

  if (!strategyInstanceId.value) {
    errorMessage.value = "请先输入策略实例 ID";
    return;
  }

  try {
    const job = await backtestStore.runJob({ strategyInstanceId: strategyInstanceId.value });
    await router.push(`/results/${job.id}`);
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : "启动回测失败";
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
  grid-template-columns: repeat(auto-fit, minmax(16rem, 1fr));
}

.error {
  color: #b42318;
}
</style>
