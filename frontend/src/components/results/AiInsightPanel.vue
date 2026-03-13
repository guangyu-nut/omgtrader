<template>
  <section class="surface-card ai-insight-panel">
    <div class="surface-header">
      <div class="surface-header__copy">
        <p class="section-label">AI Analyst</p>
        <h2>策略总结</h2>
        <p class="subtle-copy">把本次回测结果压缩成更容易继续研究的摘要和风险提示。</p>
      </div>
      <div class="status-pills">
        <span class="status-pill status-pill--signal">AI</span>
      </div>
    </div>
    <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
    <template v-else-if="insight">
      <p class="ai-summary">{{ insight.summary }}</p>
      <ul class="risk-list">
        <li v-for="risk in insight.risks" :key="risk">{{ risk }}</li>
      </ul>
    </template>
    <p v-else class="subtle-copy">AI 正在生成解读...</p>
  </section>
</template>

<script setup lang="ts">
import { onMounted, ref } from "vue";

import { generateInsight, type AiInsight } from "../../api/ai";

const props = defineProps<{
  jobId: string;
}>();

const errorMessage = ref("");
const insight = ref<AiInsight | null>(null);

onMounted(async () => {
  try {
    insight.value = await generateInsight(props.jobId);
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : "生成 AI 解读失败";
  }
});
</script>

<style scoped>
.ai-insight-panel {
  display: grid;
  min-height: 100%;
}

.error {
  color: #b45309;
  margin: 0;
}

.ai-summary {
  color: var(--text-secondary);
  line-height: 1.7;
  margin: 0;
}

.risk-list {
  display: grid;
  gap: 0.7rem;
  margin: 0;
  padding-left: 1.1rem;
}

.risk-list li {
  color: var(--text-secondary);
}
</style>
