<template>
  <main class="page-shell workbench-view">
    <header class="page-header">
      <p class="eyebrow">Research Overview</p>
      <h1>研究总览</h1>
      <p class="page-intro">
        快速查看本地研究环境、最近回测和数据就绪状态，直接进入下一步工作区。
      </p>
    </header>

    <section class="panel-grid panel-grid--three">
      <article class="surface-card surface-card--muted summary-card">
        <p class="section-label">Environment</p>
        <strong>本地研究节点</strong>
        <span>单机模式已启用，策略、数据与回测结果全部保存在当前工作区。</span>
      </article>
      <article class="surface-card summary-card">
        <p class="section-label">Recent Activity</p>
        <strong>{{ backtestStore.recentJobs.length }} 次最近回测</strong>
        <span>从最近任务继续复盘，或切换到回测中心继续发起实验。</span>
      </article>
      <article class="surface-card summary-card summary-card--signal">
        <p class="section-label">Next Step</p>
        <strong>Python 策略工作台</strong>
        <span>策略中心已经切到 Python 资产管理模式，便于后续接入执行链路。</span>
      </article>
    </section>

    <section class="panel-grid panel-grid--two">
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
.workbench-view {
  padding: var(--space-3) 0 var(--space-7);
}

.summary-card {
  min-height: 10.5rem;
}

.summary-card strong {
  font-size: 1.15rem;
}

.summary-card span {
  color: var(--text-muted);
  font-size: var(--text-sm);
}

.summary-card--signal {
  background:
    linear-gradient(135deg, rgba(255, 141, 77, 0.12) 0%, rgba(251, 252, 255, 0.96) 48%),
    var(--bg-panel);
}
</style>
