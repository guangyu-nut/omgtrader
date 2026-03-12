<template>
  <main class="page">
    <header class="page-header">
      <h1>回测中心</h1>
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

function getLastStrategyId() {
  if (typeof window === "undefined") {
    return "";
  }

  const storage = window.localStorage;
  return storage && typeof storage.getItem === "function" ? (storage.getItem("lastStrategyId") ?? "") : "";
}

const errorMessage = ref("");
const strategyInstanceId = ref(getLastStrategyId());

onMounted(async () => {
  await backtestStore.loadRecentJobs();
});

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

.grid {
  display: grid;
  gap: 1rem;
  grid-template-columns: repeat(auto-fit, minmax(16rem, 1fr));
}

.error {
  color: #b42318;
}
</style>
