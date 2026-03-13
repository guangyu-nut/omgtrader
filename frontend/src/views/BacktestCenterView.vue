<template>
  <main class="page-shell backtest-center-view">
    <header class="page-header">
      <p class="eyebrow">Launch Desk</p>
      <h1>任务发射台</h1>
      <p class="page-intro">
        当前仍沿用旧回测链路，通过策略实例 ID 发起任务，同时把历史队列整理成更清晰的研究操作台。
      </p>
    </header>

    <p v-if="errorMessage" class="error">{{ errorMessage }}</p>

    <section class="panel-grid panel-grid--three">
      <article class="surface-card surface-card--muted launch-summary-card">
        <p class="section-label">Engine</p>
        <strong>Legacy Backtest Flow</strong>
        <span>本轮只重做页面呈现，不调整旧回测 API 与调度语义。</span>
      </article>
      <article class="surface-card launch-summary-card">
        <p class="section-label">Queue</p>
        <strong>{{ backtestStore.recentJobs.length }} 条任务记录</strong>
        <span>结果页依旧按任务上下文进入，适合继续沿用当前回测闭环。</span>
      </article>
      <article class="surface-card launch-summary-card launch-summary-card--signal">
        <p class="section-label">Launch Input</p>
        <strong>{{ strategyInstanceId || "--" }}</strong>
        <span>当前入口仍使用策略实例 ID，后续可在不破坏视觉层的前提下接 Python 执行。</span>
      </article>
    </section>

    <section class="panel-grid panel-grid--two">
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
.backtest-center-view {
  padding: var(--space-3) 0 var(--space-7);
}

.error {
  color: #b45309;
  margin: 0;
}

.launch-summary-card {
  min-height: 10.5rem;
}

.launch-summary-card strong {
  font-size: 1.15rem;
}

.launch-summary-card span {
  color: var(--text-muted);
  font-size: var(--text-sm);
}

.launch-summary-card--signal {
  background:
    linear-gradient(135deg, rgba(123, 176, 255, 0.16) 0%, rgba(251, 252, 255, 0.96) 55%),
    var(--bg-panel);
}
</style>
