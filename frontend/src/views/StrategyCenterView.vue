<template>
  <main class="page">
    <header class="page-header">
      <h1>策略中心</h1>
    </header>

    <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
    <p v-if="successMessage" class="success">{{ successMessage }}</p>

    <section class="grid">
      <StockPoolEditor
        v-model:name="stockPoolName"
        v-model:symbols-text="symbolsText"
        @submit="handleCreateStockPool"
      />
      <StrategyForm v-model:hold-count="holdCount" v-model:name="strategyName" @submit="handleCreateStrategy" />
    </section>

    <section class="panel">
      <h2>最近策略</h2>
      <p>{{ strategyStore.latestStrategyId || "暂无策略" }}</p>
    </section>
  </main>
</template>

<script setup lang="ts">
import { ref } from "vue";

import StockPoolEditor from "../components/strategies/StockPoolEditor.vue";
import StrategyForm from "../components/strategies/StrategyForm.vue";
import { strategyStore } from "../stores/strategies";

const errorMessage = ref("");
const holdCount = ref(2);
const stockPoolName = ref("CSI300 manual");
const strategyName = ref("Top N demo");
const successMessage = ref("");
const symbolsText = ref("000001.SZ\n600000.SH\n000002.SZ");

async function handleCreateStockPool() {
  errorMessage.value = "";
  successMessage.value = "";

  try {
    const stockPool = await strategyStore.createStockPool({
      name: stockPoolName.value,
      symbols: symbolsText.value
        .split(/\s+/)
        .map((symbol) => symbol.trim())
        .filter(Boolean),
    });
    successMessage.value = `股票池已创建：${stockPool.id}`;
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : "创建股票池失败";
  }
}

async function handleCreateStrategy() {
  errorMessage.value = "";
  successMessage.value = "";

  try {
    const strategy = await strategyStore.createStrategy({
      benchmark_symbol: "000300.SH",
      commission_bps: 5,
      hold_count: holdCount.value,
      name: strategyName.value,
      slippage_bps: 15,
    });
    successMessage.value = `策略已创建：${strategy.id}`;
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : "创建策略失败";
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

.error {
  color: #b42318;
}

.success {
  color: #027a48;
}
</style>
